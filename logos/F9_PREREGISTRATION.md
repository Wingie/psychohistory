# PRE-REGISTRATION: Falsifier F9, the observation bound (`logos-harness`)

**Checklist item:** F9 (`logos.tex` §15 falsifier table, row F9 at `logos.tex:693`; `logos/GAPS.md` §2 Tier 0, P0).
**Status of this document:** PLANNING / COMMITMENT ARTIFACT. It is not a claim of results. It fixes, before any run, every quantity that `logos/LOGOS_HARNESS.md` leaves free: sample size, seeds, endpoints, effect sizes, test statistics, multiplicity correction, stopping rule, and the gate, yield and round parameters that silently determine each arm's training corpus.
**Date drafted:** 2026-07-25.
**Source of record:** `logos.tex` §12 (`sec:observation`), the ordering claim at `logos.tex:602`, the F9 falsifier row at `logos.tex:693`, and the phase and gate table at `logos/LOGOS_HARNESS.md:290-307`.
**House format:** matches `validation/PRE_REGISTRATION.md` and `validation/neff_v4/PRE_REGISTRATION_neff_v4.md`. A frozen rule, evaluated exactly ONCE, reported straight.

Values marked **[FROZEN]** are binding once this document is lodged (§11). Values marked **[CALIBRATED]** are fixed by a rule stated here and executed on a calibration pass BEFORE any experimental arm is scored; the rule, not the number, is what is frozen now.

---

## THE HEADLINE FINDING, STATED FIRST: F9 IS UNDERPOWERED ON ONE CONSUMER GPU

**At the budget `logos/GAPS.md:33` assigns F9, this experiment cannot produce the result it exists to produce.** That is not a footnote. It is the most important thing this document says, and it is the reason it exists.

`GAPS.md:33` budgets F9 at "3-4 days training", which is 72 to 96 GPU-hours. `LOGOS_HARNESS.md:258` gives 18k to 30k tokens/s at 350M parameters and context 2048. A 2.0e9-token run is therefore 2.0e9 / 2.4e4 = 23.15 GPU-h (range 18.5 to 30.9). The budget buys 72/23.15 = 3.12 to 96/23.15 = 4.16 runs. The experiment has four arms. **That is one seed per arm.**

Three consequences follow, each demonstrable:

1. **With n=1 there is no within-arm variance estimate, so no test statistic of any kind can be computed.** The observed ordering is not falsifiable at n=1; it is a picture.

2. **Single-seed runs at this model size are corrupted at a measured rate of 20%.** PolyPythias (arXiv:2503.09543, 50 pre-training runs, 10 seeds per size) reports at 410M parameters, the size closest to this spec's 350M: "only two such combinations: 410M seed 3 and 4; only for these very seeds we observe 'loss spikes'", with those two performing notably worse than the other eight. At n=1 across five arms, P(at least one arm corrupted) = 1 - 0.8^5 = 0.672. The same paper declines to run ANOVA on 50 runs because "a formal statistical test (e.g., ANOVA and Tukey's test) would have required a larger sample size". MultiBERTs (arXiv:2106.16163, 25 pre-training seeds) independently reports "r values between 0.1 and 0.7 depending on pre-training seed".

3. **The deliverable F9 promises is a NEGATIVE, and negatives cost more N than positives.** `LOGOS_HARNESS.md:307`: "If unfiltered self-play matches grounded trajectories at matched token counts, the observation bound is wrong and this line of work should stop." "Matches" is an equivalence claim, which requires a two-one-sided-tests procedure with a pre-declared margin, which needs MORE N than a superiority test, not less. The exact Jonckheere-Terpstra permutation floor for a perfectly separated four-arm ordering is 1/((4n)!/(n!)^4): p = 3.97e-4 at n=2 and 2.71e-6 at n=3, so the POSITIVE direction is cheap. The TOST equivalence margin at 80% power is 2.486 sigma at n=2, 2.030 sigma at n=3, and 1.243 sigma at n=8, so the NEGATIVE direction is not.

**F9 as budgeted can confirm and cannot refute.** That is the exact inverse of the role `GAPS.md:111` assigns it: "the only experiment here that can return a cheap decisive negative."

### What compute fixes it

| | GPU-hours | Dollars |
|---|---|---|
| Budget implied by `GAPS.md:33` | 72 to 96 | ~$20 rented |
| **Powered design in this document** | **~718** | **$145 to $180 rented; ~EUR 76 of electricity on an owned RTX 3090** |

