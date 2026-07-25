# Pre-registration: test (ii') v5 -- onset-locking of the dynamic N_eff collapse

**Status of this document: PLANNING / COMMITMENT ARTIFACT.** It contains no results.
It is written *before* any v5 harvest, any onset-shift null, and any re-scoring of an
existing event, and it fixes every threshold in advance. Frozen here and in
`roster_v5.py` (to be committed with it, unmodified thereafter).

**Why v5 exists.** v4 reported a SEALED PASS at binomial `p = 1.7e-7` against an
assumed null fire rate `p0 = 0.10`. Round-2 findings P-01 and P-02, and the measurement
in `../neff_v4/NULL_RECALIBRATION.md`, established two things: the assumed rate is
unsupported (four estimates of the real false-fire rate land at 0.49, 0.60, 0.80 and
0.83, against a break point for the decision rule at 0.378), and the block-label shuffle
the endpoint is scored against is degenerate on this substrate, reducing the test to a
sign check on `drop_macro > 0`. The v4 pass is retracted. v5 does not retry the same
test with a different constant. It states the hypothesis the program actually wants and
builds the null that hypothesis implies.

**This is run 7 in the neff family and the family is disclosed, not reset.** Runs 1-6
are tabulated in `../NEFF_COLLAPSE_SYNTHESIS.md` under "Forking paths". v5 changes the
null and keeps every decision bar from v4 byte for byte, in both directions: no bar is
loosened to make a pass reachable and no bar is tightened to make the retraction look
inevitable.

---

## 0. The seal

Binding, and it is the thing v4 did not have (finding P-05). Before any v5 code is run:

1. This file and `roster_v5.py` are committed, and the commit hash is recorded in
   `../PREREGISTRATION_SEAL.md` with a SHA-256 digest of each, per §0.1 of
   `../PRE_REGISTRATION.md`.
2. The harvest, the calibration arm and the primary arm are run in the order given in
   §6, in **separate commits**, so `git log --follow` carries an ordering between
   threshold and result. v4's six files share one commit and therefore prove nothing
   about their order.
3. If step 1 is skipped, v5 is reported as **UNSEALED** whatever it returns, and may
   not be described as pre-registered.

---

## 1. Hypothesis

**H1.** The N_eff collapse inside the existing community's frozen block partition is
**time-locked to cascade onset**.

**H0.** It is not. The collapse statistic at a cascade onset is what the same community,
in the same period, would have produced at a pseudo-onset placed anywhere else in quiet
time.

H0 is stated this way deliberately. v4's H0 was "the partition carries no
community-specific structure", which this repository asserts elsewhere is false of
r/wallstreetbets at all times (`reddit_wsb/RESULTS.md:118-130`). Rejecting a claim we
already believe to be false is not evidence for the theory. Onset-locking is the claim
near-decomposability actually makes, and it is the claim a forecaster would need.

---

## 2. Substrate, statistic and windows (all frozen, all unchanged from v3/v4)

r/wallstreetbets comments from `wallstreetbets_comments.zst` (subreddits24 full-history
dump). Per-event statistic is `reddit_wsb/neff_collapse_wsb.analyze_run`, unmodified:
pre-onset 90-day co-thread graph, blind Louvain partition (K blocks, no outcome
knowledge), canonical macro variance-ratio N_eff, baseline window
`[onset-56d, onset-7d)` against onset window `[onset-3d, onset+22d)`, 3-day buckets,
`drop = 1 - N_eff(onset)/N_eff(baseline)`. Caps unchanged: `USER_CAP` 6000,
`THREAD_SUBSAMPLE` 40000, `PER_THREAD_CAP` 120.

**Nothing about the statistic changes. Only the null changes.** That is the whole point
of v5, and it is what makes the comparison against v4 interpretable.

---

## 3. The null (N2, onset-shift), frozen

For each event, hold **fixed**: the co-thread graph, the Louvain partition, the per-user
bucket matrices, and every parameter above. Vary **only** the onset date.

A pseudo-onset `o'` is **admissible** iff all of:

