"""Concentration and recovery on the paper's own transport equation.

The paper's fast layer (Eq. master) is dp/dt = L(b)^T p with a belief drift
b = beta * grad(M p) that pulls attention toward already-popular, adjacent
nodes, plus diffusion D that relaxes toward uniform. Written out, that is an
aggregation-diffusion equation on a graph: the same family as Keller-Segel
chemotaxis, whose density concentrates in finite time above a critical
drift-to-diffusion ratio while the total mass stays exactly conserved.

This script reads three things the paper's E2 check did not:

  1. total mass          -- the paper's conservation check (flat, always)
  2. p_max and the graph Dirichlet energy sum_edges (p_i - p_j)^2
                          -- the concentration observables (the enstrophy
                             analogue: what moves when the total does not)
  3. recovery time       -- two-trajectory protocol: perturb one run, keep the
                             unperturbed run as the MOVING reference, report
                             the first step the separation falls back under a
                             declared tolerance in a declared norm, or
                             CENSORED if the window closes first.

Run:  uv run --with numpy python concentration_blowup.py
Writes RESULTS.md and results.json beside itself. No plotting dependency.
"""
from __future__ import annotations

import json
import os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(0)

n = 40
A = (rng.random((n, n)) < 0.15).astype(float)
A = np.triu(A, 1); A = A + A.T
edges = np.argwhere(np.triu(A, 1) > 0)
deg = A.sum(1)


def generator(p, beta, D):
    """Row-sum-zero rate matrix with non-negative off-diagonals.

    Diffusion: rate D along every edge. Belief drift: preferential attachment,
    edge i->j gets an extra rate beta * max(p_j - p_i, 0) * A_ij, so attention
    flows uphill in popularity. Transpose convention as in the paper: p
    evolves by L^T p, and L 1 = 0 keeps 1^T p fixed to machine precision.
    """
    diff = np.maximum(p[None, :] - p[:, None], 0.0) * A
    L = D * A + beta * diff
    np.fill_diagonal(L, 0.0)
    np.fill_diagonal(L, -L.sum(axis=1))
    return L


def step(p, beta, D, dt):
    L = generator(p, beta, D)
    q = p + dt * (L.T @ p)
    return q


def dirichlet(p):
    return float(((p[edges[:, 0]] - p[edges[:, 1]]) ** 2).sum())


def run(beta, D, T=3000, dt=0.02, p0=None, kick=None):
    p = (np.ones(n) / n) if p0 is None else p0.copy()
    if kick is not None:
        p = p + kick
    traj = [p.copy()]
    for _ in range(T):
        p = step(p, beta, D, dt)
        traj.append(p.copy())
    return np.array(traj)


def summarise(tr):
    mass = tr.sum(1)
    return {
        "mass_err_max": float(np.abs(mass - 1.0).max()),
        "p_max_start": float(tr[0].max()), "p_max_end": float(tr[-1].max()),
        "dirichlet_start": dirichlet(tr[0]), "dirichlet_end": dirichlet(tr[-1]),
        "min_p_end": float(tr[-1].min()),
    }


# ---- 1+2. sweep the drift-to-diffusion ratio at fixed total mass ---------
D = 0.05
# Bound to names so the header below cannot drift from what the sweep ran; it
# said 3000 steps, which was run()'s default rather than this call's T.
T_STEPS = 6000
DT = 0.02
seed_kick = rng.normal(0, 1e-3, n); seed_kick -= seed_kick.mean()
sweep = []
for beta in [0.0, 1.0, 2.0, 2.5, 3.0, 3.5, 4.0, 8.0, 16.0, 32.0]:
    tr = run(beta, D, T=T_STEPS, dt=DT, kick=seed_kick)
    s = summarise(tr)
    # time for p_max to double from its start, if it ever does
    pm = tr.max(1)
    dbl = np.argmax(pm >= 2 * pm[0]) if (pm >= 2 * pm[0]).any() else None
    s.update({"beta": beta, "beta_over_D": beta / D,
              "t_pmax_doubles": None if dbl is None else int(dbl)})
    sweep.append(s)

# ---- 2b. the focusing precursor: a finite-time fit of p_max --------------
def tstar_fit(tr, lo=0.05, hi=0.5):
    """Fit p_max(t) ~ C (T* - t)^-alpha on the window where p_max is between
    lo and hi (past the linear regime, before the finite graph saturates).
    Scan T* over the steps after the window, pick the best log-log fit, and
    compare with the step at which p_max actually reaches hi."""
    pm = tr.max(1)
    idx = np.where((pm > lo) & (pm < hi))[0]
    if len(idx) < 20:
        return None
    t = idx.astype(float); y = np.log(pm[idx])
    t_hit = int(np.argmax(pm >= hi)) if (pm >= hi).any() else None
    best = None
    for T in np.arange(idx[-1] + 1, idx[-1] + 6000, 5.0):
        x = np.log(T - t)
        a, b = np.polyfit(x, y, 1)
        r = float(((y - (a * x + b)) ** 2).mean())
        if best is None or r < best[0]:
            best = (r, float(T), float(-a))
    return {"fit_window": [int(idx[0]), int(idx[-1])], "T_star_fit": best[1],
            "alpha": best[2], "resid": best[0], "t_reach_hi": t_hit, "hi": hi}

focus = run(32.0, D, T=6000, kick=seed_kick)
tfit = tstar_fit(focus)
tfit_mid = tstar_fit(run(8.0, D, T=6000, kick=seed_kick))

