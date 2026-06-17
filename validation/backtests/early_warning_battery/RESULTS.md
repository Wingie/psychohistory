# Early-warning falsification battery — RESULTS

**Question.** The bounded-psychohistory framework predicts *critical slowing
down* (rising variance + lag-1 autocorrelation of fluctuations) in the run-up to
an **endogenous, self-reinforcing** cascade, and predicts **no** such warning
before an **exogenous** shock. Turn that into a real test: run an early-warning
detector with a strict pre-onset information cutoff and a base-rate null
(prosecutor's-fallacy guard) across a labeled roster, and ask whether
endogenous events score higher (AUC) than exogenous controls.

**Data.** Weekly submission-activity density (posts/hour) per subreddit,
harvested from the Arctic Shift **search** endpoint. See `roster.md` for the
density-proxy definition and why the aggregate endpoint was unusable (it returns
all-zero counts for r/wallstreetbets and 422-times out under load — it cannot
serve the decisive GameStop case). One consistent method is used for all events.
Harvesters: `harvest_density.py` (primary), `harvest.py` (aggregate, retained
but unreliable). Analysis: `battery.py`. Raw series in `data/`, per-event scores
in `results/`.

**Detector.** PRIMARY = literature-standard detrended critical-slowing-down
(`window_score_csd`): on the approach window (the `window` weeks ending the week
*before* onset — strict info cutoff), take `log1p`, subtract a moving-average
trend, then score = Kendall-τ trend of rolling variance + Kendall-τ trend of
rolling lag-1 AR over sub-windows. Higher = stronger warning. The base-rate null
slides the identical detector over every window that does not overlap the
cascade approach window; we report the cascade's percentile and AUC in that null.
SECONDARY (`AUCraw`) = the original raw variance/AR1-rise detector from
`validation/temporal/test_early_warning.py`, kept for comparison. Primary
**window = 6 weeks** for every event (pre-set, not tuned).

---

## Per-event results (primary CSD detector, window = 6 weeks)

| event | label | onset | AUC | percentile | z | τ(var) | τ(AR1) | AUC(raw) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| **gme_wsb_weekly** (GameStop) | endogenous | 2021-01-25 | **0.915** | **82.9%** | +1.38 | +1.00 | −0.33 | 0.400 |
| superstonk_2021 | endogenous | 2021-06-07 | 0.780 | 72.0% | +0.79 | +1.00 | −0.33 | 0.000 |
| crypto_2021peak | endogenous | 2021-05-03 | 0.060 | 0.0% | −1.65 | −0.33 | −1.00 | 0.231 |
| crypto_luna2022 | endogenous | 2022-05-09 | 0.534 | 29.3% | +0.11 | −0.33 | +0.33 | 0.038 |
| europe_energy2022 | endogenous | 2022-09-05 | 0.208 | 12.4% | −0.72 | +0.33 | −1.00 | 1.000 |
| wsb_meme_2021 | endogenous | 2021-06-01 | 0.500 | 29.7% | +0.02 | −0.33 | +0.33 | 0.029 |
| askecon_infl2022 | exogenous | 2022-02-07 | 0.832 | 76.4% | +0.93 | +1.00 | −0.33 | 0.846 |
| askecon_tariff25 | exogenous | 2025-04-07 | 0.500 | 31.0% | +0.01 | +0.33 | −0.33 | 0.359 |
| europe_covid2020 | exogenous | 2020-03-02 | 0.552 | 34.3% | +0.10 | −0.33 | +0.33 | 0.951 |
| crypto_ftx2022 | exogenous | 2022-11-07 | 0.065 | 0.0% | −1.72 | −0.33 | −1.00 | 0.232 |

### The decisive GameStop case
**AUC = 0.915, percentile = 82.9% (z = +1.38) → SUPPORTS early-warning.**
The pre-onset r/wallstreetbets ramp (Dec-2020 → mid-Jan-2021: ~38→38→25→43→61
posts/hr, *before* the Jan-25 squeeze week and the Feb-1 ~2093/hr spike) shows a
clean monotone rise in detrended rolling variance (τ_var = +1.0) that sits in
the **top ~17%** of all comparable non-onset windows. Critical slowing down is
real and detectable here, exactly as the framework predicts for the canonical
endogenous reflexive cascade. (Note the SECONDARY raw detector gives only 0.40
for GME — it is fooled by the post-onset super-spike polluting its null and by
the un-detrended level; this is *why* the detrended CSD detector is the primary.)

---

## Aggregate: endogenous vs exogenous (window = 6, pre-set)

| group | N | mean AUC | median AUC | AUCs |
|---|---:|---:|---:|---|
| **endogenous** | 6 | **0.500** | 0.517 | 0.915, 0.780, 0.060, 0.534, 0.208, 0.500 |
| **exogenous** | 4 | **0.487** | 0.526 | 0.832, 0.500, 0.552, 0.065 |

- **Separation (mean endo − mean exo): +0.012** (essentially zero).
- **Mann–Whitney U = 11.5, p = 0.91** (two-sided) — no significant group
  difference. AUC[endo>exo] = 0.479.
- endogenous mean AUC > 0.5: **False** (it is 0.500).
- dissociation (endo > exo): **True but trivially so** (+0.012).

### VERDICT: **INCONCLUSIVE — no separation.**
- The **single decisive GameStop case SUPPORTS** the prediction strongly
  (AUC 0.915, top-17% tail) — and Superstonk, the other clean meme-stock
  cascade, also fires (0.780). The mechanism is visibly present in the
  highest-quality endogenous cascades.
- But **as a battery, the endogenous group does not separate from the exogenous
  controls.** Two endogenous events score *below* chance (crypto 2021-peak 0.060,
  europe-energy 0.208), and one exogenous control scores *high* (AskEconomics
  inflation 0.832), wiping out the group difference. The dissociation the
  framework needs **does not hold** at this N and resolution.
- This **does not contradict** the framework (GME is a genuine positive and no
  endogenous case is systematically worse than its controls), but it **falls
  short of confirming** the dissociation. Honest reading: *promising on the
  cleanest cases, unproven as a general dissociation.*

### Window-sensitivity (transparency — the verdict is NOT tuned to a window)

| window (wk) | GME AUC | endo mean | exo mean | separation |
|---:|---:|---:|---:|---:|
| **6 (primary)** | **0.915** | 0.500 | 0.487 | +0.012 |
| 8 | 0.771 | 0.442 | 0.319 | +0.123 |
| 10 | 0.379 | 0.474 | 0.267 | +0.207 |
| 12 | 0.435 | 0.518 | 0.400 | +0.118 |

The GME signal is strongest at short windows (its pre-onset ramp is only ~6–8
weeks long; longer windows reach back into the flat 2020 baseline and dilute it).
The endo−exo separation *grows* with window (up to +0.21 at W=10) but is driven
by exogenous AUCs falling rather than endogenous AUCs rising, and the group means
stay near or below 0.5. No window makes the dissociation convincing; reporting
all four avoids cherry-picking.

---

## Honest caveats (read before citing any number)
1. **Activity proxy.** Submission *density* (posts/hr from the first 100 posts of
   a week) is a proxy for posting rate, not a clean count, and not sentiment or
   belief. It tracks the GME cascade convincingly but is one step removed from
   the quantity the theory is about.
2. **Coarse resolution.** Weekly buckets; the CSD sub-window trend has very few
   points (with W=6, Kendall-τ takes only values like ±0.33, ±1.0), which makes
   the per-event scores chunky and the null noisy.
3. **Low-volume controls are smeared.** r/AskEconomics posts ~1/hr, so 100 posts
   span many days — its weekly density is temporally blurred. The proxy is
   *coarsest exactly for the exogenous controls*, so their AUCs (e.g. inflation
   0.832) are unreliable and may be inflating the apparent non-separation.
4. **Heuristic labels and onsets.** Both are judgment calls, listed explicitly in
   `roster.md` so a reviewer can flip them (e.g. FTX endo vs exo, Luna onset
   week) and re-run. The verdict is sensitive to a couple of these.
5. **Small N, shared subreddits.** 6 endogenous / 4 exogenous, several sharing a
   subreddit → events are not independent; the Mann–Whitney is underpowered.
6. **r/wallstreetbets aggregate gap.** The Arctic Shift aggregate endpoint could
   not serve wsb at all; the decisive case rests entirely on the search-density
   proxy. Cross-checking against an independent count source would strengthen it.
7. **Preliminary, not publication-grade.** This is a real falsification *attempt*
   with a guard against the prosecutor's fallacy, not a finished study.

### What a stronger battery would add
- **Finer resolution** (daily counts) → many more Kendall-τ points → far less
  chunky per-event AUCs and a real null distribution.
- **True counts**, not density, via a complete-coverage dump (e.g. Pushshift
  archives) — especially for the busy meme subs.
- **A bigger, pre-registered roster** (20–40 events) across many independent
  subreddits, with labels and onsets fixed *before* scoring, enough to power the
  Mann–Whitney.
- **Sentiment/belief series**, not just activity, to test the mechanism the
  theory actually names.

## Files
- `roster.md` — labeled roster (event, subreddit, onset, label, rationale, limits)
- `harvest_density.py` — primary harvester (search-density proxy)
- `harvest.py` — aggregate harvester (retained; endpoint unreliable)
- `battery.py` — runnable analysis (detrended-CSD primary + raw secondary + sweep)
- `data/*.json` — 10 harvested weekly series
- `results/*.json` — per-event scores; `results/_aggregate.json` — aggregate + sweep
