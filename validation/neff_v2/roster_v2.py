"""FRESH roster for the SEALED dynamic-N_eff-collapse test (test ii', v2).

Committed BEFORE harvest (see PRE_REGISTRATION_neff_v2.md). DISJOINT from the 20
tuning titles in validation/wikipedia/roster.py -- none reused.

Inclusion rule (frozen): article ALREADY EXISTED with steady editing before a clean
EXTERNAL onset (public event date, not chosen from edit data); a genuinely-quiet
pre-onset calm window plausibly exists; selected for pre-onset activity to clear K>=3,
NOT for collapse outcome; mix endogenous-community and a few exogenous shocks.

onset = the public date of the attention spike. created = article creation year
(all comfortably pre-onset). Selection blind to collapse outcome.
"""
import datetime as dt

# (wikipedia_title, onset_iso, created_year, kind, one-line justification)
# kind: ENDO = existing community synchronizes; EXO = exogenous newcomer-flood shock.
EVENTS = [
    ("Ethereum",                 "2021-11-08", 2014, "ENDO", "all-time-high price peak; crypto editor community active 7y"),
    ("Tesla, Inc.",              "2021-11-04", 2009, "ENDO", "$1.2T valuation / Hertz deal peak; very active pre-onset"),
    ("Binance",                  "2023-06-05", 2017, "ENDO", "SEC lawsuit; exchange article actively edited"),
    ("Dogecoin",                 "2021-05-08", 2013, "ENDO", "SNL/Musk peak; meme-coin editors active"),
    ("Nvidia",                   "2023-05-25", 2001, "ENDO", "AI-driven $1T approach; long-active tech article"),
    ("Sam Bankman-Fried",        "2022-11-11", 2022, "EXO",  "FTX founder; existed pre-onset but flooded at collapse"),
    ("Luna Foundation Guard",    "2022-05-09", 2022, "ENDO", "UST depeg; crypto community"),
    ("Lehman Brothers",          "2008-09-15", 2002, "EXO",  "bankruptcy; historical, used as out-of-era control"),
    ("Northern Rock",            "2007-09-14", 2004, "EXO",  "bank run; existed 3y prior"),
    ("Wirecard",                 "2020-06-18", 2005, "ENDO", "accounting-fraud collapse; existed 15y"),
    ("Archegos Capital Management", "2021-03-26", 2020, "EXO", "margin-call blowup; existed pre-onset"),
    ("Gautam Adani",             "2023-01-24", 2008, "ENDO", "Hindenburg short report; biography actively edited"),
    ("First Republic Bank",      "2023-05-01", 2007, "EXO",  "FDIC seizure / JPMorgan; existed 16y"),
    ("Coinbase",                 "2021-04-14", 2013, "ENDO", "direct listing day; crypto community active"),
    ("Reddit",                   "2021-01-28", 2005, "ENDO", "WSB/GME platform spike; very active article"),
]

# Windows (days) -- IDENTICAL to the tuning run so the frozen pipeline is unchanged.
BASELINE_DAYS = 90
POST_DAYS = 21
EDITOR_CAP = 150
CALM_OFFSET_DAYS = 365   # kept only so harvest can pull a calm island for the clean-null
                         # window search; the clean null is the V2 genuinely-quiet window,
                         # NOT this fixed offset (see PRE_REGISTRATION_neff_v2.md).


def calm_onset(onset_iso):
    return (dt.date.fromisoformat(onset_iso) - dt.timedelta(days=CALM_OFFSET_DAYS)).isoformat()


def all_runs():
    """Yield (title, onset_iso, arm) for both event and calm-island arms."""
    for title, onset, _yr, _kind, _why in EVENTS:
        yield (title, onset, "event")
        yield (title, calm_onset(onset), "calm")
