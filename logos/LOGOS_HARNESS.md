# logos-harness

**Implementation specification for the loop described in `../logos.tex` §12, "The observation bound."**
Status: **SPEC, unbuilt.** Hardware: one RTX 3090 (24 GB).

---

## 0. What this is

The paper's argument ends at a limit that scale does not move. Sparsity removes the compute constraint, tower decomposition raises the data ceiling, four-bit serving handles memory, and after all of that the system is still capped by how fast something outside it can tell it that it is wrong. This directory specifies the cheapest experiment that can test that claim and return a decisive negative.

The loop:

> Towers disagree. They act on an environment. The environment settles the disagreement. Trajectories are kept in proportion to how much the ensemble was surprised, and they accumulate rather than replace.

Two environments, chosen because they fail differently:

| | **Substrate A: Pokémon** | **Substrate B: psychohistory** |
|---|---|---|
| Environment | Game Boy emulator (PyBoy) | Real social and economic systems |
| Observation | Rendered frames, RAM state | Reddit / GitHub / Wikipedia / market series |
| Adjudicator | Game mechanics: exact, instant, free | Reality: noisy, delayed, expensive |
| Cost per trajectory | Milliseconds | Weeks to months |
| Can the model internalise it? | **Yes, eventually.** It is a deterministic program | **No.** This is the whole point |
| Role | **Volume** | **Validity** |

---

## 1. The theory, and whose it is

Four separate literatures converge on one conclusion. **None of these results is ours**, and an earlier draft of this document presented the synthesis as an original conjecture, which was wrong. What follows is the corrected attribution.

**1. Debate among agents with the same information is a martingale.** Under a Dirichlet-Categorical belief model, standard multi-agent debate induces a martingale over agents' belief in the correct answer: expected correctness does not improve over rounds when agents receive identical inputs (Choi et al., arXiv:2601.19921, 2026). Deliberation among parties who already know the same things reinforces a shared prior. Empirically, multi-agent debate does not reliably beat self-consistency ("Should we be going MAD?", ICML 2024), and swapping specialised agents for identical ones costs several points of accuracy.

**Consequence for this spec:** the towers must be informatively different, or the loop is provably worthless. Substrate design is secondary to participant diversity.

**2. RLVR sharpens rather than expands.** Probing the reasoning boundary with pass@k at large k, base models catch up with their RL-trained versions across every benchmark and model family tested, and eventually surpass them (Yue et al., NeurIPS 2025, Best Paper Runner-up). RLVR improves sampling efficiency; it does not enlarge the set of solvable problems.

**Consequence:** you cannot get past the wall by running RL harder on a fixed problem set. The problems have to come from somewhere.

**3. Self-training without grounding provably degenerates.** Formalised as a discrete-time dynamical system, recursive self-training has two failure modes: entropy decay, where finite sampling monotonically destroys distributional diversity, and variance amplification, where the absence of persistent grounding produces drift by a random walk. If the fraction of exogenous, externally grounded signal vanishes asymptotically, degeneration follows (Zenil et al., arXiv:2601.05280, 2026).

Model collapse (Shumailov et al., *Nature* 631:755–759, 2024) is the empirical face of this. **It is not automatic**, and the first draft of this document overstated it: collapse is established when synthetic data *replaces* real data, and accumulating real and synthetic together avoids it (Gerstgrasser et al., arXiv:2404.01413, 2024).

**Consequence:** the exogenous-signal fraction is the design variable, and the corpus must accumulate, not rotate.

**4. Self-play works when something external checks the answer.** The strongest zero-human-data result trains a model to propose and solve its own tasks, reaching state-of-the-art coding and mathematical reasoning with no external data, using **a code executor** to validate proposed tasks and verify answers (Absolute Zero, arXiv:2505.03335, NeurIPS 2025).

**Consequence:** the executor is not an implementation detail, it is the entire source of correction. And a code executor is a deterministic program, which is why Substrate B exists.

Silver and Sutton ("Welcome to the Era of Experience", DeepMind 2025) frame the destination: experiential data will come to dwarf human data. The four results above say what the limiting resource is on the way there.

### 1.1 What is actually ours

Three things, all Tier C, all in `../logos.tex` §12:

