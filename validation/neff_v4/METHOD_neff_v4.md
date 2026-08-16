# Method: test (ii') v4 -- community-SPECIFICITY of the dynamic N_eff collapse

This file plus `roster_v4.py` (the roster and all params) constitute the v4 design. The
analysis script `analyze_v4.py` evaluates the rule below.

## 0. What this tests

The theory's claim about the criticality gear is precise: **before an endogenous
cascade, the EXISTING community loses its internal independence** -- the pre-onset
near-decomposable block structure synchronizes, so the effective number of
independent macro-modes N_eff collapses *within the community partition*. The
sharp form of "within the community partition" is **specificity**: the
real blind-Louvain partition must collapse harder than a random relabeling (block-
label shuffle) of the very same nodes. If the collapse were a generic crowd effect,
the shuffle would collapse just as much and specificity would fail.

The v3 run (`validation/neff_v3`) bundled specificity with a second endpoint,
a MAGNITUDE threshold f on the raw collapse. v3's own clean-null discovery
showed the magnitude endpoint does not discriminate: genuinely-quiet WSB windows
already drop macro-N_eff a median 0.098 with a tail to 0.43, because short high-volume
onset windows compress N_eff generically. Magnitude therefore cannot separate an
endogenous cascade from a busy-but-quiet window on this substrate. The specificity
endpoint, by contrast, fired 9/10 in v3 (the observed collapse sat at the 100th
percentile of its own 300-shuffle null in 8 of 10 events).

v4 makes **specificity the standalone PRIMARY endpoint** and tests it on a
**fresh roster disjoint from every prior run**. It is a DIFFERENT, independently-
motivated endpoint on NEW data. v3's magnitude result stands unchanged; v4 asks
the question v3's null showed was the right one.

## 1. Substrate and unit (same as v3)

r/wallstreetbets comment co-thread graphs from `wallstreetbets_comments.zst`
(subreddits24 full-history dump). Unit = one cascade onset. The substrate is chosen
a priori because its precondition holds: commenters in a WSB cascade ARE the existing
community (no newcomer-flood that lands outside the blocks, the failure mode
that made Wikipedia population-wide in the n=14 pilot). Per-event pipeline is byte-
for-byte the v3 pipeline (`reddit_wsb/neff_collapse_wsb.analyze_run`):
pre-onset [onset-90d, onset) co-thread graph -> blind Louvain partition (K blocks,
no outcome knowledge) -> canonical macro variance-ratio N_eff baseline-vs-onset drop
-> 300x block-label-shuffle null -> "fires" iff observed drop > 90th pctile of that
shuffle null.

## 2. Roster (in roster_v4.py)

12 fresh events, each an externally-dated public market event, DISJOINT from the
original-10 and the v3-10 (every onset >= 14 days from any used onset, and internal
onsets >= 14 days apart; asserted as a calendar fact in roster_v4.py, blind to any
collapse number). Listed there with per-row date sources.

## 3. PRIMARY endpoint and decision rule

Let n = number of roster events that yield a usable partition with K >= 3 blocks, and
k = number of those that FIRE (observed macro-N_eff drop > 90th pctile of the 300x
block-label shuffle null). Under the reference model ("the partition carries no
community-specific structure"), the real partition is treated as exchangeable with its
shuffles, so each event fires with probability p0 = 0.10 (it exceeds its own
90th-percentile shuffle by chance one time in ten).

**PASS iff all three hold:**
- (a) **fire fraction** k/n >= 0.60;
- (b) **binomial tail** P(X >= k | n trials, p0 = 0.10) < 0.01 (one-sided);
- (c) **powered** n >= 8.

Any other outcome is a FAIL, reported straight. The bar is deliberately stricter
than a 0.05 threshold (for n=12, even k=4 would clear 0.05); (a)+(b)
demand a supermajority and a 1% tail so a pass is not a marginal artifact.

## 4. SECONDARY / non-gating (reported, never decides the verdict)

- **Magnitude.** Median per-event macro-N_eff drop and the per-event drops are
  reported for continuity with v3, explicitly flagged NON-GATING with v3's clean-null
  diagnosis attached (quiet WSB windows drop a median ~0.10, so magnitude is not a
  valid discriminator here).
- **Concentration (free Upgrade-3 check).** Pre-onset commenter Gini / HHI / top-5%
  share, for cross-substrate consistency with the operator-concentration invariant.
- **Pearson-Kish N_eff** retained as a legacy secondary metric; the canonical macro
  variance-ratio is primary, as everywhere else in this program.

## 5. Scope

Analyst-set onsets (public event dates). Tractability caps logged
(USER_CAP 6000, THREAD_SUBSAMPLE 40000, PER_THREAD_CAP 120). The shuffle null guards
against the prosecutor's fallacy. This is a structural signal measured on a fresh
roster, not a calibrated classifier.

## 6. Reproduce

```
py -3.12 validation/neff_v4/harvest_v4.py     # stream the dump once (sequential, HDD-safe)
py -3.12 validation/neff_v4/analyze_v4.py     # evaluate the rule
```
