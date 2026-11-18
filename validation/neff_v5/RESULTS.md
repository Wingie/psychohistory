# neff_v5: sparse block-coupling fit against a fitted null

`potts_fit.py` fits a sparse symmetric pairwise coupling J (and fields h) between the
blocks of an activity matrix by pseudolikelihood (Besag 1975) with an L1 penalty,
solved by accelerated proximal gradient. The fitting recipe follows CRAM (Hoover,
Blayney and Whittington, arXiv 2611.17309, Apache-2.0); the code is a numpy rewrite
that runs on CPU. The null for each run is the same fit repeated on 50 copies of the
data where every block's time order is permuted independently, so each block keeps its
exact marginal and cross-block co-occurrence is broken.

This is aimed at the null-geometry gap in `neff_v4/RESULTS.md`: the block-label
shuffle gives a median event p90 of 0.4909 on Wikipedia and 0.0137 on WSB. A fitted
null is set by each substrate's own marginals rather than by relabelling a Louvain
partition, so the obs/null coupling-mass ratio is on the same scale on both.

## Readout per run

| field | meaning |
|-------|---------|
| `sparsity` | share of block pairs whose fitted coupling is exactly zero |
| `top_couplings` | largest pairs, with signed J for two-state data |
| `coupling_mass` | sum of |J_ij| over pairs i<j |
| `null_mass_mean`, `null_mass_p90` | the same sum on the 50 shuffled refits |
| `obs_over_null_mass` | `coupling_mass / null_mass_mean`; about 1 when blocks move independently |
| `null_pctile_of_obs` | share of shuffled refits with less mass than the observed fit |
| `nlpl`, `nlpl_fields_only` | mean negative log pseudolikelihood per window, with and without J |

States are q=2: 1 when a block's log1p count rose from the previous day (week, for the
ecosystem basket), else 0. L1 weight is `sqrt(log K / T)`.

## Run of 2026-11-18

`py -3.12 run_v5.py` writes `result_potts_v5.json`.

| substrate | data | runs | obs/null mass | sparsity | pctile |
|-----------|------|------|---------------|----------|--------|
| wsb_v4 (Louvain blocks, daily) | `neff_v4/data/` not on this machine | 12 NO_DATA | n/a | n/a | n/a |
| wiki (Louvain blocks, daily) | `wikipedia/data/` not on this machine | NO_DATA | n/a | n/a | n/a |
| ecosystem (7 finance subreddits, weekly, 2020-06 to 2021-06) | committed `conservation_ecosystem/weekly_counts.json` | 1 OK | **2.82** | 0.48 (11 of 21 pairs nonzero) | 1.00 |

Ecosystem detail: coupling mass 2.21 against a null mean of 0.78 (sd 0.30, p90 1.15).
The largest couplings are investing-stocks (+0.61), stocks-StockMarket (+0.46) and
wallstreetbets-options (+0.25); every nonzero coupling is positive. GME, Superstonk and
amcstock are left out because they do not exist for the full span.

The WSB and Wikipedia Louvain runs need their harvests. `neff_v4/harvest_v4.py` reads
the `wallstreetbets_comments.zst` dump from the academictorrents Reddit archive;
`wikipedia/harvest.py` calls the public Wikimedia API. Once either `data/` folder is
present, `run_v5.py` fits it with no further change.

## Tests

`python -m pytest validation/neff_v5 -q` (CPU, about 10 s): a planted four-block Ising
system with couplings +0.8, +0.5 and -0.8 is recovered in sign and support with the
three zero pairs below 0.1; column-shuffled data sits at its null (mean obs/null 0.6 to
1.4 over 12 shuffles); the same seed gives identical output; wrong-shaped, non-integer
and out-of-range input raises.
