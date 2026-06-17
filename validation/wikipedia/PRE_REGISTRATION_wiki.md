# Pre-registration: powered dynamic-N_eff-collapse test on Wikipedia (test ii')

**Status: thresholds committed BEFORE any data was harvested or any graph built.**
This file is written first, on purpose, so the pass/fail line cannot move after the
numbers are seen. It discharges (in a cross-domain, powered form) falsification test
**(ii') Dynamic N_eff collapse** of the paper's pre-registration, which the GitHub
pilot could only run at n=1 ("only suggestive").

## The claim under test

Near-decomposability says a calm population is partitioned into many statistically
independent blocks (high effective number N_eff). The criticality mechanism says that
at a cascade onset those blocks SYNCHRONIZE, so the effective number of independent
blocks COLLAPSES (N_eff falls toward 1). The static half (distinct blocks pre-onset)
was already confirmed blind; this test is the DYNAMIC half (the collapse across onset),
which is the load-bearing unconfirmed gear.

## Substrate and design (frozen)

- **Substrate:** English Wikipedia editor activity, via the public Wikimedia API
  (`prop=revisions`, `list=usercontribs`). No throttle wall, no torrent, direct HTTPS.
- **Unit:** a focal article that ALREADY EXISTED with steady editing before its
  attention spike (articles created AT the event are "born into cascade" and excluded,
  the GitHub failure mode). Roster in `roster.py` / `roster.md`, frozen here.
- **Blocks (blind):** editors active on the focal article in the pre-onset baseline
  window `[onset-90d, onset)` define the editor set (cap: 150 most-active, logged);
  their main-namespace co-editing graph (edge = co-edited >= 1 article in the baseline
  window, weighted by shared articles) is partitioned by blind Louvain. NO outcome
  knowledge enters the partition. The partition is FROZEN on the pre-onset graph.
- **N_eff trajectory:** the frozen blocks' edit activity ON THE FOCAL ARTICLE is bucketed
  in time from baseline through onset. Two metrics, reported side by side:
  - **PRIMARY (canonical):** macro variance-ratio on z-scored per-block activity,
    `N_eff = mean_k Var_t(z_k) / Var_t(mean_k z_k)` (the engine `block_metrics`
    definition; collapses K->1 under full synchrony). This is the paper's metric.
  - **SECONDARY (legacy):** the Pearson-Kish form `K/(1+(K-1) rho_bar)` used by the
    GitHub/Reddit pipeline. Reported only to show whether the GitHub "suggestive"
    result was partly a metric artifact (engine.py flags Pearson-Kish as misleading
    under sign-sharing synchrony).
- **Collapse statistic:** `drop = 1 - N_eff(onset window)/N_eff(baseline window)`,
  computed on the PRIMARY metric.

## Null models (against the prosecutor's fallacy)

1. **Block-label shuffle** (>= 200 permutations per article): randomly permute the
   editor->block assignment, recompute the collapse. A real structural collapse must
   exceed the shuffled-null distribution.
2. **Matched calm window:** the SAME article re-run with onset := real_onset - 365 days
   (a presumed-quiet period). The collapse there is the base rate of "N_eff change with
   no event."

## Committed thresholds (frozen)

- **f = 0.30** : the minimum median primary-N_eff `drop` across the event roster for the
  collapse mechanism to be SUPPORTED (the GitHub langchain pilot showed 0.23 and was
  called "only suggestive"; we require a larger, powered median).
- **percentile = 0.90** : an event article "fires" iff its observed collapse exceeds the
  90th percentile of its own block-label-shuffle null (the suite's 90th-pctile convention).
- **Powered = n >= 8** event articles that yield a non-trivial pre-onset partition (K >= 3).

## Decision rule (frozen, evaluated once)

The dynamic-collapse mechanism is **SUPPORTED (powered, cross-domain)** iff ALL hold:
1. median event-window primary-N_eff `drop` >= **f = 0.30**;
2. fraction of event articles that fire against their shuffle null (>= 90th pctile) >= **0.5**;
3. event-window drops exceed matched-calm-window drops (one-sided; event median drop
   above the 90th percentile of the calm-window drop distribution).

If (1)-(3) hold on n>=8 it is a powered positive. If they fail, that is a real, reportable
NEGATIVE for test (ii') (the collapse is a metric/anecdote artifact), and the paper's
criticality gear stays "unconfirmed" honestly. Either way the result is reported straight.

## Honesty rails

Single platform; analyst-frozen onsets (public event dates); in-sample thresholds (these
are committed but not externally lodged to OSF/hash, so this is a powered PILOT, not the
externally-sealed FA-0 test). The matched-calm and shuffle nulls guard the prosecutor's
fallacy. Result is illustrative of direction and magnitude across a real roster, not a
calibrated classifier.
