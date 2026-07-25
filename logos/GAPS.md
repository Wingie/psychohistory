# GAPS: what is left to measure

Companion to `../logos.tex`, in the form of the repository's `RUN_AND_CHECK.md`.
**Audit date:** 2026-07-25. **Stance:** adversarial.

---

## 0. Status in one paragraph

The desk work that was open in the previous revision is done: the router design, the cost model, the evaluation metric, the failure semantics, the partition criterion, and the corpus-residency contradiction are all resolved in the paper. **Most of what remains is measurement, and most of it needs accelerators.** **Thirteen** falsifiers now stand in `../logos.tex` §15, which has since minted F11, F12 and F13. Ten of them (F1 to F10) are the rows this ledger tracks, **five** of those on one consumer accelerator (F9, F3, F10, F4, F5), which is four independent runs because F5 falls out of F9 for free. Of the three added since: F11 and F12 need no accelerator at all and are two of the §4 items below; F13's limb (b) is an arm of F9 at 12.7 GPU-h, and its limb (a) is a further Tier-0 rung whose cost is not yet derived (§2).

Three corrections to how earlier revisions of this paragraph read, all from the round-2 audit (§6):

- **"GPU-only, no desk work left" was false and is withdrawn.** §4 below lists five items that need no accelerator at all. Two of them are the measurements on which `ARCHITECTURE_REVIEW.md` F-14 and F-15 remain open: corpus overlap, which settles `../logos.tex` §3.4's "four towers, not five", and the residency fraction, which decides whether Proposition 2 has any headroom left.
- **The `../logos.tex` §15 falsifier table is not the complete list of open work.** The tiered ledger in §2 below carries eight further measurement rows whose ID cell is `:` and which have no F-number in §15: embedding inversion on post-router latents, MXFP4+OAS+MBS versus NVFP4 on a real MoE, QAD versus QAT versus PTQ, the KDA:MLA hybrid with sparse prefix caching, the LatentMoE crossover, routing efficiency eta in practice, tower co-activation as an N_eff analogue, and all-to-all straggler behaviour. Eight measurement rows plus the three §4 items the paper has not numbered is eleven open items outside the table, and none of the §4 items is a GPU job. The other two §4 items have since been promoted into that table as F11 and F12, which is the register of record working as it should.
- **"Four of the ten on one consumer GPU" was an undercount.** The Tier-0 table below lists five.

**The audit itself is now open work.** `REVIEW_ROUND2.md` records 46 surviving findings, of which **2 CRITICAL and 6 HIGH are open**. Neither CRITICAL is a measurement question: one is a citation read backwards in the abstract, one is a null calibration in the psychohistory validation suite. Desk work is therefore not finished, and §6 lists it.

---

## 1. Why the CPU checks were cut

An earlier version of this ledger proposed six CPU-only mechanism checks: quantile balancing on synthetic router logits, subspace quantization on synthetic latents, delta-attention routing contrast on synthetic hidden states, and so on. **All cut as circular.** Implementing an equation and then measuring that the implementation satisfies the equation is not evidence about anything. Load balance on fake logits is decided by the fake logits. Effective dimension on a synthetic latent distribution is decided by the synthetic distribution. None of it constrains behaviour at 2.8T, which is the only question.

Two things survived and neither is a CPU check:

- **The scaling arithmetic** is not a check, it is the paper's Table 1. It is a calculation, it caught three real errors, and it is done.
- **Canary duty-cycle degradation** is not scale-dependent, but the honest version needs a benign null *measured* across two accelerators of different models. That makes it a two-GPU task. It is F8 below.

---

## 2. The ledger

Ordered by hardware. The ten rows carrying an F-number map to F1 to F10 in `../logos.tex` §15; that table now also carries F11, F12 and F13, which §4 and the Tier-0 note below pick up.

### Tier 0: one consumer GPU (3090 / 4090, 24 GB)

