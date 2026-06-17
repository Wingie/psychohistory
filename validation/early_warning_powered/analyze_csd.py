"""Falsifier (iii) POWERED early-warning analysis.

For each roster window (event pre-onset + matched calm) harvested by
harvest_text.py:
  1. load submissions, subsample per day (cap for embedding tractability),
  2. embed title+selftext locally with all-MiniLM-L6-v2 (CPU, cached .npy),
  3. compute the SEMANTIC-VARIANCE series (per-day variance of pairwise cosine
     similarity = belief dispersion) and the centroid AR1 series, IDENTICAL to
     validation/pipeline_v03/semantic_csd.py,
  4. run the SAME detrended-Kendall-tau CSD detector (common.detrended_csd) over
     the pre-onset semantic-variance series.

Classifier = pre-onset semantic-CSD score (tau_var + tau_ar1). Ground truth =
roster endo/exo label (committed below, NOT relabelled by outcome). We build a
ROC across the event roster (endo vs exo) and report AUC, plus the Boettiger
guard-banded null from the matched-calm windows.

Run:  py -3.12 analyze_csd.py   ->  result_powered.json, figure_roc.png

Honesty: retrospective, in-sample, single embedding model, submission-text proxy.
"""
import json
import os
import sys
import datetime as dt
from collections import defaultdict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
PIPE = os.path.abspath(os.path.join(HERE, "..", "pipeline_v03"))
ROSTER = os.path.abspath(os.path.join(HERE, "..", "reddit_wsb"))
sys.path.insert(0, PIPE)
sys.path.insert(0, ROSTER)
import common as C            # noqa: E402  (detrended_csd, kendall_tau)
import semantic_csd as S      # noqa: E402  (semantic_series, centroid_ar1_series, get_model)
import roster_wsb as R        # noqa: E402

MODEL_NAME = "all-MiniLM-L6-v2"
RNG = np.random.default_rng(20210125)

# Per-day cap on posts embedded (tractability; WSB submission volume is huge on
# cascade days). The semantic-variance observable is a within-day dispersion
# statistic, so a random per-day subsample is an unbiased estimator of it.
MAX_PER_DAY = 120
MIN_PER_BUCKET = 8   # min posts/day for a usable semantic-variance bucket

# ----------------------------------------------------------------------------
# Endo / exo ground-truth labels (committed from roster character, NOT outcome).
# Endogenous = reflexive meme-stock build, the crowd talking itself into the
#   position over the pre-onset window (the CSD-RISE-predicted class).
# Exogenous  = externally-triggered macro / bank / vol shock (no reflexive
#   pre-build; expect NULL early-warning).
# Mirrors roster_wsb.py justifications verbatim in spirit.
# ----------------------------------------------------------------------------
ENDO = {
    "GME_squeeze_jan2021": 1,   # canonical endogenous reflexive short squeeze
    "GME_leg2_feb2021":    1,   # reflexive second GME leg
    "AMC_meme_jun2021":    1,   # meme reflexive second wave
    "GME_runup_nov2021":   1,   # meme reflexive runup
    "gme_kitty_may2024":   1,   # Roaring Kitty reflexive return
    "market_selloff_jan2022": 0,  # exogenous macro/rate tech selloff
    "market_drop_may2022":    0,  # exogenous broad drop / LUNA
    "svb_collapse_mar2023":   0,  # exogenous bank collapse
    "regional_bank_may2023":  0,  # exogenous regional-bank shock
    "aug2024_vix_spike":      0,  # exogenous carry-unwind vol crash
}


def load_window(label, arm):
    path = os.path.join(DATA, f"{label}__{arm}.jsonl")
    by_day = defaultdict(list)
    for L in open(path, encoding="utf-8"):
        L = L.strip()
        if not L:
            continue
        o = json.loads(L)
        ts = int(o["t"])
        d = dt.datetime.fromtimestamp(ts, dt.timezone.utc).date()
        txt = ((o.get("title") or "") + ". " + (o.get("self") or "")).strip()
        if len(txt) < 12:
            continue
        by_day[d].append(dict(id=o["id"], created_utc=ts, date=d, text=txt[:2000]))
    # per-day subsample (unbiased for the within-day dispersion statistic)
    posts = []
    for d in sorted(by_day):
        rows = by_day[d]
        if len(rows) > MAX_PER_DAY:
            idx = RNG.choice(len(rows), MAX_PER_DAY, replace=False)
            rows = [rows[i] for i in sorted(idx)]
        posts.extend(rows)
    posts.sort(key=lambda x: x["created_utc"])
    return posts


