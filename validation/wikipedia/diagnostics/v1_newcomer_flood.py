"""V1 -- Newcomer-flood hypothesis.

Theory: the frozen-partition N_eff collapse measures whether the EXISTING
pre-onset community loses independence. If the onset crowd is mostly NEW
editors (not in the frozen pre-onset partition), they flood the focal article
but do not synchronize the frozen blocks, so the measured collapse is small.

For each event article:
  f_existing = fraction of onset-window focal edits made by editors that are IN
               the frozen pre-onset partition.
  newcomers  = # distinct onset-window focal editors NOT in the frozen partition.
  new_frac   = fraction of distinct onset-window focal editors who are newcomers.

Then correlate f_existing (and raw newcomer count, new_frac) with the per-article
macro collapse drop (Spearman). Prediction: f_existing correlates POSITIVELY with
the drop. Writes v1_newcomer_flood.json + a scatter PNG.
"""
import os
import json
import datetime as dt
from collections import defaultdict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

import _shared as S
from _shared import N


def per_article():
    rows = []
    for rec in S.load_runs():
        if rec.get("arm") != "event":
            continue
        part, mod, K, G = S.frozen_partition(rec)
        if K < 3:
            continue
        onset = dt.date.fromisoformat(rec["onset"])
        olo, ohi = S.onset_window(onset)

        tot_edits = 0
        existing_edits = 0
        editors_in = set()
        editors_out = set()
        for rv in rec["focal_revs"]:
            ts = rv.get("ts")
            u = rv.get("user")
            if not ts or not u:
                continue
            d = N.parse_ts(ts).date()
            if olo <= d < ohi:
                tot_edits += 1
                if u in part:
                    existing_edits += 1
                    editors_in.add(u)
                else:
                    editors_out.add(u)
        if tot_edits == 0:
            continue
        f_existing = existing_edits / tot_edits
        n_distinct = len(editors_in) + len(editors_out)
        newcomers = len(editors_out)
        new_frac = newcomers / n_distinct if n_distinct else float("nan")

        # the per-article collapse via the frozen pipeline
        r = N.analyze_run(rec)
        drop = r.get("drop_macro")
        rows.append(dict(
            title=rec["title"], onset=rec["onset"], K=K,
            drop_macro=drop,
            f_existing=f_existing,
            onset_focal_edits=tot_edits,
            existing_edits=existing_edits,
            newcomers=newcomers,
            new_frac=new_frac,
            n_distinct_onset_editors=n_distinct,
        ))
    return rows


def main():
    rows = [r for r in per_article()
            if r["drop_macro"] is not None and not np.isnan(r["drop_macro"])]
    drops = np.array([r["drop_macro"] for r in rows])
    fexist = np.array([r["f_existing"] for r in rows])
    newc = np.array([r["newcomers"] for r in rows], float)
    newf = np.array([r["new_frac"] for r in rows])

    rho_fe, p_fe = spearmanr(fexist, drops)
    rho_nc, p_nc = spearmanr(newc, drops)
    rho_nf, p_nf = spearmanr(newf, drops)

    out = dict(
        variation="V1 newcomer-flood",
        n=len(rows),
        spearman_f_existing_vs_drop=dict(rho=float(rho_fe), p=float(p_fe)),
        spearman_newcomer_count_vs_drop=dict(rho=float(rho_nc), p=float(p_nc)),
        spearman_new_frac_vs_drop=dict(rho=float(rho_nf), p=float(p_nf)),
        prediction="f_existing positively correlates with drop (existing community synchronizes)",
        rows=sorted(rows, key=lambda r: -r["drop_macro"]),
    )
    json.dump(out, open(os.path.join(S.HERE, "v1_newcomer_flood.json"), "w"), indent=2)

    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    ax[0].scatter(fexist, drops, c="#8e44ad")
    for r in rows:
        ax[0].annotate(r["title"], (r["f_existing"], r["drop_macro"]),
                       fontsize=6, alpha=0.7)
    ax[0].set_xlabel("f_existing (onset focal edits by frozen-partition members)")
    ax[0].set_ylabel("macro N_eff collapse drop")
    ax[0].axhline(0, c="k", lw=0.5)
    ax[0].set_title(f"f_existing vs collapse  rho={rho_fe:.2f} p={p_fe:.3f}", fontsize=9)
    ax[1].scatter(newf, drops, c="#16a085")
    for r in rows:
        ax[1].annotate(r["title"], (r["new_frac"], r["drop_macro"]),
                       fontsize=6, alpha=0.7)
    ax[1].set_xlabel("newcomer fraction of distinct onset editors")
    ax[1].set_ylabel("macro N_eff collapse drop")
    ax[1].axhline(0, c="k", lw=0.5)
    ax[1].set_title(f"newcomer-frac vs collapse  rho={rho_nf:.2f} p={p_nf:.3f}", fontsize=9)
    fig.tight_layout()
    fig.savefig(os.path.join(S.HERE, "v1_newcomer_flood.png"), dpi=120)
    plt.close(fig)

    print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=2))
    for r in out["rows"]:
        print(f"  {r['title']:22s} drop={r['drop_macro']:+.2f} "
              f"f_exist={r['f_existing']:.2f} newcomers={r['newcomers']:3d} "
              f"new_frac={r['new_frac']:.2f}")


if __name__ == "__main__":
    main()
