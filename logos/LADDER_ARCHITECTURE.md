# The ladder architecture

**A revision of the Mixture-of-Towers as a domain x size grid under one explicit lineage-sharing parameter.**

Status: **SPECIFICATION. ZERO RUNS.** Nothing in this document has been trained, served, benchmarked or measured. Every number below is arithmetic over stated assumptions, or arithmetic over figures already carried in `../logos.tex` at that paper's own declared tier. Where a figure is an assumption it is labelled as one at the point of use. Where a claim needs a citation this document has not verified, it is marked **[NEEDS VERIFICATION]**; `PRIOR_ART_v03.md` is delivered and is where most of those were resolved or withdrawn, and the ones it did not cover are named as such at the point of use.

Companion documents: `../logos.tex` (the paper, and **the register of record wherever this document and it disagree**), `REVIEW_ROUND2.md` (the referee report this revision responds to), `ARCHITECTURE_REVIEW.md` (findings F-01 to F-15), `GAPS.md` (the work ledger, whose §4a carries the over-constraint result this document's §1.5 confronts), `PRIOR_ART_v03.md` (the prior-art sweep), `LOGOS_HARNESS.md` and `F9_PREREGISTRATION.md` (the observation-bound experiment, which is a different experiment from the one in §7 below and must not be conflated with it), `TIER0_3090_PLAN.md` (the priced Tier-0 rungs).

**Scope note.** This document owns the architecture. It does not restate the observation bound, does not touch the psychohistory validation suite, and takes no position on F9. It raises one finding that the paper has since adopted (§1), confronts the arithmetic that closes it against the design (§1.5), records the paper's now-three-case cost model (§5), records the retirement of one metric (§6), specifies one experiment (§7), specifies a measurement scaffold for narrowing the paper's central bet (§8), states the paper's thesis as a growth equation and makes its rate term a function of capability (§9), and states the case for consuming un-digitised archives visually (§10).

**What changed in this pass, so a reader of the previous draft is not misled.** Four things, and three of them are the paper overtaking this document rather than the other way round.

1. **L-01 is adopted.** The lineage parameter this document raised as a new finding is now `../logos.tex` §3.3, under the symbol `λ` on a three-point ladder. **The paper's ladder is the register of record**; §1.1's six-level ladder is retained here as an implementation-level refinement and §1.1 gives the mapping.
2. **Section numbers shifted.** Inserting §3.3 pushed the extrapolation to **§3.4** and the partition criterion to **§3.5**. Every cross-reference into the paper has been re-checked against the delivered file and two were wrong for reasons unrelated to the shift; §12 records them.
3. **`η` is retired, not demoted.** `../logos.tex` §11.2 states there is no residual question `η` answers that APGR does not answer better. The primary scalar is **AIQ**; the secondary pair is **APGR with CPT(50%)**. `REVIEW_ROUND2.md`'s A-02 recommended a `δ` guard on the denominator and keeping the metric; **that recommendation is superseded** and §6 is rewritten against the paper rather than against A-02.
4. **The over-constraint is new and it is the sharpest result in the programme.** `GAPS.md` §4a and `../logos.tex` §3.3 establish `f ≤ 1-g`, hence a unique-corpus requirement bounded by `5.6e13 * (5 - 4g)`, which is **2.8e14 at `g = 0`** and **6.05e13 at `g = 0.98`** against a central supply estimate near **6e13**, and **no setting of `g` satisfies X-04, C-02 and F-04 at once.** §1.5 confronts it. An earlier draft of this document said `f` was "unbounded anywhere in the paper"; that is false as of `../logos.tex` v0.3 and is withdrawn wherever it appeared.

There are now **fourteen falsifiers** in `../logos.tex` §15. **Seven run on one consumer accelerator** (F3, F4, F9, F10 as independent experiments; F5 and F13 limb (b) falling out of F9; F14 sharing an instrument with F13 limb (a), which runs on that card too but not as an F9 arm). **F11 and F12 need no accelerator at all.** F14 is new in v0.3 and it is the residue of L-01.

---

## 0. What this is, in one paragraph

`logos.tex` described five independently trained 2.8T towers behind a router. The revision here keeps the tower idea and adds a second axis: each domain gets a **distillation ladder** of sizes descending from one parent, and the size distribution is **asymmetric across domains**, matched to traffic and difficulty rather than uniform. Making the second axis explicit forced a question the paper had been answering inconsistently in four places without noticing, which is how much lineage the members share. That question is now `logos.tex` §3.3 and it is **the single master design parameter**; everything else in this document is downstream of where it is set. The architecture that results is cheaper to argue for than the one in the paper, because its central justification becomes a cost argument rather than a diversity argument, and cost arguments are checkable. It is also more exposed, because it concentrates the entire diversity budget in one place, and §7 specifies the experiment that would find out whether that budget exists at all.

**Two things have moved since that framing was written and they change what the document is for.** First, the lineage parameter turns out to be **over-constrained**: `f ≤ 1-g` means no setting of it satisfies the data-wall argument, the diversity conjecture and Branch-Adapt-Route at once (§1.5), so the architecture has to pick a corner rather than find a middle, and this document picks the corner that drops the diversity budget from the justification. Second, once the diversity argument is set aside, the binding quantity is the one `logos.tex` §12 already named: **the rate at which something outside the model can say that it is wrong.** §9 states that as a growth equation and makes its rate term a function of capability rather than a constant, and §10 argues that the largest available source of exogenous bits is not bootstrapping at all but **acquisition of content that was never digitised**. Those two sections are where the leverage now is, and neither of them is about towers.

---

## 1. Finding L-01: the paper assumed three different lineage regimes in four sections. It has since fixed this.

**ID namespace.** Round 2 used four stream prefixes: `A-` arithmetic, `C-` citations, `X-` consistency, `P-` psychohistory. This finding belongs to none of them, so it takes a new prefix, `L-` for lineage, to avoid collision. **L-01 is not in `REVIEW_ROUND2.md`.** It was raised here for the first time, and the reason it is not there is itself part of the finding (§1.3).

**Severity: HIGH. Status: ADOPTED into `../logos.tex` §3.3, and the residue is falsifier F14.** Four load-bearing passages assumed mutually incompatible amounts of shared lineage between towers. Each passage was internally sound. No two of them described the same system. The paper now names the parameter, prints the conflict as a table, resolves it against the diversity claim, and mints F14 for what the resolution costs. **This section is retained rather than deleted because the resolution has a price the architecture has to pay, and §1.5 is where this document pays it.**

### 1.1 The parameter, and the paper's version of it wins

Define **lineage sharing** as an ordered ladder of concrete commitments. It is an ordinal index over design choices, not a measured scalar, and it should never be reported as a number without naming the level:

| Level | Commitment | Shared |
|---|---|---|
| **L0** | Independent pretraining | Nothing. Separate init, separate tokenizer, separate corpora, separate objectives |
| **L1** | Shared tokenizer only | Vocabulary and token boundaries. Weights and init independent |
| **L2** | Shared dense seed, then fully divergent pretraining | Init. This is Branch-Train-MiX's actual setting |
| **L3** | Shared seed, shared attention and shared experts, divergent feed-forward | Init plus a merged subset of weights. This is BTX's merge target |
| **L4** | One base, divergent continued pretraining, weights fully separate afterwards | Init plus the entire pretraining run. Domain-adaptive continued pretraining |
| **L5** | One frozen base, divergence lives entirely in adapters | Everything except the adapters |

Two things move monotonically along this ladder and they move in opposite directions.

**Going up buys mechanism.** Weight merging needs a common seed. Hidden-state mixing needs a common latent space. Logit mixing needs a common tokenizer. Exact key-value tensor reuse needs identical layer geometry and closely related weights. Adapter batching over a frozen backbone needs one backbone. Every composition mechanism in §4 has a minimum level below which it does not function.

**Going down buys diversity and unique-data ceiling.** At L5 the members' errors are correlated by construction, because they share every weight that is not an adapter. At L0 the corpora may be genuinely disjoint and Proposition 2's union bound applies in full. Between them, the union shrinks as the shared fraction grows, which is the same algebra `logos.tex` §11.4 already does for residency fraction `f` and reaches the same shape of answer. §1.5 turns that observation into the arithmetic that decides the architecture.

**The paper's ladder, and the mapping.** `logos.tex` §3.3 names the same parameter as `λ` on three points rather than six, and gives the reason: what matters is where the discontinuities fall, not how finely the interval is subdivided. **The paper's ladder is the register of record and every claim in this repository should be stated on it.** The six levels above are an implementation-level refinement of the paper's three and map onto them as follows:

| This document | `logos.tex` §3.3 | Note |
|---|---|---|
| L0, independent pretraining | **`λ = 0`**, independent | Exact correspondence |
| L1, shared tokenizer only | `λ = 0` | The paper does not distinguish it, because a shared vocabulary buys no shared basis. Retained here only because logit mixing needs it and nothing else does |
| L2, shared dense seed then divergent pretraining | **`λ = 1`**, divergent branches | Exact correspondence. This is Branch-Train-MiX's setting |
| L3, shared seed plus merged attention and experts | `λ = 1`, at the high end | The BTX merge target. The paper folds it into `λ = 1` because the merge is what a branch is *for* |
| L4, one base, divergent continued pretraining | `λ = 1` to `λ = 2`, set by `g` | **This is where the parameter `g` of §1.5 lives**, and the paper's `g` resolves the interval the six-level ladder could only bracket |
| L5, frozen base, divergence in adapters only | **`λ = 2`**, shared corpus | The paper's `λ = 2` is "towers differing only in post-training", which contains the adapter case |

The one thing the six-level ladder still buys is §1.4's minimum-level table, because composition mechanisms fail at different points inside the paper's `λ = 1`. The one thing it obscures is that `λ = 1` is not a point but a segment parameterised by `g`, which is exactly what §1.5 is about.

### 1.2 Where the paper sat, and where it now sits

The conflict as this document found it, stated on the six-level ladder and with section numbers **as they now stand after §3.3 was inserted**:

| Passage | Assumed level | Evidence |
|---|---|---|
| **§3.5**, the partition criterion (P1 corpus disjointness) | **L0** | "Two towers drawing on the same corpus contribute nothing to it." The criterion is written as though corpora can be made disjoint by choosing domains, which requires independent pretraining |
| §3.2, Branch-Train-MiX and Branch-Adapt-Route | **L2 to L3** | "From a shared dense seed, training branches into asynchronous parallel runs." BTX merges feed-forward parameters into MoE layers and **averages shared self-attention weights**, which is only defined for models that started from one seed |
| §8.1, adapters over a frozen backbone | **L5** | "Freeze the backbone and map client data in through low-rank adaptation, with thousands of adapters batched over frozen experts by segmented gather kernels" |
| §12.3, the diversity conjecture (falsifier F13) | **L0** | "Towers pretrained on disjoint corpora under different objectives with different alignment histories differ in a way that persona-level heterogeneity does not capture" |

Four passages, three levels, no cross-reference between them, and no sentence anywhere in the paper naming the choice.

**The sharpest instance.** **§3.4** names Branch-Adapt-Route as "the architecture's central unhedged bet" at a 400x extrapolation, which is `ARCHITECTURE_REVIEW.md` F-04 and falsifier F2. But **BTX works because it branches from a common seed.** The asynchronous parallel branches it describes are branches *of one model*. Averaging self-attention weights across branches is a meaningful operation only because the branches are alignable, and they are alignable only because they share an init. So the paper's central bet is an **L2** method, and **§3.5** and §12.3 were simultaneously demanding **L0**. Those are not compatible. Either the towers are independently pretrained, in which case BAR is not the method being extrapolated and the 400x bet is on something else entirely, or the towers share a seed, in which case §3.5's "disjoint corpora" must weaken to **"common seed, divergent continued pretraining"** and §12.3's conjecture is about a weaker object than it claims.

**The resolution, as the paper made it.** `logos.tex` §3.3 resolves the conflict **against the diversity claim rather than against the method**, on the ground that Branch-Adapt-Route is the central bet of §3.4 and there is no version of this architecture without it. Verbatim from the paper: "independently trained towers" has to weaken to "one common seed, five divergent continued-pretraining branches", that is `λ = 1` and not `λ = 0`. Everything downstream of the diversity argument inherits the weaker object. Whether a branch is a large enough perturbation to carry the conjecture is not something the paper claims to know, and it is **falsifier F14**, which runs on the same instrument and the same card as F13's limb (a).

**What this document owes on top of that.** Two things the paper marks rather than asserts, and this document does not upgrade either: whether Branch-Adapt-Route *strictly* requires a common seed as opposed to being demonstrated on one is a reading of the source and not a quoted claim; and the same question for the BTX attention-averaging step is a stronger inference, believed sound because averaging weights across unaligned bases is a known failure. Both belong in the next prior-art sweep, together with the model-merging literature on permutation alignment, which is where a `λ = 0` merge would have to come from if one exists.

### 1.3 Why round 2 did not catch this

Round 2 ran four audit streams and every one of them read sections locally. Arithmetic checked the numbers inside §11. Citations checked whether §12's sources say what §12 says they say. Consistency checked whether §11.4's claim matches §3.2's claim **as claims**, which is a different operation from checking whether their *unstated premises* are compatible. Psychohistory read the validation suite.

L-01 is invisible to all four, because no single section contains an error. The defect is that §3.5 and §8.1 are each correct about a different system, and only a reader holding both in mind at once sees it. Per-section auditing is structurally blind to cross-section premise conflicts, and this document's own §5 finds a second instance of the same class in §11.1. That is a finding about the review method, and it is worth recording: **a review that partitions by stream and reads locally will pass a paper whose sections describe different systems.** The check that would catch it is a premise ledger, one row per load-bearing assumption, one column per section that relies on it, which nobody has built for this paper. `logos.tex` §3.3's Table 1 is the first row-set of exactly that ledger, built for one premise; the rest of the ledger does not exist.

### 1.4 The consequence that decides the architecture

Here is the result that makes the parameter unavoidable rather than merely tidy.

**No composition mechanism functions at L0.**

- Weight merging (BTX, model soups, task arithmetic) requires a common seed. **L2 minimum.**
- Hidden-state mixing requires a common latent space. Independent pretraining destroys it. **L3 minimum, and see §4.2.**
- Logit-level mixing requires a common tokenizer, because you cannot average distributions over different vocabularies. **L1 minimum.**
- Exact key-value tensor reuse requires identical layer geometry. **L5 in practice, see §2.3.**
- Adapter batching over one backbone requires one backbone. **L5.**

The only mechanism that survives at L0 is **selection**: pick one member per query, use its output verbatim, combine nothing. That is the cascade and the router, and nothing else. So the design space is not "how much lineage should we share", it is "we are above L0 or we have a router and no ensemble". The diversity argument wants L0 and every composition mechanism forbids it. **The architecture must sit strictly between**, and §1.5 is the arithmetic that says the interval is empty on a third axis the mechanism argument does not see.

### 1.5 The over-constraint: no setting of `g` works

**This is the sharpest result in the programme and it is the one the ladder specification has to confront rather than route around.** It is not this document's; it is `logos.tex` §3.3's arithmetic, collected in `GAPS.md` §4a, and stated here because it decides what the ladder is allowed to be.

Write `g` for the fraction of each tower's token budget consumed **before** the branch point. The seed corpus is shared by construction, so the residency-bound fraction `f` of `logos.tex` §11.4 cannot exceed the post-branch fraction:

```
f <= 1 - g
```

and §11.4's unique-supply requirement `5.6e13 * (1 + 4f)` is therefore bounded by

```
5.6e13 * (1 + 4f)  <=  5.6e13 * (5 - 4g)
```

**`f` is not a free parameter over `[0,1]`. Fixing the training plan fixes `g`, and `g` bounds `f` without anybody touching a corpus.** That is a real improvement on the state of the review: an earlier draft of this document, and `REVIEW_ROUND2.md` X-04, both recorded `f` as unbounded anywhere in the paper. **It no longer is, and that claim is withdrawn wherever it appeared here.**

Evaluated against the central unique-token-stock estimate of about `6e13` that `logos.tex` §11.4 reads Eq. (residency) against:

| `g` | Bound on unique-corpus requirement | Against a central supply near 6e13 | Lineage |
|---:|---:|---|---|
| 0.00 | **2.80e14** | 4.67x over. This is the undecomposed 14T monolith's requirement, so decomposition buys exactly nothing | `λ = 0` |
| 0.50 | 1.68e14 | 2.80x over | `λ = 1`, genuinely divergent |
| 0.90 | 7.84e13 | 1.31x over | `λ = 1`, shallow branch |
| 0.95 | 6.72e13 | 1.12x over | `λ = 1`, very shallow |
| 0.98 | **6.05e13** | 1.01x over, that is **at** the estimate | `λ = 1` pushed as close to `λ = 2` as it goes |
| 1.00 | 5.60e13 | 0.93x, under the estimate, and the towers are one model | `λ = 2` |

**The trilemma, stated as three demands on one number.**

- **X-04, the data wall**, needs `g` at or above about **0.98** for the decomposed requirement to reach the central supply estimate at all. Below that the token argument for towers is dead against that estimate.
- **C-02 and the diversity conjecture (F13, F14)** need `g` **low**. At `g = 0.98` the towers share 98 percent of their token budget and differ over the remaining 2 percent, which is the setting §3.2's `rho` table prices as having lost most or all of the ensemble gain. The conjecture is stated at `λ = 0` and F13's limb (a) explicitly rules out two finetunes of one checkpoint as an instrument, precisely because a shared checkpoint is suspected of destroying the treatment.
- **F-04, Branch-Adapt-Route**, forces `g > 0` at all, because BAR needs a common seed and there is no version of this architecture without BAR.

**No setting of `g` satisfies all three.** Raising `g` to rescue the data ceiling makes the towers more alike and makes C-02 worse. Lowering `g` to rescue the diversity claim puts the unique-corpus requirement up to 4.67x over the central supply estimate and removes the data-wall motivation entirely. Dropping BAR to escape the constraint removes the method F-04 is the extrapolation of, and with it the update economics that motivation (T1) is built on. **Three findings that were tracked separately are three views of one parameter, and fixing any one of them in isolation moves the other two.**

**The only branch on which both survive, and what it rests on.** Against the 90-percent **upper** supply bound of `2e14` rather than the central `6e13`, Eq. (residency) survives to `f ≈ 0.64`, hence to any `g ≥ 0.36`, which admits a genuinely divergent branch and leaves the diversity claim intact. So the trilemma is not a theorem about architectures. **It is a function of which token-supply estimate is believed, and nothing in this repository measures that number.** That is the honest statement and it is also the uncomfortable one, because it means the paper's most load-bearing constraint is inherited from a survey figure rather than derived.

**What the ladder specification must therefore do.** Three coherent responses exist. This document does not get to leave the choice open, so it makes one and records the other two.

1. **High `g`, no diversity budget.** Set `g` near 0.98, accept that the towers are near-replicas, **drop the diversity claim from the architecture's justification entirely**, and carry the architecture on §5's cost argument and §2.2's size axis, both of which survive untouched because neither uses ensembling. The system this leaves is one domain-general parent plus a size ladder, which is **exactly the collapse target §7.4 refutation condition 1 names**, reached here by arithmetic instead of by experiment.
2. **Low `g`, no data-wall motivation.** Keep the divergent branches and the diversity budget, and concede that tower decomposition does not convert an impossible unique-corpus requirement into a possible one against the central estimate. The architecture is then justified by cost (§5), serviceability (§9.2 of the paper) and alignment isolation, and the abstract's data-wall framing goes.
3. **Dispute the supply estimate.** Everything above turns on `6e13`. Establishing a defensible higher figure is a desk measurement, it is not budgeted anywhere in this repository, and **§10 is the one mechanism in this programme that would actually move it**, because the estimates count the digitised corpus and not the corpus.

**This document adopts response 1**, because it is the paper's own resolution (`logos.tex` §3.3 resolves against the diversity claim), because it leaves every checkable argument in this document intact, and because **this document's own §3.4** independently predicts that the ladder's alignment objective pushes `rho_bar` the wrong way. **Response 1 is a real loss and it should be written as one:** it removes the third motivation of `logos.tex` §3.1, which that section itself calls "the one we think matters most". It also makes §7 **more** decisive rather than less, because §7 is the cheapest way to find out whether response 1 costs anything real at all, and §10 is the only route by which response 3 becomes available.

---

## 2. The architecture

A **domain x size grid**, asymmetrically populated. The two axes are different objects and the difference is the whole design.

### 2.1 Domain axis: disjoint corpora, separate continued pretraining, no key-value reuse

Domains are separated by `logos.tex` **§3.5**'s criterion, unchanged: corpus disjointness, objective conflict, update cadence, separate on at least two of three. Each domain gets its own continued pretraining over its own corpus, from a common seed (L2 to L4 per §1.2's resolution, that is `λ = 1` in the paper's terms, with the position inside that segment set by `g` per §1.5). **`logos.tex` §3.5 now carries the two-axis statement itself**, in a subsection that says the domain axis has low lineage and no key-value reuse while the size axis has shared lineage and working reuse, and defers the full ladder specification to this file. So the axes below are the paper's as much as this document's; what remains this document's is the asymmetry (§2.4), the reuse correction (§2.3.1) and the serving regime (§2.3.2).

**No key-value reuse across domains.** Two domain parents that have diverged through separate continued pretraining hold representations that are not commensurable at any layer index. Their key and value tensors at layer `l` are projections through different weights of different training histories, and there is no reason for them to occupy the same subspace. Escalating a query from Code to Life Sciences therefore **re-prefills from scratch**, and that cost is real and must be priced into any cross-domain routing policy.

The domain axis is where the diversity claim lives, and it is the axis §7 tests.

### 2.2 Size axis: a distillation ladder from one parent per domain

Each domain parent at 2.8T distils down through a ladder. The reference ladder:

```
2.8T parent  ->  70B  ->  7B  ->  277M (edge)
```

Every tier in a ladder shares the parent's lineage by construction. There is no diversity here at all and none is claimed: the tiers exist to make cost a routable variable, not to disagree with each other.

**The size axis is nearly free in parameters.** Adding 70B and 7B tiers to a 2.8T parent costs `77e9 / 2.8e12 = 2.75%` extra parameters. Adding the 277M edge tier as well brings it to `2.760%`. Against a four-parent ensemble at 11.2T total, the full three-tier ladder on every domain costs 309B additional parameters, which is 2.76% of the ensemble. That is the argument for the axis existing at all, and it is arithmetic, not a measurement.

**The bottom tier runs on a phone.** 277M parameters at Q4_K_M GGUF (about 4.5 bits per parameter) is **156 MB**. At MXFP4's 4.25 bits it is 147 MB. Either fits in a mobile application bundle with room left over.

### 2.3 What "key-value reuse works along the size axis" actually means

The owner's framing states that escalating `Code-small -> Code-large` carries the prefill while escalating across domains re-prefills. That is right in one of its three possible readings and wrong or unproven in the other two, and the three must be separated or an implementer will build the wrong thing.

**(a) Locality. Solid.** The escalation target sits in the same serving pool as the small tier, so no session state crosses the wire, no second sticky-owner selection under §9.3's `eq:sticky` objective is performed, and **§11.3**'s failure semantics do not re-arm. Cross-domain escalation crosses pools and pays all of that. This reading needs **co-location**, which is a placement decision, and it does not need lineage at all. It is the reading §9's machinery actually cares about and it is the one that carries the design. (Two corrections to an earlier draft of this line, both unrelated to the §3.3 renumbering: failure semantics are collected in `logos.tex` **§11.3**, not §9.5, which is "Routing across models, not only inside them"; and the sticky-owner objective is referred to here by its label rather than by an equation number, because the paper's equation numbering is not stable across revisions and a wrong number is worse than no number.)

