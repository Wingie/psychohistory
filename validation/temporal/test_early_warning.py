#!/usr/bin/env py -3.12
"""
Test (iii) EARLY-WARNING SIGNALS  --  critical slowing down before a cascade.

HYPOTHESIS (paper: criticality with early-warning):
    As a system approaches a tipping point / cascade, it exhibits "critical
    slowing down": rising VARIANCE, rising LAG-1 AUTOCORRELATION, and (across
    communities) rising CROSS-COMMUNITY CORRELATION in the window BEFORE the
    cascade.

THE PROSECUTOR'S-FALLACY GUARD (the whole point of this script):
    Showing the indicators "rose before the cascade" is worthless on its own,
    because indicators rise before lots of non-events too. P(signal | cascade)
    is NOT P(cascade | signal). So we build a BASE RATE: we slide the SAME
    pre-window detector across all comparable NON-cascade periods and ask how
    often it fires there. We report:
        - the indicator's pre-cascade value(s),
        - the distribution of the same statistic over all non-cascade windows
          (the base rate / null),
        - the percentile / z of the cascade window within that null,
        - an AUC-style separation: P(cascade window scores higher than a random
          non-cascade window).
    A real early-warning capability requires the cascade window to sit far in
    the tail of the base-rate distribution.

WHAT THIS SCRIPT DOES
    1. Ingest a univariate time series: either
         (a) a per-bucket count series JSON: {"sub": [["2024-01-01", 833], ...]}
             (pass --series-key sub), or a bare list [["date",count],...], or
         (b) raw submissions (NDJSON / JSON list / pullpush-arctic envelope),
             which it buckets into counts per --bin (day|week).
    2. Optionally compute the activity series' anomaly (remove slow trend).
    3. Rolling window: variance and lag-1 autocorrelation (AR1).
    4. Accept a labeled cascade date (--cascade YYYY-MM-DD). The "pre-cascade
       window" is the --lead buckets immediately before it.
    5. Score the pre-cascade window by a composite (var rise + AR1 rise relative
       to each window's own earlier baseline). Slide the identical scorer over
       every other window of the series to form the base rate, EXCLUDING windows
       overlapping the cascade. Report base rate, percentile, AUC.

EXPECTED DATA FORMAT
    A single community's activity over time, long enough that the pre-cascade
    lead window is a small fraction of the series (rule of thumb: >= 30 buckets,
    ideally >= 60). Monthly counts over several years, or weekly counts over a
    year+, work well.

USAGE
    # from a precomputed monthly count series
    py -3.12 test_early_warning.py data/monthly_submissions.json \\
        --series-key europe --cascade 2022-02-01 --lead 3 --window 6
    # from raw submissions bucketed weekly
    py -3.12 test_early_warning.py data/loc_europe.ndjson --bin week \\
        --cascade 2025-05-08 --lead 3 --window 6
"""
import sys, json, argparse, math, statistics, datetime
from collections import defaultdict


def load_any(path):
    txt = open(path, encoding="utf-8").read().strip()
    try:
        obj = json.loads(txt)
        return ("json", obj)
    except Exception:
        recs = []
        for line in txt.splitlines():
            line = line.strip()
            if line:
                try:
                    recs.append(json.loads(line))
                except Exception:
                    pass
        return ("ndjson", recs)


def to_date(s):
    return datetime.date.fromisoformat(str(s)[:10])


def get_ts(r):
    for k in ("created_utc", "created"):
        if r.get(k) is not None:
            try:
                return float(r[k])
            except Exception:
                pass
    return None


