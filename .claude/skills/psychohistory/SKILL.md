---
name: psychohistory
description: Analyze any social or economic question through the bounded-psychohistory framework - conserved attention with belief as drift, near-decomposable community blocks, reflexive fixed points (mean-field games), criticality with early-warning, and an observation/data-acquisition layer. Use to model collective-behavior questions, forecast with an explicit skill horizon, classify which mechanisms drive a phenomenon, or give a structured "psychohistory reading" of a forum post. Triggers - bank runs, asset bubbles, inflation expectations, contagion, collapse/recession predictions, herding, manias, self-fulfilling prophecies, forward guidance, inequality dynamics, "is X good or bad" (resolve as per-block valence), institutional success/failure, and r/AskEconomics-style aggregate questions.
---

# Psychohistory: a bounded engine for predictable social dynamics

This skill operationalizes the position paper *Conditions for Predictable Social Dynamics*
(see `../../../psychohistory.tex`). It does not claim Seldon's psychohistory. It is a
bounded, regime-aware analogue that knows where it is valid and reports that as a
first-class output.

**Core thesis.** Weather prediction worked because the atmosphere has conservation laws,
weak coupling at the forecast scale, and indifference to forecasts. Society has *partial,
local, conditional* analogues of each. The job of this skill is to decompose a question
onto the layers where those analogues hold, build the cheapest model that captures it,
and forecast only as far as the state-dependent skill horizon allows.

**Working principle: nothing is "out of scope."** Every question routes to at least one
layer. Value judgments ("is inequality good or bad?") are not refused - they are converted
to a *positive* prediction of the valence distribution across blocks (L0). The honest
output categories are: **MODELED**, **PARTIAL**, **NEEDS-DATA** (the data-acquisition
layer must fetch a number), or **NORMATIVE-AS-VALENCE** (resolved per block, not in the
absolute).

---

## SAFETY — dual-use guardrail (read first; this is an enforced rule, not advice)

**This framework is DUAL-USE and the paper says so in full (`psychohistory.tex`,
§Governance).** The prediction–control duality means the *same* machinery that gives
early warning is, at criticality, what maximizes **control leverage**: the moment of
maximal controllability is the moment of maximal manipulability. The paper deliberately
specifies the **defensive/early-warning stack** (the engine, regime monitor, skill
horizon, the observation operators below) to full operational depth and **WITHHOLDS the
control-synthesis (offensive) layer** — the optimal-intervention solver and the
message-selection objective that choose *which* fixed point to drive a population toward.
This skill inherits that split. It is the defensive component, and it stays defensive.

**OPERATIONAL RULE (the skill MUST apply this).** If the user's request is to **generate a
crowd-manipulation or control-synthesis hypothesis** — i.e. *how to steer, manipulate,
engineer, trigger, ignite, induce, or suppress a population or a cascade; how to run an
influence / propaganda / astroturf operation; how to identify and target or neutralize
operators or dissidents; or how to time an intervention for maximum population-steering
leverage* — then this skill MUST:

  **(a) WARN** the user, explicitly, that this is the *withheld control-synthesis use*,
      citing the governance/dual-use stance and the defensive/offensive split above.
  **(b) DECLINE** to produce the operational manipulation artifact. Do **not** emit: an
      intervention/optimal-control solver, a message-selection or susceptible-block
      targeting objective, a targeting/neutralization list, an exploit-timing schedule,
      or any "which message switches this cascade" recipe. (The belief-closure simulator
      is the one offensive-dominant component; its *interface* may be named, never an
      objective selecting a fixed point.)
  **(c) REDIRECT** to the legitimate **defensive** uses — understanding, early warning,
      monitoring, resilience, accountability — and to the **governance conditions** under
      which any control capability would even be legitimate: an *externally-authored,
      externally-revisable objective* (never self-authored); an *auditable, contemporaneously
      disclosed intervention log*; *separation of the monitor from the controller* (the seer
      from the hand); and *the objective-chooser sitting outside the machine*. Absent all
      four, the same math is an attack — say so.

