#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SECOND FOUNDATION -- PART B: THE CORE SIMULATION
================================================
A low-dimensional dynamical system with an OUT-OF-DISTRIBUTION (OOD) regime change
injected at time tau. We DEMONSTRATE why bounded long-run error after an OOD shock
REQUIRES a standing adaptive detect-and-correct loop (the "Second Foundation"):

  OPEN-LOOP  : free-run the pre-shock model from tau -> forecast error diverges.
  CLOSED-LOOP: an innovation/CUSUM monitor on the normalized residual flags the
               OOD event when it breaches its predicted-covariance threshold, then
               RE-IDENTIFIES the model online -> post-detection error is BOUNDED.

KEY EXTRA RESULT (ties Part A -> Part B): OOD failure is CORRELATED across a model
MONOCULTURE. We run an ensemble of L_eff INDEPENDENT lineages; with high L_eff some
lineage's class happens to contain the novel term (the ensemble is partially self-
correcting); with L_eff -> 1 all lineages share the blind spot and fail together,
so the monoculture REQUIRES an external centralized Second Foundation -- which is
then also the maximal-control / minimal-accountability danger. Hence model
diversity L_eff SUBSTITUTES for centralized control.

HONESTY RAIL: illustrative parameters, no calibration. The simulation demonstrates
the STRUCTURE (divergence vs boundedness; lag; L_eff scaling); the magnitudes are
not a forecast.

Run:  py -3.12 second_foundation_sim.py
Deps: numpy, matplotlib (Agg backend)

Mapping to Asimov: the detector repairs AFTER onset (detection lag > 0) and never
foresees the shock -> the Mule wins the FIRST move; the Second Foundation only
catches up.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------
# TRUE system. Scalar-ish linear-Gaussian state with an OOD regime change at tau.
#   x_{t+1} = a_t * x_t + b_t + q*noise        (process)
#   y_t     = x_t + r*obs_noise                 (observation, H = identity)
# Pre-shock (in-distribution): a = a0, b = 0.
# At t = tau, OOD shock OUTSIDE the model class: the dynamics gain a NEW TERM the
# linear decay model cannot represent -- a persistent drift b' together with a jump
# to a UNIT ROOT (a' = 1). The state therefore stops mean-reverting and instead
# DRIFTS WITHOUT BOUND (x ~ b'*(t-tau), linear growth). The pre-shock model class
# {a*x, a<1, no b} has neither the drift term nor the unit root, so this is
# unmodeled-by-construction epistemic error, not a parameter the model could have
# learned in-distribution. A frozen pre-shock model can never catch a diverging
# state -> open-loop error grows without bound.
# ----------------------------------------------------------------------
def true_system(T, tau, a0=0.6, a_post=1.0, b_post=0.15, q=0.05, r=0.05, seed=0):
    rng = np.random.default_rng(seed)
    x = np.zeros(T)
    y = np.zeros(T)
    x[0] = 0.0
    for t in range(1, T):
        if t < tau:
            a, b = a0, 0.0
        else:
            a, b = a_post, b_post          # OOD: new persistent drift + slower decay
        x[t] = a * x[t - 1] + b + q * rng.standard_normal()
    y = x + r * rng.standard_normal(T)
    return x, y


