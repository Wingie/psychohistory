#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THE MYTHOS FABLE SCENARIO
=========================
A SPECULATIVE forward projection applying the bounded-psychohistory framework
to AI itself. NOT a measured or validated prediction. Illustrative parameters,
no empirical calibration. The framework's own thesis (L5 criticality) says the
TIMING and BRANCH here are precisely what it cannot forecast; what is robust is
the SHAPE: monotone attention capture -> N_eff collapse -> critical regime that
is simultaneously less self-predictable (chi diverges, tau* -> 0) and more
steerable (frontier leverage rises).

Run:  py -3.12 model.py
Deps: numpy, matplotlib (Agg backend)

State (stocks), deterministic difference system, monthly steps over ~10 years:
  C_f(t)   FRONTIER / unrestricted capability (the major players). Compounds.
  C_d(t)   DEPLOYED / restricted consumer capability = C_f*(1-tax). The mass.
  kappa(t) cost per token, exponential decay (~10x/yr down) -- real-ish input.
  A_ai(t)  AI share of human attention in [0,1]; A_human = 1 - A_ai (conserved=1).
  rho(t)   cross-human correlation / homogenization, rises with A_ai.
  N_eff(t) = K / (1 + (K-1)*rho)   -- the verified criticality identity.

Derived readouts:
  chi(t)   controllability / susceptibility proxy ~ 1/N_eff (diverges at crit).
  tau*(t)  skill / forecast horizon, shrinks with homogenization (~ N_eff/K).
  L(t)     frontier leverage = (C_f - C_d) * (1 - N_eff/K).
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# PARAMETERS  (HONESTY: which are real-ish vs guessed)
# ----------------------------------------------------------------------
# real-ish (observed trends):
#   delta  -- cost/token falls ~10x/yr  (well documented, REAL-ISH)
#   g      -- frequent frontier releases, ~2-3x effective capability/yr (REAL-ISH trend)
# guessed (no calibration -- these set the DATES and are NOT a forecast):
#   alpha  -- attention capture rate          (GUESSED)
#   p      -- homogenization exponent          (GUESSED)
#   K      -- baseline independent communities  (GUESSED)
#   tax    -- alignment/safety gap             (GUESSED)
#   churn, rho_max, value squashing scale       (GUESSED)

def default_params():
    return dict(
        years      = 10.0,
        dt         = 1.0/12.0,      # monthly steps
        # --- capability ---
        Cf0        = 1.0,
        g          = np.log(2.5),   # ~2.5x / year frontier growth  (REAL-ISH trend)
        super_exp  = False,         # toggle: mild recursive self-improvement
        rsi        = 0.04,          # super-exponential coefficient (GUESSED)
        tax        = 0.30,          # alignment/safety tax: deployed lags frontier (GUESSED)
        # --- cost ---
        kappa0     = 1.0,
        delta      = np.log(10.0),  # ~10x / year cost drop  (REAL-ISH)
        # --- attention capture (logistic) ---
        A0         = 0.05,          # initial AI attention share
        alpha      = 0.28,          # capture rate (GUESSED)
        churn      = 0.10,          # attention decay back to human (GUESSED)
        val_scale  = 6.0,           # squashing scale for value pull (GUESSED)
        # --- homogenization / blocks ---
        rho_max    = 0.995,         # ceiling on cross-human correlation (GUESSED)
        p          = 1.6,           # homogenization exponent, rho = rho_max*A_ai^p (GUESSED)
        K          = 1000.0,        # baseline number of independent human blocks (GUESSED)
        tau0       = 1.0,           # nominal forecast horizon at rho=0 (units: normalized)
    )