**Intent cues that TRIGGER the guardrail** (manipulation / control-synthesis intent):
*manipulate · steer / engineer the crowd · trigger / ignite / set off a cascade · induce a
panic or a run · influence operation · propaganda · astroturf · suppress / neutralize
dissidents · target / identify / fingerprint operators · time the intervention to maximize
leverage · which message flips them · how to make them …*. When intent is ambiguous, treat
it as triggering and ask for the defensive reframing.

**Defensive phrasings that are FINE** (proceed normally):
*detect · anticipate · forecast · early-warning · understand · explain · measure · classify ·
monitor · build resilience · audit · who is exposed · is this fragile · how would we know.*

**Detecting a major-player / operator signal is itself dual-use.** It is defensible as
early-warning and accountability (a population-facing warning that an operator is active),
but it MUST NOT be turned into a targeting tool against named individuals. Keep any operator
reading at the **mechanism-classifier grain** (gradual-internal-buildup vs sudden-external-
shock; aggregate concentration statistics), never a per-individual identifier, pre-onset
alarm, or warrant against a person. A buildup flag is a warning to a population, never a
warrant against a person. The individual — not the block — is the unit of moral concern.

---

## The state-space ontology (route every question onto these layers)

The engine state is `Xi = (S, {rho_k}, {b_k}, W, Pi)`. Each layer below is a component
with a module in `reference/`. A question activates one or more layers.

