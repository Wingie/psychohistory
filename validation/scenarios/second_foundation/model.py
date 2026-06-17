#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SECOND FOUNDATION -- PART A: REGIME / LINEAGE MODEL
===================================================
Extends the MYTHOS FABLE scenario with MODEL-LINEAGE DIVERSITY, the model:human
ratio M/H, and a RESOURCE layer.

HONESTY RAIL: this is a THEORETICAL / SCENARIO analysis with ILLUSTRATIVE
parameters. No number here is fit to data. The robust content is the STRUCTURE
(the shape of how L_eff and human N_eff move across regimes), not the magnitudes.

Core idea -- the variable that matters is not the raw number of deployed models M
but the EFFECTIVE number of INDEPENDENT model LINEAGES, computed with the SAME
verified Kish/N_eff machinery the project uses for human blocks:

    N_eff(N, rho) = N / (1 + (N - 1) * rho)          (Kish 1965 design-effect)

    L_eff = N_eff(M, rho_model)        # effective independent MODEL lineages
    Nh_eff = N_eff(K, rho_human)       # effective independent HUMAN blocks

The link A -> B: human homogenization is driven by how few INDEPENDENT lineages
the population's cognition routes through. A monoculture of agents forked from one
base (high rho_model) gives L_eff ~ 1 no matter how large M is; so rho_human is
floored by 1/L_eff and human N_eff collapses with L_eff.

Run:  py -3.12 model.py
Deps: numpy, matplotlib (Agg backend)
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------
# The verified N_eff machinery (Kish design-effect). Reused verbatim.
# ----------------------------------------------------------------------
def n_eff(N, rho):
    """Effective number of independent units. N_eff = N / (1 + (N-1)*rho).
    rho in [0,1]: 0 -> N (fully independent), 1 -> 1 (monoculture)."""
    N = float(N)
    rho = float(np.clip(rho, 0.0, 1.0))
    return N / (1.0 + (N - 1.0) * rho)


# ----------------------------------------------------------------------
# Human homogenization driven by lineage diversity.
# ----------------------------------------------------------------------
# If the population routes its cognition through L_eff INDEPENDENT lineages, the
# minimum achievable cross-human correlation is floored: even a perfectly mixed
# population cannot be more independent than the number of distinct "minds" it
# consults. We model rho_human as rising with attention capture A_ai and floored
# by the monoculture term (1/L_eff):
#
#   rho_human = A_ai * ( c_floor/L_eff + (1 - c_floor/L_eff) * rho_within )
#
# - c_floor in (0,1]: how strongly lineage scarcity dominates the floor.
# - rho_within: residual within-lineage correlation from shared prompts/UX (GUESSED).
# As L_eff -> 1 the floor -> ~A_ai*1 (everyone correlated); as L_eff grows the
# floor -> small, so a diverse-lineage world keeps human N_eff high.
def rho_human_from_lineage(L_eff, A_ai, c_floor=0.85, rho_within=0.10):
    floor = c_floor / max(L_eff, 1.0)
    floor = min(floor, 1.0)
    return float(np.clip(A_ai * (floor + (1.0 - floor) * rho_within), 0.0, 1.0))


# ----------------------------------------------------------------------
# Regimes. Each names M, rho_model, and a label. A_ai (attention captured) and
# H (humans, billions) and K (baseline human blocks) are shared scenario context.
# ----------------------------------------------------------------------
def regimes():
    # H = humans (billions), K = baseline independent human blocks (from mythos fable)
    return [
        # name, M (deployed models), rho_model, note
        dict(name="Global oligopoly",  M=5,         rho_model=0.70,
             note="few frontier labs, models share architecture/data"),
        dict(name="Per-tribe",         M=200,       rho_model=0.05,
             note="one independent lineage per community: diversity preserved"),
        dict(name="Mega omnilingual (ENIAC)", M=1,  rho_model=1.00,
             note="one single global model: L_eff = 1 by construction"),
        dict(name="SLM swarm",         M=1_000_000, rho_model=0.97,
             note="huge M but all distilled from one base: apparent != actual diversity"),
    ]


