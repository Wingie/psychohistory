"""Dynamic-N_eff-collapse analysis on r/wallstreetbets (Reddit mirror of Wikipedia
test ii', powered cross-domain). Mirrors validation/wikipedia/neff_collapse_wiki.py
EXACTLY in method and frozen thresholds; only the substrate differs.

For each frozen roster run (event + matched-calm):
  1. Build the USER co-thread graph from pre-onset comments in [onset-PRE_GRAPH_DAYS,
     onset): nodes = commenters, edge weight = # threads (link_id) both commented in
     (concordance_cothread_graph pattern from pipeline_v03). This is the Reddit analogue
     of the Wikipedia co-EDITING graph. Cap to USER_CAP most-active pre-onset commenters
     and subsample threads to THREAD_SUBSAMPLE (both logged).
  2. Blind Louvain -> frozen partition (K blocks, modularity). No outcome knowledge.
  3. Bucket the frozen blocks' COMMENT activity through time (3-day buckets), baseline
     window vs onset window, and compute N_eff:
       - PRIMARY: macro variance-ratio (engine block_metrics definition); collapses K->1.
       - SECONDARY: Pearson-Kish K/(1+(K-1)rho_bar) (legacy pipeline metric).
     collapse drop = 1 - N_eff(onset)/N_eff(baseline).
  4. Nulls: block-label shuffle (300 perms) + the matched-calm arm.
  5. Concentration: pre-onset commenter comment-count gini/hhi/top5.

Emits result_wsb_neff.json + figure_wsb_neff.png. Evaluates the FROZEN decision rule.
Run: py -3.12 neff_collapse_wsb.py
"""
import json
import os
import sys
import random
import datetime as dt
from collections import defaultdict
from itertools import combinations

import numpy as np
import networkx as nx
import community as community_louvain
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline_v03"))
import common as C  # noqa: E402  gini/hhi/top_k_share
import roster_wsb as R  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

BUCKET_DAYS = R.BUCKET_DAYS
# baseline window length before onset-3d, mirroring wiki: 2*POST_DAYS + 7
W_BASELINE_DAYS = 2 * R.POST_DAYS + 7
N_SHUFFLE = R.N_SHUFFLE
F_THRESHOLD = R.F_THRESHOLD     # frozen: min median drop
PCTILE = R.PCTILE              # frozen: fire vs shuffle null at 90th pctile
RNG = np.random.default_rng(20260616)


def load_run_comments(path):
    """Read compact jsonl -> list of dicts {author, link_id, created_utc, date}."""
    out = []
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            ts = int(r["t"])
            out.append(dict(author=r["a"], link_id=r["l"], created_utc=ts,
                            date=dt.datetime.fromtimestamp(ts, dt.timezone.utc).date()))
    return out


def cothread_graph(comments, user_cap, thread_cap, per_thread_cap, seed=42):
    """User-user weighted co-thread graph. Edge weight = # threads both commented in.
    Cap to the `user_cap` most-active commenters; subsample threads to `thread_cap`.
    To keep the edge set tractable on WSB mega-threads (a single GME-mania thread can
    contain thousands of our capped users -> O(k^2) ~ tens of millions of edges), a
    thread with > per_thread_cap of our users contributes only a random subsample of
    per_thread_cap of them to the pairing (documented subsampling; bounds edges/thread
    to ~per_thread_cap^2/2). Returns (G, n_users_pre, cap_hit, n_threads_used,
    n_threads_subsampled)."""
    # most-active commenters in the pre-onset window
    ucount = defaultdict(int)
    for c in comments:
        ucount[c["author"]] += 1
    ranked = sorted(ucount.items(), key=lambda kv: (-kv[1], kv[0]))
    cap_hit = len(ranked) > user_cap
    keep_users = set(u for u, _ in ranked[:user_cap])

    thread_members = defaultdict(set)
    for c in comments:
        if c["author"] in keep_users and c["link_id"]:
            thread_members[c["link_id"]].add(c["author"])
    # only threads with >=2 of our kept users contribute edges
    threads = [t for t, m in thread_members.items() if len(m) >= 2]
    rnd = random.Random(seed)
    if len(threads) > thread_cap:
        rnd.shuffle(threads)
        threads = threads[:thread_cap]
    n_threads_used = len(threads)

    G = nx.Graph()
    G.add_nodes_from(keep_users)
    ew = defaultdict(int)
    n_sub = 0
    for t in threads:
        m = sorted(thread_members[t])
        if len(m) > per_thread_cap:
            m = rnd.sample(m, per_thread_cap)
            m.sort()
            n_sub += 1
        for a, b in combinations(m, 2):
            ew[(a, b)] += 1
    for (a, b), w in ew.items():
        G.add_edge(a, b, weight=w)
    return G, len(ucount), cap_hit, n_threads_used, n_sub