def run(params=None):
    P = default_params()
    if params:
        P.update(params)

    dt    = P["dt"]
    n     = int(round(P["years"] / dt)) + 1
    t     = np.linspace(0.0, P["years"], n)

    Cf    = np.zeros(n)
    Cd    = np.zeros(n)
    kappa = np.zeros(n)
    A_ai  = np.zeros(n)
    rho   = np.zeros(n)
    Neff  = np.zeros(n)
    chi   = np.zeros(n)
    tau   = np.zeros(n)
    Lev   = np.zeros(n)
    value = np.zeros(n)

    Cf[0]   = P["Cf0"]
    A_ai[0] = P["A0"]
    K       = P["K"]

    def derive(i):
        # deployed capability lags frontier by the alignment/safety tax
        Cd[i]    = Cf[i] * (1.0 - P["tax"])
        kappa[i] = P["kappa0"] * np.exp(-P["delta"] * t[i])
        # value pull: rises with deployed capability, falls with cost; squashed to (0,1)
        raw      = Cd[i] / kappa[i]
        value[i] = raw / (raw + P["val_scale"] * Cd[0] / kappa[0] *
                          np.exp(0.0))   # normalized; logistic-like saturation below
        # homogenization & effective independence
        rho[i]   = P["rho_max"] * (A_ai[i] ** P["p"])
        Neff[i]  = K / (1.0 + (K - 1.0) * rho[i])
        # readouts
        chi[i]   = 1.0 / Neff[i]                       # susceptibility / controllability
        tau[i]   = P["tau0"] * (Neff[i] / K)           # skill horizon ~ N_eff/K
        Lev[i]   = (Cf[i] - Cd[i]) * (1.0 - Neff[i] / K)

    derive(0)

    for i in range(1, n):
        # --- frontier capability: compounding, optional mild super-exponential ---
        gi = P["g"]
        if P["super_exp"]:
            gi = P["g"] + P["rsi"] * np.log1p(Cf[i-1])   # recursive improvement toggle
        Cf[i] = Cf[i-1] * np.exp(gi * dt)

        # --- attention capture (logistic, conserved A_human = 1 - A_ai) ---
        # value pull at previous step
        Cd_prev    = Cf[i-1] * (1.0 - P["tax"])
        kappa_prev = P["kappa0"] * np.exp(-P["delta"] * t[i-1])
        raw_prev   = Cd_prev / kappa_prev
        v0         = Cd[0] if Cd[0] > 0 else P["Cf0"] * (1.0 - P["tax"])
        k0         = P["kappa0"]
        vnorm      = raw_prev / (raw_prev + P["val_scale"] * (v0 / k0))  # in (0,1)

        dA = (P["alpha"] * vnorm * (1.0 - A_ai[i-1]) - P["churn"] * A_ai[i-1])
        A_ai[i] = np.clip(A_ai[i-1] + dt * dA, 0.0, 1.0)

        derive(i)

    A_hum = 1.0 - A_ai

    return dict(t=t, Cf=Cf, Cd=Cd, kappa=kappa, A_ai=A_ai, A_hum=A_hum,
                rho=rho, Neff=Neff, chi=chi, tau=tau, Lev=Lev, value=value, P=P)


def crossing_time(t, y, thr, rising=True):
    """First time y crosses thr (linear interp). None if never."""
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
    m = {}
    m["A_ai>0.25"] = crossing_time(t, R["A_ai"], 0.25, rising=True)
    m["A_ai>0.50"] = crossing_time(t, R["A_ai"], 0.50, rising=True)
    m["Neff<10"]   = crossing_time(t, R["Neff"], 10.0, rising=False)
    m["Neff<2"]    = crossing_time(t, R["Neff"], 2.0,  rising=False)
    tau0 = R["tau"][0]
    m["tau*halves"] = crossing_time(t, R["tau"], 0.5 * tau0, rising=False)
    return m


def fmt_months(y):
    if y is None:
        return "never (within horizon)"
    return f"{y:.2f} yr (~month {y*12:.0f})"


