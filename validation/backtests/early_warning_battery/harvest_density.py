#!/usr/bin/env py -3.12
"""
Density-proxy harvester for subreddits the Arctic Shift AGGREGATE endpoint
cannot serve (notably r/wallstreetbets, which returns all-zero aggregate counts
and/or server-side 422 'Timeout' for every era -- a coverage/scale gap in the
aggregator). The SEARCH endpoint, however, returns real post records fast.

METHOD (submission-activity proxy, weekly):
    For each week start t, request the first up-to-100 posts with created_utc>=t,
    sorted ascending, fields=created_utc only. The 100 posts span some number of
    seconds; activity = 100 / span (posts per hour). Denser posting => shorter
    span => higher proxy value. This is an *inverse-inter-arrival-time* density
    estimate -- a monotone proxy for submission rate, NOT an absolute count.

    Validated by hand on r/wallstreetbets across the GME timeline:
      2020-09 ~19/hr (calm) -> 2020-12-28 ~38 -> 2021-01-18 ~61 ->
      2021-01-25 ~151 (squeeze) -> 2021-02-08 ~248. Tracks the cascade cleanly.

Writes data/<key>.json as [["week_start", posts_per_hour], ...].
"""
import json, urllib.request, urllib.parse, sys, time, os, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)
BASE = "https://arctic-shift.photon-reddit.com/api/posts/search"


def fetch(params, tries=6, timeout=90):
    url = BASE + "?" + urllib.parse.urlencode(params)
    for t in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 research/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            try:
                body = e.read().decode()[:60]
            except Exception:
                body = ""
            sys.stderr.write(f"    HTTP{e.code} {body} try{t}\n"); sys.stderr.flush()
            time.sleep(3 + 3 * t)
        except Exception as e:
            sys.stderr.write(f"    {e} try{t}\n"); sys.stderr.flush()
            time.sleep(3 + 3 * t)
    return None


def week_density(sub, week_start_date):
    after = int(datetime.datetime(week_start_date.year, week_start_date.month,
                                  week_start_date.day, tzinfo=datetime.timezone.utc).timestamp())
    d = fetch({"subreddit": sub, "after": str(after), "limit": "100",
               "sort": "asc", "fields": "created_utc"})
    if not d or not d.get("data"):
        return None
    ts = sorted(float(r["created_utc"]) for r in d["data"])
    n = len(ts)
    if n < 5:
        return None
    span = ts[-1] - ts[0]
    if span <= 0:
        return None
    return n / span * 3600.0  # posts per hour


def harvest(key, sub, start, end):
    start = datetime.date.fromisoformat(start)
    end = datetime.date.fromisoformat(end)
    out = []
    cur = start
    while cur < end:
        v = week_density(sub, cur)
        if v is not None:
            out.append([cur.isoformat(), round(v, 4)])
            sys.stderr.write(f"  {key} {cur}: {v:.1f}/hr\n")
        else:
            sys.stderr.write(f"  {key} {cur}: NONE\n")
        sys.stderr.flush()
        cur = cur + datetime.timedelta(days=7)
        time.sleep(1.2)
    path = os.path.join(DATA, key + ".json")
    json.dump(out, open(path, "w"), indent=0)
    nz = sum(1 for _, c in out if c > 0)
    print(f"{key:20s} weeks={len(out):3d} nonzero={nz:3d} "
          f"{out[0][0] if out else '-'}..{out[-1][0] if out else '-'}")
    return out


# key, subreddit, start, end  (weekly density)
# Full battery harvested via the SEARCH/density proxy because the AGGREGATE
# endpoint is unreliable (all-zero for wallstreetbets; global 422 timeouts under
# load). Using one consistent method across every event is also methodologically
# cleaner. Spans put the pre-onset lead window as a small fraction of the series
# and leave a long non-onset stretch for the base-rate null.
JOBS = {
    # ---- ENDOGENOUS ----
    "gme_wsb_weekly":    ("wallstreetbets", "2020-06-01", "2021-07-01"),
    "superstonk_2021":   ("Superstonk",     "2021-03-01", "2022-06-01"),
    "crypto_2021peak":   ("CryptoCurrency", "2020-08-01", "2022-01-01"),
    "crypto_luna2022":   ("CryptoCurrency", "2021-08-01", "2023-01-01"),
    "europe_energy2022": ("europe",         "2021-06-01", "2023-06-01"),
    "wsb_meme_2021":     ("wallstreetbets", "2021-03-01", "2022-03-01"),
    # ---- EXOGENOUS ----
    "askecon_infl2022":  ("AskEconomics",   "2021-01-01", "2023-06-01"),
    "askecon_tariff25":  ("AskEconomics",   "2024-01-01", "2025-12-01"),
    "europe_covid2020":  ("europe",         "2019-06-01", "2021-01-01"),
    "crypto_ftx2022":    ("CryptoCurrency", "2022-02-01", "2023-08-01"),
}


def main():
    only = set(sys.argv[1:])
    for key, (sub, s, e) in JOBS.items():
        if only and key not in only:
            continue
        sys.stderr.write(f"=== {key} ({sub}) {s}..{e} weekly density ===\n"); sys.stderr.flush()
        harvest(key, sub, s, e)
        sys.stdout.flush()


if __name__ == "__main__":
    main()
