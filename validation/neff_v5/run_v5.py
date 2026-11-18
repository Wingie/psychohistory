"""neff_v5: sparse block-coupling fit (potts_fit.py) per substrate, against its own
fitted null.

For each run the block x day activity matrix is discretized (q=2, sign of the
day-over-day change of log1p(count)), a sparse pairwise coupling is fitted by L1
pseudolikelihood, and the same fit is repeated on N_NULL marginal-preserving
shuffles. The readout per run is coupling sparsity, the top couplings and the
ratio of observed to null coupling mass.

Substrates, each read from the data its own harvest script caches:
  wsb_v4     validation/neff_v4/data/event__<label>.jsonl (harvest_v4.py), blocks =
             blind Louvain on the pre-onset co-thread graph, as in neff_v4
  wiki       validation/wikipedia/data/*.json (harvest.py), blocks = blind Louvain
             on the pre-onset co-editing graph, as in neff_collapse_wiki.py
  ecosystem  validation/conservation_ecosystem/weekly_counts.json (committed),
             blocks = the subreddits present in every week, rows = weeks
A run whose data file is absent is recorded as NO_DATA. The Louvain substrates
import networkx and python-louvain only when their data is present.

Emits result_potts_v5.json. Run: py -3.12 run_v5.py [--substrate all] [--k 50]
"""
import argparse
import datetime as dt
import json
import os
import sys
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
VAL = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)

import potts_fit as PF  # noqa: E402

N_NULL = 50
SEED = 20261118
Q = 2
METHOD = "diff"
WSB_DATA = os.path.join(VAL, "neff_v4", "data")
WIKI_DATA = os.path.join(VAL, "wikipedia", "data")
ECO_FILE = os.path.join(VAL, "conservation_ecosystem", "weekly_counts.json")


def daily_block_matrix(events, partition, lo, hi):
    """M[t, k] = events by members of block k on day t of [lo, hi). events: (user, date)."""
    blocks = sorted(set(partition.values()))
    bidx = {b: i for i, b in enumerate(blocks)}
    M = np.zeros(((hi - lo).days, len(blocks)))
    for user, d in events:
        b = partition.get(user)
        if b is None or d < lo or d >= hi:
            continue
        M[(d - lo).days, bidx[b]] += 1
    return M, blocks


def potts_run(M, labels, k, seed):
    S = PF.discretize(M, q=Q, method=METHOD)
    return PF.readout(S, labels=labels, k=k, seed=seed, q=Q)


def run_wsb_v4(k, seed):
    sys.path.insert(0, os.path.join(VAL, "neff_v4"))
    import roster_v4 as RV
    out = []
    for label, onset, _why in RV.all_events():
        path = os.path.join(WSB_DATA, f"event__{label}.jsonl")
        rec = dict(substrate="wsb_v4", label=label, onset=onset)
        if not os.path.exists(path):
            rec["status"] = "NO_DATA"
            out.append(rec)
            continue
        try:
            sys.path.insert(0, os.path.join(VAL, "reddit_wsb"))
            sys.path.insert(0, os.path.join(VAL, "pipeline_v03"))
            import neff_collapse_wsb as NB
            comments = NB.load_run_comments(path)
            o = dt.date.fromisoformat(onset)
            lo = o - dt.timedelta(days=RV.PRE_GRAPH_DAYS)
            hi = o + dt.timedelta(days=RV.POST_DAYS + 1)
            pre = [c for c in comments if lo <= c["date"] < o]
            G, *_ = NB.cothread_graph(pre, RV.USER_CAP, RV.THREAD_SUBSAMPLE, RV.PER_THREAD_CAP)
            part, mod, K = NB.blind_partition(G)
            rec.update(K_blocks=K, modularity=mod)
            if K < 3:
                rec["status"] = "TRIVIAL_PARTITION"
            else:
                M, blocks = daily_block_matrix(
                    ((c["author"], c["date"]) for c in comments), part, lo, hi)
                rec.update(potts_run(M, [f"b{b}" for b in blocks], k, seed))
                rec["status"] = "OK"
        except Exception as e:
            rec.update(status="ERROR", err=f"{type(e).__name__}: {e}")
        out.append(rec)
    return out


