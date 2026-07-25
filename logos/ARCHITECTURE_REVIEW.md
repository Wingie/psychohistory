# Architecture review, the 10T Mixture-of-Towers, and where it does not close

> ## Read this first: this is SELF-REVIEW, not independent review
>
> This document was written by the same authoring process that wrote `logos.tex`. It is not an outside referee report and must not be cited as one. **The independent pass is [`logos/REVIEW_ROUND2.md`](REVIEW_ROUND2.md)** (2026-07-25), which audited this document alongside the paper and returned forty-six surviving findings, two of them CRITICAL.
>
> Round 2 named four classes of defect that the method used here was structurally unable to catch. All four are present in this document:
>
> 1. **A citation that resolves, is real, is quoted accurately, and supports the opposite of the inference drawn from it.** Round-2 finding C-02, CRITICAL: both debate papers are cited in `logos.tex` for a diversity claim that both explicitly disclaim, and the claim is printed in the abstract. Verifying that a citation exists and is quoted correctly cannot detect this. It collapses the only architectural item in the paper's own list of three original contributions, and this review passed over it entirely.
> 2. **A claim with no citation at all.** A citation-checking method sees nothing where there is nothing to check. `logos.tex:94`, the token-supply premise the entire data wall rests on, carries no citation and no number; `logos.tex:172`, one of two enumerated motivations for the tower split, asserts a measurement with no source. Neither is listed here or in `BIBLIOGRAPHY_REVIEW.md`.
> 3. **A derivation this document reproduced rather than audited.** F-01 below computes `N_act ≈ 5e10` from the expert fraction and treats it as ground truth. Round-2 finding A-01 shows that method understates by 1.54x on Kimi K2 and 1.76x on DeepSeek-V3, the only two shipped models where ground truth exists, because it ignores always-active attention, embeddings and shared experts. F-01's diagnosis is right and its input is wrong. Defensible range: 6.4e10 to 9.1e10 active parameters.
> 4. **An entire artefact never opened.** `grep -i 'substrate b|psychohistory|validation/'` over this document returns zero matches. The psychohistory validation suite is the adjudicator that falsifier F9 depends on, and it had received no referee pass from this document at all. Round 2 opened it and found CRITICAL and HIGH defects there.
>
> Nothing below has been softened in response. The findings round 2 confirmed as real fixes (F-01, F-03, F-06, F-07) stand. The severity-index labels round 2 showed to overstate what `logos.tex` delivers have been re-graded in place, and every correction is attributed inline to its round-2 finding ID.

**Audit date:** 2026-07-25. **Stance:** adversarial. This document is the referee report the paper would get *from its own author*. It is organised by severity, not by section order.

The short version: **the architecture is buildable and the individual mechanisms are real, but three of its load-bearing arguments are arithmetically or logically wrong as originally stated, and two components are in the wrong place.** All five are fixable, and the corrected versions are in `logos.tex` draft v0.2. Four findings are *not* closed by v0.2 (F-04, F-13, F-14, F-15) and two are closed only in part (F-09, F-10); see the re-graded index below. The single risk that cannot be closed by argument at all is the BAR extrapolation (F-04), which needs a training run.

---

## 0. Severity index

Section numbers refer to `logos.tex` **draft v0.2**, in which every finding below was addressed.

