# Temporal falsification tests for the bounded-psychohistory paper

Three falsification tests, each a `py -3.12` script with robust field
auto-detection, an explicit null / base rate, and an honest verdict.

| # | script | tests | conserved quantity / signature |
|---|--------|-------|--------------------------------|
| i | `test_zero_sum.py` | zero-sum attention within a subreddit | de-trended topic shares trade off (negative co-movement beyond a permutation null) |
| iii | `test_early_warning.py` | critical slowing down before a cascade | variance + lag-1 autocorrelation rise pre-cascade **vs a base rate of non-cascade windows** |
| ii | `test_blocks_sync.py` | location-subreddit block synchrony | macro variance-ratio N_eff collapses K→1 around a shared shock |

All three are pure standard-library Python (no numpy/pandas needed) and read the
same dump formats.

## Data sources (what to download / fetch)

Reddit.com is blocked, but the archive mirrors are separate hosts and work:

### A. Arctic Shift aggregation API (BEST for time-series; used to build the bundled data)
Host: `https://arctic-shift.photon-reddit.com`
Aggregation endpoint returns **counts per time bucket** without downloading every
post — ideal and cheap:

```
GET /api/posts/search/aggregate?aggregate=created_utc&frequency=month&subreddit=<SUB>&after=YYYY-MM-DD&before=YYYY-MM-DD&limit=100
```
Notes learned empirically:
- `frequency` is required: year|quarter|month|week|day|hour.
- `limit` must be >= 1 (it caps something internal; `count` per bucket is still the true total).
- **Monthly works back several years**; very recent weeks/days can return 0 because
  the recent index lags. Use `frequency=month`.
- Large/busy subs **time out (HTTP 422 "Timeout. Maybe slow down a bit")** on
  multi-year spans — **chunk one year per request** and merge (see `data/_harvest_monthly.py`).
- For comment bodies / comment time-series use `/api/comments/search` and
  `/api/comments/search/aggregate` (same params). Comment bodies for the separate
  "comment-concordance" idea come from these same comment dumps.

### B. PullPush API (Pushshift successor; post-level NDJSON)
Host: `https://api.pullpush.io`
```
GET /reddit/search/submission/?subreddit=<SUB>&size=100&sort=desc[&before=<epoch>]
```
Paginate with `before=<oldest created_utc seen>`. Returns full post objects.
Rate-limited (HTTP 429) — sleep ~1.2 s between pages, retry with backoff. Used to
build the bundled `data/*.ndjson` post-level files. Aggregation variant
(`&aggs=created_utc&frequency=month&size=0`) exists but was 429-throttled at
harvest time; Arctic Shift was used instead.

### C. Monthly dumps (bulk, for serious runs)
- academic-torrents.com — Watchful1 / Pushshift monthly `RS_YYYY-MM.zst`
  (submissions) and `RC_YYYY-MM.zst` (comments), NDJSON inside zstd.
- the-eye.eu / `/redarcs/` and Arctic Shift's own dump listing — same format.
Each script auto-detects NDJSON, so a decompressed `RS_*.ndjson` filtered to a
subreddit drops straight in. Do **not** download multi-GB files unless running at
scale; the API path above is enough for these tests.

## Recommended subreddit set

**Economics topic sub (zero-sum, early-warning):** `AskEconomics`
(also good: `Economics`, `AskEconomics`, `wallstreetbets` for a sharper cascade).

**Location BLOCKS (synchrony test):**
`europe`, `germany`, `france`, `italy`, `spain`, `unitedkingdom`, `Netherlands`,
`poland` (add `sweden`, `ireland`, `austria`, `portugal` for more blocks → higher
K → cleaner N_eff).

**Time span:** 2021-01 → present, monthly, for the block + early-warning tests
(need many buckets for a base rate). 8+ weeks suffices only for a quick zero-sum check.

**Candidate shared shocks / cascades to label:**
- 2022-02-24 Russia invades Ukraine (continental shock → expect N_eff collapse).
- 2020-03 COVID lockdowns (global shock).
- 2022-09 European energy crisis peak.
Use `--shock 2022-02-01` etc. (bucket containing the event).

## What's already in `data/`

Fetched live during construction (real data, not synthetic):
- `monthly_submissions.json` — **monthly submission counts** per subreddit
  (Arctic Shift aggregation, 2021→2025), for the block + early-warning tests.
- `ask_econ.ndjson` (4000 posts, ~11 wk), `loc_*.ndjson` (europe/france/germany/
  italy/spain post-level, ~2-6 wk each) — PullPush post-level, for the zero-sum
  topic test and short-horizon checks.
- `_harvest_monthly.py`, `_harvest.py` — the harvesters (re-run to extend).

## Commands

```bash
cd D:/code/psychohistory_v04_bundle/validation/temporal

# (i) zero-sum attention on AskEconomics (topic = keyword buckets)
py -3.12 test_zero_sum.py data/ask_econ.ndjson --topics keywords --perms 2000
#   or by flair:
py -3.12 test_zero_sum.py data/ask_econ.ndjson --topics flair

# (iii) early-warning, from the monthly count series, around a labeled cascade
py -3.12 test_early_warning.py data/monthly_submissions.json \
    --series-key europe --cascade 2022-02-01 --window 6
#   or bucket raw submissions weekly:
py -3.12 test_early_warning.py data/loc_europe.ndjson --bin week --cascade 2025-05-08 --window 4

# (ii) block synchrony / N_eff collapse on the location blocks
py -3.12 test_blocks_sync.py data/monthly_submissions.json \
    --blocks germany france italy spain europe unitedkingdom Netherlands poland \
    --window 6 --shock 2022-02-01 2020-03-01
```

## Honesty notes baked into the scripts
- **Zero-sum:** the simplex constraint sum(shares)=1 forces *some* negative
  co-movement mechanically; the permutation null is what turns "shares trade off"
  into an actual test.
- **Early-warning:** "the indicators rose before the cascade" is the prosecutor's
  fallacy. The script reports the **base rate** (how often the same detector fires
  in non-cascade windows), a percentile, and an AUC. One cascade = one point;
  real validation aggregates AUC over many labeled cascades.
- **Blocks:** N_eff is the **macro variance-ratio / order parameter** (K independent
  blocks → N_eff≈K, full synchrony → N_eff≈1), not a mean of pairwise Pearson
  correlations of fluctuations.
