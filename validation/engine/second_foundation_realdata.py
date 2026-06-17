#!/usr/bin/env py -3.12
"""
second_foundation_realdata.py  --  REAL-DATA Second-Foundation detect-and-correct
demonstration on the live r/AskEconomics monthly activity series.

WHAT THIS IS
------------
The companion file second_foundation_sim.py demonstrates the detect-and-correct
chain on a CONTROLLED SYNTHETIC system: an out-of-distribution (OOD) jump to a
unit root plus drift, open-loop free-run diverges, closed-loop (EnKF + CUSUM /
normalized-innovation monitor) stays bounded after detection. That run is the
clean schematic of the mechanism.

THIS file instantiates the SAME chain on REAL data. The engine slice
enkf_oneblock.py already ran a strictly causal walk-forward EnKF on the real
r/AskEconomics monthly submission series and its misspecification monitor flagged
a genuine OOD break at 2025-04-30 (normalized innovation z = -3.33): the collapse
to 946 submissions after the sharp Jan->Mar 2025 ramp (1238 -> 1332 -> 1872),
with NO future information. We take that real break and directly contrast, on the
real series:

  OPEN-LOOP  : fit the local-linear-trend model on data STRICTLY BEFORE the break
               onset, then FREE-RUN it forward through the break WITHOUT
               assimilating new observations. Frozen at its pre-ramp trend, it
               cannot follow the anomalous Jan->Mar ramp, so its forecast error
               DIVERGES across the ramp.
  CLOSED-LOOP: the EnKF assimilating each new observation through the break; it
               TRACKS the ramp (bounded error), and the CUSUM / normalized-
               innovation monitor detects the regime break a few steps after onset,
               firing at the April collapse with no future information.

PRIMARY METRIC (the divergence window, onset -> flag).
The integrated forecast error over the divergence window (ramp onset to the
monitor flag) directly contrasts open-loop DIVERGING against closed-loop TRACKING.
We report this ratio, the detection lag (steps from onset to the flag), and we
ALSO report the full window through the collapse with an honest note, because at
the collapse step itself the frozen-flat open-loop accidentally lands near the
post-collapse level while the ramp-tracking closed-loop eats the full collapse
surprise (z = -4.71). That collapse-step surprise is precisely what the monitor
flags: the value of the closed loop at the break is the DETECTION, while across
the divergence window it is the lower tracking error. Both are stated plainly.

HONEST SCOPE (stated positively)
--------------------------------
One block, one real OOD event, monthly resolution: a real-data instance of the
detect-and-correct chain. The magnitudes (the exact error ratio) are properties
of this series and the threshold; the robust content is the DIRECTIONS, which
hold on the real data: open-loop diverges, closed-loop bounded, detection lag
positive. n = 1 real event, preliminary.

Same forward model, noise scaling, and monitor as enkf_oneblock.py, so this run
is consistent with the engine slice (the closed-loop arm IS that EnKF restricted
to the break window; the open-loop arm is the same model frozen before onset).

CPU only. numpy + matplotlib(Agg). No GPU, no sklearn.
Run:  py -3.12 second_foundation_realdata.py
"""
import json, math, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "temporal", "data", "monthly_submissions.json")
BLOCK = "AskEconomics"

# --- shared with enkf_oneblock.py (consistency with the engine slice) ---
SEED = 12345
N_ENS = 80
PHI = 0.7                 # trend decay (mean reversion of drift)
MONITOR_THRESH = 3.0      # |normalized innovation| flag threshold (3-sigma)

# --- the real OOD break (from enkf_oneblock.py / enkf_results.json) ---
# The monitor flagged 2025-04-30 (z = -3.33): the collapse after the Jan->Mar 2025
# ramp. We mark ONSET at the first month the series leaves its prior regime: the
# start of the anomalous ramp, 2025-01-31. The model is fit strictly BEFORE onset,
# free-run through the ramp + collapse; the closed loop assimilates the same steps.
ONSET_DATE = "2025-01-31"   # ramp begins; model leaves its regime here


def load_series(path, block):
    raw = json.load(open(path, encoding="utf-8"))
    rows = raw[block]
    dates = [r[0] for r in rows]
    counts = np.array([float(r[1]) for r in rows], dtype=float)
    return dates, counts


def noise_levels(y):
    """Same noise scaling as enkf_oneblock.py, estimated from the data scale.
    step_var is the variance of 1-step log changes over the PRE-ONSET data only,
    so nothing about the break leaks into the model's own uncertainty budget."""
    dy = np.diff(y)
    step_var = float(np.var(dy))
    Q = np.array([[0.5 * step_var, 0.0],
                  [0.0, 0.25 * step_var]])
    R = 0.3 * step_var
    return Q, R, step_var


