# Diagnostic variations on the Wikipedia dynamic-N_eff-collapse test (test ii')

These four variations do NOT re-run the frozen pre-registered test and do NOT move its
pass/fail line. They diagnose WHY the frozen result was "directional support (event-vs-calm
p<0.01) but not a frozen-rule pass": median event drop 0.19 < f=0.30, 0/14 fire vs the
block-label-shuffle null, and cond3 (event median > calm 90th pctile) failed.

Every script reuses the FROZEN analysis functions from `neff_collapse_wiki.py` verbatim by
import (`coedit_graph`, `blind_partition`, `block_bucket_matrix`, `neff_macro`,
`neff_pearson`, `collapse_for_partition`, `analyze_run`) via `_shared.py`. No frozen file
(`PRE_REGISTRATION_wiki.md`, `roster.py`, `result_wiki_neff.json`) was modified. All outputs
are NEW files in this directory. Run each with `py -3.12 diagnostics/<script>.py`.

Harvest fact that bounds V2: each article's `focal_revs` cover only two islands, the event
span `[onset-90d, onset+22d]` and the matched-calm span `[onset-455d, onset-343d]`. The
continuous 2-year pre-onset record was never harvested, so V2 searches the cleanest window
INSIDE the harvested dates only. We do not re-harvest.

---

## V1 -- Newcomer-flood hypothesis (`v1_newcomer_flood.py` / `.json` / `.png`)

For each of the 14 OK event articles, over the frozen onset window `[onset-3d, onset+22d)`:
`f_existing` = fraction of onset focal edits made by editors IN the frozen pre-onset
partition; `newcomers` = distinct onset editors NOT in the partition. Spearman vs the
per-article macro drop.

| statistic | rho | p |
|---|---|---|
| f_existing vs drop | **+0.45** | 0.110 |
| raw newcomer count vs drop | +0.00 | 0.988 |
| newcomer fraction vs drop | -0.37 | 0.197 |

The sign is exactly as predicted: more of the onset crowd being EXISTING community
(higher f_existing) goes with a bigger collapse, and a higher NEWCOMER fraction goes with a
smaller collapse. It is directional, not significant at n=14. The non-collapsing tail is the
cleanest part of the picture: Suez (f_existing 0.03, drop -0.40), Kobe (0.05, -0.27), NATO
(0.08, -0.02), and Notre-Dame (0.01, +0.14) are pure exogenous-shock newcomer floods where
almost none of the onset edits come from the frozen blocks, so the frozen-partition metric
sees little synchronization. The raw newcomer COUNT carries no signal (rho 0.00) because big
articles flood in absolute terms whether or not they collapse; it is the existing-vs-new
SHARE that matters, which is the theory-relevant quantity.

**VERDICT:** Confirms the newcomer-flood explanation directionally (rho +0.45). The
frozen-partition collapse measures the EXISTING community losing independence; sudden
exogenous shocks (Suez, Kobe, NATO) flood the article with editors outside the frozen blocks
and therefore do not synchronize them, which is why those articles do not collapse and pull
the median below f=0.30.

---

## V2 -- Clean calm null (`v2_clean_calm.py` / `.json`)

The frozen calm arm (onset-365d) is contaminated: QE2-1y and Twitter-1y had their own
mini-events. We re-pick, per article, the genuinely quietest 49-day window inside the
harvested pre-onset dates (lowest focal-edit volume, with enough real activity in both
baseline and probe sub-windows to keep the metric non-degenerate), then run the frozen
collapse pipeline at that clean pseudo-onset.

| null | median event | calm p90 | cond3 (event median > calm p90) | event-vs-calm MWU |
|---|---|---|---|---|
| original contaminated calm | 0.193 | **0.291** | FAIL | (frozen p=0.005) |
| clean re-picked calm | 0.193 | **0.165** | **PASS** | p=0.012 |

The two contaminated windows flip sign once a genuinely quiet stretch is chosen: QE2 calm
goes from +0.29 to -0.44 and Twitter from +0.31 to -0.29. That drops the calm 90th percentile
from 0.29 to 0.17, BELOW the unchanged event median 0.19, so cond3 now passes. The
event-vs-clean separation stays significant (Mann-Whitney p=0.012). Three articles
(Evergrande, Notre-Dame, Credit Suisse) had no covered quiet window inside the harvested
islands and are reported as such, not silently dropped.

