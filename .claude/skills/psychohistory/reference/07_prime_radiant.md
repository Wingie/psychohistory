# L7 — The Prime Radiant (synthesis engine)

Named for Asimov's device: the **live, editable system of equations** that ties the active
layers into ONE model and emits ONE forecast bounded by the skill horizon `tau*`. L7 always
runs last. It does not introduce new physics — it **selects** the active layers, **builds**
each cheaply, finds the **dominant mechanism** and the load-bearing **cross-terms**, decides
**what is even predictable** in the current regime, and writes the reading.

The Prime Radiant is *editable*: as L6 acquires a number or a falsifier fires, you change the
equations and re-emit. It is a working model, not a verdict carved in stone.

---

## What L7 fuses

- **L1 dynamics & stocks** — `systems.parse` stock-flows for the slow conserved core
  (`reference/01_stocks_lethain.md`); supplies totals and source terms.
- **L2/L3/L5 sim dynamics** — `scripts/engine.py` (the verified primitives from `sims_v2.py`):
  `run_blocks(K, W, seed=...)` for coupled-block dynamics, `block_metrics(tr)` →
  `{S, neff_correct, neff_pearson}` for synchrony and effective independence, and the skill
  horizon. The criticality knob is the coupling **`W`**; the order parameter is
  **`S = mean|<sign x>|`** (Kuramoto-style), and `N_eff` is the **macro variance-ratio**,
  **never** Pearson-of-fluctuations (which stays ~K even at full synchrony — it is wrong).
- **L4 reflexivity** — the reaction map `T(f)`, monotone(congestion) → unique publishable
  fixed point vs imitative → bistable / multiple fixed points.
- **L6 data** — fetched, URL-cited magnitudes; integrity diagnosis.

> Honesty rail: the sims verify **internal consistency only**. Never cite a sim run as
> empirical validation. Numbers below are illustrative of the *procedure*.

---

## The synthesis procedure

1. **Classify.** Map the question onto active layers (cue table + `08_classification.md`).
   Most real questions hit 2–4 layers. Record them.
2. **Model each active layer** with the cheapest faithful tool (L1 stock-flow, engine.py
   blocks, L4 reaction map, L6 fetch).
3. **Identify the dominant mechanism + cross-terms.** One sentence for the driver; then the
   load-bearing couplings — e.g. *a strategic actor (L4) amplifying an endogenous cascade
   (L5) that was triggered by an exogenous shock (L1)*. The cross-terms are usually where the
   answer lives.
4. **Determine the regime.** Read `S` and `N_eff` off `block_metrics`:
   - **smooth / subcritical** (`S` low, `N_eff` large) — averaging holds, forecast the
     trajectory;
   - **pre-critical** (`S` rising, `N_eff` falling, variance & lag-1 autocorrelation rising) —
     early-warning regime;
   - **critical / over-synchronized** (`S` high, `N_eff → O(1)`) — the LLN is gone, point
     prediction fails.
5. **Set the objective from the regime:**
   - smooth → **predict the trajectory**;
   - pre-critical/critical → **predict the transition, not the branch** (forecast *that* it is
     fragile, not *which way* it breaks or *when*);
   - reflexive/controllable → **recommend minimal-intervention control** (the announcement /
     guarantee that moves the fixed point).
6. **Compute the skill horizon** `tau*` via `engine.skill_horizon` (ensemble-spread growth vs
   climatological spread). `tau*` **collapses** as `W` rises toward criticality — report it
   honestly; near-critical `tau*` is short.
7. **Assign confidence** (low/med/high + why) — driven by regime, data quality (L6), and
   model agreement.
8. **List falsifiers** — the concrete observation that would break the reading.
9. **Assign the scope verdict** — MODELED | PARTIAL | NEEDS-DATA | NORMATIVE-AS-VALENCE.
10. **Emit** via the OUTPUT TEMPLATE from `SKILL.md` (reproduced exactly in both examples
    below).

---

## Worked example A — "Nvidia is worth over $4T… how is this not a bubble?"

