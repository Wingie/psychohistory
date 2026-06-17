#!/usr/bin/env py -3.12
"""
Test (ii) LOCATION-SUBREDDIT SYNCHRONY  --  block decomposition & criticality.

HYPOTHESIS (paper: near-decomposable community BLOCKS; criticality/synchronization):
    Treat location subreddits (r/germany, r/france, r/italy, r/spain, r/europe,
    ...) as quasi-independent community BLOCKS. Under NORMAL conditions the
    blocks fluctuate fairly independently, so the effective number of
    independent blocks N_eff is close to the actual count K. Under a SHARED
    SHOCK (a continental / global event) the blocks SYNCHRONISE: cross-block
    activity correlation rises and N_eff COLLAPSES toward 1. That collapse is
    the criticality / loss-of-independence signature.

THE N_eff STATISTIC (macro variance-ratio / order-parameter, NOT Pearson-of-fluctuations):
    For K blocks with per-bucket (z-scored) activity x_k(t), the AGGREGATE is
    X(t) = sum_k x_k(t). If blocks were independent, Var(X) ~ sum_k Var(x_k).
    If they synchronise, Var(X) -> (sum_k sd_k)^2. Define
        N_eff(t-window) = (sum_k Var(x_k)) / Var(sum_k x_k)     (variance ratio)
    Independent => N_eff ~ K ; fully synchronised => N_eff ~ 1.
    We ALSO report a Kuramoto-style order parameter R on the SIGNS of the
    per-block fluctuations (fraction co-moving), as a second, robust view.
    Both are computed on a SLIDING window so we can watch N_eff over time and
    around labeled shock dates.

WHAT THIS SCRIPT DOES
    1. Ingest several blocks' activity series. Either:
         (a) one JSON dict {"germany": [["2024-01-01",N],...], "france":[...], ...}
             (e.g. data/monthly_submissions.json), or
         (b) several raw-submission files (NDJSON / JSON / envelope), one per
             block, named so the subreddit is recoverable, bucketed by --bin.
    2. Align blocks to a common time grid, z-score each block (so big and small
       subs contribute comparably).
    3. Sliding window: compute N_eff (variance ratio) and Kuramoto R.
    4. If --shock dates are given, compare N_eff in windows CONTAINING a shock
       vs all other windows (the base rate), reporting whether N_eff is
       significantly LOWER (more synchronised) around shocks.

EXPECTED DATA FORMAT
    >= 3 location blocks, overlapping in time, with >= ~2*window aligned buckets.
    Monthly counts over multiple years are ideal; weekly over a year works.

USAGE
    # precomputed multi-block series
    py -3.12 test_blocks_sync.py data/monthly_submissions.json \\
        --blocks germany france italy spain europe \\
        --window 6 --shock 2022-02-01 2020-03-01
    # several raw NDJSON files (block name = filename stem after 'loc_')
    py -3.12 test_blocks_sync.py data/loc_germany.ndjson data/loc_france.ndjson \\
        data/loc_italy.ndjson data/loc_spain.ndjson --bin week --window 4
"""
import sys, json, argparse, math, statistics, datetime, os
from collections import defaultdict


def load_any(path):
    txt = open(path, encoding="utf-8").read().strip()
    try:
        return ("json", json.loads(txt))
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


def get_ts(r):
    for k in ("created_utc", "created"):
        if r.get(k) is not None:
            try:
                return float(r[k])
            except Exception:
                pass
    return None


def block_name_from_file(path):
    stem = os.path.splitext(os.path.basename(path))[0]
    for pre in ("loc_", "sub_", "r_"):
        if stem.startswith(pre):
            stem = stem[len(pre):]
    return stem