def figure(R, path):
    t = R["t"]
    fig, ax = plt.subplots(2, 3, figsize=(16, 9))
    fig.suptitle("THE MYTHOS FABLE  -  AI capability/cost -> human attention capture -> "
                 "N_eff collapse\n(SPECULATIVE SCENARIO, illustrative parameters - NOT a "
                 "forecast; dates are illustrative only)", fontsize=12, fontweight="bold")

    # mark critical crossing: N_eff < 10
    tc = crossing_time(t, R["Neff"], 10.0, rising=False)
    tA = crossing_time(t, R["A_ai"], 0.50, rising=True)

    def mark(a):
        if tc is not None:
            a.axvline(tc, color="crimson", ls="--", lw=1.2, alpha=0.8)
        if tA is not None:
            a.axvline(tA, color="darkorange", ls=":", lw=1.2, alpha=0.8)

    # (0,0) attention shares
    a = ax[0, 0]
    a.plot(t, R["A_ai"], color="crimson", lw=2, label="A_ai (AI attention share)")
    a.plot(t, R["A_hum"], color="steelblue", lw=2, label="A_human = 1 - A_ai")
    a.axhline(0.5, color="gray", ls=":", lw=0.8)
    a.set_title("Attention shares (conserved, sum = 1)")
    a.set_xlabel("years"); a.set_ylabel("share"); a.set_ylim(0, 1); a.legend(fontsize=8); mark(a)

    # (0,1) capability frontier vs deployed (log)
    a = ax[0, 1]
    a.semilogy(t, R["Cf"], color="black", lw=2, label="C_f frontier (unrestricted)")
    a.semilogy(t, R["Cd"], color="seagreen", lw=2, ls="--", label="C_d deployed (restricted)")
    a.set_title("Capability: frontier vs deployed (alignment/safety tax gap)")
    a.set_xlabel("years"); a.set_ylabel("capability (log)"); a.legend(fontsize=8); mark(a)

    # (0,2) cost per token (log)
    a = ax[0, 2]
    a.semilogy(t, R["kappa"], color="purple", lw=2, label="kappa (cost/token)")
    a.set_title("Cost per token (~10x/yr down, real-ish)")
    a.set_xlabel("years"); a.set_ylabel("cost (log)"); a.legend(fontsize=8); mark(a)

    # (1,0) N_eff collapse (log)
    a = ax[1, 0]
    a.semilogy(t, R["Neff"], color="darkred", lw=2, label="N_eff (independent human blocks)")
    a.axhline(10, color="crimson", ls="--", lw=1, label="N_eff = 10 (critical)")
    a.axhline(2,  color="maroon", ls=":", lw=1, label="N_eff = 2")
    a.set_title("N_eff = K/(1+(K-1)*rho) collapsing")
    a.set_xlabel("years"); a.set_ylabel("N_eff (log)"); a.legend(fontsize=8); mark(a)

    # (1,1) skill horizon tau*
    a = ax[1, 1]
    a.plot(t, R["tau"] / R["tau"][0], color="teal", lw=2, label="tau* / tau*_0 (skill horizon)")
    a.axhline(0.5, color="gray", ls=":", lw=0.8, label="half horizon")
    a.set_title("Skill horizon tau* shrinking (self-unpredictability)")
    a.set_xlabel("years"); a.set_ylabel("normalized tau*"); a.set_ylim(0, 1.05)
    a.legend(fontsize=8); mark(a)

    # (1,2) controllability chi and frontier leverage L
    a = ax[1, 2]
    a.plot(t, R["chi"] / R["chi"][0], color="darkorange", lw=2,
           label="chi/chi_0 (controllability/susceptibility)")
    a.set_xlabel("years"); a.set_ylabel("chi (norm)")
    a.set_yscale("log")
    a2 = a.twinx()
    a2.plot(t, R["Lev"], color="indigo", lw=2, ls="--", label="L (frontier leverage)")
    a2.set_ylabel("frontier leverage L")
    a.set_title("Controllability chi (log) & frontier leverage L rising")
    lines1, lab1 = a.get_legend_handles_labels()
    lines2, lab2 = a2.get_legend_handles_labels()
    a.legend(lines1 + lines2, lab1 + lab2, fontsize=8, loc="upper left")
    mark(a)

    fig.text(0.5, 0.005,
             "Red dashed = CRITICAL CROSSING (N_eff < 10).  Orange dotted = A_ai crosses 0.5.  "
             "Parameters are illustrative; the SHAPE is the claim, the dates are not.",
             ha="center", fontsize=9, style="italic", color="dimgray")
    fig.tight_layout(rect=[0, 0.02, 1, 0.95])
    fig.savefig(path, dpi=110)
    plt.close(fig)


