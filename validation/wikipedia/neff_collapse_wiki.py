"""Dynamic-N_eff-collapse analysis on Wikipedia (test ii', powered cross-domain).

For each frozen roster run (event + matched-calm):
  1. Build the editor co-editing graph from pre-onset usercontribs (edge = co-edited
     >=1 OTHER article; the FOCAL article is EXCLUDED so blocks come from genuinely
     distinct interests, not the trivial everyone-edits-the-focal clique).
  2. Blind Louvain -> frozen partition (K blocks, modularity). No outcome knowledge.
  3. Bucket the frozen blocks' edit activity ON THE FOCAL article through time, and
     compute N_eff in a baseline window vs an onset window:
       - PRIMARY: macro variance-ratio (engine block_metrics definition), counts
         normalized by each block's full-trajectory mean. Collapses K->1 under synchrony.
       - SECONDARY: Pearson-Kish K/(1+(K-1)rho_bar) (the legacy pipeline metric).
     collapse drop = 1 - N_eff(onset)/N_eff(baseline).
  4. Nulls: block-label shuffle (>=200 perms) + the matched-calm arm.
  5. Concentration (Upgrade-3 cross-domain): editor edit-count gini/hhi/top5 pre-onset.

Emits result_wiki_neff.json + figure_wiki_neff.png. Evaluates the FROZEN decision rule
from PRE_REGISTRATION_wiki.md. Run: py -3.12 neff_collapse_wiki.py
"""
import json
import os
import sys
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
import common as C  # noqa: E402  gini/hhi/top_k_share/percentile_rank
import roster as R  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")

BUCKET_DAYS = 3
W_BASELINE_DAYS = 2 * R.POST_DAYS + 7   # baseline window length before onset-7d
N_SHUFFLE = 300
F_THRESHOLD = 0.30      # frozen: min median drop
PCTILE = 0.90           # frozen: fire vs shuffle null at 90th pctile
RNG = np.random.default_rng(20260616)


def parse_ts(ts):
    return dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")


def coedit_graph(editor_contribs, focal_title):
    """editor-editor weighted graph; edge weight = # OTHER articles co-edited.
    Focal article excluded so blocks reflect distinct interests, not the focal clique."""
    article_editors = defaultdict(set)
    for ed, contribs in editor_contribs.items():
        for c in contribs:
            t = c.get("title")
            if t and t != focal_title:
                article_editors[t].add(ed)
    G = nx.Graph()
    G.add_nodes_from(editor_contribs.keys())
    ew = defaultdict(int)
    for t, eds in article_editors.items():
        if len(eds) < 2:
            continue
        for a, b in combinations(sorted(eds), 2):
            ew[(a, b)] += 1
    for (a, b), w in ew.items():
        G.add_edge(a, b, weight=w)
    return G


def blind_partition(G):
    if G.number_of_edges() == 0:
        return {}, float("nan"), 0
    comps = sorted(nx.connected_components(G), key=len, reverse=True)
    GC = G.subgraph(comps[0]).copy()
    part = community_louvain.best_partition(GC, weight="weight", random_state=42)
    mod = community_louvain.modularity(part, GC, weight="weight")
    return part, float(mod), len(set(part.values()))


