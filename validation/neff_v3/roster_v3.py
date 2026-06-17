"""Frozen FRESH roster + shared frozen params for the SEALED WSB dynamic-N_eff
collapse test (test ii', v3).

This is the single source of truth for harvest_v3.py, derive_f_v3.py and
analyze_v3.py. EVERY date / param here is committed BEFORE the fresh-roster
collapse numbers are computed.

Design contract (see PRE_REGISTRATION_neff_v3.md):
  - The fresh roster is DISJOINT from the original 10 WSB cascades in
    validation/reddit_wsb/roster_wsb.py (no onset reused).
  - Each onset is an EXTERNAL, publicly-dated market event (date source noted per
    row). Onsets are NOT chosen from the collapse outcome.
  - WSB is continuously high-volume, so every onset trivially has a usable
    pre-onset partition window [onset-90d, onset).
  - Params (bucket_days, n_shuffle, windows, caps) are IDENTICAL to the prior WSB
    run (validation/reddit_wsb) for comparability.

The FROZEN threshold f is derived separately by derive_f_v3.py (95th percentile of
a CLEAN WSB null) and recorded in derive_f_v3.json + the prereg BEFORE this fresh
roster is harvested. f is NOT defined in this file because it is data-derived; the
DECISION RULE that consumes it is frozen in the prereg and in analyze_v3.py.
"""
import datetime as dt

# ---------------------------------------------------------------- frozen params
PRE_GRAPH_DAYS = 90        # pre-onset window for commenter selection + co-thread graph
POST_DAYS = 21             # window after onset to capture the spike
BASELINE_DAYS = 90         # full-trajectory span lead-in (= PRE_GRAPH_DAYS)
USER_CAP = 6000            # most-active pre-onset commenters kept per run (logged)
THREAD_SUBSAMPLE = 40000   # cap on # threads used to build co-thread edges (logged)
PER_THREAD_CAP = 120       # max kept-users sampled per thread for pairing (logged)

BUCKET_DAYS = 3
N_SHUFFLE = 300
PCTILE = 0.90              # "fires vs shuffle" tested at the 90th pctile of the null

# ---------------------------------------------------------------- fresh roster
# (label, onset_iso, "external date source / one-line justification")
# NONE of these onsets appears in roster_wsb.py's original 10.
# Onsets are calendar dates of the public market event (or the first US trading
# session that reacts to it). We pick for clean external dates + arm independence,
# blind to collapse size.
#
# FROZEN INDEPENDENCE RULE (applied to the candidate pool BEFORE harvest, blind to
# collapse outcome): a candidate is EXCLUDED if its onset is within 14 days of any
# original-10 onset OR its full harvest window overlaps an original-10 window by
# > 0.90. This drops three candidates that are effectively the SAME event as an
# original-10 cascade (overlap/proximity is a calendar fact, not a collapse number):
#   - yen_carry_jul2024 (2024-07-31): gap 5d to aug2024_vix_spike -- it IS that crash's cause.
#   - credit_suisse_mar2023 (2023-03-19): gap 9d AND 0.92 window overlap with svb_collapse_mar2023.
#   - meta_crash_feb2022 (2022-02-03): gap 10d AND 0.91 window overlap with market_selloff_jan2022.
# The surviving 10 all have onsets >= 31 days from any original-10 onset and full-
# window overlap <= 0.72, so the measured spike is a distinct external event.
EVENTS = [
    ("tesla_sp500_dec2020",   "2020-12-21",
     "Tesla added to S&P 500, effective 2020-12-21 (S&P Dow Jones Indices announcement 2020-11-16)."),
    ("hood_ipo_aug2021",      "2021-08-04",
     "Robinhood (HOOD) IPO debut week; first full trading day 2021-07-29, retail-frenzy spike peaked 2021-08-04 (Nasdaq listing)."),
    ("evergrande_sep2021",    "2021-09-20",
     "Evergrande default scare; global risk-off session 2021-09-20 (Reuters/Bloomberg market reports)."),
    ("ukraine_shock_feb2022", "2022-02-24",
     "Russia invades Ukraine 2022-02-24; global market shock session (public geopolitical date)."),
    ("bbby_squeeze_aug2022",  "2022-08-08",
     "Bed Bath & Beyond (BBBY) meme squeeze; RC Ventures filing 2022-08-15 run-up began 2022-08-08 (SEC 13D/news)."),
    ("jpow_jackson_aug2022",  "2022-08-26",
     "Powell Jackson Hole hawkish speech 2022-08-26; S&P -3.4% session (Fed public calendar)."),
    ("ftx_collapse_nov2022",  "2022-11-08",
     "FTX collapse; Binance LOI / withdrawal halt 2022-11-08 (public crypto-market date)."),
    ("debt_ceiling_jun2023",  "2023-06-01",
     "US debt-ceiling deal passes House 2023-05-31 / Senate 2023-06-01 (Congressional record)."),
    ("fitch_downgrade_aug2023", "2023-08-02",
     "Fitch downgrades US sovereign rating AAA->AA+ 2023-08-01; market reaction session 2023-08-02 (Fitch Ratings release)."),
    ("djt_media_mar2024",     "2024-03-26",
     "Trump Media (DJT) SPAC merger trading debut 2024-03-26 (Nasdaq listing date)."),
]

# Sanity: assert disjoint from the original-10 onsets (defensive; the original
# onsets are hardcoded here to avoid importing the other roster at module import).
_ORIGINAL_10_ONSETS = {
    "2021-01-25", "2021-02-24", "2021-06-02", "2021-11-02", "2022-01-24",
    "2022-05-09", "2023-03-10", "2023-05-01", "2024-08-05", "2024-05-13",
}
for _l, _o, _ in EVENTS:
    assert _o not in _ORIGINAL_10_ONSETS, f"roster_v3 onset {_o} collides with original-10"


def all_events():
    """Yield (label, onset_iso, why) for the fresh event roster (event arm only).
    The calm/null arm is NOT here: in v3 the calm comparison is the clean-null
    distribution produced by derive_f_v3.py, NOT an onset-365d matched arm."""
    for label, onset, why in EVENTS:
        yield (label, onset, why)


def window_for(onset_iso):
    """(lo_date, hi_date) the harvest must cover for a run at this onset:
    full pre-graph window through POST_DAYS after onset."""
    o = dt.date.fromisoformat(onset_iso)
    lo = o - dt.timedelta(days=PRE_GRAPH_DAYS)
    hi = o + dt.timedelta(days=POST_DAYS + 1)
    return lo, hi
