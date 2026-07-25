# Null recalibration for test (ii') v4: the binomial p = 1.7e-7 is withdrawn

**Status: the v4 SEALED PASS does not survive. It is retracted.**

This file answers round-2 finding P-01 (`logos/REVIEW_ROUND2.md`), and in doing so it
runs into P-02. It is written in the same place as the verdict it overturns, and it is
the file `RESULTS.md`, `roster_v4.py`, `README.md`, `RUN_AND_CHECK.md`,
`../NEFF_COLLAPSE_SYNTHESIS.md`, `../PRE_REGISTRATION.md` and `psychohistory.tex` now
point at.

One-paragraph summary. The v4 headline `p = 1.7e-7` is the exact binomial tail
`P(X >= 9 | n = 12, p0 = 0.10)`, and `p0 = 0.10` is asserted from construction rather
than measured. The assertion is only valid if the observed statistic is exchangeable
with the null draws it is scored against. It is not: the observation uses a
modularity-optimised Louvain partition and every null draw is a random relabelling of
the same nodes. We measured what that fire rule actually does when no cascade is
present, four different ways, and got 0.49, 0.60, 0.80 and 0.83 rather than 0.10.
Condition (b) breaks above `p0 = 0.378`, below all four. But swapping the constant is
not the repair, because the same measurements show the block-label shuffle is not a
null of anything: on this substrate the rule reduces to a sign test on
`drop_macro > 0`. The correct object is an onset-aligned null, under which `p0 = 0.10`
becomes justified by construction, and under which the best proxy we can compute from
committed data returns **0 of 12 events firing**. Restricting instead to the two events
whose null is not degenerate fails all three frozen conditions outright. That is a
negative, not a weakened positive, and we report it as one.

---

## 1. What was reproduced, and what was not

### Reproduced exactly, from committed artefacts

| quantity | recomputed | published (`result_neff_v4.json`) |
|---|---|---|
| powered events (status OK, K >= 3) | 12 | 12 |
| k, events firing vs shuffle | 9 | 9 |
| fire fraction | 0.75 | 0.75 |
| `P(X >= 9 \| n = 12, p0 = 0.10)` | 1.658350e-07 | 1.658350e-07 |
| conditions (a), (b), (c) | all true | all true |

The binomial is bit-exact against `math.comb`, so `1.7e-7` is arithmetically correct
given its inputs, and `p0` is the only contested input. We also recomputed the twelve
`fires_vs_shuffle` flags from the stored `shuffle_pctile_of_obs` values under the frozen
rule `pctile >= 0.90`, and all twelve agree with the stored flags. There is no coding
error in the v4 decision path. The defect is entirely in what `p0 = 0.10` claims.

### Not reproduced

The upstream pipeline was **not** re-run. `analyze_v4.py` needs
`validation/reddit_dump/reddit/subreddits24/wallstreetbets_comments.zst`, which is
gitignored, absent from this machine, and only obtainable as a multi-tens-of-GB
academic-torrent dump. So `drop_macro`, `shuffle_null_p90` and
`shuffle_pctile_of_obs` for the twelve WSB events are taken as published; we did not
rebuild a co-thread graph, re-run Louvain, or regenerate a 300-shuffle null on real
WSB comments. Everything below is either arithmetic over committed JSON, or the
repository's own statistic functions
(`reddit_wsb/neff_collapse_wsb.neff_macro` and `_collapse_from_user_mats`, imported
and called unmodified) run on synthetic substrate. That is a real limit on this file
and it is why section 6 names a re-run rather than declaring a replacement constant.

**The 30-quiet-window measurement P-01 asks for was not run, for that reason.** What
follows is the largest defensible substitute.

---

## 2. What `p0 = 0.10` assumes, and why it fails

`PRE_REGISTRATION_neff_v4.md:57-61`: "Under H0 ('the partition carries no
community-specific structure'), the real partition is exchangeable with its shuffles,
so each event fires with probability p0 = 0.10 (it exceeds its own 90th-percentile
shuffle by chance one time in ten)."

