# logos-harness

**Implementation specification for the loop described in `../logos.tex` §12, "The observation bound."**
Status: **SPEC, unbuilt. Nothing in this document has run on a GPU.** Every throughput, GPU-hour and cost figure here is arithmetic against a published hardware ceiling, not a measurement. Hardware: one RTX 3090, 24 GB, Ampere; bf16 and FlashAttention-2 available, **no FP8**, no NVLink, no second card.

**Companion artifact:** `F9_PREREGISTRATION.md` fixes everything this document leaves free (arms, seeds, endpoints, effect sizes, test statistics, multiplicity, stopping rule, kill conditions) and is the binding statistical design. Where the two disagree, the pre-registration wins.

**Revision note.** This version applies the round-2 referee findings in `REVIEW_ROUND2.md` that land on this file: C-01, C-02, C-04, C-05 and C-08 (§1, §1.1, §10), X-12 (§2.1, §4.1), P-08 and X-11 (§4), P-11 (§4.3), and the substrate-B and pretraining method-track conclusions (§3.2, §3.3, §5.2, §5.3, §5.4, §7, §8). Corrections are recorded inline where a previous claim was wrong, rather than silently replaced.

**Revision note, proposer pass.** This version also repairs a design defect that made the loop unrunnable as specified: this file and `F9_PREREGISTRATION.md` named two different proposers and neither could execute. The repair is §2.2, **one observation with two renderings**, and it propagates to §2.3 (the outcome space and the yield decision), §3.2 (the RQ-VAE is off the proposal path), §3.4 (the observation card and its equivalence check), §5.2 and §5.3 (the ablation switch is costed rather than left unbuildable, and the trace carries the proposal distribution), §7 (Phase 4, and the gate order), §8 and §9. The generation ledger moves with it and is re-derived in `F9_PREREGISTRATION.md` §8.1. **Falsifier F13 limb (a) and falsifier F14 acquire a derived cost for the first time** (`F9_PREREGISTRATION.md` §8.4), because the instrument the repair installs is the instrument those falsifiers need.

---

## 0. What this is

The paper's argument ends at a limit that scale does not move. Sparsity removes the compute constraint, tower decomposition raises the data ceiling, four-bit serving handles memory, and after all of that the system is still capped by how fast something outside it can tell it that it is wrong. This directory specifies the cheapest experiment that can test that claim and return a decisive negative. **Cheapest, not free:** a negative is an equivalence claim, and equivalence needs seeds. At about **1,540 GPU-hours** (1,536.5 at the planning instantiation of `F9_PREREGISTRATION.md` §8.1: n = 8 at 125M as the powered screen, n = 3 at 350M confirmatory, and proposers frozen at 1B-class) the negative **on the bound** is licensed; at the 72 to 96 GPU-hours the repository's ledger currently budgets, it is not, because at 350M that budget buys **0.24 to 0.31 seeds per arm** across the five arms of `F9_PREREGISTRATION.md` §2, a quarter of one seed, and no test statistic of any kind can be computed from it. **And that total is a band, not a number, until the proposer roster is frozen:** §2.2 puts the proposals on frozen open-weight models, generation scales linearly in their parameter count, and the same design costs 1,376.8 GPU-h at 0.5B-class proposers and 3,773.3 at 8B-class. (The figures 1,683.6 / 1,467.6 / 4,707.2 stood here until `F9_PREREGISTRATION.md` §8.1 withdrew a per-seed corpus multiplier and a duplicated A0 arm from Study 2; they are superseded, not scaled.) **What 1,540 GPU-hours does not buy is the gate contrast.** At n = 8 the tightest declarable equivalence margin is 6.2 accuracy points while superiority needs 7.9, so a true gate effect between the two is INCONCLUSIVE by construction; buying a 3.0-point verdict would cost 1,676 GPU-h in Study 1 alone and it is not bought. Those distinctions are the difference between an experiment and a picture, and they are settled in `F9_PREREGISTRATION.md` rather than left to whoever runs it.

The loop:

> Towers disagree. They act on an environment. The environment settles the disagreement. Trajectories are kept in proportion to how much the ensemble was surprised, and they accumulate rather than replace.

Two environments, chosen because they fail differently:

| | **Substrate A: Pokémon** | **Substrate B: psychohistory** |
|---|---|---|
| Environment | Game Boy emulator (PyBoy) | Real social and economic systems |
| Observation | Rendered frames, RAM state | Reddit / GitHub / Wikipedia / market series |
| Adjudicator | Game mechanics: exact, instant, free | Reality: noisy, delayed, expensive |
| Latency per trajectory | Milliseconds | **112 days of calendar window per adjudication, of which 22 days must accrue after the onset before any verdict exists** (§4.3) |
| Can the model internalise it? | **Yes, eventually.** It is a deterministic program | **No.** This is the whole point |
| Role | **Volume** | **Validity, once, at the end.** Not a loop, not a token source (§4.3) |

---

## 1. The theory, and whose it is

Four separate literatures converge on one conclusion. **None of these results is ours**, and an earlier draft of this document presented the synthesis as an original conjecture, which was wrong. What follows is the corrected attribution.

**1. Debate is a martingale, and informational diversity is not what breaks it.** Under a Dirichlet-Categorical belief model with homogeneous agents and unweighted belief updates, multi-agent debate induces a martingale over agents' belief in the correct answer: expected correctness does not improve over rounds (Choi, Zhu and Li, *Debate or vote*, arXiv:2508.17536, 2025). That same paper extends the martingale **to heterogeneous agents explicitly**, so diversity of information does not by itself break it. The two mechanisms the literature does show breaking it are both protocol-internal, not observational:

- **Confidence weighting.** Under agents that are explicitly *homogeneous* and fully connected, with confidence positively correlated with correctness, the belief process becomes a strict submartingale (Zhu, Zhang, Chi, Stafford, Collier and Vlachos, arXiv:2601.19921, 2026, Theorem 1). No diversity and no external observation are involved.
- **Better initialisation.** Diversity injection in that same paper raises the prior probability of success and its Appendix D states it is "not changing the dynamics of the martingale process".

Empirically, multi-agent debate does not reliably beat self-consistency (Smit, Duckworth, Grinsztajn, Barrett and Pretorius, *Should we be going MAD?*, arXiv:2311.17371, ICML 2024). On the one matched comparison that exists, Choi et al.'s heterogeneous-persona results run a mean **6.19 points in favour of identical agents** on GSM8K, and majority voting beats every heterogeneous-persona debate configuration they report; that comparison is confounded, because the persona single-agent baseline is itself 6.66 points weaker, so it does not establish that homogenisation helps either.

**Correction recorded.** Earlier drafts of this document said the martingale is broken by informational diversity, and that "swapping specialised agents for identical ones costs several points of accuracy". Both are wrong. Neither cited source supports the first, and the only source that runs the second comparison reports the opposite sign. The martingale theorem was also attributed here to the wrong paper: it is Choi et al. arXiv:2508.17536, not arXiv:2601.19921, whose author list contains no Choi.

**Consequence for this spec, corrected.** Result (1) does **not** license "the towers must be informatively different". It says the opposite of a licence: neither identical nor diverse agents improve by talking, absent either a protocol change (confidence weighting) or something outside the conversation that settles it. What the theory supports is the adjudicator, which is what this loop supplies. Tower diversity is now stated as a conjecture of ours (§1.1 item 2, falsifier F13 in `../logos.tex` §15), it runs against the source it was drawn from, and it is **measured before any arm runs** rather than assumed: the S4 proposer-diversity gate in `F9_PREREGISTRATION.md` §4 voids the experiment if mean pairwise JS divergence between the proposers, over the outcome space of §2.3, is below 0.15, and its companion gate S5 voids it if a proposer cannot beat chance on the control condition. **It is also now conditioned on falsifier F14** (`../logos.tex` §3.3 and §15): the reference architecture's towers are divergent branches of one common seed rather than independent models, because Branch-Adapt-Route requires it, and whether a branch preserves the informative difference F13 needs is unsettled. S4 does not discharge F14. See §1.1 item 2.

**2. RLVR sharpens rather than expands.** Probing the reasoning boundary with pass@k at large k, base models catch up with their RL-trained versions across every benchmark and model family tested, and eventually surpass them (Yue et al., NeurIPS 2025, Best Paper Runner-up). RLVR improves sampling efficiency; it does not enlarge the set of solvable problems.

**Consequence:** you cannot get past the wall by running RL harder on a fixed problem set. The problems have to come from somewhere.

**3. Self-training without grounding provably degenerates.** Formalised as a discrete-time dynamical system, recursive self-training has two failure modes: entropy decay, where finite sampling monotonically destroys distributional diversity, and variance amplification, where the absence of persistent grounding produces drift by a random walk. If the fraction of exogenous, externally grounded signal vanishes asymptotically, degeneration follows (H. Zenil, arXiv:2601.05280, 2026; single-author, and earlier drafts of this document wrote "Zenil et al.").

Model collapse (Shumailov et al., *Nature* 631:755–759, 2024) is the empirical face of this. **It is not automatic**, and the first draft of this document overstated it: collapse is established when synthetic data *replaces* real data, and accumulating real and synthetic together avoids it (Gerstgrasser et al., arXiv:2404.01413, 2024).

**Consequence:** the exogenous-signal fraction is the design variable, and the corpus must accumulate, not rotate.

**4. Self-play works when something external checks the answer.** The strongest zero-human-data result trains a model to propose and solve its own tasks, reaching state-of-the-art coding and mathematical reasoning with no external data, using **a code executor** to validate proposed tasks and verify answers (Absolute Zero, arXiv:2505.03335, NeurIPS 2025).

**Consequence:** the executor is not an implementation detail, it is the entire source of correction. And a code executor is a deterministic program, which is why Substrate B exists.

Silver and Sutton ("Welcome to the Era of Experience", DeepMind 2025) frame the destination: experiential data will come to dwarf human data. The four results above say what the limiting resource is on the way there.

### 1.1 What is actually ours

Three things, all Tier C, all in `../logos.tex` §12:

1. **The bound is derived as the residual, and instantiated cheaply.** Not "we named the observation bound": naming it is not ours and the surrounding literature is thick. Genewein et al. (arXiv:2606.12683) enumerate the same friction taxonomy including the data wall and an embodied bottleneck, though they explicitly decline to say which friction binds; Ding and Wang (arXiv:2606.22495) argue environment determinism is a complementary binding axis; Sun et al. (arXiv:2510.14253) show empirically that verification capacity is the bottleneck in agentic self-learning, "if frozen, it induces reward hacking and stalls progress", nine months before `logos.tex` v0.2. What is ours is narrower and checkable: the bound falls out as the **residual** after §§2–11 lift compute, the data ceiling and memory for one specific 5x2.8T architecture, and it is turned into a falsifiable loop that runs on one 24 GB card. Against Genewein's embodied bottleneck we differ in that our channel is not physical manipulation but adjudication of any kind; against Ding and Wang we differ in that determinism is a property of the environment while bandwidth is a property of the coupling. If those distinctions do not survive scrutiny, this item is subsumed and should be withdrawn.
2. **Conjecture, stated against a published result, and now conditioned on falsifier F14: corpus-level difference between towers is a different object from persona-level difference, and it is exploitable.**

   > **The condition, and it is not a caveat.** `../logos.tex` §3.3 makes **lineage sharing** an explicit design parameter and shows this claim is stated about an object the reference architecture cannot build. Branch-Adapt-Route joins separately post-trained experts into one mixture-of-experts, and the Branch-Train-MiX merge averages shared self-attention weights across branches; neither operation means anything across independently initialised models, whose neurons sit in unrelated permutations. So Branch-Adapt-Route requires `λ ≥ 1` (one common seed, divergent continued-pretraining branches) while **F13 states the diversity conjecture at `λ = 0` and explicitly excludes two finetunes of one checkpoint as an instrument**, on the suspicion that a shared checkpoint destroys the treatment. A Branch-Train-MiX branch is longer than a finetune and nothing says it is long enough. **`../logos.tex` §15 mints falsifier F14 for exactly that gap**: whether a common seed with divergent continued pretraining preserves the informative difference F13 needs, tested by whether debate between two continued-pretraining branches of one base checkpoint tracks the martingale measurably more closely than debate between two independently pretrained models of matched size and matched benchmark quality, under an identical protocol. If it does, the architecture cannot have both Branch-Adapt-Route and the diversity conjecture, and this harness is testing its Tier-C claim on an object the reference architecture cannot build. **F14 runs on one consumer accelerator, on the same instrument as limb (a) below, and that instrument is now the F9 proposer inventory of §2.2, so its cost is derived for the first time in `F9_PREREGISTRATION.md` §8.4.**
   >
   > **So this item is now conditional and should be read that way everywhere it appears in this document.** The claim is not "tower diversity raises the loop's yield". It is "tower diversity raises the loop's yield **if** F14 clears, and if it does not, the claim survives only for towers this architecture is not able to build." The S4 proposer-diversity gate in `F9_PREREGISTRATION.md` §4 does **not** discharge F14: S4 measures Jensen-Shannon divergence between the proposers as used, which is a property of the models on the shelf, not of the branch-length question F14 asks.
   >
   > **The same conclusion arrives independently from `PRIOR_ART_v03.md` mechanism 4a**, which finds that **key-value-cache alignment and ensemble decorrelation are the same knob with opposite signs**: an objective that maximises representational agreement so KV projections are interchangeable is directly opposed to the error decorrelation any ensemble gain lives on. Fort et al. (arXiv:1912.02757) is the load-bearing result: "random initializations explore entirely different modes, while functions along an optimization trajectory or sampled from the subspace thereof cluster within a single mode predictions-wise", and "the decorrelation power of random initializations is unmatched by popular subspace sampling methods", and Nam et al. (arXiv:2110.14149) add that "the typical distillation procedure does not effectively transfer such diversity", with the scope limit recorded there that Nam et al. distil an ensemble into one model rather than ensembling students of one teacher, so it supports the concern by mechanism and not directly. That document also says in terms that this particular negative is the weaker of its two, because "ensemble of distilled siblings" has no standard name and a paper could exist under vocabulary the search did not guess, and its §7 lists **thirteen** gaps in its own coverage (six areas not searched at all, seven claims resolved only to a secondary source), of which **non-English literature is named the largest single blind spot**.

   Branch-Adapt-Route produces towers pretrained on disjoint corpora under different objectives with different alignment histories, which a single self-playing model cannot manufacture, and we conjecture that this raises the loop's yield. **The literature says otherwise and we are not going to paraphrase around it.** Choi et al. (arXiv:2508.17536) extend the martingale explicitly to heterogeneous agents, and Zhu et al.'s diversity result moves only the starting distribution. Both evaluate one base model under different prompts, personas or priors, which is the reason we think the extension has not been tested against what we mean; that reason is a conjecture, not an argument from the sources. This is falsifier **F13** in `../logos.tex` §15, it is the least defended claim in the paper, and it is the claim we would most like tested. In this harness it is H3 in `F9_PREREGISTRATION.md`, isolated by the A3-versus-A4 contrast, and that document states in advance that it is the contrast the design is worst powered to detect.

   **Falsifier, and it has two limbs.** (a) Debate between towers with disjoint pretraining corpora tracks the martingale as closely as debate between personas of one model. (b) **Calibrated-confidence weighting alone** lifts ensemble accuracy on the held-out battery with no environment adjudication of any kind, which would locate the gain in the protocol rather than in the observation channel, and would mean the observation bound is not what limits the loop. **Limb (b) is not Zhu et al. Theorem 1, and an earlier revision of this document said it was.** The theorem is stated for agents that are explicitly *homogeneous* and fully connected, and it concerns a submartingale **over debate rounds**. This arm is two aggregation rules over **two heterogeneous frozen models at R = 1**: no debate, no rounds, hence no process for a submartingale to be a property of. And with two proposers "unweighted majority" is not a majority, it is `argmax P_M` (§2.3), so the contrast reduces to "trust the more confident of two models". **Restated honestly, limb (b) is an ensembling comparison**, and that confidence-weighted ensembling beats uniform averaging is standard and carries no information about whether external adjudication supplies novel information. It is an **ensemble-level comparison rather than a pretraining arm**: two aggregation rules over the same two §2.2 proposers, unweighted mean against calibrated-confidence weighting, on the frozen §3.3 battery in the **proposer rendering** of §3.4, with no emulator, no RAM and no adjudicator.