| ID | Test | What it settles | Budget | Pri |
|---|---|---|---|---|
| **F9** | **`logos-harness`.** Multi-tower proposal, disagreement gate, environment adjudication, yield scoring, accumulating admission, 350M early-fusion decoder. Substrate A: Pokémon (emulator adjudicates in ms). Substrate B: psychohistory (reality adjudicates). Spec: [`LOGOS_HARNESS.md`](LOGOS_HARNESS.md). Frozen design, endpoints, power analysis and kill conditions: [`F9_PREREGISTRATION.md`](F9_PREREGISTRATION.md) | **The observation bound.** Does the ordering hold: grounded > disagreement-gated self-play > unfiltered self-play? This is the constraint no part of the architecture relaxes. **Five arms, not four:** `F9_PREREGISTRATION.md` §2 adds **A4, ungated grounded**, without which the gate effect under grounding is unidentified, and A4 is also the arm any number compared against an external baseline must be scored in, because a statistic computed on gated output is a statistic on a difficulty-biased subsample. A4 is **excluded** from the Jonckheere-Terpstra trend test, which stays k = 4, because the paper never ordered A4 | **~1,400 GPU-h** (1,402.6, derived line by line in `F9_PREREGISTRATION.md` §8.1). The ~718 GPU-h this row used to carry was priced off a throughput that exceeded the card's dense BF16 ceiling of 71 TFLOPS, is withdrawn, and is superseded. The budget the row carried before that (72 to 96 GPU-h) buys **0.24 to 0.31 seeds per arm** at 350M across five arms, a quarter of one seed and not one seed per arm, which yields no within-arm variance and therefore no test statistic of any kind. At that budget F9 can confirm and cannot refute, which is the inverse of the role §5 assigns it. **The 125M screen is the lever that makes the powered version fit:** 9.579 GPU-h per run against 61.050 at 350M, so the five-arm n = 8 ordering study is 383.1 GPU-h | **P0** |
| **F3** | **Quantile Balancing and Causal Dual Bias in a real training loop.** 1B params, 64 experts, against three baselines: no balancing, auxiliary loss, auxiliary-loss-free bias (arXiv:2408.15664). Measure max-to-mean load ratio, dead experts, per-sequence imbalance, **and downstream loss** | Whether Quantile Balancing does what the vendor blog says. **QB and CDB have blog-grade sourcing only** (`BIBLIOGRAPHY_REVIEW.md` §4); no paper states the update rule. This produces the missing evidence. Round-2 note: an at-scale run already exists (32B-A5B, 1e22 FLOPs, 64 routed experts), so this is a downscale replication at roughly 83x less compute, not a first test | 72 to 120 GPU-h [repo estimate] | **P0** |
| **F10** | **Router-swap cost.** Train a small MoE (≤1B, 8 experts), replace one expert, measure how much routing efficiency η the descriptor warm-start recovers, and at what retraining cost | **Branch-Adapt-Route's whole economic case is linear update cost.** If router retraining after each swap is expensive, the economics are not linear and the ensemble loses its main advantage over a monolith. Testable at 1B. Nobody has published it | 96 GPU-h [repo estimate] | **P0** |
| **F4** | **Delta-Attention-Residual checkpoint conversion.** Convert a small open checkpoint by finetuning, per the additive-initialisation argument. Measure stability and routing max-weight (claimed 0.2 → 0.6) | The paper's claim that *existing checkpoints convert without destabilising* is what makes the mechanism deployable at all. On a real checkpoint this is not circular; on synthetic hidden states it would be | 48 GPU-h [repo estimate] | P1 |
| **F5** | **Codebook collapse on real hidden states.** Monolithic RQ-VAE vs subspace partitioning, effective dimension by participation ratio, on real embeddings rather than a synthetic latent distribution | Whether the 4-to-10 effective-dimension collapse reproduces on the distributions this architecture would actually quantize | **0 marginal GPU-h**: a by-product of F9, whose collapse monitor (`F9_PREREGISTRATION.md` §6) uses the same participation-ratio primitive. It still runs on one consumer accelerator, so it counts in the five | P1 |
|: | **Embedding inversion on post-router latents.** Attack latents from a small MoE, quantify how much input text a peer recovers | Puts a number on the withdrawn confidentiality claim (paper, Remark 5). The paper currently asserts that latents are not confidential; this measures how badly | not re-derived in GPU-h | P1 |