**(b) Within-tier prefix caching across turns. Solid and standard.** Orthogonal to both axes. Mentioned only so it is not miscounted as a benefit of the ladder.

**(c) Cross-tier tensor reuse: the small tier's KV cache is consumed directly by the large tier.** This is the interesting reading, it is the one with residual novelty, and it is the one this document was wrong about in draft. The prior-art check (`PRIOR_ART_v03.md` §1) resolves it and §2.3.1 gives the corrected treatment.

**Consequence.** The cost model in §5 uses reading (a) and does not claim (c). Any figure that assumes (c) is an assumption on a research bet, and §2.3.1 states what the bet is and what already argues against it.

### 2.3.1 Cross-tier KV reuse, corrected against the prior art

**A correction to this document.** An earlier draft of §2.3 stated that tiers of a ladder "do not share `d_model`, head count, head dimension or layer count", and concluded that the tensors are not shape-compatible. **The head-count and head-dimension half of that is false for a grouped-query-attention family and is withdrawn.** Llama 3 Table 3 (arXiv:2407.21783, fetched and primary-sourced in `PRIOR_ART_v03.md` §1.1) gives **8 key/value heads and head dimension 128 at 8B, 70B and 405B alike**, so per-layer KV state is `2 x 8 x 128 = 2048` elements, that is **4096 bytes per token per layer at fp16, identical across the whole family**. Model dimension and layer count do differ (4,096/8,192/16,384 and 32/80/126). So the objection is not tensor shape. It is **layer correspondence and semantic compatibility**, which are the harder objections, and stating the easy wrong one in place of the hard right one would have been the more comfortable error.

**What the enabling fact does not buy.** Per-layer shape identity says nothing about which of a 32-layer sibling's layers supplies KV to which of a 126-layer sibling's, across roughly a four-times depth difference. That is the actual research content and the mechanism's falsifier should be stated in those terms.

**The direct negative, confronted rather than cited as support.** DroidSpeak (arXiv:2411.02820) reuses KV cache across different LLMs **provided they have the same architecture**, and reports up to 4x throughput and about 3.1x faster prefill. But it does not reuse the cache wholesale: it "selectively recomputes a few layers of the KV cache produced by another LLM and reuses the remaining layers." **At identical architecture and identical size, differing only by finetuning, direct reuse was not good enough and per-layer selective recomputation was required.** This proposal asks for direct reuse across a four-times depth difference, which is strictly harder. Two honest responses are available and this document takes the second:

1. Argue that an explicit alignment objective during distillation succeeds where post-hoc reuse between independently finetuned models failed. That is a plausible bet and **nothing supports it**; DroidSpeak did not train for alignment, so its negative does not strictly cover the aligned case.
2. **Concede that partial recomputation is the realistic outcome and cost it.** If a fraction `beta` of layers must be recomputed on escalation, the prefill saving is `(1 - beta)` of the prefill, not all of it. DroidSpeak's "a few layers" at zero depth difference sets a floor on `beta` that a four-times depth difference can only raise. **Every figure in §5.4 uses reading (a) of §2.3 and therefore does not depend on `beta`**, which is why the cost argument survives this negative intact. Any future figure that claims cross-tier prefill savings must carry `beta` explicitly and must not assume `beta = 0`.

**The simpler design that already works, and why an aligned ladder would have to beat it.** ICaRus (arXiv:2603.13281) and PrefillShare (arXiv:2602.12029), from one author group fifteen days apart, get cache interchangeability the cheap way: **one frozen shared encoder produces the KV, and lightweight LoRA'd decoders consume it.** ICaRus reports up to **11.1x lower P95 latency and 3.8x higher throughput** on an eight-model multi-agent workflow with accuracy comparable to task-specific finetuned models. That is a simpler construction than an aligned-but-independent ladder, it is published, and it is months old.

**So the document must say why an aligned ladder would beat a shared frozen encoder, and the honest answer is that on serving latency alone it probably would not.** The case for the ladder is not throughput. It is that a shared frozen encoder fixes the representation for every member, which is **L5 on §1.1's ladder** and therefore the worst possible setting for §3's diversity budget, and it caps every tier at the encoder's capacity so the ladder cannot span 277M to 2.8T. ICaRus is the right design for a family of same-size task variants. It is not a design for a size ladder. **If the ladder's only argument were serving latency, ICaRus wins and the ladder should not be built.**

**The most promising construction, and it may be free.** MatFormer (arXiv:2310.07707) nests **feed-forward blocks only**, extracting hundreds of submodels from one parent at zero extra training cost. Because the nesting never touches attention, every MatFormer submodel shares the same `W_k` and `W_v` and the same layer count, so caches are shape-compatible and approximately semantically aligned **by construction**. The paper never claims or measures KV compatibility. That is the nearest unexploited adjacency in the whole area and it is the construction this ladder should try first, because it removes the layer-correspondence problem entirely rather than solving it.

**The crowded neighbourhood, cited so it is not rediscovered.** Cross-model KV transfer through a **trained translation adapter** is an active subfield: Cache-to-Cache (arXiv:2510.03215, ICLR 2026), Latent Cache Flow (arXiv:2605.22863), Semantic Cache Distillation (arXiv:2606.07684). LayerSkip (arXiv:2404.16710) is the degenerate case where the small model is a layer prefix of the large one, so interchangeability is identity rather than a learned property; note that its KV mechanics are **not primary-sourced** in the prior-art check and must be read before being relied on. DFlash (LMSYS, 2026-06-15) re-projects target latents through the draft's own KV projection, which is the reverse direction of this proposal and six weeks old.

**One load-bearing unknown.** `PRIOR_ART_v03.md` §7 item 8 could **not resolve Minitron's attention layout** (arXiv:2408.11796). If its width pruning changes `num_key_value_heads` or `head_dim`, **the constant-KV-shape property does not survive a Minitron-style ladder construction**, and the enabling fact above applies only to families that hold the GQA layout fixed by design. This is directly load-bearing and needs the full paper.

**Status of the whole mechanism: candidate contribution, not found as stated across eleven search strings plus four arXiv API queries, and carrying the largest prior-art exposure of anything in this document.** Any write-up must cite and differentiate all seven papers above. That is the exact shape of round 2's C-04, and the subfield is crowded enough that "unaware" is the charitable reading.

### 2.3.2 Serving the ladder: where multi-adapter batching binds and where it does not

One practical correction, because the answer differs by regime and a single verdict would be wrong in one of them.

**llama.cpp does support per-request adapters.** The `/completion` endpoint takes a `lora` field of per-adapter ids and scales, with `GET`/`POST /lora-adapters` and `--lora` loading. But its server README states verbatim: **"requests with different LoRA configurations will not be batched together, which may result in performance degradation."** That is structural batch fragmentation, not a bug: N distinct adapters in flight split the continuous batch N ways.

**It binds multi-tenant serving only.** At batch size 1 on a 277M edge model there is no batch to fragment, so the 156 MB edge case of §2.2 is unaffected and llama.cpp is the right engine for it. If the ladder is served multi-tenant, llama.cpp is the wrong engine and the published answer is vLLM's S-LoRA heterogeneous-batching kernels (arXiv:2311.03285), which report up to 4x throughput over HuggingFace PEFT and adapter counts higher by several orders of magnitude.

**Labelling, per the paper's own tiers.** S-LoRA's "small overhead" is unquantified in its abstract, and vLLM's documentation claims "minimal overhead" with **no benchmark**. That is vendor documentation and therefore Tier B. Anyone repeating it is repeating a vendor claim, and this document does not treat it as measured.

**So the design must state which regime it claims**, because the same evidence supports opposite conclusions in the two. Edge: llama.cpp, unaffected. Multi-tenant: vLLM, and the §8.1 adapter-batching assumption inherits a Tier-B overhead figure.

### 2.4 Asymmetry

Sizes are **not** a uniform grid. Each domain gets the size distribution its traffic and difficulty warrant:

- A domain with heavy traffic and a high easy-query fraction wants a fat bottom of the ladder and many small-tier replicas.
- A domain with light traffic and uniformly hard queries wants the parent and one intermediate tier, and no edge tier at all.
- Administration, whose objective conflicts with capability maximisation and whose queries are largely policy lookup, is the strongest candidate for a heavily bottom-weighted ladder. **That is a guess and nothing measures it.**

Which cells exist is a deployment decision driven by measured traffic and measured per-tier exit rates. **Neither has been measured.** The asymmetry is what makes §5's third case win, and the asymmetry is currently unparameterised.

### 2.5 "Four towers, not five" survives

`logos.tex` **§3.5**'s criterion applies **entirely to the domain axis**. All three of its axes (corpus disjointness, objective conflict, update cadence) are properties of what a model was trained on and why, not of how large it is. Applying the criterion to the size axis is degenerate by construction: tiers of one ladder share a corpus exactly (the child is distilled on the parent's distribution), share an alignment objective exactly, and are revised on exactly the parent's cadence. They fail all three axes and should merge, which is the correct answer, because they are not towers. They are tiers of one tower.

So the criterion is well-typed on the domain axis, degenerate on the size axis, and the degeneracy is a confirmation that the axes are genuinely different objects rather than two readings of one.

**Mathematics and Logic still merge.** The result is unchanged: **four domains**, Code, Life Sciences, Mathematics-and-Logic, Administration. It is still falsifier F11, it is one of the **two falsifiers of fourteen that need no accelerator at all** (the other is F12), and it still has not run. `logos.tex` §3.5 reaches the same verdict and keeps the five-way figure in its scaling table "for continuity with the arithmetic", which is disclosed there rather than hidden; the consequence for this document is that §5.3's cases below are computed on **four** domains while the paper's §11.1 computes its own three cases on **five**, and §5.1 says why both are correct and which is the register of record.

---

## 3. Where the diversity actually comes from, and the central risk

### 3.1 The risk, stated plainly

If every member of the ensemble descends from one parent, **base diversity is near zero and errors are correlated by construction.** Two tiers of one ladder fail on the same items, because the child was trained to reproduce the parent. Two domain parents from a common seed at L2 are less correlated than that but more correlated than two independent pretraining runs, and how much less is exactly the quantity nobody has measured.

