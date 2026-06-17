# L3 — Blocks: near-decomposability and the N_eff correction

**Role.** Decide *which communities are the statistical units*, measure how
synchronized they are, and report the **effective number of independent units
`N_eff`** — which is what controls whether the law of large numbers (predictability)
is working or has collapsed (contagion). This layer contains the framework's most
important measurement correction.

---

## 1. Near-decomposability → blocks

- **Simon (1962, *Proc. Am. Phil. Soc.* 106:467)** — *The Architecture of
  Complexity*: complex systems are **nearly decomposable**. Interactions within a
  subsystem are strong and fast; interactions between subsystems are weak and
  slow. On short timescales subsystems equilibrate internally and act as units.
- **Simon–Ando aggregation**: because of that timescale separation, you can
  aggregate each subsystem into a single variable and track the **between-block**
  dynamics on the slow timescale with controlled error. This is the justification
  for replacing N individuals with K blocks.

So the statistical unit is the **block** `B_1 … B_K`, not the individual. Blocks
are communities/tribes/sectors that mix internally fast and couple externally slow.

## 2. Mixed membership (individuals are convex combinations of blocks)

Real individuals belong to several blocks at once. Use the **Mixed-Membership
Stochastic Blockmodel — Airoldi, Blei, Fienberg & Xing (2008, *JMLR* 9:1981)**:
each individual `i` carries a membership vector `π_i` on the simplex
(`Σ_k π_ik = 1`), so they are a **convex combination of blocks**. This avoids the
fiction of hard partitions and gives soft block assignments to feed the metrics
below.

## 3. The coupled-block model (engine's L3/L5 core)

`engine.run_blocks(K, W, …)` integrates K bistable blocks coupled at strength `W`:

```
x_k += dt*(theta*x_k - x_k**3 + W*(mean - x_k)) + sqrt(dt)*sigma*noise
```

- Small `W`: blocks ~independent → LLN over blocks holds. **Verified (E3):**
  `std(population mean) ~ K^-1/2` (single-seed slope -0.63 is estimator noise;
  over 20 seeds -0.47 ± 0.13, consistent with -0.5; monotone θ=0 gives -0.52).
- Large `W`: blocks synchronize → independence collapses.

---

## 4. THE N_eff CORRECTION (central to this layer)

> **Pearson correlation of fluctuations is the WRONG synchronization metric.**

When blocks well-synchronize they share a **sign** (a discrete macro state), but
their residual jitter around that state stays weakly correlated. So the mean
off-diagonal Pearson correlation `rbar` of the *fluctuations* barely rises, and
the Kish-form `N_eff = K/(1+(K-1)·rbar)` built from it **barely falls**.

> **Verified (E4).** As coupling sweeps `W: 0 → 2.5`, the Pearson `N_eff` falls
> only **64 → 29.5** — it completely misses a transition into *full* synchrony.
> **This metric is wrong here; do not report it as the answer.**

### The RIGHT observables

**(a) Synchrony order parameter.** Use the Kuramoto order parameter or the
mean-field magnetization, not a correlation:

```
Kuramoto:   r = |<e^{iθ_j}>|          (Strogatz 2000, Physica D 143:1)
            onset at coupling K_c = 2 / (π g(0))   (g = nat-freq density)
magnetization (engine):   m = <sign x> ,   S = mean_t |<sign x>|
```

`S` runs 0 (blocks split) → 1 (all blocks share a sign).
**Verified (E4):** `S` goes **0.05 → 1.00** with the **transition near W ≈ 0.4**.
`engine.block_metrics(...)['S']` returns exactly this.

**(b) Correct N_eff.** Use the **Kish design-effect** form:

```
N_eff = N / (1 + (N-1)·rho)        rho = INTRACLASS correlation   (Kish 1965)
```

with `rho` the **intraclass** correlation (within-block clustering), realized
operationally as the **macro variance-ratio**:

```
N_eff = Var_t(single-block sign) / Var_t(population-mean sign)
```

This is what collapses when the macro variable gets pinned by synchrony.
**Verified (E4):** the macro variance-ratio `N_eff` collapses **61 → 1.0** across
the same sweep. `engine.block_metrics(...)['neff_correct']` (clipped to `[1,K]`)
returns this.

### Caveats on Kish N_eff

- Kish assumes **equal block sizes** and a **common, positive** intraclass `rho`.
- **Negative rho** (contrarian / anti-correlated blocks — agents who define
  themselves *against* the crowd) gives `N_eff > N`: the population is *more*
  independent than its headcount. Don't blindly clip that away when modeling
  genuine contrarian structure; flag it.

---

## 5. The rule

> **Report `S` / Kuramoto `r` and the macro-variance-ratio `N_eff`.
> NEVER report Pearson-correlation-of-fluctuations as synchrony or as `N_eff`.**

`engine.block_metrics` returns all three (`S`, `neff_correct`, `neff_pearson`,
`rbar`) and the docstring warns that `neff_pearson` is the misleading one — it is
included only to *demonstrate* the failure, never to drive a reading.

---

## HOW THE SKILL USES THIS LAYER

- [ ] If cue words hit (contagion, spread, herding, "everyone," harbinger,
      correlated, tribe, community): activate L3.
- [ ] Identify the **blocks** (near-decomposable communities). Use soft
      mixed-membership `π_i` if individuals span tribes (MMSB).
- [ ] **Compute** with `engine.block_metrics(run_blocks(K, W, seed=…))`.
- [ ] **Report** `S` (or Kuramoto `r`) for synchrony and `neff_correct`
      (macro variance-ratio) for effective independence. State the transition
      vs the coupling knob `W` (engine transition ≈ W 0.4).
- [ ] **Never** quote `neff_pearson` as the answer — name it only to show the
      correlation metric stays high (≈K) while real synchrony has already hit.
- [ ] Low `N_eff` → LLN is failing → hand off to **L5 (criticality)**: the system
      is near a transition and forecasts lose skill.
