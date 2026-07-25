# Prior-art check for the four v0.3 candidate mechanisms

**Audit date:** 2026-07-25.
**Scope:** the four mechanisms proposed for the LOGOS v0.3 revision. Nothing else in `logos.tex` was re-checked.
**Standard of evidence:** the standard set by `REVIEW_ROUND2.md` §0 and applied in C-04. Every paper reported below was fetched. Where a paper appeared only as a search-result title and was not fetched, it is listed in §7 as unverified and is not used to support any verdict. §6 lists every search string so the negative results are auditable. §7 states what was not searched.

**Why this document exists.** Round 2 finding C-04 caught three uncited papers on the observation-bound thesis, one of them nine months prior. The failure mode was not dishonesty, it was not looking. This is the looking, done before the claims are written rather than after.

---

## 0. Verdicts in one line each

| # | Mechanism | Verdict |
|---|-----------|---------|
| 1 | KV-cache-aligned distillation across a size ladder | **Not found as stated. Candidate contribution.** Seven adjacent papers exist and must be cited and differentiated. One of them is empirical evidence that the hard part is harder than the enabling fact suggests. |
| 2 | Looped forward pass with a learned exit | **Fully published, including the specific reasoning-not-knowledge distinction, twice, with numbers.** Zero novelty. Highest C-04 recurrence risk of the four. |
| 3 | Cost-quality Pareto frontier as a routing metric | **Fully published and named.** AIQ (RouterBench) and APGR/CPT (RouteLLM). Confirmed to fix three of eta's four defects outright; the fourth is avoided by APGR and made non-load-bearing by AIQ, with one caveat recorded below. Zero novelty, and none is being claimed: this is a repair, not a contribution. |
| 4 | Ensembles of distilled siblings plus runtime adapters | **(a)** The theory is published and points against the design. A direct measurement of ensemble gain among N students of one parent LLM was searched for and not found, which is a weak unclaimed slot. **(b)** Fully answered by current engineering documentation, no novelty. |

---

## 1. KV-cache-aligned distillation across a size ladder

### 1.1 The enabling fact is confirmed

Fetched `ar5iv.labs.arxiv.org/html/2407.21783`, Table 3 of *The Llama 3 Herd of Models*:

| | 8B | 70B | 405B |
|---|---|---|---|
| Layers | 32 | 80 | 126 |
| Model Dimension | 4,096 | 8,192 | 16,384 |
| Attention Heads | 32 | 64 | 128 |
| Key/Value Heads | **8** | **8** | **8** |

The same source, §3.1: "We use grouped query attention (GQA) with 8 key-value heads to improve inference speed and to reduce the size of key-value caches during decoding."

Head dimension is model dimension over attention heads: 4096/32 = 8192/64 = 16384/128 = **128** at all three sizes. Per-layer KV state is therefore 2 x 8 x 128 = 2048 elements, or **4096 bytes per token per layer at fp16, identical across all three sizes**. The claim in the brief is correct and now has a primary citation.

Note what the fact does and does not establish. It establishes *shape* compatibility per layer. It does not establish semantic compatibility, and it says nothing about the layer-correspondence problem: layer 12 of the 8B is not layer 12 of the 70B in any defined sense, and the ladder differs in depth by a factor of roughly four. The enabling fact removes a tensor-shape objection. It does not remove the alignment problem, which is the actual research content.

### 1.2 What is published (all fetched)

**Same-architecture cross-model KV reuse.** DroidSpeak, arXiv:2411.02820, Liu, Huang, Yao, Feng, Gu, Du, Li, Cheng, Jiang, Lu, Musuvathi, Choukse; submitted 2024-11-05, revised 2025-07-14. Reuses KV cache across *different* LLMs provided "the LLMs have the same architecture." Reported: up to 4x throughput, approximately 3.1x faster prefill, negligible quality loss. Critically, it does **not** reuse the cache wholesale: it "selectively recomputes a few layers of the KV cache produced by another LLM and reuses the remaining layers."

That last detail is a useful empirical datum and it is **weaker evidence than an earlier revision of this paragraph claimed**. Even between models of identical architecture and identical size differing only by fine-tuning, direct cache reuse was not good enough and per-layer selective recomputation was required, which says something real about how hard alignment is. But DroidSpeak **requires a shared foundation model** ("the pair of models should share the same foundational model", and it "does not support KV cache sharing across LLMs originating from different foundation models") and it **never crosses a size boundary**. So it is not a direct negative against a cross-size ladder, and calling it "the closest thing to a negative result the literature offers" over-reads it. v0.3 must neither cite it as support nor lean on it as a refutation; the correct use is as evidence that shape compatibility does not imply semantic compatibility. **The work that actually bears on the novelty claim is MatFormer, and it bears on it positively** (§1.2, §1.3).

**Shared frozen prefill plus adapted decoders.** Two papers from what is evidently one group (overlapping author lists: Sunghyeon Woo, Joonghoon Kim, Sungjae Lee, Minjung Jo, Baeseong Park, Se Jung Kwon, Dongsoo Lee appear on both), published fifteen days apart:

- PrefillShare, arXiv:2602.12029, submitted 2026-02-12. "Multiple task-specific models share a prefill module and the KV cache generated for the same prompt." Reported 4.5x lower p95 latency, 3.9x higher throughput.
- ICaRus, arXiv:2603.13281, submitted 2026-02-27. Decomposes a decoder-only transformer into a logical encoder producing KV caches and a logical decoder producing tokens; freezes the encoder, fine-tunes only the decoder with "lightweight adapters such as LoRA". Reported up to 11.1x lower P95 latency and 3.8x higher throughput on an 8-model multi-agent workflow, with "comparable accuracy to task-specific fine-tuned model".

