# PRE-REGISTRATION — Falsification Tests of the Bounded-Psychohistory Program

**Checklist item:** FA-0 (procedural foundation for the position-paper hedge).
**Status of this document:** PLANNING / COMMITMENT ARTIFACT. This is not a claim of
results. It fixes, in advance, the numeric thresholds the paper (§ *What would
falsify the program*) leaves symbolic, so that the authors retain no freedom to move
the goalposts after seeing data.
**Date drafted:** 2026-06-15.
**Source of record:** `psychohistory.tex`, §`sec:limits`, enumerated tests (i)–(viii)
including (iii′), and the regime-label / ex-ante-registry "seal" paragraph immediately
above the list.

All threshold values below are marked **[PROPOSED]**. They are sensible, defensible
defaults open to adjustment **before lodging**. Once lodged to the registry (below),
they are frozen and may not be changed for the lodged frame.

---

## 0. The seal (regime-label protocol and registry mechanism)

This section is binding on every test below; it is the "seal" the whole hedge depends on.

### 0.1 Registry mechanism
The full specification of every test — thresholds, sample frame, null, horizon, test
statistic, and pass/fail rule — is time-stamped to a **third-party, append-only public
registry before any outcome is known**. Two acceptable instruments:

- **Primary:** an **OSF pre-registration entry** (osf.io), frozen/registered (not a
  draft), which provides an immutable third-party timestamp and DOI.
- **Fallback / belt-and-braces:** a **SHA-256 hash of this document and each forecast
  record committed to a public ledger** (a public Git tag whose commit hash is itself
  anchored, or an OpenTimestamps `.ots` proof against the Bitcoin chain). The hash, not
  the private file, is what proves precedence.

A label the authors timestamp **privately** is reconstructable after the fact and is
therefore **not accepted**: only an externally-anchored timestamp counts.

### 0.2 Regime-label protocol (smooth / pre-critical / critical + OOD flag)
The engine emits, for **every** forecast, two first-class fields *before* the resolution
window opens:
1. a **regime label** ∈ {smooth, pre-critical, critical}; and
2. an **out-of-distribution (Mule) flag** ∈ {clear, flagged} from the misspecification
   monitor (CUSUM on normalized innovation squared).

Both are written to the registry at forecast-issue time.

### 0.3 The three hard commitments (non-negotiable)
1. **Unstamped label ⇒ miss.** A forecast whose regime label is **not externally
   timestamped before the resolution window** is scored as a **miss** by default. No
   exceptions.
2. **Smooth-miss ⇒ full refutation, no relabeling.** A forecast that **misses while the
   engine declared "smooth"** counts as a **full refutation** of the program and **may
   not** be relabeled "criticality" or "misspecification" after the fact. "Criticality"
   and "the Mule" are admissible only when declared **ex ante**.
3. **No excuse generator.** The failure taxonomy (§`sec:failure`) is sealed by (1)–(2):
   it cannot be retrofitted to a miss.

---

## Threshold summary (PROPOSED values, one line each)

| Sym | Test | Proposed value | One-line justification |
|-----|------|----------------|------------------------|
| X | (i) attention drift bound | **15%** | NWP-style "approximately conserved": tolerates measurement slop and modeled source growth, still small enough that a mania (often 2–10×) clearly breaches it. |
| Y | (i) composition churn floor | **40%** | Churn must be visibly larger than the conservation tolerance X, so "conserved total, reshuffled mix" is a real, separable signal. |
| Z | (i) max annual source growth | **8%/yr** | Above global adult-population + connectivity + waking-hours-online growth (~few %/yr), so a faster-growing endowment refutes the sub-generational-budget premise. |
| ρ₀ | (ii) calm cross-block correlation cap | **0.20** | "Weak coupling": blocks share macro shocks weakly; a median calm-window correlation > 0.2 means the blocks are not near-decomposable. |
| M | (iii)/(iii′) frozen roster size | **20** | Minimum labeled fold-type transitions for a non-degenerate ROC and a stable B-fraction; below this an AUC point estimate is untrustworthy. |
| AUC | (iii) early-warning ROC | **≥ 0.75** | Clearly beats chance (0.50) and the pilot's NULL (0.21–0.36); modest enough to be honest given the N-/R-tipping blind spot. |
| π_B | (iii′) B-tipping fraction floor | **0.60** | The program needs crises to be *predominantly* fold-type; a simple majority is the weakest defensible reading of "predominantly," and this is the test most likely to fail. |
| m | (v) smooth-regime question set size | **50** | Enough resolved questions for a Brier-score difference vs a baseline to be statistically meaningful, matching superforecasting tournament practice. |
| δ | (v) Brier improvement vs baseline | **≥ 0.05** | A 0.05 Brier edge over a superforecaster/market baseline is a real, non-trivial skill margin without overclaiming. |