# A_ai context for Part A (attention already substantially captured -- this is the
# regime the mythos fable drifts into). Illustrative.
A_AI_CONTEXT = 0.70
K_HUMAN_BLOCKS = 1000.0
H_HUMANS = 8.0   # billions


def fragility(L_eff, Nh_eff, K=K_HUMAN_BLOCKS):
    """A simple fragility score in [0,1]. High when lineages are few AND humans
    are homogenized. fragility = (1/L_eff) * (1 - Nh_eff/K) blended with 1/L_eff.
    Illustrative composite, not a calibrated index."""
    mono = 1.0 / L_eff                         # monoculture pressure (1 -> single lineage)
    homog = 1.0 - Nh_eff / K                   # how collapsed human independence is
    return float(np.clip(0.5 * mono + 0.5 * homog, 0.0, 1.0))


def analyze_regimes(A_ai=A_AI_CONTEXT, H=H_HUMANS, K=K_HUMAN_BLOCKS):
    rows = []
    for r in regimes():
        M = r["M"]
        L_eff = n_eff(M, r["rho_model"])
        rho_h = rho_human_from_lineage(L_eff, A_ai)
        Nh_eff = n_eff(K, rho_h)
        MH = M / (H * 1e9)                       # model:human ratio (per-person agents)
        frag = fragility(L_eff, Nh_eff, K)
        rows.append(dict(name=r["name"], M=M, rho_model=r["rho_model"],
                         L_eff=L_eff, MH=MH, rho_human=rho_h, Nh_eff=Nh_eff,
                         fragility=frag, note=r["note"]))
    return rows


# ----------------------------------------------------------------------
# M/H sweep: raising the model:human ratio does NOT raise L_eff if rho stays high.
# ----------------------------------------------------------------------
def mh_sweep(H=H_HUMANS, A_ai=A_AI_CONTEXT, K=K_HUMAN_BLOCKS):
    """Sweep M from 1 to 10x the human population at several fixed rho_model.
    Show L_eff saturates at 1/rho_model regardless of how big M (and M/H) gets."""
    M = np.logspace(0, np.log10(10 * H * 1e9), 200)   # 1 -> 10 agents per human
    out = {}
    for rho in [0.0, 0.3, 0.7, 0.9, 0.97, 0.999]:
        L = np.array([n_eff(m, rho) for m in M])
        out[rho] = L
    return M, out, (M / (H * 1e9))


# ----------------------------------------------------------------------
# Resource layer: training cost (barrier to a NEW lineage) vs inference cost.
# ----------------------------------------------------------------------
# A new INDEPENDENT lineage requires paying T_cost (training a base from scratch).
# Number of lineages the ecosystem can AFFORD is ~ Budget / T_cost. As T_cost
# rises (frontier scale) and is not offset, the affordable lineage count -> small.
# Inference cost kappa falls ~10x/yr (real-ish), which RAISES attention capture
# A_ai (cheaper to deploy everywhere) but does NOTHING to raise L_eff -- it just
# multiplies M of the SAME base (rho_model stays ~1). So the economic attractor is
# small L_eff with rising A_ai: human N_eff collapses.
def resource_attractor(years=8, K=K_HUMAN_BLOCKS, H=H_HUMANS):
    t = np.arange(years + 1)
    # training cost per new base lineage (illustrative, normalized; rises ~1.6x/yr)
    T_cost = 1.0 * (1.6 ** t)
    # ecosystem R&D budget for new base models (rises ~1.3x/yr -- slower than cost)
    Budget = 6.0 * (1.3 ** t)
    L_afford = np.maximum(Budget / T_cost, 1.0)          # affordable independent lineages
    # inference cost falls ~10x/yr -> attention capture rises (logistic toward ~0.9)
    kappa = 1.0 * (0.1 ** t)
    A_ai = 0.9 * (1.0 - np.exp(-0.6 * t)) + 0.05
    A_ai = np.clip(A_ai, 0.0, 0.95)
    # deployed models M tracks falling inference cost (cheap -> deploy many of same base)
    M = np.maximum(1.0, 50.0 / kappa)                    # explodes as kappa falls
    # but rho_model stays high because new BASES are unaffordable: lineages = L_afford
    L_eff = L_afford                                     # the actual independent diversity
    rho_h = np.array([rho_human_from_lineage(le, a) for le, a in zip(L_eff, A_ai)])
    Nh_eff = np.array([n_eff(K, rh) for rh in rho_h])
    return dict(t=t, T_cost=T_cost, Budget=Budget, L_afford=L_afford,
                kappa=kappa, A_ai=A_ai, M=M, L_eff=L_eff, Nh_eff=Nh_eff)


