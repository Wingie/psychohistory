# Test (i) - Conservation / Zero-Sum Attention at ECOSYSTEM scale

**Status: CONTRADICTED at the basket scale (total balloons during the mania).**
Pre-registered thresholds (from `validation/PRE_REGISTRATION.md`): drift bound
**X = 15%**, composition churn floor **Y = 40%**.

## What the test claims

Aggregate human attention is approximately a conserved, sub-generational budget.
During a mania, attention is supposed to REDISTRIBUTE across topics (composition
churns) while the TOTAL stays roughly flat (net drift inside +/- X). The prior pilot
(`validation/backtests/RESULTS.md`, within r/AskEconomics) contradicted the claim,
but at the wrong scale: a single subreddit can freely import or export attention
from the rest of the internet. The pre-registered fix is to measure a BASKET of
related subreddits, whose total should be more nearly conserved than any one member.

This run executes that ecosystem-scale test for the canonical case: the January
2021 GameStop / meme-stock mania, over a finance/meme basket of 10 subreddits.

## Data

Per-subreddit SUBMISSIONS dumps streamed from the academictorrents Reddit dump
(see `FETCH_LOG.md`). Basket (frozen): wallstreetbets, investing, stocks,
StockMarket, options, pennystocks, CryptoCurrency, GME, amcstock, Superstonk.
Weekly submission counts were built for every week in 2020-06-01 .. 2021-07-04
(`harvest_weekly.py` -> `weekly_counts.json`; 1.42 M WSB submissions in range,
~3.0 M submissions in range across the basket).

**Proxy disclosure.** Submission count is an ACTIVITY PROXY for attention-minutes,
not a direct measure. It is the cleanest cheap proxy available from the dump and it
moves with the quantity the conservation claim is about; it is not the quantity
itself.

## Windows (8 ISO-weeks each)

- **CALM**:  2020-10-05 .. 2020-11-23 (autumn 2020, pre-mania, quiescent).
- **MANIA**: 2021-01-18 .. 2021-03-08 (GME squeeze peak + immediate aftermath).

## Result

| quantity                         | CALM (mean wk) | MANIA (mean wk) | drift / churn |
|----------------------------------|---------------:|----------------:|--------------:|
| BASKET TOTAL submissions / week  |        11,900  |        170,660  | **+1,334%**   |
| composition churn (TV distance)  |              - |               - | **40.0%**     |

- **Total attention drift = +1,334%** (the basket total grew about 14x). The
  pre-registered bound is X = 15%. The total did not stay flat; it ballooned by
  roughly **89x the tolerance**. WSB alone went from ~5,100 to ~123,500
  submissions/week (about 24x).
- **Composition churn = 40.0%** (TV distance between the calm and mania share
  vectors), right at the Y = 40% floor: the mix did reshuffle (CryptoCurrency's
  share collapsed as GME/amcstock/WSB took over). But churn is moot once the total
  has exploded.

### Incumbent-only control (drop the newborn subs)

amcstock and Superstonk barely existed before the mania (0 submissions in the calm
window; Superstonk was created in March 2021, after the peak). To check that the
balloon is not merely "new subreddits being born," we recomputed on the 8 subs that
already existed in the calm window (dropping amcstock and Superstonk):

- incumbent-only drift = **+1,290%** (still ~13x), churn = **39.4%**.

The balloon survives. Even among channels that existed before the mania, total
activity grew about thirteenfold. This is import, not redistribution.

## Verdict

**CONTRADICTED at the basket scale.** During a documented mania the basket's total
submission activity expanded by far more than X = 15% (by ~14x), so aggregate
activity in this finance/meme ecosystem is NOT conserved. The "conserved total,
reshuffled mix" picture fails: the mix did churn (40%), but the total did not hold.
Under the pre-registered pass/fail rule for test (i), "net attention-minutes expand
by > X during >= 1 documented mania" is the explicit FAIL condition, and it is met
decisively.

## Scale caveat (carried, and load-bearing)

This does **not** by itself refute the GLOBAL sub-generational-budget claim, for two
honest reasons:

1. **Proxy, not minutes.** Submission count is an activity proxy. A 14x jump in
   posts need not be a 14x jump in attention-minutes (posts got shorter, lower-effort,
   and more numerous per active minute during the frenzy). The direction is not in
   doubt, but the magnitude in attention-minutes is an upper bound, not a measurement.

2. **A basket is not the economy.** This finance/meme basket is a tiny slice of the
   attention economy. A balloon here is exactly what the global claim PREDICTS if
   attention is conserved globally: a mania pulls minutes IN from outside the basket
   (other subreddits, other platforms, sleep, work) and dumps them onto GME. Local
   import is consistent with global conservation. So this result refutes conservation
   **at the ecosystem-basket scale** and leaves the global claim untested - it cannot
   be settled until the measurement spans the top-N platform total, as the
   pre-registration fixes for the lodged global frame.

What this run DOES establish, against the program's own framing: the basket-scale
fix proposed to rescue test (i) from the single-sub pilot does not rescue it. A
"basket of related subreddits" is still a porous, attention-importing region during a
mania - it behaves like the single subreddit did, just with more channels. The honest
read is that conservation only has a chance of holding at a genuinely closed
boundary (the whole platform ecosystem, ideally in attention-minutes), and every
scale below that will show import during a mania. The mania is, almost by
definition, the event that recruits attention from outside; a bounded basket will
always record that recruitment as a balloon.

## Files

- `FETCH_LOG.md`        - what was fetched / skipped from the torrent.
- `harvest_weekly.py`   - streams the 10 SUBMISSIONS .zst, builds weekly counts.
- `weekly_counts.json`  - per-sub weekly submission counts, 2020-06 .. 2021-07.
- `analyze.py`          - windows, drift, TV churn, incumbent-only control, figure.
- `result.json`         - machine-readable result.
- `figure_ecosystem.png`- stacked area of the basket + black BASKET TOTAL line,
                          calm and mania windows shaded.
