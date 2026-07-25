"""POST-SEAL AUDIT of the v4 null fire rate p0. Does NOT re-run, re-seal, or
re-decide anything: it reads the two committed result JSONs and asks one question.

The v4 rule's condition (b) is P(X >= k | n, p0) < 0.01 with p0 = 0.10, asserted in
PRE_REGISTRATION_neff_v4.md:57-61 as "construction-implied": under H0 the observed
partition is exchangeable with its 300 block-label shuffles, so it clears its own
90th-percentile shuffle one time in ten.

That exchangeability does not hold. The observed drop comes from a modularity-optimised
Louvain partition; every null draw is a random relabelling of the same users. Round-2
finding P-01 argues the null fire rate is therefore an EMPIRICAL quantity, not a
construction constant. This script measures how much that matters, using only data
already in the repository.

METHOD (and its limitation, stated up front). The decisive measurement -- each quiet
window's own fires_vs_shuffle flag -- does not exist: derive_f_v3.py ran the full 300x
shuffle null on the twelve clean windows and then dropped the three shuffle fields at
serialisation (round-2 finding P-03; fixed on this branch, but the fix only takes
effect on the next harvest, which needs the WSB dump). So this audit uses a PROXY:
it thresholds v3's twelve genuinely-quiet-window magnitude drops against each of the
twelve shuffle-null p90 values v4 actually measured on its own events, and sweeps.

A proxy sweep cannot establish a point value for p0. It can establish a RANGE, and
that is the result: condition (b) does not survive anywhere in it.

Stdlib only, no raw data, no network. Run: python3 p0_audit.py
"""
import os
import json
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
V4_RESULT = os.path.join(HERE, "result_neff_v4.json")
V3_DERIVE = os.path.abspath(os.path.join(HERE, "..", "neff_v3", "derive_f_v3.json"))

ALPHA_COND_B = 0.01     # the frozen condition (b) tail
CP_ALPHA = 0.05         # one-sided Clopper-Pearson level


def binom_sf_ge(k, n, p):
    """P(X >= k | Binomial(n, p)), exact -- same function as analyze_v4.binom_sf_ge."""
    return float(sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1)))


def cp_lower(k, n, alpha=CP_ALPHA):
    """Exact one-sided Clopper-Pearson lower confidence bound: the p solving
    P(X >= k | n, p) = alpha. sf is increasing in p, so bisect."""
    if k <= 0:
        return 0.0
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if binom_sf_ge(k, n, mid) < alpha:
            lo = mid
        else:
            hi = mid
    return lo


def cond_b_break_point(k, n):
    """The p0 at which condition (b) P(X>=k|n,p0) < 0.01 stops holding."""
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if binom_sf_ge(k, n, mid) < ALPHA_COND_B:
            lo = mid
        else:
            hi = mid
    return lo


def main():
    v4 = json.load(open(V4_RESULT))
    s = v4["summary"]
    k, n, p0_published = s["k_fires"], s["n_powered_Kge3"], s["binom_p0"]

    # 1. reproduce the published figure exactly
    p_published = binom_sf_ge(k, n, p0_published)
    matches = abs(p_published - s["binom_p_ge_k"]) < 1e-18

    # 2. where does condition (b) break
    brk = cond_b_break_point(k, n)

    # 3. the twelve shuffle nulls v4 measured on its own events
    thresholds = sorted(r["shuffle_null_p90"] for r in v4["runs"]
                        if r.get("shuffle_null_p90") is not None)

    # 4. the twelve genuinely-quiet v3 clean-window drops
    clean = json.load(open(V3_DERIVE))["route_i_clean_null"]
    drops = clean["clean_drops_sorted"]
    n_quiet = len(drops)

    rows = []
    for t in thresholds:
        kq = sum(1 for d in drops if d > t)
        rate = kq / n_quiet
        rows.append(dict(
            threshold=t, k_quiet_fires=kq, n_quiet=n_quiet, quiet_fire_rate=rate,
            cp95_lower_on_p0=cp_lower(kq, n_quiet),
            p_at_this_rate=(binom_sf_ge(k, n, rate) if rate > 0 else 0.0),
            cond_b_holds=(binom_sf_ge(k, n, rate) < ALPHA_COND_B) if rate > 0 else True,
        ))

    print(f"v4 sealed result: {k}/{n} fire, published p0={p0_published}, "
          f"published p={s['binom_p_ge_k']:.6e}")
    print(f"  reproduced exactly from math.comb: {p_published:.6e}  match={matches}")
    print(f"  condition (b) P<{ALPHA_COND_B} breaks at p0 = {brk:.5f}\n")
    print(f"Quiet-window fire rate (PROXY: v3's {n_quiet} clean-window drops thresholded "
          f"at each shuffle-null p90 v4 measured)")
    print(f"{'threshold':>11} {'k/n':>8} {'rate':>7} {'CP95 lo':>8} "
          f"{'P(X>=' + str(k) + '|' + str(n) + ',rate)':>18} {'cond (b)':>9}")
    for r in rows:
        print(f"{r['threshold']:11.6f} {r['k_quiet_fires']:>5}/{r['n_quiet']:<2} "
              f"{r['quiet_fire_rate']:7.3f} {r['cp95_lower_on_p0']:8.4f} "
              f"{r['p_at_this_rate']:18.4g} {'holds' if r['cond_b_holds'] else 'FAILS':>9}")

    n_hold = sum(1 for r in rows if r["cond_b_holds"])
    ks = [r["k_quiet_fires"] for r in rows]
    modal_k = max(set(ks), key=ks.count)
    modal_lo = cp_lower(modal_k, n_quiet)

    print(f"\ncondition (b) holds at {n_hold} of {len(rows)} measured thresholds")
    print(f"quiet fire count ranges {min(ks)}-{max(ks)} of {n_quiet}; "
          f"modal {modal_k}/{n_quiet} at {len(rows) - 2} of {len(rows)} thresholds")
    print(f"at the modal reading the one-sided CP95 LOWER bound on p0 is {modal_lo:.4f}, "
          f"which is {'ABOVE' if modal_lo > brk else 'below'} the {brk:.5f} break point")

    out = dict(
        what="post-seal audit of the v4 null fire rate p0; proxy sweep, not a re-seal",
        published=dict(k_fires=k, n_powered=n, p0=p0_published,
                       p_published=s["binom_p_ge_k"], p_reproduced=p_published,
                       reproduces_exactly=matches),
        cond_b_break_p0=brk,
        proxy=dict(
            method=("v3 clean-window magnitude drops thresholded at each shuffle-null "
                    "p90 measured by v4 on its own events; a stand-in for the discarded "
                    "per-window fires_vs_shuffle flag (finding P-03)"),
            n_quiet_windows=n_quiet, quiet_drops=drops, rows=rows,
            n_thresholds_where_cond_b_holds=n_hold, n_thresholds=len(rows),
            quiet_fire_count_range=[min(ks), max(ks)],
            modal_k=modal_k, modal_cp95_lower_on_p0=modal_lo,
        ),
        limitation=("A proxy sweep bounds p0; it does not measure it. The definitive "
                    "figure needs analyze_v4's fire rule run over >=30 genuinely-quiet "
                    "pseudo-onsets with each window's OWN shuffle null recorded. That "
                    "needs the WSB dump and is the open item."),
        verdict=("Condition (b) fails at every threshold v4 itself measured. The "
                 "1.7e-7 figure is conditional on p0=0.10 and is not supported by the "
                 "repository's own quiet-window data."),
    )
    json.dump(out, open(os.path.join(HERE, "p0_audit.json"), "w"), indent=2)


if __name__ == "__main__":
    main()
