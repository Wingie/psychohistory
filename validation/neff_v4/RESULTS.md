# Test (ii') v4: community-SPECIFICITY of the dynamic N_eff collapse -- RETRACTED

**Verdict: RETRACTED. The pass does not stand and the p-value is withdrawn.**

> This run originally reported **SEALED PASS** at binomial **p = 1.7e-7**. Both are
> withdrawn. The binomial's assumed null fire rate `p0 = 0.10` is unsupported, the
> block-label shuffle null it is scored against is degenerate on this substrate, and
> under either the measured `p0`, the degeneracy gate this file itself proposes, or the
> null the hypothesis actually implies, the frozen rule **fails**. The measurement, the
> corrected verdict and the reasons are in **`NULL_RECALIBRATION.md`** in this
> directory; the frozen re-test is `../neff_v5/PRE_REGISTRATION_neff_v5.md`. No
> replacement p-value is asserted, because none has been measured to a defensible point
> value. The rest of this file is kept as the record of what was run and what was
> claimed, with the original verdict text preserved and marked.

**As originally reported (superseded):** SEALED PASS (community-specificity, fresh
roster); all three frozen primary conditions met; no condition failed.

> **Read that superseded verdict together with "Known defects in this run" below.** A
> round-2 referee review found that the shuffle null this endpoint is scored against is
> near-degenerate on this substrate, that the null fire rate the binomial assumes was never
> measured although the measurement was computed and discarded, that "SEALED" here means
> in-session pre-registration rather than an independent timestamp, and that the endo/exo
> reading of the three silent events was assigned after seeing which events fired. None of
> that is repaired by argument, and none of it is hidden below.

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
AND (c) n >= 8 powered (K>=3) events. Here p0 = 0.10 is the construction-implied
null fire rate (under "no community-specific structure," the real partition is
exchangeable with its shuffles, so it exceeds its own 90th-percentile shuffle one time
in ten).

| condition | bar | result | pass as claimed | pass on recalibration |
|-----------|-----|--------|------|------|
| (a) fire fraction | >= 0.60 | 9/12 = 0.75 | YES | **no** (0/12 under an onset-aligned null) |
| (b) binomial tail P(X>=9 \| 12, p0) | < 0.01 | 1.658e-7 at p0=0.10 | YES | **no** (p0 = 0.10 unsupported; breaks above 0.378, and every measured value is above it) |
| (c) powered n at K>=3 | >= 8 | 12 | YES | **no** (2 survive the degeneracy gate below) |

**The right-hand column is the verdict.** `1.658e-7` is arithmetically exact given
`p0 = 0.10` and carries no other support; `p0` is doing 100% of the work. See
`NULL_RECALIBRATION.md` for the four measurements of the real false-fire rate, the
comparison of candidate nulls, and the corrected verdict.

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

## Why this was argued to be a real pass and not a tuned one (superseded)

The first two bullets below were the run's own defence. The first still stands as a
statement about endpoint selection and is irrelevant to the retraction, which is about
the null, not the endpoint. **The second is withdrawn**: "the observed 9/12 clears it by
five orders of magnitude" is exactly the claim `NULL_RECALIBRATION.md` retracts, because
those five orders of magnitude are produced entirely by an assumed `p0` that measurement
puts between 0.49 and 0.83.

- **It is the correct endpoint, pre-registered before the data.** Specificity is what
  the near-decomposability premise predicts; magnitude was a yardstick v3 showed to be
  invalid on this substrate. We did NOT relax v3's magnitude threshold (that would be
  goalpost-moving). We pre-registered a different, independently-motivated endpoint and
  ran it on a fresh disjoint roster. v3's magnitude verdict stands unchanged.
- **WITHDRAWN: "the bar is strict, not gerrymandered".** This bullet previously read
  "For n=12 even k=4 would reject H0 at 0.05; we required a supermajority (>=0.60) and a
  1% binomial tail. The observed 9/12 clears it by five orders of magnitude
  (p = 1.7e-7)." The bar is strict in `k`, and that part is true. It is not strict in the
  quantity that mattered: every one of those five orders of magnitude comes from
  `p0 = 0.10`, an assumed constant that was never measured and that measurement now puts
  between 0.49 and 0.83. At any measured value the 1% tail is not cleared at all. See
  `NULL_RECALIBRATION.md` sections 3 and 5.