```
QUESTION: Nvidia is worth over $4T — how is this not a bubble?
ACTIVE LAYERS: L2 attention (over-concentration), L4 reflexivity (self-fulfilling price),
               L5 criticality (over-synchronized regime)
DOMINANT MECHANISM: Endogenous attention/capital concentration locked in by imitative
                    coupling — the price is high partly because it is high (a reflexive
                    near-fixed-point), which is the definition of an over-concentrated,
                    fragile regime rather than a falsifiable "wrong valuation."

MODEL:
  L2 (attention transport): valuation share is a conserved-salience carrier with belief
    drift (preferential attachment / rich-get-richer). Capital and narrative flow to the
    leader at a rate proportional to its current share -> super-linear concentration. The
    attention "bubble" is FORMATION = over-concentration, not creation of value.
  L4 (reflexivity / MFG): reaction map T(f) of "buy because others buy / it will keep
    rising." This is the IMITATIVE regime, not the monotone/congestion regime -> the map is
    S-shaped and admits MULTIPLE fixed points (a justified-high-price fixed point AND a
    collapsed fixed point). A high price can be a self-fulfilling fixed point: as long as
    coordination holds, T(f)=f at the high branch. Bistable => no unique publishable
    forecast => this is where point-prediction fails and the system is steerable by
    narrative shocks.
  L5 (criticality): run engine.py coupled blocks; read S = mean|<sign x>| and the macro-
    variance-ratio N_eff. High investor synchrony (everyone long the same thesis) =>
    S near 1, N_eff -> O(1): the market is OVER-SYNCHRONIZED. The crowd has collapsed to
    one effective agent, so the LLN that would smooth idiosyncratic shocks is gone and a
    single shock propagates. tau* (engine.skill_horizon) is SHORT in this regime.

DATA ACQUIRED (if L6): NEEDS for sharpness, not for the structural verdict. To quantify
  fragility, fetch (WebSearch/WebFetch, cite URL+date): Nvidia's share of index market cap /
  of AI-capex flows; forward P/E vs sector history; concentration of revenue in a few
  hyperscaler customers; breadth (share of funds long the same names). [Acquire before
  putting a number on the fragility; structural reading below does not depend on it.]

FORECAST / STRUCTURAL CLAIM:
  "Bubble" is not a price level you can declare wrong — it is a STATE: over-concentrated
  attention (L2) sustained by an imitative, bistable reflexive regime (L4) in an
  over-synchronized market (L5). That state is FRAGILE and shows early-warning signatures
  (rising synchrony S, falling N_eff, rising variance & lag-1 autocorrelation, breadth
  collapse). The honest claim: we can forecast the FRAGILITY and read the early-warning
  signals; we CANNOT forecast the POP DATE. The pop is on the unpredictable branch — a
  bistable, near-critical transition whose timing is set by which shock arrives when, not by
  the current state. Objective therefore = "predict the transition, not the branch": flag
  the regime as pre-critical/critical and monitor S, N_eff, breadth, autocorrelation.
  Skill horizon: SHORT for timing (near-critical => tau* collapses; no reliable date).
    STRUCTURAL / no-horizon for the fragility claim itself (it is a state diagnosis, not a
    forecast of an event).
  Confidence: med-high on "this is an over-concentrated, imitative, over-synchronized
    (fragile) regime"; LOW on any specific pop date or peak level.

FALSIFIERS:
  - Synchrony S stays LOW / breadth stays WIDE (gains broaden across many uncorrelated
    names) and N_eff stays large -> NOT over-synchronized -> reading wrong, treat as
    broad-based repricing, not a bubble state.
  - The reaction map is actually MONOTONE (fundamentals-anchored, congestion-like: more
    buyers raise the price toward a unique justified level with no imitative amplification)
    -> unique fixed point, not bistable -> not a "bubble" in this sense.
  - Earnings / cash flows rise to validate the price with falling, not rising, variance and
    autocorrelation -> the high fixed point was the fundamental one.

SCOPE VERDICT: PARTIAL  (structural state diagnosed and early-warning regime identified;
  pop timing is on the unpredictable branch and is NOT modeled; fragility magnitude is
  NEEDS-DATA until the concentration/breadth figures are fetched.)
```

---

## Worked example B — "Is the United States heading toward an economic collapse?"

