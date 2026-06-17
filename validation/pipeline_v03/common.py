"""Shared loaders + detector primitives for the v0.3 pipeline upgrades.

These are L2/L6 OBSERVATION-LAYER components (data-acquisition + observation
operators), NOT new theory. They replace the scalar mention-density proxy used
in the v0.2 pilots with vector / graph / concentration observation operators.

All functions here are pure transforms (no global state, no I/O side effects
beyond the explicit `load_*` readers). Everything runs LOCAL on CPU.
"""
import json
import glob
import math
import os
import datetime as dt
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
VAL = os.path.abspath(os.path.join(HERE, ".."))
GITHUB_DATA = os.path.join(VAL, "github", "data")
CONCORDANCE_DATA = os.path.join(VAL, "comment_concordance", "data")
ASK_ECON_NDJSON = os.path.join(VAL, "temporal", "data", "ask_econ.ndjson")

# GitHub cascade onsets (verbatim from github/replicate_github.py ONSETS).
GITHUB_ONSETS = {
    "autogpt":      "2023-04-02",
    "langchain":    "2023-01-08",
    "gpt_engineer": "2023-06-11",
    "metagpt":      "2023-08-06",
    "superagi":     "2023-06-04",
    "agentgpt":     "2023-04-09",
}
# The 8 repos of the LLM-agent cohort that are usable (babyagi dropped as
# degenerate per github/RESULTS.md; gharchive_probe is not a repo).
GITHUB_REPOS = ["autogpt", "langchain", "gpt_engineer", "metagpt",
                "superagi", "agentgpt", "privategpt", "agentgpt"]
GITHUB_REPOS = ["autogpt", "langchain", "gpt_engineer", "metagpt",
                "superagi", "agentgpt", "privategpt"]


def to_date(s):
    return dt.date.fromisoformat(s)


def week_of(ts):
    """Monday-anchored ISO week date for a unix timestamp."""
    d = dt.datetime.utcfromtimestamp(int(ts)).date()
    return d - dt.timedelta(days=d.weekday())


# ----------------------------------------------------------------- GitHub ----
def load_github_contrib(repo):
    """Return list of contributor records: {login, weeks:[{w,c,a,d}]}."""
    path = os.path.join(GITHUB_DATA, repo + "_contrib.json")
    d = json.load(open(path, encoding="utf-8"))
    out = []
    for c in d:
        login = (c.get("author") or {})
        login = login.get("login") if isinstance(login, dict) else str(login)
        out.append(dict(login=login or "?", weeks=c.get("weeks", [])))
    return out


def github_author_week_commits(repo):
    """{week_date: {login: commits}} for a repo (only weeks with activity)."""
    recs = load_github_contrib(repo)
    out = defaultdict(lambda: defaultdict(int))
    for r in recs:
        for wk in r["weeks"]:
            if wk.get("c", 0):
                out[week_of(wk["w"])][r["login"]] += wk["c"]
    return {k: dict(v) for k, v in out.items()}


# ----------------------------------------------- AskEconomics comment corpus -
def load_concordance_comments():
    """Return list of {author, created_utc, parent_id, link_id, name, week}.

    Drops [deleted]/null authors. link_id = thread (t3_*); parent_id is the
    immediate parent (t1_* comment or t3_* the post)."""
    out = []
    for f in glob.glob(os.path.join(CONCORDANCE_DATA, "*.json")):
        data = json.load(open(f, encoding="utf-8")).get("data", [])
        for c in data:
            if not isinstance(c, dict):
                continue
            a = c.get("author")
            if not a or a == "[deleted]" or a == "AutoModerator":
                continue
            ts = c.get("created_utc")
            if not ts:
                continue
            out.append(dict(author=a, created_utc=int(ts),
                            parent_id=c.get("parent_id"),
                            link_id=c.get("link_id"),
                            name=c.get("name"),
                            week=week_of(ts)))
    return out