Breakdown in §8.1. The powered programme is 7.5x to 10x the current line item and is still under two hundred dollars. **The underpowered version is therefore not a budget constraint. It is an unforced error, and this document exists to remove it before the first run rather than to discover it afterwards.**

`GAPS.md:33` must be corrected to ~720 GPU-h, and `GAPS.md:111` must be qualified: at n=1 no negative is licensed at all.

---

## 0. Why this document exists

`logos/GAPS.md:111` orders F9 first in the entire programme. `logos/LOGOS_HARNESS.md` states the experiment as an ORDERING and supplies no sample size, no seeds, no effect size, no test statistic, no alpha and no stopping rule. `logos/ARCHITECTURE_REVIEW.md`, the repository's own self-review, contains no finding about F9's design at all: its fifteen findings are entirely about the Mixture-of-Towers architecture. F9 has had no referee pass before this one, and it is the P0 experiment on which the whole ledger is ordered.

---

## 1. Hypotheses

| | Claim | H0 |
|---|---|---|
| **H1** (the bound) | Environment-adjudicated grounded trajectories install held-out semantics that text cannot supply: g_A3 > g_A1 and g_A4 > g_A0. | equality |
| **H2** (the ordering) | The monotone ordering of `logos.tex:602` holds: g_A0 <= g_A1 <= g_A2 <= g_A3, at least one strict. | equality throughout |
| **H3** (the Tier-C claim) | The disagreement gate contributes over and above grounding: g_A3 > g_A4. This is the claim `logos.tex:561` and `LOGOS_HARNESS.md:58` both flag as "the claim we would most like tested". | equality |
| **H4** (the admission rule) | Yield-weighted accumulating admission prevents degeneration: the collapse monitor fires on A1 and not on A3. | fires on both or neither |

All tests one-sided in the direction the paper predicts. A reversal is reported as a reversal, never as a two-sided pass.

---

## 2. Arms [FROZEN]

`LOGOS_HARNESS.md:305` names four arms. `LOGOS_HARNESS.md:331` describes three. "Disagreement-gated self-play" is never operationally defined anywhere in `logos.tex` or `logos/*.md`; a grep for the phrase returns only the ordering sentences themselves. This section supplies the missing definition and one missing cell.

The four arms of the paper's ordering, as a 2x2 factorial on (disagreement gate) x (environment adjudication) plus a no-trajectory control:

| Arm | Gate | Environment | Trajectory source |
|---|---|---|---|
| **A0** "nothing" | | | none; the trajectory budget is spent on additional text |
| **A1** unfiltered self-play | OFF | OFF | proposals kept regardless of divergence; outcome is the ensemble's own majority prediction, never the emulator |
| **A2** disagreement-gated self-play | ON | OFF | kept only above tau_JS; outcome is still the ensemble's own majority prediction |
| **A3** grounded (the advocated configuration) | ON | ON | kept above tau_JS; outcome is the emulator's |

**Plus one arm the four-arm design cannot do without:**

| **A4** ungated grounded | OFF | ON | kept regardless of divergence; outcome is the emulator's |

**A4 is not optional.** Without it, A3 minus A2 estimates the adjudication effect with the gate ON, and A2 minus A1 estimates the gate effect with the environment OFF. The gate effect UNDER grounding, which is the only configuration the architecture advocates and the entire subject of H3, is unidentified. The paper's own flagged contribution cannot be isolated by the experiment built to test it. A4 costs 8 runs = 33 GPU-h.

---

## 3. Primary endpoint [FROZEN]

**g = p_heldout minus p_control**, a per-run scalar, difference-in-differences on the behavioural probe of `LOGOS_HARNESS.md:138`.

- **Battery.** 10,000 held-out items and 10,000 control items, enumerated from the Generation-I type chart under the constraint that **exactly one of the four offered moves is super-effective**, so chance is exactly 0.25 in both conditions by construction. RNG seed 20260725, written to `logos-harness/eval/battery_v1.jsonl`, SHA-256 in §11.
- **Presentation.** A battle-screen observation as RQ-VAE codes plus the trace-schema prefix of `LOGOS_HARNESS.md:202-219`, truncated at `action:`.
- **Scoring.** Deterministic argmax over the four legal `select_move` continuations by length-normalised total log-probability. No sampling, so decode noise is exactly zero.
- **Checkpoint.** Final checkpoint only. Intermediate checkpoints are diagnostics.

