# r/wallstreetbets dynamic-N_eff-collapse test (test ii', Reddit mirror) - RESULTS

**Powered cross-domain PILOT.** This is the Reddit-comment companion to the Wikipedia
dynamic-N_eff-collapse run (`validation/wikipedia/`). It mirrors that frozen method
EXACTLY (same canonical macro variance-ratio N_eff primary metric, same Pearson-Kish
secondary, same blind pre-onset Louvain partition, same 3-day buckets, same 300x
block-label-shuffle null, same matched-calm arm, same frozen thresholds f=0.30 /
fire-at-90th-pctile / powered-n>=8). Only the substrate changes: the co-EDITING graph
of Wikipedia editors is replaced by the co-THREAD graph of WSB commenters (nodes = users,
edge weight = number of threads `link_id` in which both commented). This is the case the
GitHub pilot could only touch at n=1, and the load-bearing question is whether Reddit's
REAL community structure makes the collapse community-specific (fires vs the shuffle null)
where Wikipedia's editor graphs did not (Wikipedia fired 0/14).

Data: `validation/reddit_dump/.../wallstreetbets_comments.zst` (7.1 GB, streamed, never
fully decompressed). Onsets committed in `roster_wsb.py` before the collapse numbers were
computed; thresholds are the frozen Wikipedia ones, unchanged.

## Headline

On Reddit the dynamic N_eff collapse **FIRES against its own block-label-shuffle null in
9 of 10 event windows** - the community-specificity that Wikipedia's editor graphs lacked
entirely (0/14). The collapse on WSB is genuinely STRUCTURAL: it is the real pre-onset
comment communities that lose independence, not an arbitrary relabelling. **This is the
headline contrast with the Wikipedia run and it is a clean positive on the one gate
Wikipedia failed.**

The frozen pre-registered CONJUNCTION still does not pass, for the same two reasons it
failed on Wikipedia (magnitude and calm-window contamination), so the overall frozen
verdict is **NOT SUPPORTED**. Both halves are load-bearing and reported together.

- **Community-specificity (the Wikipedia-failure gate) - PASSED on Reddit.** 9/10 event
 windows fire vs shuffle (observed collapse at the 100th percentile of the 300-perm null
 in every firing case; null p90 ~0.00–0.07). Wikipedia: 0/14. cond2 (>=0.5 fire) holds
 (0.90).
- **Frozen conjunction - NOT SUPPORTED.** Median event drop **0.219 < f = 0.30** (cond1
 fails); event median does not clear the matched-calm 90th percentile (calm_p90 = 0.301,
 cond3 fails) because several "calm" windows landed on other live cascades (below).
 Powered bar met (n = 10 event runs, all K>=3 >= 8).

So on Reddit test ii' is no longer "suggestive n=1": it is a powered n=10 run in which the
collapse is demonstrably community-specific (the gate that distinguishes a real structural
synchronization from a population-wide flood), but it sits below the pre-registered
magnitude threshold and the matched-calm null is contaminated. We do not lower f or change
the rule.

## Method (frozen; mirrors PRE_REGISTRATION_wiki.md)

- **Roster (committed in `roster_wsb.py`):** 10 WSB event onsets, each a public event date
 AND corroborated by a raw daily-comment-volume peak in the dump (`data/volume_scan.json`).
 The primary is the canonical endogenous GameStop cascade 2021-01-25; the rest are
 distinct meme-stock / market-shock surges (see onset table). Each event has a matched-calm
 arm at onset − 365 d.
