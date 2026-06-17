# Fetch log - conservation_ecosystem basket

Date: 2026-06-16. Source torrent: `validation/reddit_dump/reddit.torrent`
(academictorrents per-subreddit dump, 2005-06 .. 2024-12, total 3,050 GiB).
Tool: `aria2c --select-file=<idx> --seed-time=0 --max-concurrent-downloads=1
--max-connection-per-server=4 -d validation/reddit_dump <torrent>`.

Policy: SUBMISSIONS files only (far smaller than comments), bounded finance/meme
basket, low concurrency to avoid saturating the D: HDD.

## Fetched (SUBMISSIONS .zst only)

| subreddit       | torrent idx | size      | note |
|-----------------|-------------|-----------|------|
| wallstreetbets  | (prior run) | 546 MB    | already on disk; mania core |
| CryptoCurrency  | 10799       | 585 MB    | fetched this run |
| GME             | 17528       | 170 MB    | fetched this run |
| StockMarket     | 40816       | 63 MB     | fetched this run |
| Superstonk      | 41360       | 498 MB    | fetched this run (born during mania) |
| amcstock        | 49236       | 201 MB    | fetched this run (born during mania) |
| investing       | 62084       | 98 MB     | fetched this run |
| options         | 67983       | 38 MB     | fetched this run |
| pennystocks     | 68588       | 71 MB     | fetched this run |
| stocks          | 73852       | 94 MB     | fetched this run |

New download this run: ~1.8 GiB across 9 files (avg 14 MiB/s). All verified on disk.

## Skipped on purpose

- ALL `*_comments.zst` files - the comments dumps are 5-15x larger (wallstreetbets
  comments alone is 7.1 GB vs 546 MB submissions). Submission count is sufficient
  as the weekly activity proxy for this test and keeps HDD I/O bounded.
- Niche / derivative meme subs visible in the file list but outside the frozen
  basket: DDintoGME, DRSyourGME, MemeStockMarket, Wallstreetbetsnew,
  WallStreetbetsELITE, wallstreetbetsOGs, WallStreetBetsCrypto, SafeMoonInvesting,
  Pepecryptocurrency, etc. Adding the long tail of newborn spinoffs would only
  amplify the import signal (more new channels), so the chosen basket is the
  conservative core, not a cherry-pick toward the result.
- Regional / off-topic collisions: IndianStockMarket, UKInvesting, ValueInvesting,
  realestateinvesting, PokeInvesting, Canadapennystocks - out of the US-equity
  meme-mania ecosystem under test.

The 10-sub basket is: wallstreetbets, investing, stocks, StockMarket, options,
pennystocks, CryptoCurrency, GME, amcstock, Superstonk.
