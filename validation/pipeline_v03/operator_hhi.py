"""OBJ 3 - operator_hhi.py  (L2/L6 observation operator)

TIME-INVARIANT operator-concentration statistic. The v0.2 operator pilot
discriminated cascades by RAMP DURATION (Reddit ~13 weeks vs GitHub ~days),
which is platform-specific. HHI and Gini read the *concentration of activity
across actors* and are time-invariant: they give the same number whether the
buildup took 13 weeks or 3 days. The hypothesis is that operator CONCENTRATION
is the domain-general invariant that unifies the two platforms.

For each cascade we:
  1. compute, over the PRE-ONSET window (the W weeks before onset), the actor
     activity-share HHI, Gini, and top-5% share;
  2. build a PLATFORM BASELINE = the same statistic over every non-onset rolling
     window of equal length (the battery's base-rate-null construction);
  3. FLAG if pre-onset concentration > 90th percentile of that baseline,
     REGARDLESS of ramp duration.

Substrates: (a) GitHub per-contributor weekly commits (8-repo LLM-agent cohort);
(b) AskEconomics comment authors (second substrate, Reddit).

Pure transforms; run end-to-end with `py -3.12 operator_hhi.py`.
"""
import json
import os
import datetime as dt

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import common as C

HERE = os.path.dirname(os.path.abspath(__file__))
PRE_W = 4   # pre-onset window length (weeks) for the concentration read


def rolling_concentration(week_counts, weeks_sorted, i, window):
    """Pool actor counts over weeks_sorted[i-window:i] and return concentration
    stats. Returns None if the window is empty."""
    block = weeks_sorted[i - window:i]
    if len(block) < window:
        return None
    pooled = {}
    for wk in block:
        for actor, cnt in week_counts.get(wk, {}).items():
            pooled[actor] = pooled.get(actor, 0) + cnt
    counts = list(pooled.values())
    if sum(counts) <= 0 or len(counts) < 2:
        return None
    return dict(hhi=C.hhi(counts), gini=C.gini(counts),
                top5=C.top_k_share(counts, 0.05),
                n_actors=len(counts), total=int(sum(counts)))


def baseline_pool(week_counts, weeks_sorted, onset_idx, window):
    """All equal-length rolling windows that do NOT overlap the pre-onset window
    -> the platform base-rate null distribution of each statistic."""
    pre_lo = onset_idx - window
    pools = {"hhi": [], "gini": [], "top5": []}
    for i in range(window, len(weeks_sorted) + 1):
        # exclude windows overlapping the pre-onset read
        if not (i <= pre_lo or i - window >= onset_idx):
            continue
        r = rolling_concentration(week_counts, weeks_sorted, i, window)
        if r:
            for k in pools:
                pools[k].append(r[k])
    return pools


def analyze_substrate(name, week_counts, onset_date, window=PRE_W):
    weeks_sorted = sorted(week_counts.keys())
    if onset_date not in weeks_sorted:
        # snap onset to the nearest week boundary present
        onset_date = min(weeks_sorted, key=lambda w: abs((w - onset_date).days))
    onset_idx = weeks_sorted.index(onset_date)
    if onset_idx < window:
        return dict(substrate=name, status="NO_PRE_WINDOW",
                    weeks_pre_onset=onset_idx, onset=str(onset_date))
    pre = rolling_concentration(week_counts, weeks_sorted, onset_idx, window)
    if pre is None:
        return dict(substrate=name, status="EMPTY_PRE", onset=str(onset_date))
    pools = baseline_pool(week_counts, weeks_sorted, onset_idx, window)
    pct = {k: C.percentile_rank(pre[k], pools[k]) for k in ("hhi", "gini", "top5")}
    p90 = {k: (float(np.percentile(pools[k], 90)) if pools[k] else float("nan"))
           for k in ("hhi", "gini", "top5")}
    base_med = {k: (float(np.median(pools[k])) if pools[k] else float("nan"))
                for k in ("hhi", "gini", "top5")}
    flag = bool(pct["hhi"] >= 0.90 or pct["gini"] >= 0.90)
    return dict(substrate=name, status="OK", onset=str(onset_date),
                weeks_pre_onset=int(onset_idx), n_baseline_windows=len(pools["hhi"]),
                pre_onset=pre, baseline_p90=p90, baseline_median=base_med,
                percentile=pct, flag_exceeds_p90=flag)


