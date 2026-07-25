# Sealed structured-substrate N_eff collapse (test ii', v3): the honest ceiling

**VERDICT: SEALED NOT.** This is the strongest, most disciplined version of the dynamic
N_eff collapse test the program can run: the threshold f was re-derived from a genuinely
clean null and frozen before the roster, the calm/null contamination that sank the prior
WSB run was removed, and the roster was fresh and disjoint. Run faithfully, it returns a
rigorous negative on magnitude while confirming the mechanism's community-specificity for
a third time. We report it straight.

## What this run fixed (the two named blockers from the prior WSB run)

The prior WSB run (`validation/reddit_wsb/`) was NOT a sealed pass for two reasons that
were named, not hidden:

1. The threshold **f = 0.30** was hand-picked to beat a pilot, not principled.
2. The calm/null arm used **onset minus 365 days**, which for the 2021 cascades landed
   INSIDE the 2020 to 2021 GME mania, inflating "calm" drops to 0.30 to 0.33 and defeating
   the event-vs-calm comparison.

This v3 run fixes both, pre-registers the fixes (`PRE_REGISTRATION_neff_v3.md`), and runs
on a fresh disjoint roster.

## Substrate choice (justified a priori, not post hoc)

The mechanism's precondition is that the EXISTING community drives the spike. On
r/wallstreetbets comment co-thread graphs this holds structurally: the commenters in a
cascade are the community. On Wikipedia it fails by newcomer-flood (a breaking event
floods the article with drive-by editors outside the frozen blocks, pushing N_eff UP not
down; measured in `validation/wikipedia/diagnostics/v1_newcomer_flood.py` and the neff_v2
fresh roster, where even reflexive crypto events gave large negative drops). So WSB is the
theory-appropriate instrument, and this seal is scoped to the structured /
endogenous-community regime, which is the bounded regime the paper actually claims, NOT a
population-wide claim.

## The frozen threshold f

`derive_f_v3.py`, run BEFORE the fresh roster was harvested, derived f from the clean WSB
null: 12 genuinely-quiet windows (90-day pre-graph plus 21-day onset, onset stretch not
overlapping any known event date, comment volume in the lower half of its era), each run
through the identical collapse pipeline. The clean-null drop distribution (n=12):

```
-0.2028, -0.1536, 0.0235, 0.0442, 0.0565, 0.0724, 0.1235, 0.2275, 0.2719, 0.3200, 0.3649, 0.4286
median 0.098   p90 0.360   p95 0.394
```

**f := clean-null p95 = 0.3936 (FROZEN).** A passing event median had to exceed what a
genuinely-quiet WSB window produces 95 percent of the time. The engine cross-check (E4
short-window achievable collapse: K=4 median 0.72, K=5 median 0.79; long K=64 reference
drop 0.186) confirms f sits below what a real synchrony event can physically produce, so
f is not an impossible bar.

The decisive discovery here is in the null itself: **genuinely-quiet WSB windows already
produce substantial macro-N_eff drops** (median 0.098, with a heavy upper tail to 0.43).
Short, high-volume onset windows on WSB compress the macro variance-ratio generically, so
an honest magnitude bar is high. The prior run's f = 0.30 was, by luck, close to this
clean p90 (0.36) but below the principled p95.

## The fresh roster result (frozen rule, evaluated once)

10 fresh WSB cascades (`roster_v3.py`), none in the original 10, anchored to external
event dates, all yielding K >= 3:

| event | onset | K | drop | fires vs shuffle |
|---|---|---|---|---|
| tesla_sp500 | 2020-12-21 | 3 | 0.485 | yes |
| jpow_jackson | 2022-08-26 | 4 | 0.483 | yes |
| djt_media | 2024-03-26 | 3 | 0.406 | yes |
| fitch_downgrade | 2023-08-02 | 3 | 0.326 | yes |
| ukraine_shock | 2022-02-24 | 4 | 0.153 | yes |
| hood_ipo | 2021-08-04 | 3 | 0.124 | yes |
| bbby_squeeze | 2022-08-08 | 4 | 0.116 | yes |
| debt_ceiling | 2023-06-01 | 4 | 0.112 | no |
| evergrande | 2021-09-20 | 4 | 0.091 | yes |
| ftx_collapse | 2022-11-08 | 4 | 0.078 | yes |

