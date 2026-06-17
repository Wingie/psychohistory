#!/usr/bin/env py -3.12
"""
PILOT BACKTESTS of the psychohistory framework against real harvested Reddit data.

Goal: adversarial. Find where the framework FAILS, not confirm it.

Three tests:
  (i)   Zero-sum attention conservation        -> r/AskEconomics
  (iii) Critical-slowing-down early warning     -> r/AskEconomics (tariff shock)
  (ii)  Block synchronization / N_eff           -> 5 location subreddits

Outputs JSON per test + a written summary table (RESULTS.md is authored from these
numbers by hand/tooling). Robust to malformed NDJSON lines (skipped).

Run:  py -3.12 run_backtests.py
"""
import json, os, math, datetime as dt
from collections import defaultdict, Counter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "temporal", "data"))
OUT  = HERE

# ---------------------------------------------------------------------------
# IO
# ---------------------------------------------------------------------------
def load(name):
    """Load NDJSON, skipping malformed lines. Returns (records, n_bad)."""
    recs, bad = [], 0
    path = os.path.join(DATA, name)
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
                t = float(o["created_utc"])
            except Exception:
                bad += 1
                continue
            o["_t"] = t
            o["_date"] = dt.datetime.fromtimestamp(t, dt.timezone.utc).date()
            recs.append(o)
    return recs, bad

def daystr(d):
    return d.isoformat()

def iso_week(d):
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"

# ---------------------------------------------------------------------------
# TEST (i): ZERO-SUM ATTENTION
# ---------------------------------------------------------------------------
TOPIC_RULES = [
    ("tariffs_trade", ["tariff", "trade war", "trade deficit", "import", "export",
                        "protectionism", "free trade", "wto", "trade", "supply chain"]),
    ("inflation",     ["inflation", "cpi", "deflation", "price level", "stagflation",
                        "cost of living", "prices rising", "purchasing power"]),
    ("jobs_labor",    ["job", "labor", "labour", "unemploy", "wage", "salary",
                        "minimum wage", "union", "employment", "worker"]),
    ("housing",       ["housing", "rent", "mortgage", "real estate", "home price",
                        "house price", "landlord", "property"]),
    ("stocks_markets",["stock", "market", "s&p", "nasdaq", "dow", "equit", "bond",
                        "yield", "recession", "bear market", "bull market", "sell-off",
                        "selloff", "fed ", "interest rate"]),
    ("debt_deficit",  ["debt", "deficit", "national debt", "fiscal", "budget",
                        "government spending", "treasury"]),
    ("crypto",        ["crypto", "bitcoin", "ethereum", "btc", "stablecoin", "blockchain"]),
    ("banking",       ["bank", "banking", "credit", "loan", "lending", "default",
                        "financial crisis", "bailout"]),
]

def classify_topic(title):
    t = (title or "").lower()
    for name, kws in TOPIC_RULES:
        for kw in kws:
            if kw in t:
                return name
    return "general"

def detrend(x):
    """Remove linear trend; return residuals."""
    x = np.asarray(x, float)
    n = len(x)
    if n < 3:
        return x - x.mean()
    t = np.arange(n)
    A = np.vstack([t, np.ones(n)]).T
    coef, *_ = np.linalg.lstsq(A, x, rcond=None)
    return x - A @ coef

