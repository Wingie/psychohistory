"""V4 -- Metric + window sensitivity.

(a) Per-article macro drop vs Pearson-Kish drop (both already in
    result_wiki_neff.json): do the two metrics agree on direction and ranking?
    Report Spearman rank correlation + sign-agreement count.

(b) Sensitivity of the 0.19 median event drop to analysis knobs. Recompute the
    median event macro drop over BUCKET_DAYS in {2,3,5,7} and baseline-window
    length W_BASELINE_DAYS in {35,49,70} days, by monkeypatching the frozen
    module-level constants (the frozen run uses BUCKET_DAYS=3, W_BASELINE=49).
    Is 0.19 stable or fragile? Emits a small table.

Writes v4_sensitivity.json.
"""
import os
import json

import datetime as dt

import numpy as np
from scipy.stats import spearmanr

import _shared as S
from _shared import N, R


def median_event_drop():
    """Median event macro drop using the SAME windows as analyze_run but skipping
    the (slow, irrelevant-here) shuffle null. Honors current N.BUCKET_DAYS and
    N.W_BASELINE_DAYS so the sensitivity grid takes effect."""
    runs = S.load_runs()
    drops = []
    for rec in runs:
        if rec.get("arm") != "event":
            continue
        part, mod, K, G = S.frozen_partition(rec)
        if K < 3:
            continue
        onset = dt.date.fromisoformat(rec["onset"])
        lo_full = onset - dt.timedelta(days=R.BASELINE_DAYS)
        hi_full = onset + dt.timedelta(days=R.POST_DAYS + 1)
        base_lo = onset - dt.timedelta(days=N.W_BASELINE_DAYS + 7)
        base_hi = onset - dt.timedelta(days=7)
        onset_lo = onset - dt.timedelta(days=3)
        onset_hi = onset + dt.timedelta(days=R.POST_DAYS + 1)
        try:
            res = N.collapse_for_partition(rec["focal_revs"], part, onset, lo_full,
                                           hi_full, base_lo, base_hi, onset_lo, onset_hi)
        except Exception:
            continue
        d = res.get("drop_macro")
        if d is not None and not np.isnan(d):
            drops.append(d)
    return (float(np.median(drops)) if drops else None), len(drops)


def main():
    # (a) macro vs pearson on the FROZEN result
    res = S.load_primary_result()
    ev = [r for r in res["runs"] if r.get("arm") == "event" and r.get("status") == "OK"]
    macro, pear, names = [], [], []
    for r in ev:
        dm, dp = r.get("drop_macro"), r.get("drop_pearson")
        if dm is None or dp is None or np.isnan(dm) or np.isnan(dp):
            continue
        macro.append(dm)
        pear.append(dp)
        names.append(r["title"])
    macro = np.array(macro)
    pear = np.array(pear)
    rho, p = spearmanr(macro, pear)
    sign_agree = int(np.sum(np.sign(macro) == np.sign(pear)))
    metric_rows = sorted(
        [dict(title=n, drop_macro=float(m), drop_pearson=float(pp))
         for n, m, pp in zip(names, macro, pear)],
        key=lambda x: -x["drop_macro"])

    # (b) sensitivity grid over BUCKET_DAYS and W_BASELINE_DAYS
    orig_bucket = N.BUCKET_DAYS
    orig_wbase = N.W_BASELINE_DAYS
    grid = {}
    for bd in (2, 3, 5, 7):
        for wb in (35, 49, 70):
            N.BUCKET_DAYS = bd
            N.W_BASELINE_DAYS = wb
            med, n = median_event_drop()
            grid[f"bucket{bd}_base{wb}"] = dict(bucket_days=bd, baseline_days=wb,
                                                median_event_drop=med, n=n)
    N.BUCKET_DAYS = orig_bucket
    N.W_BASELINE_DAYS = orig_wbase

    meds = [v["median_event_drop"] for v in grid.values()
            if v["median_event_drop"] is not None]
    out = dict(
        variation="V4 metric + window sensitivity",
        a_metric_agreement=dict(
            n=len(macro),
            spearman_macro_vs_pearson=dict(rho=float(rho), p=float(p)),
            sign_agreement=f"{sign_agree}/{len(macro)}",
            note="macro is the canonical primary metric; pearson is the legacy secondary",
            rows=metric_rows,
        ),
        b_sensitivity=dict(
            frozen_cell="bucket3_base49 (= the reported 0.19)",
            grid=grid,
            median_range=[float(min(meds)), float(max(meds))],
            median_of_medians=float(np.median(meds)),
            all_below_f030=bool(all(m < 0.30 for m in meds)),
        ),
    )
    json.dump(out, open(os.path.join(S.HERE, "v4_sensitivity.json"), "w"), indent=2)
    print(f"(a) macro vs pearson: rho={rho:.2f} p={p:.3f} sign_agree={sign_agree}/{len(macro)}")
    print("(b) median event drop sensitivity grid:")
    print(f"    {'bucket\\base':>12} " + " ".join(f"{wb:>7}" for wb in (35, 49, 70)))
    for bd in (2, 3, 5, 7):
        cells = []
        for wb in (35, 49, 70):
            m = grid[f"bucket{bd}_base{wb}"]["median_event_drop"]
            cells.append(f"{m:+.3f}" if m is not None else "   nan")
        print(f"    {bd:>12} " + " ".join(f"{c:>7}" for c in cells))
    print(f"    range [{min(meds):+.3f}, {max(meds):+.3f}], all < 0.30: {out['b_sensitivity']['all_below_f030']}")


if __name__ == "__main__":
    main()
