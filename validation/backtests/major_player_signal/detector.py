#!/usr/bin/env py -3.12
"""
MAJOR-PLAYER-SIGNAL early-warning detector.

FRAMEWORK CLAIM (operator-skill mechanism)
------------------------------------------
Endogenous social cascades are preceded by a single operator / major-player's
signal RISING and LEADING the aggregate activity (internal priming). Exogenous
shocks are sudden spikes driven by an OUTSIDE major player (head of state, data
release) with NO internal-operator priming -- the driver's mention SPIKES *at*
the event, it does not LEAD it.

The test: can a detector tell these two mechanisms apart on real data?

THE DETECTOR
------------
For an event with onset week t0, on the STRICTLY-PRE-ONSET window measure whether
a single identifiable driver's signal LEADS the aggregate activity. Two
sub-measures (we use both):

(a) LEAD-LAG (cross-correlation).  Normalise (z-score) the driver signal and the
    aggregate over a window spanning the pre-onset run-up plus the onset itself.
    Compute the cross-correlation as a function of integer lag k (weeks). With the
    convention used here, xcorr(k) = mean_t[ driver(t) * aggregate(t+k) ]; a
    POSITIVE peak-lag k* means the driver leads the aggregate by k* weeks (the
    driver at t best matches aggregate k* weeks LATER). Operator-led => k* > 0.

(b) BUILDUP SLOPE.  Over a LONG pre-onset window (months before onset), is the
    driver signal rising (gradual internal priming) or flat-then-spiking
    (exogenous)? Two complementary numbers:
      - pre-onset log-linear slope of the driver (per week) and its level-vs-time
        Pearson r  -> a rising, well-correlated ramp = priming.
      - "spike-at-onset ratio": driver level in the onset week / max driver level
        in the long pre-onset window. >> 1 means the driver was essentially flat
        before and jumped AT the event (exogenous); ~1 or <1 means the driver had
        already built up before onset (endogenous priming).

(c) CONCENTRATION (optional).  Driver share = driver / aggregate, and whether that
    share rises over the pre-onset window (a single voice taking over before the
    crowd does). Reported, not used in the scalar.

OPERATOR-LED SCORE
------------------
    score = lead_weeks * buildup_factor
where lead_weeks = k* (peak-xcorr lag, weeks; + = driver leads) and
buildup_factor = clip(pre-onset driver slope sign & magnitude) folded with the
spike-at-onset test:  buildup_factor = +1 if the driver ramped before onset
(slope>0 AND spike_at_onset_ratio < ONSET_RATIO_THR), else -1 (flat-then-spike).
A simple, transparent classifier:
    INTERNAL-OPERATOR-LED  if  lead_weeks >= 1  AND  buildup_factor > 0
    EXOGENOUS-SPIKE        if  lead_weeks <= 0  OR   spike_at_onset_ratio is large
The headline scalar is (lead_weeks, buildup) reported together so the reader sees
both components, plus the product `operator_led_score`.

DATA
----
Arctic Shift search endpoint, inverse-inter-arrival density proxy (posts/hour),
weekly resolution -- the same proxy validated across this codebase. GameStop
reuses already-harvested series. AskEconomics aggregate + entity-mention series
are harvested here into ./data/.

Run:  py -3.12 detector.py            # harvest (idempotent cache) + analyze + figure
      py -3.12 detector.py analyze    # skip harvest, reuse ./data
"""
import json, os, sys, time, datetime, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
GME_DATA = os.path.join(HERE, "..", "gamestop_counterfactual", "data")  # READ-ONLY
os.makedirs(DATA, exist_ok=True)
BASE = "https://arctic-shift.photon-reddit.com/api/posts/search"

# classifier knobs
ONSET_RATIO_THR = 2.5   # spike-at-onset ratio above this => "flat-then-spike" (exogenous)


