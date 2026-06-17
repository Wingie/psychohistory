# Psychohistory Framework — Pilot Backtests Against Real Reddit Data

**Date:** 2026-06-15
**Data:** harvested Reddit NDJSON (read-only) in `validation/temporal/data/`
**Script:** `validation/backtests/run_backtests.py` (run with `py -3.12`)
**Stance:** adversarial. The goal was to find where the framework FAILS, not to confirm it. All numbers below are real script outputs (see `result_*.json`), not placeholders. Malformed lines were skipped: **0 bad lines** across all 6 files.

---

## TEST (i) — Zero-Sum Attention Conservation (r/AskEconomics)

**What was computed.** 4000 posts (2025-03-04 → 2025-05-19) bucketed into 9 topics by title-keyword rules (tariffs/trade, inflation, jobs/labor, housing, stocks/markets, debt/deficit, crypto, banking, general). Built a **weekly** time series of each topic's *share* of posts. Reported total weekly volume (the "budget"), de-trended each topic-share series (linear de-trend), and computed the cross-topic pairwise correlations of the de-trended shares. Compared the mean off-diagonal correlation against the **mechanical simplex baseline** -1/(K-1).

**Actual numbers.**
- Weeks used: 11. Weekly total volume = `[287, 370, 319, 270, 635, 643, 393, 326, 309, 229, 206]`. Mean ≈ **362/wk**, **CV = 0.387**, linear trend **-10.3 posts/week** (mildly declining, but dominated by a large mid-series spike).
- The "budget" is **NOT flat**: volume more than doubled (≈300 → 635/643) in the tariff-shock weeks, then decayed. A fixed-attention-budget assumption fails *within this single sub* — attention to economics is elastic, not conserved, when a shock hits.
- Mean off-diagonal de-trended cross-topic correlation = **-0.022**. Fraction of negative pairs = **0.53**. Mechanical simplex expectation = **-0.125**.
- The observed mean correlation (-0.022) is **less negative** than the mechanical simplex constraint predicts (-0.125). So topics do **not** trade off *beyond* the simplex; if anything they co-move slightly more than the null. Strongest negative pair is `tariffs_trade ↔ general` (r=-0.985), which is essentially the mechanical "one topic crowds out the residual" effect — not evidence of a conserved attention budget. Several pairs are strongly *positive* (e.g. `debt_deficit ↔ banking` r=+0.61, `crypto ↔ general` r=+0.56).

**VERDICT: CONTRADICTS (as a within-sub test).** Net of the simplex constraint there is no genuine cross-topic trade-off, and the total budget visibly inflates under the shock. The one strong anti-correlation is a mechanical residual artifact, not conservation.

**Honest caveat.** A single subreddit is a **weak proxy** for the ecosystem-wide attention-conservation claim. Conservation in the framework is across the *whole media ecosystem*; one sub can freely import/export attention from the rest of the internet, so within-sub elasticity does NOT refute ecosystem-level conservation. Treat this as a pilot signal, not a verdict on the framework.

**What fuller data would need.** Cross-subreddit (ideally cross-platform) total attention with a fixed denominator — a panel of many subs/sites measured simultaneously — so the simplex is over the real ecosystem, plus a permutation null for the de-trended correlation matrix.

---

## TEST (iii) — Critical-Slowing-Down Early Warning (r/AskEconomics)

**What was computed.** Daily activity series (posts/day; comments/day via `num_comments` retained as a proxy). Detected the largest sustained activity jump (3-day forward mean vs 7-day trailing baseline, z-scored). Using **only data strictly before event onset** (no look-ahead), computed rolling (window=7) **variance** and **lag-1 autocorrelation** of the de-trended activity, and their trend slopes. Built a **base-rate null**: the same indicator slopes over all equal-length non-event windows (guard band around the event), then ranked the pre-event slope against that null distribution (percentile = single-positive AUC).

**Actual numbers.**
- Event detected: **2025-04-02**, z = **9.46**, ratio = **3.22×** baseline. Daily posts around onset: `…37, 52, 39, [88, 185, 117], 80, 74…`. This is the early-April US tariff-shock spike. Detector works.
- Pre-event window length = 29 days. Pre-event indicator slopes: var slope = **-7.11**, ac1 slope = **-0.016** (both essentially *flat-to-declining*, i.e. NO rise).
- Base-rate null (14 windows each): null var-slope median = -5.93, null ac1-slope median = -0.010.
- Pre-event **var-slope percentile vs null = 0.36** (AUC 0.36); pre-event **ac1-slope percentile vs null = 0.21** (AUC 0.21). Both are *below* the median of the null — the pre-event window is, if anything, slightly *less* slowing-down than a random window. No early-warning rise.

