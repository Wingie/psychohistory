"""Frozen FRESH roster + shared frozen params for the SEALED WSB dynamic-N_eff
community-SPECIFICITY test (test ii', v4).

Why v4 exists. The v3 sealed run (validation/neff_v3) tested a CONJUNCTION that
bundled two endpoints: (1) a frozen MAGNITUDE threshold on the N_eff collapse and
(2) community-SPECIFICITY (the real block partition collapses harder than a block-
label shuffle of the same nodes). v3 taught us, in the null itself, that the
magnitude endpoint is NOT a valid discriminator on this substrate: genuinely-quiet
WSB windows already compress macro-N_eff a median 0.10 with a tail to 0.43, because
short high-volume onset windows shrink N_eff generically. So magnitude was the wrong
yardstick. The endpoint that actually tests the theory's claim -- "the EXISTING
community loses its independence before an endogenous cascade" -- is specificity,
and in v3 it fired 9/10 (shuffle-pctile of the observed collapse = 1.0 in 8 of 10
events). v4 pre-registers SPECIFICITY as the standalone PRIMARY endpoint and tests it
on a FRESH roster disjoint from every prior run. We do NOT relax v3's magnitude
threshold (that would be goalpost-moving); we test the correct hypothesis on new data.

Design contract (see PRE_REGISTRATION_neff_v4.md):
  - The roster is DISJOINT from the original-10 WSB cascades (reddit_wsb/roster_wsb.py)
    AND from the v3-10 (neff_v3/roster_v3.py). No onset within 14 days of any used
    onset; checked below as a calendar fact, blind to any collapse number.
  - Each onset is an EXTERNAL, publicly-dated market event (source noted per row).
    Onsets are NOT chosen from the collapse outcome.
  - WSB is continuously high-volume, so every onset has a usable pre-onset partition
    window [onset-90d, onset).
  - Params (bucket_days, n_shuffle, windows, caps) are IDENTICAL to v3/the original WSB
    run for comparability. The shuffle null and "fires" pctile are the SAME.

The PRIMARY decision rule (frozen in the prereg, consumed by analyze_v4.py):
  PASS iff  (a) fraction of K>=3 events firing vs shuffle >= 0.60
       AND  (b) binomial P(X >= k | n, p0=0.10) < 0.01   [p0 = construction-implied
            false-fire rate: observed > 90th pctile of its own shuffle null]
       AND  (c) n >= 8 powered events at K>=3.
Magnitude is still computed and REPORTED (median drop, per-event drops) but is
explicitly NON-GATING in v4, with v3's diagnosis attached.
"""
import datetime as dt

# ---------------------------------------------------------------- frozen params
PRE_GRAPH_DAYS = 90        # pre-onset window for commenter selection + co-thread graph
POST_DAYS = 21             # window after onset to capture the spike
BASELINE_DAYS = 90
USER_CAP = 6000            # most-active pre-onset commenters kept per run (logged)
THREAD_SUBSAMPLE = 40000   # cap on # threads used to build co-thread edges (logged)
PER_THREAD_CAP = 120       # max kept-users sampled per thread for pairing (logged)

BUCKET_DAYS = 3
N_SHUFFLE = 300
PCTILE = 0.90              # "fires vs shuffle" tested at the 90th pctile of the null

# ---------------------------------------------------------------- frozen primary rule
FIRE_FRACTION_BAR = 0.60   # (a) supermajority of powered events must fire
BINOM_P0 = 0.10            # null per-event fire rate (obs exchangeable with shuffles)
BINOM_ALPHA = 0.01         # (b) binomial tail must clear this
MIN_POWERED_N = 8          # (c)

