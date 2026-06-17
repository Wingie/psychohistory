"""V2 -- Clean calm null.

The frozen matched-calm arm is onset-365d. Two of those windows were not
actually quiet (Queen Elizabeth II -1y, Twitter -1y had their own mini-events),
inflating calm_p90 to 0.29 and defeating cond3.

Here we RE-PICK, per event article, the genuinely quietest pseudo-onset in the
harvested pre-onset span: slide a 49-day window and choose the start with the
LOWEST focal-edit volume, treating its center as a clean "calm onset", then run
the frozen collapse pipeline (frozen pre-onset partition + macro metric) on it.

HARVEST CONSTRAINT (honest): the event-arm focal_revs only span ~[onset-90d,
onset+22d]; the calm-arm focal_revs span ~[onset-455d, onset-343d]. So the
available pre-onset coverage is roughly two islands near onset-365d and near
onset-90d, NOT a continuous 2-year record. We search the cleanest window inside
the ACTUALLY HARVESTED pre-onset dates and say so. We do NOT re-harvest.

For the collapse to be computable the chosen window must have enough buckets in
both baseline and onset sub-windows; we require the calm pseudo-onset to sit far
enough inside a harvested island. Writes v2_clean_calm.json.
"""
import os
import json
import datetime as dt
from collections import defaultdict

import numpy as np
from scipy.stats import mannwhitneyu

import _shared as S
from _shared import N, R


WIN = R.POST_DAYS + 1 + (2 * R.POST_DAYS + 7) + 7  # full span the metric needs (~84d)
# baseline sub-window length used by analyze_run = 2*POST+7 = 49d; we label the
# pick by its 49-day quietness as the prompt specifies.
QUIET_LEN = 2 * R.POST_DAYS + 7  # 49 days


def all_focal_dates(arms):
    """Merge focal_revs across both harvested arms for one article -> sorted dates."""
    ds = []
    for d in arms.values():
        ds += [N.parse_ts(rv["ts"]).date() for rv in d["focal_revs"] if rv.get("ts")]
    return sorted(ds)


def merged_focal_revs(arms):
    revs = []
    for d in arms.values():
        revs += [rv for rv in d["focal_revs"] if rv.get("ts") and rv.get("user")]
    return revs


def harvested_islands(dates, gap=14):
    """Contiguous-ish coverage islands (split where there is a >gap-day hole)."""
    if not dates:
        return []
    islands = [[dates[0], dates[0]]]
    for d in dates[1:]:
        if (d - islands[-1][1]).days > gap:
            islands.append([d, d])
        else:
            islands[-1][1] = d
    return islands


def quietest_pseudo_onset(dates, onset, islands):
    """Slide a 49-day window over harvested PRE-onset dates and pick the quietest
    window that is STILL COVERED BY HARVESTED DATA. The truly empty stretch sits in
    the unharvested gap between the calm island (~onset-365d) and the event island
    (~onset-90d); a zero-edit window there is no-data, not a genuine quiet-but-live
    window, and would make the collapse degenerate. So we require the FULL metric
    span [pseudo_onset-90d, pseudo_onset+22d] to lie inside ONE harvested island and
    the baseline sub-window to contain real edits. Among the qualifying picks we take
    the one with the lowest focal-edit volume in its 49-day quiet stretch."""
    counts = defaultdict(int)
    for d in dates:
        counts[d] += 1
    cands = []
    # the metric actually uses [pseudo-56d, pseudo+22d] (49d baseline + 7d gap +
    # onset probe). full_mean normalizes and tolerates empty lookback buckets, so we
    # only require THIS ~78-day usable span to fit inside one harvested island; the
    # quiet island near onset-365d is the genuine clean-calm coverage.
    SPAN_LO = (2 * R.POST_DAYS + 7) + 7   # 56d
    SPAN_HI = R.POST_DAYS + 1             # 22d
    for a, b in islands:
        if (b - a).days < SPAN_LO + SPAN_HI:
            continue
        po_lo = a + dt.timedelta(days=SPAN_LO)
        po_hi = min(b - dt.timedelta(days=SPAN_HI),
                    onset - dt.timedelta(days=30))
        po = po_lo
        while po <= po_hi:
            q_lo = po - dt.timedelta(days=QUIET_LEN)   # 49-day quiet stretch = baseline
            q_hi = po
            vol = sum(c for d, c in counts.items() if q_lo <= d < q_hi)
            base_lo = po - dt.timedelta(days=SPAN_LO)
            base_hi = po - dt.timedelta(days=7)
            base_vol = sum(c for d, c in counts.items() if base_lo <= d < base_hi)
            onset_vol = sum(c for d, c in counts.items()
                            if po - dt.timedelta(days=3) <= d < po + dt.timedelta(days=SPAN_HI))
            # both sub-windows must have real activity, else collapse is degenerate
            if base_vol >= 5 and onset_vol >= 3:
                cands.append((vol, po, q_lo, q_hi))
            po += dt.timedelta(days=7)
    if not cands:
        return None, None, "no_covered_quiet_window"
    cands.sort(key=lambda x: x[0])
    vol, po, q_lo, q_hi = cands[0]
    return po, dict(quiet_vol=int(vol), quiet_lo=q_lo.isoformat(),
                    quiet_hi=q_hi.isoformat(),
                    n_candidate_windows=len(cands)), "ok"


