#!/usr/bin/env py -3.12
"""
DECISIVE early-warning backtest of the psychohistory framework on an ENDOGENOUS
social cascade: the Jan-2021 GameStop / r/wallstreetbets short squeeze.

This is the POSITIVE-direction test that could FALSIFY the framework's claim:
  Before an endogenous, self-reinforcing cascade, critical-slowing-down (CSD)
  indicators (rising variance, rising lag-1 autocorrelation, rising within-
  community cross-correlation of activity) SHOULD rise.

It is the dissociation partner to the exogenous tariff-shock test in
../result_early_warning.json, which correctly returned NULL (no CSD rise) for an
exogenous shock.

Methodology is deliberately IDENTICAL to run_backtests.py::test_early_warning so
the two events are comparable:
  - detrend the activity series (so a pure volume ramp can't masquerade as CSD),
  - rolling (window=7) variance + lag-1 autocorrelation,
  - STRICT information cutoff: indicators computed ONLY on data strictly BEFORE
    the cascade onset index,
  - base-rate null: same indicator slopes over many non-cascade windows drawn from
    the 2020 baseline; report percentile (=single-positive AUC).

Cross-correlation proxy: submissions vs comments daily series (a 2-series within-
community proxy), rolling Pearson over the pre-onset window, and its slope.

Run:  py -3.12 run_gme.py
"""
import json, os, math, datetime as dt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

# --------------------------------------------------------------------------- #
# shared math (copied to match the tariff test exactly)
# --------------------------------------------------------------------------- #
def detrend(x):
    x = np.asarray(x, float)
    n = len(x)
    if n < 3:
        return x - x.mean()
    t = np.arange(n)
    A = np.vstack([t, np.ones(n)]).T
    coef, *_ = np.linalg.lstsq(A, x, rcond=None)
    return x - A @ coef

def rolling_var_ac1(x, win):
    n = len(x)
    var = np.full(n, np.nan)
    ac1 = np.full(n, np.nan)
    for i in range(win, n + 1):
        seg = x[i - win:i]
        seg = seg - seg.mean()
        v = seg.var()
        var[i - 1] = v
        if v > 1e-12 and len(seg) > 2:
            num = np.sum(seg[1:] * seg[:-1])
            den = np.sum(seg * seg)
            ac1[i - 1] = num / den if den > 1e-12 else np.nan
    return var, ac1

def rolling_xcorr(a, b, win):
    """Rolling Pearson correlation of two series (within-community proxy)."""
    n = len(a)
    out = np.full(n, np.nan)
    for i in range(win, n + 1):
        sa = a[i - win:i]; sb = b[i - win:i]
        if sa.std() > 1e-9 and sb.std() > 1e-9:
            out[i - 1] = np.corrcoef(sa, sb)[0, 1]
    return out

def trend_slope(y):
    y = np.asarray(y, float)
    m = ~np.isnan(y)
    if m.sum() < 3:
        return float("nan")
    t = np.arange(len(y))[m]
    s, _ = np.polyfit(t, y[m], 1)
    return float(s)

def daystr(d):
    return d.isoformat()

# --------------------------------------------------------------------------- #
# data loading: per-day dicts -> dense daily arrays over an explicit axis
# --------------------------------------------------------------------------- #
def load_perday(name):
    with open(os.path.join(DATA, name), "r", encoding="utf-8") as fh:
        d = json.load(fh)
    return d["per_day"], d.get("method")

def dense(per_day, start, end):
    """per_day: {iso->count}. start/end: date. Returns (days[], arr[])."""
    days, arr = [], []
    d = start
    while d <= end:
        days.append(d)
        arr.append(float(per_day.get(d.isoformat(), 0)))
        d += dt.timedelta(days=1)
    return days, np.array(arr, float)

def parse(s):
    y, m, dd = map(int, s.split("-"))
    return dt.date(y, m, dd)

# --------------------------------------------------------------------------- #
# onset detection: first SUSTAINED departure from baseline, BEFORE the 01-27 peak
# --------------------------------------------------------------------------- #
def detect_onset(days, posts, peak_cap_date):
    """First sustained jump: 3-day forward mean vs 7-day trailing baseline z-score,
    restricted to onset BEFORE the known peak (no using the peak itself as onset).
    Returns the FIRST index whose z exceeds a sustained threshold, not the max."""
    n = len(posts)
    w, fwd = 7, 3
    cap_idx = next((i for i, d in enumerate(days) if d >= peak_cap_date), n)
    # First, find the max-z point (descriptive). Then find first sustained crossing.
    cands = []
    for i in range(w, n - fwd):
        base_mu = posts[i - w:i].mean()
        base_sd = posts[i - w:i].std() + 1e-9
        fwd_mu = posts[i:i + fwd].mean()
        z = (fwd_mu - base_mu) / base_sd
        ratio = fwd_mu / (base_mu + 1e-9)
        cands.append((i, base_mu, fwd_mu, z, ratio))
    # max z overall (peak), descriptive
    peak = max(cands, key=lambda c: c[3])
    # ONSET = first index BEFORE the peak-cap where z >= 2 and ratio >= 1.5 sustained
    onset = None
    for (i, base_mu, fwd_mu, z, ratio) in cands:
        if i >= cap_idx:
            break
        if z >= 2.0 and ratio >= 1.5:
            onset = (i, base_mu, fwd_mu, z, ratio)
            break
    if onset is None:
        # fall back: the pre-cap candidate with the largest z
        pre = [c for c in cands if c[0] < cap_idx]
        onset = max(pre, key=lambda c: c[3]) if pre else peak
    return {
        "onset_index": onset[0],
        "onset_date": daystr(days[onset[0]]),
        "onset_baseline_mean": float(onset[1]),
        "onset_forward_mean": float(onset[2]),
        "onset_z": float(onset[3]),
        "onset_ratio": float(onset[4]),
        "peak_index": peak[0],
        "peak_date": daystr(days[peak[0]]),
        "peak_z": float(peak[3]),
        "peak_ratio": float(peak[4]),
    }

