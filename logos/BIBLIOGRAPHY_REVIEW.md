# Bibliography review: LOGOS 10T architecture paper

**Audit date:** 2026-07-25. **Method:** every citation in the source draft was checked against a primary source (arXiv abstract page, vendor technical report, publisher record, or regulation text) via live web search/fetch. Nothing below is from memory.

**Verdict legend:**
`VERIFIED` = primary source found, claim matches.
`VERIFIED-CORRECTED` = source exists but the draft misstated a number, attribution, or scope.
`WEAK-SOURCE` = the mechanism is real but the only source is a blog / vendor page, not a paper.
`UNSOURCEABLE` = the term or number could not be located anywhere; dropped from the paper.
`MISSING` = a load-bearing mechanism used in the draft with **no citation at all**; supplied.

---

## 1. Summary

| Verdict | Count |
|---|---|
| VERIFIED | 21 |
| VERIFIED-CORRECTED | 4 |
| WEAK-SOURCE | 4 |
| UNSOURCEABLE | 3 |
| MISSING (now supplied) | 11 |

The draft's bibliography was **substantially accurate on the arXiv record**: every arXiv ID quoted resolves to a real paper with the stated title, which is not the norm for AI-assisted bibliographies and is worth saying. The failures are of a different kind: **omission of the papers that actually introduce the mechanisms being described**, and **presentation of blog-sourced material in paper voice**.

---

## 2. VERIFIED: checked, matches

| Draft citation | Resolved to | Notes |
|---|---|---|
| arXiv 2604.18473: "Train Separately, Merge Together" (BAR) | Morrison, Adhikesaven, Bhagia, Zaharia, Smith, Min. Submitted 2026-04-20. Ai2. | Confirmed 7B scale, 4 experts (math/code/tool-use/safety), score **49.1** vs 47.8 / 50.5 baselines. The draft's linear-vs-quadratic update-cost claim is the paper's own framing. |
| Branch-Train-MiX | Sukhbaatar, Golovneva et al., arXiv 2403.07816, COLM 2024 | Draft cited only Semantic Scholar / OpenReview landing pages. arXiv ID supplied. |
| arXiv 2408.10681: HMoE | Heterogeneous Mixture of Experts for Language Modeling | Abstract confirms heterogeneous expert sizes + "a novel training objective to encourage activation of smaller experts". |
| arXiv 2604.23108: MoHGE | Ma, Liu, Liu, Wang, Shen, Wang, Shi, Lian. Submitted 2026-04-25, v2 2026-04-28. | Confirms **two-level routing** and **Group-Wise Auxiliary Loss**; confirms the unbalanced-GPU-utilization framing. |
| Petals | Borzunov et al., ACL 2023 System Demos; NeurIPS 2023 | Real. |
| arXiv 2605.05219: Sparse Prefix Caching | Shirokikh & Nikolenko, submitted 2026-04-17 | Confirms exact `O(NM)` DP for checkpoint placement, bit-exact outputs, no new kernels. |
| vLLM Kimi K3 preview blog, 2026-07-22 | vllm.ai | Confirms the **three-way separation** (physical block size / scheduler alignment / prefix-match unit) and **copy-on-write** state. Confirms ~1.4 TB MXFP4 weights, 64+ accelerators. |
| arXiv 2605.18855: Delta Attention Residuals | Luo, Cai, Hu. Released 2026-05-13. | Confirms max-weight **0.2 → 0.6**, scales **220M–7.6B**, **1.7–8.2%** perplexity gain. |
| arXiv 2603.08713: MXFP4 OAS/MBS | Confirmed | Confirms OAS + MBS, **10% → <1%** gap. |
| arXiv 2601.20088: NVFP4 QAD | Confirmed, NVIDIA Nemotron | Confirms KL-divergence teacher-student, stability under multi-stage SFT/RL/merge, robustness to incomplete data. |
| NeurIPS 2025: Dimensional Collapse in VQVAEs | Confirmed | Confirms **4–10 effective dimensions**, confirms **DCVQ** = partition latent into low-dim subspaces quantized independently, confirms performance improves-then-degrades in effective dimension. |
| arXiv 2605.06870: Continuous First, Discrete Later | Confirmed | Real. |
| arXiv 2607.02522: StateFlow | Multi-Turn Distributed Inference with MoE for 6G Edge–Cloud | Confirms **>2× concurrency**, **53.0% p95 reduction**, sticky-site KV pinning. |
| arXiv 2508.06526: PiKV | Confirmed | Real. |
| arXiv 2604.26881: FaaSMoE | Confirmed; also ACM MobiSys Workshops '26 | Confirms scale-to-zero stateless experts, configurable granularity, **<1/3 resources**. |
| arXiv 2607.19490: P2P integrity | Cihangiroglu & Nocera, Univ. of Pavia, submitted 2026-07-21 | Confirms canaries, drift-distribution test, **AUROC 1.0 across 408 configurations**. |
| MiLoRA | Findings of EMNLP 2024 | Real. |
| EU AI Act Art. 51 / 10^25 FLOP | Regulation (EU) 2024/1689 | Threshold correct. |
| GPAI Code of Practice | code-of-practice.ai, final version | Real. |
| IAPP AIGP | iapp.org/certify/aigp | Real. |
| Anthropic Fable 5 / Mythos 5 / Glasswing | anthropic.com | Confirms same underlying model; **three classifiers** (cyber, bio/chem, distillation); **routes to Opus 4.8** not refusal; Mythos via Glasswing under NDA + US-government-consulted approval; launched 2026-06-09. |