Chosen primary over the grounding probe because it measures capability, and the bound is a claim about capability, not representation; because the internal control absorbs arm-level general-competence differences, which is what makes a null interpretable; and because its within-run sampling error is nearly free to shrink. At m = 10,000 per condition and p ~ 0.3, sd = sqrt(2 x 0.21 / 10000) = 0.0065, negligible against between-seed sigma. Battery size is free; seeds are the entire constraint.

### 3.1 Corrected held-out and control vocabulary [FROZEN]

**The table at `LOGOS_HARNESS.md:131` is degenerate and must be replaced before any run.** Its control moves are `tackle` and `scratch`, both Normal-type, and Generation-I Normal-type moves have no super-effective matchup whatsoever (Bulbapedia Gen-I type chart: 1x against everything except 0.5x versus Rock and 0x versus Ghost). Its only Fire move, `ember`, is on the held-out side. **The control condition of the primary measurement therefore cannot register the quantity being measured**, which destroys exactly the interpretability `LOGOS_HARNESS.md:134` insists on ("The control set is not optional. It is what makes a null result interpretable").

| Class | HELD OUT (scrubbed from the entire text stream) | CONTROL (kept in text) |
|---|---|---|
| Types | `water`, `rock`, `grass`, `electric`, `ground` | `fire`, `normal`, **`bug`**, **`ice`** |
| Moves | `water_gun`, `thunder_shock`, `vine_whip`, `flamethrower` | **`ember`**, `tackle`, `scratch` |
| Phrases | `super effective`, `not very effective` | held out in BOTH conditions, so the verbal-readout channel stays matched |

Generation-I Fire is 2x against Bug, Grass and Ice. Grass is held out; Bug and Ice are kept; `ember` is kept. So `ember` against a Bug-type or Ice-type defender is a **valid text-supported super-effective control item**, which the original table had none of. `flamethrower` replaces `ember` on the held-out side so a Fire held-out item still exists.

Scrubbing is enforced at tokenizer level as a hard post-processing step (`LOGOS_HARNESS.md:246`) and verified by the Phase-2 leak validator (`LOGOS_HARNESS.md:296`), with the leak count recorded in §11. **A non-zero leak count voids the run.**

### 3.2 What the primary endpoint can and cannot do, stated in advance

Held-out semantics are unavailable to A0, A1 and A2 **by construction**: the terms are scrubbed from all text and only A3 and A4 touch the environment. g is therefore expected at ~0 for all three, and the primary endpoint reads exactly one bit, grounding versus no grounding. **The four-arm ordering of `logos.tex:602` is not measurable on any single endpoint**, because the arms differ on two orthogonal dimensions and g reads one. The gate contrasts are carried by the secondaries. A flat primary across A0, A1 and A2 is the PREDICTED pattern and may not be written up as "the ordering partially held".

---

## 4. Secondary endpoints [FROZEN]

Holm-corrected within the secondary family, evaluated only if the primary gate (§7 STEP 2, contrast C1) passes. Supportive, never confirmatory.

- **S1 grounding probe.** Fraction of held-out terms whose top-5 nearest observation codes by cosine come from frames containing that type or move (`LOGOS_HARNESS.md:138`), versus the same fraction for control terms, against a 1,000-draw permutation null over code assignment. Not primary: the held-out set is ~11 terms, a hard resolution ceiling, and cosine nearest-neighbour reads representation rather than behaviour.
- **S2 collapse monitor.** §6.
- **S3 mean admitted yield per arm** (Eq. `LOGOS_HARNESS.md:68`). Manipulation check that the gate did what `LOGOS_HARNESS.md:298` claims. **If mean admitted yield in A3 does not exceed A1, the loop did not run as specified and the run is VOID, not negative.**
- **S4 proposer diversity.** Mean pairwise Jensen-Shannon divergence between the two proposer models' predictive distributions on a frozen 5,000-item probe set, measured and recorded **before any training arm runs**. `LOGOS_HARNESS.md:35` states the precondition absolutely ("the towers must be informatively different, or the loop is provably worthless") and `LOGOS_HARNESS.md:298` then asserts it categorically (">=2 distinct open models") without measuring it. **If mean pairwise JS < 0.15 the experiment is VOID**: a null on the gate arms would otherwise be uninterpretable between "the gate does nothing" and "the proposers were not diverse".

### 4.1 Exploratory: labelled, no inference, no gate

