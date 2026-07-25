# GAPS: what is left to measure

Companion to `../logos.tex`, in the form of the repository's `RUN_AND_CHECK.md`.
**Audit date:** 2026-07-25. **Stance:** adversarial.

---

## 0. Status in one paragraph

Everything in the paper is now either settled by arithmetic, argued in full, or corrected against a primary source. **What remains open is measurement, and every open item needs accelerators.** There is no desk work left in the ledger: the router design, the cost model, the evaluation metric, the failure semantics, the partition criterion, and the corpus-residency contradiction were all open in the previous revision and are resolved in the paper. Ten falsifiers remain, four of them on one consumer GPU.

---

## 1. Why the CPU checks were cut

An earlier version of this ledger proposed six CPU-only mechanism checks: quantile balancing on synthetic router logits, subspace quantization on synthetic latents, delta-attention routing contrast on synthetic hidden states, and so on. **All cut as circular.** Implementing an equation and then measuring that the implementation satisfies the equation is not evidence about anything. Load balance on fake logits is decided by the fake logits. Effective dimension on a synthetic latent distribution is decided by the synthetic distribution. None of it constrains behaviour at 2.8T, which is the only question.

Two things survived and neither is a CPU check:

- **The scaling arithmetic** is not a check, it is the paper's Table 1. It is a calculation, it caught three real errors, and it is done.
- **Canary duty-cycle degradation** is not scale-dependent, but the honest version needs a benign null *measured* across two accelerators of different models. That makes it a two-GPU task. It is F8 below.

---

## 2. The ledger

Ordered by hardware. All ten map to falsifiers F1 to F10 in `../logos.tex` §15.

### Tier 0: one consumer GPU (3090 / 4090, 24 GB)

| ID | Test | What it settles | Budget | Pri |
|---|---|---|---|---|
| **F9** | **`logos-harness`.** Multi-tower proposal, disagreement gate, environment adjudication, yield scoring, accumulating admission, 350M early-fusion decoder. Substrate A: Pokémon (emulator adjudicates in ms). Substrate B: psychohistory (reality adjudicates). Spec: [`LOGOS_HARNESS.md`](LOGOS_HARNESS.md) | **The observation bound.** Does the ordering hold: grounded > disagreement-gated self-play > unfiltered self-play? This is the constraint no part of the architecture relaxes | ~5 weeks incl. data gen; 3–4 days training | **P0** |
| **F3** | **Quantile Balancing and Causal Dual Bias in a real training loop.** 1B params, 64 experts, against three baselines: no balancing, auxiliary loss, auxiliary-loss-free bias (arXiv:2408.15664). Measure max-to-mean load ratio, dead experts, per-sequence imbalance, **and downstream loss** | Whether Quantile Balancing does what the vendor blog says. **QB and CDB have blog-grade sourcing only** (`BIBLIOGRAPHY_REVIEW.md` §4); no paper states the update rule. This produces the missing evidence | 3–5 days | **P0** |
| **F10** | **Router-swap cost.** Train a small MoE (≤1B, 8 experts), replace one expert, measure how much routing efficiency η the descriptor warm-start recovers, and at what retraining cost | **Branch-Adapt-Route's whole economic case is linear update cost.** If router retraining after each swap is expensive, the economics are not linear and the ensemble loses its main advantage over a monolith. Testable at 1B. Nobody has published it | 4 days | **P0** |
| **F4** | **Delta-Attention-Residual checkpoint conversion.** Convert a small open checkpoint by finetuning, per the additive-initialisation argument. Measure stability and routing max-weight (claimed 0.2 → 0.6) | The paper's claim that *existing checkpoints convert without destabilising* is what makes the mechanism deployable at all. On a real checkpoint this is not circular; on synthetic hidden states it would be | 2 days | P1 |
| **F5** | **Codebook collapse on real hidden states.** Monolithic RQ-VAE vs subspace partitioning, effective dimension by participation ratio, on real embeddings rather than a synthetic latent distribution | Whether the 4-to-10 effective-dimension collapse reproduces on the distributions this architecture would actually quantize | 1 day, **free if F9 runs** | P1 |
|: | **Embedding inversion on post-router latents.** Attack latents from a small MoE, quantify how much input text a peer recovers | Puts a number on the withdrawn confidentiality claim (paper, Remark 6). The paper currently asserts that latents are not confidential; this measures how badly | 3 days | P1 |

