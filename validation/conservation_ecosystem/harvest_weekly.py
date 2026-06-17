"""Ecosystem-scale conservation test (pre-registration test (i)) - harvest step.

Stream each finance/meme-basket SUBMISSIONS .zst once and build a weekly
submission-count series per subreddit over 2020-06-01 .. 2021-07-04 (spanning
the Jan-2021 GME mania). Submission counts are an ACTIVITY PROXY for attention
minutes, not a direct measure.

We do NOT early-break on time order: the per-subreddit submission dumps are only
approximately chronological, and a wrong early-break would silently truncate
counts. Each file is fully streamed once (submissions are far smaller than
comments). Memory-light: never decompresses the whole file.

Output (validation/conservation_ecosystem/):
  - weekly_counts.json : {subreddit: {week_iso_monday: count}}  (only weeks in range)

Run:  py -3.12 harvest_weekly.py
Resumable: if weekly_counts.json exists, exits fast.
"""
import io
import json
import os
import sys
import datetime as dt
from collections import defaultdict

import zstandard

HERE = os.path.dirname(os.path.abspath(__file__))
ZDIR = os.path.abspath(os.path.join(HERE, "..", "reddit_dump", "reddit", "subreddits24"))
OUT = os.path.join(HERE, "weekly_counts.json")

# The frozen basket (a finance/meme co-engagement basket). WSB is the mania core;
# the rest are the related subs across which attention can redistribute.
BASKET = [
    "wallstreetbets",
    "investing",
    "stocks",
    "StockMarket",
    "options",
    "pennystocks",
    "CryptoCurrency",
    "GME",
    "amcstock",
    "Superstonk",
]

# Analysis span: 2020-06-01 .. 2021-07-04 (inclusive of the week boundaries).
LO = dt.date(2020, 6, 1)
HI = dt.date(2021, 7, 5)  # exclusive upper bound
LO_TS = int(dt.datetime(LO.year, LO.month, LO.day, tzinfo=dt.timezone.utc).timestamp())
HI_TS = int(dt.datetime(HI.year, HI.month, HI.day, tzinfo=dt.timezone.utc).timestamp())


def week_monday(d: dt.date) -> str:
    """ISO week label = the Monday of that week, as YYYY-MM-DD."""
    monday = d - dt.timedelta(days=d.weekday())
    return monday.isoformat()


def scan_one(sub: str) -> dict:
    path = os.path.join(ZDIR, f"{sub}_submissions.zst")
    counts = defaultdict(int)
    dctx = zstandard.ZstdDecompressor(max_window_size=2 ** 31)
    n_lines = n_inrange = 0
    with open(path, "rb") as fh:
        reader = dctx.stream_reader(fh)
        tr = io.TextIOWrapper(reader, encoding="utf-8", errors="ignore")
        for line in tr:
            n_lines += 1
            if n_lines % 1_000_000 == 0:
                sys.stderr.write(f"  [{sub}] ..{n_lines:,} lines, {n_inrange:,} in-range\n")
            # cheap pre-filter before JSON parse: created_utc must be present
            try:
                obj = json.loads(line)
            except Exception:
                continue
            ts = obj.get("created_utc")
            if ts is None:
                continue
            try:
                ts = int(ts)
            except Exception:
                continue
            if ts < LO_TS or ts >= HI_TS:
                continue
            d = dt.datetime.fromtimestamp(ts, dt.timezone.utc).date()
            counts[week_monday(d)] += 1
            n_inrange += 1
    sys.stderr.write(f"[{sub}] DONE: {n_lines:,} lines, {n_inrange:,} in-range "
                     f"({len(counts)} weeks)\n")
    return dict(sorted(counts.items()))


def main():
    if os.path.exists(OUT):
        sys.stderr.write("weekly_counts.json already present; nothing to do.\n")
        return
    result = {}
    for sub in BASKET:
        path = os.path.join(ZDIR, f"{sub}_submissions.zst")
        if not os.path.exists(path):
            sys.stderr.write(f"!! MISSING {path}; skipping {sub}\n")
            continue
        sys.stderr.write(f"scanning {sub} ...\n")
        result[sub] = scan_one(sub)
    json.dump(result, open(OUT, "w"), indent=1)
    sys.stderr.write(f"wrote {OUT} ({len(result)} subs)\n")


if __name__ == "__main__":
    main()
