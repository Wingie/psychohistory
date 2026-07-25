# logos-harness — agentic bootstrap pretraining past the token wall

**Development specification.** Codename `logos-harness`. Status: **SPEC, unbuilt.**
Role in the LOGOS programme: **the pretraining strategy that takes over once human text data runs out.**
Companion to `../logos.tex` §"Beyond the data wall".

---

## 0. The idea

Proposition 2 of `logos.tex` says the binding constraint at 10T is **unique high-quality tokens**, not training FLOPs. Sparsity removed the compute constraint. Tower decomposition bought corpus-overlap headroom. 4-bit serving handled memory. **Nothing in the architecture manufactures tokens**, and past some point of LOGOS development there is no more human text to buy.

The proposal:

> **The towers talk to each other, act on the world, and the world answers.**
> Inter-tower agentic dialogue generates candidate trajectories; a real-world observation channel adjudicates them; the adjudicated trajectories become new training tokens. The ensemble incrementally improves itself when human text is unavailable.

Two things make this a real proposal rather than perpetual motion:

1. **The environment must be able to contradict the towers.** Towers arguing among themselves generate no new information about the world (§1). The observation channel is the only source of new bits, and it must be a channel the ensemble cannot fake.
2. **The yield is measurable.** Not every trajectory is worth training on. §1.3 gives a computable priority — inter-tower disagreement resolved by observation — that ranks trajectories by how much the ensemble actually learned.

We test the mechanism on **two substrates**, chosen because they fail differently:

| | **Substrate A — Pokémon** | **Substrate B — psychohistory** |
|---|---|---|
| Environment | Game Boy emulator (PyBoy) | Real social/economic systems |
| Observation | Rendered frames, RAM state | Reddit / GitHub / Wikipedia / market series |
| Adjudicator | Game mechanics — exact, instant, free | Reality — noisy, delayed, expensive |
| Ground truth | RAM (types, HP, moves) | Did the cascade actually happen? |
| Cost per trajectory | Milliseconds | Weeks to months |
| What it tests | **Does the mechanism work at all?** | **Does it work when the world is the adjudicator?** |
| Hardware | One RTX 3090 | One RTX 3090 + this repo's existing harvest pipeline |

Pokémon is the cheap decisive test. Psychohistory is the real one — and it is already half-built in this repository (`../validation/`), with pre-registered falsifiers, harvest scripts, and a forward engine whose own blocked tests need exactly this kind of trajectory generator.

**Secondary payoff, and it is not small:** this puts the RQ-VAE codebook in the position `ARCHITECTURE_REVIEW.md` F-06 says it belongs — as an **observation tokenizer in a shared vocabulary** — rather than in the hidden-state serving path where the source draft misplaced it. The mechanism the paper had to relocate is the mechanism this spec is built on.

---

## 1. The bootstrap principle

### 1.1 Why ungrounded self-play is the null result, not the method

The known result is negative. Shumailov et al. (*Nature* 631:755–759, 2024) show that recursively training a generative model on its own output causes **model collapse**: irreversible defects in which the tails of the original distribution disappear and output diversity degrades. Recursive self-training collapse has since been reproduced specifically in code models (arXiv:2606.28438).

So "towers generate data, we train on it" is, by default, the thing that is known to fail. Any bootstrap proposal has to say precisely what makes it different.

### 1.2 The information argument

**Conjecture (ours, Tier C).** Let the ensemble's joint knowledge be a distribution `P_M` over world-states. Inter-tower dialogue applies only functions of `P_M`: rearrangement, compression, deduction, chain-of-thought elaboration. By a data-processing argument, no such function increases mutual information with the world beyond what `P_M` already carries. Deduction can make implicit knowledge explicit and *usable* — which is genuinely valuable, and is what reasoning-distillation and SPICE-style corpus self-play (arXiv:2510.24684) exploit — but it cannot introduce a bit the ensemble did not have.

**Every genuinely new bit must enter through an observation channel.** Therefore:

> The value of a bootstrap harness scales with the **entropy of the environment conditional on the model**, not with the volume of inter-tower dialogue.

This has a sharp design consequence, and it is the opposite of the intuitive one: **do not seek environments the towers handle well.** Seek environments where they are *wrong*, because surprisal is the yield.

### 1.3 The yield metric and the generation algorithm

Both quantities below are computable without human labels, which is the point.

**Yield of a trajectory** = the surprisal of the observation under the ensemble's own predictive distribution before it acted:

```
yield(τ) = −log P_M(o_observed | context, action)
```

A trajectory where the towers agreed and were right has yield ≈ 0 — it is pure self-confirmation, and training on it is exactly the Shumailov collapse path. A trajectory where towers **disagreed** and the environment **adjudicated** is high-yield.

**Generation algorithm — disagreement-seeking:**

1. **Propose.** Present the current observation to ≥2 towers independently. Each emits a prediction and an action, with reasoning.
2. **Score disagreement.** Compute divergence between tower predictive distributions (JS divergence over the action/outcome space). Low disagreement → discard the candidate; the ensemble already agrees and nothing will be learned.
3. **Act.** Execute the action in the environment.
4. **Observe and adjudicate.** The environment returns the outcome. It settles the disagreement.
5. **Score yield.** Compute the surprisal above.
6. **Admit or discard.** Retain the trajectory for training weighted by yield. Discard the low-surprisal tail.
7. **Retrain incrementally**, then repeat. Disagreement should shrink where the environment has been explored, pushing generation toward the frontier automatically.

Steps 2 and 6 are the anti-collapse mechanism: the harness **structurally cannot** train on its own confident agreement, which is the distribution-narrowing dynamic Shumailov identifies.

**This is closest in spirit to** verifiable-environment RL (EvoEnv, arXiv:2605.14392, whose thesis is that stable self-improvement requires environments whose difficulty stays structurally beyond the model's reach) and RLVR generally — with the difference that here the target is **corpus generation for pretraining**, not policy improvement, and the participants are heterogeneous frontier-scale towers rather than one model self-playing.

### 1.4 The honest caveat

§1.2 is a conjecture stated in information-theoretic language, not a theorem. The data-processing inequality applies cleanly to a fixed channel; a tower ensemble doing multi-step reasoning with tool access is not a fixed channel, and "the model already has the bit but cannot access it" is doing real work in the argument that we have not formalised. Treat §1.2 as a **design principle that makes a testable prediction** — that yield-weighted trajectory selection outperforms unweighted self-play, and that both are beaten by grounded trajectories — rather than as a proof. That prediction is falsifier **F9** (`../logos.tex`).

---

## 2. Substrate A — Pokémon (the cheap decisive test)

Fully observable, exact ground truth in RAM, adjudication in milliseconds, and — critically — **the semantics being tested are printed on screen**, so the observation channel's fidelity is verifiable pixel by pixel.

### 2.1 Harnesses

Two exist and both centre on PyBoy. **Use both, for different jobs.**

**PufferLib Pokémon Red** — `PufferAI/pokegym`, `drubinstein/pokemonred_puffer`, descended from `PWhiddy/PokemonRedExperiments`, MIT. Cite Suarez et al., arXiv:2406.12905. Gymnasium over PyBoy with heavy performance engineering; several thousand steps/sec headless with aggressive frameskip. Full RAM instrumentation (party, HP, badges, map ID, coordinates), savestates via `save_state()`/`load_state()`. **Role: trajectory generation, curriculum, RAM ground truth.**

**VideoGameBench** — Zhang, Griffiths, Narasimhan, Press (Princeton), arXiv:2505.18134, MIT. `main.py --game pokemon_red --model gpt-4o`. Game Boy logic in `src/emulators/gba/`, base interface in `src/emulators/interface_base.py`, ReAct agent in `src/llm/vgagent.py`, LiteLLM routing. **Lite mode pauses the emulator during inference**, decoupling model latency from the game clock — essential for a slow local model. **Raw-frames-only ruleset**, no RAM overlays. **Role: the headline agent eval, reported in the same terms as frontier VLMs.** The benchmark is hard; frontier models score very low under the strict ruleset.

Also useful: `NousResearch/pokemon-agent` (headless PyBoy + JSONL event logging, RAM walkability maps, A*, frames from `screen.ndarray` with no display server); `drubinstein/pokerl` docs on reading RAM via the PRET symbol table (`wPartyMon1HP` at `0xD16C`, `wPartyMon1Type1` at `0xD170`) and assembly-label injection for events with no RAM flag; canonical RAM map at `datacrystal.tcrf.net`.

**A confusion to avoid.** The NeurIPS 2025 **PokéAgent Challenge** (Karten et al., arXiv:2603.15563 — Battling Track on Showdown with 20M+ trajectories, Speedrunning Track on Emerald, 100+ teams) is **not** Red/Blue frame logging. Cite it only for "Pokémon as an AI benchmark."

### 2.2 The observation tokenizer (RQ-VAE)

Game Boy is 160×144, 20×18 tiles of 8×8, DMG palette of 4 shades. **Unusually easy tokenizer target — this is the entire reason the vision side is tractable at this scale.**

Base: `lucidrains/vector-quantize-pytorch` `ResidualVQ` (MIT) — shared codebooks, stochastic code sampling (the two RQ-VAE modifications from Lee et al. 2022), EMA, `kmeans_init=True`, quantizer dropout, dead-code handling. `LFQ` (MAGVIT-v2, Yu et al. ICLR 2024) and `FSQ` are alternatives.

| Knob | Start at | Why |
|---|---|---|
| Input | DMG 4-colour → single luminance channel | Makes the encoder's job trivial |
| Downsampling | factor 16 (four stride-2 blocks): 160×144 → **10×9 = 90 positions** | Lands in the 64–128 target |
| Residual levels | **3** (TIGER uses 3–4) | Coarse-to-fine |
| Codebook | 1,024–2,048/level; grow only on failure | DMG diversity is tiny |
| Update | EMA + dead-code reinit | More stable than gradient updates for VQ |
| Losses | L1/L2 + commitment + **edge-weighted** + **region weighting on the HP-bar and text-box rectangles** | Fixed pixel rectangles on Game Boy; the semantically critical areas |

**Resolve in Phase 1:** tokens per frame = positions × levels *unless* residual levels are collapsed into one composite token per position. Prefer **~64 positions × 2–3 levels**, or collapse per position. This drives sequence length and the observation/text ratio and cannot be deferred.

**THE GATE.** Before any LM training, on held-out frames: **HP-bar within 1px · menu/dialog text legible (OCR or human panel) · sprite identity correct · codebook utilisation >95%.** If any fail: more levels, bigger codebook, less downsampling, or restrict to battle screens. **Do not proceed on a failed gate.** The held-out vocabulary is grounded through on-screen battle text — a tokenizer that blurs it destroys the experiment *silently*.

### 2.3 The held-out vocabulary experiment

This is how Substrate A proves grounding actually happened rather than being inferred from text co-occurrence.

Scrub a curated term set from the **entire** text stream — essays, tool results, analyses — so meaning can only be acquired from grounded trajectories.

| Class | Held out | Matched control (kept in text) |
|---|---|---|
| Types | `water`, `rock`, `grass`, `electric`, `ground` | `fire`, `normal` |
| Moves | `water_gun`, `thunder_shock`, `vine_whip`, `ember` | `tackle`, `scratch` |
| Effectiveness | `super effective`, `not very effective` | — |

**The control set is not optional.** It is what makes a null result interpretable rather than merely disappointing.

RAM-derived type/move/HP state labels **probe targets only** — never model input in the held-out condition.

**Probes:** (1) *Interpretability* — nearest image-code embeddings to each held-out word embedding by cosine; success = held-out type/move embeddings sit nearest the codes of frames where those types/moves appear (mirrors TIGER, arXiv:2305.05065, where RQ-VAE codes captured category structure). (2) *Behavioural* — does the model pick super-effective moves in held-out matchups above chance, versus the text-supported controls?

---

## 3. Substrate B — psychohistory (the real-world test)

Substrate A proves the mechanism. Substrate B asks whether it survives when the adjudicator is reality: noisy, delayed, partially observable, and expensive.

**This repository already contains the environment.** `../validation/` has harvest scripts for Reddit (WSB, AskEconomics, location subs), GitHub, and Wikipedia; pre-registered falsifiers with frozen thresholds; blind Louvain community detection; semantic critical-slowing-down detectors; and an EnKF forward engine. What it does not have is a trajectory generator — and the companion paper's blocked falsifiers (smooth-regime skill, fixed-point reliability, Lucas invariance, regime occupancy) are blocked on exactly that.

### 3.1 The loop

1. **Observation.** A block's state at time `t`: mention-density series, embedding-variance (belief dispersion), community partition, operator-concentration (HHI/Gini). The repo's existing observation operators.
2. **Tower dialogue.** Towers propose competing readings — *is this endogenous or exogenous? is `N_eff` collapsing? is there an operator ramp?* — with explicit reasoning and a forecast at horizon `h`.
3. **Disagreement scoring.** JS divergence across tower forecasts. Agreement → discard.
4. **Adjudication by reality.** Wait out the horizon. Harvest what happened. **The observation channel is the world and it cannot be faked by the ensemble** — which is precisely the property §1.2 requires.
5. **Yield.** Surprisal of the realised outcome under the pre-registered ensemble forecast.
6. **Admit.** High-yield disagreement-resolved trajectories become training tokens.

### 3.2 Why this substrate is the honest one

- **The adjudicator is genuinely external.** In Pokémon the environment is a deterministic program the ensemble could in principle learn to simulate, at which point yield → 0 legitimately. Social reality cannot be simulated away, which is the psychohistory paper's own central negative result (out-of-model agents, misspecification against which more data does not help).
- **It is already pre-registered.** The repo's discipline — frozen thresholds, sealed rosters, binomial rules committed before harvest — is exactly the protocol a bootstrap harness needs to avoid grading its own homework.
- **Reflexivity is the hard case, and it is the interesting one.** A LOGOS-class ensemble forecasting a social system it is also deployed inside is the mean-field-game fixed-point problem the companion paper formalises. This substrate tests bootstrap generation *in the presence of the reflexivity failure mode*, which Pokémon cannot.

### 3.3 The cost problem, stated plainly

Adjudication takes weeks to months. A generator that yields a few thousand high-quality trajectories per quarter is not a pretraining corpus — it is three orders of magnitude short of relevance to a 2.8T tower. **Substrate B does not scale as a token source at this stage and we should not pretend otherwise.**

What it *is*: the validity check. If yield-weighted grounded trajectories help on Pokémon but not when reality adjudicates, the mechanism is learning emulator quirks, and the whole bootstrap story is worth much less than it looks. Run Substrate B for **validity**, Substrate A for **volume**, and be explicit about which is which.

Retrospective backtesting partially rescues the cost problem — historical episodes with known outcomes give instant adjudication — at the price of the usual hindsight contamination. The repo's existing pre-registration protocol is the mitigation, and it is imperfect.

---

## 4. Model, training, and the trace schema

Shared across both substrates. One grammar, so sequence packing sees a single format.

### 4.1 Model

Decoder-only, RMSNorm, RoPE, SwiGLU, **QK-norm**, no bias.

| | 125M (debug) | 350M (main) |
|---|---|---|
| d_model / layers / heads / head_dim | 768 / 12 / 12 / 64 | 1024 / 24 / 16 / 64 |
| context | 2048 | 2048 |

QK-norm is not optional: Chameleon (arXiv:2405.09818) found it essential for mixed-modal stability — without it, loss diverges after ~20% of an epoch at 7B.

**Vocabulary:** text 8k–16k (mined) + observation codes 2k–8k + specials (BOI/EOI, role delimiters, held-out mask) ≈ **10k–24k**. Small vocab keeps the embedding table cheap, which matters at 24 GB.

**Observation-code embedding init:** from the RQ-VAE codebook vectors via a learned linear projection (codebook dim → d_model); if codes are factorised, use MAGVIT-v2's token-factorisation pattern (embed each sub-codebook, sum). Reuse the existing mean-of-subtoken init for mined text tokens.

### 4.2 Early fusion, and the loss decision

- **Delimiters.** Wrap every observation-code span in BOI/EOI specials, as Chameleon does.
- **Mask the loss on observation codes.** The model must **read** observations, not generate them. Prefix-LM style: observation codes are context, loss lands on thought + action tokens. This is the Emu3 understanding-stage pattern (arXiv:2409.18869; *Nature* s41586-025-10041-x — phased training with loss weighting so vision tokens do not dominate), independently supported by PaliGemma (arXiv:2407.07726), which found predicting the prefix "clearly reduces average performance." Chameleon Fig. 6b — instability vanishes when image generation is disabled — is the stability argument for the same choice. **Keep an ablation switch.**
- **Intra-observation bidirectional attention** (optional, v2): Transfusion (arXiv:2408.11039) showed it significantly boosts performance. Causal across the sequence, bidirectional within one observation's span.
- **Chain-of-thought must be load-bearing.** Loss is on thought + action; if the action were trivially decodable from the observation alone, the reasoning span would never be learned. **Enforce by data design, not by the loss** — and in the bootstrap loop this is automatic, because disagreement-seeking only admits trajectories where the answer was *not* obvious.

### 4.3 Trace schema

Same keys throughout; only the `observation` payload type differs.

**Substrate A (Pokémon):**
```yaml
episode: pokemon_red_battle_0142
step: 17
observation:
  type: screen
  frame: [<boi> <v_412> <v_87> <v_1003> ... <eoi>]   # RQ-VAE codes, LOSS-MASKED
proposals:                       # the disagreement that justified generating this trajectory
  - tower: logic    ; predict: "rock resists normal moves"; action: select_move water_gun
  - tower: code     ; predict: "type chart unknown"       ; action: select_move tackle
  js_divergence: 0.61
thought: enemy Onix is rock/ground; water and grass hit 2x; my Squirtle knows water_gun
action: select_move water_gun
result:
  type: screen
  frame: [<boi> <v_...> <eoi>]
  hp_delta: -18                  # RAM-derived; PROBE LABELS ONLY
  yield: 2.31                    # −log P_M(observed | context, action)
```

**Substrate B (psychohistory):**
```yaml
episode: wsb_cascade_2021w04
horizon_weeks: 3
observation:
  type: block_state
  block: r/wallstreetbets
  neff: 1.42
  semantic_variance_z: +2.1
  operator_hhi: 0.31
proposals:
  - tower: logic  ; predict: endogenous_cascade ; p: 0.72
  - tower: admin  ; predict: exogenous_shock    ; p: 0.65
  js_divergence: 0.58
thought: operator ramp is 13 weeks and N_eff is collapsing past its own block-label shuffle;
         that is the endogenous signature, not a news shock
action: forecast
action_input: {label: endogenous, onset_window: "2021-01-25/2021-02-01"}
result:
  type: adjudication
  source: harvested_outcome
  realised: endogenous_cascade_confirmed
  yield: 1.04
```

**Text-harness variant** (agentic OSINT/PDF, for the language-competence half of the corpus) uses the same keys with `observation.type: tool_result`, and the four-variant fan-out — **hit / near-miss / misleading-but-plausible / multi-hop** — following AgentFounder (arXiv:2509.13310) and the phi "textbooks" methodology, generated locally by a Qwen3-class MoE on the same GPU at zero API cost. Apply the held-out filter as a **hard** post-processing step (regex *and* tokenizer-level scrub).

### 4.4 Training

**Trainer:** a modded-nanoGPT derivative (`KellerJordan/modded-nanogpt`; `Deveraux-Parker/nanoGPT_1GPU_SPEEDRUN` for the single-consumer-GPU adaptation). `litgpt` is a viable fallback.

**Optimizer:** Muon on 2D matrices + AdamW on embeddings/head/norms/1D. Muon uses one momentum buffer instead of two, saving ~4 B/param on 2D matrices (~1 GB at 350M), reported ~35% faster to a target loss. Fallback: plain AdamW (β 0.9/0.95, wd 0.1, clip 1.0, cosine/trapezoidal, warmup).

**Precision:** bf16. FlashAttention-2 works on Ampere; **FP8 does not** (GA10x tensor cores: TF32/BF16/FP16/INT8/INT4 only).

**Memory at 350M/2048/bf16/24 GB:** ~5.6 GB fixed for AdamW state (16 B/param mixed) + activations. Micro-batch ~4 without checkpointing; 8 may need it. Gradient accumulation to ~256k–500k tokens/step.

**Wall clock — planning numbers, not measurements.** ~18k–30k tok/s at 350M/2048 → ~9–14 h per 1B tokens, ~1 day for 2B, ~3–4 days for a 4-epoch pass over 2B. 125M: ~45k–90k tok/s. **These are interpolations from measured 4090 / A30 / L20 runs, not a first-party 3090 log at these sizes.** Run a forward+backward probe with `torch.cuda.max_memory_allocated` on day one and set the schedule from the measurement.

**Data schedule:** ≤4 epochs (Muennighoff et al., arXiv:2305.16264, NeurIPS 2023: up to 4 epochs of repeated data yields near-negligible loss change vs unique data, validated across 400+ runs, 10M–9B params, up to 900B tokens). Watch for the epoch-5 jump. **20–30% text replay whenever observation data is mixed in**; cap the observation stream at 15–30% of tokens.

**Packing:** multiple traces per 2048-token sequence with document boundaries; FlexAttention block masks to prevent cross-document attention.

---

## 5. Repository layout

```
logos-harness/
  configs/     rqvae.yaml  tokenizer.yaml  model_{125m,350m}.yaml  train.yaml
               heldout_vocab.yaml  bootstrap.yaml        # disagreement + yield thresholds
  data/        raw/  frames/  traces_text/  traces_game/  traces_psycho/  packed/
  bootstrap/   propose.py        # multi-tower proposal + JS-divergence scoring
               adjudicate.py     # environment step + outcome capture
               yield_score.py    # surprisal under the pre-action ensemble distribution
               admit.py          # yield-weighted corpus admission
  substrate_a/ pokegym_dump.py  savestates/  vgbench_eval.py
  substrate_b/ harvest_adapter.py   # thin wrapper over ../validation/**/harvest_*.py
               block_state.py       # observation operators -> block_state payload
  rqvae/       model.py  train_rqvae.py  recon_gate.py  tokenize_frames.py
  tokenizer/   mine_vocab.py  build_tokenizer.py  embed_init.py
  schema/      compiler.py  validate.py
  corpus/      generate_text_traces.py
  train/       train.py  pack.py
  eval/        grounding_probe.py  behavioral_probe.py  agent_eval.py  collapse_monitor.py
```

---

## 6. Phases and gates

| Phase | Work | **Gate** |
|---|---|---|
| **0** | Substrate A harness: headless PyBoy, scripted + random-walk dump of ≥100k `(frame, action, RAM-state)` tuples, savestates at Pallet Town / first battle / first gym | 100k+ frames dumped headlessly; savestates load; RAM state parsed and **aligned to frames**; **measured** disk-write throughput recorded (published steps/sec are rollout figures and do not apply to a frame-dump, which is I/O-bound) |
| **1** | RQ-VAE observation tokenizer; resolve flatten-vs-collapse | **HP-bar within 1px · text legible · sprite identity correct · codebook utilisation >95%.** No LM training until this passes |
| **2** | Tokenizer mining, joint vocab, YAML→token-id compiler, held-out leak validator | Round-trip lossless both variants; **zero held-out terms in the text stream**; embedding init sane |
| **3** | Text corpus, 4-variant fan-out, quality + leak filtering | Token count reached; variant distribution as designed; leak scan clean; human spot-check passes |
| **4** | **Bootstrap loop, Substrate A.** Multi-tower proposal (use ≥2 distinct open models as stand-in towers), JS-divergence gating, emulator adjudication, yield scoring, admission | Admitted trajectories have **mean yield strictly above** an unfiltered-self-play control; disagreement shrinks over rounds where the environment has been explored |
| **5** | Pretraining: 125M debug end-to-end, then 350M. ≤4 epochs, packing, replay, curriculum, observation-loss masked | Stable loss (no divergence, QK-norm on); no epoch-5 jump; **collapse monitor** shows no tail-narrowing vs the text-only baseline |
| **6** | Probes + agent eval | Held-out terms show above-chance grounding **vs control**; super-effective choice above chance; agent clears early VideoGameBench Lite checkpoints |
| **7** | **Substrate B.** Wire `../validation/` harvest scripts as the observation channel; run the loop retrospectively on sealed rosters, then forward | Yield-weighted grounded trajectories beat both unfiltered self-play **and** a text-only control, **with reality as adjudicator**. If A passes and B fails, the mechanism was learning emulator quirks |

---

## 7. Risks

| Risk | Mitigation |
|---|---|
| **Model collapse** — the known failure mode for training on self-generated data (Shumailov, *Nature* 2024) | Disagreement gating + yield weighting **structurally exclude** confident self-agreement, which is the distribution-narrowing path. Plus an explicit `collapse_monitor.py` tracking output-distribution tails against a text-only baseline. **If the monitor fires, the mechanism is refuted** |
| **Lossy RQ-VAE caps everything.** No HP bars / text → no grounding, and it fails silently | The hard Phase-1 gate. Edge/region-weighted loss. Low downsampling. DMG's 4 colours are in your favour |
| **Substrate B does not scale.** Adjudication takes weeks; a few thousand trajectories/quarter is 3 orders short | **Stated as a known limit, not solved.** B is the validity check; A is the volume test. Retrospective backtesting on sealed rosters partially rescues it, at the cost of hindsight contamination |
| **The information argument is a conjecture, not a theorem** (§1.4) | It makes a testable prediction (F9): yield-weighted > unweighted self-play, and grounded > both. Falsify it directly |
| Held-out term never learnable — co-occurrence too sparse | Over-represent battle frames; verify the tokenizer preserves on-screen text; **keep the control set so a null is interpretable** |
| Grammar not learnable from structured traces alone | 70–85% text stream includes prose, not just tool calls. BabyLM (arXiv:2504.08165) shows 100M-word natural-text budgets suffice for grammar |
| Observation codes swamp or destabilise training | Mask observation loss; cap at 15–30%; 20–30% text replay; QK-norm + z-loss |
| 3090 memory / time overrun | Micro-batch 4 + grad accumulation; Muon; 125M debug first; ≤4 epochs |
| **Throughput estimates are scaled, not measured on a 3090** | Day-one probe before committing to a schedule |
| **Towers stand in for towers.** At 350M with two open models, these are not 2.8T towers and the disagreement structure may not transfer | Unavoidable at this budget. State it; do not claim the mechanism is validated at tower scale |
| PokéAgent confusion | Showdown + Emerald, not Red/Blue frame logging. Citation only |
| ROM legality | ROMs are in none of these repos and must be supplied by the user. Code is MIT; the games are not |

---

## 8. What this settles, and what it does not

**Settles:** whether disagreement-gated, environment-adjudicated trajectory generation produces training data that (a) beats unfiltered self-play, (b) beats a matched text-only control, and (c) does not trigger model collapse — on two substrates that fail differently, with a control set that makes a null interpretable.

**Does not settle:** whether it transfers to 2.8T towers; whether the yield rate scales to the 10¹³–10¹⁴ tokens Proposition 2 needs; whether the effect survives when the environment is code execution, wet-lab protocol, or a market rather than an emulator; and whether the information argument of §1.2 is actually true rather than merely useful. Those are the real questions and this answers none of them.

**Why run it anyway:** it is the cheapest experiment that can return a **decisive negative** on the LOGOS data strategy. If disagreement-gated grounded trajectories do not beat a text control at 350M on the easiest imaginable grounding substrate — 4 colours, 160×144, with the exact semantics under test printed on screen — then the plan past the token wall is repetition plus synthesis, Proposition 2's headroom is all there is, and `logos.tex` should say so plainly. A cheap decisive negative on a research bet is worth more than an expensive confirmation of a mechanism.

---

## 9. References

**Bootstrap / self-play / collapse.** Shumailov, Shumaylov, Zhao, Papernot, Anderson, Gal — AI models collapse when trained on recursively generated data, *Nature* 631:755–759, 2024. Recursive self-training collapse in code LLMs — arXiv:2606.28438. SPICE: Self-Play In Corpus Environments Improves Reasoning — arXiv:2510.24684. EvoEnv / verifiable environment synthesis — arXiv:2605.14392. AgentFounder — arXiv:2509.13310.

**Harnesses.** VideoGameBench — Zhang, Griffiths, Narasimhan, Press, arXiv:2505.18134, `alexzhang13/videogamebench` (MIT). PufferLib — Suarez et al., arXiv:2406.12905, `PufferAI/pokegym`, `drubinstein/pokemonred_puffer`, `PWhiddy/PokemonRedExperiments`. PokéAgent Challenge — Karten et al., arXiv:2603.15563 (citation only). Pokémon Red via RL — Pleines et al., arXiv:2502.19920. `NousResearch/pokemon-agent`. RAM map: datacrystal.tcrf.net.

**Tokenizers / VQ.** `lucidrains/vector-quantize-pytorch` (MIT). TIGER — Rajput et al., arXiv:2305.05065, NeurIPS 2023. Lee et al. 2022, residual quantization. MAGVIT-v2 / LFQ — Yu et al., ICLR 2024. Open-MAGVIT2 — arXiv:2409.04410.

**Early fusion.** Chameleon — arXiv:2405.09818. Emu3 — arXiv:2409.18869; *Nature* s41586-025-10041-x. Transfusion — arXiv:2408.11039. PaliGemma — arXiv:2407.07726.

**Training / data.** `KellerJordan/modded-nanogpt`. `Deveraux-Parker/nanoGPT_1GPU_SPEEDRUN`. Muon — kellerjordan.github.io/posts/muon. Data-constrained scaling — Muennighoff et al., arXiv:2305.16264, NeurIPS 2023. BabyLM — arXiv:2504.08165, arXiv:2412.05149. phi-1 — arXiv:2306.11644. phi-1.5 — arXiv:2309.05463.

**Substrate B.** W. Sharon, *Conditions for Predictable Social Dynamics*, draft v0.5 — and this repository's `../validation/` suite.