# ----------------------------------------------------------------------
# Figure
# ----------------------------------------------------------------------
def figure(path):
    rows = analyze_regimes()
    M_sweep, L_by_rho, MH_axis = mh_sweep()
    RA = resource_attractor()

    fig, ax = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle("SECOND FOUNDATION  Part A -- model-LINEAGE diversity (L_eff), the "
                 "model:human ratio, and the resource attractor\n"
                 "(THEORETICAL SCENARIO, illustrative parameters -- structure is the "
                 "claim, magnitudes are not calibrated)",
                 fontsize=12, fontweight="bold")

    # (0,0) regimes: L_eff and human N_eff bars
    a = ax[0, 0]
    names = [r["name"] for r in rows]
    L_effs = [r["L_eff"] for r in rows]
    Nh = [r["Nh_eff"] for r in rows]
    x = np.arange(len(names))
    a.bar(x - 0.2, L_effs, width=0.4, color="indigo", label="L_eff (model lineages)")
    a.bar(x + 0.2, Nh, width=0.4, color="seagreen", label="human N_eff (/1000)")
    a.set_yscale("log")
    a.set_xticks(x)
    a.set_xticklabels([n.replace(" ", "\n") for n in names], fontsize=8)
    a.set_title("Per-regime: effective lineages L_eff and human N_eff (log)")
    a.set_ylabel("effective count (log)")
    for xi, (le, nh) in enumerate(zip(L_effs, Nh)):
        a.text(xi - 0.2, le, f"{le:.1f}", ha="center", va="bottom", fontsize=7)
        a.text(xi + 0.2, nh, f"{nh:.1f}", ha="center", va="bottom", fontsize=7)
    a.legend(fontsize=8)

    # (0,1) M/H sweep: L_eff saturates at 1/rho regardless of M
    a = ax[0, 1]
    for rho, L in L_by_rho.items():
        a.loglog(MH_axis, L, lw=2, label=f"rho_model={rho}")
        if rho > 0:
            a.axhline(1.0 / rho if rho > 0 else np.nan, color="gray", ls=":", lw=0.6)
    a.set_title("Raising M/H does NOT raise L_eff when rho_model is high\n"
                "(L_eff -> 1/rho_model ceiling; per-person agents from one base = monoculture)")
    a.set_xlabel("model:human ratio M/H (agents per person)")
    a.set_ylabel("L_eff (log)")
    a.axvline(1.0, color="black", ls="--", lw=0.8, alpha=0.6)
    a.text(1.0, a.get_ylim()[0] * 1.5, "1 agent/person", rotation=90,
           fontsize=7, va="bottom")
    a.legend(fontsize=7, loc="upper left")

    # (1,0) resource layer: T_cost vs budget -> affordable lineages; kappa down
    a = ax[1, 0]
    a.semilogy(RA["t"], RA["T_cost"], color="firebrick", lw=2,
               label="T_cost (train new base lineage)")
    a.semilogy(RA["t"], RA["Budget"], color="navy", lw=2, ls="--",
               label="ecosystem budget for new bases")
    a.semilogy(RA["t"], RA["kappa"], color="purple", lw=2, ls=":",
               label="kappa (inference cost, ~10x/yr down)")
    a.set_title("Resource layer: training cost is the barrier; inference cost collapses")
    a.set_xlabel("years"); a.set_ylabel("normalized cost / budget (log)")
    a.legend(fontsize=8)

    # (1,1) economic attractor: M explodes, L_eff stays small, human N_eff collapses
    a = ax[1, 1]
    a.semilogy(RA["t"], RA["M"], color="darkorange", lw=2,
               label="M deployed models (explodes as kappa falls)")
    a.semilogy(RA["t"], RA["L_eff"], color="indigo", lw=2,
               label="L_eff affordable lineages (stays small)")
    a.semilogy(RA["t"], RA["Nh_eff"], color="seagreen", lw=2, ls="--",
               label="human N_eff (tracks L_eff, collapses)")
    a.set_title("Economic attractor: small L_eff regardless of M;\nhuman N_eff tracks L_eff down")
    a.set_xlabel("years"); a.set_ylabel("count (log)")
    a.legend(fontsize=8)

    fig.text(0.5, 0.005,
             "L_eff = M/(1+(M-1)*rho_model) -- the SAME Kish/N_eff identity used for human "
             "blocks. Diversity that matters is INDEPENDENT lineages, not deployed count M.",
             ha="center", fontsize=9, style="italic", color="dimgray")
    fig.tight_layout(rect=[0, 0.02, 1, 0.94])
    fig.savefig(path, dpi=110)
    plt.close(fig)


