# Major-player-signal early-warning detector

**Question.** Can a detector tell apart the two cascade mechanisms the framework
posits?

- **Endogenous / operator-skill cascade** — a single identifiable operator
  (major player) primes the system: their signal RISES and LEADS the aggregate
  activity for a sustained run-up before the cascade. *Expectation: the operator
  signal leads, with a long gradual buildup.*
- **Exogenous shock** — an OUTSIDE major player (a head of state, a data release)
  drives a sudden spike with NO internal-operator priming: the relevant entity
  mention SPIKES *at* the event, it does not LEAD it. *Expectation: no internal
  operator lead; a sudden spike, at most short news-anticipation.*

If a detector scores GameStop as internal-operator-led while the AskEconomics
shock scores as exogenous, the operator-signal-as-early-warning method is
supported as a **mechanism classifier** — which is the right test (vs the
impersonal "tremor" / variance-based early-warning test that washed out earlier
in this project).

---

## The detector

For an event with onset week `t0`, on the strictly-pre-onset window we ask whether
a single identifiable DRIVER signal LEADS the aggregate activity. Two measures,
both reported; the second is the primary discriminator at this resolution.

**(a) LEAD-LAG (cross-correlation), guarded.** We correlate the *week-over-week
change* (first difference) of the driver with the change of the aggregate as a
function of integer lag `k` weeks, over a window covering the pre-onset run-up
plus onset. `peak_lag > 0` ⇒ the driver's change leads the aggregate's change.

*Why first differences:* on raw levels, GameStop's single co-located terminal
mega-spike (operator and aggregate both peak in the SAME week, 2021-01-31) pins
the peak correlation to lag 0 (xcorr 0.97) and hides the run-up lead entirely.
Differencing isolates run-up dynamics from the terminal spike.

A `guarded_lead` only credits a lead when the peak is at `k>0`, exceeds the lag-0
value by ≥ 0.08, and clears a noise floor of 0.20 — because argmax-over-lags on a
flat/noisy entity series otherwise returns a spurious large lead (it does, for
the 2022 inflation case: raw peak at +5 weeks is argmax-on-noise).

**(b) BUILDUP SHAPE / DURATION — the primary discriminator.** Over a long
(14-week) pre-onset window we measure the driver's log-linear ramp
(`slope`, `level_vs_time_r`) and, crucially, **`ramp_run`** = the number of
consecutive non-decreasing weeks rising *into* the onset. An internal operator
priming a position grows steadily for **months** (long run); a pre-announced or
sudden external shock produces at most a **short (1–3 wk) news-anticipation bump**
or no ramp. We also report `early_half_slope_ratio` (is the ramp already underway
in the first half of the window, vs all in the final weeks). `buildup_factor = +1`
(sustained internal priming) requires `slope>0 AND level_r>0.3 AND ramp_run ≥ 6 AND
early_half_ratio ≥ 0.30`; else `-1`.

**(c) CONCENTRATION (reported, NOT used in the scalar).** Driver share
(driver/aggregate) trend over the pre-onset window. This did **not** discriminate
(positive for all three events) — see caveats — so it is reported but excluded
from the classifier.

**Operator-led score (scalar).**
```
ramp_strength      = sign(slope) * max(level_r,0) * sqrt(ramp_run)
lead_bonus         = 0.5 * guarded_lead   (credited only if buildup_factor > 0)
operator_led_score = buildup_factor * (1 + ramp_strength) + lead_bonus
```
**Classifier.** `INTERNAL-OPERATOR-LED` iff `buildup_factor > 0` (i.e. a sustained
≥6-week operator ramp). `EXOGENOUS-SPIKE (mild anticipation)` if there is a short
ramp (≥3 wk) or a guarded growth-lead but no sustained ramp. `EXOGENOUS-SPIKE`
otherwise. Sign of the scalar: **positive ⇒ internal-operator-led; negative ⇒
exogenous.**

## Data

Arctic Shift search endpoint (`arctic-shift.photon-reddit.com`), inverse-inter-
arrival **density proxy** (posts/hour) at weekly resolution — the proxy validated
across this codebase. A monotone proxy for posting/mention RATE, not an absolute
count, not price.