# --------------------------------------------------------------------------- #
# Harvest (Arctic Shift density proxy)
# --------------------------------------------------------------------------- #
def fetch(params, tries=6, timeout=90):
    url = BASE + "?" + urllib.parse.urlencode(params)
    for t in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 research/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            try:
                body = e.read().decode()[:60]
            except Exception:
                body = ""
            sys.stderr.write(f"    HTTP{e.code} {body} try{t}\n"); sys.stderr.flush()
            time.sleep((8 + 6 * t) if e.code == 429 else (3 + 3 * t))
        except Exception as e:
            sys.stderr.write(f"    {e} try{t}\n"); sys.stderr.flush()
            time.sleep(3 + 3 * t)
    return None


def week_density(sub, wk, query=None):
    after = int(datetime.datetime(wk.year, wk.month, wk.day,
                                  tzinfo=datetime.timezone.utc).timestamp())
    p = {"subreddit": sub, "after": str(after), "limit": "100",
         "sort": "asc", "fields": "created_utc"}
    if query:
        p["query"] = query
    d = fetch(p)
    if not d or not d.get("data"):
        return 0, 0.0
    ts = sorted(float(r["created_utc"]) for r in d["data"])
    n = len(ts)
    if n < 3:
        return n, 0.0
    span = ts[-1] - ts[0]
    if span <= 0:
        return n, 0.0
    return n, n / span * 3600.0


def _weeks(start, end):
    start = datetime.date.fromisoformat(start)
    end = datetime.date.fromisoformat(end)
    cur, ws = start, []
    while cur < end:
        ws.append(cur)
        cur += datetime.timedelta(days=7)
    return ws


def harvest(key, sub, start, end, query=None, workers=4, force=False):
    path = os.path.join(DATA, key + ".json")
    if os.path.exists(path) and not force:
        out = json.load(open(path))
        print(f"[cache] {key:26s} weeks={len(out)}")
        return out
    weeks = _weeks(start, end)

    def one(cur):
        n, v = week_density(sub, cur, query)
        return cur, round(v, 4)

    res = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for cur, val in ex.map(one, weeks):
            res[cur] = val
    out = [[c.isoformat(), res[c]] for c in weeks]
    json.dump(out, open(path, "w"), indent=0)
    nz = sum(1 for _, c in out if c > 0)
    print(f"{key:26s} weeks={len(out):3d} nonzero={nz:3d} "
          f"{out[0][0]}..{out[-1][0]} max={max((c for _, c in out), default=0):.2f}")
    return out


# --------------------------------------------------------------------------- #
# Load helpers
# --------------------------------------------------------------------------- #
def load(path):
    return json.load(open(path))


def as_series(raw):
    """raw [[date,val],...] -> (dates list[date], vals np.array)."""
    dates = [datetime.date.fromisoformat(w) for w, _ in raw]
    vals = np.array([float(v) for _, v in raw], dtype=float)
    return dates, vals


def align(dates_a, a, dates_b, b):
    """Align two weekly series on their common week set (intersection)."""
    map_a = {d: v for d, v in zip(dates_a, a)}
    map_b = {d: v for d, v in zip(dates_b, b)}
    common = sorted(set(map_a) & set(map_b))
    return common, (np.array([map_a[d] for d in common]),
                    np.array([map_b[d] for d in common]))


def zscore(x):
    x = np.asarray(x, float)
    s = x.std()
    return (x - x.mean()) / s if s > 0 else x - x.mean()