def blind_partition(G):
    if G.number_of_edges() == 0:
        return {}, float("nan"), 0
    comps = sorted(nx.connected_components(G), key=len, reverse=True)
    GC = G.subgraph(comps[0]).copy()
    part = community_louvain.best_partition(GC, weight="weight", random_state=42)
    mod = community_louvain.modularity(part, GC, weight="weight")
    return part, float(mod), len(set(part.values()))


def block_bucket_matrix(comments, partition, lo, hi):
    """M[t,k] = # comments by block-k members in bucket t over [lo,hi)."""
    nb = int((hi - lo).days // BUCKET_DAYS) + 1
    blocks = sorted(set(partition.values()))
    bidx = {b: i for i, b in enumerate(blocks)}
    M = np.zeros((nb, len(blocks)))
    for c in comments:
        u = c["author"]
        if u not in partition:
            continue
        d = c["date"]
        if d < lo or d >= hi:
            continue
        t = (d - lo).days // BUCKET_DAYS
        if 0 <= t < nb:
            M[t, bidx[partition[u]]] += 1
    return M, blocks


def neff_macro(M_window, full_mean):
    """Canonical macro variance-ratio N_eff; each block normalized by its
    full-trajectory mean. ->K independent, ->1 synchronized."""
    active = full_mean > 0
    Mw = M_window[:, active]
    fm = full_mean[active]
    K = Mw.shape[1]
    if K < 2 or Mw.shape[0] < 3:
        return float(K), K
    R_ = Mw / fm
    var_single = float(np.mean(np.var(R_, axis=0)))
    var_mean = float(np.var(R_.mean(axis=1)))
    if var_mean <= 1e-12:
        return float(K), K
    return float(np.clip(var_single / var_mean, 1.0, K)), K


def neff_pearson(M_window):
    """Legacy Pearson-Kish on the block x time window matrix."""
    stds = M_window.std(axis=0)
    Mk = M_window[:, stds > 1e-12]
    K = Mk.shape[1]
    if K < 2 or Mk.shape[0] < 3:
        return float(max(K, 1))
    Rm = np.corrcoef(Mk.T)
    off = Rm[np.triu_indices_from(Rm, k=1)]
    off = off[~np.isnan(off)]
    rho = float(np.mean(np.abs(off))) if off.size else 0.0
    return float(K / (1.0 + (K - 1) * rho))


def build_user_window_matrices(comments, user_index, windows):
    """Single pass over comments -> a per-USER bucket matrix for EACH window.
    windows: list of (lo, hi). Returns list of np.ndarray (n_users x n_buckets).
    Only counts comments whose author is in user_index. np.add.at vectorization."""
    nu = len(user_index)
    nbs = [int((hi - lo).days // BUCKET_DAYS) + 1 for lo, hi in windows]
    rows = [[] for _ in windows]
    cols = [[] for _ in windows]
    for c in comments:
        ui = user_index.get(c["author"])
        if ui is None:
            continue
        d = c["date"]
        for wi, (lo, hi) in enumerate(windows):
            if d < lo or d >= hi:
                continue
            t = (d - lo).days // BUCKET_DAYS
            if 0 <= t < nbs[wi]:
                rows[wi].append(ui)
                cols[wi].append(t)
    mats = []
    for wi, nb in enumerate(nbs):
        U = np.zeros((nu, nb))
        if rows[wi]:
            np.add.at(U, (np.asarray(rows[wi]), np.asarray(cols[wi])), 1.0)
        mats.append(U)
    return mats


def _collapse_from_user_mats(Uf, Ub, Uo, block_vec, n_blocks):
    """Given per-user bucket matrices (nu x nb) for full/base/onset windows and a
    block assignment vector block_vec (len nu, values 0..n_blocks-1), aggregate to
    block x time matrices and compute the macro + Pearson collapse. Pure numpy."""
    # B: (nu x n_blocks) one-hot
    nu = block_vec.shape[0]
    B = np.zeros((nu, n_blocks))
    B[np.arange(nu), block_vec] = 1.0
    Mfull = Uf.T @ B   # (nbf x n_blocks)
    Mb = Ub.T @ B
    Mo = Uo.T @ B
    full_mean = Mfull.mean(axis=0)
    nb_macro, kb = neff_macro(Mb, full_mean)
    no_macro, ko = neff_macro(Mo, full_mean)
    nb_p, no_p = neff_pearson(Mb), neff_pearson(Mo)
    drop = 1.0 - (no_macro / nb_macro) if nb_macro > 0 else float("nan")
    drop_p = 1.0 - (no_p / nb_p) if nb_p > 0 else float("nan")
    return dict(neff_base_macro=nb_macro, neff_onset_macro=no_macro, drop_macro=drop,
                neff_base_pearson=nb_p, neff_onset_pearson=no_p, drop_pearson=drop_p,
                k_active=int(min(kb, ko)))


def analyze_run(label, onset_iso, arm, comments):
    onset = dt.date.fromisoformat(onset_iso)
    lo_full = onset - dt.timedelta(days=R.BASELINE_DAYS)
    hi_full = onset + dt.timedelta(days=R.POST_DAYS + 1)
    base_lo = onset - dt.timedelta(days=W_BASELINE_DAYS + 7)
    base_hi = onset - dt.timedelta(days=7)
    onset_lo = onset - dt.timedelta(days=3)
    onset_hi = onset + dt.timedelta(days=R.POST_DAYS + 1)

    # pre-onset graph from comments strictly BEFORE onset within the graph window
    pre = [c for c in comments if lo_full <= c["date"] < onset]
    G, n_users_pre, cap_hit, n_threads, n_sub = cothread_graph(
        pre, R.USER_CAP, R.THREAD_SUBSAMPLE, R.PER_THREAD_CAP)
    part, mod, K = blind_partition(G)
    out = dict(label=label, onset=onset_iso, arm=arm, K_blocks=K, modularity=mod,
               n_nodes=G.number_of_nodes(), n_edges=G.number_of_edges(),
               n_users_pre=n_users_pre, user_cap_hit=cap_hit,
               n_threads_used=n_threads, n_threads_subsampled=n_sub,
               n_comments_total=len(comments), n_comments_pre=len(pre))
    if K < 3:
        out["status"] = "TRIVIAL_PARTITION"
        return out

    # Precompute per-USER bucket matrices ONCE for the three windows; the observed
    # collapse and all 300 shuffles are then pure numpy on these (block reassignment =
    # a one-hot matmul). This is the only way to keep 300 shuffles tractable on the
    # huge WSB comment files (one bucketing pass over comments instead of 300).
    nodes = list(part.keys())
    user_index = {u: i for i, u in enumerate(nodes)}
    block_of = np.array([part[u] for u in nodes])
    blocks_sorted = sorted(set(part.values()))
    bremap = {b: i for i, b in enumerate(blocks_sorted)}
    block_vec0 = np.array([bremap[b] for b in block_of])
    n_blocks = len(blocks_sorted)

    Uf, Ub, Uo = build_user_window_matrices(
        comments, user_index,
        [(lo_full, hi_full), (base_lo, base_hi), (onset_lo, onset_hi)])

    base = _collapse_from_user_mats(Uf, Ub, Uo, block_vec0, n_blocks)
    out.update(base)
    out["status"] = "OK"

    # block-label shuffle null on the macro drop (permute block_vec only)
    null = []
    for _ in range(N_SHUFFLE):
        perm = RNG.permutation(block_vec0)
        d = _collapse_from_user_mats(Uf, Ub, Uo, perm, n_blocks)["drop_macro"]
        if not (isinstance(d, float) and np.isnan(d)):
            null.append(d)
    out["shuffle_null_p90"] = float(np.percentile(null, 90)) if null else None
    out["shuffle_pctile_of_obs"] = (float(np.mean([d < base["drop_macro"] for d in null]))
                                    if null and not np.isnan(base["drop_macro"]) else None)
    out["fires_vs_shuffle"] = bool(out["shuffle_pctile_of_obs"] is not None
                                   and out["shuffle_pctile_of_obs"] >= PCTILE)

    # concentration: pre-onset commenter comment counts
    pre_counts = defaultdict(int)
    for c in pre:
        pre_counts[c["author"]] += 1
    counts = list(pre_counts.values())
    out["user_gini_pre"] = C.gini(counts) if counts else None
    out["user_hhi_pre"] = C.hhi(counts) if counts else None
    out["user_top5_pre"] = C.top_k_share(counts, 0.05) if counts else None
    return out


def main():
    results = []
    for label, onset, arm in R.all_runs():
        suffix = label if arm == "event" else label  # label already carries __calm
        # harvest wrote files as <label>__<arm>.jsonl where label for calm = base+'__calm'
        path = os.path.join(DATA, f"{label}__{arm}.jsonl")
        comments = load_run_comments(path)
        if not comments:
            results.append(dict(label=label, onset=onset, arm=arm, status="NO_DATA"))
            sys.stderr.write(f"  {label:26s} [{arm}] NO_DATA ({path})\n")
            continue
        try:
            r = analyze_run(label, onset, arm, comments)
        except Exception as e:
            r = dict(label=label, onset=onset, arm=arm, status="ERROR", err=str(e))
        results.append(r)
        sys.stderr.write(f"  {label:26s} [{arm}] {r.get('status')} "
                         f"K={r.get('K_blocks')} mod={r.get('modularity')} "
                         f"drop={r.get('drop_macro')} fires={r.get('fires_vs_shuffle')}\n")

    ev = [r for r in results if r.get("arm") == "event" and r.get("status") == "OK"]
    ca = [r for r in results if r.get("arm") == "calm" and r.get("status") == "OK"]
    ev_drops = [r["drop_macro"] for r in ev if r.get("drop_macro") is not None
                and not np.isnan(r["drop_macro"])]
    ca_drops = [r["drop_macro"] for r in ca if r.get("drop_macro") is not None
                and not np.isnan(r["drop_macro"])]
    fires = [r for r in ev if r.get("fires_vs_shuffle")]

    median_ev = float(np.median(ev_drops)) if ev_drops else None
    frac_fire = (len(fires) / len(ev)) if ev else None
    calm_p90 = float(np.percentile(ca_drops, 90)) if ca_drops else None

    mw_p = wil_p = n_paired = None
    try:
        from scipy.stats import mannwhitneyu, wilcoxon
        if ev_drops and ca_drops:
            mw_p = float(mannwhitneyu(ev_drops, ca_drops, alternative="greater").pvalue)
        pairs = {}
        for r in ev:
            pairs.setdefault(r["label"], {})["e"] = r.get("drop_macro")
        for r in ca:
            base = r["label"][:-6] if r["label"].endswith("__calm") else r["label"]
            pairs.setdefault(base, {})["c"] = r.get("drop_macro")
        matched = [(v["e"], v["c"]) for v in pairs.values()
                   if v.get("e") is not None and v.get("c") is not None
                   and not np.isnan(v["e"]) and not np.isnan(v["c"])]
        n_paired = len(matched)
        if n_paired >= 6:
            wil_p = float(wilcoxon([e for e, _ in matched], [c for _, c in matched],
                                   alternative="greater").pvalue)
    except Exception as e:
        sys.stderr.write(f"  (supplementary stats skipped: {e})\n")

    cond1 = median_ev is not None and median_ev >= F_THRESHOLD
    cond2 = frac_fire is not None and frac_fire >= 0.5
    cond3 = (median_ev is not None and calm_p90 is not None and median_ev > calm_p90)
    powered = len(ev) >= 8
    supported = bool(cond1 and cond2 and cond3 and powered)

    summary = dict(
        substrate="r/wallstreetbets comments (subreddits24 dump)",
        n_event_ok=len(ev), n_calm_ok=len(ca), n_event_powered=powered,
        median_event_drop_macro=median_ev, frac_event_fires_vs_shuffle=frac_fire,
        n_event_fires=len(fires),
        median_calm_drop_macro=(float(np.median(ca_drops)) if ca_drops else None),
        calm_drop_p90=calm_p90,
        event_vs_calm_mannwhitney_p=mw_p, paired_wilcoxon_p=wil_p, n_paired=n_paired,
        thresholds=dict(f=F_THRESHOLD, fire_pctile=PCTILE, min_n=8),
        decision=dict(cond1_median_drop=cond1, cond2_half_fire=cond2,
                      cond3_beats_calm=cond3, powered_n8=powered),
        VERDICT="SUPPORTED (powered cross-domain)" if supported else "NOT SUPPORTED / negative",
    )
    out = dict(summary=summary, runs=results,
               params=dict(bucket_days=BUCKET_DAYS, n_shuffle=N_SHUFFLE,
                           pre_graph_days=R.PRE_GRAPH_DAYS, post_days=R.POST_DAYS,
                           user_cap=R.USER_CAP, thread_subsample=R.THREAD_SUBSAMPLE,
                           per_thread_cap=R.PER_THREAD_CAP,
                           metric_primary="macro variance-ratio (canonical)",
                           metric_secondary="Pearson-Kish (legacy)"))
    json.dump(out, open(os.path.join(HERE, "result_wsb_neff.json"), "w"), indent=2)
    make_figure(results, summary)
    print(json.dumps(summary, indent=2))


def make_figure(results, summary):
    ev = [r for r in results if r.get("arm") == "event" and r.get("status") == "OK"]
    ca = [r for r in results if r.get("arm") == "calm" and r.get("status") == "OK"]
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    ev2 = sorted(ev, key=lambda r: -(r.get("drop_macro") or 0))
    names = [r["label"] for r in ev2]
    drops = [r.get("drop_macro") or 0 for r in ev2]
    p90 = [r.get("shuffle_null_p90") or 0 for r in ev2]
    y = np.arange(len(names))
    ax[0].barh(y, drops, color="#8e44ad", label="event N_eff drop")
    ax[0].plot(p90, y, "k.", label="shuffle-null p90")
    ax[0].axvline(F_THRESHOLD, ls="--", c="r", label=f"f={F_THRESHOLD}")
    ax[0].set_yticks(y); ax[0].set_yticklabels(names, fontsize=7)
    ax[0].set_xlabel("canonical N_eff collapse drop (1 - onset/baseline)")
    ax[0].set_title("Per-event dynamic N_eff collapse (WSB)", fontsize=10)
    ax[0].legend(fontsize=8)
    ev_d = [r["drop_macro"] for r in ev if r.get("drop_macro") is not None]
    ca_d = [r["drop_macro"] for r in ca if r.get("drop_macro") is not None]
    ax[1].hist(ev_d, bins=10, alpha=0.6, color="#8e44ad", label=f"event (n={len(ev_d)})")
    ax[1].hist(ca_d, bins=10, alpha=0.6, color="#16a085", label=f"calm null (n={len(ca_d)})")
    ax[1].axvline(F_THRESHOLD, ls="--", c="r")
    ax[1].set_xlabel("N_eff collapse drop"); ax[1].set_ylabel("events")
    ax[1].set_title(f"Event vs matched-calm null\nVERDICT: {summary['VERDICT']}", fontsize=10)
    ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "figure_wsb_neff.png"), dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