**VERDICT: NULL (theory-consistent).** Neither variance nor lag-1 autocorrelation rose before the event; both score below the null median (AUC 0.36 / 0.21, where ~0.5 = indistinguishable and >~0.8 would be a real signal).

**Key interpretation.** The tariff shock was an **exogenous policy surprise** (rate/noise-induced tipping). The framework *predicts no critical-slowing-down* for such events. The observed NULL is therefore **consistent with the framework's own claim** — and importantly, we did NOT manufacture a false positive from reactive volume. (Had we seen a strong pre-event rise beating the null, that would have been evidence *against* the CSD claim or merely reactive volume; we did not.)

**Honest caveat.** This is one event, in one sub, over ~10 weeks. A NULL on a single exogenous shock confirms the *negative* prediction but says nothing about the *positive* one (that endogenous bifurcations DO show CSD) — we have no labeled endogenous-bifurcation event here to test that direction.

**What fuller data would need.** Multiple labeled events of *both* kinds — exogenous shocks (expect null) and endogenous build-ups like bubbles/bank-runs (expect a rise) — to estimate a real ROC, not a single-point AUC.

---

## TEST (ii) — Block Synchronization / N_eff (5 location subreddits)

**What was computed.** Daily posts/day for europe, france, germany, italy, spain. Restricted to the common overlap window (bounded by r/europe's late start). Computed cross-block correlation matrix, an **N_eff via the macro variance-ratio estimator** (mean per-block temporal variance ÷ variance of the block-mean series; = N if independent, = 1 if fully synchronized), the same on standardized series, and a Kuramoto-style order parameter R = Var(z-mean)/mean Var(z-block) ∈ [0,1].

**Actual numbers.**
- Overlap: **2025-05-08 → 2025-05-19 (12 days)**. (Per-block spans differ; italy/spain go back to early April, but europe starts 05-08 and sets the common window.)
- Mean cross-block Pearson correlation = **0.592** (notably high; e.g. france↔germany 0.89, germany↔spain 0.75).
- **N_eff (raw variance-ratio) = 2.15** out of 5 blocks. **N_eff (standardized) = 1.48** out of 5.
- **Kuramoto-like order parameter R = 0.674** (0 = independent, 1 = fully synchronized).
- Synchronization spike: **2025-05-15**.

**VERDICT: INCONCLUSIVE-PILOT (method demonstrated; first number suggests strong coupling).** The numbers point to substantial synchronization (5 nominal blocks collapse to N_eff ≈ 1.5–2.2 effective), but the window is far too short to trust.

**Honest caveat.** The overlap is only **12 days**. With ~12 points, both the correlation matrix and the variance-ratio N_eff are high-variance and easily inflated by a single shared weekly/news cycle (the 05-15 spike likely dominates). This is a **feasibility pilot that demonstrates the METHOD and yields a first number, not a conclusive test.** These location subs also share language/EU-news exposure, so high coupling is unsurprising and is not evidence for the framework's specific near-decomposability prediction.

**What fuller data would need.** Months of overlapping daily data across all blocks (to stabilize variance-ratio), plus a within-block / between-block separation-of-timescales test, and a null from shuffled or unrelated subreddits to show N_eff < N is specific rather than generic.

---

## Overall Honest Assessment

What we have now **actually measured against real social data**, for the first time: (1) the event-detector and the strict-cutoff early-warning + base-rate-null pipeline are **real and working**, and on a genuinely exogenous shock they correctly returned **NULL** (AUC 0.36/0.21) — the framework's *negative* CSD prediction survived a fair test that could have falsified it; (2) the macro variance-ratio N_eff estimator runs on real multi-block data and yields a concrete number (N_eff ≈ 1.5–2.2 of 5). What we **cannot** yet claim: the zero-sum *conservation* law (the within-sub test CONTRADICTS it, but a single sub is the wrong measurement scale, so this is unresolved, not falsified), the *positive* CSD prediction (no endogenous-bifurcation event in this data), and the block-synchronization claim (12-day window is a feasibility demo only). In short: one falsifiable prediction passed a real test, one cleanly contradicts at the wrong scale, and the rest remain **internal-consistency-only** pending longer spans, more labeled events, and ecosystem-wide (cross-subreddit/cross-platform) attention totals.