| # | Finding | Severity | Resolution in v0.2 |
|---|---|---|---|
| F-01 | Dense compute arithmetic applied to sparse towers, a 55× error | **CRITICAL** | **Fixed**, §2.2, Prop. 1, Table 1 |
| F-02 | Token fragmentation argument is arithmetically false as stated | **CRITICAL** | **Fixed**, §2.3, Prop. 2 |
| F-03 | Regulatory argument built on the wrong FLOP number | **CRITICAL** | **Fixed and promoted**, §13.2 + Conjecture 3 |
| F-04 | BAR extrapolated 400× with no hedge | **HIGH**, unresolvable by argument | **Named, still unhedged.** §3.3, falsifier F2. The central bet |
| F-05 | 10T vs 14T slides between sections | **HIGH**, it breaks F-03 | **Fixed**, §2.4, threshold predicate |
| F-06 | RQ-VAE codebook placed in the hidden-state path | **HIGH** | **Relocated**, §8.3 |
| F-07 | Latent dispatch claimed as confidentiality protection | **HIGH** | **Withdrawn**, §9.1 Remark 5 |
| F-08 | Canary AUROC 1.0 generalised beyond its adversary model | **HIGH** | **Bounded**, §10.1 + Conjecture 2, falsifier F8 |
| F-09 | Master router is an unanalysed single point of failure | **MEDIUM** | **Designed, untested**, §4. Bandit training signal, verifiability asymmetry, failure ladder, descriptor warm-start, post-routing mask. §4.3 states only that the warm start is *measurable* at 1B scale, so router drift under tower swap is deferred to falsifier F10, not closed (round-2 X-07) |
| F-10 | No fault tolerance or straggler analysis anywhere | **MEDIUM** | **Solved for three of four paths**, §11.3: tower unreachable, sticky owner lost, straggler in expert dispatch. The fourth gap named in the F-10 body below, the FaaSMoE cold-start budget, is not in §11.3; `logos.tex:438` defers it to falsifier F7 instead (round-2 X-17) |
| F-11 | Truncated and reconstructed formulas | **MEDIUM** | **Labelled as reconstructions**, §5.3 Remark 3 and §9.2 |
| F-12 | No cost model, no evaluation method for a composed ensemble | **MEDIUM** | **Solved**, §11.1 and §11.2. Cost model plus routing efficiency η |
| F-13 | Petals analogy imported without checking it transfers to MoE | **LOW-MED** | Partial. §9.1 keeps the topology and drops the confidentiality claim; the sparse-dispatch cost model is still not re-derived |
| F-14 | Domain partition asserted, never justified | **LOW-MED** | **Criterion supplied, partition still unmeasured**, §3.4. A three-axis criterion, which says **four towers, not five**, and §3.4 itself closes with "a data question we can specify but have not run". F-14's actual complaint, no ablation and no clustering evidence, is unanswered: an argued partition is not a measured one, and Table 1 still prints five (round-2 X-17) |
| F-15 | Prop. 2 requires overlapping corpora while §13 treats towers as clean residency partitions | **MEDIUM**, found late | **Contradiction resolved, consequence unquantified**, §11.4. Split by residency class, and the headroom "shrinks" by an amount §11.4 concedes it does not bound. Let `f` be the residency-bound corpus fraction: the system needs `56T × (1 + 4f)` unique tokens, so at `f = 1` the headroom is exactly zero, and `f` is bounded nowhere in the paper (round-2 X-04, X-17) |

**F-04, F-13, F-14 and F-15 are not closed, and F-09 and F-10 are closed only in part.** F-04 cannot be closed by argument, only by a training run. F-14 and F-15 need measurements (corpus overlap, residency fraction) that no falsifier in the §15 table covers.

---

## 1. CRITICAL, the arithmetic

### F-01 · The dense/sparse category error

The draft argues:

> "the pretraining compute required ... for a dense 10T model is estimated by C ≈ 6ND, yielding approximately 1.30×10^28 FLOPs" → therefore go sparse
> ... and then the table lists **"Monolithic Dense 2.8 Trillion → 9.40×10^26 → Nearing Upper Limit of Global Compute"**

But **the towers are not dense.** Kimi K3 is 2.8T total with 16 of 896 experts active: roughly 5×10^10 active parameters. The correct estimator for a sparse model is `C ≈ 6·N_act·D`, giving:

```
6 × 5e10 × 5.6e13 ≈ 1.7e25 FLOPs
```

That is **55× smaller** than the number in the table, and it is not "nearing the upper limit of global compute": it is a training run that demonstrably happened, since the model exists and shipped.