# --------------------------------------------------------------------------- #
WIN = 7  # rolling window (matches tariff test)

def ews_block(series, comments=None):
    if len(series) < 2 * WIN:
        return None
    ser = detrend(series)
    var, ac1 = rolling_var_ac1(ser, WIN)
    out = {
        "var_slope": trend_slope(var),
        "ac1_slope": trend_slope(ac1),
        "var_first": float(np.nanmean(var[:max(1, len(var)//3)])),
        "var_last": float(np.nanmean(var[-max(1, len(var)//3):])),
        "ac1_first": float(np.nanmean(ac1[:max(1, len(ac1)//3)])),
        "ac1_last": float(np.nanmean(ac1[-max(1, len(ac1)//3):])),
    }
    if comments is not None and len(comments) == len(series):
        xc = rolling_xcorr(detrend(series), detrend(comments), WIN)
        out["xcorr_slope"] = trend_slope(xc)
        out["xcorr_first"] = float(np.nanmean(xc[:max(1, len(xc)//3)]))
        out["xcorr_last"] = float(np.nanmean(xc[-max(1, len(xc)//3):]))
    return out

def main():
    # ---- load harvested series ----
    cas_sub, m1 = load_perday("cascade_submission.json")
    cas_com, m2 = load_perday("cascade_comment.json")
    base_sub, m3 = load_perday("baseline_submission.json")
    base_com, m4 = load_perday("baseline_comment.json")

    cas_start, cas_end = dt.date(2020, 11, 1), dt.date(2021, 2, 15)
    base_start, base_end = dt.date(2020, 1, 1), dt.date(2020, 10, 31)

    cdays, cposts = dense(cas_sub, cas_start, cas_end)
    _,     ccomm  = dense(cas_com, cas_start, cas_end)
    bdays, bposts = dense(base_sub, base_start, base_end)
    _,     bcomm  = dense(base_com, base_start, base_end)

    peak_cap = dt.date(2021, 1, 27)  # squeeze peak; onset must be earlier
    onset = detect_onset(cdays, cposts, peak_cap)
    oi = onset["onset_index"]

    # ---- STRICT cutoff: indicators on data strictly BEFORE onset ----
    pre_posts = cposts[:oi]
    pre_comm  = ccomm[:oi]
    pre_ews = ews_block(pre_posts, pre_comm)

    # ---- BASE-RATE NULL from the 2020 calm baseline ----
    # slide equal-length (= pre-onset length) windows across the baseline series,
    # compute the same indicator slopes -> null distribution.
    L = len(pre_posts)
    null_var, null_ac1, null_xc = [], [], []
    n = len(bposts)
    step = 1
    for s in range(0, n - L + 1, step):
        segp = bposts[s:s + L]
        segc = bcomm[s:s + L]
        if len(segp) < 2 * WIN:
            continue
        e = ews_block(segp, segc)
        if e is None:
            continue
        if not math.isnan(e["var_slope"]):
            null_var.append(e["var_slope"])
        if not math.isnan(e["ac1_slope"]):
            null_ac1.append(e["ac1_slope"])
        if "xcorr_slope" in e and not math.isnan(e["xcorr_slope"]):
            null_xc.append(e["xcorr_slope"])

    def pct(val, arr):
        if val is None or (isinstance(val, float) and math.isnan(val)) or not arr:
            return None
        arr = np.asarray(arr, float)
        return float((arr < val).mean())

    pv = pct(pre_ews["var_slope"] if pre_ews else None, null_var)
    pa = pct(pre_ews["ac1_slope"] if pre_ews else None, null_ac1)
    px = pct(pre_ews.get("xcorr_slope") if pre_ews else None, null_xc)

    # ---- VERDICT logic ----
    # SUPPORTS if a CSD indicator both RISES (positive slope, last>first) AND beats
    # the null (percentile >= 0.80). NULL if no rise. CONTRADICTS if it falls.
    def rose(first, last, slope):
        return (slope is not None and not math.isnan(slope)
                and slope > 0 and last > first)

    var_rose = pre_ews and rose(pre_ews["var_first"], pre_ews["var_last"], pre_ews["var_slope"])
    ac1_rose = pre_ews and rose(pre_ews["ac1_first"], pre_ews["ac1_last"], pre_ews["ac1_slope"])
    xc_rose  = pre_ews and "xcorr_slope" in pre_ews and rose(
        pre_ews["xcorr_first"], pre_ews["xcorr_last"], pre_ews["xcorr_slope"])

    beats = lambda p: (p is not None and p >= 0.80)
    n_rose = sum(bool(x) for x in [var_rose, ac1_rose, xc_rose])
    n_beats = sum(bool(beats(p)) for p in [pv, pa, px] if p is not None)

    if pre_ews is None:
        verdict = "INCONCLUSIVE"
        rationale = "pre-onset window too short for rolling indicators"
    elif n_rose >= 2 and n_beats >= 1:
        verdict = "SUPPORTS"
        rationale = (f"{n_rose}/3 CSD indicators rose; {n_beats} beat the base-rate "
                     f"null (>=0.80 percentile)")
    elif n_rose >= 1 and beats(pv):
        verdict = "SUPPORTS (partial)"
        rationale = "variance rose and beats null; AC1/xcorr weaker"
    elif n_rose == 0:
        # did any indicator fall meaningfully?
        fell = any(pre_ews[k + "_last"] < pre_ews[k + "_first"]
                   for k in ["var", "ac1"])
        verdict = "CONTRADICTS" if fell else "NULL"
        rationale = "no CSD indicator rose before onset"
    else:
        verdict = "INCONCLUSIVE"
        rationale = (f"{n_rose}/3 rose but none decisively beat the null "
                     f"(var pct={pv}, ac1 pct={pa})")

    result = {
        "test": "early_warning_csd_ENDOGENOUS",
        "event": "GameStop / r/wallstreetbets short squeeze (Jan 2021)",
        "subreddit": "wallstreetbets",
        "harvest_methods": {"cascade_sub": m1, "cascade_com": m2,
                            "baseline_sub": m3, "baseline_com": m4},
        "cascade_window": [daystr(cas_start), daystr(cas_end)],
        "baseline_window": [daystr(base_start), daystr(base_end)],
        "cascade_daily_posts": [int(x) for x in cposts],
        "cascade_daily_comments": [int(x) for x in ccomm],
        "cascade_days": [daystr(d) for d in cdays],
        "baseline_n_days": len(bposts),
        "baseline_total_posts": int(bposts.sum()),
        "onset": onset,
        "pre_onset_window_len_days": L,
        "ews_window": WIN,
        "pre_onset_ews": pre_ews,
        "null_n_windows_var": len(null_var),
        "null_n_windows_ac1": len(null_ac1),
        "null_n_windows_xcorr": len(null_xc),
        "null_var_slope_median": float(np.median(null_var)) if null_var else None,
        "null_ac1_slope_median": float(np.median(null_ac1)) if null_ac1 else None,
        "null_xcorr_slope_median": float(np.median(null_xc)) if null_xc else None,
        "pre_onset_var_slope_percentile_vs_null": pv,
        "pre_onset_ac1_slope_percentile_vs_null": pa,
        "pre_onset_xcorr_slope_percentile_vs_null": px,
        "auc_var_slope": pv,
        "auc_ac1_slope": pa,
        "auc_xcorr_slope": px,
        "indicators_rose": {"variance": bool(var_rose), "ac1": bool(ac1_rose),
                            "xcorr": bool(xc_rose)},
        "verdict": verdict,
        "verdict_rationale": rationale,
    }

    with open(os.path.join(HERE, "result_gme.json"), "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)

    # console summary
    print("=== GME ENDOGENOUS CSD BACKTEST ===")
    print(f"harvest methods: {result['harvest_methods']}")
    print(f"cascade posts total = {int(cposts.sum())} over {len(cposts)} days")
    print(f"baseline posts total = {int(bposts.sum())} over {len(bposts)} days")
    print(f"ONSET: {onset['onset_date']} (z={onset['onset_z']:.2f}, ratio={onset['onset_ratio']:.2f})")
    print(f"PEAK : {onset['peak_date']} (z={onset['peak_z']:.2f}, ratio={onset['peak_ratio']:.2f})")
    print(f"pre-onset window = {L} days")
    if pre_ews:
        print(f"  var: first={pre_ews['var_first']:.2f} last={pre_ews['var_last']:.2f} "
              f"slope={pre_ews['var_slope']:.4f}  pct_vs_null={pv}")
        print(f"  ac1: first={pre_ews['ac1_first']:.3f} last={pre_ews['ac1_last']:.3f} "
              f"slope={pre_ews['ac1_slope']:.5f}  pct_vs_null={pa}")
        if "xcorr_slope" in pre_ews:
            print(f"  xcorr: first={pre_ews['xcorr_first']:.3f} last={pre_ews['xcorr_last']:.3f} "
                  f"slope={pre_ews['xcorr_slope']:.5f}  pct_vs_null={px}")
    print(f"null windows: var={len(null_var)} ac1={len(null_ac1)} xcorr={len(null_xc)}")
    print(f"VERDICT: {verdict}  ({rationale})")

if __name__ == "__main__":
    main()
