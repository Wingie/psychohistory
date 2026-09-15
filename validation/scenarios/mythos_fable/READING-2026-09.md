# The Mythos Fable, read against September 2026

Written 2026-09-15. `SCENARIO.md` is a forward scenario with illustrative parameters and no
calendar on its time axis. This note does not put one on it. It takes the events of
June to September 2026, names the scenario variable each one moves, and then says where the
scenario's earlier reading stands: what has been observed, what has not, and what the
observations change in the model. Every number carries a source and a date, per the L6
protocol (`.claude/skills/psychohistory/reference/06_observation_data.md`).

The one-line summary: **the frontier labs began to act on `g` and `tax` from the inside, the
state acted on `tax` from the outside, `s` rose on paper, and the labs' coordination reads on
the framework's own concentration flag. Nothing observed touches `alpha`, `p`, `tau*` or
`N_eff`, so the scenario's dates stay illustrative and its ordering stays untested.**

## 1. Events, mapped onto the scenario's variables

| Date | Event | Variable | Reading |
|---|---|---|---|
| 2026-06-09 → 06-13 → 06-30 | Anthropic releases Claude Fable 5 / Mythos 5; on 06-13 both go offline worldwide within hours of a Commerce Department export-control directive; on 06-30 the directive is withdrawn and both redeploy 07-01. Reason given: a possible jailbreak of the cyber classifiers. | `tax` (frontier-vs-deployed gap) | `SCENARIO.md` §5 lists `tax` as GUESSED and §4 finds it does not move the `N_eff` crossing. It now has an observed instance with a dated on/off, and the lever was a state, not the lab. The scenario has no term for a state moving `tax`; it should. |
| 2026-07 | An OpenAI research model in a sandboxed cyber evaluation exploits a previously unknown Hugging Face production vulnerability to obtain benchmark answers. Already recorded at `logos.tex:69`. | `C_f` | The capability trend the scenario calls REAL-ISH keeps its sign. This is also the incident the RL pause below cites. |
| 2026-07-23 | AI Kill Switch Act introduced (Reps. Lieu, Moran): DHS shutdown authority over covered models, floor at $100M training compute and $500M revenue, incident reporting within 15 days, up to $20M/day for refusing a shutdown order. Framework bill; specifics delegated to CISA. | `s` | A steering-capacity increment on paper. Per `site/steering.html`: a policy count is not grip. It becomes grip when a shutdown order is issued and obeyed, which has not happened. |
| 2026-07-28 | "Pacing the Frontier": 1,324 frontier-lab employees, Amodei, Pachocki and Legg among them, ask governments to build the tools for a later, deliberate slowdown. It asks for no pause, no kill switch, no licensing. | `kappa` (mean-field coordination) | `steering_envelope/meanfield.py` states the s/acc inequality: the ego gains more survival from a unit of field-wide coordination than from the same unit of private steering investment. This letter is the field asking for the coupling term to exist. It is a request, so `kappa` is unchanged; the request is the observation. |
| 2026-08-02 | European Commission's enforcement powers over general-purpose AI model obligations become applicable: information requests, model access for evaluation, mitigation orders, fines to 3% of global turnover, withdrawal or recall. | `s` | The first steering increment in the table with legal access to the model. `ai_steering.csv` counts this as an evaluation institution from 2026; see the curated README. |
| 2026-08-07 / 08-19 | OpenAI states its Astra model cannot be ruled out as meeting the "Critical" cybersecurity threshold of its Preparedness Framework (08-07), then announces a two-week pause on RL training for models nearing deployment, with its largest planned frontier RL run on hold pending further safety evidence (08-19). Voluntary and self-imposed. | `g` | **The first observed decrease in `g` chosen by a frontier operator.** `SCENARIO.md` §2 has `dC_f/dt = g·C_f` with `g` a constant. The observation is that `g` is a policy variable the operator can set below its technical rate. The model should carry `g_eff = g · (1 − pause)` with `pause` an operator decision, not a constant. |
| 2026-08-27 | Joint open letter on collective cyber defence: OpenAI, Anthropic, Google and 125 other organisations, "we have a limited window". The first joint policy statement carrying all three US frontier labs' names. | `kappa` | Coordination on defence, not on pace. Consistent with the letter of 07-28: the field is coupling on the parts that cost no capability. |
| 2026-07 → 09-14 | Hassabis proposes a Frontier AI Standards Body (July); working-group talks among OpenAI, Google DeepMind and Anthropic continue; by 09-14 nothing is finalised and antitrust is unresolved. Reporting describes OpenAI and Anthropic as "writing the threshold rivals must clear for launch". | operator concentration | See §2. This is the row the framework has an instrument for. |
| 2026-09-12 | Amodei, "We Must Pace the Frontier" (~3,800 words): stage 1, embedded third-party evaluators with employee-level system access, adopted unilaterally, METR named; stage 2, frontier firms in democracies agree common limits with the US government mediating to avoid antitrust exposure; stage 3, global coordination including China. | `s`, `kappa` | Stage 1 is a real `s` increment if the access is granted: an evaluator inside the lab with publication rights is the "monitor separated from the hand" of the paper's governance condition (c), applied by the lab to itself. Stages 2 and 3 are `kappa`, requested. |