> **The `5×10^10` above is itself wrong, and this review did not audit it (round-2 A-01, HIGH).** It is not a vendor figure; it is `(16/896) × 2.8e12`, which assumes 100% of parameters are routed-expert parameters. Applied to the only two shipped models with published active-parameter counts, the same method understates by **1.54x** (Kimi K2: gives 2.08e10 against an actual 3.20e10) and **1.76x** (DeepSeek-V3: gives 2.10e10 against an actual 3.70e10), because always-active attention, embeddings, the LM head and shared experts are invisible to the expert fraction; on V3 those are 34.65% of active parameters. Moonshot has published no comparable single figure for K3. Sweeping the always-on fraction over [0.5%, 1.5%] gives `N_act` in **[6.4e10, 9.1e10]**, so `C` per tower is 2.15e25 to 3.06e25 and the "55×" is 31x to 44x. The direction of F-01 is unaffected and Proposition 1 survives. What does not survive is the regulatory sentence at `logos.tex:619`: the tower clears 1e25 by 2.2x to 3.1x, not "by less than a factor of two".

**Why this matters beyond pedantry:** the whole rhetorical structure of the paper is "dense is impossible → therefore MoT." If sparse 2.8T is comfortably achievable, the motivation for the *tower* decomposition has to come from somewhere else, and it does (unique-data supply, modular update cost, alignment isolation, serving memory). The argument survives; the version given does not.

**Fixed:** `logos.tex` §2.2, Proposition 1, and Table 1 now separate the estimators.

---

### F-02 · The token fragmentation fallacy

The draft:

> "By decentralizing the parameter count, the token burden is fragmented. A single 2.8T tower requires a much more achievable 56 trillion tokens ... the system completely bypasses the monolithic token starvation limit."

**5 towers × 56T = 280T token-instances > 216T for the monolith.** Fragmentation consumes *more* tokens in aggregate, not fewer. Fragmentation cannot create data.

The argument is rescuable, and the rescued version is strictly more interesting:

> What decomposition buys is a reduction in the **peak unique-corpus** requirement per independently optimised model: from `D_opt(N_total)` to `max_i D_opt(N_i)`, because the tower corpora `C_i` may overlap arbitrarily. Re-reading a corpus costs compute, and per F-01 compute is not the binding constraint.

Domain specialisation then widens `|∪ C_i|` without any single tower needing to see all of it. **That** is the data-wall argument.

**Residual weakness that survives the fix:** `D_opt(N) = 20N` is a dense law being applied to sparse `N_total`. The MoE scaling literature says the optimal token-per-parameter ratio for sparse models is neither 20 nor constant in scale. The 56T number is an order-of-magnitude placeholder and should never be quoted as a budget.

**Fixed:** §2.3, Proposition 2. Made falsifier **F1**.

---

### F-03 · The regulatory argument rests on a borrowed number

The draft's governance section:

> "A 10T MoT model trained on 56 trillion tokens utilizes compute several orders of magnitude above this threshold (1.30×10^28 FLOPs)"

1.30×10^28 is the **dense monolithic 10T** figure from six sections earlier. It has nothing to do with the MoT. Correct ensemble figure is ~8.4×10^25: still above the 10^25 threshold, but by **~8×, not by "several orders of magnitude."**

That difference is not cosmetic. It changes the answer to the only question that matters here: *a slightly sparser tower falls below the threshold entirely.* Which exposes the real finding:

> **The EU AI Act's 10^25 FLOP presumption is written against "a model." A Mixture-of-Towers has no settled answer to "how many models is this."**

Three readings, all defensible from the text:
- **R1 per-tower:** each tower at ~1.7×10^25 is individually in scope, but by under 2×.
- **R2 composed-system:** ~8.4×10^25, in scope.
- **R3 router-only:** the provider trained only the router (~10^20 FLOPs). Under this reading the composed system is *integration of third-party models*, not a model the integrator trained, and BAR's entire economic proposition is that towers are sourceable and swappable.

R3 is the arbitrage. It falls straight out of reading the threshold next to any modular-composition paper.

**Fixed and promoted:** §13.2 and Conjecture 3 (*modular composition is a compute-threshold arbitrage surface*). This is now the paper's strongest original contribution: it came out of chasing down a wrong number.

---

## 2. HIGH

### F-04 · The BAR extrapolation is 400× and unhedged

BAR is demonstrated at **7B with 4 experts**, achieving 49.1 vs 47.8/50.5 retraining baselines. The architecture applies it at **2.8T with 5 towers**.

