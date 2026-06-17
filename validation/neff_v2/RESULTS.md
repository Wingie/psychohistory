# SEALED dynamic-N_eff-collapse test on a fresh roster (test ii', v2)

**Verdict: NOT A PASS.** On a fresh, disjoint roster of Wikipedia articles, with the
threshold f derived from existing data and frozen in advance and the calm null built from
genuinely-quiet windows, the dynamic N_eff collapse does NOT clear the sealed rule. The
prior "directional support" does not convert to a sealed result here. This is reported
straight; the threshold and rule were not moved after the numbers were seen.

## What was sealed before harvest

The two honest fixes were pre-registered in `PRE_REGISTRATION_neff_v2.md` and the threshold
was derived by `derive_f.py` using ONLY the existing 20-article tuning data and the verified
engine, BEFORE the fresh roster was selected:

- **f re-derived principledly.** Route (i): the clean-null distribution (the V2
  genuinely-quiet window method applied to the existing data) gives, over n = 10 clean
  windows, percentiles p90 = 0.165 and **p95 = 0.298**. f was frozen at the 95th
  percentile, **f = 0.298**: a passing event must beat what a genuinely-quiet window
  produces 95 percent of the time. This lands almost exactly on the old hand-picked 0.30,
  but now because the clean-null 95th percentile is there, not because 0.30 beat a
  competitor's 0.23.
- **Engine sanity bound (Route ii).** The verified coupled-block engine on short, sparse
  windows matched to the Wikipedia bucketing reaches median macro-collapse 0.72 (K = 4) and
  0.79 (K = 5), so f = 0.298 sits well below the physically attainable collapse and is not
  an impossibly high bar.
- **Clean null frozen.** The calm arm is the V2 genuinely-quiet window, not the contaminated
  fixed onset - 365 d offset.

Integrity caveat carried from the pre-registration: n = 10 is small, so the p95 interpolates
toward the single largest clean drop (Kobe 0.43), making it the least stable summary. We
froze f at p95 = 0.298 as the route specifies and did NOT lower it to the more robust
p90 = 0.165. As it happens the verdict is insensitive to this choice (see below).

## Fresh roster

15 articles, none reused from the tuning roster (`roster_v2.py`, disjoint verified). Mostly
finance and crypto onsets (Ethereum, Tesla, Binance, Dogecoin, Nvidia, Sam Bankman-Fried,
Luna Foundation Guard, Lehman Brothers, Northern Rock, Wirecard, Archegos, Gautam Adani,
First Republic Bank, Coinbase, Reddit), mixing endogenous-community and exogenous shocks,
selected blind to collapse outcome. 4 collapsed to a trivial partition (K < 3: Archegos,
Luna Foundation Guard, Northern Rock, Wirecard) and are reported, not dropped. **11 yielded
K >= 3**, so the test is powered (n = 11 >= 8).

## Result

| quantity | value | frozen target | pass |
|---|---|---|---|
| median event drop | **0.000** | >= f = 0.298 | NO |
| event > clean p90 (0.311) AND MWU p < 0.05 | 0.000 vs 0.311; p = 0.617 | both | NO |
| fraction firing vs shuffle | **2/11 = 0.18** | >= 0.50 | NO |
| powered (K >= 3) | 11 | >= 8 | YES |

Per-article event drops (K >= 3), sorted: **-0.88, -0.63, -0.24, -0.10, -0.03, 0.00, 0.00,
0.00, 0.00, +0.59, +0.64**. Only 2 of 11 (Lehman Brothers +0.64, Sam Bankman-Fried +0.59)
cleared f; the rest sit at zero or negative. Mean -0.06. The event-vs-clean separation is
absent (Mann-Whitney p = 0.617, paired Wilcoxon p = 0.71): the event drops do not exceed the
clean-null drops.

The verdict is robust to the f caveat: the median event drop is 0.00, which fails even
against the more stable clean-null p90 = 0.165, so no reasonable choice of f along the
clean-null distribution rescues a pass.

## Honest reading: why this roster is weaker than the tuning roster

The tuning roster had a median event drop of 0.19 with a significant event-vs-calm
separation; this fresh roster has a median of 0.00 and no separation. The fresh roster is
dominated by finance and crypto onsets, and many of them show the V1-diagnostic
newcomer-flood signature: the onset floods the article with editors OUTSIDE the frozen
pre-onset blocks (Ethereum -0.88, Reddit -0.63, Dogecoin -0.24), so the frozen-partition
metric sees the existing community DILUTED, not synchronized, and the drop goes negative.
The two articles that did collapse hard (Lehman, SBF) are the ones where the pre-existing
editor community itself converged on the event. This is consistent with the established
mechanism (the collapse tracks the existing community losing independence, not raw onset
volume), but it means a roster selected blind to outcome and skewed toward exogenous
financial shocks does not, on aggregate, clear the bar. Selecting for collapse magnitude
would have biased the test; we did not, and the honest consequence is a NOT.

## What this does and does not establish

- It does NOT seal test (ii'). The sealed conjunction fails on magnitude, on the clean-null
  contrast, and on shuffle-firing, on a powered fresh roster.
- It does confirm, on out-of-sample data, that the collapse is heterogeneous and
  outcome-dependent in exactly the direction the newcomer-flood diagnostic predicted:
  endogenous-community events (Lehman, SBF) collapse, exogenous floods (Ethereum, Reddit,
  Dogecoin) do not, and a blind mix of the two averages to zero.
- The paper's criticality gear (test ii') therefore stays honestly UNCONFIRMED at the
  sealed level. The directional/mechanistic findings from the prior synthesis stand; a
  sealed pass would require either a roster pre-screened for high existing-community
  involvement (which biases the test and was deliberately avoided here) or a different
  substrate where the pre-onset blocks are the ones that actually activate.

## Files

- `PRE_REGISTRATION_neff_v2.md` -- written first; f frozen at 0.298 before harvest.
- `derive_f.py` / `derive_f.json` -- principled f derivation (Route i clean-null p95;
  Route ii engine bound).
- `roster_v2.py` -- fresh 15-article roster, disjoint from tuning.
- `harvest_v2.py` -- Wikimedia harvester (adapted from wikipedia/harvest.py).
- `analyze_v2.py` -- sealed analysis (reuses frozen functions + V2 clean-null verbatim).
- `result_neff_v2.json` -- full per-article result and frozen decision.
- `figure_neff_v2.png` -- per-article collapse vs f, and event-vs-clean distributions.

## Reproduce

```
py -3.12 validation/neff_v2/derive_f.py        # derive + freeze f (existing data only)
py -3.12 validation/neff_v2/harvest_v2.py       # fresh roster (Wikimedia API)
py -3.12 validation/neff_v2/analyze_v2.py       # sealed verdict
```
