"""OBJ 2 - blind_neff_collapse.py  (L2/L6 observation operator)

Removes the post-hoc basket-selection bias of the v0.2 GME counterfactual (which
RESULTS.md flagged: the six tickers were chosen *because* they are the known meme
basket -> hypothesis-confirming by construction). Instead we run BLIND community
detection on a PRE-ONSET interaction graph -> the blocks K are discovered from
structure, with no outcome knowledge. We then freeze that partition and track the
Kish effective number of independent blocks

        N_eff = K / (1 + (K-1) * rho_bar)

where rho_bar is the mean off-diagonal cross-block activity correlation, as the
window advances toward / into the onset. Near-decomposability claim = blocks were
statistically DISTINCT before locking (high modularity, low cross-block corr);
collapse = N_eff falls across the onset (synchronization).

Substrates:
  (a) GitHub: nodes = contributors; edge weight = number of (repo,week) cells in
      which both contributed commits within the pre-onset window. (A co-commit
      / co-activity graph projected onto contributors.)
  (b) AskEconomics: nodes = users; edge weight = number of comment threads
      (link_id) in which both authored a comment (co-participation).

Honest about graph-construction choices and small n. Pure transforms.
"""
import json
import os
import datetime as dt
from collections import defaultdict
from itertools import combinations

import numpy as np
import networkx as nx
import community as community_louvain
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import common as C

HERE = os.path.dirname(os.path.abspath(__file__))


# ----------------------------------------------------------- graph builders --
def github_cocommit_graph(weeks_window):
    """weeks_window: list of (repo, week_date). Build a contributor-contributor
    weighted graph; edge weight = # of (repo,week) cells both were active in."""
    cell_members = defaultdict(set)  # (repo,week) -> {login}
    for repo, wk in weeks_window:
        wc = _GH_CACHE.setdefault(repo, C.github_author_week_commits(repo))
        for login in wc.get(wk, {}):
            cell_members[(repo, wk)].add(login)
    G = nx.Graph()
    edge_w = defaultdict(int)
    for members in cell_members.values():
        for a, b in combinations(sorted(members), 2):
            edge_w[(a, b)] += 1
        for m in members:
            G.add_node(m)
    for (a, b), w in edge_w.items():
        G.add_edge(a, b, weight=w)
    return G


_GH_CACHE = {}


def concordance_cothread_graph(comments):
    """comments: list of dicts with author/link_id. Edge weight = # threads in
    which both authored a comment."""
    thread_members = defaultdict(set)
    for c in comments:
        if c.get("link_id"):
            thread_members[c["link_id"]].add(c["author"])
    G = nx.Graph()
    edge_w = defaultdict(int)
    for members in thread_members.values():
        for m in members:
            G.add_node(m)
        for a, b in combinations(sorted(members), 2):
            edge_w[(a, b)] += 1
    for (a, b), w in edge_w.items():
        G.add_edge(a, b, weight=w)
    return G


# ----------------------------------------------------- partition + N_eff -----
def blind_partition(G):
    """Louvain on G. Returns (partition dict, modularity, K) for the largest
    connected component (community detection on a disconnected graph just bundles
    isolates)."""
    if G.number_of_edges() == 0:
        return {}, float("nan"), 0
    # operate on giant component for a meaningful modularity
    comps = sorted(nx.connected_components(G), key=len, reverse=True)
    GC = G.subgraph(comps[0]).copy()
    part = community_louvain.best_partition(GC, weight="weight", random_state=42)
    mod = community_louvain.modularity(part, GC, weight="weight")
    K = len(set(part.values()))
    return part, float(mod), int(K)


def block_activity_series(partition, activity_by_actor):
    """activity_by_actor: {actor: scalar activity in some sub-window}.
    Returns {block_id: total activity}."""
    out = defaultdict(float)
    for actor, blk in partition.items():
        out[blk] += activity_by_actor.get(actor, 0.0)
    return dict(out)


