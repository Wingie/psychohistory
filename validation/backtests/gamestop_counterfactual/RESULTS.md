# GameStop counterfactual: Seldon Crisis vs the Mule

**Question.** Was the January-2021 GameStop squeeze structurally *overdetermined*
(a Seldon Crisis — the system was critically primed, the trigger interchangeable,
Roaring Kitty selecting the branch but not *whether* a cascade happened), or was
Roaring Kitty *necessary* (a Mule — one individual without whom no cascade)?

**This is not a true counterfactual.** We have no no-Roaring-Kitty world. The test
is therefore about two *observable structural signatures*: (a) whether the
susceptibility (retail attention) was rising on its own *before* GME, and (b)
whether the squeeze was *overdetermined* across many tickers (many simultaneous
or rapidly-contagious squeezes ⇒ systemic conditions, not a GME-specific freak).

**Data.** Arctic Shift search endpoint, r/wallstreetbets. The aggregate endpoint
422s for this subreddit and search caps at 100 records, so we use the
codebase-validated inverse-inter-arrival **density proxy** (posts/hour), a
monotone proxy for posting/mention *rate* — not an absolute count, and not price
or short-interest.

---

## Check 1 — Was the powder keg building independent of GME / Roaring Kitty?

Overall r/wallstreetbets submission activity, 2019-01 to 2021-03, judged on the
window **strictly before the GME spike (2021-01-18)**.

```
{
  "window": "2019-01-06..2021-01-17 (strictly pre GME spike 2021-01-18)",
  "log_linear_weekly_growth_pct": 2.19,
  "level_vs_time_pearson_r": 0.602,
  "mean_perhr_2019": 4.31,
  "mean_perhr_2020H1": 23.82,
  "mean_perhr_2020H2": 18.5,
  "mean_perhr_dec2020": 25.85,
  "growth_factor_2019_to_dec2020": 5.99,
  "verdict": "attention rising structurally BEFORE GME spike"
}
```

**Read.** attention rising structurally BEFORE GME spike. Mean activity rose from
~4.31/hr (2019) → ~18.5/hr (H2 2020)
→ ~25.85/hr (Dec 2020), a
**x5.99 growth before GME ever spiked**
(log-linear pre-spike weekly growth 2.19%,
level-vs-time r=0.602). The susceptibility was
rising structurally — 2020 (COVID lockdown, stimulus checks, zero-commission
retail brokerages, options gamma) primed the keg independent of any operator.

## Check 2 — Was the squeeze overdetermined across many stocks?

Per-ticker mention density, 2020-09 to 2021-02, for GME/AMC/BB/NOK/BBBY/KOSS.

```
{
  "tickers": {
    "GME": {
      "spike_week": "2021-01-31",
      "peak_perhr": 430.62,
      "baseline_perhr": 0.444,
      "amplification": 970.0
    },
    "AMC": {
      "spike_week": "2021-01-31",
      "peak_perhr": 244.4,
      "baseline_perhr": 0.07,
      "amplification": 3501.4
    },
    "BB": {
      "spike_week": "2021-01-31",
      "peak_perhr": 33.07,
      "baseline_perhr": 0.078,
      "amplification": 423.4
    },
    "NOK": {
      "spike_week": "2021-01-31",
      "peak_perhr": 33.68,
      "baseline_perhr": 0.038,
      "amplification": 874.7
    },
    "BBBY": {
      "spike_week": "2021-01-31",
      "peak_perhr": 2.39,
      "baseline_perhr": 0.04,
      "amplification": 60.3
    },
    "KOSS": {
      "spike_week": "2021-01-24",
      "peak_perhr": 2.18,
      "baseline_perhr": 0.882,
      "amplification": 2.5
    }
  },
  "gme_spike_week": "2021-01-31",
  "n_tickers_spiking_in_gme_window_pm7d": 6,
  "tickers_clustered_with_gme": [
    "GME",
    "AMC",
    "BB",
    "NOK",
    "BBBY",
    "KOSS"
  ],
  "onset_week_3x_baseline": {
    "GME": "2020-11-29",
    "AMC": "2021-01-10",
    "BB": "2020-11-29",
    "NOK": "2021-01-17",
    "BBBY": "2021-01-17",
    "KOSS": null
  },
  "onset_lag_days_vs_gme": {
    "GME": 0,
    "AMC": 42,
    "BB": 0,
    "NOK": 49,
    "BBBY": 49
  },
  "n_others_same_window_or_before": 1,
  "n_others_within_1wk_after": 0,
  "timing_verdict": "contagion-from-GME (others onset shortly after GME)",
  "verdict": "6/6 tickers spike in same week as GME; contagion-from-GME (others onset shortly after GME)"
}
```