def sensitivity():
    """Vary g (release rate), delta (cost decline), tax. Report N_eff<10 crossing."""
    rows = []
    base = default_params()
    grid = {
        "g":     [np.log(1.8), np.log(2.5), np.log(3.5)],      # 1.8x / 2.5x / 3.5x per yr (REAL-ISH)
        "delta": [np.log(5.0), np.log(10.0), np.log(20.0)],     # 5x / 10x / 20x per yr cost drop (REAL-ISH)
        "tax":   [0.15, 0.30, 0.50],                            # alignment/safety gap (GUESSED)
        "alpha": [0.15, 0.28, 0.50],                            # attention capture rate (GUESSED - dominant)
        "p":     [1.2, 1.6, 2.2],                               # homogenization exponent (GUESSED)
    }
    for knob, vals in grid.items():
        for v in vals:
            R = run({knob: v})
            tc = crossing_time(R["t"], R["Neff"], 10.0, rising=False)
            ta = crossing_time(R["t"], R["A_ai"], 0.50, rising=True)
            # human-readable knob value
            if knob == "g":
                disp = f"{np.exp(v):.1f}x/yr"
            elif knob == "delta":
                disp = f"{np.exp(v):.0f}x/yr"
            else:
                disp = f"{v:.2f}"
            real = knob in ("g", "delta")
            rows.append((knob, disp, real,
                         None if tc is None else round(tc, 2),
                         None if ta is None else round(ta, 2)))
    return rows


if __name__ == "__main__":
    R = run()
    png = "mythos_fable_trajectory.png"
    figure(R, png)

    M = milestones(R)
    print("=" * 70)
    print("THE MYTHOS FABLE SCENARIO  (illustrative parameters - NOT a forecast)")
    print("=" * 70)
    print("\nBASELINE MILESTONES:")
    for k, v in M.items():
        print(f"  {k:14s}: {fmt_months(v)}")

    print("\nKEY STATE AT END (t = {:.0f} yr):".format(R['t'][-1]))
    print(f"  A_ai   = {R['A_ai'][-1]:.3f}   A_human = {R['A_hum'][-1]:.3f}")
    print(f"  rho    = {R['rho'][-1]:.4f}")
    print(f"  N_eff  = {R['Neff'][-1]:.2f}  (from K={R['P']['K']:.0f})")
    print(f"  tau*   = {R['tau'][-1]/R['tau'][0]:.4f} x nominal")
    print(f"  chi    = {R['chi'][-1]/R['chi'][0]:.1f} x baseline")
    print(f"  Cf/Cd  = {R['Cf'][-1]:.1f} / {R['Cd'][-1]:.1f}")

    # super-exponential toggle comparison
    Rse = run({"super_exp": True})
    tc0 = crossing_time(R["t"],  R["Neff"], 10.0, rising=False)
    tcs = crossing_time(Rse["t"], Rse["Neff"], 10.0, rising=False)
    print("\nRECURSIVE-IMPROVEMENT TOGGLE (super_exp):")
    print(f"  N_eff<10 crossing: {fmt_months(tc0)}  ->  {fmt_months(tcs)} (with RSI)")

    print("\nSENSITIVITY (N_eff<10 crossing yr | A_ai>0.5 crossing yr):")
    print(f"  {'knob':6s} {'value':10s} {'kind':9s} {'Neff<10':>10s} {'A_ai>0.5':>10s}")
    cross_real, cross_guess = [], []
    for knob, disp, real, tc, ta in sensitivity():
        kind = "REAL-ISH" if real else "GUESSED"
        print(f"  {knob:6s} {disp:10s} {kind:9s} {str(tc):>10s} {str(ta):>10s}")
        if tc is not None:
            (cross_real if real else cross_guess).append(tc)
    if cross_real:
        print(f"\n  N_eff<10 crossing range, REAL-ISH knobs (g, delta): "
              f"{min(cross_real):.2f} - {max(cross_real):.2f} yr")
    if cross_guess:
        print(f"  N_eff<10 crossing range, GUESSED knobs (tax, alpha, p): "
              f"{min(cross_guess):.2f} - {max(cross_guess):.2f} yr")
    allc = cross_real + cross_guess
    if allc:
        print(f"  N_eff<10 crossing range, ALL knobs: "
              f"{min(allc):.2f} - {max(allc):.2f} yr")
    print("  -> collapse is QUALITATIVELY ROBUST (it always happens); the DATE is "
          "parameter-sensitive,\n     dominated by the GUESSED capture rate -> the date is NOT a forecast.")
    print(f"\nFigure saved: {png}")
    print("=" * 70)
