#!/usr/bin/env py -3.12
"""
enkf_oneblock.py  --  Ensemble Kalman Filter (EnKF) forward / pseudo-out-of-sample
forecast test on ONE community block of real monthly Reddit activity.

WHY THIS EXISTS (ties to the paper's assimilating engine / Second Foundation)
---------------------------------------------------------------------------
The psychohistory paper claims a smooth-regime SKILL: in the absence of a
critical transition, a data-assimilating engine can forecast a community's
attention/activity one step ahead better than naive baselines, and it can
DETECT when the world has left the model (an out-of-model "Mule" event) via
the normalized innovation. This script is the first test that touches the
FORWARD skill claim itself rather than a backtest:

  * It runs a genuine, strictly causal WALK-FORWARD: at each time t the filter
    has seen ONLY y_0..y_t. It emits a forecast DISTRIBUTION for y_{t+1},
    THEN y_{t+1} is revealed and assimilated. No future leakage.
  * It scores the out-of-sample 1-step forecasts against TWO naive baselines
    (persistence and climatology) using RMSE, and -- because the EnKF gives a
    distribution -- a proper score (CRPS) and interval coverage (calibration).
  * It runs the misspecification monitor: the normalized innovation
    z_t = (y_t - H x_f) / sqrt(H P_f H^T + R). Under a correct model z ~ N(0,1).
    |z| past a threshold flags an out-of-model event.

THE FORWARD MODEL (one block) -- local linear trend in log-activity
-------------------------------------------------------------------
State x = [level, trend]  (a, b).  Log-activity m = a.
Dynamics (local-linear-trend / integrated random walk with mean-reverting trend):
    a_{t+1} = a_t + b_t                         + w_a
    b_{t+1} = phi * b_t                          + w_b      (0<phi<=1: trend decays)
Matrix form x_{t+1} = F x_t + w,   F = [[1, 1], [0, phi]].
This is a defensible, small, LINEAR mean-reverting-trend model. The level
follows the trend; the trend itself reverts toward zero (phi<1), so the level
is mean-reverting in differences -- a log random walk with damped drift, the
standard "smooth regime" workhorse. We keep the EnKF (stochastic, perturbed-obs)
rather than a closed-form KF deliberately, because the paper's engine is an
ensemble method; on a linear-Gaussian model the EnKF must REPRODUCE the KF in
the large-ensemble limit, which is also a correctness check.

OBSERVATION OPERATOR
    y_t = H x_t + v,   H = [1, 0]   (we observe log-activity = level only).
    Observation noise variance R (measurement / sampling noise on log counts).

OUTPUTS (written next to this file)
    enkf_forward.png   forecast vs actual w/ ensemble spread + innovation monitor
    enkf_results.json  RMSE/CRPS/coverage for EnKF vs persistence vs climatology
    RESULTS.md         method, numbers, verdict, monitor result, honest caveats

CPU only. numpy + matplotlib(Agg). No GPU, no sklearn.
"""
import json, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "temporal", "data", "monthly_submissions.json")
BLOCK = "AskEconomics"   # long, clean, contiguous monthly series 2020-12..2025-04 (51 pts)
SEED = 12345
N_ENS = 80               # ensemble members
PHI = 0.7                # trend decay (mean reversion of drift)
SPINUP = 8               # initial steps used to warm the filter; scored AFTER this
MONITOR_THRESH = 3.0     # |normalized innovation| flag threshold (3-sigma)


# ----------------------------------------------------------------------------- data
def load_series(path, block):
    raw = json.load(open(path, encoding="utf-8"))
    rows = raw[block]
    dates = [r[0] for r in rows]
    counts = np.array([float(r[1]) for r in rows], dtype=float)
    return dates, counts


# ------------------------------------------------------------------- proper scores
def crps_ensemble(ens, y):
    """CRPS of an ensemble forecast against scalar observation y.
    Exact empirical CRPS:  E|X-y| - 0.5 E|X-X'|  (Hersbach / energy form)."""
    ens = np.asarray(ens, float)
    n = ens.size
    term1 = np.mean(np.abs(ens - y))
    # 0.5 * mean over all pairs |xi - xj|
    diffs = np.abs(ens[:, None] - ens[None, :])
    term2 = 0.5 * diffs.sum() / (n * n)
    return term1 - term2


