# Wikipedia dynamic-N_eff-collapse test (test ii') — RESULTS

**Powered cross-domain PILOT.** This run answers the standing objection that the dynamic
N_eff collapse (the load-bearing criticality gear) was "only suggestive, n=1" on GitHub.
It does not rely on any throttled API or torrent: English Wikipedia editor activity via
the public Wikimedia API. Thresholds were frozen in `PRE_REGISTRATION_wiki.md` BEFORE any
data was harvested.

## Headline

The dynamic N_eff collapse is **real and statistically robust across a powered, n=14
cross-domain roster, but it does NOT clear the frozen pre-registered falsification bar.**
Both halves of that sentence are load-bearing; we report them together.

- **Directional prediction — SUPPORTED (p < 0.01).** Real attention-spike onsets collapse
  the effective number of independent editor blocks; matched calm windows on the same
  articles do not. Event median N_eff drop **+0.19** vs calm median **−0.25** (N_eff
  actually *rises* in quiet windows). Event-vs-calm Mann-Whitney one-sided
  **p = 0.0054**; paired Wilcoxon over 9 articles present in both arms **p = 0.0098**.
- **Frozen pre-registered rule — NOT SUPPORTED.** The committed conjunction fails:
  median event drop 0.19 is below **f = 0.30**; **0 of 14** event articles fire against
  their own block-label-shuffle null; the event median does not exceed the matched-calm
  90th percentile (which is inflated by calm-window contamination, below). Powered bar
  met (n = 14 >= 8).

So test ii' moves from *"suggestive, n=1 anecdote"* to *"a powered, p<0.01 directional
effect that is below the pre-registered magnitude threshold and is population-wide rather
than community-specific."* The objection is largely removed; the criticality gear demonstrably
turns. It is not yet a clean pre-registered PASS, and we do not claim one.

## Method (frozen; see PRE_REGISTRATION_wiki.md)

- Roster: 20 articles that ALREADY EXISTED and were actively edited before a clean
  external attention-spike onset (articles created at the event are excluded — the GitHub
  "born into cascade" failure mode). Event arm + matched-calm arm (onset − 365 d).
- Blocks (blind): editors active on the focal article in `[onset−90d, onset)` define the
  editor set (cap 150, logged); their main-namespace co-editing graph — **focal article
  excluded** so blocks come from genuinely distinct interests, not the trivial everyone-
  edits-the-focal clique — is partitioned by blind Louvain. Partition frozen pre-onset.
- N_eff trajectory: frozen blocks' edit activity ON the focal article, bucketed (3 d),
  baseline window vs onset window. **Primary metric = canonical macro variance-ratio**
  (engine `block_metrics`: `mean_k Var_t(z_k)/Var_t(mean_k z_k)`, collapses K→1 under
  synchrony). Secondary = legacy Pearson-Kish, reported for comparison.
- Nulls: block-label shuffle (300 perms) + matched-calm arm.

## Per-article event collapse (canonical metric, K>=3)

| article | onset | K | N_eff drop |
|---|---|---|---|
| Evergrande Group | 2021-09-20 | 4 | **+0.61** |
| Diego Maradona | 2020-11-25 | 4 | **+0.57** |
| Volodymyr Zelenskyy | 2022-02-24 | 4 | **+0.44** |
| Queen Elizabeth II | 2022-09-08 | 3 | **+0.41** |
| Donald Trump | 2021-01-06 | 3 | **+0.35** |
| Boeing 737 MAX | 2019-03-10 | 3 | +0.29 |
| Bitcoin | 2021-04-14 | 7 | +0.22 |
| Joe Biden | 2020-11-07 | 7 | +0.16 |
| Notre-Dame de Paris | 2019-04-15 | 3 | +0.14 |
| Credit Suisse | 2023-03-19 | 3 | +0.07 |
| Twitter | 2022-10-27 | 3 | +0.03 |
| NATO | 2022-02-24 | 4 | −0.02 |
| Kobe Bryant | 2020-01-26 | 3 | −0.27 |
| Suez Canal | 2021-03-23 | 4 | −0.40 |

