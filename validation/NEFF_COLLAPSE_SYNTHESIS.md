# Dynamic N_eff collapse (test ii'): cross-substrate synthesis

This ties together six runs that together address, in a powered form, the criticality
gear the GitHub pilot could only touch at n=1 ("only suggestive"). Same method
throughout (`validation/wikipedia/METHOD_wiki.md`): blocks from a blind pre-onset
interaction graph, canonical macro variance-ratio N_eff, baseline-vs-onset collapse drop,
fire vs 300x block-label-shuffle null at the 90th percentile, n>=8 powered. The magnitude
threshold f was hand-picked at 0.30 in the first passes, then re-derived from a
clean null in the two re-tests (neff_v2 Wikipedia f=0.298; neff_v3 WSB f=0.3936).
The decisive lesson of those re-tests was that magnitude is the WRONG endpoint on a
continuously high-volume forum (quiet windows compress N_eff just as much), so the sixth
run (neff_v4) took community-SPECIFICITY as the standalone primary endpoint and
reported 9/12 fires on a fresh roster at binomial p=1.658e-7 (at p0 = 0.10).

## The six runs

1. **Wikipedia** (`validation/wikipedia/`, n=14 articles). Editor co-editing graphs.
   Events collapse N_eff (median drop +0.19), matched-calm windows do not (median -0.25);
   event-vs-calm Mann-Whitney p=0.005, paired Wilcoxon p=0.010. But median < 0.30 and
   **0/14 fire vs shuffle** (collapse population-wide, not community-specific).
2. **Reddit / r/wallstreetbets** (`validation/reddit_wsb/`, n=10 cascades). Commenter
   co-thread graphs from the 7.1 GB Pushshift dump. Median drop +0.22; **9/10 fire vs
   shuffle** (null p90 ~0.00-0.07 vs observed 0.11-0.32). The run's verdict still fails on
   magnitude (0.22<0.30) and a contaminated calm arm.
3. **Wikipedia diagnostics** (`validation/wikipedia/diagnostics/`). Four variations that
   explain the failures mechanistically.
4. **Fresh-roster re-test, Wikipedia** (`validation/neff_v2/`, n=15 disjoint articles).
   The follow-through on the two "named, not done" upgrades below: a magnitude
   threshold **re-derived from clean quiet windows** (f=0.298 = 95th percentile of clean
   quiet-window collapse) and a **fresh disjoint roster**. Median collapse **0.00, NOT met**.
   It cleared f only on the reflexive events (Lehman +0.64, SBF +0.59) and was silent on the
   exogenous-shock majority. Consistent with the mechanism being **endogenous-specific, not
   population-wide**.
5. **Structured-substrate re-test, WSB** (`validation/neff_v3/`, n=10 fresh disjoint
   cascades). Run on the substrate where the mechanism's precondition holds (commenters in a
   cascade ARE the community, so no newcomer-flood), with BOTH prior WSB failures fixed.
   (a) The threshold was re-derived from a genuinely-quiet clean null: **f=0.3936**
   (clean-null p95); the clean windows themselves drop a median 0.098 with a heavy tail to
   0.43, so short high-volume WSB onset windows compress N_eff generically and the bar is
   correspondingly high. (b) The calm/null contamination (onset-365d landing inside the GME
   mania) was removed by using the clean-null distribution as the comparison. Result: median
   event drop **0.138 < f**, Mann-Whitney event-vs-clean **p=0.069**; but **9/10 fire vs
   shuffle** again. **NOT A PASS** (2 of 4 conditions: specificity PASS, powered PASS;
   magnitude FAIL, beats-clean-null FAIL). The threshold was not moved.
6. **SPECIFICITY-primary re-test, WSB** (`validation/neff_v4/`, n=12 fresh disjoint
   cascades). Runs 2-5 had shown the magnitude endpoint does not discriminate on this
   substrate (quiet windows compress N_eff too), and that the endpoint carrying the theory
   is SPECIFICITY (the real partition collapses past a block-label shuffle). v4 takes
   specificity as the standalone PRIMARY endpoint (`METHOD_neff_v4.md`, binomial rule:
   fire-fraction >=0.60 AND binomial P(X>=k | n, p0=0.10) <0.01 AND n>=8) and runs it on a
   fresh roster disjoint from the original-10 AND the v3-10 (COVID crash, Archegos,
   Coinbase, the Nvidia prints, Credit-Suisse, 2024 election, etc). Result: **9/12 fire,
   binomial p=1.658e-7, median observed collapse at the 100th percentile of its own 300x
   shuffle.** Read alongside "Null geometry" below: that 100th percentile is a percentile
   within a null whose median p90 is 0.0137. The choice of ENDPOINT was not a relaxation of
   the magnitude threshold, which stands.