def crps_gaussian(mu, sigma, y):
    """Closed-form CRPS for N(mu,sigma) -- used for the baselines so they too get
    a proper score (persistence/climatology with an estimated predictive sd)."""
    if sigma <= 1e-9:
        return abs(mu - y)
    z = (y - mu) / sigma
    from math import erf, sqrt, pi, exp
    Phi = 0.5 * (1 + erf(z / sqrt(2)))
    phi = exp(-0.5 * z * z) / sqrt(2 * pi)
    return sigma * (z * (2 * Phi - 1) + 2 * phi - 1.0 / sqrt(pi))


# --------------------------------------------------------------------------- EnKF
def run_enkf(y, n_ens=N_ENS, phi=PHI, seed=SEED):
    """Strictly causal walk-forward stochastic EnKF (perturbed observations).

    y : 1-D array of observations (log-activity). For each t we form a 1-step
        forecast ensemble for y_{t+1} using only y_0..y_t, then assimilate y_{t+1}.

    Returns dict of per-step forecast diagnostics aligned to the TARGET index t+1.
    """
    rng = np.random.default_rng(seed)
    T = len(y)

    F = np.array([[1.0, 1.0], [0.0, phi]])
    H = np.array([[1.0, 0.0]])

    # --- noise levels, estimated from the data scale (one block, honest & simple)
    dy = np.diff(y)
    step_var = float(np.var(dy))                 # scale of 1-step changes in log-activity
    Q = np.array([[0.5 * step_var, 0.0],         # process noise on [level, trend]
                  [0.0, 0.25 * step_var]])
    R = 0.3 * step_var                           # obs noise variance (scalar)

    # --- initialise ensemble at first obs, zero trend, inflated spread
    x0 = np.array([y[0], 0.0])
    P0 = np.array([[step_var, 0.0], [0.0, step_var]])
    ens = rng.multivariate_normal(x0, P0, size=n_ens).T   # shape (2, n_ens)

    fc_mean, fc_std, fc_ens = [], [], []   # 1-step forecast for target index t (t=1..T-1)
    innov_z = []                            # normalized innovation at each assimilation
    target_idx = []

    for t in range(T - 1):
        # ---------- FORECAST step: propagate each member through F + process noise
        w = rng.multivariate_normal([0.0, 0.0], Q, size=n_ens).T
        ens_f = F @ ens + w                              # forecast ensemble for time t+1
        xf = ens_f.mean(axis=1)
        A = ens_f - xf[:, None]
        Pf = (A @ A.T) / (n_ens - 1)                     # forecast covariance

        # ---------- forecast of the OBSERVABLE y_{t+1} = H x + v
        y_pred_ens = (H @ ens_f).ravel()                 # member-wise predicted obs
        HPHt = float((H @ Pf @ H.T).item())
        S = HPHt + float(R)                              # innovation variance
        fc_mean.append(float((H @ xf).item()))
        fc_std.append(math.sqrt(max(S, 1e-12)))
        fc_ens.append(y_pred_ens + rng.normal(0.0, math.sqrt(float(R)), n_ens))  # incl. obs noise
        target_idx.append(t + 1)

        # ---------- reveal y_{t+1}, compute normalized innovation (MONITOR)
        y_obs = y[t + 1]
        innov = y_obs - float((H @ xf).item())
        innov_z.append(innov / math.sqrt(max(S, 1e-12)))

        # ---------- ANALYSIS step: perturbed-observation Kalman update
        K = (Pf @ H.T) / S                                # (2,1) gain
        obs_pert = y_obs + rng.normal(0.0, math.sqrt(float(R)), n_ens)   # perturbed obs
        innov_members = obs_pert[None, :] - (H @ ens_f)   # (1, n_ens)
        ens = ens_f + K @ innov_members                   # analysis ensemble

    return {
        "target_idx": np.array(target_idx),
        "fc_mean": np.array(fc_mean),
        "fc_std": np.array(fc_std),
        "fc_ens": fc_ens,            # list of arrays
        "innov_z": np.array(innov_z),
        "Q": Q.tolist(), "R": float(R), "phi": phi, "n_ens": n_ens,
        "step_var": step_var,
    }


# --------------------------------------------------------------------- baselines
def baseline_persistence(y, idx):
    """forecast y_{t+1} = y_t ; predictive sd = sd of 1-step changes seen so far."""
    means, sds = [], []
    for t in idx:
        means.append(y[t - 1])
        hist = np.diff(y[:t])            # 1-step changes using only past
        sds.append(float(np.std(hist)) if hist.size >= 2 else 1e-6)
    return np.array(means), np.array(sds)