def test_zero_sum(recs):
    topics = [name for name, _ in TOPIC_RULES] + ["general"]
    # weekly counts per topic
    wk_counts = defaultdict(lambda: Counter())
    for o in recs:
        wk = iso_week(o["_date"])
        wk_counts[wk][classify_topic(o.get("title", ""))] += 1
    weeks = sorted(wk_counts.keys())
    # drop partial first/last weeks (keep only weeks with >= 50% of median volume)
    totals = {wk: sum(wk_counts[wk].values()) for wk in weeks}
    med = np.median(list(totals.values()))
    keep = [wk for wk in weeks if totals[wk] >= 0.5 * med]
    weeks = keep

    total_vol = np.array([totals[wk] for wk in weeks], float)
    # share matrix: rows=weeks, cols=topics
    shares = np.zeros((len(weeks), len(topics)))
    for i, wk in enumerate(weeks):
        tot = totals[wk]
        for j, tp in enumerate(topics):
            shares[i, j] = wk_counts[wk][tp] / tot if tot else 0.0

    # volume trend
    vt = np.arange(len(total_vol))
    if len(total_vol) >= 3:
        slope, intercept = np.polyfit(vt, total_vol, 1)
    else:
        slope, intercept = 0.0, total_vol.mean() if len(total_vol) else 0.0
    vol_cv = float(total_vol.std() / total_vol.mean()) if total_vol.mean() else None

    # de-trend each topic's share series, then cross-correlations
    det = np.zeros_like(shares)
    for j in range(shares.shape[1]):
        det[:, j] = detrend(shares[:, j])
    # correlation matrix of de-trended shares
    # guard against zero-variance columns
    stds = det.std(axis=0)
    valid = stds > 1e-9
    corr = np.full((len(topics), len(topics)), np.nan)
    if valid.sum() >= 2:
        sub = det[:, valid]
        c = np.corrcoef(sub.T)
        idx = np.where(valid)[0]
        for a, ia in enumerate(idx):
            for b, ib in enumerate(idx):
                corr[ia, ib] = c[a, b]

    # off-diagonal pairwise correlations among valid topics
    pairs = []
    idx = np.where(valid)[0]
    for a in range(len(idx)):
        for b in range(a + 1, len(idx)):
            ia, ib = idx[a], idx[b]
            pairs.append((topics[ia], topics[ib], float(corr[ia, ib])))
    offdiag = [p[2] for p in pairs]
    mean_off = float(np.mean(offdiag)) if offdiag else None
    frac_neg = float(np.mean([v < 0 for v in offdiag])) if offdiag else None

    # Mechanical simplex baseline: if shares were independent multinomial noise around
    # fixed means, expected mean pairwise correlation is slightly negative ~ -1/(K-1).
    K = int(valid.sum())
    simplex_expected = -1.0 / (K - 1) if K > 1 else None

    return {
        "test": "zero_sum_attention",
        "subreddit": "AskEconomics",
        "n_weeks_used": len(weeks),
        "weeks": weeks,
        "topics": topics,
        "weekly_total_volume": [int(v) for v in total_vol],
        "volume_trend_slope_per_week": float(slope),
        "volume_mean": float(total_vol.mean()) if len(total_vol) else None,
        "volume_cv": vol_cv,
        "share_matrix_weeks_x_topics": shares.round(4).tolist(),
        "detrended_pairwise_correlations": [
            {"a": a, "b": b, "r": round(r, 3)} for (a, b, r) in pairs
        ],
        "mean_offdiag_detrended_corr": mean_off,
        "frac_negative_pairs": frac_neg,
        "simplex_mechanical_expected_mean_corr": simplex_expected,
        "n_topics_valid": K,
    }

# ---------------------------------------------------------------------------
# TEST (iii): EARLY WARNING / CRITICAL SLOWING DOWN
# ---------------------------------------------------------------------------
def daily_series(recs):
    cnt = Counter()
    com = Counter()
    for o in recs:
        d = o["_date"]
        cnt[d] += 1
        com[d] += int(o.get("num_comments", 0) or 0)
    days = sorted(cnt.keys())
    d0, d1 = days[0], days[-1]
    all_days = []
    d = d0
    while d <= d1:
        all_days.append(d)
        d += dt.timedelta(days=1)
    posts = np.array([cnt.get(d, 0) for d in all_days], float)
    comments = np.array([com.get(d, 0) for d in all_days], float)
    return all_days, posts, comments

