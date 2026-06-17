"""Psychohistory engine: verified numerical primitives for the bounded-psychohistory skill.

This module is the importable, side-effect-free port of the verified sim file
``sims_v2.py``. It contains NO plotting, NO file writes, and NO global RNG state
that other modules can trip over. The math is reproduced *exactly* from the
verified file so that the numbers cited in the reference modules remain valid.

Verified behaviors of this engine (internal consistency only -- never cite as
empirical validation of society):

  E1  stock-flow total-attention drift = 0 (conserved).
  E2  graph master equation mass error ~3.3e-16; belief drift concentrates a node
      share 0.025 -> 0.221 without creating mass.
  E3  std(population mean) ~ K^-1/2 over blocks (single-seed slope -0.63 is
      estimator noise; over 20 seeds -0.47 +/- 0.13, consistent with -0.5).
  E4  well-synchrony S goes 0.05 -> 1.00 with transition near coupling W ~ 0.4.
      Pearson-correlation N_eff only falls 64 -> 29.5 (MISLEADING); the macro
      variance-ratio N_eff collapses 61 -> 1.0 (CORRECT).
  E5  reaction map: no-guarantee fixed point ~0.995, deposit-guarantee ~0; a
      bistable 3-fixed-point regime appears at nearby parameters (the
      imitative/run regime).

Layer map (see reference/):
  L1  systems_stockflow   (lethain stock-flow, conserved total)
  L2  rate_matrix / integrate   (graph master equation, attention transport)
  L3  run_blocks / block_metrics   (blocks, synchrony, N_eff)
  L4  reaction / fixed_points   (MFG reaction-map cartoon)
  L5  run_blocks / block_metrics / skill_horizon   (criticality, EWS, horizon)
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------
# L3 / L5  coupled-block bistable SDE
# ---------------------------------------------------------------------------
def run_blocks(K, W, theta=1.0, sigma=0.5, T=3000, dt=0.01, x0=None, seed=None):
    """Integrate K coupled bistable blocks (Euler-Maruyama).

    Per block:  x += dt*(theta*x - x**3 + W*(mean - x)) + sqrt(dt)*sigma*noise.

    The single-block drift theta*x - x**3 is a double-well (Model-A / Ginzburg-
    Landau) force with minima at x = +/-sqrt(theta); W is the mean-field coupling
    (the criticality knob) that pulls each block toward the population mean.

    Parameters
    ----------
    K : int            number of blocks
    W : float          mean-field coupling strength (criticality knob)
    theta : float      well depth / linear instability (default 1.0)
    sigma : float      noise amplitude (default 0.5)
    T : int            number of time steps (default 3000)
    dt : float         time step (default 0.01); model time = T*dt
    x0 : ndarray|None  initial state (K,); default N(0, 0.1) draws
    seed : int|None    RNG seed for reproducibility

    Returns
    -------
    traj : ndarray, shape (T, K)   the trajectory of all blocks.
    """
    r = np.random.default_rng(seed)
    x = r.normal(0, 0.1, K) if x0 is None else x0.copy()
    traj = np.empty((T, K))
    for t in range(T):
        m = x.mean()
        x = x + dt * (theta * x - x ** 3 + W * (m - x)) + np.sqrt(dt) * sigma * r.normal(size=K)
        traj[t] = x
    return traj


def block_metrics(traj, burn=1500):
    """Synchrony / effective-N diagnostics for a block trajectory.

    Reads off, from the post-burn-in portion of ``traj`` (shape (T, K)):

      S            mean over time of |<sign x>_blocks| -- the CORRECT well-
                   synchrony order parameter (mean-field magnitude of the
                   magnetization). 0 = blocks split, 1 = all blocks share a sign.

      neff_correct macro variance-ratio effective N:
                       Var_t(single-block sign) / Var_t(population-mean sign),
                   clipped to [1, K]. This is the operational Kish design-effect
                   N_eff: it collapses K -> 1 at well-synchronization (CORRECT).

      neff_pearson the MISLEADING metric K / (1 + (K-1)*rbar) where rbar is the
                   mean off-diagonal Pearson correlation of the block
                   *fluctuations*. WARNING: under well-synchronization the blocks
                   share a SIGN but their jitter stays weakly correlated, so this
                   stays ~K (e.g. 64 -> 29.5) and badly *understates* synchrony.
                   Reported only to expose why it is the wrong metric. Never use
                   it as the N_eff in a reading.

      rbar         mean off-diagonal Pearson correlation of fluctuations
                   (>=0 clipped), i.e. the quantity neff_pearson is built from.

    Parameters
    ----------
    traj : ndarray (T, K)
    burn : int   number of leading steps to discard as burn-in (default 1500)

    Returns
    -------
    dict with keys: S, neff_correct, neff_pearson, rbar.
    """
    tr = traj[burn:]
    K = tr.shape[1]

    # --- CORRECT order parameter: well-synchrony / mean-field magnetization ---
    S = float(np.abs(np.sign(tr).mean(axis=1)).mean())

    # --- CORRECT N_eff: variance reduction of the MACRO (sign/order) variable ---
    sgn = np.sign(tr)
    var_single = sgn.var(axis=0).mean()        # typical single-block temporal variance
    var_mean = sgn.mean(axis=1).var()          # temporal variance of population mean
    # var_mean ~ 0 means the population mean is pinned (full well-synchrony): the
    # macro variable carries the information of a single block, so N_eff -> 1.0
    # (this is exactly the E4 collapse 61 -> 1.0). Otherwise it is the variance
    # ratio, clipped to [1, K].
    neff_correct = (var_single / var_mean) if var_mean > 1e-12 else 1.0
    neff_correct = float(np.clip(neff_correct, 1.0, K))

    # --- MISLEADING N_eff: Pearson correlation of fluctuations (Kish form) ---
    C = np.corrcoef(tr.T)
    off = C[np.triu_indices(K, 1)]
    rbar = float(max(off.mean(), 0.0))
    neff_pearson = float(K / (1 + (K - 1) * rbar))

    return {"S": S, "neff_correct": neff_correct,
            "neff_pearson": neff_pearson, "rbar": rbar}


# ---------------------------------------------------------------------------
# L2  graph master equation (attention transport + belief drift)
# ---------------------------------------------------------------------------
def rate_matrix(A, base=0.05, bias_node=None, bias=0.0):
    """Build a row-sum-zero generator L for the attention master equation.

    Off-diagonal rates are ``base`` along the edges of adjacency matrix ``A``.
    A belief drift toward ``bias_node`` is added as extra inflow rate ``bias``
    along that node's edges; the diagonal is then set to minus the row sum so
    that ``L`` is a proper generator (each row sums to zero), which is what
    structurally conserves total attention mass 1^T p under dp/dt = L^T p.

    Parameters
    ----------
    A : ndarray (n, n)   symmetric 0/1 adjacency matrix
    base : float         baseline hopping rate along each edge (default 0.05)
    bias_node : int|None node toward which belief drift concentrates attention
    bias : float         extra inflow rate along the biased node's edges

    Returns
    -------
    L : ndarray (n, n)   generator with rows summing to zero.
    """
    L = A * base
    if bias_node is not None:
        L[:, bias_node] += A[:, bias_node] * bias   # belief drift toward node
    np.fill_diagonal(L, 0)
    np.fill_diagonal(L, -L.sum(axis=1))             # rows sum to zero
    return L


def integrate(L, p, T=400, dt=0.05):
    """Forward-Euler integrate the master equation dp/dt = L^T p.

    Because ``L`` has zero row sums, ``L^T p`` has zero column-sum contribution
    and total mass 1^T p is conserved to machine precision (E2: ~3.3e-16).

    Parameters
    ----------
    L : ndarray (n, n)   generator from ``rate_matrix``
    p : ndarray (n,)     initial probability vector (should sum to 1)
    T : int              number of steps (default 400)
    dt : float           step size (default 0.05)

    Returns
    -------
    traj : ndarray (T+1, n)   attention-share trajectory (incl. initial p).
    """
    p = p.copy()
    traj = [p.copy()]
    for _ in range(T):
        p = p + dt * (L.T @ p)
        traj.append(p.copy())
    return np.array(traj)


# ---------------------------------------------------------------------------
# L4  reflexivity: prediction -> reaction map (MFG fixed-point cartoon)
# ---------------------------------------------------------------------------
def reaction(f, guarantee=0.0, a=8, c=1.6, d=6, e=3):
    """Reaction map T(f): realized outcome as a function of published forecast f.

    Logistic coordination map  T(f) = sigmoid(a*f + c - d*guarantee - e), where
    f is the published forecast (e.g. probability of depositor loss) and
    ``guarantee`` is an engineered intervention (deposit insurance) that shifts
    the map down. Publishable forecasts are fixed points T(f) = f.

    Defaults reproduce sims_v2 E5 (note c = 1.6 = 4*0.4, the original 4*0.4 term):
        no guarantee  -> a single high fixed point ~0.995 (the run);
        guarantee=0.8 -> a single low fixed point ~0       (run averted).
    A bistable 3-fixed-point regime (the imitative regime) appears at nearby
    parameters / intermediate guarantee.
    """
    return 1.0 / (1.0 + np.exp(-(a * f + c - d * guarantee - e)))


def fixed_points(g, a=8, c=1.6, d=6, e=3, grid=None):
    """Fixed points of the reaction map for guarantee level ``g``.

    Finds sign changes of T(f) - f on a fine grid in [0, 1]; one root = unique
    (monotone/congestion-like) regime, three roots = bistable (imitative) regime.

    Parameters
    ----------
    g : float            guarantee level passed to ``reaction``
    a, c, d, e : float   reaction-map parameters (must match ``reaction``)
    grid : ndarray|None  evaluation grid; default linspace(0, 1, 200)

    Returns
    -------
    ndarray of approximate fixed points (f values where T(f) crosses f).
    """
    f = np.linspace(0, 1, 200) if grid is None else grid
    out = reaction(f, g, a=a, c=c, d=d, e=e) - f
    return f[np.where(np.diff(np.sign(out)))[0]]


# ---------------------------------------------------------------------------
# L5  skill horizon: ensemble spread vs climatology crossing
# ---------------------------------------------------------------------------
def skill_horizon(K, W, sigma=0.5, ens=8, seed0=10):
    """Predictability (skill) horizon in model time for coupling W.

    Launches an ``ens``-member ensemble from nearly-identical initial states and
    grows the spread of the population mean; the horizon is the model time at
    which ensemble spread first reaches 0.8 * the climatological spread (the
    point at which the forecast no longer beats climatology). Mirrors E4's tau*.

    Parameters
    ----------
    K : int            number of blocks
    W : float          coupling
    sigma : float      noise amplitude
    ens : int          ensemble size (default 8)
    seed0 : int        base seed; members use seed0 + e

    Returns
    -------
    float  skill horizon in model time (steps * dt). Equals the run length if
           the spread never crosses (effectively unbounded skill at that W).
    """
    pert_rng = np.random.default_rng(seed0)
    T = 1500
    dt = 0.01
    members = []
    for e in range(ens):
        x0 = np.full(K, 0.0) + pert_rng.normal(0, 1e-3, K)
        members.append(run_blocks(K, W, sigma=sigma, T=T, dt=dt,
                                   x0=x0, seed=seed0 + e).mean(axis=1))
    ens_arr = np.stack(members)
    spread = ens_arr.std(axis=0)
    clim = run_blocks(K, W, sigma=sigma, T=4000, dt=dt, seed=99)[2000:].mean(axis=1).std()
    mask = spread > 0.8 * clim
    cross = int(np.argmax(mask)) if mask.any() else T
    return cross * dt


# ---------------------------------------------------------------------------
# L1  slow stocks: lethain/systems stock-flow wrapper
# ---------------------------------------------------------------------------
def systems_stockflow(spec_str, rounds):
    """Run a lethain ``systems`` stock-flow model and return per-round dicts.

    Thin wrapper over ``systems.parse.parse(spec_str).run(rounds=rounds)`` so the
    skill can build a conserved (or leaky) macro stock model from a DSL string
    without importing systems directly. Total across a closed set of flows is
    conserved (E1 drift = 0).

    Parameters
    ----------
    spec_str : str   a lethain systems spec, e.g.
                         "OtherTopics(990) > BankTopic(10) @ Leak(0.35)\n"
                         "BankTopic > OtherTopics @ Leak(0.05)\n"
    rounds : int     number of rounds to simulate

    Returns
    -------
    list[dict]  per-round stock values keyed by stock name.
    """
    from systems.parse import parse
    return parse(spec_str).run(rounds=rounds)


# ---------------------------------------------------------------------------
# self-test (no plotting, no file writes)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    lo = block_metrics(run_blocks(K=64, W=0.0, seed=2))
    hi = block_metrics(run_blocks(K=64, W=1.0, seed=2))
    print(f"[engine self-test] S(W=0.0)={lo['S']:.3f}  S(W=1.0)={hi['S']:.3f}  "
          f"(expect rise toward synchrony); "
          f"neff_correct {lo['neff_correct']:.1f}->{hi['neff_correct']:.1f}, "
          f"neff_pearson {lo['neff_pearson']:.1f}->{hi['neff_pearson']:.1f} "
          f"(pearson barely moves -- MISLEADING)")
