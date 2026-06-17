#!/usr/bin/env py -3.12
"""
Test (i) ZERO-SUM ATTENTION  --  conservation of attention within a subreddit.

HYPOTHESIS (paper: attention as an approximately conserved, slowly-sourced measure):
    Within a single subreddit, total posting activity per week is a "budget".
    If attention is conserved, a surge in one TOPIC's share must come at the
    EXPENSE of other topics' shares -> the cross-correlation of de-trended topic
    SHARES is, on average, NEGATIVE (off-diagonal mean < 0). The conserved
    constraint sum_k share_k(t) = 1 mechanically forces SOME negativity, so the
    real test is whether the observed mean off-diagonal correlation is MORE
    negative than a permutation null that destroys week-to-week co-movement while
    preserving the simplex constraint and the marginal topic sizes.

    Non-conservation (independent growth) predicts the de-trended share
    correlations are ~0 / indistinguishable from the permutation null.

WHAT THIS SCRIPT DOES
    1. Ingest submissions (NDJSON, one JSON object per line, OR a JSON list, OR
       the pullpush/arctic-shift {"data":[...]} envelope).
    2. Auto-detect fields: created_utc, title, selftext, score, id, subreddit,
       link_flair_text.
    3. Assign each post to a TOPIC. Two modes:
         --topics flair      : use link_flair_text (one topic per distinct flair)
         --topics keywords   : keyword buckets (default; embedding-free) defined
                               in TOPIC_KEYWORDS below; posts matching none go to
                               "other"; posts matching several go to the first.
    4. Build a weekly count matrix C[week, topic], convert to SHARES
       S = C / rowsum, then remove the slow "source term" (overall growth) by
       working in shares (already growth-normalised) AND additionally
       de-trending each share column with a centered rolling mean.
    5. Compute the topic-share cross-correlation matrix; summary statistic =
       mean of the off-diagonal entries (negative => trade-off => conservation).
    6. Permutation null: independently circularly-shift each topic's de-trended
       share series many times, recompute the mean off-diagonal each time. Report
       the observed value, the null mean+/-sd, and a one-sided p-value
       (P[null <= observed]).

EXPECTED DATA FORMAT
    One subreddit. >= ~8 weeks of data, the more the better. Each record needs
    created_utc (epoch seconds, int or float-string) and at least a title; flair
    optional (required only for --topics flair).

USAGE
    py -3.12 test_zero_sum.py data/ask_econ.ndjson
    py -3.12 test_zero_sum.py data/ask_econ.ndjson --topics keywords --perms 2000
    py -3.12 test_zero_sum.py data/ask_econ.ndjson --topics flair --min-week-posts 20
"""
import sys, json, argparse, math, statistics, datetime, random, re
from collections import defaultdict

# --- topic keyword buckets (edit for your subreddit) ----------------------
TOPIC_KEYWORDS = {
    "inflation":   ["inflation", "cpi", "price level", "deflation", "stagflation"],
    "labor":       ["wage", "labor", "labour", "employment", "unemploy", "job", "minimum wage", "union"],
    "trade":       ["tariff", "trade", "import", "export", "trade war", "protectionis"],
    "monetary":    ["interest rate", "fed", "central bank", "monetary", "money supply", "rate cut", "rate hike"],
    "inequality":  ["inequality", "wealth", "poverty", "redistribut", "billionaire", "wage gap", "gini"],
    "housing":     ["housing", "rent", "mortgage", "real estate", "home price"],
    "growth":      ["gdp", "growth", "recession", "productivity", "business cycle"],
    "tax":         ["tax", "fiscal", "deficit", "debt", "subsid", "spending"],
    "crypto":      ["crypto", "bitcoin", "stablecoin", "blockchain"],
    "theory":      ["theory", "model", "curve", "elasticity", "marginal", "textbook", "econ 101"],
}


def load_records(path):
    txt = open(path, encoding="utf-8").read().strip()
    recs = []
    # try NDJSON first
    looks_ndjson = "\n" in txt and txt.lstrip()[0] == "{" and '"data"' not in txt[:200]
    if looks_ndjson:
        for line in txt.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                recs.append(json.loads(line))
            except Exception:
                pass
        if recs:
            return recs
    # try whole-file JSON
    try:
        obj = json.loads(txt)
    except Exception:
        # fall back to NDJSON even if heuristic missed
        for line in txt.splitlines():
            line = line.strip()
            if line:
                try:
                    recs.append(json.loads(line))
                except Exception:
                    pass
        return recs
    if isinstance(obj, list):
        return obj
    if isinstance(obj, dict):
        if "data" in obj and isinstance(obj["data"], list):
            data = obj["data"]
            # arctic/pullpush envelopes; also reddit Listing {data:{children:[{data:..}]}}
            if data and isinstance(data[0], dict) and data[0].get("kind") and "data" in data[0]:
                return [c["data"] for c in data]
            return data
        if "data" in obj and isinstance(obj["data"], dict) and "children" in obj["data"]:
            return [c["data"] for c in obj["data"]["children"]]
    return recs


def get_ts(r):
    for k in ("created_utc", "created"):
        if k in r and r[k] is not None:
            try:
                return float(r[k])
            except Exception:
                pass
    return None


def week_key(ts):
    d = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).date()
    iso = d.isocalendar()
    return (iso[0], iso[1])  # (iso_year, iso_week)