def detect_event(days, posts):
    """Largest sustained activity jump. Use a 3-day forward mean vs trailing baseline."""
    n = len(posts)
    w = 7  # trailing baseline window
    fwd = 3  # forward sustained window
    best = None
    for i in range(w, n - fwd):
        base_mu = posts[i - w:i].mean()
        base_sd = posts[i - w:i].std() + 1e-9
        fwd_mu = posts[i:i + fwd].mean()
        z = (fwd_mu - base_mu) / base_sd
        ratio = fwd_mu / (base_mu + 1e-9)
        score = z
        if best is None or score > best[0]:
            best = (score, i, base_mu, fwd_mu, z, ratio)
    score, i, base_mu, fwd_mu, z, ratio = best
    return {
        "event_index": i,
        "event_date": daystr(days[i]),
        "baseline_mean": float(base_mu),
        "forward_mean": float(fwd_mu),
        "z_score": float(z),
        "ratio": float(ratio),
    }

def rolling_var_ac1(x, win):
    """Rolling variance and lag-1 autocorrelation; returns arrays aligned to window end."""
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

def trend_slope(y):
    y = np.asarray(y, float)
    m = ~np.isnan(y)
    if m.sum() < 3:
        return float("nan")
    t = np.arange(len(y))[m]
    s, _ = np.polyfit(t, y[m], 1)
    return float(s)