- **VideoGameBench Lite progress.** `LOGOS_HARNESS.md:300` makes this a Phase-6 GATE. It cannot be one. VideoGameBench (arXiv:2505.18134): "The best performing models, Gemini 2.5 Pro and Claude 3.7 Sonnet, complete only 0.48% of VideoGameBench and 1.6% of VideoGameBench Lite." A 350M model scores 0 in every arm; zero between-arm variance is zero power, and as a gate it fails Phase 6 for reasons unrelated to the hypothesis. Demoted to descriptive reporting.
- **Validation NLL on a shared natural-text set.** Disqualified as a between-arm capability comparison: each arm trains on a different distribution by construction, so cross-arm NLL confounds distribution distance with capability. Monitor only.
- Anything not named in §3 or §4 is exploratory and must be labelled as such in the write-up.

---

## 5. Matching protocol [FROZEN]

At fixed model, fixed sequence length 2048 and fixed global batch, matched total tokens, matched optimizer steps and matched training FLOPs are the **same experiment**. The apparent four-way ambiguity is a two-way one: total versus unique. The fork exists only because the gate is a filter.

**PRIMARY matching M1: matched total AND unique, achieved by over-generating in the gated arms.**

| Quantity | 125M screen | 350M confirmatory |
|---|---|---|
| Total training tokens T, every arm | 1.0e9 | 2.0e9 |
| Trajectory share phi, arms A1 to A4 (A0: 0) | 0.25 | 0.25 |
| Unique admitted trajectory tokens U = phi x T / 2 | 1.25e8 | 2.5e8 |
| Unique text tokens U_text = T/4 | 2.5e8 | 5.0e8 |
| Text epochs, A0 | **4.0** | **4.0** |
| Text epochs, A1 to A4 | 3.0 | 3.0 |
| Trajectory epochs, A1 to A4 | 2.0 | 2.0 |

A1 to A4 over-generate proposals to reach the identical U. **Generation compute is deliberately not matched** and is reported as a separate per-arm ledger line (proposals generated, admission rate, GPU-h); the claim under test is about training data, not generation cost.

**The epoch sizing is not cosmetic.** `LOGOS_HARNESS.md:260` commits to "<=4 epochs" and warns "Watch for the epoch-5 jump" (Muennighoff, arXiv:2305.16264). At matched total tokens A0 has no trajectory data and spends the whole budget on text at 1/(1 - 0.25) = 1.33x the trajectory arms' epochs. Sizing U_text naively would put A0 at 5.33 epochs, inside the degradation regime the spec itself flags, and the "nothing" arm would then lose for a reason with nothing to do with grounding. U_text = T/4 pins A0 at exactly 4.0.

**Dilution, stated in advance.** At phi = 0.25 the arms are identical over 75% of their training tokens (`LOGOS_HARNESS.md:260` caps observation tokens at 15 to 30% and mandates 20 to 30% text replay). All effect sizes here are per-TOTAL-token; the per-differentiating-token effect is roughly 4x larger and may not be quoted as if it were the headline.

**SECONDARY matching M2 [FROZEN], reported alongside M1:** matched GENERATION budget, that is, identical proposal count in all arms, which forces the gated arms to fewer unique tokens and more repetition. M2 is the question an operator faces; M1 is the question the paper asks. M2 would show the gate losing on any diversity-sensitive endpoint purely because a q = 0.25 gate quarters unique data, which is a result about repetition, not grounding. Registered because **a positive under M2 is strictly stronger than a positive under M1**.

---

## 6. The collapse monitor, specified [FROZEN rule, CALIBRATED thresholds]

`LOGOS_HARNESS.md:285` names `collapse_monitor.py` and never specifies it. This section is the specification.

**Probe set P:** 2,000 sequences of 2,048 tokens of natural text from the same source as the training text, disjoint from all training data, frozen at Phase 3, SHA-256 in §11. All statistics teacher-forced, so decoding temperature cannot confound anything.

| | Statistic | Direction under collapse |
|---|---|---|
| **M1** | tail NLL: mean of -log p(target given context) over probe positions whose target is in the bottom decile of the training-text unigram frequency distribution AND occurs >= 100 times (excludes hapax noise) | rises |
| **M2** | predictive entropy: mean over all probe positions of -sum_v p_v log p_v | falls |
| **M3** | representational effective dimension: participation ratio (sum lambda)^2 / sum(lambda^2) of the final-layer hidden-state covariance eigenspectrum over the 2,000 last positions | falls |

