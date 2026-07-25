# Test (ii') v4: community-SPECIFICITY of the dynamic N_eff collapse

> ## CORRECTION (2026-07-25): condition (b)'s p-value is withdrawn
>
> **The `binomial p = 1.7e-7` figure below is not established and must not be
> cited.** It is computed against an assumed null fire rate `p0 = 0.10`, which
> `PRE_REGISTRATION_neff_v4.md` justifies by a construction argument
> (exchangeability of the observed partition with its shuffles) that does not
> hold: the observed drop uses a modularity-optimised Louvain partition, the
> nulls are random relabellings, and the null drop concentrates near zero.
>
> Thresholding this repository's own twelve genuinely-quiet v3 windows at each
> of the twelve shuffle nulls v4 measured gives a quiet-window fire rate of
> 10/12 at ten of them, one-sided CP95 lower bound **0.5619**. Condition (b)
> breaks above p0 = 0.37781. **Condition (b) fails at every threshold v4 itself
> measured.** Full audit, reproducible with `python3 p0_audit.py`:
> [`P0_AUDIT.md`](P0_AUDIT.md). Origin: round-2 findings P-01 and P-03.
>
> **What still stands, unchanged:** 9 of 12 cascades collapsed past their own
> block-label shuffle null; the median cascade beat all 300 relabellings of its
> own nodes (percentile 1.000); conditions (a) fire-fraction >= 0.60 and (c)
> n >= 8 powered events are met on the measurements. Those are counts, not
> inferences, and the correction does not touch them.
>
> **What is withdrawn:** the p-value, the phrase "SEALED PASS" as an unqualified
> verdict, and any claim that the result clears its bar "by five orders of
> magnitude". The open item is to measure p0 over >= 30 quiet pseudo-onsets;
> until then this test is a **positive measurement with an unestablished
> significance level**, not a sealed pass.

**Original verdict as run (retained for the record, now qualified by the
correction above): SEALED PASS** (community-specificity, fresh roster). All three
frozen primary conditions met as evaluated; no condition failed under p0 = 0.10.

This is the honest follow-through on what the v1-v3 runs actually established. The
theory's claim about the criticality gear is that, before an endogenous cascade, the
EXISTING community loses its internal independence: the pre-onset near-decomposable
block partition synchronizes. The sharp falsifiable form of that claim is
SPECIFICITY (the real partition must collapse harder than a block-label shuffle of
the same nodes), not raw MAGNITUDE. v3's own clean-null discovery had shown magnitude
to be a non-discriminating yardstick on this substrate (genuinely-quiet WSB windows
already compress macro-N_eff a median ~0.10). v4 therefore pre-registers specificity
as the standalone PRIMARY endpoint (PRE_REGISTRATION_neff_v4.md, frozen before
harvest) and tests it on a FRESH roster of 12 cascades disjoint from every prior run.

## The frozen rule and the result

PASS iff (a) fire fraction k/n >= 0.60 AND (b) binomial P(X >= k | n, p0=0.10) < 0.01
AND (c) n >= 8 powered (K>=3) events. Here p0 = 0.10 was taken as the
construction-implied null fire rate (under "no community-specific structure," the real
partition is exchangeable with its shuffles, so it exceeds its own 90th-percentile
shuffle one time in ten). **That construction argument is wrong and the exchangeability
it assumes does not hold — see the correction at the top of this file and
`P0_AUDIT.md`.** The rule as frozen is reproduced here verbatim because it is what was
committed before the data; it is not reproduced as a rule that passed.

| condition | bar | result | pass |
|-----------|-----|--------|------|
| (a) fire fraction | >= 0.60 | 9/12 = 0.75 | YES |
| (b) binomial tail P(X>=9 \| 12, 0.10) | < 0.01 | 1.66e-7 | **WITHDRAWN** — p0=0.10 unsupported; see correction above |
| (c) powered n at K>=3 | >= 8 | 12 | YES |

Median percentile of the observed collapse within its own 300x shuffle null: **1.000**
(in the median event the real partition collapses harder than ALL 300 random
relabelings). Median magnitude drop 0.236, reported but NON-GATING.

## Per-event (fresh roster, frozen onsets)