def run_wiki(k, seed):
    if not os.path.isdir(WIKI_DATA) or not any(f.endswith(".json") for f in os.listdir(WIKI_DATA)):
        return [dict(substrate="wiki", label="*", status="NO_DATA", path=WIKI_DATA)]
    sys.path.insert(0, os.path.join(VAL, "wikipedia"))
    sys.path.insert(0, os.path.join(VAL, "pipeline_v03"))
    out = []
    for f in sorted(x for x in os.listdir(WIKI_DATA) if x.endswith(".json")):
        rec = dict(substrate="wiki", label=f)
        try:
            import neff_collapse_wiki as NW
            import roster as RW
            run = json.load(open(os.path.join(WIKI_DATA, f), encoding="utf-8"))
            rec.update(label=run.get("title"), onset=run.get("onset"), arm=run.get("arm"))
            o = dt.date.fromisoformat(run["onset"])
            lo = o - dt.timedelta(days=RW.BASELINE_DAYS)
            hi = o + dt.timedelta(days=RW.POST_DAYS + 1)
            G = NW.coedit_graph(run["editor_contribs"], run["title"])
            part, mod, K = NW.blind_partition(G)
            rec.update(K_blocks=K, modularity=mod)
            if K < 3:
                rec["status"] = "TRIVIAL_PARTITION"
            else:
                events = ((rv.get("user"), NW.parse_ts(rv["ts"]).date())
                          for rv in run["focal_revs"] if rv.get("ts"))
                M, blocks = daily_block_matrix(events, part, lo, hi)
                rec.update(potts_run(M, [f"b{b}" for b in blocks], k, seed))
                rec["status"] = "OK"
        except Exception as e:
            rec.update(status="ERROR", err=f"{type(e).__name__}: {e}")
        out.append(rec)
    return out


def run_ecosystem(k, seed):
    rec = dict(substrate="ecosystem", label="finance_basket_weekly_2020_06_2021_06")
    if not os.path.exists(ECO_FILE):
        rec["status"] = "NO_DATA"
        return [rec]
    counts = json.load(open(ECO_FILE, encoding="utf-8"))
    weeks = sorted(set().union(*(set(v) for v in counts.values())))
    subs = [s for s, v in counts.items() if len(v) == len(weeks)]
    M = np.array([[counts[s][w] for s in subs] for w in weeks], dtype=float)
    rec.update(blocks=subs, weeks=[weeks[0], weeks[-1]],
               dropped_partial_blocks=sorted(set(counts) - set(subs)))
    rec.update(potts_run(M, subs, k, seed))
    rec["status"] = "OK"
    return [rec]


def summarize(runs):
    by = defaultdict(list)
    for r in runs:
        by[r["substrate"]].append(r)
    out = {}
    for sub, rs in by.items():
        ok = [r for r in rs if r.get("status") == "OK"]
        ratios = [r["obs_over_null_mass"] for r in ok if r.get("obs_over_null_mass") is not None]
        out[sub] = dict(
            n_runs=len(rs), n_ok=len(ok),
            n_no_data=sum(1 for r in rs if r.get("status") == "NO_DATA"),
            median_obs_over_null_mass=float(np.median(ratios)) if ratios else None,
            median_sparsity=float(np.median([r["sparsity"] for r in ok])) if ok else None,
            median_null_pctile_of_obs=(float(np.median([r["null_pctile_of_obs"] for r in ok]))
                                       if ok else None),
        )
    return out


RUNNERS = dict(wsb_v4=run_wsb_v4, wiki=run_wiki, ecosystem=run_ecosystem)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--substrate", choices=["all"] + list(RUNNERS), default="all")
    ap.add_argument("--k", type=int, default=N_NULL, help="shuffled refits per run")
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--out", default=os.path.join(HERE, "result_potts_v5.json"))
    a = ap.parse_args(argv)
    names = list(RUNNERS) if a.substrate == "all" else [a.substrate]
    runs = []
    for name in names:
        rs = RUNNERS[name](a.k, a.seed)
        for r in rs:
            sys.stderr.write(f"  {name:9s} {str(r.get('label')):40s} {r.get('status')} "
                             f"ratio={r.get('obs_over_null_mass')}\n")
        runs.extend(rs)
    summary = summarize(runs)
    out = dict(summary=summary, runs=runs,
               params=dict(q=Q, discretize=METHOD, n_null=a.k, seed=a.seed,
                           lam="potts_fit.default_lam: "
                               f"{PF.DEFAULT_LAM_SCALE} * sqrt(log K / T)",
                           field_ridge=PF.FIELD_RIDGE,
                           null="each block's time order permuted independently"))
    with open(a.out, "w") as fh:
        json.dump(out, fh, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