# --------------------------------------------------------------------------- #
# Detector core
# --------------------------------------------------------------------------- #
def cross_corr_lead(driver, aggregate, max_lag=6):
    """
    Lead-lag on the GROWTH of each series (first difference), which isolates the
    run-up dynamics from a single co-located terminal mega-spike. Differencing is
    the key fix: on raw levels, GameStop's one giant same-week spike (operator and
    aggregate both peak the same week) pins the peak correlation to lag 0 and hides
    the fact that the operator's RAMP led. On the week-over-week change, a leading
    ramp shows up as a positive lag.

    xcorr(k) = corr( d_driver(t), d_aggregate(t+k) ), k in [-max_lag, max_lag].
    best_lag>0 => driver's change LEADS the aggregate's change by best_lag weeks.

    We also return a GUARDED lead: the peak only counts as a real lead if (i) it is
    at k>0, (ii) it exceeds the lag-0 value by >= LEAD_MARGIN, and (iii) it clears a
    noise floor. Otherwise guarded_lead = 0 (coincident / no resolvable lead).
    """
    LEAD_MARGIN = 0.08
    NOISE_FLOOR = 0.20
    dd = np.diff(driver)
    da = np.diff(aggregate)
    n = len(dd)
    out = {}
    for k in range(-max_lag, max_lag + 1):
        if k >= 0:
            x = dd[:n - k] if k > 0 else dd
            y = da[k:]
        else:
            x = dd[-k:]
            y = da[:n + k]
        if len(x) >= 3 and x.std() > 0 and y.std() > 0:
            out[k] = float(np.corrcoef(x, y)[0, 1])
        else:
            out[k] = np.nan
    valid = {k: v for k, v in out.items() if not np.isnan(v)}
    best_lag = max(valid, key=valid.get)
    best_corr = valid[best_lag]
    lag0 = valid.get(0, 0.0)
    guarded = best_lag if (best_lag > 0 and best_corr >= NOISE_FLOOR
                           and (best_corr - lag0) >= LEAD_MARGIN) else 0
    return best_lag, best_corr, guarded, out


