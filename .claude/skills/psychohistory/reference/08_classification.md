# 08 — Classification: the routing rubric + scope verdicts

This is the router. Given any question, it tells you (a) which layers L0–L7 are active,
(b) how to model each, and (c) which of the four **scope verdicts** to emit. It is the
operational front door of the skill; `00_framework.md` is the theory behind it.

Working principle (from SKILL.md): **nothing is out of scope.** Every question routes to
at least one layer. The job is to find the *active* layers (most real questions hit 2–4),
not to declare a question unanswerable.

---

## 1. Decompose any question onto L0–L7

Cross-reference the cue table in `SKILL.md`. Below, each layer is expanded with 3–5 example
phrasings so you can pattern-match fast.

### L0 — Valence / normativity (`b_k` field)
Not refused, not answered in the absolute. A "should/good/bad/fair/just" question is
converted to a *positive prediction of the valence field `b_k` across blocks*. See §2 (the
Normativity Rule) below.
- "Is rising inequality good or bad?"
- "Should the minimum wage be raised?"
- "Is it fair that landlords profit from scarcity?"
- "Do billionaires deserve their wealth?"
- "Is gentrification a good thing for a city?"

### L1 — Slow stocks (lethain / systems-dynamics)
Demographics, debt, fiscal capacity, wages, firm/industry accounting; comparative statics over
parameters `θ_S`. The quiet, reliable core. Build a stock-and-flow model.
- "Can the city afford to fund this program?"
- "How do wages keep up with the cost of housing?"
- "What happens to the deficit if we cut this tax?"
- "Why does this subsidy program run out of money?"
- "Is the pension fund solvent in twenty years?"

### L2 — Attention transport
Concentration of salience; preferential attachment / rich-get-richer; bubble *formation* as
attention over-concentration. Conserved carrier, belief = drift.
- "Why did this stock/coin go parabolic?"
- "Is this a bubble or real demand?"
- "Why does everyone suddenly care about X?"
- "How did this go viral / become winner-take-all?"
- "Is attention to this topic concentrating or dispersing?"

### L3 — Blocks (community structure, N_eff)
Which communities; `N_eff` (Kuramoto/Kish, NOT Pearson-of-fluctuations); synchronization;
contagion across blocks.
- "Will this spread from one community to the whole market?"
- "Is everyone really moving together or is it one tribe?"
- "Are these 'harbinger' customers correlated?"
- "How many independent groups are actually deciding here?"
- "Is this herding or independent judgment?"

### L4 — Reflexivity / MFG
Self-fulfilling/self-defeating; announcements as control inputs; coordination games; publishable
forecast = fixed point. Monotone(congestion) ⇒ unique; imitative ⇒ multiple/bistable.
- "If the Fed announces X, what happens?"
- "Is this a self-fulfilling prophecy?"
- "Will forward guidance be credible / anchor expectations?"
- "Do people vote for the winner *because* they expect them to win?"
- "Will publishing this forecast change the outcome?"