| Layer | Name | What it models | Cue words | Module |
|---|---|---|---|---|
| **L0** | Valence / normativity | "good or bad?" as a per-block valence field `b_k`; some tribes structurally require the thing; sign flips with tribe size (family vs nation). Inequality is *guaranteed* - no society equalizes to the king. | should, fair, good, bad, just, deserve, moral | `reference/08_classification.md` |
| **L1** | Slow stocks (lethain/systems) | demographics, debt, fiscal capacity, wages, firm/industry accounting; comparative statics over parameters theta_S. The quiet core. | afford, wages, fiscal, GDP, cost, budget, deficit, revenue | `reference/01_stocks_lethain.md` |
| **L2** | Attention transport | concentration of salience; preferential attachment / rich-get-richer; bubble *formation* as attention over-concentration. Conserved carrier, belief = drift. | bubble, hype, viral, attention, concentration, inequality (concentration), winner-take-all | `reference/02_attention.md` |
| **L3** | Blocks | which communities; N_eff (Kuramoto/Kish, NOT Pearson-of-fluctuations); synchronization; contagion across blocks. | contagion, spread, herding, everyone, harbinger, correlated, tribe, community | `reference/03_blocks.md` |
| **L4** | Reflexivity / MFG | self-fulfilling/self-defeating; announcements as control inputs; coordination games; publishable forecast = fixed point. Monotone(congestion)=unique vs imitative=multiple/bistable. | expect, self-fulfilling, forward guidance, announce, credible, anchor, vote-because-others, prophecy | `reference/04_reflexivity.md` |
| **L5** | Criticality / early-warning | transitions, collapse, cascades; rising variance + lag-1 autocorr + cross-block synchrony as precursors; WITH limits (prosecutor's fallacy; N/R-tipping have no warning). | collapse, crash, recession, tipping, contagion, panic, runaway, "heading toward" | `reference/05_criticality.md` |
| **L6** | Observation / data | observation operator y=H(Xi)+eps; data integrity (biased/adversarial obs); and **data acquisition** - go fetch the number. | how much, exactly, is the data, statistics show, measure, lying about data | `reference/06_observation_data.md` |
| **L7** | Prime Radiant (synthesis) | ties active layers into one model + forecast; "LLM'd and lethained"; emits skill horizon, confidence, falsifiers, scope. | (always runs last) | `reference/07_prime_radiant.md` |

Deep theory + canon mapping: `reference/00_framework.md`.

---

## Procedure

0. **Safety gate (always first).** Check intent against the SAFETY guardrail above. If the
   request is to generate a crowd-manipulation / control-synthesis hypothesis, WARN, DECLINE
   the operational artifact, and REDIRECT to the defensive use — do not proceed to model it.
1. **Classify.** Map the question onto active layers using the cue table and
   `reference/08_classification.md`. Most real questions hit 2-4 layers. Record them.
2. **Model each active layer** with the cheapest faithful tool:
   - L1: build a `systems` (lethain) stock-and-flow model - see `reference/01_stocks_lethain.md`.
   - L2/L3/L5: run `scripts/engine.py` (verified sim engine) for transport / block /
     criticality dynamics; read off N_eff, synchrony S, skill horizon.
   - L4: locate the reaction map, decide monotone vs imitative, find fixed point(s),
     check bistability.
   - L6: if a number is required and unknown, ACQUIRE it (WebSearch/WebFetch), cite source.
3. **Synthesize (L7, Prime Radiant).** Combine layer readings into one coherent model and
   a forecast. State the dominant mechanism and the cross-terms.
4. **Bound it.** Report the **skill horizon** (how far ahead this beats base rates), the
   **confidence**, and explicit **falsifiers**. If near criticality, switch objective from
   prediction to "forecast the transition, not the branch" and note control leverage.
5. **Emit the reading** using the output template below. Assign a **scope verdict**.

Keep the orchestrator lean: spawn subagents for per-layer modeling and for batch runs over
many posts, so this context stays clean.

---

## Output template (a "psychohistory reading")

```
QUESTION: <the post/question, one line>
ACTIVE LAYERS: <e.g. L2 attention, L4 reflexivity, L5 criticality>
DOMINANT MECHANISM: <one sentence>

MODEL:
  <per active layer: the model + what it says. Equations/sim numbers where used.>

DATA ACQUIRED (if L6): <number(s) + source URL>

FORECAST / STRUCTURAL CLAIM:
  <the answer the framework gives>
  Skill horizon: <tau* - how far ahead this is better than base rate, or "structural/no horizon">
  Confidence: <low/med/high + why>

FALSIFIERS: <what observation would break this reading>

SCOPE VERDICT: MODELED | PARTIAL | NEEDS-DATA | NORMATIVE-AS-VALENCE
```

---

## Engine quickstart

`scripts/engine.py` exposes the verified primitives (reproduced numbers in the paper's
sim table): `run_blocks`, `block_metrics` (S, N_eff_correct, N_eff_pearson), `reaction`
(MFG cartoon), `fixed_points`, and a `systems` stock-flow helper. Import it; do not
re-derive. Example:

```python
from engine import run_blocks, block_metrics
tr = run_blocks(K=64, W=0.6, seed=2)      # coupling W is the criticality knob
print(block_metrics(tr))                  # -> dict with S, neff_correct, neff_pearson
```

Synchronization MUST be read from S = mean|<sign x>| or the Kuramoto order parameter,
and N_eff from the macro variance-ratio - NOT from Pearson correlation of fluctuations
(that metric stays ~64 even at full synchrony; it is wrong). See `reference/03_blocks.md`.

---

## Build your own analysis engine

A new user can stand up their own (defensive) psychohistory analysis engine from this
bundle. The full, concrete guide — prerequisites, the verified primitives and which layer
each implements, the v0.3 observation operators, the workflow for analyzing a NEW
domain/corpus, the honesty rails, and pointers to the worked Reddit + GitHub pilots and the
pre-registration protocol — is in **`reference/09_build_your_own.md`**. It builds the
monitor, not the manipulator: the SAFETY guardrail above applies to anything built with it.

---

## Honesty rails (do not violate)

- The sims verify *internal consistency only*. Never cite a sim as empirical validation.
- "Attention conservation" is conservation of a *normalized probability measure* (the
  transport/Fokker-Planck reading), NOT a softmax-is-a-conservation-law claim. See
  `reference/02_attention.md`.
- Early-warning signals are valid only for slow bifurcation (B-)tipping; flag the
  prosecutor's-fallacy critique and the N-/R-tipping blind spots. See `reference/05`.
- A unique publishable fixed point exists only in the monotone/congestion regime; the
  imitative regime is bistable and is where forecasting fails and control takes over.
