#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THE MYTHOS FABLE -- CALIBRATED SCENARIO ENSEMBLE
================================================
Upgrade of the single-trajectory cartoon into an ENSEMBLE.

OBSERVED parameters (fixed across the ensemble, set from real data):
  delta  -- cost/token decline.  Epoch AI: median ~50x/yr per fixed capability
            (range 9x-900x; GPQA/GPT-4-level ~40x/yr). The paper's own prose
            uses the conservative ~10x/yr anchor, so we keep delta = ln(10) as
            the CONSERVATIVE observed central value (the steeper Epoch median
            only accelerates the collapse, so 10x/yr is the cautious choice).
  g      -- frontier release cadence ~50-60 day median gap between frontier
            releases (OpenAI 58d, Anthropic 75d, Google 67.5d in 2025; industry
            median ~17d across all labs). Frequent releases -> ~2.5x/yr effective
            capability trend. g = ln(2.5).
  A0     -- AI share of human informational attention. Bounded plausible CURRENT
            range: chatbot-vs-search traffic ~3%, but ChatGPT ~900M weekly users
            mediating a larger informational slice. We take A0 in [0.05, 0.15]
            as a clearly-bounded estimate (NOT a measurement), central 0.08.

SWEPT structural parameters (genuinely unknown -> ranges, not point values):
  alpha     -- attention-capture rate            (low/central/high)
  p         -- homogenization exponent            [1, 3]
  L_eff     -- effective model-lineage diversity, via rho_model: monoculture
               (L_eff ~ 1.3) to diverse (L_eff ~ 18). Enters as a ceiling on
               cross-human correlation: rho = rho_max(L_eff) * A_ai^p, with
               rho_max shrinking as lineages diversify (diverse lineages cannot
               correlate the whole population even at full AI attention).
  K         -- baseline independent human-block count (low/central/high).