Therefore: **the ensemble's entire diversity budget lives in the adapters, trained on disjoint data, and not in the base ladder.**

That is the central risk of this architecture. It is a single point of failure for every claim that depends on members disagreeing informatively, and it is placed in the cheapest, lowest-rank, most heavily regularised component in the system.

### 3.2 How fast the gain dies

Take five members, each with per-item error rate `p = 0.30`, aggregated by unweighted majority vote. Model member errors as exchangeable Bernoulli with intra-class correlation `rho` (Beta-Binomial). Then majority-vote error is:

| `rho` | Majority error | Absolute gain over one member | Fraction of the independent gain retained |
|---:|---:|---:|---:|
| 0.00 | 0.1631 | 0.1369 | 100% |
| 0.10 | 0.2060 | 0.0940 | 68.6% |
| 0.20 | 0.2351 | 0.0649 | **47.4%** |
| 0.30 | 0.2557 | 0.0443 | 32.3% |
| 0.50 | 0.2814 | 0.0186 | **13.6%** |
| 0.70 | 0.2943 | 0.0057 | 4.2% |
| 1.00 | 0.3000 | 0.0000 | 0% |

**At `rho = 0.2` the ensemble has already lost more than half its gain. At `rho = 0.5` it has lost 86%.**

Three honest caveats on that table, because it is the most persuasive object in this document and it is arithmetic rather than evidence. Real member errors are not exchangeable, so a single `rho` is a summary of a structure it does not capture. `p = 0.30` and `k = 5` are chosen for legibility and the shape of the curve, not the levels, is what transfers. And unweighted majority vote is the weakest aggregation rule available, so the table is a lower bound on what a better rule could extract; §4 discusses two rules that are not majority vote.

What the table establishes is the sensitivity, not the value. **The value of `rho` for adapters over a shared base has not been measured anywhere in this repository.** §7 measures it.

### 3.3 This is the same knob C-02 damaged

`REVIEW_ROUND2.md` C-02 established that neither cited debate paper says informational diversity is what breaks the martingale, and that Choi et al. extend the martingale to heterogeneous agents explicitly. The paper's response, correctly, was to restate tower diversity as a conjecture that runs against its source (F13, `LOGOS_HARNESS.md` §1.1 item 2).

The architecture here does not escape that. It **raises the stakes on the same quantity**. C-02 damaged the theoretical argument that diversity helps; §3.1 makes diversity the sole surviving source of ensemble benefit on the capability side; and §3.2 shows the benefit is quantitatively fragile in `rho`. Three separate arguments now converge on one unmeasured number.

Restating it as one sentence: **C-02 removed the theoretical warrant for diversity, this architecture removes every alternative source of it, and nothing has measured whether it exists.** That is not a comfortable position and it should not be written as one.

**And §1.5 adds a fourth argument, from a direction none of the other three come from.** The three above are all about whether diversity *helps*. §1.5 is about whether the architecture is *allowed to have any*: at the `g` the data-wall argument needs, the towers share 98 percent of their token budget, which is `λ = 1` pushed as close to `λ = 2` as it goes, and §3.2's table prices what is left. So the count is now four arguments converging on one unmeasured number, and one of the four says the number is small by construction rather than by accident. This document's response is §1.5's response 1: stop billing for the diversity budget in the architecture's justification, and let §7 report what it actually was.

### 3.4 The central design tension: alignment and decorrelation are the same knob with opposite signs

This is the sharpest problem in the document and it is internal, not a citation gap. It was surfaced by the prior-art check (`PRIOR_ART_v03.md` §4a) and it is stated here as the design's central tension rather than as a caveat, because that is what it is.

**§2.3.1 proposes a training objective that maximises representational *agreement* between ladder members, so their key and value projections become interchangeable. §3 requires those same members to have *decorrelated* errors, or the ensemble buys nothing.**

Those are not two independent design goals that happen to be in mild conflict. **They are the same parameter with opposite signs.** Every step that makes the ladder's caches more interchangeable makes its members more alike, and members that are more alike fail on the same items. This is §1.1's lineage ladder again, but sharper and worse: previously the tension was between two things the design wanted at different levels, and a middle setting was conceivable. Now a **mechanism the design actively wants to build** pushes the knob toward the end that destroys the other thing the design wants. Shipping §2.3.1 successfully shrinks the payoff from §3 by construction.

**The published evidence is on the decorrelation side, and it is against the ensemble.**

- Fort, Hu and Lakshminarayanan (arXiv:1912.02757), verbatim: "random initializations explore entirely different modes, while functions along an optimization trajectory or sampled from the subspace thereof cluster within a single mode predictions-wise", and **"the decorrelation power of random initializations is unmatched by popular subspace sampling methods."** Ensemble benefit is a function of error decorrelation; decorrelation comes from independent initialisation; a ladder distilled from one parent on one corpus is the precise opposite of independent initialisation. Recorded honestly: the diversity-accuracy-plane numerics were not extracted, so only the two qualitative statements above are used.
- Nam, Yoon, Lee and Lee (arXiv:2110.14149), verbatim: **"the typical distillation procedure does not effectively transfer such diversity, especially for complex models that achieve near-zero training error."**

**The limitation on that second citation must be stated, not buried.** Nam et al. study distilling *an ensemble into one model*, not ensembling *multiple students of one teacher*. **It supports the concern by mechanism and by analogy, not directly.** Asserting otherwise would be a C-02-shaped error, citing a real paper for an inference it does not make, which is the defect round 2 graded critical. This document does not make that assertion and any downstream text must not either.

**And the direct measurement does not exist.** `PRIOR_ART_v03.md` §4a searched five strings and found **no primary source measuring ensemble gain among N students distilled from one common parent LLM as a function of N with the error-correlation matrix reported.** That negative is explicitly weaker than the one in §2.3.1: "ensemble of distilled siblings" has no standard name, so a paper could exist under vocabulary the check did not guess. **Do not write "nobody has measured this" without that qualifier.**

**The consequence, which is the decision this document exists to force.** The design must either pick a side or measure the sign:

- **Pick the cascade side.** Optimise the ladder for interchangeability, accept that its members are not an ensemble, and let §4.1's cascade be the only composition mechanism. This is coherent, it is cheap, and §5's entire cost argument survives untouched because §5.4 never uses ensembling.
- **Pick the ensemble side.** Abandon the alignment objective, accept re-prefill on escalation, and keep the diversity budget. This costs exactly the prefill saving §2.3.1 was invented to buy, and §5.4 shows the cascade still pays without it.
- **Measure the sign.** Measure sibling error correlation before and after KV-alignment distillation, and pre-commit the predicted direction. That is the falsifier form and it is the recommended one.

**Nothing here has measured it. The prediction, stated in advance so it cannot be claimed afterwards: KV-alignment distillation raises `rho_bar` between siblings.** If it does, §3.2's table prices the loss, and the ensemble half of the architecture should be dropped in favour of the cascade half.

---

## 4. Composition mechanisms, and what each costs

Four mechanisms. Three are live, one is ruled out. Each is stated with its minimum lineage level from §1.1 and with what it forfeits.

### 4.1 Cascade with a learned exit

Route to the cheapest tier first, escalate on low confidence. Pure selection: one member's output is returned verbatim, nothing is combined.

- **Minimum lineage: L0.** This is the only mechanism that works at any level.
- **Buys:** tokens. See §5.4 for the break-even.
- **Escapes C-02** trivially, because there is no belief updating and no debate.
- **Costs:** the exit classifier is a second router trained on less signal than either tier, and it inherits every risk `logos.tex` **§3.4** names for the main router. Escalation is not free: a query that escalates pays both tiers.
- **Verdict: solid.** This is the mechanism the cost argument in §5 rests on.

### 4.2 Tower-expert selection inside the forward pass

Treat towers, or tiers, as experts selected within a single forward pass rather than as debaters exchanging messages.

**This escapes C-02.** The martingale theorem is about sequential belief updating in debate: agents exchange positions across rounds and update beliefs. A mixture computed inside one forward pass is not a sequence of belief updates and the theorem does not reach it. That is a real escape and it should be stated as one, because it is the only route by which combining members can help without contradicting a published theorem the paper has already been caught misreading.

**But granularity decides whether §9.2's argument survives, and the commitment must be explicit.** §9.2 argues that a monolithic sparse MoE pays one peer round trip per layer, which at 60 layers and 10 ms is 0.60 s per token, and that a Mixture-of-Towers pays one per query. Recomputing that ratio for each granularity:

| Granularity | Serial round trips | At 10 ms RTT | At 30 ms RTT | §9.2's argument |
|---|---|---|---|---|
| **Per query**, k-of-N | k parallel dispatches, **1 round trip per query** | negligible | negligible | **Survives intact** |
| **Per token**, k-of-N | 1 round trip per token | 100 tok/s ceiling | 33 tok/s ceiling | **Survives at low RTT, degrades at high** |
| **Per layer**, interleaved across towers | 60 round trips per token | **1.67 tok/s** | **0.56 tok/s** | **Forfeited entirely** |

The per-layer row reproduces §9.2's own monolith figures exactly. That is not a coincidence and it is worth stating: **per-layer tower interleaving is latency-identical to the monolith §9.2 argues against**, even though it dispatches 4 ways rather than 896.

**A presentational finding falls out of that.** §9.2's headline is "nine hundred and sixty dispatches per token against one per query", but its own latency arithmetic shows dispatch within a layer is parallel and only layers are serial. The operative ratio is therefore **60 serial round trips per token against 1 per query**, and against a 500-token response it is 30,000 to 1. The 960 figure is doing rhetorical work its own derivation does not support, in a direction that happens to flatter the conclusion. The conclusion is right and the number carrying it is the wrong number.

**Commitment: per-query k-of-N. Per-layer interleaving is out of scope for any wide-area deployment.** Per-token is admissible only inside a single-site pool where RTT is a bus latency rather than a network one, and any design that uses it must say so.

**The mixing level is a second, separate commitment.**

- **Hidden-state mixing requires a shared latent space that independent pretraining destroys.** Averaging or gating over hidden states from two independently pretrained models assumes their activations occupy a comparable basis. Nothing makes that true. **This is F-06's defect exactly**: F-06 found a shared residual-quantized codebook placed in the hidden-state path with no cited source putting it there, and the paper relocated it to the two positions where discrete identifiers genuinely are the interface. Proposing hidden-state mixing across independently pretrained towers would reintroduce the identical error, a real mechanism placed in the hidden-state path because it is convenient rather than because any source puts it there. **Minimum lineage: L3, and even at L3 it is a bet.**
- **Logit-level mixing survives this**, because logits over a shared vocabulary are comparable by construction. It requires a shared tokenizer. **Minimum lineage: L1.**

**And this mechanism is the paper's central bet under a different name.** Branch-Train-MiX, BTX and Branch-Adapt-Route *are* tower-expert selection in the forward pass. So §4.2 is not a new option added alongside F2, it is F2. It carries the same 400x extrapolation, the same F-04 status of unresolvable by argument, and the same absence of a hedge. Nothing in this document reduces that bet. It only names it correctly and forces the lineage commitment BTX has always required.

### 4.3 Looped forward pass with a learned exit

Run the same weights repeatedly over the residual stream, with a learned rule that decides when to stop.

- **Minimum lineage: not applicable.** This is internal to one member.
- **Escapes C-02**, for the same reason as §4.2: it is not debate and there is no belief-updating protocol.
- **Buys:** effective **depth** without additional parameters, which is a partial answer to the effective-capacity question the size ladder otherwise leaves open. A 7B tier with an adaptive loop has more effective depth than a 7B tier without one, at no memory cost and at a compute cost paid only on the queries that need it.
- **Honest caveat, and it is the one that matters:** more passes over fixed weights buy **reasoning depth, not knowledge**. No number of iterations can surface a fact the weights do not contain. Anywhere the ladder's small tiers are missing knowledge rather than missing computation, looping does nothing, and knowledge is precisely what distillation to 277M loses first. The loop is therefore a partial answer to effective capacity and not an answer to the knowledge gap.
- **Constraint: loop locally, route globally.** If the loop crosses a peer boundary, the round-trip cost multiplies by the iteration count and the §4.2 table applies with the iteration count in place of the layer count. At 8 iterations and 10 ms that is 12.5 tok/s. The loop must be confined to one pool.

**Prior art: zero novelty, in the mechanism and in the caveat. Cite all of it, claim none of it.** `PRIOR_ART_v03.md` §2 resolves the verification item this document previously raised, and the answer is that everything above is published. The lineage runs Adaptive Computation Time (arXiv:1603.08983, Graves) through Universal Transformers (arXiv:1807.03819), recurrent-depth latent reasoning (arXiv:2502.05171), Mixture-of-Recursions (arXiv:2507.10524, which also carries a KV-sharing variant reusing pairs from the first recursion) and Ouro (arXiv:2510.25741).

**The reasoning-not-knowledge caveat above is not this document's observation. It is established twice, with numbers.** Saunshi et al. (arXiv:2502.17416) give the iso-FLOP ablation: a looped 12x2 model scores **9.3% on closed-book QA against an iso-FLOP baseline's 11.2%**, and **34.3% on math word problems against 26.7%**, beating even a 24-layer non-looped reference at 29.3%. Looping **loses** on memorisation and wins on reasoning, measured. Ouro states it at 1.4B and 2.6B scale, verbatim: "this advantage stems not from increased knowledge capacity, but from superior knowledge manipulation capabilities." **Presenting the distinction as a finding of this architecture would repeat round 2's C-04 with two more prominent papers, and the distinction is used here strictly as a premise.**

**The learned exit specifically is the weak part, and the newest result argues against it.** Popescu, Sáez de Ocáriz Borde and Liò (arXiv:2607.20519) find that "simple post-hoc confidence readouts often match or outperform learned linear and MLP gates", localise the failure to "the trajectory induced by joint gate training rather than from limited gate expressivity", and report that on Ouro's models pretrained ponder gates are "competitive but not uniformly Pareto-optimal". **So the default here is a post-hoc confidence readout, not a learned gate.** Retaining a learned gate requires an argument for why this setting differs, and no such argument exists in this document.

### 4.4 Looping over towers as debate: ruled out

**Ruled out by C-02, and named as ruled out so nobody reintroduces it.**

Sending a query to multiple towers, letting them exchange positions across rounds, and updating each tower's belief on what the others said is exactly the protocol Choi et al. prove is a martingale, and exactly the protocol they extend to heterogeneous agents. Under unweighted belief updates, expected correctness does not improve over rounds, and holding informatively different views does not change that. The two known escapes are protocol-internal: calibrated-confidence weighting, which buys a strict submartingale but purchases the calibration with external supervision; and diversity-aware initialisation, whose own authors state it does not change the update dynamics.

This mechanism is out. It is not out pending measurement, it is out because a published theorem covers it and the paper has already been caught once claiming the theorem says the opposite. Any future revision that reintroduces multi-round tower debate must first say which limb of C-02 it thinks is wrong.

### 4.5 Summary

| Mechanism | Min lineage | Escapes C-02 | Buys | Forfeits / cost |
|---|---|---|---|---|
| Cascade with learned exit | L0 | Yes (not debate) | Tokens | Second router; escalation pays both tiers |
| Forward-pass expert selection, per query | L1 (logits) / L3 (hidden states) | Yes (not debate) | Quality, if diversity exists | Is F2; 400x unhedged; hidden-state variant repeats F-06 |
| Forward-pass expert selection, per layer | as above | Yes | Same | **Forfeits §9.2 entirely.** Out of scope |
| Looped forward pass with learned exit | n/a | Yes (not debate) | Effective depth | Buys no knowledge; must stay in one pool |
| Multi-round tower debate | any | **No** | Nothing, per theorem | **Ruled out** |

---

## 5. The §11.1 correction: one case is three. **Adopted.**

### 5.1 What the paper used to say, and what it says now

**Status: ADOPTED into `logos.tex` §11.1, which now carries three cases and the fungibility argument.** The section is retained here because the paper's instantiation and this document's differ in a way a reader will otherwise think is an error.

What the paper used to say: five towers of 64 accelerators is 320 accelerators, five replicas of a single 2.8T tower is also 320 accelerators, the hardware bill is the same, and therefore the ensemble is justified by traffic entropy. The conclusion was then softened in the following paragraph, which added wide-area serviceability as a second justification, and `REVIEW_ROUND2.md` X-05 caught the conclusion's "by nothing else" contradicting the body.

**The defect L-01's method finds is different from X-05's, and it is upstream of it.** §11.1 presented one comparison as though it were the comparison. It is one case out of three, and the three have different signs. The paper now says so, and it goes one step further than this document did: it states that the **decision rule inverts**. Under uniform tower sizing the ensemble's advantage grows with the entropy of the domain distribution; under demand-proportional sizing the rule reverses, because skew is precisely what asymmetric allocation converts into parameters where the traffic is. The paper's single sentence, which is the right one and is now the register of record: *an ensemble wins on serving cost when the traffic mix is skewed, stable, and known before the towers are trained, and loses when it is skewed and not known.*

