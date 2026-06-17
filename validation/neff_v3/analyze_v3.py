"""SEALED evaluation of test (ii') v3 on the FRESH WSB roster.

Reuses validation/reddit_wsb/neff_collapse_wsb.py's frozen pipeline. For each fresh
event: build the pre-onset co-thread graph, blind-Louvain partition, macro variance-
ratio N_eff baseline-vs-onset drop, 300x block-label-shuffle null. Then evaluate the
FROZEN four-condition decision rule (PRE_REGISTRATION_neff_v3.md section 5) ONCE,
against the clean-null distribution + f from derive_f_v3.json.

Emits result_neff_v3.json + figure_v3.png. Run: py -3.12 analyze_v3.py
(requires harvest_v3.py + derive_f_v3.py to have run first).
"""
import os
import sys
import json
import datetime as dt

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
WSB = os.path.abspath(os.path.join(HERE, "..", "reddit_wsb"))
sys.path.insert(0, WSB)
sys.path.insert(0, os.path.join(HERE, "..", "pipeline_v03"))

import neff_collapse_wsb as NB   # noqa: E402
import roster_v3 as RV           # noqa: E402


def load(label):
    return NB.load_run_comments(os.path.join(DATA, f"event__{label}.jsonl"))


def main():
    derive = json.load(open(os.path.join(HERE, "derive_f_v3.json")))
    f = derive["FROZEN_f"]
    clean_p90 = derive["clean_null_p90"]
    clean_p95 = derive["derived_f_route_i_p95"]
    clean_drops = [d for d in derive["route_i_clean_null"]["clean_drops_sorted"]]

    results = []
    for label, onset, why in RV.all_events():
        comments = load(label)
        if not comments:
            results.append(dict(label=label, onset=onset, status="NO_DATA"))
            sys.stderr.write(f"  {label:26s} NO_DATA\n")
            continue
        try:
            r = NB.analyze_run(label, onset, "event", comments)
        except Exception as e:
            r = dict(label=label, onset=onset, status="ERROR", err=str(e))
        r["why"] = why
        results.append(r)
        sys.stderr.write(f"  {label:26s} {r.get('status')} K={r.get('K_blocks')} "
                         f"mod={r.get('modularity')} drop={r.get('drop_macro')} "
                         f"fires={r.get('fires_vs_shuffle')}\n")

    ev = [r for r in results if r.get("status") == "OK"]
    ev_drops = [r["drop_macro"] for r in ev if r.get("drop_macro") is not None
                and not np.isnan(r["drop_macro"])]
    fires = [r for r in ev if r.get("fires_vs_shuffle")]
    median_ev = float(np.median(ev_drops)) if ev_drops else None
    frac_fire = (len(fires) / len(ev)) if ev else None

    mw_p = wil_p = None
    try:
        from scipy.stats import mannwhitneyu, wilcoxon
        if ev_drops and clean_drops:
            mw_p = float(mannwhitneyu(ev_drops, clean_drops, alternative="greater").pvalue)
        # supplementary paired Wilcoxon: pair each event drop against the median clean
        # drop is not a true pair; instead report Wilcoxon of event drops vs f as a
        # one-sample location test (non-gating, legibility only).
        if len(ev_drops) >= 6:
            wil_p = float(wilcoxon(np.array(ev_drops) - f, alternative="greater").pvalue)
    except Exception as e:
        sys.stderr.write(f"  (supplementary stats skipped: {e})\n")

    # FROZEN four-condition decision rule (evaluated ONCE)
    cond1 = median_ev is not None and f is not None and median_ev >= f
    cond2 = (median_ev is not None and clean_p90 is not None and median_ev > clean_p90
             and mw_p is not None and mw_p < 0.05)
    cond3 = frac_fire is not None and frac_fire >= 0.5
    cond4 = len(ev) >= 8
    sealed_pass = bool(cond1 and cond2 and cond3 and cond4)

    failed = []
    if not cond1:
        failed.append(f"COND1 magnitude: median {median_ev:.4f} < f {f:.4f}"
                      if median_ev is not None else "COND1: no event drops")
    if not cond2:
        bits = []
        if median_ev is not None and clean_p90 is not None and not median_ev > clean_p90:
            bits.append(f"median {median_ev:.4f} <= clean_p90 {clean_p90:.4f}")
        if mw_p is None or not mw_p < 0.05:
            bits.append(f"MannWhitney p={mw_p}")
        failed.append("COND2 beats-clean-null: " + "; ".join(bits))
    if not cond3:
        failed.append(f"COND3 specificity: only {frac_fire:.2f} fire vs shuffle (<0.50)")
    if not cond4:
        failed.append(f"COND4 powered: only n={len(ev)} K>=3 events (<8)")

    summary = dict(
        substrate="r/wallstreetbets comments (subreddits24 dump), FRESH disjoint roster",
        scope="structured / endogenous-community regime (NOT population-wide)",
        n_event_total=len(results), n_event_ok=len(ev),
        n_event_powered=cond4,
        median_event_drop_macro=median_ev,
        frac_event_fires_vs_shuffle=frac_fire, n_event_fires=len(fires),
        FROZEN_f_clean_p95=f, clean_null_p90=clean_p90, clean_null_p95=clean_p95,
        n_clean=len(clean_drops),
        clean_null_median=(float(np.median(clean_drops)) if clean_drops else None),
        event_vs_clean_mannwhitney_p=mw_p,
        supp_wilcoxon_event_minus_f_p=wil_p,
        thresholds=dict(f_is_clean_p95=f, fire_pctile=0.90, min_n=8,
                        mannwhitney_alpha=0.05),
        decision=dict(cond1_magnitude=cond1, cond2_beats_clean_null=cond2,
                      cond3_specificity=cond3, cond4_powered=cond4),
        failed_conditions=failed,
        VERDICT=("SEALED PASS (structured/endogenous-community regime)"
                 if sealed_pass else "SEALED NOT"),
    )
    out = dict(summary=summary, runs=results,
               clean_null_drops=clean_drops,
               params=dict(bucket_days=RV.BUCKET_DAYS, n_shuffle=RV.N_SHUFFLE,
                           pre_graph_days=RV.PRE_GRAPH_DAYS, post_days=RV.POST_DAYS,
                           user_cap=RV.USER_CAP, thread_subsample=RV.THREAD_SUBSAMPLE,
                           per_thread_cap=RV.PER_THREAD_CAP,
                           metric_primary="macro variance-ratio (canonical)",
                           metric_secondary="Pearson-Kish (legacy)"))
    json.dump(out, open(os.path.join(HERE, "result_neff_v3.json"), "w"), indent=2)
    make_figure(results, clean_drops, summary, f, clean_p90)
    print(json.dumps(summary, indent=2))


