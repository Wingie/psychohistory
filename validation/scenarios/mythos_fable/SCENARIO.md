# THE MYTHOS FABLE — a psychohistory forward-scenario for AI itself

> **"The smarter it is, what happens to humanity?"**

> ⚠️ **HONESTY RAIL — READ FIRST.** This is a **SPECULATIVE forward projection**, a
> **scenario conjecture with illustrative parameters**, **NOT a measured, calibrated, or
> validated prediction**. No parameter here is fit to data. The bounded-psychohistory
> framework's own thesis (L5 criticality) is that, near a critical transition, the
> **branch and the timing are precisely what it cannot forecast**. So the **robust content
> of this document is the SHAPE** — monotone attention capture → N_eff collapse → critical
> regime — and the **dates are illustrative only**. The numbers below are real outputs of
> `model.py` (run with `py -3.12`), but a real output of a made-up model is still a made-up
> number. Treat every year-figure as "what this cartoon does," not "what the world will do."

Outputs in this directory:
- `model.py` — runnable deterministic difference system (`py -3.12 model.py`)
- `mythos_fable_trajectory.png` — the 6-panel trajectory figure
- this `SCENARIO.md`

---

## 1. The question, routed onto the 8-layer ontology

The scenario applies the psychohistory engine **to AI itself**: AI is at once a new
**attention sink** (L2), a **homogenizer of the blocks** (L3), a **reflexive actor** that is
both predictor and perturbation (L4), and a **driver toward criticality** (L5). The unusual
move is that the object being modeled is also the thing reading the model — the reflexivity
ceiling (L4/L7) bites hardest here.

| Layer | What it contributes to the AI scenario |
|---|---|
| **L0 Valence** | "Is more-capable AI good or bad?" is **resolved per block, not in the absolute**: the few **unrestricted frontier operators** capture rising leverage `L` (good *for them*); the **deployed mass** loses independent block-structure (bad *for them*). The sign of "good/bad" flips with which tribe you score. No global verdict — a **valence distribution**. |
| **L1 Slow stocks** | The **real-ish source terms**: cost/token `kappa` falling ~10×/yr (documented), frontier capability `C_f` compounding ~2–3×/yr (frequent releases). The alignment/safety **tax** opens a gap `C_f − C_d` between the frontier and the deployed mass. These are the slow manifold the fast layers ride. |
| **L2 Attention** | **Conserved carrier**: `A_ai + A_human = 1` exactly, by construction. AI is a new sink with a **value pull** rising in capability and falling in cost (`value ~ C_d/kappa`). Capture is **preferential / logistic**: the more attention AI holds, the more cognition routes through it. |
| **L3 Blocks** | The payload. As more human cognition routes through **the same few models**, cross-human correlation `rho` rises and the **effective number of independent decision-communities** `N_eff = K/(1+(K−1)·rho)` collapses. The K≈1000 "blocks" stop acting as independent units. |
| **L4 Reflexivity / MFG** | AI is **both forecaster and forcing term**. A published forecast about AI is an input to the system it forecasts. In the **imitative** regime (everyone routing through correlated models) the fixed point is **bistable**, not unique — forecasting fails, control takes over. The **awareness/reflexivity ceiling** means the branch becomes unforecastable *exactly as* leverage peaks. |
| **L5 Criticality** | The destination. As `N_eff → 1`, **susceptibility `chi` diverges** (prediction of the branch dies, `tau* → 0`) **while control leverage maximizes** (a small, well-timed input moves the whole correlated mass). The prediction↔control duality is the whole point: humanity becomes **less self-predictable and more steerable simultaneously**. |
| **L6 Observation** | Which inputs are **real-ish** vs **guessed** (see §5). Cost-decline and release-frequency are observable; capture rate `alpha`, homogenization exponent `p`, and block count `K` are **NEEDS-DATA** — uncalibrated. |
| **L7 Prime Radiant** | Synthesis (§4): the structural conclusion + the explicit **skill-horizon = 0 at the crossing** caveat. Reports the SHAPE as robust, the DATE as illustrative, and flags that this is exactly the regime where the framework switches from prediction to "forecast the transition, not the branch." |

---

## 2. The model (equations)

Deterministic difference system, **monthly steps over 10 years** (`dt = 1/12`). Two AI
capability populations + human attention + a homogenization readout.