## What the decision rule says on magnitude, on both substrates: NOT a pass

Both substrates fail the magnitude conjunction, for the SAME two reasons:
- **Magnitude.** Median collapse 0.19 (Wikipedia) / 0.22 (Reddit), both below f=0.30. The
  sensitivity sweep (diagnostic V4) shows the Wikipedia 0.19 is stable in sign across 12
  bucket/window combinations (11/12 positive) but never reaches 0.30, so the sub-threshold
  magnitude is a real property, not a tuning artifact.
- **Calm-null contamination.** The matched-calm arm (onset-365d) is contaminated on both
  substrates: on Wikipedia by 2 windows with their own mini-events; on Reddit catastrophically,
  because the -365d windows for 2021 cascades land INSIDE the 2020-21 GME mania. Diagnostic V2
  re-picks a genuinely-quietest window on Wikipedia and the event-vs-calm gate (cond3) FLIPS
  TO PASS (clean calm p90 0.165 < event median 0.193; Mann-Whitney still p=0.012). That is
  reported as a diagnosis of which failure was an artifact, and is not applied to the
  original verdict.

## What the runs DID establish

- **The collapse is real and event-specific, not a calm-window artifact.** Wikipedia
  event-vs-calm p=0.005; the clean-null diagnostic strengthens it.
- **It is community-specific where communities exist.** Wikipedia editor-on-one-article
  spikes are population-wide (0/14 fire); WSB comment co-thread graphs have genuine internal
  blocks (K=3-4, the synchronization concentrated in the real blocks), and there the collapse
  fires 9/10 vs shuffle. So cond2 did not fail because the theory is wrong; it failed on
  Wikipedia because the editor graph for a single breaking article has little block structure
  to be specific about, and it PASSES on the substrate that has the structure. The
  substrate difference in null scale reported under "Null geometry" bears on how much of the
  contrast this reading can carry.
- **The collapse measures the EXISTING community losing independence.** Diagnostic V1:
  collapse magnitude correlates with the existing-editor share of onset activity
  (Spearman rho +0.45). Pure exogenous shocks that flood with NEW editors outside the
  pre-onset blocks (Suez 3% existing -> -0.40, Kobe 5% -> -0.27, NATO 8% -> -0.02) do not
  collapse the pre-onset partition; events where the existing community synchronizes
  (Evergrande, Maradona, Zelenskyy, Queen Elizabeth II) collapse hard. This is the
  endogenous-vs-exogenous distinction emerging from the metric itself.
- **Operator concentration replicates cross-domain (free Upgrade-3 check).** WSB pre-onset
  Gini 0.82-0.86, top-5% share 0.66-0.77 in every window; Wikipedia editor concentration
  also high. Consistent with the time-invariant concentration invariant.

## Where test ii' stands

From "only suggestive, n=1" to a powered six-run investigation on two substrates. The
single-anecdote objection is gone.

The criticality gear's prediction is community-SPECIFICITY: the effective number of
independent blocks collapses within the existing community's pre-onset partition. The four
fire counts are Wikipedia 0/14, original WSB 9/10, neff_v3 fresh WSB 9/10, neff_v4 fresh
primary-endpoint WSB 9/12.

What about magnitude? The first passes tried a blunter yardstick, a MAGNITUDE
threshold on the raw collapse. Runs 2-5 carried that out (neff_v2 Wikipedia
re-derived f=0.298, fresh roster, median 0.00; neff_v3 WSB re-derived f=0.3936 from a
genuinely-quiet clean null, fresh roster, median 0.138 < f, Mann-Whitney p=0.069). The
decisive discovery there was in the null itself: genuinely-quiet WSB windows already drop
macro N_eff a median 0.098 with a tail to 0.43, because short high-volume onset windows
compress N_eff generically. So MAGNITUDE IS THE WRONG INSTRUMENT on this substrate,
reported with the threshold never moved. neff_v4 then stopped scoring the wrong quantity
and scored specificity itself, on new data.