**Read — two metrics, one honest answer.** The data give a *split* signal that is
itself the interesting result:

- **Peak clustering (the overdetermination signature): SYSTEMIC.** All **6 of 6**
  meme tickers reach their mention-density PEAK in the **same week**
  (2021-01-31; KOSS one week earlier, 2021-01-24) — every ticker within +/-7d of
  GME. The amplifications are enormous and simultaneous: GME x970, AMC x3501,
  NOK x875, BB x423, BBBY x60, all peaking together. Six independent tickers do
  not peak in the same 7-day window by chance — the squeeze fired *across the
  whole meme basket at once*. This is the structural-overdetermination signature.

- **Onset of the ramp (the contagion signature): GME-LED.** But the *first* week
  each ticker's mention-rate crosses 3x its own baseline tells a different story:
  GME and BB begin ramping back in **late Nov 2020** (GME onset 2020-11-29),
  whereas AMC/NOK/BBBY do not lift until **mid-Jan 2021** (lags of **42-49 days**
  after GME). So GME's attention started building well before the others, and the
  rest only ignited in the final two weeks.

**Reconciliation.** The two metrics are not contradictory — together they say:
**GME led, then the basket squeezed *together* within days.** The late-January
*event* was systemic (6/6 simultaneous peaks); the *months-long preheating* of the
specific GME thesis was GME/RK-led (early onset). That is exactly the
"operator selects the flagship and lights it early, but the primed system then
carries the cascade across many tickers at once" picture. The same-week clustering
of multiple tickers is the overdetermination evidence; the early GME onset is the
operator-selection evidence. The documented *market* record (GME short interest
>100% of float, and the simultaneous late-Jan-2021 price squeezes of
AMC/BBBY/NOK/BB/KOSS) corroborates the systemic reading independently of the
Reddit footprint.

## Check 3 — The Roaring Kitty / DFV signal vs the susceptibility

Weekly density of DFV / DeepFuckingValue / Roaring Kitty / GME-YOLO mentions,
2020-06 to 2021-02.

```
{
  "weeks": [
    "2020-06-07",
    "2020-06-14",
    "2020-06-21",
    "2020-06-28",
    "2020-07-05",
    "2020-07-12",
    "2020-07-19",
    "2020-07-26",
    "2020-08-02",
    "2020-08-09",
    "2020-08-16",
    "2020-08-23",
    "2020-08-30",
    "2020-09-06",
    "2020-09-13",
    "2020-09-20",
    "2020-09-27",
    "2020-10-04",
    "2020-10-11",
    "2020-10-18",
    "2020-10-25",
    "2020-11-01",
    "2020-11-08",
    "2020-11-15",
    "2020-11-22",
    "2020-11-29",
    "2020-12-06",
    "2020-12-13",
    "2020-12-20",
    "2020-12-27",
    "2021-01-03",
    "2021-01-10",
    "2021-01-17",
    "2021-01-24",
    "2021-01-31",
    "2021-02-07",
    "2021-02-14"
  ],
  "dfv_total_density": [
    0.224,
    0.224,
    0.224,
    0.224,
    0.229,
    0.229,
    0.229,
    0.311,
    0.318,
    0.318,
    0.318,
    0.318,
    0.319,
    0.321,
    0.324,
    0.326,
    0.329,
    0.334,
    0.337,
    0.343,
    0.351,
    0.365,
    0.371,
    0.384,
    0.401,
    0.415,
    0.498,
    0.52,
    0.551,
    0.74,
    0.959,
    1.428,
    2.119,
    4.893,
    16.926,
    2.14,
    3.153
  ],
  "peak_week": "2021-01-31",
  "peak_value_perhr": 16.93,
  "priming_window_pearson_r_jun_dec_2020": 0.862,
  "nonzero_weeks_before_jan2021": 30,
  "n_weeks_before_jan2021": 30,
  "first_nonzero_week": "2020-06-07",
  "verdict": "RK/DFV signal present and building for months before Jan-2021, peaks in the squeeze window"
}
```

