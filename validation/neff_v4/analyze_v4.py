"""SEALED evaluation of test (ii') v4 on the FRESH WSB roster, with community-
SPECIFICITY (fire vs block-label shuffle) as the PRIMARY endpoint.

For each fresh event: build the pre-onset co-thread graph, blind-Louvain partition,
canonical macro variance-ratio N_eff baseline-vs-onset drop, 300x block-label-shuffle
null (all via the frozen reddit_wsb pipeline). Then evaluate the FROZEN primary
decision rule (PRE_REGISTRATION_neff_v4.md section 3) ONCE:

    PASS iff  (a) k/n >= 0.60
         AND  (b) binomial P(X >= k | n, p0=0.10) < 0.01
         AND  (c) n >= 8 powered (K>=3) events.

Magnitude is computed and reported but is NON-GATING in v4 (v3's clean-null
diagnosis: quiet WSB windows drop a median ~0.10, so magnitude does not discriminate).

Emits result_neff_v4.json + figure_v4.png. Run: py -3.12 analyze_v4.py
(requires harvest_v4.py to have run first).
"""
import os
import sys
import json

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
WSB = os.path.abspath(os.path.join(HERE, "..", "reddit_wsb"))
sys.path.insert(0, WSB)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "pipeline_v03"))

import neff_collapse_wsb as NB   # noqa: E402
import roster_v4 as RV           # noqa: E402


def load(label):
    return NB.load_run_comments(os.path.join(DATA, f"event__{label}.jsonl"))


def binom_sf_ge(k, n, p0):
    """P(X >= k | Binomial(n, p0)), exact."""
    from math import comb
    return float(sum(comb(n, i) * p0 ** i * (1 - p0) ** (n - i) for i in range(k, n + 1)))


def main():
    results = []
    for label, onset, why in RV.all_events():
        comments = load(label)
        if not comments:
            results.append(dict(label=label, onset=onset, status="NO_DATA", why=why))
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

    # powered events = usable partition with K>=3 (the frozen scope)
    powered = [r for r in results if r.get("status") == "OK" and (r.get("K_blocks") or 0) >= 3]
    n = len(powered)
    fires = [r for r in powered if r.get("fires_vs_shuffle")]
    k = len(fires)
    frac_fire = (k / n) if n else None
    binom_p = binom_sf_ge(k, n, RV.BINOM_P0) if n else None

    drops = [r["drop_macro"] for r in powered if r.get("drop_macro") is not None
             and not np.isnan(r["drop_macro"])]
    median_drop = float(np.median(drops)) if drops else None
    pctiles = [r.get("shuffle_pctile_of_obs") for r in powered
               if r.get("shuffle_pctile_of_obs") is not None]
    median_pctile = float(np.median(pctiles)) if pctiles else None

    # FROZEN primary decision rule (evaluated ONCE)
    cond_a = frac_fire is not None and frac_fire >= RV.FIRE_FRACTION_BAR
    cond_b = binom_p is not None and binom_p < RV.BINOM_ALPHA
    cond_c = n >= RV.MIN_POWERED_N
    sealed_pass = bool(cond_a and cond_b and cond_c)

    failed = []
    if not cond_a:
        failed.append(f"COND_a fire-fraction: {frac_fire} < {RV.FIRE_FRACTION_BAR}"
                      if frac_fire is not None else "COND_a: no powered events")
    if not cond_b:
        failed.append(f"COND_b binomial: P(X>={k}|n={n},p0={RV.BINOM_P0})={binom_p} "
                      f">= alpha {RV.BINOM_ALPHA}")
    if not cond_c:
        failed.append(f"COND_c powered: only n={n} K>=3 events (<{RV.MIN_POWERED_N})")

    summary = dict(
        endpoint="PRIMARY = community-specificity (fire vs 300x block-label shuffle)",
        substrate="r/wallstreetbets comments (subreddits24 dump), FRESH disjoint roster",
        scope="structured / endogenous-community regime (K>=3 blocks)",
        n_event_total=len(results),
        n_event_ok=sum(1 for r in results if r.get("status") == "OK"),
        n_powered_Kge3=n,
        k_fires=k, fire_fraction=frac_fire,
        binom_p_ge_k=binom_p, binom_p0=RV.BINOM_P0,
        median_shuffle_pctile_of_obs=median_pctile,
        median_event_drop_macro_NONGATING=median_drop,
        thresholds=dict(fire_fraction_bar=RV.FIRE_FRACTION_BAR,
                        binom_alpha=RV.BINOM_ALPHA, min_powered_n=RV.MIN_POWERED_N,
                        fire_pctile=RV.PCTILE, n_shuffle=RV.N_SHUFFLE),
        decision=dict(cond_a_fire_fraction=cond_a, cond_b_binomial=cond_b,
                      cond_c_powered=cond_c),
        failed_conditions=failed,
        VERDICT=("SEALED PASS (community-specificity, fresh roster)"
                 if sealed_pass else "SEALED NOT"),
        magnitude_note=("NON-GATING in v4: v3's clean null showed genuinely-quiet WSB "
                        "windows already drop macro-N_eff a median ~0.10 (tail to 0.43), "
                        "so raw magnitude does not discriminate an endogenous cascade on "
                        "this substrate. Specificity is the valid endpoint."),
    )
    out = dict(summary=summary, runs=results,
               params=dict(bucket_days=RV.BUCKET_DAYS, n_shuffle=RV.N_SHUFFLE,
                           pre_graph_days=RV.PRE_GRAPH_DAYS, post_days=RV.POST_DAYS,
                           user_cap=RV.USER_CAP, thread_subsample=RV.THREAD_SUBSAMPLE,
                           per_thread_cap=RV.PER_THREAD_CAP,
                           metric_primary="macro variance-ratio (canonical)",
                           metric_secondary="Pearson-Kish (legacy)"))
    json.dump(out, open(os.path.join(HERE, "result_neff_v4.json"), "w"), indent=2)
    make_figure(results, powered, summary)
    print(json.dumps(summary, indent=2))


