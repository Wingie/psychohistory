"""Sparse pairwise block-coupling fit with a per-substrate fitted null.

Method: a pairwise (Ising for two states, Potts for more) energy over the blocks
of an activity matrix, fitted by pseudolikelihood (Besag 1975, "Statistical
analysis of non-lattice data", The Statistician 24:179-195) with an L1 penalty
on the couplings, solved by accelerated proximal gradient (FISTA with
backtracking, Beck and Teboulle 2009). The recipe follows the training loop of
CRAM (Hoover, Blayney and Whittington, arXiv 2611.17309, Apache-2.0); this file
is a clean CPU-only numpy rewrite and contains none of their code.

Input: an integer state matrix S with rows = time windows and columns = blocks
(Louvain communities, subreddits, ...), values in 0..q-1. Use `discretize` to
turn a count matrix into states.

Outputs are plain dicts and numpy arrays. Nothing here writes files.

    fit = fit_couplings(S)                      # J, h, objective
    null = fitted_null(S, k=50, seed=0)         # coupling mass on shuffled copies
    out = readout(S, labels=names, k=50)        # sparsity, top pairs, obs/null ratio
"""
import numpy as np

DEFAULT_LAM_SCALE = 1.0
FIELD_RIDGE = 1e-3
ZERO_TOL = 1e-8


def as_states(S, q=None):
    """Check S and return (int array, q). Raises TypeError / ValueError on bad input."""
    S = np.asarray(S)
    if S.ndim != 2:
        raise ValueError(f"state matrix must be 2-D (time x blocks), got ndim={S.ndim}")
    if S.dtype == bool:
        S = S.astype(np.int64)
    if not np.issubdtype(S.dtype, np.integer):
        raise TypeError(f"state matrix must hold integers, got dtype {S.dtype}; "
                        "use discretize() on counts first")
    T, K = S.shape
    if K < 2:
        raise ValueError(f"need at least 2 blocks (columns), got {K}")
    if T < 4:
        raise ValueError(f"need at least 4 time windows (rows), got {T}")
    if S.min() < 0:
        raise ValueError("states must be non-negative")
    q_data = int(S.max()) + 1
    if q is None:
        q = max(2, q_data)
    elif q_data > q:
        raise ValueError(f"state value {q_data - 1} out of range for q={q}")
    if q < 2:
        raise ValueError(f"q must be at least 2, got {q}")
    return S.astype(np.int64), int(q)


def discretize(M, q=2, method="diff"):
    """Counts (time x blocks) to integer states.

    method="diff": the per-block change of log1p(count) between consecutive rows,
    so a shared trend does not register as coupling; the output has one row fewer.
    method="level": the counts as they are.
    q=2 maps a value to 1 when it is above the block's median (for "diff", above 0).
    q>2 bins each block by its own quantiles into q levels.
    """
    M = np.asarray(M, dtype=float)
    if M.ndim != 2:
        raise ValueError(f"count matrix must be 2-D (time x blocks), got ndim={M.ndim}")
    if not np.all(np.isfinite(M)):
        raise ValueError("count matrix holds NaN or inf")
    if method == "diff":
        V = np.diff(np.log1p(np.clip(M, 0, None)), axis=0)
        centre = np.zeros(V.shape[1])
    elif method == "level":
        V = M
        centre = np.median(V, axis=0)
    else:
        raise ValueError(f"unknown method {method!r}; use 'diff' or 'level'")
    if q == 2:
        return (V > centre).astype(np.int64)
    if q < 2:
        raise ValueError(f"q must be at least 2, got {q}")
    S = np.zeros(V.shape, dtype=np.int64)
    for k in range(V.shape[1]):
        cuts = np.quantile(V[:, k], np.arange(1, q) / q)
        S[:, k] = np.searchsorted(cuts, V[:, k], side="right")
    return S


def _onehot(S, q):
    T, K = S.shape
    X = np.zeros((T, K * q))
    X[np.repeat(np.arange(T), K), (np.arange(K) * q + S).ravel()] = 1.0
    return X


