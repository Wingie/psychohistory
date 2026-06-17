# EnKF one-block forward forecast test — RESULTS

**Date:** 2026-06-15
**Script:** `enkf_oneblock.py` (CPU, `py -3.12`, numpy + matplotlib-Agg, no GPU)
**Block:** `r/AskEconomics`, monthly submission counts, 2020-12 → 2025-04 (53 contiguous monthly points), from `../temporal/data/monthly_submissions.json` (Arctic Shift harvest).
**Observable:** natural log of monthly submission count (log-activity).

This is the first test in the suite that touches the paper's **smooth-regime forward-skill claim** rather than a backtest. It runs the assimilating engine (an Ensemble Kalman Filter) as a genuine **pseudo-out-of-sample, strictly causal walk-forward** and scores the 1-step forecasts against naive baselines with a proper score, then runs the misspecification monitor.

---

## Method

### Forward model (one block)
A small linear **local-linear-trend** model in log-activity. State `x = [level a, trend b]`:

```
a_{t+1} = a_t + b_t        + w_a
b_{t+1} = phi * b_t        + w_b        phi = 0.7  (trend reverts toward 0)
```

Matrix form `x_{t+1} = F x_t + w`, `F = [[1, 1], [0, phi]]`. This is a log random walk with a damped drift term — the standard "smooth regime" workhorse: mean-reverting in differences, no exotic structure.

**Observation operator** `H = [1, 0]`: we observe the level (= log-activity) plus measurement/sampling noise `v ~ N(0, R)`. So `y_t = a_t + v`.

Noise levels are estimated from the data scale (variance of 1-step log changes, `step_var = 0.0289`): `Q = diag(0.5·step_var, 0.25·step_var)`, `R = 0.3·step_var`. One block, honest and simple — no per-step tuning, no peeking at future data.

### EnKF loop + forward test (the point)
Standard **stochastic (perturbed-observation) EnKF**, `N = 80` members:

- **Forecast step:** each member propagated through `F` + sampled process noise → forecast ensemble for `t+1`; `P_f` from ensemble covariance.
- **Forecast distribution for the observable:** predicted `y_{t+1}` ensemble, innovation variance `S = H P_f Hᵀ + R`.
- **Reveal `y_{t+1}`, then analysis step:** perturbed-observation Kalman gain `K = P_f Hᵀ / S`, each member updated with its own perturbed observation.

The loop is **strictly causal**: at step `t` the filter has seen only `y_0..y_t` when it emits the forecast for `t+1`. The first 8 steps are spin-up (filter warming) and are **excluded from scoring**; we score the 45 out-of-sample 1-step forecasts from 2021-08 → 2025-04.

### Baselines (same out-of-sample steps, also given predictive distributions)
- **Persistence:** `ŷ_{t+1} = y_t`; predictive sd = sd of past 1-step changes.
- **Climatology:** `ŷ_{t+1} = running mean of y_0..y_t`; predictive sd = running sd.

### Scores
- **RMSE / MAE** on the forecast mean.
- **CRPS** (proper score): exact empirical-ensemble CRPS for the EnKF; closed-form Gaussian CRPS for the baselines (they get a fair predictive distribution).
- **Coverage** of the nominal 95% forecast interval (calibration).

All metrics are in **log-activity units** (dimensionless log-counts).

---

## Forward-skill numbers (45 out-of-sample steps, log units)

| Forecaster   | RMSE   | MAE    | CRPS   | 95% coverage |
|--------------|--------|--------|--------|--------------|
| **EnKF**     | 0.1806 | 0.1267 | 0.1005 | 0.98         |
| Persistence  | 0.1786 | 0.1247 | 0.0937 | 0.87         |
| Climatology  | 0.2245 | 0.1606 | 0.1183 | 0.80         |

### Verdict — does assimilation beat the baselines?

