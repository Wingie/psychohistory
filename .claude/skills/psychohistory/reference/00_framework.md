# 00 — Framework: condensed theory + Asimov canon mapping

This is the theory spine for the skill. It compresses the position paper
*Conditions for Predictable Social Dynamics* into the smallest set of load-bearing
claims, then maps each Asimov-canon concept to its real-math analogue. Read it once;
the per-layer modules (`01`–`07`) and the router (`08`) assume it.

---

## 1. The thesis

Numerical weather prediction (NWP) is the existence proof that a system of comparable
apparent difficulty to "society" can be forecast. It worked not because of compute but
because the atmosphere has three structural properties:

- **(P1) Conservation laws.** Mass, energy, momentum are conserved. Trajectories are
  confined to low-dimensional manifolds; the governing equations are licensed.
- **(P2) Effective decomposition (weak coupling at forecast scale).** Perturbations
  propagate at finite speed; ensemble statistics over quasi-independent regions are
  meaningful. No model tracks molecules; it tracks grid cells.
- **(P3) Non-reflexivity.** The atmosphere does not read the forecast. The hurricane does
  not reroute to spite the model.

The three classical objections to social prediction are exactly the negations of (P1)–(P3):

- **O1 (no conservation):** belief, legitimacy, salience appear freely creatable; without
  a continuity equation the state space is unconstrained.
- **O2 (reflexivity):** a published forecast is an input to the system it describes —
  Lucas critique (agents re-optimize against announced policy) and Goodhart (a measure
  that becomes a target stops being a good measure). Asimov encoded this as the secrecy
  requirement.
- **O3 (correlated agents):** mass media and recommenders synchronize individuals, so the
  effective N is small, fluctuations do not average out, and history-making events are
  single correlated excursions rather than aggregable noise.

**The claim of the program:** each objection has a *partial, local, conditional* repair.
Society satisfies (P1)–(P3) not natively but in bounded regimes, and the engineering job
is to (a) decompose a question onto the layers where the analogues hold, (b) build the
cheapest faithful model, and (c) forecast only as far as a state-dependent skill horizon
allows. The conditions, not the compute, are the theory.

The running example throughout the paper is the **Silicon Valley Bank failure (March 2023)**:
attention concentrated on one topic in days (conservation/concentration), the forecast of
failure caused the failure (reflexivity), the run propagated within one professional block
before jumping (decomposition then criticality), and a single deposit-guarantee announcement
at peak sensitivity halted the cascade (minimal-intervention control). Every component of
the framework appears in that one week.

---

## 2. The three repairs (one paragraph each)

**R1 — Attention as a conserved measure; belief as drift.** Nothing about a panic creates
new hours in anyone's day; what looks like belief appearing from nowhere is attention moving
from somewhere. Aggregate attention supply `A(t) = N_pop · h̄ · w̄` varies slowly, and total
media-consumption time is roughly flat while its composition churns — reallocation is
approximately zero-sum on sub-generational timescales. In the transformer analogue the
normalization is *exact* (`Σ_j α_ij = 1`). So attention is a **probability measure**:
allocated, never created. This yields a continuity equation
`∂ρ/∂t + ∇·J = s`, with flux `J = ρv − D∇ρ + ρb`. Crucially **belief is a drift field `b`,
not a conserved stock** — you can attend maximally to what you reject (protest, hate-watching),
so belief is a *direction imposed on transport*, not a sub-measure of ρ. Valence/legitimacy
rides on top as a non-conserved order parameter (Ising analogy: energy conserved,
magnetization not). High ρ with `b` pointing inward = legitimacy; high ρ with coherent `b`
pointing outward = crisis. Honesty rail: this is conservation of a *normalized probability
measure*, NOT a "softmax is a conservation law" claim.

