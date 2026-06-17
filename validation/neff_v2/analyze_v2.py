"""SEALED analysis for test ii' v2 on the FRESH roster.

Reuses the FROZEN analysis functions from validation/wikipedia/neff_collapse_wiki.py
(coedit_graph, blind_partition, block_bucket_matrix, neff_macro, collapse_for_partition,
analyze_run) and the V2 clean-null window picker (quietest_pseudo_onset, collapse_at)
verbatim by import. Applies the FROZEN threshold f and decision rule from
PRE_REGISTRATION_neff_v2.md. Nothing here is tuned.

Emits result_neff_v2.json + figure_neff_v2.png. Run: py -3.12 analyze_v2.py
"""
import os
import sys
import json
import datetime as dt
from collections import defaultdict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu, wilcoxon

HERE = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.abspath(os.path.join(HERE, "..", "wikipedia"))
DIAG = os.path.join(WIKI, "diagnostics")
DATA = os.path.join(HERE, "data")
sys.path.insert(0, WIKI)
sys.path.insert(0, DIAG)

import neff_collapse_wiki as N   # noqa: E402 frozen analysis functions
import roster_v2 as R            # noqa: E402
import v2_clean_calm as V2       # noqa: E402 clean-null window picker

# ---- FROZEN values (from PRE_REGISTRATION_neff_v2.md / derive_f.json) ----
FROZEN_F = 0.298       # Route (i) clean-null 95th percentile, frozen before harvest
P90 = 0.90             # fire-vs-shuffle and beats-clean pctile
MIN_N = 8


def load_by_title():
    files = sorted(f for f in os.listdir(DATA) if f.endswith(".json"))
    bytitle = defaultdict(dict)
    for f in files:
        d = json.load(open(os.path.join(DATA, f), encoding="utf-8"))
        bytitle[d["title"]][d["arm"]] = d
    return bytitle


def main():
    bytitle = load_by_title()
    rows = []
    for title, arms in sorted(bytitle.items()):
        if "event" not in arms:
            continue
        ev = arms["event"]
        # frozen primary event analysis (partition, macro drop, shuffle null)
        res = N.analyze_run(ev)
        K = res.get("K_blocks")
        row = dict(title=title, onset=ev["onset"], K=K,
                   status=res.get("status"),
                   event_drop=res.get("drop_macro"),
                   shuffle_p90=res.get("shuffle_null_p90"),
                   fires_vs_shuffle=res.get("fires_vs_shuffle"),
                   modularity=res.get("modularity"))
        if res.get("status") != "OK" or (K is not None and K < 3):
            row["clean_drop"] = None
            rows.append(row)
            continue

        # clean null = V2 genuinely-quiet window (frozen def)
        G = N.coedit_graph(ev["editor_contribs"], ev["title"])
        part, mod, Kp = N.blind_partition(G)
        onset = dt.date.fromisoformat(ev["onset"])
        dates = V2.all_focal_dates(arms)
        revs = V2.merged_focal_revs(arms)
        islands = V2.harvested_islands(dates)
        pseudo, info, cstatus = V2.quietest_pseudo_onset(dates, onset, islands)
        cd = None
        if pseudo is not None:
            cd = V2.collapse_at(revs, part, pseudo).get("drop_macro")
        row["clean_drop"] = (None if cd is None or (isinstance(cd, float) and np.isnan(cd))
                             else float(cd))
        row["clean_status"] = cstatus
        rows.append(row)

    ok = [r for r in rows if r.get("status") == "OK" and r.get("K") and r["K"] >= 3]
    ev_drops = [r["event_drop"] for r in ok
                if r["event_drop"] is not None and not np.isnan(r["event_drop"])]
    clean_drops = [r["clean_drop"] for r in ok if r.get("clean_drop") is not None]
    fires = [r for r in ok if r.get("fires_vs_shuffle")]

    median_ev = float(np.median(ev_drops)) if ev_drops else None
    clean_p90 = float(np.percentile(clean_drops, 90)) if clean_drops else None
    clean_median = float(np.median(clean_drops)) if clean_drops else None
    clean_p95 = float(np.percentile(clean_drops, 95)) if clean_drops else None
    frac_fire = (len(fires) / len(ok)) if ok else None

    # Mann-Whitney one-sided (event > clean) + paired Wilcoxon
    mw_p = (float(mannwhitneyu(ev_drops, clean_drops, alternative="greater").pvalue)
            if ev_drops and clean_drops else None)
    matched = [(r["event_drop"], r["clean_drop"]) for r in ok
               if r["event_drop"] is not None and r.get("clean_drop") is not None
               and not np.isnan(r["event_drop"])]
    wil_p = None
    if len(matched) >= 6:
        try:
            wil_p = float(wilcoxon([e for e, _ in matched], [c for _, c in matched],
                                   alternative="greater").pvalue)
        except Exception:
            wil_p = None

    # ---- FROZEN decision rule (evaluated once) ----
    cond1 = median_ev is not None and median_ev >= FROZEN_F
    cond2 = (median_ev is not None and clean_p90 is not None
             and median_ev > clean_p90 and mw_p is not None and mw_p < 0.05)
    cond3 = frac_fire is not None and frac_fire >= 0.5
    powered = len(ok) >= MIN_N
    sealed_pass = bool(cond1 and cond2 and cond3 and powered)

    summary = dict(
        n_event_total=len([r for r in rows]),
        n_event_ok_K3=len(ok), n_clean=len(clean_drops),
        median_event_drop=median_ev,
        clean_null_median=clean_median, clean_null_p90=clean_p90, clean_null_p95=clean_p95,
        frac_fires_vs_shuffle=frac_fire, n_fires=len(fires),
        event_vs_clean_mannwhitney_p=mw_p, paired_wilcoxon_p=wil_p, n_paired=len(matched),
        FROZEN_f=FROZEN_F, fire_pctile=P90, min_n=MIN_N,
        decision=dict(
            cond1_magnitude_median_ge_f=cond1,
            cond2_beats_clean_p90_and_mwu=cond2,
            cond3_half_fire_vs_shuffle=cond3,
            powered_n8=powered),
        SEALED_VERDICT="PASS" if sealed_pass else "NOT A PASS",
    )
    out = dict(summary=summary, rows=sorted(rows, key=lambda r: -(r.get("event_drop") or -9)),
               params=dict(frozen_f=FROZEN_F, clean_null="V2 genuinely-quiet window",
                           bucket_days=N.BUCKET_DAYS, n_shuffle=N.N_SHUFFLE,
                           metric="macro variance-ratio (canonical)"))
    json.dump(out, open(os.path.join(HERE, "result_neff_v2.json"), "w"), indent=2)
    make_figure(rows, summary)
    print(json.dumps(summary, indent=2))
    print("\nper-article:")
    for r in out["rows"]:
        ed = r.get("event_drop"); cd = r.get("clean_drop")
        print(f"  {r['title']:30s} K={str(r.get('K')):>4} "
              f"event={'  None' if ed is None else f'{ed:+.2f}'} "
              f"clean={'  None' if cd is None else f'{cd:+.2f}'} "
              f"fire={r.get('fires_vs_shuffle')} [{r.get('status')}]")