**Two instantiations, both correct, and which to quote.** `logos.tex` §11.1 computes its three cases on **five** domains at shares `(0.60, 0.20, 0.10, 0.05, 0.05)`; §5.3 below computes them on **four** domains at `(0.55, 0.20, 0.15, 0.10)`, because §2.5's criterion returns four. The arithmetic differs accordingly: the paper's case 2 loses a factor of 3 and two thirds of a 320-accelerator fleet to idleness, and §5.3's case 2 loses a factor of 2.20 and 54.5 percent of the fleet. **Both are the same argument evaluated at different assumed skews on different domain counts, and neither skew is measured.** Quote the paper's figures when citing the paper. Quote §5.3's when reasoning about the four-domain partition the criterion actually returns. Do not interleave them.

### 5.2 The thing the paper does not say

**Replicas are fungible and towers are not.** Any replica can serve any query. A Code query cannot use an idle Life Sciences accelerator, ever, at any load, because the Life Sciences weights are what is resident there. The ensemble therefore gives up statistical multiplexing across domains, and §11.1 never prices that, because at uniform traffic it costs nothing and uniform traffic is the only case the paper considers.

### 5.3 The three cases, with arithmetic

Setup, all of it stated as assumption. Budget `A = 320` accelerators, the conservative end of §11.1's own bracket. Four domains per §2.5. Serving capacity within a domain is taken proportional to accelerators assigned once the residency floor is met, in units where the whole fleet is 320. Comparator is a fungible fleet of 320 accelerators of a generalist model of the same per-instance size, which is the interesting baseline; §11.1's stated baseline of five replicas of one 2.8T tower covers only one domain and so is not a competitor to an ensemble at all. Traffic skew used throughout: **Code 55%, Mathematics-and-Logic 20%, Life Sciences 15%, Administration 10%.** That skew is illustrative and nothing measures it.

Maximum admissible load for the ensemble is `min_d (accelerators_d / p_d)`, because the hottest domain saturates first and the others cannot help it.

**Case 1: uniform traffic, uniform sizing.** Four towers at 80 accelerators each, `p_d = 0.25` for all d.

```
Lambda_max = min(80/0.25, 80/0.25, 80/0.25, 80/0.25) = 320
Fungible fleet                                        = 320
```

**Same cost, no advantage.** The ensemble's benefit here, whatever it is, is not a cost benefit. This is the case §11.1 computes, and its conclusion is correct for it.

**Case 2: skewed traffic, uniform sizing.** Four towers at 80 each, skew as above.

```
Lambda_max = min(80/0.55, 80/0.20, 80/0.15, 80/0.10)
           = min(145.5,   400,     533,     800)
           = 145.5
Fungible fleet = 320
```

**The ensemble is worse by a factor of 2.20.** At saturation, 54.5% of the fleet is idle and structurally cannot be used, because the idle accelerators hold the wrong weights. To serve the same 320 under uniform sizing the ensemble needs Code at 176 accelerators and therefore, uniform, `4 x 176 = 704` accelerators, a 2.20x hardware bill for identical served load. **This case does not appear anywhere in the paper, and it is the case that matters, because real traffic is not uniform.**

**Case 3: skewed traffic, asymmetric sizing.** Allocate proportional to demand: Code 176, Mathematics-and-Logic 64, Life Sciences 48, Administration 32.

```
Lambda_max = min(176/0.55, 64/0.20, 48/0.15, 32/0.10)
           = min(320,      320,     320,     320)
           = 320
Fungible fleet = 320
```

Throughput parity with the fungible fleet, and the ensemble additionally holds a specialised model per domain rather than one generalist. **A fixed-size replica fleet structurally cannot do this**, because every replica is the same model and therefore allocates the same parameters to a policy lookup as to a hard proof. Proportional allocation is available only to a heterogeneous fleet.

### 5.4 Where "better" rather than "parity" comes from

Case 3 buys parity on throughput. The strict win comes from the **size axis**, which allocates parameters per query rather than per domain.

Work in activated-parameter units. Take the domain parent's activated parameters at the bottom of §2.2's swept bracket, `N_large = 64B`. A dense small tier at `N_small`. Cascade exit rate `e` is the fraction of queries the small tier resolves. A query that escalates pays both tiers.

```
cost(e) = e * N_small  +  (1 - e) * (N_small + N_large)
```

Break-even against always running the parent is at `e* = N_small / N_large`:

| Ladder step | Break-even exit rate |
|---|---|
| 7B under a 64B-active parent | **0.109** |
| 277M under a 7B tier | **0.040** |
| 277M under a 64B-active parent | 0.004 |

**The cascade pays whenever the small-tier exit rate exceeds the size ratio**, which is a clean and checkable statement and the sharpest thing in this document. Worked points, two-tier, 7B under a 64B-active parent:

| Exit rate `e` | Cost, activated-parameter units | Ratio against the parent |
|---:|---:|---:|
| 0.30 | 51.80B | 1.24x |
| 0.50 | 39.00B | 1.64x |
| 0.70 | 26.20B | 2.44x |

Three-tier, 277M then 7B then the parent, at `e1 = 0.40` and `e2 = 0.35`:

```
0.40*0.277 + 0.35*(0.277+7) + 0.25*(0.277+7+64) = 20.48B  ->  3.13x
```

**Every exit rate above is an assumption. None has been measured.** The break-even is arithmetic and holds; whether real traffic clears it is exactly the unmeasured quantity, and it is measurable cheaply (§7.5).

### 5.5 Why this matters more than the arguments it replaces

This is a **cost** argument and therefore checkable against a measured serving deployment. Contrast:

- The **diversity** argument, which C-02 damaged at the theoretical level and which §3 shows is quantitatively fragile in an unmeasured `rho`.
- The **data-wall** argument, which X-04 left surviving only when the residency-bound corpus fraction `f` is below about 0.02 against the central token-supply estimate, that is only when almost the entire corpus is shared core. **`f` is now bounded, by `f ≤ 1-g`, and the bound is what §1.5 shows makes the argument unwinnable against the diversity claim.** The earlier statement here that "`f` is unbounded anywhere in the paper" is withdrawn; it was true of the version round 2 read and is false of `logos.tex` v0.3.
- The **wide-area serviceability** argument, which §9.2 supplies and which is arithmetic over an unverified layer count against a sparse-dispatch cost model nobody has measured (F-13, still open).

Against three arguments that are respectively refuted, conditional on an unmeasured parameter, and unmeasured, an argument whose only inputs are traffic distribution and per-tier exit rates is the one worth carrying. Both inputs are measurable on hardware the owner has.

**The paper has been revised.** §11.1 now carries three cases and states the cost justification as **skew plus asymmetry** rather than entropy. Entropy was the wrong summary statistic: a domain distribution can have high entropy and still saturate one tower, and what the ensemble needs is that allocation matches the distribution, not that the distribution is flat. The paper adds the condition this document had left implicit, and it is the binding one: the mix must be **known before the towers are trained**, because re-sizing a tower is a training run and not a scheduling decision. That is the sense in which this ensemble is less elastic than a replica fleet even where it is cheaper, and nothing in this document buys the elasticity back.

---

## 6. The metric: eta is retired. AIQ primary, APGR with CPT(50%) secondary.

### 6.1 What was retired, and the word is retired rather than demoted

`logos.tex` §11.2 defined routing efficiency

```
eta = (S_router - S_best_single_tower) / (S_oracle - S_best_single_tower)
```

and `REVIEW_ROUND2.md` A-02 found four defects, **all four of which the paper now discloses as (E1) to (E4)**. The disclosure is honest and it does not fix the metric; it documents that the metric requires four separate corrections before it can be read. A metric that needs four caveats to be interpretable is not the metric to hang falsifier F10 on.

**Two things must be stated exactly, because an earlier draft of this section got the strength of the paper's move wrong.**

- **The paper retires eta. It does not demote it and it does not keep it as a diagnostic.** `logos.tex` §11.2, verbatim: "there is no residual question `η` answers that APGR does not answer better." The one thing eta was for, the fraction of available headroom a router recovered, is what APGR measures, with endpoints designated in advance instead of maximised over. Nothing in this document should be read as proposing to keep eta anywhere, under any guard, for any purpose.
- **A-02's own recommended fix is superseded.** Round 2 recommended defining eta only above a stated denominator floor `δ` and keeping it. The paper went further and dropped the metric, and `GAPS.md` §4a records that **the paper is the register of record** on this. Anyone working from the round-2 fix text is working from a superseded recommendation.

The size axis was the additional reason, and it stands: eta has no way to express the thing the size axis exists to do. If the 277M tier answers a query correctly and the parent also answers it correctly, eta records nothing, and yet the routing decision that sent it to 277M is the entire point of the architecture. **eta is quality-only, and half of this design is cost.**

### 6.2 The shape of the replacement, stated before the names

**Read §6.5 first if the only question is what to report.** This subsection derives the object from A-02's defects; §6.5 gives it its published name and supersedes the homegrown formulation here wherever a name exists. The derivation is kept because it shows the replacement is forced by the defects rather than chosen by preference, and because §6.4's fragmentation argument needs it.

For a routing policy `pi`, report the pair

```
(C(pi), Q(pi))
```

where `C` is expected serving cost per query in a stated unit (activated-parameter-tokens, accelerator-seconds, or joules; state which) and `Q` is quality on a frozen battery. The system is characterised by the **achievable frontier**, the set of non-dominated `(C, Q)` pairs over the policy family. Comparison is stated one of two ways, and either is a scalar:

- **Quality at fixed token budget**: fix `C = B`, report `Q`.
- **Tokens at fixed quality**: fix `Q = q`, report `C`.

Baselines are points on the same axes, not terms inside a ratio: each single tower is a point, the parent-always policy is a point, the oracle is a point, the router is a point.

### 6.3 Against A-02's four defects

**(1) Zero denominator.** There is no denominator. The degenerate case where one tower dominates every other appears as a frontier that coincides with that tower's point, which is a **readable result** rather than an undefined quantity. A-02's own simulation (three towers at 0.90/0.20/0.20 on a 50-item slice, `P(denominator = 0) = 0.16`) becomes, on the frontier, the statement that the frontier has one interesting point. That is the actionable answer §11.2's (E1) already says the verdict should be, arrived at without a special case.

**(2) Unboundedness below.** Both coordinates are bounded and both are interpretable in their own units. `Q` lies on the battery's scale. `C` is bounded below by the cheapest tier's cost and above by the budget cap. A router worse than a baseline is a point below and to the right of it, and the magnitude of "worse" is read directly in accuracy points and accelerator-seconds. Nothing is unbounded and nothing requires clipping.

**(3) Winner's-curse floor.** There is no `max` over `k` noisy scores anywhere in the definition, so the bias A-02 measured (`+1.12` points at `k=2`, `+2.90` at `k=8` with towers of genuinely equal skill) never enters. Each tower is its own point with its own confidence interval. **Residual, stated:** if a reader wants the summary "did the router beat the best single tower", selecting the best tower for that comparison reintroduces selection bias. The protocol is therefore to **plot every tower's point** and to treat any "beat the best" claim as a multiple-comparison problem with an explicit correction, not as a term inside a ratio where the bias is invisible.

**(4) Chance-inflated ceiling.** The oracle does not appear in a denominator, so `S_oracle = 1 - 0.75^k` reaching 0.76 at `k=5` with zero-skill towers no longer manufactures headroom. If an oracle frontier is plotted at all, chance-correct it before plotting, but no other quantity depends on it. A-02's fifth observation, that five independent towers at `p = 0.70` give `S_oracle = 0.99757` so reaching `eta = 1` requires the router to already know the answer, becomes visible directly: the oracle point sits far up and to the left, and the distance from it is read rather than normalised away.

### 6.4 Why it does not fragment under a two-dimensional partition

This is the property that matters for this architecture specifically, and it is where eta fails hardest.

`logos.tex` §11.2 mandates that eta be reported per domain. On a domain x size grid that becomes per cell. With four domains and three tiers there are twelve cells, each needing its own oracle and its own best-single-member floor computed on a per-cell slice. Using A-02's own measured degeneracy rate of 0.16 per slice:

```
P(at least one cell undefined) = 1 - (1 - 0.16)^12 = 0.877
```

At a 0.30 per-cell rate it is 0.986; at twenty cells and 0.16 it is 0.969. **Per-cell eta is undefined somewhere on the grid with probability approaching one.**

And the size axis drives the per-cell rate *up*, not down. Tiers of one ladder are far more correlated than towers are, because the child was distilled from the parent, so the small tier rarely solves an item the parent misses, and the per-cell denominator `S_oracle - S_best_single` collapses toward zero much harder than A-02's cross-tower simulation. The metric is worst exactly where the architecture is most distinctive.

The frontier does not fragment, because both of its coordinates are **traffic-weighted averages** over cells:

```
C = sum_d p_d * C_d          Q = sum_d p_d * Q_d
```

Both are always defined. A cell with no interesting structure contributes its point and nothing breaks. Per-cell frontiers can still be plotted for diagnosis, and the aggregate is recoverable from them, which is not true of per-cell eta at all.

### 6.5 This is standard practice, not a contribution, and it already has names

`PRIOR_ART_v03.md` §3 establishes that the frontier above is **fully published and named**, and this document claims no novelty for it. Naming the existing objects is not a formality; it makes the replacement auditable and it stops §6 from reading as an invention.

- **AIQ**, average improvement in quality (RouterBench, arXiv:2403.12031): the normalised area under the cost-quality curve, `AIQ = 1/(c_max - c_min) * integral R~ dc`. Dimensionless, and in `[0,1]` with quality normalised. **Recommended as the primary scalar**, because §3.2 of the prior-art check confirms it avoids all four of A-02's defects in its own value.
- **APGR** and **CPT(x%)** (RouteLLM, arXiv:2406.18665): the integral of performance-gap-recovered over cost, and the minimum strong-model call rate reaching a given gap recovery. **Recommended as the secondary pair.** APGR avoids A-02's defects (2), (3) and (4) outright; its denominator `r(M_s) - r(M_w)` can still vanish, but the endpoints are two models designated in advance rather than a post-hoc maximum over k, so the condition is diagnosable before evaluation rather than emerging from per-domain slicing. Strictly weaker failure, same shape.
- **The non-decreasing convex hull** (RouterBench) is exactly the frontier object of §6.2 and already has a definition and a 405k-outcome benchmark behind it. **Adopt the construction and the name.**
- **FrugalGPT** (arXiv:2305.05176) is the source of the two reporting directions §6.2 uses, quality at fixed cost and cost at fixed quality.

**Two caveats carried forward rather than dropped.** RouterBench's **Oracle Router is a per-item max over k models and therefore carries A-02 defect (4) in full**; it is a reported reference line rather than a term inside AIQ, so AIQ's value is unaffected, but the oracle line must be chance-corrected before it is plotted or it manufactures `1 - 0.75^k` of apparent headroom exactly as A-02 showed. And AIQ's `[0,1]` boundedness is an **inference from normalised quality, not a stated theorem** in the paper; `PRIOR_ART_v03.md` §7 item 11 records that the fetch found it "not explicitly bounded".

**Status: ADOPTED, and the recommendation is now the paper's text.** `logos.tex` §11.2 reports **AIQ as the primary scalar and APGR with CPT(50%) as the secondary pair**, retires eta outright, carries both caveats above (the oracle line reported only chance-corrected and captioned as corrected; AIQ's `[0,1]` boundedness recorded as following from normalised quality rather than from a theorem in RouterBench), and restates F10 on AIQ: a warm-started router fails F10 if, on any domain carrying at least five percent of evaluation traffic, its post-swap AIQ falls more than **0.02** below its pre-swap AIQ, or its CPT(50%) rises by more than **ten percentage points of calls**. Both are defined on every evaluation set including the ones where one tower dominates, which is the property eta lacked.

The paper also states the non-fragmentation property in its own terms and its statement is cleaner than §6.4's: cost and quality are both per-query quantities, so a domain slice or a size slice is read on the same axes and slices aggregate under the traffic weights, which is the operator's own objective. Eta is a ratio of differences and does not aggregate at all.

**What this document still owes on the metric.** Nothing in §6 has been computed on real numbers anywhere in this repository. §7.4's tertiary endpoint is the only place a frontier would be plotted, and it has not run.

### 6.6 What has to be pre-committed

Frontier reporting is not free of researcher degrees of freedom and it should not be presented as if it were. Before any policy is evaluated: the battery and its split, the cost unit, the policy family swept, the budget points `B` and quality points `q` at which scalars are reported, and the confidence-interval method. Otherwise the frontier is chosen after the fact by choosing where to read it. **F10 should be restated in terms of a pre-committed budget point rather than in terms of eta**, which A-02's fix already noted is unmeasurable as currently worded.