- `[o'-90d, o'+22d)` lies inside the harvested span for that event;
- `|o' - onset| >= 45d`;
- `[o'-3d, o'+22d)` does not overlap the real onset window `[onset-3d, onset+22d)`;
- `o'` is at least 21 days from every date in `neff_v3/clean_windows.EXCLUDED_DATES`
  (the frozen macro-event list plus every onset used by runs 1-6). The null must be a
  *quiet* onset-shift null, or it contains the very cascades the test is about;
- `o'` steps in 3-day increments from the start of the admissible span (deterministic,
  no sampling, no seed).

`fires_vs_onset_shift` iff the observed drop exceeds the **90th percentile** of that
event's admissible onset-shift drops. Bar unchanged from v4.

**`p0 = 0.10` is retained, and under this null it is justified by construction.** The
observed statistic and each null draw differ only in the onset date, so under H0 they
are exchangeable and the observation exceeds its own p90 one time in ten. This was
always the right reasoning; v4 applied it to a null for which it does not hold.

**Minimum null size.** An event with fewer than 40 admissible pseudo-onsets is
**UNPOWERED** and excluded from n. Frozen here so it cannot be decided later.

**Scale gate (from P-02's repair, frozen).** An event whose onset-shift null has a p90
below 0.02 is **UNPOWERED** and excluded from n, because at that scale the null cannot
discriminate the drops being scored. Under N2 we expect this never to trigger; it is
frozen anyway so that a degenerate null can never again be read as a pass.

---

## 4. Roster

**Arm P (PRIMARY, confirmatory).** All **32** WSB onsets already committed across runs
1-6: the original 10 (`reddit_wsb/roster_wsb.py`), the v3 10 (`neff_v3/roster_v3.py`)
and the v4 12 (`neff_v4/roster_v4.py`), verbatim, with no additions, no removals and no
reweighting. Re-using them is legitimate here and it is worth stating why: the onset-shift
null has never been computed for any of these events, so the primary test statistic
(the observed drop's percentile within its own onset-shift null) is **unobserved for all
32**. The drops are known; the statistic is not. Re-using the roster also removes every
degree of freedom in roster construction, which is where v4's disjointness argument spent
its credibility (finding P-04: 11 of 12 v4 windows overlap a prior run's window anyway).

Events are **not** pooled blindly: n, k and the verdict are reported for Arm P as a
whole **and** broken out by source run, and if the three runs disagree in direction that
disagreement is the headline.

**Arm C (CALIBRATION, runs first, see §6).** At least **30** genuinely-quiet pseudo-onsets
from an extension of `neff_v3/clean_windows.py`: minimum separation relaxed from 45 days
to 21, and the lowest-volume-first greedy selection replaced by *all* admissible windows
in the volume record, taking the 30 with the lowest onset-window mean volume within era.
Selection is a pure function of the daily volume record and the frozen exclusion list,
blind to any collapse number. This is the measurement finding P-01 asked for.

---

## 5. Decision rule (frozen, evaluated exactly once)

Let `n` = Arm P events yielding K >= 3 blocks and passing both UNPOWERED gates of §3,
and `k` = those that fire vs their own onset-shift null.

**PASS iff all three hold:**
- **(a)** fire fraction `k/n >= 0.60`;
- **(b)** binomial `P(X >= k | n, p0 = 0.10) < 0.01`, one-sided;
- **(c)** `n >= 8`.

Identical to `PRE_REGISTRATION_neff_v4.md:63-66`. Any other outcome is a FAIL, reported
straight, in this file's companion `RESULTS.md`, with the failing condition named.

**Calibration gate, frozen, and it can void the run.** Arm C is scored under the identical
rule. If Arm C's realised fire rate falls outside **[0.02, 0.25]**, the null is declared
miscalibrated and **no verdict is issued for Arm P**, pass or fail. A test whose measured
false-positive rate is not near its nominal 0.10 has not earned the right to report either
outcome. v4 had no such gate, and its null's false-fire rate was later measured at roughly
0.5 to 0.8.

**Multiplicity, disclosed not adjusted.** v5 is the 7th run in the family. The primary
alpha stays at 0.01, unchanged from v4. Alongside it we report the family-wise figure
`0.01/7 = 0.00143` and state whether the result clears it. We do not move the primary bar
after the fact in either direction.

---

## 6. Order of operations (binding)

1. **Widen the harvest.** `harvest_v5.py`, adapted from `harvest_v4.py` with the same
   single sequential pass over the dump, covering `[onset-400d, onset+200d)` per event.
   The wider span is what makes ~130 admissible pseudo-onsets per event possible; the
   existing 112-day windows leave no room to shift an onset 45 days. One stream, all
   events, as before.
2. **Fix P-03 first.** Add `fires_vs_shuffle`, `shuffle_pctile_of_obs` and
   `shuffle_null_p90` to the row dict `derive_f_v3.py:57-64` drops, and re-run it. This
   costs one existing script and converts `NULL_RECALIBRATION.md` §3.4 from imputed to
   measured. Commit separately.
3. **Run Arm C.** Report the measured false-fire rate with a Clopper-Pearson interval,
   under both N1 (block-label shuffle, for the record) and N2. Commit separately. This
   arm touches no event data, so it cannot leak into Arm P.
4. **Evaluate the calibration gate.** If it fails, stop and report that. Do not proceed.
5. **Run Arm P once.** Commit separately.
6. **Report.** `RESULTS.md` in this directory, in the house format, whatever it says.

---

## 7. Secondary and non-gating (reported, never decides the verdict)

- **N3, matched quiet-window contrast.** Arm P drops against Arm C drops, one-sided
  Mann-Whitney with Cliff's delta and a 200,000-draw permutation test on the mean
  difference. Reported for every arm. This is the between-event approximation of N2 and
  it confounds onset timing with window identity, which is why it is not primary.
- **N4, degree-preserving configuration model.** Rewire each co-thread graph preserving
  the degree sequence, re-run Louvain, and report the modularity of the real partition
  against that null. This is a diagnostic on whether the WSB partitions are real. It is
  **not** a test of (ii') and must never be reported as one.
- **N1, block-label shuffle.** Still computed, for continuity with runs 1-6 and so the
  v4 retraction stays auditable. Explicitly non-gating and labelled degenerate.
- **Magnitude.** Median and per-event drops, non-gating, with v3's clean-null diagnosis
  attached, unchanged from v4.
- **Concentration.** Pre-onset Gini / HHI / top-5% share, the free Upgrade-3 check.

---

## 8. What would refute the program's claim here

Stated in advance so it cannot be renegotiated. If Arm C calibrates inside the gate and
Arm P returns `k/n` at or below 0.25 across 32 events, then the collapse is **not**
time-locked to cascade onset on this substrate, and test (ii') is a **refutation**, not
an open question. `NULL_RECALIBRATION.md` §5.2 already shows the best available proxy
returning 0 of 12 against a between-event quiet null, so this is the outcome we consider
most likely, and it is the reason this document exists rather than a retry.

If Arm P returns a pass under a calibrated null, that is a stronger result than v4 ever
claimed, because it would be onset-locking rather than the existence of community
structure. Both directions are live and both will be reported.

## 9. Honesty rails (carried)

Analyst-frozen onsets (public event dates, all committed in runs 1-6). Threshold
committed here and, unlike v4, to be folded into the `PREREGISTRATION_SEAL.md` hash seal
before any v5 code runs (§0). Tractability caps logged and unchanged. Single platform;
the 32 events are three overlapping looks at one substrate, not 32 independent
observations, and 11 of the v4 12 share calendar days with a prior run's window (P-04),
so the effective independent n is materially below 32 and the reported n will carry that
caveat. Read the outcome as a test of onset-locking on r/wallstreetbets, not as a
calibrated classifier.

## 10. Reproduce (once the scripts exist)

```
py -3.12 validation/neff_v5/harvest_v5.py      # one sequential pass, widened spans
py -3.12 validation/neff_v3/derive_f_v3.py     # P-03 fix, three extra serialised keys
py -3.12 validation/neff_v5/calibrate_v5.py    # Arm C, >=30 quiet windows
py -3.12 validation/neff_v5/analyze_v5.py      # Arm P, evaluates the frozen rule ONCE
```
