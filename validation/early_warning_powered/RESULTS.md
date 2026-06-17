# Powered semantic early-warning across the WSB roster (falsifier iii) - RESULTS

**Powered POWER test of the semantic critical-slowing-down (CSD) early-warning
observable.** This converts the n=2 semantic-CSD pilot (the embedding-variance
detector that scored +0.90 on GME vs +0.01 on the 2025 tariff onset in
`validation/pipeline_v03/semantic_csd.py`) into a powered run across the full
10-cascade r/wallstreetbets roster, with a Boettiger guard-banded null.

The detector is UNCHANGED. We embed submission text (title + selftext) with
all-MiniLM-L6-v2 on CPU, compute the daily semantic-variance series (variance of
pairwise cosine similarity within each day = belief dispersion) and the centroid
AR1 series, then run the SAME detrended-Kendall-tau CSD detector
(`common.detrended_csd`, `score = tau_var + tau_ar1`) over the pre-onset window.
Only the substrate changes: WSB submission text instead of AskEconomics text.

Data: `validation/reddit_dump/.../wallstreetbets_submissions.zst` (546 MB,
streamed once, never fully decompressed). Onsets and endo/exo labels are taken
verbatim from `validation/reddit_wsb/roster_wsb.py` (committed before these
numbers were computed); labels are assigned from cascade CHARACTER, never from
the CSD outcome.

## Headline

Across the powered roster the semantic-CSD score is a **weak** endo-vs-exo
classifier (**AUC = 0.60**, n = 5 endo vs 5 exo, Mann-Whitney one-sided
p = 0.345, NOT significant) but a **real** event-vs-baseline detector: every one
of the five endogenous cascades scores ABOVE its own matched-calm window (5/5),
the endogenous-event mean sits at the **90th percentile** of the Boettiger
calm-window null, and endo-events beat the calm null with **Mann-Whitney one-sided
p = 0.020**. Pooling all ten events vs the ten calm windows is also significant
(p = 0.032).

So the honest verdict is split and we report both halves:

- **The directional claim survives and is powered.** Pre-onset semantic CSD rises
  before endogenous WSB cascades relative to guard-banded calm baselines, with a
  significant null test (p = 0.02). The n=2 pilot direction (GME positive)
  generalizes: GME_squeeze_jan2021 is at the 90th percentile of the null, and all
  five endo events clear their matched calm.
- **The endo-vs-exo SEPARATION does NOT generalize cleanly.** AUC is only 0.60 and
  the endo>exo contrast is not significant (p = 0.345), because two EXOGENOUS
  shocks (the May-2022 broad drop and the Aug-2024 VIX spike) also produced strong
  pre-onset semantic-CSD rises. The detector flags "something is building" better
  than it flags "this build is reflexive vs externally driven."

This is a HONEST PARTIAL POSITIVE, not the clean AUC the n=2 pilot hinted at.

## Numbers

| quantity | value |
|---|---|
| events scored OK | 10 / 10 (60 daily buckets each) |
| **AUC, endo vs exo** | **0.600** |
| endo mean CSD score | +0.097 |
| exo mean CSD score | +0.004 |
| endo - exo separation | +0.093 |
| Mann-Whitney one-sided p (endo > exo) | 0.345 (ns) |
| **Boettiger calm-null mean (std)** | **-0.157 (0.221)** |
| calm-null p90 | +0.106 |
| endo-event mean percentile vs null | **90th** |
| Mann-Whitney one-sided p (endo-events > calm null) | **0.020** |
| Mann-Whitney one-sided p (all events > calm null) | 0.032 |
| endo events scoring above their own calm | **5 / 5** |
| all events scoring above their own calm | 7 / 10 |

## Per-event pre-onset semantic-CSD score (ranked)

| event | endo? | CSD score | percentile vs calm null |
|---|---|---|---|
| aug2024_vix_spike | exo | +0.330 | 1.00 |
| market_drop_may2022 | exo | +0.296 | 1.00 |
| gme_kitty_may2024 | **endo** | +0.221 | 1.00 |
| GME_squeeze_jan2021 (primary) | **endo** | +0.120 | 0.90 |
| GME_runup_nov2021 | **endo** | +0.090 | 0.80 |
| GME_leg2_feb2021 | **endo** | +0.079 | 0.80 |
| AMC_meme_jun2021 | **endo** | -0.023 | 0.70 |
| regional_bank_may2023 | exo | -0.070 | 0.70 |
| market_selloff_jan2022 | exo | -0.261 | 0.30 |
| svb_collapse_mar2023 | exo | -0.274 | 0.30 |