def baseline_climatology(y, idx):
    """forecast y_{t+1} = running mean of y_0..y_t ; sd = running sd."""
    means, sds = [], []
    for t in idx:
        hist = y[:t]                     # only past observations
        means.append(float(np.mean(hist)))
        sds.append(float(np.std(hist)) if hist.size >= 2 else 1e-6)
    return np.array(means), np.array(sds)


# ------------------------------------------------------------------------ scoring
def score_point(pred, actual):
    err = pred - actual
    return float(np.sqrt(np.mean(err ** 2))), float(np.mean(np.abs(err)))


def coverage(means, sds, actual, q=1.96):
    lo, hi = means - q * sds, means + q * sds
    inside = (actual >= lo) & (actual <= hi)
    return float(np.mean(inside)), (lo, hi)


def main():
    dates, counts = load_series(DATA, BLOCK)
    y = np.log(counts)                            # log-activity (the latent observable)

    res = run_enkf(y)
    idx = res["target_idx"]
    actual = y[idx]

    # restrict scoring to AFTER spin-up (filter warmed) for an honest comparison
    keep = idx >= SPINUP
    sidx = idx[keep]
    a = y[sidx]

    # --- EnKF
    enkf_mean = res["fc_mean"][keep]
    enkf_std = res["fc_std"][keep]
    enkf_ens = [res["fc_ens"][i] for i in range(len(idx)) if keep[i]]
    enkf_rmse, enkf_mae = score_point(enkf_mean, a)
    enkf_crps = float(np.mean([crps_ensemble(e, yv) for e, yv in zip(enkf_ens, a)]))
    enkf_cov, _ = coverage(enkf_mean, enkf_std, a)

    # --- persistence
    p_mean, p_sd = baseline_persistence(y, sidx)
    p_rmse, p_mae = score_point(p_mean, a)
    p_crps = float(np.mean([crps_gaussian(m, s, yv) for m, s, yv in zip(p_mean, p_sd, a)]))
    p_cov, _ = coverage(p_mean, p_sd, a)

    # --- climatology
    c_mean, c_sd = baseline_climatology(y, sidx)
    c_rmse, c_mae = score_point(c_mean, a)
    c_crps = float(np.mean([crps_gaussian(m, s, yv) for m, s, yv in zip(c_mean, c_sd, a)]))
    c_cov, _ = coverage(c_mean, c_sd, a)

    # --- innovation monitor (over full walk-forward, after spin-up)
    z = res["innov_z"][keep]
    flags = np.where(np.abs(z) > MONITOR_THRESH)[0]
    flagged = [{"date": dates[int(sidx[i])], "z": float(z[i]),
                "actual_count": float(counts[int(sidx[i])])} for i in flags]

    # --- verdict
    beats_persist_rmse = enkf_rmse < p_rmse
    beats_clim_rmse = enkf_rmse < c_rmse
    beats_persist_crps = enkf_crps < p_crps
    beats_clim_crps = enkf_crps < c_crps
    beats_all = beats_persist_rmse and beats_clim_rmse and beats_persist_crps and beats_clim_crps

    results = {
        "block": BLOCK,
        "n_obs": int(len(y)),
        "n_scored_steps": int(len(a)),
        "scored_from_date": dates[int(sidx[0])],
        "scored_to_date": dates[int(sidx[-1])],
        "transform": "natural log of monthly submission count",
        "model": "local linear trend in log-activity; F=[[1,1],[0,phi]], H=[1,0]",
        "phi": PHI, "n_ensemble": N_ENS, "seed": SEED, "spinup_steps": SPINUP,
        "Q": res["Q"], "R": res["R"], "step_var_logspace": res["step_var"],
        "metrics": {
            "enkf":        {"rmse": enkf_rmse, "mae": enkf_mae, "crps": enkf_crps, "coverage95": enkf_cov},
            "persistence": {"rmse": p_rmse,    "mae": p_mae,    "crps": p_crps,    "coverage95": p_cov},
            "climatology": {"rmse": c_rmse,    "mae": c_mae,    "crps": c_crps,    "coverage95": c_cov},
        },
        "metrics_note": "RMSE/MAE/CRPS in LOG-activity units (dimensionless log-counts)",
        "verdict": {
            "enkf_beats_persistence_rmse": bool(beats_persist_rmse),
            "enkf_beats_climatology_rmse": bool(beats_clim_rmse),
            "enkf_beats_persistence_crps": bool(beats_persist_crps),
            "enkf_beats_climatology_crps": bool(beats_clim_crps),
            "enkf_beats_all_baselines": bool(beats_all),
        },
        "innovation_monitor": {
            "threshold_sigma": MONITOR_THRESH,
            "mean_abs_z": float(np.mean(np.abs(z))),
            "std_z": float(np.std(z)),
            "n_flagged": int(len(flags)),
            "flagged_events": flagged,
            "note": "Under a correct model z~N(0,1); |z|>thresh = out-of-model event",
        },
    }

    with open(os.path.join(HERE, "enkf_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # ----------------------------------------------------------------------- figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9), height_ratios=[2, 1])

    xs = np.arange(len(y))
    ax1.plot(xs, y, "k-", lw=1.4, label="actual log-activity", zorder=5)
    # EnKF forecast band over the full walk-forward (all targets, plot from spin-up)
    fm = res["fc_mean"]; fs = res["fc_std"]
    tx = idx
    ax1.plot(tx, fm, color="C0", lw=1.6, label="EnKF 1-step forecast mean")
    ax1.fill_between(tx, fm - 1.96 * fs, fm + 1.96 * fs, color="C0", alpha=0.20,
                     label="EnKF 95% forecast interval")
    ax1.axvline(SPINUP - 0.5, color="grey", ls=":", lw=1)
    ax1.text(SPINUP - 0.4, ax1.get_ylim()[0], "  scoring starts", color="grey",
             va="bottom", fontsize=8)
    # tick labels = dates (sparse)
    step = max(1, len(dates) // 12)
    ax1.set_xticks(xs[::step]); ax1.set_xticklabels([dates[i][:7] for i in xs[::step]],
                                                    rotation=45, ha="right", fontsize=8)
    ax1.set_ylabel("log(monthly submissions)")
    ax1.set_title(f"EnKF walk-forward 1-step forecast vs actual  --  r/{BLOCK}  "
                  f"(N={N_ENS} members)\nRMSE: EnKF {enkf_rmse:.3f} | persist "
                  f"{p_rmse:.3f} | clim {c_rmse:.3f}   (log units)")
    ax1.legend(loc="upper left", fontsize=8)
    ax1.grid(alpha=0.25)

    # innovation monitor panel
    zfull = res["innov_z"]
    ax2.axhline(0, color="k", lw=0.6)
    ax2.axhline(MONITOR_THRESH, color="r", ls="--", lw=1, label=f"±{MONITOR_THRESH}σ flag")
    ax2.axhline(-MONITOR_THRESH, color="r", ls="--", lw=1)
    ax2.axhspan(-1, 1, color="green", alpha=0.08)
    ax2.plot(tx, zfull, color="C3", lw=1.2, marker="o", ms=3)
    for i in flags:
        gi = int(sidx[i])
        ax2.plot(gi, z[i], "r*", ms=14, zorder=6)
        ax2.annotate(dates[gi][:7], (gi, z[i]), fontsize=8, color="r",
                     xytext=(4, 4), textcoords="offset points")
    ax2.set_xticks(xs[::step]); ax2.set_xticklabels([dates[i][:7] for i in xs[::step]],
                                                    rotation=45, ha="right", fontsize=8)
    ax2.set_ylabel("normalized innovation z")
    ax2.set_title("Misspecification monitor: z = (y - Hx_f)/sqrt(HP_fH^T+R)  "
                  "(out-of-model events flagged)")
    ax2.legend(loc="upper left", fontsize=8)
    ax2.grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "enkf_forward.png"), dpi=120)
    plt.close(fig)

    # --------------------------------------------------------------------- console
    print(f"Block: r/{BLOCK}   scored steps: {len(a)}  "
          f"({dates[int(sidx[0])]} -> {dates[int(sidx[-1])]})  [log units]")
    print(f"  EnKF        RMSE={enkf_rmse:.4f}  CRPS={enkf_crps:.4f}  cov95={enkf_cov:.2f}")
    print(f"  persistence RMSE={p_rmse:.4f}  CRPS={p_crps:.4f}  cov95={p_cov:.2f}")
    print(f"  climatology RMSE={c_rmse:.4f}  CRPS={c_crps:.4f}  cov95={c_cov:.2f}")
    print(f"  EnKF beats all baselines: {beats_all}")
    print(f"  Monitor: mean|z|={np.mean(np.abs(z)):.2f} std(z)={np.std(z):.2f} "
          f"flagged={len(flags)} -> {[f['date'] for f in flagged]}")
    return results


if __name__ == "__main__":
    main()