def build_series(path, series_key, binmode):
    kind, obj = load_any(path)
    # case A: precomputed series
    if kind == "json":
        series = None
        if isinstance(obj, dict) and series_key and series_key in obj:
            series = obj[series_key]
        elif isinstance(obj, list) and obj and isinstance(obj[0], (list, tuple)):
            series = obj
        elif isinstance(obj, dict) and "data" in obj and isinstance(obj["data"], list) \
                and obj["data"] and isinstance(obj["data"][0], dict) and "created_utc" in obj["data"][0]:
            # arctic aggregate envelope
            series = [[d["created_utc"][:10], int(d.get("count", d.get("doc_count", 0)))]
                      for d in obj["data"]]
        if series is not None:
            pairs = [(to_date(d), float(c)) for d, c in series]
            pairs.sort()
            return [d for d, _ in pairs], [c for _, c in pairs]
        # else: maybe a JSON list of submission dicts
        if isinstance(obj, list) and obj and isinstance(obj[0], dict):
            recs = obj
        elif isinstance(obj, dict) and isinstance(obj.get("data"), list):
            recs = obj["data"]
        else:
            raise SystemExit("Could not interpret JSON; pass --series-key or give submissions.")
    else:
        recs = obj
    # case B: bucket raw submissions
    buckets = defaultdict(int)
    for r in recs:
        ts = get_ts(r)
        if ts is None:
            continue
        d = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).date()
        if binmode == "week":
            d = d - datetime.timedelta(days=d.weekday())
        elif binmode == "month":
            d = d.replace(day=1)
        buckets[d] += 1
    if not buckets:
        raise SystemExit("No timestamped records found.")
    # fill gaps
    lo, hi = min(buckets), max(buckets)
    step = {"day": 1, "week": 7}.get(binmode, 1)
    dates, vals = [], []
    cur = lo
    while cur <= hi:
        dates.append(cur)
        vals.append(float(buckets.get(cur, 0)))
        if binmode == "month":
            y, m = cur.year, cur.month + 1
            if m > 12:
                y, m = y + 1, 1
            cur = datetime.date(y, m, 1)
        else:
            cur = cur + datetime.timedelta(days=step)
    return dates, vals


def ar1(x):
    n = len(x)
    if n < 3:
        return float("nan")
    m = sum(x) / n
    v = sum((xi - m) ** 2 for xi in x)
    if v == 0:
        return 0.0
    c = sum((x[i] - m) * (x[i + 1] - m) for i in range(n - 1))
    return c / v


def variance(x):
    return statistics.pvariance(x) if len(x) > 1 else 0.0


