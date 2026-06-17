"""Derive and FREEZE the threshold f for the v3 SEALED WSB test.

Route (i) PRIMARY -- clean WSB null (this sets f):
  For each of the 12 frozen CLEAN windows (clean_windows.pick_clean_onsets), run the
  FROZEN collapse pipeline (same as the event arm: pre-onset co-thread graph -> blind
  Louvain partition -> canonical macro variance-ratio N_eff, baseline vs onset drop)
  at that clean pseudo-onset. This yields the clean-null macro-N_eff drop distribution.
  f := its 95th percentile. p90 reported for legibility; seal is on p95.

Route (ii) CROSS-CHECK -- engine E4 sanity bound (does NOT set f):
  Reuses validation/neff_v2/derive_f.py's logic verbatim: the verified coupled-block
  engine on short/sparse windows matched to the WSB bucketing, to confirm f sits below
  what the mechanism can physically produce.

Reuses validation/reddit_wsb/neff_collapse_wsb.py's pipeline functions; does NOT touch
the fresh event roster. Run AFTER harvest of the clean windows, BEFORE analyze_v3.

Emits derive_f_v3.json. Run: py -3.12 derive_f_v3.py
"""
import os
import sys
import json
import datetime as dt

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
WSB = os.path.abspath(os.path.join(HERE, "..", "reddit_wsb"))
sys.path.insert(0, WSB)
sys.path.insert(0, os.path.join(HERE, "..", "pipeline_v03"))

import neff_collapse_wsb as NB   # noqa: E402 frozen pipeline functions
import clean_windows as CW       # noqa: E402

SKILL = os.path.abspath(os.path.join(HERE, "..", "..", ".claude", "skills",
                                     "psychohistory", "scripts"))
sys.path.insert(0, SKILL)
import engine as ENG             # noqa: E402 verified run_blocks / block_metrics


def load(label):
    return NB.load_run_comments(os.path.join(DATA, f"clean__{label}.jsonl"))


def route_i_clean_null():
    picks = CW.pick_clean_onsets()
    rows, clean_drops = [], []
    for label, onset, mv, era in picks:
        comments = load(label)
        if not comments:
            rows.append(dict(label=label, onset=onset, status="NO_DATA"))
            sys.stderr.write(f"  {label} NO_DATA\n")
            continue
        r = NB.analyze_run(label, onset, "clean", comments)
        drop = r.get("drop_macro")
        rows.append(dict(label=label, onset=onset, era=era, onset_mean_vol=mv,
                         status=r.get("status"), K=r.get("K_blocks"),
                         modularity=r.get("modularity"), drop_macro=drop,
                         neff_base=r.get("neff_base_macro"),
                         neff_onset=r.get("neff_onset_macro"),
                         n_comments=r.get("n_comments_total"),
                         user_cap_hit=r.get("user_cap_hit"),
                         n_threads_subsampled=r.get("n_threads_subsampled")))
        sys.stderr.write(f"  {label:22s} {r.get('status')} K={r.get('K_blocks')} "
                         f"drop={drop}\n")
        if (r.get("status") == "OK" and drop is not None
                and not (isinstance(drop, float) and np.isnan(drop))):
            clean_drops.append(float(drop))
    cd = sorted(clean_drops)
    out = dict(
        n_windows_total=len(picks), n_clean_ok=len(cd),
        clean_drops_sorted=[round(x, 4) for x in cd],
        p75=float(np.percentile(cd, 75)) if cd else None,
        p80=float(np.percentile(cd, 80)) if cd else None,
        p90=float(np.percentile(cd, 90)) if cd else None,
        p95=float(np.percentile(cd, 95)) if cd else None,
        median=float(np.median(cd)) if cd else None,
        maxv=float(max(cd)) if cd else None,
        rows=rows,
    )
    return out


def _macro_sign(window):
    """Canonical sign-based macro variance-ratio N_eff (engine block_metrics def),
    verbatim from neff_v2/derive_f.py."""
    K = window.shape[1]
    sgn = np.sign(window)
    var_single = float(sgn.var(axis=0).mean())
    var_mean = float(sgn.mean(axis=1).var())
    if var_mean <= 1e-12:
        return 1.0
    return float(np.clip(var_single / var_mean, 1.0, K))


def route_ii_engine_bound():
    rng = np.random.default_rng(20260616)
    BUCK_BASE, BUCK_ONSET, STRIDE = 16, 8, 50
    results = []
    for K in (3, 4, 5):
        drops = []
        for _ in range(300):
            seed = int(rng.integers(1, 1_000_000))
            base = ENG.run_blocks(K, W=0.0, T=2000, seed=seed)[-BUCK_BASE * STRIDE::STRIDE]
            onset = ENG.run_blocks(K, W=1.0, T=2000, seed=seed + 7)[-BUCK_ONSET * STRIDE::STRIDE]
            nb = _macro_sign(base)
            no = _macro_sign(onset)
            if nb > 0:
                drops.append(1.0 - no / nb)
        drops = np.array(drops)
        results.append(dict(K=K, median_drop=float(np.median(drops)),
                            p25=float(np.percentile(drops, 25)),
                            p75=float(np.percentile(drops, 75)),
                            mean_drop=float(np.mean(drops))))
    lo = ENG.block_metrics(ENG.run_blocks(K=64, W=0.0, seed=2))
    hi = ENG.block_metrics(ENG.run_blocks(K=64, W=1.0, seed=2))
    e4 = dict(neff_calm=lo["neff_correct"], neff_sync=hi["neff_correct"],
              e4_drop=1.0 - hi["neff_correct"] / lo["neff_correct"])
    return dict(per_K=results, e4_long_reference=e4,
                note="short-window achievable median collapse; ceiling check that f "
                     "sits below what a real synchrony event can produce.")


def main():
    ri = route_i_clean_null()
    rii = route_ii_engine_bound()
    f = round(ri["p95"], 4) if ri["p95"] is not None else None
    out = dict(
        route_i_clean_null=ri,
        route_ii_engine_bound=rii,
        derived_f_route_i_p95=ri["p95"],
        clean_null_p90=ri["p90"],
        FROZEN_f=f,
        note="f frozen = Route (i) 95th pctile of the genuinely-quiet CLEAN WSB null "
             "drop distribution. A passing event must beat what a genuinely-quiet WSB "
             "window produces 95%% of the time. Route (ii) engine bound is the sanity "
             "ceiling: short-window macro collapse is achievable above f.",
    )
    json.dump(out, open(os.path.join(HERE, "derive_f_v3.json"), "w"), indent=2)
    print(json.dumps(dict(
        route_i={k: ri[k] for k in ("n_windows_total", "n_clean_ok", "p75", "p80",
                                    "p90", "p95", "median", "maxv",
                                    "clean_drops_sorted")},
        route_ii_per_K=rii["per_K"], route_ii_e4=rii["e4_long_reference"],
        clean_null_p90=ri["p90"], FROZEN_f=f), indent=2))


if __name__ == "__main__":
    main()
