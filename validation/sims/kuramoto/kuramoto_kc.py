#!/usr/bin/env python3
"""
C-KC : Kuramoto synchronization demo for the psychohistory paper.

Backs three things the paper (psychohistory.tex, sec:nearcond / sec:blocks) reuses:

  1. The mean-field Kuramoto critical coupling  K_c = 2 / (pi * g(0))   (Strogatz 2000).
  2. The order parameter  r = |(1/N) sum_j exp(i theta_j)|  as the FIRST-MOMENT
     phase-coherence synchrony observable that detects the transition.
  3. The paper's first-moment-vs-second-moment distinction (sec:blocks): r (and a
     macroscopic variance-ratio N_eff) catch the collapse of independence, whereas a
     Pearson correlation of the oscillators' *fluctuations around the common motion*
     does NOT, so an N_eff built from that Pearson correlation is the WRONG metric.

This is an INTERNAL-CONSISTENCY check of the math the paper imports (Kuramoto /
Strogatz 2000), not an empirical social claim. The model is the textbook all-to-all
Kuramoto model; the only thing being verified is that the paper's quoted formula and
its choice of synchrony observable are self-consistent and reproduce the known result.

Model:   dtheta_i/dt = omega_i + (K/N) sum_j sin(theta_j - theta_i)
Natural frequencies omega_i ~ g, with g a unimodal symmetric distribution.

We use a LORENTZIAN (Cauchy) g because it has an EXACT closed-form K_c:
    g(w) = (gamma/pi) / (w^2 + gamma^2),  g(0) = 1/(pi*gamma)
    => K_c = 2/(pi*g(0)) = 2*gamma   (exact, finite-N-corrected only by sampling).
We also run a GAUSSIAN g as a secondary check (g(0)=1/(sigma*sqrt(2pi))).

Run:  py -3.12 kuramoto_kc.py
Deps: numpy, matplotlib (Agg).
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = __file__.rsplit("/", 1)[0] if "/" in __file__ else "."
OUT = OUT.replace("\\", "/")

# ---------------------------------------------------------------------------
# integrator
# ---------------------------------------------------------------------------
def kuramoto_run(omega, K, dt=0.05, T=400.0, transient=200.0, seed=0,
                 record=False):
    """RK4 integrate the all-to-all Kuramoto model.

    Returns steady-state mean order parameter r (time-averaged over the
    post-transient window). If record=True also returns the recorded phase
    trajectory (n_rec_steps x N) for the post-transient window.
    """
    rng = np.random.default_rng(seed)
    N = omega.size
    theta = rng.uniform(0, 2 * np.pi, N)
    nsteps = int(T / dt)
    ntrans = int(transient / dt)

    def deriv(th):
        # mean field: (K/N) sum_j sin(theta_j - theta_i)
        # = K * Im( e^{-i theta_i} * (1/N) sum_j e^{i theta_j} )
        z = np.exp(1j * th).mean()           # complex order parameter
        return omega + K * (z * np.exp(-1j * th)).imag

    r_acc = []
    rec = [] if record else None
    for s in range(nsteps):
        k1 = deriv(theta)
        k2 = deriv(theta + 0.5 * dt * k1)
        k3 = deriv(theta + 0.5 * dt * k2)
        k4 = deriv(theta + dt * k3)
        theta = theta + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        if s >= ntrans:
            r_acc.append(np.abs(np.exp(1j * theta).mean()))
            if record:
                rec.append(theta.copy())
    r = float(np.mean(r_acc))
    if record:
        return r, np.array(rec)
    return r


# ---------------------------------------------------------------------------
# distributions and their exact K_c
# ---------------------------------------------------------------------------
def lorentzian_omega(N, gamma, seed):
    rng = np.random.default_rng(seed)
    # inverse-CDF sampling of Cauchy(0, gamma)
    u = rng.uniform(0, 1, N)
    return gamma * np.tan(np.pi * (u - 0.5))

def gaussian_omega(N, sigma, seed):
    rng = np.random.default_rng(seed)
    return rng.normal(0.0, sigma, N)

def kc_theory(g0):
    return 2.0 / (np.pi * g0)


# ---------------------------------------------------------------------------
# empirical K_c from a sweep: fit r=0 below, r=sqrt-rise above.
# Standard estimator: in the partially-locked branch r ~ sqrt((K-K_c)/K_c)
# (mean-field, Strogatz 2000). We locate the knee by the largest-r-curvature /
# by linear extrapolation of r^2 vs K in the rising region back to r^2 -> 0.
# ---------------------------------------------------------------------------
def empirical_kc(Ks, rs, r_floor=0.05, r_hi=0.6):
    Ks = np.asarray(Ks); rs = np.asarray(rs)
    # use the rising branch: r between r_floor and r_hi, where r^2 ~ linear in K
    mask = (rs > r_floor) & (rs < r_hi)
    if mask.sum() < 3:
        # fall back to widen
        mask = (rs > r_floor)
    x = Ks[mask]; y = rs[mask] ** 2          # r^2 linear in K near onset
    A = np.vstack([x, np.ones_like(x)]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    kc_emp = -intercept / slope              # K where r^2 -> 0
    return float(kc_emp), float(slope), float(intercept)


# ---------------------------------------------------------------------------
# MAIN SWEEP (Lorentzian, exact K_c)
# ---------------------------------------------------------------------------
N = 2000
GAMMA = 0.5                                   # Lorentzian half-width
g0_lor = 1.0 / (np.pi * GAMMA)
KC_TH_LOR = kc_theory(g0_lor)                 # = 2*gamma = 1.0
omega_lor = lorentzian_omega(N, GAMMA, seed=7)

Ks = np.linspace(0.0, 3.0, 31)
rs = []
# second-moment machinery, recorded at a subset of K to keep it cheap
neff_pearson = []      # WRONG metric: N_eff from Pearson corr of fluctuations
neff_varratio = []     # CORRECT metric: macro variance-ratio N_eff
r2_curve = []          # r^2 (the exact pairwise block coherence under MF factorization)

for K in Ks:
    r, rec = kuramoto_run(omega_lor, K, seed=11, record=True,
                          T=300.0, transient=150.0)
    rs.append(r)
    r2_curve.append(r * r)

    # ---- second-moment metrics on the recorded phase trajectory ----
    # Work with the "velocity" fluctuation: phases drift, so use sin(theta) as a
    # bounded observable x_i(t) = sin(theta_i(t)). The common (mean-field) motion is
    # the population mean; fluctuations are the residual after removing it.
    x = np.sin(rec)                           # (Tsteps x N)
    xbar = x.mean(axis=1, keepdims=True)      # common motion (macro variable)
    fluct = x - xbar                          # residual fluctuations per oscillator

    # WRONG metric: Pearson correlation of the residual fluctuations between
    # oscillators, averaged off-diagonal -> N_eff = N/(1+(N-1)*rho_pearson).
    # Subsample columns to keep the correlation matrix cheap.
    idx = np.random.default_rng(3).choice(N, size=120, replace=False)
    F = fluct[:, idx]
    F = F - F.mean(axis=0, keepdims=True)
    sd = F.std(axis=0)
    keep = sd > 1e-9
    F = F[:, keep] / sd[keep]
    C = (F.T @ F) / F.shape[0]
    m = C.shape[0]
    off = (C.sum() - np.trace(C)) / (m * (m - 1))
    rho_pearson = max(off, 0.0)
    neff_pearson.append(N / (1 + (N - 1) * rho_pearson))

    # CORRECT metric: macro variance-ratio N_eff = Var_t(single)/Var_t(macro mean).
    # If the units were independent the population mean would have variance
    # 1/N of a single unit's; as they synchronize the macro variable keeps full
    # variance and the ratio -> 1.
    var_single = x.var(axis=0).mean()         # mean temporal variance of one unit
    var_macro = xbar[:, 0].var()              # temporal variance of the macro mean
    neff_varratio.append(var_single / var_macro if var_macro > 1e-12 else float(N))

rs = np.array(rs)
kc_emp_lor, slope, intercept = empirical_kc(Ks, rs)

# ---------------------------------------------------------------------------
# GAUSSIAN secondary check
# ---------------------------------------------------------------------------
SIGMA = 1.0
g0_gauss = 1.0 / (SIGMA * np.sqrt(2 * np.pi))
KC_TH_GAUSS = kc_theory(g0_gauss)             # = 2/(pi*g0) = 2*sigma*sqrt(2/pi)
omega_g = gaussian_omega(N, SIGMA, seed=7)
Ks_g = np.linspace(0.0, 4.0, 33)
rs_g = np.array([kuramoto_run(omega_g, K, seed=11, T=260.0, transient=130.0)
                 for K in Ks_g])
kc_emp_gauss, _, _ = empirical_kc(Ks_g, rs_g)

# ---------------------------------------------------------------------------
# FIGURE
# ---------------------------------------------------------------------------
fig, axs = plt.subplots(1, 3, figsize=(15, 4.3))

# panel A: r vs K with K_c marked (Lorentzian, exact)
axs[0].plot(Ks, rs, "o-", color="C0", label="r (order parameter)")
axs[0].axvline(KC_TH_LOR, color="r", ls="--", lw=1.2,
               label=f"$K_c$ theory = 2/($\\pi g(0)$) = {KC_TH_LOR:.3f}")
axs[0].axvline(kc_emp_lor, color="g", ls=":", lw=1.6,
               label=f"$K_c$ empirical = {kc_emp_lor:.3f}")
axs[0].set_xlabel("coupling K"); axs[0].set_ylabel("steady-state r")
axs[0].set_title("A  Kuramoto transition (Lorentzian g)\n$r\\approx0$ below $K_c$, rises above")
axs[0].legend(fontsize=8); axs[0].set_ylim(-0.02, 1.02)

# panel B: the metric distinction -- N_eff: only the right metric collapses
axs[1].semilogy(Ks, neff_pearson, "o-", color="C3",
                label=r"$N_{\rm eff}$ from Pearson corr of fluctuations (WRONG)")
axs[1].semilogy(Ks, neff_varratio, "s-", color="C2",
                label=r"$N_{\rm eff}$ from macro variance-ratio (CORRECT)")
axs[1].axvline(KC_TH_LOR, color="r", ls="--", lw=1.0)
axs[1].axhline(1, color="k", ls=":", lw=0.8)
axs[1].set_xlabel("coupling K"); axs[1].set_ylabel(r"$N_{\rm eff}$ (log)")
axs[1].set_title("B  first vs second moment\nonly the right metric sees independence collapse")
axs[1].legend(fontsize=8)

# panel C: r (first moment) detects onset; r^2 = exact MF pairwise block coherence
axs[2].plot(Ks, rs, "o-", color="C0", label="r  (first-moment phase coherence)")
axs[2].plot(Ks, r2_curve, "^-", color="C4",
            label=r"$r^2$  (MF pairwise coherence $\to\varrho$)")
# overlay the normalized Pearson fluctuation-corr to show it stays flat-ish
rho_norm = np.array([1.0 / nf * N for nf in neff_pearson])  # recover rho approx
axs[2].axvline(KC_TH_LOR, color="r", ls="--", lw=1.0)
axs[2].set_xlabel("coupling K"); axs[2].set_ylabel("coherence")
axs[2].set_title("C  $r$ and $r^2$ rise at $K_c$\n(these drive $\\varrho$ in the Kish $N_{\\rm eff}$)")
axs[2].legend(fontsize=8); axs[2].set_ylim(-0.02, 1.02)

fig.tight_layout()
figpath = OUT + "/kuramoto_kc.png"
fig.savefig(figpath, dpi=120)

# ---------------------------------------------------------------------------
# REPORT NUMBERS
# ---------------------------------------------------------------------------
def agree(a, b):
    return 100.0 * abs(a - b) / b

print("=" * 70)
print("C-KC  Kuramoto K_c / order-parameter internal-consistency check")
print("=" * 70)
print(f"N oscillators          : {N}")
print()
print("LORENTZIAN g (exact K_c):")
print(f"  gamma                : {GAMMA}")
print(f"  g(0)                 : {g0_lor:.6f}")
print(f"  K_c theory  = 2/(pi g(0)) : {KC_TH_LOR:.4f}")
print(f"  K_c empirical (sweep)     : {kc_emp_lor:.4f}")
print(f"  relative error            : {agree(kc_emp_lor, KC_TH_LOR):.1f}%")
print(f"  r at K=0                  : {rs[0]:.3f}")
print(f"  r at K=2*K_c              : {rs[np.argmin(np.abs(Ks-2*KC_TH_LOR))]:.3f}")
print()
print("GAUSSIAN g (secondary):")
print(f"  sigma                : {SIGMA}")
print(f"  g(0)                 : {g0_gauss:.6f}")
print(f"  K_c theory                : {KC_TH_GAUSS:.4f}")
print(f"  K_c empirical (sweep)     : {kc_emp_gauss:.4f}")
print(f"  relative error            : {agree(kc_emp_gauss, KC_TH_GAUSS):.1f}%")
print()
print("METRIC DISTINCTION (Lorentzian sweep):")
print(f"  N_eff(Pearson-fluct)  K=0 -> K=3 : {neff_pearson[0]:.0f} -> {neff_pearson[-1]:.0f}")
print(f"  N_eff(macro var-ratio) K=0 -> K=3: {neff_varratio[0]:.0f} -> {neff_varratio[-1]:.2f}")
print(f"  r                     K=0 -> K=3 : {rs[0]:.3f} -> {rs[-1]:.3f}")
print(f"  r^2                   K=0 -> K=3 : {r2_curve[0]:.3f} -> {r2_curve[-1]:.3f}")
print()
print(f"figure: {figpath}")

# dump a small json of the key numbers for the writeup / reproducibility
import json
summary = {
    "N": N,
    "lorentzian": {
        "gamma": GAMMA, "g0": g0_lor,
        "Kc_theory": KC_TH_LOR, "Kc_empirical": kc_emp_lor,
        "rel_error_pct": agree(kc_emp_lor, KC_TH_LOR),
        "r_at_K0": float(rs[0]), "r_at_Kmax": float(rs[-1]),
    },
    "gaussian": {
        "sigma": SIGMA, "g0": g0_gauss,
        "Kc_theory": KC_TH_GAUSS, "Kc_empirical": kc_emp_gauss,
        "rel_error_pct": agree(kc_emp_gauss, KC_TH_GAUSS),
    },
    "metric_distinction": {
        "neff_pearson_K0": float(neff_pearson[0]),
        "neff_pearson_Kmax": float(neff_pearson[-1]),
        "neff_varratio_K0": float(neff_varratio[0]),
        "neff_varratio_Kmax": float(neff_varratio[-1]),
        "r_K0": float(rs[0]), "r_Kmax": float(rs[-1]),
    },
    "Ks": Ks.tolist(), "rs": rs.tolist(),
    "neff_pearson": [float(v) for v in neff_pearson],
    "neff_varratio": [float(v) for v in neff_varratio],
    "r2_curve": [float(v) for v in r2_curve],
}
with open(OUT + "/kuramoto_kc.json", "w") as fh:
    json.dump(summary, fh, indent=2)
print(f"json  : {OUT}/kuramoto_kc.json")