def assign_topic(r, mode):
    if mode == "flair":
        f = r.get("link_flair_text")
        return (f or "none").strip()
    text = (str(r.get("title") or "") + " " + str(r.get("selftext") or "")).lower()
    for topic, kws in TOPIC_KEYWORDS.items():
        for kw in kws:
            if kw in text:
                return topic
    return "other"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infile")
    ap.add_argument("--topics", choices=["keywords", "flair"], default="keywords")
    ap.add_argument("--perms", type=int, default=2000)
    ap.add_argument("--min-week-posts", type=int, default=10,
                    help="drop weeks with fewer total posts (edge weeks are partial)")
    ap.add_argument("--min-topic-share", type=float, default=0.01,
                    help="drop topics whose mean share is below this")
    ap.add_argument("--roll", type=int, default=5, help="centered rolling window for de-trending shares")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    random.seed(args.seed)

    recs = load_records(args.infile)
    counts = defaultdict(lambda: defaultdict(int))   # week -> topic -> n
    topics = set()
    n_used = 0
    for r in recs:
        ts = get_ts(r)
        if ts is None:
            continue
        wk = week_key(ts)
        tp = assign_topic(r, args.topics)
        counts[wk][tp] += 1
        topics.add(tp)
        n_used += 1

    weeks = sorted(counts.keys())
    # drop partial edge weeks by total volume
    weeks = [w for w in weeks if sum(counts[w].values()) >= args.min_week_posts]
    if len(weeks) < 6:
        print(f"VERDICT: INSUFFICIENT DATA - only {len(weeks)} usable weeks "
              f"(need >= 6). Records read: {len(recs)}, used: {n_used}.")
        return

    topics = sorted(topics)
    # shares matrix
    shares = {tp: [] for tp in topics}
    for w in weeks:
        tot = sum(counts[w].values())
        for tp in topics:
            shares[tp].append(counts[w][tp] / tot if tot else 0.0)

    # drop tiny topics
    topics = [tp for tp in topics if statistics.mean(shares[tp]) >= args.min_topic_share]
    shares = {tp: shares[tp] for tp in topics}
    if len(topics) < 3:
        print(f"VERDICT: INSUFFICIENT TOPICS - only {len(topics)} topics above "
              f"min-topic-share. Try --topics flair or lower --min-topic-share.")
        return

    # de-trend each share series with centered rolling mean (removes slow source/drift)
    def detrend(x, k):
        n = len(x)
        out = []
        h = k // 2
        for i in range(n):
            lo, hi = max(0, i - h), min(n, i + h + 1)
            m = sum(x[lo:hi]) / (hi - lo)
            out.append(x[i] - m)
        return out

    res = {tp: detrend(shares[tp], args.roll) for tp in topics}

    def pearson(a, b):
        n = len(a)
        ma, mb = sum(a) / n, sum(b) / n
        va = sum((x - ma) ** 2 for x in a)
        vb = sum((x - mb) ** 2 for x in b)
        if va == 0 or vb == 0:
            return 0.0
        cov = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
        return cov / math.sqrt(va * vb)

    def mean_offdiag(series_map):
        ts = list(series_map.keys())
        vals = []
        for i in range(len(ts)):
            for j in range(i + 1, len(ts)):
                vals.append(pearson(series_map[ts[i]], series_map[ts[j]]))
        return statistics.mean(vals), vals

    obs, pair_vals = mean_offdiag(res)

    # permutation null: independently circular-shift each de-trended series
    n = len(weeks)
    null_means = []
    keys = list(res.keys())
    for _ in range(args.perms):
        shifted = {}
        for k in keys:
            s = random.randrange(1, n) if n > 1 else 0
            x = res[k]
            shifted[k] = x[s:] + x[:s]
        m, _ = mean_offdiag(shifted)
        null_means.append(m)
    nm = statistics.mean(null_means)
    nsd = statistics.pstdev(null_means) or 1e-12
    # one-sided: how often is null at least as negative as observed
    p = (sum(1 for x in null_means if x <= obs) + 1) / (len(null_means) + 1)
    z = (obs - nm) / nsd

    print("=" * 64)
    print("TEST (i) ZERO-SUM ATTENTION  (conservation of attention)")
    print("=" * 64)
    print(f"input            : {args.infile}")
    print(f"records / used   : {len(recs)} / {n_used}")
    print(f"weeks (kept)     : {len(weeks)}  ({weeks[0]} .. {weeks[-1]})")
    print(f"topic mode       : {args.topics}")
    print(f"topics           : {', '.join(topics)}")
    print("-" * 64)
    print(f"observed mean off-diagonal share-corr : {obs:+.4f}")
    print(f"permutation null  mean +/- sd         : {nm:+.4f} +/- {nsd:.4f}")
    print(f"z vs null                              : {z:+.2f}")
    print(f"one-sided p (null <= observed)         : {p:.4f}")
    print("-" * 64)
    most_neg = sorted(
        ((pearson(res[a], res[b]), a, b)
         for i, a in enumerate(topics) for b in topics[i+1:]),
        key=lambda t: t[0])[:5]
    print("most negative topic pairs (strongest trade-offs):")
    for c, a, b in most_neg:
        print(f"   {c:+.3f}  {a} <-> {b}")
    print("-" * 64)
    if obs < 0 and p < 0.05:
        print("VERDICT: SUPPORTS CONSERVATION - share co-movement is significantly")
        print("         more negative than the permutation null (zero-sum trade-off).")
    elif obs < 0:
        print("VERDICT: WEAK/INCONCLUSIVE - shares trade off on average but not")
        print("         beyond the simplex-induced null at p<0.05. More weeks needed.")
    else:
        print("VERDICT: AGAINST CONSERVATION - topic shares co-move non-negatively;")
        print("         consistent with independent growth, not a fixed attention budget.")
    print("NOTE: with the simplex constraint sum(shares)=1, a NEGATIVE mean is")
    print("      partly mechanical; the permutation null is what makes this a test.")


if __name__ == "__main__":
    main()