**R2 — Reflexivity dissolved at mean-field-game fixed points.** The Lasry–Lions MFG couples a
continuum of optimizers to the density they constitute: a backward Hamilton–Jacobi–Bellman
equation (each agent best-responds to the anticipated ρ) and a forward Fokker–Planck equation
(the continuity law transporting ρ). An MFG **equilibrium** is a trajectory ρ\* that reproduces
itself when every agent best-responds to it — "a story about the future that comes true once
everyone believes it and acts on it." **Proposition:** a forecast is robust to its own
publication iff it is a fixed point of the prediction–reaction map. Reflexivity does not
preclude prediction; it restricts the *publishable* set to the equilibrium set. Deposit
insurance is the canonical engineered fixed point ("no depositor will lose money" induces the
non-running that makes it true); "the bank is sound" was not a fixed point and publishing it
accelerated the run. Two caveats: equilibria need not be unique (coordination games are
genuinely multiple/bistable — this caps resolution at the equilibrium *set*), and agents of
non-negligible measure (platforms, states, central banks, the Mule) break the continuum
hypothesis and must be modeled as major players or boundary conditions.

**R3 — Effective N from Simon near-decomposability; the block is the statistical unit.** The
synchronization objection assumes media correlate *everyone*; the platform era instead produced
a proliferation of densely-connected, mutually-sparse communities — tribes. Simon (1962): systems
that persist under selection are **nearly decomposable** hierarchies (dense interaction within
subsystems, weak between), because full global coupling is thermodynamically and organizationally
unaffordable. So model communities, not persons. Define blocks `B_1…B_K`; intra-block dynamics
are fast/strongly-coupled, inter-block coupling weak and slow. The statistical unit of the law of
large numbers is the **block**: `N_eff ≈ K ≪ N_pop` — thousands, not billions, but ample for
aggregate statistics in the weakly-coupled regime. Individuals re-enter as superpositions: each
person carries a membership vector `π_i ∈ Δ^{K−1}` (mixed-membership stochastic blockmodel —
identity as a convex combination of tribal belief vectors). Blocks and memberships are estimable
from interaction graphs by community detection, so the decomposition is empirical, not a
convenience. Honesty rail: read `N_eff` from the macro variance-ratio (Kuramoto/Kish), NOT from
Pearson correlation of fluctuations (that stays ~K even at full synchrony — it is the wrong metric).

---

## 3. The engine as a state-space system

The repairs are components; the engine is the standard filtering loop that wires them together.
It runs like a weather bureau: maintain a best estimate of the current "social weather," correct
it against fresh observations several times a day, run many perturbed copies forward, report the
*spread* as the forecast plus an honest skill horizon.

**State.**
```
Ξ_t = ( S_t , {ρ_k}_{k=1..K} , {b_k}_{k=1..K} , W , Π )
```
- `S_t` — slow macro stocks (demographics, debt, energy, aggregate attention supply A). [L1]
- `ρ_k` — block k's attention density over the topic space X (in practice a probability vector
  `p_k ∈ Δ^{n-1}` over a topic graph G of n embedded/clustered nodes). [L2]
- `b_k` — block k's belief (drift) field. [L2/L4]
- `W ∈ R^{K×K}_{≥0}` — slowly varying inter-block coupling matrix (the criticality knob). [L3/L5]
- `Π = (π_i)` — mixed-membership matrix. [L3/L6]

**Forward model M: Ξ_t → Ξ_{t+δ}**, three coupled layers ordered by timescale:
1. **Slow layer (stocks):** `Ṡ = F(S; θ_S)`, standard systems-dynamics; reliable, low-dimensional;
   supplies source terms `s_k` and total supply `A(t)` downward. [L1]
2. **Fast layer (transport master equation):**
   `dp_k/dt = L(b_k)ᵀ p_k + Σ_{j≠k} W_kj (p_j − p_k) + s_k`.
   `L(b_k)` is a rate matrix combining baseline drift, diffusion (graph Laplacian), and belief bias;
   each row sums to zero so conservation is enforced **structurally**. The exchange term is the weak
   coupling of R3; the regime monitor watches whether it stays perturbative. [L2/L3]
3. **Belief layer (MFG closure):**
   `b_k = b_k^ext(t) + β_k(−∇_G Φ(p_1…p_K)) + b_k^strat`.
   Exogenous = events feed; endogenous = herding on the current configuration (source of multiplicity);
   strategic = solving the multi-population MFG to equilibrium. The HJB layer is evaluated *inside* the
   forward model, so published forecasts are fixed points by construction. [L4]

**Observation operator.** `y_t = H(Ξ_t) + ε_t`, `ε ~ N(0,R)`; H aggregates block densities through Π,
so an individual-level signal is a `π_i`-weighted mixture of block states. [L6]

