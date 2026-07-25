# PRE-REGISTRATION: Falsifier F9, the observation bound (`logos-harness`)

**Checklist item:** F9 (`logos.tex` §15 falsifier table, row F9; `logos/GAPS.md` §2 Tier 0, P0). Also carries **F5** (by-product, §6) and **F13 limb (b)** (costed in §8.2), both of which `logos.tex` §15 scopes as arms or by-products of F9.

**Line references.** This document cites `logos.tex` and `logos/LOGOS_HARNESS.md` by SECTION, not by line number. Both files are under active revision and line numbers in earlier drafts of this document had already gone stale by the time the round-2 corrections landed.
**Status of this document:** PLANNING / COMMITMENT ARTIFACT. It is not a claim of results. It fixes, before any run, every quantity that `logos/LOGOS_HARNESS.md` leaves free: sample size, seeds, endpoints, effect sizes, test statistics, multiplicity correction, stopping rule, and the gate, yield and round parameters that silently determine each arm's training corpus.
**Date drafted:** 2026-07-25.
**Source of record:** `logos.tex` §12 (`sec:observation`), its ordering claim, the F9 and F13 falsifier rows in `logos.tex` §15, and the phase and gate table at `logos/LOGOS_HARNESS.md` §7.

**Revision note, 2026-07-25.** This version reconciles against the corrections that landed in `LOGOS_HARNESS.md` after the first draft was written: the withdrawn throughput figures (§5.4 of that file, reflected in the banner above and §8), the resolved observation tokenizer at 90 tokens per frame rather than 270 (§3.2 there, reflected in §5 here), the inverted model sizing that makes 125M the powered screen (§5.1 there, §8.1 here), the ungated-scoring mandate from round-2 finding X-12 (§2.1 there, §2 here), and falsifier F13 limb (b), which `logos.tex` §15 scopes as an arm of F9 and which the previous budget did not pay for (§8.2 here). Every number touched was recomputed rather than scaled.
**House format:** matches `validation/PRE_REGISTRATION.md` and `validation/neff_v4/PRE_REGISTRATION_neff_v4.md`. A frozen rule, evaluated exactly ONCE, reported straight.

Values marked **[FROZEN]** are binding once this document is lodged (§11). Values marked **[CALIBRATED]** are fixed by a rule stated here and executed on a calibration pass BEFORE any experimental arm is scored; the rule, not the number, is what is frozen now.

---

## THE HEADLINE FINDING, STATED FIRST: F9 IS UNDERPOWERED ON ONE CONSUMER GPU, AND THE CONTRAST THE PAPER CARES MOST ABOUT STAYS UNDERPOWERED EVEN AFTER THE FIX

Two claims, in the order of what they cost to repair. Neither is a footnote. Together they are the reason this document exists.

### Claim 1: the ledger budget does not buy even one seed per arm, and the corrected throughput makes that worse by a factor of 2.6

`GAPS.md` §2 budgets F9 at "3-4 days training", which is 72 to 96 GPU-hours. Earlier drafts of this document costed runs against `LOGOS_HARNESS.md`'s original figure of 18k to 30k tokens/s at 350M, **which was interpolated from 4090, A30 and L20 runs and was never measured on a 3090**. `LOGOS_HARNESS.md` §5.4 has since withdrawn it: at 2.526 GFLOP/token, 30k tok/s demands 75.8 TFLOP/s sustained, above the RTX 3090's dense BF16-with-FP32-accumulate peak of 71 TFLOPS (NVIDIA GA102 whitepaper, Appendix A Table 9, p.44). The replacement figures are **about 9.1k tok/s at 350M** and **about 29k tok/s at 125M**.

```
python3: 1.0e9/2.90e4/3600 =  9.579 GPU-h per 1e9 tokens at 125M
         1.0e9/9.10e3/3600 = 30.525 GPU-h per 1e9 tokens at 350M   (band 29.9 to 42.1 at 9.3k to 6.6k)
         one 125M run, T=1.0e9  =  9.579 GPU-h   (planned at 4.12 on the old figure, x2.32)
         one 350M run, T=2.0e9  = 61.050 GPU-h   (planned at 23.15 on the old figure, x2.64)
```

At 350M the ledger budget buys 72/61.05 = **1.18** to 96/61.05 = **1.57** runs. The experiment has **five** arms (§2). That is **0.24 to 0.31 seeds per arm**: not one seed per arm, a quarter of one. At the 125M screen it buys 72/9.579 = 7.52 to 10.02 runs, which is **1.50 to 2.00 seeds per arm**. Either way n <= 2.

Three consequences follow, each demonstrable:

1. **With n=1 there is no within-arm variance estimate, so no test statistic of any kind can be computed.** The observed ordering is not falsifiable at n=1; it is a picture. At n=2, which is the best the ledger budget reaches and only at 125M, a variance estimate exists on one degree of freedom and the five-contrast MDE is 3.168 sigma, which is 0.158 accuracy points, above the delta = 0.15 the design exists to detect. **So even the generous reading of the ledger budget cannot detect the effect it is looking for.**

2. **Single-seed runs at this model size are corrupted at a measured rate of 20%.** PolyPythias (arXiv:2503.09543, 50 pre-training runs, 10 seeds per size) reports at 410M parameters, the size closest to this spec's 350M: "only two such combinations: 410M seed 3 and 4; only for these very seeds we observe 'loss spikes'", with those two performing notably worse than the other eight. At n=1 across five arms, P(at least one arm corrupted) = 1 - 0.8^5 = 0.672. The same paper declines to run ANOVA on 50 runs because "a formal statistical test (e.g., ANOVA and Tukey's test) would have required a larger sample size". MultiBERTs (arXiv:2106.16163, 25 pre-training seeds) independently reports "r values between 0.1 and 0.7 depending on pre-training seed".

3. **The deliverable F9 promises is a NEGATIVE, and negatives cost more N than positives.** `LOGOS_HARNESS.md` §7: "If unfiltered self-play matches grounded trajectories at matched token counts, the observation bound is wrong and this line of work should stop." "Matches" is an equivalence claim, which requires a two-one-sided-tests procedure with a pre-declared margin, which needs MORE N than a superiority test, not less. The exact Jonckheere-Terpstra permutation floor for a perfectly separated four-arm ordering is 1/((4n)!/(n!)^4): p = 3.97e-4 at n=2 and 2.71e-6 at n=3, so the POSITIVE direction is cheap. The TOST equivalence margin at 80% power is 2.486 sigma at n=2, 2.030 sigma at n=3, and 1.243 sigma at n=8, so the NEGATIVE direction is not.

**F9 as budgeted can confirm and cannot refute.** That is the exact inverse of the role `GAPS.md` §5 assigns it: "the only experiment here that can return a cheap decisive negative."

**What compute fixes it, and it is the 125M screen that does the fixing.** The lever is not more money, it is the model size the seeds are bought at. A 125M run is 9.579 GPU-h against 61.05 at 350M, a factor of 6.37, so **the entire five-arm n = 8 ordering study costs 40 x 9.579 = 383.1 GPU-h**, less than seven 350M runs. This is why §8.1 inverts the spec's phase order and makes 125M the powered screen and 350M a low-n confirmatory replicate.

| | GPU-hours | Dollars | Electricity on the owned card |
|---|---|---|---|
| Budget implied by `GAPS.md` §2 | 72 to 96 | $14 to $24 rented | ~EUR 10 |
| Old figure in this document, planned off the withdrawn throughput | 718 | $145 to $180 | ~EUR 76 |
| **Powered design, re-derived against the corrected throughput** | **~1,400** | **$281 to $351 rented** | **491 kWh, ~EUR 147** |
| Same, if the day-one probe fires the frozen "reduce T" rule (§8.3) | ~1,073 | $215 to $268 | 376 kWh, ~EUR 113 |

Breakdown in §8.1. The powered programme is 14.6x to 19.5x the current ledger line and is still under four hundred dollars, or under EUR 150 of electricity on a card that is already owned. **The underpowered version is therefore not a budget constraint. It is an unforced error, and this document exists to remove it before the first run rather than to discover it afterwards.**

`GAPS.md` §2 and §5 must be corrected from ~718 to **~1,400 GPU-h**, and `GAPS.md` §5's "cheap decisive negative" must be qualified: at n <= 2 no negative is licensed at all.

### Claim 2: the corrected budget fixes the ordering test and does NOT fix K3

