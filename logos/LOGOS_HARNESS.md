# logos-harness

**Implementation specification for the loop described in `../logos.tex` §12, "The observation bound."**
Status: **SPEC, unbuilt. Nothing in this document has run on a GPU.** Every throughput, GPU-hour and cost figure here is arithmetic against a published hardware ceiling, not a measurement. Hardware: one RTX 3090, 24 GB, Ampere; bf16 and FlashAttention-2 available, **no FP8**, no NVLink, no second card.

**Companion artifact:** `F9_PREREGISTRATION.md` fixes everything this document leaves free (arms, seeds, endpoints, effect sizes, test statistics, multiplicity, stopping rule, kill conditions) and is the binding statistical design. Where the two disagree, the pre-registration wins.

**Revision note.** This version applies the round-2 referee findings in `REVIEW_ROUND2.md` that land on this file: C-01, C-02, C-04, C-05 and C-08 (§1, §1.1, §10), X-12 (§2.1, §4.1), P-08 and X-11 (§4), P-11 (§4.3), and the substrate-B and pretraining method-track conclusions (§3.2, §3.3, §5.2, §5.3, §5.4, §7, §8). Corrections are recorded inline where a previous claim was wrong, rather than silently replaced.

---

## 0. What this is

The paper's argument ends at a limit that scale does not move. Sparsity removes the compute constraint, tower decomposition raises the data ceiling, four-bit serving handles memory, and after all of that the system is still capped by how fast something outside it can tell it that it is wrong. This directory specifies the cheapest experiment that can test that claim and return a decisive negative. **Cheapest, not free:** a negative is an equivalence claim, and equivalence needs seeds. At about **1,400 GPU-hours** (1,402.6 exactly, `F9_PREREGISTRATION.md` §8.1: n = 8 at 125M as the powered screen, n = 3 at 350M confirmatory) the negative **on the bound** is licensed; at the 72 to 96 GPU-hours the repository's ledger currently budgets, it is not, because at 350M that budget buys **0.24 to 0.31 seeds per arm** across the five arms of `F9_PREREGISTRATION.md` §2, a quarter of one seed, and no test statistic of any kind can be computed from it. **What 1,400 GPU-hours does not buy is the gate contrast.** At n = 8 the tightest declarable equivalence margin is 6.2 accuracy points while superiority needs 7.9, so a true gate effect between the two is INCONCLUSIVE by construction; buying a 3.0-point verdict would cost 1,676 GPU-h in Study 1 alone and it is not bought. Those distinctions are the difference between an experiment and a picture, and they are settled in `F9_PREREGISTRATION.md` rather than left to whoever runs it.

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

