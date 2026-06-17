# 09 — Build your own analysis engine

This module enables someone else to stand up their own bounded-psychohistory **analysis
engine** — the *defensive*, early-warning/monitoring stack — and point it at a new domain.
It is the operational companion to the implementation sketch in the paper (`psychohistory.tex`,
§Implementation: the staged L1–L6 program with the explicit governance gate).

> **Read the SAFETY guardrail in `SKILL.md` first.** What you build here is the **monitor,
> not the manipulator.** The paper specifies the early-warning/defensive layer in full and
> WITHHOLDS the control-synthesis layer; this guide does the same. Build to understand,
> anticipate, monitor, and hold accountable — never to steer, target, or time an intervention
> against a population. If your intended use is on the manipulation side of the
> defensive/offensive split, stop and re-read the guardrail.

---

## 1. Prerequisites / install

- **Python 3.12.** All of it runs on **CPU — no GPU required** (the sentence-transformer
  embeddings run on CPU via `all-MiniLM-L6-v2`).
- Install the dependencies:

  ```bash
  pip install -r requirements.txt
  ```

  which pulls `systems` (the lethain stock-flow library), `numpy`, `matplotlib`, `scipy`,
  `networkx`, `python-louvain` (community detection), and `sentence-transformers` (local
  CPU embeddings). Nothing else is needed to reproduce the primitives below.

Verify the core engine imports and runs:

```python
from engine import run_blocks, block_metrics
print(block_metrics(run_blocks(K=64, W=0.6, seed=2)))   # -> {S, neff_correct, neff_pearson}
```

---

## 2. The verified primitives (and which layer each implements)

### `scripts/engine.py` — the verified simulation core (L2 / L3 / L4 / L5)

These reproduce the paper's sim-table numbers; **import them, do not re-derive.**

| Primitive | Computes | Layer |
|---|---|---|
| `run_blocks(K, W, …, seed=)` | coupled-block dynamics; `W` is the **criticality knob** | L3/L5 |
| `block_metrics(traj)` | `{S, neff_correct, neff_pearson}` — synchrony `S = mean|<sign x>|` and the **macro variance-ratio** `N_eff` (use `neff_correct`, **never** `neff_pearson`, which stays ~K even at full synchrony) | L3 |
| `reaction(f, guarantee=…)` | the MFG reaction map `T(f)` (the cartoon best-response) | L4 |
| `fixed_points(g, …)` | the fixed point(s) of the reaction map; monotone ⇒ unique, imitative ⇒ multiple/bistable | L4 |
| `skill_horizon(K, W, …)` | `tau*` from ensemble-spread growth vs climatological spread; **collapses as `W` → criticality** | L5/L7 |
| `systems_stockflow(spec_str, rounds)` | the lethain stock-and-flow helper for the slow conserved core | L1 |

> Honesty rail: these sims verify **internal consistency only**. Never cite a sim run as
> empirical validation.

### `validation/pipeline_v03/` — the v0.3 observation-operator upgrades (L2 / L6)

The v0.2 pilots measured everything off **mention-density** (a scalar — the zeroth moment).
The v0.3 operators move to the **vector / embedding** observables the theory actually
specifies. Each is a pure transform; run end-to-end on CPU with `py -3.12 <script>.py`.

| Script | Computes | What layer / why |
|---|---|---|
| `semantic_csd.py` | **vector belief-variance early-warning**: embeds raw post text (`all-MiniLM-L6-v2`, CPU), then takes second-moment signatures — rolling **variance of sequential-post cosine similarity** (belief spread) and **lag-1 autocorrelation of bucket centroids** (slowing) — and runs the same detrended Kendall-tau critical-slowing-down detector the volume pilots used. Sees belief *dispersion* rising even when volume is flat. | L5 early-warning via the L6 observation operator. The semantic CSD is the proper vector observable; mention-density was its scalar shadow. |
| `blind_neff_collapse.py` | **blind community detection + Kish N_eff**: Louvain community detection on a **pre-onset** interaction graph (blocks discovered from structure, no outcome knowledge), then freezes the partition and tracks `N_eff = K / (1 + (K−1)·rho_bar)` as the window advances into onset. Near-decomposability = distinct blocks before locking; collapse = `N_eff` falls across the onset (synchronization). | L3 blocks / N_eff via L6. Removes the post-hoc basket-selection bias of the v0.2 counterfactual. |
| `operator_hhi.py` | **HHI / Gini operator-concentration**: over the pre-onset window computes actor activity-share **HHI, Gini, top-5% share**; builds a platform base-rate null from every non-onset rolling window of equal length; flags only if pre-onset concentration exceeds the 90th percentile of that null — **time-invariant** (same verdict whether the buildup took 13 weeks or 3 days). | L2 attention-concentration / operator signal via L6. Kept at mechanism-classifier grain (see guardrail). |