The reasoning is sound and the arithmetic is right. Exchangeability is the load-bearing
word, and it does not hold. The observed partition is the output of
`community_louvain.best_partition`, which maximises modularity; each null draw is
`RNG.permutation(block_vec0)`, a uniform relabelling. A modularity-optimised partition
and a uniform relabelling are not draws from a common distribution. What a relabelling
produces on WSB is K near-identical random mixtures of the same users, whose
mean-normalised activity series are all close to the same global volume series, so
`neff_macro` returns approximately 1 in both the baseline and the onset window and the
null drop concentrates on zero.

The committed data show exactly that concentration. The twelve per-event
`shuffle_null_p90` values, sorted:

```
0.00279  0.00360  0.00450  0.00527  0.00832  0.01334
0.01403  0.01510  0.01712  0.01792  0.09576  0.22424
median 0.0136828
```

Ten of twelve sit below 0.018 while the observed drops they gate run to 0.35. A null
whose 90th percentile is 0.014 does not discriminate a drop of 0.24 from a drop of
0.05; it discriminates a positive drop from a negative one. This is finding P-02, and
P-01 cannot be answered without it.

---

## 3. Measuring the false-fire rate

Four estimates. None is the 30-window measurement P-01 asks for, none is offered as a
point value, and they are listed with what is wrong with each.

### 3.1 Synthetic substrate, repository statistic, no cascade (120 trials)

We generated WSB-shaped substrate with genuine community structure and **no cascade of
any kind**: 3000 users with lognormal activity rates, K = 3 blocks, a common
autocorrelated global volume driver with heavy-tailed spikes, and independent
per-block AR(1) drivers. We then called the repository's own
`_collapse_from_user_mats` under the repository's own window geometry (3-day buckets,
90-day full window, 49-day baseline ending onset-7d, onset window onset-3d to
onset+22d) and its own 300-shuffle rule at the 90th percentile. The block-independence
amplitude was swept so the answer does not rest on one generative setting.

| block-independence alpha | fire rate with no cascade | Clopper-Pearson 95% |
|---|---|---|
| 0.35 | 21/40 = 0.525 | [0.361, 0.685] |
| 0.55 | 18/40 = 0.450 | [0.293, 0.615] |
| 0.80 | 20/40 = 0.500 | [0.338, 0.662] |
| **pooled** | **59/120 = 0.492** | **[0.399, 0.584]** |

And, decisively for section 4: **`fires_vs_shuffle` equalled `drop_macro > 0` in
120 of 120 trials.** On this substrate the fire rule is a sign test. It carries no
information about the partition at all.

Weakness: synthetic. It measures what the rule does to data with the coarse statistical
shape of WSB, not to WSB.

### 3.2 r/wallstreetbets calm arm, measured (10 windows)

`reddit_wsb/result_wsb_neff.json` ran the identical fire rule, with a real per-window
300-shuffle null, on ten matched non-event windows. **8 of 10 fire**, Clopper-Pearson
95% [0.444, 0.975]. These are genuine measurements of the rule's false-fire rate on the
real substrate, not imputations. The event arm fires 9 of 10, so Fisher exact on the
event-versus-calm fire rate is p = 0.50: the endpoint does not distinguish the two arms.

Weakness: contamination, which the repository already concedes
(`reddit_wsb/RESULTS.md:141-142`). Five of the ten calm onsets land on or beside a
market event, four of them on dates the repository's own `neff_v3/clean_windows.py`
excludes: 2020-02-25 (COVID crash onset week), 2020-11-02 (US election eve), 2021-01-24
(GameStop squeeze eve), 2022-05-01 (May-2022 broad drop / LUNA week), 2023-08-06 (four
days after the Fitch downgrade, itself a v3 event onset).

### 3.3 The uncontaminated subset of that arm (5 windows)

Dropping those five leaves 2020-01-26, 2020-06-02, 2021-05-09, 2022-03-10 and
2023-05-14: **3 of 5 fire**, Clopper-Pearson 95% [0.147, 0.947]. This is the only
estimate that is both measured and uncontaminated, and it is the weakest-powered.

### 3.4 v3's twelve genuinely-quiet windows, at an imputed bar (12 windows)