1. **The bound is the answer to the paper's own question.** Every other constraint on a 10T system gets lifted in §§2–11; this one is left standing.
2. **The tower architecture supplies the diversity the martingale theorem requires.** Result (1) says improvement needs participants who know different things. Branch-Adapt-Route produces towers trained on different corpora under different objectives with different alignment histories. A single self-playing model cannot manufacture that. The property chosen for update economics turns out to be the precondition for learning from disagreement. **This is the claim we would most like tested.**
3. **The admission rule.** If exogenous signal is scarce, keep trajectories in proportion to how much of it they carry.

---

## 2. The loop

**Yield** of a trajectory τ is the surprisal of the observed outcome under the ensemble's own prediction before it acted:

```
yield(τ) = −log P_M(o_observed | context, action)
```

Agreed-and-right scores near zero: self-confirmation, which is the entropy-decay path of result (3). Disagreed-and-adjudicated scores high.

1. **Propose.** Show an observation to ≥2 towers independently. Each returns a prediction, an action, and reasoning.
2. **Gate on disagreement.** JS divergence between tower predictive distributions. Below threshold, discard: result (1) says nothing will be learned.
3. **Act** on the environment.
4. **Adjudicate.** The environment returns the outcome.
5. **Score yield.**
6. **Admit** weighted by yield, and **accumulate** rather than replace (result 3 / Gerstgrasser).
7. **Retrain incrementally, repeat.** Disagreement shrinks where the environment has been explored, pushing generation toward the frontier without being told to.

Steps 2 and 6 are the anti-collapse mechanism, and they are structural rather than heuristic: the loop cannot train on its own confident agreement.

**Both gates are computable without human labels.** That is what makes the thing runnable.

---

## 3. Substrate A: Pokémon

Fully observable, exact ground truth in RAM, adjudication in milliseconds, and the semantics under test are printed on screen, so observation fidelity is checkable pixel by pixel.

### 3.1 Harnesses

Two exist, both built on PyBoy. Use both, for different jobs.

**PufferLib Pokémon Red** (`PufferAI/pokegym`, `drubinstein/pokemonred_puffer`, from `PWhiddy/PokemonRedExperiments`, MIT; cite Suarez et al., arXiv:2406.12905). Gymnasium over PyBoy with heavy performance work: several thousand steps/sec headless at aggressive frameskip. Full RAM instrumentation (party, HP, badges, map ID, coordinates), savestates via `save_state()`/`load_state()`. **Role: trajectory generation, curriculum, ground truth.**

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

**Resolve in Phase 1:** tokens per frame = positions × levels, unless residual levels collapse into one composite token per position. Prefer **~64 positions × 2–3 levels**, or collapse per position. This sets sequence length and the observation-to-text ratio, so it cannot wait.

**THE GATE.** Before any LM training, on held-out frames: **HP-bar within 1px · menu and dialog text legible (OCR or human panel) · sprite identity correct · codebook utilisation >95%.** On failure: more levels, bigger codebook, less downsampling, or restrict to battle screens. **Do not proceed past a failed gate.** The held-out vocabulary is grounded through on-screen battle text, so a tokenizer that blurs it destroys the experiment without saying so.

### 3.3 The held-out vocabulary

How Substrate A shows that grounding happened rather than text co-occurrence.

Scrub a term set from the **entire** text stream (essays, tool results, analyses) so meaning can only come from grounded trajectories.

| Class | Held out | Matched control (kept in text) |
|---|---|---|
| Types | `water`, `rock`, `grass`, `electric`, `ground` | `fire`, `normal` |
| Moves | `water_gun`, `thunder_shock`, `vine_whip`, `ember` | `tackle`, `scratch` |
| Effectiveness | `super effective`, `not very effective` |: |

**The control set is not optional.** It is what makes a null result interpretable.

RAM-derived type/move/HP state labels **probe targets only**, never model input in the held-out condition.

**Probes.** *Interpretability:* nearest observation-code embeddings to each held-out word embedding by cosine; success means held-out type and move embeddings sit nearest the codes of frames where those types and moves appear (mirrors TIGER, arXiv:2305.05065, where RQ-VAE codes captured category structure). *Behavioural:* does the model choose super-effective moves in held-out matchups above chance, versus the text-supported controls?