Both achieve interchangeability the easy way: by making the KV-producing part **literally the same frozen weights** for every family member. This is the strongest structural precedent and it is four to five months old. Any v0.3 claim must state why an aligned-but-independent ladder is preferable to a shared frozen encoder, because ICaRus already gets cache interchangeability for free and is already published.

**Adapter-translated cross-model KV.** Three papers, all fetched:

- Cache-to-Cache (C2C), arXiv:2510.03215, Fu, Min, Zhang, Yan, Dai, Ouyang, Wang; submitted 2025-10-03, revised 2026-03-02, published ICLR'26. Trains "a neural network to project and fuse the source model's KV-cache with that of the target model" plus a learnable gate. Reported 6.4 to 14.2% higher average accuracy than individual models, approximately 3.1 to 5.4% over text communication, 2.5x latency speedup.
- Latent Cache Flow (LCF), arXiv:2605.22863, Rossi, Raghunath, Wu; submitted 2026-05-19, revised 2026-06-06. Explicitly targets C2C's limitations: "the adapters are large and expensive to train, and translate individual tokens, which requires the target context to be identical." Reduces the adapter to about 4% of C2C's size (13 MB pruned versus 956 MB), +7.5% F1 and +23% Exact Match in differing-context settings, 8.5x faster than text-based communication.
- Semantic Cache Distillation, arXiv:2606.07684, Ma, Tang, Cui, Yao, Jia; submitted 2026-06-05. Transmits "compact semantic codes" instead of raw KV, handles reuse "across heterogeneous models (e.g., base and fine-tuned variants)", 2.65x TTFT speedup versus oracle consumer prefill, quality within 5% F1.

These three establish that cross-model KV transfer is an active and crowded subfield as of mid-2026. All three solve it with a **trained translation layer at serving time**. None of them makes the base models' own projections natively interchangeable, which is the distinguishing feature of the proposal.

**Depth-prefix reuse within one model.** LayerSkip, arXiv:2404.16710, Elhoushi, Shrivastava, Liskovich, Hosmer, Wasti, Lai, Mahmoud, Acun, Agarwal, Roman, Aly, Chen, Wu; submitted 2024-04-25, revised 2024-10-18. Exits at early layers and verifies with the remaining layers, and "benefits from shared compute and activations of the draft and verification stages." Reported up to 2.16x on CNN/DM summarization, 1.82x on coding, 2.0x on TOPv2. This is the degenerate case of the proposed mechanism: a small model whose KV is consumed by a larger one, where "small" is a layer prefix of "large" so interchangeability is identity rather than a learned property. Recorded honestly: the abstract page does not spell out the KV mechanics, so the "reuses KV-cache from draft stages" phrasing came from a search-result summary and is **not** primary-sourced. Treat the LayerSkip KV detail as unverified until the full text is read.

**Nested ladder from one parent with shared attention.** MatFormer, arXiv:2310.07707, Devvrit, Kudugunta, Kusupati, Dettmers, Chen, Dhillon, Tsvetkov, Hajishirzi, Kakade, Farhadi, Jain; submitted 2023-10-11, revised 2024-12-15. Nests **FFN blocks only**, extracting hundreds of submodels from one parent at zero extra training cost. Because the nesting does not touch attention, every MatFormer submodel shares the same `W_k`/`W_v` and the same layer count, so the caches are shape-compatible by construction.

**CORRECTED, and this correction moves the verdict of §1.3.** An earlier revision of this entry said the paper "does not mention KV cache compatibility or make any claim about it" and called it "the nearest unclaimed adjacency ... nobody appears to have exploited it". **That is false against the paper's own main text.** From `arxiv.org/html/2310.07707v2`, beside Table 2, verbatim: *"This additional speed-up can be primarily attributed to the more consistent nature of MatLM-based drafter and verifier models and is further boosted by **the ability to share attention cache across models from MatLM which is infeasible for the baselines** (see Appendix C.1)."* Appendix C.1 is titled "Speculative Decoding Attention Sharing", and the measurement is isolated in its own ablation row: speculative-decoding speed-ups of Baseline 1.10x / 1.08x, MatLM 1.14x / 1.11x, and **MatLM plus shared attention cache 1.16x / 1.14x** on LAMBADA and TriviaQA, with a 1.5B draft and a 2.6B verifier (`ar5iv.labs.arxiv.org/html/2310.07707`). In a decoder-only transformer the attention cache *is* the key-value cache.

**So MatFormer is a published, measured instance of a KV cache produced by a smaller sibling and consumed by a larger sibling of the same parent, across a size boundary, with no translation adapter and no re-prefill.** The sharing is not trivial-by-identity either: MatFormer's submodels differ in feed-forward width, so hidden states diverge after the first layer and the K/V tensors genuinely differ, and the separate ablation row is the evidence that the sharing is an approximation somebody had to test.

**Ladder distillation from one parent with no KV claim.** Minitron, arXiv:2408.11796, Sreenivas, Muralidharan, Joshi, Chochowski, Mahabaleshwarkar, Shen, Zeng, Chen, Suhara, Diao, Yu, Chen, Ross, Olabiyi, Aithal, Kuchaiev, Korzekwa, Molchanov, Patwary, Shoeybi, Kautz, Catanzaro; submitted 2024-08-21, revised 2024-12-09. Compresses Llama 3.1 8B to 4B and Mistral NeMo 12B to 8B via depth pruning and joint hidden/attention/MLP width pruning plus distillation. **Honest status:** the abstract page does not state whether pruning preserves `num_key_value_heads` or `head_dim`, and contains no mention of KV cache compatibility between parent and child. Width pruning that touches attention heads would break the constant-KV-shape property that makes the proposal work. This needs the full paper before v0.3 cites Minitron either way.