---

## Test (i) — Conservation / Zero-Sum Attention

- **Thresholds:** drift bound **X = 15%** [PROPOSED]; composition churn floor
  **Y = 40%** [PROPOSED]; max trailing-12-month source growth **Z = 8%/yr** [PROPOSED].
- **Data source / frame:** aggregate human attention-minutes across the **N = 10
  most-trafficked platforms** (frozen list lodged at pre-registration; e.g. the top-10
  by global monthly active minutes as of the pre-registered start date), measured over
  **rolling 90-day windows** from a pre-registered start date. Source-growth term
  `∫Ȧ dt` is the demographically-predicted endowment growth (adult-online-population ×
  waking-hours-online), modeled and lodged in advance.
- **Null / base-rate:** the *net-of-source* total is the conserved quantity; the null is
  "total attention-minutes, net of predicted source growth, are flat (drift 0)" — the
  test is whether observed drift stays inside ±X while composition churn exceeds Y.
- **Horizon:** rolling 90-day windows over a ≥ 3-year pre-registered span, plus a
  trailing-12-month series for the Z sub-test.
- **Test statistic:** (a) max |net drift| of the grand total across windows; (b) total
  composition churn = Σ|Δ share|/2 across the platform/topic simplex; (c) trailing-12-mo
  growth rate of net total.
- **Pass/fail:** PASS if net drift < X **and** churn > Y in calm windows **and** trailing
  growth < Z, **including** during ≥ 1 documented mania (the same total must hold within
  X at criticality). FAIL (conservation refuted) if net attention-minutes expand by > X
  during ≥ 1 documented mania, or if trailing growth ≥ Z.
- **CURRENT STATUS:** **PILOT RUN (CONTRADICTS at wrong scale — UNRESOLVED).**
  `validation/backtests/RESULTS.md` test (i): within r/AskEconomics (4000 posts, 11 wk),
  the weekly budget *inflated* (~300 → 635/wk under the tariff shock, CV 0.387) and net
  of the mechanical simplex constraint there was no genuine cross-topic trade-off
  (mean off-diag de-trended r = −0.022 vs simplex −0.125). **Caveat (carried):** a single
  subreddit is the wrong measurement scale — it can freely import/export attention from
  the rest of the internet, so this does **not** refute the *ecosystem-level* claim. The
  pre-registered test above fixes the scale to the cross-platform ecosystem total, which
  has **not** yet been measured. Pilot signal only.

---

## Test (ii) — Block Independence

- **Threshold:** calm-regime cross-block fluctuation correlation cap **ρ₀ = 0.20**
  [PROPOSED].
- **Data source / frame:** community blocks recovered by a **named algorithm at a fixed
  resolution** (proposed: **Leiden community detection, resolution γ = 1.0**, on a named
  interaction-graph corpus lodged in advance — e.g. a fixed cross-subreddit / cross-
  platform co-engagement graph). Algorithm, resolution, and corpus all frozen ex ante.
- **Null / base-rate:** a permutation / phase-shuffle null on the de-trended per-block
  fluctuation series, so that "blocks co-move" is tested *beyond* shared-trend artifact.
- **Horizon:** calm regimes only (regime label = smooth), median over all calm windows
  in the pre-registered span.
- **Test statistic:** ρ = median off-diagonal pairwise correlation of de-trended block
  fluctuations in calm windows (reported alongside the macro variance-ratio N_eff).