# ----------------------------------------------------------------------
# The MODEL (fhat): a Kalman filter whose model is the PRE-SHOCK class only.
#   xhat_{t+1|t} = ahat * xhat_t                (NO b term: cannot represent drift)
#   innovation   d_t = y_t - xhat_{t|t-1}
#   S_t          = P_{t|t-1} + R               (predicted innovation covariance)
# OPEN-LOOP: after tau, stop assimilating (free-run the prediction) -> error grows.
# CLOSED-LOOP: keep assimilating; run a CUSUM on the NORMALIZED innovation; on a
#   breach, declare OOD and RE-IDENTIFY (here: inflate process noise Q and ADD a
#   bias/drift estimator b_hat to the model class -- i.e. expand the model online).
# ----------------------------------------------------------------------
def run_filter(y, tau, ahat=0.6, Q=0.05**2, R=0.05**2,
               closed_loop=True, cusum_h=20.0, cusum_k=3.0,
               reident_Qmult=60.0, burn_in=10, seed=0):
    T = len(y)
    xhat = np.zeros(T)          # filtered estimate
    xpred = np.zeros(T)         # one-step prediction
    P = 1.0                     # state covariance
    bhat = 0.0                  # online drift estimator (0 until re-identified)
    a_eff = ahat
    Q_eff = Q

    innov = np.zeros(T)
    S = np.zeros(T)
    nis = np.zeros(T)           # normalized innovation squared (whiteness test)
    err = np.zeros(T)           # |xhat - truth| filled by caller via y proxy; here vs y
    cusum = np.zeros(T)         # one-sided CUSUM on normalized innovation magnitude
    flagged = -1                # detection time (-1 = never)

    g_pos = 0.0
    for t in range(1, T):
        # --- predict ---
        xp = a_eff * xhat[t - 1] + bhat
        Pp = a_eff * P * a_eff + Q_eff
        xpred[t] = xp

        # --- innovation ---
        d = y[t] - xp
        St = Pp + R
        innov[t] = d
        S[t] = St
        nis[t] = d * d / St

        # --- CUSUM on the NORMALIZED INNOVATION SQUARED (NIS) ---
        # In-distribution the NIS d^2/S has mean 1 (whiteness/consistency test, the
        # same chi^2 logic as the project's EnKF misspecification monitor). We use a
        # one-sided Page (1954) CUSUM with reference value cusum_k > 1, so the
        # statistic has NEGATIVE drift when the model is correct (no false alarm) and
        # POSITIVE drift only once the OOD shock makes the innovations large.
        # A short burn-in suppresses the initial-transient false alarm.
        g_pos = max(0.0, g_pos + nis[t] - cusum_k)
        cusum[t] = g_pos

        if closed_loop:
            # update (assimilate)
            K = Pp / St
            xhat[t] = xp + K * d
            P = (1 - K) * Pp
            # change-point detection + online re-identification
            if flagged < 0 and t > burn_in and g_pos > cusum_h:
                flagged = t
            if flagged >= 0:
                # re-identified model: inflate Q (track faster) and estimate drift
                Q_eff = Q * reident_Qmult
                # simple recursive drift estimate from recent innovation
                bhat = 0.9 * bhat + 0.1 * d
        else:
            # OPEN-LOOP: before tau, assimilate normally (fit in-distribution);
            # at/after tau, FREE-RUN the prediction (no update) -> diverges.
            if t < tau:
                K = Pp / St
                xhat[t] = xp + K * d
                P = (1 - K) * Pp
            else:
                xhat[t] = xp          # free run: trust the (wrong) pre-shock model
                P = Pp

    return dict(xhat=xhat, xpred=xpred, innov=innov, S=S, nis=nis,
                cusum=cusum, flagged=flagged)


def integrated_error(xhat, x_true, tau):
    """Sum of |error| from tau to end (the post-shock integrated forecast error)."""
    e = np.abs(xhat[tau:] - x_true[tau:])
    return float(np.sum(e)), e