```
QUESTION: Is the United States heading toward an economic collapse?
ACTIVE LAYERS: L1 slow stocks (debt/fiscal), L3 blocks (which communities, synchrony),
               L5 criticality + early-warning (WITH its limits), L4 reflexivity (collapse
               narratives as control inputs)
DOMINANT MECHANISM: The answerable question is not "will it collapse" but "is the system in
                    a pre-critical regime." You can sometimes forecast THAT a transition is
                    near (rising synchrony / variance / autocorrelation across blocks); you
                    cannot forecast WHICH branch it takes or WHEN. Collapse narratives (L4)
                    are themselves reflexive inputs that can move the fixed point.

MODEL:
  L1 (slow stocks): build a systems.parse fiscal stock-flow -- debt stock, interest outflow,
    primary deficit inflow/outflow, GDP-growth denominator. Read the TRAJECTORY of
    debt/GDP and the interest-coverage margin. This is the slow manifold; it sets WHETHER a
    bifurcation parameter is drifting toward a tipping value. [Stock MAGNITUDES are
    NEEDS-DATA: fetch current federal debt/GDP, interest-to-revenue ratio, deficit path from
    CBO / Fed / IMF / BIS, cite URL+date, before running.]
  L3 (blocks): collapse is a CROSS-BLOCK synchronization event, not an average. Use
    engine.py run_blocks; read S and the macro-variance-ratio N_eff (NOT Pearson). A robust
    economy has many weakly coupled blocks (N_eff large, LLN smooths shocks); danger is
    rising coupling W driving S up and N_eff -> O(1) (blocks moving as one).
  L5 (criticality + EARLY-WARNING WITH LIMITS): rising variance, rising lag-1
    autocorrelation, and rising cross-block synchrony are genuine precursors of a SLOW
    (B-)tipping. BUT: (i) PROSECUTOR'S FALLACY -- P(signals | crisis) being high does NOT
    make P(crisis | signals) high; precursors fire far more often than crises occur, so a
    raw "warning" is mostly false alarm. (ii) N-tipping and R-tipping (a fast shock, or
    too-rapid change of a parameter) have NO early warning at all. So early-warning bounds
    the claim to "elevated fragility," never to "collapse imminent."
  L4 (reflexivity): "collapse is coming" narratives are control inputs into the reaction
    map. They can be self-defeating (prompting pre-emptive fiscal tightening / hedging) or
    self-fulfilling (triggering the run they predict). Bistable/imitative => the published
    forecast itself perturbs the outcome; no unique publishable point forecast.

DATA ACQUIRED (if L6): debt/GDP, interest-to-revenue, primary-deficit path, maturity wall
  -- fetch from CBO, Federal Reserve, IMF/BIS (WebSearch -> WebFetch -> record number + URL +
  date + cross-source spread). Until fetched, the L1 magnitudes are placeholders and the
  stock trajectory is qualitative only.

FORECAST / STRUCTURAL CLAIM:
  The framework REFUSES the point prediction and answers the answerable question: you can
  forecast THAT the system is near a transition (if S, variance, autocorrelation, and
  cross-block synchrony are rising on fetched data), NOT WHICH branch (muddle-through /
  inflation / restructuring / acute crisis) nor WHEN. Pair this with the failed-prediction
  lesson: people predicted Russia's collapse for ~3 years before it happened (see corpus
  post #9) -- a standing illustration that confident point-predictions of criticality fail
  precisely because (a) the prosecutor's fallacy makes "warning signs" chronically present,
  and (b) the branch/timing live on the unpredictable side. Objective = "predict the
  transition, not the branch," plus flag L4 control leverage (credible fiscal anchoring
  moves the fixed point away from the bad branch).
  Skill horizon: tau* for "elevated/normal fragility regime" = quarters, IF the
    early-warning indicators are real and the regime is slow-tipping (B-tipping). NO horizon
    for branch or date; a fast (N/R) shock has tau* = 0 (no warning).
  Confidence: med on "fragility regime, yes/no" given fetched stock + synchrony data;
    LOW on any timing or specific collapse scenario; the Russia-3-years lesson caps
    confidence on point-predictions hard.

FALSIFIERS:
  - Cross-block synchrony S and N_eff stay healthy (N_eff large, S low) and variance /
    lag-1 autocorrelation are flat or falling -> NOT pre-critical -> "heading toward
    collapse" reading is unsupported.
  - Debt/GDP stabilizes or interest-coverage improves on fetched data -> slow manifold not
    drifting toward a tipping value.
  - A confident DATE or BRANCH is offered and survives -- this would falsify the framework's
    core claim that branch/timing are unpredictable here (we expect such confident calls to
    keep failing, cf. Russia).

SCOPE VERDICT: PARTIAL, with NEEDS-DATA on the stock magnitudes. (The regime-level
  structural claim is modelable; the stock trajectory needs fetched debt/deficit numbers;
  the branch and date are structurally NOT predictable and are reported as such.)
```

---

## Orchestration note

When batch-running the corpus (e.g. the top r/AskEconomics posts in
`top200askeconomics.json`), the orchestrator should **spawn one subagent per post**. Each
subagent runs the full procedure (classify → model layers → synthesize → emit the template)
in its own context and returns only the finished reading. This keeps the orchestrator's
context clean, lets posts run in parallel, and prevents one post's modeling state (sim runs,
fetched numbers, layer scratch-work) from leaking into another's.