**Draft consuming target latents through its own projection.** DFlash, LMSYS blog, 2026-06-15, Z Lab / Modal / SGLang teams. "The latents of the target model are instead passed through a KV projection by the draft model", with immediate materialization via a layer-batched linear projection and a fused Triton kernel. Reported: >4.3x baseline throughput and 1.5x MTP on Qwen 3.5 397B-A17B / HumanEval; on Qwen 3-4B, acceptance length / speedup of 4.2/3.3x GSM8K, 4.0/3.2x HumanEval, 3.0/2.2x MT-Bench. This is the reverse direction of the proposal (large feeds small) and it is a re-projection rather than interchangeability, but it is the closest published instance of one model's internal state being consumed by another model's attention without re-prefill, and it is six weeks old.

### 1.3 What is not published

Across the fourteen search strings in §6.1, plus four arXiv API queries, **no paper was found that trains a family of siblings of differing depth from one parent under an explicit objective that makes their key and value projections interchangeable.** That negative is narrower than the one an earlier revision of this section stated, and the narrowing is forced by MatFormer (§1.2), which claims and measures cross-submodel attention-cache sharing at *constant* depth.

The nearest published things, in decreasing order of proximity. **MatFormer moves from rank 3 to rank 1**, because for a mechanism defined by crossing a size boundary, the only work that actually crosses one belongs first:

1. **MatFormer: cross-size KV sharing claimed in the main text and measured in Appendix C.1** (1.14x -> 1.16x LAMBADA, 1.11x -> 1.14x TriviaQA, 1.5B draft into 2.6B verifier), with no adapter and no re-prefill, achieved by literal weight sharing of the attention projections at constant layer count.
2. ICaRus / PrefillShare: interchangeability achieved by sharing one frozen KV-producing module, not by aligning independent ones.
3. C2C / LCF / SCD: interchangeability across genuinely different models, achieved by a trained translation adapter at serving time.
4. LayerSkip: cross-depth cache reuse where the small model is a layer prefix of the large one.
5. DFlash: target latents re-projected through the draft's own KV projection.
6. DroidSpeak: cross-model reuse between models that **share a foundation model**, at same architecture and same size, found to require per-layer selective recomputation.

**Verdict, downgraded: candidate contribution on two conjuncts only, and the reason previously given for it is withdrawn.** The sentence "the property exists in MatFormer by construction and nobody appears to have exploited it" was the load-bearing claim and it is false on the document's own named neighbour. What survives is **differing depth plus an explicit learned alignment objective**. Everything else in the original formulation, one parent, no adapter, no re-prefill, small prefills large, is instantiated *and measured* in MatFormer. With three conditions on how it is written.

- It must cite and differentiate all **ten** papers in §1.2. (An earlier revision said "all seven papers above" while §1.2 presents ten and this ranked list enumerates nine; no exclusion rule was ever stated, and the work most likely to fall off a "seven" list is MatFormer, which is the one most damaging to omit.) A referee in KV-cache systems will know at least four of them, and ICaRus plus PrefillShare are recent enough that "unaware" is the charitable reading and "non-disclosing" is the other one. This is the exact shape of C-04.
- **It must cite MatFormer as the positive existence result, not as a latent adjacency.** §1.2 previously carried DroidSpeak as the only existence result in the neighbourhood and had no positive one, which made the field read as more open than it is.
- **It must not cite DroidSpeak as a direct negative either.** DroidSpeak requires that "the pair of models should share the same foundational model" and states it "does not support KV cache sharing across LLMs originating from different foundation models", and it never crosses a size boundary. So it is evidence that direct reuse is imperfect *between same-size siblings of one foundation*, which bears on how hard alignment is and does not refute a cross-size ladder. Calling it "the closest thing to a negative result the literature offers" over-reads it; the finding that actually bites is MatFormer's positive.
- It must state the layer-correspondence problem explicitly. The enabling fact gives per-layer shape identity; it gives no answer to which of the small sibling's 32 layers supplies KV to which of the large sibling's 126, and the paper's own falsifier for this mechanism should be stated in those terms. **This is now the whole of the residual novelty** and should be written as such.

---

## 2. Looped forward pass with a learned exit

### 2.1 Lineage (all fetched)

- **Adaptive Computation Time**, arXiv:1603.08983, Alex Graves; submitted 2016-03-29, revised 2017-02-21. Introduces ACT so RNNs "determine how many computational steps are necessary between receiving input and generating output", deterministic and differentiable. Gains on parity, logic, addition and sorting; limited gain on character-level Wikipedia but with the observation that more computation is allocated "to harder-to-predict transitions, such as spaces between words and ends of sentences."
- **Universal Transformers**, arXiv:1807.03819, Dehghani, Gouws, Vinyals, Uszkoreit, Kaiser; submitted 2018-07-10. "We also add a dynamic per-position halting mechanism and find that it improves accuracy on several tasks." Turing-complete under stated assumptions; SOTA on LAMBADA at the time; +0.9 BLEU on WMT14 En-De.
- **Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach**, arXiv:2502.05171, Geiping, McLeish, Jain, Kirchenbauer, Singh, Bartoldson, Kailkhura, Bhatele, Goldstein; submitted 2025-02-07. 3.5B parameters, 800B tokens, "improve its performance on reasoning benchmarks, sometimes dramatically, up to a computation load equivalent to 50 billion parameters."
- **Mixture-of-Recursions**, arXiv:2507.10524, Bae, Kim, Bayat, Kim, Ha, Schuster, Fisch, Harutyunyan, Ji, Courville, Yun; submitted 2025-07-14, revised 2025-10-25. Per-token recursion depth via lightweight routers, plus "a KV sharing variant that reuses KV pairs from the first recursion". Scales 135M to 1.7B; lower validation perplexity, better few-shot accuracy, higher throughput than vanilla and recursive baselines. Exact numerics are not in the abstract and were not extracted.
- **Scaling Latent Reasoning via Looped Language Models** (Ouro), arXiv:2510.25741, Zhu, Wang, Hua and 28 co-authors including Bengio and Eshraghian; submitted 2025-10-29. 1.4B and 2.6B variants trained on 3.7T tokens, "match the results of up to 12B SOTA LLMs across a wide range of benchmarks."
- **Adaptive Depth in Looped Transformers: Diagnosing Learned Halting Gates and Trajectory Readouts**, arXiv:2607.20519, Popescu, Sáez de Ocáriz Borde, Liò; submitted 2026-07-08.