---

## 7. The decisive cheap experiment on the architecture side

**This is the point of the document's architecture half.** Work is funded only after an experiment succeeds on one RTX 3090, 24 GB, Ampere, bf16 and FlashAttention-2 available, no FP8, no NVLink, no second card. So the question is which claim in §1 to §6 can be settled on that card.

The answer is §3: **the diversity claim**. It is the load-bearing unmeasured quantity, it is the one C-02 damaged and §3.1 made single-point-of-failure, and it is measurable at 1/400,000 of tower scale because error decorrelation is a property of what a model was trained on, not of how large it is.

**One thing is cheaper still and it is not on the architecture side.** §9.6's `C*` measurement needs no training run at all and gates every token figure in §8 and §9, so in the programme-wide ordering of §11 it comes first. §7 is the cheapest experiment on the **architecture** claim; §9.6 is the cheapest experiment in the **programme**. The two are not competitors and the distinction should be kept, because an earlier draft of this heading claimed the stronger title for §7 without qualification.

**Design: train N QLoRA adapters on deliberately disjoint corpora over one small base, then measure error decorrelation and realised ensemble gain against a single-adapter baseline. §7.3.1 adds a nano-scale pretrain replicate that reaches the lineage level the conjecture is actually stated at.**

### 7.1 Base and instrument

- **Primary base:** one open-weight base model in the 7B to 8B class, NF4-quantized (about 3.9 to 4.5 GB resident), which leaves headroom on 24 GB for QLoRA training at rank 16 over attention and MLP projections, and for sequential N-member inference at evaluation. Adapters at rank 16 are of order tens of megabytes each, so all N are resident simultaneously.
- **Sanity replicate:** a 350M base, matching `F9_PREREGISTRATION.md`'s stand-in scale, run as a cheap check that the effect is not an artifact of one base. Reported separately, never pooled.
- **`N = 8` adapters.**
- **Lineage level under test: L5, which is `λ = 2` in `logos.tex` §3.3's terms.** Every member shares one frozen backbone, which is deliberately the *worst case for diversity* in §1.1's ladder. If decorrelation appears at L5 it will appear at L2 to L4 as well. If it does not appear at L5, the experiment has not refuted L2, and §7.4 says so. **Note the relation to §1.5**: `λ = 2` is the limit of the high-`g` response the data-wall argument needs, so a positive here is evidence that response 1 costs less than §1.5 fears, and a negative is evidence it costs nothing at all because there was nothing to lose. Neither reading makes the trilemma go away; both make the price of the chosen corner legible.

### 7.2 Corpora, and disjointness as a measured quantity not an assertion

Eight corpora chosen to be domain-disjoint. **Disjointness is measured before any training step and pre-committed**, applying `logos.tex` **§3.5**'s P1 criterion at small scale, which is exactly what F11 asks for and has never been run:

- pairwise token-level Jaccard over quality-filtered n-gram sets, reported as a full 8x8 matrix;
- document-level near-duplicate rate across every pair;
- a pre-committed **maximum admissible pairwise overlap**, above which the corpus pair is rejected and replaced before training begins.

Substring containment is not an admissible overlap measure and must not be used; tokenized set membership over unigrams and n-grams only.

### 7.3 Arms

| Arm | Description | Isolates |
|---|---|---|
| **A1** | One adapter, union corpus, `N x` the token budget | "One model, all the data." The no-ensemble control |
| **A2** | N adapters, **disjoint** corpora, `1/N` tokens each, unweighted logit averaging | The treatment |
| **A3** | N adapters, i.i.d. random `1/N` splits of the **same union corpus**, same token budget, same adapter count, unweighted logit averaging | **The critical control.** Diversity destroyed by construction while everything else is held identical. Separates *corpus disjointness* from *ensembling as such* |
| **A4** | A2's members, combined by a learned per-query router rather than averaged | Selection against mixing (§4.1 against §4.2) |
| **A5** | A2's members, calibrated-confidence weighting, ungated, on the same battery | Limb (b) of F13. Shares the battery with `F9_PREREGISTRATION.md`'s K5 arm so the two documents' results are comparable |

**A2 against A3 is the experiment.** Everything else is context. A2 and A3 have identical member count, identical total tokens, identical base, identical rank, identical schedule, and differ in exactly one thing: whether the per-member corpora are disjoint or are random splits of one pool.

### 7.3.1 The nano-scale pretrain replicate, which reaches L0 and is affordable

**A correction to this document's design, and the correction improves it.** An earlier draft asserted that testing anything below L5 needs separate pretraining runs and that those are out of reach on the owned card. **That is false at nano scale.** `F9_PREREGISTRATION.md` §8.1 costs a **125M pretrain at `T = 1.0e9` tokens at 9.579 GPU-hours** on the owned RTX 3090, at the corrected 29k tokens/s throughput. Full pretrains are therefore affordable, and the whole adapter-only framing of §7.3 understated what the card can do.

**Why it matters, and it is not a cost point.** An adapter-only design cannot reach the lineage level F13 actually asserts. F13's claim is about models whose **pretraining corpora, objectives and alignment histories genuinely differ**, and `logos.tex` §15 rules out two finetunes of one base checkpoint as an instrument precisely because a shared checkpoint is suspected of destroying the treatment. Adapters over one frozen backbone are that ruled-out instrument. **Running the arms as actual pretrains from independent initialisations reaches `λ = 0`, which is the level the conjecture is stated at, and it is the real treatment.**

**The three-arm pretrain replicate.** All at 125M, all at the frozen F9 house scale, all with **independent random initialisation** per member:

| Arm | Construction | Lineage | Runs | GPU-h |
|---|---|---|---:|---:|
| **P1** | One 125M pretrain on the **union** corpus at `8.0e9` tokens. The no-ensemble control | single model | 1 (8x length) | **76.6** |
| **P2** | **8 independent 125M pretrains, independent init, disjoint corpora**, `1.0e9` tokens each. The treatment | **L0 / `λ = 0`** | 8 | **76.6** |
| **P3** | **8 independent 125M pretrains, independent init, i.i.d. random 1/8 splits of the union corpus**, `1.0e9` tokens each. The critical control | **L0 / `λ = 0`**, corpus diversity destroyed | 8 | **76.6** |
| | | | **17** | **229.9** |

`P2` against `P3` isolates **corpus disjointness at independent initialisation**, which is what the adapter version could never isolate: A2 against A3 holds the base fixed and therefore holds init-diversity at zero in both arms, so it measures only the corpus term over a shared basis. The pretrain version measures the corpus term with init-diversity present in both arms, which is the object Fort et al. say carries the decorrelation.

**And it makes `g` directly sweepable, which is the §1.5 trilemma made empirical.** A shared seed trained for a fraction `g` of the token budget and then branched 8 ways costs `9.579 x (8 - 7g)` GPU-hours per sweep point, because the seed is amortised across the members and only the branches are paid 8 times. **Higher `g` is cheaper**, which is the one place in this programme where the uncomfortable direction is also the affordable one:

| `g` | Tokens | GPU-h | What it is |
|---:|---:|---:|---|
| 0.00 | 8.0e9 | **76.6** | `λ = 0`, independent. This is P2 |
| 0.50 | 4.5e9 | **43.1** | `λ = 1`, deep branch |
| 0.90 | 1.7e9 | **16.3** | `λ = 1`, shallow branch |
| 0.98 | 1.14e9 | **10.9** | `λ = 1` at the setting §1.5's data-wall corner needs |
| | | **146.9** | four-point sweep, one seed |

**That sweep is the cheapest direct measurement of §1.5's trade-off anywhere in this repository**, at about 147 GPU-hours, 51 kWh, EUR 15 of electricity on the owned card or USD 32 rented. It returns `rho_bar(g)`: how fast error decorrelation dies as the shared seed grows. If `rho_bar` at `g = 0.98` is indistinguishable from `rho_bar` at `g = 0`, the trilemma is empty and response 1 of §1.5 costs nothing. If it is not, the sweep prices exactly what the data-wall corner costs, in the units of §3.2's table. **It is also the nano-scale instrument for falsifier F14**, which asks the same question in the paper's own terms, and it should be planned with F14 rather than separately.

**Four limitations, stated up front.**

1. **`1.0e9` tokens at 125M is 8 tokens per parameter**, against Chinchilla's 20. Every member is under-trained by a factor of 2.5. This is the **frozen F9 house scale** and it is adopted here for comparability with that experiment rather than because it is optimal. Under-training plausibly *raises* apparent diversity, because members are further from any shared optimum, so this design is biased toward finding decorrelation and a null is correspondingly stronger than a positive.
2. **125M is 22,400x below a 2.8T tower.** §7.4 condition 4 applies here unchanged and with more force: a positive at 125M says corpus disjointness produces decorrelation at all, and says nothing whatever about F2.
3. **The pretraining corpora must be built.** §7.2's overlap measurement is a prerequisite here rather than a by-product, because at `λ = 0` there is no shared base to blame a null on and the corpora carry the entire treatment.
4. **One seed per arm.** The table above buys 17 runs at one seed. A second seed doubles it to 459.8 GPU-h. `F9_PREREGISTRATION.md` §9.4's rule applies verbatim: **a non-significant result at low seed count is reported UNDERPOWERED, not negative.**

### 7.4 Endpoints and refutation conditions

**Primary endpoint: error decorrelation.** `rho_bar`, the mean pairwise phi coefficient between members' per-item correctness vectors on a held-out battery. Compare `rho_bar(A2)` against `rho_bar(A3)` with a pre-committed margin and a permutation test over member pairs.

**Secondary endpoint, and the one that decides the design: realised ensemble gain.** `Delta = Q(ensemble) - Q(best single member)`, reported for A2, A3 and A4, against A1's single point. Read against §3.2's table: the design predicts `rho_bar(A2)` low enough that `Delta(A2)` retains a usable fraction of the independent-errors gain.

**Tertiary: the §6 frontier.** Plot `(C, Q)` for A1 through A5. This exercises the replacement metric at small scale and is the only place in this repository where it would have been used on real numbers.

**Refutation conditions, pre-committed:**

1. **If `rho_bar(A2)` is statistically indistinguishable from `rho_bar(A3)`**, then training on disjoint corpora does not decorrelate errors at this scale and lineage level. The adapters are not carrying a diversity budget, §3.1's single point of failure is empty, and **the domain axis loses its diversity justification entirely.** The architecture should then collapse to one domain-general parent plus a size ladder, which is a substantially cheaper system and would be the correct thing to build. This is the result that would refute the design, and it is a useful result.
2. **If `rho_bar` separates but `Delta` does not** (A2, A3 and best-single-member all within margin), decorrelation is real and not exploitable by the aggregation rules tested. That refutes the composition mechanisms of §4 rather than the diversity claim, and points at A4-style selection over A2-style mixing.
3. **If A5 lifts quality over A2 with no adjudication of any kind**, the gain is protocol-internal, which is C-02's confidence-weighting route and Zhu et al.'s Theorem 1, and the diversity argument is not what is doing the work. Record the steelman in advance: that route buys its calibration with external supervision, so it is not free of exogenous signal either, and the calibration cost must be reported as a separate ledger line.
4. **What a positive does not license.** A2 beating A3 at 7B with adapters says nothing about 2.8T towers. It is evidence that corpus disjointness produces decorrelation at all, which is currently supported by nothing. It is not evidence about F2 and must never be reported as such.

**One limitation stated up front, not in a footnote, and it is smaller than an earlier draft claimed.** The **adapter** arms A1 to A5 test diversity at **L5**, adapters over one frozen backbone, which is the level where diversity should be hardest to find. That makes a positive strong and a negative weak: a null at L5 does not refute the claim at L2 or L0.

**The earlier statement that testing below L5 "requires separate pretraining runs and is out of reach on this card" is withdrawn. It is false.** A 125M pretrain is 9.579 GPU-hours at the corrected throughput, so §7.3.1's pretrain replicate reaches **L0 / `λ = 0`** for 229.9 GPU-hours at one seed, and sweeps `g` across the whole `λ = 1` segment for a further 146.9. The card can reach the level F13 actually asserts, and the design should use it. **Where a result is reported, the arm's lineage level must be stated with it**, because A2 and P2 answer the same question at two levels and pooling them would be exactly the error §1.1 exists to prevent.

Three instruments now reach three different lineage levels and none of them substitutes for another:

| Instrument | Lineage reached | Control over corpora | Where |
|---|---|---|---|
| Adapter arms A2 vs A3 | **L5 / `λ = 2`** | Full | §7.3 |
| Pretrain arms P2 vs P3 | **L0 / `λ = 0`** | Full, at 125M | §7.3.1 |
| `g`-sweep | **the `λ = 1` segment**, parameterised | Full, at 125M | §7.3.1 |
| F13 limb (a), open-weight models of distinct lineage | `λ = 0` at real scale | **None** | `LOGOS_HARNESS.md` §1.1 |

Limb (a) has real lineage diversity at real scale and no control over the corpora; §7.3.1 has full control over the corpora at 125M. **Neither alone settles the question and the set does not either.** Run them; report them separately with their level attached; do not pool them.

### 7.5 The nearly-free companion measurement

Separately, and much cheaper: measure the cascade exit rates `e` of §5.4 using an existing open-weight model family that ships several sizes from one lineage. That measures the input the entire cost argument depends on, on the same card, with no training step anywhere.

**Note the instrument inverts between the axes, and this is the point.** A same-lineage family is the **right** instrument for the size axis, because same-lineage is what the size axis is, and the **wrong** instrument for the domain axis, where `LOGOS_HARNESS.md` §1.1 already establishes that distinct lineage is the treatment variable and two finetunes of one checkpoint cannot fill a slot. An experiment that used one family for both would measure nothing on the domain axis and would look like it had.

### 7.6 Budget

Parametric, because the throughput term is an assumption and asserting it as a measurement would be the error this whole repository is written against.

```
per-adapter training cost = T_adapter / r_train
```

Instantiating with `T_adapter = 50e6` tokens and an **assumed** `r_train = 2.0e3` tokens/s for QLoRA at rank 16 on a 7B NF4 base with gradient checkpointing:

| Line | GPU-hours |
|---|---:|
| A2, 8 adapters at 50M tokens each | 55.6 |
| A3, 8 adapters at 50M tokens each | 55.6 |
| A1, 1 adapter at 400M tokens | 55.6 |
| **Training subtotal** | **166.7** |
| Evaluation, 5 arms over the battery, batched | 30 to 90, unmeasured |
| **Total** | **197 to 257** |

Derived, at an assumed 0.45 kW board plus host:

| Total GPU-h | Energy | At EUR 0.30/kWh | Rented at USD 0.22/h |
|---:|---:|---:|---:|
| 197 | 89 kWh | EUR 27 | USD 43 |
| 257 | 116 kWh | EUR 35 | USD 57 |

**The pretrain replicate, priced separately and on a firmer basis.** §7.3.1's runs are costed against `F9_PREREGISTRATION.md` §8.1's **corrected and derived** 125M throughput of about 29k tokens/s, not against this subsection's assumed `r_train`, so these figures do not inherit the assumption above:

| Line | Runs | GPU-h | Energy at 0.35 kW | At EUR 0.30/kWh | Rented at USD 0.22/h |
|---|---:|---:|---:|---:|---:|
| P1 + P2 + P3, one seed | 17 | **229.9** | 80 kWh | EUR 24 | USD 51 |
| `g`-sweep, four points, one seed | 32 branches + 3 seeds | **146.9** | 51 kWh | EUR 15 | USD 32 |
| Second seed on P1 to P3 | 17 | 229.9 | 80 kWh | EUR 24 | USD 51 |

**Comparator:** `F9_PREREGISTRATION.md` §8.1 budgets 1,402.6 GPU-hours for the observation-bound experiment. The adapter experiment is roughly one seventh of that and the pretrain replicate plus `g`-sweep is roughly one quarter; all three test different claims and none substitutes for another. `r_train` and the evaluation line are the two remaining assumptions in the adapter budget; both are measurable in a single short profiling run before committing the budget, and that profiling run should happen first. **The pretrain lines do not need it**, because F9's throughput correction already paid for that derivation on the same card at the same model size.

---

## 8. Narrowing F2: the composition-gap scaling ladder

**Nothing in this section is evidence for F2. It is a specification for obtaining evidence, and no rung has run.**

### 8.1 What F2 currently is, and why it cannot be settled as stated

`logos.tex` §15 states F2's falsifying observation as "composed ensemble scoring below a matched jointly post-trained baseline at any scale from 7B upward". `REVIEW_ROUND2.md` §7 observes that this is **already satisfied by the paper's own cited source at zero GPU cost**: Branch-Adapt-Route reports 49.1 composed against a jointly post-trained baseline of 50.5 with mid-training, and 49.1 < 50.5. §3.2 of the paper even concedes "Branch-Adapt-Route matches a retraining baseline; it does not beat one" without noticing that this satisfies its own falsifier as written.

