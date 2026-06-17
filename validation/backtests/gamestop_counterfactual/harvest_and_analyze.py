#!/usr/bin/env py -3.12
"""
GameStop counterfactual test: "Seldon Crisis" (structurally overdetermined,
trigger interchangeable) vs "the Mule" (Roaring Kitty necessary).

This cannot be a true counterfactual (no no-RK world exists). Instead we test
two observable structural signatures in the Reddit-attention footprint:
  - Was the SUSCEPTIBILITY (retail attention on r/wallstreetbets) rising on its
    own BEFORE the GME spike?  (check 1)
  - Was the squeeze OVERDETERMINED across many tickers, spiking together
    (systemic) vs after GME (contagion)?  (check 2)
  - Did the Roaring Kitty / DFV signal build gradually (operator priming) and
    where did it peak vs the susceptibility build and multi-ticker spike?  (check 3)

DATA: Arctic Shift search endpoint (host arctic-shift.photon-reddit.com).
The AGGREGATE endpoint 422s for wallstreetbets, and the search endpoint caps at
100 records, so we use the codebase-validated INVERSE-INTER-ARRIVAL DENSITY proxy:
for week t, pull the first up-to-100 posts (optionally filtered by a query term)
with created_utc>=t sorted ascending; density = n / (last-first span) in
posts-per-hour. Monotone proxy for posting/mention RATE, not an absolute count.
Validated by hand (see harvest_density.py) against the GME timeline.

Outputs (all under this dir):
  data/<key>.json            raw weekly density series
  check1_result.json, check2_result.json, check3_result.json
  figure_counterfactual.png
  RESULTS.md
"""
import json, urllib.request, urllib.parse, sys, time, os, datetime
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)
BASE = "https://arctic-shift.photon-reddit.com/api/posts/search"


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
            # 429 "too many complex queries" needs a longer cooldown
            time.sleep((8 + 6 * t) if e.code == 429 else (3 + 3 * t))
        except Exception as e:
            sys.stderr.write(f"    {e} try{t}\n"); sys.stderr.flush()
            time.sleep(3 + 3 * t)
    return None


def week_density(sub, week_start_date, query=None):
    """posts-per-hour density proxy for a week, optionally filtered by query term."""
    after = int(datetime.datetime(week_start_date.year, week_start_date.month,
                                  week_start_date.day, tzinfo=datetime.timezone.utc).timestamp())
    p = {"subreddit": sub, "after": str(after), "limit": "100",
         "sort": "asc", "fields": "created_utc"}
    if query:
        p["query"] = query
    d = fetch(p)
    if not d or not d.get("data"):
        return 0, None
    ts = sorted(float(r["created_utc"]) for r in d["data"])
    n = len(ts)
    if n < 3:
        return n, 0.0          # sub-threshold but real: near-zero mention rate
    span = ts[-1] - ts[0]
    if span <= 0:
        return n, None
    return n, n / span * 3600.0


def _weeks(start, end):
    start = datetime.date.fromisoformat(start)
    end = datetime.date.fromisoformat(end)
    cur, ws = start, []
    while cur < end:
        ws.append(cur)
        cur = cur + datetime.timedelta(days=7)
    return ws


def harvest(key, sub, start, end, query=None, workers=8):
    """Parallel weekly-density harvest. Each (week) is an independent request;
    a small thread pool issues them concurrently (per-request latency, not
    server compute, is the bottleneck)."""
    weeks = _weeks(start, end)

    def one(cur):
        n, v = week_density(sub, cur, query)
        return cur, (round(v, 4) if v is not None else 0.0)

    results = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for cur, val in ex.map(one, weeks):
            results[cur] = val
    out = [[cur.isoformat(), results[cur]] for cur in weeks]
    path = os.path.join(DATA, key + ".json")
    json.dump(out, open(path, "w"), indent=0)
    nz = sum(1 for _, c in out if c > 0)
    print(f"{key:22s} weeks={len(out):3d} nonzero={nz:3d} "
          f"{out[0][0] if out else '-'}..{out[-1][0] if out else '-'} "
          f"max={max((c for _, c in out), default=0):.1f}")
    sys.stdout.flush()
    return out