def block_bucket_matrix(focal_revs, partition, onset, lo, hi):
    """Return (M, blocks): M[t,k] = focal edits by block k in bucket t over [lo,hi)."""
    nb = int((hi - lo).days // BUCKET_DAYS) + 1
    blocks = sorted(set(partition.values()))
    bidx = {b: i for i, b in enumerate(blocks)}
    M = np.zeros((nb, len(blocks)))
    for rv in focal_revs:
        u = rv.get("user")
        if u not in partition:
            continue
        ts = rv.get("ts")
        if not ts:
            continue
        d = parse_ts(ts).date()
        if d < lo or d >= hi:
            continue
        t = (d - lo).days // BUCKET_DAYS
        if 0 <= t < nb:
            M[t, bidx[partition[u]]] += 1
    return M, blocks


def neff_macro(M_window, full_mean):
    """Canonical macro variance-ratio N_eff on counts, each block normalized by its
    full-trajectory mean. var_single/var_mean; ->K independent, ->1 synchronized."""
    active = full_mean > 0
    Mw = M_window[:, active]
    fm = full_mean[active]
    K = Mw.shape[1]
    if K < 2 or Mw.shape[0] < 3:
        return float(K), K
    R_ = Mw / fm  # relative activity, blocks comparable
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


def collapse_for_partition(focal_revs, partition, onset, lo_full, hi_full,
                           base_lo, base_hi, onset_lo, onset_hi):
    Mfull, blocks = block_bucket_matrix(focal_revs, partition, onset, lo_full, hi_full)
    full_mean = Mfull.mean(axis=0)
    Mb, _ = block_bucket_matrix(focal_revs, partition, onset, base_lo, base_hi)
    Mo, _ = block_bucket_matrix(focal_revs, partition, onset, onset_lo, onset_hi)
    nb_macro, kb = neff_macro(Mb, full_mean)
    no_macro, ko = neff_macro(Mo, full_mean)
    nb_p, no_p = neff_pearson(Mb), neff_pearson(Mo)
    drop = 1.0 - (no_macro / nb_macro) if nb_macro > 0 else float("nan")
    drop_p = 1.0 - (no_p / nb_p) if nb_p > 0 else float("nan")
    return dict(neff_base_macro=nb_macro, neff_onset_macro=no_macro, drop_macro=drop,
                neff_base_pearson=nb_p, neff_onset_pearson=no_p, drop_pearson=drop_p,
                k_active=int(min(kb, ko)))


def analyze_run(rec):
    title, onset_iso, arm = rec["title"], rec["onset"], rec["arm"]
    onset = dt.date.fromisoformat(onset_iso)
    lo_full = onset - dt.timedelta(days=R.BASELINE_DAYS)
    hi_full = onset + dt.timedelta(days=R.POST_DAYS + 1)
    base_lo = onset - dt.timedelta(days=W_BASELINE_DAYS + 7)
    base_hi = onset - dt.timedelta(days=7)
    onset_lo = onset - dt.timedelta(days=3)
    onset_hi = onset + dt.timedelta(days=R.POST_DAYS + 1)

    G = coedit_graph(rec["editor_contribs"], title)
    part, mod, K = blind_partition(G)
    out = dict(title=title, onset=onset_iso, arm=arm, K_blocks=K, modularity=mod,
               n_nodes=G.number_of_nodes(), n_edges=G.number_of_edges(),
               n_editors=rec.get("n_editors"), editor_cap_hit=rec.get("editor_cap_hit"))
    if K < 3:
        out["status"] = "TRIVIAL_PARTITION"
        return out

    base = collapse_for_partition(rec["focal_revs"], part, onset, lo_full, hi_full,
                                  base_lo, base_hi, onset_lo, onset_hi)
    out.update(base)
    out["status"] = "OK"

    # block-label shuffle null on the macro drop
    nodes = list(part.keys())
    labels = np.array([part[n] for n in nodes])
    null = []
    for _ in range(N_SHUFFLE):
        perm = RNG.permutation(labels)
        shuf = {nodes[i]: int(perm[i]) for i in range(len(nodes))}
        d = collapse_for_partition(rec["focal_revs"], shuf, onset, lo_full, hi_full,
                                   base_lo, base_hi, onset_lo, onset_hi)["drop_macro"]
        if not (isinstance(d, float) and np.isnan(d)):
            null.append(d)
    out["shuffle_null_p90"] = float(np.percentile(null, 90)) if null else None
    out["shuffle_pctile_of_obs"] = (float(np.mean([d < base["drop_macro"] for d in null]))
                                    if null and not np.isnan(base["drop_macro"]) else None)
    out["fires_vs_shuffle"] = bool(out["shuffle_pctile_of_obs"] is not None
                                   and out["shuffle_pctile_of_obs"] >= PCTILE)

    # concentration (Upgrade-3 cross-domain): pre-onset editor edit counts on focal
    pre_counts = defaultdict(int)
    for rv in rec["focal_revs"]:
        ts = rv.get("ts")
        if ts and base_lo <= parse_ts(ts).date() < onset:
            pre_counts[rv["user"]] += 1
    counts = list(pre_counts.values())
    out["editor_gini_pre"] = C.gini(counts) if counts else None
    out["editor_hhi_pre"] = C.hhi(counts) if counts else None
    out["editor_top5_pre"] = C.top_k_share(counts, 0.05) if counts else None
    return out


def main():
    files = sorted(f for f in os.listdir(DATA) if f.endswith(".json"))
    runs = [json.load(open(os.path.join(DATA, f), encoding="utf-8")) for f in files]
    sys.stderr.write(f"analyzing {len(runs)} cached runs\n")
    results = []
    for rec in runs:
        try:
            r = analyze_run(rec)
        except Exception as e:
            r = dict(title=rec.get("title"), arm=rec.get("arm"), status="ERROR", err=str(e))
        results.append(r)
        sys.stderr.write(f"  {r.get('title'):24s} [{r.get('arm')}] {r.get('status')} "
                         f"K={r.get('K_blocks')} drop={r.get('drop_macro')}\n")

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

    # SUPPLEMENTARY (not part of the frozen decision): quantify the event-vs-calm
    # separation that is the primary directional prediction.
    mw_p = wil_p = n_paired = None
    try:
        from scipy.stats import mannwhitneyu, wilcoxon
        if ev_drops and ca_drops:
            mw_p = float(mannwhitneyu(ev_drops, ca_drops, alternative="greater").pvalue)
        pairs = {}
        for r in ev:
            pairs.setdefault(r["title"], {})["e"] = r.get("drop_macro")
        for r in ca:
            pairs.setdefault(r["title"], {})["c"] = r.get("drop_macro")
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
        n_event_ok=len(ev), n_calm_ok=len(cca) if (cca := ca) else 0,
        n_event_powered=powered,
        median_event_drop_macro=median_ev, frac_event_fires_vs_shuffle=frac_fire,
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
                           baseline_days=R.BASELINE_DAYS, post_days=R.POST_DAYS,
                           metric_primary="macro variance-ratio (canonical)",
                           metric_secondary="Pearson-Kish (legacy)"))
    json.dump(out, open(os.path.join(HERE, "result_wiki_neff.json"), "w"), indent=2)
    make_figure(results, summary)
    print(json.dumps(summary, indent=2))