### L5 — Criticality / early-warning
Transitions, collapse, cascades; rising variance + lag-1 autocorrelation + cross-block synchrony
as precursors — WITH limits (prosecutor's fallacy; N-/R-tipping have no warning).
- "Are we heading toward a recession / crash / collapse?"
- "Is the system at a tipping point?"
- "Will this contagion cascade?"
- "Is a panic about to start?"
- "How close are we to a runaway transition?"

### L6 — Observation / data
Observation operator `y = H(Ξ) + ε`; data integrity (biased/adversarial observation); and
**data acquisition** — go fetch the number (WebSearch/WebFetch) and cite it.
- "Exactly how much of X is caused by Y?"
- "What do the statistics actually show?"
- "Is the official number lying / mismeasured?"
- "What's the current value of this indicator?"
- "How is this even measured?"

### L7 — Prime Radiant (synthesis)
Always runs last. Ties active layers into one model + forecast, emits skill horizon, confidence,
falsifiers, scope. "LLM'd and lethained." Not cued by words — it is the closing step.

---

## 2. THE NORMATIVITY RULE (L0) — stated carefully

A "should / good / bad / fair / just / deserve" question is **never refused** and is **not
answered in the absolute.** It is converted to a *positive prediction of the valence field
`b_k` across blocks*: predict which tribes will judge the thing good vs bad and **why**, state
the structural-necessity facts, and give the stability implications. The output is a **per-block
valence table, not a verdict.**

Why this is legitimate and not a dodge: under R1, valence is a non-conserved order parameter that
rides on the attention measure — it is a real, predictable field, just one that takes different
signs in different blocks. "Good or bad" is therefore a **classifier over (block, scale)**, and a
classifier is exactly the kind of object a positive model predicts.

### Worked example — "Is rising inequality good or bad?"

**(a) Structural fact (the necessity layer).** Inequality is *guaranteed*. No society equalizes
everyone to the king / president / founder; some dispersion of resources and status is a fixed
point of every observed social structure. So the question is never "inequality vs no inequality" —
it is "where does the level sit and who reads that level which way."

**(b) Per-block valence.** Predict the sign of `b_k` per block:

| Block | Reads rising inequality as | Why (structural) |
|---|---|---|
| Capital-holding blocks | **positive** | their stock grows; the level *is* their return |
| Meritocratic-ideology blocks | **positive** | inequality reads as a signal that effort/talent is rewarded |
| Wage-labor blocks | **negative** | their relative position falls; rising prices outrun wages |
| Egalitarian-ideology blocks | **negative** | violates the fairness norm that anchors the block's identity |

**(c) Scale dependence (the sign flips with block size).** This is the load-bearing subtlety.
At **family / small-tribe** scale, low inequality is the norm and high inequality *destabilizes*
(a household where one member hoards is dysfunctional). At **nation** scale, *some* inequality is
**load-bearing** for the incentive structure — flatten it entirely and the engine that allocates
effort stalls. So the sign of the valence **flips with block size**: the same fact is destabilizing
at small scale and structurally necessary at large scale.

**(d) The verdict is a classifier, not a value.** "Good/bad" is thus predictable with enough data:
it is a function of (block, scale). **Output a per-block valence table plus the scale-flip note —
never a single good/bad ruling.** If pressed for "the answer," the answer is the distribution and
its stability implications (e.g. "negative valence concentrated in wage-labor blocks + rising
cross-block synchrony ⇒ pre-critical for redistribution conflict").

---

## 3. INSTITUTIONAL questions → L1 + qualitative reasoning ("LLM'd and lethained")

Example: *"Why do military commissaries succeed where municipal groceries fail?"*

Route to **L1 (slow stocks)** plus qualitative LLM reasoning over the incentive structure. Build a
small **systems stock-flow comparison** of the two institutions and reason over what differs:

| Dimension | Military commissary | Municipal grocery |
|---|---|---|
| Funding (stock) | appropriated subsidy + captive demand | thin margin, must self-fund |
| Scale / buying power | national procurement, bulk | single-store scale |
| Customer base | fixed, eligibility-gated, predictable flow | open, variable, must compete |
| Objective function | retention/morale benefit, not profit | profit or political survival |
| Failure cost | absorbed by the larger institution | store closes |

The insight is the *difference in incentive structure and the stocks that back it*, not a magnitude.
This is exactly the kind of synthesis the Prime Radiant (L7) produces. **Scope = PARTIAL** (structure
modeled; exact magnitudes — actual subsidy size, margin, foot traffic — need data, which would push
the relevant sub-question to L6).

---

## 4. DATA questions → L6 (acquire and cite)

Example: *"Exactly how much of housing unaffordability is caused by immigration?"*

Route to **L6**, which **acquires** the data (WebSearch/WebFetch) and cites it. The word "exactly"
plus a requested magnitude is the tell: this is an observation-operator question, answerable only by
fetching a number.
- **Scope = NEEDS-DATA** until acquired.
- After acquisition, the verdict upgrades to **PARTIAL / MODELED** depending on how cleanly the number
  maps onto the model (a single cited elasticity ⇒ PARTIAL; a well-identified decomposition ⇒ MODELED).
- Always cite the source URL in the `DATA ACQUIRED` line of the reading. Flag data integrity if the
  source is biased or adversarial (that is the other half of L6).

---

## 5. Pure accounting tautologies / jokes → touch only H

Example: *"Did my \$5 slap raise GDP?"*

These touch **only the observation operator H** — a definitional/accounting question about how a
quantity is *defined and measured*, not about any dynamics. (GDP is a measurement convention; whether
a transaction is "counted" is a property of H, not of the forward model M.)
- **Recommendation: DROP from a serious coverage run.** It exercises no dynamics — no transport, no
  blocks, no reflexivity, no criticality — so it teaches the engine nothing and consumes a slot.
- But *explain why* when you drop it: it is a question about `H`, the definitional map, not about `Ξ`'s
  evolution. (If someone insists, the honest one-liner is: "yes, by the definition of GDP as the sum of
  final expenditures — this is a tautology about the accounting identity, not a prediction.")

---

## 6. The four scope verdicts (1-line decision rule each)

| Verdict | Decision rule |
|---|---|
| **MODELED** | The active layers are fully specified and the model gives a forecast/structural claim with a stated skill horizon — no missing number blocks the answer. |
| **PARTIAL** | The *structure* is modeled (mechanism, signs, comparative statics) but exact magnitudes require data not in hand — answer the shape, flag the gap. |
| **NEEDS-DATA** | A specific number is required to answer at all and is not yet acquired — L6 must fetch it; until then, state what number would resolve it. |
| **NORMATIVE-AS-VALENCE** | The question is a should/good/bad/fair query — resolve per block as a valence table (§2), never in the absolute. |

(A question can move verdicts mid-reading: a NEEDS-DATA question becomes PARTIAL/MODELED once L6
acquires the number.)

---

## 7. Five worked classifications (representative r/AskEconomics posts)

### P1 — Bubble question
> "Bitcoin just doubled in a month. Is this a bubble or real adoption?"

- **Active layers:** L2 (attention over-concentration = bubble formation), L4 (reflexivity —
  price rise pulls in buyers who expect further rises), L5 (criticality — is it pre-crash?).
- **Dominant mechanism:** endogenous attention concentration with a reflexive price–belief loop.
- **Reading:** distinguish monotone/fundamental drift from imitative cascade; check cross-block
  synchrony (is it one crypto block or has it jumped to retail generally?). Bubble = imitative regime,
  bistable, no unique fixed point.
- **Scope: PARTIAL** (mechanism diagnosable; "will it crash and when" is branch-unpredictable near
  criticality — forecast the transition risk, not the date).

### P2 — Collapse-prediction question
> "Is the US heading toward a recession in the next year?"

- **Active layers:** L1 (slow stocks — debt, employment, fiscal), L5 (criticality / early-warning),
  L6 (acquire current indicators).
- **Dominant mechanism:** slow-stock drift plus proximity to a critical transition.
- **Reading:** report early-warning state (rising variance / autocorrelation / cross-block synchrony)
  as a *state variable*; forecast *that* a transition is near, not which branch. Flag prosecutor's-
  fallacy and the N-/R-tipping blind spots (some recessions have no precursor).
- **Scope: NEEDS-DATA** (current indicator values must be fetched), → PARTIAL once acquired.

### P3 — Inequality good/bad question
> "Is it bad that the top 1% own so much?"

- **Active layers:** L0 (valence), L2 (attention/wealth concentration as a transport phenomenon),
  L1 (stocks behind the distribution).
- **Dominant mechanism:** normative query resolved as a per-block valence field.
- **Reading:** apply the Normativity Rule (§2) — structural fact (concentration is guaranteed),
  per-block valence table, scale-flip note. Output the table, not a verdict.
- **Scope: NORMATIVE-AS-VALENCE.**

### P4 — Fiscal-comparison question
> "Would a flat tax raise or lower total revenue versus the current brackets?"

- **Active layers:** L1 (slow stocks — revenue, the tax base), L6 (elasticities / base data),
  L4 (mild reflexivity — behavioral response to rates, the Lucas point).
- **Dominant mechanism:** comparative statics over `θ_S` (tax parameters) on the revenue stock,
  adjusted for behavioral response.
- **Reading:** build the stock-flow revenue model; the sign depends on the labor/avoidance elasticity,
  which is a number to fetch.
- **Scope: NEEDS-DATA** (elasticity), → PARTIAL once acquired (resolution capped by elasticity
  uncertainty).

### P5 — Institutional question
> "Why do credit unions survive when their members could get better rates at big banks?"

- **Active layers:** L1 (stocks — capital, scale, member deposits), L3 (block — members as a
  cohesive community), plus qualitative incentive reasoning.
- **Dominant mechanism:** institution-as-block with a non-profit objective function and member
  loyalty lowering churn.
- **Reading:** stock-flow comparison vs a commercial bank (objective function, cost of capital,
  customer stickiness as a block-cohesion effect); "LLM'd and lethained" over the incentive structure.
- **Scope: PARTIAL** (structure modeled; exact rate/retention magnitudes need data).

---

## 8. Quick routing checklist

1. Scan for L0 cue words (should/good/bad/fair/just) → if present, this is **NORMATIVE-AS-VALENCE**;
   build the per-block table, do not rule.
2. Scan for a requested magnitude ("exactly how much", "what's the number") → L6, **NEEDS-DATA**.
3. Scan for dynamics cues (bubble/spread/collapse/expect/self-fulfilling) → L2/L3/L4/L5; run the
   engine for transport / block / criticality.
4. Scan for slow-stock cues (afford/wages/deficit/revenue) → L1; build the stock-flow model.
5. If it is a pure accounting tautology / joke (touches only H) → recommend **DROP**, explain why.
6. Always close with L7: synthesize active layers, emit skill horizon + confidence + falsifiers +
   one of the four scope verdicts.