`neff_v3/derive_f_v3.py` ran all twelve of its clean quiet windows through
`analyze_run`, which computes `fires_vs_shuffle` unconditionally, and then serialised a
row dict that omits it (finding P-03). So the measurement was taken and discarded. What
survives is `clean_drops_sorted`. Imputing the v4 median shuffle-null p90 (0.0136828) as
a common bar, **10 of 12 clear it**, Clopper-Pearson 95% [0.516, 0.979]. Equivalently,
10 of 12 have `drop_macro > 0`, which by section 3.1 is the same test.

Weakness: imputed, not measured. It substitutes one common bar for twelve per-window
nulls.

### 3.5 Where that leaves the constant

| estimate | fire rate | CP 95% | P(p0 < 0.378), Jeffreys |
|---|---|---|---|
| synthetic no-cascade, repo statistic | 59/120 = 0.492 | [0.399, 0.584] | 0.006 |
| WSB calm arm, all 10 | 8/10 = 0.800 | [0.444, 0.975] | 0.003 |
| WSB calm arm, 5 uncontaminated | 3/5 = 0.600 | [0.147, 0.947] | 0.153 |
| v3 clean windows at imputed bar | 10/12 = 0.833 | [0.516, 0.979] | 0.001 |

Condition (b) `P < 0.01` breaks above **p0 = 0.377807** (bisection on the exact
binomial; at that value `P(X >= 9 | 12, p0) = 1.0000e-02`). All four point estimates
are above it. Three of the four put less than 1% posterior mass below it.

**We do not assert a corrected point value.** The review's own correction stands:
`p0 = 0.80` and a corrected `p = 0.79` are not established. Carrying the four estimates
through the frozen rule gives a corrected headline **somewhere in
`P(X >= 9 | 12) = 0.065 to 0.85`**, an interval spanning more than an order of
magnitude, and condition (b) fails at every point in it. The defensible statement is:

> `p0 = 0.10` is unsupported; condition (b) fails above `p0 = 0.378`; every available
> estimate of the false-fire rate lies above 0.378; the corrected tail probability is an
> interval, not a number.

---

## 4. What H0 should have been

Recalibrating the constant would still leave the endpoint measuring the wrong thing.
Section 3.1 measured `fires_vs_shuffle == (drop_macro > 0)` in 120 of 120 synthetic
trials, and the committed data agree: 11 of 12 in v4, 10 of 12 in the v3 quiet windows.
An endpoint that reduces to the sign of a difference is not testing specificity.

Worse, the H0 the pre-registration writes is one the repository elsewhere asserts is
false of this substrate at all times. `reddit_wsb/RESULTS.md:118-130` argues WSB fires
where Wikipedia does not *precisely because* WSB has community structure. "The partition
carries no community-specific structure" is therefore a straw H0: rejecting it says
WSB has communities, which was never in doubt and is not the theory's claim.

The claim the program actually wants is narrower and testable:

> **H1: the N_eff collapse within the existing community's frozen partition is
> time-locked to cascade onset.**
>
> **H0: it is not. The collapse statistic is what a randomly placed window on the same
> community, in the same period, would have produced.**

That H0 needs a null which destroys onset alignment and preserves everything else: the
real Louvain partition, the real per-user series, the real autocorrelation, the real
volume spikes. Four candidates.

### N1. Block-label shuffle (what v4 used)

Permute block labels; keep the onset. **Rejected.** It destroys the partition, which is
not the thing under test, and preserves the onset, which is. On this substrate it is
degenerate: measured null standard deviation 0.0020 against an observed statistic on the
scale of 0.3, i.e. **184 times too narrow**, with a false-fire rate near 0.5.

### N2. Onset-shift (recommended)

Keep the partition and the series; relocate the pseudo-onset to other admissible days
in the observation span, at least 45 days from the real onset, and recompute the whole
statistic at each. Preserves community structure, block-level autocorrelation and the
volume-spike regime; destroys only the time-locking. This isolates exactly the claim.

We ran it, through the same repository functions, on the same synthetic substrate,
against N1:

| | N1 block-label shuffle | N2 onset-shift |
|---|---|---|
| median null standard deviation | 0.0020 | 0.3576 |
| median null p90 | 0.0014 | 0.3833 |
| **fire rate, QUIET (no cascade), 20 trials** | **11/20 = 0.55** | **2/20 = 0.10** |
| **fire rate, CASCADE injected, 20 trials** | **19/20 = 0.95** | **12/20 = 0.60** |