- **GameStop** reuses the already-harvested series in
  `../gamestop_counterfactual/data/`: operator signal = sum of
  `dfv_{DFV,DeepFuckingValue,RoaringKitty,GMEYOLO}`; aggregate =
  `wsb_overall_activity`.
- **AskEconomics** series harvested here into `./data/`: aggregate activity, plus
  entity-mention densities for `tariff`+`Trump` (2025) and `inflation`+`Fed`
  (2022). These are the would-be "operator/major-player" proxies for an event
  whose real driver is EXTERNAL (the policy/data release).

---

## Per-event results

### 1. GameStop — DFV / Roaring Kitty vs r/wallstreetbets  (endogenous / positive)

Onset 2021-01-25. Lead-lag window 2020-10-04 .. 2021-02-14.

| measure | value |
|---|---|
| guarded growth-lead | **+0 wk** (raw peak +0; level-xcorr pinned to lag 0 at 0.975) |
| **ramp_run into onset** | **13 weeks** |
| log-linear weekly growth | **+18.2 %/wk** (level-vs-time r = 0.703) |
| early-half slope ratio | 0.30 (ramp already underway in the first half) |
| onset / pre-max ratio | 3.46 |
| buildup_factor | **+1 (sustained internal priming)** |
| **operator-led score** | **+3.54** |
| **classification** | **INTERNAL-OPERATOR-LED** |

The DFV / Roaring Kitty signal rises **monotonically for 13 consecutive weeks**
(0.33 → 2.1 /hr over Oct→Jan, +18 %/wk) before both it and the crowd spike
together at the squeeze. The operator was a sustained, self-amplifying internal
voice for a full quarter — exactly the operator-priming signature.

**Honest nuance:** the *peak-to-peak* lead-lag is **0 weeks** — operator and crowd
peak in the same week. The operator lead lives in the **shape and duration of the
run-up**, not in a clean weekly peak offset. At weekly resolution the true DFV→crowd
lead (days) is below the resolution floor. So GameStop is operator-LED by *buildup*,
**coincident by peak-timing**. We report both and do not overclaim a peak lead.

### 2. AskEconomics 2025 tariff shock — tariff/Trump vs aggregate  (exogenous / contrast)

Onset 2025-03-31 ("Liberation Day" reciprocal tariffs announced 2025-04-02).
Window 2025-01-12 .. 2025-05-04.

| measure | value |
|---|---|
| guarded growth-lead | +1 wk (peak growth-xcorr 0.357) |
| **ramp_run into onset** | **3 weeks** |
| log-linear weekly growth | +10.7 %/wk |
| onset / pre-max ratio | 0.98 |
| buildup_factor | **−1 (no sustained priming)** |
| **operator-led score** | **−2.25** |
| **classification** | **EXOGENOUS-SPIKE (mild anticipation)** |

The aggregate is flat ~1.5/hr for months then spikes to 3.4/hr at 2025-04-06,
right after the announcement. The "tariff" entity term ramps only in the **final
~3 weeks** (0.13 → 0.21 → 0.30 → 0.53 /hr, mid-to-late March) as the pre-announced
policy date approached, then **collapses**. This is genuine but short
**news-anticipation of a telegraphed external event**, not a sustained internal
operator buildup — there is no major player inside r/AskEconomics priming the
surge. Correctly exogenous.

### 3. AskEconomics 2022 inflation surge — inflation/Fed vs aggregate  (exogenous / contrast)

Onset 2022-02-07 (Jan-2022 CPI print 7.5 %, a 40-year high, released 2022-02-10).
Window 2021-11-02 .. 2022-03-08.

| measure | value |
|---|---|
| raw growth-lead peak | +5 wk — **argmax-on-noise** (flat entity series; not a real lead) |
| **ramp_run into onset** | **2 weeks** |
| log-linear weekly growth | +2.7 %/wk |
| onset / pre-max ratio | 0.99 |
| buildup_factor | **−1 (no sustained priming)** |
| **operator-led score** | **−2.19** |
| **classification** | **EXOGENOUS-SPIKE (mild anticipation)** |

