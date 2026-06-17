"""reharvest_text.py  (L2 data-acquisition operator)

The v0.2 WSB/GME series stored only a scalar density proxy (no text/author). To
feed the semantic-CSD detector (OBJ 1) the marquee endogenous cascade, re-pull a
SAMPLE of r/wallstreetbets post titles+selftext around the Jan-2021 onset from the
Arctic Shift SEARCH endpoint (arctic-shift.photon-reddit.com), which returns text
+ author (capped ~100/query). Several day-bucketed queries are stitched to span
the approach window.

Writes wsb_text_harvest.json (list of post records). If the host is unreachable
(it has been blocked in this environment before), the script exits cleanly and
semantic_csd.py falls back to AskEconomics-only with the GME case marked pending.
"""
import json
import os
import sys
import time
import datetime as dt
import urllib.request
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "wsb_text_harvest.json")
BASE = "https://arctic-shift.photon-reddit.com/api/posts/search"


def epoch(d):
    return int(dt.datetime(d.year, d.month, d.day).timestamp())


def query(after, before, limit=100):
    params = dict(subreddit="wallstreetbets", after=after, before=before,
                  limit=limit, sort="desc")
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "psychohistory-v03/1.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode("utf-8"))


def harvest():
    # daily windows across the GME approach + onset (2020-12-20 .. 2021-02-07)
    start = dt.date(2020, 12, 20)
    end = dt.date(2021, 2, 7)
    recs, seen = [], set()
    d = start
    while d < end:
        nxt = d + dt.timedelta(days=2)
        try:
            resp = query(epoch(d), epoch(nxt))
            data = resp.get("data", resp if isinstance(resp, list) else [])
            for o in data:
                pid = o.get("id")
                if pid and pid in seen:
                    continue
                if pid:
                    seen.add(pid)
                recs.append(dict(id=pid, created_utc=o.get("created_utc"),
                                 title=o.get("title"), selftext=o.get("selftext"),
                                 author=o.get("author")))
            print(f"  {d}..{nxt}: +{len(data)} (total {len(recs)})")
        except Exception as e:
            print(f"  {d}: ERROR {e}", file=sys.stderr)
            return None
        d = nxt
        time.sleep(0.6)
    return recs


if __name__ == "__main__":
    print("Harvesting r/wallstreetbets text around 2021-01 onset from Arctic Shift...")
    recs = harvest()
    if recs is None or len(recs) < 20:
        print("HARVEST FAILED or too few records; GME semantic case stays PENDING.",
              file=sys.stderr)
        sys.exit(1)
    # keep only records with usable text
    recs = [r for r in recs if (r.get("title") or r.get("selftext")) and r.get("created_utc")]
    json.dump(recs, open(OUT, "w"), indent=1)
    print(f"WROTE {len(recs)} WSB posts -> {OUT}")