### 2.2 The reasoning-not-knowledge distinction is already published, twice, with numbers

**Reasoning with Latent Thoughts: On the Power of Looped Transformers**, arXiv:2502.17416, Saunshi, Dikkala, Li, Kumar, Reddi; submitted 2025-02-24. Abstract, verbatim: "we also present an interesting dichotomy between reasoning and memorization, and design a looping-based regularization that is effective on both fronts."

Fetched `arxiv.org/html/2502.17416v1` for the numbers. The looped 12⊗2 model against an iso-FLOP baseline and a 24-layer reference:

**CORRECTED: an earlier revision of this table mixed two comparators inside one column and none of its derived percentages reproduced.** Table 3 of the source gives three model rows, not two: Base (12⊗1, 12x FLOPs), Loop (12⊗2, 24x FLOPs) and Baseline (24⊗1, 24x FLOPs), with the source stating that "The Loop (12⊗2) model is iso-FLOP with the [24-layer] baseline (both have 24x FLOPs), while Base (12⊗1) is iso-**parameter** with the looped model". The old single "iso-FLOP baseline" column held the 24-layer model in row 1 and the iso-*parameter* model in rows 2 and 3. All three rows are reproduced verbatim with correct labels:

| Task class | Base (12⊗1, iso-**parameter**) | Loop (12⊗2) | Baseline (24⊗1, iso-**FLOP**) | Fraction of the Base-to-Baseline gap the loop covers |
|---|---|---|---|---|
| Closed Book QA (memorization) | 8.2% | 9.3% | 11.2% | **36.7%** (was printed as 34%) |
| Math Word Problems (reasoning) | 26.7% | 34.3% | 29.3% | **292%** (was printed as 282%) |
| Reasoning Primitives | 35.7% | 51.2% | 47.5% | **131%** (was left blank, and the 47.5 reference was omitted) |

The looped model is **worse than the iso-FLOP 24-layer baseline on closed-book QA** and beats it on math word problems and on reasoning primitives. That is the distinction, measured, seventeen months ago. **The §2.4 verdict is unaffected** and holds in both directions under the corrected labels; what failed was the evidence table, which is the C-04 failure mode this document exists to prevent, transplanted from "did not look" to "looked and mis-transcribed".

**Ouro**, arXiv:2510.25741, states it directly at scale. Verbatim from the fetched abstract page: "this advantage stems not from increased knowledge capacity, but from superior knowledge manipulation capabilities."

### 2.3 The learned exit specifically is the weak part

Popescu, Sáez de Ocáriz Borde and Liò, arXiv:2607.20519, submitted 2026-07-08, seventeen days before this audit. Verbatim findings from the fetched abstract page:

- "fixed-prior depth supervision ... produces difficulty-aware trajectories whose intermediate states expose useful stopping signals, and that simple post-hoc confidence readouts often match or outperform learned linear and MLP gates."
- "fitting gates on frozen trajectories localizes the failure: it appears to stem mainly from the trajectory induced by joint gate training rather than from limited gate expressivity."
- On Ouro's large-scale models, "pretrained ponder gates are competitive but not uniformly Pareto-optimal."

So the *learned* part of "learned exit" is exactly the component the newest paper finds is often beaten by a confidence threshold, and the diagnosis is that joint gate training corrupts the trajectory.

### 2.4 Verdict

**Zero novelty in the mechanism. Zero novelty in the distinction.** The literature does not merely "support" that looping buys reasoning depth but not knowledge; it establishes it, with an iso-FLOP ablation (Saunshi) and an at-scale statement (Ouro). Nothing was found that contradicts it.

This is the highest C-04 recurrence risk of the four mechanisms. If v0.3 presents the reasoning-versus-knowledge distinction as its own finding, it repeats C-04 with two papers instead of three, both more prominent. The correct framing is: cite Saunshi for the ablation and Ouro for the scale statement, use the distinction as a *premise*, and if the learned exit is retained, cite 2607.20519 and say why a learned gate beats a post-hoc confidence readout in this specific setting, or drop the gate for a readout.

---

## 3. Cost-quality Pareto frontier as a routing metric

### 3.1 The standard formulations (all fetched)

**FrugalGPT**, arXiv:2305.05176, Chen, Zaharia, Zou; submitted 2023-05-09. Reports both directions of the tradeoff rather than a single scalar: quality at fixed cost ("improve the accuracy over GPT-4 by 4% with the same cost") and cost at fixed quality ("match the performance of the best individual LLM (e.g. GPT-4) with up to 98% cost reduction").

**RouterBench**, arXiv:2403.12031, Hu, Bieker, Li, Jiang, Keigwin, Ranganath, Keutzer, Upadhyay; submitted 2024-03-18, revised 2024-03-28. 405k+ inference outcomes. Fetched `arxiv.org/html/2403.12031v2` for the metric. Defines **AIQ**, average improvement in quality:

```
AIQ(R_theta) = 1/(c_max - c_min) * integral_{c_min}^{c_max} R~_theta dc
```

This is the area under the cost-quality curve, normalized by the span of the cost domain. It is dimensionless and, with quality normalized to [0,1] across datasets, AIQ values fall in [0,1]. Supporting constructions: a **non-decreasing convex hull (NDCH)** enforcing q2 >= q1 whenever c2 >= c1, with violating points replaced by superior affine combinations; a **Zero Router** reference built from the individual LLMs' collective NDCH; and an **Oracle Router** that always selects the best-performing LLM, cheapest if tied.