**Consequence for this spec, corrected.** Result (1) does **not** license "the towers must be informatively different". It says the opposite of a licence: neither identical nor diverse agents improve by talking, absent either a protocol change (confidence weighting) or something outside the conversation that settles it. What the theory supports is the adjudicator, which is what this loop supplies. Tower diversity is now stated as a conjecture of ours (§1.1 item 2, falsifier F13 in `../logos.tex` §15), it runs against the source it was drawn from, and it is **measured before any arm runs** rather than assumed: the S4 proposer-diversity gate in `F9_PREREGISTRATION.md` §4 voids the experiment if mean pairwise JS divergence between the stand-in towers is below 0.15.

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
2. **Conjecture, stated against a published result: corpus-level difference between towers is a different object from persona-level difference, and it is exploitable.** Branch-Adapt-Route produces towers pretrained on disjoint corpora under different objectives with different alignment histories, which a single self-playing model cannot manufacture, and we conjecture that this raises the loop's yield. **The literature says otherwise and we are not going to paraphrase around it.** Choi et al. (arXiv:2508.17536) extend the martingale explicitly to heterogeneous agents, and Zhu et al.'s diversity result moves only the starting distribution. Both evaluate one base model under different prompts, personas or priors, which is the reason we think the extension has not been tested against what we mean; that reason is a conjecture, not an argument from the sources. This is falsifier **F13** in `../logos.tex` §15, it is the least defended claim in the paper, and it is the claim we would most like tested. In this harness it is H3 in `F9_PREREGISTRATION.md`, isolated by the A3-versus-A4 contrast, and that document states in advance that it is the contrast the design is worst powered to detect.

   **Falsifier, and it has two limbs.** (a) Debate between towers with disjoint pretraining corpora tracks the martingale as closely as debate between personas of one model. (b) **Calibrated-confidence weighting alone** lifts ensemble accuracy on the held-out battery with no environment adjudication of any kind, which would locate the gain in the protocol rather than in the observation channel, and would mean the observation bound is not what limits the loop. Limb (b) is Zhu et al. Theorem 1 run as an arm of F9, and it is an **ensemble-level comparison rather than a pretraining arm**: two aggregation rules over the same two stand-in towers, unweighted majority against calibrated-confidence weighting, on the frozen §3.3 battery, with no emulator, no RAM and no adjudicator. It is **scored ungated**, on the full battery and never on a disagreement-conditioned subsample (§2.1), and tested by exact McNemar on the discordant pairs. It costs **12.7 GPU-h** inside F9's total (`F9_PREREGISTRATION.md` §8.2), it carries its own pre-committed kill condition **K5** (§10 there), it is the cheapest kill shot available against our own thesis, and it runs on the same one consumer card. **Limb (a) is not an arm of F9 and cannot be run with 350M stand-ins, but it does run on the same card.** It needs models whose pretraining corpora, objectives and alignment histories genuinely differ, and that is a property of how a model was trained rather than of the hardware it runs on. Such models already exist: Qwen, Llama, DeepSeek, Mistral and Gemma were pretrained by different organisations on different corpora under different objectives with different alignment histories, which is arguably a **better** instrument than five towers from one lab, since same-lab towers would share data-collection pipelines and filtering decisions and be less independent than they look. So limb (a) runs as several existing open-weight models of **different pretraining lineage** used as the towers, quantized and stepped sequentially on the 24 GB card, with no gradient step anywhere. **Distinct lineage is the treatment variable**: two models from the same lab, or two finetunes of one base checkpoint, do not count as distinct and cannot be used to fill a slot. The honest limitation is that this tests the diversity claim at the level of independently trained open-weight models and not at tower scale inside one architecture, and the ensemble under test is not a Mixture-of-Towers. **Its cost is not yet derived and no figure is asserted here.** Sequential inference over a handful of quantized models is cheap relative to any training line in §8.1, but cheap is not derived, and the derivation is owed. What remains genuinely out of reach on this card is the 5 x 2.8T ensemble itself, which is falsifier **F2** and not F13; the two must not be conflated. One steelman is recorded in advance so a positive is not over-read: Zhu et al. buy calibrated confidence with external supervision (GRPO confidence calibration, LoRA r=64 alpha=32, on a manually curated subset chosen so accuracy sits near 50%), so that route is not free of exogenous signal either, and the exogenous signal has moved into the calibrator rather than left the system. The arm must therefore hold the confidence-calibration supervision identical across arms and report its token and GPU-hour cost as a separate ledger line, exactly as generation compute is reported in `F9_PREREGISTRATION.md` §5.
3. **The admission rule.** If exogenous signal is scarce, keep trajectories in proportion to how much of it they carry.

---

## 2. The loop

**Yield** of a trajectory τ is the surprisal of the observed outcome under the ensemble's own prediction before it acted:

```
yield(τ) = −log P_M(o_observed | context, action)
```

Agreed-and-right scores near zero: self-confirmation, which is the entropy-decay path of result (3). Disagreed-and-adjudicated scores high.

1. **Propose.** Show an observation to ≥2 towers independently. Each returns a prediction, an action, and reasoning.
2. **Gate on disagreement.** JS divergence between tower predictive distributions, thresholded at `tau_JS`. Below threshold, discard. **The justification is not result (1)**, which says nothing about which samples to keep and, as corrected above, does not say diversity is what improves debate. The gate is a yield-economics rule: an agreed-and-confident trajectory has near-zero surprisal at step 5 and would be admitted at near-zero weight anyway, so gating is the cheap form of yield weighting, applied *before* the environment is paid for. Whether it adds anything over grounding alone is a hypothesis (H3), tested by the A3-versus-A4 contrast, not assumed. `tau_JS` is calibrated, not chosen: it is the value admitting exactly `q = 0.25` of proposals on a 50,000-proposal calibration pool generated before any training arm runs (`F9_PREREGISTRATION.md` §7).
3. **Act** on the environment.
4. **Adjudicate.** The environment returns the outcome.
5. **Score yield.**
6. **Admit** weighted by yield: `w(tau) = clip(yield(tau), 0, 10)`, normalised to mean 1 within each round, and **accumulate** rather than replace (result 3 / Gerstgrasser).
7. **Retrain incrementally, repeat.** Disagreement shrinks where the environment has been explored, pushing generation toward the frontier without being told to. Rounds are `R = 1` for the ordering study and `R = 5` for the collapse sub-study (`F9_PREREGISTRATION.md` §7, §8.1).

