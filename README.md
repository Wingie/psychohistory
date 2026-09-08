# Conditions for Predictable Social Dynamics

*A bounded engineering specification for a weak form of Asimov's psychohistory — with a verified internal-consistency engine, an interactive website, a Claude skill, and an empirical measurement suite.*

This repository accompanies the position paper ***Conditions for Predictable Social Dynamics: Conservation, Decomposition, and Control at Criticality*** (Wingston Sharon). The paper asks whether collective human behaviour can be forecast like the weather, argues that social systems possess *partial, conditional* analogues of the three properties that make numerical weather prediction work (conservation laws, weak multi-scale coupling, non-reflexivity), and assembles them into an explicit, regime-aware engineering specification with a stated boundary of where it stops applying.

**▶ Live interactive site: https://wingie.github.io/psychohistory/** — a four-page guide (Home · Tutorial · The math · Tests &amp; data) that teaches the framework, renders every equation, and walks through every test run against real data. The same content is in [`site/`](site/) and works offline.

---

## Status

This is a **position paper plus an empirical measurement suite on proxy data.** The specification is the contribution; the measurements say how far the machinery reaches on the substrates reachable today.

- **The criticality gear measures as predicted.** The **dynamic N_eff collapse** — the structural core — was measured on a fresh r/wallstreetbets roster (`validation/neff_v4/`): **9 of 12** cascades collapse past their own block-label shuffle, binomial *p* = 1.7×10⁻⁷. The WSB work is one substrate read three times rather than three independent substrates — the three runs share the subreddit, the dump and the top-commenter graph, and 11 of the 12 v4 windows share calendar days with a window from a prior run — so it is depth on one substrate, not breadth across many.
- **Wikipedia is a different substrate and the same rule does not carry over to it**: neither the event arm (0 of 14) nor the calm arm (0 of 10) fires. The contrast is mostly null geometry rather than community structure — identical code gives a median event null p90 of 0.4909 on Wikipedia against 0.0137 on WSB, roughly 36×. The rule is tuned to substrates with WSB's block geometry.
- **Forward forecasting is specified but not yet built out.** A strictly-causal one-block EnKF walk-forward runs today (`validation/engine/`): it beats climatology and ties persistence. Fixed-point reliability and regime occupancy need a lodged announcement/question set and a regime monitor operationalised on a named series — both startable on the hardware already here. Lucas invariance needs the multi-block coupled engine **and** a multi-regime reanalysis corpus. **The binding constraint is the open social-reanalysis corpus (E-6), not compute.** The raw record already exists and is already held at population scale by closed actors, so it is an *access* problem, not an existence one.
- **The second-wave battery maps the boundary the bounded thesis draws.** Early warning beats a calm null but does not separate endogenous from exogenous onsets; the bifurcation-mix conjecture does not carry; conservation does not hold at basket scale. The impersonal/structural machinery is load-bearing on the endogenous, reflexive episodes and not beyond them — which is what a *bounded* framework asserts.
- All numerical figures in the paper (E1–E5) are **internal-consistency checks of the paper's own equations**, not empirical evidence.
- The full assimilating engine, a forward forecast that beats persistence, and the open social-reanalysis corpus **do not yet exist.** See `RUN_AND_CHECK.md` for the status ledger and [`validation/NEFF_COLLAPSE_SYNTHESIS.md`](validation/NEFF_COLLAPSE_SYNTHESIS.md) for the full account of the N_eff programme.

This is independent research; correspondence to `wingston.sharon@gmail.com`.

### The LOGOS companion paper (v0.2, new)

`logos.tex` applies the same discipline to a different object: the **machines** rather than the societies. It specifies a 10T+ Mixture-of-Towers from published 2024 to 2026 components, then audits its own arithmetic. **No model in it has been trained and no system has been served.** What it does have is arithmetic that has been checked, citations verified against primary sources, its weakest components relocated, and ten open measurements each stated with the hardware it needs.

The paper's conclusion is not the one it set out to reach. Four separate literatures converge on a single point: debate among agents holding the same information is a martingale, so expected correctness does not improve; RL with verifiable rewards sharpens sampling without expanding the set of solvable problems; recursive self-training without external grounding provably degenerates; and self-play works when, and only when, something external checks the answer. Put together, they say that **capability at this scale is bounded by observation bandwidth, not by parameters or compute.** Scale buys the capacity to be corrected quickly. It does not buy the corrections.