def buildup(driver_dates, driver_vals, onset, long_window_weeks=14):
    """
    Pre-onset run-up analysis of the DRIVER signal. The discriminator that actually
    separates the mechanisms at weekly resolution is the SHAPE and DURATION of the
    pre-onset ramp:

      - INTERNAL OPERATOR PRIMING  ->  a long, sustained, monotone ramp over MANY
        weeks (the operator's voice grows steadily for months before the crowd).
      - EXOGENOUS NEWS ANTICIPATION  ->  flat for a long time then a SHORT (1-3 wk)
        bump immediately before / at the event, or no ramp at all.

    Numbers:
      log_slope_per_week, level_vs_time_r : log-linear ramp over the long pre window.
      ramp_run_weeks   : longest run of consecutive non-decreasing weeks ending at
                         the last pre-onset week (how long the driver has been
                         rising INTO the onset).
      early_vs_late    : ratio of the slope over the FIRST half of the long pre
                         window to the slope over the whole window. A sustained
                         internal ramp is rising already in the first half
                         (early_vs_late ~ 1); a last-minute news bump has all its
                         rise in the final weeks (early_vs_late ~ 0).
      spike_at_onset_ratio : onset level / long-pre-window max (descriptive).

    buildup_factor = +1 (sustained internal priming) iff the long-window slope is
    positive AND well-correlated AND the rise is NOT confined to the final ~3 weeks
    (ramp_run_weeks long enough OR early-half already rising). Else -1.
    """
    res = {}
    # long pre-onset window
    lo = onset - datetime.timedelta(weeks=long_window_weeks)
    pre_idx = [i for i, d in enumerate(driver_dates) if lo <= d < onset]
    pre_d = [driver_dates[i] for i in pre_idx]
    pre_v = driver_vals[pre_idx]
    res["long_window"] = f"{lo}..{onset} ({len(pre_d)} wk)"
    slope = r = 0.0
    early_late = None
    if len(pre_d) >= 6 and np.any(pre_v > 0):
        x = np.array([(d - pre_d[0]).days / 7.0 for d in pre_d])
        y = np.log(np.clip(pre_v, 1e-4, None))
        A = np.vstack([x, np.ones_like(x)]).T
        slope = float(np.linalg.lstsq(A, y, rcond=None)[0][0])
        r = float(np.corrcoef(x, pre_v)[0, 1]) if pre_v.std() > 0 else 0.0
        # early-half slope vs full slope (is the ramp already underway early?)
        h = len(pre_d) // 2
        if h >= 3 and pre_v[:h].std() >= 0:
            xe, ye = x[:h], y[:h]
            Ae = np.vstack([xe, np.ones_like(xe)]).T
            slope_e = float(np.linalg.lstsq(Ae, ye, rcond=None)[0][0])
            early_late = round(slope_e / slope, 2) if abs(slope) > 1e-6 else None
        res["log_slope_per_week"] = round(slope, 4)
        res["level_vs_time_r"] = round(r, 3)
        res["weekly_growth_pct"] = round((np.exp(slope) - 1) * 100, 2)
        res["early_half_slope_ratio"] = early_late
    else:
        res.update(log_slope_per_week=None, level_vs_time_r=None,
                   weekly_growth_pct=None, early_half_slope_ratio=None)
    # ramp_run_weeks: longest non-decreasing run ending at last pre-onset week
    run = 0
    for i in range(len(pre_v) - 1, 0, -1):
        if pre_v[i] >= pre_v[i - 1] * 0.98:   # allow tiny dips
            run += 1
        else:
            break
    res["ramp_run_weeks_into_onset"] = run
    # spike-at-onset (descriptive)
    onset_idx = [i for i, d in enumerate(driver_dates)
                 if onset <= d < onset + datetime.timedelta(days=14)]
    onset_level = float(np.max(driver_vals[onset_idx])) if onset_idx else 0.0
    pre_max = float(np.max(pre_v)) if len(pre_v) and np.any(pre_v > 0) else 0.0
    ratio = (onset_level / pre_max) if pre_max > 0 else (float("inf") if onset_level > 0 else 0.0)
    res["onset_level"] = round(onset_level, 4)
    res["pre_onset_max"] = round(pre_max, 4)
    res["spike_at_onset_ratio"] = (round(ratio, 2) if np.isfinite(ratio) else "inf")
    # sustained-priming test. The DURATION of the monotone run into onset is the
    # discriminator that survives weekly resolution: an internal operator priming a
    # position grows steadily for MONTHS (long run), while a pre-announced external
    # shock produces at most a SHORT (1-3 wk) news-anticipation bump or no ramp.
    SUSTAINED_RUN_WK = 6      # >= ~1.5 months of monotone rise = internal priming
    early_already = (early_late is not None and early_late >= 0.30)
    sustained_run = run >= SUSTAINED_RUN_WK
    primed = (slope > 0 and r > 0.3 and sustained_run and early_already)
    res["sustained_run_threshold_wk"] = SUSTAINED_RUN_WK
    res["buildup_factor"] = 1 if primed else -1
    res["buildup_verdict"] = (
        f"sustained internal priming (rising {run} wk into onset >= {SUSTAINED_RUN_WK} wk "
        f"threshold, early-half slope ratio {early_late})"
        if primed else
        f"no sustained priming (ramp_run={run} wk < {SUSTAINED_RUN_WK} wk threshold, "
        f"early-half ratio {early_late}; flat-then-bump / news-anticipation)")
    return res


def concentration(common, driver, aggregate, onset):
    """driver/aggregate share, and whether it rises over the pre-onset window."""
    share = np.divide(driver, aggregate, out=np.zeros_like(driver), where=aggregate > 0)
    pre = [i for i, d in enumerate(common) if d < onset]
    if len(pre) >= 4:
        x = np.array([(common[i] - common[pre[0]]).days / 7.0 for i in pre])
        sp = share[pre]
        r = float(np.corrcoef(x, sp)[0, 1]) if sp.std() > 0 else 0.0
    else:
        r = None
    return {"share_series": [round(float(s), 4) for s in share],
            "pre_onset_share_trend_r": round(r, 3) if r is not None else None}