**Assimilation (EnKF).** Never free-run. Each cycle, propagate an ensemble `{Ξ^(e)}` and correct:
```
Ξ^(e)_a = Ξ^(e)_f + P̂_f Hᵀ (H P̂_f Hᵀ + R)^{-1} ( y_t + η^(e) − H Ξ^(e)_f )
```
— a disciplined compromise: nudge each member toward observation by an amount weighing model
uncertainty `P̂_f` against observation noise `R`. Parameters are fit offline against a historical
**social reanalysis** corpus (the analogue of ERA5 — flagged as the single largest missing piece of
infrastructure) and refined online by augmented-state assimilation. [L6]

**Forecast operator + skill horizon.** A lead-τ forecast is the pushforward of the analysis ensemble,
reported as a distribution and scored by CRPS/Brier. The ensemble doubles as the error model: read the
empirical Lyapunov rate off the growth of ensemble spread, and define **τ\*** as the lead time at which
spread reaches climatological (base-rate) spread. Beyond τ\* the engine reports base rates by
construction. τ\* is **state-dependent**: as the system approaches criticality, spread growth accelerates
and τ\* → 0 — the engine announces its own degradation as a first-class output. [L5/L7]

**One cycle:** assimilate → solve MFG closure → integrate ensemble forward → emit predictive
distributions + skill horizon + regime diagnostics → repeat.

---

## 4. Two failure modes (sharply distinguished)

Each repair has a validity condition; there are exactly two regimes where conditions fail, and they
are NOT the same phenomenon.

**(A) Criticality — in-model unpredictability.** Inter-block coupling is weak but nonzero; the coupled
system has a correlation length `ξ ~ |θ − θ_c|^{-ν}`. Near a critical transition ξ diverges and
previously decoupled blocks synchronize. Three consequences arrive together:
- `N_eff` collapses from ~K toward 1 — the recovered LLN evaporates exactly when stakes are highest
  (panics, mobilizations, cascades).
- The MFG fixed-point repair fails — critical transitions are non-equilibrium cascades, not fixed points,
  often triggered by agents of non-negligible measure.
- Conservation *survives* but loses constraining power — the drift `ρb` is dominated by one global gradient
  that swamps every coefficient calibrated in the smooth regime.

This is unpredictability *within a correct model*: dynamics known, sensitivity diverging (magnet near its
Curie point; stadium a moment before the wave). The fat tails of social history are not noise around the
model — they are the regime where the model's assumptions are the casualties. **Partial recovery:** driven
critical transitions have measurable precursors — critical slowing-down, rising variance, rising cross-unit
correlation (Scheffer et al. 2009). Rising synchrony between previously independent blocks is itself the
alarm. Predictability is therefore a *state variable* the model reports. You can often predict *that* a
transition is imminent without predicting *which branch* — early warning without trajectory.

**(B) Misspecification — out-of-model failure.** Categorically different. Asimov's **Mule** is not a chaotic
excursion of known dynamics but a hypothesis-space error: the generative process contained an agent type
assigned **zero prior mass** — an out-of-distribution (OOD) sample, epistemic not aleatoric uncertainty.
The everyday distinction: aleatoric = not knowing which face a fair die shows; epistemic = not knowing the
thrown object is not a die at all. More throws help with the first and are useless against the second.
Operationally decisive: the standard remedy (more data, tighter assimilation) does *nothing* here, because
additional observations of in-distribution agents carry no information about the existence of OOD ones.
(Canon sharpened the point: the deeper anomaly originated from a second hidden population, Gaia, which the
model could not have inferred from its training distribution at all.)

---

## 5. Prediction–control duality

Near a critical point the susceptibility diverges: `χ ~ |θ − θ_c|^{-γ}` — the macroscopic response to a
microscopic perturbation becomes unbounded. **This single fact has opposite signs for the two tasks.** For
**prediction** it is fatal (unobservable microscopic noise is amplified to macroscopic outcomes; the branch
cannot be forecast). For **control** it is maximal leverage (a small targeted intervention is amplified to
macroscopic effect; the branch can be *chosen*, cheaply). The same divergence that destroys predictability
maximizes controllability — dual objectives on the same mechanism. The SVB deposit guarantee was minimal
*because* the system was critical; the same announcement a month earlier (sub-critical) or a week later
(cascade complete) would have bought far less per unit of commitment.