**Dependencies:** F5 falls out of F9 for free. F3 and F10 share a training harness, so build one 1B MoE trainer and both run on it. **Realistic Tier-0 programme: one MoE trainer plus logos-harness, 1,619 to 1,667 GPU-h on one owned card.** At 350 W and EUR 0.30/kWh that is 567 to 583 kWh, roughly **EUR 170 to EUR 175** of electricity; rented at RTX-3090 community-cloud rates of $0.20 to $0.25 per GPU-h it is **$324 to $417**. The previous figure on this line, 934 to 982 GPU-h and EUR 98 to EUR 103 or $187 to $246, was priced off the withdrawn throughput and is superseded. The rung-by-rung breakdown is [`TIER0_3090_PLAN.md`](TIER0_3090_PLAN.md), which also carries **F13 limb (a)** as a further rung on this same card: it is not an F9 arm and its cost is not yet derived, but it runs here, because the towers it needs are existing open-weight models of different pretraining lineage rather than models trained for the purpose.

### Tier 0.5: two GPUs of *different* models

| ID | Test | What it settles | Pri |
|---|---|---|---|
| **F8** | **Canary integrity under a realistic adversary.** Measure the actual benign drift null across two different accelerators with independently compiled kernels and mixed MXFP4 / NVFP4 paths. Then sweep adversary duty cycle `p` and locate `p*` | The published AUROC of 1.0 (arXiv:2607.19490, 408 configs) is against a **static** adversary on a **homogeneous** null. The architecture creates heterogeneous numerics in §7 and then leans on a detector that assumes them away. **We expect this to fire against us** | **P0** |

A matched pair of accelerators just reproduces the published setting and settles nothing. Different models is the whole test.

### Tier 1: one datacenter GPU (A100 / H100 80 GB, rentable)

| ID | Test | What it settles | Budget | Pri |
|---|---|---|---|---|
|: | MXFP4 + OAS + MBS vs NVFP4 on a real MoE checkpoint, end-to-end downstream accuracy | arXiv:2603.08713 reports the 10% to <1% gap closure. Nobody has replicated it **on an MoE**, where routing artifacts are what post-training quantization fails on | ~100 GPU-h | P1 |
|: | QAD vs QAT vs PTQ on a multi-stage post-trained model | The four-bit story depends on KL-to-teacher preserving guardrails installed during SFT and RL. Cited, never independently checked | ~200 GPU-h | P1 |
|: | KDA:MLA 3:1 hybrid at long context with sparse prefix caching; measured cache-hit-rate gain from the scheduler split | The best-documented systems chain in the paper, and entirely unmeasured by us | ~150 GPU-h | P2 |
|: | LatentMoE crossover: where does projection cost (`2dℓ` per token per layer) stop being paid for by bandwidth saved? Sweep `d/ℓ`, batch, arithmetic intensity **on real hardware** | The mechanism is favourable because the regime is memory-bound and reverses when it is not. A roofline sketch is a guess; a measured curve is not | ~50 GPU-h | P2 |

### Tier 2: one 8-GPU node

| ID | Test | What it settles | Pri |
|---|---|---|---|
| **F2** | **Branch-Adapt-Route at 7B to 70B**, ≥4 experts, against a matched **jointly** post-trained baseline | **The closest reachable proxy for the paper's central bet.** BAR is published at 7B with 4 experts; the architecture applies it at 2.8T with 5 towers, a 400-fold extrapolation. Reaching 70B halves it in log terms and tests the failure mode that worsens with scale: stronger experts make misroutes more expensive while the router still trains on far less signal | **P0** |
| **F6** | **Compliance mask × quantile balancer.** Mask experts to `−∞` (paper Eq. 10) inside a QB-routed model and measure the shift in quantile thresholds for every *other* token in the batch | **Nobody has looked at this and it is a plausible bug.** Masking changes the routing distribution, which is what the quantile solver balances. A compliance control that silently degrades unrelated users' routing is a governance failure, not a perf bug | **P0** |
| **F7** | **FaaSMoE cold-start p95** at large expert sizes | Published evaluation is on a 2.7B model, roughly 1000× smaller than a tower. Cold start is the obvious killer at interactive latency and scale-to-zero makes it worse | P1 |
|: | **Routing efficiency η in practice.** Validate the metric of paper §11.2, per domain, on a real multi-model ensemble | Without η there is no way to tell a well-routed ensemble from a bag of models with a lookup table. Designed in the paper, unvalidated | P1 |

### Tier 3: unreachable