def make_figure(results, clean_drops, summary, f, clean_p90):
    ev = [r for r in results if r.get("status") == "OK"]
    fig, ax = plt.subplots(1, 2, figsize=(13, 5.5))
    ev2 = sorted(ev, key=lambda r: -(r.get("drop_macro") or 0))
    names = [r["label"] for r in ev2]
    drops = [r.get("drop_macro") or 0 for r in ev2]
    p90 = [r.get("shuffle_null_p90") or 0 for r in ev2]
    y = np.arange(len(names))
    ax[0].barh(y, drops, color="#8e44ad", label="event N_eff drop")
    ax[0].plot(p90, y, "k.", label="shuffle-null p90")
    if f is not None:
        ax[0].axvline(f, ls="--", c="r", label=f"f (clean p95)={f:.3f}")
    ax[0].set_yticks(y)
    ax[0].set_yticklabels(names, fontsize=7)
    ax[0].set_xlabel("canonical N_eff collapse drop (1 - onset/baseline)")
    ax[0].set_title("Per-event dynamic N_eff collapse (fresh WSB roster)", fontsize=10)
    ax[0].legend(fontsize=8)

    ev_d = [r["drop_macro"] for r in ev if r.get("drop_macro") is not None]
    ax[1].hist(clean_drops, bins=10, alpha=0.6, color="#16a085",
               label=f"clean null (n={len(clean_drops)})")
    ax[1].hist(ev_d, bins=10, alpha=0.6, color="#8e44ad",
               label=f"event (n={len(ev_d)})")
    if f is not None:
        ax[1].axvline(f, ls="--", c="r", label=f"f={f:.3f}")
    if clean_p90 is not None:
        ax[1].axvline(clean_p90, ls=":", c="orange", label=f"clean p90={clean_p90:.3f}")
    me = summary["median_event_drop_macro"]
    if me is not None:
        ax[1].axvline(me, ls="-", c="purple", lw=1, label=f"median event={me:.3f}")
    ax[1].set_xlabel("N_eff collapse drop")
    ax[1].set_ylabel("count")
    ax[1].set_title(f"Event vs CLEAN null\nVERDICT: {summary['VERDICT']}", fontsize=10)
    ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "figure_v3.png"), dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
