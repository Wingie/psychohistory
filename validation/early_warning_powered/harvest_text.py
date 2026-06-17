"""Falsifier (iii) POWERED early-warning harvest.

Stream the WSB *submissions* .zst exactly ONCE and capture submission TEXT
(title + selftext) for every submission that falls inside any roster harvest
window. We harvest:

  * EVENT pre-onset windows   [onset - PRE_DAYS, onset)        (one per roster event)
  * matched-CALM windows      [calm_onset - PRE_DAYS, calm_onset)  (Boettiger guard-banded null)

The dump is chronologically ordered by created_utc, so we stop early once the
stream passes the last needed window end. Never fully decompresses the 546 MB file.

Output (validation/early_warning_powered/data/):
  - <label>__<arm>.jsonl : compact submission per line
                           {"id","t":created_utc,"title","self":selftext,"flair"}
  - harvest_meta.json    : per-window counts + bounds

Run:  py -3.12 harvest_text.py    (resumable; exits fast if all files present)
"""
import io
import json
import os
import sys
import datetime as dt

import zstandard

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
ROSTER = os.path.abspath(os.path.join(HERE, "..", "reddit_wsb"))
sys.path.insert(0, ROSTER)
import roster_wsb as R  # noqa: E402

ZST = os.path.abspath(os.path.join(
    HERE, "..", "reddit_dump", "reddit", "subreddits24",
    "wallstreetbets_submissions.zst"))

# Pre-onset embedding window. We use a 60-day pre-onset window: long enough to
# give the daily semantic-variance CSD detector >=8 buckets with >=4 posts/bucket
# (WSB submission volume is ample), short enough to stay inside a single regime.
PRE_DAYS = 60
DROP_AUTHORS = {"AutoModerator", "[deleted]", "[removed]", None, ""}


def windows():
    """List of (label, arm, lo_date, hi_date, out_path).

    arm = 'event'  -> pre-onset window ending at the roster onset
    arm = 'calm'   -> pre-onset window ending at onset - CALM_OFFSET_DAYS (guard-banded null)
    """
    out = []
    for label, onset_iso, _why in R.EVENTS:
        o = dt.date.fromisoformat(onset_iso)
        lo = o - dt.timedelta(days=PRE_DAYS)
        out.append((label, "event", lo, o,
                    os.path.join(DATA, f"{label}__event.jsonl")))
        c = dt.date.fromisoformat(R.calm_onset(onset_iso))
        clo = c - dt.timedelta(days=PRE_DAYS)
        out.append((label, "calm", clo, c,
                    os.path.join(DATA, f"{label}__calm.jsonl")))
    return out


def main():
    os.makedirs(DATA, exist_ok=True)
    ws = windows()
    meta_path = os.path.join(DATA, "harvest_meta.json")
    if all(os.path.exists(w[4]) for w in ws) and os.path.exists(meta_path):
        sys.stderr.write("all window files + harvest_meta.json present; nothing to do.\n")
        return

    min_lo = min(w[2] for w in ws)
    max_hi = max(w[3] for w in ws)
    min_lo_ts = int(dt.datetime(min_lo.year, min_lo.month, min_lo.day,
                                tzinfo=dt.timezone.utc).timestamp())
    max_hi_ts = int(dt.datetime(max_hi.year, max_hi.month, max_hi.day,
                                tzinfo=dt.timezone.utc).timestamp())
    sys.stderr.write(f"harvest window [{min_lo} .. {max_hi}) -> ts [{min_lo_ts}..{max_hi_ts})\n")
    sys.stderr.write(f"{len(ws)} windows ({len(ws)//2} events x event+calm)\n")

    writers = {}
    counts = {}
    for label, arm, lo, hi, path in ws:
        writers[(label, arm)] = (lo, hi, open(path, "w", encoding="utf-8"))
        counts[f"{label}__{arm}"] = 0

    dctx = zstandard.ZstdDecompressor(max_window_size=2 ** 31)
    n_lines = n_kept = 0
    with open(ZST, "rb") as fh:
        reader = dctx.stream_reader(fh)
        tr = io.TextIOWrapper(reader, encoding="utf-8", errors="ignore")
        for line in tr:
            n_lines += 1
            if n_lines % 1_000_000 == 0:
                sys.stderr.write(f"  ..{n_lines:,} lines, kept {n_kept:,}\n")
            try:
                o = json.loads(line)
            except Exception:
                continue
            ts = o.get("created_utc")
            if ts is None:
                continue
            try:
                ts = int(ts)
            except Exception:
                continue
            if ts < min_lo_ts:
                continue
            if ts >= max_hi_ts:
                break  # ordered stream, past everything we need
            author = o.get("author")
            if author in DROP_AUTHORS:
                continue
            title = (o.get("title") or "").strip()
            self_ = (o.get("selftext") or "").strip()
            if self_ in ("[deleted]", "[removed]"):
                self_ = ""
            if len((title + " " + self_).strip()) < 12:
                continue
            d = dt.datetime.fromtimestamp(ts, dt.timezone.utc).date()
            rec = None
            for key, (lo, hi, w) in writers.items():
                if lo <= d < hi:
                    if rec is None:
                        rec = json.dumps(
                            {"id": o.get("id", str(ts)), "t": ts,
                             "title": title[:1000], "self": self_[:2000],
                             "flair": o.get("link_flair_text")},
                            separators=(",", ":"), ensure_ascii=False)
                    w.write(rec)
                    w.write("\n")
                    counts[f"{key[0]}__{key[1]}"] += 1
                    n_kept += 1
    for (lo, hi, w) in writers.values():
        w.close()
    meta = dict(pre_days=PRE_DAYS, n_lines_scanned=n_lines, n_kept=n_kept,
                counts=counts,
                bounds=[str(min_lo), str(max_hi)])
    json.dump(meta, open(meta_path, "w"), indent=2)
    sys.stderr.write(f"DONE. scanned {n_lines:,} lines, wrote {n_kept:,} rows.\n")
    for k, v in sorted(counts.items()):
        sys.stderr.write(f"  {k:32s} {v}\n")


if __name__ == "__main__":
    main()