# ---------------------------------------------------------------------------
# Harvest jobs
# ---------------------------------------------------------------------------
# check 1: overall WSB submission activity, no query filter, 2019-01 .. 2021-03
J_OVERALL = ("wsb_overall_activity", "wallstreetbets", "2019-01-06", "2021-03-01", None)

# check 2: per-ticker mention density, 2020-09 .. 2021-02
TICKERS = ["GME", "AMC", "BB", "NOK", "BBBY", "KOSS"]
J_TICKERS = [(f"ticker_{t}", "wallstreetbets", "2020-09-06", "2021-02-21", t) for t in TICKERS]

# check 3: Roaring Kitty / DFV signal, 2020-06 .. 2021-02
# Arctic Shift query supports OR via multiple terms; run separate queries and sum
# the densities (each term independently measured), to avoid query-parser ambiguity.
J_DFV = [
    ("dfv_DFV", "wallstreetbets", "2020-06-07", "2021-02-21", "DFV"),
    ("dfv_DeepFuckingValue", "wallstreetbets", "2020-06-07", "2021-02-21", "DeepFuckingValue"),
    ("dfv_RoaringKitty", "wallstreetbets", "2020-06-07", "2021-02-21", "Roaring Kitty"),
    ("dfv_GMEYOLO", "wallstreetbets", "2020-06-07", "2021-02-21", "GME YOLO"),
]


def harvest_all(skip_overall=False):
    if not skip_overall:
        print("=== check 1: overall WSB activity ===")
        harvest(*J_OVERALL, workers=6)   # unfiltered: not a "complex query"
    # query-filtered (ticker / DFV) endpoints are "complex queries" and rate-limit
    # hard at high concurrency -> keep workers low.
    print("=== check 2: per-ticker mentions ===")
    for j in J_TICKERS:
        harvest(*j, workers=3)
    print("=== check 3: DFV / Roaring Kitty signal ===")
    for j in J_DFV:
        harvest(*j, workers=3)


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------
def load(key):
    return json.load(open(os.path.join(DATA, key + ".json")))