**What K5 is therefore licensed to kill, re-derived.** Not "the submartingale that breaks the debate martingale is protocol-internal", which this arm cannot show, because it instantiates no debate. What it can show is narrower and still worth 36.3 GPU-hours: **that a gain of the size the loop is chasing is available from an aggregation rule alone, at zero adjudication cost, once the calibrator's own exogenous supervision is charged to the same ledger and held identical across arms.** If it is, the loop is buying with an environment what a weighting buys for free, and `../logos.tex` §12 has located its scarce resource in the wrong place. That condition is not decoration: without it the kill condition is the content of a published theorem this programme cites and accepts, and a falsifier whose kill condition is an accepted result cannot return a surprise. **Two options were considered and one is registered as the upgrade path:** adding `R = 3` debate rounds and a homogeneous-agent control would instantiate the theorem properly and is the same instrument limb (a) already uses at 17.4 GPU-h, so it is available; it is **not funded here** and limb (b) is reported as an ensembling result until it is. It is **scored ungated**, on the full battery and never on a disagreement-conditioned subsample (§2.1), and tested by exact McNemar on the discordant pairs. It costs **36.3 GPU-h** at the planning instantiation inside F9's total, re-derived from the withdrawn 12.7 that was priced against 350M stand-ins (`F9_PREREGISTRATION.md` §8.2), it carries its own pre-committed kill condition **K5** (§10 there), it is the cheapest kill shot available against our own thesis, and it runs on the same one consumer card. **Limb (a) is not an arm of F9 and cannot be run with 350M stand-ins, but it does run on the same card, and after the §2.2 repair it runs on the same models.** It needs models whose pretraining corpora, objectives and alignment histories genuinely differ, and that is a property of how a model was trained rather than of the hardware it runs on. Such models already exist: Qwen, Llama, DeepSeek, Mistral and Gemma were pretrained by different organisations on different corpora under different objectives with different alignment histories, which is arguably a **better** instrument than five towers from one lab, since same-lab towers would share data-collection pipelines and filtering decisions and be less independent than they look. So limb (a) runs as several existing open-weight models of **different pretraining lineage** used as the towers, quantized and stepped sequentially on the 24 GB card, with no gradient step anywhere. **Distinct lineage is the treatment variable**: two models from the same lab, or two finetunes of one base checkpoint, do not count as distinct and cannot be used to fill a slot. The honest limitation is that this tests the diversity claim at the level of independently trained open-weight models and not at tower scale inside one architecture, and the ensemble under test is not a Mixture-of-Towers. **Its cost is now derived rather than owed, because §2.2 makes the F9 proposers the same class of object:** `F9_PREREGISTRATION.md` §8.4 prices limb (a) together with F14 at **17.4 GPU-h** at a four-model 7-to-8B-class roster, with the arithmetic shown and the linear scaling in roster size and item count stated. Earlier revisions of this document, of `TIER0_3090_PLAN.md` and of `../logos.tex` §15 all said the cost was not derived; the first two are corrected here and the paper's sentence is now stale (§9). What remains genuinely out of reach on this card is the 5 x 2.8T ensemble itself, which is falsifier **F2** and not F13; the two must not be conflated. **Falsifier F14 runs on this same instrument and is planned as part of the same rung**: the inventory limb (a) needs already contains what F14 needs, since F14 contrasts continued-pretraining branches of one shared base against models of distinct lineage under an identical protocol. It is budgeted as one rung rather than two, and the one thing it depends on that the card cannot supply is the existence of a published continued-pretrain of a base whose original is also on the roster, which is an availability question and not a compute question. One steelman is recorded in advance so a positive is not over-read: Zhu et al. buy calibrated confidence with external supervision (GRPO confidence calibration, LoRA r=64 alpha=32, on a manually curated subset chosen so accuracy sits near 50%), so that route is not free of exogenous signal either, and the exogenous signal has moved into the calibrator rather than left the system. The arm must therefore hold the confidence-calibration supervision identical across arms and report its token and GPU-hour cost as a separate ledger line, exactly as generation compute is reported in `F9_PREREGISTRATION.md` §5.
3. **The admission rule.** If exogenous signal is scarce, keep trajectories in proportion to how much of it they carry.

---

## 2. The loop

**Yield** of a trajectory τ is the surprisal of the observed outcome under the ensemble's own prediction before it acted:

```
yield(τ) = −log P_M(o_observed | context, action)
```

Agreed-and-right scores near zero: self-confirmation, which is the entropy-decay path of result (3). Disagreed-and-adjudicated scores high. **`P_M` is the proposer ensemble's pre-action distribution, not the learner's**, and that reading is fixed in §2.3 because the two documents left it open and it decides which trajectories are admitted.

1. **Propose.** Show an observation to ≥2 proposers independently, in the **proposer rendering** of §2.2. Each returns a distribution over the pre-committed outcome space `O` (§2.3), an action from the enumerated legal set, and free-text prediction and reasoning.
2. **Gate on disagreement.** JS divergence between proposer distributions **over `O`, in bits**, thresholded at `tau_JS`. It is computed over `O` and never over token distributions, because proposers with different tokenizers have no common event space over tokens (§2.2). Below threshold, discard. **The justification is not result (1)**, which says nothing about which samples to keep and, as corrected above, does not say diversity is what improves debate. The gate is a yield-economics rule: an agreed-and-confident trajectory has near-zero surprisal at step 5 and would be admitted at near-zero weight anyway, so gating is the cheap form of yield weighting, applied *before* the environment is paid for. Whether it adds anything over grounding alone is a hypothesis (H3), tested by the A3-versus-A4 contrast, not assumed. `tau_JS` is calibrated, not chosen: it is the value admitting exactly `q = 0.25` of proposals on a 50,000-proposal calibration pool generated before any training arm runs (`F9_PREREGISTRATION.md` §7).
3. **Act** on the environment.
4. **Adjudicate.** The environment returns the outcome.
5. **Score yield.**
6. **Admit** weighted by yield: `w(tau) = clip(yield(tau), 0, 10)`, normalised to mean 1 within each round, and **accumulate** rather than replace (result 3 / Gerstgrasser).
7. **Retrain incrementally, repeat.** Rounds are `R = 1` for the ordering study and `R = 5` for the collapse sub-study (`F9_PREREGISTRATION.md` §7, §8.1).

   **One property of the paper's loop does not hold in this instantiation, and saying so is not optional.** `../logos.tex` §12 step 7 says "disagreement shrinks where the environment has been explored, which pushes generation toward the frontier without being told to". That holds when the proposers are the towers and the towers retrain. **Here the proposers are frozen and take no gradient step ever (§2.2), so their disagreement on a given observation is a constant across rounds**, and nothing pushes generation toward a frontier. What the rounds buy in Study 2 is an accumulating corpus for the learner, which is the collapse question, and not a moving proposal distribution. The self-sharpening half of the paper's loop is **not instantiated by F9** and F9 returns no evidence about it.

Steps 2 and 6 are the anti-collapse mechanism, and they are structural rather than heuristic: the loop cannot train on its own confident agreement.

**Both gates are computable without human labels.** That is what makes the thing runnable.

### 2.1 What the gate does to any statistic computed downstream of it

The gate conditions the retained sample on **predictor disagreement**, and disagreement correlates with item difficulty. Anything computed on gated output is therefore a statistic on a difficulty-biased subsample, biased in a direction that is not known in advance and not estimable from the subsample itself.

**Consequence, and it is a hard one:** the harness cannot score a skill falsifier on gated output. Brier scores, skill scores and hold rates against persistence, climatology, a market or a superforecaster panel are **population** statistics defined over a full, pre-registered question set. `RUN_AND_CHECK.md:50` and `:56` lock m = 50 questions and delta = 0.05 for exactly such a comparison; `:57` scores a hold rate against a naive base rate over a pre-registered announcement set; `:59` scores a fraction of windows classified imitative on a named series. Feeding any of those a disagreement-conditioned subsample does not make the test harder or easier, it makes it uninterpretable.

**Therefore an ungated scoring arm is mandatory** wherever the harness produces a number that will be compared against an external baseline: run the entire pre-registered question set through the towers with the gate **off**, score that, and use the gate only for corpus admission. The two uses of the loop are separate: gate for what you train on, do not gate for what you report. Arm A4 (`F9_PREREGISTRATION.md` §2, ungated grounded) already exists for this reason and is the arm any external-baseline comparison must be run in.

### 2.2 The proposers, and why one observation needs two renderings

**The defect this section replaces, stated before the repair.** Two binding documents named two different proposers and **neither works as written**. §7 Phase 4 of this file said "at least two distinct open models standing in for towers". `F9_PREREGISTRATION.md` §8.1 said "two 350M-class stand-in towers", and derived the whole 137.9 GPU-hour generation ledger at 350M throughput.

- **Distinct open models cannot read the observation as §5.3 renders it.** An observation is a span of RQ-VAE codes, `<boi> <v_412> <v_87> ... <eoi>`. Those identifiers mean something only inside the vocabulary and embedding table they were trained into. No off-the-shelf model shares that vocabulary, that hidden size, or that embedding, so no off-the-shelf model can parse them.
- **350M stand-ins have to be trained first and nothing pays for it.** Worse, two models trained the same way on the same data are exactly the homogeneous case that §1 result (1) and finding C-02 say yields a martingale, so those GPU-hours would have bought proposers guaranteed not to disagree informatively.

`LADDER_ARCHITECTURE.md` §10 records the same conflict as unresolved and declines to assume either reading. This section resolves it, and the resolution is not a compromise between the two: it is that the observation needs **two renderings** and the spec conflated them into one.

| | **proposer path** | **learner path** |
|---|---|---|
| consumer | two or more **frozen** open-weight models of **distinct pretraining lineage** | the 125M or 350M model under training |
| rendering | the **observation card** of §3.4: structured text, or the raw frame for a vision-language proposer | RQ-VAE codes, §3.2 |
| when | once per proposal, at generation time | every training step |
| gradient | none, anywhere, ever | the entire experiment |
| cost | inference only (`F9_PREREGISTRATION.md` §8.1 step 2) | training (§8.1 there) |

The two renderings must be **semantically equivalent** and they are different artifacts, produced by different code from the same emulator state. **For Substrate A a vision-language proposer can read the frame directly, so the RQ-VAE is not on the proposal path at all.** Its job is compressing observations into the *learner's* token stream, which is a separate concern with its own gate (Phase 1, §7). Equivalence is checked rather than asserted, and §3.4 says how.

**What this fixes at once, and it is more than the defect.** Proposers become frozen and cheap per unit. The circularity of training stand-ins in order to test whether training works disappears. And the proposers become genuinely distinct-lineage models, which is exactly the instrument falsifier **F13 limb (a)** requires (`../logos.tex` §15) and exactly what F14 contrasts against. The same inventory serves F9 and both of those falsifiers, so **their cost is derived for the first time** in `F9_PREREGISTRATION.md` §8.4 rather than left owed in three documents at once.

**The proposal, exactly.** Every proposer returns three things, and only the first is read by any statistic:

1. **`p_outcome`, a categorical distribution over the pre-committed outcome space `O`** (§2.3), obtained by constrained decoding over **single-token symbol labels** and renormalised over the label set. Never by parsing free text.

   **The symbols are not the human-readable names, and this is a correction [FROZEN].** An earlier revision specified "constrained decoding over single-token category labels" against the label set `{no effect, not very, neutral, super}`, which is not computable: two of those four are multi-token in every standard byte-pair encoding, and the label-to-token map is per-model. Under a first-token-only read in a byte-BPE where `"no"` is a token and `"not"` decomposes as `"no" + "t"`, *no effect* and *not very* collapse to the same first token, so that proposer's effective event space on the effectiveness axis has three cells while its partner's has four and the JS divergence is computed over a space one of the two cannot express. Under multi-token sequence scoring instead, the two-word labels carry an extra token's log-probability penalty of per-tokenizer magnitude, tilting toward the one-word categories before any knowledge is measured.

   **The fix.** Each axis is read from a **symbol** (`A`/`B`/`C`/`D` for effectiveness, `1`..`5` for the damage quintile, `Y`/`N` for faint), with the human-readable gloss carried in the observation card so the model knows what each symbol means. `proposers/roster.yaml` carries a **build-time assertion**, checked in `parity_check.py`, that every symbol is exactly one token and that the symbol set is prefix-free in **every** roster tokenizer. A roster member that fails the assertion cannot fill a slot. Without it, `../logos.tex` §12's claim that `O` restores a shared event space across models with different tokenizers is unverified rather than true.