The aggregate spikes once, sharply, at the CPI release (2.67/hr vs ~1.2 baseline);
the "inflation"/"Fed" entity mention is essentially **flat the entire window**
(~0.13–0.18 /hr, no spike, no ramp). The raw cross-correlation argmax returns a
spurious +5-week "lead" — this is the failure mode the guard is designed to catch,
and it is exactly why the score formula credits the growth-lead bonus only when a
sustained ramp is present (otherwise this flat series would score positive).
Correctly exogenous; the +5 is a documented false-positive of the unguarded lead.

---

## Discrimination verdict

| event | score | ramp_run | classification |
|---|---|---|---|
| GameStop (endogenous) | **+3.54** | 13 wk | **INTERNAL-OPERATOR-LED** |
| AskEcon tariff 2025 (exogenous) | −2.25 | 3 wk | EXOGENOUS-SPIKE (mild anticipation) |
| AskEcon inflation 2022 (exogenous) | −2.19 | 2 wk | EXOGENOUS-SPIKE |

**YES — the detector discriminates.** GameStop scores positive and is classified
internal-operator-led; both AskEconomics shocks score negative and are classified
exogenous. The single number that cleanly separates the mechanisms is the
**duration of the operator's pre-onset ramp** (`ramp_run`): **13 weeks** of
sustained operator buildup for GameStop vs **3 and 2 weeks** for the external
shocks. The buildup-SHAPE measure is the discriminator; the weekly lead-lag is at
the resolution floor and (for GameStop) actually reads coincident — so the
operator-early-warning claim is supported in its **gradual-buildup** form, not in a
naive "operator peaks N weeks before the crowd" form.

This is the right test, and it does *not* wash out the way an impersonal
variance/critical-slowing-down ("tremor") early-warning test did: a single
identified major-player signal carries mechanism information that aggregate
fluctuation statistics do not.

---

## Honest caveats

- **n = 2 events (3 series). Illustrative, not conclusive.** One endogenous case
  and two exogenous contrasts. This demonstrates the detector *can* separate the
  mechanisms on real data; it is not a calibrated, out-of-sample-validated
  classifier. Thresholds (`ramp_run ≥ 6`, margins, noise floor) were set with the
  data in view and would need a held-out test set to claim generalization.
- **GameStop's operator lead is by BUILDUP, not by peak-timing.** Peak-to-peak
  lead-lag is 0 weeks; the operator and crowd spike the same week. We do not claim
  the operator signal peaks before the crowd — only that it *ramps* over a long
  sustained run-up. Weekly resolution makes any 1–2-week peak lead near or below
  the resolution floor; the true DFV→crowd lead was days.
- **Mention-density is a proxy.** Inverse-inter-arrival posts/hour, capped at 100
  records, is a monotone proxy for RATE — not absolute counts, not price, not
  short interest. It saturates information about magnitude.
- **The external-entity-mention proxy for AskEconomics is imperfect.** "tariff",
  "Trump", "inflation", "Fed" are crude stand-ins for the would-be operator. The
  2025 tariff DID have a genuine ~3-week anticipatory ramp because the policy was
  pre-announced — so "no internal lead at all" is too strong; the honest statement
  is "a *short* news-anticipation ramp, not a *sustained* internal-operator
  buildup." "inflation"/"Fed" are perennial background topics, so their flatness is
  partly a base-rate artifact.
- **Concentration did NOT discriminate** and is excluded from the scalar: the
  driver's share of conversation trends positive in all three events
  (r = 0.53 / 0.60 / 0.75), so share-rising alone does not separate the mechanisms.
- **The +5-week "lead" for inflation 2022 is a known false positive** of the
  unguarded cross-correlation argmax on a flat series; it motivates the guard and
  the buildup-gated lead bonus, and is reported transparently rather than hidden.
- **Onset dates are analyst-chosen** from the documented event calendar (GME
  squeeze 2021-01-25; Liberation Day 2025-04-02; Jan-2022 CPI 2022-02-10). The
  classification is not very sensitive to ±1 week, but it is a researcher degree of
  freedom.

## Files

- `detector.py` — runnable: `py -3.12 detector.py` (harvest + analyze) or
  `py -3.12 detector.py analyze` (reuse `./data/`).
- `results.json` — per-event detector output (all measures).
- `figure_major_player.png` — operator signal vs aggregate timeline per event,
  with onset marked and the operator pre-onset ramp shaded.
- `data/askecon_*.json` — harvested weekly density series.