**Regime-switching architecture:**

| Regime | Diagnostic | Mode |
|---|---|---|
| Smooth | low cross-block synchrony | open-loop prediction (MFG fixed points, block statistics) |
| Pre-critical | rising synchrony, critical slowing-down | early warning; forecast the *transition*, not the branch |
| Critical | ξ, χ diverging | closed-loop control; minimal intervention, maximal leverage |

**Dual-use warning.** The control mode is, read adversarially, a specification for propaganda: low-cost
steering of populations at moments of maximal susceptibility, with information release as a control input.
Early-warning infrastructure (L6) is comparatively safe to build and publish; control capability concentrates
exactly the power the Second Foundation novels warn about. Who holds the controller is a design constraint of
the same rank as any equation, not an ethics appendix.

---

## 6. Asimov canon — verified facts (use precisely)

These are the canonical facts the mapping table rests on. Do not embellish beyond them.

- **The two axioms** (verbatim, Encyclopedia Galactica epigraph opening *Foundation* (1951), via Gaal
  Dornick): (1) the human conglomerate must be **"sufficiently large for valid statistical treatment"**;
  (2) it **"be itself unaware of psychohistoric analysis in order that its reactions be truly random."**
  The load-bearing clause of axiom 2 is **RANDOMNESS**, not mere secrecy — secrecy is the means; statistical
  randomness (independence) is the requirement.
- A canonical **"third assumption"** (constant human nature / no fundamental change in the structure of
  society) is voiced later by **Ebling Mis in *Foundation and Empire* (1952)** — an elaboration, NOT one of
  Seldon's original two. A **"fourth"** (that humans are the only sentience in the galaxy) is raised by
  **Trevize in *Foundation's Edge* (1982)**.
- The **gas / kinetic-theory analogy** is verbatim from ***Foundation and Earth* (1986)**, NOT *Prelude*:
  Seldon "devised psychohistory by modeling it upon the kinetic theory of gases… we can work out the rules
  governing their overall behavior… even though the solutions would not apply to the behavior of individual
  human beings."
- **"Psychohistory dealt not with man, but with man-masses… The reaction of one man could be forecast by no
  known mathematics; the reaction of a billion is something else again."** — *Foundation and Empire* (1952).
- The **Mule** breaks the Plan because he is an out-of-model individual (a mutant mentalic) the statistical
  mass-action model assigned **zero prior mass** — the canonical model-misspecification / OOD example. (No
  single verbatim "the Mule broke psychohistory" line exists; it is canon in substance.)

---

## 7. CANON MAPPING TABLE (Asimov concept → real-math analogue)

| Asimov concept | Real-math analogue | Lives in |
|---|---|---|
| **Psychohistory** | Statistical mechanics of populations / mean-field theory | whole engine |
| **Axiom 1** ("sufficiently large for valid statistical treatment") | Law of large numbers / thermodynamic limit — but over **blocks**, so N_eff ≈ K | R3, L3 |
| **Axiom 2** ("unaware… so reactions be truly random") | Reflexivity / Lucas critique / observer effect — randomness = *independence* needed for the LLN; failure = correlation/reflexivity | R2, L4 |
| **Seldon Plan** | Mean-field equilibrium trajectory ρ\* (publishable forecast = MFG fixed point) | R2, L4, L7 |
| **Seldon Crises** | Bifurcations / critical transitions (forced choice points where ξ, χ diverge) | A, L5 |
| **Prime Radiant** | The live system of governing equations + phase-portrait / dashboard of the state Ξ | engine, L7 |
| **Time Vault holograms** | Open-loop **reference signal** (the precomputed trajectory to track) | L4/L7 |
| **First Foundation** | **Plant** — open-loop forward model M that runs forward | engine, L7 |
| **Second Foundation** | **Controller** — closed-loop corrector (Kalman correction / optimal control); the control layer, not a forecasting agency | L5, control mode |
| **Second Foundation mentalics** | Feedback control layer: EnKF correction + minimal-intervention optimal control at criticality | EnKF, control |
| **The Mule** | OOD agent / model misspecification (zero-prior-mass type; epistemic uncertainty; more data does not help) | B, L5 |
| **Gaia / Galaxia** | Total-observability, fully-coupled limit — N_eff → 1 *by design*; zero sim-to-real gap purchased by abolishing independent agents | trilemma, L5 |
| **R. Daneel / Zeroth Law** | Exogenous meta-controller with a humanity-level objective function (and the value-alignment problem of validating it) | trilemma |
| **Seldon trial (publishing the Plan's existence, hiding its contents)** | Information release as a control input; publish only components that are already fixed points of common knowledge | R2, control |

Two readings worth keeping explicit:
- Seldon **inverts** the secrecy requirement: he hid the *contents* of the Plan while deliberately placing
  its *existence* on the public record (the trial). In our terms, he published only the fixed-point
  components and withheld the non-fixed-point ones. Information release is itself a control input.
- Asimov's **patch sequence** is an argument: Second Foundation (abandon predicting OOD events, keep a
  standing corrective controller — but the controllers become an unaccountable power, the explicit subject
  of the later novels) → Galaxia (collapse the model/world distinction; no OOD agents by construction;
  N_eff → 1 the pathology turned into the cure) → and Asimov makes Galaxia's activation hinge on an external
  human chooser, because the controller cannot validate its own objective function at the decisive branch.
  That is a very early statement of the value-alignment problem.