def window_score(vals, i, window):
    """Composite EWS score for the window ENDING at index i-1 (the lead window),
    relative to the equal-length baseline before it. Higher = stronger warning."""
    lead = vals[i - window:i]
    base = vals[i - 2 * window:i - window]
    if len(lead) < window or len(base) < window:
        return None
    v_lead, v_base = variance(lead), variance(base)
    a_lead, a_base = ar1(lead), ar1(base)
    # relative rises; guard zeros
    dv = (v_lead - v_base) / (v_base + 1e-9)
    da = a_lead - a_base
    if math.isnan(da):
        da = 0.0
    return dv + da, dict(var_lead=v_lead, var_base=v_base, ar1_lead=a_lead, ar1_base=a_base)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infile")
    ap.add_argument("--series-key", default=None, help="key into a {name:series} JSON dict")
    ap.add_argument("--bin", choices=["day", "week", "month"], default="week",
                    help="bucket size when ingesting raw submissions")
    ap.add_argument("--cascade", required=True, help="labeled cascade date YYYY-MM-DD")
    ap.add_argument("--lead", type=int, default=3, help="(kept for CLI compat; window is the lead length)")
    ap.add_argument("--window", type=int, default=6, help="EWS rolling window length (buckets)")
    args = ap.parse_args()

    dates, vals = build_series(args.infile, args.series_key, args.bin)
    if len(vals) < 4 * args.window:
        print(f"VERDICT: INSUFFICIENT DATA - {len(vals)} buckets; need >= "
              f"{4*args.window} for a base rate at window={args.window}.")
        print(f"  series range: {dates[0]} .. {dates[-1]}")
        return

    casc = to_date(args.cascade)
    # index of first bucket >= cascade
    ci = next((k for k, d in enumerate(dates) if d >= casc), None)
    if ci is None or ci < 2 * args.window:
        print(f"VERDICT: CASCADE NOT USABLE - cascade {casc} maps to index {ci}; "
              f"need >= {2*args.window} prior buckets for the lead+baseline.")
        return

    casc_sc = window_score(vals, ci, args.window)
    if casc_sc is None:
        print("VERDICT: CASCADE NOT USABLE - not enough buckets before cascade.")
        return
    casc_score, casc_detail = casc_sc

    # base rate: slide scorer over all windows whose lead window does NOT overlap cascade lead
    null_scores = []
    casc_lead_lo, casc_lead_hi = ci - args.window, ci  # lead window indices
    for i in range(2 * args.window, len(vals) + 1):
        lead_lo, lead_hi = i - args.window, i
        # exclude any window overlapping the cascade lead window
        if not (lead_hi <= casc_lead_lo or lead_lo >= casc_lead_hi):
            continue
        sc = window_score(vals, i, args.window)
        if sc is not None:
            null_scores.append(sc[0])

    if len(null_scores) < 5:
        print(f"VERDICT: INSUFFICIENT NULL - only {len(null_scores)} non-cascade "
              f"windows. Need a longer series for a base rate.")
        return

    nm = statistics.mean(null_scores)
    nsd = statistics.pstdev(null_scores) or 1e-12
    z = (casc_score - nm) / nsd
    pct = sum(1 for s in null_scores if s < casc_score) / len(null_scores)
    auc = sum((1.0 if casc_score > s else 0.5 if casc_score == s else 0.0)
              for s in null_scores) / len(null_scores)
    base_rate_exceed = sum(1 for s in null_scores if s >= casc_score) / len(null_scores)

    print("=" * 64)
    print("TEST (iii) EARLY-WARNING SIGNALS  (critical slowing down)")
    print("=" * 64)
    print(f"input         : {args.infile}" + (f"  [{args.series_key}]" if args.series_key else ""))
    print(f"buckets       : {len(vals)} ({args.bin})  {dates[0]} .. {dates[-1]}")
    print(f"cascade label : {casc}  -> bucket index {ci} ({dates[ci] if ci < len(dates) else 'end'})")
    print(f"EWS window    : {args.window} buckets (lead vs equal baseline)")
    print("-" * 64)
    print("pre-cascade lead window indicators:")
    print(f"   variance   base={casc_detail['var_base']:.3g} -> lead={casc_detail['var_lead']:.3g}")
    print(f"   lag-1 AR   base={casc_detail['ar1_base']:+.3f} -> lead={casc_detail['ar1_lead']:+.3f}")
    print(f"   composite EWS score          : {casc_score:+.3f}")
    print("-" * 64)
    print(f"BASE RATE (null = {len(null_scores)} non-cascade windows):")
    print(f"   null score  mean +/- sd      : {nm:+.3f} +/- {nsd:.3f}")
    print(f"   cascade percentile in null   : {pct*100:.1f}%")
    print(f"   z vs base rate               : {z:+.2f}")
    print(f"   AUC (P[cascade > random null]): {auc:.3f}")
    print(f"   base-rate false-alarm share  : {base_rate_exceed*100:.1f}% of non-cascade "
          f"windows score >= cascade")
    print("-" * 64)
    if pct >= 0.90 and auc >= 0.80:
        print("VERDICT: SUPPORTS EARLY-WARNING - the pre-cascade window sits in the")
        print("         tail of the base rate; EWS separate cascade from non-events.")
    elif pct >= 0.75:
        print("VERDICT: WEAK SUPPORT - elevated vs base rate but not deep in the tail.")
        print("         Single cascade => anecdote; repeat across many labeled cascades.")
    else:
        print("VERDICT: NO EARLY-WARNING EDGE - the pre-cascade window is unremarkable")
        print("         against the base rate. 'It rose' would have been the fallacy.")
    print("NOTE: one cascade gives one point vs a null. Real validation aggregates")
    print("      AUC/percentile over MANY labeled cascades across communities.")


if __name__ == "__main__":
    main()