Steps 2 and 6 are the anti-collapse mechanism, and they are structural rather than heuristic: the loop cannot train on its own confident agreement.

**Both gates are computable without human labels.** That is what makes the thing runnable.

### 2.1 What the gate does to any statistic computed downstream of it

The gate conditions the retained sample on **predictor disagreement**, and disagreement correlates with item difficulty. Anything computed on gated output is therefore a statistic on a difficulty-biased subsample, biased in a direction that is not known in advance and not estimable from the subsample itself.

**Consequence, and it is a hard one:** the harness cannot score a skill falsifier on gated output. Brier scores, skill scores and hold rates against persistence, climatology, a market or a superforecaster panel are **population** statistics defined over a full, pre-registered question set. `RUN_AND_CHECK.md:50` and `:56` lock m = 50 questions and delta = 0.05 for exactly such a comparison; `:57` scores a hold rate against a naive base rate over a pre-registered announcement set; `:59` scores a fraction of windows classified imitative on a named series. Feeding any of those a disagreement-conditioned subsample does not make the test harder or easier, it makes it uninterpretable.

**Therefore an ungated scoring arm is mandatory** wherever the harness produces a number that will be compared against an external baseline: run the entire pre-registered question set through the towers with the gate **off**, score that, and use the gate only for corpus admission. The two uses of the loop are separate: gate for what you train on, do not gate for what you report. Arm A4 (`F9_PREREGISTRATION.md` §2, ungated grounded) already exists for this reason and is the arm any external-baseline comparison must be run in.

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

**Cost of the decision, disclosed.** The §5.2 ablation switch (unmask the observation loss) is **not available** under collapse without adding a factorised head of 3 sub-softmaxes over 1,024 codes each. If that ablation is run it must either build that head and say so, or run on the flattened 270-codes-per-frame variant with everything else held fixed, and be reported as a different sequence-length regime rather than a clean ablation.

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
2. **Tower dialogue.** Towers propose competing readings (endogenous or exogenous? is N_eff collapsing? is there an operator ramp?) with reasoning and a forecast at horizon `h`.
3. **Disagreement gate.** JS divergence across tower forecasts, **for corpus admission only**. Per §2.1, no skill statistic may be computed on the gated subsample: a Brier or hold-rate comparison against persistence, climatology, a market or a superforecaster baseline is a population statistic over the full pre-registered question set, and disagreement conditioning biases it by construction. Any number reported against an external baseline comes from the ungated arm.
4. **Adjudication by reality.** Wait out the horizon, harvest what happened.
5. **Yield.** Surprisal of the realised outcome under the pre-registered ensemble forecast.
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
- **Demonstrated lifetime yield: 94 adjudicated windows**, across every substrate and every run the programme has ever done (Wikipedia 14 event + 10 calm, WSB 10 + 10, neff_v2 15, neff_v3 10 + 12, neff_v4 12).
- **CPU-only.** The validation pipeline is numpy on CPU, so it contributes zero GPU utilisation while imposing a calendar barrier.
- **The shortfall, recomputed.** Against a 2.8T tower at 20 tokens per parameter = 5.6e13 tokens, at a generous 1e4 tokens per trajectory: 3,000 trajectories per quarter is 3.0e7 tokens, **6.3 orders of magnitude short**. At the demonstrated lifetime yield it is **7.8 orders**. Call it 6 to 8, not 3.

**Consequence, and this is a re-scope rather than a hedge.** Substrate B is removed from anything shaped like a loop. It is a **single end-of-training validity probe**: one verdict, on the order of 10 to 30 admitted episodes, run once, after the Substrate-A arms are complete. It is not a token source, not a training signal, and not an endpoint in F9's primary or secondary families (`F9_PREREGISTRATION.md` §12). If yield-weighted grounded trajectories help on the emulator but not when reality adjudicates, the mechanism was learning emulator artifacts. **A for volume, B for validity, once.**