def csd_score(label, arm, onset_date):
    """Run the IDENTICAL semantic-variance detrended-CSD detector on a window.
    Returns dict with the pre-onset CSD score (= the classifier value)."""
    posts = load_window(label, arm)
    if len(posts) < MIN_PER_BUCKET * 6:
        return dict(label=label, arm=arm, status="TOO_FEW_POSTS", n_posts=len(posts))
    emb = S.embed_posts(posts, f"{label}__{arm}")
    # daily semantic-variance series (identical observable to semantic_csd.py)
    dates, sem_var, cents = S.semantic_series(posts, emb, freq="day",
                                              min_per_bucket=MIN_PER_BUCKET)
    if len(dates) < 8:
        return dict(label=label, arm=arm, status="TOO_FEW_BUCKETS",
                    n_buckets=len(dates), n_posts=len(posts))
    # whole window is pre-onset by construction (harvest ends at onset), so the
    # detector runs over the full harvested series.
    csd = C.detrended_csd(sem_var, sub=4, log=False)
    cent_ar1 = S.centroid_ar1_series(cents, sub=4)
    tau_ar1 = C.kendall_tau(list(cent_ar1)) if len(cent_ar1) >= 3 else float("nan")
    return dict(label=label, arm=arm, status="OK",
                onset=str(onset_date), n_posts=len(posts),
                n_buckets=len(dates), dates=[str(d) for d in dates],
                sem_var=[float(x) for x in sem_var],
                csd=csd, score=float(csd["score"]) if csd else float("nan"),
                centroid_ar1_tau=(None if np.isnan(tau_ar1) else float(tau_ar1)))


def roc_auc(scores, labels):
    """ROC over all thresholds; AUC via trapezoid. labels in {0,1}."""
    s = np.asarray(scores, float)
    y = np.asarray(labels, int)
    order = np.argsort(-s)
    s, y = s[order], y[order]
    P = y.sum()
    N = len(y) - P
    if P == 0 or N == 0:
        return float("nan"), [], []
    tpr, fpr = [0.0], [0.0]
    tp = fp = 0
    thr = None
    pts = []
    for i in range(len(s)):
        if thr is not None and s[i] != thr:
            tpr.append(tp / P)
            fpr.append(fp / N)
        if y[i] == 1:
            tp += 1
        else:
            fp += 1
        thr = s[i]
    tpr.append(tp / P)
    fpr.append(fp / N)
    # AUC = Mann-Whitney U statistic (rank-based, ties handled)
    pos = s[y == 1]
    neg = s[y == 0]
    wins = 0.0
    for a in pos:
        wins += np.sum(a > neg) + 0.5 * np.sum(a == neg)
    auc = wins / (P * N)
    return float(auc), fpr, tpr


def mann_whitney_p(pos, neg):
    """One-sided (pos > neg) Mann-Whitney U p-value via scipy."""
    from scipy.stats import mannwhitneyu
    if len(pos) == 0 or len(neg) == 0:
        return float("nan"), float("nan")
    U, p = mannwhitneyu(pos, neg, alternative="greater")
    return float(U), float(p)