| ID | Test | Blocked on |
|---|---|---|
| **F1** | Fit an MoE scaling law at 98% sparsity; is compute-optimal `D` anywhere near `20·N_total`? | Scaling sweep |
| **F2** (real) | The actual 5×2.8T ensemble: does it compose? | Frontier training budget |
|: | Tower co-activation as an N_eff analogue; does concentration predict degradation? | A trained ensemble |
|: | Straggler behaviour of all-to-all sparse dispatch on a real P2P network; sticky-owner loss | Cluster |

Named so they are not mistaken for oversights. **F2 is the paper.** There is no honest way to call the architecture validated until it runs.

---

## 3. Resolved since the last revision

These were open desk items in the previous ledger. All are now addressed in `../logos.tex`. **"Addressed" is not "closed":** `ARCHITECTURE_REVIEW.md`'s re-graded index, after round 2, records F-04, F-13, F-14 and F-15 as **not closed** and F-09 and F-10 as **closed only in part**, and the rows below say which is which.

| Was open | Now |
|---|---|
| The regulatory question (R1 / R2 / R3) | §13.2 and Conjecture 3. Three readings worked through; R3 identified as the arbitrage; stated as an open question for the AI Office rather than a settled legal opinion, which is the honest status |
| The master router had no design | §4. Bandit-feedback training signal with a capability prior and ε-exploration; the structural finding that **routing quality will track domain verifiability**, so it must be reported per domain; a three-step failure ladder with a mandatory degradation flag; descriptor warm-start for tower swaps (now F10); and the mask placed **after** routing so users cannot steer around it. **Designed, untested, and closed only in part** (`ARCHITECTURE_REVIEW.md` F-09): none of it is measured, and §4.3 claims only that the warm start is measurable at 1B, so router drift under tower swap is deferred to F10 rather than settled |
| No cost model | §11.1. Memory floor ~100 accelerators, realistic ~320 by extrapolation from Kimi K3's serving ratio. **The comparison the paper never made:** five towers costs the same 320 accelerators as five replicas of one tower, so the ensemble is justified by traffic entropy across domains and nothing else |
| No composed-ensemble evaluation method | §11.2. Routing efficiency η, normalised between the best-single-tower floor and the oracle ceiling, reported per domain |
| No failure semantics | §11.3. Three paths, one contract each, with the principle that the caller always learns quality dropped. **Closed for three of four paths** (`ARCHITECTURE_REVIEW.md` F-10): FaaSMoE scale-to-zero cold start is not among the three and is deferred to F7 |
| Domain partition asserted, never justified | §3.4. A three-axis criterion (corpus disjointness, objective conflict, update cadence). Applying it says **four towers, not five**: Mathematics and Logic fail all three axes and should merge. **Not closed** (`ARCHITECTURE_REVIEW.md` F-14): the criterion is supplied, the partition is still unmeasured, §3.4 itself calls it "a data question we can specify but have not run", and Table 1 still prints five. An argued partition is not a measured one. The measurement is §4 below, and it is now **falsifier F11** in `../logos.tex` §15, which needs no accelerator; an earlier revision of this row said no falsifier covered it, and that is superseded |
| Proposition 2 requires overlapping corpora; §13 treats towers as clean residency partitions | §11.4. Split by residency class rather than by tower: a shared core all towers may consume, plus residency-bound shards. **The honest consequence is that Proposition 2's headroom shrinks** by an amount §11.4 concedes it does not bound. **Not closed** (`ARCHITECTURE_REVIEW.md` F-15): with `f` the residency-bound corpus fraction the system needs `56T x (1 + 4f)` unique tokens, so at `f = 1` the headroom is exactly zero, and nothing in the paper bounds `f`. Measuring `f` is §4 below, and it is now **falsifier F12** in `../logos.tex` §15, which needs no accelerator; an earlier revision of this row said no falsifier covered it, and that is superseded |
| The theory of self-bootstrapping was stated as our conjecture | §12. It is a **synthesis of four established results** (Choi martingale, Yue pass@k boundary, Zenil degeneration theorem, Absolute Zero's executor). Only three narrower claims are ours, and they are labelled |

---

## 4. Still unspecified

Named so they are not mistaken for oversights. **None of these needs an accelerator**, which is why §0 withdraws the "GPU-only, no desk work left" framing. Two of them **now do** have an F-number: `../logos.tex` §15 has since minted **F11** for the corpus-overlap measurement and **F12** for the residency fraction, so the promotion discussed at the end of this section has happened and this ledger follows it. The other three carry no F-number, which is why §0 still says that table is not the complete list of open work. Round 2 counted four items here; this revision adds a fifth, the residency fraction, because `ARCHITECTURE_REVIEW.md` F-15 needs it and nothing in the ledger was carrying it.

- **Training-run fault tolerance across towers.** Five independent frontier training runs have five independent failure processes. No checkpointing or restart story.
- **Provenance for sourced towers.** Under regulatory reading R3 an integrator sources towers from third parties. What assurance beyond hash-against-ledger? What if a tower is backdoored?
- **Multi-tenant fairness.** Thousands of adapters over shared frozen experts with scale-to-zero, and no isolation or noisy-neighbour analysis.
- **Corpus-overlap measurement.** §3.4's partition criterion needs measured corpus disjointness to settle four towers versus five. That is a data question, specified but not run. It is what `ARCHITECTURE_REVIEW.md` F-14 is still open on.
- **Residency-fraction measurement.** §11.4 splits the corpus into a shared core plus residency-bound shards and concedes Proposition 2's headroom shrinks without bounding by how much. With `f` the residency-bound fraction the requirement is `56T x (1 + 4f)` unique tokens, and `f = 1` takes the headroom to zero. Measuring or bounding `f` is a corpus question, not a training run. It is what `ARCHITECTURE_REVIEW.md` F-15 is still open on.

**On promoting these two to numbered falsifiers: done, in the paper, not here.** They belonged in the falsifier table on merit, because both are pre-registerable, both have a stated decision rule, and both bear on load-bearing claims (four-versus-five towers, and whether Proposition 2 has any headroom at all). This ledger did not mint `F11` and `F12` unilaterally, because `../logos.tex` §15 is the register of record for F-numbers and inventing IDs here that the paper does not carry would recreate exactly the divergence §0 exists to record. **That promotion has since happened in the register of record:** corpus overlap is **F11** and the residency fraction is **F12** in `../logos.tex` §15, both marked as needing no accelerator, and this ledger follows the paper rather than the other way round.

---

## 5. Order of work

1. **F9 (`logos-harness`).** **~1,400 GPU-h** (1,402.6, `F9_PREREGISTRATION.md` §8.1) on one owned consumer card, per the powered design there. It tests the constraint nothing else in the architecture relaxes. The ~718 GPU-h this line used to carry was priced off a withdrawn throughput and is superseded. **The 125M screen is the whole lever:** a 125M run is 9.579 GPU-h against 61.050 at 350M, a factor of 6.37, so the powered five-arm n = 8 ordering study is 383.1 GPU-h, where the same study at 350M would be 2,442 GPU-h and would not fit the card at any defensible electricity bill. **Correction to what this line used to say:** it is not "the only experiment here that can return a cheap decisive negative". A negative here is an equivalence claim, which needs a two-one-sided-tests procedure and therefore more seeds than the positive direction, so the negative is the expensive half. `F9_PREREGISTRATION.md` §9.4 pre-commits that a non-significant result below n = 8 is reported UNDERPOWERED, not negative.

   **And the corrected budget does not buy K3, the kill condition on the gate, which is the contrast the paper cares most about.** K3 is a conjunction of two equivalence declarations, and equivalence is the direction that needs more seeds, not fewer. At n = 8 the tightest declarable equivalence margin is **6.2 accuracy points** while superiority needs **7.9**, so a true gate effect between the two is INCONCLUSIVE by construction, and that window is where H3 most plausibly lives. Closing it costs **622.6 GPU-h** in Study 1 at n = 13 for a 5.0-point margin, or **1,676 GPU-h in one study** at n = 35 for 3.0 points. Neither is bought, and the margin is **not** widened to make K3 easier to declare, because widening it would make a false K3 easier to reach as well. F9 also carries a fifth pre-committed kill condition, **K5**: F13 limb (b), calibrated-confidence weighting lifting ensemble accuracy on the held-out battery with no environment adjudication of any kind, an ensemble-level McNemar comparison costed at **12.7 GPU-h** inside F9's total, and the cheapest kill shot the programme has against its own thesis. F13 limb (a) is **not** an F9 arm; it is a separate rung on the same card, priced nowhere yet, and [`TIER0_3090_PLAN.md`](TIER0_3090_PLAN.md) states its instrument and its limitation.
2. **F3 and F10.** Build one 1B MoE trainer, run both. 168 to 216 GPU-h. Quantile Balancing's missing evidence, and Branch-Adapt-Route's economic case.
3. **F8.** Two accelerators of different models, and it is where we expect to be wrong. The cost was never re-derived in GPU-hours and the binding cost is not hours, it is access to a second accelerator of a different model.
4. **F6.** One node. Cheap, and nobody has looked at the mask-balancer interaction.
5. **F2 proxy at 7B to 70B.** One node. The closest reachable version of the central bet.
6. Everything else waits on hardware that does not exist for this project.

**Before any of it:** the two CRITICAL findings in §6 are desk work, cost nothing but tokens, and one of them invalidates the claim F9 is designed to test the architecture's contribution to. Fix those first.

---

## 6. Open work the round-2 audit added

[`REVIEW_ROUND2.md`](REVIEW_ROUND2.md) (2026-07-25) is an adversarial referee report written independently of the process that wrote `../logos.tex`, `ARCHITECTURE_REVIEW.md` and `BIBLIOGRAPHY_REVIEW.md`. Every finding was handed to a second pass whose only job was to refute it; those that did not survive were dropped, those that survived weakened were downgraded with the weakening recorded inline. **46 findings survived: 2 CRITICAL, 6 HIGH, 18 MEDIUM, 20 LOW.** `REVIEW_ROUND2.md` §6 records what round 2 checked and found sound, which is a large fraction of the paper and the honest counterweight to a raw finding count.

**The two CRITICAL findings are open.** Neither is a measurement.

| ID | What it is | Why it is not GPU work |
|---|---|---|
| **C-02** | Both debate papers are cited for a diversity conclusion that both explicitly disclaim, in a sentence printed in the abstract. The cited theorem holds for *homogeneous* agents and extends to heterogeneous ones; the known ways to break the martingale are protocol-internal, not informational diversity | It collapses the second of the paper's three stated original contributions, the only architectural one, and the one `LOGOS_HARNESS.md` flags as "the claim we would most like tested". Rewriting the claim is a desk fix; deciding whether the Tier-C claim survives as a conjecture is a judgement, not a run |
| **P-01** | In the psychohistory validation suite that `logos-harness` names as its adjudicator, the assumed null fire rate p0 = 0.10 is a construction constant, and the repository's own uncontaminated clean-window data puts the measured rate far above it. The cheapest decisive fix, per **P-03**, is to serialise three fields that the v3 code already computes and then discards one function return before writing its JSON, and re-run over 12 already-harvested quiet windows | Pure CPU, one pass over data already on disk. No new harvest, no accelerator |

The six HIGH findings are **A-01** (N_act derived by an expert-fraction method that is wrong by 1.5x to 1.8x on both models where ground truth exists, changing a regulatory conclusion rather than a digit), **C-01** (the martingale theorem attributed to the wrong paper and the wrong authors, with the actual source uncited), **P-02** (the block-label shuffle null is degenerate on the substrate used, so the specificity endpoint reduces to a magnitude test at a bar seven times below the median quiet-window drop), **P-03** (above), **P-04** (three overlapping looks at one substrate plus one non-informative control, reported as four confirmations across two substrates), and **P-09** (three documents give three different blockers for the same falsifiers). P-04 and P-09 are fixed in `../README.md`; the rest are open.

Two artifacts were produced alongside the audit:

- [`F9_PREREGISTRATION.md`](F9_PREREGISTRATION.md): a sealable pre-registration for F9 in the house format of `../validation/PRE_REGISTRATION.md`. It fixes sample size, seeds, endpoints, effect sizes, test statistics, multiplicity correction, stopping rule and the gate/yield/round parameters that silently set each arm's training corpus. Its headline is that **F9 is underpowered at the budget this ledger used to assign it**, with the power arithmetic shown, and §9.4 pre-commits to reporting UNDERPOWERED rather than negative below n = 8.
- [`TIER0_3090_PLAN.md`](TIER0_3090_PLAN.md): the Tier-0 rungs priced in GPU-hours, electricity and rental dollars on the owned card, with the pre-committed kill conditions for F9, F2 and F8 stated before the runs. It is a run plan, not a funding document.
