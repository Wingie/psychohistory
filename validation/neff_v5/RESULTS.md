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

`py -3.12 run_v5.py` writes `result_potts_v5.json`. The wiki summary carries a `by_arm` split.

| substrate | data | runs | obs/null mass | sparsity | pctile |
|-----------|------|------|---------------|----------|--------|
| wsb_v4 (Louvain blocks, daily) | `neff_v4/data/` not on this machine | 12 NO_DATA | n/a | n/a | n/a |
| wiki, event arm (Louvain blocks, daily) | `wikipedia/harvest.py`, 20 roster articles | 14 OK, 6 K<3 | **2.10** (pooled 2.98) | 0.83 | 0.94 |
| wiki, matched calm arm (onset minus 365 days) | same harvest | 11 OK, 9 K<3 | 3.18 (pooled 6.11) | 0.83 | 0.96 |
| ecosystem (7 finance subreddits, weekly, 2020-06 to 2021-06) | committed `conservation_ecosystem/weekly_counts.json` | 1 OK | **2.82** | 0.48 (11 of 21 pairs nonzero) | 1.00 |

Ecosystem detail: coupling mass 2.21 against a null mean of 0.78 (sd 0.30, p90 1.15).
The largest couplings are investing-stocks (+0.61), stocks-StockMarket (+0.46) and
wallstreetbets-options (+0.25); every nonzero coupling is positive. GME, Superstonk and
amcstock are left out because they do not exist for the full span.

Wikipedia detail (harvest of 2026-11-18, the roster default: 20 articles, event and
calm arm each, 90 baseline days, 21 post days, at most 150 editors per article; 1,563
API calls, 25 MB, kept out of git). Each OK run has 111 daily windows and 50 shuffled
refits. "Pooled" is the summed coupling mass over the summed null mean, which is steadier
than the median of per-run ratios: the L1 penalty fits all-zero couplings on many
shuffles, so a run's null mean can sit near zero (three runs have a null mean of exactly
0 and no ratio) and per-run ratios range from 0 to 31. Across the 25 OK runs, 14 have
coupling mass above their null p90 and 8 fit no coupling at all. 34 of the 37 listed top
couplings are positive (range -0.08 to +0.60). The event arm does not carry more
coupling than its calm arm on either readout.

Largest coupling per event run, with each block named by the two articles most of its
members co-edited in the baseline window (`block_top_articles` in the JSON):

| article | J | block a | block b |
|---------|---|---------|---------|
| Credit Suisse | +0.19 | Silicon Valley Bank, 15-minute city | John Wick: Chapter 4, Alicia Garza |
| Queen Elizabeth II | +0.29 | Liz Truss, Olivia Newton-John | July 2022 UK government crisis, Boris Johnson |
| Donald Trump | +0.22 | Joe Biden, Mike Pence | US racial unrest 2020-2023, 2020 US election |
| Boeing 737 MAX | +0.17 | Aeroperú Flight 603, Air France Flight 447 | Boeing 787, Boeing 737 |
| NATO | +0.16 | Russo-Ukrainian war, 2022 Winter Olympics | B-52, Canadian Armed Forces |
| Joe Biden | +0.14 | Donald Trump, Kamala Harris | Ruth Bader Ginsburg, Electoral College |

GameStop, FTX, OpenAI, Robinhood, Silicon Valley Bank and Terra give fewer than three
Louvain blocks in the event arm (too few pre-onset editors with shared articles), so
they have no fit.

Two fixes came out of this run, each with a test. Louvain partitions changed with
`PYTHONHASHSEED`, because networkx's subgraph view iterates a set of string node names
when the giant component is under half the graph; `pipeline_v03/common.louvain_giant_component`
relabels nodes to sorted integers first, and the three `blind_partition` functions call
it. Two roster titles are redirects ("Queen Elizabeth II" to "Elizabeth II", "Twitter"
to "X (social network)"), so the focal article stayed in the co-editing graph under its
current name; `harvest.py` now stores `resolved_title` and `coedit_graph` drops both.
`wikipedia/result_wiki_neff.json` was computed before both fixes and has not been rerun.

The WSB Louvain runs stay NO_DATA: `neff_v4/harvest_v4.py` reads the
`wallstreetbets_comments.zst` dump from the academictorrents Reddit archive, which is
not on the host. Once `neff_v4/data/` is present, `run_v5.py` fits it with no further
change.

## Tests

`python -m pytest validation/neff_v5 -q` (CPU, about 10 s): a planted four-block Ising
system with couplings +0.8, +0.5 and -0.8 is recovered in sign and support with the
three zero pairs below 0.1; column-shuffled data sits at its null (mean obs/null 0.6 to
1.4 over 12 shuffles); the same seed gives identical output; wrong-shaped, non-integer
and out-of-range input raises; the summary splits event and calm arms; Louvain gives
one partition across six `PYTHONHASHSEED` values; the co-editing graph drops the focal
article under its current title.
