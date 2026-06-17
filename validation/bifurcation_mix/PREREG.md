# PRE-REGISTRATION -- Test (iii') Bifurcation-Mix Conjecture (the bet most likely to fail)

**Status:** COMMITMENT ARTIFACT. This document freezes the classification rule BEFORE any
B-fraction is computed. It is written first, on purpose, so the rule cannot be tuned to
clear the floor after seeing the answer.

**Date frozen:** 2026-06-16.

**Parent specification:** `validation/PRE_REGISTRATION.md`, test (iii'). Committed floor
**pi_B = 0.60**. Refutation rule: the conjecture is REFUTED on this roster if the
B-tipping fraction is **< 0.60**.

**The conjecture under test.** The program's predictive value rests on decision-relevant
social crises being PREDOMINANTLY B-tipping (slow fold / saddle-node bifurcation, which
emits early warning) rather than N-tipping (noise-induced) or R-tipping (rate-induced /
sudden external shock), the latter two giving NO early warning. Operationally: adjudicate
each event on a labelled roster as B / N / R by a pre-declared rule, blind to the
early-warning scores, and refute if the B-fraction falls below pi_B.

---

## 0. The roster (frozen, named here before classification)

The roster is the dynamic-N_eff-collapse event roster already harvested for test (ii'):

- **Wikipedia (n = 14 OK events)** -- `validation/wikipedia/roster.py`,
  `validation/wikipedia/result_wiki_neff.json`. The 14 events whose pre-onset editor
  partition had K >= 3 structure (status OK in the result file): Bitcoin, Boeing 737 MAX,
  Credit Suisse, Diego Maradona, Donald Trump, Evergrande Group, Joe Biden, Kobe Bryant,
  NATO, Notre-Dame de Paris, Queen Elizabeth II, Suez Canal, Twitter, Volodymyr Zelenskyy.
  (The 6 roster articles that returned TRIVIAL_PARTITION -- GameStop, FTX, OpenAI,
  Robinhood, Silicon Valley Bank, Terra -- carry no frozen blocks and no collapse number,
  so the STRUCTURAL proxy cannot be computed for them; they are EXCLUDED from the
  structural arm and noted. The SUBSTANTIVE arm rates all events for which a public onset
  description exists.)
- **r/wallstreetbets (n = 10 OK cascades)** -- `validation/reddit_wsb/roster_wsb.py`,
  `validation/reddit_wsb/result_wsb_neff.json`: GME_squeeze_jan2021, GME_leg2_feb2021,
  AMC_meme_jun2021, GME_runup_nov2021, market_selloff_jan2022, market_drop_may2022,
  svb_collapse_mar2023, regional_bank_may2023, aug2024_vix_spike, gme_kitty_may2024.

**Combined frozen roster size = 24 labelled cascades** (14 Wikipedia + 10 WSB). This meets
the parent M = 20 minimum. Both rosters are CONVENIENCE SAMPLES of attention cascades, not
a random sample of social crises (selection caveat carried in RESULTS.md).

---

## 1. STRUCTURAL classification rule (blind to early-warning scores)

**Inputs used (and ONLY these):** for each event, (a) the existing-community share of
onset activity, and (b) onset abruptness. NEITHER input touches the early-warning / N_eff
collapse SCORE. The existing-community share is the diagnostic V1 quantity
(`validation/wikipedia/diagnostics/v1_newcomer_flood.py`), whose correlation with collapse
magnitude (Spearman rho = +0.45) is the V1 finding motivating this proxy. We use the share
itself as a STRUCTURAL feature, not the collapse outcome it correlates with.

**Existing-community share f_existing** (frozen definition, identical on both substrates):
fraction of ONSET-window focal activity made by participants who were ALSO active in the
pre-onset window (i.e. members of the frozen pre-onset partition / pre-onset author set).
- Wikipedia: onset-window = `[onset, onset+21d)` focal article revisions; pre-onset set =
  the frozen K-block editor partition. (Exactly V1's `f_existing`.)
- WSB: onset-window = `[onset-3d, onset+22d)` comments; pre-onset set = authors who
  commented in `[onset-90d, onset)`. (Mirrors V1, adapted to the WSB windows used by
  `neff_collapse_wsb.py`.)

**Onset abruptness a_abrupt** (frozen definition): the ratio of onset-window mean daily
activity to pre-onset-window mean daily activity (focal edits/day for Wikipedia,
comments/day for WSB). High ratio = sudden spike; low ratio = gradual ramp. This is a
purely volumetric feature, computed from the same harvested activity, independent of the
block-synchronization SCORE.

**Frozen thresholds (committed now, before computation):**
- `SHARE_HI = 0.20` -- existing-share at or above this counts as "high existing-share"
  (endogenous-community-driven). Justification: V1's exogenous floods cluster well below
  this (Suez 0.03, Notre-Dame 0.01, Kobe 0.05, NATO 0.08), while the endogenous
  synchronizers sit at or above it (Evergrande 0.43, Trump 0.57, Bitcoin 0.71, Queen 0.30,
  Zelenskyy 0.27). 0.20 is the natural gap between the two clusters and is fixed here
  before the WSB shares are computed.
- `ABRUPT_HI = 8.0` -- onset/pre-onset activity ratio at or above this counts as a "sudden"
  spike (a near-order-of-magnitude jump within the onset window). Below it the ramp is
  "gradual."

**Decision map (applied mechanically):**
1. **B-tipping** if `f_existing >= SHARE_HI` (the existing community supplies a meaningful
   share of onset activity, i.e. endogenous synchronization of a pre-existing population --
   the signature of a slow fold approached by a drifting control parameter). Abruptness is
   recorded but B is keyed on existing-share, because endogenous community synchronization
   is the B signature regardless of how fast the public spike looks.
2. **R-tipping** if `f_existing < SHARE_HI` AND `a_abrupt >= ABRUPT_HI` (low existing
   share + sudden external trigger = a population flooded by newcomers reacting to an
   exogenous shock, no pre-existing community drift).
3. **N-tipping** if `f_existing < SHARE_HI` AND `a_abrupt < ABRUPT_HI` (low existing share,
   no sudden trigger = diffuse noise-like onset with neither endogenous synchronization nor
   a sharp external shock).

For the proportion test, B counts as B; N and R both count as not-B.

---

## 2. SUBSTANTIVE classification rule (blind to the N_eff / collapse outcome)

For each event, classify B / N / R from the PUBLIC description of the onset, using only
what was knowable at or before onset, with a one-line rationale per event. The rater does
NOT consult any collapse / N_eff number when rating.

- **B-tipping** if the onset is the culmination of a SLOW-BUILDING crisis or bubble whose
  control parameter was visibly drifting toward a tipping point (a fold approached
  gradually): e.g. a months-long balance-sheet deterioration, a reflexive price bubble
  inflating over weeks, a long-anticipated institutional failure.
- **R-tipping** if the onset is a SUDDEN, largely UNANTICIPATED external shock that drove a
  stable state past a threshold with no preceding slow drift: e.g. a fatal crash, a sudden
  death, a surprise invasion, a one-off physical accident, a surprise acquisition close.
- **N-tipping** if the onset is best described as endogenous noise crossing a basin
  boundary with neither a slow control-parameter drift nor a single identifiable external
  shock.

Rationales are written into the script's `SUBSTANTIVE` table (one line each), committed in
the same commit as this PREREG, and are not revised after the B-fraction is seen.

---

## 3. Test statistics (frozen)

- **B-fraction (structural)** = (# events classed B by rule 1) / (# events with a
  computable structural classification).
- **B-fraction (substantive)** = (# events classed B by rule 2) / (# all roster events).
- **Inter-rater agreement** between the structural proxy and the substantive rating, on the
  events classifiable by both, reported as raw agreement and Cohen's kappa over the
  3-category {B, N, R} labels (and, secondarily, over the binary {B, not-B} collapse).
- **Pass/fail vs pi_B:** SUPPORTED if B-fraction >= 0.60; REFUTED if < 0.60. Reported
  honestly for each classification separately; if they disagree across the floor, that is
  reported as the headline.

This is a proportion test against a committed floor, not a skill test; no null model is
required (per the parent spec).

---

## 4. Honesty rails

- The rule above is frozen BEFORE the B-fraction is computed. No threshold is moved after
  seeing the answer. If the result is REFUTED, it is reported as REFUTED.
- The roster is a convenience sample of ATTENTION cascades (selection caveat): events were
  selected for having a harvestable pre-onset community and a clean public onset date, NOT
  randomly from the space of decision-relevant social crises. A B-fraction on this roster
  does not transport to "social crises in general" without that caveat attached.
- Thresholds are committed in-sample (not externally OSF/hash-lodged); this matches the
  current status of the sibling test (ii') runs and is stated, not hidden.
