# Test (iii') Bifurcation-Mix Conjecture -- RESULTS

**The bet the paper names as most likely to fail.** Pre-registered rule frozen in
`PREREG.md` BEFORE any B-fraction was computed. Committed floor **pi_B = 0.60**: the
conjecture is REFUTED on this roster if the B-tipping fraction is below 0.60. Two
independent classifications were applied to the same frozen roster of 24 attention
cascades (14 Wikipedia + 10 r/wallstreetbets), one STRUCTURAL (blind to the early-warning
/ N_eff score) and one SUBSTANTIVE (blind to the N_eff collapse outcome).

## Headline

**The two pre-registered classifications disagree across the floor, and the honest verdict
is split.**

- **STRUCTURAL proxy: B-fraction = 0.750 (18 B / 6 R / 0 N of 24) -> SUPPORTED.**
- **SUBSTANTIVE adjudication: B-fraction = 0.333 (8 B / 16 R / 0 N of 24) -> REFUTED.**
- **Inter-rater agreement is weak:** raw agreement 0.583, Cohen's kappa = 0.286 (identical
  on the 3-category {B,N,R} and the binary {B, not-B} collapse).

When two pre-registered rules straddle the committed floor, we do NOT pick the one that
passes. The substantive rule is the one that actually encodes the conjecture's MEANING
(slow-building crisis = B vs sudden external shock = R, judged from the public onset), and
it REFUTES. The structural proxy is a mechanical feature that, on inspection below,
saturates on one substrate and therefore over-counts B. So the defensible reading is:
**on this roster the bifurcation-mix conjecture is REFUTED by the meaningful classifier and
only "passes" under a proxy that is shown below to be biased toward B.** We report it as a
REFUTATION with the disagreement and its cause stated in full.

## The pre-registered rule (frozen first)

STRUCTURAL (keyed on two features that never touch the N_eff SCORE):
- `f_existing` = existing-community share of onset activity (the diagnostic V1 quantity,
  whose Spearman rho = +0.45 with collapse magnitude motivated this proxy). For Wikipedia
  this is V1's per-article value; for WSB it is the fraction of onset-window comments by
  authors already active in the pre-onset 90-day window.
- `a_abrupt` = onset/pre-onset mean-daily-activity ratio (volumetric, score-free).
- **B** if `f_existing >= 0.20`; else **R** if `a_abrupt >= 8.0`; else **N**.

SUBSTANTIVE (public onset description, one line per event, blind to the collapse outcome):
slow-building crisis/bubble = **B**; sudden unanticipated external shock = **R**; endogenous
noise = **N**. Rationales are in `classify.py`'s `SUBSTANTIVE` table, committed with the
PREREG.

Thresholds `SHARE_HI = 0.20` and `ABRUPT_HI = 8.0` were fixed in `PREREG.md` before the WSB
shares were computed.

## Results table

See `classification_table.md` for the full per-event table. The shape of the disagreement:

- On **Wikipedia** the two rules agree well: 9/14 agree, and the structural proxy correctly
  separates the endogenous synchronizers (Bitcoin, Trump, Evergrande, Credit Suisse all
  B/B) from the exogenous shocks (Boeing, Maradona, NATO, Kobe, Suez, Notre-Dame all R/R).
  The 5 Wikipedia disagreements (Joe Biden, Twitter, Queen, Zelenskyy structural-B but
  substantive-R) are events with a moderate existing-editor share that the proxy reads as
  endogenous but whose public onset was a discrete sudden event (an election call, a deal
  close, a death, a surprise invasion).
- On **WSB** the structural proxy collapses to near-useless: `f_existing` is 0.83-0.93 for
  9 of 10 cascades, so the proxy labels almost everything B regardless of substance. This
  is the methodological flaw: on a SINGLE subreddit the pre-onset author pool is enormous
  (hundreds of thousands of commenters over 90 days), so nearly every onset comment comes
  from someone who posted before, and the existing-share is high by construction. The
  feature that cleanly discriminated endogenous vs exogenous on Wikipedia does not transfer
  to a single dense community. Substantively, only 4 of the 10 WSB cascades are genuine
  endogenous reflexive bubbles (the GME/AMC meme-squeeze family); the other 6 are reactions
  to external macro/banking/volatility shocks and rate SUBSTANTIVE-R.

## Verdict vs pi_B = 0.60

| Classification | B-fraction | vs pi_B = 0.60 | Verdict |
|---|---:|:---:|:---:|
| STRUCTURAL proxy | 0.750 | above | SUPPORTED |
| SUBSTANTIVE adjudication | 0.333 | below | **REFUTED** |
| Inter-rater (3-cat) | kappa = 0.286 | -- | weak agreement |

**Adopted verdict on this roster: REFUTED.** The conjecture that decision-relevant social
crises are PREDOMINANTLY (>= 60%) slow-fold B-tipping does not hold on this roster under the
classifier that encodes the conjecture's actual content. The structural proxy's 0.75 is not
taken as a pass because it is driven by the WSB saturation artifact (remove WSB and the
proxy's own B-count is 8/14 = 0.571 on Wikipedia alone, already below the floor; the
substantive Wikipedia-only B-fraction is 4/14 = 0.286). On both substrates the substantive
rating puts B in the minority once the GME/AMC meme family is separated from the
shock-reactions.

This is the outcome the paper pre-committed to as the most likely failure, and it failed.
The framework's early-warning machinery (test iii) is consequently load-bearing only on the
minority B-tipping subset (the meme bubbles and the slow balance-sheet failures), exactly
the events where critical slowing-down is expected, and is correctly silent on the majority
R-tipping shocks where it predicts no warning.

## Selection caveat (carried, load-bearing)

The roster is a CONVENIENCE SAMPLE of attention cascades, not a random sample of
decision-relevant social crises. Events were chosen for having a harvestable pre-onset
community and a clean public onset date. A B-fraction measured on attention cascades does
not transport to "social crises in general." In particular the roster is heavy with sudden
public events (deaths, crashes, deal closes, invasions) precisely because those produce
clean, datable attention spikes, which biases the substantive count toward R; and the WSB
arm over-samples one venue's reflexive bubbles, which biases its substantive count toward B.
Neither bias is corrected. The honest claim is narrow: on this specific labelled roster,
under a pre-registered substantive rule, B-tipping is the minority, so the conjecture is
refuted here. A clean test would require a randomly drawn frame of decision-relevant crises
with externally lodged thresholds, which this is not.

## Honesty rails

- Rule frozen in `PREREG.md` before any B-fraction was computed; thresholds not moved after
  seeing the answer; the result that refutes is reported as refuting.
- Two classifications reported side by side, including the one that "passes"; the
  disagreement (kappa = 0.286) and its mechanical cause (WSB existing-share saturation) are
  stated, not hidden.
- In-sample thresholds, not externally OSF/hash-lodged (same status as the sibling test ii'
  runs), stated here.

## Files

- `PREREG.md` -- frozen rule (written first).
- `classify.py` -- classification script (structural features + substantive table + kappa).
- `classification_table.md` -- full per-event table.
- `result_bifurcation_mix.json` -- machine-readable result.
- `RESULTS.md` -- this file.

## Reproduce

```
py -3.12 validation/bifurcation_mix/classify.py
```