Median **+0.19**. The collapse is heterogeneous: insider/financial and slow-building or
death-of-long-tracked-figure events collapse hard (Evergrande, Maradona, Zelenskyy, QE2,
Trump); some sudden exogenous shocks where the onset crowd is mostly NEW editors not in
the frozen pre-onset partition do not (Kobe, Suez). This is consistent with the theory
that it is the EXISTING community's loss of independence that the frozen-partition metric
measures; a pure external flood of newcomers need not synchronize the pre-existing blocks.

## Why the frozen rule fails (honest diagnosis, not goalpost-moving)

1. **Shuffle-null fires 0/14.** At onset essentially the whole active population converges
   on the focal article, so a *randomly* relabelled partition collapses about as much as
   the real one. The collapse is therefore **population-wide, not community-specific.**
   This is theory-consistent (loss of independence of *any* partition = total
   synchronization) but means the shuffle-specificity gate tested a stronger claim than
   test ii' requires. We keep the frozen result and report it as a negative on that gate.
2. **Magnitude below f=0.30.** The median is 0.19; pulled down by the heterogeneous
   exogenous-shock cases above. We do NOT lower f to claim a pass.
3. **Calm-null contamination.** Two "calm" windows (Queen Elizabeth II −1 y, Twitter −1 y)
   were not actually quiet (their own mini-events), inflating `calm_p90` to 0.29 and
   defeating cond3 even though the event-vs-calm Mann-Whitney/Wilcoxon tests are highly
   significant. We report the contamination rather than re-pick the calm dates post-hoc.

## Excluded as trivial (K<3 pre-onset partition; logged, not hidden)

FTX (K=2), GameStop (2), OpenAI (2), Robinhood (2), Silicon Valley Bank (1), Terra (0).
These articles were too sleepy before their spike to form >=3 distinct pre-onset editor
communities — the same low-pre-onset-structure limit that capped the GitHub pilot. Their
exclusion is structural (no measurable blocks), not outcome-based.

## Honesty rails

Single platform; analyst-frozen onsets (public event dates); in-sample thresholds committed
but not externally lodged (OSF/hash) — this is a powered PILOT, not the externally-sealed
FA-0 test. Editor cap 150/article (a handful hit it). Matched-calm and shuffle nulls guard
the prosecutor's fallacy. The result is illustrative of direction and magnitude across a
real roster, not a calibrated classifier.

## What this changes for the paper (decision deferred to the author)

The paper's §obsupgrades / conclusion currently call the dynamic collapse "only suggestive
(n=1)." That sentence is now understated in one direction and must not be overstated in the
other. The accurate replacement, if adopted: *the dynamic collapse is directionally confirmed
on a powered n=14 cross-domain Wikipedia roster (events collapse the effective number of
independent editor blocks, matched-calm windows do not; event-vs-calm p<0.01), but it sits
below the pre-registered magnitude threshold and is population-wide rather than community-
specific, so test (ii') has directional support and is not yet a clean pre-registered pass.*

## Reproduce

```
py -3.12 harvest.py              # Wikimedia API -> data/*.json (resumable)
py -3.12 neff_collapse_wiki.py   # -> result_wiki_neff.json + figure_wiki_neff.png
```

## Second substrate (ready, not yet run)

`validation/reddit_dump/wallstreetbets_comments.zst` (7.1 GB) and `..._submissions.zst`
(521 MB) were fetched from the per-subreddit Pushshift dump (aria2c, no API throttle).
They contain the canonical WSB / GameStop January-2021 cascade with full comment-level
co-thread structure — the exact case the GitHub pilot could only touch at n=1. Running the
same dual-N_eff collapse test on that comment co-thread graph is the obvious next increment.
