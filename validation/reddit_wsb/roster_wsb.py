"""Frozen roster for the WSB dynamic-N_eff-collapse test (Reddit mirror of test ii').

Mirrors validation/wikipedia/roster.py. Single source of truth for harvest_filter.py
and neff_collapse_wsb.py.

Onset selection (documented honestly):
  - The PRIMARY onset is the canonical endogenous GameStop reflexive cascade,
    2021-01-25 (external/public date, not chosen from the data).
  - The remaining onsets are distinct WSB activity-surge events. Each is anchored to a
    PUBLIC event date AND corroborated by a raw daily-comment-volume peak in the dump
    (see volume_scan.json produced by harvest_filter.py --scan). Every onset has a
    usable pre-onset window [onset-PRE_GRAPH_DAYS, onset) that is NOT itself inside a
    larger surge (so a genuine "calm-ish" baseline partition exists).
  - For EACH event a matched-calm arm uses the SAME subreddit at onset - CALM_OFFSET_DAYS
    (a presumed-quiet window), exactly as the Wikipedia design.

These dates are committed BEFORE the collapse numbers are computed. The frozen
thresholds (f=0.30, fire vs shuffle at 90th pctile, n>=8 powered) are unchanged.
"""
import datetime as dt

# (label, onset_iso, one-line justification)
EVENTS = [
    ("GME_squeeze_jan2021",   "2021-01-25", "canonical endogenous GME short squeeze; primary"),
    ("GME_leg2_feb2021",      "2021-02-24", "second GME spike late Feb 2021"),
    ("AMC_meme_jun2021",      "2021-06-02", "AMC/meme second wave June 2021"),
    ("GME_runup_nov2021",     "2021-11-02", "late-2021 GME/meme runup"),
    ("market_selloff_jan2022","2022-01-24", "Jan 2022 tech selloff WSB surge"),
    ("market_drop_may2022",   "2022-05-09", "May 2022 broad market drop / crypto (LUNA) surge"),
    ("svb_collapse_mar2023",  "2023-03-10", "SVB bank collapse; WSB activity surge"),
    ("regional_bank_may2023", "2023-05-01", "First Republic / regional bank crisis surge"),
    ("aug2024_vix_spike",     "2024-08-05", "Aug 2024 VIX/carry-unwind crash surge"),
    ("gme_kitty_may2024",     "2024-05-13", "Roaring Kitty return GME spike May 2024"),
]

# Windows (days) -- mirror wiki roster intent, adapted for Reddit volume.
PRE_GRAPH_DAYS = 90    # pre-onset window for commenter selection + co-thread graph
POST_DAYS = 21         # window after onset to capture the spike
BASELINE_DAYS = 90     # full-trajectory span lead-in (= PRE_GRAPH_DAYS)
USER_CAP = 6000        # most-active pre-onset commenters kept per run (logged)
THREAD_SUBSAMPLE = 40000  # cap on # threads used to build co-thread edges (logged)
PER_THREAD_CAP = 120   # max kept-users sampled per thread for pairing (bounds O(k^2)
                       # edge blowup on WSB mega-threads; logged)
CALM_OFFSET_DAYS = 365  # matched calm window = onset - 1 year

# bucket / null params mirrored from neff_collapse_wiki.py
BUCKET_DAYS = 3
N_SHUFFLE = 300
F_THRESHOLD = 0.30
PCTILE = 0.90


def calm_onset(onset_iso):
    return (dt.date.fromisoformat(onset_iso) - dt.timedelta(days=CALM_OFFSET_DAYS)).isoformat()


def all_runs():
    """Yield (label, onset_iso, arm) for both event and matched-calm arms."""
    for label, onset, _why in EVENTS:
        yield (label, onset, "event")
        yield (label + "__calm", calm_onset(onset), "calm")


def window_for(onset_iso):
    """Return (lo_date, hi_date) the harvest must cover for a run at this onset.
    Need full pre-graph window through POST_DAYS after onset."""
    o = dt.date.fromisoformat(onset_iso)
    lo = o - dt.timedelta(days=PRE_GRAPH_DAYS)
    hi = o + dt.timedelta(days=POST_DAYS + 1)
    return lo, hi