**F2 is mis-specified as a level test.** A level test at one scale cannot constrain a 400x extrapolation, in either direction. Passing it at 7B would not license 2.8T and failing it at 7B does not forbid 2.8T. The quantity that constrains an extrapolation is a **trend**.

The owner holds the 2.8T bet as a strong prior and is working toward it as a longer-horizon goal. The paper's job is not to adjudicate that prior. It is to **label it** and to **specify the cheapest path to evidence**. This section is that path.

### 8.2 The quantity

Define, measured identically at every rung:

```
Delta(N) = (composed ensemble quality) - (baseline quality)
```

at fixed `N` per expert, on a fixed task suite. **The claim under test is not any single value of `Delta`. It is the shape of `Delta(N)` in `log N`.**

**The baseline arm must be frozen before any rung runs, and the choice is not cosmetic.** Two readings are in circulation and they disagree in sign at the only point that exists:

| Baseline | `Delta(7e9)` from BAR's published table |
|---|---:|
| Jointly post-trained monolith, with mid-training (50.5) | **-1.4** |
| Jointly post-trained monolith, without mid-training (47.8) | **+1.3** |
| Best single expert | not reported by BAR; unavailable |

The recorded anchor `Delta(7e9) = -1.4` (`TIER0_3090_PLAN.md`, `REVIEW_ROUND2.md` §7) uses the first row. The owner's framing of `Delta` as "composed minus best single expert" is a **third** quantity that BAR does not report, so adopting it would discard the only anchor that exists. **Recommendation: freeze on `Delta_joint` against the with-mid-training arm.** It is the arm BAR itself performs per expert, so it is the matched comparison; it is the one F2 is actually about; and it is the one with a data point. Record explicitly that the weaker arm flips the sign, so any rung reported against an unstated baseline is uninterpretable.

### 8.3 The rungs

| `N` per expert | Where it runs | Status |
|---|---|---|
| ~1B | The owned RTX 3090, 24 GB | Not run |
| **7B** | The owned card. **Branch-Adapt-Route's published point.** `Delta(7e9) = -1.4` recorded, see §8.5 for the caveat that matters | Published, not re-measured under this harness |
| ~24B | The owned card quantized, or a pooled worker | Not run |
| 70B | A rented datacenter accelerator, or a pooled multi-worker run. Does not fit the owned card: 70B at NF4 is 37.2 GB of weights before optimizer state or activations | Not run |

**What four points buy, stated without inflation.** The extrapolation from BAR's single 7B point to 2.8T is 400x, which is 2.602 decades. Anchoring at 70B leaves 40x, which is 1.602 decades. That is a **38.4% reduction in log span**, not a halving; the figure is worth stating correctly because this document's whole argument is that overstated numbers get caught. The larger gain is categorical rather than proportional: **one point becomes four, so a shape is observable rather than only a level.** A single point cannot be monotone, cannot turn over, and cannot be extrapolated by anything except assumption. Four points spanning 1.845 decades can.

### 8.4 Cost per rung

Two variants, and they measure different quantities. Whichever is chosen must be frozen across every rung.

**Variant A: full continued pretraining per expert plus a matched full-retrain joint baseline.** This is what BAR did and it is what makes `Delta(7e9) = -1.4` an anchor. `REVIEW_ROUND2.md` §7 costs a three-point 1B/7B/24B ladder, both arms, at **4.24e22 FLOPs, about 40,000 H100-hours, $79k to $131k**, with a **1B pilot rung alone at about 1,240 H100-hours, $2.5k to $4.1k**. Those figures are the review's derivation, not this document's, and its implied effective throughput is 2.94e14 FLOP/s.

Extending Variant A to the 70B rung: **not derived.** The review does not publish the token budget per rung, so it cannot be determined whether its cost scales linearly in `N` (fixed tokens per expert) or quadratically (compute-optimal `D = 20N`). Both readings, at the review's own implied throughput:

| Scaling assumption | 70B rung FLOPs | H100-hours | Cost at the review's implied rate |
|---|---:|---:|---:|
| Linear in `N` | 9.28e22 | ~87,500 | $173k to $287k |
| Quadratic in `N` | 3.32e23 | ~313,000 | $618k to $1.03M |

A factor of 3.6 separates them and **publishing the review's per-rung token budget resolves it**. Until then, the 70B rung's Variant A cost is a range, not a figure.

**Variant B: an existing open-weight checkpoint at each size as the common seed, LoRA expert specialisation, light router training, and a LoRA-on-union joint baseline.** Estimator `C ≈ 4ND` for LoRA over a frozen base (forward plus input-gradient backward, no weight gradients on frozen parameters). Instantiating with `E = 4` experts, `D_spec = 2e8` tokens per expert, and a joint arm at `4 x D_spec` on the union corpus:

| `N` | FLOPs | On the 3090 at an assumed MFU 0.25 | On a datacenter part at 2.94e14 FLOP/s | NF4 weights |
|---|---:|---:|---:|---:|
| 1B | 6.40e18 | 100 GPU-h | 6 GPU-h | 0.5 GB |
| 7B | 4.48e19 | 701 GPU-h | 42 GPU-h | 3.7 GB |
| 24B | 1.54e20 | 2,404 GPU-h | 145 GPU-h | 12.8 GB |
| 70B | 4.48e20 | does not fit | 423 GPU-h | 37.2 GB |

`MFU = 0.25`, `D_spec = 2e8` and `E = 4` are assumptions. A short profiling run settles the first and it should happen before any budget is committed. Evaluation cost is **not derived**; it is dominated by training at 24B and 70B and is comparable to it at 1B.

**The problem Variant B creates, stated rather than hidden.** Variant B is roughly two orders cheaper and it changes what `Delta` means: the baseline becomes a LoRA-on-union model rather than a full retrain. **The existing anchor `Delta(7e9) = -1.4` is a Variant A measurement and is not a point on a Variant B ladder.** So a Variant B ladder starts with zero anchors and must re-measure 7B itself, which its own table says costs 701 GPU-h on the owned card. That is affordable and it is the recommended path, but it must not be presented as inheriting BAR's point.

### 8.5 The scaffold, which is the actual contribution and is unglamorous

**The measurement must be identical across rungs or the points never compose into a trend.** Four rungs measured four different ways are four one-off results, and the extrapolation they were run to constrain remains exactly as unconstrained as it was. Everything below must be frozen once, before the first rung, and versioned:

- **Task suite.** One frozen battery, one file, one hash. Same items, same order, same prompt templates at every rung. No per-rung task selection, no "the 1B model could not do the hard split".
- **Composition mechanism.** One mechanism per ladder, per §4.5. Per-query k-of-N selection and logit-level mixing are different ladders and their points do not interleave.
- **Scoring function.** One scorer, one version, deterministic, with its decoding parameters fixed. A scorer change between rungs is indistinguishable from a `Delta` change.
- **Seed protocol.** Number of seeds per arm fixed in advance and identical at every rung, with the aggregation rule (mean, and which dispersion statistic) fixed. A rung with more seeds is not a better version of a rung with fewer, it is a different measurement.
- **Tokenizer treatment.** The composition mechanism's minimum lineage level from §1.1 must be the same at every rung. Mixing logits at one rung and selecting whole outputs at another measures two different things under one symbol.
- **Expert count and domain assignment.** `E` fixed. The domains the experts specialise on fixed. BAR used four (mathematics, code, tool use, safety); matching that keeps the 7B anchor usable under Variant A.
- **Specialisation budget rule.** Either `D_spec` fixed across rungs or `D_spec = alpha x 20N`, committed in advance. This is not a detail: under a fixed budget a larger model receives relatively less specialisation, which would push `Delta` down at large `N` **for a reason unrelated to routing**, and would look exactly like the failure the ladder exists to detect. Whichever rule is chosen, it is a declared confound and must be reported alongside every point.
- **Baseline arm**, per §8.2.

**The payoff of freezing.** With the scaffold fixed, **every experiment run against it becomes a permanent data point, including runs performed for other reasons.** A rung run for an unrelated purpose, by a different person, later, still lands on the same plot. Without it, each run informs only itself. This is the entire reason the section exists, and it is worth less attention than it deserves precisely because it is boring.

### 8.6 The harness interface, concretely enough to build

One rung is one invocation. It takes:

- `scaffold.lock` : the frozen scaffold above, content-hashed. A rung refuses to run if the hash does not match the ladder's declared hash. This is the single mechanism that makes rungs comparable, so it is a hard failure and not a warning.
- `N` : parameter count per expert.
- `seed_checkpoint` : the common seed, identified by an immutable reference (a model hash, not a name).
- `corpora[E]` : the E specialisation corpora, content-hashed, with the pairwise overlap matrix of §7.2 attached.
- `variant` : A or B, per §8.4.
- `seeds[]` : the seed list, length fixed by the scaffold.

It emits, per rung, one immutable record:

- `Delta` with its dispersion statistic across seeds.
- The **component scores** that `Delta` was computed from: composed, baseline, and every individual expert. Emitting only the difference makes a later re-derivation under a different baseline impossible, which is exactly the situation §8.2 is currently in with BAR's numbers.
- The full `(C, Q)` pair of §6 for the composed arm and every baseline, so the ladder also populates the frontier.
- Router diagnostics: dispatch distribution over experts, and per-item routing decisions, so a turnover in `Delta` can be attributed to misrouting rather than merely observed.
- `rho_bar` across experts per §7.4, so the ladder measures diversity decay with scale as a by-product. This costs nothing extra and it is the quantity §3 says everything depends on.
- The scaffold hash, the variant, the realised token counts, the GPU-hours consumed, and every assumption instantiated at run time.

Records append to one ladder file. They are never edited, and a re-run under a changed scaffold gets a new hash and starts a new ladder rather than overwriting points on the old one.

### 8.7 The pre-registered shape, committed before any point exists

**This is the strongest move available here and it should be stated as such.** Pre-registering the extrapolation shape before the data exists is what separates this from fitting a curve to whatever comes back. It costs nothing and it is not recoverable afterwards.

Committed in advance, across **at least three rungs**:

1. **`Delta(N)` flat or increasing in `log N`.** The extrapolation to 2.8T is **supported**, and the bet stops being a conjecture and becomes an evidence-backed extrapolation. It is still an extrapolation across the remaining 1.602 decades and must still be labelled as one.

2. **`Delta(N)` monotonically decreasing across three or more rungs.** **F2 is refuted. The five-tower architecture should not be built.** Stated plainly and pre-committed, in the same terms as the repository's existing published negatives: the composition gap widens with scale, a 400x extrapolation from 7B is extrapolating the wrong way down a curve, and the correct response is to stop, not to add rungs until the trend reverses. The architecture that survives a refutation here is the domain-general parent plus size ladder of §7.4 condition 1, which is a much cheaper system.

3. **Ambiguous or non-monotone.** Not support. **The default reading of a messy result must be "unresolved", never "consistent with the hypothesis"**, and stating that in advance is the point of stating anything in advance. Two named sub-cases:
   - **Non-monotone with a turnover**: `Delta` rises then falls. The turnover point is the informative quantity and it should be bracketed by adding a rung between the two scales that straddle it, not by extending the ladder upward.
   - **Flat within noise across all rungs**: the ladder lacks power, not the hypothesis lacks support. Resolved by more seeds per rung at the existing scales, which is cheaper than a new rung, before any conclusion is drawn.

**What the ladder is built to detect.** `ARCHITECTURE_REVIEW.md` F-04 names the failure mode expected to worsen with scale: when experts are weak and narrow a misroute is cheap, but when each expert is itself strong a misroute costs the full quality gap between two strong models, while the router trains on far less signal than any expert it dispatches to. If that mechanism is real, **it shows up as `Delta(N)` turning over**, and the router diagnostics of §8.6 are what would attribute the turnover to misrouting rather than leaving it as an unexplained decline. The ladder is designed around that specific prediction, and case 2 above is what happens when the prediction is right.

---

## 9. The bootstrap ladder, and why `R(C)` is the only term that matters

**Nothing here has run. None of it is evidence.** This section restates `logos.tex` §12's observation bound as a growth equation, which converts a qualitative thesis into one with a measurable free parameter.

### 9.1 The setup

A model at parameter count `N`, having produced enough adjudicated tokens, trains the next rung at `2N`. Under the paper's stated data law `D_opt = 20N`, training the `2N` rung needs `40N` tokens.

### 9.2 Result 1: the ladder is nearly free in total tokens, and this is favourable

Because each rung needs `20N` and `N` doubles, the sum is a geometric series dominated by its final term. Two readings, both computed:

| Ladder | Total tokens | Against 5.600e13 for the top rung alone |
|---|---:|---:|
| 12 doublings from 1e9, landing at 4.096e12 | 1.638e14 | **2.92x** |
| Landing exactly on 2.8e12, 12 rungs from 1.367e9 | 1.120e14 | **2.00x** |

The two differ because `log2(2800) = 11.451` is not an integer, so a 12-doubling ladder from 1e9 overshoots the target. The closed form for the exact-landing case is `40 x N_top - 20 x N_0`, which is 1.11970e14 and confirms the sum.

**The conclusion is identical under both readings and is robust to the discrepancy: bootstrapping does not blow up multiplicatively.** The overhead is a small constant between 2 and 3, not an exponential. The intuition that "it is just a doubling" is correct on token economics, and every rung below the top is, in aggregate, cheaper than the top rung itself. Token economics is not what stops the bootstrap.

### 9.3 Result 2: the binding quantity is adjudicated tokens, not tokens

Unadjudicated self-generated tokens **do not count at any volume**. Recursive self-training without exogenous grounding provably degenerates through entropy decay and variance amplification, and if the fraction of exogenous grounded signal vanishes asymptotically, degeneration follows (Zenil, arXiv:2601.05280, already cited in the paper as result (3) of §12.2). Producing more unadjudicated tokens does not move the ladder; it moves the failure mode.

Measured against the 5.6e13 requirement for the top rung, using the harness's own figures:

| Adjudication source | Tokens per trajectory | Adjudicated tokens | Short by |
|---|---:|---:|---:|
| Substrate B, demonstrated lifetime (94 adjudications) | 1e4, the paper's figure | 9.4e5 | **7.78 orders** |
| Substrate B, per quarter (3,000 trajectories) | 1e4, the paper's figure | 3.0e7 | **6.27 orders** |
| **Emulator at 1e6 trajectories** | **310, the frozen geometry** | **3.10e8** | **5.26 orders** |

**A correction to this document, and it is a 32x one.** An earlier draft priced the emulator row at 1e4 tokens per trajectory, borrowed from the Substrate-B figure, and got 1.0e10 adjudicated tokens and a 3.75-order shortfall. **That is wrong.** The Substrate-A trace geometry is **frozen** at `LOGOS_HARNESS.md` §3.2 and `F9_PREREGISTRATION.md` §5.1: 90 tokens per frame after the collapse decision (not 270), two frames per trace, about 130 loss-bearing tokens, **about 310 tokens per trace**. Using 1e4 overcounted the emulator's yield by `1e4 / 310 = 32.3x`. The geometry is frozen and the number in this document was the one that was wrong; it is corrected above rather than the geometry being adjusted to preserve the conclusion.

**The two Substrate-B rows stand unchanged, and the reason is that the paper owns them.** `logos.tex` §12.6 prices a Substrate-B trajectory explicitly and self-consciously at "generously $10^4$ tokens" and derives 6.3 and 7.8 orders from it. Substrate B traces are tower dialogue with reasoning and a horizon forecast, not RQ-VAE frame pairs, so the 310-token geometry does not apply to them. **The paper wins and this document does not revise its figure.** One consequence should be recorded rather than left implicit: the paper calls 1e4 generous, so **the 6.3 and 7.8-order figures are lower bounds on the Substrate-B shortfall**, and if a real Substrate-B trace turns out to be nearer 1e3 the shortfall grows by a further order.

These reproduce `logos.tex` §12.6's "six to eight orders" for Substrate B exactly, and extend the accounting to the emulator, which the paper prices only as "volume" without a number.

**The same shortfall read forward instead of backward, which is the more useful direction.** Since total ladder tokens are about `40 x N_top`, the parameter count reachable by bootstrap is **linear in cumulative adjudicated tokens** with coefficient `1/40`:

| Adjudicated-token supply | Reachable `N` |
|---|---:|
| Substrate B lifetime, 9.4e5 | **2.35e4 parameters** |
| Substrate B per quarter, 3.0e7 | 7.5e5 parameters |
| **Emulator, 1e6 trajectories, 3.10e8** | **7.75e6 parameters** |
| Required for 2.8e12 | 1.120e14 |

Two of those deserve to be read out loud. Substrate B's demonstrated lifetime yield bootstraps a model of **twenty-three thousand parameters**. And the emulator at a million trajectories bootstraps **7.75 million parameters**.

