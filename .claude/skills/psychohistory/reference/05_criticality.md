# L5 — Criticality, early warning, and its limits

**Role.** Handle transitions, collapses, cascades, panics. Near a critical point
forecasting *of the branch* becomes impossible while **forecasting of the
transition** and **control leverage** both become possible. This layer carries the
framework's strongest anti-overclaim discipline: most "I see the warning signs"
claims are wrong for stateable reasons, and you must say so.

---

## 1. What goes critical

The weak-coupling regime (L3) has a **correlation length**

```
xi ~ |theta - theta_c|^{-nu}
```

that **diverges** as the control parameter `theta` approaches its critical value
`theta_c` (here driven by coupling `W`). At that point:

- `N_eff` collapses `K → 1` (L3): the K blocks act as **one** unit.
- **MFG fixed-point repair fails:** cascades are *non-equilibrium* events; the
  forward/backward MFG system (L4) assumes a settled distribution, so "publish the
  fixed point" is no longer valid mid-cascade.
- **Conservation survives but loses constraining power:** total attention is
  still conserved (L2), but knowing the total tells you almost nothing about the
  *configuration* when everything is correlated. The constraint stops constraining.

This is the engine's `run_blocks` near `W ≈ 0.4` (L3's transition) and beyond.

---

## 2. Early-warning signals (EWS): critical slowing down

Approaching a **fold (saddle-node) bifurcation**, the system recovers from
perturbations ever more slowly → **critical slowing down**, which shows up as:

- **rising variance**,
- **rising lag-1 autocorrelation**,
- **rising cross-block correlation** (blocks start moving together).

Theory: **Wissel (1984, *Oecologia* 65:101)**; popularized as resilience
indicators by **Scheffer et al. (2009, *Nature* 461:53)**; toolkit and method
detail in **Dakos et al. (2012, *PLoS ONE*)**.

**The AR(1) intuition.** Model the macro variable as `x_{t+1} = alpha·x_t +
noise`. As the bifurcation nears, `alpha → 1`:

```
Var = sigma^2 / (1 - alpha^2)  → ∞          (variance blows up)
AC(1) = alpha                  → 1          (autocorrelation → 1)
```

So **rising variance + rising lag-1 autocorrelation** are the operational EWS.
Engine handle: watch `Var_t(population mean sign)` rise and `block_metrics`'
`rbar`/synchrony rise as `W` increases toward the transition.

---

## 3. MUST-STATE LIMITS (anti-overclaim — do not skip)

EWS are **only** valid for slow **bifurcation (B-)tipping**. State every limit:

- **Prosecutor's fallacy — Boettiger & Hastings (2012, *Proc. R. Soc. B*
  279:4734).** Selecting a series *known to have tipped* and then "finding" the
  warning signal **conditions on the outcome**. `P(signal | transition) ≠
  P(transition | signal)`. Without a **null model** and a **base rate** you have
  shown nothing. **Always demand a null + base rate before claiming an EWS.**
- **Noise-induced (N-)tipping has NO slowing down — Boettiger & Hastings
  (2013).** A large noise excursion can flip a stable system across a basin
  boundary with **no rising variance/autocorrelation beforehand.** EWS are blind
  to it.
- **Rate-induced (R-)tipping has no bifurcation and no warning — Ashwin et al.
  (2012).** If `theta` itself moves too fast, the system tips because it *can't
  keep up*, with **no bifurcation crossed** and **no precursor.** EWS are blind
  to it.

> **Rule:** EWS apply to slow B-tipping only. **N-tipping and R-tipping are
> explicit blind spots** — name them every time you discuss warning signals. Do
> not claim a warning signal without (a) a null model, (b) a base rate, and (c) a
> check that the mechanism is B-tipping and not N-/R-tipping.

---

## 4. The prediction–control duality

The **susceptibility** (response to a small forcing) diverges at criticality:

```
chi ~ |theta - theta_c|^{-gamma}              and, fluctuation–dissipation,
chi = Var(m) * N / T
```

The **same divergence** does two opposite things:

- it **kills prediction** (tiny perturbations produce macroscopic, branch-
  selecting swings — the forecast horizon → 0), and
- it **maximizes control leverage** (a tiny, well-timed intervention moves the
  whole system).

So at criticality the skill performs a **regime switch**: from *prediction* to
**minimal-intervention control** — stop forecasting the branch, intervene to
select it. This is the same monotone↔imitative boundary as L4: where the unique
fixed point dissolves into a bistable one is where chi diverges.

**Canonical example.** The **SVB Sunday deposit-guarantee** (March 2023): with a
run underway (imitative regime, chi large, no skill in predicting which depositors
flee), the high-leverage move was a single control input — guarantee deposits —
that selected the no-run fixed point (L4's engineered fixed point /
Diamond–Dybvig). Minimal intervention, maximal effect, precisely because chi was
diverging.

---

## HOW THE SKILL USES THIS LAYER

- [ ] If cue words hit (collapse, crash, recession, tipping, contagion, panic,
      runaway, "heading toward"): activate L5.
- [ ] **Compute** with `engine.run_blocks` + `engine.block_metrics`: watch
      `neff_correct` collapse toward 1, `S`/`rbar` rise, and rising
      `Var_t(population mean)` as the coupling/`theta` approaches `theta_c`.
- [ ] **Compute the skill horizon** with `engine.skill_horizon(K, W)`; report it
      shrinking as W → critical. Near criticality report "no horizon for the
      branch — forecast the transition, not the branch."
- [ ] **Run the EWS checklist honestly:** rising variance + lag-1 autocorr +
      cross-block correlation = candidate B-tipping warning **only if** you have
      a null model + base rate, and **only if** the mechanism is B-tipping. State
      that **N-tipping and R-tipping give no warning** (explicit blind spots).
- [ ] At criticality, **switch objective to control:** chi diverges, so report
      the **minimal-intervention** lever (the engineered fixed point, SVB/
      Diamond–Dybvig style) instead of a point forecast.
