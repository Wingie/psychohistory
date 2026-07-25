# Conditions for Predictable Social Dynamics

*A bounded, falsifiable engineering specification for a weak form of Asimov's psychohistory — with a verified internal-consistency engine, an interactive website, a Claude skill, and a preliminary empirical-validation suite.*

This repository accompanies the position paper ***Conditions for Predictable Social Dynamics: Conservation, Decomposition, and Control at Criticality*** (Wingston Sharon). The paper asks whether collective human behaviour can be forecast like the weather, argues that social systems possess *partial, conditional* analogues of the three properties that make numerical weather prediction work (conservation laws, weak multi-scale coupling, non-reflexivity), and assembles them into an explicit, regime-aware engineering specification with a stated boundary of where it must fail.

**▶ Live interactive site: https://wingie.github.io/psychohistory/** — a four-page guide (Home · Tutorial · The math · Tests &amp; data) that teaches the framework, renders every equation, and walks through every test run against real data. The same content is in [`site/`](site/) and works offline.

---

## Honest status (read this first)

This is a **position paper plus a pre-registered validation suite on proxy data. The forecasting claims remain unvalidated, and the one structural prediction that was reported as passing has been retracted by this repository's own re-analysis.**

- The framework's *forecasting* claims are **conjectures of a research program, not results.** Of the four forward-forecast falsifiers, one has already run and three have not. (iv) smooth-regime skill is **DONE-PILOT / RUNNABLE-NOW** in `RUN_AND_CHECK.md`: a strictly-causal one-block EnKF walk-forward that beats climatology, **ties persistence**, and is an honest negative on the strong claim. (v) fixed-point reliability and (vii) regime occupancy are **NEEDS-DATA**, not compute-blocked: they need a lodged announcement/question set and a regime monitor operationalised on a named series, and could start on the hardware already here. (vi) Lucas invariance needs the multi-block coupled engine **and** a multi-regime reanalysis corpus. **The binding constraint the ledger names is the open social-reanalysis corpus (E-6), not compute**; `RUN_AND_CHECK.md` labels none of the four compute-blocked, and `psychohistory.tex` calls the same corpus an access problem rather than an existence one. This is independent research; correspondence to `wingston.sharon@gmail.com`. The paper is **v0.5, in review**; it reaches v1.0 when these turn green.
- **The structural core is untested too, and the claim that it was is withdrawn.** This bullet used to say that the **dynamic N_eff collapse** — the criticality gear — had its community-specificity prediction *SEALED as a pre-registered pass on a fresh roster* (`validation/neff_v4/`: 9 of 12 r/wallstreetbets cascades collapse past their own block-label shuffle, binomial *p* = 1.7×10⁻⁷). **That pass is retracted and the p-value is withdrawn.** The entire figure came from an assumed null fire rate of `p0 = 0.10`, asserted from the construction of the test rather than measured. The assertion needs the observed statistic to be exchangeable with its null draws, and it is not: the observation uses a modularity-optimised Louvain partition while every null draw is a uniform relabelling of the same people. Measured four ways, the rule's real false-fire rate on quiet windows comes out between **0.49 and 0.83**; the decision rule breaks above **0.378**. Worse, the shuffle null is degenerate on this substrate — its 90th percentile has a median of 0.014 against drops of 0.24 — so the test reduces to a sign check on whether the drop came out positive, and it fired on 8 of 10 non-event windows too. Under the null the hypothesis actually implies (hold the community and the series fixed, move the onset), the best proxy computable from committed data fires on **0 of 12** cascades. **No replacement p-value is asserted**, because none has been measured to a defensible point value. The full measurement, the comparison of candidate nulls, and the corrected verdict are in [`validation/neff_v4/NULL_RECALIBRATION.md`](validation/neff_v4/NULL_RECALIBRATION.md); the frozen re-test is [`validation/neff_v5/PRE_REGISTRATION_neff_v5.md`](validation/neff_v5/PRE_REGISTRATION_neff_v5.md). Test (ii') is **open**: not passed, not refuted, and never yet tested on the endpoint that carries the claim.
- Two further things this bullet used to get wrong, both found by an independent round-2 review and both still true after the retraction: the r/wallstreetbets work is **one substrate looked at three times, not four independent confirmations** (the three runs share the same subreddit, the same dump and the same top-commenter graph, and 11 of the 12 v4 analysis windows share calendar days with a window from a prior run, up to 81% overlap, so the rosters are disjoint in onset date only); and the Wikipedia arm is **not** a fourth confirmation, since neither its event arm (0 of 14 fire) nor its calm arm (0 of 10 fire) fires. The Wikipedia-versus-WSB contrast turns out to be largely null geometry rather than community structure: the identical code gives a median event null p90 of 0.4909 on Wikipedia against 0.0137 on WSB, roughly 36x. The threshold was frozen before the data was harvested and never moved, and that remains true; it is the null, not the threshold, that failed. The blunter raw-magnitude reading is still reported, honestly, as non-discriminating.
- The second-wave battery is otherwise a deliberate deflation, exactly in the shape the *bounded* thesis predicts: early warning is a **partial** positive (beats a calm null, can't separate endo/exo), the bifurcation-mix conjecture is **refuted**, and conservation at basket scale is **contradicted**. The impersonal/structural machinery is real but load-bearing only on the endogenous, reflexive minority of episodes.
- All numerical figures in the paper (E1–E5) are **internal-consistency checks of the paper's own equations**, not empirical evidence.
- The full assimilating engine, a powered forward forecast that beats persistence, and the open social-reanalysis corpus **do not yet exist.** See `RUN_AND_CHECK.md` for the complete, adversarial status ledger and [`validation/NEFF_COLLAPSE_SYNTHESIS.md`](validation/NEFF_COLLAPSE_SYNTHESIS.md) for the full six-pass account of the retracted headline result.

If you take one thing from this repo: it is a *careful specification and an honest map of what is and is not yet known*, not a working oracle.

### The LOGOS companion paper (v0.2, new)

`logos.tex` applies the same discipline to a different object: the **machines** rather than the societies. It specifies a 10T+ Mixture-of-Towers from published 2024 to 2026 components, then audits it adversarially. **No model in it has been trained and no system has been served.** Its status is worse than psychohistory's, not better: psychohistory has a validation suite that has run, reported negatives, and retracted its own headline positive when the null was checked, whereas LOGOS has zero runs. What it does have is arithmetic that has been checked, citations verified against primary sources, its weakest components relocated or withdrawn, and ten falsifiers each stated with the hardware it needs.

It now also has an **independent, adversarial round-2 referee report** ([`logos/REVIEW_ROUND2.md`](logos/REVIEW_ROUND2.md), 2026-07-25): 46 findings survived a refutation pass in which a second pass tried to kill each one, graded 2 CRITICAL, 6 HIGH, 18 MEDIUM, 20 LOW. **Both CRITICAL findings are open.** The first is in the abstract: the two debate papers are cited for a diversity conclusion that both explicitly disclaim, and that conclusion is the only architectural item among the paper's three stated original contributions. The second is in the psychohistory validation suite that `logos-harness` names as its adjudicator, where the assumed null fire rate is contradicted by a fire rate this repository itself measured. Round 1 was structurally unable to catch either: it was written by the same process that wrote the paper, a citation check cannot check a claim that carries no citation, and it never opened the validation suite.

The paper's conclusion is not the one it set out to reach. Four separate literatures converge on a single point: debate among agents holding the same information is a martingale, so expected correctness does not improve; RL with verifiable rewards sharpens sampling without expanding the set of solvable problems; recursive self-training without external grounding provably degenerates; and self-play works when, and only when, something external checks the answer. Put together, they say that **capability at this scale is bounded by observation bandwidth, not by parameters or compute.** Scale buys the capacity to be corrected quickly. It does not buy the corrections.

That is where the two papers meet, and the meeting is not comfortable for either. Psychohistory ends at an observability trilemma: complete predictability would require total observability, which is surveillance, and it rejects the limit. LOGOS ends at an observation bound: improvement past human text is set by how fast the world corrects the model. Both terminate on the same quantity from opposite sides, and when the something being observed is people, the two limits are one limit.

Running the other way, `logos-harness` needs an adjudicator the model cannot fake, and psychohistory's validation pipeline is one. The reverse coupling is far narrower than earlier drafts of this README claimed, and the round-2 review is what caught it: the harness could supply the multi-block forward engine that falsifier (vi) needs, **if** the multi-regime reanalysis corpus existed. It supplies neither that corpus (E-6), nor the lodged announcement set (v) needs, nor the operationalised regime monitor (vii) needs, and (iv) has already run without it. So the dependency runs mostly one way, and "the same missing piece approached from two directions" was an overstatement.

---

## Repository map

| Path | What it is |
|---|---|
| `psychohistory.tex` / `psychohistory.pdf` | The paper (~79 pp). Sole author Wingston Sharon; includes an AI Contribution Declaration. |
| `sims.py`, `sims_v2.py` | The verified internal-consistency simulations (E1–E5). Outputs in `_verify_out/` and `figures/`. |
| `site/` | The four-page interactive site ([live](https://wingie.github.io/psychohistory/)): **Home** (thesis + canon), **Tutorial** (the layers + a worked GameStop walkthrough), **The math** (every equation with KaTeX + three live demos + the AI scenario), and **Tests &amp; data** (the full empirical program). Open `site/index.html` to run it offline. |
| `.claude/skills/psychohistory/` | A Claude skill: `SKILL.md` (with a dual-use SAFETY guardrail), reference modules `00`–`09` (including a build-your-own guide), `scripts/engine.py`, a `corpus/`, and a coverage report under `results/`. |
| `steering_envelope/` | **The Steering Envelope (s/acc): one axiom, one theorem** — the program's first *intervention* module, postulated 2026. New primitive: Ashby's Control Axiom (requisite variety); combined with the program's accumulation and plurality premises it yields the Survival Theorem: societies survive technology in proportion to the control they exert over its speed. The hazard law h = σ(β(v·k/(s·c₀) − 1)) — control-loss risk as speed over steering capacity — as a Python engine (race model, mean-field N-actor coordination theorem, Sustenance Ledger tribes layer) plus a pre-registered validation suite on public data: US roads, world aviation, the JST macrohistory panel (the ratio model wins out-of-sample, LORO AUC 0.688 vs 0.506 for credit growth alone), nuclear as a case study, and AI leading indicators. Essay at [`site/steering.html`](site/steering.html), interactive v0.4 instrument at [`site/steering_sim.html`](site/steering_sim.html), falsifiers in [`steering_envelope/README.md`](steering_envelope/README.md). |
| `logos.tex` | **The LOGOS paper** (v0.2): *Ten Trillion Parameters, and the Limit That Scale Does Not Move*. A companion position paper on the machines rather than the societies. It specifies a 5x2.8T Mixture-of-Towers, audits its arithmetic, and finds that the arithmetic points somewhere the architecture did not intend. Three corrections drive it: the usual "10T is impossible" argument prices a **dense** model nobody is building (a sparse tower costs 55x less to train and already exists); splitting a parameter budget across towers does **not** reduce total tokens consumed, only the peak *unique*-corpus requirement; and the EU AI Act's 10^25 FLOP presumption is written against *a model*, so a composed ensemble has no settled answer to "how many models is this." Following the corrections leads to the thesis: sparsity removes the compute limit, tower decomposition raises the data ceiling, 4-bit serving handles memory, and **none of them touches the rate at which something outside the model can tell it it is wrong.** A fourth correction runs against the design it starts from: applying the paper's own three-axis partition criterion (corpus disjointness, objective conflict, update cadence) says **four towers, not five** (Mathematics and Logic fail all three axes and should merge). The paper states that in its abstract, in §3.4 and in its conclusion, and it also states that settling four-versus-five needs corpus-overlap measurements that have not been run. |
| `logos/` | The LOGOS companion directory: [`REVIEW_ROUND2.md`](logos/REVIEW_ROUND2.md) (**the independent round-2 referee report**, adversarial and independent of the process that wrote the paper: 46 findings surviving a refutation pass, 2 CRITICAL, 6 HIGH, 18 MEDIUM, 20 LOW; **both CRITICAL findings are open**, and §6 records what round 2 checked and found sound), [`ARCHITECTURE_REVIEW.md`](logos/ARCHITECTURE_REVIEW.md) (15 findings, 3 critical; after round 2's re-grade, **four are not closed** (F-04 needs a training run, F-13's sparse-dispatch cost model is not re-derived, F-14's partition is argued but unmeasured, F-15's headroom consequence is unquantified) and **two are closed only in part** (F-09, F-10)), [`BIBLIOGRAPHY_REVIEW.md`](logos/BIBLIOGRAPHY_REVIEW.md) (every citation checked against a primary source: 21 verified, 4 corrected, 4 downgraded to blog-grade sourcing, 3 dropped as unsourceable, 11 missing attributions supplied; round 2 found the method structurally cannot catch a load-bearing claim that carries no citation, and lists two such claims it missed), [`GAPS.md`](logos/GAPS.md) (the measurement ledger: ten falsifiers, **five** of them on one consumer accelerator, with F5 falling out of F9 for free; the falsifier table is **not** the whole of the open work, and four items in its §4 need no accelerator at all), [`F9_PREREGISTRATION.md`](logos/F9_PREREGISTRATION.md) (a sealable pre-registration for F9, the observation-bound falsifier, which says first and loudest that F9 is **underpowered at the budget the ledger assigns it**: one seed per arm buys no within-arm variance and therefore no test statistic), [`TIER0_3090_PLAN.md`](logos/TIER0_3090_PLAN.md) (what actually runs on the owned 3090, priced in GPU-hours and electricity, with the pre-committed kill conditions), and [`LOGOS_HARNESS.md`](logos/LOGOS_HARNESS.md) (**`logos-harness`**: the implementation spec for the bootstrap loop, tested on Pokemon for volume and on **this repository's own psychohistory pipeline** for validity). |
| `validation/` | All the empirical + scenario work, one directory per test (pre-registration + analysis script + `RESULTS.md` + result JSON + figures): `neff_v4/` (RETRACTED, with its `NULL_RECALIBRATION.md`), the frozen re-test `neff_v5/`, and their `neff_v2/`, `neff_v3/`, `wikipedia/` siblings, the early-warning battery, bifurcation-mix, conservation-ecosystem, the GameStop counterfactual + operator-signal backtests, GitHub cross-domain replication, the EnKF forward test, scenario sims, Kuramoto, the v0.3 observation-operator pipeline, pre-registration, fact-check, and the run-and-check guide. Raw/harvested data is gitignored and regenerable from each test's harvest script. |
| `RUN_AND_CHECK.md` | The adversarial status ledger: every claim needing code/data/a derivation, cross-referenced to its artifact, marked DONE / PILOT / PENDING / NOT-STARTED. |
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
| **Dynamic N_eff collapse — community-specificity** (`validation/neff_v4/`, retracted in [`NULL_RECALIBRATION.md`](validation/neff_v4/NULL_RECALIBRATION.md)) | Reported as the criticality gear's prediction sealed on a fresh roster: **9 of 12** r/wallstreetbets cascades collapsing past their own block-label shuffle null at binomial *p* = 1.7×10⁻⁷. **Withdrawn.** The p-value rests entirely on an assumed false-fire rate `p0` = 0.10 that measurement puts between **0.49 and 0.83** (the rule breaks above 0.378), and the shuffle null is degenerate on this substrate: median null p90 0.014 against drops of 0.24, so the test reduces to a sign check and fired on 8 of 10 non-event windows. Under an onset-aligned null the best committed-data proxy fires on **0 of 12**. What survives is one cascade in twelve against a non-degenerate null. Also not four independent confirmations: three overlapping looks at one substrate (11 of 12 v4 windows share days with a prior run's window), plus a Wikipedia arm in which neither the event arm (0/14) nor the calm arm (0/10) fires. | **RETRACTED** — no replacement p-value is asserted. Test (ii') is **open**: never tested on the endpoint that carries the claim. Frozen re-test: [`validation/neff_v5/`](validation/neff_v5/PRE_REGISTRATION_neff_v5.md). |
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
