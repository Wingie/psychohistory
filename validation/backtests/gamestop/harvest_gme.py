#!/usr/bin/env py -3.12
"""
Harvest r/wallstreetbets daily ACTIVITY counts from pullpush.io, resilient to the
aggressive shared rate limit on the public deployment.

Design for rate limits:
  - Long fixed inter-request spacing (BASE_SPACING) so we stay under the limit
    instead of fighting it with bursty retries.
  - On 429: long linear cooldown (not exponential burst), then resume.
  - Checkpointing: every per-window dict is written to ./data/ as we go, and we
    skip windows already fully harvested on restart.

Primary method: aggs=created_utc (one request per ~month gives all daily counts).
Fallback: if aggs is unsupported (no 'aggs' key) we do a coarse DAILY count via the
  metadata.total_results field of a per-day query (size=0), one request per day.

Windows:
  cascade   2020-11-01 .. 2021-02-16
  baseline  2020-01-01 .. 2020-10-31
Series: submissions and comments.
"""
import urllib.request, urllib.error, json, time, os, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)

SUB = "wallstreetbets"
UA = {"User-Agent": "Mozilla/5.0 (academic CSD backtest; contact research)"}
BASE_SPACING = 11.0      # seconds between successful requests (stay polite)
COOLDOWN_429 = 70.0      # seconds to wait after a 429
MAX_429 = 40             # give up a single request after this many 429s

_last = [0.0]

def _space():
    dtm = time.time() - _last[0]
    if dtm < BASE_SPACING:
        time.sleep(BASE_SPACING - dtm)

def get(url):
    """One logical GET with rate-limit aware pacing. Returns parsed json or raises."""
    n429 = 0
    while True:
        _space()
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=120) as r:
                _last[0] = time.time()
                return json.load(r)
        except urllib.error.HTTPError as e:
            _last[0] = time.time()
            if e.code == 429:
                n429 += 1
                if n429 > MAX_429:
                    raise RuntimeError(f"429 wall after {MAX_429} tries: {url}")
                print(f"    429 ({n429}); cooldown {COOLDOWN_429:.0f}s", flush=True)
                time.sleep(COOLDOWN_429)
                continue
            if e.code in (500, 502, 503, 504):
                print(f"    {e.code}; cooldown 20s", flush=True)
                time.sleep(20)
                continue
            raise
        except Exception as e:
            print(f"    {type(e).__name__}: {e}; cooldown 20s", flush=True)
            time.sleep(20)

def epoch(d):
    return int(dt.datetime(d.year, d.month, d.day, tzinfo=dt.timezone.utc).timestamp())

def month_chunks(start, end):
    cur = start
    while cur < end:
        nxt = dt.date(cur.year + (cur.month == 12), (cur.month % 12) + 1, 1)
        yield cur, min(nxt, end)
        cur = min(nxt, end)

def try_aggs(kind, a, b):
    url = (f"https://api.pullpush.io/reddit/search/{kind}/"
           f"?subreddit={SUB}&after={a}&before={b}&size=0&aggs=created_utc")
    d = get(url)
    aggs = (d.get("aggs") or {}).get("created_utc")
    if not aggs:
        return None
    out = {}
    for bk in aggs:
        key = bk.get("key"); n = bk.get("doc_count", bk.get("count"))
        if key is None or n is None:
            continue
        day = dt.datetime.fromtimestamp(int(key), dt.timezone.utc).date().isoformat()
        out[day] = out.get(day, 0) + int(n)
    return out or None

def daily_count_fallback(kind, day):
    """metadata.total_results for a single day (size=0)."""
    a = epoch(day); b = epoch(day + dt.timedelta(days=1))
    url = (f"https://api.pullpush.io/reddit/search/{kind}/"
           f"?subreddit={SUB}&after={a}&before={b}&size=0")
    d = get(url)
    md = d.get("metadata") or {}
    tr = md.get("total_results")
    if tr is None:
        # last resort: count returned rows (capped at 100 -> floor)
        return len(d.get("data", [])), True
    return int(tr), False

def harvest(kind, label, start, end):
    out_path = os.path.join(DATA, f"{label}_{kind}.json")
    if os.path.exists(out_path):
        prev = json.load(open(out_path, encoding="utf-8"))
        if prev.get("complete"):
            print(f"  [skip] {label}_{kind} already complete", flush=True)
            return prev
    print(f"\n=== {label} {kind} {start}..{end} ===", flush=True)
    per_day, method, floor_days = {}, None, []
    # try aggs month by month first
    aggs_ok = True
    for cs, ce in month_chunks(start, end):
        print(f"  aggs chunk {cs}..{ce}", flush=True)
        try:
            agg = try_aggs(kind, epoch(cs), epoch(ce))
        except RuntimeError as e:
            print(f"    aggs request failed: {e}", flush=True)
            agg = None
        if agg is None:
            aggs_ok = False
            print("    -> aggs unsupported/empty; switching to daily fallback", flush=True)
            break
        method = "aggs"
        per_day.update(agg)
    if not aggs_ok:
        method = "daily_total_results"
        per_day = {}
        d = start
        while d < end:
            cnt, floored = daily_count_fallback(kind, d)
            per_day[d.isoformat()] = cnt
            if floored:
                floor_days.append(d.isoformat())
            if (d.day == 1) or (d - start).days % 10 == 0:
                print(f"    {d}: {cnt}", flush=True)
            # checkpoint mid-way
            json.dump({"method": method, "per_day": per_day, "complete": False,
                       "floor_days": floor_days},
                      open(out_path, "w", encoding="utf-8"), indent=2)
            d += dt.timedelta(days=1)
    res = {"method": method, "per_day": per_day, "complete": True,
           "floor_days": floor_days, "n_days": len(per_day),
           "total": sum(per_day.values())}
    json.dump(res, open(out_path, "w", encoding="utf-8"), indent=2)
    print(f"  -> {label}_{kind}: {len(per_day)} days, total {sum(per_day.values())} "
          f"(method={method}, floored_days={len(floor_days)})", flush=True)
    return res

def main():
    # initial cooldown to clear any active penalty window (long, to fully reset the
    # accumulated rate-limit penalty from earlier probes)
    print("initial cooldown 300s ...", flush=True)
    time.sleep(300)
    windows = [
        ("cascade", dt.date(2020, 11, 1), dt.date(2021, 2, 16)),
        ("baseline", dt.date(2020, 1, 1), dt.date(2020, 10, 31)),
    ]
    summary = {}
    for label, s, e in windows:
        for kind in ("submission", "comment"):
            r = harvest(kind, label, s, e)
            summary[f"{label}_{kind}"] = {"method": r["method"], "n_days": r["n_days"],
                                          "total": r["total"],
                                          "floor_days": len(r.get("floor_days", []))}
    json.dump(summary, open(os.path.join(DATA, "harvest_summary.json"), "w",
                            encoding="utf-8"), indent=2)
    print("\nHARVEST DONE", flush=True)
    print(json.dumps(summary, indent=2), flush=True)

if __name__ == "__main__":
    main()