---

## 4. Substrate B: psychohistory

Substrate A shows the mechanism works. Substrate B asks whether it survives when the adjudicator is reality.

**The environment already exists in this repository.** `../validation/` has harvest scripts for Reddit (WSB, AskEconomics, location subs), GitHub, and Wikipedia; pre-registered falsifiers with frozen thresholds; blind Louvain community detection; semantic critical-slowing-down detectors; and an EnKF forward engine. What it lacks is a trajectory generator, and the companion paper's four blocked falsifiers are blocked on exactly that.

### 4.1 The loop, instantiated

1. **Observation.** A block's state at time `t`: mention-density series, embedding-variance (belief dispersion), community partition, operator concentration (HHI / Gini). The repo's existing observation operators.
2. **Tower dialogue.** Towers propose competing readings (endogenous or exogenous? is N_eff collapsing? is there an operator ramp?) with reasoning and a forecast at horizon `h`.
3. **Disagreement gate.** JS divergence across tower forecasts.
4. **Adjudication by reality.** Wait out the horizon, harvest what happened.
5. **Yield.** Surprisal of the realised outcome under the pre-registered ensemble forecast.
6. **Admit.**

### 4.2 Why this substrate and not just a code executor

Result (4) shows self-play works with a code executor. A code executor is a deterministic program, and so is an emulator. A large enough model can in principle internalise either, at which point yield legitimately goes to zero and the well runs dry. **Environments that resist simulation are the renewable ones.**

Social reality cannot be internalised, which is the companion paper's central negative finding (out-of-model agents; more data does not help) restated as a resource rather than a limitation. It is also already pre-registered: frozen thresholds, sealed rosters, binomial rules committed before harvest. A bootstrap harness needs exactly that discipline, because otherwise it grades its own homework.

And reflexivity, the hard case, only appears here. A LOGOS-class ensemble forecasting a social system it is deployed inside is the mean-field-game fixed-point problem the companion paper formalises. Pokémon cannot test that.

### 4.3 The cost problem

Adjudication takes weeks to months. A few thousand good trajectories per quarter is three orders of magnitude short of relevance to a 2.8T tower. **Substrate B does not scale as a token source and this spec does not claim it does.**

It is the validity check. If yield-weighted grounded trajectories help on the emulator but not when reality adjudicates, the mechanism was learning emulator artifacts. **A for volume, B for validity.** Retrospective backtesting on sealed rosters partly relieves the cost, at the usual price in hindsight contamination.

---

## 5. Model, training, schema

### 5.1 Model

Decoder-only, RMSNorm, RoPE, SwiGLU, **QK-norm**, no bias.

| | 125M (debug) | 350M (main) |
|---|---|---|
| d_model / layers / heads / head_dim | 768 / 12 / 12 / 64 | 1024 / 24 / 16 / 64 |
| context | 2048 | 2048 |

QK-norm is not optional. Chameleon (arXiv:2405.09818) found it necessary for mixed-modal stability; without it, loss diverges after roughly 20% of an epoch at 7B.

**Vocabulary:** text 8k–16k (mined) + observation codes 2k–8k + specials (BOI/EOI, role delimiters, held-out mask), about **10k–24k total**. A small vocabulary keeps the embedding table cheap, which matters at 24 GB.

**Observation-code embedding init:** from the RQ-VAE codebook vectors through a learned linear projection (codebook dim → d_model). If codes are factorised, use MAGVIT-v2's token-factorisation pattern (embed each sub-codebook, sum). Reuse the existing mean-of-subtoken init for mined text tokens.

### 5.2 Early fusion and the loss decision

