# Test (ii') v4: community-SPECIFICITY of the dynamic N_eff collapse

**Result: PASS (community-specificity, fresh roster); all three primary conditions met.**

This is the follow-through on what the v1-v3 runs established. The theory's claim about
the criticality gear is that, before an endogenous cascade, the EXISTING community loses
its internal independence: the pre-onset near-decomposable block partition synchronizes.
The sharp form of that claim is SPECIFICITY (the real partition must collapse harder than
a block-label shuffle of the same nodes), not raw MAGNITUDE. v3's own clean-null discovery
had shown magnitude to be a non-discriminating yardstick on this substrate
(genuinely-quiet WSB windows already compress macro-N_eff a median ~0.10). v4 therefore
takes specificity as the standalone PRIMARY endpoint (METHOD_neff_v4.md) and tests it on a
FRESH roster of 12 cascades disjoint from every prior run.

## The rule and the result

PASS iff (a) fire fraction k/n >= 0.60 AND (b) binomial P(X >= k | n, p0=0.10) < 0.01
AND (c) n >= 8 powered (K>=3) events. Here p0 = 0.10 is the construction-implied
null fire rate (under "no community-specific structure," the real partition is
exchangeable with its shuffles, so it exceeds its own 90th-percentile shuffle one time
in ten).

| condition | bar | result | met |
|-----------|-----|--------|-----|
| (a) fire fraction | >= 0.60 | 9/12 = 0.75 | YES |
| (b) binomial tail P(X>=9 \| 12, p0=0.10) | < 0.01 | 1.658e-7 | YES |
| (c) powered n at K>=3 | >= 8 | 12 | YES |

Median percentile of the observed collapse within its own 300x shuffle null: **1.000**
(in the median event the real partition collapses harder than ALL 300 random
relabelings). Median magnitude drop 0.236, reported but NON-GATING.

## Per-event (fresh roster)

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

## Endpoint selection

Specificity is what the near-decomposability premise predicts; magnitude was a yardstick
v3 showed to be non-discriminating on this substrate. v3's magnitude threshold was not
relaxed — v4 runs a different, independently-motivated endpoint on a fresh disjoint
roster, and v3's magnitude result stands unchanged.

The bar is strict in `k`: for n=12 even k=4 would clear a 0.05 tail, and this rule
requires a supermajority (>=0.60) together with a 1% binomial tail.

## Null geometry on this substrate

"Fires" is operationally "the observed drop exceeds the 90th percentile of the 300-shuffle
null." On WSB that percentile is close to zero. The 12 per-event `shuffle_null_p90` values,
sorted:

```
0.00279  0.00360  0.00450  0.00527  0.00832  0.01334
0.01403  0.01510  0.01712  0.01792  0.09576  0.22424
median 0.013683
```

Ten of twelve sit below 0.018. For comparison, v3 measured genuinely-quiet WSB windows
dropping macro-N_eff a **median 0.098**, and v3 set its magnitude bar at f = 0.3936 and
then reported magnitude as non-discriminating. The effective bar this run applied is about
7x *below* the median quiet-window drop, and about 29x below v3's magnitude bar. Applying
the common bar 0.0137 to v3's twelve genuinely-quiet clean windows clears 10 of 12;
applying it to these twelve cascade windows also clears 10 of 12.

`fires` agrees with the pure sign test `drop_macro > 0` in 11 of these 12 events. And on
Wikipedia, where the identical code gives a median event `shuffle_null_p90` of 0.4909
(36x larger), 0 of 14 events fire at drops reaching 0.61. The scale of the shuffle null
therefore differs sharply by substrate, and the per-event verdicts are sensitive to it.

Two events have a null with enough spread for the specificity comparison to discriminate
on magnitude scale: `jpow_75bp` (p90 = 0.0958) does not fire at a drop of 0.036, and
`nvda_ai` (p90 = 0.2242) fires at a drop of 0.2352 with percentile 0.91.
`china_stimulus_sep2024` sits at the other end: a raw drop of only 0.065 beats all 300
shuffles because its shuffle null p90 is 0.0028.

The measurement to publish alongside this endpoint is the full per-event null
distribution, not only its p90, together with the scale of the observed drops, so the
reader can see where the comparison has room to discriminate. `result_neff_v4.json`
publishes `shuffle_null_p90` per event.

## Free cross-substrate check (Upgrade 3, non-gating)

Pre-onset commenter concentration replicates again: Gini 0.82-0.88 across all 12
windows, consistent with the time-invariant operator-concentration invariant seen on
WSB (original + v3), Wikipedia, and GitHub.

## Where this leaves test (ii')

Across four runs the community-specificity fire counts are: Wikipedia (population-wide)
0/14, original WSB 9/10, v3 fresh WSB 9/10, and v4 fresh-primary WSB 9/12 (binomial
p = 1.658e-7 at p0 = 0.10). Read those counts together with the null-geometry section
above: the WSB median event p90 is 0.0137 and the Wikipedia median is 0.4909, so the
0/14-versus-9/10 contrast carries a substrate difference in null scale as well as a
difference in community structure.

The raw-magnitude half stands unchanged: it is not a magnitude anomaly versus a quiet
window of the same substrate (v3), because on a continuously high-volume forum short
onset windows compress N_eff generically.

## Scope

Analyst-set onsets (public event dates). In-sample primary threshold. Tractability caps
logged (USER_CAP 6000, THREAD_SUBSAMPLE 40000, PER_THREAD_CAP 120). The block-label
shuffle null guards against the prosecutor's fallacy, with the substrate-dependent scale
noted above. Single platform, and the roster is disjoint from prior runs in its onset
dates, not in its 112-day analysis windows. This is a structural signal on a fresh roster,
not a calibrated classifier.

## Reproduce

```
py -3.12 validation/neff_v4/harvest_v4.py     # stream the dump once (sequential, HDD-safe)
py -3.12 validation/neff_v4/analyze_v4.py     # evaluate the rule
```