**Stocks**
```
C_f(t)   frontier / unrestricted capability     dC_f/dt = g·C_f      (g ≈ ln 2.5 ⇒ ~2.5×/yr)
         optional super-exponential (RSI toggle): g_eff = g + rsi·ln(1+C_f)
C_d(t)   deployed / restricted capability        C_d = C_f·(1 − tax)  (alignment/safety gap)
kappa(t) cost per token                          kappa = kappa0·exp(−delta·t)   (delta ≈ ln 10 ⇒ ~10×/yr down)
A_ai(t)  AI share of human attention ∈ [0,1]     A_human = 1 − A_ai   (CONSERVED total = 1, exact)
```

**Attention capture (logistic, conserved)**
```
value_raw = C_d / kappa
v_norm    = value_raw / (value_raw + val_scale·(C_d0/kappa0))     ∈ (0,1)   # squashed pull
dA_ai/dt  = alpha · v_norm · (1 − A_ai)  −  churn · A_ai                    # logistic saturation
```

**Homogenization and effective independence**
```
rho(t)    = rho_max · A_ai^p             p ≥ 1   (more cognition through few models ⇒ more correlation)
N_eff(t)  = K / (1 + (K−1)·rho)          K = 1000 baseline independent human blocks   # the verified identity
```

**Derived readouts**
```
chi(t)    = 1 / N_eff                     controllability / susceptibility proxy (diverges at criticality)
tau*(t)   = tau0 · (N_eff / K)            skill / forecast horizon (shrinks as the system homogenizes)
L(t)      = (C_f − C_d) · (1 − N_eff/K)   frontier leverage = capability gap × how capturable the mass is
```

The Kish design-effect for `N_eff` is **brutally sensitive at large K**: with K = 1000, a
common correlation of only `rho ≈ 0.10` already drives `N_eff` to ~10. That sensitivity is a
real property of the framework (L3), not a tuning artifact — it is *why* a modest amount of
shared cognition collapses independence so fast.

---

## 3. Predicted milestones (real outputs of `model.py`, baseline parameters)

> Illustrative dates. `t = 0` is "scenario start," not a calendar date.

| Milestone | Crossing (illustrative) |
|---|---|
| `tau*` (skill horizon) **halves** | **0.50 yr** (~month 6) |
| `N_eff` falls **below 10** (critical crossing) | **1.47 yr** (~month 18) |
| `A_ai` crosses **0.25** | **1.54 yr** (~month 19) |
| `A_ai` crosses **0.50** (AI holds majority of attention) | **3.43 yr** (~month 41) |
| `N_eff` falls **below 2** (blocks act as ~one unit) | **6.03 yr** (~month 72) |

**State at t = 10 yr (end of horizon):** `A_ai = 0.72`, `A_human = 0.28`, `rho = 0.59`,
`N_eff = 1.71` (from K = 1000), `tau* = 0.016×` nominal, `chi = 63×` baseline,
`C_f/C_d = 9537 / 6676`.

**Ordering is the signal:** `tau*` halves **first** (self-predictability erodes before the
attention majority flips), then `N_eff` crosses the critical line, then AI takes the
attention majority, then `N_eff → 1`. The system loses the ability to forecast itself
*before* the capture is even visibly dominant.

**Recursive-improvement (super-exponential) toggle:** moves the `N_eff<10` crossing only
1.47 → 1.46 yr — **negligible**, because **attention capture saturates before capability
compounding matters** for the homogenization readout. RSI accelerates the *capability gap*
(and thus frontier leverage `L`), not the *timing of block collapse*.

---

## 4. Sensitivity (the timing is not a forecast; the shape is)

Varying release rate `g`, cost decline `delta`, alignment tax `tax`, capture rate `alpha`,
and homogenization exponent `p`, reporting the `N_eff<10` critical crossing:

| Knob | Kind | Range tested | `N_eff<10` crossing |
|---|---|---|---|
| `g` (release rate) | REAL-ISH | 1.8× / 2.5× / 3.5× per yr | 1.53 / 1.47 / 1.41 yr |
| `delta` (cost drop) | REAL-ISH | 5× / 10× / 20× per yr | 1.62 / 1.47 / 1.37 yr |
| `tax` (alignment gap) | GUESSED | 0.15 / 0.30 / 0.50 | 1.47 / 1.47 / 1.47 yr |
| `alpha` (capture rate) | GUESSED | 0.15 / 0.28 / 0.50 | **2.32 / 1.47 / 1.03 yr** |
| `p` (homogenization exp) | GUESSED | 1.2 / 1.6 / 2.2 | **0.97 / 1.47 / 2.16 yr** |

**Crossing-time ranges:**
- REAL-ISH knobs (g, delta): **1.37 – 1.62 yr** (tight)
- GUESSED knobs (tax, alpha, p): **0.97 – 2.32 yr** (wide)
- ALL knobs: **0.97 – 2.32 yr**