N2's false-fire rate under no cascade is 0.10 on the nose, which is the nominal rate at
a p90 bar, and it retains 0.60 power against an injected synchronising surge. N1 fires
almost as readily without a cascade (0.55) as with one (0.95), which is the definition
of a non-discriminating test. (N1's 11/20 here and the pooled 59/120 = 0.49 of §3.1 are
separate runs at different seeds and block-independence settings; the two are consistent
within their intervals and neither is offered as a point value.)

This has a consequence that is easy to miss and matters: **under N2, `p0 = 0.10` is
correct by construction.** The pre-registration's reasoning was never the error. The
observed statistic and the onset-shifted draws genuinely are exchangeable under H0,
because they differ only in the onset date. The repair is to keep the constant and
replace the null, not the reverse.

### N3. Matched quiet-window contrast, Fisher or permutation

Score the events against a roster of genuinely-quiet pseudo-onsets, which is what
`neff_v3/clean_windows.py` already builds. This is the between-event approximation of
N2 and the review names it as the actual comparison of interest. **Recommended as the
secondary endpoint**, not the primary: it confounds onset timing with window identity,
because a quiet window has a different graph and a different partition from an event
window, where N2 holds both fixed.

### N4. Degree-preserving configuration model on the co-thread graph

Rewire the graph preserving the degree sequence, re-run Louvain, keep the onset.
**Rejected as the primary.** It answers "does Louvain find more structure than chance in
this graph", which is a question about the partition, not about the cascade. Worth
running once as a diagnostic on whether the WSB partitions are real, but it is not the
theory's endpoint. If it is ever run, it should be reported as a graph diagnostic and
never as a test of (ii').

### Recommendation

**Primary: N2, the within-event onset-shift null, with the p90 bar and `p0 = 0.10`
retained.** Secondary, non-gating: N3. Diagnostic, non-gating: N4. N1 should be retired
from this program: on Wikipedia its median event null p90 is 0.4909 and 0 of 14 fire, on
WSB its median is 0.0137 and 10 of 12 fire, so the verdict it returns is set by the
substrate's null geometry rather than by whether a cascade occurred.

---

## 5. The corrected verdict

### 5.1 Under the frozen rule with a recalibrated constant

Condition (a) `k/n >= 0.60` is unchanged at 0.75. Condition (c) `n >= 8` is unchanged at
12. Condition (b) fails at every measured estimate of `p0`:

| `p0` | `P(X >= 9 \| n = 12)` | condition (b) `< 0.01` |
|---|---|---|
| 0.10 (v4's assumption) | 1.658e-07 | pass |
| 0.378 (break point) | 1.004e-02 | fail |
| 0.444 (calm arm CP lower bound) | 3.23e-02 | fail |
| 0.492 (synthetic, pooled) | 6.5e-02 | fail |
| 0.60 (uncontaminated calm) | 2.25e-01 | fail |
| 0.80 (calm arm) | 7.95e-01 | fail |
| 0.833 (v3 clean, imputed) | 8.74e-01 | fail |

**The pass fails on condition (b) at every measured value of `p0`.** One condition
failing is enough: `PRE_REGISTRATION_neff_v4.md:63` requires all three.

### 5.1b Under the UNPOWERED gate, all three conditions fail, and this is settled

`RESULTS.md` §"Known defects" 1 proposes the correct repair for the degeneracy: an event
whose shuffle null p90 is below 0.02 has no discriminating power and should be marked
UNPOWERED rather than FIRING. It stops short of a verdict on the grounds that the run has
not been re-run under that gate. It does not need to be. The gate is a filter over
`shuffle_null_p90`, which is already published per event in `result_neff_v4.json`, so it
is fully determined by committed data and we settle it here.

Applying `shuffle_null_p90 >= 0.02` leaves two events, `jpow_75bp_jun2022` (p90 0.0958,
does not fire at a drop of 0.036) and `nvda_ai_aug2023` (p90 0.2242, fires at a drop of
0.235, percentile 0.91). So `n = 2`, `k = 1`:

| condition | bar | result | pass |
|---|---|---|---|
| (a) fire fraction | >= 0.60 | 1/2 = 0.50 | **no** |
| (b) binomial `P(X >= 1 \| 2, 0.10)` | < 0.01 | 0.190 | **no** |
| (c) powered n | >= 8 | 2 | **no** |

**All three frozen conditions fail**, and (b) fails there even at the unsupported
`p0 = 0.10`. The gate at 0.05 gives the identical set; at 0.10 it gives `n = 1`. There
is no threshold in that neighbourhood at which the v4 run passes.

### 5.1c What survives, stated at its real size

On the two events with a non-degenerate null the endpoint does exactly what it was sold
as doing: `jpow_75bp` is correctly silent against a null with real spread, and
`nvda_ai_aug2023` clears its own p90 at percentile 0.91. That is a genuine specificity
result. It is one event. The correct summary of the v4 run's positive content is **one
cascade in twelve produced a collapse specific to its own community partition against a
null capable of rejecting it**, not nine in twelve at `p = 1.7e-7`. That surviving
finding is small, real, and worth carrying forward, which is what §6 item 3 is for.

### 5.2 Under the null that should have been used

The proper N2 null needs the harvest. The best available proxy from committed data is
N3: score the twelve v4 event drops against the twelve v3 genuinely-quiet windows, same
pipeline, same frozen parameters.

Quiet-null distribution: median 0.0980, p75 0.2839, **p90 0.3604**, p95 0.3936, max
0.4286.

| v4 event | drop | percentile in the quiet null | fires at p90 | shuffle null said |
|---|---|---|---|---|
| cs_cds_oct2022 | +0.3515 | 0.833 | no | YES |
| nvda_earnings_feb2024 | +0.3090 | 0.750 | no | YES |
| archegos_blowup_mar2021 | +0.2952 | 0.750 | no | YES |
| vaccine_monday_nov2020 | +0.2708 | 0.667 | no | YES |
| powell_pivot_dec2023 | +0.2450 | 0.667 | no | YES |
| covid_crash_mar2020 | +0.2361 | 0.667 | no | YES |
| nvda_ai_aug2023 | +0.2352 | 0.667 | no | YES |
| djt_election_nov2024 | +0.0774 | 0.500 | no | YES |
| china_stimulus_sep2024 | +0.0648 | 0.417 | no | YES |
| jpow_75bp_jun2022 | +0.0361 | 0.250 | no | no |
| nvda_split_jun2024 | -0.0191 | 0.167 | no | no |
| coinbase_ipo_apr2021 | -0.0969 | 0.167 | no | no |

**k = 0 of 12.** Condition (a) needs 8 of 12 and gets 0. Condition (b), with the now
justified `p0 = 0.10`, gives `P(X >= 0 | 12, 0.10) = 1.000`. Both gating conditions fail
by the widest possible margin. Not one of the twelve v4 cascades produces a collapse
that a genuinely-quiet WSB window does not routinely produce.

Effect sizes on the same contrast, one-sided Mann-Whitney with Cliff's delta:

| contrast | n | medians | p | Cliff's delta |
|---|---|---|---|---|
| v4 events vs v3 quiet windows | 12 vs 12 | +0.2356 vs +0.0980 | 0.375 | +0.083 |
| v3 events vs v3 quiet windows (same run) | 10 vs 12 | +0.1383 vs +0.0980 | 0.069 | +0.383 |
| original WSB events vs its calm arm | 10 vs 10 | +0.2195 vs +0.1207 | 0.285 | +0.160 |
| v4 events vs original WSB calm arm | 12 vs 10 | +0.2356 vs +0.1207 | 0.617 | **-0.067** |

A permutation test on the mean difference between v4 events and v3 quiet windows
(200,000 relabellings, observed difference +0.0357) gives p = 0.306. The last row is
worth stating plainly: against the original run's calm windows the v4 cascades are, if
anything, marginally *below* the non-event windows.

The repository already published the same comparison for its own v3 events and acted on
it: `result_neff_v3.json` records `event_vs_clean_mannwhitney_p = 0.0690` and a verdict
of **SEALED NOT**. v4 did not overturn that with better evidence. It changed the null.

### 5.3 Verdict

**The v4 SEALED PASS is retracted. `p = 1.7e-7` is withdrawn and no corrected p-value
replaces it.**

Three independent routes, and they agree:

1. Under the frozen rule with any measured `p0`, condition (b) fails (§5.1).
2. Under the degeneracy gate the run's own `RESULTS.md` proposes, all three conditions
   fail on committed data (§5.1b).
3. Under the null the hypothesis actually implies, conditions (a) and (b) fail with
   k = 0 of 12 (§5.2).

They disagree about how badly the run fails and agree that it fails.

What we are **not** claiming. We are not claiming test (ii') is refuted. The N2 null has
not been run on WSB, section 5.2 is a between-event proxy for it, and the one properly
matched within-run contrast in the repository (v3 events against v3's own clean windows,
Cliff's delta +0.383, p = 0.069) is the largest effect in the table and points in the
theory's direction without reaching significance at n = 10. The honest reading is that
**test (ii') is open and unmeasured on its correct endpoint**, and that it was scored
as passed on an endpoint that could not have failed.

---

## 6. What would settle it

Three things, in order. `PRE_REGISTRATION_neff_v5.md` (in `../neff_v5/`) freezes the
rule for all three before any of them runs.

1. **Serialise what was already computed.** `derive_f_v3.py:57-64` drops
   `fires_vs_shuffle`, `shuffle_pctile_of_obs` and `shuffle_null_p90` from every clean
   window's row. Adding three keys turns section 3.4 from imputed into measured at the
   cost of one re-run of an existing script. This is finding P-03 and it is the cheapest
   real number in this file.
2. **Measure `p0` at the sample size P-01 asks for.** Extend
   `neff_v3/clean_windows.py` from 12 quiet pseudo-onsets to at least 30 by relaxing the
   minimum separation from 45 days to 21 and dropping the lowest-volume-first greedy
   selection in favour of all admissible windows, then run `analyze_v4`'s fire rule over
   them. That is the direct measurement, and it retires the interval in section 3.5.
3. **Run the N2 onset-shift null.** For each v4 event, hold the partition and the
   per-user series fixed and recompute the statistic at every admissible pseudo-onset in
   the harvested span at least 45 days away. This is cheap: `analyze_run` already builds
   the per-user bucket matrices once, and an onset shift is another pass over the same
   arrays, the same trick that makes 300 block-label shuffles tractable. It is the test
   the theory implies and the repository has never run it.

Until (3) reports, the correct entry for test (ii') in every summary table is **open**,
not **SEALED PASS** and not **refuted**.

---

## A note on what was deliberately left unchanged

`result_neff_v4.json` still carries `"VERDICT": "SEALED PASS ..."` and
`"binom_p_ge_k": 1.658350000000001e-07`. `analyze_v4.py` still computes them.
`roster_v4.py` still sets `BINOM_P0 = 0.10`. `PRE_REGISTRATION_neff_v4.md` still states
the unsound exchangeability argument in its own words. **None of that is patched, and
that is deliberate.** Editing a result file, a frozen script or a pre-registration after
discovering that its null was wrong is the same class of error as the one being
corrected, and it would destroy the audit trail that lets a reader check this document
against the run it retracts. Every one of those artefacts is marked SUPERSEDED in place,
in a comment or a header, pointing here. The retraction lives in prose, in the verdict
files, and in the paper; the data and the code stay exactly reproducible.

## Reproduce

```
# the arithmetic in sections 1, 3.2-3.5 and 5, over committed JSON only:
py -3.12 validation/neff_v4/analyze_v4.py     # needs the dump; not re-run here
# sections 3.1 and 4 call reddit_wsb/neff_collapse_wsb.{neff_macro,_collapse_from_user_mats}
# unmodified on synthetic substrate; no harvested data required.
```

Every number in sections 1, 3.2, 3.4, 5.1 and 5.2 is derived from
`neff_v4/result_neff_v4.json`, `neff_v3/derive_f_v3.json`, `neff_v3/result_neff_v3.json`
and `reddit_wsb/result_wsb_neff.json`, all committed. Sections 3.1 and 4 are synthetic
and are labelled as such wherever they are used.
