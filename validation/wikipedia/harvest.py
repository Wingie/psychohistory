"""Wikimedia harvester for the dynamic-N_eff-collapse test (test ii').

Pulls, per frozen roster run (event + matched-calm arms):
  - focal-article revisions (user, timestamp) over [onset-BASELINE, onset+POST]
  - for the pre-onset editors of that article, their main-namespace contributions
    over [onset-BASELINE, onset) -> the editor co-editing graph substrate.

Public Wikimedia API only (prop=revisions, list=usercontribs). No throttle wall, no
torrent. stdlib urllib (no extra deps). Polite User-Agent + small sleep. Resumable:
skips runs already cached in data/.

Run:  py -3.12 harvest.py
"""
import json
import os
import sys
import time
import datetime as dt
import urllib.request
import urllib.parse

import roster as R

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)

API = "https://en.wikipedia.org/w/api.php"
UA = "psychohistory-research/0.1 (academic validation; contact wingston.sharon@gmail.com)"
SLEEP = 0.10
N_CALLS = [0]


def _get(params):
    params = dict(params); params["format"] = "json"; params["formatversion"] = 2
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                N_CALLS[0] += 1
                time.sleep(SLEEP)
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:
            time.sleep(1.0 + attempt)
            if attempt == 4:
                sys.stderr.write(f"  ! API fail: {e}\n")
                return {}
    return {}


def iso(d):
    return d.strftime("%Y-%m-%dT%H:%M:%SZ")


def focal_revisions(title, start_newer, end_older):
    """All (user, timestamp) revisions of `title` in (end_older, start_newer]."""
    revs, cont = [], None
    while True:
        p = dict(action="query", prop="revisions", titles=title, redirects=1,
                 rvprop="timestamp|user", rvlimit="max", rvdir="older",
                 rvstart=iso(start_newer), rvend=iso(end_older))
        if cont:
            p["rvcontinue"] = cont
        d = _get(p)
        pages = (d.get("query", {}) or {}).get("pages", [])
        for pg in pages:
            for rv in pg.get("revisions", []) or []:
                u = rv.get("user")
                if u and not rv.get("userhidden"):
                    revs.append({"user": u, "ts": rv.get("timestamp")})
        cont = (d.get("continue", {}) or {}).get("rvcontinue")
        if not cont:
            break
    return revs


def user_contribs(user, start_newer, end_older, uclimit=500):
    """Main-namespace (ns0) article titles `user` edited in (end_older, start_newer].
    Single page (uclimit up to 500); truncation for hyper-active editors is logged."""
    p = dict(action="query", list="usercontribs", ucuser=user, ucnamespace=0,
             ucprop="title|timestamp", uclimit=uclimit, ucdir="older",
             ucstart=iso(start_newer), ucend=iso(end_older))
    d = _get(p)
    out = [{"title": c.get("title"), "ts": c.get("timestamp")}
           for c in (d.get("query", {}) or {}).get("usercontribs", []) or []]
    truncated = len(out) >= uclimit
    return out, truncated


def slug(title, onset, arm):
    s = "".join(ch if ch.isalnum() else "_" for ch in title)
    return f"{s}__{onset}__{arm}.json"


def harvest_run(title, onset_iso, arm):
    path = os.path.join(DATA, slug(title, onset_iso, arm))
    if os.path.exists(path):
        sys.stderr.write(f"  skip (cached) {title} [{arm}] {onset_iso}\n")
        return json.load(open(path, encoding="utf-8"))

    onset = dt.date.fromisoformat(onset_iso)
    base_start = dt.datetime.combine(onset - dt.timedelta(days=R.BASELINE_DAYS), dt.time())
    onset_dtm = dt.datetime.combine(onset, dt.time())
    post_end = dt.datetime.combine(onset + dt.timedelta(days=R.POST_DAYS), dt.time())

    sys.stderr.write(f"  harvest {title} [{arm}] onset={onset_iso} ...\n")
    # focal revisions over full [base_start, post_end]
    revs = focal_revisions(title, post_end, base_start)

    # pre-onset editors (active in [base_start, onset)) ranked by edit count
    pre_counts = {}
    for rv in revs:
        ts = rv["ts"]
        if ts and ts < iso(onset_dtm):
            pre_counts[rv["user"]] = pre_counts.get(rv["user"], 0) + 1
    editors = [u for u, _ in sorted(pre_counts.items(), key=lambda kv: -kv[1])]
    cap_hit = len(editors) > R.EDITOR_CAP
    editors = editors[:R.EDITOR_CAP]

    # each editor's co-editing footprint in the pre-onset window
    contribs, n_trunc = {}, 0
    for i, u in enumerate(editors):
        c, tr = user_contribs(u, onset_dtm, base_start)
        contribs[u] = c
        n_trunc += int(tr)
        if (i + 1) % 25 == 0:
            sys.stderr.write(f"    .. {i+1}/{len(editors)} editors, {N_CALLS[0]} calls\n")

    rec = dict(title=title, onset=onset_iso, arm=arm,
               params=dict(baseline_days=R.BASELINE_DAYS, post_days=R.POST_DAYS,
                           editor_cap=R.EDITOR_CAP),
               focal_revs=revs, pre_onset_editors=editors,
               editor_cap_hit=cap_hit, n_editors=len(editors),
               n_contrib_truncated=n_trunc, editor_contribs=contribs,
               n_api_calls=N_CALLS[0])
    json.dump(rec, open(path, "w", encoding="utf-8"))
    sys.stderr.write(f"    saved {path}  (revs={len(revs)} editors={len(editors)} "
                     f"cap_hit={cap_hit} trunc={n_trunc})\n")
    return rec


def main():
    runs = list(R.all_runs())
    sys.stderr.write(f"harvesting {len(runs)} runs ({len(R.EVENTS)} articles x event+calm)\n")
    for title, onset_iso, arm in runs:
        try:
            harvest_run(title, onset_iso, arm)
        except Exception as e:
            sys.stderr.write(f"  !! run failed {title}[{arm}]: {e}\n")
    sys.stderr.write(f"DONE. total API calls={N_CALLS[0]}\n")


if __name__ == "__main__":
    main()