**RouteLLM**, arXiv:2406.18665, Ong, Almahairi, Wu, Chiang, Wu, Gonzalez, Kadous, Stoica; submitted 2024-06-26, revised 2025-02-23. Fetched `arxiv.org/html/2406.18665v4`. Defines:

```
PGR(M_R^alpha)  = ( r(M_R^alpha) - r(M_w) ) / ( r(M_s) - r(M_w) )
APGR            = integral_0^1 PGR(M_R^alpha) d( c(M_R^alpha) )
CPT(x%)         = minimum percentage of calls to the strong model needed to reach PGR = x%
```

Endpoints are the weak model (0) and the strong model (1). APGR is stated as bounded in [0,1]. Reported: costs reduced "by over 2 times in certain cases" without compromising quality, plus transfer across swapped strong/weak pairs.

Also fetched: *A Unified Approach to Routing and Cascading for LLMs*, arXiv:2410.10347, Dekoninck, Baader, Vechev; submitted 2024-10-14, revised 2025-05-22. The abstract page carries no metric definition, so this paper contributes nothing to the metric question here and is recorded only to close the search.

### 3.2 Do these avoid eta's four failure modes?

Assessed against A-02's four defects. **Three confirmed avoided, one partly.**

| A-02 defect | AIQ (RouterBench) | APGR (RouteLLM) |
|---|---|---|
| (1) Denominator zero when best single tower dominates | **Avoided, and the reason previously given here was false.** An earlier revision said "AIQ has no ratio and no oracle in it", which is wrong against the formula this document reproduces at §3.1: the leading `1/(c_max - c_min)` **is** a ratio, and it vanishes on a degenerate single-cost candidate set. Correct statement: AIQ has **no oracle term, and its only denominator is the cost span, which is nonzero whenever the candidate models differ in price**. A dominating single model produces a flat curve with a well-defined area, so eta's failure event is avoided; a second degenerate case, cost degeneracy, exists and is different from eta's. | **Not avoided structurally.** The denominator `r(M_s) - r(M_w)` is zero if the designated weak model matches the strong one. But the endpoints are two models designated *a priori*, not a post-hoc max over k, so the condition is diagnosable before evaluation rather than emerging from per-domain slicing. Strictly weaker failure, same shape. |
| (2) Unbounded below, no scale | **Avoided.** AIQ inherits the quality scale, so with quality in [0,1] AIQ is in [0,1] and the units are interpretable as "average quality across the cost range". | **Avoided as reported.** RouteLLM states APGR is bounded in [0,1]. A single-alpha PGR can go negative if the router underperforms the weak model, but the reported statistic is the integral and the paper bounds it. |
| (3) Winner's-curse-biased floor from post-hoc max over k noisy scores | **Avoided.** No max-over-k term appears in AIQ. The NDCH is a reference *curve*, and it is a hull over the individual models rather than a maximum entering a denominator, so selection bias in the hull shifts the comparison line, not the metric value. | **Avoided.** k = 2, endpoints designated in advance, no maximum taken. |
| (4) Chance-inflated oracle ceiling | **Not avoided, but not load-bearing.** RouterBench's Oracle Router is exactly a per-item max over k models and therefore carries A-02's defect (4) in full: on 4-choice multiple choice with zero-skill models it manufactures 1 - 0.75^k of apparent headroom. The difference that matters is that the oracle is a *reported reference line*, not a term inside AIQ. AIQ's value is unaffected. Adopt AIQ, do not adopt RouterBench's oracle line uncorrected. | **Avoided entirely.** APGR uses no oracle. Its upper endpoint is a real model's real score. |

### 3.3 Verdict

**Zero novelty, and none is being claimed.** This is a citation-and-replacement fix for A-02, not a contribution, and it should be written that way.

Concrete recommendation for §11.2: replace eta with **AIQ as the primary scalar** and **APGR plus CPT(50%) as the secondary pair**. AIQ is the only one of the three that avoids all four defects in its own value. Report the RouterBench oracle line only if chance-corrected, and say so. Restate falsifier F10's criterion as a numeric threshold on AIQ, which is **bounded under normalized quality (an inference, not a stated theorem, see §7 item 11) and defined whenever the candidate set spans a nonzero cost range**, instead of "recovering less than most of its pre-swap routing efficiency eta", which A-02 showed is unmeasurable when eta can be negative or undefined. An earlier revision of this sentence said "which is bounded and defined on every evaluation set", dropping the §7 hedge in the one sentence a reader acts on, and asserting a universality the formula does not have; `logos.tex` §11.2 now carries the common-cost-domain, defined-denominator and minimum-slice-size conditions that make the restated criterion computable.

Also worth adopting from RouterBench: the NDCH construction. It is exactly the "Pareto frontier" object the brief describes, and it already has a name, a definition and a benchmark with 405k outcomes behind it.

---

## 4. Ensembles of distilled siblings plus runtime adapters

### 4a. How much ensemble gain survives shared lineage?

**The load-bearing result.** *Deep Ensembles: A Loss Landscape Perspective*, arXiv:1912.02757, Fort, Hu, Lakshminarayanan; submitted 2019-12-05, revised 2020-06-25. Verbatim: "random initializations explore entirely different modes, while functions along an optimization trajectory or sampled from the subspace thereof cluster within a single mode predictions-wise", and "the decorrelation power of random initializations is unmatched by popular subspace sampling methods." The paper introduces a diversity-accuracy plane for exactly this comparison. It gives no correlation coefficients in the abstract and the numerics were not extracted.

This is the general form of the concern and it points against the design. Ensemble benefit is a function of error decorrelation; decorrelation comes from independent initialization; a ladder distilled from one parent on one corpus is the opposite of independent initialization.