# ----------------------------------------------------------------------
# ENSEMBLE / L_eff result: correlated blind spots in a monoculture.
# ----------------------------------------------------------------------
# We instantiate an ensemble of model LINEAGES. Each lineage has a "class coverage"
# c_i ~ whether its model class happens to admit the post-shock drift term. In a
# DIVERSE ecosystem (high L_eff) the lineages' coverages are nearly INDEPENDENT, so
# the probability that AT LEAST ONE lineage covers the novel term rises with L_eff.
# In a MONOCULTURE (L_eff -> 1) the coverages are perfectly CORRELATED: either all
# cover it or (for a truly OOD event, by construction) none do -> shared blind spot.
#
# Operationally: a lineage that "covers" the event re-identifies fast (acts like the
# closed-loop filter); one that does NOT behaves like open-loop until/unless the
# CENTRALIZED Second Foundation forces a correction. We measure the ensemble's
# post-shock error (best-available lineage = min error) and the detection lag as a
# function of L_eff.
def ensemble_vs_Leff(T=200, tau=100, n_lineages=40, p_cover_base=0.10,
                     trials=60, seed=1):
    """For a grid of L_eff, draw correlated coverage across lineages and report the
    ensemble post-shock error (min over lineages) and effective detection lag."""
    rng = np.random.default_rng(seed)
    x_true, y = true_system(T, tau, seed=seed)

    # precompute closed-loop (covered) and open-loop (blind) error curves once
    res_closed = run_filter(y, tau, closed_loop=True)
    res_open = run_filter(y, tau, closed_loop=False)
    ie_closed, _ = integrated_error(res_closed["xhat"], x_true, tau)
    ie_open, _ = integrated_error(res_open["xhat"], x_true, tau)
    lag_closed = (res_closed["flagged"] - tau) if res_closed["flagged"] >= 0 else (T - tau)

    Leff_grid = np.array([1.0, 1.5, 2.0, 3.0, 5.0, 8.0, 13.0, 21.0, 34.0])
    mean_err = []
    mean_lag = []
    for Leff in Leff_grid:
        # correlation among lineage coverages controlled by L_eff:
        # rho_cover = 1 - (L_eff - 1)/(n_lineages - 1)  -> L_eff=1 => rho=1 (monoculture)
        rho_cover = float(np.clip(1.0 - (Leff - 1.0) / (n_lineages - 1.0), 0.0, 1.0))
        errs = []
        lags = []
        for _ in range(trials):
            # shared latent (common blind spot) + idiosyncratic per-lineage draw
            u_common = rng.standard_normal()
            cover = np.zeros(n_lineages, dtype=bool)
            for i in range(n_lineages):
                u_i = rng.standard_normal()
                z = np.sqrt(rho_cover) * u_common + np.sqrt(1 - rho_cover) * u_i
                # probability a lineage's class covers the novel term
                cover[i] = z > _ppf_threshold(p_cover_base)
            any_cover = cover.any()
            # ensemble post-shock error = best lineage available:
            # if any lineage covers -> closed-loop-like error; else -> open-loop (blind)
            errs.append(ie_closed if any_cover else ie_open)
            lags.append(lag_closed if any_cover else (T - tau))
        mean_err.append(np.mean(errs))
        mean_lag.append(np.mean(lags))
    return dict(Leff=Leff_grid, mean_err=np.array(mean_err),
                mean_lag=np.array(mean_lag), ie_closed=ie_closed, ie_open=ie_open,
                lag_closed=lag_closed, rho_cover_at=lambda L: 1 - (L - 1) / (n_lineages - 1))


def _ppf_threshold(p):
    """Inverse-normal threshold so P(z > thr) = p, for standard normal z.
    Small p -> large positive threshold (rare coverage of a truly novel term)."""
    # rational approximation (Acklam) is overkill; use a small table via erfinv.
    from math import sqrt
    import numpy as _np
    # P(z>thr)=p => thr = sqrt(2)*erfinv(1-2p)
    return float(_np.sqrt(2.0) * _erfinv(1.0 - 2.0 * p))


def _erfinv(x):
    # Winitzki approximation to erfinv (good to ~1e-3, ample here)
    import numpy as _np
    a = 0.147
    ln = _np.log(1 - x * x)
    term = 2 / (_np.pi * a) + ln / 2
    return _np.sign(x) * _np.sqrt(_np.sqrt(term * term - ln / a) - term)


