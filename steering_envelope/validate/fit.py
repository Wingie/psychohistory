"""Shared statistical machinery for the domain studies.

Every fittable domain reduces to the same panel schema:

    unit (country or 'world'), year, v (speed proxy), s (steering proxy),
    event (binary: corner hit / crisis onset / rate deterioration)

and the same model comparison. All models are logits nested in the full
two-covariate model on standardized log proxies zv = z(log v), zs = z(log s):

    M_full  : logit P(event) = b0 + b1*zv + b2*zs
    M_v     : b2 = 0        (speed alone — the e/acc null)
    M_s     : b1 = 0        (steering alone — the stopper null)
    M_ratio : b2 = -b1      (the ratio v/s — the s/acc form)

The key falsification test (pre-registered in the README): does adding s to
v improve fit? LR(M_full vs M_v) with 1 df. If p > 0.1 in three or more of
the four historical domains, the steering term is decoration and s/acc
loses its empirical leg. Symmetrically LR(M_full vs M_s) asks whether speed
adds anything beyond steering. The ratio constraint LR(M_full vs M_ratio)
asks whether the data are content with the single-ratio form the hazard law
uses (here a HIGH p is friendly: the constraint costs nothing).

Out-of-sample: leave-one-decade-out AUC for each model.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize, stats


# ----------------------------------------------------------------------------
# logistic regression by MLE (no sklearn dependency)
# ----------------------------------------------------------------------------

def _nll(params: np.ndarray, X: np.ndarray, y: np.ndarray) -> float:
    z = X @ params
    # log(1+e^z) - y*z, computed stably
    return float(np.sum(np.logaddexp(0.0, z) - y * z))


def fit_logit(X: np.ndarray, y: np.ndarray) -> dict:
    """MLE logistic fit. X should include the intercept column."""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    p0 = np.zeros(X.shape[1])
    res = optimize.minimize(_nll, p0, args=(X, y), method="BFGS")
    ll = -res.fun
    k = X.shape[1]
    n = len(y)
    return {
        "params": res.x,
        "loglik": ll,
        "aic": 2 * k - 2 * ll,
        "bic": k * np.log(n) - 2 * ll,
        "n": n,
        "k": k,
        "converged": bool(res.success),
    }


def predict_logit(params: np.ndarray, X: np.ndarray) -> np.ndarray:
    z = np.asarray(X, dtype=float) @ params
    return 1.0 / (1.0 + np.exp(-np.clip(z, -30, 30)))


def auc(scores: np.ndarray, y: np.ndarray) -> float:
    """Mann-Whitney AUC: P(score_event > score_nonevent)."""
    scores = np.asarray(scores, dtype=float)
    y = np.asarray(y, dtype=bool)
    pos, neg = scores[y], scores[~y]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    ranks = stats.rankdata(np.concatenate([pos, neg]))
    r_pos = ranks[: len(pos)].sum()
    return float((r_pos - len(pos) * (len(pos) + 1) / 2)
                 / (len(pos) * len(neg)))


def lr_test(ll_full: float, ll_restricted: float, df: int) -> float:
    """Likelihood-ratio test p-value for nested models."""
    lr = 2.0 * (ll_full - ll_restricted)
    return float(stats.chi2.sf(max(lr, 0.0), df))


# ----------------------------------------------------------------------------
# the standard domain comparison
# ----------------------------------------------------------------------------

def _standardize(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    sd = x.std(ddof=1)
    return (x - x.mean()) / (sd if sd > 0 else 1.0)


def _design(zv, zs, model: str) -> np.ndarray:
    one = np.ones_like(zv)
    if model == "full":
        return np.column_stack([one, zv, zs])
    if model == "v":
        return np.column_stack([one, zv])
    if model == "s":
        return np.column_stack([one, zs])
    if model == "ratio":
        return np.column_stack([one, zv - zs])
    raise ValueError(model)


def domain_comparison(v, s, y, years=None, log_v=True, log_s=True,
                      name: str = "domain") -> dict:
    """Run the full nested comparison on one domain panel.

    v, s: positive proxies (logged then z-scored unless log_*=False, for
    proxies that are already indices/rates that can be <= 0).
    y: binary events. years: used for leave-one-decade-out AUC.
    """
    v = np.asarray(v, dtype=float)
    s = np.asarray(s, dtype=float)
    y = np.asarray(y, dtype=float)
    zv = _standardize(np.log(v) if log_v else v)
    zs = _standardize(np.log(s) if log_s else s)

    fits = {m: fit_logit(_design(zv, zs, m), y)
            for m in ("full", "v", "s", "ratio")}
    scores = {m: predict_logit(fits[m]["params"], _design(zv, zs, m))
              for m in fits}

    out = {
        "name": name,
        "n": int(len(y)),
        "events": int(y.sum()),
        "beta": {
            "full_v": float(fits["full"]["params"][1]),
            "full_s": float(fits["full"]["params"][2]),
            "ratio": float(fits["ratio"]["params"][1]),
        },
        "auc": {m: auc(scores[m], y) for m in fits},
        "aic": {m: fits[m]["aic"] for m in fits},
        "bic": {m: fits[m]["bic"] for m in fits},
        # the pre-registered falsifier: does s add power over v alone?
        "lr_p_s_given_v": lr_test(fits["full"]["loglik"],
                                  fits["v"]["loglik"], 1),
        # the symmetric stopper test: does v add power over s alone?
        "lr_p_v_given_s": lr_test(fits["full"]["loglik"],
                                  fits["s"]["loglik"], 1),
        # is the single-ratio form enough? (high p = yes, friendly)
        "lr_p_ratio_ok": lr_test(fits["full"]["loglik"],
                                 fits["ratio"]["loglik"], 1),
    }

    if years is not None:
        out["loro_auc"] = leave_one_decade_out(zv, zs, y, np.asarray(years))
    return out


def leave_one_decade_out(zv, zs, y, years) -> dict:
    """For each decade, fit on all other decades and score the held-out one;
    pool held-out scores into a single out-of-sample AUC per model."""
    decades = (years // 10) * 10
    pooled = {m: np.full(len(y), np.nan) for m in ("full", "v", "s", "ratio")}
    for d in np.unique(decades):
        test = decades == d
        train = ~test
        if y[train].sum() < 3 or len(np.unique(y[train])) < 2:
            continue
        for m in pooled:
            f = fit_logit(_design(zv[train], zs[train], m), y[train])
            pooled[m][test] = predict_logit(
                f["params"], _design(zv[test], zs[test], m))
    ok = ~np.isnan(pooled["full"])
    return {m: auc(pooled[m][ok], y[ok].astype(bool)) for m in pooled}


def fit_ols(X: np.ndarray, y: np.ndarray) -> dict:
    """Gaussian ML linear fit (for continuous outcomes like log rates), with
    loglik/AIC/BIC comparable across the same nested structure."""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    n = len(y)
    sigma2 = float(np.mean(resid ** 2))
    ll = -0.5 * n * (np.log(2 * np.pi * sigma2) + 1.0)
    k = X.shape[1] + 1  # + sigma
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    return {
        "params": beta,
        "loglik": ll,
        "aic": 2 * k - 2 * ll,
        "bic": k * np.log(n) - 2 * ll,
        "r2": 1.0 - float(np.sum(resid ** 2)) / ss_tot if ss_tot > 0 else 0.0,
        "n": n, "k": k,
    }


def continuous_comparison(v, s, y, years=None, log_v=True, log_s=True,
                          name: str = "domain") -> dict:
    """Same nested comparison as domain_comparison, for a continuous outcome
    (e.g. log fatality rate): M_full, M_v, M_s, M_ratio by Gaussian ML.

    Caveat baked into the report: with trending series the level fit is
    permissive (anything monotone correlates), so a first-difference
    robustness fit is included — Delta y on Delta zv, Delta zs — and the LR
    p-values from BOTH are reported. Judge the steering term on the
    differenced test when the two disagree."""
    v = np.asarray(v, dtype=float)
    s = np.asarray(s, dtype=float)
    y = np.asarray(y, dtype=float)
    zv = _standardize(np.log(v) if log_v else v)
    zs = _standardize(np.log(s) if log_s else s)

    def _compare(zv_, zs_, y_):
        fits = {m: fit_ols(_design(zv_, zs_, m), y_)
                for m in ("full", "v", "s", "ratio")}
        return fits

    fits = _compare(zv, zs, y)
    d_fits = _compare(np.diff(zv), np.diff(zs), np.diff(y))

    out = {
        "name": name,
        "n": int(len(y)),
        "outcome": "continuous",
        "beta": {
            "full_v": float(fits["full"]["params"][1]),
            "full_s": float(fits["full"]["params"][2]),
            "ratio": float(fits["ratio"]["params"][1]),
        },
        "r2": {m: fits[m]["r2"] for m in fits},
        "aic": {m: fits[m]["aic"] for m in fits},
        "bic": {m: fits[m]["bic"] for m in fits},
        "lr_p_s_given_v": lr_test(fits["full"]["loglik"],
                                  fits["v"]["loglik"], 1),
        "lr_p_v_given_s": lr_test(fits["full"]["loglik"],
                                  fits["s"]["loglik"], 1),
        "lr_p_ratio_ok": lr_test(fits["full"]["loglik"],
                                 fits["ratio"]["loglik"], 1),
        "diff": {
            "beta_full_v": float(d_fits["full"]["params"][1]),
            "beta_full_s": float(d_fits["full"]["params"][2]),
            "r2_full": d_fits["full"]["r2"],
            "lr_p_s_given_v": lr_test(d_fits["full"]["loglik"],
                                      d_fits["v"]["loglik"], 1),
            "lr_p_v_given_s": lr_test(d_fits["full"]["loglik"],
                                      d_fits["s"]["loglik"], 1),
        },
    }
    if years is not None:
        out["loro_r"] = loro_continuous(zv, zs, y, np.asarray(years))
    return out


def loro_continuous(zv, zs, y, years) -> dict:
    """Leave-one-decade-out correlation between held-out predictions and
    outcomes, per model."""
    decades = (years // 10) * 10
    pooled = {m: np.full(len(y), np.nan) for m in ("full", "v", "s", "ratio")}
    for d in np.unique(decades):
        test = decades == d
        train = ~test
        if train.sum() < 10:
            continue
        for m in pooled:
            f = fit_ols(_design(zv[train], zs[train], m), y[train])
            pooled[m][test] = _design(zv[test], zs[test], m) @ f["params"]
    ok = ~np.isnan(pooled["full"])
    return {m: float(np.corrcoef(pooled[m][ok], y[ok])[0, 1])
            for m in pooled}


def summarize(results: list[dict]) -> str:
    """Human-readable per-domain beta/AUC/LR table."""
    lines = [
        f"{'domain':22s} {'n':>5s} {'ev':>4s} {'b_v':>6s} {'b_s':>6s} "
        f"{'AUC v':>6s} {'AUC s':>6s} {'AUC r':>6s} {'AUC f':>6s} "
        f"{'p(s|v)':>8s} {'p(v|s)':>8s}"
    ]
    for r in results:
        lines.append(
            f"{r['name'][:22]:22s} {r['n']:5d} {r['events']:4d} "
            f"{r['beta']['full_v']:6.2f} {r['beta']['full_s']:6.2f} "
            f"{r['auc']['v']:6.3f} {r['auc']['s']:6.3f} "
            f"{r['auc']['ratio']:6.3f} {r['auc']['full']:6.3f} "
            f"{r['lr_p_s_given_v']:8.2g} {r['lr_p_v_given_s']:8.2g}"
        )
    return "\n".join(lines)