**Distillation specifically does not carry diversity.** *Diversity Matters When Learning From Ensembles*, arXiv:2110.14149, Nam, Yoon, Lee, Lee; submitted 2021-10-27. Verbatim: "we empirically show that the typical distillation procedure does not effectively transfer such diversity, especially for complex models that achieve near-zero training error." Their fix is a perturbation strategy that seeks inputs where ensemble members disagree.

**Honest scope limit on that citation.** Nam et al. study distilling *an ensemble into one model*, not ensembling *multiple students of one teacher*. It supports the proposal's concern by analogy and by mechanism, not directly. Stating otherwise would be a C-02-shaped error (citing a real paper for an inference it does not make).

**What was searched for and not found.** Across the four search strings in §6.4, no paper was found that directly measures ensemble gain among N students distilled from one common parent LLM as a function of N, with the error-correlation matrix reported. Search-result summaries asserted the expected relationship in general terms, but no primary source stating it for distilled LLM siblings was located and fetched, so nothing is claimed from them.

**Distinguish the two negatives.** Mechanism 1's negative is now **narrow rather than strong**: fourteen strings plus four API queries across a subfield whose shape is known, and it found MatFormer, which claims and measures the property §1.2 originally called unclaimed (see the correction there). What the search supports is only that nobody varies depth under an explicit alignment objective. This negative is weaker. "Ensemble of distilled siblings" is a phrase with no standard name, so a paper could exist under vocabulary I did not guess. Do not write "nobody has measured this" without the qualifier.

**The finding that matters most here is internal, not external.** Mechanisms 1 and 4a are in direct tension. Mechanism 1 proposes an explicit training objective that *maximizes* representational agreement between ladder members so their KV projections are interchangeable. Mechanism 4a proposes to ensemble those same members for a gain that exists only insofar as their errors are *decorrelated*. Fort et al. is the reason to expect that shipping mechanism 1 shrinks the payoff from 4a, by construction and by the same knob. v0.3 should either state this tension and pick a side, or make it a falsifier: measure sibling error correlation before and after KV-alignment distillation, and predict the sign.

**Verdict.** The mechanism is not novel (ensembling siblings from a common parent is standard practice with a known theoretical objection). The unclaimed slot is a *measurement* whose expected result is negative for the design. That is a falsification target, not a contribution, and it should be written up as one.

### 4b. Multi-adapter serving: llama.cpp/GGUF versus vLLM

**llama.cpp, current state.** Fetched `github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md`. Per-request adapter selection **is** supported: the `/completion` endpoint takes a `lora` field of the form `[{"id": 0, "scale": 0.5}, {"id": 1, "scale": 1.1}]`. There are `GET /lora-adapters` (returns loaded adapters) and `POST /lora-adapters` (sets global scale). Adapters load via `--lora`, with `--lora-init-without-apply` to defer activation. Adapters not listed in a request default to scale 0.0, and the per-request `lora` field overrides the global scale.

The load-bearing sentence, verbatim from the README: **"requests with different LoRA configurations will not be batched together, which may result in performance degradation."**

That is the answer to the throughput question and it is structural, not a bug. llama.cpp applies adapters hot rather than merging, but it serializes across adapter configurations: N distinct adapters in flight fragment the continuous batch into N batches.

For context on how recent this is: the same repository's discussion #7850 (fetched) shows that as of mid-2024 runtime adapter swapping was an unmerged draft PR with a maintainer noting adapters must exclude token-embedding and norm tensors, and the Metal path was slow with buffer allocation errors. The capability is roughly two years old and the batching limitation has not been lifted.

**vLLM.** S-LoRA, arXiv:2311.03285, Sheng, Cao, Li, Hooper, Lee, Yang, Chou, Zhu, Zheng, Keutzer, Gonzalez, Stoica; submitted 2023-11-06, revised 2024-06-05. "S-LoRA stores all adapters in the main memory and fetches the adapters used by the currently running queries to the GPU memory", using Unified Paging over adapter weights and KV cache tensors plus "custom CUDA kernels for heterogeneous batching". Reported: throughput improved "by up to 4 times" over HuggingFace PEFT and vLLM, and the number of served adapters increased "by several orders of magnitude", serving "thousands of LoRA adapters on a single GPU or across multiple GPUs with a small overhead". The abstract does not quantify "small overhead" and no figure was extracted.

Fetched the current vLLM LoRA docs at `docs.vllm.ai/en/latest/features/lora/`. They state adapters "can be efficiently served on a per-request basis with minimal overhead"; that requests are processed "in parallel with base model requests, and potentially other LoRA adapter requests if they were provided and `max_loras` is set high enough"; and that `max_lora_rank` should be "set to the maximum rank" among adapters because "using a value much larger than needed wastes memory and can cause performance issues". **Honest status: the vLLM docs contain no quantitative throughput benchmark for LoRA-on versus LoRA-off.** The "minimal overhead" claim is vendor documentation, Tier-B by the paper's own labelling scheme, and should be labelled that way if quoted.

**Verdict.** Fully answered, zero novelty, and the answer is favourable to the design for a reason worth stating precisely: the llama.cpp limitation is a *multi-tenant batching* limitation. On an edge deployment of a 277M model at batch size 1, there is no batch to fragment, so the documented degradation does not bind. It binds only if the ladder is served multi-tenant, in which case vLLM's heterogeneous-batching kernels are the published answer and llama.cpp is the wrong engine. v0.3 should say which regime it is claiming, because the two have opposite conclusions from the same evidence.

---

## 5. Ranking by residual novelty

**1. KV-cache-aligned distillation across a size ladder.** Residual novelty, **downgraded** and narrower than an earlier revision of this line claimed, but still the only one of the four with any. Ten adjacent papers exist and must be cited; two of them (ICaRus, PrefillShare) get the same interchangeability property by a cheaper route and are four to five months old; one (DroidSpeak) shows alignment is imperfect between same-size siblings of one foundation, and is **not** a cross-size negative; and one (MatFormer) **claims and measures the cross-size property in its main text and Appendix C.1**, at constant depth. The words "latent and unexploited" were used here and are withdrawn. What is left unclaimed is **differing depth plus an explicit learned alignment objective**, and nothing else. It remains the highest-value item and it carries the largest C-04 exposure of the four, which is exactly the exposure this correction is an instance of.