def main():
    results = {"model": MODEL_NAME, "max_per_day": MAX_PER_DAY,
               "min_per_bucket": MIN_PER_BUCKET, "pre_days": 60,
               "endo_labels": ENDO, "events": {}, "calm": {}}

    onset_of = {lab: o for lab, o, _ in R.EVENTS}

    # ---- event arm (classifier + ground truth) ----
    for label, onset_iso, _why in R.EVENTS:
        rec = csd_score(label, "event", onset_iso)
        rec["endo"] = ENDO[label]
        results["events"][label] = rec
        sys.stderr.write(f"event {label:26s} score={rec.get('score')} "
                         f"endo={ENDO[label]} status={rec['status']} "
                         f"nb={rec.get('n_buckets')}\n")

    # ---- calm arm (Boettiger guard-banded null) ----
    for label, onset_iso, _why in R.EVENTS:
        rec = csd_score(label, "calm", R.calm_onset(onset_iso))
        results["calm"][label] = rec
        sys.stderr.write(f"calm  {label:26s} score={rec.get('score')} "
                         f"status={rec['status']} nb={rec.get('n_buckets')}\n")

    # ---- ROC across the event roster: endo vs exo ----
    ev = [r for r in results["events"].values() if r["status"] == "OK"]
    scores = [r["score"] for r in ev]
    labels = [r["endo"] for r in ev]
    auc, fpr, tpr = roc_auc(scores, labels)
    endo_scores = [r["score"] for r in ev if r["endo"] == 1]
    exo_scores = [r["score"] for r in ev if r["endo"] == 0]
    U, p_mw = mann_whitney_p(endo_scores, exo_scores)

    results["roc"] = dict(
        auc=auc, fpr=fpr, tpr=tpr,
        endo_scores=endo_scores, exo_scores=exo_scores,
        endo_mean=float(np.mean(endo_scores)) if endo_scores else None,
        exo_mean=float(np.mean(exo_scores)) if exo_scores else None,
        endo_n=len(endo_scores), exo_n=len(exo_scores),
        mannwhitney_U=U, mannwhitney_p_oneside=p_mw,
        sep=(float(np.mean(endo_scores) - np.mean(exo_scores))
             if endo_scores and exo_scores else None))

    # ---- Boettiger null: calm-window CSD-score distribution ----
    calm = [r for r in results["calm"].values() if r["status"] == "OK"]
    calm_scores = [r["score"] for r in calm]
    event_scores_all = scores
    endo_event_scores = endo_scores
    if calm_scores:
        cs = np.asarray(calm_scores, float)
        def pctile_of(v):
            return float(np.mean(cs < v))
        results["boettiger_null"] = dict(
            calm_scores=calm_scores,
            calm_mean=float(np.mean(cs)), calm_std=float(np.std(cs)),
            calm_p50=float(np.percentile(cs, 50)),
            calm_p90=float(np.percentile(cs, 90)),
            n_calm=len(calm_scores),
            endo_event_mean_percentile_vs_null=pctile_of(np.mean(endo_event_scores))
                if endo_event_scores else None,
            event_percentiles_vs_null={
                r["label"]: pctile_of(r["score"]) for r in ev},
            endo_mean_score=float(np.mean(endo_event_scores)) if endo_event_scores else None,
        )
        # Mann-Whitney endo-event vs calm-null
        U2, p2 = mann_whitney_p(endo_event_scores, calm_scores)
        results["boettiger_null"]["endo_vs_calm_mannwhitney_p"] = p2

    json.dump(results, open(os.path.join(HERE, "result_powered.json"), "w"), indent=2)
    make_figure(results)

    print("\n==== POWERED SEMANTIC EARLY-WARNING (falsifier iii) ====")
    print(f"events OK: {len(ev)}/10   endo={len(endo_scores)} exo={len(exo_scores)}")
    print(f"AUC (endo vs exo)         = {auc:.3f}")
    print(f"endo mean CSD = {results['roc']['endo_mean']:.3f}   "
          f"exo mean CSD = {results['roc']['exo_mean']:.3f}   "
          f"sep = {results['roc']['sep']:.3f}")
    print(f"Mann-Whitney one-sided p (endo>exo) = {p_mw:.4f}")
    if "boettiger_null" in results:
        b = results["boettiger_null"]
        print(f"Boettiger calm-null: mean={b['calm_mean']:.3f} "
              f"p90={b['calm_p90']:.3f}  endo-event mean at "
              f"{b['endo_event_mean_percentile_vs_null']*100:.0f}th pctile of null"
              f"  (endo-vs-calm MW p={b['endo_vs_calm_mannwhitney_p']:.4f})")
    return results


def make_figure(results):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    # ROC
    ax = axes[0]
    roc = results.get("roc", {})
    if roc.get("fpr"):
        ax.plot(roc["fpr"], roc["tpr"], "-o", ms=4, color="#2980b9",
                label=f"AUC = {roc['auc']:.3f}")
    ax.plot([0, 1], [0, 1], "--", color="gray", alpha=0.6, label="chance")
    ax.set_xlabel("false positive rate (exo flagged)")
    ax.set_ylabel("true positive rate (endo flagged)")
    ax.set_title("ROC: semantic-CSD score, endo vs exo")
    ax.legend(loc="lower right")
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02)
    # score distributions
    ax = axes[1]
    roc = results.get("roc", {})
    b = results.get("boettiger_null", {})
    groups = []
    if roc.get("endo_scores"):
        groups.append(("endo events", roc["endo_scores"], "#27ae60"))
    if roc.get("exo_scores"):
        groups.append(("exo events", roc["exo_scores"], "#e67e22"))
    if b.get("calm_scores"):
        groups.append(("calm null", b["calm_scores"], "#7f8c8d"))
    for i, (name, vals, col) in enumerate(groups):
        x = np.full(len(vals), i) + RNG.normal(0, 0.04, len(vals))
        ax.scatter(x, vals, color=col, s=40, alpha=0.8)
        ax.hlines(np.mean(vals), i - 0.25, i + 0.25, color=col, lw=2)
    ax.set_xticks(range(len(groups)))
    ax.set_xticklabels([g[0] for g in groups])
    ax.axhline(0, color="k", lw=0.5, alpha=0.5)
    ax.set_ylabel("pre-onset semantic-CSD score (tau_var + tau_ar1)")
    ax.set_title("CSD-score separation + Boettiger null")
    fig.suptitle("Falsifier (iii): powered semantic critical-slowing-down across WSB roster",
                 fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "figure_roc.png"), dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