**Read.** RK/DFV signal present and building for months before Jan-2021, peaks in the squeeze window. The signal is first detectable
2020-06-07, present in
30/30 weeks
before Jan-2021 (priming-window trend r=0.862),
and peaks 2021-01-31 — i.e. it builds gradually for *months* (consistent
with an operator slowly priming a position) but its peak coincides with, rather
than precedes by a long lead, the squeeze and the multi-ticker spike. RK is a
**real, sustained operator signal riding a rising structural tide**, not a bolt
from nowhere.

---

## Verdict at three resolutions

The framework distinguishes the resolution at which a forecast is being made.

- **COARSE — would a squeeze happen at all?** → **OVERDETERMINED (Seldon Crisis).**
  Attention was rising structurally through 2020 before GME (check 1), and the
  squeeze fired across 6/6 tickers
  in the same window (check 2). A retail short-squeeze cascade in the late-2020 /
  early-2021 window was structurally likely with or without any single operator.
  Psychohistory **holds** at the aggregate level.

- **MEDIUM — magnitude / which flagship / exact timing?** → **operator-shaped.**
  That GME (not AMC, not BB) was the *flagship*, that it ran to the historic
  magnitude it did, and that the trigger fired in the *specific* week of
  2021-01-25 rather than weeks earlier or later, reflect Roaring Kitty's specific
  deep-value GME thesis, his sustained year-long DFV signal (check 3), and the
  reflexive focal-point coordination he provided. The check-2 onset metric makes
  this concrete: GME's mention-rate began lifting ~6-7 weeks *before* AMC/NOK/BBBY
  (onset 2020-11-29 vs mid-Jan 2021) — the operator preheated GME specifically,
  then the primed basket squeezed together. The susceptibility chose *a* squeeze;
  the operator chose *which* and *how big*.

- **FINE — this exact path?** → **not forecastable; RK-contingent.** The precise
  trajectory — DFV's exact YOLO updates, the gamma-squeeze mechanics on GME's
  specific option chain, the Robinhood buy-button halt, the exact peak price —
  is a single realized path that psychohistory **cannot** predict and that is
  genuinely contingent on individuals and one-off institutional acts.

**Bottom line.** Closer to **Seldon Crisis than to the Mule.** Roaring Kitty was
*causally important* but **not structurally necessary** for *a* cascade: he
selected the branch (flagship, magnitude, timing), not whether a cascade happened.
The "Mule" reading would require check 1 to show no structural build and check 2
to show GME spiking alone — the data show the opposite.

---

## Honest caveats

- **Proxy, not price.** Reddit mention-density measures *attention*, not market
  short-interest or price. The independently-documented market facts (GME SI
  >100% of float; simultaneous AMC/BBBY/NOK/BB/KOSS price squeezes) *strengthen*
  check 2 but are not what we measured here.
- **No true counterfactual.** There is no no-RK world to observe. We assess
  structural *priming* and *overdetermination*, which is suggestive, not a proof
  of dispensability. A strong-Mule advocate can still argue RK was the unique
  spark that lit a keg that would otherwise have sat unlit — we can only say the
  keg was full and that *multiple* sparks landed in the same window.
- **Density proxy is capped/monotone.** The 100-record search cap means the proxy
  saturates information about absolute counts; it is a reliable *rate ordering*,
  not a calibrated magnitude. The systemic-vs-contagion call from weekly data is
  coarse — one-week resolution cannot cleanly separate "simultaneous" from
  "contagion within days."
- **Survivorship / selection.** The six tickers were chosen *because* they are the
  known meme basket; this is hypothesis-confirming by construction for "did the
  known basket spike together," though check 1 (overall activity) is not subject
  to that selection.
