# Conditions for Predictable Social Dynamics

*A bounded, falsifiable engineering specification for a weak form of Asimov's psychohistory — with a verified internal-consistency engine, an interactive website, a Claude skill, and a preliminary empirical-validation suite.*

This repository accompanies the position paper ***Conditions for Predictable Social Dynamics: Conservation, Decomposition, and Control at Criticality*** (Wingston Sharon). The paper asks whether collective human behaviour can be forecast like the weather, argues that social systems possess *partial, conditional* analogues of the three properties that make numerical weather prediction work (conservation laws, weak multi-scale coupling, non-reflexivity), and assembles them into an explicit, regime-aware engineering specification with a stated boundary of where it must fail.

**▶ Live interactive site: https://wingie.github.io/psychohistory/** — a four-page guide (Home · Tutorial · The math · Tests &amp; data) that teaches the framework, renders every equation, and walks through every test run against real data. The same content is in [`site/`](site/) and works offline.

---

## Honest status (read this first)

This is a **position paper plus a pre-registered validation suite on proxy data. The forecasting claims remain unvalidated; one structural prediction now passes a pre-registered fresh-roster test.**

- The framework's *forecasting* claims are **conjectures of a research program, not results.** Four falsifiers (smooth-regime skill, fixed-point reliability, Lucas invariance, regime occupancy) are **pending a live world-model training run** — the forward engine (a trained world model + an LLM/LRM ensemble). They are blocked on **compute, not data**. This is independent research: **compute donations directly unblock these tests** — contact the author at `wingston.sharon@gmail.com`. The paper is **v0.5, in review**; it reaches v1.0 when these four turn green.
- But the structural core is no longer untested. The **dynamic N_eff collapse** — the criticality gear — has its community-specificity prediction **SEALED as a pre-registered pass on a fresh roster** (`validation/neff_v4/`: 9 of 12 r/wallstreetbets cascades collapse past their own block-label shuffle, binomial *p* = 1.7×10⁻⁷; confirmed four times across two substrates). The threshold was frozen before the data was harvested and never moved; the blunter raw-magnitude reading is reported, honestly, as non-discriminating.
- The second-wave battery is otherwise a deliberate deflation, exactly in the shape the *bounded* thesis predicts: early warning is a **partial** positive (beats a calm null, can't separate endo/exo), the bifurcation-mix conjecture is **refuted**, and conservation at basket scale is **contradicted**. The impersonal/structural machinery is real but load-bearing only on the endogenous, reflexive minority of episodes.
- All numerical figures in the paper (E1–E5) are **internal-consistency checks of the paper's own equations**, not empirical evidence.
- The full assimilating engine, a powered forward forecast that beats persistence, and the open social-reanalysis corpus **do not yet exist.** See `RUN_AND_CHECK.md` for the complete, adversarial status ledger and [`validation/NEFF_COLLAPSE_SYNTHESIS.md`](validation/NEFF_COLLAPSE_SYNTHESIS.md) for the full six-pass account of the headline result.

If you take one thing from this repo: it is a *careful specification and an honest map of what is and is not yet known*, not a working oracle.

---

## Repository map

| Path | What it is |
|---|---|
| `psychohistory.tex` / `psychohistory.pdf` | The paper (~79 pp). Sole author Wingston Sharon; includes an AI Contribution Declaration. |
| `sims.py`, `sims_v2.py` | The verified internal-consistency simulations (E1–E5). Outputs in `_verify_out/` and `figures/`. |
| `site/` | The four-page interactive site ([live](https://wingie.github.io/psychohistory/)): **Home** (thesis + canon), **Tutorial** (the layers + a worked GameStop walkthrough), **The math** (every equation with KaTeX + three live demos + the AI scenario), and **Tests &amp; data** (the full empirical program). Open `site/index.html` to run it offline. |
| `.claude/skills/psychohistory/` | A Claude skill: `SKILL.md` (with a dual-use SAFETY guardrail), reference modules `00`–`09` (including a build-your-own guide), `scripts/engine.py`, a `corpus/`, and a coverage report under `results/`. |
| `steering_envelope/` | **Axiom One: the Steering Envelope (s/acc)** — the program's first *intervention* axiom, postulated 2026: societies survive technology in proportion to the control they exert over its speed. The hazard law h = σ(β(v·k/(s·c₀) − 1)) — control-loss risk as speed over steering capacity — as a Python engine (race model, mean-field N-actor coordination theorem, Sustenance Ledger tribes layer) plus a pre-registered validation suite on public data: US roads, world aviation, the JST macrohistory panel (the ratio model wins out-of-sample, LORO AUC 0.688 vs 0.506 for credit growth alone), nuclear as a case study, and AI leading indicators. Essay at [`site/steering.html`](site/steering.html), interactive v0.4 instrument at [`site/steering_sim.html`](site/steering_sim.html), falsifiers in [`steering_envelope/README.md`](steering_envelope/README.md). |
| `validation/` | All the empirical + scenario work, one directory per test (pre-registration + analysis script + `RESULTS.md` + result JSON + figures): the headline `neff_v4/` (SEALED PASS) and its `neff_v2/`, `neff_v3/`, `wikipedia/` siblings, the early-warning battery, bifurcation-mix, conservation-ecosystem, the GameStop counterfactual + operator-signal backtests, GitHub cross-domain replication, the EnKF forward test, scenario sims, Kuramoto, the v0.3 observation-operator pipeline, pre-registration, fact-check, and the run-and-check guide. Raw/harvested data is gitignored and regenerable from each test's harvest script. |
| `RUN_AND_CHECK.md` | The adversarial status ledger: every claim needing code/data/a derivation, cross-referenced to its artifact, marked DONE / PILOT / PENDING / NOT-STARTED. |
| `ETHICS.md` | The responsible-use / dual-use notice (the defensive/offensive split). |
| `requirements.txt` | CPU-only Python dependencies for the sims and validation scripts. |

---

## How to

### Build the paper

```sh
pdflatex psychohistory.tex
pdflatex psychohistory.tex      # run twice to resolve refs/ToC
```
Requires a TeX distribution (MiKTeX or TeX Live). A pre-built `psychohistory.pdf` is included.

### Open the site

Open `site/index.html` in any modern browser — it is fully self-contained (no build step, no server). The interactive charts use the Plotly CDN, so the **chart panels need an internet connection**; all text, structure, and the static figures work offline.

### Use the skill

The skill at `.claude/skills/psychohistory/` runs in Claude Code. It routes a social/economic question onto the framework's layers (attention transport, blocks, reflexivity, criticality, observation) and emits a structured "psychohistory reading" with an explicit skill horizon and falsifiers. Read `SKILL.md` first — the **SAFETY guardrail is an enforced rule**: the skill is the *defensive* component and declines control-synthesis / manipulation requests.

### Run the sims

```sh
py -3.12 sims_v2.py          # regenerates the E1–E5 internal-consistency figures
```
Reproduces the verified primitives behind the paper's sim table (conservation, transport+drift, block LLN, criticality / N_eff collapse, fixed points).

### Run the validation scripts

Install dependencies, then run any script with `py -3.12`. Everything is **CPU-only, no GPU, no API keys** (the embedding model `all-MiniLM-L6-v2` is downloaded once and cached locally). The large raw/harvested data is **not committed** (it is gitignored); each test regenerates its own `data/` folder by running its `harvest_*.py` script first. The committed artifacts — pre-registration, analysis scripts, `RESULTS.md`, result JSON and figures — are everything needed to read and audit a result.

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
| **Dynamic N_eff collapse — community-specificity** (`validation/neff_v4/`) | The criticality gear's actual prediction, sealed on a fresh roster: **9 of 12** r/wallstreetbets cascades collapse past their own block-label shuffle null (binomial *p* = 1.7×10⁻⁷; median cascade beats all 300 reshuffles). Confirmed four times across two substrates. The raw-magnitude reading is reported, separately, as non-discriminating. | **SEALED PASS** — pre-registered, frozen binomial rule, fresh disjoint roster; the threshold was never moved. The program's most rigorous positive. |
| **GameStop counterfactual** (`validation/backtests/gamestop_counterfactual/`) | WSB activity rose ~6× before the GME spike; 6/6 meme tickers peaked the same week. Read at three resolutions, the episode sits **closer to a Seldon-crisis (structurally overdetermined) than a Mule** (single contingent agent). | *preliminary* — single event; the ticker basket is selection-confirming by construction. |
| **Semantic critical-slowing-down** (`validation/pipeline_v03/`) | An embedding-variance (belief-dispersion) observable **discriminates** where the scalar volume proxy washed out: **+0.90** pre-onset on the endogenous GME cascade vs **+0.01** on the exogenous 2025 tariff shock. | *preliminary* — n=2 labelled cascades; not a calibrated classifier. |
| **Operator-concentration invariant** (`validation/pipeline_v03/`, `major_player_signal/`) | A **time-invariant** concentration flag (HHI / Gini vs a base-rate null) fires pre-onset on **both** GitHub (4/5 repos) and Reddit, unifying the platform-specific 13-week-Reddit / days-GitHub ramp split. | *preliminary* — small n; scale-free (Gini / top-5%) statistics are the cross-platform-comparable ones, not raw HHI. |
| **Cross-domain replication** (`validation/github/`) | Re-running the three Reddit tests on GitHub: **2 of 3 reproduce** — structural overdetermination (weak-replicate) and the impersonal-CSD non-result (replicates); the operator mechanism replicates in *concentration* but not in *temporal shape* (GitHub repos ignite within weeks, no months-long ramp). | *preliminary* — 7 repos, 3 scorable events per test. |
| **Comment-concordance failure mode** (`validation/comment_concordance/`) | Scored against the *real* r/AskEconomics vetted answers (not textbook economics): 38 AGREE / 27 PARTIAL / 11 DISAGREE. The disagreements concentrate in an **over-applied concentration/bubble template** (5/11) that asserts runaway concentration where the expert deflates it. | *preliminary* — single LLM judge; an honest, diagnostic negative. |
| **EnKF forward test** (`validation/engine/`) | The assimilation loop runs strictly causally, **beats climatology**, is best-calibrated, but **ties persistence** (does not beat it). Its misspecification monitor **fires on a real regime break** (the April-2025 collapse) in real time. | *preliminary* — one block, one series; an honest negative for the strong forward-skill claim. |

---

## Dual-use notice

This framework is **dual-use**. The same prediction-control duality that yields early warning at a critical point also maximizes control leverage there: the moment of maximal predictability of a transition is the moment of maximal manipulability. The repository deliberately provides the **defensive / early-warning** components openly and **withholds the offensive control-synthesis layer** (the optimal-intervention solver and the message-selection / targeting objective). Anyone building on this work is asked to honor the same split. See **`ETHICS.md`** and the paper's governance section (§Governance) for the full statement and the conditions under which any control use could be legitimate.

---

## License

- **Code** (`sims*.py`, `site/`, `.claude/skills/.../scripts/`, `validation/**/*.py`): **MIT** — see [`LICENSE`](LICENSE).
- **Paper text, figures, and prose** (`psychohistory.tex`, the PDF, all figures, the prose in the site and the Markdown documents): **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

---

## How to cite

> Sharon, Wingston. *Conditions for Predictable Social Dynamics: Conservation, Decomposition, and Control at Criticality.* Draft v0.5 (in review), 2026.

```bibtex
@unpublished{sharon2026psychohistory,
  author = {Sharon, Wingston},
  title  = {Conditions for Predictable Social Dynamics: Conservation, Decomposition, and Control at Criticality},
  note   = {Draft v0.5, position paper (in review). Developed with AI assistance (see the AI Contribution Declaration).},
  year   = {2026}
}
```

The manuscript was developed with AI assistance; see the **AI Contribution Declaration** at the end of `psychohistory.tex`. The human author directed the research, contributed its central conjectures, made all final scientific judgments, and takes full responsibility for the content.