def main():
    png = "lineage_regimes.png"
    figure(png)
    rows = analyze_regimes()

    print("=" * 78)
    print("SECOND FOUNDATION  PART A -- LINEAGE / REGIME MODEL "
          "(illustrative, NOT a forecast)")
    print("=" * 78)
    print(f"\nContext: A_ai={A_AI_CONTEXT}, K={K_HUMAN_BLOCKS:.0f} human blocks, "
          f"H={H_HUMANS:.0f}e9 humans")
    print(f"L_eff = M/(1+(M-1)*rho_model)  [reused Kish/N_eff machinery]\n")
    hdr = f"  {'regime':24s} {'M':>11s} {'rho_m':>6s} {'L_eff':>7s} {'M/H':>8s} {'rho_h':>6s} {'N_eff(h)':>9s} {'frag':>5s}"
    print(hdr)
    print("  " + "-" * (len(hdr) - 2))
    for r in rows:
        print(f"  {r['name']:24s} {r['M']:>11.0f} {r['rho_model']:>6.2f} "
              f"{r['L_eff']:>7.2f} {r['MH']:>8.2e} {r['rho_human']:>6.3f} "
              f"{r['Nh_eff']:>9.2f} {r['fragility']:>5.2f}")
    print("\n  Reading:")
    print("   - Oligopoly: M=5, rho=0.70 -> L_eff ~ a few; human N_eff already low.")
    print("   - Per-tribe: independent lineages -> L_eff large -> human N_eff preserved.")
    print("   - ENIAC single model: L_eff = 1 -> maximal human homogenization.")
    print("   - SLM swarm: M ~ 1e6 but rho->1 -> L_eff still small (apparent != actual).")

    # M/H result
    print("\nM/H RESULT (raising agents-per-person does not buy diversity):")
    for rho in [0.7, 0.97, 0.999]:
        L_at_huge = n_eff(1e10, rho)
        print(f"   rho_model={rho:<5}: even M=1e10 (>1 agent/person) gives "
              f"L_eff={L_at_huge:.3f} (~ 1/rho={1.0/rho:.2f})")

    # Resource attractor
    RA = resource_attractor()
    print("\nRESOURCE ATTRACTOR (training cost barrier vs falling inference cost):")
    print(f"  {'yr':>3s} {'T_cost':>9s} {'budget':>8s} {'L_eff':>7s} "
          f"{'kappa':>9s} {'A_ai':>6s} {'M':>11s} {'N_eff(h)':>9s}")
    for i in RA["t"]:
        print(f"  {RA['t'][i]:>3d} {RA['T_cost'][i]:>9.2f} {RA['Budget'][i]:>8.2f} "
              f"{RA['L_eff'][i]:>7.2f} {RA['kappa'][i]:>9.2e} {RA['A_ai'][i]:>6.2f} "
              f"{RA['M'][i]:>11.0f} {RA['Nh_eff'][i]:>9.2f}")
    print("  -> M explodes (cheap inference) while L_eff stays small (expensive training);")
    print("     human N_eff tracks L_eff DOWN. The economic attractor is monoculture.")
    print(f"\nFigure saved: {png}")
    print("=" * 78)

    return rows, RA


if __name__ == "__main__":
    main()