All three are required because each fails alone. Mean perplexity is head-dominated and can improve while tails are lost, and collapse is a tail phenomenon (Shumailov et al., *Nature* 631:755-759, 2024). Generated-text n-gram entropy is confounded by decoding temperature, which teacher-forcing removes. Representation dimension alone can move with no distributional consequence. M3 reuses the variance-ratio effective dimension the repository already uses at `validation/reddit_wsb/neff_collapse_wsb.py` and that `GAPS.md:37` names for falsifier F5, so **F5 becomes a genuine free by-product rather than a promissory one**.

**Baseline:** arm A0 at the SAME optimizer step, matched on seed index. An absolute entropy threshold is meaningless without a reference.

**Calibration [CALIBRATED, rule frozen now]:** run A0's 8 seeds first; compute s(M1), s(M2), s(M3), the across-seed standard deviation of each statistic at each checkpoint. Thresholds are 3 x s. The numeric thresholds are frozen at the end of calibration and **before any experimental arm is evaluated**, and recorded in §11. This mirrors the shuffle-null quantile rule of `validation/neff_v4/PRE_REGISTRATION_neff_v4.md` §1.

**FIRE RULE [FROZEN].** Arm a fires at checkpoint t if and only if, against A0 matched on seed index and step t:

> Delta_M1 >= 3 s(M1) **AND** ( Delta_M2 <= -3 s(M2) **OR** Delta_M3 / M3_A0 <= -3 s(M3) / M3_A0 )

holding at **two consecutive** checkpoints of the frozen grid {25, 50, 75, 100}% of steps.

**CONSEQUENCE TABLE [FROZEN].** `LOGOS_HARNESS.md:316` states "If the monitor fires, the mechanism is refuted" with no arm qualifier. That is wrong, and it contradicts the paper: `logos.tex:693` correctly says "the collapse monitor firing **on the grounded arm**". Firing on A1 is PREDICTED by the two sources the spec itself cites at `LOGOS_HARNESS.md:41-43` (Zenil arXiv:2601.05280; Shumailov, *Nature* 631). **As written, the spec refutes the mechanism on its own predicted result**, and `LOGOS_HARNESS.md:299` compounds this by making "no tail narrowing" a BLOCKING Phase-5 gate that would halt the experiment on that same predicted outcome.

| Fires on | Consequence |
|---|---|
| A1 (and not A3) | **Predicted.** Confirms monitor sensitivity. Refutes nothing. |
| A3 (grounded) | **Refutes H4**, the admission rule, the third of the paper's three original claims. Named as an F9 falsification condition at `logos.tex:693`. |
| A2 but not A1 | Anomalous. Report; do not adjudicate. |
| No arm, including A1 | **The monitor is insensitive at this budget. All collapse conclusions from F9 are VOID.** |

The last row is the most likely single outcome and is why §8.1 splits out a multi-round sub-study. The blocking Phase-5 gate at `LOGOS_HARNESS.md:299` is demoted to a reported diagnostic.

---

## 7. Analysis plan and multiplicity [FROZEN]

Hierarchical fixed-sequence gatekeeping. Executed exactly ONCE by `logos-harness/analysis/analyze_f9.py`.

**STEP 1, the gate.** Exact **Jonckheere-Terpstra** trend test on the ordered alternative g_A0 <= g_A1 <= g_A2 <= g_A3 over seed-level values, one-sided alpha = 0.05, **exact permutation null, not the normal approximation**. If STEP 1 fails, **H2 fails outright**: no pairwise testing, no subgroup, no rescue.

**STEP 2, contrasts, only if STEP 1 passes.** Five two-sample permutation tests (10,000 draws) with **Holm** correction at family alpha = 0.05, one-sided:

| # | Contrast | Estimates | Hypothesis |
|---|---|---|---|
| C1 | A3 vs A1 | grounding plus gate versus neither | H1, and the decisive contrast |
| C2 | A2 vs A1 | gate effect without environment | H2 |
| C3 | A1 vs A0 | trajectory tokens versus more text | H2 |
| C4 | A4 vs A0 | pure grounding effect | H1 |
| C5 | A3 vs A4 | **gate effect under grounding** | **H3, the Tier-C claim** |

**STEP 3, secondaries, only if C1 passes.** S1 to S4, Holm within family, supportive only.

Because STEP 1 is a closed gatekeeper, the STEP-2 family carries no additional penalty for it. Permutation rather than t throughout, because n = 8 cannot verify normality.

