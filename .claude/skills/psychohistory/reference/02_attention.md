# L2 — Attention transport: the conservation / drift layer

**Role.** This is the carrier layer. It models *where collective attention goes*:
concentration of salience, virality, preferential attachment, and the **formation**
of bubbles as attention over-concentrating on one node. The defensible conserved
object here is a **normalized probability density**, and **belief is its drift field**
— not a second conserved stock.

---

## 1. Attention as an approximately conserved measure

On sub-generational timescales the supply of collective attention is bounded:

```
A = N * hbar * wbar         N people, hbar hours/person/day awake-and-online,
                            wbar items attendable per hour
```

`A` is fixed on the relevant horizon, so attention allocation is **zero-sum
reallocation**: a topic gains salience only by taking it from others (Wu &
Huberman 2008, *novelty decay of collective attention*). Total salience does not
grow when a topic goes viral; it redistributes. This is what makes "conservation"
a usable modeling primitive rather than a metaphor.

Normalize to a density `rho(x,t)` over a space of topics/agents/positions `x`,
with `∫ rho dx = 1`. Conservation = this integral is invariant.

## 2. The continuity equation (transport with belief as drift)

```
∂rho/∂t + div J = s            (s = sources/sinks; s = 0 on the conserved core)
J = rho*v  -  D*grad(rho)  +  rho*b
   └ advection   └ diffusion      └ belief drift
```

- `v` — exogenous transport (what the algorithm/feed pushes).
- `D` — diffusion (random exploration, spreading of attention).
- `b` — **belief drift**: an endogenous field that biases flow. **Belief is a
  drift on the conserved carrier, NOT a conserved stock of its own.** You do not
  get a second continuity equation for belief; you get a force term.

When `s = 0`, integrating over the whole space gives `d/dt ∫ rho dx = 0`:
mass is conserved regardless of how violent `b` is. That is the structural
guarantee the skill leans on.

## 3. Preferential attachment = endogenous drift = inequality-as-concentration

Model rich-get-richer / winner-take-all as a **gradient drift**:

```
b = -grad(Phi)              Phi = attention potential (popularity well)
```

A node that is already salient deepens its own well, so `b` points toward it and
attention concentrates there. This is the mechanism for:

- **inequality as CONCENTRATION** (a few nodes hold most of the density), and
- **bubble FORMATION** (attention over-concentrates *before* price/belief
  follows). Bubble *bursting* is an L5 (criticality) event; **formation lives
  here.**

Concentration here is conservative: it redistributes a fixed mass, it does not
create it. That is exactly why "everyone is talking about X" can be true while
total attention is flat.

## 4. Graph discretization → master equation (the engine's L2)

Discretize `x` onto nodes of a graph with adjacency `A`. Attention shares
`p ∈ R^n` (with `1ᵀp = 1`) evolve by a **master equation**:

```
dp/dt = Lᵀ p ,     L = generator with ROW SUMS = 0
```

Row-sum-zero is the discrete continuity equation: it **structurally conserves
mass** `1ᵀp`. Belief drift is an extra inflow rate `bias` along a target node's
edges (`rate_matrix(A, bias_node=…, bias=…)`).

> **Verified (E2).** Mass error stays ~3.3e-16 (machine precision) over the whole
> run, *while* belief drift concentrates the biased node's share from 0.025 (≈
> uniform 1/40) to 0.221. Concentration without creation. Cite as engine behavior,
> never as empirical validation.

`engine.py`: `rate_matrix(A, base, bias_node, bias)` builds `L`;
`integrate(L, p, T, dt)` runs `dp/dt = Lᵀp` and conserves `1ᵀp`.

---

## 5. CRITICAL CORRECTION — softmax normalization is NOT a conservation law

State this plainly whenever attention "conservation" comes up:

- The transformer/softmax constraint `Σ_j alpha_ij = 1` (attention weights of a
  query summing to one) is an **instantaneous algebraic CONSTRAINT**, not a
  conservation law. There is **no dynamically-determined flux**, **no continuity
  equation**, and **no Noether symmetry** behind it. It is renormalized fresh at
  every step; nothing flows from one place to another.
- **Never call softmax normalization a conservation law.** It is the single
  easiest overclaim in this whole framework.

The **defensible** reading is the kinetic / Fokker–Planck one:

- **Toscani (2006, *Commun. Math. Sci.* 4:481)** — a kinetic-Fokker–Planck model
  in which **attention is a conserved normalized probability density** and
  **belief enters as its drift**. This is the rigorous version of §2–§4 and the
  legitimate source of the word "conserved" here.
- The conserved object is a *density / order-1 measure*. The **valence /
  magnetization** order parameter (the L3/L4 "which way is the crowd leaning")
  is a **NON-conserved order parameter** — it can be created and destroyed.
- This is the **Model B (conserved density) vs Model A (non-conserved order
  parameter)** distinction of **Hohenberg & Halperin (1977, *Rev. Mod. Phys.*
  49:435)**, applied to social dynamics by **Castellano, Fortunato & Loreto
  (2009, *Rev. Mod. Phys.* 81:591)**. Attention density ≈ Model B (conserved);
  belief/valence ≈ Model A (not conserved).

So: **attention density is conserved (transport/Model B); belief/valence is a
drift and a non-conserved order parameter (Model A).** Keep the two separate.

---

## HOW THE SKILL USES THIS LAYER

- [ ] If cue words hit (bubble, hype, viral, attention, concentration, winner-
      take-all, inequality-as-concentration): activate L2.
- [ ] **Compute** the transport: build `L = rate_matrix(A, bias_node=…, bias=…)`
      and run `integrate(L, p0, T, dt)`. **Report** the share of the target node
      over time (concentration) and confirm `1ᵀp` is conserved (mass error ≈ 1e-16).
- [ ] Frame bubble **formation** and inequality as **concentration of a fixed
      mass** driven by drift `b = -grad(Phi)` (preferential attachment). Bursting
      is L5, not here.
- [ ] **Say the conservation correctly:** "conserved normalized probability
      density (Toscani / Model B), belief as drift." **Never** "softmax is a
      conservation law." Belief/valence is the non-conserved order parameter.
- [ ] Hand the drift field `b` to L4 (it becomes `v = -grad_p H`, the FP drift)
      and the concentration pattern to L3/L5 (which blocks are converging).