That is where the two papers meet. Psychohistory ends at an observability trilemma: complete predictability would require total observability, which is surveillance, and it rejects the limit. LOGOS ends at an observation bound: improvement past human text is set by how fast the world corrects the model. Both terminate on the same quantity from opposite sides, and when the something being observed is people, the two limits are one limit.

Running the other way, `logos-harness` needs an adjudicator the model cannot fake, and psychohistory's validation pipeline is one. The coupling is narrow and mostly one-directional: the harness could supply the multi-block forward engine the Lucas-invariance work needs, **if** the multi-regime reanalysis corpus existed. It supplies neither that corpus (E-6), nor the lodged announcement set, nor the operationalised regime monitor.

---

## Repository map

| Path | What it is |
|---|---|
| `psychohistory.tex` / `psychohistory.pdf` | The paper (~79 pp). Sole author Wingston Sharon; includes an AI Contribution Declaration. |
| `sims.py`, `sims_v2.py` | The verified internal-consistency simulations (E1–E5). Outputs in `_verify_out/` and `figures/`. |
| `site/` | The four-page interactive site ([live](https://wingie.github.io/psychohistory/)): **Home** (thesis + canon), **Tutorial** (the layers + a worked GameStop walkthrough), **The math** (every equation with KaTeX + three live demos + the AI scenario), and **Tests &amp; data** (the full empirical program). Open `site/index.html` to run it offline. |
| `.claude/skills/psychohistory/` | A Claude skill: `SKILL.md` (with a dual-use SAFETY guardrail), reference modules `00`–`09` (including a build-your-own guide), `scripts/engine.py`, a `corpus/`, and a coverage report under `results/`. |
| `steering_envelope/` | **The Steering Envelope (s/acc): one axiom, one theorem** — the program's first *intervention* module, postulated 2026. New primitive: Ashby's Control Axiom (requisite variety); combined with the program's accumulation and plurality premises it yields the Survival Theorem: societies survive technology in proportion to the control they exert over its speed. The hazard law h = σ(β(v·k/(s·c₀) − 1)) — control-loss risk as speed over steering capacity — as a Python engine (race model, mean-field N-actor coordination theorem, Sustenance Ledger tribes layer) plus a validation suite on public data: US roads, world aviation, the JST macrohistory panel (the ratio model wins out-of-sample, LORO AUC 0.688 vs 0.506 for credit growth alone), nuclear as a case study, and AI leading indicators. Essay at [`site/steering.html`](site/steering.html), interactive v0.4 instrument at [`site/steering_sim.html`](site/steering_sim.html), open measurements in [`steering_envelope/README.md`](steering_envelope/README.md). |
| `logos.tex` | **The LOGOS paper** (v0.2): *Ten Trillion Parameters, and the Limit That Scale Does Not Move*. A companion position paper on the machines rather than the societies. It specifies a 5x2.8T Mixture-of-Towers, audits its arithmetic, and finds that the arithmetic points somewhere the architecture did not intend. Three corrections drive it: the usual "10T is impossible" argument prices a **dense** model nobody is building (a sparse tower costs 55x less to train and already exists); splitting a parameter budget across towers does **not** reduce total tokens consumed, only the peak *unique*-corpus requirement; and the EU AI Act's 10^25 FLOP presumption is written against *a model*, so a composed ensemble has no settled answer to "how many models is this." Following the corrections leads to the thesis: sparsity removes the compute limit, tower decomposition raises the data ceiling, 4-bit serving handles memory, and **none of them touches the rate at which something outside the model can tell it it is wrong.** A fourth correction runs against the design it starts from: applying the paper's own three-axis partition criterion (corpus disjointness, objective conflict, update cadence) says **four towers, not five** (Mathematics and Logic fail all three axes and should merge). The paper states that in its abstract, in §3.4 and in its conclusion, and it also states that settling four-versus-five needs corpus-overlap measurements that have not been run. |
| `logos/` | The LOGOS companion directory: [`REVIEW_ROUND2.md`](logos/REVIEW_ROUND2.md) and [`REVIEW_ROUND3.md`](logos/REVIEW_ROUND3.md) (the technical audit passes over the paper: 40 findings graded by engineering priority, with §6 recording what was checked and found sound), [`ARCHITECTURE_REVIEW.md`](logos/ARCHITECTURE_REVIEW.md) (15 findings, 3 critical; four remain open — F-04 needs a training run, F-13's sparse-dispatch cost model is not re-derived, F-14's partition is argued but unmeasured, F-15's headroom consequence is unquantified — and two are closed only in part, F-09 and F-10), [`BIBLIOGRAPHY_REVIEW.md`](logos/BIBLIOGRAPHY_REVIEW.md) (every citation checked against a primary source: 21 verified, 4 corrected, 4 downgraded to blog-grade sourcing, 3 dropped as unsourceable, 11 missing attributions supplied), [`GAPS.md`](logos/GAPS.md) (the measurement ledger: ten open measurements, **five** of them on one consumer accelerator, with F5 falling out of F9 for free; four items in its §4 need no accelerator at all), [`F9_MEASUREMENT_PLAN.md`](logos/F9_MEASUREMENT_PLAN.md) (the design for F9, the observation-bound measurement, including the note that one seed per arm buys no within-arm variance and therefore no usable statistic at the budget the ledger assigns it), [`TIER0_3090_PLAN.md`](logos/TIER0_3090_PLAN.md) (what actually runs on the owned 3090, priced in GPU-hours and electricity, with its stop conditions), and [`LOGOS_HARNESS.md`](logos/LOGOS_HARNESS.md) (**`logos-harness`**: the implementation spec for the bootstrap loop, tested on Pokemon for volume and on **this repository's own psychohistory pipeline** for validity). |
| `validation/` | All the empirical + scenario work, one directory per test (method + analysis script + `RESULTS.md` + result JSON + figures): `neff_v2/`, `neff_v3/`, `neff_v4/` and their `wikipedia/` sibling, the early-warning battery, bifurcation-mix, conservation-ecosystem, the GameStop counterfactual + operator-signal backtests, GitHub cross-domain replication, the EnKF forward test, scenario sims, Kuramoto, the v0.3 observation-operator pipeline, fact-check, and the run-and-check guide. Raw/harvested data is gitignored and regenerable from each test's harvest script. |
| `RUN_AND_CHECK.md` | The status ledger: every claim needing code/data/a derivation, cross-referenced to its artifact, marked DONE / PILOT / PENDING / NOT-STARTED. |
| `ETHICS.md` | The responsible-use / dual-use notice (the defensive/offensive split). |
| `requirements.txt` | CPU-only Python dependencies for the sims and validation scripts. |

---

## How to

### Build the papers

```sh
pdflatex psychohistory.tex
pdflatex psychohistory.tex      # twice: resolves refs/ToC

pdflatex logos.tex
pdflatex logos.tex
pdflatex logos.tex              # THREE times: pass 2 still reports "Label(s) may have changed"
```
Requires a TeX distribution (MiKTeX or TeX Live). A pre-built `psychohistory.pdf` is included; no `logos.pdf` is committed, so build it.

`logos.tex` compiles. Verified on MiKTeX at commit `dde58df`: **32 pages, exit code 0, zero undefined references, zero undefined citations.** It needs a third `pdflatex` pass, unlike `psychohistory.tex`, because pass 2 still reports "Label(s) may have changed"; two passes leave stale cross-references.

### Open the site

Open `site/index.html` in any modern browser — it is fully self-contained (no build step, no server). The interactive charts use the Plotly CDN, so the **chart panels need an internet connection**; all text, structure, and the static figures work offline.

### Use the skill

The skill at `.claude/skills/psychohistory/` runs in Claude Code. It routes a social/economic question onto the framework's layers (attention transport, blocks, reflexivity, criticality, observation) and emits a structured "psychohistory reading" with an explicit skill horizon. Read `SKILL.md` first — the **SAFETY guardrail is an enforced rule**: the skill is the *defensive* component and declines control-synthesis / manipulation requests.

### Run the sims

```sh
py -3.12 sims_v2.py          # regenerates the E1–E5 internal-consistency figures
```
Reproduces the verified primitives behind the paper's sim table (conservation, transport+drift, block LLN, criticality / N_eff collapse, fixed points).

### Run the validation scripts

Install dependencies, then run any script with `py -3.12`. Everything is **CPU-only, no GPU, no API keys** (the embedding model `all-MiniLM-L6-v2` is downloaded once and cached locally). The large raw/harvested data is **not committed** (it is gitignored); each test regenerates its own `data/` folder by running its `harvest_*.py` script first. The committed artifacts — the method document, analysis scripts, `RESULTS.md`, result JSON and figures — are everything needed to read and reproduce a result.

```sh
pip install -r requirements.txt
py -3.12 validation/pipeline_v03/semantic_csd.py
py -3.12 validation/engine/enkf_oneblock.py
py -3.12 validation/github/replicate_github.py
```

---

## Key results (see `RUN_AND_CHECK.md` and each `RESULTS.md`)

| Result | What it found | Standing |
|---|---|---|
| **Dynamic N_eff collapse — community-specificity** (`validation/neff_v4/`) | The criticality gear's prediction on a fresh roster: **9 of 12** r/wallstreetbets cascades collapse past their own block-label shuffle null, binomial *p* = 1.7×10⁻⁷. Depth on one substrate rather than breadth: three overlapping looks at WSB (11 of 12 v4 windows share days with a prior run's window). The Wikipedia arm is a different substrate and the rule does not carry to it — neither the event arm (0/14) nor the calm arm (0/10) fires, and identical code gives a median event null p90 of 0.4909 there against 0.0137 on WSB. | Measured on WSB; substrate-specific. |
| **GameStop counterfactual** (`validation/backtests/gamestop_counterfactual/`) | WSB activity rose ~6× before the GME spike; 6/6 meme tickers peaked the same week. Read at three resolutions, the episode sits **closer to a Seldon-crisis (structurally overdetermined) than a Mule** (single contingent agent). | single event; the ticker basket is selection-confirming by construction. |
| **Semantic critical-slowing-down** (`validation/pipeline_v03/`) | An embedding-variance (belief-dispersion) observable **discriminates** where the scalar volume proxy washed out: **+0.90** pre-onset on the endogenous GME cascade vs **+0.01** on the exogenous 2025 tariff shock. | n=2 labelled cascades; not a calibrated classifier. |
| **Operator-concentration invariant** (`validation/pipeline_v03/`, `major_player_signal/`) | A **time-invariant** concentration flag (HHI / Gini vs a base-rate null) fires pre-onset on **both** GitHub (4/5 repos) and Reddit, unifying the platform-specific 13-week-Reddit / days-GitHub ramp split. | small n; scale-free (Gini / top-5%) statistics are the cross-platform-comparable ones, not raw HHI. |
| **Cross-domain replication** (`validation/github/`) | Re-running the three Reddit tests on GitHub: **2 of 3 reproduce** — structural overdetermination (weak-replicate) and the impersonal-CSD non-result (replicates); the operator mechanism replicates in *concentration* but not in *temporal shape* (GitHub repos ignite within weeks, no months-long ramp). | 7 repos, 3 scorable events per test. |
| **Comment-concordance failure mode** (`validation/comment_concordance/`) | Scored against the *real* r/AskEconomics vetted answers (not textbook economics): 38 AGREE / 27 PARTIAL / 11 DISAGREE. The disagreements concentrate in an **over-applied concentration/bubble template** (5/11) that asserts runaway concentration where the expert deflates it. | Single LLM judge; a diagnostic result that located a specific over-applied template. |
| **EnKF forward test** (`validation/engine/`) | The assimilation loop runs strictly causally, **beats climatology**, is best-calibrated, but **ties persistence** (does not beat it). Its misspecification monitor **fires on a real regime break** (the April-2025 collapse) in real time. | One block, one series. |

---

## Dual-use notice

This framework is **dual-use**. The same prediction-control duality that yields early warning at a critical point also maximizes control leverage there: the moment of maximal predictability of a transition is the moment of maximal manipulability. The repository deliberately provides the **defensive / early-warning** components openly and **withholds the offensive control-synthesis layer** (the optimal-intervention solver and the message-selection / targeting objective). Anyone building on this work is asked to honor the same split. See **`ETHICS.md`** and the paper's governance section (§Governance) for the full statement and the conditions under which any control use could be legitimate.

---

## License

- **Code** (`sims*.py`, `site/`, `.claude/skills/.../scripts/`, `validation/**/*.py`): **MIT** — see [`LICENSE`](LICENSE).
- **Paper text, figures, and prose** (`psychohistory.tex`, the PDF, all figures, the prose in the site and the Markdown documents): **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

---

## How to cite

> Sharon, Wingston. *Conditions for Predictable Social Dynamics: Conservation, Decomposition, and Control at Criticality.* Draft v0.5, 2026.

```bibtex
@unpublished{sharon2026psychohistory,
  author = {Sharon, Wingston},
  title  = {Conditions for Predictable Social Dynamics: Conservation, Decomposition, and Control at Criticality},
  note   = {Draft v0.5, position paper. Developed with AI assistance (see the AI Contribution Declaration).},
  year   = {2026}
}
```

The manuscript was developed with AI assistance; see the **AI Contribution Declaration** at the end of `psychohistory.tex`. The human author directed the research, contributed its central conjectures, made all final scientific judgments, and takes full responsibility for the content.