class _Model:
    """Parameter vector theta = [fields | upper-triangle couplings]."""

    def __init__(self, S, q):
        self.S, self.q = S, q
        self.T, self.K = S.shape
        self.iu = np.triu_indices(self.K, k=1)
        self.n_pairs = len(self.iu[0])
        if q == 2:
            self.X = 2.0 * S - 1.0
            self.n_h = self.K
            self.pair_size = 1
        else:
            self.X = _onehot(S, q)
            self.n_h = self.K * q
            self.pair_size = q * q
        self.n_theta = self.n_h + self.n_pairs * self.pair_size

    def unpack(self, theta):
        h = theta[:self.n_h]
        Jp = theta[self.n_h:]
        K, q = self.K, self.q
        if q == 2:
            J = np.zeros((K, K))
            J[self.iu] = Jp
            return h, J + J.T
        J4 = np.zeros((K, K, q, q))
        J4[self.iu[0], self.iu[1]] = Jp.reshape(self.n_pairs, q, q)
        J4 = J4 + J4.transpose(1, 0, 3, 2)
        return h.reshape(K, q), J4

    def _flat(self, J4):
        K, q = self.K, self.q
        return J4.transpose(0, 2, 1, 3).reshape(K * q, K * q)

    def loss_grad(self, theta):
        h, J = self.unpack(theta)
        T, K, q = self.T, self.K, self.q
        if q == 2:
            U = h + self.X @ J
            m = -2.0 * self.X * U
            loss = np.logaddexp(0.0, m).sum() / T
            G = (-2.0 * self.X / (1.0 + np.exp(-m))) / T
            gh = G.sum(axis=0)
            GJ = G.T @ self.X
            gJ = (GJ + GJ.T)[self.iu]
        else:
            Z = (h.ravel() + self.X @ self._flat(J)).reshape(T, K, q)
            zmax = Z.max(axis=2, keepdims=True)
            lse = zmax[..., 0] + np.log(np.exp(Z - zmax).sum(axis=2))
            Xr = self.X.reshape(T, K, q)
            loss = (lse - (Z * Xr).sum(axis=2)).sum() / T
            P = np.exp(Z - lse[..., None])
            D = ((P - Xr) / T).reshape(T, K * q)
            gh = D.sum(axis=0)
            GJ = D.T @ self.X
            G4 = (GJ + GJ.T).reshape(K, q, K, q).transpose(0, 2, 1, 3)
            gJ = G4[self.iu[0], self.iu[1]].reshape(-1)
        hv = theta[:self.n_h]
        loss += 0.5 * FIELD_RIDGE * float(hv @ hv)
        gh = gh + FIELD_RIDGE * hv
        return float(loss), np.concatenate([gh, gJ])


def default_lam(T, K):
    """L1 weight scaled as sqrt(log K / T), the usual rate for sparse pairwise fits."""
    return DEFAULT_LAM_SCALE * float(np.sqrt(np.log(max(K, 2)) / T))


def _prox(theta, n_h, t):
    out = theta.copy()
    c = out[n_h:]
    out[n_h:] = np.sign(c) * np.maximum(np.abs(c) - t, 0.0)
    return out


def _fista(model, lam, max_iter, tol):
    n_h = model.n_h
    x = np.zeros(model.n_theta)
    y = x.copy()
    t = 1.0
    L = 1.0
    converged = False
    it = 0
    for it in range(1, max_iter + 1):
        fy, gy = model.loss_grad(y)
        while True:
            z = _prox(y - gy / L, n_h, lam / L)
            fz, _ = model.loss_grad(z)
            d = z - y
            if fz <= fy + float(gy @ d) + 0.5 * L * float(d @ d) + 1e-12:
                break
            L *= 2.0
        step = float(np.linalg.norm(z - x))
        t_new = 0.5 * (1.0 + np.sqrt(1.0 + 4.0 * t * t))
        y = z + ((t - 1.0) / t_new) * (z - x)
        x, t = z, t_new
        if step <= tol * max(1.0, float(np.linalg.norm(x))):
            converged = True
            break
        L = max(L / 1.5, 1e-6)
    return x, it, converged


def _gauge_double_centre(J4):
    """Zero-sum gauge of each q x q coupling block (removes what the fields can absorb)."""
    return (J4 - J4.mean(axis=2, keepdims=True) - J4.mean(axis=3, keepdims=True)
            + J4.mean(axis=(2, 3), keepdims=True))