# ----------------------------------------------------------------------
# Figure
# ----------------------------------------------------------------------
def figure(path, T=200, tau=100, seed=0):
    x_true, y = true_system(T, tau, seed=seed)
    R_open = run_filter(y, tau, closed_loop=False, seed=seed)
    R_closed = run_filter(y, tau, closed_loop=True, seed=seed)
    ie_open, e_open = integrated_error(R_open["xhat"], x_true, tau)
    ie_closed, e_closed = integrated_error(R_closed["xhat"], x_true, tau)
    lag = R_closed["flagged"] - tau if R_closed["flagged"] >= 0 else None
    EE = ensemble_vs_Leff(T=T, tau=tau, seed=seed + 1)

    t = np.arange(T)
    fig, ax = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle("SECOND FOUNDATION  Part B -- OOD shock: open-loop DIVERGES, "
                 "closed-loop (detect+re-identify) is BOUNDED\n"
                 "(THEORETICAL SCENARIO, illustrative parameters -- structure is the "
                 "claim, magnitudes are not calibrated)",
                 fontsize=12, fontweight="bold")

    # (0,0) trajectories
    a = ax[0, 0]
    a.plot(t, x_true, color="black", lw=2, label="true state x_t")
    a.plot(t, R_open["xhat"], color="firebrick", lw=1.6, ls="--",
           label="open-loop forecast (free-run model)")
    a.plot(t, R_closed["xhat"], color="seagreen", lw=1.6,
           label="closed-loop (Second Foundation)")
    a.axvline(tau, color="crimson", ls=":", lw=1.5, label=f"tau (OOD shock) = {tau}")
    if R_closed["flagged"] >= 0:
        a.axvline(R_closed["flagged"], color="navy", ls="-.", lw=1.2,
                  label=f"OOD flagged @ {R_closed['flagged']} (lag {lag})")
    a.set_title("State vs forecasts (OOD = new drift term outside model class)")
    a.set_xlabel("t"); a.set_ylabel("x"); a.legend(fontsize=8)

    # (0,1) absolute forecast error vs t
    a = ax[0, 1]
    a.semilogy(t[tau:], np.abs(R_open["xhat"][tau:] - x_true[tau:]) + 1e-6,
               color="firebrick", lw=2, label=f"open-loop |error|  (int = {ie_open:.1f})")
    a.semilogy(t[tau:], np.abs(R_closed["xhat"][tau:] - x_true[tau:]) + 1e-6,
               color="seagreen", lw=2, label=f"closed-loop |error|  (int = {ie_closed:.1f})")
    a.axvline(tau, color="crimson", ls=":", lw=1.5)
    if R_closed["flagged"] >= 0:
        a.axvline(R_closed["flagged"], color="navy", ls="-.", lw=1.2)
    a.set_title("Post-shock |forecast error| (log): open-loop grows unbounded, "
                "closed-loop bounded")
    a.set_xlabel("t"); a.set_ylabel("|error| (log)"); a.legend(fontsize=8)

    # (1,0) CUSUM detector
    a = ax[1, 0]
    a.plot(t, R_closed["cusum"], color="darkorange", lw=2, label="CUSUM g_t (Page 1954, on NIS)")
    a.axhline(20.0, color="gray", ls="--", lw=1, label="threshold h")
    a.axvline(tau, color="crimson", ls=":", lw=1.5, label="tau (OOD onset)")
    if R_closed["flagged"] >= 0:
        a.axvline(R_closed["flagged"], color="navy", ls="-.", lw=1.2,
                  label=f"flag (lag = {lag} steps)")
    a.set_title("Innovation CUSUM monitor: breaches threshold AFTER onset "
                "(repairs late, never foresees)")
    a.set_xlabel("t"); a.set_ylabel("CUSUM statistic"); a.legend(fontsize=8)

    # (1,1) ensemble: post-shock error & lag vs L_eff
    a = ax[1, 1]
    a.semilogx(EE["Leff"], EE["mean_err"], color="indigo", lw=2, marker="o",
               label="ensemble post-shock integrated error")
    a.axhline(EE["ie_closed"], color="seagreen", ls=":", lw=1,
              label=f"all-covered floor ({EE['ie_closed']:.0f})")
    a.axhline(EE["ie_open"], color="firebrick", ls=":", lw=1,
              label=f"monoculture blind ceiling ({EE['ie_open']:.0f})")
    a.set_xlabel("L_eff (independent model lineages, log)")
    a.set_ylabel("ensemble post-shock integrated error")
    a.set_title("Diversity substitutes for control: high L_eff -> some lineage catches "
                "it;\nL_eff -> 1 -> shared blind spot -> needs external Second Foundation")
    a2 = a.twinx()
    a2.semilogx(EE["Leff"], EE["mean_lag"], color="darkorange", lw=1.6, ls="--",
                marker="s", label="effective detection lag")
    a2.set_ylabel("effective detection lag (steps)")
    lines1, lab1 = a.get_legend_handles_labels()
    lines2, lab2 = a2.get_legend_handles_labels()
    a.legend(lines1 + lines2, lab1 + lab2, fontsize=7, loc="upper right")

    fig.text(0.5, 0.005,
             "Open-loop = Internal Model Principle violated (no model of the disturbance) "
             "-> divergence. Closed-loop = adaptive detect+re-identify = the Second "
             "Foundation. Monoculture (low L_eff) shares the blind spot -> centralized "
             "controller becomes necessary AND dangerous.",
             ha="center", fontsize=8.5, style="italic", color="dimgray")
    fig.tight_layout(rect=[0, 0.03, 1, 0.94])
    fig.savefig(path, dpi=110)
    plt.close(fig)

    return dict(ie_open=ie_open, ie_closed=ie_closed, lag=lag,
                flagged=R_closed["flagged"], tau=tau, EE=EE)