def run():
    results = {"params": dict(pre_window_weeks=PRE_W, flag_rule="pre-onset HHI or Gini >= platform 90th pct"),
               "github": [], "askeconomics": []}

    # ----- GitHub: one cascade per repo -----
    for repo in C.GITHUB_REPOS:
        wc = C.github_author_week_commits(repo)
        if repo not in C.GITHUB_ONSETS:
            continue
        r = analyze_substrate(repo, wc, C.to_date(C.GITHUB_ONSETS[repo]))
        results["github"].append(r)

    # ----- AskEconomics comment authors (second substrate) -----
    wc = C.concordance_author_week_counts()
    # designated onset = the largest comment-activity week inside the sampled span
    weeks_sorted = sorted(wc.keys())
    onset = max(weeks_sorted, key=lambda w: sum(wc[w].values()))
    r = analyze_substrate("askeconomics_comments", wc, onset)
    r["onset_note"] = ("designated onset = peak comment-activity week in the "
                       "thread-sampled 2025-06..2026-06 span (substrate is "
                       "thread-sampled, not a continuous stream)")
    results["askeconomics"].append(r)

    # ----- cross-domain invariant summary -----
    gh_ok = [x for x in results["github"] if x.get("status") == "OK"]
    re_ok = [x for x in results["askeconomics"] if x.get("status") == "OK"]
    summary = dict(
        github_n=len(gh_ok),
        github_mean_pre_hhi=float(np.mean([x["pre_onset"]["hhi"] for x in gh_ok])) if gh_ok else None,
        github_mean_pre_gini=float(np.mean([x["pre_onset"]["gini"] for x in gh_ok])) if gh_ok else None,
        github_flag_rate=float(np.mean([x["flag_exceeds_p90"] for x in gh_ok])) if gh_ok else None,
        reddit_pre_hhi=re_ok[0]["pre_onset"]["hhi"] if re_ok else None,
        reddit_pre_gini=re_ok[0]["pre_onset"]["gini"] if re_ok else None,
        reddit_flag=re_ok[0]["flag_exceeds_p90"] if re_ok else None,
    )
    results["cross_domain_summary"] = summary

    with open(os.path.join(HERE, "result_operator_hhi.json"), "w") as f:
        json.dump(results, f, indent=2)
    make_figure(results)
    return results


def make_figure(results):
    gh = [x for x in results["github"] if x.get("status") == "OK"]
    re_ = [x for x in results["askeconomics"] if x.get("status") == "OK"]
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # panel 1: HHI pre-onset vs baseline p90
    labels = [x["substrate"] for x in gh] + [x["substrate"] for x in re_]
    pre_hhi = [x["pre_onset"]["hhi"] for x in gh] + [x["pre_onset"]["hhi"] for x in re_]
    p90_hhi = [x["baseline_p90"]["hhi"] for x in gh] + [x["baseline_p90"]["hhi"] for x in re_]
    med_hhi = [x["baseline_median"]["hhi"] for x in gh] + [x["baseline_median"]["hhi"] for x in re_]
    xs = np.arange(len(labels))
    ax = axes[0]
    ax.bar(xs - 0.2, pre_hhi, width=0.4, label="pre-onset HHI", color="#c0392b")
    ax.bar(xs + 0.2, med_hhi, width=0.4, label="baseline median HHI", color="#95a5a6")
    ax.plot(xs, p90_hhi, "k_", ms=22, mew=2.5, label="baseline 90th pct")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, rotation=40, ha="right", fontsize=8)
    ax.set_ylabel("HHI (operator concentration)")
    ax.set_title("OBJ3: pre-onset operator HHI vs platform baseline")
    ax.legend(fontsize=8)
    ax.axvline(len(gh) - 0.5, ls=":", c="b", alpha=0.6)
    ax.text(len(gh) - 0.5, ax.get_ylim()[1] * 0.95, " Reddit ->", color="b", fontsize=8)

    # panel 2: Gini same
    pre_g = [x["pre_onset"]["gini"] for x in gh] + [x["pre_onset"]["gini"] for x in re_]
    p90_g = [x["baseline_p90"]["gini"] for x in gh] + [x["baseline_p90"]["gini"] for x in re_]
    med_g = [x["baseline_median"]["gini"] for x in gh] + [x["baseline_median"]["gini"] for x in re_]
    ax = axes[1]
    ax.bar(xs - 0.2, pre_g, width=0.4, label="pre-onset Gini", color="#2980b9")
    ax.bar(xs + 0.2, med_g, width=0.4, label="baseline median Gini", color="#95a5a6")
    ax.plot(xs, p90_g, "k_", ms=22, mew=2.5, label="baseline 90th pct")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, rotation=40, ha="right", fontsize=8)
    ax.set_ylabel("Gini (operator concentration)")
    ax.set_title("OBJ3: pre-onset operator Gini vs platform baseline")
    ax.legend(fontsize=8)
    ax.axvline(len(gh) - 0.5, ls=":", c="b", alpha=0.6)

    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "figure_operator_hhi.png"), dpi=110)
    plt.close(fig)


if __name__ == "__main__":
    r = run()
    print(json.dumps(r["cross_domain_summary"], indent=2))
    for x in r["github"]:
        if x.get("status") == "OK":
            print(f"GH {x['substrate']:14s} HHI={x['pre_onset']['hhi']:.3f} "
                  f"Gini={x['pre_onset']['gini']:.3f} top5={x['pre_onset']['top5']:.3f} "
                  f"pct(hhi)={x['percentile']['hhi']:.2f} flag={x['flag_exceeds_p90']}")
        else:
            print(f"GH {x['substrate']:14s} {x['status']}")
    for x in r["askeconomics"]:
        if x.get("status") == "OK":
            print(f"RE {x['substrate']:14s} HHI={x['pre_onset']['hhi']:.3f} "
                  f"Gini={x['pre_onset']['gini']:.3f} top5={x['pre_onset']['top5']:.3f} "
                  f"pct(hhi)={x['percentile']['hhi']:.2f} flag={x['flag_exceeds_p90']}")
