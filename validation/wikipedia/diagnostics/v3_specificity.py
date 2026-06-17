"""V3 -- Why 0/14 fire: a sharper specificity test.

The frozen block-label shuffle preserves per-block sizes, but at onset the whole
population converges on the focal article, so ANY partition (real or relabeled)
collapses about equally -> 0/14 fire. That gate tested whether the collapse is
community-SPECIFIC. It is not; it is population-wide.

Sharper question: even if magnitude is partition-agnostic, do the REAL blocks lose
independence in a STRUCTURED / correlated way that random relabelings do not? We
test the STRUCTURE of the block-activity correlation matrix, not just the scalar
collapse:

  PR (participation ratio of eigenvalues) = (sum lam)^2 / sum(lam^2) of the KxK
  block-activity correlation matrix. PR = K when blocks are independent (flat
  spectrum); PR -> 1 when one mode dominates (total synchronization). We compute
  PR_baseline and PR_onset for the REAL partition and for shuffled partitions, and
  ask whether the REAL onset PR-collapse (PR_base - PR_onset) is more extreme than
  the shuffle distribution. If real != shuffle on STRUCTURE, a specificity signal
  survives even though the scalar gate fired 0/14. Honest either way.

Writes v3_specificity.json.
"""
import os
import json
import datetime as dt

import numpy as np

import _shared as S
from _shared import N, R

RNG = np.random.default_rng(20260616)
N_SHUF = 300


def block_corr(M):
    """KxK correlation matrix of block activity over time buckets (active blocks)."""
    stds = M.std(axis=0)
    Mk = M[:, stds > 1e-12]
    if Mk.shape[1] < 2 or Mk.shape[0] < 3:
        return None
    Cm = np.corrcoef(Mk.T)
    return Cm


def participation_ratio(Cm):
    """PR of eigenvalues of a correlation matrix. K (independent) -> 1 (one mode)."""
    if Cm is None:
        return None
    w = np.linalg.eigvalsh(Cm)
    w = np.clip(w, 0, None)
    s1 = float(w.sum())
    s2 = float((w ** 2).sum())
    if s2 <= 1e-12:
        return None
    return (s1 * s1) / s2


def pr_collapse(focal_revs, partition, onset):
    base_lo = onset - dt.timedelta(days=(2 * R.POST_DAYS + 7) + 7)
    base_hi = onset - dt.timedelta(days=7)
    onset_lo = onset - dt.timedelta(days=3)
    onset_hi = onset + dt.timedelta(days=R.POST_DAYS + 1)
    Mb, _ = N.block_bucket_matrix(focal_revs, partition, onset, base_lo, base_hi)
    Mo, _ = N.block_bucket_matrix(focal_revs, partition, onset, onset_lo, onset_hi)
    pr_b = participation_ratio(block_corr(Mb))
    pr_o = participation_ratio(block_corr(Mo))
    if pr_b is None or pr_o is None:
        return None, pr_b, pr_o
    return pr_b - pr_o, pr_b, pr_o


def main():
    rows = []
    for rec in S.load_runs():
        if rec.get("arm") != "event":
            continue
        part, mod, K, G = S.frozen_partition(rec)
        if K < 3:
            continue
        onset = dt.date.fromisoformat(rec["onset"])
        real_dpr, pr_b, pr_o = pr_collapse(rec["focal_revs"], part, onset)
        if real_dpr is None:
            continue

        nodes = list(part.keys())
        labels = np.array([part[n] for n in nodes])
        null = []
        for _ in range(N_SHUF):
            perm = RNG.permutation(labels)
            shuf = {nodes[i]: int(perm[i]) for i in range(len(nodes))}
            dpr, _, _ = pr_collapse(rec["focal_revs"], shuf, onset)
            if dpr is not None and not np.isnan(dpr):
                null.append(dpr)
        pctile = float(np.mean([d < real_dpr for d in null])) if null else None
        fires_struct = bool(pctile is not None and pctile >= 0.90)
        rows.append(dict(
            title=rec["title"], K=K,
            pr_base=pr_b, pr_onset=pr_o, pr_collapse_real=real_dpr,
            shuffle_pr_collapse_p90=(float(np.percentile(null, 90)) if null else None),
            real_pctile_in_shuffle=pctile,
            fires_structure_vs_shuffle=fires_struct,
        ))

    n_fire = sum(r["fires_structure_vs_shuffle"] for r in rows)
    out = dict(
        variation="V3 specificity via correlation-matrix structure",
        statistic="participation ratio (eigenvalue concentration) of block-activity "
                  "correlation matrix; PR=K independent, PR->1 one synchronized mode",
        n=len(rows),
        n_fire_structure=n_fire,
        frac_fire_structure=(n_fire / len(rows)) if rows else None,
        interpretation=("if frac_fire_structure ~ 0 like the scalar gate, the collapse "
                        "is genuinely partition-agnostic / total synchronization; if it "
                        "fires more, real blocks lose independence in a structured way"),
        rows=sorted(rows, key=lambda r: -(r["pr_collapse_real"] or 0)),
    )
    json.dump(out, open(os.path.join(S.HERE, "v3_specificity.json"), "w"), indent=2)
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=2))
    for r in out["rows"]:
        print(f"  {r['title']:22s} PR_base={r['pr_base']:.2f} PR_onset={r['pr_onset']:.2f} "
              f"dPR_real={r['pr_collapse_real']:+.2f} pctile={r['real_pctile_in_shuffle']:.2f} "
              f"fires={r['fires_structure_vs_shuffle']}")


if __name__ == "__main__":
    main()