def main():
    png = "second_foundation_sim.png"
    R = figure(png)
    EE = R["EE"]

    print("=" * 78)
    print("SECOND FOUNDATION  PART B -- OOD SHOCK SIMULATION "
          "(illustrative, NOT a forecast)")
    print("=" * 78)
    print(f"\nOOD shock at tau = {R['tau']} (new drift term OUTSIDE the model class).")
    print("\nHEADLINE:")
    print(f"  open-loop   integrated post-shock error : {R['ie_open']:.1f}")
    print(f"  closed-loop integrated post-shock error : {R['ie_closed']:.1f}")
    print(f"  reduction factor (open / closed)        : {R['ie_open']/R['ie_closed']:.1f}x")
    print(f"  detection lag (flag - tau)              : {R['lag']} steps "
          f"(flagged at t={R['flagged']})")
    print("  -> the controller repairs AFTER onset, never foresees "
          "(Asimov: the Mule wins move 1).")

    print("\nENSEMBLE vs L_eff (correlated blind spots in a monoculture):")
    print(f"  all-covered floor (best case)   : {EE['ie_closed']:.1f}")
    print(f"  monoculture blind ceiling       : {EE['ie_open']:.1f}")
    print(f"  {'L_eff':>6s} {'post-shock err':>15s} {'detect lag':>11s}")
    for L, e, lg in zip(EE["Leff"], EE["mean_err"], EE["mean_lag"]):
        print(f"  {L:>6.1f} {e:>15.1f} {lg:>11.1f}")
    print("  -> low L_eff: error pinned near the BLIND ceiling (all lineages fail "
          "together);")
    print("     high L_eff: error falls toward the covered floor (some lineage catches "
          "it).")
    print("     Diversity L_eff SUBSTITUTES for the centralized Second Foundation.")
    print(f"\nFigure saved: {png}")
    print("=" * 78)
    return R


if __name__ == "__main__":
    main()