Run:  py -3.12 ensemble.py
Deps: numpy, matplotlib (Agg backend)
"""

import itertools
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# OBSERVED PARAMETERS (from data; fixed across the ensemble)
# ----------------------------------------------------------------------
OBS = dict(
    years     = 10.0,
    dt        = 1.0 / 12.0,
    Cf0       = 1.0,
    g         = np.log(2.5),    # ~2.5x/yr effective capability; ~50-60d release cadence (OBSERVED)
    tax       = 0.30,           # frontier-vs-deployed gap exists; size is structural, swept-irrelevant to timing
    kappa0    = 1.0,
    delta     = np.log(10.0),   # ~10x/yr cost decline, CONSERVATIVE vs Epoch median ~50x/yr (OBSERVED)
    churn     = 0.10,
    val_scale = 6.0,
    tau0      = 1.0,
    super_exp = False,
    rsi       = 0.04,
)

# ----------------------------------------------------------------------
# rho_max as a function of effective lineage diversity L_eff.
# As L_eff -> 1 (monoculture) the whole population can be driven to a
# common correlation, rho_max -> ~0.995. As L_eff grows, the achievable
# common correlation falls: rho_max ~ 1/L_eff (Kish-style ceiling).
# ----------------------------------------------------------------------
def rho_max_from_Leff(L_eff):
    # monoculture L_eff~1 -> ~0.99; diverse L_eff~18 -> ~0.06
    return float(np.clip(0.995 / L_eff, 0.0, 0.995))


def run(params):
    P = dict(OBS)
    P.update(params)
    dt = P["dt"]
    n  = int(round(P["years"] / dt)) + 1
    t  = np.linspace(0.0, P["years"], n)

    Cf   = np.zeros(n); Cd = np.zeros(n); kappa = np.zeros(n)
    A_ai = np.zeros(n); rho = np.zeros(n); Neff = np.zeros(n)
    chi  = np.zeros(n); tau = np.zeros(n); Lev = np.zeros(n)

    Cf[0]   = P["Cf0"]
    A_ai[0] = P["A0"]
    K       = P["K"]
    rho_max = rho_max_from_Leff(P["L_eff"])

    def derive(i):
        Cd[i]    = Cf[i] * (1.0 - P["tax"])
        kappa[i] = P["kappa0"] * np.exp(-P["delta"] * t[i])
        rho[i]   = rho_max * (A_ai[i] ** P["p"])
        Neff[i]  = K / (1.0 + (K - 1.0) * rho[i])
        chi[i]   = 1.0 / Neff[i]
        tau[i]   = P["tau0"] * (Neff[i] / K)
        Lev[i]   = (Cf[i] - Cd[i]) * (1.0 - Neff[i] / K)

    derive(0)
    for i in range(1, n):
        gi = P["g"]
        if P["super_exp"]:
            gi = P["g"] + P["rsi"] * np.log1p(Cf[i-1])
        Cf[i] = Cf[i-1] * np.exp(gi * dt)

        Cd_prev    = Cf[i-1] * (1.0 - P["tax"])
        kappa_prev = P["kappa0"] * np.exp(-P["delta"] * t[i-1])
        raw_prev   = Cd_prev / kappa_prev
        v0         = P["Cf0"] * (1.0 - P["tax"])
        k0         = P["kappa0"]
        vnorm      = raw_prev / (raw_prev + P["val_scale"] * (v0 / k0))

        dA = P["alpha"] * vnorm * (1.0 - A_ai[i-1]) - P["churn"] * A_ai[i-1]
        A_ai[i] = np.clip(A_ai[i-1] + dt * dA, 0.0, 1.0)
        derive(i)

    return dict(t=t, Cf=Cf, Cd=Cd, kappa=kappa, A_ai=A_ai, A_hum=1.0 - A_ai,
                rho=rho, Neff=Neff, chi=chi, tau=tau, Lev=Lev, P=P,
                rho_max=rho_max)


def crossing_time(t, y, thr, rising=True):
    for i in range(1, len(t)):
        a, b = y[i-1], y[i]
        if rising and a < thr <= b:
            f = (thr - a) / (b - a) if b != a else 0.0
            return t[i-1] + f * (t[i] - t[i-1])
        if (not rising) and a > thr >= b:
            f = (a - thr) / (a - b) if a != b else 0.0
            return t[i-1] + f * (t[i] - t[i-1])
    return None


def milestones(R):
    t = R["t"]
    tau0 = R["tau"][0]
    return dict(
        tau_halves = crossing_time(t, R["tau"], 0.5 * tau0, rising=False),
        Neff_lt10  = crossing_time(t, R["Neff"], 10.0, rising=False),
        A_maj      = crossing_time(t, R["A_ai"], 0.50, rising=True),
    )


# ----------------------------------------------------------------------
# THE SWEEP
# ----------------------------------------------------------------------
SWEEP = dict(
    alpha = [0.15, 0.28, 0.50],          # capture rate: low / central / high
    p     = [1.0, 2.0, 3.0],             # homogenization exponent in [1,3]
    L_eff = [1.3, 4.0, 18.0],            # monoculture / oligopoly / diverse
    K     = [100.0, 1000.0, 5000.0],     # baseline block count
    A0    = [0.05, 0.08, 0.15],          # observed attention share, bounded range
)


def ensemble():
    keys = list(SWEEP.keys())
    runs = []
    for combo in itertools.product(*[SWEEP[k] for k in keys]):
        params = dict(zip(keys, combo))
        R = run(params)
        M = milestones(R)
        runs.append((params, R, M))
    return runs


def summarize(runs):
    def col(name):
        return [M[name] for _, _, M in runs if M[name] is not None]

    def rng(name):
        v = col(name)
        if not v:
            return (None, None, None)
        return (min(v), float(np.median(v)), max(v))

    out = {}
    for name in ("tau_halves", "Neff_lt10", "A_maj"):
        out[name] = rng(name)
    return out


def sensitivity(runs):
    """For each swept param, how much does varying it (others fixed at center)
    move each milestone? Returns the spread (max-min) attributable to each."""
    center = dict(alpha=0.28, p=2.0, L_eff=4.0, K=1000.0, A0=0.08)
    drivers = {}
    for knob, vals in SWEEP.items():
        spreads = {}
        for ms in ("tau_halves", "Neff_lt10", "A_maj"):
            times = []
            for v in vals:
                params = dict(center); params[knob] = v
                R = run(params)
                tc = milestones(R)[ms]
                if tc is not None:
                    times.append(tc)
            if len(times) >= 2:
                spreads[ms] = max(times) - min(times)
            else:
                spreads[ms] = None
        drivers[knob] = spreads
    return drivers


def ordering_invariant(runs):
    """Confirm tau* halves BEFORE the attention majority (the robust ordering)
    in every run where both milestones occur within horizon."""
    total = 0
    holds = 0
    both = 0
    for _, _, M in runs:
        total += 1
        th, am = M["tau_halves"], M["A_maj"]
        if th is not None and am is not None:
            both += 1
            if th <= am:
                holds += 1
    return holds, both, total


def figure(runs, path):
    fig, ax = plt.subplots(1, 2, figsize=(15, 6.2))
    fig.suptitle("Mythos-fable scenario ENSEMBLE: observed drivers fixed, "
                 "structural parameters swept\n(a range of scenarios for "
                 "calibration, not a single forecast)",
                 fontsize=12, fontweight="bold")

    # LEFT: fan of N_eff trajectories (normalized by K so spans are comparable)
    a = ax[0]
    for _, R, _ in runs:
        a.semilogy(R["t"], R["Neff"] / R["P"]["K"], color="darkred",
                   lw=0.6, alpha=0.18)
    a.axhline(10.0 / 1000.0, color="gray", ls=":", lw=0.8)
    a.set_title("N_eff / K trajectory fan across the ensemble\n"
                "(each line = one structural-parameter setting)")
    a.set_xlabel("years from scenario start")
    a.set_ylabel("N_eff / K  (log)")

    # overlay A_ai fan on a twin axis (linear)
    a2 = a.twinx()
    for _, R, _ in runs:
        a2.plot(R["t"], R["A_ai"], color="crimson", lw=0.5, alpha=0.10)
    a2.set_ylabel("A_ai (AI attention share)  -- faint red")
    a2.set_ylim(0, 1)

    # RIGHT: milestone-time ranges as horizontal spread bars
    a = ax[1]
    names  = ["tau* halves", "N_eff < 10", "AI attention\nmajority"]
    keys   = ["tau_halves", "Neff_lt10", "A_maj"]
    S = summarize(runs)
    colors = ["teal", "darkred", "darkorange"]
    for j, (k, c) in enumerate(zip(keys, colors)):
        lo, med, hi = S[k]
        if lo is None:
            continue
        y = len(keys) - 1 - j
        a.hlines(y, lo, hi, color=c, lw=8, alpha=0.35)
        a.plot([med], [y], "o", color=c, ms=9)
        a.text(hi + 0.15, y, f"{lo:.1f}-{hi:.1f} yr (med {med:.1f})",
               va="center", fontsize=9, color=c)
    a.set_yticks(range(len(keys)))
    a.set_yticklabels(list(reversed(names)))
    a.set_xlabel("years from scenario start (range across the ensemble)")
    a.set_title("Milestone time RANGES across the ensemble\n"
                "(dot = ensemble median; bar = full spread)")
    a.set_xlim(0, max(11, max(S[k][2] for k in keys if S[k][2]) + 3))
    a.grid(axis="x", alpha=0.25)

    fig.text(0.5, 0.005,
             "Observed drivers (cost decline ~10x/yr, release cadence ~50-60d, "
             "A0 in [0.05,0.15]) are FIXED; structural parameters "
             "(alpha, p, L_eff, K) are SWEPT. No single date is a prediction; "
             "the robust output is the ORDERING and the qualitative shape.",
             ha="center", fontsize=8.5, style="italic", color="dimgray")
    fig.tight_layout(rect=[0, 0.03, 1, 0.93])
    fig.savefig(path, dpi=120)
    plt.close(fig)


if __name__ == "__main__":
    runs = ensemble()
    out_png = "../../../figures/mythos_fable_ensemble.png"
    figure(runs, out_png)

    print("=" * 74)
    print("MYTHOS FABLE -- CALIBRATED SCENARIO ENSEMBLE")
    print("=" * 74)
    print(f"\nEnsemble size: {len(runs)} runs "
          f"(alpha x p x L_eff x K x A0 = "
          f"{'x'.join(str(len(v)) for v in SWEEP.values())})")

    print("\nOBSERVED parameters (fixed):")
    print(f"  cost decline delta  = ln(10) ~ 10x/yr  (Epoch median ~50x/yr; conservative)")
    print(f"  release cadence g   = ln(2.5) ~2.5x/yr (~50-60d median frontier gap)")
    print(f"  A0 in {SWEEP['A0']} (bounded plausible AI-attention estimate)")

    print("\nSWEPT structural parameters:")
    for k in ("alpha", "p", "L_eff", "K"):
        print(f"  {k:6s}: {SWEEP[k]}")

    S = summarize(runs)
    label = {"tau_halves": "tau* halves",
             "Neff_lt10":  "N_eff < 10 ",
             "A_maj":      "AI attn maj"}
    print("\nMILESTONE RANGES across the ensemble (min / median / max, years):")
    for k in ("tau_halves", "Neff_lt10", "A_maj"):
        lo, med, hi = S[k]
        if lo is None:
            print(f"  {label[k]}: never within horizon for some/all")
        else:
            n_never = sum(1 for _, _, M in runs if M[k] is None)
            note = f"  ({n_never} runs never reach it within 10yr)" if n_never else ""
            print(f"  {label[k]}: {lo:.2f} / {med:.2f} / {hi:.2f} yr{note}")

    print("\nSENSITIVITY (spread in years induced by each knob, others centered):")
    drivers = sensitivity(runs)
    print(f"  {'knob':7s} {'tau_halves':>12s} {'Neff<10':>10s} {'A_maj':>10s}")
    for knob, sp in drivers.items():
        def f(x): return f"{x:.2f}" if x is not None else "  -"
        print(f"  {knob:7s} {f(sp['tau_halves']):>12s} "
              f"{f(sp['Neff_lt10']):>10s} {f(sp['A_maj']):>10s}")

    # identify dominant driver per milestone
    print("\n  Dominant driver per milestone (largest spread):")
    for ms, lab in [("Neff_lt10", "N_eff<10"), ("A_maj", "AI majority"),
                    ("tau_halves", "tau* halves")]:
        best = max((k for k in drivers if drivers[k][ms] is not None),
                   key=lambda k: drivers[k][ms], default=None)
        if best:
            print(f"    {lab:12s}: {best} "
                  f"(spread {drivers[best][ms]:.2f} yr)")

    holds, both, total = ordering_invariant(runs)
    print("\nORDERING INVARIANT (tau* halves BEFORE AI attention majority):")
    print(f"  holds in {holds}/{both} runs where both milestones occur "
          f"(of {total} total runs)")
    print(f"  -> ordering robust: {100.0*holds/both:.1f}% of applicable runs"
          if both else "  -> n/a")

    print(f"\nFigure saved: figures/mythos_fable_ensemble.png")
    print("=" * 74)