def test_early_warning(recs):
    days, posts, comments = daily_series(recs)
    ev = detect_event(days, posts)
    ei = ev["event_index"]

    win = 7  # rolling window for EWS indicators
    # PRE-EVENT window: strictly before event onset (no look-ahead)
    pre_posts = posts[:ei]            # everything before event day
    pre_days = days[:ei]

    # compute EWS over the pre-event activity series (detrended to isolate slowing-down,
    # not just the ramp). Use detrended series so a pure volume ramp doesn't masquerade.
    def ews_rise(series):
        if len(series) < 2 * win:
            return None
        ser = detrend(series)
        var, ac1 = rolling_var_ac1(ser, win)
        # slope of the indicator across the pre-event window (Kendall-style via linear slope)
        return {
            "var_slope": trend_slope(var),
            "ac1_slope": trend_slope(ac1),
            "var_first": float(np.nanmean(var[:max(1, len(var)//3)])),
            "var_last": float(np.nanmean(var[-max(1, len(var)//3):])),
            "ac1_first": float(np.nanmean(ac1[:max(1, len(ac1)//3)])),
            "ac1_last": float(np.nanmean(ac1[-max(1, len(ac1)//3):])),
        }

    pre_ews = ews_rise(pre_posts)

    # BASE-RATE NULL: slide an equal-length window across all NON-event regions and
    # compute the same indicator slopes. Then ask: is the pre-event slope extreme?
    L = len(pre_posts)  # length of the pre-event window
    null_var_slopes = []
    null_ac1_slopes = []
    n = len(posts)
    # exclude windows that overlap the event +/- a guard band
    guard = (ei - 2, min(n, ei + 5))
    step = 1
    for start in range(0, n - L, step):
        end = start + L
        if not (end <= guard[0] or start >= guard[1]):
            continue  # overlaps event region; skip
        seg = posts[start:end]
        if len(seg) < 2 * win:
            continue
        ser = detrend(seg)
        var, ac1 = rolling_var_ac1(ser, win)
        vs = trend_slope(var)
        as_ = trend_slope(ac1)
        if not math.isnan(vs):
            null_var_slopes.append(vs)
        if not math.isnan(as_):
            null_ac1_slopes.append(as_)

    def percentile_of(val, arr):
        if val is None or math.isnan(val) or not arr:
            return None
        arr = np.asarray(arr, float)
        return float((arr < val).mean())

    pct_var = percentile_of(pre_ews["var_slope"] if pre_ews else None, null_var_slopes)
    pct_ac1 = percentile_of(pre_ews["ac1_slope"] if pre_ews else None, null_ac1_slopes)

    # Simple AUC framing: treat the pre-event window as the single "positive" and all
    # null windows as "negatives"; AUC = P(pre-event indicator > random null indicator).
    auc_var = pct_var  # for a single positive, AUC == percentile rank
    auc_ac1 = pct_ac1

    return {
        "test": "early_warning_csd",
        "subreddit": "AskEconomics",
        "n_days": len(days),
        "date_start": daystr(days[0]),
        "date_end": daystr(days[-1]),
        "daily_posts": [int(p) for p in posts],
        "daily_comments": [int(c) for c in comments],
        "event": ev,
        "pre_event_window_len_days": L,
        "ews_window": win,
        "pre_event_ews": pre_ews,
        "null_n_windows_var": len(null_var_slopes),
        "null_n_windows_ac1": len(null_ac1_slopes),
        "null_var_slope_median": float(np.median(null_var_slopes)) if null_var_slopes else None,
        "null_ac1_slope_median": float(np.median(null_ac1_slopes)) if null_ac1_slopes else None,
        "pre_event_var_slope_percentile_vs_null": pct_var,
        "pre_event_ac1_slope_percentile_vs_null": pct_ac1,
        "auc_var_slope": auc_var,
        "auc_ac1_slope": auc_ac1,
    }

# ---------------------------------------------------------------------------
# TEST (ii): BLOCK SYNCHRONIZATION / N_eff
# ---------------------------------------------------------------------------
def test_block_sync(blocks):
    # blocks: dict name -> recs
    # daily series each
    series = {}
    spans = {}
    for name, recs in blocks.items():
        cnt = Counter()
        for o in recs:
            cnt[o["_date"]] += 1
        days = sorted(cnt.keys())
        spans[name] = (days[0], days[-1])
        series[name] = cnt

    lo = max(s[0] for s in spans.values())
    hi = min(s[1] for s in spans.values())
    # build common day axis
    days = []
    d = lo
    while d <= hi:
        days.append(d)
        d += dt.timedelta(days=1)

    names = sorted(blocks.keys())
    M = np.array([[series[nm].get(d, 0) for d in days] for nm in names], float)
    # M shape: (blocks, days)

    # cross-block correlation (Pearson of raw daily activity)
    corr = np.corrcoef(M) if M.shape[1] > 2 else np.full((len(names), len(names)), np.nan)
    off = []
    for a in range(len(names)):
        for b in range(a + 1, len(names)):
            off.append(corr[a, b])
    mean_corr = float(np.nanmean(off)) if off else None

    # MACRO VARIANCE-RATIO N_eff:
    #   block_mean(t) = mean over blocks of activity at t
    #   N_eff = mean_b Var_t(block_b) / Var_t(block_mean)
    # If blocks are independent: Var(mean) = (1/N) mean Var  => N_eff = N.
    # If perfectly synchronized: Var(mean) = mean Var          => N_eff = 1.
    block_mean = M.mean(axis=0)
    var_blocks = M.var(axis=1, ddof=1)         # per-block temporal variance
    var_mean = block_mean.var(ddof=1)
    mean_var_block = float(np.mean(var_blocks))
    n_eff = float(mean_var_block / var_mean) if var_mean > 1e-12 else None

    # Standardize each block (z-score over time) then variance-ratio on standardized,
    # which removes scale differences between subs.
    Mz = np.zeros_like(M)
    for i in range(M.shape[0]):
        s = M[i].std(ddof=1)
        Mz[i] = (M[i] - M[i].mean()) / s if s > 1e-12 else 0.0
    zmean = Mz.mean(axis=0)
    var_mean_z = zmean.var(ddof=1)
    # each standardized block has variance ~1
    mean_var_block_z = float(np.mean(Mz.var(axis=1, ddof=1)))
    n_eff_z = float(mean_var_block_z / var_mean_z) if var_mean_z > 1e-12 else None

    # Kuramoto-style order parameter on standardized series:
    # treat sign/phase via Hilbert-free proxy: use instantaneous standardized value as
    # a phase proxy is not rigorous; instead use the variance-ratio order param:
    # R = Var(zmean) / mean Var(z_block) in [0,1]; R->1 fully synchronized.
    R = float(var_mean_z / mean_var_block_z) if mean_var_block_z > 1e-12 else None

    # synchronization spike: day where standardized blocks are most co-aligned
    # measure daily dispersion across blocks (std across blocks each day); low dispersion
    # + high mean = synchronized surge.
    daily_cross_std = Mz.std(axis=0)
    daily_cross_mean = Mz.mean(axis=0)
    sync_score = daily_cross_mean - daily_cross_std  # high mean, low spread
    sync_idx = int(np.argmax(sync_score))

    return {
        "test": "block_synchronization_neff",
        "blocks": names,
        "per_block_span": {nm: [daystr(spans[nm][0]), daystr(spans[nm][1])] for nm in names},
        "overlap_start": daystr(lo),
        "overlap_end": daystr(hi),
        "overlap_days": len(days),
        "daily_axis": [daystr(d) for d in days],
        "activity_matrix_blocks_x_days": M.astype(int).tolist(),
        "mean_cross_block_corr": mean_corr,
        "cross_block_corr_matrix": np.round(corr, 3).tolist(),
        "n_blocks": len(names),
        "n_eff_variance_ratio_raw": n_eff,
        "n_eff_variance_ratio_standardized": n_eff_z,
        "kuramoto_like_order_param_R": R,
        "sync_spike_date": daystr(days[sync_idx]),
        "sync_spike_score": float(sync_score[sync_idx]),
    }

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    meta = {}
    ask, ask_bad = load("ask_econ.ndjson")
    meta["ask_econ_bad_lines"] = ask_bad

    r1 = test_zero_sum(ask)
    r3 = test_early_warning(ask)

    blocks = {}
    bad_loc = {}
    for nm in ["germany", "france", "italy", "spain", "europe"]:
        recs, bad = load(f"loc_{nm}.ndjson")
        blocks[nm] = recs
        bad_loc[nm] = bad
    meta["loc_bad_lines"] = bad_loc
    r2 = test_block_sync(blocks)

    for tag, r in [("zero_sum", r1), ("early_warning", r3), ("block_sync", r2)]:
        with open(os.path.join(OUT, f"result_{tag}.json"), "w", encoding="utf-8") as fh:
            json.dump(r, fh, indent=2)
    with open(os.path.join(OUT, "meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)

    # console summary
    print("=== TEST (i) ZERO-SUM ATTENTION ===")
    print(f"weeks used: {r1['n_weeks_used']}  volume mean={r1['volume_mean']:.0f} "
          f"slope/wk={r1['volume_trend_slope_per_week']:.1f} CV={r1['volume_cv']:.3f}")
    print(f"mean off-diag detrended corr = {r1['mean_offdiag_detrended_corr']:.3f}  "
          f"frac negative pairs = {r1['frac_negative_pairs']:.2f}  "
          f"simplex mechanical expected = {r1['simplex_mechanical_expected_mean_corr']:.3f}")

    print("\n=== TEST (iii) EARLY WARNING ===")
    ev = r3["event"]
    print(f"event date={ev['event_date']} z={ev['z_score']:.2f} ratio={ev['ratio']:.2f}")
    print(f"pre-event var slope pct vs null = {r3['pre_event_var_slope_percentile_vs_null']}")
    print(f"pre-event ac1 slope pct vs null = {r3['pre_event_ac1_slope_percentile_vs_null']}")
    print(f"null windows: var={r3['null_n_windows_var']} ac1={r3['null_n_windows_ac1']}")

    print("\n=== TEST (ii) BLOCK SYNC / N_eff ===")
    print(f"overlap {r2['overlap_start']}..{r2['overlap_end']} ({r2['overlap_days']} days)")
    print(f"mean cross-block corr = {r2['mean_cross_block_corr']:.3f}")
    print(f"N_eff (raw var-ratio) = {r2['n_eff_variance_ratio_raw']:.2f} of "
          f"{r2['n_blocks']} blocks")
    print(f"N_eff (standardized)  = {r2['n_eff_variance_ratio_standardized']:.2f}")
    print(f"Kuramoto-like R = {r2['kuramoto_like_order_param_R']:.3f}  "
          f"sync spike = {r2['sync_spike_date']}")

if __name__ == "__main__":
    main()