**The adjudicator should not be the real outcome.** Retrospective backtesting on sealed rosters relieves the calendar cost and was previously priced only as "the usual price in hindsight contamination". That price is not payable: every stand-in tower has read about GameStop, LUNA, FTX and COVID, 82 of 83 roster rows have onsets before 2025-01-01, so knowledge-cutoff-based model selection leaves N = 1, and entity scrubbing raises the floor without stripping structural recognisability. The contamination-proof adjudicator already exists in the repository: the **block-label shuffle** (`neff_collapse_wsb.py:275-285`, 300 permutations preserving users, volumes and the graph while destroying block structure) and the **matched-calm arm** generate episodes that never happened and therefore cannot have been memorised, at 300 shuffles across 58 episodes. **Make the shuffle-and-calm arm the primary Substrate-B adjudication and demote the real-outcome arm to a caveated secondary.** It costs nothing new to build and it is the single most valuable design change available here.

**Power, so the probe is not run blind.** Counted from the seven frozen rosters: 83 roster rows, 68 distinct onset dates, 58 distinct real-world episodes, 35 carrying a committed endogenous/exogenous label. Paired one-sided power at 80% gives a minimum detectable effect of **d = 0.42 at N = 35**, and 0.50 under Bonferroni-3 for the three pairwise comparisons a four-arm ordering needs. After K >= 3 attrition and the disagreement gate, plan for an admitted N of **20 to 30**. The empirical precedent is on this exact substrate: `early_warning_powered/result_powered.json` ran semantic-CSD endogenous versus exogenous at AUC 0.600, n = 5/5, Mann-Whitney one-sided p = 0.345. **Substrate B can refute and cannot confirm. A null from it is not evidence of absence, and this document will not read one as such.**

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
- **Mask the loss on observation codes.** The model must **read** observations, not generate them. Prefix-LM style: observation codes are context, loss lands on thought and action tokens. This follows Emu3's understanding stage (arXiv:2409.18869; *Nature* s41586-025-10041-x, phased training with loss weighting so vision tokens do not dominate) and is independently supported by PaliGemma (arXiv:2407.07726), which found that predicting the prefix "clearly reduces average performance." Chameleon Fig. 6b, where instability vanishes once image generation is disabled, is the stability argument for the same choice. **Keep an ablation switch.**
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
proposals:                       # the disagreement that justified generating this at all
  - tower: logic ; predict: "rock resists normal moves" ; action: select_move water_gun
  - tower: code  ; predict: "type chart unknown"        ; action: select_move tackle
  js_divergence: 0.61
thought: enemy Onix is rock and ground; water and grass hit 2x; my Squirtle knows water_gun
action: select_move water_gun
result:
  type: screen
  frame: [<boi> <v_...> <eoi>]   # 90 codes, LOSS-MASKED
  hp_delta: -18                  # RAM-derived; PROBE LABELS ONLY
  yield: 2.31
outcome: water_gun landed super effective; Onix lost 18 HP and the turn ended
                                 # MANDATORY, LOSS-BEARING, and the LAST span of the trace.
                                 # Without it the result frame receives zero gradient (§5.2).
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
  - tower: logic ; predict: endogenous_cascade ; p: 0.72
  - tower: admin ; predict: exogenous_shock    ; p: 0.65
  js_divergence: 0.1017          # bits, recomputed from the two probabilities above.
                                 # Earlier drafts printed 0.58, which those numbers do not give.
                                 # Admission is decided by tau_JS at q = 0.25, not by this value
thought: operator ramp is 13 weeks and N_eff is collapsing past its own block-label shuffle;
         that is the endogenous signature, not a news shock
action: forecast
action_input: {label: endogenous, onset_window: "2021-01-25/2021-02-01"}
result:
  type: adjudication
  source: block_label_shuffle      # PRIMARY adjudicator (§4.3): contamination-proof.
                                   # harvested_outcome is the caveated SECONDARY
  realised: fires_vs_shuffle_true
  yield: 1.04
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

