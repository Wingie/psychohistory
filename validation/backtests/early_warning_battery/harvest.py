#!/usr/bin/env py -3.12
"""
Harvest submission-count time series for the early-warning cascade battery.

Data source: Arctic Shift aggregation API (reddit.com and pullpush are
blocked/throttled; Arctic Shift is reachable). Endpoint:
    https://arctic-shift.photon-reddit.com/api/posts/search/aggregate
    ?aggregate=created_utc&frequency=month|week&subreddit=<s>&after=&before=&limit=100

Notes / hard-won facts (see also validation/temporal/data/_harvest_monthly.py):
  * The endpoint frequently returns HTTP 422 {"error":"Timeout. Maybe slow
    down a bit"} -- this is a SERVER-side aggregation timeout, not a parameter
    error. It clears with a longer client timeout + exponential backoff and by
    chunking the date range into small pieces (1 quarter for monthly, 1 month
    for weekly on busy subs like wallstreetbets).
  * Counts come back as strings; cast to int.
  * Bucket timestamps are ISO like "2022-01-31T23:00:00.000Z"; we key by the
    YYYY-MM-DD prefix and let the test script re-derive month/week.

Writes one JSON per series into data/<key>.json as a bare [["date",count],...]
list, plus a combined data/_all_series.json.
"""
import json, urllib.request, urllib.parse, sys, time, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)
BASE = "https://arctic-shift.photon-reddit.com/api/posts/search/aggregate"


def fetch(params, tries=8, timeout=240):
    url = BASE + "?" + urllib.parse.urlencode(params)
    for t in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 research/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read().decode()[:80]
            except Exception:
                pass
            sys.stderr.write(f"    HTTP{e.code} {body} try{t}\n"); sys.stderr.flush()
            time.sleep(5 + 4 * t)
        except Exception as e:
            sys.stderr.write(f"    {e} try{t}\n"); sys.stderr.flush()
            time.sleep(5 + 4 * t)
    return None


def month_chunks(start, end):
    """yield (after,before) one-month windows over [start,end)."""
    cur = start
    while cur < end:
        y, m = cur.year, cur.month + 1
        if m > 12:
            y, m = y + 1, 1
        nxt = datetime.date(y, m, 1)
        yield cur.isoformat(), min(nxt, end).isoformat()
        cur = nxt


def quarter_chunks(start, end):
    """yield (after,before) ~3-month windows over [start,end)."""
    cur = start
    while cur < end:
        y, m = cur.year, cur.month + 3
        while m > 12:
            y, m = y + 1, m - 12
        nxt = datetime.date(y, m, 1)
        yield cur.isoformat(), min(nxt, end).isoformat()
        cur = nxt


def harvest_series(key, subreddit, start, end, frequency, chunk):
    """Harvest one subreddit's count series; chunk='month'|'quarter'."""
    start = datetime.date.fromisoformat(start)
    end = datetime.date.fromisoformat(end)
    chunks = list(month_chunks(start, end) if chunk == "month" else quarter_chunks(start, end))
    merged = {}
    for a, b in chunks:
        d = fetch({"aggregate": "created_utc", "frequency": frequency,
                   "subreddit": subreddit, "after": a, "before": b, "limit": "100"})
        if d and d.get("data") is not None:
            for bk in d["data"]:
                merged[bk["created_utc"][:10]] = int(bk["count"])
            sys.stderr.write(f"  {key} {a}..{b}: +{len(d['data'])} buckets\n")
        else:
            sys.stderr.write(f"  {key} {a}..{b}: FAIL\n")
        sys.stderr.flush()
        time.sleep(2.5)
    series = sorted(merged.items())
    return [[k, v] for k, v in series]


# ---- ROSTER --------------------------------------------------------------
# (key, subreddit, harvest_start, harvest_end, frequency, chunk, onset, label)
# onset = labeled cascade onset date (YYYY-MM-DD). label = endogenous|exogenous.
# Date spans are chosen so the pre-onset lead window is a small fraction of the
# series and there is a long post/non-onset stretch for the base rate.
ROSTER = [
    # ---- ENDOGENOUS (framework predicts an early-warning rise) ----
    ("gme_wsb_weekly",   "wallstreetbets", "2020-06-01", "2021-07-01", "week",  "month",   "2021-01-25", "endogenous"),
    ("gme_wsb_monthly",  "wallstreetbets", "2019-01-01", "2022-07-01", "month", "quarter", "2021-01-01", "endogenous"),
    ("superstonk_2021",  "Superstonk",     "2021-03-01", "2022-06-01", "week",  "month",   "2021-06-01", "endogenous"),
    ("crypto_2021peak",  "CryptoCurrency", "2020-06-01", "2022-01-01", "month", "quarter", "2021-05-01", "endogenous"),
    ("crypto_luna2022",  "CryptoCurrency", "2021-06-01", "2023-01-01", "month", "quarter", "2022-05-01", "endogenous"),
    ("europe_energy2022","europe",         "2021-01-01", "2023-06-01", "month", "quarter", "2022-09-01", "endogenous"),
    ("wsb_aug2021_meme", "wallstreetbets", "2021-03-01", "2022-03-01", "month", "quarter", "2021-09-01", "endogenous"),
    # ---- EXOGENOUS controls (framework predicts NO early warning) ----
    ("askecon_infl2022", "AskEconomics",   "2020-06-01", "2023-06-01", "month", "quarter", "2022-02-01", "exogenous"),
    ("askecon_tariff25", "AskEconomics",   "2023-06-01", "2025-09-01", "month", "quarter", "2025-04-01", "exogenous"),
    ("europe_covid2020", "europe",         "2019-01-01", "2021-01-01", "month", "quarter", "2020-03-01", "exogenous"),
    ("crypto_ftx2022",   "CryptoCurrency", "2021-09-01", "2023-06-01", "month", "quarter", "2022-11-01", "exogenous"),
]


def main():
    only = set(sys.argv[1:])  # optional: harvest only these keys
    allser = {}
    for key, sub, s, e, freq, chunk, onset, label in ROSTER:
        if only and key not in only:
            continue
        sys.stderr.write(f"=== {key} ({sub}) {s}..{e} {freq} ===\n"); sys.stderr.flush()
        ser = harvest_series(key, sub, s, e, freq, chunk)
        path = os.path.join(DATA, key + ".json")
        json.dump(ser, open(path, "w"), indent=0)
        allser[key] = ser
        nz = sum(1 for _, c in ser if c > 0)
        rng = f"{ser[0][0]}..{ser[-1][0]}" if ser else "EMPTY"
        mx = max((c for _, c in ser), default=0)
        print(f"{key:20s} buckets={len(ser):3d} nonzero={nz:3d} {rng} max={mx}")
        sys.stdout.flush()
    # merge into combined file (preserve any already-harvested keys)
    combined_path = os.path.join(DATA, "_all_series.json")
    if os.path.exists(combined_path):
        try:
            prev = json.load(open(combined_path))
        except Exception:
            prev = {}
        prev.update(allser)
        allser = prev
    json.dump(allser, open(combined_path, "w"), indent=0)
    print(f"SAVED {combined_path} ({len(allser)} series)")


if __name__ == "__main__":
    main()