def make_figure(results, summary):
    ev = [r for r in results if r.get("arm") == "event" and r.get("status") == "OK"]
    ca = [r for r in results if r.get("arm") == "calm" and r.get("status") == "OK"]
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    # left: per-article event drop vs its shuffle p90
    ev2 = sorted(ev, key=lambda r: -(r.get("drop_macro") or 0))
    names = [r["title"] for r in ev2]
    drops = [r.get("drop_macro") or 0 for r in ev2]
    p90 = [r.get("shuffle_null_p90") or 0 for r in ev2]
    y = np.arange(len(names))
    ax[0].barh(y, drops, color="#8e44ad", label="event N_eff drop")
    ax[0].plot(p90, y, "k.", label="shuffle-null p90")
    ax[0].axvline(F_THRESHOLD, ls="--", c="r", label=f"f={F_THRESHOLD}")
    ax[0].set_yticks(y); ax[0].set_yticklabels(names, fontsize=7)
    ax[0].set_xlabel("canonical N_eff collapse drop (1 - onset/baseline)")
    ax[0].set_title("Per-article dynamic N_eff collapse (event arm)", fontsize=10)
    ax[0].legend(fontsize=8)
    # right: event vs calm drop distributions
    ev_d = [r["drop_macro"] for r in ev if r.get("drop_macro") is not None]
    ca_d = [r["drop_macro"] for r in ca if r.get("drop_macro") is not None]
    ax[1].hist(ev_d, bins=10, alpha=0.6, color="#8e44ad", label=f"event (n={len(ev_d)})")
    ax[1].hist(ca_d, bins=10, alpha=0.6, color="#16a085", label=f"calm null (n={len(ca_d)})")
    ax[1].axvline(F_THRESHOLD, ls="--", c="r")
    ax[1].set_xlabel("N_eff collapse drop"); ax[1].set_ylabel("articles")
    ax[1].set_title(f"Event vs matched-calm null\nVERDICT: {summary['VERDICT']}", fontsize=10)
    ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "figure_wiki_neff.png"), dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    main()