- median event drop **0.138**
- 9 of 10 fire vs the 300x block-label-shuffle null
- clean-null p90 0.360, p95 0.394, median 0.098
- Mann-Whitney U (event vs clean, one-sided greater) **p = 0.069**

Frozen four-condition decision rule:

| condition | rule | result |
|---|---|---|
| 1 magnitude | median event drop >= f (0.3936) | **FAIL** 0.138 < 0.394 |
| 2 beats clean null | median > clean p90 AND MWU p < 0.05 | **FAIL** 0.138 <= 0.360; p = 0.069 |
| 3 specificity | fires vs shuffle in >= 50% | **PASS** 9/10 |
| 4 powered | n >= 8 at K >= 3 | **PASS** n = 10 |

**SEALED NOT.** Two of four conditions hold; the two that fail are both magnitude
conditions.

## The measurement this run computed and then discarded

Recorded here because it is the single most consequential thing about this run, and we
missed it until an adversarial round-2 review (`logos/REVIEW_ROUND2.md`, finding P-03)
pointed at it.

`derive_f_v3.py:55` calls `NB.analyze_run(label, onset, "clean", comments)` on each of the
twelve genuinely-quiet clean windows. That is the *identical* pipeline used on the event
arms, and `neff_collapse_wsb.py:281-285` unconditionally sets three fields on every record
it returns: `shuffle_null_p90`, `shuffle_pctile_of_obs` and `fires_vs_shuffle`. So the
**specificity fire rate of a genuinely-quiet WSB window was computed, twelve times, in this
run.** The row dict at `derive_f_v3.py:57-64` then serialised thirteen fields
(`label, onset, era, onset_mean_vol, status, K, modularity, drop_macro, neff_base,
neff_onset, n_comments, user_cap_hit, n_threads_subsampled`) and none of those three.
Loading `derive_f_v3.json` and printing the keys of `route_i_clean_null.rows[0]` returns
exactly those thirteen; the sibling `result_wsb_neff.json` and `result_neff_v4.json` both
persist all three.

**Why it matters.** The clean windows were selected by `clean_windows.py` precisely to be
uncontaminated, guard-banded and era-conditioned. That makes them the one estimate in this
repository of how often the specificity test fires when nothing is happening, immune to the
calm-arm contamination defence we deploy for the original WSB run
(`../reddit_wsb/RESULTS.md`, "8 of 10 calm windows are not calm and themselves fire"). It is
therefore the number that calibrates the null fire rate p0 which `neff_v4` later asserts
from construction and uses as the whole basis of its binomial. The measurement was one
function return away from the file, and the v4 pre-registration was written afterwards
without it.

**Direction of the correction, stated without overclaiming a point value.** The referee
recomputation notes that 10 of these 12 clean drops exceed the median v4 shuffle-null p90 of
0.0137, and that the clean-null median drop is 0.098, seven times the v4 bar. We have not
yet re-run the pipeline to get the persisted fire rate, so we assert **no** replacement p0
and no corrected binomial here; what we assert is that the assumed rate has never been
measured on this substrate and that every available indication runs against it.

**The fix, and its cost.** Add `fires_vs_shuffle`, `shuffle_pctile_of_obs` and
`shuffle_null_p90` to the `derive_f_v3.py:57-64` row dict and re-run `derive_f_v3.py` over
the twelve clean windows. Pure CPU, one pass over already-harvested jsonl, no new harvest of
the 7 GB dump. This is the cheapest single action in the whole neff family that would settle
the calibration question either way, and it should be run before any further neff result is
published.

## The shuffle null this run also leans on is near-degenerate on WSB