def neff_from_blocks(block_series_over_time):
    """block_series_over_time: list of {block_id: activity} dicts (one per
    sub-window). Build the block x time matrix, Pearson-correlate blocks, take
    mean off-diagonal rho_bar, return Kish N_eff = K/(1+(K-1)*rho_bar)."""
    blocks = sorted({b for d in block_series_over_time for b in d})
    K = len(blocks)
    if K < 2 or len(block_series_over_time) < 3:
        return dict(K=K, rho_bar=float("nan"), n_eff=float(K))
    M = np.array([[d.get(b, 0.0) for b in blocks] for d in block_series_over_time], float)
    # correlate columns (blocks) across time rows
    stds = M.std(axis=0)
    keep = stds > 1e-12
    Mk = M[:, keep]
    if Mk.shape[1] < 2:
        return dict(K=K, rho_bar=float("nan"), n_eff=float(K))
    R = np.corrcoef(Mk.T)
    off = R[np.triu_indices_from(R, k=1)]
    off = off[~np.isnan(off)]
    rho_bar = float(np.mean(np.abs(off))) if off.size else 0.0
    Kk = Mk.shape[1]
    n_eff = Kk / (1.0 + (Kk - 1) * rho_bar)
    return dict(K=int(Kk), rho_bar=rho_bar, n_eff=float(n_eff))


# --------------------------------------------------------------- runners -----
def run_github(repo, onset, pre_weeks=5, sub=2):
    """Establish blocks on the pre-onset slice (blind), then advance toward/into
    onset measuring N_eff over rolling sub-windows of `sub` weeks each."""
    wc = C.github_author_week_commits(repo)
    _GH_CACHE[repo] = wc
    weeks = sorted(wc.keys())
    if onset not in weeks:
        onset = min(weeks, key=lambda w: abs((w - onset).days))
    oi = weeks.index(onset)
    if oi < pre_weeks:
        return dict(substrate="github:" + repo, status="NO_PRE_WINDOW",
                    weeks_pre=oi, onset=str(onset))
    pre_slice = weeks[oi - pre_weeks:oi]
    G_pre = github_cocommit_graph([(repo, w) for w in pre_slice])
    part, mod, K = blind_partition(G_pre)
    if K < 2:
        return dict(substrate="github:" + repo, status="TRIVIAL_PARTITION",
                    K=K, modularity=mod, onset=str(onset), n_nodes=G_pre.number_of_nodes())

    # trajectory: sub-windows from pre-onset through onset+pre_weeks
    traj = []
    lo = oi - pre_weeks
    hi = min(len(weeks), oi + pre_weeks)
    centers = list(range(lo + sub, hi + 1, sub))
    for cidx, end in enumerate(centers):
        seg = weeks[end - sub:end]
        # per-sub-window block activity series (need >=3 micro-buckets for corr)
        micro = []
        for w in seg:
            micro.append(block_activity_series(part, wc.get(w, {})))
        # widen if too few buckets: use last `max(3,sub)` weeks ending at `end`
        wide = weeks[max(0, end - max(3, sub)):end]
        micro = [block_activity_series(part, wc.get(w, {})) for w in wide]
        ne = neff_from_blocks(micro)
        midweek = weeks[min(end, len(weeks)) - 1]
        traj.append(dict(end_week=str(midweek),
                         offset_from_onset=int(end - 1 - oi),
                         **ne))
    return dict(substrate="github:" + repo, status="OK", onset=str(onset),
                K_blocks=K, modularity_pre=mod, n_nodes_pre=G_pre.number_of_nodes(),
                n_edges_pre=G_pre.number_of_edges(), trajectory=traj)


def run_concordance(onset, pre_weeks=8, sub=3):
    comments = C.load_concordance_comments()
    by_week = defaultdict(list)
    for c in comments:
        by_week[c["week"]].append(c)
    weeks = sorted(by_week.keys())
    if onset not in weeks:
        onset = min(weeks, key=lambda w: abs((w - onset).days))
    oi = weeks.index(onset)
    if oi < pre_weeks:
        return dict(substrate="askeconomics", status="NO_PRE_WINDOW", onset=str(onset))
    pre_comments = [c for w in weeks[oi - pre_weeks:oi] for c in by_week[w]]
    G_pre = concordance_cothread_graph(pre_comments)
    part, mod, K = blind_partition(G_pre)
    if K < 2:
        return dict(substrate="askeconomics", status="TRIVIAL_PARTITION",
                    K=K, modularity=mod, onset=str(onset), n_nodes=G_pre.number_of_nodes())

    # activity per actor per week = comment count
    week_actor = defaultdict(lambda: defaultdict(int))
    for c in comments:
        week_actor[c["week"]][c["author"]] += 1

    traj = []
    lo = oi - pre_weeks
    hi = min(len(weeks), oi + pre_weeks)
    for end in range(lo + sub, hi + 1, sub):
        wide = weeks[max(0, end - max(3, sub)):end]
        micro = [block_activity_series(part, dict(week_actor.get(w, {}))) for w in wide]
        ne = neff_from_blocks(micro)
        traj.append(dict(end_week=str(weeks[min(end, len(weeks)) - 1]),
                         offset_from_onset=int(end - 1 - oi), **ne))
    return dict(substrate="askeconomics", status="OK", onset=str(onset),
                K_blocks=K, modularity_pre=mod, n_nodes_pre=G_pre.number_of_nodes(),
                n_edges_pre=G_pre.number_of_edges(), trajectory=traj)


