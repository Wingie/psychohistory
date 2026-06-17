"""Principled derivation of the frozen threshold f for the neff_v2 sealed test.

Run BEFORE the fresh roster is harvested. Uses ONLY the EXISTING tuning data
(validation/wikipedia/data, the 20-article roster) and the engine simulation.
NOTHING here touches the fresh neff_v2 roster.

Route (i)  PRIMARY -- clean-null distribution.
  Re-pick, per existing event article, the genuinely-quietest 49-day window inside
  the harvested pre-onset span (the V2 clean-null method, imported verbatim from
  the diagnostics), run the frozen collapse pipeline at that clean pseudo-onset,
  and take the distribution of clean-calm N_eff drops. f := its 95th percentile so
  a passing event must exceed what a genuinely-quiet window produces 95% of the
  time. We also report a robustified variant (see notes) because the raw n is small.

Route (ii)  CROSS-CHECK -- engine E4 sanity bound.
  Run the verified coupled-block engine (run_blocks / block_metrics, the same macro
  variance-ratio N_eff) on realistically SPARSE / SHORT windows matched to the
  Wikipedia bucketing (K = 3-5 blocks, ~16 baseline buckets vs ~8 onset buckets),
  sweep coupling W from calm to synchronized, and report the macro-N_eff collapse
  fraction achievable. This bounds what a real synchrony event can produce on short
  windows, i.e. a ceiling/plausibility check on f.

Emits derive_f.json. Run: py -3.12 derive_f.py
"""
import os
import sys
import json
import datetime as dt
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.abspath(os.path.join(HERE, "..", "wikipedia"))
DIAG = os.path.join(WIKI, "diagnostics")
TUNING_DATA = os.path.join(WIKI, "data")
sys.path.insert(0, WIKI)
sys.path.insert(0, DIAG)

import neff_collapse_wiki as N   # noqa: E402 frozen analysis functions
import roster as R               # noqa: E402
import v2_clean_calm as V2       # noqa: E402 clean-null window picker

SKILL = os.path.abspath(os.path.join(HERE, "..", "..", ".claude", "skills",
                                     "psychohistory", "scripts"))
sys.path.insert(0, SKILL)
import engine as ENG             # noqa: E402 verified run_blocks / block_metrics


# --------------------------------------------------------------------------
# Route (i): clean-null distribution on the EXISTING tuning data
# --------------------------------------------------------------------------
def route_i_clean_null():
    files = sorted(f for f in os.listdir(TUNING_DATA) if f.endswith(".json"))
    bytitle = defaultdict(dict)
    for f in files:
        d = json.load(open(os.path.join(TUNING_DATA, f), encoding="utf-8"))
        bytitle[d["title"]][d["arm"]] = d

    clean_drops, rows = [], []
    for title, arms in bytitle.items():
        if "event" not in arms:
            continue
        ev = arms["event"]
        G = N.coedit_graph(ev["editor_contribs"], ev["title"])
        part, mod, K = N.blind_partition(G)
        if K < 3:
            continue
        onset = dt.date.fromisoformat(ev["onset"])
        dates = V2.all_focal_dates(arms)
        revs = V2.merged_focal_revs(arms)
        islands = V2.harvested_islands(dates)
        pseudo, info, status = V2.quietest_pseudo_onset(dates, onset, islands)
        cd = None
        if pseudo is not None:
            cd = V2.collapse_at(revs, part, pseudo).get("drop_macro")
        if cd is not None and not (isinstance(cd, float) and np.isnan(cd)):
            clean_drops.append(float(cd))
        rows.append(dict(title=title, status=status, clean_drop=cd))

    cd = sorted(clean_drops)
    out = dict(
        n_clean=len(cd),
        clean_drops_sorted=[round(x, 4) for x in cd],
        p75=float(np.percentile(cd, 75)), p80=float(np.percentile(cd, 80)),
        p90=float(np.percentile(cd, 90)), p95=float(np.percentile(cd, 95)),
        median=float(np.median(cd)), maxv=float(max(cd)),
        rows=rows,
    )
    return out


# --------------------------------------------------------------------------
# Route (ii): engine E4 sanity bound on short / sparse windows
# --------------------------------------------------------------------------
def neff_macro_short(traj_window, full_mean):
    """The Wikipedia macro N_eff applied to an engine count-like window so the
    bound is computed with the SAME estimator as the empirical test."""
    return N.neff_macro(traj_window, full_mean)


def _macro_sign(window):
    """Canonical sign-based macro variance-ratio N_eff (engine block_metrics def):
    Var_t(single-block sign) / Var_t(population-mean sign), clipped to [1,K].
    This is the SAME estimator engine.block_metrics uses for neff_correct."""
    K = window.shape[1]
    sgn = np.sign(window)
    var_single = float(sgn.var(axis=0).mean())
    var_mean = float(sgn.mean(axis=1).var())
    if var_mean <= 1e-12:
        return 1.0
    return float(np.clip(var_single / var_mean, 1.0, K))


def route_ii_engine_bound():
    """Sanity bound: what macro-N_eff collapse fraction is ACHIEVABLE on short,
    sparse windows matched to the Wikipedia bucketing?

    For K in {3,4,5}, baseline = a calm (independent, W=0.0) window of 16 buckets,
    onset = a synchronized (W=1.0) window of 8 buckets. We use the canonical
    SIGN-based macro variance-ratio (engine block_metrics definition) so the bound
    is computed with the same N_eff the paper cites. This tells us the ceiling a
    genuine synchrony event can produce when the windows are this short, i.e.
    whether the frozen f is below the physically attainable collapse."""
    rng = np.random.default_rng(20260616)
    BUCK_BASE, BUCK_ONSET = 16, 8
    STRIDE = 50          # decorrelate consecutive buckets (model time)
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
    # self-test echo of the canonical E4 collapse (long, K=64)
    lo = ENG.block_metrics(ENG.run_blocks(K=64, W=0.0, seed=2))
    hi = ENG.block_metrics(ENG.run_blocks(K=64, W=1.0, seed=2))
    e4 = dict(neff_calm=lo["neff_correct"], neff_sync=hi["neff_correct"],
              e4_drop=1.0 - hi["neff_correct"] / lo["neff_correct"])
    return dict(per_K=results, e4_long_reference=e4,
                note=("short-window achievable median collapse; ceiling/plausibility "
                      "check that f sits below what a real event can produce"))


def main():
    ri = route_i_clean_null()
    rii = route_ii_engine_bound()

    # Frozen choice: f := Route (i) 95th percentile of the clean-null drops.
    f = round(ri["p95"], 3)

    out = dict(
        route_i_clean_null=ri,
        route_ii_engine_bound=rii,
        derived_f_route_i_p95=ri["p95"],
        FROZEN_f=f,
        note=("f frozen = Route (i) 95th pctile of the genuinely-quiet clean-null "
              "drop distribution on the EXISTING tuning data. A passing event must "
              "beat what a genuinely-quiet window produces 95% of the time. Route (ii) "
              "engine bound is the sanity ceiling: short-window macro collapse is "
              "achievable well above f, so f is not above the physically attainable."),
    )
    json.dump(out, open(os.path.join(HERE, "derive_f.json"), "w"), indent=2)
    print(json.dumps(dict(
        route_i={k: ri[k] for k in ("n_clean", "p75", "p80", "p90", "p95",
                                    "median", "maxv", "clean_drops_sorted")},
        route_ii_per_K=rii["per_K"], route_ii_e4=rii["e4_long_reference"],
        FROZEN_f=f), indent=2))


if __name__ == "__main__":
    main()