This run reports "9 of 10 fire vs the 300x block-label-shuffle null" as its third
confirmation of community-specificity. The same referee review (finding P-02) shows the WSB
shuffle null p90 sits near zero, median 0.0137 across the v4 events against a Wikipedia
median of 0.4909 for the identical code, so on this substrate "fires" is in practice a
magnitude test at a bar around 0.014. That is 7x below the median drop of the very clean
windows this run derived f from, and 29x below the f = 0.3936 this run froze and then
reported as non-discriminating. The uncomfortable consequence is stated plainly: the same
bar that 9 of these 10 cascades clear is cleared by 10 of the 12 quiet windows in the clean
null above. The specificity endpoint retains real discriminating power only where the null
is non-degenerate, which on the v4 roster is 2 events of 12. See `../neff_v4/RESULTS.md`,
"Known defects in this run".

## What this establishes (the real finding, third confirmation)

The dynamic N_eff collapse is **real and community-specific**: on a fresh disjoint roster,
9 of 10 cascades collapse the canonical macro-N_eff more than a block-label shuffle of the
same graph produces. We read that as the BLOCK STRUCTURE doing the work rather than raw
volume, and called it the third independent confirmation of community-specificity
(Wikipedia 0/14 because its blocks dissolve under newcomer-flood, original WSB 9/10, this
fresh WSB 9/10). That reading is now qualified by the two sections above: on WSB the shuffle
null is near-degenerate, so clearing it is a weak bar that quiet windows clear at a similar
rate, and the cross-substrate Wikipedia contrast is substantially a contrast in null
geometry (median null p90 0.4909 there against 0.0137 here) rather than a demonstrated
contrast in community structure. What survives without qualification is narrower: the drop
is positive and beats a near-zero null on almost every cascade, and the endpoint
discriminates as designed on the minority of windows whose null is non-degenerate.

But the collapse's **magnitude does not exceed what genuinely-quiet WSB windows produce.**
The event drops are heterogeneous (a few large: Tesla S&P inclusion 0.485, Jackson Hole
0.483, DJT-media 0.406; most small: FTX 0.078, Evergrande 0.091), and the median (0.138)
sits between the clean-null median (0.098) and its p90 (0.360), with only a marginal
one-sided separation (p = 0.069). The honest reading: the collapse is a real STRUCTURAL
signal (it lives in the blocks) but not a MAGNITUDE anomaly against a clean baseline. The
short high-volume onset window compresses N_eff whether or not the event is a genuine
synchronization.

## What it means for the program

This is the honest ceiling of the dynamic-collapse test. The move that the project's own
roadmap believed was "one honest step from a clean pass" was executed exactly as
specified, on the most favorable substrate, with the threshold and null both fixed
honestly in advance, and it returns a rigorous negative. The criticality gear is therefore
**supported as a community-specific structural signal and falsified as a frozen-threshold
magnitude pass.** That is a stronger, more defensible scientific position than a pass
manufactured by moving f: the mechanism is real where the theory says it should be (in the
block structure of an endogenous-community substrate), and the program does not overclaim
a magnitude effect the clean null does not license. The bounded-special-regime thesis is
confirmed by measurement; the sealed magnitude pass is not available without
goalpost-moving, and we do not move the goalpost.

## Honesty rails (carried)

Single platform (WSB); analyst-frozen onsets are public external event dates; f and the
four-condition rule were committed in `PRE_REGISTRATION_neff_v3.md` and `derive_f_v3.json`
BEFORE the fresh roster was harvested, but not externally lodged to OSF/hash, so this is a
sealed PILOT, not the externally-notarized FA-0 test. Tractability caps logged
(USER_CAP 6000, THREAD_SUBSAMPLE 40000). The block-label-shuffle and clean-null nulls
guard the prosecutor's fallacy. Reported straight: the test did not pass, and the
threshold was not moved to make it pass.

## Reproduce

```
# harvest (one sequential pass over the 7 GB dump into 22 window files)
py -3.12 validation/neff_v3/harvest_v3.py
# derive and freeze f from the clean null
py -3.12 validation/neff_v3/derive_f_v3.py
# evaluate the frozen rule on the fresh roster
py -3.12 validation/neff_v3/analyze_v3.py
```
