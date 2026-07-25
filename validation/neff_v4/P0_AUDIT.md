# Post-seal audit of the v4 null fire rate p0

**Status: the `binomial p = 1.7e-7` figure is UNDER CHALLENGE and should not be
cited as the v4 pass's support until the open item at the bottom of this file is
run.** The sealed rule itself is not being rewritten. Conditions (a) and (c) are
untouched. What is challenged is the value of `p0` inside condition (b), which
was assumed rather than measured.

Reproduce everything below with `python3 p0_audit.py` (stdlib only, no raw data,
no network). It reads only `result_neff_v4.json` and `../neff_v3/derive_f_v3.json`,
both committed.

## What was assumed

`PRE_REGISTRATION_neff_v4.md:57-61` and `RESULTS.md:20-23` set the null fire rate
by construction: under H0 the observed partition is exchangeable with its 300
block-label shuffles, so it clears its own 90th-percentile shuffle one time in
ten, hence `p0 = 0.10`.

The exchangeability does not hold. The observed drop is computed on a
modularity-optimised Louvain partition (`neff_collapse_wsb.py:125`); every null
draw is a random relabelling of the same users. A random relabelling produces
near-identical mixtures of the same commenters, whose mean-normalised activity
series co-move, so the null drop concentrates near zero. The observed statistic
and the null draws are not draws from one distribution, and `p0` is not a
construction constant. It is an empirical quantity. Round-2 finding P-01.

## What the repository's own data says

The published figure reproduces exactly: `P(X>=9 | n=12, p0=0.10) = 1.658350e-07`,
matching `result_neff_v4.json`. Condition (b) (`P < 0.01`) breaks at **p0 = 0.37781**.

v4 measured its own shuffle-null p90 on each of the twelve events. v3 measured the
magnitude drop on twelve genuinely-quiet pseudo-onsets (windows selected before
harvest to sit in the lower half of their era's volume distribution and to avoid
every known event by ±21 days). Thresholding the quiet drops at each measured
shuffle null gives the quiet-window fire rate — the empirical p0 — twelve times over:

| shuffle-null p90 | quiet fires | rate | CP95 lower on p0 | P(X≥9\|12, rate) | condition (b) |
|---|---|---|---|---|---|
| 0.002788 | 10/12 | 0.833 | 0.5619 | 0.8748 | FAILS |
| 0.003605 | 10/12 | 0.833 | 0.5619 | 0.8748 | FAILS |
| 0.004495 | 10/12 | 0.833 | 0.5619 | 0.8748 | FAILS |
| 0.005271 | 10/12 | 0.833 | 0.5619 | 0.8748 | FAILS |
| 0.008323 | 10/12 | 0.833 | 0.5619 | 0.8748 | FAILS |
| 0.013337 | 10/12 | 0.833 | 0.5619 | 0.8748 | FAILS |
| 0.014029 | 10/12 | 0.833 | 0.5619 | 0.8748 | FAILS |
| 0.015102 | 10/12 | 0.833 | 0.5619 | 0.8748 | FAILS |
| 0.017121 | 10/12 | 0.833 | 0.5619 | 0.8748 | FAILS |
| 0.017923 | 10/12 | 0.833 | 0.5619 | 0.8748 | FAILS |
| 0.095760 | 6/12 | 0.500 | 0.2453 | 0.0730 | FAILS |
| 0.224244 | 5/12 | 0.417 | 0.1810 | 0.0206 | FAILS |

`CP95 lower` is the exact one-sided Clopper-Pearson lower confidence bound on the
quiet fire rate: the `p` solving `P(X>=k | 12, p) = 0.05`.

**Condition (b) holds at none of the twelve thresholds v4 itself measured.** At the
modal reading (10 of 12, which obtains at ten of the twelve thresholds) even the
conservative one-sided 95% lower bound on p0 is **0.5619**, above the 0.37781 break
point. The two thresholds that give a lower fire count are the two outlier nulls
(0.096 and 0.224, an order of magnitude above the other ten); condition (b) fails
there too, at 0.073 and 0.021 against a 0.01 bar.

This is a stronger statement than round 2 reached. P-01 offered p0 ≈ 0.79–0.83 as
point estimates and correctly withdrew them as not established. The result here is
not a point estimate and does not need to be: across the entire range of p0 the
repository's own measurements support, there is no value at which the sealed rule's
condition (b) passes.

## What this is not

This is a **proxy**, and the proxy is the finding's main weakness. It thresholds v3
quiet-window *magnitude drops* against shuffle nulls measured on *v4 events*, because
each quiet window's own `fires_vs_shuffle` flag does not exist in the committed data.
It was computed — `derive_f_v3.py` calls the same `analyze_run` that runs the 300×
shuffle null and returns the flag — and then dropped from the row dict one return
before serialisation (round-2 finding P-03). The shuffle compute was paid for and the
answer discarded.

That is fixed on this branch: `derive_f_v3.py` now serialises `fires_vs_shuffle`,
`shuffle_pctile_of_obs` and `shuffle_null_p90` per clean window, and aggregates the
quiet fire rate. The fix changes nothing about f (f is the p95 of the drop
distribution, which these fields do not enter) and takes effect only on the next
harvest, which needs the WSB dump.

Two further limits, stated so a referee does not have to find them: n = 12 quiet
windows is small, and the real fire criterion is a percentile within a window's own
null, not a magnitude against a constant. Neither limit points the other way —
both the point estimate and its lower bound sit far above the break point — but
neither is discharged by this audit.

## The open item

Run the `analyze_v4` fire rule over **at least 30** genuinely-quiet WSB
pseudo-onsets, recording each window's own `fires_vs_shuffle`, and use the measured
rate as p0. CPU work on harvested data; no GPU. It needs the WSB dump
(`subreddits24`), which is gitignored and regenerable via
`validation/neff_v3/harvest_v3.py`. Re-running `derive_f_v3.py` alone now yields
the n=12 version of the same measurement for free, as a first read.

Until that runs, the honest statement of the v4 result is: **9 of 12 cascades
collapsed past their own block-label shuffle null, and the median cascade beat all
300 relabellings of its own nodes. The binomial p-value attached to that count is
not established, because the null fire rate it is computed against is not.** The
9/12 count and the median-percentile-1.000 result are measurements and stand. The
1.7e-7 is an inference from an assumption the repository's own data contradicts.