K3 is the kill condition where grounding works and the disagreement gate contributes nothing (§10). It is the outcome the paper cares most about, because the gate is the part `logos.tex` §12 calls "the specific contribution" and "the claim we would most like tested". **K3 is a conjunction of two equivalence declarations** (C5 and C2 both failing superiority and both declaring TOST equivalence), and equivalence is the expensive direction. At n = 8 the tightest declarable margin is eps = 1.243 sigma, about 6.2 accuracy points at the planning sigma of 0.05. A true gate effect of 3 points is then neither significant nor equivalent, and the verdict is INCONCLUSIVE, which is the modal outcome for the contrast the paper most wants settled.

```
python3: eps = sigma*sqrt(2*(z_0.95+z_0.80)^2/n) = sigma*sqrt(12.365/n)
         n for eps = 1.243 sigma (6.2 pts):  8    -> Study 1 =  40 runs =  383.1 GPU-h
         n for eps = 1.000 sigma (5.0 pts): 13    -> Study 1 =  65 runs =  622.6 GPU-h
         n for eps = 0.600 sigma (3.0 pts): 35    -> Study 1 = 175 runs = 1676.2 GPU-h
```

**So the price of being able to say "the gate contributes less than 3 accuracy points" is 1,676 GPU-h in Study 1 alone, roughly 4.4x the powered screen, and it is not bought here.** The design below buys a decisive verdict on the BOUND (H1, C1) and buys only an inconclusive-or-refuted verdict on the GATE (H3, C5) unless the gate effect happens to exceed 1.584 sigma. That asymmetry is the honest state of this experiment and it is stated here, at the top, rather than in §10.

---

## 0. Why this document exists

`logos/GAPS.md` §5 orders F9 first in the entire programme. `logos/LOGOS_HARNESS.md` states the experiment as an ORDERING and supplies no sample size, no seeds, no effect size, no test statistic, no alpha and no stopping rule. `logos/ARCHITECTURE_REVIEW.md`, the repository's own self-review, contains no finding about F9's design at all: its fifteen findings are entirely about the Mixture-of-Towers architecture. F9 has had no referee pass before this one, and it is the P0 experiment on which the whole ledger is ordered.

---

## 1. Hypotheses

| | Claim | H0 |
|---|---|---|
| **H1** (the bound) | Environment-adjudicated grounded trajectories install held-out semantics that text cannot supply: g_A3 > g_A1 and g_A4 > g_A0. | equality |
| **H2** (the ordering) | The monotone ordering of `logos.tex` §12 holds: g_A0 <= g_A1 <= g_A2 <= g_A3, at least one strict. | equality throughout |
| **H3** (the Tier-C claim) | The disagreement gate contributes over and above grounding: g_A3 > g_A4. This is the claim `logos.tex` §12 and `LOGOS_HARNESS.md` §1.1 both flag as "the claim we would most like tested". A4 is what makes it identifiable (§2). | equality |
| **H4** (the admission rule) | Yield-weighted accumulating admission prevents degeneration: the collapse monitor fires on A1 and not on A3. | fires on both or neither |

All tests one-sided in the direction the paper predicts. A reversal is reported as a reversal, never as a two-sided pass.

---

## 2. Arms [FROZEN]: FIVE, not four

`logos.tex` §12's ordering names four arms. "Disagreement-gated self-play" is never operationally defined anywhere in `logos.tex` or `logos/*.md`; a grep for the phrase returns only the ordering sentences themselves. This section supplies the missing definition and one missing cell.

The four arms of the paper's ordering, as a 2x2 factorial on (disagreement gate) x (environment adjudication) plus a no-trajectory control:

| Arm | Gate | Environment | Trajectory source |
|---|---|---|---|
| **A0** "nothing" | | | none; the trajectory budget is spent on additional text |
| **A1** unfiltered self-play | OFF | OFF | proposals kept regardless of divergence; outcome is the ensemble's own majority prediction, never the emulator |
| **A2** disagreement-gated self-play | ON | OFF | kept only above tau_JS; outcome is still the ensemble's own majority prediction |
| **A3** grounded (the advocated configuration) | ON | ON | kept above tau_JS; outcome is the emulator's |

**Plus one arm the four-arm design cannot do without:**

| **A4** ungated grounded | OFF | ON | kept regardless of divergence; outcome is the emulator's |

**A4 is not optional, and it is now mandatory for two independent reasons.**

**Reason 1, identification.** Without A4, A3 minus A2 estimates the adjudication effect with the gate ON, and A2 minus A1 estimates the gate effect with the environment OFF. The gate effect UNDER grounding, which is the only configuration the architecture advocates and the entire subject of H3, is unidentified. The paper's own flagged contribution cannot be isolated by the experiment built to test it.

**Reason 2, scoring [NEW, round-2 finding X-12].** `LOGOS_HARNESS.md` §2.1 now mandates an ungated scoring arm wherever the harness produces a number that will be compared against an external baseline. The gate conditions the retained sample on predictor disagreement, disagreement correlates with item difficulty, and the bias direction is neither known in advance nor estimable from the subsample. **Any statistic computed on gated output is a statistic on a difficulty-biased subsample.** Brier scores, skill scores, hold rates against persistence or climatology or a market or a superforecaster panel are population statistics over a full pre-registered question set, so feeding them a disagreement-conditioned subsample does not make them harder or easier, it makes them uninterpretable. The rule is: **gate for what you train on, do not gate for what you report.** A4 is the arm every external-baseline comparison runs in, including the Substrate-B validity probe of §12 if that probe is ever scored against an external baseline.

**Consequences of five arms, carried through this document:**

| Where | Effect |
|---|---|
| §7 STEP 1, Jonckheere-Terpstra | **A4 is EXCLUDED from the trend test.** The monotone alternative of `logos.tex` §12 is over A0 <= A1 <= A2 <= A3 only. A4 is off the chain by construction: it is grounded but ungated, so the paper predicts it between A1 and A3 with no committed position relative to A2. The JT test stays k = 4, and including A4 would test an ordering the paper never asserted |
| §7 STEP 2, contrasts | five contrasts C1 to C5, so the planning multiplicity constant is **alpha/5, not alpha/3** (§8) |
| §7 blind outlier rule | P(at least one arm corrupted) at a 20% single-seed corruption rate is 1 - 0.8^5 = **0.672** over five arms, not 1 - 0.8^4 = 0.590 |
| §8.1 budget | Study 1 is 5 arms x 8 seeds = **40 runs**, and A4 alone is 8 runs = 8 x 9.579 = **76.6 GPU-h** at the corrected 125M throughput (the old figure of 33 GPU-h was planned off the withdrawn throughput) |

---

## 3. Primary endpoint [FROZEN]

**g = p_heldout minus p_control**, a per-run scalar, difference-in-differences on the behavioural probe of `LOGOS_HARNESS.md` §3.3.

- **Battery.** 10,000 held-out items and 10,000 control items, enumerated from the Generation-I type chart under the constraint that **exactly one of the four offered moves is super-effective**, so chance is exactly 0.25 in both conditions by construction. RNG seed 20260725, written to `logos-harness/eval/battery_v1.jsonl`, SHA-256 in §11.
- **Presentation.** A battle-screen observation as RQ-VAE codes plus the trace-schema prefix of `LOGOS_HARNESS.md` §5.3, truncated at `action:`. Under the resolved tokenizer geometry (`LOGOS_HARNESS.md` §3.2: 10x9 = 90 spatial positions, 3 residual levels, **collapsed to one LM position per spatial position**) the observation prefix is **90 codes, not 270**, so a probe item is about 90 + 40 = 130 tokens and the whole 20,000-item battery is one packed pass per checkpoint. Scoring cost is derived in §8.1.
- **Scoring.** Deterministic argmax over the four legal `select_move` continuations by length-normalised total log-probability. No sampling, so decode noise is exactly zero.
- **Checkpoint.** Final checkpoint only. Intermediate checkpoints are diagnostics.

Chosen primary over the grounding probe because it measures capability, and the bound is a claim about capability, not representation; because the internal control absorbs arm-level general-competence differences, which is what makes a null interpretable; and because its within-run sampling error is nearly free to shrink. At m = 10,000 per condition and p ~ 0.3, sd = sqrt(2 x 0.21 / 10000) = 0.0065, negligible against between-seed sigma. Battery size is free; seeds are the entire constraint.

### 3.1 Corrected held-out and control vocabulary [FROZEN]

**The table earlier drafts of `LOGOS_HARNESS.md` carried was degenerate and could not measure its own endpoint.** Its control moves were `tackle` and `scratch`, both Normal-type, and Generation-I Normal-type moves have no super-effective matchup whatsoever (Bulbapedia Gen-I type chart: 1x against everything except 0.5x versus Rock and 0x versus Ghost). Its only Fire move, `ember`, sat on the held-out side. **The control condition of the primary measurement therefore could not register the quantity being measured**, which destroys exactly the interpretability that file insists on ("The control set is not optional. It is what makes a null result interpretable"). **Status: repaired upstream.** `LOGOS_HARNESS.md` §3.3 now carries the corrected table below and marks it FROZEN against this section, so the two files agree and this section is the register of record.