def neff_collapse_metric(rec):
    """Pre-onset mean N_eff vs onset-window mean N_eff -> collapse ratio."""
    if rec.get("status") != "OK":
        return rec
    pre = [t["n_eff"] for t in rec["trajectory"] if t["offset_from_onset"] < 0 and not np.isnan(t["n_eff"])]
    post = [t["n_eff"] for t in rec["trajectory"] if t["offset_from_onset"] >= 0 and not np.isnan(t["n_eff"])]
    rec["neff_pre_mean"] = float(np.mean(pre)) if pre else None
    rec["neff_onset_mean"] = float(np.mean(post)) if post else None
    if pre and post and np.mean(pre) > 0:
        rec["neff_collapse_ratio"] = float(np.mean(post) / np.mean(pre))
        rec["collapsed"] = bool(np.mean(post) < np.mean(pre))
    else:
        rec["neff_collapse_ratio"] = None
        rec["collapsed"] = None
    return rec


def run():
    results = {"params": dict(pre_weeks_github=5, pre_weeks_reddit=8,
                              note="blind Louvain on pre-onset graph; freeze partition; track Kish N_eff"),
               "github": [], "askeconomics": []}
    for repo in C.GITHUB_REPOS:
        if repo not in C.GITHUB_ONSETS:
            continue
        rec = neff_collapse_metric(run_github(repo, C.to_date(C.GITHUB_ONSETS[repo])))
        results["github"].append(rec)

    wc = C.concordance_author_week_counts()
    onset = max(sorted(wc.keys()), key=lambda w: sum(wc[w].values()))
    rec = neff_collapse_metric(run_concordance(onset))
    rec["onset_note"] = "designated onset = peak comment-activity week (thread-sampled span)"
    results["askeconomics"].append(rec)

    with open(os.path.join(HERE, "result_blind_neff.json"), "w") as f:
        json.dump(results, f, indent=2)
    make_figure(results)
    return results


def make_figure(results):
    ok = [r for r in results["github"] + results["askeconomics"] if r.get("status") == "OK"]
    n = len(ok)
    if n == 0:
        return
    fig, axes = plt.subplots(1, n, figsize=(4 * n, 4.2), squeeze=False)
    for ax, rec in zip(axes[0], ok):
        xs = [t["offset_from_onset"] for t in rec["trajectory"]]
        ys = [t["n_eff"] for t in rec["trajectory"]]
        ax.plot(xs, ys, "-o", ms=4, color="#8e44ad")
        ax.axvline(0, ls="--", c="r", alpha=0.7, label="onset")
        ax.axhline(rec["K_blocks"], ls=":", c="gray", alpha=0.6,
                   label=f"K={rec['K_blocks']} (full indep.)")
        ax.set_title(f"{rec['substrate']}\nmod={rec['modularity_pre']:.2f} "
                     f"collapse={rec.get('neff_collapse_ratio')}", fontsize=8)
        ax.set_xlabel("weeks from onset")
        ax.set_ylabel("Kish N_eff")
        ax.legend(fontsize=7)
    fig.suptitle("OBJ2: blind-partition N_eff trajectory across onset", fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "figure_blind_neff.png"), dpi=110)
    plt.close(fig)


if __name__ == "__main__":
    r = run()
    for rec in r["github"] + r["askeconomics"]:
        if rec.get("status") == "OK":
            print(f"{rec['substrate']:22s} K={rec['K_blocks']} mod={rec['modularity_pre']:.3f} "
                  f"nodes={rec['n_nodes_pre']} Neff_pre={rec.get('neff_pre_mean')} "
                  f"Neff_onset={rec.get('neff_onset_mean')} collapse={rec.get('neff_collapse_ratio')} "
                  f"collapsed={rec.get('collapsed')}")
        else:
            print(f"{rec['substrate']:22s} {rec['status']} {rec.get('modularity','')}")