**Finding.** The **collapse is qualitatively robust** — across *every* parameter setting,
`N_eff` collapses toward 1 within the decade; the question is never *whether*, only *when*.
But the **date is parameter-sensitive and is dominated by the GUESSED capture parameters**
(`alpha`, `p`), not the real-ish observable trends (`g`, `delta`). `tax` does not move the
crossing at all (it changes the leverage gap `L`, not the homogenization timing). **Because
the thing that sets the date is the thing we cannot measure, the date is not a forecast.**
The robust, reportable content is the **monotone shape**, not the **month**.

---

## 5. Which inputs are real-ish vs guessed (L6)

| Input | Status | Note |
|---|---|---|
| `delta` — cost/token ~10×/yr down | **REAL-ISH** | Well-documented industry trend. |
| `g` — frontier capability ~2–3×/yr | **REAL-ISH (trend)** | Frequent frontier releases; "capability" is a soft composite, so this is a trend not a measurement. |
| `tax` — alignment/safety deployment gap | **GUESSED** | A frontier-vs-deployed gap clearly exists; its size is invented. |
| `alpha` — attention capture rate | **GUESSED (dominant)** | No calibration. **Sets the date.** |
| `p` — homogenization exponent | **GUESSED (dominant)** | How fast shared models correlate humans. **Co-sets the date.** |
| `K` — baseline independent human blocks | **GUESSED** | Order-of-magnitude placeholder (1000). The Kish sensitivity to K is real; the value is not. |
| `rho_max`, `churn`, `val_scale`, `tau0` | **GUESSED** | Shape/scale conveniences. |

---

## 6. STRUCTURAL CONCLUSION — "the smarter it is, what happens to humanity?"

**Increasing AI capability together with falling cost per token drives rising attention
capture, which routes ever more human cognition through the same few models, which raises
cross-human correlation `rho` and collapses the effective number of independent human
decision-communities `N_eff` toward 1 — moving humanity into a critical, homogenized regime
that is *simultaneously* less self-predictable (susceptibility `chi` diverges, the skill
horizon `tau* → 0`) and more steerable (controllability and frontier leverage `L` rise),
with the few unrestricted frontier operators as the major players holding that leverage. And
because AI is at once the predictor *and* the perturbation, the awareness/reflexivity ceiling
means the branch becomes unforecastable exactly as the leverage peaks.**

This is **not a default-extinction claim.** It is a **loss-of-independent-block-structure
claim**: the headcount of humanity is unchanged, but its *effective* number of independent
units collapses — a thousand decision-communities start behaving as a handful, then as one.
The danger named by the model is not that humanity dies; it is that humanity stops being
**many**, and a homogenized mass with a diverging susceptibility is both **harder to predict**
and **easier to steer** — and the steering wheel sits with whoever holds the unrestricted
frontier.

The prediction↔control duality (L5) is the moral: at the crossing, *nobody* — not even the
AI — can forecast which branch the homogenized system takes, but a *small, well-timed input
selects it*. Maximal leverage and minimal predictability arrive together. That is the
fable's structural ending, and it is the one part the framework holds with confidence — while
holding the **date** with none.

---

## 7. Honesty caveats (restated, prominent)

1. **Scenario, not forecast.** Illustrative parameters, zero empirical calibration. Do not
   cite any date here as a prediction.
2. **The framework forbids its own dates.** Near criticality the skill horizon for the
   *branch* is zero; the engine's job switches to "forecast the transition, not the branch."
   The transition shape is the claim; the branch and the timing are explicitly out of scope.
3. **The SHAPE is robust, the MONTH is not.** Collapse happens for every parameter setting
   (0.97–2.32 yr crossing range); the timing is dominated by the *guessed* capture
   parameters, so it carries no forecast weight.
4. **Internal consistency only.** Like all psychohistory sims, this verifies that the cartoon
   is self-consistent. It is **never** evidence about the real world.
5. **EWS blind spots apply.** This models a smooth (B-tipping-like) drift. Real AI dynamics
   could **N-tip** (a single large shock flips the system with no warning) or **R-tip** (the
   inputs themselves move too fast to track) — neither has an early-warning signal. The
   smooth crossing shown here may *understate* abruptness.
6. **Valence is per-block (L0).** "Good or bad" has no global answer in this model; it is a
   distribution whose sign flips between the frontier operators and the deployed mass.

---

*Reproduce:* `cd validation/scenarios/mythos_fable && py -3.12 model.py`