**Dependencies:** F5 falls out of F9 for free. F3 and F10 share a training harness, so build one 1B MoE trainer and both run on it. **Realistic Tier-0 programme: one MoE trainer plus logos-harness, about 5 weeks, one GPU.**

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

These were open desk items in the previous ledger. All are now in `../logos.tex`.

| Was open | Now |
|---|---|
| The regulatory question (R1 / R2 / R3) | §13.2 and Conjecture 2. Three readings worked through; R3 identified as the arbitrage; stated as an open question for the AI Office rather than a settled legal opinion, which is the honest status |
| The master router had no design | §4. Bandit-feedback training signal with a capability prior and ε-exploration; the structural finding that **routing quality will track domain verifiability**, so it must be reported per domain; a three-step failure ladder with a mandatory degradation flag; descriptor warm-start for tower swaps (now F10); and the mask placed **after** routing so users cannot steer around it |
| No cost model | §11.1. Memory floor ~100 accelerators, realistic ~320 by extrapolation from Kimi K3's serving ratio. **The comparison the paper never made:** five towers costs the same 320 accelerators as five replicas of one tower, so the ensemble is justified by traffic entropy across domains and nothing else |
| No composed-ensemble evaluation method | §11.2. Routing efficiency η, normalised between the best-single-tower floor and the oracle ceiling, reported per domain |
| No failure semantics | §11.3. Three paths, one contract each, with the principle that the caller always learns quality dropped |
| Domain partition asserted, never justified | §3.4. A three-axis criterion (corpus disjointness, objective conflict, update cadence). Applying it says **four towers, not five**: Mathematics and Logic fail all three axes and should merge |
| Proposition 2 requires overlapping corpora; §13 treats towers as clean residency partitions | §11.4. Split by residency class rather than by tower: a shared core all towers may consume, plus residency-bound shards. **The honest consequence is that Proposition 2's headroom shrinks** |
| The theory of self-bootstrapping was stated as our conjecture | §12. It is a **synthesis of four established results** (Choi martingale, Yue pass@k boundary, Zenil degeneration theorem, Absolute Zero's executor). Only three narrower claims are ours, and they are labelled |

---

## 4. Still unspecified

Named so they are not mistaken for oversights.

- **Training-run fault tolerance across towers.** Five independent frontier training runs have five independent failure processes. No checkpointing or restart story.
- **Provenance for sourced towers.** Under regulatory reading R3 an integrator sources towers from third parties. What assurance beyond hash-against-ledger? What if a tower is backdoored?
- **Multi-tenant fairness.** Thousands of adapters over shared frozen experts with scale-to-zero, and no isolation or noisy-neighbour analysis.
- **Corpus-overlap measurement.** §3.4's partition criterion needs measured corpus disjointness to settle four towers versus five. That is a data question, specified but not run.

---

## 5. Order of work

1. **F9 (`logos-harness`).** Five weeks on one GPU. It tests the constraint nothing else in the architecture relaxes, and it is the only experiment here that can return a cheap decisive negative.
2. **F3 and F10.** Build one 1B MoE trainer, run both. Quantile Balancing's missing evidence, and Branch-Adapt-Route's economic case.
3. **F8.** Two different GPUs, an afternoon of compute, and it is where we expect to be wrong.
4. **F6.** One node. Cheap, and nobody has looked at the mask-balancer interaction.
5. **F2 proxy at 7B to 70B.** One node. The closest reachable version of the central bet.
6. Everything else waits on hardware that does not exist for this project.