Nothing in the published result licenses this. And the specific failure mode to expect gets *worse* with scale, not better:

> When experts are weak and narrow, a misroute is cheap. When each expert is itself a frontier model, a misroute costs the full quality delta between two frontier models, and the router is trained on orders of magnitude less signal than any tower it dispatches to.

Note also that BAR's own headline is *matching* a retraining baseline (49.1 vs 50.5 with mid-training), i.e. modularity buys update economics, **not quality**. The paper should not be read as claiming MoT is better than a monolith; it claims it is *affordable to maintain*.

**Status:** cannot be resolved by argument. Named as falsifier **F2**, BLOCKED on training compute. This is the architecture's central bet and it is unhedged.

---

### F-05 · 10T vs 14T

The title, the class definition, and the scaling section say **10T**. The architecture is **5 × 2.8T = 14T**, and the draft's own table says "14 Trillion (Total)" in a row headed by a section that calls it 10T.

This is not a rounding complaint. Given F-03, the difference between 10T and 14T is the difference between two regulatory answers, and sliding between them makes the compliance question unanswerable.

**Fixed:** "LOGOS-class" is now a **threshold predicate** (≥10T total), and the reference architecture is described throughout as a 14T ensemble. §2.4.

---

### F-06 · The RQ-VAE codebook is in the wrong place

The draft puts a **shared residual-quantized codebook in the multi-tenant serving path**, discretising continuous hidden states, and then defends the placement with a real pathology (dimensional collapse, 4–10 effective dims) and a real fix (DCVQ).

The pathology and the fix are both correctly cited. **The placement is not supported by any of the cited sources.** RQ-VAE and semantic-ID quantization are established for *generative retrieval and recommendation* (TIGER), where discrete hierarchical IDs **are** the interface. None of the cited work puts a shared codebook in an LLM's hidden-state path, and there is no argument in the draft for why it belongs there, the collapse discussion is doing the work that a motivation should be doing.

**Steel-man adopted in the paper:** restrict the codebook to the two positions where discrete identifiers genuinely *are* the interface, 
1. the retrieval / long-term-memory layer (semantic IDs indexing tenant corpora), and
2. the router's discrete tenant-scoped index.

In both, collapse + DCVQ apply exactly as described. In the hidden-state path they are a solution looking for a problem.

**Fixed:** §8.3, made falsifier **F5**. The check that matters is on *real* hidden states, which the harness of §12 produces as a by-product; a synthetic-latent version would be circular.

---

### F-07 · Latent dispatch is not confidentiality

The draft:

> "Crucially, to protect the proprietary integrity of the RQ-VAE codebooks and the core routing logic, this Petals-like network operates strictly after the encoding and primary MoE routing layers."

and then dispatches "dense, continuous latent vectors ... into the untrusted peer-to-peer network."

This conflates two things. Keeping the tokenizer, router, and codebook inside the trust boundary is a real **anti-replication** benefit: those are the components an adversary needs to *clone* the system. It is **not a confidentiality benefit for user content**: intermediate representations are routinely invertible to substantial fractions of their input text, and a peer that sees latents across many requests is strictly better off than one that sees none.

Any deployment handling regulated data must treat the peer network as an **untrusted processor with full visibility**. That is a data-protection posture (contracts, jurisdiction, DPAs), not a cryptographic one. Getting this wrong in a paper that also has a GDPR/AI-Act compliance section is the kind of error that propagates into a real deployment.

**Fixed:** §9.1 Remark 5. Benefit retained, confidentiality claim withdrawn.

---

### F-08 · The canary result is generalised past its adversary model

`arXiv 2607.19490` genuinely reports **AUROC 1.0 across 408 configurations**, correctly ranking the malicious shard above every benign shard on every canary. That is a strong result and it is real.

It is also narrow. Three properties of the evaluated setting do not hold in this architecture:

1. **Duty cycle.** A shard tampering on *every* pass corrupts every canary and is trivially separable. An adversary tampering with probability `p ≪ 1` corrupts a given canary with probability `p`; with `m` canaries, detection probability is `1 − (1−p)^m`, and time-to-detection grows as `1/p`. For the realistic threat: subtly biasing a fraction of code-generation outputs, an adversary can sit below any interactive-latency observation budget.
2. **Numerics heterogeneity.** The benign null is set by hardware drift. A network deliberately spanning heterogeneous accelerators, **mixed MXFP4/NVFP4 quantization (this paper's own §7)**, and independently compiled kernels has a null that is wider, multi-modal, and node-dependent. A single pooled null then over-covers the tampering signal. Note this architecture *creates* the problem in §7 and then relies on a detector that assumes it away in §10.
3. **Semantic vs value-space tampering.** The detector measures activation drift. An adversary running a legitimately-quantized variant of the assigned expert produces drift that is *in-distribution for the benign null* while changing the output.

**Conjecture (ours, testable now):** AUROC falls monotonically in `1/p`, and there exists `p*` below which it is indistinguishable from 0.5 at any `m` compatible with interactive latency; widening the null for heterogeneous numerics raises `p*`.

**Status:** falsifier **F8**. Needs a benign null *measured* across two accelerators of different models; a matched pair only reproduces the published setting. **We expect this one to fire against our own architecture.**

---

## 3. MEDIUM

### F-09 · The master router is unanalysed

The architecture's entire behaviour funnels through one RL-tuned master router, and the draft says almost nothing about it. Open questions, none addressed:

- **Training data.** What supervises the router? Tower-attributed end-task reward requires having already served the query five ways. Where does that data come from at 2.8T-tower cost per sample?
- **Single point of capability failure.** Every tower's capability is gated by the router's willingness to reach it. A router bug is a silent capability regression across the whole system, invisible to per-tower evals.
- **Router drift vs frozen towers.** BAR's proposition is that towers are swapped independently. Every swap invalidates the router's learned dispatch statistics for that tower. Update cost is only linear if router retraining is cheap; nobody has shown it is at this scale.
- **Adversarial routing.** A user who can shape which tower serves them can steer around the Administration/safety tower. This is the same object as the compliance mask in §13.3, operated by the wrong party.

**Status, corrected (round-2 X-07).** The paragraph that stood here was a v0.1 status that survived the revision and flatly contradicted this document's own F-09 severity-index row. It read: "named in `logos.tex` §12 ('not addressed at all'), not solved. Should be P1 in `GAPS.md`." All three parts of that were stale. `grep -n 'not addressed' logos.tex` returns no match; §12 in v0.2 is "The observation bound", not the router; and `GAPS.md:88` already files the router under "Resolved since the last revision".

The v0.2 status is: **designed, untested.** `logos.tex` §4 (`sec:router`) answers all four open questions above: bandit feedback with a capability prior and an ε-slice supplies the training signal, the verifiability asymmetry (the router is well trained exactly where verification is cheap and badly trained everywhere else) is stated as a structural property rather than a tuning detail, the three-step failure ladder with a mandatory degradation flag covers single-point failure, descriptor warm-start covers router drift under tower swap, and the post-routing mask covers adversarial routing. None of it is measured. §4.3 claims only that the warm start is "measurable at the one-billion-parameter scale", which makes router drift falsifier F10 rather than a closed item, and §4.4 flags the mask-versus-quantile-balancer interaction as "a likely bug rather than a solved problem" (falsifier F6). Two of the five answers are therefore bets with a named test, not results.

### F-10 · No fault tolerance, no straggler analysis

A 5-tower, 64+-accelerator, multi-node, partly-P2P system with scale-to-zero serverless experts has:
- no discussion of what happens when a tower is unreachable (degrade? refuse? route to a fallback tower, with what quality contract?),
- no straggler mitigation for all-to-all expert dispatch, where p99 is set by the slowest peer,
- no cold-start budget for FaaSMoE scale-to-zero (the obvious killer at interactive latency; FaaSMoE is evaluated on **Qwen1.5-MoE-2.7B**, a 1000× scale gap),
- no failure semantics for the sticky KV owner going away mid-session: StateFlow pins state precisely so it never moves, which means losing the owner loses the session.

### F-11 · Truncated and invented formulas

- The sticky-owner selection objective in the draft is **literally truncated**: `o_s = arg min_{v ∈ P(e_s)} [`, the bracket never closes. The paper's version invents plausible weights (`λ_lat, λ_util, λ_mem`) and says so.
- The QB α/β formulas are a **reconstruction from a blog description**, presented in the draft as transcribed equations (see `BIBLIOGRAPHY_REVIEW.md` §4).
- The PiKV hash `s(t,e) = (t mod N_tok) ⊕ (e mod N_exp)`: verify against the paper before implementing; XOR of two independent moduli is not obviously a good hash and collides structurally when `N_tok` and `N_exp` share factors.

### F-12 · No cost model, no composed-ensemble evaluation methodology

The paper argues affordability throughout and never prices anything: no $/Mtok, no accelerator-hours, no comparison against serving one 2.8T model five times. And there is no stated methodology for evaluating a **composed** ensemble. The naive metric: max over towers, is exactly what a well-routed MoT should beat and a badly-routed one will not; without a router-attributed metric there is no way to tell a good MoT from a bag of models with a lookup table.

### F-13 · The Petals analogy may not transfer

Petals distributes **dense transformer layers** in a pipeline. This architecture distributes **sparse MoE experts**, where:
- activation is data-dependent, so peer load is unpredictable in a way Petals' is not;
- the all-to-all dispatch pattern is not pipeline-parallel and has very different network characteristics;
- expert weights are far larger per-unit than a dense layer slice, worsening cold start.

Adopting Petals' *topology* without re-deriving its *cost model* for sparse dispatch is unjustified. StateFlow + FaaSMoE do part of this work; the paper should not lean on "Petals-style" as though the transfer were free.

### F-14 · The domain partition is asserted

Code / Life Sciences / Mathematics / Logic / Administration is stated and never justified. Why five? Why these? "Mathematics" and "Logic" in particular are not obviously separable, and the routing literature's own finding is that complementarity is *empirical* and often counter-intuitive. A partition chosen by human intuition is exactly the thing MoE routing was invented to avoid. There is no ablation, no clustering evidence, no argument from data-distribution disjointness.

---

## 4. What is genuinely good about the architecture

An adversarial review that lists only faults is not useful. These parts hold up:

- **The bifurcated-deployment observation is sharp and correct.** Fable/Mythos being the same model differing only in attached classifiers is documented, and the recognition that **the containment mechanism is a router, not a refusal** is a real insight. It makes the safety classifier and the load-balancing router the same object under different objectives, which is what lets the compliance mask in §13.3 be a one-line change rather than a new subsystem.
- **The open-weights-as-incident-response-dependency argument is correct and non-obvious.** A defender analysing an exploit payload is indistinguishable from an attacker authoring one. Any stack whose only reasoning capacity is behind a third party's classifier has a governance dependency it did not choose. (Refined by the audit: Fable *demotes* rather than refuses, which is **worse** for the defender, you get a silently weaker answer and no signal that it happened.)
- **BAR is the right primitive** for the update-economics problem, and the linear-vs-quadratic argument is the paper's own, not ours.
- **The regulatory finding**, once the arithmetic is fixed, is the most valuable thing here.
- **The systems chain: KDA → recurrent state → prefix-cache incoherence → scheduler split** is a genuinely well-observed example of a modelling choice propagating into the scheduler, and it is documented end-to-end in primary sources.

---

## 5. Recommended structural change

The draft's argument order is *dense is impossible → MoT rescues it*. Given F-01 and F-02, that spine does not hold. The corrected spine, which is what `logos.tex` now uses:

1. Dense at 10T is impossible: on **unique data**, and on compute.
2. Sparsity removes the compute constraint entirely (Prop. 1). It does **not** remove the data constraint or the serving-memory constraint.
3. Tower decomposition attacks the **peak unique-corpus** requirement (Prop. 2) and buys linear update economics + alignment isolation.
4. 4-bit serving attacks the memory constraint.
5. What is left binding is **unique tokens, resident memory, and router quality**, and router quality is the untested bet.

This is a less dramatic story and a true one.