def concordance_author_week_counts():
    """{week_date: {author: comment_count}}."""
    out = defaultdict(lambda: defaultdict(int))
    for c in load_concordance_comments():
        out[c["week"]][c["author"]] += 1
    return {k: dict(v) for k, v in out.items()}


# ------------------------------------------------------ concentration stats --
def hhi(shares):
    """Herfindahl-Hirschman Index = sum of squared activity SHARES.
    Input: iterable of raw counts (need not sum to 1). Returns HHI in (0,1].
    1 = a single actor holds everything; ~1/N = perfectly uniform."""
    a = np.asarray(list(shares), float)
    a = a[a > 0]
    if a.sum() <= 0:
        return float("nan")
    p = a / a.sum()
    return float(np.sum(p * p))


def gini(counts):
    """Gini coefficient of an activity distribution (raw counts).
    0 = perfectly equal, ->1 = one actor holds all activity."""
    a = np.sort(np.asarray(list(counts), float))
    a = a[a >= 0]
    n = a.size
    if n == 0 or a.sum() == 0:
        return float("nan")
    idx = np.arange(1, n + 1)
    return float((np.sum((2 * idx - n - 1) * a)) / (n * a.sum()))


def top_k_share(counts, frac=0.05):
    """Share of total activity held by the top `frac` of actors (by count)."""
    a = np.sort(np.asarray(list(counts), float))[::-1]
    a = a[a > 0]
    if a.size == 0:
        return float("nan")
    k = max(1, int(math.ceil(frac * a.size)))
    return float(a[:k].sum() / a.sum())


# --------------------------------------------- detrended CSD (from battery) --
def ar1(x):
    x = np.asarray(x, float)
    if len(x) < 2:
        return 0.0
    x = x - x.mean()
    denom = np.sum(x[:-1] ** 2)
    if denom <= 0:
        return 0.0
    return float(np.sum(x[:-1] * x[1:]) / denom)


def kendall_tau(y):
    """Kendall rank-correlation of y vs time index (Dakos et al. 2012)."""
    n = len(y)
    if n < 3:
        return float("nan")
    s = 0
    for a in range(n):
        for b in range(a + 1, n):
            d = float(y[b]) - float(y[a])
            s += (1 if d > 0 else 0) - (1 if d < 0 else 0)
    denom = n * (n - 1) / 2.0
    return s / denom if denom else float("nan")


def detrended_csd(series, sub=4, log=False):
    """Detrended critical-slowing-down score on a 1-D series (verbatim recipe
    from early_warning_battery.battery.window_score_csd, generalised to accept
    any pre-computed series so we can feed it the SEMANTIC variance instead of
    volume). Returns dict(tau_var, tau_ar1, score) or None."""
    seg = np.asarray(series, float)
    if len(seg) < 6:
        return None
    if log:
        seg = np.log1p(seg)
    k = 3
    pad = np.pad(seg, (k // 2, k // 2), mode="edge")
    trend = np.convolve(pad, np.ones(k) / k, mode="valid")
    resid = seg - trend
    rv, ra = [], []
    for j in range(len(resid) - sub + 1):
        w = resid[j:j + sub]
        rv.append(float(np.var(w)))
        ra.append(ar1(w))
    if len(rv) < 3:
        return None
    tv = kendall_tau(rv)
    ta = kendall_tau(ra)
    tv = 0.0 if math.isnan(tv) else tv
    ta = 0.0 if math.isnan(ta) else ta
    return dict(tau_var=float(tv), tau_ar1=float(ta), score=float(tv + ta),
                var_first=rv[0], var_last=rv[-1])


def percentile_rank(value, pool):
    """Fraction of `pool` strictly below `value` (the base-rate percentile)."""
    pool = [p for p in pool if not (isinstance(p, float) and math.isnan(p))]
    if not pool:
        return float("nan")
    return float(np.mean([p < value for p in pool]))
