# Bibliography review: LOGOS 10T architecture paper

> ## Read this first: this is SELF-REVIEW, not independent review
>
> This document was written by the same authoring process that wrote `logos.tex`. It is not an outside referee report and must not be cited as one. **The independent pass is [`logos/REVIEW_ROUND2.md`](REVIEW_ROUND2.md)** (2026-07-25), which audited this document alongside the paper and returned forty-six surviving findings, two of them CRITICAL.
>
> Round 2 named four classes of defect that the method used here was structurally unable to catch. Two of them are defects in *this* method specifically:
>
> 1. **A citation that resolves, is real, is quoted accurately, and supports the opposite of the inference drawn from it.** Round-2 finding C-02, CRITICAL. This document's stated method, "every citation in the source draft was checked against a primary source", and its §1 claim that every quoted arXiv ID resolves, are both true and both blind to it. `logos.tex` cites arXiv:2601.19921 and arXiv:2508.17536 for the claim that informational diversity is what breaks the debate martingale. Both papers say the opposite: 2601.19921's Theorem 1 gets a strict submartingale from *homogeneous* agents via confidence weighting and states that diversity injection leaves the dynamics a martingale, and Choi et al. extend the martingale to heterogeneous agents, measuring +6.19 points **in favour of identical agents**. That inference is printed in the paper's abstract and carries the only architectural item in its list of three original contributions. A verdict legend with five classes has no class for "resolves, matches, and refutes you".
> 2. **A claim with no citation at all.** A method that checks citations against sources cannot see a claim that has none. `logos.tex:94`, the token-supply premise the entire data wall rests on, carries no `\cite` and no number; `logos.tex:172`, one of two enumerated motivations for the tower split, asserts a measurement with no source. §6 below lists eleven load-bearing uncited mechanisms and neither of these two is among them. The `MISSING` verdict was populated by reading the draft's bibliography, not by reading the draft for unsupported sentences.
>
> The other two classes fall on the sibling document `ARCHITECTURE_REVIEW.md`: a derivation round 1 reproduced rather than audited (the `N_act` expert-fraction method, wrong by 1.5x to 1.8x, round-2 A-01), and an entire artefact never opened (the psychohistory validation suite, the adjudicator falsifier F9 depends on, which had received no referee pass at all).
>
> One round-2 finding runs the other way and is applied below: C-03 reverses §5's "12% tensor-core die area saving" row **in the paper's favour**. The figure is in the abstract of the paper cited two sentences earlier in `logos.tex`, and declaring it untraceable was this document's error, not the draft's.
>
> Nothing below has been softened. Round 2 confirmed §4 (blog-grade provenance for QB and CDB) as a real finding.

**Audit date:** 2026-07-25. **Method:** every citation in the source draft was checked against a primary source (arXiv abstract page, vendor technical report, publisher record, or regulation text) via live web search/fetch. Nothing below is from memory. The method's blind spots are stated in the header above: it cannot see an accurately-quoted source that refutes the claim it is attached to, and it cannot see a claim with no citation to check.

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
| VERIFIED | 20 |
| VERIFIED-CORRECTED | 4 |
| WEAK-SOURCE | 4 |
| UNSOURCEABLE | 2 |
| MISSING (now supplied) | 11 |

