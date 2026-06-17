# Labeled-cascade roster — early-warning battery

All series are **weekly submission-activity density** (posts/hour) for one
subreddit, harvested from the Arctic Shift **search** endpoint
(`/api/posts/search`) via an inverse-inter-arrival-time density proxy:
for each week start `t`, fetch the first ≤100 posts with `created_utc ≥ t`
sorted ascending; `activity = 100 / (last_ts − first_ts) × 3600`. Denser
posting ⇒ shorter span ⇒ higher value.

Why this proxy and not aggregate counts: the Arctic Shift **aggregate**
endpoint (`/api/posts/search/aggregate`) returns **all-zero** counts for
r/wallstreetbets in every era tested (2019/2021/2023) and frequently returns
HTTP 422 `"Timeout. Maybe slow down a bit"` for any subreddit under load — i.e.
it cannot serve the decisive GameStop case at all. The search endpoint returns
real post records reliably, so the whole battery uses one consistent method.

`label` = the framework's prediction:
- **endogenous** — self-reinforcing cascade ⇒ expect critical slowing down
  (rising variance + lag-1 autocorrelation) in the pre-onset window ⇒ AUC > 0.5.
- **exogenous** — externally-triggered shock / unexpected announcement ⇒ expect
  **no** early warning ⇒ AUC ≈ 0.5. These are the controls / the dissociation.

Onset dates and labels are **heuristic** and listed explicitly so they can be
challenged. EWS rolling window = 6 weeks for every event.

| key | subreddit | onset (week) | label | rationale |
|---|---|---|---|---|
| `gme_wsb_weekly` | r/wallstreetbets | 2021-01-25 | endogenous | **THE decisive case.** GameStop short squeeze; the canonical endogenous reflexive cascade (price↑→posts↑→price↑). |
| `superstonk_2021` | r/Superstonk | 2021-06-07 | endogenous | Superstonk (GME diaspora) June-2021 run-up; self-reinforcing "DD/HODL" community. |
| `crypto_2021peak` | r/CryptoCurrency | 2021-05-03 | endogenous | 2021 crypto bull-market blow-off top; reflexive mania. |
| `crypto_luna2022` | r/CryptoCurrency | 2022-05-09 | endogenous | Luna/UST death-spiral week; endogenous reflexive collapse (de-peg→panic→de-peg). |
| `europe_energy2022` | r/europe | 2022-09-05 | endogenous | Energy-crisis peak; prior work flags this as a known positive (AUC ≈ 0.87). Sanity check. |
| `wsb_meme_2021` | r/wallstreetbets | 2021-06-01 | endogenous | Mid-2021 AMC/meme-stock second wave on WSB; viral self-reinforcing surge. |
| `askecon_infl2022` | r/AskEconomics | 2022-02-07 | exogenous | Inflation-surge questions driven by external CPI prints; prior work flags as a known **null**. |
| `askecon_tariff25` | r/AskEconomics | 2025-04-07 | exogenous | 2025 tariff shock; externally-imposed policy announcement; known **null**. |
| `europe_covid2020` | r/europe | 2020-03-02 | exogenous | COVID lockdown shock — an exogenous unexpected announcement, not a community-internal build-up. |
| `crypto_ftx2022` | r/CryptoCurrency | 2022-11-07 | exogenous | FTX insolvency revelation (CoinDesk article → Binance tweet); a sudden external announcement, not a slow reflexive build-up. |

## Notes / honest limits on the roster
- **N is small** (6 endogenous, 4 exogenous) and several events share subreddits,
  so events are not fully independent.
- Some labels are arguable. FTX is treated as exogenous (the trigger was a leaked
  balance sheet + Binance announcement landing suddenly); one could argue an
  endogenous bank-run dynamic followed. Luna is treated as endogenous (the
  death-spiral is mechanically self-reinforcing). These choices are stated so a
  reviewer can flip them and re-run.
- r/AskEconomics is low-volume, so 100 posts span many days and the weekly
  density is **temporally smeared** — the proxy is coarsest exactly for the
  exogenous controls. Treat their AUCs as conservative/noisy.