# ---------------------------------------------------------------- fresh roster
# (label, onset_iso, "external date source / one-line justification")
# Disjoint from original-10 AND v3-10; every onset >= 14d from any used onset
# (verified in the assert block below as a pure calendar fact).
EVENTS = [
    ("covid_crash_mar2020",     "2020-03-16",
     "COVID circuit-breaker crash; S&P -12% session 2020-03-16, day after the Fed emergency cut to zero (public market date)."),
    ("vaccine_monday_nov2020",  "2020-11-09",
     "Pfizer/BioNTech 90%-efficacy readout 2020-11-09; rotation/risk-on session (company press release date)."),
    ("archegos_blowup_mar2021", "2021-03-26",
     "Archegos forced block-liquidation 2021-03-26 (VIAC/DISCA cascade; prime-broker fire-sale, public market date)."),
    ("coinbase_ipo_apr2021",    "2021-04-14",
     "Coinbase (COIN) direct-listing debut 2021-04-14 (Nasdaq reference-price date)."),
    ("jpow_75bp_jun2022",       "2022-06-15",
     "FOMC first 75bp hike of the cycle 2022-06-15 (Fed public calendar)."),
    ("cs_cds_oct2022",          "2022-10-03",
     "Credit Suisse CDS-blowout panic 2022-10-03 (weekend solvency-rumour spike, public market date)."),
    ("nvda_ai_aug2023",         "2023-08-23",
     "Nvidia Q2-FY24 AI-blowout earnings after-close 2023-08-23 (company report date)."),
    ("powell_pivot_dec2023",    "2023-12-13",
     "Dovish FOMC pivot / dot-plot cuts 2023-12-13 (Fed public calendar)."),
    ("nvda_earnings_feb2024",   "2024-02-21",
     "Nvidia Q4-FY24 blowout earnings after-close 2024-02-21 (company report date)."),
    ("nvda_split_jun2024",      "2024-06-07",
     "Nvidia 10:1 split effective 2024-06-07 (post-split trading 2024-06-10; company announced date)."),
    ("china_stimulus_sep2024",  "2024-09-24",
     "PBoC stimulus 'bazooka' 2024-09-24 (rate/RRR cuts + equity backstop, central-bank date)."),
    ("djt_election_nov2024",    "2024-11-06",
     "US election result 2024-11-06; Trump-trade risk-on session (public election date)."),
]

# ----- disjointness as a calendar fact (blind to any collapse number) ----------
_ORIGINAL_10_ONSETS = [
    "2021-01-25", "2021-02-24", "2021-06-02", "2021-11-02", "2022-01-24",
    "2022-05-09", "2023-03-10", "2023-05-01", "2024-08-05", "2024-05-13",
]
_V3_10_ONSETS = [
    "2020-12-21", "2021-08-04", "2021-09-20", "2022-02-24", "2022-08-08",
    "2022-08-26", "2022-11-08", "2023-06-01", "2023-08-02", "2024-03-26",
]
_USED = [dt.date.fromisoformat(s) for s in (_ORIGINAL_10_ONSETS + _V3_10_ONSETS)]
for _l, _o, _ in EVENTS:
    _d = dt.date.fromisoformat(_o)
    _gap = min(abs((_d - u).days) for u in _USED)
    assert _gap >= 14, f"roster_v4 onset {_o} ({_l}) only {_gap}d from a used onset"
# internal spacing >= 14d so harvest windows do not collide
_ons = sorted(dt.date.fromisoformat(o) for _, o, _ in EVENTS)
for _a, _b in zip(_ons, _ons[1:]):
    assert (_b - _a).days >= 14, f"roster_v4 internal onsets {_a},{_b} < 14d apart"


def all_events():
    """Yield (label, onset_iso, why) for the fresh event roster (event arm only).
    There is NO calm/null arm: the null for the PRIMARY specificity endpoint is the
    per-event block-label SHUFFLE computed inside analyze_run (300x), exactly as in
    v3/the original WSB run."""
    for label, onset, why in EVENTS:
        yield (label, onset, why)


def window_for(onset_iso):
    """(lo_date, hi_date) the harvest must cover for a run at this onset:
    full pre-graph window through POST_DAYS after onset."""
    o = dt.date.fromisoformat(onset_iso)
    lo = o - dt.timedelta(days=PRE_GRAPH_DAYS)
    hi = o + dt.timedelta(days=POST_DAYS + 1)
    return lo, hi


if __name__ == "__main__":
    print(f"roster_v4: {len(EVENTS)} fresh events, all >=14d from any used onset.")
    for l, o, _ in EVENTS:
        lo, hi = window_for(o)
        print(f"  {l:26s} onset {o}  harvest [{lo} .. {hi})")