def run_event(name, driver_dates, driver_vals, agg_dates, agg_vals, onset,
              xcorr_window=None, max_lag=6):
    """
    xcorr_window: optional (start,end) dates restricting the lead-lag window to the
    pre-onset run-up + onset (so a long flat tail doesn't dominate the correlation).
    If None, uses [onset-12wk, onset+4wk].
    """
    onset = datetime.date.fromisoformat(onset) if isinstance(onset, str) else onset
    common, (d_al, a_al) = align(driver_dates, driver_vals, agg_dates, agg_vals)
    if xcorr_window is None:
        lo = onset - datetime.timedelta(weeks=12)
        hi = onset + datetime.timedelta(weeks=4)
    else:
        lo = datetime.date.fromisoformat(xcorr_window[0])
        hi = datetime.date.fromisoformat(xcorr_window[1])
    sel = [i for i, d in enumerate(common) if lo <= d <= hi]
    win_dates = [common[i] for i in sel]
    win_driver, win_agg = d_al[sel], a_al[sel]
    best_lag, best_corr, guarded_lead, all_corr = cross_corr_lead(
        win_driver, win_agg, max_lag=max_lag)
    bld = buildup(driver_dates, driver_vals, onset)
    conc = concentration(common, d_al, a_al, onset)

    # ---- operator-led score ----------------------------------------------- #
    # The buildup SHAPE is the primary discriminator (weekly lead-lag is at the
    # resolution floor); the guarded growth-lead is a secondary corroborator.
    # buildup_factor: +1 sustained internal priming, -1 otherwise.
    # ramp_score: a continuous priming strength = slope_sign * level_r * sqrt(ramp_run).
    bf = bld["buildup_factor"]
    slope = bld.get("log_slope_per_week") or 0.0
    rlev = bld.get("level_vs_time_r") or 0.0
    run = bld.get("ramp_run_weeks_into_onset", 0)
    ramp_strength = round((1 if slope > 0 else -1) * max(rlev, 0.0) * (run ** 0.5), 3)
    # headline scalar: buildup_factor folded with guarded lead. The growth-lead bonus
    # is only credited when the buildup is a SUSTAINED ramp -- a lead without a
    # sustained operator ramp is anticipatory news flow / argmax-on-noise, not an
    # operator lead, so it must not push an exogenous event toward a positive score.
    lead_bonus = 0.5 * guarded_lead if bf > 0 else 0.0
    operator_led_score = round(bf * (1 + ramp_strength) + lead_bonus, 3)

    # classification: SUSTAINED ramp is necessary for INTERNAL-OPERATOR-LED. A short
    # ramp + a 1-2 wk growth-lead is anticipatory news flow, not internal priming.
    sustained = bf > 0  # buildup_factor already requires run >= SUSTAINED_RUN_WK
    if sustained:
        cls = "INTERNAL-OPERATOR-LED"
    elif guarded_lead >= 1 or run >= 3:
        # some short anticipatory ramp but not sustained internal priming
        cls = "EXOGENOUS-SPIKE (mild anticipation)"
    else:
        cls = "EXOGENOUS-SPIKE"

    return {
        "event": name,
        "onset_week": onset.isoformat(),
        "xcorr_window": [win_dates[0].isoformat(), win_dates[-1].isoformat()],
        "xcorr_window_n_weeks": len(win_dates),
        "lead_weeks_growth_xcorr_raw": int(best_lag),
        "lead_weeks_guarded": int(guarded_lead),
        "peak_growth_xcorr": round(best_corr, 3),
        "growth_xcorr_by_lag": {str(k): round(v, 3) for k, v in sorted(all_corr.items())},
        "buildup": bld,
        "ramp_strength": ramp_strength,
        "concentration": conc,
        "operator_led_score": operator_led_score,
        "classification": cls,
    }, {"common": common, "driver": d_al, "aggregate": a_al,
        "win_dates": win_dates, "onset": onset}


# --------------------------------------------------------------------------- #
# Event wiring
# --------------------------------------------------------------------------- #
def harvest_askecon():
    # aggregate AskEconomics activity, weekly, spanning both incidents
    harvest("askecon_overall_2022", "AskEconomics", "2021-06-01", "2022-08-01", None, workers=4)
    harvest("askecon_overall_2025", "AskEconomics", "2024-09-01", "2025-06-01", None, workers=4)
    # entity-mention signals (the would-be "operator/major-player" proxy)
    # 2022 inflation surge: inflation / Fed
    harvest("askecon_inflation_2022", "AskEconomics", "2021-06-01", "2022-08-01", "inflation", workers=3)
    harvest("askecon_fed_2022", "AskEconomics", "2021-06-01", "2022-08-01", "Fed", workers=3)
    # 2025 tariff shock: tariff / Trump
    harvest("askecon_tariff_2025", "AskEconomics", "2024-09-01", "2025-06-01", "tariff", workers=3)
    harvest("askecon_trump_2025", "AskEconomics", "2024-09-01", "2025-06-01", "Trump", workers=3)