**Equivalence testing [FROZEN].** Any contrast that fails superiority is submitted to a **TOST** at alpha = 0.05 with margin **eps = 1.243 x sigma_hat**, sigma_hat being the pooled across-seed standard deviation of g. At n = 8 that is the margin the design supports at 80% power. A contrast that fails superiority AND fails TOST is reported **INCONCLUSIVE**, never as "no difference".

**Blind outlier rule [FROZEN].** Any run whose training-loss curve contains a spike exceeding 3x the trailing-100-step median absolute deviation of the loss is excluded and replaced by a fresh seed. **Detection is from the loss curve alone, before any endpoint is computed.** Grounded in PolyPythias (arXiv:2503.09543): 2 of 10 seeds at 410M show loss spikes with notably worse downstream performance. Replacement reserve: 20% of runs. At n = 8 this drops P(at least one of five arms corrupted) from 0.672 to 0.051.

**Free parameters, frozen here because they set each arm's corpus:**

| Parameter | Spec status | Frozen value |
|---|---|---|
| tau_JS, the disagreement gate | `LOGOS_HARNESS.md:74` says "Below threshold, discard" and gives no value; `:271` names the config file and no number appears in the document | **[CALIBRATED]** the value admitting exactly **q = 0.25** of proposals on a 50,000-proposal calibration pool generated **before any training arm runs**. A quantile, not a magic number, mirroring `neff_v4`'s 90th-percentile shuffle rule |
| yield weighting | `LOGOS_HARNESS.md:78` says "Admit weighted by yield" and gives no function | w(tau) = clip(yield(tau), 0, 10), normalised to mean 1 within each round |
| bootstrap rounds | `LOGOS_HARNESS.md:79` says only "repeat" | R = 1 for Study 1, R = 5 for Study 2 |

---

## 8. Sample size, power and cost [FROZEN]

**Planning sigma** (across-seed standard deviation of g, in accuracy points): **0.05** after blind outlier exclusion, **0.09** if outliers are retained. Anchors: MultiBERTs (arXiv:2106.16163) r spans 0.1 to 0.7 across 25 pre-training seeds; PolyPythias (arXiv:2503.09543) 2 of 10 outlier seeds at 410M with inter-seed downstream Cohen's kappa converging to ~0.5.

**Effect size worth detecting: delta = 0.15** accuracy points (chance 0.25 to 0.40). Justified by the spec's own rhetoric at `LOGOS_HARNESS.md:335`: the substrate is "the easiest imaginable grounding substrate, where the exact semantics under test are printed on screen in four colours at 160x144". A lift under 15 points there does not support "observation bandwidth is the binding constraint"; it supports "grounding barely works".

**Power table.** Superiority MDE = sigma x sqrt(2/n) x (z_{0.05/3} + z_{0.80}) = sigma x sqrt(2/n) x 2.9696. TOST margin at 80% power = sigma x sqrt(12.366/n).

| n | MDE / sigma | MDE at sigma = 0.05 | TOST eps / sigma | eps at sigma = 0.05 | JT exact p_min, k=4, perfect separation |
|---|---|---|---|---|---|
| 1 | undefined | undefined | undefined | undefined | undefined |
| 2 | 2.970 | 0.148 | 2.486 | 0.124 | 3.97e-4 |
| 3 | 2.425 | 0.121 | 2.030 | 0.102 | 2.71e-6 |
| 5 | 1.878 | 0.094 | 1.573 | 0.079 | 8.52e-11 |
| **8** | **1.485** | **0.074** | **1.243** | **0.062** | 1.00e-17 |
| 16 | 1.050 | 0.052 | 0.879 | 0.044 | |

**n = 8 is the knee.** n = 16 buys 1.485 to 1.050 sigma for double the cost; n = 5 degrades to 1.878 and n = 3 to 2.425. n = 8 is also the smallest n at which the equivalence margin, 1.243 sigma or about 6 accuracy points, is tight enough that a declared negative is worth reporting.

### 8.1 Studies and budget

| Study | Model / tokens | Arms | Seeds | Rounds | Runs | GPU-h |
|---|---|---|---|---|---|---|
| **1, ordering (primary)** | 125M / 1.0e9 | A0 to A4 | 8 | 1 | 40 | 164 |
| **2, collapse (S2)** | 125M / 1.0e9 | A0, A1, A3 | 3 | 5 (A0: 1) | 33 | 135 |
| **3, confirmatory scale** | 350M / 2.0e9 | A0, A1, A3 | 3 | 1 | 9 | 208 |
| Outlier replacement reserve (20%) | | | | | ~16 | 101 |
| Trajectory generation, all arms, both models | | | | | | 75 |
| RQ-VAE training plus frame tokenization | | | | | | 15 |
| Eval batteries and probes across checkpoints | | | | | | 20 |
| **TOTAL** | | | | | | **~718** |