# ---- 3. recovery against a moving reference -------------------------------
def recovery(beta, D, t_kick=200, window=1500, eps=1e-3, tol_frac=0.1,
             norm="l2"):
    """Kick the state at t_kick, evolve both runs, report first return."""
    base = run(beta, D, T=t_kick + window, kick=seed_kick)
    kick = rng.normal(0, eps, n); kick -= kick.mean()
    pert = run(beta, D, T=window, p0=base[t_kick], kick=kick)
    ref = base[t_kick:t_kick + window + 1]
    if norm == "l2":
        sep = np.linalg.norm(pert - ref, axis=1)
    else:  # gradient norm: L2 of the edge differences
        g = lambda X: (X[:, edges[:, 0]] - X[:, edges[:, 1]])
        sep = np.linalg.norm(g(pert) - g(ref), axis=1)
    tol = tol_frac * sep[0]
    back = np.argmax(sep <= tol) if (sep <= tol).any() else None
    return {"beta": beta, "beta_over_D": beta / D, "norm": norm,
            "sep_0": float(sep[0]), "sep_end": float(sep[-1]),
            "recovery_step": None if back is None else int(back),
            "censored": back is None, "window": window}

rec = []
for beta in [0.0, 1.0, 4.0, 8.0]:
    for norm in ("l2", "grad"):
        rec.append(recovery(beta, D, norm=norm))

# the shrinking window: kick the focusing run later and later, with the
# observation window ending where p_max reaches 0.5
t_end = tfit["t_reach_hi"] if tfit and tfit["t_reach_hi"] else 6000
late = []
for t_kick in [200, 600, 1000, 1400]:
    w = max(t_end - t_kick, 50)
    r = recovery(32.0, D, t_kick=t_kick, window=w, norm="grad")
    r["t_kick"] = t_kick
    late.append(r)

out = {"n": n, "D": D, "sweep": sweep, "tstar_beta32": tfit, "tstar_beta8": tfit_mid, "recovery": rec,
       "recovery_shrinking_window": late}
json.dump(out, open(os.path.join(HERE, "results.json"), "w"), indent=1)

lines = ["# Concentration and recovery on the transport equation", "",
         f"n={n} topic nodes, random graph (p=0.15), D={D}, dt={DT}, "
         f"{T_STEPS} steps.",
         "Total mass is the paper's conservation check. p_max and the Dirichlet",
         "energy are the concentration observables. All three from one run.", "",
         "| beta/D | mass err | p_max start -> end | Dirichlet start -> end | min p end | p_max doubles at |",
         "|---|---|---|---|---|---|"]
for s in sweep:
    lines.append(f"| {s['beta_over_D']:.0f} | {s['mass_err_max']:.1e} | "
                 f"{s['p_max_start']:.4f} -> {s['p_max_end']:.4f} | "
                 f"{s['dirichlet_start']:.2e} -> {s['dirichlet_end']:.2e} | "
                 f"{s['min_p_end']:.2e} | {s['t_pmax_doubles']} |")
lines += ["", "## Recovery against a moving reference", "",
          "Kick of 1e-3 per node at step 200; separation from the UNPERTURBED",
          "run of the same system; recovered when separation falls under 10% of",
          "its initial value; window 1500 steps. CENSORED means not observed to",
          "return inside the window, which is not the same as not returning.", "",
          "| beta/D | norm | sep at kick | sep at window end | recovery step |",
          "|---|---|---|---|---|"]
for r in rec:
    rs = "CENSORED" if r["censored"] else str(r["recovery_step"])
    lines.append(f"| {r['beta_over_D']:.0f} | {r['norm']} | {r['sep_0']:.2e} | "
                 f"{r['sep_end']:.2e} | {rs} |")
lines += ["", "## Finite-time fit of the peak on the focusing runs", ""]
if tfit_mid:
    lines += [f"beta/D = 160: fit on steps {tfit_mid['fit_window']} gives T* = {tfit_mid['T_star_fit']:.0f}, "
              f"alpha = {tfit_mid['alpha']:.2f}, log-resid {tfit_mid['resid']:.2e}; p_max reaches 0.5 at step {tfit_mid['t_reach_hi']}."]
if tfit:
    lines[-1:] = lines[-1:]  # keep
    lines += ["beta/D = 640: " + f"fit on steps {tfit['fit_window']} gives"]
if tfit:
    lines += [f"  p_max ~ C (T*-t)^-alpha on 0.05 < p_max < {tfit['hi']}: T* = {tfit['T_star_fit']:.0f}, "
              f"alpha = {tfit['alpha']:.2f}, log-resid {tfit['resid']:.2e}; "
              f"p_max actually reaches {tfit['hi']} at step {tfit['t_reach_hi']}."]
else:
    lines += ["p_max never left the fit window; no T* fit."]
lines += ["", "## The window shrinks toward the focusing time", "",
          (f"beta/D = 640 run, kick at later steps; window ends at step {t_end}, where p_max reaches 0.5." if tfit and tfit["t_reach_hi"] else f"beta/D = 640 run, kick at later steps; p_max did not reach 0.5 inside the run, so every window ends at the run's end, step {t_end}. On this finite graph the peak grows and then slows toward a concentrated stationary state; the finite-time form is a continuum statement, and the fit above is the instrument to point at a real series, not a reading confirmed here."), "",
          "| kick step | window | sep at kick | sep at end | recovery step |", "|---|---|---|---|---|"]
for r in late:
    rs = "CENSORED" if r["censored"] else str(r["recovery_step"])
    lines.append(f"| {r['t_kick']} | {r['window']} | {r['sep_0']:.2e} | {r['sep_end']:.2e} | {rs} |")
open(os.path.join(HERE, "RESULTS.md"), "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