**The claim this replaces is withdrawn in full.** An earlier draft said the emulator at a million trajectories bootstraps 250M parameters, "which lands within 10% of §2.2's 277M edge tier", and drew the conclusion that the bottom rung of this document's own size ladder is approximately the emulator's bootstrap ceiling. **That conclusion rested entirely on the 32x overcount and it does not survive.** At the frozen geometry, reaching the 277M edge tier by bootstrap needs `40 x 2.77e8 = 1.108e10` adjudicated tokens, which is **3.57e7 traces, about thirty-six million**, against the one million the earlier draft asserted. The 277M edge tier is **1.55 orders** out of reach of a million emulator trajectories, not within 10 percent of it, and every rung above it is worse. The tidy coincidence is gone and nothing replaces it.

**Read the other way, which is now the only useful direction:** an emulator would have to produce about 36 million adjudicated traces to bootstrap the smallest artifact this document specifies. `F9_PREREGISTRATION.md` §8.1's own generation ledger produces 403,226 traces per grounded 125M arm, so the edge tier is roughly **89 arms' worth of generation** for the smallest model in the ladder, and this is the substrate whose adjudication is measured in milliseconds. That is the shape of the observation bound stated in units somebody can act on, and it is worse than the earlier draft made it look.

### 9.4 Result 3: the formulation that matters

**The ladder's doubling cost is `40N / R(C)`, where `R` is adjudicated-token throughput** in whatever unit the programme is metered in (GPU-hours, dollars, kWh, adjudication events; state which, never wall-clock).

**`R` is written as a function of capability and not as a scalar, deliberately, and an earlier draft of this subsection got that wrong.** It treated `R` as a fixed quantity of the programme to be maximised by picking a better adjudicator. It is not fixed: §9.6 establishes a capability threshold `C*` below which a model produces nothing adjudicable at all, so `R(C) ~ 0` below `C*` and positive above it. Every sentence in this subsection that reads as though `R` were a constant should be read as a statement about `R` at a fixed capability.

Everything else in the paper is a constant factor on that expression. Sparsity changes the compute per token. Quantization changes the memory per parameter. Routing granularity changes the round trips per query. Serving topology changes the accelerators per tower. The size ladder of §2.2 changes the parameters per query. **Not one of them appears in the exponent.** They multiply the constant; `R(C)` sets the rate.

Equivalently, and more sharply: cumulative adjudicated tokens `D_adj` and reachable parameters are related by `N ≈ D_adj / 40`, so `dN/dD_adj = 1/40` **regardless of every mechanism in sections 2 through 11 of the paper.** The architecture decides what a parameter costs. `R(C)` decides how many there are.

**And that makes the programme's central question a growth-rate comparison rather than a maximisation.** `dN/dD_adj = 1/40` is the demand side and it is a constant. `R(C)` is the supply side and it is a function of the capability the ladder has already reached. **The ladder is self-sustaining where `R(C(N))` grows at least as fast as `N` and stalls at the first rung where it does not**, so "maximise `R`" is the wrong instruction and "measure the shape of `R(C)` near `C*`" is the right one. §9.6 specifies that measurement.

This is `logos.tex` §12's observation bound stated as a growth equation rather than a qualitative claim, and the conversion is the contribution: a qualitative bound cannot be optimised against, and a rate function can be measured.

### 9.5 The consequence, which reframes the research programme

At a fixed capability `C` above `C*`, `R(C)` is largest for adjudicators that are simultaneously **cheap** and **non-internalisable**, and those two properties trade off directly against each other. The table below ranks adjudicators at fixed capability; §9.6 is what sweeps the other axis, and the two must be read together, because an adjudicator's rank can change with capability (internalisability is itself a statement about how capable the model is):

| Adjudicator | Cheap | Non-internalisable | Yield behaviour |
|---|---|---|---|
| Emulators and games | **Very** | No. A deterministic program a large enough model can internalise | Decays toward zero. Already conceded in `LOGOS_HARNESS.md` and in `logos.tex` §12.7 |
| Reality, the psychohistory substrate | No | **Yes.** This is the entire point | Unbounded, but `R` is 6 to 8 orders short (§9.3) |
| **Code execution** | **Yes** | Deterministic, so internalisable in principle, but the program space is effectively unbounded, so yield decays **slowly** | **The best known point on the trade-off** |
| Formal proof checking | Yes | Same shape as code execution: decidable per instance, unbounded in instance space | Candidate, unmeasured. Named here so it is not overlooked |

**Code execution is why Absolute Zero works, and the executor is doing all the work.** `logos.tex` §12.2 result (4) already says the executor "is not a detail, it is the entire source of correction". §9.4 says why that sentence is the load-bearing one in the section: the executor is a high-`R(C)` non-internalisable-in-practice adjudicator, and it is the only one in the four cited results that is both.

**So the honest open research question is not "can we afford 2.8T". It is "which adjudicator gives the fastest-growing `R(C)`, and does it grow fast enough to keep up with `N`."** Stated as a maximisation over a scalar it would be the wrong question, for the reason §9.4 gives: a large constant that stops growing stalls the ladder just as surely as a small one.

That reframing has a property the parameter ladder does not: **it is attackable on one consumer accelerator.** Measuring `R(C)` for a candidate adjudicator requires generating trajectories at several capability points, adjudicating them, and scoring yield per unit of metered resource. None of that needs a frontier model, and the harness of `LOGOS_HARNESS.md` already specifies most of the machinery. Nothing at the top of the parameter ladder is attackable that way, at any budget available here.

### 9.6 `R` is a function of capability, and the threshold is the cheapest decisive measurement in the programme

**Conjecture. Nothing here has run, and the measurement specified below has not been designed past what is written.**

**A correction to this document's own framing first.** §9.1 sets the ladder up as a model at `N` training its successor at `2N`, which invites the reading that a model can only train its successor when generator scale matches learner scale. **That reading is wrong and it is withdrawn.** Scale is not what decides whether a model can produce an adjudicable trajectory.

What decides it is a **capability threshold `C*` for tool use and agentic operation.** Below `C*` a model cannot reliably emit a well-formed tool call, cannot drive a shell, cannot carry a multi-step generalised analysis to a checkable end state, and therefore **generates nothing an adjudicator can rule on**: its raw output volume is irrelevant because its adjudicable yield is zero, and §9.3 already established that unadjudicated tokens do not count at any volume. Above `C*` the same model can generate trajectories over an external world whose instance space is effectively unbounded, and yield per attempt becomes positive.

So §9.4's `R` is not a constant of the programme. It is a function of capability:

```
R = R(C),     R(C) ~ 0 for C < C*,     R(C) > 0 and increasing for C > C*
```

and the question that decides everything, **is the ladder self-sustaining or does it stall at some rung `N`**, reduces to a comparison of growth rates. §9.4 gives the demand side: each rung needs `40N` adjudicated tokens and `dN/dD_adj = 1/40` regardless of every mechanism in the paper. `R(C)` is the supply side. **The ladder sustains itself where `R(C(N))` grows at least as fast as `N`, and stalls at the first rung where it does not.** Nothing in this repository has measured the supply side at all, at any capability, for any adjudicator.

**The measurement, specified. It requires no training run, which is what makes it the cheapest decisive experiment here.**

- **Instrument.** A sequence of open-weight models of increasing capability at **fixed quantization**, so that the axis swept is capability and not memory footprint or precision. Sequential inference on the owned card, no gradient step anywhere, which is the same instrument shape `TIER0_3090_PLAN.md` uses for F13 limb (a).
- **Battery.** One frozen battery of **tool-mediated tasks with programmatic adjudication**: shell invocations with checkable post-conditions, code with a test suite, retrieval and OSINT queries with verifiable answers, and computer-use tasks with an end-state check. Frozen once and content-hashed. **§8.5's scaffold rules apply here unchanged and for the same reason**: a battery that changes between capability points measures the battery.
- **Endpoint.** **Adjudicated yield per attempt**, that is the fraction of generated trajectories an adjudicator rules on at all and rules correct, together with adjudicated tokens per unit of metered resource (GPU-hours, kWh or dollars; state which, never wall-clock).
- **What it returns.** `C*`, the capability at which yield leaves zero, and **the shape of `R(C)` immediately above it**, which is the term that decides whether the bootstrap compounds.
- **What it does not return.** It does not measure `R` at tower scale, and a shape fitted over open-weight models in the roughly 0.5B to 70B range is an extrapolation above that range like any other in this document. It does not settle which adjudicator to use; it measures the yield of the adjudicators it is given, which is §9.5's cheap-versus-non-internalisable trade-off made numerical rather than argued. And a threshold measured at fixed quantization is a threshold for that quantization; whether `C*` moves under 4-bit serving is a second sweep and is not specified here.

**Why it gates everything downstream.** Every token figure in §9.2 and §9.3 and every cost figure in §8 is priced in tokens the programme assumes it can generate. If `R(C)` is flat above `C*`, the ladder stalls at the first rung whose demand exceeds supply, and **no architecture in this document changes that**, because §9.4 already showed the architecture only moves the constant. If `R(C)` is superlinear in `C` and `C` is superlinear in `N`, the bootstrap is self-sustaining and the interesting question moves back to which adjudicator to build. **It is desk work plus one card, it precedes §7's training in the order of work, and it has not been costed in GPU-hours here because the battery does not exist yet.** Costing it is the first token spend this section owes.

### 9.7 Three mechanisms that must be kept separate, and the test that separates them

**Conjecture and taxonomy. Nothing here has run, and one of the three items has no cost model anywhere in this repository.**

§9.5 ranks **adjudicators**. This subsection ranks **sources of exogenous bits**, which is a different axis, and the three items below are routinely collapsed into "bootstrapping" when only one of them is bootstrapping.

**The membership test: do bits enter the system from outside the model?** Everything else is presentation.

**1. Data acquisition. This is not bootstrapping, and it is the strongest item here.** Un-OCR'd scans, video, instrument and sensor readings, physical archives: real human-produced or world-produced tokens that were never in any training set. There is **no collapse risk**, because the tokens are not model-generated and Zenil's degeneration result is about recursive self-training. There is **no adjudication step**, because there is nothing to adjudicate: the bits are exogenous by construction, so they do not appear in `R` and should never be counted as part of it. And it attacks the token ceiling **directly**, because every supply estimate this programme reads, including the central `6e13` of §1.5 and the `2e14` upper bound, counts the **digitised** corpus and not the corpus. **This is the item most likely to move the binding quantity, it is the one the ladder framing obscures by putting it in the same bucket as self-generation, and §10 is where this document argues it.**

**2. Tool-adjudicated trajectories. This is bootstrapping, and it is the high-`R` adjudicator class.** Bash, code execution, test suites, checkable OSINT queries, computer use, and the emulator substrate of `LOGOS_HARNESS.md` §3. This is Absolute Zero's mechanism, it is `logos.tex` §12.2's result (4) where the executor "is not a detail, it is the entire source of correction", and it is the class §9.5 ranks as the best known point on the cheap-versus-non-internalisable trade-off. **It is what `R(C)` in §9.6 measures.**

**3. Multi-persona critique. Ruled out as a source of improvement, and named here so nobody rebuilds it as one.** §4.4 rules out multi-round tower debate under C-02. **The same ruling covers multi-persona critique, self-consistency over personas, and every variant whose only new bits are the model's own**, because the martingale result does not care whether the participants are called towers or personas and Choi et al. extend it to heterogeneous agents explicitly. It has exactly one legitimate use: **as a candidate generator feeding an adjudicator**, where its output is a proposal that something outside the model then rules on, and **the improvement is credited to the adjudication and never to the critique**. `LOGOS_HARNESS.md`'s disagreement gate is that use, and `F9_PREREGISTRATION.md`'s A4 ungated-grounded arm exists precisely so the gate's contribution is identified separately from the grounding's, without which the gate effect under grounding is unidentified. Anything that counts persona disagreement itself as improvement is claiming a published theorem is wrong, and §4.4 states what that costs.

**The ordering that falls out of the membership test.** Item 1 supplies exogenous bits and needs no model at all. Item 2 supplies fewer bits per unit of metered resource but compounds with capability, which is what §9.6 measures. Item 3 supplies none. **Nothing here has measured any of the three, and item 1 has no cost model, no corpus size estimate and no acquisition budget anywhere in this repository.** That absence is the largest unpriced item in the programme and §10.3 states the first number it owes.

### 9.8 Three caveats, stated here and not buried

1. **`20N` is Chinchilla, and Chinchilla is a dense law.** Applying `D_opt = 20N` to sparse **total** parameters is precisely the defect `logos.tex` §2.3 concedes under X-01 and registers as falsifier **F1**. The true sparse coefficient is unknown, the mixture-of-experts scaling literature reports a token-per-parameter ratio that is neither twenty nor constant in scale, and it reports the ratio **decreasing** with scale. **Every figure in this section is an order-of-magnitude placeholder and must be read as one.** The 2.92x overhead, the 1.120e14 requirement, the 250M emulator ceiling and the 7.78-order shortfall all move if F1 fires. The shape of the argument does not, because the geometric-series result and the linearity of `N` in `D_adj` hold for any linear data law, only the coefficient changes.

2. **Self-generated tokens are not equivalent to natural tokens even when adjudicated.** They are on-policy and narrower in distribution, while the `20N` law was fitted on natural text. So every token count above is **optimistic**, and by an unquantified factor. Nothing in this repository measures the exchange rate between an adjudicated on-policy token and a natural token, and until something does, the shortfalls in §9.3 are lower bounds on the shortfall.

3. **The corpus must accumulate rather than rotate.** Collapse is established when synthetic data *replaces* real data, and accumulating real and synthetic together avoids it (Gerstgrasser et al., arXiv:2404.01413). The loop of `logos.tex` §12.5 step 6 already specifies accumulation. It is restated here because a bootstrap ladder is exactly the structure in which someone would be tempted to discard rung `N`'s corpus when training rung `2N`, and doing so would convert the ladder into the failure mode result (3) describes.

---

## 10. Visual consumption of un-digitised archives, and why it may be the strongest attack on the data wall

**Conjecture throughout. Nothing in this section has run.** The density figures in §10.2 are the owner's estimates and not measurements, no pilot has been performed on any real scan, and §10.3 states the conditions under which the true cost is worse than the table. The prior-art status of the framing is **unresolved** and §10.1 says so at the point of claim.

This is §9.7's mechanism 1, **data acquisition**, argued at length because it is the item most likely to move the binding quantity and the one the bootstrap framing obscures.

### 10.1 The mechanism, and it is not new

The RQ-VAE that tokenizes Game Boy frames in `LOGOS_HARNESS.md` §3.2 is not specific to Game Boy frames. The same construction consumes a page scan directly as image tokens, with **no OCR stage to be wrong**. What survives that route and does not survive OCR: page layout, marginalia, handwriting, mathematical notation, diagrams, tables whose structure is geometric rather than tagged, and degraded regions where an OCR engine either guesses or drops the line without recording which it did.

**Claim no novelty for the mechanism.** Image-as-tokens into a single autoregressive stream is **Emu3** and **Chameleon**, both already cited in `logos.tex` §12.6's own description of the harness, and the codebook construction is the RQ-VAE lineage `LOGOS_HARNESS.md` already names (TIGER, MAGVIT-v2, and the residual-quantizer implementation it specifies). Presenting any of it as new would repeat round 2's C-04 for a third time in this repository.

**What may be unclaimed is narrower, and it has not been checked.** The framing that **visual consumption of the *un-digitised* archive routes around the token-supply ceiling, because the supply estimates count the digitised corpus and not the corpus**, is not a mechanism claim and is not covered by Emu3 or Chameleon. `PRIOR_ART_v03.md` did not search for it; it swept four mechanisms and this is not among them. **[NEEDS VERIFICATION]**, routed to the next prior-art sweep, and **it must not be asserted anywhere until that sweep runs.** The likely adjacent literature is document-understanding-without-OCR, historical-archive digitisation, and the token-supply estimates themselves, none of which this repository has read.

### 10.2 The measured cost, stated rather than hidden

One dense page of text is about **750 tokens** after OCR. The same page as image tokens, at three patch sizes:

| Patch size | Image tokens per page | Density penalty against 750 OCR'd tokens |
|---|---:|---:|
| 32 x 32 px | 8,137 | **10.8x** |
| 24 x 24 px | 14,522 | **19.4x** |
| 16 x 16 px | 32,754 | **43.7x** |

**Provenance and status.** These are the owner's estimates. They are internally consistent with a page of about 2,530 x 3,300 pixels, that is a 300 DPI scan of a Letter-sized page, with the counts being the per-dimension ceiling division of that geometry (79 x 103, 106 x 137, 159 x 206). **They are not measurements**, no pilot has been run on any real page, and §10.4 states why the true figure can only be worse. Nothing downstream should quote a single number from this table as a cost.

### 10.3 Why the trade is correct in this regime, which is the argument that matters

The penalty above is a **compute** penalty and it is between one and one and a half orders of magnitude. It is paid anyway, and the reason is the paper's own rather than this document's:

- **Proposition 1 establishes that sparsity removes the compute constraint.** `logos.tex` §2.1 and §2.2 are an extended argument that the dense arithmetic's compute bill is not what binds a sparse system, and §12's opening sentence states it flatly: "Sparsity removes the compute limit."
- **The data wall establishes that unique content is binding.** §11.4's Eq. (residency) against a central supply estimate near `6e13`, and §1.5's trilemma above, are the argument that unique tokens are the constraint that nothing in the architecture relaxes.

So the trade is: **pay roughly 20x compute per unit of content, to unlock content that has no text form at all.** That is trading the non-binding resource for the binding one, which is the correct direction whenever both statements above hold, and it is correct **because** of Proposition 1 rather than in spite of the penalty. **If Proposition 1 fails the argument fails with it**, and falsifier F1 is what would take both down together.

It is also, on §1.5's own terms, the only route to **response 3**. The trilemma is a function of a supply estimate that counts digitised text. An acquisition channel that adds un-digitised content raises the estimate rather than rearranging the architecture around it, and it is the sole mechanism in this programme that does.

**Three things this does not establish, and they are not small.**

1. **It does not establish an exchange rate.** Nothing here measures what a model trained on image tokens of a page learns relative to a model trained on the OCR'd text of the same page. §9.8's caveat 2, on self-generated tokens not being equivalent to natural tokens, has an analogue here that is entirely unquantified, and it could run in either direction: image tokens carry more (layout, notation, marginalia) and may teach less per token.
2. **It does not establish that the archive is large.** **Nobody in this repository has estimated the size of the un-digitised corpus in any unit.** That is the first number this line of work owes and it needs no accelerator, only a literature pass over library, archive and institutional-holdings figures. Until it exists, "routes around the supply ceiling" is a mechanism claim with no magnitude attached.
3. **It does not establish that acquisition is cheap.** Scanning, rights clearance and physical access are costs this repository has never priced in any unit.

### 10.4 The consequence that reorders the programme

`LOGOS_HARNESS.md` §3.2's Phase-1 gate requires, before any language-model training, that reconstructed held-out frames show **"HP-bar within 1px, menu and dialog text legible (OCR or human panel), sprite identity correct, codebook utilisation above 95%"**, at 160x144 in four colours, downsampled by a factor of 16 to 90 positions with 3 residual levels.

**That gate is the easiest possible instance of the text-preservation problem.** Four shades, a fixed 8x8 tile grid, one bitmap font, no antialiasing, no skew, no bleed-through, no foxing, no degradation, and the text sits in a fixed rectangle the reconstruction loss is already region-weighted on. Against that, 8-point serif on a foxed page scanned at 300 DPI is harder on every axis simultaneously.

**So the ranking changes, and it is not the ranking the harness currently implies: the Phase-1 RQ-VAE gate does not only gate Substrate A. It gates the entire visual-data thesis.** If a residual quantizer at that geometry cannot hold Game Boy dialog text, the un-digitised-archive route is not merely unproven, it is **refuted at its easiest instance**, and no amount of patch-size tuning on real scans is worth spending afterwards. The converse is weak in the way easy instances always are: a pass says little about the hard case and should be reported as passing the easy case.

**One repair in the harness's own failure list is an abandonment under this reading, and whoever runs Phase 1 must record which repair was used.** `LOGOS_HARNESS.md` lists, on gate failure, "more levels, bigger codebook, less downsampling, or **restrict to battle screens**". The first three are legitimate repairs for both readings. **Restricting to battle screens repairs the gate by removing most of the text**, which is a legitimate rescue for Substrate A's held-out-vocabulary design and is an abandonment of the text-preservation claim. The two readings diverge exactly there, and a gate log that does not say which repair was taken destroys the programme-level information for the sake of the substrate-level one.

**The pilot the density figures need.** §10.2's estimates assume clean synthetic geometry. A real pilot runs the same reconstruction gate on actual degraded scans: foxing, bleed-through, skew, marginalia, mixed scripts, handwriting, and variable type sizes down to footnote scale. Finer patches may be required to hold 8-point text, in which case **the penalty exceeds 43.7x and the 16x16 row is a floor rather than a worst case.** That pilot needs no language-model training, only the tokenizer and a held-out set of real scans, so it sits in the same cost class as the Phase-1 gate itself and should be run alongside it.

### 10.5 One threshold family, not two special cases

§9.6 defines a capability threshold `C*` below which a model generates nothing adjudicable. There is a second threshold implicit in this section: below some capability a model cannot make productive use of image tokens of a page either, because reading a scan is itself a tool-mediated act of the same kind, and a model that cannot carry a multi-step analysis to a checkable end state will not extract a table from a degraded scan.

**Treat them as one threshold family rather than as two special cases.** §9.6's measurement extends to it directly and at no structural cost: add page-reconstruction and page-comprehension items to the frozen battery, hold quantization fixed, sweep the same capability axis, and read the second threshold off the same instrument. Whether the two thresholds coincide is an empirical question and **this document does not assume they do**. What it does assume is that they must be measured on one instrument, because measuring them separately produces two numbers with no stated relation to each other and an open invitation to quote whichever is more convenient as the real one.

---

## 11. What this settles and what it does not

**Measurable now, on owned hardware, in the order they should be run:**

1. **`C*` and the shape of `R(C)`** (§9.6). **No training run, no gradient step, a frozen tool battery and sequential inference over open-weight models at fixed quantization.** It is the cheapest decisive experiment in the programme and it gates everything downstream, because §9.4's growth-rate comparison is undecidable without it and every token figure in §8 and §9 assumes a supply the programme has never measured. Its GPU-hour cost is **not yet derived**, because the battery does not exist; deriving it is the first token spend this document owes.
2. **Corpus overlap** under `logos.tex` §3.5's P1 criterion, which is falsifier **F11**, one of the two falsifiers of fourteen needing **no accelerator at all**, and which §7.2 runs as a by-product of the diversity experiment.
3. **Traffic skew**, from any real serving log, which is the other input to §5.3 and needs no accelerator.
4. **Cascade exit rates**, and therefore whether §5.4's break-even is cleared in practice (§7.5). One card, no training.
5. **Whether corpus disjointness decorrelates errors, and at which lineage level.** At **L5** with adapters (§7.3), at **L0** with 125M pretrains (§7.3.1, 229.9 GPU-h), and across the whole `λ = 1` segment via the `g`-sweep (§7.3.1, 146.9 GPU-h), which is the nano-scale instrument for **F14** and the only direct measurement of §1.5's trilemma anywhere.
6. **The Phase-1 RQ-VAE reconstruction gate**, which `LOGOS_HARNESS.md` already budgets for Substrate A and which §10.4 argues is a **programme-level** gate on the visual-data thesis. Free at the margin, because it is already in that plan.

**The token-efficiency thesis is measurable now.** Every input to §5 is a traffic distribution or an exit rate, and both are measurable on this card or on a log file.

**The capability thesis is not.** Whether four 2.8T domain parents with adapters outperform a 14T monolith, and whether Branch-Adapt-Route survives a 400x extrapolation from 7B with four experts to 2.8T with four towers, is falsifier **F2** and `ARCHITECTURE_REVIEW.md` **F-04**, which that document states cannot be closed by argument and needs a training run. **No experiment at this budget settles it.** Nothing in this document reduces that bet, hedges it, or makes it smaller. It only renames one of its components correctly (§4.2) and forces the lineage commitment it always required (§1.4).

**And one thing is settled by arithmetic rather than by measurement, which is unusual and worth flagging.** §1.5's trilemma is not waiting on a run. Given `f ≤ 1-g` and a central supply estimate near `6e13`, **no setting of `g` satisfies X-04, C-02 and F-04 at once**, and the architecture has to pick a corner. This document picks response 1: drop the diversity budget from the justification, carry the architecture on cost and the size axis. What the experiments above then buy is the **price** of that corner, not the decision.

Anyone reading §7's arms as evidence about F2 has misread them, and §7.4 condition 4 exists so that misreading is pre-empted rather than corrected afterwards.

**Two dependencies outside this file, recorded rather than fixed, because they bind figures this document quotes.**

- **Stand-in tower identity is unresolved and the two binding documents disagree.** `LOGOS_HARNESS.md` §7 specifies "at least two distinct open models" as the proposers; `F9_PREREGISTRATION.md` §8.1 specifies "two 350M-class stand-in towers" and derives the 137.9 GPU-hour generation ledger at 350M throughput. Either nothing trains those stand-ins or nothing pays to train them, and the generation ledger is not meaningful until it is settled. **§9.3's emulator accounting quotes that ledger's 403,226 traces per grounded 125M arm and therefore inherits the conflict.** This document assumes neither reading; where it quotes the ledger it quotes it as `F9_PREREGISTRATION.md`'s figure, and the "89 arms' worth of generation" comparison in §9.3 moves if the reading changes.
- **The proposal interface does not exist in any document.** `LOGOS_HARNESS.md` §5.3 renders observations as RQ-VAE codes and no off-the-shelf open model can read those, so multi-tower proposal requires a **second, structured-text observation view** that is unspecified everywhere. It determines what the disagreement threshold `tau_JS` is calibrated over, and therefore what `q = 0.25` means. **This document depends on it wherever it quotes emulator trajectory counts (§9.3) and it is blocking for those figures.** It does **not** block §9.6's `C*` measurement, which uses a tool battery and text-native tasks and touches no RQ-VAE codes; that independence is one of the reasons §9.6 sits first in the order above.

---

## 12. Open items

**Resolved since the previous revision**, listed first so nobody re-opens them. `PRIOR_ART_v03.md` is delivered and resolved items 1, 2 and 4 of the previous list: cross-model key-value reuse is §2.3.1 with seven papers to cite and differentiate; the looped-forward-pass lineage and the reasoning-not-knowledge distinction are both published and §4.3 now claims neither; and no primary source was found measuring ensemble gain among distilled siblings, **with the qualifier that the negative is weak because the phrase has no standard name**, per `PRIOR_ART_v03.md` §4a. The metric question is resolved into `logos.tex` §11.2. The lineage level is resolved into `logos.tex` §3.3, and §1.5 states what the resolution costs.

**Needing citation verification. Routed to the next prior-art sweep, which does not yet exist:**

1. **The un-digitised-archive framing of §10.1.** Whether anyone has already argued that visual consumption of un-digitised material routes around the token-supply ceiling. `PRIOR_ART_v03.md` did not search for it. **This must not be asserted until the sweep runs.**
2. **Minitron's attention layout** (arXiv:2408.11796), which `PRIOR_ART_v03.md` §7 item 8 could not resolve. If its width pruning changes `num_key_value_heads` or `head_dim`, §2.3.1's constant-KV-shape property does not survive a Minitron-style ladder construction. Directly load-bearing, needs the full paper.
3. **LayerSkip's KV mechanics** (arXiv:2404.16710), cited in §2.3.1 but **not primary-sourced**, and must be read before being relied on.
4. Distillation-ladder quality retention at the ratios in §2.2, in particular what a 277M child retains of a 2.8T parent, which the 156 MB figure makes attractive and nothing here justifies.
5. The model-merging literature on permutation alignment, which is where a `λ = 0` merge would have to come from if one exists (§1.2).

**Needing measurement, no accelerators required:**

6. **The size of the un-digitised corpus, in tokens or pages or any unit at all** (§10.3). This is the number that decides whether §10 is a mechanism with a magnitude or a mechanism without one, and it is a literature pass, not a run. **It is the largest unpriced item in the programme.**
7. Corpus overlap across the four domains (**F11**, still not run, no accelerator).
8. Residency-bound fraction `f` (**F12**, still not run, no accelerator). **Superseded in part:** `f` is no longer unbounded. It is bounded by `1 - g`, so **measuring `g` on an actual training plan bounds `f` without touching a corpus**, which is cheaper than the corpus measurement and should be done first.
9. Traffic skew across domains on a real serving log, which §5.3 currently assumes.

**Needing a decision, not a measurement:**

10. **The corner of §1.5's trilemma.** This document adopts response 1 (high `g`, no diversity budget in the justification), following `logos.tex` §3.3's own resolution. **If the owner prefers response 2 or 3, §3, §7 and §10 all change weight** and this document should be revised rather than reinterpreted.
11. The dispatch-granularity commitment, per §4.2. Per-query is recommended; per-layer is out of scope for wide-area; per-token needs an explicit RTT budget.
12. **Whether §7's diversity experiment runs at L5, at L0, or both**, per §7.3.1. Both is 229.9 GPU-h more than the adapter arms alone, plus 146.9 for the `g`-sweep, and only the pretrain arms reach the level F13 asserts.

**Needing derivation, and owed as the first token spend:**

13. **The GPU-hour cost of §9.6's `C*` measurement.** It is described and not costed, because the tool battery does not exist. `TIER0_3090_PLAN.md` carries the same debt for F13 limb (a) and F14, and all three should be derived together.

**Dependencies on documents this file does not own**, per §11: stand-in tower identity (`LOGOS_HARNESS.md` §7 against `F9_PREREGISTRATION.md` §8.1), and the missing structured-text proposal interface (`LOGOS_HARNESS.md` §5.3).

**Textual fixes owed to `logos.tex`.** Four of the five previously listed here have been applied in v0.3 and are recorded as closed:

14. ~~§3.5 and §12.3: weaken "disjoint pretraining" to "common seed, divergent continued pretraining", and state the lineage level.~~ **Applied**, as §3.3 plus falsifier F14.
15. ~~§11.1: replace the single cost case with three, and replace "traffic entropy" with "skew plus asymmetry".~~ **Applied**, and the paper goes further by stating that the entropy decision rule inverts under demand-proportional sizing.
16. ~~§11.2 and F10: replace eta.~~ **Applied**, and stronger than requested: eta is **retired**, AIQ is primary, APGR with CPT(50%) is secondary, and F10 is restated on AIQ at 0.02 and on CPT(50%) at ten percentage points.
17. **Still open. §9.2: the operative dispatch ratio is 60 serial round trips per token against 1 per query, not 960 against 1** (§4.2). The paper's §9.2 still leads with "Nine hundred and sixty dispatches per token against one per query", while its own latency derivation in the preceding paragraph says dispatch inside a layer is parallel and only layers are serial. The conclusion is right and the headline number is the wrong number, in the direction that flatters the conclusion.
18. **New. `logos.tex` §11.1 computes its three cost cases on five towers** while §3.5's criterion returns four and the paper keeps five "for continuity with the arithmetic". That is disclosed rather than hidden, so it is not an error, but the two arithmetics are not interleavable and a reader will try. Recommend one sentence in §11.1 saying which partition its shares are stated over.

---

## 13. Status

**Specification. Zero runs.**

No model has been trained. No adapter has been fitted. No 125M pretrain has been started. No corpus overlap has been computed. No traffic log has been read. No exit rate has been measured. No frontier has been plotted. No tool battery exists, so `C*` has not been located and the shape of `R(C)` is unknown. No page has been tokenized and no scan has been reconstructed. The 3090 has not been switched on for any of this.

Every table in this document is arithmetic over stated assumptions. §1.5's trilemma table is arithmetic over the paper's `f ≤ 1-g` against a **survey** token-supply figure that nothing in this repository verifies. §3.2's correlation table is a Beta-Binomial model with a chosen `p` and `k`. §5.3's cases use an illustrative traffic skew that nothing measures and a capacity proportionality that nothing verifies. §5.4's ratios use assumed exit rates. §6.4's degeneracy probabilities reuse A-02's own simulated per-cell rate. §7.6's adapter budget rests on an assumed training throughput that a short profiling run would settle and which nobody has run; its **pretrain** lines rest on `F9_PREREGISTRATION.md`'s corrected and derived 125M throughput, which is the firmest cost basis in this file. §9.6 and §9.7 are conjecture with a measurement attached and no measurement performed. **§10.2's density figures are estimates and a real pilot may make them worse by more than a factor of two.**

**Two numbers in this document were wrong in the previous revision and are corrected here rather than quietly adjusted.** §9.3 priced emulator trajectories at 1e4 tokens against a **frozen** 310-token trace geometry, a 32.3x overcount, and the conclusion it supported (that a million emulator trajectories bootstrap approximately the 277M edge tier) is **withdrawn**: the real figure is 7.75e6 parameters and the edge tier is 1.55 orders away. §7.4 asserted that testing below L5 was out of reach on the owned card, which is false at 9.579 GPU-hours per 125M pretrain, and the design is better for the correction.

The one thing this document was confident about was negative and was §1.4: **there is no composition mechanism that functions at L0**, so the paper's simultaneous demand for independently pretrained towers and for Branch-Train-MiX-style merging is not a design, it is two designs. **§1.5 now adds a second negative that is sharper and does not need a measurement either: `f ≤ 1-g` means no setting of `g` satisfies X-04, C-02 and F-04 at once.** Both are arguments, not measurements, and they are offered as such.