2. **an action**, drawn from the enumerated legal action set printed on the card. Anything outside that set is a malformed proposal: discarded, counted, and reported per proposer as a ledger line, because a proposer with a high malformation rate is a proposer whose disagreement is a parsing artifact.
3. **free-text prediction and reasoning**, the `predict` field, which enters the trace (§5.3) as a per-proposer record and enters no statistic.

**Who writes the trace's top-level `action` and `thought`, and this was unspecified [FROZEN here].** §5.2 puts the training loss on `thought` and `action`, so between them they are the only loss-bearing spans the loop authors, and until this revision no document said which process produced either. With two or more proposers disagreeing there is no selection rule to infer, and the previous §5.3 exemplar filled `thought` with a proposition **neither proposer produced**, which is to say with an unspecified oracle that had already seen the adjudication. That is the corpus-invalidating defect and it is closed here.

- **Action selection.** The executed action is chosen by a **seeded uniform draw over the proposers whose proposal is well formed**, using a per-item RNG stream derived from `(episode, step, run_seed)`. The drawn index and the stream seed are written into the trace as `selected_proposer` and `selection_seed`, so the choice is reproducible and auditable. A uniform draw is chosen over a fixed index because a fixed index would make one roster member the sole author of every executed action and would confound roster choice with the endpoint, and over `argmax P_M` because `P_M` is a distribution over outcomes and does not name an action.
- **`thought` is not authored.** It is a **verbatim copy of the selected proposer's `predict` field**, and `schema/validate.py` asserts `thought in {proposals[i].predict}` and `thought == proposals[selected_proposer].predict`. Nothing else may write it.
- **Nothing may be authored after `result`.** `schema/validate.py` rejects any trace carrying a loss-bearing span authored after the adjudication other than the mandatory `outcome` span of §5.2, and rejects any `thought` or `predict` containing a token not present before the environment was stepped. Without that assertion the loop trains on hindsight and reports it as grounding.

**Consequence, stated rather than hidden.** `thought` is now proposer text, and proposer text is the reasoning the learner is asked to internalise. If the selected proposer's reasoning is wrong, the learner is trained on wrong reasoning with a correct adjudicated `outcome` after it. That is the intended contrast and it is what the disagreement gate exists to select for; it is not a defect. What *was* a defect was an oracle writing the right answer into the span before the environment was consulted.

**Everything statistical is computed on `p_outcome` and nothing is computed on token distributions.** That is forced rather than chosen: two models with different tokenizers share no event space over tokens, so a Jensen-Shannon divergence between their next-token distributions is undefined, and the old spec's `js_divergence` field was undefined the moment the proposers stopped being two copies of one architecture. Over `O` it is defined. The disagreement gate `tau_JS` (§2 step 2), the S4 proposer-diversity gate, the yield of §2 step 5, and the confidence weighting of F13 limb (b) are then four functionals of **one** object, which is what makes them mutually calibratable.

**What the proposers may not be.** Two models from one lab, two sizes of one family, or two finetunes of one base checkpoint do not count as distinct lineage and may not fill a slot (`../logos.tex` §15, F13 limb (a)). Personas or system prompts over one model are the F13 **control** condition, not a proposer pair.

**Two honest limits.** First, the proposers are not towers, and a 1B-class open model standing in for a 2.8T tower is a stand-in whichever way it was obtained; §8 keeps that risk row and it is not discharged here. Second, the roster is not frozen in this document. Which open models are used sets the generation cost outright (`F9_PREREGISTRATION.md` §8.1), so the F9 total is a **band until the roster is frozen**, and saying otherwise would be inventing a number.

### 2.3 The outcome space `O`, and whose ensemble the yield is scored under

**The decision, because the documents did not make it.** Yield is defined as the surprisal of the observed outcome "under the ensemble's own prediction before it acted". Under the two-path split of §2.2 that is ambiguous between the proposers and the learner, and it changes which trajectories are admitted. **Frozen: `P_M` is the proposer ensemble's pre-action distribution, computed from the frozen open models' own `p_outcome` at proposal time.** Three reasons, in the order that decides it:

1. **The paper says so.** `../logos.tex` §12 defines yield as the surprisal under the prediction of the thing that acted, and the thing that acts in this loop is the proposer ensemble. The learner never acts; it reads traces afterwards.
2. **It keeps the corpus shared across seeds.** `F9_PREREGISTRATION.md` §8.1 generates one corpus per arm and shares it across the 8 seeds, so that the seeds estimate training-seed variance with data held fixed. A learner-side yield would make admission depend on the seed and the arm, forcing a separate corpus per seed. At the §8.1 planning instantiation that alone is `python3: 8*112.5 = 900.3` GPU-h for Study 1 generation against 112.5, a **787.7 GPU-h** difference bought for nothing.
3. **The learner reading is circular at round 1**, when the learner has seen no trajectories at all, so its surprisal is a statement about its text pretraining and not about the observation.

**Consequence, carried through.** `tau_JS`, S4 and the yield are all computed over the same distribution, so the gate threshold is calibrated on exactly the object the admission weight is computed from. Nothing downstream may quietly substitute the learner's likelihood for `P_M`, and `bootstrap/yield_score.py` never loads a training checkpoint.

**`O` for Substrate A [frozen here, and it restricts the loop].** `O_A` is the triple