- **Delimiters.** Wrap every observation-code span in BOI/EOI specials, as Chameleon does.
- **Mask the loss on observation codes.** The model must **read** observations, not generate them. Prefix-LM style: observation codes are context, loss lands on thought and action tokens. This follows Emu3's understanding stage (arXiv:2409.18869; *Nature* s41586-025-10041-x, phased training with loss weighting so vision tokens do not dominate) and is independently supported by PaliGemma (arXiv:2407.07726), which found that predicting the prefix "clearly reduces average performance." Chameleon Fig. 6b, where instability vanishes once image generation is disabled, is the stability argument for the same choice. **Keep an ablation switch.**
- **Intra-observation bidirectional attention** (optional, v2): Transfusion (arXiv:2408.11039) reports a significant gain. Causal across the sequence, bidirectional within one observation's span.
- **Chain-of-thought must be load-bearing.** Loss is on thought and action; if the action were decodable from the observation alone, the reasoning span would never be learned. In the bootstrap loop this is automatic, because disagreement gating only admits trajectories where the answer was not obvious.

### 5.3 Trace schema

One grammar, so sequence packing sees a single format. Only the `observation` payload type differs.

**Substrate A:**
```yaml
episode: pokemon_red_battle_0142
step: 17
observation:
  type: screen
  frame: [<boi> <v_412> <v_87> <v_1003> ... <eoi>]   # RQ-VAE codes, LOSS-MASKED
proposals:                       # the disagreement that justified generating this at all
  - tower: logic ; predict: "rock resists normal moves" ; action: select_move water_gun
  - tower: code  ; predict: "type chart unknown"        ; action: select_move tackle
  js_divergence: 0.61
thought: enemy Onix is rock and ground; water and grass hit 2x; my Squirtle knows water_gun
action: select_move water_gun
result:
  type: screen
  frame: [<boi> <v_...> <eoi>]
  hp_delta: -18                  # RAM-derived; PROBE LABELS ONLY
  yield: 2.31
```

**Substrate B:**
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
  - tower: logic ; predict: endogenous_cascade ; p: 0.72
  - tower: admin ; predict: exogenous_shock    ; p: 0.65
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

**Text-harness variant** for the language-competence half of the corpus uses the same keys with `observation.type: tool_result`, and a four-variant fan-out (hit / near-miss / misleading-but-plausible / multi-hop) following AgentFounder (arXiv:2509.13310) and the phi "textbooks" method, generated locally by a Qwen3-class MoE on the same GPU at zero API cost. Apply the held-out filter as a hard post-processing step, regex **and** tokenizer-level.

### 5.4 Training

**Trainer:** a modded-nanoGPT derivative (`KellerJordan/modded-nanogpt`; `Deveraux-Parker/nanoGPT_1GPU_SPEEDRUN` for the single-consumer-GPU adaptation). `litgpt` is a fallback.

**Optimizer:** Muon on 2D matrices, AdamW on embeddings, head, norms, and 1D params. Muon keeps one momentum buffer instead of two, saving about 4 B/param on 2D matrices (~1 GB at 350M), and is reported roughly 35% faster to a target loss. Fallback: plain AdamW (β 0.9/0.95, wd 0.1, clip 1.0, cosine or trapezoidal, warmup).

**Precision:** bf16. FlashAttention-2 works on Ampere; **FP8 does not** (GA10x tensor cores do TF32/BF16/FP16/INT8/INT4 only).

**Memory at 350M / 2048 / bf16 / 24 GB:** about 5.6 GB fixed for AdamW state (16 B/param mixed) plus activations. Micro-batch ~4 without checkpointing; 8 may need it. Gradient accumulation to a global batch of 256k–500k tokens per step.

**Wall clock, planning numbers only.** About 18k–30k tok/s at 350M/2048, so roughly 9–14 h per 1B tokens, ~1 day for 2B, ~3–4 days for a 4-epoch pass over 2B. 125M: 45k–90k tok/s. **These are interpolations from measured 4090, A30, and L20 runs, not a first-party 3090 log at these sizes.** Run a forward-backward probe with `torch.cuda.max_memory_allocated` on day one and set the schedule from what it says.

**Data schedule:** ≤4 epochs (Muennighoff et al., arXiv:2305.16264, NeurIPS 2023: up to 4 epochs of repeated data costs almost nothing against unique data, validated across 400+ runs, 10M–9B params, up to 900B tokens). Watch for the epoch-5 jump. **20–30% text replay whenever observation data is mixed in**; cap the observation stream at 15–30% of tokens. **Accumulate the corpus across rounds, never rotate it** (Gerstgrasser).

