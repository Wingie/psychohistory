# GAPS — what to test and what to build, for the LOGOS 10T paper

Companion to `../logos.tex`, in the same form as the repository's `RUN_AND_CHECK.md`.
**Audit date:** 2026-07-25. **Stance:** adversarial.

---

## 0. On CPU checks — mostly useless, and here is the exact line

The first draft of this ledger proposed six CPU-only "mechanism checks": quantile balancing on synthetic router logits, DCVQ on synthetic latents, delta-attention-residual routing contrast on synthetic hidden states, and so on. **Cut. They were circular.** Implementing an equation and then measuring that the implementation satisfies the equation is not evidence about anything. Load balance on fake logits is determined by the fake logits; effective dimension on a synthetic latent distribution is determined by the synthetic distribution. None of it constrains what happens at 2.8T, which is the only question.

Two things survive, and only two:

- **L1 · The scaling arithmetic.** Not a "check" — it is the paper's Table 1, and it caught three real errors (a 55× dense/sparse category error, the token-fragmentation fallacy, and a three-order-of-magnitude number in the regulatory argument). It is a spreadsheet. Keep it as an appendix calculation, not a validation result. **Status: DONE, folded into `logos.tex` §2.**
- **L6 · Canary duty-cycle degradation.** This one is genuinely not scale-dependent — whether detector AUROC survives a low-duty-cycle adversary is a property of a *statistical test on drift distributions*, not of a 2.8T model. **But** the honest version needs a *measured* benign null from real heterogeneous hardware, which makes it a 2-GPU task, not a CPU task. Promoted to **G-1.5** below.

Everything else in this document needs a GPU. The rest of the ledger is organised by **how much GPU**, because that is the only axis that determines what is actually runnable.

---

## 1. Tier 0 — one consumer GPU (RTX 3090 / 4090, 24 GB)

**This is the tier where real work is possible today.**