**2. Ensembles of distilled siblings (4a only).** Thin residual novelty, of the wrong sign. Nobody found measuring ensemble gain versus N for LLM siblings of one parent, but Fort et al. and Nam et al. both predict the answer is small, and mechanism 1 would make it smaller still by design. Publishable as a falsifier and a recorded tension, not as a contribution. Ranked second only because a genuinely unmade measurement exists here and does not exist in items 3 and 4. Part (b), multi-adapter serving, has zero novelty and is a settled engineering question.

**3. Cost-quality Pareto frontier as a routing metric.** Zero novelty, low risk. AIQ and APGR/CPT are established, named, benchmarked metrics. This is a repair for A-02 and should be presented as adopting standard practice, which is a strength, not a weakness. Ranked above item 4 only because adopting it carries no risk of appearing to claim a known result, whereas item 4 does.

**4. Looped forward pass with a learned exit.** Zero novelty and the highest C-04 recurrence risk of the four. The mechanism runs from Graves 2016 through Universal Transformers to Geiping, MoR and Ouro. The specific distinction the brief asks to be "established" is already established twice with numbers: Saunshi et al. with an iso-FLOP ablation showing looping *loses* on closed-book QA while winning on math word problems, and Ouro stating at 1.4B/2.6B scale that the advantage "stems not from increased knowledge capacity, but from superior knowledge manipulation capabilities." A paper published seventeen days ago (2607.20519) further finds that learned halting gates are often matched or beaten by post-hoc confidence readouts. Cite all of it, claim none of it.

---

## 6. Search terms used

Listed so the negatives are auditable. All run 2026-07-25 via WebSearch unless marked as an arXiv API query.

### 6.1 Mechanism 1
1. `KV cache sharing across different models cross-model KV cache reuse`
2. `KV cache distillation align key value projections across model sizes small model prefill large model`
3. `cascade inference shared KV cache small model large model skip re-prefill`
4. `speculative decoding draft model target model share KV cache same key value projections`
5. `Minitron Nemotron structured pruning depth pruning preserve KV cache layout distillation model family`
6. `"KV cache" reuse across models of different sizes same family cross-scale cache transfer`
7. `MatFormer Flextron elastic nested transformer submodels extracted one parent shared weights KV cache`
8. `LayerSkip early exit shared KV cache self-speculative decoding skip re-prefill larger model`
9. `knowledge distillation align key value cache representations student teacher attention KV alignment loss interchangeable`
10. `"cache-compatible" OR "KV-aligned" OR "cache-aligned" distillation model ladder student teacher shared cache no re-prefill`
11. `prefill with small model decode with large model KV cache handoff avoid recomputation model cascade`
12. `escalate to larger model reuse prefill KV cache without recompute routing quality escalation LLM serving 2026`
13. `distillation train student to match teacher key value projections so caches are interchangeable across depth`
14. `arxiv 2026 KV cache interchangeable across distilled model sizes ladder progressive distillation shared attention cache`

arXiv API queries (`export.arxiv.org/api/query`, sorted by submittedDate descending):
- `all:"KV cache" AND all:"distillation" AND all:"model family"`
- `abs:"KV cache" AND abs:"different sizes"`
- `abs:"KV cache" AND abs:"reuse" AND abs:"across models"`
- `abs:"KV cache" AND (abs:"smaller model" OR abs:"larger model") AND abs:"distill"`

### 6.2 Mechanism 2
1. `Mixture-of-Recursions looped transformer adaptive depth learned exit recurrent depth latent reasoning`
Direct fetches of the six lineage papers followed from that one search plus prior knowledge of the lineage; the reasoning-versus-knowledge question was answered by fetching 2502.17416 (abstract and HTML v1) and 2510.25741 directly rather than by further searching, because both were already identified.

### 6.3 Mechanism 3
1. `FrugalGPT LLM cascade cost quality tradeoff metric accuracy at fixed cost area under cost-accuracy curve routing evaluation`
Followed by direct fetches of 2305.05176, 2403.12031 (abstract and HTML v2), 2406.18665 (abstract and HTML v4), 2410.10347.

### 6.4 Mechanism 4
1. `ensemble diversity distilled students same teacher correlated errors ensemble gain reduced shared lineage`
2. `ensemble of student models distilled from same teacher diminished gain error correlation empirical study`
3. `llama.cpp GGUF multiple LoRA adapters runtime hot-swap versus vLLM multi-LoRA batched throughput overhead`
4. `llama.cpp server lora-adapters endpoint per-request lora scale 2026 multi adapter batch support`
Plus direct fetches of 1912.02757, 2110.14149, 2311.03285, the llama.cpp server README on master, llama.cpp discussion #7850, and the vLLM LoRA docs.

---

## 7. What was NOT searched, and what was not fetched

Stated plainly, per the standard `REVIEW_ROUND2.md` §8 sets.

**Not searched at all:**