def make_figure(results, powered, summary):
    fig, ax = plt.subplots(1, 2, figsize=(13, 5.5))
    ev2 = sorted(powered, key=lambda r: -(r.get("drop_macro") or 0))
    names = [r["label"] for r in ev2]
    drops = [r.get("drop_macro") or 0 for r in ev2]
    p90 = [r.get("shuffle_null_p90") or 0 for r in ev2]
    colors = ["#27ae60" if r.get("fires_vs_shuffle") else "#c0392b" for r in ev2]
    y = np.arange(len(names))
    ax[0].barh(y, drops, color=colors, label="event N_eff drop (green=fires)")
    ax[0].plot(p90, y, "k.", label="shuffle-null p90")
    ax[0].set_yticks(y)
    ax[0].set_yticklabels(names, fontsize=7)
    ax[0].set_xlabel("canonical N_eff collapse drop (1 - onset/baseline)")
    ax[0].set_title("Per-event collapse vs its own shuffle null (fresh WSB roster)", fontsize=10)
    ax[0].legend(fontsize=8)

    pcts = [r.get("shuffle_pctile_of_obs") for r in ev2
            if r.get("shuffle_pctile_of_obs") is not None]
    ax[1].hist(pcts, bins=np.linspace(0, 1.0, 21), color="#27ae60", alpha=0.8)
    ax[1].axvline(RV.PCTILE, ls="--", c="k", label=f"fire bar = p{int(RV.PCTILE*100)}")
    ax[1].set_xlabel("percentile of observed collapse within its 300x shuffle null")
    ax[1].set_ylabel("# events")
    s = summary
    ax[1].set_title(f"Specificity: {s['k_fires']}/{s['n_powered_Kge3']} fire "
                    f"(binom p={s['binom_p_ge_k']:.1e})\nVERDICT: {s['VERDICT']}",
                    fontsize=10)
    ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "figure_v4.png"), dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