| Class | HELD OUT (scrubbed from the entire text stream) | CONTROL (kept in text) |
|---|---|---|
| Types | `water`, `rock`, `grass`, `electric`, `ground` | `fire`, `normal`, **`bug`**, **`ice`** |
| Moves | `water_gun`, `thunder_shock`, `vine_whip`, `flamethrower` | **`ember`**, `tackle`, `scratch` |
| Phrases | `super effective`, `not very effective` | held out in BOTH conditions, so the verbal-readout channel stays matched |

Generation-I Fire is 2x against Bug, Grass and Ice. Grass is held out; Bug and Ice are kept; `ember` is kept. So `ember` against a Bug-type or Ice-type defender is a **valid text-supported super-effective control item**, which the original table had none of. `flamethrower` replaces `ember` on the held-out side so a Fire held-out item still exists.

**Scrubbing is by exact tokenized set membership, never by regex and never by substring containment** (`LOGOS_HARNESS.md` §3.3, "The leak filter"). NFKC plus casefold, split on UAX #29 word boundaries and additionally on `_` and `-`, then n-gram tuple membership in a hash set over the banned unigrams, bigrams (`("water","gun")`, `("super","effective")`) and the trigram `("not","very","effective")`. Substring matching would silently scrub `ember` out of `remember`, `ice` out of `service` and `bug` out of `debug`, which removes the control set, which is the one thing that makes a null interpretable. The filter scans three surfaces (raw corpus, detokenized output of the trained subword tokenizer, and the mined vocabulary itself) and **fails closed**: if the tokenizer or `heldout_vocab.yaml` will not load it refuses the run rather than falling back to a weaker matcher. Verified by the Phase-2 leak validator (`LOGOS_HARNESS.md` §7), with the leak count and the per-control-term occurrence counts recorded in §11. **A non-zero leak count voids the run, and so does any control term occurring fewer than 1,000 times in the final text stream:** a control term that never appears is not a control.

### 3.2 What the primary endpoint can and cannot do, stated in advance

Held-out semantics are unavailable to A0, A1 and A2 **by construction**: the terms are scrubbed from all text and only A3 and A4 touch the environment. g is therefore expected at ~0 for all three, and the primary endpoint reads exactly one bit, grounding versus no grounding. **The four-arm ordering of `logos.tex` §12 is not measurable on any single endpoint**, because the arms differ on two orthogonal dimensions and g reads one. The gate contrasts are carried by the secondaries. A flat primary across A0, A1 and A2 is the PREDICTED pattern and may not be written up as "the ordering partially held".

---

## 4. Secondary endpoints [FROZEN]

Holm-corrected within the secondary family, evaluated only if the primary gate (§7 STEP 2, contrast C1) passes. Supportive, never confirmatory.

- **S1 grounding probe.** Fraction of held-out terms whose top-5 nearest observation codes by cosine come from frames containing that type or move (`LOGOS_HARNESS.md` §3.3), versus the same fraction for control terms, against a 1,000-draw permutation null over code assignment. Not primary: the held-out set is ~11 terms, a hard resolution ceiling, and cosine nearest-neighbour reads representation rather than behaviour. Note the code space is the collapsed one: 90 composite per-position codes per frame, so a "nearest observation code" is a per-position composite, not one of 270 residual-level codes.
- **S2 collapse monitor.** §6.
- **S3 mean admitted yield per arm** (`yield(tau) = -log P_M(o_observed | context, action)`, `LOGOS_HARNESS.md` §2). Manipulation check that the gate did what the loop claims. **If mean admitted yield in A3 does not exceed A1, the loop did not run as specified and the run is VOID, not negative.**
- **S4 proposer diversity.** Mean pairwise Jensen-Shannon divergence between the two proposer models' predictive distributions on a frozen 5,000-item probe set, measured and recorded **before any training arm runs**. **If mean pairwise JS < 0.15 the experiment is VOID**: a null on the gate arms would otherwise be uninterpretable between "the gate does nothing" and "the proposers were not diverse".

  **Provenance of this gate, corrected.** An earlier draft of this section justified S4 by quoting `LOGOS_HARNESS.md` to the effect that "the towers must be informatively different, or the loop is provably worthless". **That sentence has been withdrawn upstream and this document does not inherit it.** The corrected §1 of that file establishes the opposite: Choi et al. (arXiv:2508.17536) extend the debate martingale explicitly to HETEROGENEOUS agents, so informational diversity does not by itself break it, and the two mechanisms that do break it (confidence weighting, better initialisation) are protocol-internal rather than observational. Tower diversity is therefore a **conjecture of the authors** running against the source it was drawn from, it is falsifier F13, and S4 measures it rather than assuming it. The gate's role is unchanged and its justification is now the weaker and correct one: without measured diversity, a null on A2 versus A1 is uninterpretable. What S4 does **not** do is license the claim that diversity is what makes the loop work; F13 limb (a) tests that and F13 limb (b) is costed in §8.2.

### 4.1 Exploratory: labelled, no inference, no gate