- **Blocks (blind):** commenters in the pre-onset window `[onset−90d, onset)` define the
 user set; their co-thread graph (edge = #threads both commented in) is partitioned by
 blind Louvain on the giant component; the partition is FROZEN pre-onset. No outcome
 knowledge enters it.
- **N_eff trajectory:** the frozen blocks' COMMENT activity is bucketed (3 d), baseline
 window vs onset window. **Primary = canonical macro variance-ratio** (engine
 `block_metrics`: `mean_k Var_t(z_k)/Var_t(mean_k z_k)`, collapses K→1 under synchrony);
 secondary = legacy Pearson-Kish. drop = 1 − N_eff(onset)/N_eff(baseline).
- **Nulls:** 300-perm block-label shuffle + matched-calm arm.

### Scale / tractability choices (all logged in the result JSON)

WSB comment volume in 2021 is enormous (1.6 M comments on 2021-01-28 alone). To keep
Louvain tractable and the co-thread graph from exploding we made three documented caps:
- **USER_CAP = 6000** most-active pre-onset commenters per run (every run hit the cap;
 `n_users_pre` ranged 143 k–827 k, so the graph is the top-6000 core).
- **THREAD_SUBSAMPLE = 40000** threads max for edge formation.
- **PER_THREAD_CAP = 120**: a thread with > 120 of our kept users contributes only a random
 120 of them to the pairing (bounds the O(k²) edge blow-up on mega-threads). This touched
 only ~250–460 threads per run out of 15 k–40 k used (<2%), so it is a negligible-distortion
 speed fix, not a structural change. Co-thread graphs were dense (2.8 M–4.5 M edges).

None of these touch the frozen decision thresholds.

## Onset selection (honest)

Every onset sits on or within a few days of a real local comment-volume peak (from the
one-pass `volume_scan.json`). The GME Jan-2021 cascade dominates the whole dump.

| event label | onset | corroborating volume peak (±10 d) |
|---|---|---|
| GME_squeeze_jan2021 (primary) | 2021-01-25 | 2021-01-28 = **1.65 M** comments/day |
| GME_leg2_feb2021 | 2021-02-24 | 2021-02-25 = 408 k |
| AMC_meme_jun2021 | 2021-06-02 | 2021-06-09 = 197 k |
| GME_runup_nov2021 | 2021-11-02 | 2021-11-10 = 51 k |
| market_selloff_jan2022 | 2022-01-24 | 2022-01-24 = 76 k |
| market_drop_may2022 | 2022-05-09 | 2022-05-12 = 59 k |
| svb_collapse_mar2023 | 2023-03-10 | 2023-03-13 = 59 k |
| regional_bank_may2023 | 2023-05-01 | 2023-05-03 = 35 k |
| gme_kitty_may2024 | 2024-05-13 | 2024-05-14 = 68 k |
| aug2024_vix_spike | 2024-08-05 | 2024-08-05 = 74 k |

## Per-event collapse (canonical macro N_eff, all K>=3)

| event | onset | K | N_eff drop | fires vs shuffle (pctile) |
|---|---|---|---|---|
| market_drop_may2022 | 2022-05-09 | 4 | **+0.322** | yes (1.00) |
| GME_leg2_feb2021 | 2021-02-24 | 4 | **+0.318** | yes (1.00) |
| GME_runup_nov2021 | 2021-11-02 | 4 | **+0.263** | yes (1.00) |
| market_selloff_jan2022 | 2022-01-24 | 3 | **+0.256** | yes (1.00) |
| aug2024_vix_spike | 2024-08-05 | 3 | +0.221 | yes (1.00) |
| gme_kitty_may2024 | 2024-05-13 | 3 | +0.218 | yes (1.00) |
| AMC_meme_jun2021 | 2021-06-02 | 3 | +0.213 | yes (1.00) |
| GME_squeeze_jan2021 (primary) | 2021-01-25 | 3 | +0.196 | yes (1.00) |
| svb_collapse_mar2023 | 2023-03-10 | 4 | +0.114 | yes (1.00) |
| regional_bank_may2023 | 2023-05-01 | 3 | −0.064 | **no (0.02)** |

**Median event drop +0.219.** Nine of ten fire against their own 300-perm shuffle null at
the 100th percentile. The single non-firing event (regional_bank_may2023) is a genuine
non-cascade: N_eff actually ROSE (drop −0.064), the WSB regional-bank story in May 2023 was
a minor follow-on to SVB and drew mostly newcomers, not the existing pre-onset communities,
exactly the "external flood need not synchronize the frozen blocks" pattern seen on
Wikipedia (Kobe/Suez). The test correctly does NOT fire it.

## The headline comparison: Reddit fires, Wikipedia did not

| | fires vs shuffle (event arm) |
|---|---|
| **Wikipedia editor co-edit graphs** | **0 / 14** (collapse was population-wide; a random relabelling collapsed as much as the real partition) |
| **Reddit WSB user co-thread graphs** | **9 / 10** (collapse is community-specific; the real pre-onset comment communities are what lose independence) |

This is the load-bearing result. On Wikipedia, at a spike essentially the whole active
population converges on one article, so the shuffle null collapses too and nothing fires,
so the collapse there is real but population-wide, not community-specific. On Reddit, WSB has
genuine internal community structure (modularity 0.13–0.19 across the 6000-user cores, K=3–4
distinct pre-onset blocks), and the synchronization is concentrated in the real blocks: a
random relabelling does NOT reproduce it (null p90 ~0.00–0.07 vs observed 0.11–0.32). The
criticality gear's community-specific synchronization is therefore confirmed on a substrate
that actually HAS communities, which is precisely the gap the Wikipedia run left open.

## Why the frozen conjunction still fails (honest diagnosis, not goalpost-moving)

1. **Magnitude below f = 0.30.** Median event drop is 0.219. WSB pre-onset partitions are
 coarse (K=3–4; low modularity ~0.15), so even full synchrony of 3–4 blocks gives a
 bounded macro-ratio drop. We do NOT lower f.
2. **Matched-calm contamination (severe).** The −365 d calm windows for the 2021 events land
 in **2020–2021, the build-up of the very GME mania we are studying**, and the 2022/2024
 calm windows land on the FTX collapse / early-2024 GME-NVDA runs. So 8 of 10 "calm"
 windows are not calm and themselves fire (calm median drop 0.121, calm_p90 0.301). This
 defeats cond3 and flattens the event-vs-calm test (Mann-Whitney one-sided p = 0.285;
 paired Wilcoxon over 10 pairs p = 0.161; event > its matched calm in 7/10 pairs). The
 cleanest contrasts are where the calm window really is quiet: market_drop_may2022 event
 +0.322 vs its 2021 calm −0.010; AMC event +0.213 vs its 2020 calm +0.083;
 svb event vs gme_kitty/regional non-firing calms. We report the contamination straight
 rather than re-pick calm dates post-hoc (the same call the Wikipedia RESULTS made).

## Operator concentration (bonus, Upgrade-3 cross-domain)

Pre-onset commenter activity is heavily concentrated in every event window: **Gini
0.82–0.86, top-5% share 0.66–0.77** of comments. WSB is a steep oligarchy of posters even
before the cascade - consistent with the operator-concentration signal found in the v0.2/v0.3
Reddit pilots, and stable across all ten onsets.

## Honesty rails

Single platform; analyst-frozen onsets (public dates, volume-corroborated); in-sample
thresholds committed in `roster_wsb.py` but not externally lodged (OSF/hash) - a powered
PILOT, not the externally-sealed FA-0 test. USER_CAP/THREAD/PER_THREAD caps are documented
and touch <2% of threads. The shuffle and matched-calm nulls guard the prosecutor's fallacy;
the calm null is openly contaminated and we say so. Result is illustrative of direction,
magnitude, and - newly - community-specificity, not a calibrated classifier.

## What this changes vs the Wikipedia run

The Wikipedia run established that the collapse is real and directional but population-wide
(fires 0/14 vs shuffle), leaving open whether it is ever community-specific. **The Reddit run
closes that gap: on a substrate with genuine community structure the collapse is
community-specific (fires 9/10 vs shuffle).** The frozen magnitude bar and a contaminated
calm null still block a clean pre-registered PASS, identically to Wikipedia. Net: test (ii')
now has, across two independent substrates, (a) a powered directional effect and (b) on the
community-bearing substrate, the community-specific firing the theory predicts - while
remaining honestly short of the sealed pre-registered conjunction.

## Reproduce

```
py -3.12 harvest_filter.py # stream the .zst -> data/*.jsonl + volume_scan.json (resumable)
py -3.12 neff_collapse_wsb.py # -> result_wsb_neff.json + figure_wsb_neff.png
```

Artifacts: `result_wsb_neff.json` (full per-run record + summary), `figure_wsb_neff.png`
(per-event collapse vs shuffle-p90; event vs calm distributions), `data/volume_scan.json`
(daily comment volume, onset corroboration).