def build_gamestop():
    # operator signal = sum of the four DFV/RoaringKitty proxy series
    dfv_keys = ["dfv_DFV", "dfv_DeepFuckingValue", "dfv_RoaringKitty", "dfv_GMEYOLO"]
    series = {k: dict(load(os.path.join(GME_DATA, k + ".json"))) for k in dfv_keys}
    all_w = sorted(set().union(*[set(series[k]) for k in dfv_keys]))
    op_dates = [datetime.date.fromisoformat(w) for w in all_w]
    op_vals = np.array([sum(series[k].get(w, 0.0) for k in dfv_keys) for w in all_w])
    agg = load(os.path.join(GME_DATA, "wsb_overall_activity.json"))
    agg_dates, agg_vals = as_series(agg)
    return op_dates, op_vals, agg_dates, agg_vals


def sum_series(*keys):
    series = {k: dict(load(os.path.join(DATA, k + ".json"))) for k in keys}
    all_w = sorted(set().union(*[set(series[k]) for k in keys]))
    dates = [datetime.date.fromisoformat(w) for w in all_w]
    vals = np.array([sum(series[k].get(w, 0.0) for k in keys) for w in all_w])
    return dates, vals


# --------------------------------------------------------------------------- #
def analyze():
    results = {}
    plotdata = {}

    # ---- EVENT 1: GameStop (endogenous / positive case) ----
    op_d, op_v, agg_d, agg_v = build_gamestop()
    # GME spike onset 2021-01-25; run-up window covers the DFV priming
    res, pd = run_event(
        "GameStop (DFV/RoaringKitty vs r/wallstreetbets)",
        op_d, op_v, agg_d, agg_v, onset="2021-01-25",
        xcorr_window=("2020-10-01", "2021-02-15"), max_lag=8)
    results["gamestop"] = res
    plotdata["gamestop"] = pd

    # ---- EVENT 2: AskEconomics 2025 tariff shock (exogenous / contrast) ----
    agg_d2, agg_v2 = sum_series("askecon_overall_2025")  # single key, reuse helper
    ent_d2, ent_v2 = sum_series("askecon_tariff_2025", "askecon_trump_2025")
    # tariff onset: "Liberation Day" reciprocal tariffs 2025-04-02; onset week 2025-03-31
    res2, pd2 = run_event(
        "AskEconomics 2025 tariff shock (tariff/Trump vs AskEconomics)",
        ent_d2, ent_v2, agg_d2, agg_v2, onset="2025-03-31",
        xcorr_window=("2025-01-06", "2025-05-05"), max_lag=6)
    results["askecon_tariff_2025"] = res2
    plotdata["askecon_tariff_2025"] = pd2

    # ---- EVENT 3: AskEconomics 2022 inflation surge (exogenous / contrast) ----
    agg_d3, agg_v3 = sum_series("askecon_overall_2022")
    ent_d3, ent_v3 = sum_series("askecon_inflation_2022", "askecon_fed_2022")
    # 2022-02-10: Jan-2022 CPI print 7.5% (40-yr high), surge in AskEconomics traffic
    res3, pd3 = run_event(
        "AskEconomics 2022 inflation surge (inflation/Fed vs AskEconomics)",
        ent_d3, ent_v3, agg_d3, agg_v3, onset="2022-02-07",
        xcorr_window=("2021-11-01", "2022-03-14"), max_lag=6)
    results["askecon_inflation_2022"] = res3
    plotdata["askecon_inflation_2022"] = pd3

    json.dump(results, open(os.path.join(HERE, "results.json"), "w"), indent=2)
    print("\nSAVED results.json")
    for k, r in results.items():
        b = r["buildup"]
        print(f"  {k:24s} guard_lead={r['lead_weeks_guarded']:+d}w (raw{r['lead_weeks_growth_xcorr_raw']:+d}) "
              f"ramp_run={b['ramp_run_weeks_into_onset']}w slope={b.get('weekly_growth_pct')}% "
              f"buildup={b['buildup_factor']:+d} score={r['operator_led_score']:+.2f}  {r['classification']}")
    return results, plotdata


