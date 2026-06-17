# L4 — Reflexivity: mean-field games and the fixed point of forecasting

**Role.** Model the loop where *the forecast changes the outcome*: self-fulfilling
and self-defeating prophecies, forward guidance, coordination games, bank runs,
bubbles. The publishable forecast is a **fixed point** of the prediction→reaction
map. The decisive question is whether that fixed point is **unique** (forecasting
works) or **multiple/bistable** (forecasting fails, control takes over).

---

## 1. Mean-field games (the reflexive engine)

**Lasry & Lions (2007, *Japan. J. Math.* 2:229)** — a continuum of small agents,
each best-responding to the *distribution* `m` of all agents. Equilibrium is a
coupled system:

```
HJB  (backward in time):   value function u, agents optimize against m
FP   (forward in time):    density m transported by the optimal control
```

- The **forward Fokker–Planck equation IS the continuity equation of the
  attention layer (L2)**, with drift `v = -grad_p H` (H the Hamiltonian). **State
  this identification explicitly:** it is what grounds L2's transport equation —
  the attention density's drift field `b` and the MFG's `v = -grad_p H` are the
  same object. L2 and L4 share one continuity equation.
- A **publishable forecast = MFG equilibrium = a fixed point of the
  prediction→reaction map** `T`: you publish `f`, agents react, the realized
  outcome is `T(f)`, and a self-consistent (publishable) forecast satisfies
  `T(f) = f`.

`engine.reaction(f, guarantee)` is the cartoon reaction map; `engine.fixed_points(g)`
returns the roots of `T(f) - f`.

---

## 2. THE UNIQUENESS CONDITION (the decisive split)

**Lasry–Lions monotonicity.** If the coupling `F(x,m)` satisfies

```
∫ ( F(x, m1) - F(x, m2) ) d(m1 - m2)  >=  0     for all m1, m2
```

then the MFG equilibrium is **UNIQUE**. Monotonicity is the **congestion /
strategic-substitutes** regime: agents **avoid the crowd** (a crowded choice
becomes less attractive). Unique equilibrium ⇒ **a single publishable forecast**.
Forecasting is well-posed.

**When monotonicity FAILS:** the coupling is **imitative / strategic
complements** — agents **pile into** the very thing the forecast points at
(bubbles, bank runs, manias; a crowded choice becomes *more* attractive).
Then there are **MULTIPLE / bistable equilibria**: a good one and a bad one
coexist, and which is realized depends on coordination/sunspots, not on
fundamentals.

> **Verified (E5).** The reaction map has a single high fixed point ~0.995 (run)
> with no guarantee and a single low fixed point ~0 with a deposit guarantee; at
> **nearby parameters a bistable 3-fixed-point regime appears** — exactly the
> imitative/run regime. Cite as engine behavior, not as proof about real banks.
> See **Bardi & Fischer (2019)** on non-uniqueness / multiplicity in MFG.

---

## 3. KEY SYNTHESIS — monotone vs imitative IS smooth vs critical

> The **monotone (unique, predictable)** vs **imitative (multiple, unpredictable)**
> split is the **SAME boundary** as the **smooth vs critical** split of L5.

- In the **monotone/congestion** regime: one fixed point, `N_eff` high, skill
  horizon long → **forecasting works**. Publish the fixed point.
- In the **imitative/complements** regime: multiple/bistable fixed points,
  `N_eff` collapsing (L3), critical slowing down (L5) → **forecasting fails and
  CONTROL takes over.** Stop trying to call the branch; intervene to select it.

This is the framework's central duality: the same parameter boundary that breaks
prediction is where intervention gains maximal leverage (see L5 §susceptibility).

## 4. Engineered fixed points (control)

When the bad equilibrium exists, you don't predict your way out — you **engineer
the fixed point**. **Deposit insurance (Diamond–Dybvig)** is the canonical move:
the guarantee shifts the reaction map so the run equilibrium **disappears**,
leaving only the no-run fixed point. In the engine this is the `guarantee` knob —
`reaction(f, guarantee=0.8)` collapses the fixed point from ~0.995 to ~0. The
announcement is a **control input**, not a forecast.

## 5. Blocks extension (multi-population / graphon MFG)

Real populations are not one mean field but **K coupled blocks** (L3). Use
**multi-population / graphon MFG — Caines & Huang (2018)**: each block is a
population with its own distribution, coupled through a graphon. This lets
reflexivity run *between* tribes (one block's run triggering another's) and ties
L4 back to L3's block structure.

---

## HOW THE SKILL USES THIS LAYER

- [ ] If cue words hit (expect, self-fulfilling, forward guidance, announce,
      credible, anchor, prophecy, vote-because-others, bank run, bubble):
      activate L4.
- [ ] **Locate the reaction map** `T(f)`: what does a published forecast do to
      the outcome? Use/adapt `engine.reaction(f, guarantee)`.
- [ ] **Decide the regime:** is coupling **monotone/congestion** (agents avoid
      the crowd → strategic substitutes) or **imitative/complements** (agents
      pile in)? This determines everything.
- [ ] **Find fixed points** with `engine.fixed_points(g)`. One root → unique
      publishable forecast (report it). Three roots → bistable → **switch from
      prediction to control.**
- [ ] If imitative/bistable: name the **engineered fixed point** that kills the
      bad equilibrium (deposit-insurance analogue) and treat the announcement as
      a control input. Cross-reference L5 for the prediction→control handoff.
- [ ] State plainly that the forward FP equation = L2's continuity equation
      (drift `v = -grad_p H`); for inter-block reflexivity use graphon MFG.