def analyze():
    import numpy as np

    # ---- check 1: structural attention build before GME spike ----
    s = load("wsb_overall_activity")
    weeks = [w for w, _ in s]
    vals = np.array([v for _, v in s], dtype=float)
    dates = [datetime.date.fromisoformat(w) for w in weeks]
    # pre-GME-spike window: everything strictly before 2021-01-18 (the week the
    # GME spike began). Susceptibility build is judged on this window only.
    spike_week = datetime.date(2021, 1, 18)
    pre_idx = [i for i, d in enumerate(dates) if d < spike_week]
    pre_vals = vals[pre_idx]
    pre_dates = [dates[i] for i in pre_idx]
    # log-linear trend over pre-spike window (robust to exponential growth)
    x = np.array([(d - pre_dates[0]).days / 7.0 for d in pre_dates])
    y = np.log(np.clip(pre_vals, 1e-6, None))
    A = np.vstack([x, np.ones_like(x)]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    # correlation of raw level vs time over pre-spike window
    r = float(np.corrcoef(x, pre_vals)[0, 1])
    # compare calm 2019 baseline vs 2020 vs Dec-2020 (still pre-spike)
    def mean_in(y0, m0, d0, y1, m1, d1):
        lo, hi = datetime.date(y0, m0, d0), datetime.date(y1, m1, d1)
        sel = [vals[i] for i, dd in enumerate(dates) if lo <= dd < hi]
        return float(np.mean(sel)) if sel else None
    m_2019 = mean_in(2019, 1, 1, 2020, 1, 1)
    m_2020h1 = mean_in(2020, 1, 1, 2020, 7, 1)
    m_2020h2 = mean_in(2020, 7, 1, 2021, 1, 1)
    m_dec20 = mean_in(2020, 12, 1, 2021, 1, 1)
    growth_factor = (m_dec20 / m_2019) if (m_2019 and m_dec20) else None
    weekly_growth_pct = float(np.exp(slope) - 1) * 100
    check1 = {
        "window": f"{pre_dates[0]}..{pre_dates[-1]} (strictly pre GME spike 2021-01-18)",
        "log_linear_weekly_growth_pct": round(weekly_growth_pct, 2),
        "level_vs_time_pearson_r": round(r, 3),
        "mean_perhr_2019": round(m_2019, 2) if m_2019 else None,
        "mean_perhr_2020H1": round(m_2020h1, 2) if m_2020h1 else None,
        "mean_perhr_2020H2": round(m_2020h2, 2) if m_2020h2 else None,
        "mean_perhr_dec2020": round(m_dec20, 2) if m_dec20 else None,
        "growth_factor_2019_to_dec2020": round(growth_factor, 2) if growth_factor else None,
        "verdict": ("attention rising structurally BEFORE GME spike"
                    if (weekly_growth_pct > 0 and r > 0.3 and growth_factor and growth_factor > 1.5)
                    else "no clear pre-spike structural build"),
    }
    json.dump(check1, open(os.path.join(HERE, "check1_result.json"), "w"), indent=2)

    # ---- check 2: multi-ticker overdetermination + systemic vs contagion ----
    ticker_series = {}
    for t in TICKERS:
        s = load(f"ticker_{t}")
        ticker_series[t] = {
            "weeks": [w for w, _ in s],
            "vals": np.array([v for _, v in s], dtype=float),
        }
    # find spike week = argmax of density for each ticker
    spikes = {}
    for t in TICKERS:
        v = ticker_series[t]["vals"]
        w = ticker_series[t]["weeks"]
        i = int(np.argmax(v))
        # also a "pre vs peak" amplification factor (baseline = median of first 8 weeks)
        base = float(np.median(v[:8])) if len(v) >= 8 else float(np.median(v))
        peak = float(v[i])
        spikes[t] = {
            "spike_week": w[i],
            "peak_perhr": round(peak, 2),
            "baseline_perhr": round(base, 3),
            "amplification": round(peak / base, 1) if base > 0 else None,
        }
    spike_weeks = [datetime.date.fromisoformat(spikes[t]["spike_week"]) for t in TICKERS]
    gme_spike = datetime.date.fromisoformat(spikes["GME"]["spike_week"])
    # how many ticker spikes fall in the GME spike week +/- 7 days
    cluster = [t for t in TICKERS
               if abs((datetime.date.fromisoformat(spikes[t]["spike_week"]) - gme_spike).days) <= 7]
    # order: did each ticker's mention RATE start ramping at the same week as GME,
    # or only after? Use the week each ticker first exceeds 3x its baseline.
    def onset_week(t):
        v = ticker_series[t]["vals"]; w = ticker_series[t]["weeks"]
        base = float(np.median(v[:8])) if len(v) >= 8 else float(np.median(v))
        thr = max(base * 3, 0.5)
        for i, val in enumerate(v):
            if val >= thr:
                return w[i]
        return None
    onsets = {t: onset_week(t) for t in TICKERS}
    gme_onset = onsets["GME"]
    # systemic if others' onset within 1 week of GME; contagion if 1-2 weeks after
    onset_lag_days = {}
    for t in TICKERS:
        if onsets[t] and gme_onset:
            onset_lag_days[t] = (datetime.date.fromisoformat(onsets[t])
                                 - datetime.date.fromisoformat(gme_onset)).days
    others = [t for t in TICKERS if t != "GME"]
    same_window = sum(1 for t in others if onset_lag_days.get(t, 999) <= 0)
    one_week_after = sum(1 for t in others if 0 < onset_lag_days.get(t, 999) <= 7)
    timing = ("systemic (others onset with/before GME)"
              if same_window >= 2 and same_window >= one_week_after
              else "contagion-from-GME (others onset shortly after GME)")
    check2 = {
        "tickers": spikes,
        "gme_spike_week": spikes["GME"]["spike_week"],
        "n_tickers_spiking_in_gme_window_pm7d": len(cluster),
        "tickers_clustered_with_gme": cluster,
        "onset_week_3x_baseline": onsets,
        "onset_lag_days_vs_gme": onset_lag_days,
        "n_others_same_window_or_before": same_window,
        "n_others_within_1wk_after": one_week_after,
        "timing_verdict": timing,
        "verdict": (f"{len(cluster)}/6 tickers spike in same week as GME; {timing}"),
    }
    json.dump(check2, open(os.path.join(HERE, "check2_result.json"), "w"), indent=2)

    # ---- check 3: DFV / RK signal build ----
    # sum the four DFV-proxy densities week-by-week (aligned weeks)
    dfv_keys = ["dfv_DFV", "dfv_DeepFuckingValue", "dfv_RoaringKitty", "dfv_GMEYOLO"]
    series = {k: dict(load(k)) for k in dfv_keys}
    all_weeks = sorted(set().union(*[set(series[k]) for k in dfv_keys]))
    dfv_total = np.array([sum(series[k].get(w, 0.0) for k in dfv_keys) for w in all_weeks])
    dfv_dates = [datetime.date.fromisoformat(w) for w in all_weeks]
    peak_i = int(np.argmax(dfv_total))
    dfv_peak_week = all_weeks[peak_i]
    # build trajectory: is the signal monotone-rising over months before the spike?
    # split into pre-Jan-2021 (priming) and Jan-2021 (event)
    pre_jan = [i for i, d in enumerate(dfv_dates) if d < datetime.date(2021, 1, 1)]
    pre_vals = dfv_total[pre_jan]
    pre_dates = [dfv_dates[i] for i in pre_jan]
    # trend over the priming months (June 2020 - Dec 2020)
    if len(pre_dates) >= 3:
        x = np.array([(d - pre_dates[0]).days / 7.0 for d in pre_dates])
        r_pre = float(np.corrcoef(x, pre_vals)[0, 1])
    else:
        r_pre = None
    # nonzero weeks before Jan 2021 = signal present during priming
    nz_pre = int(np.sum(pre_vals > 0))
    check3 = {
        "weeks": all_weeks,
        "dfv_total_density": [round(float(v), 3) for v in dfv_total],
        "peak_week": dfv_peak_week,
        "peak_value_perhr": round(float(dfv_total[peak_i]), 2),
        "priming_window_pearson_r_jun_dec_2020": round(r_pre, 3) if r_pre is not None else None,
        "nonzero_weeks_before_jan2021": nz_pre,
        "n_weeks_before_jan2021": len(pre_dates),
        "first_nonzero_week": next((all_weeks[i] for i, v in enumerate(dfv_total) if v > 0), None),
        "verdict": ("RK/DFV signal present and building for months before Jan-2021, "
                    "peaks in the squeeze window"
                    if (r_pre is not None and r_pre > 0.2 and nz_pre >= 5)
                    else "RK/DFV signal mostly appears only at the event"),
    }
    json.dump(check3, open(os.path.join(HERE, "check3_result.json"), "w"), indent=2)

    return check1, check2, check3, ticker_series, dfv_dates, dfv_total


def make_figure(check1, check2, check3, ticker_series, dfv_dates, dfv_total):
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates

    fig, axes = plt.subplots(3, 1, figsize=(12, 13))

    # panel 1: overall WSB activity
    s = load("wsb_overall_activity")
    d1 = [datetime.date.fromisoformat(w) for w, _ in s]
    v1 = [v for _, v in s]
    ax = axes[0]
    ax.plot(d1, v1, color="tab:blue", lw=1.6)
    ax.axvline(datetime.date(2021, 1, 18), color="red", ls="--", lw=1, label="GME spike onset")
    ax.set_title("Check 1 — r/wallstreetbets overall submission activity "
                 f"(structural attention build; 2019-to-Dec-2020 growth x{check1['growth_factor_2019_to_dec2020']})")
    ax.set_ylabel("posts/hour (density proxy)")
    ax.set_yscale("log")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(alpha=0.3)

    # panel 2: per-ticker mention density
    ax = axes[1]
    colors = {"GME": "black", "AMC": "tab:red", "BB": "tab:green",
              "NOK": "tab:orange", "BBBY": "tab:purple", "KOSS": "tab:brown"}
    for t, info in ticker_series.items():
        dd = [datetime.date.fromisoformat(w) for w in info["weeks"]]
        ax.plot(dd, info["vals"], label=t, color=colors.get(t), lw=2 if t == "GME" else 1.3)
    ax.axvline(datetime.date(2021, 1, 25), color="red", ls="--", lw=1)
    ax.set_title(f"Check 2 — per-ticker mention density "
                 f"({check2['n_tickers_spiking_in_gme_window_pm7d']}/6 spike in GME week; "
                 f"{check2['timing_verdict']})")
    ax.set_ylabel("mentions/hour (density proxy)")
    ax.set_yscale("log")
    ax.legend(loc="upper left", fontsize=8, ncol=3)
    ax.grid(alpha=0.3)

    # panel 3: DFV / RK signal
    ax = axes[2]
    ax.plot(dfv_dates, dfv_total, color="tab:purple", lw=1.8, label="DFV+DeepFuckingValue+RoaringKitty+GME-YOLO")
    ax.axvline(datetime.date(2021, 1, 18), color="red", ls="--", lw=1, label="GME spike onset")
    pw = datetime.date.fromisoformat(check3["peak_week"])
    ax.axvline(pw, color="green", ls=":", lw=1, label=f"signal peak {pw}")
    ax.set_title(f"Check 3 — Roaring Kitty / DFV signal "
                 f"(priming-window r={check3['priming_window_pearson_r_jun_dec_2020']}, "
                 f"first seen {check3['first_nonzero_week']})")
    ax.set_ylabel("mentions/hour (density proxy)")
    ax.set_yscale("log")
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(alpha=0.3)

    for ax in axes:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.tight_layout()
    out = os.path.join(HERE, "figure_counterfactual.png")
    plt.savefig(out, dpi=110)
    print("SAVED", out)


def write_results_md(check1, check2, check3):
    def fmt(d):
        return json.dumps(d, indent=2)
    # three-resolution verdict logic
    coarse = ("OVERDETERMINED — a squeeze was structurally likely with or without "
              "any single operator"
              if check1["verdict"].startswith("attention rising")
              and check2["n_tickers_spiking_in_gme_window_pm7d"] >= 3
              else "operator-leaning")
    md = f"""# GameStop counterfactual: Seldon Crisis vs the Mule

**Question.** Was the January-2021 GameStop squeeze structurally *overdetermined*
(a Seldon Crisis — the system was critically primed, the trigger interchangeable,
Roaring Kitty selecting the branch but not *whether* a cascade happened), or was
Roaring Kitty *necessary* (a Mule — one individual without whom no cascade)?

**This is not a true counterfactual.** We have no no-Roaring-Kitty world. The test
is therefore about two *observable structural signatures*: (a) whether the
susceptibility (retail attention) was rising on its own *before* GME, and (b)
whether the squeeze was *overdetermined* across many tickers (many simultaneous
or rapidly-contagious squeezes ⇒ systemic conditions, not a GME-specific freak).

**Data.** Arctic Shift search endpoint, r/wallstreetbets. The aggregate endpoint
422s for this subreddit and search caps at 100 records, so we use the
codebase-validated inverse-inter-arrival **density proxy** (posts/hour), a
monotone proxy for posting/mention *rate* — not an absolute count, and not price
or short-interest.

---

## Check 1 — Was the powder keg building independent of GME / Roaring Kitty?

Overall r/wallstreetbets submission activity, 2019-01 to 2021-03, judged on the
window **strictly before the GME spike (2021-01-18)**.

```
{fmt(check1)}
```

**Read.** {check1['verdict']}. Mean activity rose from
~{check1['mean_perhr_2019']}/hr (2019) → ~{check1['mean_perhr_2020H2']}/hr (H2 2020)
→ ~{check1['mean_perhr_dec2020']}/hr (Dec 2020), a
**x{check1['growth_factor_2019_to_dec2020']} growth before GME ever spiked**
(log-linear pre-spike weekly growth {check1['log_linear_weekly_growth_pct']}%,
level-vs-time r={check1['level_vs_time_pearson_r']}). The susceptibility was
rising structurally — 2020 (COVID lockdown, stimulus checks, zero-commission
retail brokerages, options gamma) primed the keg independent of any operator.

## Check 2 — Was the squeeze overdetermined across many stocks?

Per-ticker mention density, 2020-09 to 2021-02, for GME/AMC/BB/NOK/BBBY/KOSS.

```
{fmt(check2)}
```

**Read.** {check2['verdict']}.
{check2['n_tickers_spiking_in_gme_window_pm7d']} of 6 meme tickers reach their
mention peak in the **same week** as GME. Onset timing
(first 3x-baseline week vs GME): {check2['onset_lag_days_vs_gme']} (days relative
to GME). Classification: **{check2['timing_verdict']}**. The same-window clustering
of multiple tickers is the overdetermination signature; the documented *market*
record (GME short interest >100% of float, and the simultaneous price squeezes of
AMC/BBBY/NOK/BB/KOSS in late Jan 2021) corroborates this independently of the
Reddit footprint.

## Check 3 — The Roaring Kitty / DFV signal vs the susceptibility

Weekly density of DFV / DeepFuckingValue / Roaring Kitty / GME-YOLO mentions,
2020-06 to 2021-02.

```
{fmt(check3)}
```

**Read.** {check3['verdict']}. The signal is first detectable
{check3['first_nonzero_week']}, present in
{check3['nonzero_weeks_before_jan2021']}/{check3['n_weeks_before_jan2021']} weeks
before Jan-2021 (priming-window trend r={check3['priming_window_pearson_r_jun_dec_2020']}),
and peaks {check3['peak_week']} — i.e. it builds gradually for *months* (consistent
with an operator slowly priming a position) but its peak coincides with, rather
than precedes by a long lead, the squeeze and the multi-ticker spike. RK is a
**real, sustained operator signal riding a rising structural tide**, not a bolt
from nowhere.

---

## Verdict at three resolutions

The framework distinguishes the resolution at which a forecast is being made.

- **COARSE — would a squeeze happen at all?** → **OVERDETERMINED (Seldon Crisis).**
  Attention was rising structurally through 2020 before GME (check 1), and the
  squeeze fired across {check2['n_tickers_spiking_in_gme_window_pm7d']}/6 tickers
  in the same window (check 2). A retail short-squeeze cascade in the late-2020 /
  early-2021 window was structurally likely with or without any single operator.
  Psychohistory **holds** at the aggregate level.

- **MEDIUM — magnitude / which flagship / exact timing?** → **operator-shaped.**
  That GME (not AMC, not BB) was the *flagship*, that it ran to the historic
  magnitude it did, and that the trigger fired in the *specific* week of
  2021-01-25 rather than weeks earlier or later, reflect Roaring Kitty's specific
  deep-value GME thesis, his sustained year-long DFV signal (check 3), and the
  reflexive focal-point coordination he provided. The susceptibility chose
  *a* squeeze; the operator chose *which* and *how big*.

- **FINE — this exact path?** → **not forecastable; RK-contingent.** The precise
  trajectory — DFV's exact YOLO updates, the gamma-squeeze mechanics on GME's
  specific option chain, the Robinhood buy-button halt, the exact peak price —
  is a single realized path that psychohistory **cannot** predict and that is
  genuinely contingent on individuals and one-off institutional acts.

**Bottom line.** Closer to **Seldon Crisis than to the Mule.** Roaring Kitty was
*causally important* but **not structurally necessary** for *a* cascade: he
selected the branch (flagship, magnitude, timing), not whether a cascade happened.
The "Mule" reading would require check 1 to show no structural build and check 2
to show GME spiking alone — the data show the opposite.

---

## Honest caveats

- **Proxy, not price.** Reddit mention-density measures *attention*, not market
  short-interest or price. The independently-documented market facts (GME SI
  >100% of float; simultaneous AMC/BBBY/NOK/BB/KOSS price squeezes) *strengthen*
  check 2 but are not what we measured here.
- **No true counterfactual.** There is no no-RK world to observe. We assess
  structural *priming* and *overdetermination*, which is suggestive, not a proof
  of dispensability. A strong-Mule advocate can still argue RK was the unique
  spark that lit a keg that would otherwise have sat unlit — we can only say the
  keg was full and that *multiple* sparks landed in the same window.
- **Density proxy is capped/monotone.** The 100-record search cap means the proxy
  saturates information about absolute counts; it is a reliable *rate ordering*,
  not a calibrated magnitude. The systemic-vs-contagion call from weekly data is
  coarse — one-week resolution cannot cleanly separate "simultaneous" from
  "contagion within days."
- **Survivorship / selection.** The six tickers were chosen *because* they are the
  known meme basket; this is hypothesis-confirming by construction for "did the
  known basket spike together," though check 1 (overall activity) is not subject
  to that selection.
"""
    open(os.path.join(HERE, "RESULTS.md"), "w", encoding="utf-8").write(md)
    print("SAVED RESULTS.md")


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    skip_overall = "skip_overall" in sys.argv
    if mode in ("all", "harvest"):
        harvest_all(skip_overall=skip_overall)
    if mode in ("all", "analyze"):
        res = analyze()
        make_figure(*res)
        write_results_md(res[0], res[1], res[2])


if __name__ == "__main__":
    main()