| ID | Test | What it settles | Budget | Status | Pri |
|---|---|---|---|---|---|
| **G-0.1** | **`logos-harness`** — the agentic bootstrap loop. Multi-tower proposal → disagreement gating (JS divergence) → environment adjudication → yield scoring → corpus admission → 350M early-fusion decoder. **Substrate A: Pokémon** (emulator adjudicates, ms latency). **Substrate B: psychohistory** (reality adjudicates, this repo's `../validation/` pipeline). Spec: [`LOGOS_HARNESS.md`](LOGOS_HARNESS.md). Falsifier **F9** | **Whether the towers can bootstrap past the token wall.** Do disagreement-gated, environment-adjudicated trajectories beat (a) unfiltered self-play and (b) a matched text-only control, *without* triggering model collapse? The only data strategy past the wall that is not repetition or synthesis (§8) | ~5 weeks incl. data gen; 3–4 days of training | **SPEC** | **P0** |
| **G-0.2** | **QB + CDB in a real training loop.** 1B params, 64 experts, against three baselines: no balancing / auxiliary loss / aux-loss-free bias (arXiv:2408.15664). Measure max-mean load ratio, dead-expert count, per-sequence imbalance, **and downstream loss** | Whether Quantile Balancing does what the Kimi K3 blog says. **QB and CDB currently have blog-grade sourcing only** (`BIBLIOGRAPHY_REVIEW.md` §4) — no paper states the α/β update. This test produces the missing evidence | ~3–5 days | **SPEC** | **P0** |
| **G-0.3** | **Router-swap cost.** Train a small MoE (≤1B, 8 experts), replace one expert, measure router-retraining cost as a fraction of expert-training cost | **BAR's entire economic case is linear update cost.** If router retraining after each swap is expensive, the economics are not linear and MoT loses its main advantage over a monolith. Testable at 1B. Nobody has published it | ~4 days | **SPEC** | **P0** |
| **G-0.4** | **Delta-Attention-Residual checkpoint conversion.** Take a small open checkpoint, convert to Delta AttnRes by finetuning per the additive-initialisation argument, measure stability and the routing max-weight (claimed 0.2 → 0.6) | The paper's claim that *existing checkpoints convert without destabilisation* is what makes the mechanism deployable at all. On a real checkpoint this is not circular; on synthetic hidden states it would be | ~2 days | **SPEC** | P1 |
| **G-0.5** | **Embedding-inversion on post-router latents.** Attack latents from a small MoE; quantify how much input text a peer actually recovers | Puts a number on the withdrawn confidentiality claim (`ARCHITECTURE_REVIEW.md` F-07). Currently the paper asserts "latents are not confidential" — this measures it | ~3 days | **SPEC** | P1 |
| **G-0.6** | **DCVQ on real hidden states.** Run the monolithic-RQ-VAE vs DCVQ effective-dimension comparison on **real** embeddings/hidden states, not a synthetic latent distribution | Whether the 4–10-effective-dimension collapse reproduces on the distributions this architecture would actually quantize. `logos-harness` Phase 1 produces exactly this data as a by-product | ~1 day (free if G-0.1 runs) | **SPEC** | P1 |

**Note the dependency:** G-0.6 falls out of G-0.1 for free. G-0.2 and G-0.3 share a training harness — build one 1B MoE trainer and both run on it. **Realistic Tier-0 programme: one MoE trainer + logos-harness, ~5 weeks, one GPU.**

---

## 1.5 Tier 0.5 — two heterogeneous GPUs

| ID | Test | What it settles | Status | Pri |
|---|---|---|---|---|
| **G-1.5** | **Canary integrity under a realistic adversary.** Measure the *actual* benign drift null across two different accelerators with independently compiled kernels and mixed MXFP4/NVFP4 paths. Then sweep adversary duty cycle `p` and locate `p*` where AUROC falls to chance | Falsifier **F8**, and the one we expect to fire against our own architecture. The published AUROC 1.0 (arXiv:2607.19490, 408 configs) is against a **static** adversary on a **homogeneous** null. This architecture deliberately creates heterogeneous numerics in §6 and then relies in §9 on a detector that assumes them away | **SPEC** | **P0** |

Two GPUs of *different* models is the whole point — a homogeneous pair reproduces the published setting and settles nothing.

---

## 2. Tier 1 — one datacenter GPU (A100/H100 80 GB, rentable)

| ID | Test | What it settles | Budget | Pri |
|---|---|---|---|---|
| **G-1.1** | **MXFP4 + OAS + MBS vs NVFP4 on a real MoE checkpoint**, end-to-end downstream accuracy | arXiv:2603.08713 reports the 10%→<1% gap closure. Nobody has replicated it **on an MoE**, where routing artifacts are exactly what post-training quantization fails on | ~100 GPU-h | P1 |
| **G-1.2** | **QAD vs QAT vs PTQ on a multi-stage post-trained model.** Does KL-to-teacher actually preserve alignment where cross-entropy QAT destroys it? | The architecture's whole 4-bit story depends on QAD preserving guardrails installed in SFT/RL. Cited, never independently checked | ~200 GPU-h | P1 |
| **G-1.3** | **KDA:MLA 3:1 hybrid at long context** with sparse prefix caching; measure the actual cache-hit-rate improvement from the scheduler split | The systems chain (KDA → recurrent state → prefix-cache incoherence → scheduler split) is the best-documented part of the paper and entirely unmeasured by us | ~150 GPU-h | P2 |
| **G-1.4** | **LatentMoE crossover.** Where does the projection FLOP cost (`2dℓ`/token/layer) stop being paid for by the bandwidth saved? Sweep `d/ℓ`, batch size, arithmetic intensity **on real hardware** | The mechanism is favourable *because the regime is memory-bound* and inverts when it is not. A roofline sketch on CPU is a guess; a measured curve is not | ~50 GPU-h | P2 |

---

## 3. Tier 2 — one 8-GPU node

| ID | Test | What it settles | Pri |
|---|---|---|---|
| **G-2.1** | **BAR at 7B→70B.** Modular post-training with ≥4 experts at 7B minimum, ideally 70B, scored against a matched **jointly** post-trained baseline | **This is the closest reachable proxy for the paper's central bet.** BAR is published at 7B/4-experts; the architecture applies it at 2.8T/5-towers, a 400× extrapolation. Getting to 70B halves the extrapolation in log terms and, critically, tests the failure mode that *worsens* with scale: as experts get stronger, a misroute costs more, and the router is trained on far less signal than any expert it dispatches to | **P0** |
| **G-2.2** | **Router-attributed evaluation methodology.** Build and validate a metric that distinguishes a well-routed ensemble from a bag of models with a lookup table. The naive "max over towers" is precisely what a good MoT beats and a bad one does not | Without this there is no way to *evaluate* an MoT at all, at any scale. Desk-designed (G-D4), validated here | **P0** |
| **G-2.3** | **FaaSMoE cold-start p95** at large expert sizes | Falsifier F6. The published evaluation is on Qwen1.5-MoE-2.7B — a ~1000× gap to a tower. Cold start is the obvious killer at interactive latency and scale-to-zero makes it worse | P1 |
| **G-2.4** | **Compliance-mask × quantile-balancer interaction.** Mask experts to `-∞` (Eq. 10) inside a QB-routed model and measure what happens to the quantile thresholds for every *other* token in the batch | **Nobody has looked at this and it is a real interaction bug waiting to happen.** Masking changes the routing distribution, which is exactly what QB's quantile solver is balancing. A compliance control that silently degrades unrelated users' routing is a governance failure, not just a perf bug | **P0** |

**G-2.4 is the sleeper.** It costs one node and it sits at the intersection of the paper's safety story and its performance story, which is exactly where nobody looks.

---

## 4. Tier 3+ — multi-node cluster and frontier budget (unreachable)

| ID | Test | Blocked on |
|---|---|---|
| **G-3.1** | The actual 5×2.8T MoT: does it compose? (falsifier **F2**) | TRAINING-RUN |
| **G-3.2** | Fit an MoE scaling law at 98% sparsity; is compute-optimal `D` anywhere near `20·N_total`? (falsifier **F1**) | TRAINING-RUN sweep |
| **G-3.3** | Tower co-activation as an `N_eff` analogue; does concentration predict degradation? (falsifier **F7**) | needs a trained MoT |
| **G-3.4** | Straggler behaviour of all-to-all sparse dispatch across a real P2P network; sticky-owner loss semantics | CLUSTER |

These are named so they are not mistaken for oversights. **G-3.1 is the paper**; everything else is elaboration, and there is no honest way to call the architecture validated until it runs.

---

## 5. DESK — no GPU, highest value per hour

Unchanged in priority by the shift to GPU planning. **The paper's original contributions are here, not in the code.**

| ID | Work | Why it matters | Pri |
|---|---|---|---|
| **G-D1** | **The regulatory question.** Work R1/R2/R3 (per-tower / composed-system / router-only) against the actual text of Regulation (EU) 2024/1689, Annex XIII, and the GPAI Code of Practice. Has the Commission addressed modular composition anywhere? Consider writing to the AI Office | Conjecture 2 is the paper's strongest claim and is currently an argument from reading, not a legal analysis. If a settled answer exists we need it; if not, **that is a finding worth publishing on its own** | **P0** |
| **G-D2** | **Design the master router.** No training-data story, no failure semantics, no adversarial-routing analysis, no drift-vs-frozen-towers treatment. All capability flows through it | The largest hole in the architecture (`ARCHITECTURE_REVIEW.md` F-09). Also blocks G-2.2 | **P0** |
| **G-D3** | **Cost model.** $/Mtok, accelerator-hours; MoT vs serving one 2.8T model five times vs a dense equivalent | The paper argues affordability throughout and prices nothing. Also the only way to evaluate Conjecture 1 (compute-economics) | P1 |
| **G-D4** | **Composed-ensemble evaluation methodology** (design; validated in G-2.2) | Without it, "is this MoT good" is unanswerable | P1 |
| **G-D5** | **Fault tolerance and straggler semantics.** Tower unreachability, all-to-all p99, sticky-owner loss mid-session — StateFlow pins state *precisely so it cannot move*, so losing the owner loses the session | A multi-node partly-P2P system with no failure semantics is not a design | P1 |
| **G-D6** | **Justify the domain partition.** Why five, why Code/Bio/Math/Logic/Admin? Math and Logic are not obviously separable | A partition chosen by human intuition is the thing MoE routing exists to avoid | P2 |
| **G-D7** | **Re-derive the Petals cost model for sparse dispatch.** Petals is dense pipeline-parallel; this is data-dependent all-to-all with much larger per-unit weights | "Petals-style" is currently doing unearned work | P2 |
| **G-D8** | **Get the PDFs.** LatentMoE (2601.18089), Kimi Linear (2510.26692), StateFlow (2607.02522), PiKV (2508.06526). Replace the reconstructed equations in `logos.tex` with transcriptions | Three equations are labelled reconstructions. Honest, but not good enough to implement from | **P1** |

---

## 6. Still not specified anywhere

- **Training-run fault tolerance across towers.** Five independent frontier training runs, five independent failure processes, no checkpointing/restart story.
- **Data governance across towers.** Proposition 2 *requires* tower corpora to overlap. So licensing, PII, and residency constraints apply per-tower to overlapping data. The compliance section treats towers as clean partitions; the data argument says they cannot be. **These two parts of the paper contradict each other and neither notices.**
- **Provenance for sourced towers.** Under reading R3 an integrator sources towers from third parties. What assurance beyond hash-against-ledger? What if a tower is backdoored?
- **Multi-tenant fairness.** Thousands of LoRA adapters over shared frozen experts with scale-to-zero — no isolation or noisy-neighbour analysis.

---

## 7. Order of work

1. **G-D1 + G-D2** — one week of desk work, no hardware. The regulatory analysis and the router design are the paper's actual contributions and both are currently gaps. **Do this before writing any more architecture prose.**
2. **G-D8** — one day. Get the four PDFs, fix the reconstructed equations.
3. **G-0.1 (`logos-harness`)** — the grounded-pretraining programme. Five weeks on the 3090 you already have, and it is the only experiment here that can return a **cheap decisive negative** on a research bet. See §8.
4. **G-0.2 + G-0.3** — build one 1B MoE trainer, run both. QB's missing evidence, and BAR's economic case.
5. **G-1.5** — canary under a heterogeneous null. Two different GPUs, an afternoon of compute, and it is where we expect to be wrong.
6. **G-2.4** — the mask × balancer interaction, if a node is available. Cheap, and nobody has looked.
7. Everything else waits on hardware that does not exist for this project.

---

## 8. Why `logos-harness` is P0 and not a side quest

The paper's own Proposition 2 says the binding constraint at 10T is **unique high-quality tokens**. Sparsity removed the compute constraint; tower decomposition bought corpus-overlap headroom; 4-bit serving handled memory. **Nothing in the architecture manufactures tokens**, and past some point of LOGOS development there is no more human text to buy.

Past the wall there are exactly three moves: **repeat** (bounded at ~4 epochs — Muennighoff et al., NeurIPS 2023), **synthesise from text** (derivative; re-samples a distribution the ensemble already carries and inherits its errors), or **ground** — towers argue, act on the world, and the world answers.

Only the third is open-ended, and it has a known failure mode: training on self-generated data causes model collapse (Shumailov et al., *Nature* 631:755–759, 2024). The harness's claim to be different is structural, not hopeful. **Disagreement gating plus yield weighting mean the loop cannot train on its own confident agreement** — which is precisely the distribution-narrowing dynamic that produces collapse. Trajectories are admitted in proportion to `−log P_M(observed | context, action)`: high when the towers disagreed and the environment settled it, near zero when they agreed and were right.

Three properties make this the right P0:

1. **It is the cheapest experiment in the whole ledger that can return a decisive *negative*.** One consumer GPU, ~5 weeks. If disagreement-gated grounded trajectories do not beat a matched text-only control at 350M on the easiest imaginable grounding substrate — Game Boy frames, 4 colours, 160×144, with the exact semantics under test *printed on screen* — then the LOGOS data strategy past the wall is repetition plus synthesis, Proposition 2's headroom is all there is, and `logos.tex` should say so plainly.
2. **The null is interpretable.** The held-out vocabulary has a matched control set that *does* appear in the text stream, and the collapse monitor runs against a text-only baseline. A failure tells you which of three things failed.
3. **Substrate B ties the two papers in this repository together.** The psychohistory validation suite already has the harvest scripts, the observation operators, the pre-registered thresholds, and the sealed rosters. What it lacks is a trajectory generator — and its own blocked falsifiers (forward skill, fixed-point reliability, Lucas invariance, regime occupancy) are blocked on exactly that. The bootstrap harness needs an adjudicator the ensemble cannot fake; psychohistory needs a generator. They are the same missing piece from two directions.

It is also the one place where a mechanism the architecture review had to *relocate* lands correctly: the RQ-VAE codebook, misplaced in the hidden-state serving path by the source draft (F-06), is exactly right as an **observation tokenizer in a shared vocabulary** — which is why G-0.6 falls out of G-0.1 for free.

**Caveat, stated once and kept:** at 350M with two open models standing in for towers, these are not 2.8T towers and the disagreement structure may not transfer. And Substrate B does not scale as a token source — adjudication by reality takes weeks, which is three orders of magnitude short of a 2.8T corpus. Run **A for volume, B for validity**, and do not conflate them.