- **VideoGameBench Lite progress.** An earlier draft of `LOGOS_HARNESS.md` made this a Phase-6 GATE. It cannot be one (that file's §7 now carries it as descriptive). VideoGameBench (arXiv:2505.18134): "The best performing models, Gemini 2.5 Pro and Claude 3.7 Sonnet, complete only 0.48% of VideoGameBench and 1.6% of VideoGameBench Lite." A 350M model scores 0 in every arm; zero between-arm variance is zero power, and as a gate it fails Phase 6 for reasons unrelated to the hypothesis. Demoted to descriptive reporting.
- **Validation NLL on a shared natural-text set.** Disqualified as a between-arm capability comparison: each arm trains on a different distribution by construction, so cross-arm NLL confounds distribution distance with capability. Monitor only.
- Anything not named in §3 or §4 is exploratory and must be labelled as such in the write-up.

---

## 5. Matching protocol [FROZEN]

At fixed model, fixed sequence length 2048 and fixed global batch, matched total tokens, matched optimizer steps and matched training FLOPs are the **same experiment**. The apparent four-way ambiguity is a two-way one: total versus unique. The fork exists only because the gate is a filter.

**Label collision, resolved.** The matching protocols are **MP1** and **MP2** throughout. Earlier drafts called them M1 and M2, which collided with the collapse-monitor statistics M1, M2 and M3 of §6 inside a document that has to be sealed and read literally. The collapse statistics keep M1 to M3; the matching protocols are MP1 and MP2; the contrasts are C1 to C5.

**PRIMARY matching MP1: matched total AND unique, achieved by over-generating in the gated arms.**

| Quantity | 125M screen | 350M confirmatory |
|---|---|---|
| Total training tokens T, every arm | 1.0e9 | 2.0e9 |
| Trajectory share phi, arms A1 to A4 (A0: 0) | 0.25 | 0.25 |
| Unique admitted trajectory tokens U = phi x T / 2 | 1.25e8 | 2.5e8 |
| Unique text tokens U_text = T/4 | 2.5e8 | 5.0e8 |
| Text epochs, A0 | **4.0** | **4.0** |
| Text epochs, A1 to A4 | 3.0 | 3.0 |
| Trajectory epochs, A1 to A4 | 2.0 | 2.0 |

A1 to A4 over-generate proposals to reach the identical U. **Generation compute is deliberately not matched** and is reported as a separate per-arm ledger line (proposals generated, admission rate, GPU-h); the claim under test is about training data, not generation cost. The generation ledger is derived in §8.1.

**The epoch sizing is not cosmetic.** `LOGOS_HARNESS.md` §5.4 commits to "<=4 epochs" and warns "Watch for the epoch-5 jump" (Muennighoff, arXiv:2305.16264). At matched total tokens A0 has no trajectory data and spends the whole budget on text at 1/(1 - 0.25) = 1.33x the trajectory arms' epochs. Sizing U_text naively would put A0 at 5.33 epochs, inside the degradation regime the spec itself flags, and the "nothing" arm would then lose for a reason with nothing to do with grounding. U_text = T/4 pins A0 at exactly 4.0.

### 5.1 Sequence, packing and observation-fraction arithmetic [FROZEN, recomputed against the resolved tokenizer]

The observation tokenizer decision is no longer deferred. `LOGOS_HARNESS.md` §3.2 freezes **90 spatial positions per frame, 3 residual levels, collapsed to one LM position per spatial position: 90 tokens per frame, not 270.** A Substrate-A trace carries two frames (observation and result), so **180 loss-masked observation tokens per trace**. Collapse is free because the loss is masked on observation codes, so a composite per-position token is never a prediction target and needs an input embedding only, formed as the sum of the 3 projected residual-level codebook vectors.

Everything downstream of sequence length in this document is recomputed against 90, not 270:

| Quantity | Old flatten assumption (270/frame) | **FROZEN, collapsed (90/frame)** |
|---|---|---|
| Loss-masked observation tokens per trace | 540 | **180** |
| Loss-bearing tokens per trace (proposals, thought, action, mandatory `outcome`) | ~130 | **~130** |
| Trace length | ~670 | **~310** |
| Traces per 2048-token packed sequence | 3 | **6** (2048/310 = 6.61, floored to 6 under FlexAttention document boundaries) |
| Observation-code share of the training stream at phi = 0.25 | 20.1% | **14.5%** (0.25 x 180/310) |
| Loss-bearing trajectory share of the training stream | 4.9% | **10.5%** (0.25 x 130/310) |
| Traces needed for U = 1.25e8 (125M) | 186,567 | **403,226** |
| Traces needed for U = 2.5e8 (350M) | 373,134 | **806,452** |

The observation stream at 14.5% sits inside `LOGOS_HARNESS.md` §5.4's 15 to 30% cap rather than at its ceiling, which is what makes the 20 to 30% text-replay mandate satisfiable at phi = 0.25 without pushing anything out.

**Dilution, restated in advance and corrected.** At phi = 0.25 the arms are identical over 75% of their training tokens, so all effect sizes here are per-TOTAL-token and the per-differentiating-token effect is larger by a factor that depends on which denominator is meant:

```
python3: per trajectory token              1/0.25            =  4.0x
         per LOSS-BEARING trajectory token 310/(0.25*130)    =  9.5x
         (under the withdrawn flatten geometry it would have been 670/(0.25*130) = 20.6x)
```

**Neither the 4.0x nor the 9.5x figure may be quoted as if it were the headline.** The headline is per-total-token. The collapse decision roughly doubles the differentiating signal per training token at fixed phi (10.5% loss-bearing against 4.9%), which is a real gain in effective power at zero cost, and it is the reason the 9.5x rescaling is smaller than it would have been. It does not change the primary endpoint, the frozen effect size, or any threshold in §8.

**Cost of the collapse decision, disclosed.** The observation-loss ablation switch (`LOGOS_HARNESS.md` §5.2) is unavailable under collapse without a factorised head of 3 sub-softmaxes over 1,024 codes each. If that ablation is ever run it must either build that head or run on the flattened 270-per-frame variant, and in the latter case it is a **different sequence-length regime**, not a clean ablation, and is exploratory under §4.1. It is not budgeted in §8.1.

### 5.2 Secondary matching MP2 [FROZEN]

**MP2, reported alongside MP1:** matched GENERATION budget, that is, identical proposal count in all arms, which forces the gated arms to fewer unique tokens and more repetition. MP2 is the question an operator faces; MP1 is the question the paper asks. MP2 would show the gate losing on any diversity-sensitive endpoint purely because a q = 0.25 gate quarters unique data, which is a result about repetition, not grounding. Registered because **a positive under MP2 is strictly stronger than a positive under MP1**.

**MP2 costs training runs and is priced here rather than left as an unfunded registration.** Under MP2 the ungated arms are unchanged: A0 has no trajectories, and A1 and A4 admit every proposal, so matched generation and matched admission coincide and their MP1 corpora are reused verbatim. **Only A2 and A3 change**, because only they discard 75% of proposals. So MP2 is 2 arms x 8 seeds = 16 additional 125M runs and no additional generation (it uses fewer proposals than MP1, not more).

```
python3: 16 * 9.579 = 153.3 GPU-h
```

**MP2 is registered and is NOT in the §8.1 core total.** It is priced as a §8.3 contingent rung, run only if MP1's C1 passes, because an MP2 replication of a null is not informative. Earlier drafts registered MP2 with no line item at all, which is the failure mode this document exists to prevent.

---

## 6. The collapse monitor, specified [FROZEN rule, CALIBRATED thresholds]

`LOGOS_HARNESS.md` §6 names `collapse_monitor.py` and never specifies it. This section is the specification.

**Probe set P:** 2,000 sequences of 2,048 tokens of natural text from the same source as the training text, disjoint from all training data, frozen at Phase 3, SHA-256 in §11. All statistics teacher-forced, so decoding temperature cannot confound anything.

| | Statistic | Direction under collapse |
|---|---|---|
| **M1** | tail NLL: mean of -log p(target given context) over probe positions whose target is in the bottom decile of the training-text unigram frequency distribution AND occurs >= 100 times (excludes hapax noise) | rises |
| **M2** | predictive entropy: mean over all probe positions of -sum_v p_v log p_v | falls |
| **M3** | representational effective dimension: participation ratio (sum lambda)^2 / sum(lambda^2) of the final-layer hidden-state covariance eigenspectrum over the 2,000 last positions | falls |

All three are required because each fails alone. Mean perplexity is head-dominated and can improve while tails are lost, and collapse is a tail phenomenon (Shumailov et al., *Nature* 631:755-759, 2024). Generated-text n-gram entropy is confounded by decoding temperature, which teacher-forcing removes. Representation dimension alone can move with no distributional consequence. M3 reuses the variance-ratio effective dimension the repository already uses at `validation/reddit_wsb/neff_collapse_wsb.py` and that `GAPS.md` §2 names for falsifier F5, so **F5 becomes a genuine free by-product rather than a promissory one**, at 0 marginal GPU-h.

**Baseline:** arm A0 at the SAME optimizer step, matched on seed index. An absolute entropy threshold is meaningless without a reference.

**Calibration [CALIBRATED, rule frozen now]:** run A0's 8 seeds first; compute s(M1), s(M2), s(M3), the across-seed standard deviation of each statistic at each checkpoint. Thresholds are 3 x s. The numeric thresholds are frozen at the end of calibration and **before any experimental arm is evaluated**, and recorded in §11. This mirrors the shuffle-null quantile rule of `validation/neff_v4/PRE_REGISTRATION_neff_v4.md` §1.

**FIRE RULE [FROZEN].** Arm a fires at checkpoint t if and only if, against A0 matched on seed index and step t:

> Delta_M1 >= 3 s(M1) **AND** ( Delta_M2 <= -3 s(M2) **OR** Delta_M3 / M3_A0 <= -3 s(M3) / M3_A0 )

holding at **two consecutive** checkpoints of the frozen grid {25, 50, 75, 100}% of steps.

**CONSEQUENCE TABLE [FROZEN].** An earlier draft of `LOGOS_HARNESS.md` stated "If the monitor fires, the mechanism is refuted" with no arm qualifier, and made "no tail narrowing" a BLOCKING Phase-5 gate. Both were wrong and both contradicted the paper, whose F9 row in `logos.tex` §15 correctly says "the collapse monitor firing **on the grounded arm**". Firing on A1 is PREDICTED by the two sources the spec itself cites (Zenil arXiv:2601.05280; Shumailov, *Nature* 631), so as written the spec would have refuted the mechanism on its own predicted result and halted the experiment on a prediction coming true. **Status: repaired upstream.** `LOGOS_HARNESS.md` §7 phase 5 now carries the monitor as a reported diagnostic rather than a blocking gate, and its §8 risks table now arm-qualifies the consequence. The table below is the frozen rule and is the register of record.

| Fires on | Consequence |
|---|---|
| A1 (and not A3) | **Predicted.** Confirms monitor sensitivity. Refutes nothing. |
| A3 (grounded) | **Refutes H4**, the admission rule, the third of the paper's three original claims. Named as an F9 falsification condition in `logos.tex` §15. |
| A2 but not A1 | Anomalous. Report; do not adjudicate. |
| No arm, including A1 | **The monitor is insensitive at this budget. All collapse conclusions from F9 are VOID.** |

The last row is the most likely single outcome and is why §8.1 splits out a multi-round sub-study (Study 2).

**Study 2's round budget, corrected [FROZEN].** `LOGOS_HARNESS.md` §2 step 7 says "retrain incrementally, repeat", and §7 of this document sets R = 5 for Study 2. An earlier draft of §8.1 costed each round as a **full 1.0e9-token training run**, which is wrong on the design's own terms in two ways, and both would have invalidated Study 2 rather than merely overcharging for it:

1. **It breaks the epoch cap.** Five full rounds is 5.0e9 total tokens against U_text = 2.5e8 unique text tokens, which is 20 text epochs, five times the <=4-epoch cap of §5 and far past the epoch-5 jump the spec flags.
2. **It breaks this section's own baseline.** The fire rule compares arm a against **A0 at the same optimizer step**. A0 runs at R = 1. If a round were a full run, A1 and A3 would have five times A0's steps and the matched-step baseline would be undefined beyond 20% of their trajectory.

**Frozen:** Study 2 holds total tokens per seed at 1.0e9, identical to Study 1, and partitions that budget into R = 5 sequential segments of 2.0e8 tokens with the corpus accumulating (never rotating) between segments. Checkpoints for the fire rule remain the frozen grid {25, 50, 75, 100}% of steps, which now straddles round boundaries at 1.25, 2.5, 3.75 and 5 rounds. A0 trains the same 1.0e9 tokens at R = 1, so the matched-step baseline is defined everywhere. Study 2 is therefore 3 arms x 3 seeds = **9 training runs, not 33**, and the cost falls from a mis-derived 316.1 GPU-h to 86.2 (§8.1). The trajectory-generation cost does not fall, because a multi-round corpus is model-dependent and every seed must generate its own (§8.1 generation ledger).

---

## 7. Analysis plan and multiplicity [FROZEN]

Hierarchical fixed-sequence gatekeeping. Executed exactly ONCE by `logos-harness/analysis/analyze_f9.py`.

**STEP 1, the gate.** Exact **Jonckheere-Terpstra** trend test on the ordered alternative g_A0 <= g_A1 <= g_A2 <= g_A3 over seed-level values, one-sided alpha = 0.05, **exact permutation null, not the normal approximation**. If STEP 1 fails, **H2 fails outright**: no pairwise testing, no subgroup, no rescue.

**A4 is excluded from STEP 1 [FROZEN].** The trend test is over k = 4 groups, not 5. The monotone alternative is the one `logos.tex` §12 actually asserts, and it does not place A4: A4 is grounded but ungated, so the paper predicts it above A1 and does not commit to its position relative to A2 or A3. Including it would test an ordering nobody claimed and would spend power on a hypothesis with no source. A4 enters only through the STEP-2 contrasts C4 and C5, and through its §2 Reason-2 role as the arm any external-baseline comparison is scored in.

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

**The multiplicity correction, corrected for five arms [FROZEN].** The STEP-2 family is **five** contrasts, not three. Holm at family alpha = 0.05 tests the smallest p-value at alpha/5 = 0.01, and only that first step is at alpha/5; subsequent steps relax. Power planning must nevertheless be done at the **worst-case first step**, so the planning constant in §8 is `z_{1-0.05/5} + z_{0.80}`, not `z_{1-0.05/3} + z_{0.80}`:

```
python3: z_{1-0.05/3} = 2.1280 ; z_{1-0.05/5} = 2.3263 ; z_{0.80} = 0.8416
         3-contrast planning constant = 2.9697   (what earlier drafts used)
         5-contrast planning constant = 3.1680   (FROZEN)
         MDE at n = 8: sigma*sqrt(2/8)*3.1680 = 1.584 sigma = 0.0792 at sigma = 0.05
                        (was quoted as 1.485 sigma = 0.0742)
```

**This raises the pre-declared MDE from 0.074 to 0.0792 accuracy points and no threshold is relaxed to compensate.** The frozen effect size worth detecting stays delta = 0.15, which is 1.89x the corrected MDE, so the design still detects it at above 80% power. Holm is uniformly more powerful than Bonferroni, so planning at alpha/5 is conservative and the realised power is at least this.

**TOST alpha is NOT multiplicity-corrected, and that is disclosed rather than hidden.** The equivalence procedure below runs at alpha = 0.05 per contrast. Correcting it would widen every equivalence margin and make a declared negative easier to reach, which is the wrong direction for a document whose deliverable is a negative. The consequence is that the family-wise rate for *falsely declaring equivalence* is above 0.05 across five contrasts, and any K1 or K3 verdict is reported with that stated.

**Equivalence testing [FROZEN].** Any contrast that fails superiority is submitted to a **TOST** at alpha = 0.05 with margin **eps = 1.243 x sigma_hat**, sigma_hat being the pooled across-seed standard deviation of g. At n = 8 that is the margin the design supports at 80% power. A contrast that fails superiority AND fails TOST is reported **INCONCLUSIVE**, never as "no difference".

**Blind outlier rule [FROZEN].** Any run whose training-loss curve contains a spike exceeding 3x the trailing-100-step median absolute deviation of the loss is excluded and replaced by a fresh seed. **Detection is from the loss curve alone, before any endpoint is computed.** Grounded in PolyPythias (arXiv:2503.09543): 2 of 10 seeds at 410M show loss spikes with notably worse downstream performance. Replacement reserve: 20% of runs. At n = 8 this drops P(at least one of five arms corrupted) from 0.672 to 0.051.

**Free parameters, frozen here because they set each arm's corpus:**

| Parameter | Spec status | Frozen value |
|---|---|---|
| tau_JS, the disagreement gate | `LOGOS_HARNESS.md` §2 said "Below threshold, discard" and gave no value | **[CALIBRATED]** the value admitting exactly **q = 0.25** of proposals on a 50,000-proposal calibration pool generated **before any training arm runs**. A quantile, not a magic number, mirroring `neff_v4`'s 90th-percentile shuffle rule. Now adopted upstream in `LOGOS_HARNESS.md` §2 |
| yield weighting | `LOGOS_HARNESS.md` §2 said "Admit weighted by yield" and gave no function | w(tau) = clip(yield(tau), 0, 10), normalised to mean 1 within each round. Now adopted upstream |
| bootstrap rounds | `LOGOS_HARNESS.md` §2 said only "repeat" | R = 1 for Study 1, R = 5 for Study 2, **with Study 2's five rounds inside the same 1.0e9-token budget** (§6), not five full runs |

---

## 8. Sample size, power and cost [FROZEN]

**Planning sigma** (across-seed standard deviation of g, in accuracy points): **0.05** after blind outlier exclusion, **0.09** if outliers are retained. Anchors: MultiBERTs (arXiv:2106.16163) r spans 0.1 to 0.7 across 25 pre-training seeds; PolyPythias (arXiv:2503.09543) 2 of 10 outlier seeds at 410M with inter-seed downstream Cohen's kappa converging to ~0.5.

**Effect size worth detecting: delta = 0.15** accuracy points (chance 0.25 to 0.40). Justified by the spec's own rhetoric (`LOGOS_HARNESS.md` §9): the substrate is "the easiest imaginable grounding substrate, where the exact semantics under test are printed on screen in four colours at 160x144". A lift under 15 points there does not support "observation bandwidth is the binding constraint"; it supports "grounding barely works". **This threshold is not relaxed anywhere in this revision.**

**Power table [FROZEN, five contrasts].** Superiority MDE = sigma x sqrt(2/n) x (z_{1-0.05/5} + z_{0.80}) = sigma x sqrt(2/n) x 3.1680. TOST margin at 80% power = sigma x sqrt(2 x (z_{0.95} + z_{0.80})^2 / n) = sigma x sqrt(12.365/n).

| n | MDE / sigma, 3 contrasts (superseded) | **MDE / sigma, 5 contrasts** | **MDE at sigma = 0.05** | TOST eps / sigma | eps at sigma = 0.05 | JT exact p_min, k=4, perfect separation |
|---|---|---|---|---|---|---|
| 1 | undefined | undefined | undefined | undefined | undefined | undefined |
| 2 | 2.970 | 3.168 | 0.158 | 2.486 | 0.124 | 3.97e-4 |
| 3 | 2.425 | 2.587 | 0.129 | 2.030 | 0.102 | 2.71e-6 |
| 5 | 1.878 | 2.004 | 0.100 | 1.573 | 0.079 | 8.52e-11 |
| **8** | 1.485 | **1.584** | **0.0792** | **1.243** | **0.062** | 1.00e-17 |
| 16 | 1.050 | 1.120 | 0.056 | 0.879 | 0.044 | |

**n = 8 is still the knee, and the fifth arm costs 0.099 sigma of MDE.** Correcting the multiplicity constant from three contrasts to five moves the n = 8 MDE from 1.485 to 1.584 sigma, which at the planning sigma is 0.0742 to 0.0792 accuracy points. That is 53% of the frozen delta = 0.15, so the design retains above 80% power on the effect it exists to detect. n = 16 buys 1.584 to 1.120 sigma for double the training cost; n = 5 degrades to 2.004 and n = 3 to 2.587. n = 8 is also the smallest n at which the equivalence margin, 1.243 sigma or about 6.2 accuracy points, is tight enough that a declared negative is worth reporting.

**What n = 8 does NOT buy, quantified.** The equivalence margin is the binding constraint on K3, and it shrinks only as sqrt(n):

```
python3: n = 12.365/(eps/sigma)^2
         eps = 1.243 sigma =  6.2 acc pts -> n =  8  -> Study 1 =  40 runs =  383.1 GPU-h
         eps = 1.000 sigma =  5.0 acc pts -> n = 13  -> Study 1 =  65 runs =  622.6 GPU-h
         eps = 0.800 sigma =  4.0 acc pts -> n = 20  -> Study 1 = 100 runs =  957.9 GPU-h
         eps = 0.600 sigma =  3.0 acc pts -> n = 35  -> Study 1 = 175 runs = 1676.2 GPU-h
```

A gate effect of 3 accuracy points under grounding is entirely plausible and would land INCONCLUSIVE at n = 8: neither significant (needs 1.584 sigma = 7.9 pts) nor equivalent (needs the estimate inside 6.2 pts with the interval clearing it). **The dead zone between 6.2 and 7.9 accuracy points is where H3 most likely lives, and this design does not resolve it.** Buying a 3-point verdict costs 1,676 GPU-h in Study 1 alone. It is not bought, and §10 K3 says so.

### 8.1 Studies and budget [FROZEN, re-derived against the corrected throughput]

**Every figure in this table was recomputed from the corrected throughput of `LOGOS_HARNESS.md` §5.4. None was scaled from the previous total of 718 GPU-h.**

**Step 1: the unit costs.**

```
python3: 125M, T=1.0e9 @ 29.0k tok/s : 1.0e9/2.90e4/3600 =  9.579 GPU-h per run
         350M, T=2.0e9 @  9.1k tok/s : 2.0e9/9.10e3/3600 = 61.050 GPU-h per run
         ratio 61.050/9.579 = 6.37, which is why the seeds are bought at 125M
```

**Step 2: the trajectory-generation ledger, derived rather than asserted.** Proposals are generated by the two 350M-class stand-in towers. Forward-only inference costs about one third of the forward-plus-backward FLOPs per token, so the effective proposal throughput is 3 x 9.1k = 27.3k tok/s. Each proposal costs 2 towers x (about 400 tokens of observation-plus-context prefill, plus about 80 generated tokens of prediction, action and reasoning) = 960 tokens processed. Gated arms (A2, A3) over-generate by 1/q = 4x to reach the same admitted U; ungated arms (A1, A4) do not. Under §5.1, a trace is 310 tokens.

```
python3: traces for U=1.25e8 (125M) = 1.25e8/310 = 403,226   ; for U=2.5e8 (350M) = 806,452
         ungated arm, 125M: 403226      * 960 / 2.73e4 / 3600 =  3.94 GPU-h
         gated   arm, 125M: 403226/0.25 * 960 / 2.73e4 / 3600 = 15.75 GPU-h
         ungated arm, 350M: 806452      * 960 / 2.73e4 / 3600 =  7.88 GPU-h
         gated   arm, 350M: 806452/0.25 * 960 / 2.73e4 / 3600 = 31.51 GPU-h
         Study 1 (A1,A4 ungated + A2,A3 gated; ONE corpus per arm, shared across the 8 seeds
                  so that the 8 seeds estimate TRAINING-seed variance with data held fixed):
                  2*3.94 + 2*15.75 = 39.4 GPU-h
         Study 2 (A1,A3, R=5 accumulating rounds; the corpus is model-dependent across rounds
                  so EACH SEED must generate its own): 3*(3.94+15.75) = 59.1 GPU-h
         Study 3 (A1 ungated + A3 gated at 350M):     7.88+31.51      = 39.4 GPU-h
         TOTAL GENERATION = 137.9 GPU-h
```

Only admitted proposals are acted on, so the emulator is stepped 403,226 times per grounded 125M arm and not 1.6M times; PyBoy stepping is CPU-bound and contributes zero GPU-hours.

**Step 3: evaluation.**

```
python3: battery scoring: 20000 items * 4 continuations * ~300 tok = 2.40e7 tok, forward-only
         collapse probe P: 2000 * 2048 * 4 checkpoints              = 1.64e7 tok, teacher-forced
         per run at 125M: (2.40e7+1.64e7)/(3*2.90e4)/3600 = 0.129 GPU-h
         per run at 350M: (2.40e7+1.64e7)/(3*9.10e3)/3600 = 0.411 GPU-h
         (49 * 1.2)*0.129 + (9 * 1.2)*0.411 = 12.0 GPU-h        # 1.2 covers the replacement reserve
```

**Step 4: the budget.**

| Line | Model / tokens | Arms | Seeds | Rounds | Runs | GPU-h |
|---|---|---|---|---|---|---|
| **Study 1, ordering (primary)** | 125M / 1.0e9 | A0 to A4 | 8 | 1 | 40 | **383.1** |
| **Study 2, collapse (S2)** | 125M / 1.0e9 | A0, A1, A3 | 3 | 5 within the same 1.0e9 (A0: 1) | 9 | **86.2** |
| **Study 3, confirmatory scale** | 350M / 2.0e9 | A0, A1, A3 | 3 | 1 | 9 | **549.5** |
| Outlier replacement reserve, 20% of training | | | | | ~12 | 203.8 |
| Trajectory generation, all arms, all studies | | | | | | 137.9 |
| tau_JS calibration pool (50k proposals) plus S4 diversity | | | | | | 0.5 |
| RQ-VAE training plus frame tokenization | | | | | | 15.0 |
| Eval batteries, grounding and collapse probes | | | | | | 12.0 |
| **F13 limb (b), confidence-weighted aggregation (§8.2)** | | | | | | **12.7** |
| Day-one throughput and memory probe | | | | | | 2.0 |
| **TOTAL** | | | | | | **1,402.6, call it ~1,400** |

```
python3: 383.1+86.2+549.5+203.8+137.9+0.5+15.0+12.0+12.7+2.0 = 1402.6
```

**What moved, and why, line by line.**

| Line | Was | Now | Cause |
|---|---|---|---|
| Study 1 | 164 | 383.1 | throughput correction only (40 runs x 9.579 against 40 x 4.12) |
| Study 2 | 135 | 86.2 | throughput correction (+2.32x) AND the round-accounting correction of §6 (33 runs to 9), which is a **reduction** because the old accounting silently ran 5.0e9 tokens per seed and broke the epoch cap |
| Study 3 | 208 | 549.5 | throughput correction only (9 x 61.05 against 9 x 23.15). **This is now the largest single line in the budget and it buys n = 3, which supports no test statistic** |
| Reserve | 101 | 203.8 | 20% of the corrected training cost |
| Generation | 75 | 137.9 | derived here for the first time; the old 75 was an unshown estimate |
| Eval | 20 | 12.0 | derived here; the collapsed 90-tokens-per-frame geometry makes battery items about 130 tokens instead of about 310 |
| F13 limb (b) | absent | 12.7 | §8.2. `logos.tex` §15 scopes F13 as "an arm of F9" and the old budget could not pay for it |
| tau_JS pool, day-one probe | absent | 2.5 | both are mandated elsewhere in this document and neither had a line |

**The 125M screen is what makes this affordable, and it is the whole lever.** `LOGOS_HARNESS.md` §5.1 now inverts the spec's original phase order and labels 125M the **powered screen** (n = 8, five arms) and 350M the **confirmatory** replicate (n = 3, three arms). At 125M the entire five-arm n = 8 ordering study is 383.1 GPU-h. The same study at 350M with T = 2.0e9 would be 40 x 61.05 = 2,442 GPU-h, which is 6.4x the whole Study-1 line and 1.7x this entire budget. **Without the inversion the powered design does not fit on one card at any sane electricity bill; with it, the powered part costs less than a third of the total.**

**Cost:** ~1,400 GPU-h. At RTX-3090 community-cloud rates of $0.20 to $0.25 per GPU-h that is **$281 to $351**. On the owned RTX 3090 at 350 W (GA102 whitepaper) and EUR 0.30/kWh it is 1402.6 x 0.350 = **491 kWh, about EUR 147**.

### 8.2 F13 limb (b), costed [FROZEN]

`logos.tex` §15 scopes falsifier **F13** as "One consumer GPU (arm of F9)", and its limb (b) is: *calibrated-confidence weighting alone lifting ensemble accuracy without any environment adjudication, which would locate the gain in the protocol rather than in the observation channel.* That is Zhu et al. (arXiv:2601.19921) Theorem 1, under which confidence positively correlated with correctness turns the debate belief process into a strict submartingale with no diversity and no external observation involved. **The previous version of this budget contained no confidence-weighted aggregation line, so the paper claimed an arm the experiment could not pay for.** That is fixed here rather than deferred.

**What limb (b) actually is.** It is an ENSEMBLE-level comparison on the frozen §3 battery, not a pretraining arm. Two aggregation rules over the same two stand-in towers: unweighted majority (the rule A1 and A2 already use to manufacture their pseudo-outcomes) versus calibrated-confidence weighting. No emulator, no RAM, no adjudicator. The endpoint is ensemble accuracy on the 10,000 held-out and 10,000 control items, paired per item, tested by exact McNemar on the discordant pairs at one-sided alpha = 0.05. Item-level n is 20,000, so this limb is well powered on a budget that is a rounding error against Study 1.

**Cost.**

```
python3: confidence calibration per proposer per seed (GRPO + LoRA r=64 alpha=32, per Zhu et al.):
           rollouts 5000 prompts * 8 samples * 256 tok = 1.024e7 generated tokens
           generation 1.024e7/(3*9.1e3)/3600 = 0.104 h ; policy update 1.024e7/9.1e3/3600 = 0.313 h
           = 0.417 GPU-h
         battery scoring per proposer per seed: 20000*4*300/(3*9.1e3)/3600 = 0.244 GPU-h
         8 calibration seeds x 2 proposers x (0.417+0.244) = 10.6 GPU-h
         +20% slack = 12.7 GPU-h  [BUDGETED]
```

**Design constraints, frozen so a positive is not over-read.**

1. **The calibration supervision is held identical across arms.** Zhu et al. buy calibrated confidence with external supervision (GRPO calibration on a manually curated subset chosen so accuracy sits near 50%), so limb (b) is **not** free of exogenous signal: the exogenous signal has moved into the calibrator rather than left the system. The calibrated proposers are produced ONCE, before any training arm, alongside the tau_JS calibration pool and the S4 diversity measurement, and all of A0 to A4 then use the same calibrated proposers. Its token and GPU-hour cost is a separate ledger line, exactly as generation compute is (§5).
2. **8 calibration seeds, because the calibration is itself a stochastic training procedure.** The aggregation comparison is deterministic given calibrated proposers, so the seed variance that matters is the calibrator's.
3. **Limb (b) is scored in the ungated condition** (§2 Reason 2). Confidence weighting is compared against majority voting on the FULL battery, never on a disagreement-conditioned subsample.

**The training-arm extension is registered and NOT funded here.** "Does a confidence-weighted pseudo-label also install held-out semantics?" would be a sixth arm, A5, identical to A2 except that the pseudo-outcome is confidence-weighted rather than majority-voted. That is 8 x 9.579 = 76.6 GPU-h at 125M. It is a §8.3 contingent rung, triggered only if limb (b) fires at ensemble level, because a null at ensemble level makes the training arm uninformative. **F13 limb (a)**, debate between corpus-disjoint towers tracking the martingale as closely as debate between personas of one model, is NOT in this budget at all and is NOT an F9 arm: it needs models whose pretraining corpora, objectives and alignment histories genuinely differ, and no 350M stand-in trained for this harness supplies that. `logos.tex` §15's "arm of F9" scoping is correct for limb (b) and is **not** correct for limb (a).

**Limb (a) is nevertheless runnable on the same owned card, and an earlier version of this section wrongly implied it was not.** Distinct pretraining lineage is a property of how a model was trained, not of the hardware it runs on, and models with that property already exist: Qwen, Llama, DeepSeek, Mistral and Gemma were pretrained by different organisations on different corpora under different objectives with different alignment histories. That is arguably a **better** instrument for limb (a) than five towers from one lab, which would share data-collection pipelines and filtering decisions and be less independent than they look. The instrument is therefore several existing open-weight models of **different pretraining lineage**, quantized and stepped sequentially on the 24 GB card, with no gradient step anywhere. **Distinct lineage is the treatment variable**: two models from the same lab, or two finetunes of one base checkpoint, do not count as distinct and may not fill a slot. Two things are owed and neither is invented here. First, **the cost is not derived**: sequential inference over a handful of quantized models is cheap relative to every training line in §8.1, but cheap is not a number and this document does not assert one. Second, the **limitation is real**: limb (a) so instrumented tests the diversity claim at the level of independently trained open-weight models rather than at tower scale inside one architecture, and the ensemble under test is not a Mixture-of-Towers. What is genuinely out of reach on this card is the 5 x 2.8T ensemble itself, which is falsifier **F2**, not F13, and the two are not to be conflated.

### 8.3 Contingent rungs, priced now so the choice is not made after seeing data [FROZEN]

| Rung | Trigger | GPU-h |
|---|---|---|
| **MP2 replication** (§5.2), A2 and A3 re-run at matched generation budget | MP1 contrast C1 passes | 16 x 9.579 = **153.3** |
| **A5 confidence-weighted training arm** (§8.2) | F13 limb (b) fires at ensemble level | 8 x 9.579 = **76.6** |
| **Study 3 token reduction**, T from 2.0e9 to 1.0e9 at 350M | the day-one probe measures below 60% of the planning midpoint | **saves 329.7** (549.5 to 274.7, plus its 20% reserve), taking the total to ~1,073 |
| **n = 13 at 125M**, to reach a 5-point equivalence margin | never triggered automatically; a decision to fund it, not a result-dependent one | +239.5 on Study 1 |

**Day-one probe [FROZEN].** The corrected throughput is still arithmetic against a published ceiling, not a measurement: `LOGOS_HARNESS.md` §5.4 says so explicitly, and 9.1k tok/s at 350M assumes an MFU inside a 25% to 35% band. **Before committing, run a forward-backward probe with `torch.cuda.max_memory_allocated` and record measured tokens/s at both sizes in §11.** If measured throughput falls below 60% of the planning midpoint, **reduce T before reducing n**, per the row above. Seeds are the inferential currency; tokens are not. If measured throughput comes in ABOVE the planning midpoint, the surplus is spent on seeds in Study 1, not on tokens, and not on Study 3.

---

## 9. Stopping rule [FROZEN]

1. **No interim analysis on the primary.** g is computed once, on final checkpoints, after all Study-1 runs complete. No peeking, no sequential stopping, no alpha spending.
2. **The only permitted early termination is technical**: a run diverges (loss NaN or inf) or trips the blind outlier rule of §7. It is replaced by a fresh seed from the pre-declared seed list `[1001..1024]`, consumed in order.
3. **Voiding conditions**, checked before any endpoint is computed: (a) S4 proposer diversity < 0.15; (b) S3 mean admitted yield in A3 not exceeding A1; (c) the leak scan finds any held-out term on any of the three surfaces of §3.1, or any control term occurring fewer than 1,000 times; (d) the Phase-1 RQ-VAE reconstruction gate of `LOGOS_HARNESS.md` §7 fails; (e) the Phase-2 trace-terminal-span assertion fails, that is, any trace ends on a loss-masked span, which would give the result frame exactly zero gradient and manufacture a false negative before any GPU ran. Any of these gives **VOID, no directional conclusion**.
4. **Underpowered condition.** If realised sigma_hat makes the realised MDE exceed the pre-declared **0.0792** (§8, five-contrast planning constant at n = 8), the run is reported **UNDERPOWERED**, the realised MDE and TOST margin are published, and no equivalence claim is made. The superseded figure of 0.074 was computed at a three-contrast constant and does not apply to a five-arm design.
5. Study 2 and Study 3 run regardless of Study 1's outcome. A negative Study 1 does not license skipping the collapse and scale checks; those are what distinguish a real negative from a broken harness.

---

## 10. What would kill the programme [FROZEN]

**K1, the bound is refuted.** C1 (A3 versus A1) fails superiority AND TOST declares equivalence at eps = 1.243 sigma_hat. Then grounding buys under about 6.2 accuracy points over pure self-play on the easiest imaginable grounding substrate; the observation channel is not the scarce resource at this scale; `logos.tex` §12 is wrong as stated; its ordering sentence must be struck; and per `LOGOS_HARNESS.md` §7 and §9, "the strategy past the token wall is repetition plus synthesis, the paper's Proposition 2 headroom is all there is, and `logos.tex` should say so."

**K2, the admission rule is refuted.** The collapse monitor fires on A3 under the §6 rule. Already named in the F9 row of `logos.tex` §15. The third of the paper's three original claims falls.

**K3, the Tier-C claim is refuted while the bound survives.** C1 passes but C5 (A3 versus A4) and C2 (A2 versus A1) both fail superiority and both declare TOST equivalence. Then grounding works and the disagreement gate contributes nothing. The claim `logos.tex` §12 calls "the specific contribution" and "the claim we would most like tested" is dead, and the Mixture-of-Towers architecture loses its learning-from-disagreement justification entirely; it must then be defended on update economics alone.

**K3 is the outcome this design is worst powered to detect and the paper cares most about, and the corrected budget does not fix that.** The asymmetry is structural, not a budgeting oversight: K3 is a **conjunction of two equivalence declarations**, and equivalence is the direction that needs more N, not less. At n = 8 the design can declare the gate contributes less than 6.2 accuracy points and cannot declare anything tighter. A true gate effect between 6.2 and 7.9 points is INCONCLUSIVE by construction. Closing that window to 3 points costs 1,676 GPU-h in Study 1 alone against the 383.1 budgeted (§8). **This is disclosed at the top of the document, in §8, and here, rather than discovered afterwards, and it is not repaired by widening eps: widening the margin to make K3 declarable would make a false K3 easier to reach, which is exactly the trade this document refuses.**

**K4, not a result.** Any voiding condition of §9.3, or the underpowered condition of §9.4, or the no-arm-fires row of §6. Reported VOID or UNDERPOWERED. **A non-significant C1 at n < 8 is explicitly NOT K1** and may not be written up as one.

**K5, the gain is in the protocol and not in the observation channel [NEW].** F13 limb (b) (§8.2) fires: calibrated-confidence weighting alone lifts ensemble accuracy on the held-out battery, with no environment adjudication of any kind, by a margin that survives exact McNemar at one-sided alpha = 0.05. Then the submartingale that breaks the debate martingale is protocol-internal, the observation bound is not what limits the loop, and `logos.tex` §12's central claim is located in the wrong place. **Steelman, recorded in advance so a positive is not over-read:** Zhu et al. purchase calibrated confidence with external supervision, so limb (b) firing does not show that exogenous signal is unnecessary, only that it can enter through the calibrator instead of through the environment. K5 therefore refutes the *channel* claim and not the *exogenous signal* claim, and the write-up must say which. If limb (b) fires AND C1 also passes, both are reported; they are not mutually exclusive and neither cancels the other.

No result here is renegotiated after the numbers land. The rule above is the whole verdict.

---

## 11. Seal [FROZEN]

SHA-256 digests, computed and lodged **before the first training run**:

| Artifact | sha256 |
|---|---|
| this file | *(fill at lodge)* |
| `logos-harness/configs/arms.yaml` (A0 to A4, five arms) | *(fill)* |
| `logos-harness/configs/rqvae.yaml` (90 positions, 3 levels, collapsed per position) | *(fill)* |
| calibrated-confidence LoRA adapters, both proposers, 8 seeds (§8.2) | *(fill)* |
| `logos-harness/configs/heldout_vocab.yaml` | *(fill)* |
| `logos-harness/configs/bootstrap.yaml` | *(fill)* |
| `logos-harness/eval/battery_v1.jsonl` | *(fill)* |
| collapse probe set P | *(fill)* |
| seed list `[1001..1024]` | *(fill)* |

**Anchor: an OpenTimestamps `.ots` Bitcoin proof is REQUIRED, not optional, in addition to the git tag and the GitHub push time.**

`validation/PREREGISTRATION_SEAL.md:29-32` concedes that OpenTimestamps "is not installed here" and that no OSF DOI is lodged, and lines 37-44 concede that two prior pre-registrations were authored "in a single working session rather than under an independent prior timestamp". That concession is defensible for retrospective tests over dumps that already existed. **It is not defensible for F9, whose data does not exist yet.** A genuine ex-ante third-party anchor costs nothing here, so accepting the weaker git-only anchor would be a pure unforced loss of evidential value. This is also the correct place to record that `PREREGISTRATION_SEAL.md` names neither `neff_v3` nor `neff_v4` in its scope, so no prior seal covers this document by inheritance.

**Post-calibration addendum**, appended and re-hashed after the calibration pass and before any experimental arm is scored: tau_JS at q = 0.25; s(M1), s(M2), s(M3) from the A0 calibration; **measured 3090 tokens/s at 125M and 350M, and the resulting GPU-hour total recomputed from the measurement rather than from the 71-TFLOPS ceiling**; whether the 60% rule of §8.3 fired and which contingent row it selected; the S4 proposer-diversity value; the leak-scan count and the per-control-term occurrence counts; the measured admission rate at tau_JS.

---

## 12. Honesty rails (carried)

- The design is **underpowered at the budget the repository currently assigns it**, by a factor of 14.6 to 19.5, and that is stated at the top of this document rather than in a footnote (see the banner above §0). The ledger's 72 to 96 GPU-h does not buy one seed per arm; at 350M it buys about a quarter of one.
- The primary endpoint reads **one bit**, grounding versus no grounding. It cannot rank the three ungrounded arms. Stated in §3.2 in advance.
- The paper's own flagged contribution (H3) is the contrast this design is **worst** powered to detect, and **the corrected budget does not fix it**. K3 requires two equivalence declarations, the tightest declarable margin at n = 8 is 6.2 accuracy points, and the price of a 3-point margin is 1,676 GPU-h in Study 1 alone. Stated in the banner, in §8 and in §10 K3, in advance.
- **The throughput figures this pre-registration is costed against are still arithmetic, not measurement.** The original 18k to 30k tok/s at 350M was an interpolation from 4090, A30 and L20 runs that exceeded the RTX 3090's dense BF16 ceiling; `LOGOS_HARNESS.md` §5.4 has replaced it with about 9.1k tok/s at 350M and about 29k at 125M, derived against 71 TFLOPS dense and an assumed 25% to 35% MFU. That is a defensible ceiling-based derivation and it is **not** a first-party 3090 log. The day-one probe of §8.3 is the resolution, the frozen response to a shortfall is to reduce T and never n, and until the probe runs the total in §8.1 carries a **band of roughly 1,200 to 1,800 GPU-h** from the MFU assumption alone.
- **The largest single line in the budget buys no test statistic.** Study 3 at 549.5 GPU-h is 39% of the total and runs at n = 3. It is a scale sanity check, and this document does not pretend otherwise: nothing in §7 tests a hypothesis on Study 3, and a Study-3 disagreement with Study 1 is reported as a scale caveat, never as a refutation.
- **Any number this harness reports against an external baseline is scored in the ungated arm A4, never on gated output** (§2 Reason 2, round-2 finding X-12). This binds Substrate B in particular: a Brier score, skill score or hold rate against persistence, climatology, a market or a superforecaster panel is a population statistic over a full pre-registered question set, and the disagreement gate selects exactly the difficulty-biased subsample on which such a comparison cannot be scored.
- Substrate B (the psychohistory validation pipeline as adjudicator) is **not** part of this pre-registration's primary or secondary endpoints. An independent count of the sealed rosters gives 83 rows, 68 distinct onset dates, 58 distinct real-world episodes and 35 carrying a committed endogenous/exogenous label, which caps a paired Substrate-B contrast at a minimum detectable effect of about 0.42 sigma before any disagreement gate discards anything. Substrate B is a directional sanity check that can refute and cannot confirm, and a null from it is not evidence of absence.
- If the primary endpoint FAILS, that is a real negative for the observation bound and will be reported as such. The rule above is the whole verdict and will not be renegotiated after the numbers land.

---

## 13. Reproduce

```
py -3.12 logos-harness/train/throughput_probe.py      # day-one measured tok/s, 125M and 350M (§8.3)
py -3.12 logos-harness/eval/battery_build.py          # frozen probe battery + sha256
py -3.12 logos-harness/eval/proposer_diversity.py     # S4 gate, BEFORE any training
py -3.12 logos-harness/bootstrap/calibrate_confidence.py --seed {1001..1008}  # §8.2, BEFORE any arm
py -3.12 logos-harness/bootstrap/calibrate_gate.py    # tau_JS at q=0.25, BEFORE any training
py -3.12 logos-harness/train/run_arm.py --arm A0 --model 125m --seed {1001..1008}  # calibration arm first
py -3.12 logos-harness/eval/collapse_monitor.py --calibrate            # freeze s(M1..M3)
py -3.12 logos-harness/train/run_arm.py --arm {A1..A4} --model 125m --seed {1001..1008}
py -3.12 logos-harness/train/run_arm.py --arm {A0,A1,A3} --model 125m --rounds 5 --seed {1001..1003}
py -3.12 logos-harness/train/run_arm.py --arm {A0,A1,A3} --model 350m --seed {1001..1003}
py -3.12 logos-harness/analysis/analyze_f13b.py       # F13 limb (b), McNemar, ungated (§8.2)
py -3.12 logos-harness/analysis/analyze_f9.py         # evaluate the frozen rule ONCE
```