- **vs Climatology: YES.** The EnKF beats climatology on every metric (RMSE 0.181 vs 0.224, CRPS 0.101 vs 0.118). Assimilation clearly extracts more than the unconditional running mean — it tracks the level.
- **vs Persistence: NO (essentially tied, marginally worse).** EnKF RMSE 0.1806 vs persistence 0.1786 (+1.1%); CRPS 0.1005 vs 0.0937 (+7%). On a monthly log random walk, **last value is a hard baseline to beat**, and the EnKF does not beat it here. This is an **honest negative** for the strong form of the smooth-regime skill claim at monthly resolution on this single block.

So `enkf_beats_all_baselines = false`. The assimilation loop runs, is well-calibrated, and dominates climatology, but it does **not** demonstrate skill over persistence on this series.

**Calibration:** EnKF coverage 0.98 vs nominal 0.95 — slightly over-dispersed (forecast intervals a touch wide; the `S` includes both ensemble spread and obs noise). Persistence/climatology under-cover (0.87 / 0.80), so the EnKF's predictive distribution is the best-calibrated of the three even though its point/CRPS edge over persistence is absent.

---

## Misspecification monitor (Second-Foundation argument)

Normalized innovation `z_t = (y_t − H x_f) / sqrt(H P_f Hᵀ + R)`. Under a correct model `z ~ N(0,1)`. Threshold `|z| > 3σ`.

- **mean|z| = 0.61, std(z) = 0.87** — innovations are, on the whole, *smaller* than the model's own predicted uncertainty (consistent with the slight over-dispersion above). The model is not systematically surprised in the smooth regime.
- **1 flagged out-of-model event: 2025-04-30, z = −3.33.** After tracking the sharp ramp 1238 → 1332 → 1872 (Jan–Mar 2025), the filter's drift carried the forecast upward and it was blindsided by the collapse to **946** submissions in April — a genuine, large, negative surprise outside the model's distribution. This is exactly the "Mule" / out-of-model signature the paper's monitor is designed to raise: the smooth-regime model is invalid precisely at the regime break, and the normalized innovation flags it in real time without any future information.

This is the constructive half of the result: even where the EnKF does not beat persistence on average skill, the assimilation framework delivers something persistence cannot — a **calibrated, self-diagnosing forecast** that announces when it has left its own model.

---

## Honest caveats

- **One block, one series.** AskEconomics only. Nothing here generalizes; it is a single demonstration.
- **Simple forward model.** Local-linear-trend in log-activity. No seasonality, no exogenous drivers, no coupling to other blocks. A richer model might (or might not) beat persistence.
- **Monthly resolution, ~45 scored steps.** Small sample; the EnKF–persistence gap (1% RMSE) is well within sampling noise — read it as "tied", not "beaten". No formal significance test is claimed.
- **Proxy activity.** Submission counts are a proxy for community attention/activity, with platform-, harvest-, and moderation-driven artifacts.
- **Noise levels are heuristic** (fractions of the empirical 1-step variance), not fitted by MLE. Different `Q/R/phi` would shift the numbers; they were fixed *a priori* from the data scale to avoid in-sample tuning, but they are not optimal.
- **What this is:** a demonstration that the assimilation loop **runs end-to-end, is strictly causal, yields a SCORED forward forecast distribution, is well-calibrated, and that its misspecification monitor fires on a real regime break.** It is **not** a validated forecaster, and on this block it does **not** establish skill over persistence.

### Tie to the falsification program
The smooth-regime skill claim is **falsifiable** and was put at risk here: a forward test that fails to beat persistence is a real, reportable negative, and we report it as one. The claim survives only in the weaker, defensible form — *better than climatology, well-calibrated, and equipped with a working out-of-model detector* — pending richer models, more blocks, and finer resolution.

---

## Files

- `enkf_oneblock.py` — runnable EnKF forward test (CPU).
- `enkf_forward.png` — top: walk-forward 1-step forecast vs actual with 95% ensemble band; bottom: normalized-innovation monitor with the 2025-04 out-of-model event flagged.
- `enkf_results.json` — all numbers above, machine-readable.
- `RESULTS.md` — this file.