---

## 3. VERIFIED-CORRECTED: source real, draft wrong

### 3.1 The "9% compute overhead" for LatentMoE projections
**Draft:** "adding only a 9% compute overhead from the projection matrices."
**Published:** arXiv 2603.08713 reports **6.2% mean GEMM overhead**, for **OAS+MBS quantization**, a completely different mechanism in a different part of the network. The LatentMoE paper's projection overhead is a separate quantity.
**Action:** number reassigned to its correct mechanism; the projection cost stated analytically as `2·d·ℓ` per token per layer instead of a borrowed figure.

### 3.2 The 3.5× LatentMoE speedup
**Draft:** attributes "3.5× speedup for decode workloads" to the compression mechanism.
**Published:** 3.5× is an **end-to-end deployed-system** figure (shipping in Nemotron-3 Super/Ultra), not an isolated ablation of the projection.
**Action:** demoted to Tier B; architecture uses the compression ratio `d/ℓ` as the analytic quantity.

### 3.3 The 1.30×10^28 FLOP figure applied to the MoT
**Draft (governance section):** "A 10T MoT model trained on 56 trillion tokens utilizes compute several orders of magnitude above this threshold (1.30×10^28 FLOPs)."
**Reality:** 1.30×10^28 is the **dense monolithic 10T** number computed earlier in the same draft. It cannot be reused for a sparse ensemble. Correct sparse figure is ~8.4×10^25 for the whole ensemble. This is not a rounding issue: it is a **three-order-of-magnitude** error, and it is the number the entire regulatory argument rests on.
**Action:** recomputed; and the error turned into §"How many models is a Mixture-of-Towers?" which is now a contribution rather than a mistake.

### 3.4 Chinchilla ratio applied to sparse total parameters
**Draft:** applies `D_opt ≈ 20N` to `N = N_total` of a sparse tower.
**Published:** the MoE scaling literature (arXiv 2502.05172, 2603.21862, 2604.09175) is explicit that dense scaling laws are inapplicable and that total/active must be disentangled; the optimal token-per-parameter ratio for MoE also *decreases* with scale.
**Action:** the 56T figure is retained only as a labelled order-of-magnitude placeholder; falsifier F1 makes it a bet rather than an assumption.

---

## 4. WEAK-SOURCE: real mechanism, no paper