**Packing:** several traces per 2048-token sequence with document boundaries, FlexAttention block masks to stop cross-document attention.

---

## 6. Layout

```
logos-harness/
  configs/     rqvae.yaml  tokenizer.yaml  model_{125m,350m}.yaml  train.yaml
               heldout_vocab.yaml  bootstrap.yaml        # disagreement + yield thresholds
  data/        raw/  frames/  traces_text/  traces_game/  traces_psycho/  packed/
  bootstrap/   propose.py        # multi-tower proposal + JS-divergence gate
               adjudicate.py     # environment step + outcome capture
               yield_score.py    # surprisal under the pre-action ensemble distribution
               admit.py          # yield-weighted, accumulating corpus admission
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

## 7. Phases and gates

| Phase | Work | **Gate** |
|---|---|---|
| **0** | Substrate A harness: headless PyBoy, scripted and random-walk dump of ≥100k (frame, action, RAM-state) tuples, savestates at Pallet Town / first battle / first gym | 100k+ frames dumped headlessly; savestates load; RAM state parsed and **aligned to frames**; **measured** disk-write throughput recorded (published steps/sec are rollout figures and do not apply to a frame dump, which is I/O bound) |
| **1** | RQ-VAE observation tokenizer; resolve flatten-vs-collapse | **HP-bar within 1px · text legible · sprite identity correct · codebook utilisation >95%.** No LM training until this passes |
| **2** | Tokenizer mining, joint vocab, YAML-to-token-id compiler, held-out leak validator | Round-trip lossless both variants; **zero held-out terms in the text stream**; embedding init sane |
| **3** | Text corpus, four-variant fan-out, quality and leak filtering | Token count reached; variant distribution as designed; leak scan clean; human spot-check passes |
| **4** | **Bootstrap loop, Substrate A.** Multi-tower proposal (≥2 distinct open models standing in for towers), JS-divergence gate, emulator adjudication, yield scoring, accumulating admission | Admitted trajectories have **mean yield strictly above** an unfiltered self-play control; disagreement shrinks over rounds in explored regions |
| **5** | Pretraining: 125M debug end to end, then 350M. ≤4 epochs, packing, replay, curriculum, observation loss masked | Stable loss (no divergence, QK-norm on); no epoch-5 jump; **collapse monitor** shows no tail narrowing against the text-only baseline |
| **6** | Probes and agent eval | Held-out terms show above-chance grounding **against the control**; super-effective choice above chance; agent clears early VideoGameBench Lite checkpoints |
| **7** | **Substrate B.** Wire `../validation/` harvest scripts as the observation channel; run retrospectively on sealed rosters, then forward | Yield-weighted grounded trajectories beat both unfiltered self-play **and** a text-only control, **with reality adjudicating**. If A passes and B fails, the mechanism was learning emulator artifacts |

**The headline ordering the whole spec tests (falsifier F9 in the paper):**

> grounded > disagreement-gated self-play > unfiltered self-play > nothing

If unfiltered self-play matches grounded trajectories at matched token counts, the observation bound is wrong and this line of work should stop.

---

## 8. Risks

| Risk | Mitigation |
|---|---|
| **Lossy RQ-VAE caps everything.** No HP bars or text means no grounding, and it fails silently | The hard Phase-1 gate. Edge and region weighted loss. Low downsampling. Four-colour frames are in your favour |
| **Model collapse** | Disagreement gating and yield weighting structurally exclude confident self-agreement; corpus accumulates rather than rotates (Gerstgrasser). Explicit `collapse_monitor.py` against a text-only baseline. **If the monitor fires, the mechanism is refuted** |
| **Towers stand in for towers.** Two open models at 350M are not 2.8T towers, and the disagreement structure may not transfer | Unavoidable at this budget. State it; do not claim validation at tower scale |
| **Substrate B does not scale.** Three orders of magnitude short | Stated, not solved. B is validity, A is volume |
| Held-out term never learnable, co-occurrence too sparse | Over-represent battle frames; verify the tokenizer preserves on-screen text; **keep the control set so a null is interpretable** |
| Grammar not learnable from structured traces alone | 70–85% text stream includes prose, not only tool calls. BabyLM (arXiv:2504.08165) shows 100M-word natural-text budgets suffice for grammar |
| Observation codes swamp or destabilise training | Mask observation loss; cap at 15–30%; 20–30% text replay; QK-norm and z-loss |
| 3090 memory or time overrun | Micro-batch 4 plus gradient accumulation; Muon; 125M debug first; ≤4 epochs |
| **Throughput estimates are scaled, not measured on a 3090** | Day-one probe before committing to a schedule |
| PokéAgent confusion | Showdown and Emerald, not Red/Blue frame logging. Citation only |
| ROM legality | ROMs are in none of these repos and must be supplied by the user. The code is MIT; the games are not |

---

## 9. What this settles, and what it does not

**Settles:** whether disagreement-gated, environment-adjudicated trajectory generation beats unfiltered self-play and a matched text-only control without triggering collapse, on two substrates that fail differently, with a control set that makes a null interpretable.

**Does not settle:** whether it transfers to 2.8T towers; whether the yield rate scales to the 10¹³–10¹⁴ tokens the paper's Proposition 2 needs; whether the effect survives when the environment is code execution, a wet lab, or a market rather than an emulator; and whether the tower-diversity claim of §1.1 holds when the towers are actually frontier-scale. Those are the real questions and this answers none of them.

**Run it anyway** because it is the cheapest experiment that can return a decisive negative. If disagreement-gated grounded trajectories do not beat a text control at 350M on the easiest imaginable grounding substrate, where the exact semantics under test are printed on screen in four colours at 160×144, then the strategy past the token wall is repetition plus synthesis, the paper's Proposition 2 headroom is all there is, and `logos.tex` should say so.

---

## 10. References

**Theory (§1).** Choi et al., Demystifying multi-agent debate: the role of confidence and diversity, arXiv:2601.19921, 2026. Should we be going MAD?, ICML 2024. Yue et al., Does RL really incentivize reasoning capacity in LLMs beyond the base model?, NeurIPS 2025. Zenil et al., On the limits of self-improving in LLMs, arXiv:2601.05280, 2026. Shumailov et al., *Nature* 631:755–759, 2024. Gerstgrasser et al., arXiv:2404.01413, 2024. Zhao et al., Absolute Zero, arXiv:2505.03335, NeurIPS 2025. Silver and Sutton, Welcome to the era of experience, DeepMind, 2025. SPICE, arXiv:2510.24684. EvoEnv, arXiv:2605.14392.

**Harnesses.** VideoGameBench, Zhang, Griffiths, Narasimhan, Press, arXiv:2505.18134, `alexzhang13/videogamebench` (MIT). PufferLib, Suarez et al., arXiv:2406.12905, `PufferAI/pokegym`, `drubinstein/pokemonred_puffer`, `PWhiddy/PokemonRedExperiments`. PokéAgent Challenge, Karten et al., arXiv:2603.15563 (citation only). Pokémon Red via RL, Pleines et al., arXiv:2502.19920. `NousResearch/pokemon-agent`. RAM map: datacrystal.tcrf.net.

**Tokenizers and VQ.** `lucidrains/vector-quantize-pytorch` (MIT). TIGER, Rajput et al., arXiv:2305.05065, NeurIPS 2023. Lee et al. 2022, residual quantization. MAGVIT-v2 / LFQ, Yu et al., ICLR 2024. Open-MAGVIT2, arXiv:2409.04410.

**Early fusion.** Chameleon, arXiv:2405.09818. Emu3, arXiv:2409.18869; *Nature* s41586-025-10041-x. Transfusion, arXiv:2408.11039. PaliGemma, arXiv:2407.07726.

**Training and data.** `KellerJordan/modded-nanogpt`. `Deveraux-Parker/nanoGPT_1GPU_SPEEDRUN`. Muon, kellerjordan.github.io/posts/muon. Muennighoff et al., arXiv:2305.16264, NeurIPS 2023. BabyLM, arXiv:2504.08165, arXiv:2412.05149. phi-1, arXiv:2306.11644. phi-1.5, arXiv:2309.05463. AgentFounder, arXiv:2509.13310.

**Substrate B.** W. Sharon, *Conditions for Predictable Social Dynamics*, draft v0.5, and this repository's `../validation/` suite.