# --------------------------------------------------------------------------- #
def make_figure(results, plotdata):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    order = ["gamestop", "askecon_tariff_2025", "askecon_inflation_2022"]
    titles = {
        "gamestop": "GameStop — DFV/RoaringKitty (operator) vs r/wallstreetbets (aggregate)",
        "askecon_tariff_2025": "AskEconomics 2025 tariff shock — tariff/Trump vs aggregate",
        "askecon_inflation_2022": "AskEconomics 2022 inflation surge — inflation/Fed vs aggregate",
    }
    fig, axes = plt.subplots(3, 1, figsize=(12, 13))
    for ax, key in zip(axes, order):
        pd = plotdata[key]
        r = results[key]
        onset = pd["onset"]
        # restrict the plot to the xcorr window so the run-up is visible
        wlo = datetime.date.fromisoformat(r["xcorr_window"][0])
        whi = datetime.date.fromisoformat(r["xcorr_window"][1])
        idx = [i for i, d in enumerate(pd["common"]) if wlo <= d <= whi]
        common = [pd["common"][i] for i in idx]
        driver = pd["driver"][idx]
        agg = pd["aggregate"][idx]
        ax2 = ax.twinx()
        l1, = ax.plot(common, agg, color="tab:blue", lw=1.8, marker=".", label="aggregate activity")
        l2, = ax2.plot(common, driver, color="tab:red", lw=1.8, marker=".", label="driver/operator signal")
        ax.axvline(onset, color="black", ls="--", lw=1.2)
        ax.annotate("onset", (onset, ax.get_ylim()[1]), color="black", fontsize=8,
                    ha="left", va="top")
        # shade the operator pre-onset ramp run (the priming window)
        run = r["buildup"]["ramp_run_weeks_into_onset"]
        if run >= 1:
            ramp_start = onset - datetime.timedelta(weeks=run)
            ax.axvspan(ramp_start, onset, color="green", alpha=0.08)
            ax.annotate(f"operator ramp {run}wk", (ramp_start, ax.get_ylim()[1]),
                        color="green", fontsize=8, ha="left", va="top")
        gl = r["lead_weeks_guarded"]
        ax.set_title(f"{titles[key]}\nguarded growth-lead={gl:+d}w  ramp_run={run}wk  "
                     f"buildup={r['buildup']['buildup_factor']:+d}  score={r['operator_led_score']:+.2f}  "
                     f"=>  {r['classification']}", fontsize=10)
        ax.set_ylabel("aggregate (posts/hr)", color="tab:blue")
        ax2.set_ylabel("driver (mentions/hr)", color="tab:red")
        ax.tick_params(axis="y", labelcolor="tab:blue")
        ax2.tick_params(axis="y", labelcolor="tab:red")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        ax.grid(alpha=0.3)
        ax.legend([l1, l2], ["aggregate", "driver/operator"], loc="upper left", fontsize=8)
    plt.tight_layout()
    out = os.path.join(HERE, "figure_major_player.png")
    plt.savefig(out, dpi=110)
    print("SAVED", out)


# --------------------------------------------------------------------------- #
def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("all", "harvest"):
        print("=== harvesting AskEconomics aggregate + entity series ===")
        harvest_askecon()
    if mode in ("all", "analyze"):
        results, plotdata = analyze()
        make_figure(results, plotdata)


if __name__ == "__main__":
    main()