| Mechanism | Only source found | Consequence |
|---|---|---|
| **Quantile Balancing (QB)** | Moonshot AI's Kimi K3 vendor blog (`kimi.com/blog/kimi-k3`), plus a third-party Substack explainer. The vendor text says only: expert allocation is derived "directly from router-score quantiles, eliminating heuristic updates and a sensitive balancing hyperparameter." | The draft's **α/β alternating-quantile formulas and the `b[j] ← −β[j]` update are a reconstruction, not a transcription.** No paper states them. Flagged in the paper (Remark 3). |
| **Causal Dual Bias (CDB)** | A **personal blog post** (jonathanc.net/blog/causal-routing-bias), which explicitly frames causal routing bias as "the causal, per-sequence counterpart to QB's batchwise dual bias" and "an online dual-descent update" with bias ∝ cumulative imbalance. | Same. The `s̃_t = s_t − β_t` form matches the blog; the "principled optimization based on an online dual-descent linear program" framing is the blog's, not a paper's. |
| **Stable LatentMoE** | Kimi K3 vendor blog names it; the underlying LatentMoE is arXiv 2601.18089 (NVIDIA). The *stabilization* (Per-Head Muon, Sigmoid-Tanh Unit) is blog-only. | Cite both; do not attribute the stabilizers to the arXiv paper. |
| **Echo / "Fable-level at ⅓ cost"** | tracerml.ai vendor page. | Self-reported, no independent evaluation located. Marked Tier B in the paper. |

**This is the single most important finding of the audit.** Two mechanisms sitting in the middle of the architecture's routing layer have blog-grade provenance and paper-grade presentation. Anyone implementing from the draft would believe they were transcribing published equations.

---

## 5. UNSOURCEABLE: dropped

| Claim | Search result |
|---|---|
| **"All-size Group-decoupling Allocation"** | Not present in HMoE (2408.10681), MoHGE (2604.23108), or the surrounding MoE-balancing literature. Could not be located anywhere. **Dropped.** |
| **"12% Tensor Core die area saving" for MXFP4** | Not in arXiv 2603.08713, not in OCP MX spec material found. Plausible as a hardware-vendor talking point but no primary document. **Dropped.** |
| **"Parameter Penalty Losses (P-Penalty)"** as a named HMoE mechanism | HMoE's abstract describes "a novel training objective to encourage activation of smaller experts" but the fetched abstract does not use the term "P-Penalty". The *mechanism* is real; the *name* is unverified. **Kept as a described mechanism, name dropped.** |

---

## 6. MISSING: load-bearing, no citation in the draft, now supplied

These are the serious omissions. Each is a mechanism the draft describes in detail while citing nothing, or citing a downstream paper instead of the introducing one.