def make_figure(rows, summary):
    ok = [r for r in rows if r.get("status") == "OK" and r.get("K") and r["K"] >= 3
          and r.get("event_drop") is not None]
    ok = sorted(ok, key=lambda r: -(r["event_drop"]))
    fig, ax = plt.subplots(1, 2, figsize=(13, 5.5))
    names = [r["title"] for r in ok]
    drops = [r["event_drop"] for r in ok]
    p90 = [r.get("shuffle_p90") or 0 for r in ok]
    y = np.arange(len(names))
    ax[0].barh(y, drops, color="#8e44ad", label="event N_eff drop")
    ax[0].plot(p90, y, "k.", label="shuffle-null p90")
    ax[0].axvline(summary["FROZEN_f"], ls="--", c="r", label=f"frozen f={summary['FROZEN_f']}")
    ax[0].set_yticks(y); ax[0].set_yticklabels(names, fontsize=7)
    ax[0].set_xlabel("canonical N_eff collapse drop (1 - onset/baseline)")
    ax[0].set_title("Fresh roster: per-article N_eff collapse (event arm)", fontsize=10)
    ax[0].legend(fontsize=8)
    ev_d = [r["event_drop"] for r in ok]
    ca_d = [r["clean_drop"] for r in ok if r.get("clean_drop") is not None]
    ax[1].hist(ev_d, bins=10, alpha=0.6, color="#8e44ad", label=f"event (n={len(ev_d)})")
    ax[1].hist(ca_d, bins=10, alpha=0.6, color="#16a085", label=f"clean null (n={len(ca_d)})")
    ax[1].axvline(summary["FROZEN_f"], ls="--", c="r", label=f"f={summary['FROZEN_f']}")
    if summary["median_event_drop"] is not None:
        ax[1].axvline(summary["median_event_drop"], ls=":", c="#8e44ad",
                      label=f"event median={summary['median_event_drop']:.2f}")
    ax[1].set_xlabel("N_eff collapse drop"); ax[1].set_ylabel("articles")
    ax[1].set_title(f"Event vs clean null  --  SEALED: {summary['SEALED_VERDICT']}", fontsize=10)
    ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "figure_neff_v2.png"), dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
