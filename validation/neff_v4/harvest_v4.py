"""Stream wallstreetbets_comments.zst ONCE (sequential; D: is an HDD) and capture
the compact comment fields (author, link_id, created_utc) for every comment that
falls inside ANY v4 FRESH-event window (roster_v4.py). v4 has NO calm/clean arm: the
PRIMARY specificity null is the per-event block-label shuffle computed in analysis.

Output (validation/neff_v4/data/):
  - event__<label>.jsonl   one compact comment per line ({"a":author,"l":link_id,"t":ts})

Resumable: if every target file already exists, exits fast.
Adapted verbatim from validation/neff_v3/harvest_v3.py (same streaming, same
DROP_AUTHORS, same early-stop on the ordered stream).

Run:  py -3.12 harvest_v4.py
"""
import io
import json
import os
import sys
import datetime as dt

import zstandard

import roster_v4 as RV

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
ZST = os.path.abspath(os.path.join(
    HERE, "..", "reddit_dump", "reddit", "subreddits24", "wallstreetbets_comments.zst"))

DROP_AUTHORS = {"AutoModerator", "[deleted]", "[removed]", None, ""}


def all_windows():
    """List of (label, lo_date, hi_date, out_path)."""
    out = []
    for label, onset, _why in RV.all_events():
        lo, hi = RV.window_for(onset)
        out.append((label, lo, hi, os.path.join(DATA, f"event__{label}.jsonl")))
    return out


def main():
    os.makedirs(DATA, exist_ok=True)
    windows = all_windows()
    if all(os.path.exists(w[3]) for w in windows):
        sys.stderr.write("all v4 window files already present; nothing to do.\n")
        return

    min_lo = min(w[1] for w in windows)
    max_hi = max(w[2] for w in windows)
    min_lo_ts = int(dt.datetime(min_lo.year, min_lo.month, min_lo.day,
                                tzinfo=dt.timezone.utc).timestamp())
    max_hi_ts = int(dt.datetime(max_hi.year, max_hi.month, max_hi.day,
                                tzinfo=dt.timezone.utc).timestamp())
    sys.stderr.write(f"harvest window [{min_lo} .. {max_hi}) -> ts [{min_lo_ts}..{max_hi_ts})\n")
    sys.stderr.write(f"{len(windows)} v4 event windows\n")

    writers = {}
    for label, lo, hi, path in windows:
        writers[label] = (lo, hi, open(path, "w", encoding="utf-8"))

    dctx = zstandard.ZstdDecompressor(max_window_size=2 ** 31)
    n_lines = n_kept = 0
    with open(ZST, "rb") as fh:
        reader = dctx.stream_reader(fh)
        tr = io.TextIOWrapper(reader, encoding="utf-8", errors="ignore")
        for line in tr:
            n_lines += 1
            if n_lines % 5_000_000 == 0:
                sys.stderr.write(f"  ..{n_lines:,} lines, kept {n_kept:,}\n")
            try:
                c = json.loads(line)
            except Exception:
                continue
            ts = c.get("created_utc")
            if ts is None:
                continue
            try:
                ts = int(ts)
            except Exception:
                continue
            if ts < min_lo_ts:
                continue
            if ts >= max_hi_ts:
                break  # ordered stream -> past everything we need
            author = c.get("author")
            if author in DROP_AUTHORS:
                continue
            link = c.get("link_id")
            if not link:
                continue
            d = dt.datetime.fromtimestamp(ts, dt.timezone.utc).date()
            rec = None
            for (lo, hi, w) in writers.values():
                if lo <= d < hi:
                    if rec is None:
                        rec = json.dumps({"a": author, "l": link, "t": ts},
                                         separators=(",", ":"))
                    w.write(rec)
                    w.write("\n")
                    n_kept += 1
    for (lo, hi, w) in writers.values():
        w.close()
    sys.stderr.write(f"DONE. scanned {n_lines:,} lines, wrote {n_kept:,} rows "
                     f"across {len(windows)} files.\n")


if __name__ == "__main__":
    main()