Per-run cost from `LOGOS_HARNESS.md:258`: 125M at 45k to 90k tokens/s gives 1.0e9 tokens = 3.1 to 6.2 GPU-h, planned at 4.12; 350M at 18k to 30k tokens/s gives 2.0e9 tokens = 18.5 to 30.9 GPU-h, planned at 23.15.

**This inverts the spec's phase order.** `LOGOS_HARNESS.md:299` runs "125M debug end to end, then 350M". Here 125M is the POWERED SCREEN and 350M is a low-n confirmatory replicate, because at this budget seeds buy more inferential value than parameters.

**Cost:** ~718 GPU-h. At RTX-3090 community-cloud rates of $0.20 to $0.25 per GPU-h that is **$145 to $180**. On an owned RTX 3090 at 350 W and EUR 0.30/kWh it is 251 kWh, about **EUR 76**.

**Day-one probe [FROZEN].** `LOGOS_HARNESS.md:258` states its throughput figures "are interpolations from measured 4090, A30, and L20 runs, not a first-party 3090 log at these sizes". An independent recomputation against the NVIDIA GA102 whitepaper (Appendix A, Table 9, p.44: RTX 3090 peak BF16 tensor with FP32 accumulate 71 TFLOPS dense, 142 only with 2:4 structural sparsity) puts the 350M sustained rate at ~9.1k tokens/s, not 18k to 30k, because 30k tokens/s at 2.526 GFLOP/token would require 75.8 TFLOP/s sustained, which exceeds the card's dense peak. **Before committing, run a forward-backward probe and record measured tokens/s at both sizes in §11. If measured throughput falls below 60% of the planning midpoint, reduce T before reducing n.** Seeds are the inferential currency; tokens are not.

---

## 9. Stopping rule [FROZEN]

1. **No interim analysis on the primary.** g is computed once, on final checkpoints, after all Study-1 runs complete. No peeking, no sequential stopping, no alpha spending.
2. **The only permitted early termination is technical**: a run diverges (loss NaN or inf) or trips the blind outlier rule of §7. It is replaced by a fresh seed from the pre-declared seed list `[1001..1024]`, consumed in order.
3. **Voiding conditions**, checked before any endpoint is computed: (a) S4 proposer diversity < 0.15; (b) S3 mean admitted yield in A3 not exceeding A1; (c) the leak scan finds any held-out term in the text stream; (d) the Phase-1 RQ-VAE gate of `LOGOS_HARNESS.md:295` fails. Any of these gives **VOID, no directional conclusion**.
4. **Underpowered condition.** If realised sigma_hat makes the realised MDE exceed the pre-declared 0.074, the run is reported **UNDERPOWERED**, the realised MDE and TOST margin are published, and no equivalence claim is made.
5. Study 2 and Study 3 run regardless of Study 1's outcome. A negative Study 1 does not license skipping the collapse and scale checks; those are what distinguish a real negative from a broken harness.

---

## 10. What would kill the programme [FROZEN]

**K1, the bound is refuted.** C1 (A3 versus A1) fails superiority AND TOST declares equivalence at eps = 1.243 sigma_hat. Then grounding buys under about 6 accuracy points over pure self-play on the easiest imaginable grounding substrate; the observation channel is not the scarce resource at this scale; `logos.tex` §12 is wrong as stated; the ordering sentence at `logos.tex:602` must be struck; and per `LOGOS_HARNESS.md:307` and `logos.tex:335`, "the strategy past the token wall is repetition plus synthesis, the paper's Proposition 2 headroom is all there is, and `logos.tex` should say so."

**K2, the admission rule is refuted.** The collapse monitor fires on A3 under the §6 rule. Already named at `logos.tex:693`. The third of the paper's three original claims falls.

**K3, the Tier-C claim is refuted while the bound survives.** C1 passes but C5 (A3 versus A4) and C2 (A2 versus A1) both fail superiority and both declare TOST equivalence. Then grounding works and the disagreement gate contributes nothing. The claim `logos.tex:561` calls "the specific contribution" and "the claim we would most like tested" is dead, and the Mixture-of-Towers architecture loses its learning-from-disagreement justification entirely; it must then be defended on update economics alone (`logos.tex:32`). **K3 is the outcome this design is worst powered to detect and the paper cares most about. That asymmetry is disclosed here rather than discovered afterwards.**