def collapse_at(rec_like_revs, part, pseudo_onset):
    """Run the frozen collapse pipeline at an arbitrary pseudo-onset using a merged
    focal_revs list and the frozen pre-onset partition."""
    onset = pseudo_onset
    lo_full = onset - dt.timedelta(days=R.BASELINE_DAYS)
    hi_full = onset + dt.timedelta(days=R.POST_DAYS + 1)
    base_lo = onset - dt.timedelta(days=(2 * R.POST_DAYS + 7) + 7)
    base_hi = onset - dt.timedelta(days=7)
    onset_lo = onset - dt.timedelta(days=3)
    onset_hi = onset + dt.timedelta(days=R.POST_DAYS + 1)
    res = N.collapse_for_partition(rec_like_revs, part, onset, lo_full, hi_full,
                                   base_lo, base_hi, onset_lo, onset_hi)
    return res


def main():
    files = sorted(f for f in os.listdir(S.DATA) if f.endswith(".json"))
    bytitle = defaultdict(dict)
    for f in files:
        d = json.load(open(os.path.join(S.DATA, f), encoding="utf-8"))
        bytitle[d["title"]][d["arm"]] = d

    # event drops from the frozen primary run (re-derived, identical pipeline)
    rows = []
    for title, arms in bytitle.items():
        if "event" not in arms:
            continue
        ev = arms["event"]
        part, mod, K, G = S.frozen_partition(ev)
        if K < 3:
            continue
        onset = dt.date.fromisoformat(ev["onset"])
        ev_drop = N.analyze_run(ev).get("drop_macro")

        dates = all_focal_dates(arms)
        revs = merged_focal_revs(arms)
        islands = harvested_islands(dates)
        pseudo, info, status = quietest_pseudo_onset(dates, onset, islands)
        clean_drop = None
        if pseudo is not None:
            res = collapse_at(revs, part, pseudo)
            clean_drop = res.get("drop_macro")
        rows.append(dict(
            title=title, onset=ev["onset"], K=K, event_drop=ev_drop,
            clean_calm_pseudo_onset=(pseudo.isoformat() if pseudo else None),
            clean_calm_drop=clean_drop,
            quiet_info=info, status=status,
            harvested_islands=[[a.isoformat(), b.isoformat()] for a, b in islands],
            orig_calm_drop=(N.analyze_run(arms["calm"]).get("drop_macro")
                            if "calm" in arms else None),
        ))

    ev_drops = [r["event_drop"] for r in rows
                if r["event_drop"] is not None and not np.isnan(r["event_drop"])]
    clean_drops = [r["clean_calm_drop"] for r in rows
                   if r["clean_calm_drop"] is not None and not np.isnan(r["clean_calm_drop"])]
    orig_calm = [r["orig_calm_drop"] for r in rows
                 if r["orig_calm_drop"] is not None and not np.isnan(r["orig_calm_drop"])]

    median_ev = float(np.median(ev_drops)) if ev_drops else None
    clean_p90 = float(np.percentile(clean_drops, 90)) if clean_drops else None
    clean_median = float(np.median(clean_drops)) if clean_drops else None
    orig_p90 = float(np.percentile(orig_calm, 90)) if orig_calm else None

    mw_clean = (float(mannwhitneyu(ev_drops, clean_drops, alternative="greater").pvalue)
                if ev_drops and clean_drops else None)

    cond3_orig = median_ev is not None and orig_p90 is not None and median_ev > orig_p90
    cond3_clean = median_ev is not None and clean_p90 is not None and median_ev > clean_p90

    out = dict(
        variation="V2 clean calm null",
        harvest_constraint="event focal_revs span ~[onset-90d,onset+22d]; calm "
                            "focal_revs span ~[onset-455d,onset-343d]; clean window "
                            "searched only inside harvested pre-onset dates (no re-harvest)",
        n_event=len(ev_drops), n_clean_calm=len(clean_drops),
        median_event_drop=median_ev,
        orig_calm_p90=orig_p90, cond3_orig_pass=bool(cond3_orig),
        clean_calm_median=clean_median, clean_calm_p90=clean_p90,
        cond3_clean_pass=bool(cond3_clean),
        event_vs_clean_mannwhitney_p=mw_clean,
        rows=sorted(rows, key=lambda r: -(r["event_drop"] or 0)),
    )
    json.dump(out, open(os.path.join(S.HERE, "v2_clean_calm.json"), "w"), indent=2)
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=2))
    for r in out["rows"]:
        print(f"  {r['title']:22s} event={r['event_drop']:+.2f} "
              f"orig_calm={r['orig_calm_drop'] if r['orig_calm_drop'] is None else round(r['orig_calm_drop'],2)!s:>6} "
              f"clean_calm={r['clean_calm_drop'] if r['clean_calm_drop'] is None else round(r['clean_calm_drop'],2)!s:>6} "
              f"[{r['status']}]")


if __name__ == "__main__":
    main()
