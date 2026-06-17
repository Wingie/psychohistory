# Pre-registration: SEALED dynamic-N_eff-collapse test on a FRESH, DISJOINT WSB roster (test ii', v3)

**Status: this file, the threshold rule, the clean-null window set, the fresh roster,
and the four-condition decision rule are all written and FROZEN BEFORE any fresh-roster
event is harvested or any fresh-roster collapse number is computed.** It converts test
(ii') from "directional support" to an honest SEALED PASS or an honest SEALED NOT, with
the pass line fixed in advance.

This v3 fixes the two named, fixable failures of the prior WSB run
(`validation/reddit_wsb/result_wsb_neff.json`):

1. The threshold **f = 0.30** was hand-picked to beat a pilot (0.23). Not principled.
2. The calm/null arm used **onset - 365 days**, which for the 2021 cascades landed INSIDE
   the 2020-21 GME mania, inflating "calm" drops to 0.30-0.33 and defeating the
   event-vs-calm comparison.

v3 replaces (1) with a principled clean-null p95 and (2) with a genuinely-quiet clean-null
distribution, both frozen here before the fresh roster is touched.

---

## 0. Substrate justification (a-priori, NOT post-hoc)

The mechanism's precondition is "the EXISTING community drives the spike." On WSB comment
co-thread graphs this holds structurally: the commenters in a cascade ARE the community,
so a breaking event synchronizes the frozen pre-onset blocks rather than flooding the
article with outsiders. On Wikipedia the precondition FAILS by newcomer-flood: a breaking
event floods the article with drive-by editors outside the frozen blocks, which pushes
N_eff UP not down (measured in `validation/wikipedia/diagnostics/v1_newcomer_flood.py` and
neff_v2; even reflexive crypto events like Ethereum gave -0.88). Therefore WSB is the
theory-appropriate instrument, and this seal is scoped to the **structured / endogenous-
community regime** that the paper actually claims, NOT a population-wide claim. This
scoping is committed in advance; it is not chosen after seeing which substrate passed.

---

## 1. The principled threshold f (clean WSB null, frozen RULE; numeric value set by `derive_f_v3.py`)

**The RULE is frozen here: `f := the 95th percentile of a CLEAN WSB clean-null macro-N_eff
drop distribution.`** The numeric value of f is produced by `derive_f_v3.py` from genuinely-
quiet WSB windows and is recorded in `derive_f_v3.json` and copied into RESULTS.md. f is
computed and frozen BEFORE the fresh roster is harvested or analyzed; it is the seal line
and is NOT moved after the fresh-roster numbers are seen. p90 is reported for legibility
but the SEAL is on p95.

### 1a. Clean-null window definition (frozen)

A clean (genuinely-quiet) pseudo-onset c is selected by `clean_windows.py` such that:

- the full collapse span `[c-90d, c+22d]` lies inside the continuous daily WSB comment-
  volume record we already have (2019-10-28 .. 2024-08-26, reused from the prior run's
  `volume_scan.json`; not re-scanned);
- the 21-day onset stretch `[c-3d, c+22d]` does NOT overlap any EXCLUDED known-event date
  (padded +-21d). The frozen exclusion list = the 10 original WSB onsets + the 10 fresh-v3
  onsets + the macro events: 2020-02/03 COVID crash and trough, 2020-12-21 Tesla S&P,
  2021-01/02 GME, 2021-06 AMC, 2021-11 runup, 2022-01 selloff, 2022-02-24 Ukraine,
  2022-05 LUNA, 2022-11-08 FTX, 2023-03-10 SVB, 2023-05-01 regional banks, 2024-05-13
  GME-Kitty, 2024-08-05 VIX. (Full list in `clean_windows.py:EXCLUDED_DATES`.)
- the 21-day onset stretch's mean daily comment volume is in the LOWER HALF of the WSB
  volume distribution for its ERA (calendar year). This is the contamination fix: a clean
  window is quiet RELATIVE TO ITS OWN TIME, so a 2020 window is not disqualified merely
  for being in the high-volume COVID-growth year, and no clean window sits inside a mania.

Greedy lowest-onset-volume-first with a >=45-day minimum separation yields the FROZEN set
of **12 clean windows** (committed here, before harvest):

```
2020-06-21  2020-08-09  2020-09-27  2021-04-18  2021-12-12  2022-03-27
2022-06-26  2022-12-25  2023-09-03  2023-11-05  2023-12-24  2024-06-16
```

For each clean window the FROZEN collapse pipeline (identical to the event arm: pre-onset
co-thread graph -> blind Louvain partition -> macro variance-ratio N_eff baseline vs onset)
is run at that clean pseudo-onset, giving the clean-null drop distribution. **f := its 95th
percentile.** A window that yields K < 3 (trivial partition) contributes no drop, exactly
as in the event arm.

### 1b. Engine cross-check (does NOT set f)

`derive_f_v3.py` also runs the verified coupled-block engine (`engine.run_blocks` /
`block_metrics`, the same macro variance-ratio N_eff) on short, sparse windows matched to
the WSB bucketing (K in {3,4,5}, baseline 16 buckets at W=0, onset 8 buckets at W=1.0; 300
trials per K), reproducing the neff_v2 `derive_f.py` logic, to confirm that f sits BELOW
what the mechanism can physically produce. This is a sanity ceiling, not a threshold input.

---

## 2. Clean calm-null definition (frozen)

The calm/null comparison distribution IS the section-1a clean-null distribution (the 12
genuinely-quiet windows). **`onset - 365 days` is NOT used anywhere in v3.** This is the
fix for the prior contamination.

---

## 3. Fresh DISJOINT roster (frozen, selected BLIND to collapse outcome)

`roster_v3.py` commits 10 WSB cascades, each anchored to an EXTERNAL, publicly-dated market
event (date source documented per row in the file). **NONE of these onsets appears in the
original 10 of `validation/reddit_wsb/roster_wsb.py`.** WSB is continuously high-volume, so
every onset has a usable pre-onset partition window `[onset-90d, onset)`.

Frozen independence rule (applied to the candidate pool before harvest, blind to outcome;
overlap/proximity is a calendar fact, not a collapse number): a candidate is EXCLUDED if
its onset is within 14 days of any original-10 onset OR its full window overlaps an
original-10 window by > 0.90. This dropped three candidates that are effectively the SAME
event as an original-10 cascade: `yen_carry_jul2024` (5d from aug2024_vix_spike, its cause),
`credit_suisse_mar2023` (9d + 0.92 overlap with SVB), `meta_crash_feb2022` (10d + 0.91
overlap with the Jan-2022 selloff). The surviving 10 all have onsets >=31 days from any
original onset and full-window overlap <=0.72.

The frozen 10 fresh events (label, onset, source one-liner is in `roster_v3.py`):

```
tesla_sp500_dec2020     2020-12-21   Tesla S&P 500 inclusion effective
hood_ipo_aug2021        2021-08-04   Robinhood (HOOD) IPO debut week
evergrande_sep2021      2021-09-20   Evergrande default scare risk-off
ukraine_shock_feb2022   2022-02-24   Russia invades Ukraine, market shock
bbby_squeeze_aug2022    2022-08-08   Bed Bath & Beyond meme squeeze
jpow_jackson_aug2022    2022-08-26   Powell Jackson Hole hawkish, S&P -3.4%
ftx_collapse_nov2022    2022-11-08   FTX collapse / Binance LOI
debt_ceiling_jun2023    2023-06-01   US debt-ceiling deal passes
fitch_downgrade_aug2023 2023-08-02   Fitch US sovereign downgrade reaction
djt_media_mar2024       2024-03-26   Trump Media (DJT) trading debut
```

Onsets are public external event dates committed before harvest. They are NOT selected for
collapse size.

---

## 4. Harvest + pipeline params (frozen, identical to the prior WSB run for comparability)

`bucket_days=3`, `n_shuffle=300`, `pre_graph_days=90`, `post_days=21`, `user_cap=6000`,
`thread_subsample=40000`, `per_thread_cap=120`. Primary metric = canonical macro variance-
ratio N_eff (engine `block_metrics` definition); secondary = Pearson-Kish (legacy). Every
USER_CAP / THREAD_SUBSAMPLE cap hit is logged per run, as the prior run did. Harvest streams
the 7.07 GB `wallstreetbets_comments.zst` SEQUENTIALLY (one pass; D: is an HDD, never
concurrent streams).

---

## 5. Decision rule (FROZEN, evaluated ONCE on the fresh roster)

Let `event_drops` be the per-event frozen macro-N_eff collapse drops on the fresh roster
(K >= 3 events only), and `clean_drops` be the section-1a clean-null drops.

Test (ii') is a **SEALED PASS** iff ALL of:

1. **MAGNITUDE.** median(event_drops) >= **f** (clean-null p95).
2. **BEATS CLEAN NULL.** median(event_drops) > clean-null p90 AND Mann-Whitney U
   (event_drops vs clean_drops, one-sided `greater`) **p < 0.05**.
3. **SPECIFICITY.** observed drop >= block-label-shuffle null p90 in **>= 50%** of fresh
   events (the 300-permutation shuffle fires).
4. **POWERED.** **n >= 8** fresh events yield **K >= 3**.

If all four hold -> **SEALED PASS**. If any fail -> **SEALED NOT**, naming exactly which
condition failed and by how much. **f and the rule are NOT moved after the numbers are
seen.** Paired Wilcoxon and the per-event table are reported as supplementary / non-gating.

---

## 6. Honesty rails (carried into RESULTS.md verbatim)

Single platform (WSB). Analyst-frozen onsets are public external event dates. Thresholds
are committed in-file before results but NOT externally lodged to OSF / hash, so this is a
sealed PILOT, not the externally-notarized FA-0 test. Tractability caps (USER_CAP,
THREAD_SUBSAMPLE, PER_THREAD_CAP) are logged. The block-label-shuffle null + the clean-null
guard against the prosecutor's fallacy. The result is reported straight either way; if PASS,
it is scoped explicitly to the structured / endogenous-community regime, NOT a population-
wide claim.