> (effectiveness bucket ∈ {no effect, not very, neutral, super}) × (damage bucket ∈ 5 quintiles of the defender's max HP) × (faint ∈ {yes, no}), so **|O_A| = 40**. Read from the symbols of §2.2 item 1: effectiveness `A`/`B`/`C`/`D`, damage `1`..`5`, faint `Y`/`N`.

**`super` conflates 2x and 4x, and the conflation is deliberate [FROZEN].** Generation-I type effectiveness has five multipliers, 0x, 0.5x (and 0.25x against two resisting types), 1x, 2x and 4x, and `O_A` has four effectiveness cells. A dual-type defender resisting or weak on both halves lands outside the four names: Water against Onix, which is Rock and Ground, is **4x**, not 2x, and the flagship example in §5.3 asserted 2x until this revision. **We keep four cells and record the cost rather than adding a fifth**, for one reason that is not aesthetic: `|O_A| = 40` is frozen, the yield floor `ln(40/1e-3) = 10.597` nats is derived from it, `tau_JS` is calibrated over it, and every JS and yield figure in this document is computed on the 40-cell factorised joint. A fifth effectiveness cell makes `|O_A| = 50` and invalidates all of them for a resolution the primary endpoint does not read: the behavioural probe scores whether the model **chooses** the super-effective move out of four offered, not whether it predicts 2x against 4x. **The cost is real and is stated:** the loop cannot distinguish a 2x matchup from a 4x one, so no claim may be made about learned multiplier magnitude, only about learned effectiveness ordering. `configs/outcome_space.yaml` carries the mapping `{0x -> no effect, 0.25x and 0.5x -> not very, 1x -> neutral, 2x and 4x -> super}` explicitly, so the conflation is in the sealed artifact rather than in a reader's head.

Each proposer supplies the three marginals by three constrained single-token reads and `p_outcome` is their product, which is an independence assumption stated here and not hidden: JS, yield and the confidence weighting are all computed on that factorised joint. **The Substrate-A loop therefore proposes on battle steps only.** Menu and overworld frames still enter the frame dump and the RQ-VAE training set, but they carry no pre-committed outcome space and no proposal is taken on them. The cost of that restriction is real and is stated in §8: the loop learns battle semantics, which is what the held-out vocabulary of §3.3 and the primary endpoint measure, and it learns nothing about navigation.

**`O` for Substrate B.** The pre-registered label set already in the §5.3 payload: (endogenous, exogenous) × (`fires_vs_shuffle` true, false), so **|O_B| = 4**.

**The mixture and the floor.** `P_M` is the unweighted mean of the proposers' `p_outcome`, which is the same aggregation rule A1 and A2 use to manufacture their pseudo-outcomes, floored at `P = (1 − eps) P_ens + eps/|O|` with `eps = 1e-3`. The floor bounds the surprisal:

```
python3: import math; math.log(40/1e-3)   = 10.597 nats   # Substrate A, |O| = 40
         math.log(4/1e-3)                 =  8.294 nats   # Substrate B, |O| = 4
```

so the `clip(yield, 0, 10)` of step 6 almost never binds, which is what a clip put there to stop unbounded weights should do. Yield is in **nats** (natural log, matching the paper's equation); JS divergence is in **bits**. Both units are stated because S4's threshold of 0.15 is an absolute number and a base change would silently move it.

**One thing this pins down that was loose before.** A1 and A2 take "the outcome is the ensemble's own majority prediction". Over free text that was not well defined. Over `O` it is: the argmax of `P_M`.

---

## 3. Substrate A: Pokémon

Fully observable, exact ground truth in RAM, adjudication in milliseconds, and the semantics under test are printed on screen, so observation fidelity is checkable pixel by pixel.

### 3.1 Harnesses

Two exist, both built on PyBoy. Use both, for different jobs.

**PufferLib Pokémon Red** (`PufferAI/pokegym`, `drubinstein/pokemonred_puffer`, from `PWhiddy/PokemonRedExperiments`, MIT; cite J. Suarez, arXiv:2406.12905, single-author). Gymnasium over PyBoy with heavy performance work: several thousand steps/sec headless at aggressive frameskip. Full RAM instrumentation (party, HP, badges, map ID, coordinates), savestates via `save_state()`/`load_state()`. **Role: trajectory generation, curriculum, ground truth.**

**VideoGameBench** (Zhang, Griffiths, Narasimhan, Press, Princeton; arXiv:2505.18134, MIT). `main.py --game pokemon_red --model gpt-4o`. Game Boy logic in `src/emulators/gba/`, base interface in `src/emulators/interface_base.py`, ReAct agent in `src/llm/vgagent.py`, LiteLLM routing. **Lite mode pauses the emulator during inference**, which decouples model latency from the game clock and is essential for a slow local model. **Raw-frames-only ruleset**, no RAM overlays. **Role: headline agent eval, reported in the same terms as frontier VLMs.** It is a hard benchmark; frontier models score very low under the strict ruleset.

Also useful: `NousResearch/pokemon-agent` (headless PyBoy, JSONL event logging, RAM walkability maps, A*, frames from `screen.ndarray` with no display server); `drubinstein/pokerl` docs on reading RAM via the PRET symbol table (`wPartyMon1HP` at `0xD16C`, `wPartyMon1Type1` at `0xD170`); RAM map at `datacrystal.tcrf.net`.

**Do not confuse this with the PokéAgent Challenge** (Karten et al., arXiv:2603.15563, NeurIPS 2025: Showdown battling with 20M+ trajectories, plus Emerald speedrunning, 100+ teams). That is not Red/Blue frame logging. Citation only.

### 3.2 The observation tokenizer

Game Boy is 160×144, 20×18 tiles of 8×8, four shades. An unusually easy tokenizer target, which is why the vision side is tractable at this budget.

**This tokenizer is on the learner path only (§2.2).** No proposer ever sees a code. The RQ-VAE exists to compress observations into the learner's token stream, and its Phase-1 gate is a reconstruction gate on that compression. Nothing in the proposal loop, the disagreement gate, the yield, S4 or F13 limb (b) depends on it, which is why the run order in `TIER0_3090_PLAN.md` can put those ahead of Phase 1 and could not before.

Base: `lucidrains/vector-quantize-pytorch` `ResidualVQ` (MIT): shared codebooks, stochastic code sampling (Lee et al. 2022), EMA, `kmeans_init=True`, quantizer dropout, dead-code handling. `LFQ` (MAGVIT-v2, Yu et al. ICLR 2024) and `FSQ` are alternatives.

| Knob | Start at | Why |
|---|---|---|
| Input | 4-colour → single luminance channel | Makes the encoder's job trivial |
| Downsampling | factor 16 (four stride-2 blocks): 160×144 → **10×9 = 90 positions** | Lands in the 64–128 target |
| Residual levels | **3** (TIGER uses 3–4) | Coarse to fine |
| Codebook | 1,024–2,048 per level; grow only on failure | Frame diversity is tiny |
| Update | EMA + dead-code reinit | More stable than gradient updates for VQ |
| Losses | L1/L2 + commitment + **edge-weighted** + **region weighting on the HP-bar and text-box rectangles** | Fixed pixel rectangles; the semantically critical areas |

**RESOLVED HERE, no longer deferred to Phase 1: collapse per position.** Earlier drafts left "tokens per frame = positions × levels versus one composite token per position" open and called it a Phase-1 question. It is not a Phase-1 question, because it sets sequence length, and sequence length sets the trajectory share the training matching protocol is built on. The decision:

> **90 positions per frame, 3 residual levels, one LM position per spatial position.** Tokens per frame = **90**, not 270. A Substrate-A trace carries two frames (observation and result), so **180 loss-masked observation tokens per trace**.

**Why collapse is free here.** The loss is masked on observation codes (§5.2): the model reads observations and never generates them. A composite per-position token therefore never appears as a prediction target, so it needs no factorised softmax, only an input embedding. That embedding is the sum of the 3 residual-level codebook vectors after projection, which is the MAGVIT-v2 token-factorisation pattern §5.1 already names. All 3 levels still reach the model, so reconstruction fidelity is untouched; only the sequence cost changes.

**The arithmetic that decides it.** Take a trace's loss-bearing spans (proposals, thought, action, and the mandatory `outcome` span of §5.2) at roughly 130 tokens, and let `P` be observation tokens per frame:

| | Flatten (90 x 3 = 270/frame) | **Collapse (90/frame)** |
|---|---|---|
| Masked tokens per trace | 540 | **180** |
| Trace length | ~670 | **~310** |
| Loss-bearing share of a trace | 19% | **42%** |
| Traces per 2048-token packed sequence | 3 | **6** |
| Observation share of the training stream at trajectory share phi = 0.25 | 20.2% | **14.5%** |
| Loss-bearing trajectory share of the training stream | 4.9% | **10.5%** |

Collapse doubles the differentiating signal per training token at fixed phi, and lands the observation stream under the 15 to 30% cap of §5.4 instead of at its ceiling. Since the arms already differ over only a quarter of their tokens (`F9_PREREGISTRATION.md` §5 dilution note), halving that again for nothing is not affordable.

**Cost of the decision, disclosed, and now paid rather than deferred.** The §5.2 ablation switch (unmask the observation loss) is **not available** under collapse without adding a factorised head of 3 sub-softmaxes over 1,024 codes each. An earlier revision registered that switch and budgeted nothing for it, which made it unbuildable as budgeted. It is now **costed** as contingent rung **A6** (`F9_PREREGISTRATION.md` §8.3), not withdrawn, because the head is small and the arithmetic says so:

```
python3: head params = 3 levels * 768 d_model * 1024 codes            = 2,359,296
         extra FLOP/token, averaged over the stream
           = 3 (fwd+bwd) * 2 * 2359296 * 0.145 (observation share)    = 2.053e6
         baseline 125M training FLOP/token = 2.29866e13 / 2.90e4      = 7.926e8
         overhead = 2.053e6 / 7.926e8                                 = 0.259%
         one A6 run = 9.579 * 1.00259 = 9.604 GPU-h ; n = 8           = 76.8 GPU-h
```

So the head costs a quarter of a percent of a run and the ablation costs the eight runs it needs. It stays **exploratory under `F9_PREREGISTRATION.md` §4.1 and outside the core total**, and it is triggered only as a contingent rung. The flattened 270-codes-per-frame alternative remains available and remains a **different sequence-length regime rather than a clean ablation**, so it is the fallback and not the plan. Codebook size is quoted at 1,024 per level; if Phase 1 grows the codebook the head grows linearly with it and the 0.259% moves proportionally.

**What Phase 1 still decides.** Phase 1 remains a *reconstruction* gate on the RQ-VAE (HP bar, text legibility, sprite identity, codebook utilisation), and it no longer decides sequence length. If the gate fails, more levels and bigger codebooks cost nothing in sequence length, which is precisely why collapse was chosen; **less downsampling is the one repair that does**, since factor 8 gives 20x18 = 360 positions per frame, pushes the observation stream to about 21% of tokens, and must be re-costed against the cap before it is adopted.

**THE GATE.** Before any LM training, on held-out frames: **HP-bar within 1px · menu and dialog text legible (OCR or human panel) · sprite identity correct · codebook utilisation >95%.** On failure: more levels, bigger codebook, less downsampling, or restrict to battle screens. **Do not proceed past a failed gate.** The held-out vocabulary is grounded through on-screen battle text, so a tokenizer that blurs it destroys the experiment without saying so.

### 3.3 The held-out vocabulary

How Substrate A shows that grounding happened rather than text co-occurrence.

Scrub a term set from the **entire** text stream (essays, tool results, analyses) so meaning can only come from grounded trajectories. The scrub applies to the text corpus, **not** to the trajectory traces: held-out terms appear inside traces as action identifiers and inside `thought` spans, and whether their semantics can be installed that way, with an adjudicated outcome attached, is the entire experiment. An ungrounded arm asserting "water_gun was super effective" from its own majority vote is the contrast, not a leak.

**Corrected table [FROZEN in `F9_PREREGISTRATION.md` §3.1].** The table earlier drafts of this document carried was degenerate and could not measure its own endpoint: its control moves were `tackle` and `scratch`, both Normal-type, and Generation-I Normal-type moves have **no** super-effective matchup at all (1x against everything except 0.5x versus Rock and 0x versus Ghost), while the only Fire move, `ember`, sat on the held-out side. The control condition of the behavioural probe therefore had no super-effective item to register.

| Class | HELD OUT (scrubbed from the entire text stream) | CONTROL (kept in text) |
|---|---|---|
| Types | `water`, `rock`, `grass`, `electric`, `ground` | `fire`, `normal`, **`bug`**, **`ice`** |
| Moves | `water_gun`, `thunder_shock`, `vine_whip`, **`flamethrower`** | **`ember`**, `tackle`, `scratch` |
| Phrases | `super effective`, `not very effective` | held out in **both** conditions, so the verbal-readout channel stays matched |

Generation-I Fire is 2x against Bug, Grass and Ice. Grass is held out, Bug and Ice are kept, `ember` is kept, so `ember` against a Bug-type or Ice-type defender is a **valid text-supported super-effective control item**, which the old table had none of. `flamethrower` replaces `ember` on the held-out side so a Fire held-out item still exists.

**The control set is not optional.** It is what makes a null result interpretable.

RAM-derived type/move/HP state labels **probe targets only**, never model input in the held-out condition.

#### The leak filter: exact tokenized set membership. Regex and substring matching are banned.

Earlier drafts specified the filter as "regex **and** tokenizer-level". Both halves of that are withdrawn. A hand-rolled regex is not an acceptable detector here, and **substring containment is worse than useless**: it silently scrubs the control set, which is the one thing that makes a null interpretable, and it does so without erroring. Concretely, `term in text` on this vocabulary removes `ember` from `remember`, `September` and `member`; `ice` from `police`, `service`, `practice` and `nice`; `bug` from `debug`; `normal` from `abnormal`; and on the held-out side it removes `rock` from `rocket`, `ground` from `background` and `underground`, `grass` from `grasshopper`, `water` from `watermark`. Word-boundary regex repairs some of that and still fails on the identifier forms (`water_gun`), on hyphenation, and on Unicode normalisation, and it fails quietly.

The filter, exactly:

1. **Normalise.** NFKC, then casefold. No stemming, no lemmatisation, no fuzzy matching, no edit distance. Every accepted surface form is enumerated, never derived by a rule.
2. **Tokenize to word unigrams.** Split on Unicode word boundaries (UAX #29). Additionally split identifier tokens on `_` and `-`, keeping **both** the split sequence and the joined form as separate candidate members, so `water_gun` is caught as the bigram `("water","gun")` and as the unigram `("water_gun",)`.
3. **Build the banned set** from `configs/heldout_vocab.yaml` as a set of **tuples**: unigrams `("water",)`, `("rock",)`, `("grass",)`, `("electric",)`, `("ground",)`, `("flamethrower",)`; bigrams `("water","gun")`, `("thunder","shock")`, `("vine","whip")`, `("super","effective")`; the trigram `("not","very","effective")`. `n` runs from 1 to the longest held-out phrase, currently 3. Inflections and plurals that must also be banned (`rocks`, `grasses`, `grounded`, and so on) are enumerated as additional explicit members in the same file.
4. **Scan by set membership.** Slide an n-gram window over the unigram sequence for each `n` present in the banned set and test tuple membership in a hash set. This is O(tokens x n_max), it never inspects the inside of a word, and it cannot produce the false positives above.
5. **Scan three surfaces, not one.** (a) The raw text corpus. (b) The detokenized output of the trained subword tokenizer, so a leak cannot survive a subword split. (c) The **mined vocabulary itself**: every text-vocabulary entry is normalised and word-split by the same rule, and any entry whose split contains a banned unigram is dropped from the vocabulary before training. Surface (c) is what catches a merged subword such as `watergun`, which surfaces (a) and (b) would both pass.
6. **Fail closed.** If the tokenizer or `heldout_vocab.yaml` cannot load, the filter **refuses the run**. It never falls back to a weaker matcher. A non-zero leak count voids the run (`F9_PREREGISTRATION.md` §9.3c).
7. **Check the inverse property on the control set.** A control term that never appears is not a control. Assert a minimum occurrence count per control term in the final text stream (>= 1,000), and record both the leak count and the control counts in the seal.

**Probes.** *Interpretability (secondary S1):* nearest observation-code embeddings to each held-out word embedding by cosine; success means held-out type and move embeddings sit nearest the codes of frames where those types and moves appear (mirrors TIGER, arXiv:2305.05065, where RQ-VAE codes captured category structure). Note the resolution ceiling: about 11 held-out terms, which is why this is secondary. *Behavioural (primary):* does the model choose super-effective moves in held-out matchups above chance, versus the text-supported controls? Operationalised as `g = p_heldout - p_control` over a 10,000-item battery per condition, constructed so that exactly one of four offered moves is super-effective and chance is exactly 0.25 in both conditions (`F9_PREREGISTRATION.md` §3).

### 3.4 The proposer rendering: the observation card, and how equivalence to the code rendering is checked

The proposer path of §2.2 needs a rendering an off-the-shelf model can read. There are two, and **a run declares which it uses at run level, not per proposer. Mixed pairs are forbidden [FROZEN, corrected].** An earlier revision made the rendering a per-proposer declaration, which permits an R-text proposer and an R-frame proposer in the same pair, and the two are not in information parity: all four checks below are defined over the card's field list and **none is defined for R-frame**, which is by construction a superset. The Gen-I HP bar is 6 tiles, 48 pixels, quantising HP into about 49 distinguishable states, `log2(49) = 5.61` bits, against the card's bucket at `log2(5) = 2.32` bits, so an R-frame proposer receives about **3.3 bits more per HP field** and about 6.6 bits more per observation, on precisely the variable `O_A` quantises. Worse, check 3 *drops* card fields the learner's codes cannot carry, and dropping a field from the card does nothing to R-frame: if `status condition` is dropped, the R-text proposer cannot see the defender is asleep and the R-frame proposer can, `JS(P1,P2)` on sleeping-defender items is inflated by a pure rendering artifact, `tau_JS`'s calibration pool is enriched with rendering-asymmetry disagreement, S4 passes for the wrong reason, and `P_M` becomes the unweighted mean of a blind and a sighted predictor.

**If R-frame is used at all**, the frame served to the proposer must be **masked or quantised down to the certified field set at the certified resolution** before it reaches the model, the HP bar included, with a byte-level assertion in `parity_check.py` that the served image is a deterministic function of the same field tuple the card is built from. S4 is then re-run within the declared rendering rather than across renderings. The two R-frame proposers' differing effective resolutions and image-token budgets (§3.4 below) remain a ledger issue and are now also an information issue, and the assertion is what closes it.

**R-text, the observation card.** A structured text block emitted by `bootstrap/render_observation.py` from the **same (frame, RAM-state) tuple Phase 0 dumps**, deterministically, with no model in the loop. Contents, and the list is the whole list:

- **Party slot under control:** species, level, current HP as a bucket of max HP, status condition, and the four moves with remaining PP.
- **Opposing slot:** species, level, HP as a bucket, status condition.
- **Screen state:** which screen is displayed (battle main, move select, bag, party) and the verbatim contents of the text box, transcribed from the tile map.
- **The legal action set,** enumerated, exactly as offered on screen, with the identifiers the trace uses (`select_move water_gun`, and so on).
- **The outcome category labels of §2.3,** so the constrained reads have somewhere to land.

**What the card must not contain, and this is the load-bearing half.** No type chart. No effectiveness verdict. No damage calculation. No RAM quantity that the screen does not display: enemy HP is a bucket because the screen shows a bar, not an integer. The card describes state and never adjudication, because a card that adjudicates makes the proposal trivial and the yield identically zero.

**R-frame.** For a vision-language proposer, the raw 160×144 frame at native resolution, nearest-neighbour upscaled to the model's expected input, plus the legal action set and the category labels as text. VideoGameBench's raw-frames-only ruleset (§3.1) is the existing plumbing for this path and its lite mode pauses the emulator during inference, which matters for a slow local model. Image-token counts are model-specific and are a per-roster quantity, so a run using R-frame recomputes its generation ledger with its own prefill length rather than inheriting the card's.

**Equivalence to the code rendering is checked in both directions, and the check is a gate.** The property that matters is **information parity**: the proposer must see what the learner will see, no more and no less. More, and the gate and the yield are computed over a richer observation than the learner ever gets, which biases every admitted trajectory in a direction the learner cannot exploit. Less, and the proposals are about a different problem.

1. **Field-list diff, exact.** The card's field list is diffed against the field list the Phase-1 reconstruction gate certifies (HP bar within 1px, menu and dialog text legible, sprite identity correct). Any card field not on that list is a field the learner's codes are not certified to carry, and any certified field missing from the card is a field the proposer is blind to. Both are build failures, not warnings.
2. **Dual independent human-or-OCR audit** on a frozen sample of **1,000 held-out frames**, drawn **separately from the Phase-1 selection sample** rather than reusing it. Pass condition, corrected: an earlier revision demanded **100% on the four Phase-1 gate fields and at least 99% overall**, which is unattainable and insufficient at the same time. At a realistic human or OCR keying error rate of 0.5 percent, `P(a clean 1,000-frame audit) = 0.995^1000 = 0.0067`: the gate fails 99.3 percent of the time for reasons that have nothing to do with the card, which in practice means it gets rubber-stamped. And a clean audit bounds the true card-error rate at 0.3 percent by the rule of three, not at zero, so it misses a 0.2-percent-prevalence class 13.5 percent of the time. **Frozen pass condition:** two independent auditors score the same sample, disagreements are adjudicated by a third, and the gate passes when the **upper 95 percent binomial bound** on the card-error rate is below **0.5 percent** on the four Phase-1 gate fields and below **2 percent** overall. The realised counts and bounds go in the seal either way.
3. **Code-side recoverability probe.** For each card field, fit a linear probe from the 90 collapsed codes of the same frame to that field. **The representation, the validation scheme and the floor are named here, because an earlier revision named none of them and the natural instantiation is vacuous:** under a one-hot reading the input is `90 x 1,024 = 92,160` dimensions against about 1,000 frames, and by Cover's theorem any labelling of 1,000 points in general position in 92,160 dimensions is linearly separable, so every field passes, no field is ever dropped, and the "no more than the learner sees" half of parity is never enforced. **Frozen:** the probe input is the **sum of the 3 residual-level codebook vectors per position, mean-pooled over the 90 positions**, which is the same representation §5.1 gives the model, at 256 or 512 dimensions and in any case **below `n`**; scoring is **frozen 5-fold cross-validation over frames**, never in-sample; and the floor is the **95th percentile of a label-permutation null** computed on the same folds, fixed before the real labels are read. A field below the floor is **dropped from the card**, because the proposer must not condition on what the learner cannot see. The probes are linear over cached codes and add under 0.1 GPU-h, absorbed in the RQ-VAE line of `F9_PREREGISTRATION.md` §8.1.
4. **Anteriority assertion [NEW]. No card field may be a function of post-action state.** This is the check §3.4 was missing and the reason it was missing is that the ban was written as prose: "no effectiveness verdict" is stated at the top of this subsection and **no gate anywhere tested it**. A card whose text-box field reads `IT'S SUPER EFFECTIVE!` passes checks 1, 2 and 3 unchanged, because the field is on the certified list, it faithfully transcribes what the frame shows, and Phase 1 certifies text legibility. Check 2 cannot save it: at a 0.2 percent prevalence a 1,000-frame audit sees none of the class 13.5 percent of the time, and when it does see one it scores it **correct**. **Frozen:** `render_observation.py` takes as input only the **pre-action** `(frame, RAM)` tuple, with the emulator state hash recorded alongside the card; `parity_check.py` reloads that state, regenerates the card before any action is applied, and asserts the two are **byte-identical**. In addition a **hard filter** rejects, at generation time and not at audit time, any frame whose text-box field carries game-message content rather than the FIGHT/PKMN/ITEM/RUN decision menu, and any frame whose legal action set is empty. Gen-I Red clears the bottom box to that menu on a decision frame, so a strict decision-frame sampler probably never carries the previous turn's verdict, but that is a property of a sampler and the spec previously asserted it instead of implementing it. Both halves are computable in Phase 0.

Checks 1, 2 and 4 need **Phase 0 only**. Check 3 needs Phase 1, so it runs when the RQ-VAE gate passes, and a card field it drops is a card change that re-runs checks 2 and 4 on the same sample. Nothing here is a GPU cost of any size; the human audit is not GPU work and is not priced in GPU-hours.

**What equivalence does not mean.** It does not mean the two renderings carry the same number of tokens, the same ordering, or the same surface form; they cannot. It means they support the same field set at the same resolution. Any stronger claim would need a shared model to measure it, and there is not one.

---

## 4. Substrate B: psychohistory

Substrate A shows the mechanism works. Substrate B asks whether it survives when the adjudicator is reality.

**The observation operators exist in this repository. The observation data does not, and the coupling to the companion paper is far narrower than earlier drafts of this document claimed.** `../validation/` has harvest scripts for Reddit (WSB, AskEconomics, location subs), GitHub, and Wikipedia; pre-registered falsifiers with frozen thresholds; blind Louvain community detection; semantic critical-slowing-down detectors; and an EnKF forward engine.

**What the harness supplies, and what it does not.** Earlier drafts said "what it lacks is a trajectory generator, and the companion paper's four blocked falsifiers are blocked on exactly that". That is false, and it is false in the direction that flatters this document. The repository's own feasibility ledger (`RUN_AND_CHECK.md`) says:

| Falsifier | Real blocker | Does this harness supply it? |
|---|---|---|
| A-iv smooth-regime skill | **Not blocked.** DONE-PILOT, RUNNABLE-NOW, 45 scored steps, an honest negative against persistence | n/a, it has already run |
| A-v fixed-point reliability | A **lodged question set** with outcomes (m = 50, delta = 0.05) | **No** |
| A-vi Lucas invariance | A calibrated multi-block coupled engine **and** a multi-regime social reanalysis corpus | **Half.** The loop could be the forward-engine half, *if* the corpus existed. It does not |
| A-vii regime occupancy | An **operationalised regime monitor** on a live named series | **No** |

So it is three unstarted falsifiers, not four; two of the three are NEEDS-DATA, not engine-blocked; and neither this harness nor the paper supplies E-6, the social reanalysis corpus that `RUN_AND_CHECK.md:125` calls the "single largest missing piece", nor the live externally-timestamped track record. The dependency is narrow and one-directional and should be stated that way. "Blocked on exactly that" and "the same missing piece approached from two directions" are withdrawn.

**Three things must be built or fixed before Substrate B can be an observation channel at all.**

- **The data is not in the tree.** `.gitignore` excludes `validation/**/data/` wholesale and the 7.1 GB Reddit dump that five harvesters depend on is not committed. The channel has to be re-harvested before anything here runs.
- **One of the three trace fields does not exist.** Of `neff`, `semantic_variance_z` and `operator_hhi` in the §5.3 Substrate-B payload, `operator_hhi` maps to an existing correct function, `neff` maps to a function with the defect below, and **`semantic_variance_z` does not exist anywhere in the repository**. It must be written and pre-registered before it appears in a trace.
- **`neff` as currently called is a look-ahead leak.** `neff_collapse_wsb.py:234` sets `hi_full = onset + POST_DAYS + 1` and `:221` normalises the baseline window by that full-span mean, so the pre-onset observation depends on post-onset data: on an identical pre-onset matrix, N_eff is 2.4590 or 2.1642 depending only on the future. **Using it as a causal observation voids any forward claim made from it.** Fix the normalisation to use pre-onset data only, and re-derive any threshold that was set against the leaked version.

### 4.1 The loop, instantiated

1. **Observation.** A block's state at time `t`: mention-density series, embedding-variance (belief dispersion), community partition, operator concentration (HHI / Gini). Mostly the repo's existing observation operators, with the two exceptions named above: belief dispersion has no implementation, and `neff` has a look-ahead leak that must be fixed before it can be an observation at all.
2. **Proposal.** The §2.2 proposers read the block state as structured text, which on this substrate is what the observation already is, so there is no second rendering to build and no equivalence check to run. Each returns a distribution over `O_B` (§2.3), a forecast at horizon `h`, and reasoning.
3. **Disagreement gate.** JS divergence across tower forecasts, **for corpus admission only**. Per §2.1, no skill statistic may be computed on the gated subsample: a Brier or hold-rate comparison against persistence, climatology, a market or a superforecaster baseline is a population statistic over the full pre-registered question set, and disagreement conditioning biases it by construction. Any number reported against an external baseline comes from the ungated arm.
4. **Adjudication by reality.** Wait out the horizon, harvest what happened.
5. **Yield.** Surprisal of the realised outcome under the pre-registered **proposer** ensemble forecast, per §2.3, over `O_B` and floored, so it is bounded by 8.294 nats.
6. **Admit.**

### 4.2 Why this substrate and not just a code executor

Result (4) shows self-play works with a code executor. A code executor is a deterministic program, and so is an emulator. A large enough model can in principle internalise either, at which point yield legitimately goes to zero and the well runs dry. **Environments that resist simulation are the renewable ones.**

Social reality cannot be internalised, which is the companion paper's central negative finding (out-of-model agents; more data does not help) restated as a resource rather than a limitation. It also comes with pre-registration discipline: frozen thresholds, committed rosters, decision rules written before harvest. A bootstrap harness needs exactly that discipline, because otherwise it grades its own homework.

**But do not overstate the discipline, because the round-2 audit did not.** `PREREGISTRATION_SEAL.md` pins digests for exactly two files and names neither `neff_v3` nor `neff_v4`, and git carries no temporal separation between those thresholds and their results, so "sealed" is not earned for the runs this harness would consume (P-05). The headline binomial p = 1.7e-7 rests on an assumed null fire rate p0 = 0.10 that the repository's own clean-window data does not support, and its pass condition breaks above p0 = 0.378 (P-01). **Neither claim may be inherited by this document as evidence.** What Substrate B contributes is the *form* of the discipline, not a validated result to lean on, and the fix is forward-looking: lodge an independent timestamp before the run, per `F9_PREREGISTRATION.md` §11, rather than claiming one retrospectively.

And reflexivity, the hard case, only appears here. A LOGOS-class ensemble forecasting a social system it is deployed inside is the mean-field-game fixed-point problem the companion paper formalises. Pokémon cannot test that.

### 4.3 The cost problem, measured

Earlier drafts said "a few thousand good trajectories per quarter is three orders of magnitude short". Both halves of that are wrong, and both in the flattering direction. The measured numbers:

- **Structural latency floor.** `window_for()` spans `[onset-90d, onset+22d)`, so no verdict exists until **22 days of post-onset reality** have accrued, on top of 90 days of pre-onset history. Nothing in the design shortens this.
- **Not model-triggered.** Onsets are analyst-frozen public event dates (`PRE_REGISTRATION_neff_v4.md:85`), so a human nominates every single adjudication. The loop cannot decide what to observe next.
- **One bit per trajectory.** The verdict is `fires_vs_shuffle` plus two scalars (`drop_macro`, `shuffle_pctile`) over a 112-day window. A terminal binary label is not the dense step-wise signal a training loop consumes.
- **Hard substrate ceiling.** The WSB continuous record runs 2019-10-28 to 2024-08-26, 1764 days. At the 112-day window that is **15 non-overlapping adjudications on the entire dump**, and 39 even at the repository's looser 45-day separation. There is no thousand.
- **Demonstrated lifetime yield: 93 adjudicated windows**, across every substrate and every run the programme has ever done (Wikipedia 14 event + 10 calm, WSB 10 + 10, neff_v2 15, neff_v3 10 + 12, neff_v4 12). Earlier revisions of this line, and `../logos.tex` §12, printed **94**, which does not sum from its own breakdown: `14+10+10+10+15+10+12+12 = 93`. The shortfall is unchanged at 7.8 orders (`log10(5.6e13/9.3e5) = 7.78`), but this is the headline count of a recomputation whose whole point is that the earlier numbers were wrong, so it is corrected rather than rounded past.
- **CPU-only.** The validation pipeline is numpy on CPU, so it contributes zero GPU utilisation while imposing a calendar barrier.
- **The shortfall, recomputed.** Against a 2.8T tower at 20 tokens per parameter = 5.6e13 tokens, at a generous 1e4 tokens per trajectory: 3,000 trajectories per quarter is 3.0e7 tokens, **6.3 orders of magnitude short**. At the demonstrated lifetime yield it is **7.8 orders**. Call it 6 to 8, not 3.

**Consequence, and this is a re-scope rather than a hedge.** Substrate B is removed from anything shaped like a loop. It is a **single end-of-training validity probe**: one verdict, on the order of 10 to 30 admitted episodes, run once, after the Substrate-A arms are complete. It is not a token source, not a training signal, and not an endpoint in F9's primary or secondary families (`F9_PREREGISTRATION.md` §12). If yield-weighted grounded trajectories help on the emulator but not when reality adjudicates, the mechanism was learning emulator artifacts. **A for volume, B for validity, once.**

**The adjudicator should not be the real outcome.** Retrospective backtesting on sealed rosters relieves the calendar cost and was previously priced only as "the usual price in hindsight contamination". That price is not payable: every frozen open-weight proposer has read about GameStop, LUNA, FTX and COVID, 82 of 83 roster rows have onsets before 2025-01-01, so knowledge-cutoff-based model selection leaves N = 1, and entity scrubbing raises the floor without stripping structural recognisability. The contamination-proof adjudicator already exists in the repository: the **block-label shuffle** (`neff_collapse_wsb.py:275-285`, 300 permutations preserving users, volumes and the graph while destroying block structure) and the **matched-calm arm** generate episodes that never happened and therefore cannot have been memorised, at 300 shuffles across 58 episodes. **Make the shuffle-and-calm arm the primary Substrate-B adjudication and demote the real-outcome arm to a caveated secondary.** It costs nothing new to build and it is the single most valuable design change available here.

**Power, so the probe is not run blind.** Counted from the seven frozen rosters: 83 roster rows, 68 distinct onset dates, 58 distinct real-world episodes, 35 carrying a committed endogenous/exogenous label. Paired one-sided power at 80% gives a minimum detectable effect of **d = 0.42 at N = 35**, and 0.50 under Bonferroni-3 for the three pairwise comparisons a four-arm ordering needs. After K >= 3 attrition and the disagreement gate, plan for an admitted N of **20 to 30**, **at which the MDE is not 0.42**: it is 0.556 at N = 20, 0.497 at N = 25 and 0.454 at N = 30, or 0.664, 0.594 and 0.542 under the same Bonferroni-3. The 0.42 belongs to the unattritted N = 35 and quoting it at the planned N understates the design's own MDE by 8 to 58 percent. The empirical precedent is on this exact substrate: `early_warning_powered/result_powered.json` ran semantic-CSD endogenous versus exogenous at AUC 0.600, n = 5/5, Mann-Whitney one-sided p = 0.345. **Substrate B can refute and cannot confirm. A null from it is not evidence of absence, and this document will not read one as such.**

---

## 5. Model, training, schema

### 5.1 Model

Decoder-only, RMSNorm, RoPE, SwiGLU, **QK-norm**, no bias.

| | 125M (**powered screen**, n = 8, 5 arms) | 350M (**confirmatory**, n = 3, 3 arms) |
|---|---|---|
| d_model / layers / heads / head_dim | 768 / 12 / 12 / 64 | 1024 / 24 / 16 / 64 |
| context | 2048 | 2048 |

Earlier drafts had 125M as a debug rung and 350M as the main event. That ordering is inverted: at this budget seeds buy more inferential value than parameters, so 125M carries the ordering test and 350M is a low-n replicate that checks the effect does not vanish with scale (`F9_PREREGISTRATION.md` §8.1).

QK-norm is not optional. Chameleon (arXiv:2405.09818) found it necessary for mixed-modal stability; without it, loss diverges after roughly 20% of an epoch at 7B.

**Vocabulary:** text 8k–16k (mined) + observation codes 2k–8k + specials (BOI/EOI, role delimiters, held-out mask), about **10k–24k total**. A small vocabulary keeps the embedding table cheap, which matters at 24 GB.

**Observation codes are input-side only.** Under §3.2's per-position collapse the model never emits an observation code, so the codes need input embeddings and **no output-head rows**: keep the head over text tokens and specials, and mask observation-code logits to `-inf`. Untie the embeddings if the trainer ties them by default. This is the memory dividend of the collapse decision and it is worth taking at 24 GB. The §5.2 ablation switch is the one configuration that re-introduces them on the output side, via a factorised head of 3 sub-softmaxes.

**Observation-code embedding init:** from the RQ-VAE codebook vectors through a learned linear projection (codebook dim → d_model). Under collapse the per-position input embedding is the **sum** of the 3 residual levels' projected codebook vectors, which is MAGVIT-v2's token-factorisation pattern. Reuse the existing mean-of-subtoken init for mined text tokens.

### 5.2 Early fusion and the loss decision

- **Delimiters.** Wrap every observation-code span in BOI/EOI specials, as Chameleon does.
- **Mask the loss on observation codes.** The model must **read** observations, not generate them. Prefix-LM style: observation codes are context, loss lands on thought and action tokens. This follows Emu3's understanding stage (arXiv:2409.18869; *Nature* s41586-025-10041-x, phased training with loss weighting so vision tokens do not dominate) and is independently supported by PaliGemma (arXiv:2407.07726), which found that predicting the prefix "clearly reduces average performance." Chameleon Fig. 6b, where instability vanishes once image generation is disabled, is the stability argument for the same choice. **Keep an ablation switch, and it is now paid for:** unmasking needs the factorised head of §3.2, which costs 0.259% of a run's FLOPs, and the ablation itself is 8 runs at 9.604 GPU-h, registered as contingent rung **A6** in `F9_PREREGISTRATION.md` §8.3. It is not withdrawn and it is not in the core total.
- **Intra-observation bidirectional attention** (optional, v2): Transfusion (arXiv:2408.11039) reports a significant gain. Causal across the sequence, bidirectional within one observation's span.
- **Chain-of-thought must be load-bearing.** Loss is on thought and action; if the action were decodable from the observation alone, the reasoning span would never be learned. In the bootstrap loop this is automatic, because disagreement gating only admits trajectories where the answer was not obvious.
- **Every trace must END on a loss-bearing span, and this is a correctness requirement, not a style rule.** Under causal attention an input embedding at position `i` receives gradient only from loss-bearing positions `j > i`, and §5.4's FlexAttention block masks forbid attention across document boundaries. The §5.3 schema as first drafted ends on `result.frame`, a loss-masked span (`hp_delta` is probe labels only, `yield` is a curation scalar), so **the gradient to every code in the result frame is identically zero**: the outcome the entire loop exists to observe would train nothing, and the experiment would return a false negative before any GPU ran. The cited support does not transfer, because PaliGemma masks the image as a *prefix* that is always followed by loss, whereas here the masked span is last. **Fix, mandatory:** a loss-bearing natural-language `outcome` span after every result frame, and a compiler assertion in `schema/validate.py` that no trace ends on a loss-masked span. Traces failing the assertion are rejected at compile time, not dropped silently.

### 5.3 Trace schema

One grammar, so sequence packing sees a single format. Only the `observation` payload type differs.

**Substrate A:**
```yaml
episode: pokemon_red_battle_0142
step: 17
observation:
  type: screen
  frame: [<boi> <v_412> <v_87> <v_1003> ... <eoi>]   # 90 collapsed RQ-VAE codes (§3.2), LOSS-MASKED
proposals:                       # the disagreement that justified generating this at all.
                                 # Proposers are the frozen distinct-lineage open models of §2.2
                                 # and they read the §3.4 observation card, never the codes above
  - proposer: P1 ; predict: "rock resists normal moves" ; action: select_move water_gun
    p_outcome: {eff: [0.05,0.10,0.20,0.65], dmg: [0.05,0.10,0.20,0.35,0.30], faint: [0.20,0.80]}
  - proposer: P2 ; predict: "type chart unknown"        ; action: select_move tackle
    p_outcome: {eff: [0.10,0.35,0.45,0.10], dmg: [0.30,0.35,0.20,0.10,0.05], faint: [0.75,0.25]}
  js_divergence: 0.5467          # bits, recomputed from the two p_outcome vectors above over the
                                 # factorised joint on O_A (|O_A| = 40, §2.3). Earlier drafts
                                 # printed 0.61 against no distribution at all. Never computed over
                                 # token distributions: the proposers do not share a tokenizer, so
                                 # a token-level divergence is undefined (§2.2)
selected_proposer: P1            # seeded uniform draw over well-formed proposals (§2.2)
selection_seed: 4c1f9a02
thought: rock resists normal moves
                                 # VERBATIM COPY of proposals[P1].predict (§2.2). Not authored.
                                 # schema/validate.py asserts equality. An earlier draft printed
                                 # "enemy Onix is rock and ground; water and grass hit 2x; my
                                 # Squirtle knows water_gun" here, which no proposer produced, which
                                 # states the adjudication the loop is about to make, and which
                                 # states it WRONGLY: Onix is Rock/Ground and Water is 2x against
                                 # both, so water_gun against Onix is 4x. That span was the single
                                 # most loss-bearing text in the corpus and it was written by an
                                 # oracle with outcome access
action: select_move water_gun    # proposals[P1].action, per selected_proposer above
result:
  type: screen
  frame: [<boi> <v_...> <eoi>]   # 90 codes, LOSS-MASKED
  hp_delta: -18                  # RAM-derived; PROBE LABELS ONLY
  max_hp: 34                     # RAM-derived; PROBE LABELS ONLY. REQUIRED, because hp_delta alone
                                 # does not determine the damage quintile: -18 is q4 at max_hp 30,
                                 # q3 at 36, q2 at 60, all plausible Onix values across levels
  o_observed: {eff: super, dmg: q3, faint: no}
                                 # REQUIRED. Names the exact cell of O_A. 18/34 = 0.529 -> q3
  yield: 2.9101                  # nats. -ln( floor(P_M)[o_observed] ), reproducible from the two
                                 # p_outcome vectors above: P_M = 0.5*(0.65*0.20*0.80
                                 # + 0.10*0.20*0.25) = 0.0545, floored to 0.0544705, -ln = 2.9101.
                                 # Earlier drafts printed 2.31, which is not any reachable cell:
                                 # the five values under (super, no) are 4.0885, 2.9101... in q
                                 # order 4.0885 / 3.4937 / 2.9101 / 2.3839 / 2.5443, and 2.31
                                 # implies P_M = 0.0993, which no cell produces.
                                 # schema/validate.py asserts this equality to four decimals
outcome: water_gun landed super effective; Onix lost 18 of 34 HP and the turn ended
                                 # MANDATORY, LOSS-BEARING, and the LAST span of the trace.
                                 # Without it the result frame receives zero gradient (§5.2).
                                 # "super" is O_A's cell name and conflates 2x with 4x (§2.3);
                                 # the true multiplier here is 4x and O_A cannot express it
```

**Substrate B:**
```yaml
episode: wsb_cascade_2021w04
horizon_weeks: 3
observation:
  type: block_state
  block: r/wallstreetbets
  neff: 1.42                     # pre-onset window ONLY; see the look-ahead leak in §4
  semantic_variance_z: +2.1      # OPERATOR DOES NOT EXIST YET; must be written and pre-registered
  operator_hhi: 0.0011           # measured WSB pre-onset range is 3.4e-05 to 2.0e-03.
                                 # Earlier drafts printed 0.31, which is the GitHub
                                 # small-cohort regime, not this substrate
proposals:
  - proposer: P1 ; predict: endogenous_cascade ; p_label: 0.72
    p_outcome: {endo_fires: 0.576, endo_not: 0.144, exo_fires: 0.154, exo_not: 0.126}
  - proposer: P2 ; predict: exogenous_shock    ; p_label: 0.35
    p_outcome: {endo_fires: 0.210, endo_not: 0.140, exo_fires: 0.455, exo_not: 0.195}
  js_divergence: 0.1254          # bits, recomputed over the full O_B joint (|O_B| = 4, §2.3).
                                 # Earlier drafts printed 0.58, which no numbers here give, and
                                 # then 0.1017, which is the divergence over the LABEL MARGINAL
                                 # alone; the yield needs the joint, so the joint is what the gate
                                 # scores. Admission is decided by tau_JS at q = 0.25, not by this
selected_proposer: P1            # seeded uniform draw over well-formed proposals (§2.2)
selection_seed: 9b30d7e5
thought: endogenous_cascade
                                 # VERBATIM COPY of proposals[P1].predict (§2.2). Not authored.
                                 # An earlier draft printed a composed analyst sentence here
                                 # ("operator ramp is 13 weeks and N_eff is collapsing past its own
                                 # block-label shuffle; that is the endogenous signature, not a news
                                 # shock") which no proposer produced and which nothing generated
action: forecast                 # proposals[P1].action
action_input: {label: endogenous, onset_window: "2021-01-25/2021-02-01"}
result:
  type: adjudication
  source: block_label_shuffle      # PRIMARY adjudicator (§4.3): contamination-proof.
                                   # harvested_outcome is the caveated SECONDARY
  realised: fires_vs_shuffle_true
  o_observed: endo_fires           # REQUIRED. `realised` alone under-determines the cell, because
                                   # O_B is the product space and the endo/exo half is not in it
  yield: 0.9343                    # nats. P_M(endo_fires) = 0.5*(0.576+0.210) = 0.393, floored to
                                   # 0.392857, -ln = 0.9343. Earlier drafts printed 1.04, which
                                   # implies P_M = 0.3535 and is not any of the four reachable
                                   # values 0.9343 / 1.9512 / 1.1893 / 1.8289
outcome: the observed N_eff drop cleared its own 300-draw block-label shuffle null;
         the operator ramp preceded it rather than following the news
                                   # MANDATORY, LOSS-BEARING, LAST span (§5.2)
```

**Text-harness variant** for the language-competence half of the corpus uses the same keys with `observation.type: tool_result`, and a four-variant fan-out (hit / near-miss / misleading-but-plausible / multi-hop) following AgentFounder (arXiv:2509.13310) and the phi "textbooks" method, generated locally by a Qwen3-class MoE on the same GPU at zero API cost. Apply the held-out filter of §3.3 as a hard post-processing step over all three surfaces (raw text, detokenized text, mined vocabulary): **exact tokenized set membership over word unigrams and n-grams, never regex and never substring containment**, failing closed if the vocabulary or tokenizer will not load.

### 5.4 Training

**Trainer:** a modded-nanoGPT derivative (`KellerJordan/modded-nanogpt`; `Deveraux-Parker/nanoGPT_1GPU_SPEEDRUN` for the single-consumer-GPU adaptation). `litgpt` is a fallback.

**Optimizer:** Muon on 2D matrices, AdamW on embeddings, head, norms, and 1D params. Muon keeps one momentum buffer instead of two, saving about 4 B/param on 2D matrices (~1 GB at 350M), and is reported roughly 35% faster to a target loss. Fallback: plain AdamW (β 0.9/0.95, wd 0.1, clip 1.0, cosine or trapezoidal, warmup).

**Precision:** bf16. FlashAttention-2 works on Ampere; **FP8 does not** (GA10x tensor cores do TF32/BF16/FP16/INT8/INT4 only).

**Memory at 350M / 2048 / bf16 / 24 GB:** about 5.6 GB fixed for AdamW state (16 B/param mixed) plus activations. Micro-batch ~4 without checkpointing; 8 may need it. Gradient accumulation to a global batch of 256k–500k tokens per step.

**Throughput, corrected against the card's own ceiling.** Earlier drafts of this document gave 18k–30k tok/s at 350M/2048 and 45k–90k tok/s at 125M, interpolated from 4090, A30 and L20 runs. **The upper end of that is not reachable on this card.** At 350M/2048 the model costs 2.526 GFLOP/token forward plus backward, so 30k tok/s would require **75.8 TFLOP/s sustained**, while the NVIDIA GA102 whitepaper (Appendix A, Table 9, p.44) gives the RTX 3090 a peak BF16 tensor throughput with FP32 accumulate of **71 TFLOPS dense** (142 only with 2:4 structural sparsity, which does not apply here). The stated upper bound needs above 100% MFU. The same table lists FP16/BF16/TF32/INT8/INT4 and no FP8 row, which independently confirms the precision note above.

Derived replacements, still arithmetic and still not a measurement: **about 9.1k tok/s at 350M** (band 6.6k to 9.3k for 25% to 35% MFU) and **about 29k tok/s at 125M**. In budget terms that is **about 30 to 42 GPU-hours per 1e9 tokens at 350M**, and about **9.6 GPU-hours per 1e9 tokens at 125M**. Every GPU-hour figure in `F9_PREREGISTRATION.md` §8.1 has been **recomputed** against these replacements rather than scaled from the withdrawn ones. The training lines that came out total 1,402.6 GPU-h under the withdrawn stand-in proposers, and **1,536.5 GPU-h once §2.2's frozen open-weight proposers are priced** at the 1B-class planning instantiation (1,683.6 before Study 2's per-seed corpus multiplier and duplicated A0 arm were withdrawn there). Two independent bands sit on that: the 25% to 35% MFU assumption, which is what the day-one probe below resolves, and the proposer roster, which is what freezing the roster resolves.

**The proposer arithmetic runs off the same sustained figure, which is why it is stated here.** The frozen 9.1k tok/s at 350M and 2.526 GFLOP/token imply a sustained `python3: 2.526e9*9.1e3 = 2.29866e13` FLOP/s, and the harness already prices forward-only inference at one third of forward-plus-backward. Inference therefore costs `2.526e9/3/3.5e8 = 2.4057` FLOP per token per parameter, so a proposer of `N` parameters runs at `2.29866e13/(2.4057*N)` tokens/s: `python3: 2.29866e13/(2.4057*3.5e8) = 27,300` reproduces the ledger's own 27.3k figure at 350M exactly, and the same expression gives 9,555 tok/s at 1B and 1,194 at 8B. Batch at least 8 so decode is compute-bound rather than bandwidth-bound: at 4.25-bit weights an 8B proposer reads 4.24 GB per decode step, and `python3: 8*936e9/4.24e9 = 1,766` tok/s of bandwidth-limited throughput already exceeds the 1,194 compute cap. This is still arithmetic against a published ceiling, the decode MFU assumption is the optimistic end, and the day-one probe now measures quantized proposer inference as well as training.

**Day-one probe, before committing to any schedule.** Run a forward-backward probe with `torch.cuda.max_memory_allocated` and record measured tok/s at both sizes. **If measured throughput falls below 60% of the planning midpoint, reduce tokens per run before reducing seeds.** Seeds are the inferential currency here; tokens are not.

**Data schedule:** ≤4 epochs (Muennighoff et al., arXiv:2305.16264, NeurIPS 2023: up to 4 epochs of repeated data costs almost nothing against unique data, validated across 400+ runs, 10M–9B params, up to 900B tokens). Watch for the epoch-5 jump. **20–30% text replay whenever observation data is mixed in**; cap the observation stream at 15–30% of tokens. **Accumulate the corpus across rounds, never rotate it** (Gerstgrasser).

**Packing:** several traces per 2048-token sequence with document boundaries, FlexAttention block masks to stop cross-document attention.

---

## 6. Layout

```
logos-harness/
  configs/     rqvae.yaml  tokenizer.yaml  model_{125m,350m}.yaml  train.yaml
               heldout_vocab.yaml  bootstrap.yaml        # disagreement + yield thresholds
               arms.yaml                                 # A0..A4, per F9_PREREGISTRATION.md §2
  data/        raw/  frames/  traces_text/  traces_game/  traces_psycho/  packed/
  bootstrap/   propose.py        # frozen-proposer proposal over O + JS-divergence gate, in bits
               render_observation.py # the §3.4 observation card (R-text) and R-frame packing
               parity_check.py   # §3.4 field-list diff, audit sample, code-recoverability probe
               calibrate_gate.py # tau_JS at q=0.25 on 50k proposals, BEFORE any arm
               calibrate_confidence.py # F13 limb (b) calibrators, BEFORE any arm
               adjudicate.py     # environment step + outcome capture, mapped into O
               yield_score.py    # surprisal under the PROPOSER ensemble's pre-action distribution.
                                 # Loads no training checkpoint, by construction (§2.3)
               admit.py          # yield-weighted, accumulating corpus admission
  proposers/   roster.yaml       # the frozen proposer roster: model ids, revisions, quantization,
                                 # lineage attestation, sha256 of each weight file (§11 seal there)
  substrate_a/ pokegym_dump.py  savestates/  vgbench_eval.py
  substrate_b/ harvest_adapter.py   # thin wrapper over ../validation/**/harvest_*.py
               block_state.py       # observation operators -> block_state payload
  rqvae/       model.py  train_rqvae.py  recon_gate.py  tokenize_frames.py
  tokenizer/   mine_vocab.py  build_tokenizer.py  embed_init.py
               heldout_filter.py    # exact tokenized set membership; NO regex, NO substring
  schema/      compiler.py  validate.py   # asserts no trace ends on a loss-masked span
  corpus/      generate_text_traces.py
  train/       train.py  pack.py  run_arm.py
  eval/        grounding_probe.py  behavioral_probe.py  agent_eval.py  collapse_monitor.py
               battery_build.py     # frozen 10k+10k behavioural battery, chance exactly 0.25
               proposer_diversity.py# S4 gate, BEFORE any training arm
  analysis/    analyze_f9.py        # evaluates the frozen rule ONCE
```

---

## 7. Phases and gates

| Phase | Work | **Gate** |
|---|---|---|
| **0** | Substrate A harness: headless PyBoy, scripted and random-walk dump of ≥100k (frame, action, RAM-state) tuples, savestates at Pallet Town / first battle / first gym | 100k+ frames dumped headlessly; savestates load; RAM state parsed and **aligned to frames**; **measured** disk-write throughput recorded (published steps/sec are rollout figures and do not apply to a frame dump, which is I/O bound) |
| **1** | RQ-VAE observation tokenizer at the §3.2 frozen geometry (90 positions, 3 levels, collapsed per position) | **HP-bar within 1px · text legible · sprite identity correct · codebook utilisation >95%.** No LM training until this passes. This is a reconstruction gate only; sequence length is already fixed in §3.2 |
| **2** | Tokenizer mining, joint vocab, YAML-to-token-id compiler, held-out leak validator, **trace-terminal-span assertion** | Round-trip lossless both variants; **zero held-out terms** on all three surfaces of §3.3 (raw text, detokenized text, mined vocabulary); every control term present at >= 1,000 occurrences; **no trace ends on a loss-masked span**; embedding init sane |
| **3** | Text corpus, four-variant fan-out, quality and leak filtering | Token count reached; variant distribution as designed; leak scan clean by set membership, not by regex; human spot-check passes |
| **4** | **Bootstrap loop, Substrate A.** Proposal by **≥2 frozen open-weight models of distinct pretraining lineage, reading the §3.4 observation card and never the codes** (§2.2), each returning a distribution over `O_A`; JS-divergence gate over `O_A` in bits; emulator adjudication; yield scored under the **proposer** ensemble (§2.3); accumulating admission. Arms A0 to A4 per `F9_PREREGISTRATION.md` §2, including **A4 ungated grounded**, without which the gate effect under grounding is unidentified | **Before any arm runs:** the proposer roster is frozen with lineage attested, digests lodged, and the **S5 attempt count recorded in the seal**; the §3.4 parity checks 1 to 4 pass; **S4** proposer diversity measured, mean pairwise JS >= 0.15 or the experiment is VOID; **S5** proposer competence on a **disjoint** gate battery, one-sided exact-binomial `LCB99 > 0.35` per proposer, Bonferroni-corrected across roster members, or the experiment is VOID (`F9_PREREGISTRATION.md` §4); `tau_JS` calibrated to q = 0.25 on a 50,000-proposal pool. **Then:** the gated set's mean yield is compared against the **identity prediction** `0.5*(H(P1)+H(P2)) + JS` computed on the same items, and a **shortfall** is the informative signal; parity with the identity is the null (see below) |
| **5** | Pretraining. **125M is the powered screen (n = 8 seeds, 5 arms); 350M is the low-n confirmatory replicate (n = 3, 3 arms).** ≤4 epochs, packing, replay, curriculum, observation loss masked | Stable loss (no divergence, QK-norm on); no epoch-5 jump. **The collapse monitor is a reported diagnostic here, not a blocking gate**: firing on the unfiltered self-play arm is the *predicted* result, and halting the experiment on it would halt on a prediction coming true. See §8 |
| **6** | Probes and agent eval | Held-out terms show above-chance grounding **against the control**; super-effective choice above chance. **VideoGameBench Lite is descriptive, not a gate**: frontier models complete 1.6% of Lite, a 350M model scores 0 in every arm, and an endpoint with zero between-arm variance has zero power |
| **7** | **Substrate B, once, at the end.** Re-harvest the observation channel (the dump is not in the tree), write `semantic_variance_z`, fix the `neff` look-ahead leak, then run **one** verdict over 10 to 30 episodes with the block-label shuffle and matched-calm arm as primary adjudicator | Yield-weighted grounded trajectories beat both unfiltered self-play **and** a text-only control, **with the shuffle-and-calm arm adjudicating** and the real-outcome arm reported as a contaminated secondary. If A passes and B fails, the mechanism was learning emulator artifacts. A null here is not evidence of absence at N = 20 to 30 (§4.3) |

**The Phase-4 yield gate as previously written could not fail, and it is replaced rather than kept.** The gate read: "admitted trajectories have mean yield strictly above the unfiltered control (if not, the run is VOID, not negative)". That is an algebraic identity in Jensen-Shannon divergence, not a check. `H(P_M) = 0.5*(H(P1)+H(P2)) + JS(P1,P2)` exactly, and expected yield on an item, if outcomes track `P_M`, is `E[-ln P_M(o)] = H(P_M)`. Gating on `JS >= tau_JS` therefore selects items of higher expected yield **by construction**, one nat of yield per nat of divergence, for any two proposers including two uniformly random ones. On this document's own §5.3 vectors both sides come to **4.9420 bits**, identical to four decimal places. The units separation at §2.3, yield in nats and JS in bits, is precisely what hid the identity from its own authors. And on the second reading it is worse: if "the unfiltered control" is A1 or A2, whose pseudo-outcome is `argmax P_M`, its yield is the surprisal of the *mode*, the minimum over `O`, and the comparison is won before it is run.

**What replaces it, and what it can now detect.** Compare the gated set's realised mean yield against the identity prediction on the same items. **Parity is the null.** A **shortfall** means the environment is *less* surprising than the ensemble's own disagreement predicts, which is the direction that carries information: it says the proposers disagree about things the environment does not distinguish. A large *excess* means outcomes do not track `P_M` at all, which is a proposer-calibration failure that S4 and S5 already exist to catch, and is reported as such rather than as evidence about the loop. **This gate no longer VOIDs the run**, because it can no longer certify the property it was installed to certify: `../logos.tex` §12 step 2's distinction between "the environment carried information the ensemble lacked" and "the two proposers disagreed" is not decidable from mean yield alone, and pretending otherwise is what the identity above exposes. It is a reported diagnostic. The VOID conditions that remain are S4, S5, the parity checks and the leak scan.

**The phase numbers are not the run order, and the two used to be inconsistent.** Phases are a dependency order for what is *built*; `TIER0_3090_PLAN.md` carries the order things are *run* in, and under §2.2 that order changes: S4, S5, `tau_JS` and F13 limb (b) run on the observation card, which is built from the Phase-0 dump, so **nothing on the proposal path waits for the Phase-1 RQ-VAE**. Under the withdrawn stand-in reading every one of those gates needed the codes, and the run order that scheduled them before Phase 1 could not have executed.

**But the Phase-4 gates are not Phase-0-only, and an earlier revision of this paragraph said they were.** They are conditioned on the §3.4 parity checks, and **check 3 needs Phase 1** while check 1 diffs against the field list the Phase-1 reconstruction gate certifies. The cost of pretending otherwise is concrete: if check 3 drops `status condition`, then all 50,000 `tau_JS` calibration proposals were conditioned on a card that no longer exists, `tau_JS` no longer admits `q = 0.25`, and S4, S5 and the 36.3-hour limb (b) were all measured on a retired rendering. **Frozen, and it is a scheduling statement rather than a new experiment:** the card's field set is **pre-committed to the four Phase-1 target fields plus the legal action set and the category labels**, and post-hoc drops are forbidden; if check 3 nevertheless fails on a pre-committed field, the RQ-VAE is repaired rather than the card trimmed, and **one `tau_JS` re-calibration is priced** (1.8 GPU-h at the planning roster) rather than assumed free.

**One Phase-0 quantity moves with the split and is recorded here.** The Phase-0 gate asks for 100k frames, which is a gate and not the dump size. The loop needs a **distinct battle observation per proposal**, and `F9_PREREGISTRATION.md` §8.1 counts 403,226 proposals for an ungated 125M arm and 1,612,904 for a gated one. Battle observations at that volume come from scripted play against savestates and are I/O and CPU bound, contributing zero GPU-hours, but they are not free of engineering and the dump plan has to target the gated figure rather than the gate.

**The statistical design is not in this document.** Arms, sample size, seeds, endpoints, effect sizes, test statistics, multiplicity correction, stopping rule and kill conditions are frozen in `logos/F9_PREREGISTRATION.md`, which is the binding artifact. This document specifies what is built; that one specifies what counts as a result.

**The headline ordering the whole spec tests (falsifier F9 in the paper):**

> grounded > disagreement-gated self-play > unfiltered self-play > nothing

If unfiltered self-play matches grounded trajectories at matched token counts, the observation bound is wrong and this line of work should stop. **"Matches" is an equivalence claim and it is expensive**: the 72 to 96 GPU-hour budget the ledger carries buys **0.24 to 0.31 seeds per arm** at 350M across the **five** arms of `F9_PREREGISTRATION.md` §2, and 1.50 to 2.00 seeds per arm at the 125M screen, so n <= 2 either way. At n = 1 there is no within-arm variance estimate and no test statistic of any kind can be computed; at n = 2 the five-contrast MDE is 3.168 sigma, which is 0.158 accuracy points, above the delta = 0.15 the design exists to detect. Either way the experiment can confirm and cannot refute, which is the exact inverse of its purpose. The powered design is **about 1,540 GPU-hours** (1,536.5 at the §8.1 planning instantiation, and 1,376.8 to 3,773.3 across the proposer sizes priced there), which at 1,536.5 is **$307 to $384** rented at RTX-3090 community-cloud rates or **538 kWh, about EUR 161** of electricity on the owned card. **The 125M screen is what makes it affordable:** a 125M run is 9.579 GPU-h against 61.050 at 350M, so the powered five-arm n = 8 ordering study is 383.1 GPU-h, where the same study run at 350M would be 2,442 GPU-h and would not fit the card. A non-significant result below n = 8 is reported UNDERPOWERED, never as a negative. **And the gate contrast is still not bought:** at n = 8 the tightest declarable equivalence margin is 6.2 accuracy points against a superiority threshold of 7.9, so a true gate effect in that window lands INCONCLUSIVE by construction. Closing it needs n = 13, which is 622.6 GPU-h in Study 1, at 5.0 points, or n = 35, which is 1,676 GPU-h in one study, at 3.0.

---

## 8. Risks

| Risk | Mitigation |
|---|---|
| **Lossy RQ-VAE caps everything.** No HP bars or text means no grounding, and it fails silently | The hard Phase-1 gate. Edge and region weighted loss. Low downsampling. Four-colour frames are in your favour |
| **Model collapse** | Disagreement gating and yield weighting structurally exclude confident self-agreement; corpus accumulates rather than rotates (Gerstgrasser). Explicit `collapse_monitor.py` against arm A0 at the same optimizer step, on three statistics (tail NLL, predictive entropy, representational participation ratio). **The consequence must be arm-qualified, and earlier drafts of this document were not.** Firing on **A3, the grounded arm**, refutes the admission rule, which is the third of the paper's three original claims. Firing on **A1** is *predicted* by the two sources §1 result (3) cites and refutes nothing. Firing on **no arm at all, including A1**, means the monitor is insensitive at this budget and every collapse conclusion from F9 is VOID |
| **Towers stand in for towers.** Frozen open models of 0.5B to 8B class are not 2.8T towers, and the disagreement structure may not transfer | Unavoidable at this budget. State it; do not claim validation at tower scale. Two things *are* measured before any arm runs: **S4**, mean pairwise JS >= 0.15 over `O`, or VOID; and **S5**, proposer competence, or VOID. S4 alone was not enough, because two incompetent proposers disagreeing at random satisfy it while turning the gate into a random sampler. **S5 as first written was not enough either, and it is repaired here in four places.** (i) "Strictly above chance" on a 10,000-item battery at chance 0.25 has standard deviation 43.3, so a uniformly random proposer needs 2,501 correct and passes with probability **0.4954**, and two random proposers both pass with probability 0.2454, which is exactly the failure mode S5 exists to prevent. It is replaced by a one-sided exact-binomial lower confidence bound, **`LCB99 > 0.35`**, Bonferroni-corrected across roster members. (ii) With an unfrozen roster, VOID is a re-roll rather than a terminus: three candidate pairs give `P(at least one passes by luck) = 0.5703`. **The roster is frozen before S5 runs and the S5 attempt count is written into the seal.** (iii) S5 selected proposers on `p_control` scored over **the same battery the primary endpoint's subtrahend is computed on**, and because proposer text is loss-bearing (§5.2) that inflates the learner's `p_control` and biases `g = p_heldout - p_control` toward zero, that is toward the equivalence verdict. This is the hazard `F9_PREREGISTRATION.md` §10 refuses when it declines to widen the K3 margin, and S5 was doing it to the endpoint. **S5 now runs on a disjoint gate battery**, same construction, different items, never used to score the learner. (iv) "The control condition" had two referents, §3.3's text-supported control set and the F13 persona control; **S5 means the §3.3 control set** and nothing else. Each proposer's held-out accuracy is reported alongside its control accuracy and the two must match within a pre-committed tolerance, since otherwise roster choice alone moves the headline endpoint |
| **The proposers could not read the observation, and the two binding documents named two different proposers** | Repaired in §2.2: two renderings, one observation. Proposers are frozen distinct-lineage open models reading the §3.4 card; the RQ-VAE serves the learner only. This also removes the circularity of training stand-ins in order to test whether training works, and it makes the F9 proposer inventory the F13 limb (a) and F14 instrument |
| **The loop proposes on battle steps only**, because that is where a finite pre-committed outcome space exists (§2.3) | Accepted, not solved. The primary endpoint, the held-out vocabulary and the control set are all battle semantics, so the restriction costs nothing the experiment measures, and it costs everything the experiment does not: navigation, menu use and overworld semantics are outside the loop and no claim is made about them. Extending `O` to other screen classes is a design change with its own pre-registration, not a run-time decision |
| **The generation line is now proposer-size-dominated, and the roster is not frozen** | Disclosed, not solved. Generation scales linearly in proposer parameters: 140.7 GPU-h at 0.5B against 2,251.6 at 8B (`F9_PREREGISTRATION.md` §8.1). **The F9 total is a band until the roster is frozen**, the run order puts the roster freeze and a proposer-inference measurement early, and no single total is asserted as if the roster were settled |
| **Substrate B does not scale.** **6 to 8 orders of magnitude short**, not 3, with a hard ceiling of 15 to 39 adjudicable windows on the entire WSB dump and 94 produced in the programme's lifetime | Stated, not solved, and now re-scoped: B is one end-of-training validity probe, not a loop and not a token source (§4.3) |
| **Substrate B episodes are memorised.** 82 of 83 roster onsets predate 2025-01-01; every frozen open-weight proposer has read about GameStop, LUNA, FTX and COVID | Knowledge-cutoff model selection leaves N = 1 and entity scrubbing cannot strip structural recognisability. Make the **block-label shuffle and matched-calm arm** the primary adjudicator: those episodes never happened and cannot have been memorised (§4.3) |
| **Look-ahead leak in the `neff` observation operator.** The pre-onset observation is normalised by a full-span mean that includes 22 days of post-onset data | Fix the normalisation to pre-onset only before Phase 7 and re-derive any threshold set against the leaked version. Until then, no forward claim may be made from that operator (§4) |
| **One seed per arm proves nothing.** At the corrected throughput the 72 to 96 GPU-h budget `GAPS.md` used to assign F9 buys 1.18 to 1.57 runs at 350M across **five** arms, which is 0.24 to 0.31 seeds per arm, and 7.52 to 10.02 runs at the 125M screen, which is 1.50 to 2.00 | n = 8 at 125M as the powered screen, n = 3 at 350M confirmatory, a blind loss-spike outlier rule detected from the loss curve alone, and a 20% replacement reserve, which drops P(at least one of five arms corrupted) from 0.672 to 0.051. About **1,540 GPU-hours** total (1,536.5 at the §8.1 planning instantiation), of which the powered screen is 383.1 |
| **The gate contrast is not bought, and no seed count in this budget buys it.** At n = 8 the tightest declarable equivalence margin is 6.2 accuracy points and superiority needs 7.9, so a true gate effect between them is INCONCLUSIVE by construction | Not mitigated, disclosed. n = 13 (622.6 GPU-h in Study 1) reaches 5.0 points and n = 35 (1,676 GPU-h in one study) reaches 3.0; neither is budgeted, and the margin is **not** widened to make kill condition K3 easier to declare, because that would make a false K3 easier to reach as well (`F9_PREREGISTRATION.md` §10) |
| **The result frame receives zero gradient** if a trace ends on a loss-masked span | Mandatory loss-bearing `outcome` span, enforced by a compiler assertion (§5.2). This would have produced a false negative before any GPU ran |
| **The disagreement gate biases any statistic computed after it** | Gate for what you train on; report from the ungated arm (§2.1) |
| Held-out term never learnable, co-occurrence too sparse | Over-represent battle frames; verify the tokenizer preserves on-screen text; **keep the control set so a null is interpretable** |
| Grammar not learnable from structured traces alone | 70–85% text stream includes prose, not only tool calls. BabyLM (arXiv:2504.08165) shows 100M-word natural-text budgets suffice for grammar |
| Observation codes swamp or destabilise training | Mask observation loss; cap at 15–30%; 20–30% text replay; QK-norm and z-loss |
| 3090 memory or GPU-hour overrun | Micro-batch 4 plus gradient accumulation; Muon; 125M as the screen rather than a warm-up; ≤4 epochs |
| **Throughput figures are derived, not measured on a 3090** | Day-one forward-backward probe before committing to a schedule; the old 18k–30k tok/s upper bound exceeded the card's dense BF16 peak (§5.4) |
| PokéAgent confusion | Showdown and Emerald, not Red/Blue frame logging. Citation only |
| ROM legality | ROMs are in none of these repos and must be supplied by the user. The code is MIT; the games are not |

---

## 9. What this settles, and what it does not

**Settles:** whether disagreement-gated, environment-adjudicated trajectory generation beats unfiltered self-play and a matched text-only control without triggering collapse, at 125M with 8 seeds per arm, on the emulator substrate, with a control set that makes a null interpretable.

**Does not settle:** whether it transfers to 2.8T towers; whether the yield rate scales to the 10¹³–10¹⁴ tokens the paper's Proposition 2 needs; whether the effect survives when the environment is code execution, a wet lab, or a market rather than an emulator; and whether the tower-diversity claim of §1.1 holds when the towers are actually frontier-scale. Those are the real questions and this answers none of them. **Add one more it does not settle:** whether the diversity claim holds for the towers the reference architecture can actually build, which are divergent branches of one common seed rather than independent models. That is falsifier **F14** (`../logos.tex` §3.3, §15), it is not an arm of this harness, and it runs on the same card as F13 limb (a).

**Specifically does not settle, and this is new since the proposer pass.** Whether the observation card and the code rendering are equivalent in any sense stronger than field parity at matched resolution (§3.4). Measuring more than that would need a model that reads both, and there is not one. Also: the Substrate-A loop now proposes on **battle steps only** (§2.3), so nothing here says anything about grounded navigation, menu semantics, or any part of the game the outcome space does not cover.

**One correction owed upstream, and it has landed.** An earlier revision of this line said `../logos.tex` §15 "prices F13 limb (b) at 12.7 GPU-hours and says limb (a)'s cost is not derived", and recorded the edits as owed there. **That is no longer true and the rail is inverted rather than deleted:** `grep -n "12\.7" ../logos.tex` and `grep -n "not derived" ../logos.tex` both return no matches, and §15 carries **36.3** for limb (b) and **17.4** for limb (a) with F14, repeated in the surrounding prose and in the conclusion. Three documents in this directory went on recording those edits as owed after they landed; this one was among them. The register of record is ahead of its companions and the companions now follow it.

**Specifically does not settle, and this is new since the round-2 audit:** anything about Substrate B beyond a single directional probe at N = 20 to 30 with a minimum detectable effect of **0.45 to 0.56 sigma**, or 0.54 to 0.66 under the Bonferroni-3 this design applies, which can refute and cannot confirm. (An earlier revision quoted 0.42 here, which is the value at the unattritted N = 35, not at the planned admitted N; see §4.3.) and the gate contrast under grounding (A3 versus A4), which is the claim §1.1 says we would most like tested and is the contrast this design is **worst** powered to detect. That asymmetry is disclosed here and in `F9_PREREGISTRATION.md` §10 in advance, rather than discovered after the numbers land.

**Run it anyway** because it is the cheapest experiment that can return a decisive negative, provided it is run with enough seeds to license one. If disagreement-gated grounded trajectories do not beat a text control, at n = 8 with an equivalence margin of 1.243 sigma (about 6 accuracy points), on the easiest imaginable grounding substrate, where the exact semantics under test are printed on screen in four colours at 160×144, then the strategy past the token wall is repetition plus synthesis, the paper's Proposition 2 headroom is all there is, and `logos.tex` should say so.

---

## 10. References

**Theory (§1).** **The martingale result:** H. K. Choi, X. Zhu and Y. (Sharon) Li, *Debate or vote: which yields better decisions in multi-agent large language models?*, arXiv:2508.17536, 2025. **Confidence weighting and diversity initialisation:** X. Zhu, C. Zhang, Y. Chi, T. Stafford, N. Collier and A. Vlachos, *Demystifying multi-agent debate: the role of confidence and diversity*, arXiv:2601.19921, 2026. Earlier drafts of this document fused these two into one entry, attributing the martingale theorem to the wrong paper and to authors who are not on it; the string "Choi et al." does not belong to arXiv:2601.19921. Smit, Duckworth, Grinsztajn, Barrett and Pretorius, *Should we be going MAD?*, arXiv:2311.17371, ICML 2024. Yue et al., Does RL really incentivize reasoning capacity in LLMs beyond the base model?, NeurIPS 2025. H. Zenil, On the limits of self-improving in LLMs, arXiv:2601.05280, 2026 (single author). Shumailov et al., *Nature* 631:755–759, 2024. Gerstgrasser et al., arXiv:2404.01413, 2024. Zhao et al., Absolute Zero, arXiv:2505.03335, NeurIPS 2025. Silver and Sutton, Welcome to the era of experience, DeepMind, 2025. SPICE, arXiv:2510.24684. EvoEnv, arXiv:2605.14392.

**Related work on the observation bound (§1.1 claim 1).** Genewein, Franklin, Lerchner, Orseau, Albanie, Bales, Wyeth, Chan, Gabriel, Leibo, Dafoe, Hutter, Graepel and Legg, *From AGI to ASI*, arXiv:2606.12683, 2026 (friction taxonomy including the data wall and an embodied bottleneck; explicitly declines to name a binding friction). Ding and Wang, arXiv:2606.22495, 2026 (environment determinism as a complementary binding axis). Sun et al., arXiv:2510.14253, 2025 (verification capacity as the empirical bottleneck in agentic self-learning).

**Harnesses.** VideoGameBench, Zhang, Griffiths, Narasimhan, Press, arXiv:2505.18134, `alexzhang13/videogamebench` (MIT). PufferLib, J. Suarez, arXiv:2406.12905 (single author), `PufferAI/pokegym`, `drubinstein/pokemonred_puffer`, `PWhiddy/PokemonRedExperiments`. PokéAgent Challenge, Karten et al., arXiv:2603.15563 (citation only). Pokémon Red via RL, Pleines et al., arXiv:2502.19920. `NousResearch/pokemon-agent`. RAM map: datacrystal.tcrf.net.

**Tokenizers and VQ.** `lucidrains/vector-quantize-pytorch` (MIT). TIGER, Rajput et al., arXiv:2305.05065, NeurIPS 2023. Lee et al. 2022, residual quantization. MAGVIT-v2 / LFQ, Yu et al., ICLR 2024. Open-MAGVIT2, arXiv:2409.04410.

**Early fusion.** Chameleon, arXiv:2405.09818. Emu3, arXiv:2409.18869; *Nature* s41586-025-10041-x. Transfusion, arXiv:2408.11039. PaliGemma, arXiv:2407.07726.

**Training and data.** `KellerJordan/modded-nanogpt`. `Deveraux-Parker/nanoGPT_1GPU_SPEEDRUN`. Muon, kellerjordan.github.io/posts/muon. Muennighoff et al., arXiv:2305.16264, NeurIPS 2023. Seed variance: PolyPythias, arXiv:2503.09543; MultiBERTs, arXiv:2106.16163. Hardware ceiling: NVIDIA GA102 whitepaper, Appendix A Table 9, p.44. BabyLM, arXiv:2504.08165, arXiv:2412.05149. phi-1, arXiv:2306.11644. phi-1.5, arXiv:2309.05463. AgentFounder, arXiv:2509.13310.

**Substrate B.** W. Sharon, *Conditions for Predictable Social Dynamics*, draft v0.5, and this repository's `../validation/` suite.