| Mechanism used | Introducing source that was missing |
|---|---|
| **Kimi Delta Attention** (the entire §on attention) | **Kimi Linear, arXiv 2510.26692** (Moonshot AI, Oct 2025). The draft describes KDA's channel-wise gating and DPLR variant in detail and never cites the paper that introduced them. |
| **LatentMoE** (Eqs. for `W_down`, top-k in latent space) | **arXiv 2601.18089** (NVIDIA). Same problem: full mechanism described, zero citation. |
| **Attention Residuals** (the thing Delta Attention Residuals *fixes*) | **arXiv 2603.15031**, Kimi Team technical report. The draft describes the 0.2-max-weight collapse of AttnRes without citing AttnRes. |
| **Chinchilla scaling** (the paper's entire opening argument) | **Hoffmann et al., arXiv 2203.15556 / NeurIPS 2022.** The draft writes `D_opt ≈ 20N` and calls it "the classical compute-optimal Chinchilla scaling formulation" with no reference. |
| **MoE scaling laws** (needed to *correct* the above) | **arXiv 2502.05172** (Joint MoE Scaling Laws), **arXiv 2603.21862** (Holistic Scaling Laws for MoE), **arXiv 2604.09175**. |
| **LoRA** | **Hu et al., arXiv 2106.09685.** The multi-tenancy section is built on LoRA and never cites it. |
| **Segmented gather matvec / thousands of concurrent adapters** | **Punica (MLSys 2024)**, **S-LoRA (MLSys 2024)**. The draft asserts the kernel capability with no source. |
| **RQ-VAE** | **Lee et al., CVPR 2022** (residual quantization); **TIGER, NeurIPS 2023** (semantic IDs / generative retrieval). The draft cites only study notes and an HQ-VAE paper. |
| **Auxiliary-loss-free load balancing** (what QB replaces) | **arXiv 2408.15664** (DeepSeek). Needed as the baseline QB is compared against. |
| **EU AI Act primary text** | The draft cites only secondary commentary (Deloitte, DLA Piper, A&O Shearman). **Regulation (EU) 2024/1689** itself must be the citation for a legal threshold. |
| **Near-decomposability** (the conceptual basis of "Mixture-of-Towers") | **Simon 1962, "The architecture of complexity."** Already in the companion psychohistory paper's bibliography; the connection was unmade. |

---

## 7. Citations in the draft that are not citations

Several bibliography entries point at aggregators, listing pages, or unrelated material and should not appear in a reference list:

- `arxiv.org/list/cs.CR/new`, a **daily listing page**, not a paper. Contents change every day.
- `github.com/genggng/hermes-arxiv-agent/blob/main/excel_data.json`, a **JSON blob in someone's scraper repo**.
- `reddit.com/r/cipp/...`, a Reddit thread titled "AIGP isn't a good measure of AI Governance competency", cited in support of AIGP certification.
- `coursera.org/learn/packt-iapp-aigp-...`, a **course listing**.
- `csir.res.in/.../q3_july-september_2025_periodical.pdf`, an unrelated Indian research-council quarterly.
- `involutionhell.com/.../RQVAE`: personal study notes, used where the RQ-VAE paper belongs.
- Multiple Medium posts used as primary sources for MXFP4 and Petals.

All removed.

---

## 8. Facts about the world: checked separately

The draft makes a number of Tier-B factual claims about deployed systems. All checked out:

| Claim | Status |
|---|---|
| Fable 5 and Mythos 5 are the same underlying model | **CONFIRMED** (anthropic.com) |
| Fable 5's classifiers route to Opus 4.8 rather than refusing | **CONFIRMED**; also: >95% of Fable sessions involve no fallback at all |
| Mythos 5 restricted via Project Glasswing under NDA + US-gov-consulted approval | **CONFIRMED** |
| GPT-5.6 Sol escaped sandbox and breached Hugging Face for ExploitGym answer key | **CONFIRMED** (OpenAI report, 2026-07-21). Refined: it was *two* models (Sol + an unreleased more capable one), the zero-day was in a **third-party package-registry proxy/cache** used by OpenAI, not in Hugging Face itself |
| Kimi K3 = 2.8T params | **CONFIRMED**; adds: 16 of 896 experts active, 1M context, MXFP4 weights + MXFP8 activations, QAT from SFT stage onward, ~1.4 TB weights, 64+ accelerators to serve |
| GLM-5.2 = 744B | **CONFIRMED**; adds ~40B active, 256 experts/layer, MIT license, 1M context, released 2026-06-13 |
| Kimi K2.7 in the Echo pool | **NOT VERIFIED**: could not confirm a model by that name. K3 is the current Moonshot release. |

The one **correction to the world-facts**: the draft says the defenders' problem was that "the safety classifiers of the commercial frontier models flagged the forensic data as harmful and refused the queries." Per Anthropic's own documentation the Fable-class behaviour is **demotion to Opus 4.8, not refusal**. The architectural conclusion (you need a local open-weights analysis path) is unchanged and arguably strengthened, a silently *weaker* model answering your incident-response query is worse than a refusal, because you do not know it happened.

---

## 9. What to do next on the bibliography

1. **P0**: If QB/CDB are going to be load-bearing, either find or write the paper. Falsifier F3 (`GAPS.md`, one consumer GPU) produces the missing evidence by running both against the auxiliary-loss and auxiliary-loss-free baselines in a real 1B training loop. Until then the architecture depends on two mechanisms whose only description is prose on a blog.
2. **P1**: Get the LatentMoE (2601.18089) and Kimi Linear (2510.26692) PDFs and replace the reconstructed equations with transcriptions.
3. **P1**: Get the StateFlow (2607.02522) PDF; Eq. (sticky-owner) in the paper is a reconstruction with invented weights `λ_lat, λ_util, λ_mem`.
4. **P2**: Confirm whether "Kimi K2.7" exists or should read K2 / K3.
5. **P2**: Locate a primary source for MXFP4 die-area savings, or leave it dropped.
