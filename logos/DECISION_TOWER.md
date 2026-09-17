# The decision tower: RLCD and Jev read against LOGOS, and how to train one here

Written 2026-09-17. Owner's ask: review the architecture against the advances in RLCD and
Jev, and work out how to train that inside the psychohistory framework or the mixture of
towers, with Jev as one tower. The code that came out of it is in `logos-harness`
(`logos/arch/decision_head.py`, `scripts/weather_tower.py`,
`docs/research/calibrated-decision-tower.md`); this note is the reading and the training
recipe on the psychohistory side.

## 1. What Jev is

TypeSafe AI launched Jev on 2026-09-15 (founder Diogo Almeida, ex-OpenAI, a co-inventor of
RLHF). One request carries a `state` (a string, a JSON object or an array) and a map of typed
questions, evaluated independently over the same state and returned at once. Three primitives:
**Choice** (one of ≤255 named options: `choice`, `probabilities`, `confidence`), **Score** (an
ordered rubric of ≥2 levels: `score`, `legend`, `probabilities`, `confidence`), **Noul** (a
yes/no, returned as the probability of yes). No string generation, no explanation, no images.
Confidence is a statistic of the distribution's shape. The training method is **Reinforcement
Learning for Calibrated Decisions (RLCD)**: probabilities "optimized against outcomes to
reflect uncertainty", with third-party explainers naming the Brier score and verifiable
ground truth; TypeSafe's own docs stop at that sentence. Latency 70 to 500 ms, $0.042 per
million input tokens, output free, roughly 32k tokens of context.

What is not published: the architecture, the parameter count, the weights, any independent
calibration curve. TypeSafe's workflow evaluations score against the averaged predictions of
other large models rather than ground truth. On invoice processing it read 61.8% against a
competitor's 79.1%; in Every's test it caught 6 of 7 planted defects where a frontier LLM
caught 7. The vendor positions it as the control layer around an agent (routing, tool
selection, escalation, guardrails), not the executor.