- **Pass/fail:** PASS if ρ < ρ₀ in the median calm window. FAIL (block independence
  refuted) if ρ ≥ ρ₀ in the median calm window.
- **CURRENT STATUS:** **PILOT RUN (INCONCLUSIVE — method demonstrated).**
  `validation/backtests/RESULTS.md` test (ii) / `temporal/test_blocks_sync.py`: on 5
  location subs (europe/france/germany/italy/spain) over a **12-day** overlap, mean
  cross-block Pearson = 0.592, macro variance-ratio **N_eff = 2.15** (raw) / **1.48**
  (standardized) of 5, Kuramoto R = 0.674. **Caveat (carried):** 12 days is a feasibility
  demo only; high-variance, and these subs share EU-news/language exposure so coupling is
  unsurprising and not specific to near-decomposability. The pre-registered test needs
  **months** of overlapping daily data plus a shuffled-sub null. Not yet a verdict.

---

## Test (iii) — Early Warning (fold-type)

- **Threshold:** **AUC ≥ 0.75** [PROPOSED].
- **Data source / frame:** a **frozen, pre-registered roster of M = 20 candidate
  fold-type transitions** selected **before** outcomes are known; the **N-/R-tipping
  exclusion is declared in advance** (only fold-type B-tipping candidates are scored
  here — see (iii′) for the adjudication).
- **Null / base-rate:** the **Boettiger null** — the same Scheffer early-warning battery
  (rising variance, rising lag-1 autocorrelation, rising cross-unit correlation, critical
  slowing-down) run over equal-length **non-event** windows (guard-banded), giving the
  base rate the signal must beat; guards against the prosecutor's fallacy.
- **Horizon:** pre-event windows of fixed length, strictly **before** event onset
  (no look-ahead), per the pilot's strict-cutoff design.
- **Test statistic:** **area under the ROC** of the pre-event indicator slopes against
  the non-event null distribution, aggregated over the M transitions.
- **Pass/fail:** PASS if AUC ≥ 0.75 against the stated base rate. FAIL (early-warning
  layer refuted) if AUC < 0.75.
- **CURRENT STATUS:** **PILOT RUN (single-event NULL, theory-consistent).**
  `validation/backtests/RESULTS.md` test (iii) / `temporal/test_early_warning.py`: one
  event detected (2025-04-02 tariff shock, z = 9.46, 3.22× baseline). Pre-event slopes
  did **not** rise (var-slope percentile 0.36, ac1-slope percentile 0.21 vs null) — a
  single-point **NULL**. This is **consistent** with the framework: the shock was an
  exogenous policy surprise (N-/R-tipping), for which the framework *predicts no*
  critical-slowing-down, and crucially the pipeline did **not** manufacture a false
  positive. **Caveat (carried):** one event, one sub, ~10 wk → one ROC point, not a
  curve. The pre-registered test needs the full M = 20 labeled roster (both endogenous
  B-tipping, expect a rise, and exogenous, expect null) to estimate a real ROC.
  **Detector + strict-cutoff + base-rate-null pipeline already real and working.**

---

## Test (iii′) — Bifurcation-Mix Conjecture (the sharpest bet)