**K4, not a result.** Any voiding condition of §9.3, or the underpowered condition of §9.4, or the no-arm-fires row of §6. Reported VOID or UNDERPOWERED. **A non-significant C1 at n < 8 is explicitly NOT K1** and may not be written up as one.

No result here is renegotiated after the numbers land. The rule above is the whole verdict.

---

## 11. Seal [FROZEN]

SHA-256 digests, computed and lodged **before the first training run**:

| Artifact | sha256 |
|---|---|
| this file | *(fill at lodge)* |
| `logos-harness/configs/arms.yaml` | *(fill)* |
| `logos-harness/configs/heldout_vocab.yaml` | *(fill)* |
| `logos-harness/configs/bootstrap.yaml` | *(fill)* |
| `logos-harness/eval/battery_v1.jsonl` | *(fill)* |
| collapse probe set P | *(fill)* |
| seed list `[1001..1024]` | *(fill)* |

**Anchor: an OpenTimestamps `.ots` Bitcoin proof is REQUIRED, not optional, in addition to the git tag and the GitHub push time.**

`validation/PREREGISTRATION_SEAL.md:29-32` concedes that OpenTimestamps "is not installed here" and that no OSF DOI is lodged, and lines 37-44 concede that two prior pre-registrations were authored "in a single working session rather than under an independent prior timestamp". That concession is defensible for retrospective tests over dumps that already existed. **It is not defensible for F9, whose data does not exist yet.** A genuine ex-ante third-party anchor costs nothing here, so accepting the weaker git-only anchor would be a pure unforced loss of evidential value. This is also the correct place to record that `PREREGISTRATION_SEAL.md` names neither `neff_v3` nor `neff_v4` in its scope, so no prior seal covers this document by inheritance.

**Post-calibration addendum**, appended and re-hashed after the calibration pass and before any experimental arm is scored: tau_JS at q = 0.25; s(M1), s(M2), s(M3) from the A0 calibration; measured 3090 tokens/s at 125M and 350M; the S4 proposer-diversity value; the leak-scan count.

---

## 12. Honesty rails (carried)

- The design is **underpowered at the budget the repository currently assigns it**, and that is stated at the top of this document rather than in a footnote (see the banner above §0).
- The primary endpoint reads **one bit**, grounding versus no grounding. It cannot rank the three ungrounded arms. Stated in §3.2 in advance.
- The paper's own flagged contribution (H3) is the contrast this design is **worst** powered to detect. Stated in §10 K3 in advance.
- Three of the numbers this pre-registration depends on come from `LOGOS_HARNESS.md:258`, which itself declares them "interpolations ... not a first-party 3090 log". An independent recomputation against the GA102 whitepaper puts the true 350M rate about 2.6x lower. §8.1's day-one probe is the resolution, and until it runs **the GPU-hour totals in §8.1 are a lower bound**.
- Substrate B (the psychohistory validation pipeline as adjudicator) is **not** part of this pre-registration's primary or secondary endpoints. An independent count of the sealed rosters gives 83 rows, 68 distinct onset dates, 58 distinct real-world episodes and 35 carrying a committed endogenous/exogenous label, which caps a paired Substrate-B contrast at a minimum detectable effect of about 0.42 sigma before any disagreement gate discards anything. Substrate B is a directional sanity check that can refute and cannot confirm, and a null from it is not evidence of absence.
- If the primary endpoint FAILS, that is a real negative for the observation bound and will be reported as such. The rule above is the whole verdict and will not be renegotiated after the numbers land.

---

## 13. Reproduce

```
py -3.12 logos-harness/eval/battery_build.py          # frozen probe battery + sha256
py -3.12 logos-harness/eval/proposer_diversity.py     # S4 gate, BEFORE any training
py -3.12 logos-harness/bootstrap/calibrate_gate.py    # tau_JS at q=0.25, BEFORE any training
py -3.12 logos-harness/train/run_arm.py --arm A0 --seed {1001..1008}   # calibration arm first
py -3.12 logos-harness/eval/collapse_monitor.py --calibrate            # freeze s(M1..M3)
py -3.12 logos-harness/train/run_arm.py --arm {A1..A4} --seed {1001..1008}
py -3.12 logos-harness/analysis/analyze_f9.py         # evaluate the frozen rule ONCE
```