def fit_couplings(S, q=None, lam=None, max_iter=3000, tol=1e-7):
    """Fit fields h and a sparse symmetric coupling J by L1 pseudolikelihood.

    Returns a dict:
      J          (K, K) signed couplings for q=2; for q>2 the (K, K, q, q) tensor
      strength   (K, K) per-pair coupling size: |J| for q=2, Frobenius norm of the
                 zero-sum-gauged block for q>2
      h          fields, (K,) or (K, q)
      mass       sum over pairs i<j of strength
      nlpl       mean negative log pseudolikelihood per row at the fit
      nlpl_fields_only  the same with J = 0 (fields refit alone)
      lam, q, n_iter, converged
    Deterministic: there is no randomness in the fit.
    """
    S, q = as_states(S, q)
    T, K = S.shape
    lam = default_lam(T, K) if lam is None else float(lam)
    if lam < 0:
        raise ValueError("lam must be non-negative")
    model = _Model(S, q)
    theta, n_iter, converged = _fista(model, lam, max_iter, tol)
    h, J = model.unpack(theta)
    if q == 2:
        strength = np.abs(J)
    else:
        strength = np.sqrt((_gauge_double_centre(J) ** 2).sum(axis=(2, 3)))
    strength[strength < ZERO_TOL] = 0.0
    iu = np.triu_indices(K, k=1)
    nlpl, _ = model.loss_grad(theta)
    theta0, _, _ = _fista(model, 1e12, max_iter, tol)
    nlpl0, _ = model.loss_grad(theta0)
    return dict(J=J, strength=strength, h=h, mass=float(strength[iu].sum()),
                nlpl=nlpl, nlpl_fields_only=nlpl0, lam=lam, q=q,
                n_iter=int(n_iter), converged=bool(converged))


def shuffle_columns(S, rng):
    """Permute each block's time order independently: every block keeps its exact
    marginal, and cross-block co-occurrence is broken."""
    S = np.asarray(S)
    out = np.empty_like(S)
    for k in range(S.shape[1]):
        out[:, k] = S[rng.permutation(S.shape[0]), k]
    return out


def fitted_null(S, k=50, seed=0, q=None, lam=None, max_iter=3000, tol=1e-7):
    """Refit on k marginal-preserving shuffles; returns the null coupling masses."""
    S, q = as_states(S, q)
    if k < 1:
        raise ValueError("k must be at least 1")
    T, K = S.shape
    lam = default_lam(T, K) if lam is None else float(lam)
    rng = np.random.default_rng(seed)
    masses = np.array([fit_couplings(shuffle_columns(S, rng), q=q, lam=lam,
                                     max_iter=max_iter, tol=tol)["mass"]
                       for _ in range(k)])
    return dict(masses=masses, mean=float(masses.mean()), sd=float(masses.std()),
                p90=float(np.percentile(masses, 90)), k=int(k), seed=int(seed), lam=lam)


def readout(S, labels=None, k=50, seed=0, q=None, lam=None, top=10):
    """Fit, fitted null and summary numbers for one substrate. Returns a JSON-ready dict."""
    S, q = as_states(S, q)
    T, K = S.shape
    if labels is None:
        labels = [str(i) for i in range(K)]
    labels = [str(x) for x in labels]
    if len(labels) != K:
        raise ValueError(f"{len(labels)} labels for {K} blocks")
    lam = default_lam(T, K) if lam is None else float(lam)
    fit = fit_couplings(S, q=q, lam=lam)
    null = fitted_null(S, k=k, seed=seed, q=q, lam=lam)
    iu = np.triu_indices(K, k=1)
    st = fit["strength"][iu]
    nnz = int((st > 0).sum())
    order = np.argsort(-st, kind="stable")[:top]
    pairs = []
    for o in order:
        if st[o] <= 0:
            break
        i, j = int(iu[0][o]), int(iu[1][o])
        pairs.append(dict(a=labels[i], b=labels[j], strength=float(st[o]),
                          J=float(fit["J"][i, j]) if q == 2 else None))
    mass = fit["mass"]
    ratio = (mass / null["mean"]) if null["mean"] > 0 else None
    return dict(
        n_windows=int(T), n_blocks=int(K), q=int(q), lam=float(lam),
        n_pairs=int(len(st)), nnz_pairs=nnz,
        sparsity=float(1.0 - nnz / len(st)),
        coupling_mass=float(mass),
        null_mass_mean=null["mean"], null_mass_sd=null["sd"], null_mass_p90=null["p90"],
        obs_over_null_mass=(float(ratio) if ratio is not None else None),
        null_pctile_of_obs=float(np.mean(null["masses"] < mass)),
        null_k=null["k"], null_seed=null["seed"],
        nlpl=fit["nlpl"], nlpl_fields_only=fit["nlpl_fields_only"],
        fit_converged=fit["converged"], fit_iters=fit["n_iter"],
        top_couplings=pairs,
    )
