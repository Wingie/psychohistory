"""Frozen selection of CLEAN (genuinely-quiet) WSB pseudo-onset windows for the
v3 clean-null distribution. Deterministic, committed BEFORE the fresh roster is
harvested or analyzed.

A clean window is a pseudo-onset date c such that:
  * the full collapse span [c-90d, c+22d] lies inside the continuous daily volume
    record we have (2019-10-28 .. 2024-08-26);
  * the 21-day onset stretch [c-3d, c+22d] does NOT overlap any EXCLUDED known-event
    date (the 10 original WSB onsets + the macro event list below, each padded);
  * the 21-day onset stretch's mean daily comment volume is in the LOWER HALF of the
    WSB volume distribution for its ERA (calendar year), i.e. genuinely quiet for
    its time -- this is the contamination fix: we never compare against a window
    that sits inside a mania.

We then take >=12 such windows spread across 2019-2024 (greedy: lowest-volume-first,
enforcing a minimum 45-day separation between picks so they are quasi-independent).

This module exposes:
  EXCLUDED_DATES      : frozen list of (iso, why)
  pick_clean_onsets() : -> list of (label, onset_iso, mean_vol, era) selected windows
It reads the volume histogram from validation/reddit_wsb/data/volume_scan.json
(a continuous daily count produced by the prior run's harvest; reused, not re-scanned).
"""
import os
import json
import datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
VOL_PATH = os.path.abspath(os.path.join(
    HERE, "..", "reddit_wsb", "data", "volume_scan.json"))

PRE_GRAPH_DAYS = 90
POST_DAYS = 21
MIN_SEPARATION_DAYS = 45     # quasi-independence between selected clean windows
N_CLEAN_TARGET = 14          # aim for >=12 surviving the collapse pipeline
EXCLUDE_PAD_DAYS = 21        # pad each excluded date by +-this when masking onsets

# Frozen EXCLUSION list. The 10 original WSB onsets are added programmatically
# below; here are the macro event dates the prompt specifies.
MACRO_EVENTS = [
    ("2020-02-24", "COVID crash begins (week of 2020-02-24)"),
    ("2020-03-16", "COVID crash trough / circuit breakers"),
    ("2020-12-21", "Tesla S&P 500 inclusion effective"),
    ("2021-01-27", "GME mania peak"),
    ("2021-02-24", "GME leg-2"),
    ("2021-06-02", "AMC meme second wave"),
    ("2021-11-02", "late-2021 meme runup"),
    ("2022-01-24", "Jan 2022 tech selloff"),
    ("2022-02-24", "Russia-Ukraine market shock"),
    ("2022-05-09", "May 2022 broad drop / LUNA"),
    ("2022-11-08", "FTX collapse"),
    ("2023-03-10", "SVB collapse"),
    ("2023-05-01", "regional bank crisis"),
    ("2024-05-13", "Roaring Kitty GME return"),
    ("2024-08-05", "VIX / carry-unwind crash"),
]
# original-10 WSB onsets (verbatim, also excluded)
ORIGINAL_10 = [
    "2021-01-25", "2021-02-24", "2021-06-02", "2021-11-02", "2022-01-24",
    "2022-05-09", "2023-03-10", "2023-05-01", "2024-08-05", "2024-05-13",
]
# the 10 FRESH v3 onsets are ALSO excluded as clean-window centers (a clean null
# must not sit on the very events we are testing).
FRESH_10 = [
    "2020-12-21", "2021-08-04", "2021-09-20", "2022-02-24", "2022-08-08",
    "2022-08-26", "2022-11-08", "2023-06-01", "2023-08-02", "2024-03-26",
]

EXCLUDED_DATES = (
    [(d, w) for d, w in MACRO_EVENTS]
    + [(d, "original-10 WSB onset") for d in ORIGINAL_10]
    + [(d, "fresh-v3 onset (must not be a clean null)") for d in FRESH_10]
)


def _load_volume():
    v = json.load(open(VOL_PATH))
    return {dt.date.fromisoformat(k): int(n) for k, n in v.items()}


def _excluded_date_set():
    s = set()
    for iso, _ in EXCLUDED_DATES:
        d = dt.date.fromisoformat(iso)
        for k in range(-EXCLUDE_PAD_DAYS, EXCLUDE_PAD_DAYS + 1):
            s.add(d + dt.timedelta(days=k))
    return s


def pick_clean_onsets():
    vol = _load_volume()
    days = sorted(vol.keys())
    lo_avail, hi_avail = days[0], days[-1]
    excl = _excluded_date_set()

    # per-era (calendar year) lower-half threshold on the 21d-onset mean volume
    # First, compute, for every candidate center, the mean daily volume over its
    # 21d onset stretch [c-3, c+22). Then the era threshold is the MEDIAN of all
    # candidate onset-means in that year; "lower half" = at/below the median.
    cand = []  # (center, mean_vol, era)
    c = lo_avail + dt.timedelta(days=PRE_GRAPH_DAYS)
    last = hi_avail - dt.timedelta(days=POST_DAYS + 1)
    onset_lo_off, onset_hi_off = 3, POST_DAYS + 1  # [c-3, c+22)
    while c <= last:
        # full span must be covered
        span_ok = all((c + dt.timedelta(days=k)) in vol
                      for k in range(-PRE_GRAPH_DAYS, POST_DAYS + 1, 7))
        if span_ok:
            onset_days = [c + dt.timedelta(days=k)
                          for k in range(-onset_lo_off, onset_hi_off)]
            if not any(d in excl for d in onset_days):
                mv = sum(vol.get(d, 0) for d in onset_days) / len(onset_days)
                cand.append((c, mv, c.year))
        c += dt.timedelta(days=7)

    # era median threshold
    from collections import defaultdict
    by_era = defaultdict(list)
    for cc, mv, era in cand:
        by_era[era].append(mv)
    era_med = {era: sorted(vs)[len(vs) // 2] for era, vs in by_era.items()}

    lower_half = [(cc, mv, era) for cc, mv, era in cand if mv <= era_med[era]]
    # greedy lowest-volume-first with min separation, spread across eras
    lower_half.sort(key=lambda t: t[1])
    picked = []
    for cc, mv, era in lower_half:
        if all(abs((cc - p[0]).days) >= MIN_SEPARATION_DAYS for p in picked):
            picked.append((cc, mv, era))
        if len(picked) >= N_CLEAN_TARGET:
            break
    picked.sort(key=lambda t: t[0])
    out = []
    for i, (cc, mv, era) in enumerate(picked):
        out.append((f"clean_{cc.isoformat()}", cc.isoformat(), round(mv, 1), era))
    return out


def window_for(onset_iso):
    o = dt.date.fromisoformat(onset_iso)
    lo = o - dt.timedelta(days=PRE_GRAPH_DAYS)
    hi = o + dt.timedelta(days=POST_DAYS + 1)
    return lo, hi


if __name__ == "__main__":
    picks = pick_clean_onsets()
    print(f"selected {len(picks)} clean windows:")
    for label, onset, mv, era in picks:
        print(f"  {onset}  mean_onset_vol={mv:>9.1f}  era={era}")