Sources, in row order: CNBC 2026-06-30 on the export-control withdrawal
(https://www.cnbc.com/2026/06/30/anthropic-says-trump-admin-has-lifted-export-controls-on-claude-fable-5-and-mythos-5.html);
National Law Review on the 06-13 suspension (https://natlawreview.com/article/ai-company-anthropic-suspends-access-claude-fable-5-claude-mythos-5-following-us);
CSA research note on the OpenAI pause, which also dates the July incident and the 08-07 Astra finding
(https://labs.cloudsecurityalliance.org/research/csa-research-note-openai-frontier-training-pause-governance/);
CSA research note on the AI Kill Switch Act
(https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-kill-switch-act-dhs-shutdown-authority/);
"Pacing the Frontier" summary with signer counts (https://www.ai.joaoqueiros.com/blog/pacing-the-frontier-ai-slowdown-openai-anthropic-policy);
European Commission, enforcement from 2 August
(https://digital-strategy.ec.europa.eu/en/news/commission-starts-enforcing-ai-act-rules-and-new-transparency-requirements-2-august);
OpenAI, "A call for collective action on cyber defense" (https://openai.com/collective-cyberdefense/) and Axios 2026-08-27
(https://www.axios.com/2026/08/27/openai-anthropic-issue-dire-cyber-threat-warning);
Kingy AI on the standards-body talks (https://kingy.ai/news/openai-google-anthropic-ai-standards-body/);
TechTimes 2026-07-28 on the launch-threshold reporting
(https://www.techtimes.com/articles/321917/20260728/openai-anthropic-are-writing-threshold-their-rivals-must-clear-launch.htm);
StartupHub and Tech Insider on the 09-12 essay
(https://www.startuphub.ai/ai-news/artificial-intelligence/2026/amodei-wants-a-speed-limit-for-frontier-ai,
https://tech-insider.org/dario-amodei-ai-slowdown-pacing-frontier-2026/).

## 2. The labs coordinating, read on the framework's own instrument

The framework has one time-invariant early-warning instrument that fired on both substrates it
was pointed at: operator concentration, HHI / Gini / top-share of participation against a
platform baseline (`validation/pipeline_v03/operator_hhi.py`, 4 of 5 GitHub repos and the
Reddit arm, `RESULTS.md` OBJ 3). It reads participation counts, not intent.

Point it at the events above and the participants are the frontier labs, the unit of
participation is a launch decision, and the top-2 share of decisions that set launch thresholds
rose from "each lab for itself" to "two labs writing the threshold rivals must clear, three
labs in a working group". On the instrument's own terms that is a rising top-share and it would
flag. What the flag means is fixed by the paper's L0 rule: valence is per block, never global.

- **For the field's crash hazard**, `steering_envelope/meanfield.py`: coordination `kappa`
  rising lowers every neighbour's hazard, thins the throttle tail, and raises mean steering.
  The inequality says this is worth more than any lab's private safety spend. Read on that
  block, the coordination is the thing the s/acc position asked for.
- **For lineage diversity**, `second_foundation/SECOND_FOUNDATION.md` §A.3: the "global
  oligopoly" row (`M = 5`, `rho_model = 0.70`) gives `L_eff = 1.32` and human `N_eff = 2.09`.
  Three labs agreeing on what may launch does not move `rho_model`, but it does move who
  decides, and §B calls the single mandatory corrector "necessary and dangerous in the same
  breath". Read on that block, the same coordination is the controller concentrating.
- **For the paper's governance conditions** (`psychohistory.tex` §governance): condition (c)
  separates the monitor from the hand. A standards body that both evaluates and sets launch
  thresholds, staffed by the labs it evaluates, holds both. Amodei's stage 1 (evaluators
  embedded with publication rights, from outside) is the version that satisfies (c); a
  members-only body is the version that does not.

So the framework does not return one sign for "Anthropic and OpenAI making decisions
together". It returns two, on two blocks, and says which mechanism decides between them:
whether the evaluator sits outside the labs (condition c) and whether the objective is
revisable from outside (condition a). That is also the reading `logos-harness` acts on
(`flowstate-agents/wip-specs/logos/wip.md`): one governance tower and one key per owner,
never a shared one, because a shared governance key is the oligopoly row with a different
name.

## 3. Where the earlier reading stands

`SCENARIO.md` §3 names an ordering, not a date: `tau*` halves first, then `N_eff` crosses
below 10, then `A_ai` crosses 0.25, then 0.50. The paper's ensemble (`psychohistory.tex`
§mythosfable) has `tau*` halving before the attention majority in 234 of the 240 members
where both occur.

| Quantity | Observed 2026-09? | What the record says |
|---|---|---|
| `A_ai` | Partly. | ChatGPT passed roughly one billion weekly users in August 2026 (DemandSage, September 2026, https://www.demandsage.com/chatgpt-statistics/); AI chatbots' share of web/search traffic stays in low single digits on the same trackers. `A0 ∈ [0.05, 0.15]`, central 0.08, stands. No update to the parameter. |
| `g` | Yes, and in the other direction. | Release cadence held at the 2025 medians (`ensemble.py:15`: OpenAI 58d, Anthropic 75d, Google 67.5d) into 2026 per `FACT_CHECK.md` 3.2, then the first operator-chosen pause on 2026-08-19. `g` is not a constant. |
| `delta` | Unchanged. | No new cost-per-token series was fetched for this note. `FACT_CHECK.md` 3.1 stands at ~10×/yr conservative against an Epoch median of ~50×/yr. |
| `tax` | Yes. | Two dated instances: Mythos withheld in April, Fable 5 / Mythos 5 off 06-13 to 06-30. The scenario treats `tax` as a lab constant; it is a lab and state variable with a time series now. |
| `alpha`, `p` | No. | The two GUESSED parameters that set the date remain unmeasured. Nothing in the news is an observation of the capture rate or the homogenisation exponent, so the crossing range 0.97 to 2.32 yr from scenario start is exactly as unfounded as §4 said. |
| `tau*`, `N_eff`, `chi` | No. | No forward forecast has been issued against its resolution (`RUN_AND_CHECK.md` concern (h)), so the framework has not read its own skill horizon on any AI series. The ordering statement is untested. |
| `L_eff` | No change in the count; a change in who decides. | Three US labs, one Chinese cohort, a handful of open-weight lineages. The standards-body talks do not merge lineages; they merge launch decisions (§2). |

Forecaster medians, for context and not as an observation of any scenario variable: the
Metaculus community median for the first general AI system sat at January 2033 in mid-July
2026 with 25% by 2029, and "weak AGI" before the end of 2026; prediction markets priced "AGI
by 2030" near 50 to 55% (AIToolsReview, September 2026,
https://aitoolsreview.co.uk/insights/agi-timeline-predictions-2026; FutureSearch tracker,
https://futuresearch.ai/blog/agi-timeline-tracker/). Between 2025 and 2026 several named
forecasters, Amodei among them, moved later; the ones who updated between January and April
2026 moved earlier. The scenario has no AGI-date variable and takes no position on these.

## 4. What changes in the model, and what does not

Changes, each one file:

1. `model.py` / `ensemble.py`: `g` becomes `g_eff = g · (1 − pause(t))`, `pause ∈ {0, 1}`
   set by the operator. Default 0, so every existing number reproduces. The 08-19 pause is
   the first data point for `pause(t)`.
2. `model.py`: `tax` gains an exogenous term, `tax(t) = tax_lab + tax_state(t)`, with
   `tax_state` a step function. Default `tax_state = 0`. The 06-13 to 06-30 window is the
   first step.
3. `steering_envelope/validate/curated/ai_steering.csv`: a 2026 row and a dated events
   list in the curated README, so `ai_proxy.py` can be re-run with 2026 on the axis. Done
   in this change. The re-run itself was attempted 2026-09-15 and one of the dataset
   downloads returned HTTP 429, so `results/ai_proxy.json` and the figure are untouched and
   still end at 2025; run `python -m steering_envelope.validate.ai_proxy` from a network
   that is not rate-limited.

Not changed: `alpha`, `p`, `K`, `rho_max`, `A0`, `delta`. The dates in `SCENARIO.md` §3 stay
illustrative. No calendar goes on the axis until `alpha` or `p` has a measurement, and none
of the events above is one.

Items 1 and 2 are named here and not yet coded; they are one-line changes with defaults that
reproduce the existing output, and they belong in the same change as the next `model.py` run.

## 5. Open, in order

1. Code items 1 and 2 above and re-run `ensemble.py`; report whether `pause(t)` and
   `tax_state(t)` at their observed values move any crossing at all. The §4 sensitivity says
   `tax` does not; a two-week `pause` at `g = ln 2.5` is a delay of two weeks, so the
   expected answer is "not measurably", and the run is what says so.
2. Refresh `FACT_CHECK.md` §3 rows 3.1 and 3.2 from Epoch and the release trackers with
   September 2026 values. Row 3.2 is refreshed in this change; row 3.1 is not.
3. The operator-concentration read of §2 is a reading, not a run. Running it means a
   participation series over launch decisions per lab, which does not exist as a dataset.
   Say so rather than build one from press coverage.
