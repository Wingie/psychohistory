# Pre-registration: SEALED dynamic-N_eff-collapse test on a FRESH Wikipedia roster (test ii', v2)

**Status: this file is written, and f is frozen, BEFORE any fresh-roster article is
selected, harvested, or analyzed.** It exists to convert test (ii') from "directional
support" to an honest SEALED PASS or an honest NOT, with the pass line fixed in advance.

The prior frozen test (`validation/wikipedia/PRE_REGISTRATION_wiki.md`,
`validation/NEFF_COLLAPSE_SYNTHESIS.md`) was NOT a sealed pass for two reasons that were
named, not hidden:

1. The threshold **f = 0.30** was picked to beat the langchain pilot's 0.23. That is a
   competitive anchor, not a principled one.
2. The matched-calm null used a fixed **onset - 365 d** offset, which was contaminated
   (Queen Elizabeth II - 1 y and Twitter - 1 y had their own mini-events, inflating the
   calm 90th percentile to 0.29 and defeating cond3).

This v2 fixes BOTH, pre-registers the fixes, and then runs on a FRESH roster of articles
that were NOT used in any tuning.

---

## 1. The principled threshold f (derived from existing data only, frozen here)

`derive_f.py` (run BEFORE the fresh roster exists; reads ONLY the existing 20-article
tuning data in `validation/wikipedia/data/` and the verified engine) derives f by two
routes.

### Route (i) PRIMARY -- clean-null 95th percentile (this sets f)

Using the existing Wikipedia data and the V2 clean-null method (imported verbatim from
`validation/wikipedia/diagnostics/v2_clean_calm.py`): for each existing event article,
re-pick the genuinely-quietest 49-day window inside the harvested pre-onset span (lowest
focal-edit volume, with enough real activity in both baseline and probe sub-windows that
the metric stays non-degenerate), and run the frozen collapse pipeline at that clean
pseudo-onset. This yields the distribution of clean-calm N_eff drops a genuinely-quiet
window produces.

Result (n = 10 clean windows, sorted):

```
-0.895, -0.553, -0.441, -0.291, 0.000, 0.000, 0.038, 0.062, 0.136, 0.430
median 0.000   p75 0.056   p80 0.077   p90 0.165   p95 0.298   max 0.430
```

**f := the 95th percentile of the clean-null drop distribution = 0.298.** A passing event
must exceed what a genuinely-quiet window produces 95 percent of the time. This is the
principled replacement for the old hand-picked 0.30: it converges on nearly the same
number, but now because the clean-null 95th percentile lands there, not because 0.30 beat
a competitor.

**Integrity caveat, stated in advance, not used to move f:** n = 10 is small, so the 95th
percentile interpolates toward the single largest clean drop (Kobe Bryant 0.430), which
makes it the least stable summary of this distribution. We freeze f at the p95 = 0.298 as
the prompt specifies (95th percentile). We do NOT lower f to the more stable p90 = 0.165,
even though that would make a pass easier, because the pre-registration route says p95.
If a reader prefers the more robust p90, the fresh-roster median is reported against both
so the verdict is legible either way, but the SEALED line is f = 0.298.

### Route (ii) CROSS-CHECK -- engine sanity bound (does NOT set f)

The verified coupled-block engine (`engine.run_blocks` / `block_metrics`, the same macro
variance-ratio N_eff) run on SHORT, sparse windows matched to the Wikipedia bucketing
(baseline 16 buckets at W = 0, onset 8 buckets at W = 1.0; 300 trials per K):

| K | median achievable collapse | p75 |
|---|---|---|
| 3 | 0.00 | 0.67 |
| 4 | 0.72 | 0.75 |
| 5 | 0.79 | 0.80 |

A genuine synchrony event on windows this short can drive the macro collapse to
0.7 - 0.8 for K >= 4 (K = 3 is noisier, median 0.0, consistent with the empirical
heterogeneity at low K). So **f = 0.298 sits well below the physically attainable collapse**;
it is not an impossibly high bar. The long-window K = 64 E4 reference collapse is 0.186
on the sign metric (the canonical 61 -> 1.0 expressed as a drop), which is the conservative
end; the short higher-K windows reach much further. f = 0.298 is bounded above by what the
mechanism can produce and above the clean-null base rate. **f is FROZEN at 0.298.**

---

## 2. Clean-null definition (frozen)

The matched-calm null is the V2 genuinely-quiet window, NOT onset - 365 d. For each fresh
event article: slide a 49-day window across the harvested pre-onset focal-edit dates;
require the full metric span to lie inside one harvested coverage island and both the
baseline and onset probe sub-windows to contain real activity (base_vol >= 5, onset_vol
>= 3) so the metric is non-degenerate; among qualifying windows pick the one with the
LOWEST focal-edit volume in its 49-day stretch; treat its center as a clean pseudo-onset
and run the frozen collapse pipeline there. This is `quietest_pseudo_onset` /
`collapse_at`, reused verbatim.

---

## 3. Decision rule (frozen, evaluated once on the fresh roster)

Let event drops be the per-article frozen macro-N_eff collapse drops on the fresh roster
(K >= 3 articles only), and clean drops be the clean-null drops from section 2.

The dynamic-collapse mechanism (test ii') is a **SEALED PASS** iff ALL of:

1. **Magnitude.** median event drop >= **f = 0.298**.
2. **Beats the clean null.** event drops exceed clean-calm drops at the 90th percentile
   AND the event-vs-clean separation is significant one-sided (Mann-Whitney U,
   alternative = greater, **p < 0.05**). Concretely: median event drop > clean-null 90th
   percentile, and Mann-Whitney p < 0.05.
3. **Structured-substrate specificity.** on a structured substrate the collapse fires
   versus the block-label-shuffle null (observed drop >= 90th percentile of the
   300-permutation shuffle null) in **>= 50%** of event articles.
4. **Powered.** **n >= 8** fresh event articles yield a non-trivial partition (K >= 3).

If all four hold on n >= 8, test (ii') is a sealed positive and ii' is converted from
"directional support" to a sealed result. If any fail, that is reported straight, naming
exactly which condition failed and by how much. The threshold f and the rule are NOT
moved after the fresh-roster numbers are seen.

Supplementary (reported, not gating): paired Wilcoxon where event and clean windows pair
per article; the Mann-Whitney effect direction; per-article table.

---

## 4. Fresh roster inclusion rule (frozen; selection blind to collapse outcome)

- The article must have ALREADY EXISTED with steady editing before a clean EXTERNAL onset
  (a public event date, not chosen from edit data), so a pre-onset editor partition exists.
  Articles born at the event are excluded (the GitHub failure mode).
- A genuinely-quiet calm window must plausibly exist in the pre-onset span (active article
  with quiet stretches), so the clean null is computable.
- **NONE of the 20 titles in `validation/wikipedia/roster.py` may be reused.** The fresh
  roster is disjoint from all tuning data.
- Mix endogenous-community events (where the existing community synchronizes) and a few
  exogenous shocks, selected for pre-onset activity to clear K >= 3, NOT for collapse
  outcome. Aim for >= 10 so >= 8 survive K >= 3.

The fresh roster is committed in `roster_v2.py` and harvested by `harvest_v2.py` into
`validation/neff_v2/data/`.

---

## 5. Honesty rails (carried)

Single platform (Wikipedia); analyst-frozen onsets (public event dates); thresholds
committed in this file but not externally lodged to OSF/hash, so this is a sealed PILOT,
not the externally-notarized FA-0 test. The clean-null and block-label-shuffle nulls guard
the prosecutor's fallacy. f is derived from existing data, frozen before the fresh roster,
and not moved after results. Result is reported straight either way.