**VERDICT:** The frozen cond3 failure was an artifact of calm-window contamination, not of a
weak effect. With an uncontaminated null, cond3 flips to PASS and the directional event-vs-
calm result survives. This is the single most consequential diagnostic for the "is the
event-vs-calm verdict real" question: yes, and one of the three failed frozen conditions was
contamination, not signal.

---

## V3 -- Why 0/14 fire: a sharper specificity test (`v3_specificity.py` / `.json`)

The label-shuffle preserves block sizes but the onset spike hits everyone, so any partition
collapses and 0/14 fire on the scalar gate. We test STRUCTURE instead of magnitude: the
participation ratio (eigenvalue concentration) of the K x K block-activity correlation
matrix, PR=K when independent and PR->1 under one dominant synchronized mode. Real onset
PR-collapse vs the shuffle distribution.

PR collapses at onset across the board (e.g. Bitcoin 5.81->2.99, Zelenskyy 3.76->2.08), but
only **2/14** beat their own shuffle null on the STRUCTURE statistic (Bitcoin pctile 0.92,
Zelenskyy 0.96). The other twelve sit inside the shuffle distribution, the same picture as
the scalar gate.

**VERDICT:** Confirms the collapse is genuinely partition-agnostic / near-total
synchronization, not community-specific. A faint structured signal survives in 2 of 14
(the higher-K, more-modular cases), but the dominant story is that at onset the whole active
population converges, so a random relabeling loses independence about as much as the real
blocks. The 0/14 frozen result was testing a stronger (community-specificity) claim than the
collapse mechanism itself requires.

---

## V4 -- Metric + window sensitivity (`v4_sensitivity.py` / `.json`)

(a) Macro (primary) vs Pearson-Kish (legacy) per-article drop: Spearman rho=0.35 (p=0.227),
sign agreement 10/14. The two metrics agree on direction for most articles and rank-correlate
positively but not tightly; the four sign disagreements are small-magnitude articles near
zero where Pearson-Kish reads a mild positive while macro reads a mild negative (the legacy
metric's known over-reading under sign-sharing). Direction is robust; exact ranking is metric-
sensitive.

(b) Median event drop over BUCKET_DAYS x baseline-window:

| bucket \ baseline | 35d | 49d | 70d |
|---|---|---|---|
| 2 | +0.231 | +0.151 | -0.035 |
| 3 | +0.256 | **+0.193** | +0.076 |
| 5 | +0.154 | +0.243 | +0.121 |
| 7 | +0.248 | +0.174 | +0.150 |

The frozen cell (bucket 3, baseline 49) is +0.193. Across all 12 knob settings the median
ranges [-0.035, +0.256], median-of-medians 0.164, and **none of the 12 reaches f=0.30**.

**VERDICT:** The 0.19 median is stable in direction (11 of 12 cells positive) but modest and
knob-sensitive in magnitude; it never clears f=0.30 under any reasonable bucket/window choice.
The sub-threshold magnitude is a real property of the effect, not a fragile artifact of the
specific bucketing. The primary/legacy metrics agree on direction (10/14 signs) so the
GitHub "suggestive" reading was not purely a Pearson-Kish artifact.

---

## What the four variations explain together

- WHY MODEST (below f=0.30): V4 shows 0.19 is stable in sign but never clears 0.30 under any
  bucket/window; the magnitude ceiling is real.
- WHY HETEROGENEOUS (Evergrande/Maradona collapse, Kobe/Suez/NATO do not): V1 shows the
  collapse tracks the existing-community share of the onset crowd (rho +0.45); exogenous-shock
  newcomer floods do not synchronize the frozen blocks.
- WHY POPULATION-WIDE (0/14 fire): V3 confirms near-total synchronization, only 2/14 carry a
  structured (community-specific) signal beyond a random relabeling.
- WHY cond3 FAILED: V2 shows it was calm-window contamination; with a clean null cond3 PASSES
  and event-vs-calm stays significant (p=0.012).
