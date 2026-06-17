"""Stream the WSB comments .zst once; (a) build a daily comment-volume histogram
(to corroborate onset selection honestly) and (b) capture the compact fields
(author, link_id, created_utc) for every comment that falls inside ANY roster run's
harvest window. Resumable + memory-light (streaming, never decompresses the whole
7.1 GB file).

Output (validation/reddit_wsb/data/):
  - volume_scan.json            : {date_iso: comment_count} for the whole stream
  - <label>__<arm>.jsonl        : one compact comment per line for that run's window
                                  ({"a":author,"l":link_id,"t":created_utc})

The dump is chronologically ordered by created_utc, so once the stream passes the
LAST needed window end we stop early. AutoModerator / [deleted] authors are dropped
at harvest time (they cannot be graph nodes).

Run:  py -3.12 harvest_filter.py
Resumable: if all per-run .jsonl files + volume_scan.json already exist, exits fast.
"""
import io
import json
import os
import sys
import datetime as dt
from collections import defaultdict

import zstandard

import roster_wsb as R

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
ZST = os.path.abspath(os.path.join(
    HERE, "..", "reddit_dump", "reddit", "subreddits24", "wallstreetbets_comments.zst"))

DROP_AUTHORS = {"AutoModerator", "[deleted]", "[removed]", None, ""}


def run_windows():
    """List of (label, arm, lo_date, hi_date, out_path)."""
    out = []
    for label, onset, arm in R.all_runs():
        lo, hi = R.window_for(onset)
        out.append((label, arm, lo, hi, os.path.join(DATA, f"{label}__{arm}.jsonl")))
    return out


def main():
    os.makedirs(DATA, exist_ok=True)
    windows = run_windows()
    vol_path = os.path.join(DATA, "volume_scan.json")

    done = all(os.path.exists(w[4]) for w in windows) and os.path.exists(vol_path)
    if done:
        sys.stderr.write("all run files + volume_scan.json already present; nothing to do.\n")
        return

    # global harvest bounds: only inspect comments inside [min_lo, max_hi)
    min_lo = min(w[2] for w in windows)
    max_hi = max(w[3] for w in windows)
    min_lo_ts = int(dt.datetime(min_lo.year, min_lo.month, min_lo.day,
                                tzinfo=dt.timezone.utc).timestamp())
    max_hi_ts = int(dt.datetime(max_hi.year, max_hi.month, max_hi.day,
                                tzinfo=dt.timezone.utc).timestamp())
    sys.stderr.write(f"harvest window [{min_lo} .. {max_hi}) -> ts [{min_lo_ts}..{max_hi_ts})\n")
    sys.stderr.write(f"{len(windows)} run windows\n")

    # open all per-run writers
    writers = {}
    for label, arm, lo, hi, path in windows:
        writers[(label, arm)] = (lo, hi, open(path, "w", encoding="utf-8"))

    daily = defaultdict(int)
    dctx = zstandard.ZstdDecompressor(max_window_size=2 ** 31)
    n_seen = n_kept = n_lines = 0
    with open(ZST, "rb") as fh:
        reader = dctx.stream_reader(fh)
        tr = io.TextIOWrapper(reader, encoding="utf-8", errors="ignore")
        for line in tr:
            n_lines += 1
            if n_lines % 2_000_000 == 0:
                sys.stderr.write(f"  ..{n_lines:,} lines, kept {n_kept:,}\n")
                for _, _, _, _, _ in []:
                    pass
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
                # ordered stream -> we're past everything we need
                break
            d = dt.datetime.fromtimestamp(ts, dt.timezone.utc).date()
            daily[d.isoformat()] += 1
            n_seen += 1
            author = c.get("author")
            if author in DROP_AUTHORS:
                continue
            link = c.get("link_id")
            if not link:
                continue
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
    json.dump(dict(sorted(daily.items())), open(vol_path, "w"), indent=0)
    sys.stderr.write(f"DONE. scanned {n_lines:,} lines, {n_seen:,} in-range, "
                     f"wrote {n_kept:,} run-rows across {len(windows)} files.\n")


if __name__ == "__main__":
    main()