Derived replacements, still arithmetic and still not a measurement: **about 9.1k tok/s at 350M** (band 6.6k to 9.3k for 25% to 35% MFU) and **about 29k tok/s at 125M**. In budget terms that is **about 30 to 42 GPU-hours per 1e9 tokens at 350M**, and about **9.6 GPU-hours per 1e9 tokens at 125M**. Every GPU-hour figure in `F9_PREREGISTRATION.md` §8.1 has been **recomputed** against these replacements rather than scaled from the withdrawn ones, and the F9 total that came out is **1,402.6 GPU-h**. Because the 25% to 35% MFU band is an assumption and not a measurement, that total carries a band of roughly **1,200 to 1,800 GPU-h** until the day-one probe below runs.

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
  bootstrap/   propose.py        # multi-tower proposal + JS-divergence gate
               calibrate_gate.py # tau_JS at q=0.25 on 50k proposals, BEFORE any arm
               adjudicate.py     # environment step + outcome capture
               yield_score.py    # surprisal under the pre-action ensemble distribution
               admit.py          # yield-weighted, accumulating corpus admission
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
| **4** | **Bootstrap loop, Substrate A.** Multi-tower proposal (≥2 distinct open models standing in for towers), JS-divergence gate, emulator adjudication, yield scoring, accumulating admission. Arms A0 to A4 per `F9_PREREGISTRATION.md` §2, including **A4 ungated grounded**, without which the gate effect under grounding is unidentified | **Before any arm runs:** S4 proposer diversity measured, mean pairwise JS >= 0.15 or the experiment is VOID; `tau_JS` calibrated to q = 0.25 on a 50,000-proposal pool. **Then:** admitted trajectories have **mean yield strictly above** the unfiltered control (if not, the run is VOID, not negative); disagreement shrinks over rounds in explored regions |
| **5** | Pretraining. **125M is the powered screen (n = 8 seeds, 5 arms); 350M is the low-n confirmatory replicate (n = 3, 3 arms).** ≤4 epochs, packing, replay, curriculum, observation loss masked | Stable loss (no divergence, QK-norm on); no epoch-5 jump. **The collapse monitor is a reported diagnostic here, not a blocking gate**: firing on the unfiltered self-play arm is the *predicted* result, and halting the experiment on it would halt on a prediction coming true. See §8 |
| **6** | Probes and agent eval | Held-out terms show above-chance grounding **against the control**; super-effective choice above chance. **VideoGameBench Lite is descriptive, not a gate**: frontier models complete 1.6% of Lite, a 350M model scores 0 in every arm, and an endpoint with zero between-arm variance has zero power |
| **7** | **Substrate B, once, at the end.** Re-harvest the observation channel (the dump is not in the tree), write `semantic_variance_z`, fix the `neff` look-ahead leak, then run **one** verdict over 10 to 30 episodes with the block-label shuffle and matched-calm arm as primary adjudicator | Yield-weighted grounded trajectories beat both unfiltered self-play **and** a text-only control, **with the shuffle-and-calm arm adjudicating** and the real-outcome arm reported as a contaminated secondary. If A passes and B fails, the mechanism was learning emulator artifacts. A null here is not evidence of absence at N = 20 to 30 (§4.3) |

**The statistical design is not in this document.** Arms, sample size, seeds, endpoints, effect sizes, test statistics, multiplicity correction, stopping rule and kill conditions are frozen in `logos/F9_PREREGISTRATION.md`, which is the binding artifact. This document specifies what is built; that one specifies what counts as a result.

**The headline ordering the whole spec tests (falsifier F9 in the paper):**

> grounded > disagreement-gated self-play > unfiltered self-play > nothing

If unfiltered self-play matches grounded trajectories at matched token counts, the observation bound is wrong and this line of work should stop. **"Matches" is an equivalence claim and it is expensive**: the 72 to 96 GPU-hour budget the ledger carries buys **0.24 to 0.31 seeds per arm** at 350M across the **five** arms of `F9_PREREGISTRATION.md` §2, and 1.50 to 2.00 seeds per arm at the 125M screen, so n <= 2 either way. At n = 1 there is no within-arm variance estimate and no test statistic of any kind can be computed; at n = 2 the five-contrast MDE is 3.168 sigma, which is 0.158 accuracy points, above the delta = 0.15 the design exists to detect. Either way the experiment can confirm and cannot refute, which is the exact inverse of its purpose. The powered design is **about 1,400 GPU-hours** (1,402.6, `F9_PREREGISTRATION.md` §8.1), which is **$281 to $351** rented at RTX-3090 community-cloud rates or **491 kWh, about EUR 147** of electricity on the owned card. **The 125M screen is what makes it affordable:** a 125M run is 9.579 GPU-h against 61.050 at 350M, so the powered five-arm n = 8 ordering study is 383.1 GPU-h, where the same study run at 350M would be 2,442 GPU-h and would not fit the card. A non-significant result below n = 8 is reported UNDERPOWERED, never as a negative. **And the gate contrast is still not bought:** at n = 8 the tightest declarable equivalence margin is 6.2 accuracy points against a superiority threshold of 7.9, so a true gate effect in that window lands INCONCLUSIVE by construction. Closing it needs n = 13, which is 622.6 GPU-h in Study 1, at 5.0 points, or n = 35, which is 1,676 GPU-h in one study, at 3.0.