---

## 8. The trilemma (the only complete repair, and why we decline it)

The two residual failure modes admit, between them, only one complete repair. Criticality can be *controlled*
but not predicted through. Misspecification can be *detected and corrected* after the fact but not
anticipated. The single architecture that eliminates both — no unpredictable branches, no OOD agents — is
**total observability of all components: the Galaxia limit.**

**Prediction, agent independence, and bounded observation form a trilemma.** Perfecting the first requires
surrendering one of the other two, and the surrender of independence is the totalitarian limit of the
program. Asimov's ambivalence at exactly this point is, we hold, the correct ending, and we adopt it. The
skill therefore never pursues the Galaxia repair; it reports scope and stops at the bounded analogue.

---

## 9. Real-world precedents

These are the actual research programs the framework is adjacent to. Cite only these; do not invent more.

- **Peter Turchin — cliodynamics / structural-demographic theory.** The closest real attempt at quantitative
  history. Key works: *Historical Dynamics* (Turchin 2003), *Secular Cycles* (Turchin & Nefedov 2009),
  *Ages of Discord* (Turchin 2016). His 2010 commentary (**Turchin, *Nature* 463:608, 2010**) forecast rising
  US structural instability into the 2020s. Turchin explicitly credits Asimov but draws the post-chaos
  distinction sharply: you predict **structural trends, not individuals** — in his phrase, after the onset of
  deterministic chaos at the individual scale, **"we are all Mules."** This is precisely the resolution-limit
  of §8 / the block-aggregate restriction of R3.
- **Paul Krugman** has repeatedly said he became an economist because **"I grew up wanting to be Hari
  Seldon"** — the Foundation novels as the stated motivation for mathematical social science.
- **Sociophysics** is the parallel physics-of-society program: Serge **Galam** (opinion-dynamics models) and
  the survey **Castellano, Fortunato & Loreto, *Reviews of Modern Physics* 81:591, 2009** ("Statistical
  physics of social dynamics") — the Ising/voter/Kuramoto machinery the attention-transport and block layers
  draw on.

---

## 10. Honesty rails (inherited from SKILL.md — do not violate)

- The sims verify **internal consistency only**. Never cite a sim as empirical validation.
- "Attention conservation" = conservation of a **normalized probability measure** (transport / Fokker–Planck),
  NOT "softmax is a conservation law."
- Early-warning signals are valid only for **slow bifurcation (B-)tipping**; always flag the prosecutor's-
  fallacy critique and the noise-induced (N-) / rate-induced (R-) tipping blind spots, which have no warning.
- A unique publishable fixed point exists only in the **monotone / congestion** regime; the **imitative**
  regime is bistable — that is where forecasting fails and control takes over.
- Society satisfies (P1)–(P3) **partially, locally, conditionally** — never natively. Report scope as a
  first-class output, every time.