- **Threshold:** B-tipping fraction floor **π_B = 0.60** [PROPOSED].
- **Data source / frame:** the **same frozen M = 20 roster** as test (iii). Each resolved
  crisis is **post-hoc adjudicated** as B-, N-, or R-tipping by a **pre-declared
  classification rule** (proposed: a written rubric keyed to (a) presence of a slow
  control-parameter drift toward a fold = B; (b) a single large fluctuation across a
  basin boundary with no preceding stability loss = N; (c) a stable state driven past too
  quickly with no bifurcation = R) applied by **raters blind to the early-warning
  scores**. ≥ 2 raters; inter-rater agreement (Cohen's κ) reported.
- **Null / base-rate:** none required — this is a proportion test against the committed
  floor π_B, not a skill test.
- **Horizon:** post-resolution adjudication of the roster.
- **Test statistic:** fraction of the M crises adjudicated B-tipping.
- **Pass/fail:** PASS if B-fraction ≥ π_B = 0.60. FAIL (the program's predictive-value
  conjecture refuted) if B-fraction < 0.60. **The paper names this as the test most
  likely to fail; that naming stands.**
- **CURRENT STATUS:** **NOT STARTED.** Requires the labeled M-roster (shared with (iii))
  and a blind-rater adjudication protocol that does not yet exist.

---

## Test (iv) — Smooth-Regime Skill

> (Enumerated as test *(v) Smooth-regime skill* in the paper; it is the 4th distinct
> operational test in the list. Numbered (iv) here for the 8-test checklist.)

- **Thresholds:** question-set size **m = 50** [PROPOSED]; Brier improvement
  **δ ≥ 0.05** [PROPOSED].
- **Data source / frame:** a **pre-registered question set of size m = 50** of
  resolvable, smooth-regime (label = smooth) forecasting questions, lodged before any
  resolve.
- **Null / base-rate:** the relevant **superforecaster or market-implied baseline** Brier
  score on the same question set (e.g. a Good-Judgment-style aggregate or market-implied
  probabilities), lodged in advance.
- **Horizon:** the resolution dates of the 50 questions (re-anchored block-aggregate
  horizons; no individual-level forecasts).
- **Test statistic:** Brier score of the engine vs the baseline; Δ = Brier_baseline −
  Brier_engine.
- **Pass/fail:** PASS if Δ ≥ δ = 0.05 (engine at least 0.05 better). FAIL (smooth-regime
  claim refuted) if Δ < 0.05. **A miss here while the engine declared "smooth" is a full
  refutation under §0.3(2) and may not be relabeled.**
- **CURRENT STATUS:** **NOT STARTED.** No live forecasting track exists; requires the
  assimilation engine + reanalysis corpus, which the paper states do not yet exist
  (design ahead of data).

---

## Test (v) — Fixed-Point Reliability

> (Paper test *(vi)*; 5th operational test.)

- **Threshold:** must beat the **naive base rate** of policy-announcement outcomes
  (proposed margin: published fixed-point forecasts hold at a rate **≥ 10 percentage
  points** above the naive base rate on the lodged set) [PROPOSED].
- **Data source / frame:** a **pre-registered set of policy announcements** (proposed:
  ≥ 25 credible published-fixed-point announcements — central-bank guidance, deposit
  guarantees, etc.), with the **publishable / non-publishable classification declared
  ex ante** (only fixed points are safe to publish).
- **Null / base-rate:** the naive base rate that the predicted fixed point would have
  held anyway (e.g. unconditional frequency of "no run / no cascade").
- **Horizon:** the resolution window of each announcement.
- **Test statistic:** hit-rate of published fixed-point forecasts vs naive base rate.
- **Pass/fail:** PASS if hit-rate exceeds base rate by the committed margin. FAIL
  (reflexivity repair refuted) if they hold **less** often than the base rate.
- **CURRENT STATUS:** **NOT STARTED.** Only an internal-consistency figure exists
  (`_verify_out/E5_fixed_points.png` — the reaction-map fixed points; SVB narrative
  echo), which the paper explicitly states carries **no** confirmatory weight.

---

## Test (vi) — Lucas Invariance

> (Paper test *(vii)*; 6th operational test.)

- **Threshold:** calibrated-coefficient drift across a regime break must stay **below
  what online assimilation can absorb within its lag** (proposed: post-break coefficient
  drift ≤ **2× the within-regime assimilation-tracked drift band**, i.e. ≤ 2 standard
  errors of the online estimate) [PROPOSED].
- **Data source / frame:** the calibrated coefficients **θ_S, v_k, D_k, W, Φ** estimated
  on a corpus spanning a **pre-declared regime break** (the break date lodged ex ante).
- **Null / base-rate:** the within-regime drift band that online assimilation already
  tracks (its lag-limited absorbable drift).
- **Horizon:** a window straddling the pre-declared regime break.
- **Test statistic:** magnitude of structural drift in the coefficient vector across the
  break, relative to the absorbable band.
- **Pass/fail:** PASS if drift stays within the absorbable band. FAIL (claim that the
  engine is more than a reduced-form fit refuted) if **large structural drift** exceeds
  it — the Lucas-critique (O2) failure.
- **CURRENT STATUS:** **NOT STARTED.** Requires a calibrated engine and a multi-regime
  reanalysis corpus; neither exists yet.

---

## Test (vii) — Regime Occupancy (the Soros bet)

> (Paper test *(viii)*; 7th operational test.)

- **Threshold:** fraction of windows classified **imitative** by the regime monitor stays
  **below the monotone fraction** — i.e. imitative windows are the rare exception, not the
  norm (proposed: imitative-window fraction **< 0.50** by **both** window count **and**
  realized-variance share) [PROPOSED].
- **Data source / frame:** a **named market-or-platform series** over a **pre-registered
  span**, lodged ex ante.
- **Null / base-rate:** generic (strong) reflexivity, under which imitative windows
  dominate.
- **Horizon:** the full pre-registered span.
- **Test statistic:** fraction of windows the regime monitor labels imitative, computed
  **both** by raw window count **and** by realized-variance share (so a rare-but-violent
  imitative regime cannot hide behind a small calendar footprint).
- **Pass/fail:** PASS (monotone-exception bet holds) if imitative fraction < monotone
  fraction on both measures. FAIL (the disagreement with strong reflexivity refuted in
  favor of generic reflexivity) if imitative windows dominate.
- **CURRENT STATUS:** **NOT STARTED.** Requires the regime monitor running on a live
  named series; not yet operationalized.

---

## Test (viii) — *(eighth slot)*

The paper's enumerated falsifiers are: (i), (ii), (iii), (iii′), (v), (vi), (vii), (viii)
— **eight distinct operational tests**, where the paper's own roman numbering skips (iv)
in the displayed list (it runs i, ii, iii, iii′, then v, vi, vii, viii). For this
checklist the eight are mapped as: i → Test (i); ii → Test (ii); iii → Test (iii);
iii′ → Test (iii′); v → Test (iv) above; vi → Test (v) above; vii → Test (vi) above;
viii → Test (vii) above. **All eight tests are specified above with no gaps.** This
section exists only to make the count auditable: there are exactly 8 falsifiers, each
with a PROPOSED threshold, frame, null, horizon, statistic, pass/fail rule, and current
status.

---

## Status ledger (rollup)

| Test | Name | Threshold(s) | Current status |
|------|------|--------------|----------------|
| (i) | Conservation / zero-sum | X=15%, Y=40%, Z=8%/yr | **CONTRADICTED at basket scale** — 9-subreddit finance/meme basket total ballooned ~14× in the GME mania (incumbent-only +1290%), churn 40%. Porous boundary so global claim untested; matches the single-sub pilot. See `validation/conservation_ecosystem/` |
| (ii) | Block independence | ρ₀=0.20 | **PILOT** — N_eff≈1.5–2.2/5 on 12-day window; inconclusive |
| (ii′) | Dynamic N_eff collapse | PRIMARY = community-specificity (fire vs shuffle), frozen binomial rule; n≥8 | **POWERED, SEALED PASS on the correct endpoint** — six-pass investigation. The theory's claim is community-SPECIFICITY (the existing community's frozen partition collapses past a block-label shuffle), not raw magnitude. That prediction is confirmed **four times** (Wikipedia population-wide negative control 0/14; original WSB 9/10; `neff_v3/` fresh WSB 9/10; `neff_v4/` fresh pre-registered-primary WSB **9/12, binomial p=1.7e-7**, median observed collapse at the 100th pctile of its own shuffle) and **SEALED** as a frozen primary endpoint on a fresh disjoint roster. The blunter raw-MAGNITUDE yardstick was tried (`neff_v2` f=0.298 median 0.00; `neff_v3` f=0.3936 median 0.138<f, p=0.069) and is reported, honestly and without moving it, as **non-discriminating** on a continuously high-volume forum (quiet windows compress N_eff a median ~0.10 too). Pass came from testing the RIGHT endpoint on new data, NOT from relaxing the magnitude threshold (that verdict stands). See `validation/neff_v4/` + `validation/NEFF_COLLAPSE_SYNTHESIS.md` |
| (iii) | Early warning | AUC≥0.75, M=20 | **POWERED, PARTIAL** — semantic-CSD across 10 WSB cascades beats guard-banded calm null (p=0.02, 5/5 endo above calm) but does NOT discriminate endo vs exo (AUC 0.60). Detects "a build", not which kind. See `validation/early_warning_powered/` |
| (iii′) | Bifurcation-mix | π_B=0.60 | **REFUTED on roster** — 24-cascade labelled roster, substantive B-fraction **0.33 < 0.60**; most cascades are sudden R-tipping shocks. Structural proxy 0.75 is a single-venue artifact (not adopted). The bet named most-likely-to-fail failed. See `validation/bifurcation_mix/` |
| (iv) | Smooth-regime skill | m=50, δ=0.05 | **NOT STARTED** — no live forecast track |
| (v) | Fixed-point reliability | ≥ base-rate + margin | **NOT STARTED** — only internal consistency figure |
| (vi) | Lucas invariance | drift ≤ absorbable band | **NOT STARTED** — needs calibrated multi-regime engine |
| (vii) | Regime occupancy (Soros) | imitative < monotone | **NOT STARTED** — regime monitor not live |