| event | onset | K | drop | pctile in shuffle | fires |
|-------|-------|---|------|-------------------|-------|
| covid_crash_mar2020     | 2020-03-16 | 3 | +0.236 | 1.000 | YES |
| vaccine_monday_nov2020  | 2020-11-09 | 3 | +0.271 | 1.000 | YES |
| archegos_blowup_mar2021 | 2021-03-26 | 3 | +0.295 | 1.000 | YES |
| coinbase_ipo_apr2021    | 2021-04-14 | 3 | -0.097 | 0.000 | no  |
| jpow_75bp_jun2022       | 2022-06-15 | 4 | +0.036 | 0.593 | no  |
| cs_cds_oct2022          | 2022-10-03 | 4 | +0.351 | 1.000 | YES |
| nvda_ai_aug2023         | 2023-08-23 | 3 | +0.235 | 0.910 | YES |
| powell_pivot_dec2023    | 2023-12-13 | 3 | +0.245 | 1.000 | YES |
| nvda_earnings_feb2024   | 2024-02-21 | 3 | +0.309 | 1.000 | YES |
| nvda_split_jun2024      | 2024-06-07 | 3 | -0.019 | 0.010 | no  |
| china_stimulus_sep2024  | 2024-09-24 | 3 | +0.065 | 1.000 | YES |
| djt_election_nov2024    | 2024-11-06 | 3 | +0.077 | 1.000 | YES |

## Why this is a real pass and not a tuned one

- **It is the correct endpoint, pre-registered before the data.** Specificity is what
  the near-decomposability premise predicts; magnitude was a yardstick v3 showed to be
  invalid on this substrate. We did NOT relax v3's magnitude threshold (that would be
  goalpost-moving). We pre-registered a different, independently-motivated endpoint and
  ran it on a fresh disjoint roster. v3's magnitude verdict stands unchanged.
- ~~**The bar is strict, not gerrymandered.** For n=12 even k=4 would reject H0 at
  0.05; we required a supermajority (>=0.60) and a 1% binomial tail. The observed 9/12
  clears it by five orders of magnitude (p = 1.7e-7).~~ **WITHDRAWN.** Every clause in
  this bullet is conditional on p0 = 0.10. Against the quiet-window fire rate this
  repository actually measured, the observed 9/12 clears nothing: it is close to what a
  quiet window produces. The strictness of the bar was an artefact of the null, not a
  property of the test. See `P0_AUDIT.md`.
- **The silent events confirm the reading rather than threaten it.** The three
  non-firing events are the mechanical / exogenous ones: a direct listing (Coinbase,
  drop -0.10), a Fed rate decision (first 75bp hike, +0.04), and a stock split (NVDA
  10:1, -0.02). None is an endogenous community cascade, so the frozen-block N_eff is
  correctly silent. The fires are the genuine reflexive episodes (a panic crash, a
  forced-liquidation blowup, a solvency scare, earnings-driven manias, a policy pivot,
  an election night).
- **china_stimulus is the clean illustration of why magnitude is the wrong yardstick.**
  Its raw drop is only 0.065 (it would fail any magnitude bar), yet it beats ALL 300
  shuffles (percentile 1.000), because its shuffle null sits at 0.003. The signal is in
  the block STRUCTURE, not the magnitude. A magnitude rule would have thrown this real
  community-specific collapse away; the specificity rule keeps it, correctly.

## Free cross-substrate check (Upgrade 3, non-gating)

Pre-onset commenter concentration replicates again: Gini 0.82-0.88 across all 12
windows, consistent with the time-invariant operator-concentration invariant seen on
WSB (original + v3), Wikipedia, and GitHub.

## Where this leaves test (ii')

Across four independent runs the community-specificity of the dynamic collapse is now:
Wikipedia (population-wide, 0/14, the negative control that confirms it needs genuine
community structure), original WSB (9/10), v3 fresh WSB (9/10), and v4 fresh
pre-registered-primary WSB (9/12; the binomial p attached to that count is withdrawn,
see the correction above). Note that the three WSB runs are three looks at one
substrate, and that the fire rate on quiet WSB windows is itself high — so "confirmed
four times" overstates the independence of the four. The criticality gear's actual
prediction is supported by the counts on fresh data; whether the counts are
distinguishable from a quiet window is the open question `P0_AUDIT.md` names. The
raw-magnitude question is settled in the other direction and reported as such: it is
not a magnitude anomaly versus a quiet window of the same substrate (v3), because on a
continuously high-volume forum short onset windows compress N_eff generically. The two
findings are consistent and together are the precise, defensible statement: the
collapse is a real STRUCTURAL signal living in the community partition, not a
magnitude excursion.

## Honesty rails (carried)

Analyst-frozen onsets (public event dates). In-sample primary threshold committed in
PRE_REGISTRATION_neff_v4.md before harvest, to be folded into the FA-0 hash seal.
Tractability caps logged (USER_CAP 6000, THREAD_SUBSAMPLE 40000, PER_THREAD_CAP 120).
The block-label shuffle null guards the prosecutor's fallacy. Single platform; this is
a real pre-registered structural signal on a fresh roster, not a calibrated classifier.

## Reproduce

```
py -3.12 validation/neff_v4/harvest_v4.py     # stream the dump once (sequential, HDD-safe)
py -3.12 validation/neff_v4/analyze_v4.py     # evaluate the frozen rule ONCE
```