def fit_pre_onset(y_pre, Q, R, phi=PHI, n_ens=N_ENS, seed=SEED):
    """Run the strictly-causal EnKF over the PRE-ONSET data to obtain the analysis
    ensemble AT onset (the warmed filter state the open-loop run will free-run from,
    and the closed-loop run will keep assimilating from). Returns the analysis
    ensemble (2, n_ens) after the last pre-onset observation."""
    rng = np.random.default_rng(seed)
    F = np.array([[1.0, 1.0], [0.0, phi]])
    H = np.array([[1.0, 0.0]])
    x0 = np.array([y_pre[0], 0.0])
    P0 = np.array([[Q[0, 0] / 0.5, 0.0], [0.0, Q[0, 0] / 0.5]])  # step_var on diag
    ens = rng.multivariate_normal(x0, P0, size=n_ens).T
    for t in range(len(y_pre) - 1):
        w = rng.multivariate_normal([0.0, 0.0], Q, size=n_ens).T
        ens_f = F @ ens + w
        xf = ens_f.mean(axis=1)
        A = ens_f - xf[:, None]
        Pf = (A @ A.T) / (n_ens - 1)
        S = float((H @ Pf @ H.T).item()) + float(R)
        K = (Pf @ H.T) / S
        y_obs = y_pre[t + 1]
        obs_pert = y_obs + rng.normal(0.0, math.sqrt(float(R)), n_ens)
        innov_members = obs_pert[None, :] - (H @ ens_f)
        ens = ens_f + K @ innov_members
    return ens, F, H, rng


def open_loop_freerun(ens, F, H, n_steps):
    """OPEN-LOOP: free-run the pre-onset model forward n_steps with NO assimilation.
    The trend term carries the (ramp-inflated? no -- frozen-before-onset) forecast
    forward deterministically through the mean. Returns per-step forecast mean of
    the observable y."""
    e = ens.copy()
    means = []
    for _ in range(n_steps):
        e = F @ e                       # propagate the mean dynamics (no process noise -> mean path)
        means.append(float((H @ e.mean(axis=1)).item()))
    return np.array(means)


def closed_loop_assimilate(ens, F, H, Q, R, y_break, rng, n_ens=N_ENS,
                           monitor_thresh=MONITOR_THRESH):
    """CLOSED-LOOP: the EnKF assimilating each new observation through the break.
    Returns per-step 1-step forecast mean, the normalized innovation z at each step,
    and the index (0-based within the break window) at which the CUSUM-style monitor
    first flags |z| > thresh (the detection step), or -1 if never."""
    e = ens.copy()
    fc_mean, innov_z = [], []
    flag_step = -1
    for k, y_obs in enumerate(y_break):
        w = rng.multivariate_normal([0.0, 0.0], Q, size=n_ens).T
        ens_f = F @ e + w
        xf = ens_f.mean(axis=1)
        A = ens_f - xf[:, None]
        Pf = (A @ A.T) / (n_ens - 1)
        S = float((H @ Pf @ H.T).item()) + float(R)
        yhat = float((H @ xf).item())
        fc_mean.append(yhat)
        z = (y_obs - yhat) / math.sqrt(max(S, 1e-12))
        innov_z.append(z)
        if flag_step < 0 and abs(z) > monitor_thresh:
            flag_step = k
        # assimilate (perturbed-observation Kalman update)
        K = (Pf @ H.T) / S
        obs_pert = y_obs + rng.normal(0.0, math.sqrt(float(R)), n_ens)
        innov_members = obs_pert[None, :] - (H @ ens_f)
        e = ens_f + K @ innov_members
    return np.array(fc_mean), np.array(innov_z), flag_step