The magnitude half is settled: the collapse is **not** a raw-magnitude excursion, which
the near-decomposability premise never required it to be.

## The two endpoints across the six runs

| run | substrate | magnitude endpoint | specificity endpoint |
|---|---|---|---|
| 1 Wikipedia | wiki | FAIL (median 0.19 < f=0.30) | FAIL (0/14) |
| 2 original WSB | wsb | FAIL (median 0.22 < f=0.30) | PASS (9/10) |
| 3 wiki diagnostics | wiki | diagnostic only | diagnostic only |
| 4 neff_v2 | wiki | FAIL (median 0.00 < f=0.298) | not primary |
| 5 neff_v3 | wsb | FAIL (median 0.138 < f=0.3936) | PASS (9/10) |
| 6 neff_v4 | wsb | reported NON-GATING | standalone PRIMARY, PASS (9/12) |

Specificity became the primary endpoint at run 6, after run 5 returned the magnitude /
specificity split within a single run. Run 6 re-tests that endpoint on a fresh roster.

## Null geometry of the specificity endpoint

Across the 12 v4 events the per-event `shuffle_null_p90` values are [0.00279, 0.00360,
0.00450, 0.00527, 0.00832, 0.01334, 0.01403, 0.01510, 0.01712, 0.01792, 0.09576, 0.22424],
median 0.0137, with 10 of 12 below 0.018. So on this substrate "fires vs shuffle" applies a
bar around 0.014, which is 7x below the median collapse of a genuinely-quiet WSB window
(0.098, measured in neff_v3) and 29x below the f = 0.3936 that neff_v3 set and then
reported as non-discriminating. Applying the 0.0137 bar to neff_v3's twelve clean quiet
windows clears 10 of 12; applying it to the twelve v4 cascades also clears 10 of 12.
`fires` agrees with the bare sign test `drop_macro > 0` on 11 of the 12 v4 events. The
endpoint discriminates on scale for the two events whose null has real spread (`jpow`
silent at p90 0.0958; `nvda_ai` fires at p90 0.2242).

Wikipedia's median event null p90 is 0.4909, 36x WSB's, so the 0/14 versus 9/10 split
carries a difference in null geometry between substrates alongside any difference in block
structure.

The measurement that would calibrate the endpoint on this substrate is the quiet-window
fire rate. neff_v3's `derive_f_v3.py` ran all twelve genuinely-quiet clean windows through
the identical pipeline, which computes `fires_vs_shuffle`, `shuffle_pctile_of_obs` and
`shuffle_null_p90` on every record, and then serialised a thirteen-field row dict
containing none of them. Recovering it is a single CPU pass over already-harvested data;
see `neff_v3/RESULTS.md`.

## Scope

Two substrates, analyst-set onsets (public event dates / volume peaks), in-sample
thresholds. Tractability caps on WSB logged (USER_CAP 6000, THREAD_SUBSAMPLE 40000,
touching <2% of threads). Shuffle and calm nulls guard against the prosecutor's fallacy.
Illustrative of direction, magnitude, and mechanism across real rosters, not a calibrated
classifier.

## Reproduce

```
# Wikipedia
py -3.12 validation/wikipedia/harvest.py
py -3.12 validation/wikipedia/neff_collapse_wiki.py
py -3.12 validation/wikipedia/diagnostics/v1_newcomer_flood.py   # + v2,v3,v4
# Reddit (needs the dump in validation/reddit_dump/)
py -3.12 validation/reddit_wsb/harvest_filter.py
py -3.12 validation/reddit_wsb/neff_collapse_wsb.py
# Fresh-roster re-test (Wikipedia)
py -3.12 validation/neff_v2/derive_f.py
py -3.12 validation/neff_v2/harvest_v2.py
py -3.12 validation/neff_v2/analyze_v2.py
# Magnitude re-test (WSB structured substrate, clean null + re-derived f) = NOT A PASS on magnitude
py -3.12 validation/neff_v3/harvest_v3.py
py -3.12 validation/neff_v3/derive_f_v3.py
py -3.12 validation/neff_v3/analyze_v3.py
# SPECIFICITY-primary re-test (WSB, fresh roster, binomial rule)
py -3.12 validation/neff_v4/harvest_v4.py
py -3.12 validation/neff_v4/analyze_v4.py
```