- **WITHDRAWN: "the silent events confirm the reading".** This bullet previously read
  "the three non-firing events are the mechanical / exogenous ones (a direct listing, a
  Fed rate decision, a stock split); none is an endogenous community cascade, so the
  frozen-block N_eff is correctly silent, and the fires are the genuine reflexive
  episodes." We withdraw it. The roster carries **no endogenous/exogenous field**:
  `roster_v4.py:61-86` gives each event a single `why` string that is a date-provenance
  note ("Fed public calendar", "company report date", "Nasdaq reference-price date"), and
  `analyze_v4.py` stores it for display only, so it enters no computation. The endo/exo
  partition was therefore assigned **after** seeing which events fired, which makes it a
  narration of the result, not a test of it. It is also not self-consistent as applied: a
  circuit-breaker crash the day after an emergency Fed cut, a vaccine-efficacy press
  release, and a scheduled national election were counted as endogenous reflexive episodes
  because they fired, while a scheduled FOMC decision was counted as exogenous-mechanical
  because it did not. The program maintains a committed, outcome-blind endo/exo taxonomy
  elsewhere in this same tree (`early_warning_powered/analyze_csd.py:14`, "roster endo/exo
  label, committed below, NOT relabelled by outcome"), under which most of the v4 firing
  set would be labelled **exo**. The v4 narration contradicted our own discipline.
  The claim is testable and worth testing: publish an endo/exo label for every event in a
  `roster_v5.py` before harvest, under a stated rule (for example, "was the proximate
  trigger scheduled and externally dated?"), and score endo-fires-versus-exo-silent as the
  primary endpoint. Until that is run, nothing here supports the endo/exo reading.
- **china_stimulus was presented as the clean illustration of why magnitude is the wrong
  yardstick. It is better read as the clearest exhibit of the null degeneracy below.**
  Its raw drop is only 0.065, yet it beats ALL 300 shuffles (percentile 1.000), because
  its shuffle null p90 sits at 0.0028. We read that as "the signal is in the block
  STRUCTURE, not the magnitude". The competing reading, which the data does not let us
  dismiss, is that 0.0028 is not a null but numerical noise, so "beats all 300 shuffles"
  is a bar of 0.0028 rather than evidence about structure. See the next section.

## Known defects in this run, found on referee review and recorded here

These were found by an adversarial round-2 review (`logos/REVIEW_ROUND2.md`, findings
P-02, P-03, P-05, P-06, P-07) after this file was first written. They are recorded in the
file that carries the verdict, not in a separate rebuttal document.

### 1. The block-label shuffle null is near-degenerate on this substrate

"Fires" is operationally "the observed drop exceeds the 90th percentile of the 300-shuffle
null". On WSB that percentile is close to zero, so on this substrate **"fires" is in
practice a magnitude test with a very low bar**, which is not what the endpoint was sold as.
The 12 per-event `shuffle_null_p90` values, sorted:

```
0.00279  0.00360  0.00450  0.00527  0.00832  0.01334
0.01403  0.01510  0.01712  0.01792  0.09576  0.22424
median 0.013683
```

Ten of twelve sit below 0.018. For comparison, v3 measured genuinely-quiet WSB windows
dropping macro-N_eff a **median 0.098**, and v3 froze its magnitude bar at f = 0.3936 and
then reported magnitude as non-discriminating. The effective bar this run applied is about
7x *below* the median quiet-window drop, and about 29x below the magnitude bar v3 discarded
as too generous. Applying the common bar 0.0137 to v3's twelve genuinely-quiet clean windows
clears 10 of 12; applying it to these twelve cascade windows also clears 10 of 12. Those are
the same number.

Two further facts point the same way. `fires` agrees with the pure sign test
`drop_macro > 0` in 11 of these 12 events, so almost all of the endpoint's discrimination is
"did the drop come out positive". And on Wikipedia, where the identical code gives a median
event `shuffle_null_p90` of 0.4909 (36x larger), 0 of 14 events fire at drops reaching 0.61.
The verdict on each substrate is therefore set substantially by that substrate's null
geometry rather than by whether a cascade occurred.

**Where the endpoint does real work.** For the two events with a non-degenerate null it
discriminates exactly as intended: `jpow_75bp` (p90 = 0.0958) correctly does not fire at a
drop of 0.036, and `nvda_ai` (p90 = 0.2242) fires at a drop of 0.2352 with percentile 0.91.
That is the specificity test working. It is 2 of 12 events.

**What the honest repair looks like.** Publish the full per-event null distribution, not
only its p90, and add a positive-control gate to the endpoint: the test has power only where
the null p90 is comparable in scale to the observed drops. Marking events with null
p90 < 0.02 as UNPOWERED rather than FIRING removes 10 of these 12 from the powered set, at
which point frozen condition (c) (n >= 8 powered) **fails outright**. We have not re-run
under that gate, so we do not claim a verdict under it; we state that the gate is the
correct one and that this run has not passed it.

**Settled, on committed data (added with `NULL_RECALIBRATION.md`).** No re-run is needed:
the gate is a filter over `shuffle_null_p90`, which `result_neff_v4.json` already
publishes per event, so it is fully determined. It leaves `jpow_75bp_jun2022` and
`nvda_ai_aug2023`, i.e. n = 2 and k = 1, and **all three** frozen conditions fail:
(a) 1/2 = 0.50 < 0.60; (b) P(X >= 1 | 2, 0.10) = 0.190, not < 0.01, and that is at the
unsupported p0; (c) 2 < 8. A gate at 0.05 gives the identical pair; at 0.10 it gives
n = 1. There is no threshold in that neighbourhood at which this run passes.

### 2. The null fire rate that condition (b) assumes was never measured

Condition (b)'s p0 is asserted from the construction of the shuffle test rather than
measured on this substrate. The measurement existed and was thrown away: `neff_v3`'s
`derive_f_v3.py` ran all twelve genuinely-quiet clean windows through the identical
pipeline, which unconditionally computes `fires_vs_shuffle`, `shuffle_pctile_of_obs` and
`shuffle_null_p90` for every record, and then serialised a row dict
(`derive_f_v3.py:57-64`) carrying thirteen fields, none of them those three. So
`derive_f_v3.json` contains the clean-window drops but no clean-window fire rate, and this
run's pre-registration was written afterwards asserting a null fire rate while the measured
one sat one function return away. See `../neff_v3/RESULTS.md` for the full record and the
one-pass CPU fix. Whatever that measurement returns is the number condition (b) should have
used; the current binomial is calibrated against an assumption, not against this substrate.

**Estimated, four ways, in `NULL_RECALIBRATION.md` section 3 (added after this section was
written).** Synthetic no-cascade substrate through this repository's own statistic
functions: 59/120 = 0.492. The original WSB calm arm, measured with real per-window
shuffle nulls: 8/10 = 0.800. Its uncontaminated subset: 3/5 = 0.600. v3's twelve quiet
windows at an imputed common bar: 10/12 = 0.833. Condition (b) breaks above 0.378, below
all four. **No replacement constant is asserted**, and none is written into
`roster_v4.py`, because the four estimates span too wide an interval to defend a point
value. The direct measurement at n >= 30 that would close it is item 2 of
`NULL_RECALIBRATION.md` section 6 and is pre-registered as Arm C of
`../neff_v5/PRE_REGISTRATION_neff_v5.md`.

### 3. "SEALED" here means in-session pre-registration, not an independent timestamp

`validation/PREREGISTRATION_SEAL.md` pins SHA-256 digests of two files, and neither is this
run's pre-registration; until that file's revision, it did not mention neff_v4 at all. The
honesty rail below says the threshold was committed "to be folded into the FA-0 hash seal",
and it was never folded in. `git log --follow` on this run's pre-registration, roster,
harvest, analysis, result JSON and this RESULTS.md returns the same single commit for all
six, so the history carries no ordering between threshold and result. The threshold was in
fact written before the harvest, and we still say so; but that rests on our word, not on
anything a reader can check.

### 4. The endpoint itself was selected after seeing v3

v3 returned specificity PASS and both magnitude conditions FAIL in the same run, and v4 then
promoted specificity to standalone primary. Re-testing a selected endpoint on a fresh roster
is the standard remedy and it is what we did. But no multiplicity or forking-path adjustment
has been applied across the six-run neff sequence, and this repository applies exactly that
discipline elsewhere (the GameStop detector-window sweep is published with its full
0.915 -> 0.771 -> 0.379 -> 0.435 spread). The sequence should be read as **exploratory in its
choice of endpoint**, with v4 the confirmatory run for that choice and nothing more. See
`../NEFF_COLLAPSE_SYNTHESIS.md`, "Forking paths".

## Free cross-substrate check (Upgrade 3, non-gating)

Pre-onset commenter concentration replicates again: Gini 0.82-0.88 across all 12
windows, consistent with the time-invariant operator-concentration invariant seen on
WSB (original + v3), Wikipedia, and GitHub.

## Where this leaves test (ii')

**Open, and unmeasured on its correct endpoint.** Not passed, and not refuted.

This section previously read: "Across four independent runs the community-specificity of
the dynamic collapse is now: Wikipedia (population-wide, 0/14, the negative control that
confirms it needs genuine community structure), original WSB (9/10), v3 fresh WSB
(9/10), and v4 fresh pre-registered-primary WSB (9/12, binomial p=1.7e-7). The
criticality gear's actual prediction is confirmed and now carries a clean pre-registered
pass on fresh data." **All of that is withdrawn.** Those four fire counts are counts
against a null that measurement shows to be degenerate: on WSB its median event p90 is
0.0137, on Wikipedia 0.4909, roughly 36x larger, so the 0/14 versus 9/10 contrast is
substantially a difference in null geometry rather than in community structure. The
counts are not four independent confirmations of anything; they are four readings of the
same non-discriminating instrument.

The raw-magnitude half stands unchanged and is still reported straight: it is not a
magnitude anomaly versus a quiet window of the same substrate (v3), because on a
continuously high-volume forum short onset windows compress N_eff generically.

What survives from this run, at its real size: **one** of the twelve cascades
(`nvda_ai_aug2023`) produced a collapse specific to its own community partition against a
null with enough spread to have rejected it, and a second (`jpow_75bp_jun2022`) was
correctly silent against such a null. That is a small honest positive on a base of two,
and it is the reason the re-test in `../neff_v5/` is worth running rather than abandoning
the test. The defensible statement about the dynamic N_eff collapse is now: **its
onset-locking has never been tested, and the endpoint that was reported as sealing it
could not have failed.**

## Honesty rails (carried)

Analyst-frozen onsets (public event dates). In-sample primary threshold committed in
PRE_REGISTRATION_neff_v4.md before harvest, and NOT folded into the FA-0 hash seal (it was
written here that it would be; it was not, and `PREREGISTRATION_SEAL.md` now records that
gap explicitly). Tractability caps logged (USER_CAP 6000, THREAD_SUBSAMPLE 40000,
PER_THREAD_CAP 120). The block-label shuffle null is intended to guard the prosecutor's
fallacy, and on ten of these twelve events it is too degenerate to do so (defect 1 above).
Single platform, and the roster is disjoint from prior runs only in its onset dates, not in
its 112-day analysis windows. Read this as a pre-registered structural signal on a fresh
roster whose primary null is under-powered on this substrate, not as a calibrated
classifier.

## Reproduce

```
py -3.12 validation/neff_v4/harvest_v4.py     # stream the dump once (sequential, HDD-safe)
py -3.12 validation/neff_v4/analyze_v4.py     # evaluate the frozen rule ONCE
```

`result_neff_v4.json` still carries `"VERDICT": "SEALED PASS ..."`, `analyze_v4.py` still
computes it, and `roster_v4.py` still sets `BINOM_P0 = 0.10`. That is deliberate: those
artefacts are marked SUPERSEDED in place rather than patched, so the retracted run stays
bit-for-bit reproducible and this file can be checked against it. Rewriting a result file
after learning its null was wrong would be the same class of error as the one being
corrected. See `NULL_RECALIBRATION.md`, "A note on what was deliberately left unchanged".
