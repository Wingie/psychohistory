"""Frozen roster for the Wikipedia dynamic-N_eff-collapse test (test ii').

Committed BEFORE harvest (see PRE_REGISTRATION_wiki.md). Single source of truth for
both harvest.py and neff_collapse_wiki.py.

Inclusion rule: the article must have ALREADY EXISTED with steady editing before its
attention spike (so a pre-onset editor partition exists). Articles created AT the event
("born into cascade") are excluded -- that is the GitHub failure mode we are escaping.

onset = the public date of the attention spike (an external event date, not chosen by
looking at edit data). created = year the article was created (all comfortably pre-onset).
"""
import datetime as dt

# (wikipedia_title, onset_iso, created_year, one-line justification)
EVENTS = [
    ("GameStop",            "2021-01-25", 2001, "short squeeze; article existed 20y"),
    ("Queen Elizabeth II",  "2022-09-08", 2001, "death; decades of steady editing"),
    ("Silicon Valley Bank", "2023-03-10", 2005, "bank collapse; existed ~18y"),
    ("FTX",                 "2022-11-08", 2019, "exchange collapse; existed 3y prior"),
    ("Boeing 737 MAX",      "2019-03-10", 2016, "Ethiopian crash/grounding; existed 3y"),
    ("Bitcoin",             "2021-04-14", 2010, "Coinbase-IPO price peak; existed 11y"),
    ("OpenAI",              "2022-11-30", 2015, "ChatGPT launch; org article existed 7y"),
    ("Donald Trump",        "2021-01-06", 2004, "Capitol storming; huge existing article"),
    ("Credit Suisse",       "2023-03-19", 2003, "UBS emergency takeover; existed 20y"),
    ("Terra (blockchain)",  "2022-05-09", 2019, "UST death-spiral; existed 3y"),
    ("Twitter",             "2022-10-27", 2006, "Musk acquisition close; existed 16y"),
    ("Evergrande Group",    "2021-09-20", 2009, "default crisis; existed 12y"),
    # --- power augmentation (same inclusion rule: pre-existing + actively edited +
    #     clean external onset; selected for high pre-onset activity to clear the
    #     K>=3 structural bar, NOT for collapse outcome; frozen thresholds unchanged).
    ("Joe Biden",           "2020-11-07", 2001, "election called; very active article"),
    ("Kobe Bryant",         "2020-01-26", 2002, "death; highly active pre-onset"),
    ("Volodymyr Zelenskyy", "2022-02-24", 2014, "invasion; active pre-onset"),
    ("NATO",                "2022-02-24", 2001, "invasion response; active pre-onset"),
    ("Diego Maradona",      "2020-11-25", 2001, "death; active pre-onset"),
    ("Suez Canal",          "2021-03-23", 2001, "Ever Given blockage; active pre-onset"),
    ("Robinhood (company)", "2021-01-28", 2014, "GME trading halt; existed 7y"),
    ("Notre-Dame de Paris", "2019-04-15", 2001, "fire; very active pre-onset"),
]

# Windows (days)
BASELINE_DAYS = 90     # pre-onset window for editor selection + co-editing graph
POST_DAYS = 21         # window after onset to capture the spike
EDITOR_CAP = 150       # most-active pre-onset editors kept per article (logged)
CALM_OFFSET_DAYS = 365 # matched calm window = onset - 1 year (same article/blocks)


def calm_onset(onset_iso):
    return (dt.date.fromisoformat(onset_iso) - dt.timedelta(days=CALM_OFFSET_DAYS)).isoformat()


def all_runs():
    """Yield (title, onset_iso, arm) for both event and matched-calm arms."""
    for title, onset, _yr, _why in EVENTS:
        yield (title, onset, "event")
        yield (title, calm_onset(onset), "calm")