`validation/pipeline_v03/common.py` holds the shared harness (embedding cache, base-rate-null
construction); `RESULTS.md` in that directory records the pilot outputs.

---

## 3. Workflow — analyze a NEW domain / corpus

1. **Harvest a timestamped activity + text corpus.** You need *(timestamp, actor, text)*
   tuples spanning before and after the episode of interest. Sources that work:
   - **Reddit** — **Arctic Shift** (the post/comment dump + API replacing the retired
     Pushshift) for historical, timestamped post and comment text.
   - **GitHub** — the **REST API** for per-contributor, per-repo, per-week commit activity;
     and **GH Archive** for the bulk event firehose when you need many repos.
   Keep raw text (the v0.3 operators need the vector, not just the count) and exact timestamps.

2. **Classify the question onto layers L0–L7** using `reference/08_classification.md`. Record
   the active layers; most real questions hit 2–4.

3. **Run the relevant observation operators** for the active layers:
   - early-warning / criticality (L5) → `semantic_csd.py` (vector belief-variance CSD);
   - blocks / N_eff (L3) → `blind_neff_collapse.py` (blind Louvain partition + Kish N_eff);
   - operator / attention concentration (L2) → `operator_hhi.py` (HHI / Gini vs base-rate null).
   Pair these with the `engine.py` primitives for any sim-side modeling (regime, fixed points,
   `skill_horizon`).

4. **Score against a base-rate null with a strict pre-onset information cutoff.** Build the
   null from every non-onset rolling window of equal length (as the operators do) and compute
   all features using *only* data available **before** the onset. This is what avoids the
   **prosecutor's fallacy**: a high P(signal | crisis) is worthless without the base rate of
   the signal firing in non-crisis windows. A backtest with any post-onset leakage proves
   nothing.

5. **Synthesize via the Prime Radiant (L7)** (`reference/07_prime_radiant.md`): fuse the
   active layers into one reading, state the dominant mechanism and cross-terms, set the
   objective from the regime, and **report with the skill horizon `tau*` and honest caveats**,
   using the output template in `SKILL.md`.

---

## 4. Honesty rails to carry (non-negotiable)

- **Mention-density is a scalar shadow of the vector theory.** Prefer the semantic / embedding
  observables (semantic CSD, centroid dispersion); a scalar count cannot see belief dispersion
  rising while volume is flat.
- **Results are preliminary on small n.** The pilots run on modest corpora; treat every number
  as illustrative of the *procedure*, not as a validated effect.
- **A backtest discharges no pre-registered test.** Retrospective fits on already-resolved
  episodes are hypothesis-generating, not confirmatory. They do not count as the falsification
  the program owes.
- **Pre-register thresholds before lodging.** Fix and time-stamp every numeric threshold *before*
  you see the out-of-sample data, so there is no freedom to move the goalposts after the fact.
- And the sims verify internal consistency only — never cite a sim as empirical validation.

---

## 5. Worked examples and the test protocol

- **`validation/`** holds the worked pilots: the **Reddit** pilots (AskEconomics text and the
  GME/WSB episode) and the **GitHub** pilot (`validation/github/`, the LLM-agent contributor
  cohort), plus `validation/backtests/` for the early-warning / block-sync / operator backtests
  and `validation/pipeline_v03/RESULTS.md` for the v0.3 operator outputs.
- **`validation/PRE_REGISTRATION.md`** is the test protocol: the pre-registered, time-stamped
  falsification tests (the seal / registry mechanism, the enumerated tests, and the proposed
  thresholds to freeze before lodging). Read it before claiming any result is a confirmation.

---

## 6. The boundary, restated

Everything in this module is the **defensive layer**: detection, early warning, blocks, N_eff,
operator concentration at mechanism-classifier grain, skill horizon, accountability. The
moment a build turns toward *which message switches the cascade*, *which block to target at
peak susceptibility*, *when to time the push for maximum leverage*, or a *named-individual
targeting* use of the operator detector, it has crossed into the withheld control-synthesis
layer — and the SAFETY guardrail in `SKILL.md` requires the skill to warn, decline, and
redirect. Build the monitor; do not build the manipulator.