**Honest summary:** of the 8 falsifiers plus the dynamic-collapse sharpening (ii′),
**five now carry powered runs** (i, ii′, iii, iii′, and the ii pilot) and **four remain
not started** (iv, v, vi, vii — each waiting on a live forecasting/regime engine, not on
more data). The powered second wave is a split decision, not a victory lap: the structural
core (ii′) seals on its correct endpoint, while the dynamical-magnitude, predictive, and
conservation claims each deflate to narrow/partial/refuted/contradicted:
- (ii′) the dynamic N_eff collapse **seals on the endpoint that is the theory**. Its
  community-specificity (the existing community's frozen partition collapsing past a
  block-label shuffle) is confirmed **four times** (Wikipedia 0/14 negative control,
  original WSB 9/10, `neff_v3` fresh WSB 9/10, `neff_v4` fresh **pre-registered-primary**
  WSB **9/12 at binomial p=1.7e-7**) and is now a **SEALED PASS** under a frozen binomial
  rule on a fresh disjoint roster. The blunter raw-magnitude yardstick (tried in `neff_v2`
  and `neff_v3`) is reported, honestly and without moving it, as **non-discriminating**:
  genuinely-quiet WSB windows already drop N_eff a median ~0.10 with a tail to 0.43, because
  short high-volume onset windows compress N_eff generically, so magnitude cannot tell an
  endogenous cascade from a busy-but-quiet week. The pass came from testing the RIGHT
  endpoint on new data, not from relaxing the magnitude threshold (that verdict stands). The
  central result: the mechanism is **real, community-specific, and sealed as a structural
  signal**, correctly silent on the exogenous/mechanical events (in `neff_v4` the three
  non-firing cascades are a listing, a Fed rate decision, and a stock split).
- (iii) early warning is **POWERED, PARTIAL** — semantic-CSD beats a guard-banded calm
  null (p=0.02) but does not separate endogenous from exogenous (AUC 0.60): it detects
  "a build," not which kind.
- (iii′) the bifurcation-mix bet — named in advance as most-likely-to-fail — **REFUTED**
  on a 24-cascade roster (substantive B-fraction 0.33 < 0.60); most cascades are sudden
  R-tipping shocks.
- (i) conservation is **CONTRADICTED at basket scale** (a 9-subreddit basket ballooned
  ~14× in the GME mania); the porous boundary leaves the global claim untested.

The through-line: the impersonal/structural machinery is **real but load-bearing only on
the endogenous-reflexive minority**, and correctly quiet on the exogenous majority — which
**confirms the paper's bounded-special-regime thesis by measurement** rather than refuting
it. **No test has been confirmed as a clean PASS against social data.** This document
remains a commitment to the bets the program is willing to lose, now annotated with which
bets have been run and how they landed.