def bucket_recs(recs, binmode):
    b = defaultdict(int)
    for r in recs:
        ts = get_ts(r)
        if ts is None:
            continue
        d = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).date()
        if binmode == "week":
            d = d - datetime.timedelta(days=d.weekday())
        elif binmode == "month":
            d = d.replace(day=1)
        b[d] += 1
    return b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--blocks", nargs="*", default=None,
                    help="block keys to use from a single JSON dict input")
    ap.add_argument("--bin", choices=["day", "week", "month"], default="week")
    ap.add_argument("--window", type=int, default=6)
    ap.add_argument("--shock", nargs="*", default=[], help="shock dates YYYY-MM-DD")
    args = ap.parse_args()

    # snap a date to the canonical bucket key for the chosen bin. Aggregation
    # APIs (e.g. Arctic Shift) emit period-start at 22:00 UTC of the PRIOR day,
    # so a "month" bucket can show up as YYYY-MM-(28..31); normalise those to the
    # 1st of the following month so blocks align on a common grid.
    def snap(d):
        if args.bin == "month":
            if d.day >= 28:
                y, m = (d.year + 1, 1) if d.month == 12 else (d.year, d.month + 1)
                return datetime.date(y, m, 1)
            return d.replace(day=1)
        if args.bin == "week":
            return d - datetime.timedelta(days=d.weekday())
        return d

    # ---- build {block: {date: count}} ------------------------------------
    block_counts = {}
    if len(args.inputs) == 1 and load_any(args.inputs[0])[0] == "json":
        kind, obj = load_any(args.inputs[0])
        if isinstance(obj, dict):
            keys = args.blocks or [k for k in obj.keys() if isinstance(obj[k], list)]
            for k in keys:
                if k not in obj:
                    print(f"  (skip) block '{k}' not in file"); continue
                bc = {}
                for d, c in obj[k]:
                    bc[snap(datetime.date.fromisoformat(str(d)[:10]))] = float(c)
                block_counts[k] = bc
        else:
            print("VERDICT: BAD INPUT - single JSON input must be a {block: series} dict.")
            return
    else:
        for p in args.inputs:
            kind, obj = load_any(p)
            recs = obj if kind == "ndjson" else (
                obj if isinstance(obj, list) else obj.get("data", []))
            if recs and isinstance(recs[0], dict) and recs[0].get("kind") and "data" in recs[0]:
                recs = [c["data"] for c in recs]
            bc = bucket_recs(recs, args.bin)
            block_counts[block_name_from_file(p)] = {d: float(c) for d, c in bc.items()}

    blocks = sorted(block_counts.keys())
    if len(blocks) < 3:
        print(f"VERDICT: TOO FEW BLOCKS - need >= 3, have {len(blocks)}: {blocks}")
        return

    # ---- common aligned grid --------------------------------------------
    lo = max(min(bc) for bc in block_counts.values())
    hi = min(max(bc) for bc in block_counts.values())
    if lo >= hi:
        print(f"VERDICT: NO TIME OVERLAP across blocks. ranges:")
        for b in blocks:
            print(f"   {b}: {min(block_counts[b])} .. {max(block_counts[b])}")
        return

    # step
    def next_date(cur):
        if args.bin == "month":
            y, m = cur.year, cur.month + 1
            if m > 12:
                y, m = y + 1, 1
            return datetime.date(y, m, 1)
        return cur + datetime.timedelta(days=(7 if args.bin == "week" else 1))

    grid = []
    cur = lo
    while cur <= hi:
        grid.append(cur)
        cur = next_date(cur)
    if len(grid) < 2 * args.window:
        print(f"VERDICT: INSUFFICIENT OVERLAP - {len(grid)} aligned buckets, "
              f"need >= {2*args.window}. overlap {lo}..{hi}")
        return

    # raw aligned matrix
    raw = {b: [block_counts[b].get(d, 0.0) for d in grid] for b in blocks}
    # z-score each block over the whole grid
    z = {}
    for b in blocks:
        x = raw[b]
        m = statistics.mean(x)
        sd = statistics.pstdev(x) or 1e-9
        z[b] = [(xi - m) / sd for xi in x]

    K = len(blocks)

    def window_neff(idx_lo, idx_hi):
        # variance ratio N_eff and Kuramoto R on [idx_lo, idx_hi)
        cols = [[z[b][t] for b in blocks] for t in range(idx_lo, idx_hi)]
        # per-block variance within window
        per = []
        for b in blocks:
            seg = [z[b][t] for t in range(idx_lo, idx_hi)]
            per.append(statistics.pvariance(seg) if len(seg) > 1 else 0.0)
        agg = [sum(row) for row in cols]
        var_agg = statistics.pvariance(agg) if len(agg) > 1 else 0.0
        sum_per = sum(per)
        neff = (sum_per / var_agg) if var_agg > 1e-12 else float(K)
        neff = max(0.0, min(neff, K))
        # Kuramoto-style order parameter on signs of fluctuations
        Rs = []
        for row in cols:
            s = sum(1 if v > 0 else -1 if v < 0 else 0 for v in row)
            Rs.append(abs(s) / K)
        R = statistics.mean(Rs) if Rs else 0.0
        return neff, R

    # sliding
    series_neff = []
    series_R = []
    centers = []
    for i in range(0, len(grid) - args.window + 1):
        neff, R = window_neff(i, i + args.window)
        series_neff.append(neff)
        series_R.append(R)
        centers.append(grid[i + args.window // 2])

    overall_neff, overall_R = window_neff(0, len(grid))

    print("=" * 64)
    print("TEST (ii) LOCATION-SUBREDDIT BLOCK SYNCHRONY")
    print("=" * 64)
    print(f"blocks (K={K})  : {', '.join(blocks)}")
    print(f"aligned grid   : {len(grid)} {args.bin} buckets  {grid[0]} .. {grid[-1]}")
    print(f"window         : {args.window} buckets, {len(series_neff)} sliding positions")
    print("-" * 64)
    print(f"full-span N_eff (variance ratio, ideal K={K}) : {overall_neff:.2f}")
    print(f"full-span Kuramoto R (0 indep .. 1 sync)       : {overall_R:.3f}")
    print("-" * 64)
    # show N_eff trajectory (compact)
    lo_i = min(range(len(series_neff)), key=lambda i: series_neff[i])
    hi_i = max(range(len(series_neff)), key=lambda i: series_neff[i])
    print(f"N_eff range over time : min {series_neff[lo_i]:.2f} @ {centers[lo_i]}  "
          f"max {series_neff[hi_i]:.2f} @ {centers[hi_i]}")

    # ---- shock test ------------------------------------------------------
    if args.shock:
        shock_dates = [datetime.date.fromisoformat(s) for s in args.shock]
        shock_neff, base_neff = [], []
        for i, c in enumerate(centers):
            wlo = grid[i]
            whi = grid[min(i + args.window - 1, len(grid) - 1)]
            hit = any(wlo <= sd <= whi for sd in shock_dates)
            (shock_neff if hit else base_neff).append(series_neff[i])
        print("-" * 64)
        if not shock_neff:
            print("shock dates fall outside the aligned/overlap window; cannot test.")
            print(f"   overlap is {grid[0]}..{grid[-1]}; shocks {args.shock}")
        elif len(base_neff) < 3:
            print("not enough non-shock windows for a base rate.")
        else:
            ms, mb = statistics.mean(shock_neff), statistics.mean(base_neff)
            sdb = statistics.pstdev(base_neff) or 1e-9
            zc = (ms - mb) / sdb
            print(f"SHOCK TEST  (does N_eff COLLAPSE around shocks?)")
            print(f"   shock-window N_eff   mean : {ms:.2f}  (n={len(shock_neff)})")
            print(f"   base-rate  N_eff     mean : {mb:.2f}  (n={len(base_neff)})")
            print(f"   z of shock vs base rate   : {zc:+.2f}")
            print("-" * 64)
            if ms < mb and zc <= -1.0:
                print("VERDICT: SUPPORTS BLOCK SYNCHRONY - N_eff collapses (blocks lose")
                print("         independence) around the shared shock(s).")
            elif ms < mb:
                print("VERDICT: WEAK SUPPORT - N_eff lower around shocks but within base")
                print("         -rate noise. More blocks / longer series needed.")
            else:
                print("VERDICT: NO COLLAPSE - blocks do not synchronise more around the")
                print("         labeled shocks than at random times.")
    else:
        print("-" * 64)
        print("(no --shock dates given; reported N_eff trajectory only.)")
        print(f"VERDICT: DESCRIPTIVE - full-span N_eff={overall_neff:.2f} of K={K}. "
              f"{'Blocks largely independent.' if overall_neff > 0.6*K else 'Blocks substantially co-move.'}")
    print("NOTE: N_eff here is the macro variance-ratio (order parameter), not a")
    print("      mean of pairwise Pearson correlations. K independent blocks give")
    print("      N_eff~K; full synchrony gives N_eff~1.")


if __name__ == "__main__":
    main()