---

## 8. Risks

| Risk | Mitigation |
|---|---|
| **Lossy RQ-VAE caps everything.** No HP bars or text means no grounding, and it fails silently | The hard Phase-1 gate. Edge and region weighted loss. Low downsampling. Four-colour frames are in your favour |
| **Model collapse** | Disagreement gating and yield weighting structurally exclude confident self-agreement; corpus accumulates rather than rotates (Gerstgrasser). Explicit `collapse_monitor.py` against arm A0 at the same optimizer step, on three statistics (tail NLL, predictive entropy, representational participation ratio). **The consequence must be arm-qualified, and earlier drafts of this document were not.** Firing on **A3, the grounded arm**, refutes the admission rule, which is the third of the paper's three original claims. Firing on **A1** is *predicted* by the two sources §1 result (3) cites and refutes nothing. Firing on **no arm at all, including A1**, means the monitor is insensitive at this budget and every collapse conclusion from F9 is VOID |
| **Towers stand in for towers.** Two open models at 350M are not 2.8T towers, and the disagreement structure may not transfer | Unavoidable at this budget. State it; do not claim validation at tower scale. The one thing that *is* measured is whether the stand-ins are diverse at all: S4, mean pairwise JS >= 0.15, before any arm runs, or VOID |
| **Substrate B does not scale.** **6 to 8 orders of magnitude short**, not 3, with a hard ceiling of 15 to 39 adjudicable windows on the entire WSB dump and 94 produced in the programme's lifetime | Stated, not solved, and now re-scoped: B is one end-of-training validity probe, not a loop and not a token source (§4.3) |
| **Substrate B episodes are memorised.** 82 of 83 roster onsets predate 2025-01-01; every stand-in tower has read about GameStop, LUNA, FTX and COVID | Knowledge-cutoff model selection leaves N = 1 and entity scrubbing cannot strip structural recognisability. Make the **block-label shuffle and matched-calm arm** the primary adjudicator: those episodes never happened and cannot have been memorised (§4.3) |
| **Look-ahead leak in the `neff` observation operator.** The pre-onset observation is normalised by a full-span mean that includes 22 days of post-onset data | Fix the normalisation to pre-onset only before Phase 7 and re-derive any threshold set against the leaked version. Until then, no forward claim may be made from that operator (§4) |
| **One seed per arm proves nothing.** At the corrected throughput the 72 to 96 GPU-h budget `GAPS.md` used to assign F9 buys 1.18 to 1.57 runs at 350M across **five** arms, which is 0.24 to 0.31 seeds per arm, and 7.52 to 10.02 runs at the 125M screen, which is 1.50 to 2.00 | n = 8 at 125M as the powered screen, n = 3 at 350M confirmatory, a blind loss-spike outlier rule detected from the loss curve alone, and a 20% replacement reserve, which drops P(at least one of five arms corrupted) from 0.672 to 0.051. About **1,400 GPU-hours** total (1,402.6), of which the powered screen is 383.1 |
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

**Does not settle:** whether it transfers to 2.8T towers; whether the yield rate scales to the 10¹³–10¹⁴ tokens the paper's Proposition 2 needs; whether the effect survives when the environment is code execution, a wet lab, or a market rather than an emulator; and whether the tower-diversity claim of §1.1 holds when the towers are actually frontier-scale. Those are the real questions and this answers none of them.

**Specifically does not settle, and this is new since the round-2 audit:** anything about Substrate B beyond a single directional probe at N = 20 to 30 with a minimum detectable effect around 0.42 sigma, which can refute and cannot confirm; and the gate contrast under grounding (A3 versus A4), which is the claim §1.1 says we would most like tested and is the contrast this design is **worst** powered to detect. That asymmetry is disclosed here and in `F9_PREREGISTRATION.md` §10 in advance, rather than discovered after the numbers land.

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