1. **Non-English literature.** No Chinese-language venues, no `kexue.fm`-class technical blogs, no WeChat or Zhihu technical posts. Given that C-06 in round 2 already turned on a Chinese-language primary source that could not be fetched, and that several of the most relevant labs here (Moonshot, DeepSeek, Qwen) publish substantively in Chinese first, this is the largest single blind spot in this document, and it bears most on mechanism 1.
2. **Patents.** No USPTO, EPO or WIPO search on any of the four mechanisms. KV-cache reuse across model variants is exactly the kind of serving optimization that gets patented before it gets published, and NVIDIA, Google and Microsoft are all active in the adjacent space. A patent that reads on mechanism 1 would not have surfaced in any search run here.
3. **Closed-lab internal practice.** Whether OpenAI, Anthropic, Google or Meta already ship cache-interchangeable model ladders internally is unknowable from public sources and was not attempted.
4. **Vendor engineering blogs beyond LMSYS.** No systematic sweep of the NVIDIA, vLLM, SGLang, TensorRT-LLM, HuggingFace or Modal blogs. DFlash was found through a search hit, not through a sweep, which means comparable posts elsewhere plausibly exist and were missed.
5. **OpenReview submissions under review.** No search of ICLR 2027 or NeurIPS 2026 submission pools. Given the pace of the KV-cache subfield in 2026, an anonymous submission on mechanism 1 is plausible and would not appear anywhere searched here.
6. **Code without papers.** No search of GitHub, so an implementation of mechanism 1 shipped without a write-up would not have been found.

**Searched but resolved only to a secondary source, so not usable as evidence:**

7. **LayerSkip's KV-cache mechanics.** The claim that LayerSkip "reuses KV-cache from draft stages" came from a search-result summary, not from the fetched abstract page, which says only "shared compute and activations". Read the full paper before v0.3 relies on it.
8. **Minitron's attention layout.** Whether width pruning preserves `num_key_value_heads` and `head_dim` is not answerable from the abstract page and was not resolved. It is directly load-bearing: if Minitron-style pruning changes the KV head count, then the constant-KV-shape property that motivates mechanism 1 does not survive that particular ladder construction. Read the full paper.
9. **MoR's numerics.** Perplexity, accuracy and throughput figures are not in the abstract and were not extracted. The claims about MoR above are qualitative only.
10. **Fort et al.'s correlation numbers.** The diversity-accuracy plane results were not extracted; only the two verbatim qualitative statements from the abstract are used.
11. **RouterBench's AIQ boundedness.** The fetch reported the metric "is not explicitly bounded in the paper", with [0,1] following implicitly from normalized quality. §3.2's boundedness row rests on that inference, not on a stated theorem.
12. **S-LoRA's "small overhead".** Unquantified in the abstract, not extracted from the body.
13. **vLLM's LoRA throughput cost.** The documentation makes a qualitative "minimal overhead" claim with no benchmark. No quantitative figure for LoRA-on versus LoRA-off throughput in vLLM was located. Anyone repeating "minimal overhead" is repeating vendor documentation.

**Papers that appeared in search results and were NOT fetched.** None of these support any verdict above and none should be cited from this document: Flextron, AmoebaLLM, SortedNet, KVCOMM, KaVa (2510.02312), KV-Distill (2503.10337), KVSculpt (2603.27819), Punica, *Efficient Multi-Adapter LLM Serving via Cross-Model KV-Cache Reuse with Activated LoRA* (2512.17910), *Efficient Reasoning on the Edge* (2603.16867, seen only as an arXiv API summary), *What Makes Looped Transformers Perform Better Than Non-Recursive Ones* (2510.10089), SkipV1Former (2510.16807), Cross-Layer Attention (2405.12981). Item 2512.17910 in particular looks like it could matter to mechanism 1 and 4b both, and was not read.

---

## 8. Primary sources fetched

Twenty-eight rows recording thirty-one fetch events (three rows record two fetches each: an abstract page plus an HTML rendering). Every claim in §§1-5 traces to one of these. An earlier revision headed this table "Twenty-one fetches", which matched neither the row count nor the event count.

| Source | What was fetched | Used for |
|---|---|---|
| arXiv:2407.21783 (ar5iv HTML) | Table 3, §3.1 GQA sentence | §1.1 enabling fact |
| arXiv:2411.02820 | abstract page | §1.2 DroidSpeak |
| arXiv:2602.12029 | abstract page | §1.2 PrefillShare |
| arXiv:2603.13281 | abstract page | §1.2 ICaRus |
| arXiv:2510.03215 | abstract page | §1.2 C2C |
| arXiv:2605.22863 | abstract page | §1.2 LCF |
| arXiv:2606.07684 | abstract page | §1.2 SCD |
| arXiv:2404.16710 | abstract page | §1.2 LayerSkip |
| arXiv:2310.07707 | abstract page | §1.2 MatFormer |
| arXiv:2408.11796 | abstract page | §1.2 Minitron |
| lmsys.org DFlash blog, 2026-06-15 | full post | §1.2 DFlash |
| arXiv:1603.08983 | abstract page | §2.1 ACT |
| arXiv:1807.03819 | abstract page | §2.1 Universal Transformers |
| arXiv:2502.05171 | abstract page | §2.1 recurrent depth |
| arXiv:2507.10524 | abstract page | §2.1 MoR |
| arXiv:2510.25741 | abstract page | §2.1, §2.2 Ouro |
| arXiv:2502.17416 | abstract page + HTML v1 | §2.2 dichotomy and numbers |
| arXiv:2607.20519 | abstract page | §2.3 halting gates |
| arXiv:2305.05176 | abstract page | §3.1 FrugalGPT |
| arXiv:2403.12031 | abstract page + HTML v2 | §3.1 AIQ, NDCH |
| arXiv:2406.18665 | abstract page + HTML v4 | §3.1 PGR, APGR, CPT |
| arXiv:2410.10347 | abstract page (no metric found) | §3.1 search closure |
| arXiv:1912.02757 | abstract page | §4a Fort et al. |
| arXiv:2110.14149 | abstract page | §4a Nam et al. |
| arXiv:2311.03285 | abstract page | §4b S-LoRA |
| llama.cpp `tools/server/README.md` (master) | LoRA section | §4b batching limitation |
| llama.cpp discussion #7850 | full thread summary | §4b historical context |
| docs.vllm.ai LoRA features page | full page | §4b vLLM state |