**41 verdicts over 41 distinct items.** The earlier tally read 21 / 4 / 4 / 3 / 11 = 43 verdicts over 42 distinct items, which was arithmetically impossible. Round 2 found both causes. The EU AI Act was counted in two mutually exclusive classes, VERIFIED in §2 and MISSING in §6 (X-16); the §2 row is deleted and its verification folded into the §6 row, taking VERIFIED from 21 to 20. The "12% tensor-core die area saving" was listed UNSOURCEABLE when the figure is in the abstract of a paper the draft already cites (C-03); the §5 row is deleted and the finding folded into the §2 row for arXiv 2603.08713, taking UNSOURCEABLE from 3 to 2 and removing one distinct item.

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
| arXiv 2603.08713: MXFP4 OAS/MBS | Confirmed | Confirms OAS + MBS, **10% → <1%** gap. **Also confirms the 12% figure** (round-2 C-03): the closing sentence of the abstract reads "enabling near-NVFP4 accuracy while retaining MX's hardware-efficiency advantages (e.g., 12% relative area savings in tensor cores)". An earlier revision of this review listed that figure under §5 UNSOURCEABLE, and the remark at `logos.tex:363` said "we could not trace it to a primary document and do not repeat it". Both were false: the source is the same paper that remark cites twice. The §5 row is deleted here and the §1 count corrected. The `logos.tex` remark needs the corresponding correction, tracked as §9 item 4. |
| arXiv 2601.20088: NVFP4 QAD | Confirmed, NVIDIA Nemotron | Confirms KL-divergence teacher-student, stability under multi-stage SFT/RL/merge, robustness to incomplete data. |
| NeurIPS 2025: Dimensional Collapse in VQVAEs | Confirmed | Confirms **4–10 effective dimensions**, confirms **DCVQ** = partition latent into low-dim subspaces quantized independently, confirms performance improves-then-degrades in effective dimension. |
| arXiv 2605.06870: Continuous First, Discrete Later | Confirmed | Real. |
| arXiv 2607.02522: StateFlow | Multi-Turn Distributed Inference with MoE for 6G Edge–Cloud | Confirms **>2× concurrency**, **53.0% p95 reduction**, sticky-site KV pinning. |
| arXiv 2508.06526: PiKV | Confirmed | Real. |
| arXiv 2604.26881: FaaSMoE | Confirmed; also ACM MobiSys Workshops '26 | Confirms scale-to-zero stateless experts, configurable granularity, **<1/3 resources**. |
| arXiv 2607.19490: P2P integrity | Cihangiroglu & Nocera, Univ. of Pavia, submitted 2026-07-21 | Confirms canaries, drift-distribution test, **AUROC 1.0 across 408 configurations**. |
| MiLoRA | Findings of EMNLP 2024 | Real. |
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
**Reality:** 1.30×10^28 is the **dense monolithic 10T** number computed earlier in the same draft. It cannot be reused for a sparse ensemble. Correct sparse figure is ~8.4×10^25 for the whole ensemble. This is not a rounding issue: it is a substitution by **a factor of about 155, i.e. two orders of magnitude** (1.30×10^28 / 8.4×10^25 = 154.76, log10 = 2.19), and it is the number the entire regulatory argument rests on. An earlier revision of this row called it "three orders of magnitude", which would require the corrected figure to be about 1.3×10^25; the overstatement was this document's, never `logos.tex`'s (round-2 X-15). The separate quantity in `ARCHITECTURE_REVIEW.md`, "above the 10^25 threshold by ~8×, not by several orders of magnitude", is the threshold margin and is correct as stated.
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
| **MoE scaling laws** (needed to *correct* the above) | **arXiv 2502.05172** (Joint MoE Scaling Laws) and **arXiv 2603.21862** (Holistic Scaling Laws for MoE), supplied as `ludziejewski2025` (`logos.tex:775`) and `moescaling2026` (`:787`). **arXiv 2604.09175 was listed here as supplied and is not** (round-2 X-16): `grep -c '2604.09175' logos.tex` returns 0 and no bibitem carries it. It remains outstanding, and §9 item 6 tracks it. `logos.tex:154`'s claim is carried by the two sources that are cited. |
| **LoRA** | **Hu et al., arXiv 2106.09685.** The multi-tenancy section is built on LoRA and never cites it. |
| **Segmented gather matvec / thousands of concurrent adapters** | **Punica (MLSys 2024)**, **S-LoRA (MLSys 2024)**. The draft asserts the kernel capability with no source. |
| **RQ-VAE** | **Lee et al., CVPR 2022** (residual quantization); **TIGER, NeurIPS 2023** (semantic IDs / generative retrieval). The draft cites only study notes and an HQ-VAE paper. |
| **Auxiliary-loss-free load balancing** (what QB replaces) | **arXiv 2408.15664** (DeepSeek). Needed as the baseline QB is compared against. |
| **EU AI Act primary text** | The draft cites only secondary commentary (Deloitte, DLA Piper, A&O Shearman). **Regulation (EU) 2024/1689** itself must be the citation for a legal threshold. Now cited as `euaiact2024` (`logos.tex:751`, Art. 51 and Annex XIII), and the 10^25 FLOP threshold it carries is verified correct against the regulation text. **This item was previously counted twice** (round-2 X-16), once here under MISSING and once in §2 under VERIFIED; the §2 row is deleted and the verification folded into this one. |
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
4. **P1**: Correct `logos.tex:363`. It says the 12% tensor-core die-area figure "could not be traced to a primary document"; it is in the closing sentence of the abstract of arXiv 2603.08713, which the same remark cites twice (round-2 C-03). A false negative provenance claim about a paper you cite is worse than the sourcing gap it was meant to disclose, because it invites a referee to re-check every other negative provenance claim in the draft, and there are several.
5. **P2**: Confirm whether "Kimi K2.7" exists or should read K2 / K3.
6. **P2**: Add a bibitem for arXiv 2604.09175 or stop listing it under §6 as supplied. It is currently listed as supplied and is absent from `logos.tex` (round-2 X-16).
