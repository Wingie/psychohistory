# Steering Envelope — s/acc as a testable hazard model

A module of the [psychohistory](../README.md) repository. Python reference
implementation of the Steering Envelope race model (ported from the JS v0.2
artifact), a mean-field N-actor extension, the v0.3 Sustenance Ledger
society layer, and an empirical validation suite that tests the core
structural claim against public historical datasets. The interactive v0.4
instrument lives at [`../site/steering_sim.html`](../site/steering_sim.html)
and shares these equations; the essay is [`page.md`](page.md) (rendered at
[`../site/steering.html`](../site/steering.html)).

## The claim under test

For any technology transition, control-loss risk at a critical threshold
(a "corner") is logistic in the ratio of deployment velocity to steering
capacity:

    h = sigma( beta * ( (v * k) / (s * c0) - 1 ) )

where `v` is deployment/capability velocity, `s` is steering capacity
(regulation, verification, operator skill, institutional absorption), `k`
is corner tightness, `beta` hazard steepness, `c0` normalization.

The four flags encoded alongside it: **e/acc** maximizes v unconditionally
(engine); **d/acc** reallocates v toward defense-dominant tech (armor);
**s/acc** constrains v <= f(s) — throttle bounded by grip (steering, our
thesis); **w/acc** grows the judgment feeding s (driver).

The validation question: **does v/s predict realized disaster rates across
historical transitions better than v alone or s alone?**

## Layout

    model.py            capability path, corners, hazard, Monte Carlo (JS v0.2 port)
    meanfield.py        N actors; coordination kappa; theorem check
    society.py          Sustenance Ledger: basket, labour channels, 8 tribes,
                        hours-per-week-of-essentials, PROOF table
    validate/
      datasets.py       cached loaders (JST, FHWA-via-Wikipedia, OWID, World
                        Bank, Epoch AI) + curated steering indices
      fit.py            nested logistic/Gaussian comparisons, AUC, AIC/BIC,
                        LR tests, leave-one-decade-out
      roads.py aviation.py finance.py nuclear.py ai_proxy.py run_all.py
      curated/          committed hand-coded s-proxies, sources + honesty notes
      data/             raw downloads (gitignored, regenerable)
      results/          per-domain JSON results
    notebooks/          01_model.ipynb, 02_validation.ipynb (executed)
    tests/              pytest acceptance suite
    figures/            generated figures (dark instrument style)

Quickstart:

    pip install -r ../requirements.txt
    python -m pytest steering_envelope/tests -q      # acceptance suite
    python -m steering_envelope.validate.run_all     # fetches+caches, fits, figures

## Pre-registered analysis (frozen before the published run)

Fit windows, event definitions and holdouts:

- **Roads (US)**: panel 1926-2023 (VMT series begins 1921; five years feed
  the growth window). v = trailing 5-year annualized VMT growth (as 1+g).
  s = curated steering-stack index, 5-year phase-in. Primary outcome:
  log(fatalities per 100M VMT), Gaussian ML on levels **and, judged
  stricter, first differences**. Secondary: binary deterioration years
  (rate rises year-over-year). Holdout: leave-one-decade-out.
- **Aviation (world)**: 1976-2019 (departures begin 1970; 2020+ excluded —
  the pandemic collapse breaks the growth proxy). v = 5-year departures
  growth; s = curated oversight index; outcome log(fatal accidents per
  million flights); same level/difference/decade-holdout scheme.
- **Finance (JST, 18 countries)**: 1875-2020 excluding both world wars
  (1914-18, 1939-45), following Schularick-Taylor. v = 5-year real credit
  growth; s = era-coded regulation index (curated/README.md documents the
  coding and its coarseness); event = systemic crisis flag (crisisJST);
  panel logit; leave-one-decade-out.
- **Nuclear**: decade case study ONLY (7 decades, 10 INES>=4-class
  events): rate table with Jeffreys intervals + Spearman rank test. No
  logistic fit — with N this small it would be numerology.
- **AI**: leading indicators only; no outcome fit exists or is claimed.

Disclosure: during development the binary deterioration-year event was
tried first for roads and came out null; the continuous level+difference
framework was then fixed and applied unchanged to aviation and finance.
The null binary result is retained and reported in `results/roads.json`
(`secondary_binary`), not hidden.

## Falsification criteria (no weaseling)

- If v/s adds no predictive power over v alone — LR(full vs v-only)
  p > 0.1 — in 3 or more of the fittable historical domains, the steering
  term is decoration and **s/acc loses its empirical leg**. Report either
  way.
- If s alone dominates everywhere (v adds nothing anywhere), the stopper
  position gains support, not s/acc.
- Nuclear may only be described as "consistent" or "inconsistent", never
  as evidence that discriminates hypotheses.

## Results (from `validate/results/summary.json`)

| domain | test | p(s given v) | p(v given s) | verdict |
|---|---|---|---|---|
| roads (US) | differenced levels | 0.045 | 0.016 | both terms carry signal |
| roads (US) | levels | 3e-52 | 0.052 | s dominates (trend-permissive; upper bound) |
| aviation | differenced levels | 0.59 | 0.12 | null at annual frequency — a point for the stopper reading |
| aviation | levels | 2e-19 | 0.005 | s dominates |
| finance | panel logit | 4e-9 | 0.008 | **both**; ratio model best out-of-sample (LORO AUC 0.688 vs 0.506 v-only) |
| nuclear | case study | — | — | consistent: 13x event rate in high-v/s decades (Spearman rho 0.82, p 0.02) |
| ai | leading indicators | — | — | no outcome data; ratio peaked 2014-16 above every historical corner band, now below its own mean on these proxies |

Scoreboard: the steering term survives in 2/3 fittable domains
(falsification required it to fail in 3/3 or 2/3); speed survives in 2/3.
Where the tests are sharpest (finance, the only true panel), the **ratio
form generalizes best out-of-sample**, which is precisely the s/acc form.
Aviation is logged honestly as favoring the stopper reading. The
Schularick-Taylor credit-boom result reproduces before our addition is
tested. Model-layer acceptance: the e/acc preset lands 61% crash+pileup,
the saxxer preset's plurality outcome is convoy (0.79), the mean-field
theorem (coordination beats private virtue for a diligent ego) passes at
9/9 gridpoints, and the kitchen PROOF table shows s/acc winning only
through the coordination dial — with K forced to 0, every tribe row is a
tie.

## Licenses

Dataset licenses are listed in [`validate/curated/README.md`](validate/curated/README.md).
All raw downloads are cached locally and never committed; fetch scripts are.