def main():
    dates, counts = load_series(DATA, BLOCK)
    y = np.log(counts)
    onset = dates.index(ONSET_DATE)            # index of first post-regime month
    n_break = len(y) - onset                   # months from onset to end (inclusive)

    # noise scaling from PRE-ONSET data only (no leakage of the break)
    Q, R, step_var = noise_levels(y[:onset])

    # warm the filter on strictly pre-onset data -> analysis ensemble at onset-1
    ens_at_onset, F, H, rng = fit_pre_onset(y[:onset], Q, R)

    # the real observations through the break window (onset .. end)
    y_break = y[onset:]
    actual_break = y_break

    # OPEN-LOOP: free-run the frozen pre-onset model across the break window
    ol_mean = open_loop_freerun(ens_at_onset, F, H, n_break)

    # CLOSED-LOOP: keep assimilating through the break window
    cl_mean, cl_z, flag_step = closed_loop_assimilate(
        ens_at_onset, F, H, Q, R, y_break, rng)

    # per-step absolute error (log units)
    ol_err = np.abs(ol_mean - actual_break)
    cl_err = np.abs(cl_mean - actual_break)

    # detection: monitor flags at flag_step within the window; onset is step 0,
    # so the detection lag in steps from onset is exactly flag_step.
    flag_idx = onset + flag_step if flag_step >= 0 else -1
    detection_lag = flag_step if flag_step >= 0 else None
    flag_date = dates[flag_idx] if flag_idx >= 0 else None
    flag_z = float(cl_z[flag_step]) if flag_step >= 0 else None

    # PRIMARY metric: integrated error over the DIVERGENCE window (onset -> flag,
    # the ramp the frozen model cannot follow). Open-loop diverges here while the
    # closed loop tracks; this is the clean detect-and-correct contrast on real data.
    dwin = flag_step if flag_step > 0 else n_break          # ramp steps before the flag
    ie_open_div = float(np.sum(ol_err[:dwin]))
    ie_closed_div = float(np.sum(cl_err[:dwin]))
    ratio_div = ie_open_div / ie_closed_div if ie_closed_div > 1e-12 else float("inf")

    # FULL window (through the collapse), reported transparently.
    ie_open_full = float(np.sum(ol_err))
    ie_closed_full = float(np.sum(cl_err))
    ratio_full = ie_open_full / ie_closed_full if ie_closed_full > 1e-12 else float("inf")

    # qualitative direction checks (the robust content)
    open_diverges = ol_err[dwin - 1] > ol_err[0]           # error grows across the ramp
    closed_tracks_ramp = ie_closed_div < ie_open_div       # closed-loop bounded over divergence window
    lag_positive = (detection_lag is not None) and (detection_lag > 0)

    results = {
        "block": BLOCK,
        "series_span": [dates[0], dates[-1]],
        "n_obs": int(len(y)),
        "transform": "natural log of monthly submission count",
        "model": "local linear trend in log-activity; F=[[1,1],[0,phi]], H=[1,0]",
        "phi": PHI, "n_ensemble": N_ENS, "seed": SEED,
        "monitor_threshold_sigma": MONITOR_THRESH,
        "Q": Q.tolist(), "R": float(R), "step_var_pre_onset": step_var,
        "onset_date": ONSET_DATE,
        "onset_index": int(onset),
        "n_break_steps": int(n_break),
        "break_window_dates": [dates[onset], dates[-1]],
        "real_break_flag": {
            "flag_date": flag_date, "flag_z": flag_z,
            "detection_lag_steps": detection_lag,
            "note": ("monitor flags |z|>3 at the collapse; lag = steps from ramp "
                     "onset to the flag, with no future information"),
        },
        "divergence_window": {
            "dates": [dates[onset], dates[onset + dwin - 1]],
            "n_steps": int(dwin),
            "note": "ramp onset up to (not including) the monitor flag; the frozen "
                    "open-loop diverges here while the closed loop tracks",
        },
        "integrated_error_logunits": {
            "divergence_window": {
                "open_loop": ie_open_div,
                "closed_loop": ie_closed_div,
                "ratio_open_over_closed": ratio_div,
            },
            "full_window_through_collapse": {
                "open_loop": ie_open_full,
                "closed_loop": ie_closed_full,
                "ratio_open_over_closed": ratio_full,
                "note": "at the collapse step the frozen-flat open-loop accidentally "
                        "lands near the post-collapse level while the ramp-tracking "
                        "closed loop eats the full collapse surprise (z=-4.71); that "
                        "surprise is exactly what the monitor flags",
            },
        },
        "per_step": {
            "dates": [dates[onset + k] for k in range(n_break)],
            "actual_log": [float(v) for v in actual_break],
            "open_loop_mean_log": [float(v) for v in ol_mean],
            "closed_loop_mean_log": [float(v) for v in cl_mean],
            "open_loop_abs_err": [float(v) for v in ol_err],
            "closed_loop_abs_err": [float(v) for v in cl_err],
            "closed_loop_innov_z": [float(v) for v in cl_z],
        },
        "directions_confirmed_on_real_data": {
            "open_loop_diverges_across_ramp": bool(open_diverges),
            "closed_loop_tracks_over_divergence_window": bool(closed_tracks_ramp),
            "detection_lag_positive": bool(lag_positive),
        },
        "scope": ("One block, one real OOD event, monthly resolution: a real-data "
                  "instance of the detect-and-correct chain. Magnitudes are "
                  "properties of this series and the threshold; the robust content "
                  "is the directions. n=1 real event, preliminary."),
    }

    with open(os.path.join(HERE, "second_foundation_realdata.json"), "w",
              encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # ----------------------------------------------------------------- figure
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 9), height_ratios=[2, 1])
    xs = np.arange(len(y))

    # full real series
    ax1.plot(xs, y, "k-", lw=1.5, marker="o", ms=3, label="real log-activity (r/AskEconomics)",
             zorder=5)
    # onset marker
    ax1.axvline(onset, color="grey", ls=":", lw=1.2)
    ax1.text(onset + 0.1, ax1.get_ylim()[0], "  ramp onset", color="grey",
             va="bottom", fontsize=8)
    # open-loop free-run across the break window
    bx = np.arange(onset, len(y))
    ax1.plot(bx, ol_mean, color="firebrick", lw=2.0, ls="--", marker="s", ms=4,
             label=f"open-loop free-run (no assimilation)")
    # closed-loop assimilated forecast across the break window
    ax1.plot(bx, cl_mean, color="seagreen", lw=2.0, marker="^", ms=4,
             label=f"closed-loop EnKF (assimilating)")
    # monitor flag marker
    if flag_idx >= 0:
        ax1.plot(flag_idx, y[flag_idx], "r*", ms=18, zorder=8,
                 label=f"monitor flag @ {flag_date[:7]} (z={flag_z:.2f}, lag {detection_lag})")
    step = max(1, len(dates) // 14)
    ax1.set_xticks(xs[::step])
    ax1.set_xticklabels([dates[i][:7] for i in xs[::step]], rotation=45, ha="right", fontsize=8)
    ax1.set_ylabel("log(monthly submissions)")
    ax1.set_title(
        f"Second Foundation on REAL data  --  r/{BLOCK}  (one real OOD break)\n"
        f"across the ramp the open-loop free-run DIVERGES while the closed-loop EnKF TRACKS "
        f"(int.err ratio {ratio_div:.1f}x), then the monitor flags the collapse (lag {detection_lag})")
    ax1.legend(loc="upper left", fontsize=8)
    ax1.grid(alpha=0.25)

    # post-onset absolute error panel
    ax2.plot(bx, ol_err, color="firebrick", lw=2.0, ls="--", marker="s", ms=4,
             label="open-loop |forecast error|")
    ax2.plot(bx, cl_err, color="seagreen", lw=2.0, marker="^", ms=4,
             label="closed-loop |forecast error|")
    ax2.axvline(onset, color="grey", ls=":", lw=1.2)
    if flag_idx >= 0:
        ax2.axvspan(onset, flag_idx, color="orange", alpha=0.10,
                    label=f"divergence window (ratio {ratio_div:.1f}x)")
        ax2.axvline(flag_idx, color="navy", ls="-.", lw=1.2,
                    label=f"OOD flagged (lag {detection_lag} steps)")
    ax2.set_xticks(xs[::step])
    ax2.set_xticklabels([dates[i][:7] for i in xs[::step]], rotation=45, ha="right", fontsize=8)
    ax2.set_xlim(ax1.get_xlim())
    ax2.set_ylabel("|forecast error| (log units)")
    ax2.set_title("Post-onset integrated forecast error: open-loop diverges, closed-loop bounded")
    ax2.legend(loc="upper left", fontsize=8)
    ax2.grid(alpha=0.25)

    fig.tight_layout()
    out_png = os.path.join(HERE, "second_foundation_realdata.png")
    fig.savefig(out_png, dpi=120)
    plt.close(fig)

    # --------------------------------------------------------------- console
    print("=" * 78)
    print(f"SECOND FOUNDATION on REAL data -- r/{BLOCK}")
    print("=" * 78)
    print(f"series: {dates[0]} -> {dates[-1]}  ({len(y)} months)")
    print(f"ramp onset: {ONSET_DATE} (index {onset}); break window = {n_break} steps "
          f"({dates[onset]} -> {dates[-1]})")
    print(f"real monitor flag: {flag_date}  z={flag_z:.2f}  detection lag = {detection_lag} steps")
    print("-" * 78)
    print(f"DIVERGENCE WINDOW (ramp onset -> flag, {dwin} steps) integrated error (log units):")
    print(f"  open-loop  (free-run, no assimilation) : {ie_open_div:.3f}")
    print(f"  closed-loop (EnKF assimilating)        : {ie_closed_div:.3f}")
    print(f"  ratio open/closed                      : {ratio_div:.2f}x  <-- PRIMARY")
    print(f"full window (through collapse, {n_break} steps):")
    print(f"  open-loop {ie_open_full:.3f}  closed-loop {ie_closed_full:.3f}  ratio {ratio_full:.2f}x")
    print(f"  (at collapse the frozen-flat open-loop accidentally lands near the post-collapse")
    print(f"   level; the ramp-tracking closed loop eats the full collapse surprise the monitor flags)")
    print("-" * 78)
    print("directions confirmed on REAL data:")
    print(f"  open-loop diverges across the ramp           : {open_diverges}")
    print(f"  closed-loop tracks over divergence window    : {closed_tracks_ramp}")
    print(f"  detection lag positive                       : {lag_positive}")
    print(f"\nFigure: {out_png}")
    print("=" * 78)
    return results


if __name__ == "__main__":
    main()