The two failures of the endo-vs-exo separation are at the TOP of this table: the
May-2022 drop and the Aug-2024 VIX spike. Both are macro shocks that nonetheless
showed a multi-week pre-onset belief-dispersion build on WSB (the market was
visibly deteriorating and the crowd was talking itself toward the move), so the
semantic-CSD observable correctly fires "build in progress" but cannot tell that
the eventual trigger was exogenous. Conversely the two cleanest exogenous shocks,
the SVB collapse and the Jan-2022 selloff, score strongly NEGATIVE: those landed
out of a quiet pre-onset window with no semantic build, exactly the NULL the test
expects for a true exogenous surprise. So the detector's errors are interpretable,
not random.

## Boettiger null (guard-banded)

The null is the SAME detector run on matched-calm windows: for each event we take
the equal-length (60-day) pre-onset window ending at onset - 365 days
(`roster_wsb.calm_onset`), a guard-banded non-event baseline. The calm-window
CSD-score distribution is centered well below zero (mean -0.157, p90 +0.106). The
endogenous-event mean (+0.097) sits at the 90th percentile of this null and the
endo-events beat the null at p = 0.020. The calm null is cleaner here than in the
N_eff test (`reddit_wsb/RESULTS.md`) because the semantic observable is a daily
within-day dispersion statistic, far less sensitive than the co-thread-graph
collapse to the 2020-2021 GME build-up that contaminated the calm windows there.
Several calm windows still score positive (svb calm +0.190, market_selloff calm
+0.097), so we report the full distribution rather than a single threshold.

## Method (detector frozen, substrate swapped)

- **Roster:** the 10 onsets in `roster_wsb.py`, unchanged.
- **Endo/exo labels:** committed from cascade character (`analyze_csd.py:ENDO`).
  Endogenous = reflexive meme-stock build (GME Jan/Feb-2021, GME runup Nov-2021,
  AMC Jun-2021, Roaring Kitty May-2024). Exogenous = externally-triggered macro /
  bank / vol shock (Jan-2022 selloff, May-2022 drop, SVB Mar-2023, regional banks
  May-2023, Aug-2024 VIX). Five each. Labels never look at the CSD score.
- **Window:** 60 days pre-onset, daily buckets, >= 8 posts/bucket. Per-day random
  subsample capped at 120 posts (WSB submission volume is huge; the semantic
  variance is a within-day dispersion statistic so a per-day random subsample is
  an unbiased estimator of it). Every window yielded the full 60 buckets.
- **Observable + detector:** identical to `pipeline_v03/semantic_csd.py` /
  `common.detrended_csd` (sub=4, k=3 moving-average detrend, Kendall-tau of
  windowed variance + AR1).
- **Classifier:** pre-onset `score = tau_var + tau_ar1`. ROC/AUC via the
  Mann-Whitney U identity. Boettiger null = matched-calm CSD scores.

## Honesty rails

Retrospective; in-sample (no externally-lodged thresholds); submission-text proxy
(not the full comment stream); single embedding model (all-MiniLM-L6-v2); n = 5
per class so the AUC has a wide confidence interval (a single event swap moves it
substantially). The endo-vs-exo AUC of 0.60 is reported as the HONEST near-null it
is. The load-bearing positive is the narrower, better-powered claim: semantic CSD
rises before endogenous WSB cascades relative to a guard-banded calm null
(p = 0.020, 5/5 events above their own calm). We do not relabel events by outcome
to inflate the AUC, and we do not lower any threshold. We flag explicitly that the
detector cannot separate a reflexive build from an exogenous shock that happens to
be preceded by a build.

## Verdict

**Partial generalization.** The n=2 semantic-CSD direction (CSD rises before
endogenous cascades) generalizes across the powered roster as a significant
event-vs-calm-null effect (p = 0.020), but it does NOT generalize as a clean
endo-vs-exo classifier (AUC 0.60, p = 0.345): two exogenous macro shocks also
showed pre-onset semantic build. Semantic critical slowing down is a real
powered early-warning for "a belief build is underway", not a powered
discriminator of build vs shock.

## Reproduce

```
py -3.12 harvest_text.py    # stream submissions .zst -> data/<label>__<arm>.jsonl (resumable)
py -3.12 analyze_csd.py     # embed (cached .npy) + CSD + ROC -> result_powered.json, figure_roc.png
```

Artifacts: `result_powered.json` (per-event + per-calm CSD records, ROC, Boettiger
null), `figure_roc.png` (ROC + endo/exo/calm score separation), `data/` (harvested
window text + `harvest_meta.json`).