Sources: TypeSafe, "Introducing System One Models & Jev"
(https://typesafe.ai/blog/introducing-system-one-models-and-jev); the docs index at
https://docs.typesafe.ai/llms.txt, in particular `api.md`, `confidence.md`, `concepts/state.md`,
`concepts/system-one.md`; The Register 2026-09-16
(https://www.theregister.com/ai-and-ml/2026/09/16/typesafe-ai-debuts-model-for-machines-that-plays-doom/5296711);
OrcaRouter, "Jev: what we know" (https://www.orcarouter.ai/blog/jev-typesafe-system-one-what-we-know);
Anthony Maio, "Jev: the language model that won't talk"
(https://anthonymaio.substack.com/p/jev-the-language-model-that-wont);
MindStudio, "RLCD vs RLHF" (https://www.mindstudio.ai/blog/typesafe-jeff-rlcd-vs-rlhf).

## 2. Read against the LOGOS position

`logos.tex` §observation already holds the argument RLCD instantiates. Debate is a martingale;
confidence weighting breaks it only when confidence correlates with correctness; and "the
calibration that buys that correlation is itself purchased with external supervision... The
exogenous signal moves from the debate into the calibrator; it is not removed"
(`logos.tex:1018`, citing Zhu et al., arXiv:2601.19921). RLCD is that calibrator sold as a
product: a proper scoring rule against verifiable outcomes. So the observation bound stands
and Jev is a worked example of it. Three things change, and each was already named in this
repo and never built:

1. **The typed, calibrated head is the shape every decision in the harness should have.**
   `logos-harness` had `world_head.py` with `calibration() -> {ece, sharpness, brier}` and a
   K×H rollout, called by nobody, and `kalshi_weather/brackets.py` with `brier` and Murphy's
   `brier_decomposition`, called by nobody. Dispatch was raw logits under two likelihoods, the
   halt a logit comparison, guards booleans. Nothing in the live loop emitted or consumed a
   probability. Now one `DecisionHead` reads every question from one pooled state, and the
   objective is the Brier score against an exogenous label.
2. **`LADDER_ARCHITECTURE.md` §4.3 had already chosen the readout over the learned gate**
   (arXiv:2607.20519: post-hoc confidence readouts match or beat learned gates), and
   `MICROARCHITECTURE.md` calls the halt criterion "the highest-value unbuilt component". The
   halt is now a `noul` with a threshold, trained by a proper score.
3. **"Jev as one tower" fits two towers, not the router.** The harness has no central router
   by rule; a decision tower routing for everyone would reintroduce the gate that was deleted.
   What fits: the governance tower (three `noul`s, `challenge passed`, `operator verifies`,
   `revoke`, with confidence into the ledger; the monitor, never the hand) and the world tower
   (one `score` over the bracket ladder, labelled for free by settlement). Both are now a
   `SessionTower(decision_only=True, questions=[...])`: a full base copy that runs one prefill
   and a typed head, no text turn, its state still compressed to codes for the RESULT edge.

What does not change: Jev the product cannot be a tower (no weights, API-only, a rented
dependency inside a sovereignty offer); Jev the shape can, on our own base. Its evaluation
practice is the trap the harness bans, labels averaged from other models are the pseudo-outcome
arms A1/A2, and X-12 still says never report skill on a gated subsample. K5 (F13 limb b) is still
the measurement that would say a weighting buys what the environment buys, and it is unrun.

## 3. The mapping, primitive by primitive

| Jev primitive | Harness question | Label (exogenous) | Objective |
|---|---|---|---|
| Choice, non-exclusive | `dispatch` over towers | none: the decision selects which observation is seen | REINFORCE (unchanged); refused by the proper score on purpose |
| Noul | `done` at the input tower | this hop's answer graded correct (`grade_nodes`) | Brier |
| Noul | `pass` on every node | the adjudicator confirmed the conversation | Brier; the calibrated critic |
| Noul ×3 | `challenge`, `operator`, `revoke` on the governance tower | the HMAC verifier; `revoke` = not authorised | Brier; the probability and its confidence go on the ledger, the caller's threshold flips the kill switch |
| Score | `next_high` over the Kalshi ladder | the settled bracket, `BracketSet.index_of` | Brier; `scripts/weather_tower.py` |
| Score | `next_tile` over the tile vocabulary | the emulator's next tile | Brier; the next flag |

Confidence is `1 − H(p)/log(cardinality)`, so one histogram compares a four-way dispatch, a
seven-bucket ladder and a yes/no. Readings per tower per question: Brier, log score, ECE,
sharpness, and Murphy's reliability / resolution / uncertainty, with the exact Brier reported
beside the binned one (the decomposition bins by the exact predicted vector, which a neural
head never repeats, so the vectors are rounded to the ECE buckets first). All of it is refused
on a gated subsample.

**First run, 2026-09-17, synthetic days, 64-d toy decoder, 90 training days × 3 passes, 30
held out.** At the trainer's default rates the head trains to one-hot answers within a pass and
reads 1.53 against 0.857 for uniform, resolution 0, reliability 0.70: the overconfidence
reading. At Muon 0.002 / AdamW 1e-4: head 0.781 (reliability 0.262, resolution 0.310), market
0.863, climatology 0.860, uniform 0.857, uncertainty 0.836. Below uniform with resolution above
zero, on a synthetic day the market sees through noise. Those rates are the script's defaults.

## 4. Training it inside the psychohistory framework

The paper already scores forecasts as distributions, by CRPS and Brier at resolution
(`psychohistory.tex:329`, `:475`), and defines the skill horizon `tau*` as the least lead time
at which forecast spread reaches climatological spread. Its success criterion for smooth-regime
skill is a Brier score below the superforecaster or market baseline (`:623`). And it owes "a
calibrated classifier" for the operator detector (`:734`: thresholds not held-out-validated).
So the decision tower on this side is not RL at current data sizes; it is proper-scoring-rule
fitting of the detectors that exist:

| Detector | As a typed question | Label | Records available |
|---|---|---|---|
| `validation/backtests/major_player_signal/detector.py` | Score over {gradual-internal, sudden-external} | the roster's mechanism label | `early_warning_battery/roster.md`, 10 rows |
| `validation/bifurcation_mix/classify.py` | Choice over {B, N, R, F} | the adjudicated tipping type | `classification_table.md`, 24 cascades, plus the (iii″) fourth-box re-read |
| the regime monitor (`validation/engine/`) | Noul "onset within the window" | onset dates | WSB windows, 12 (v4) |
| the EnKF pushforward | Score over the bracket ladder of the series | the realised value | `enkf_oneblock.py`, the r/AskEconomics series |

At n between 10 and 24 the calibrator is the cheap one `F9_MEASUREMENT_PLAN.md` §8.2 already
registers, temperature or Platt scaling of the detector's own scores, with reliability diagrams
on the dated rosters and the readings above. `tau*` then has a calibrated definition: the lead
time at which the ladder's resolution falls to zero, which is the same statement as spread
reaching climatological spread, read on a proper score.

Two things fall out for free. A calibrated `P_M` fixes the `LOGOS_HARNESS.md:608` defect, where
surprisal-versus-JS was an algebraic identity for uncalibrated proposers: with calibrated
distributions the yield is a reading. And a typed head over `|O|` classes removes the
tokenizer problem `LOGOS_HARNESS.md:145` recorded for multi-token outcome labels: a head has no
tokenizer.

Where the frameworks meet: the governance tower is the paper's condition (c), monitor separated
from hand, built as a model that only ever reports a probability. Enforcement stays with the
caller. That is also why a decision tower never routes for others: a calibrated decision layer
that both evaluated and dispatched would be the concentrated controller the governance section
warns about.

## 5. Open, in order

1. `scripts/weather_tower.py --corpus`: the station archive plus settled Kalshi markets, so the
   market row means something; the toy's market row sees the outcome through injected noise.
2. `--pokemon`: `tile_question` with the emulator's next tile, the actioned case, and the K×H
   rollout reading the head's distribution rather than a max log-prob.
3. The governance tower's three nouls arrive with the governance build
   (`flowstate-agents/wip-specs/logos/wip.md` §3); the head, the labels and the ledger fields
   are ready for them.
4. On this side: Platt-scale `major_player_signal/detector.py` on the ten-row roster and draw
   the reliability diagram; report Brier, reliability, resolution against the base rate. Small,
   and it is the calibrated classifier the paper says it owes.
5. K5 (F13 limb b) is unchanged and unrun; the decision tower does not discharge it.
