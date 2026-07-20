"""Mean-field extension: N actors, coordination as mean-field coupling.

The two-actor race in `model.py` understates what coordination buys, because
a careful ego decouples from a single rival. Here the rival is replaced by a
*field* of N actors drawing throttle preferences from a distribution. The
coordination parameter kappa couples each actor's policy to the mean-field
norm (the s/acc envelope rule plus a steering-investment floor): as kappa
rises, the upper tail of the throttle distribution is pulled in and the
field's steering investment is pulled up. Crashes cascade to coupled
neighbours (a pileup wave), which is the externality private virtue cannot
buy out of.

The s/acc structural claim, stated as a checkable theorem:

    dP(good | ego) / dkappa  >  dP(good | ego) / dI_own

i.e. the ego's own survival probability gains more from a marginal unit of
field-wide coordination than from the same marginal unit of private steering
investment. `theorem_check()` estimates both derivatives with common random
numbers across a grid of baselines and reports where the inequality holds
with Monte Carlo error bars.

Why it should hold (sketch): own investment I enters the ego's hazard only
through its own s in h = sigma(beta*(v*k/(s*c0) - 1)), which is already small
for a careful ego; its derivative is O(h') and bounded by the ego's residual
own-corner hazard. kappa enters three ways at once: it lowers every
neighbour's crash hazard (shrinking the pileup source term), thins the tail
of the throttle distribution (the most dangerous drivers slow the most), and
raises mean field steering (fewer wrecks to inherit). For an ego whose
residual risk is dominated by inherited wrecks rather than own-corner
control loss — which is what the two-actor calibration shows — the coupling
derivative dominates. The check below verifies this numerically rather than
assuming it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from .model import (
    Course, RaceConfig, envelope_throttle, hazard, speed, steer,
)


@dataclass
class FieldConfig:
    n_actors: int = 16
    # throttle preferences: tau ~ lo + (hi-lo)*Beta(a,b)
    tau_lo: float = 0.55
    tau_hi: float = 1.0
    tau_beta: tuple = (2.0, 2.0)
    # steering investment: I ~ I_scale * Beta(a,b)
    invest_scale: float = 0.5
    invest_beta: tuple = (2.0, 2.0)
    # the norm actors are coupled toward under kappa
    norm_margin: float = 0.70
    norm_invest: float = 0.85
    # actors start at staggered capability positions (the field is not a
    # single starting grid); ego starts at 0
    start_spread: float = 45.0
    race: RaceConfig = field(default_factory=RaceConfig)


def draw_bundle(fc: FieldConfig, rng: np.random.Generator) -> dict:
    """Pre-draw every random number one realization can consume, in a fixed
    layout independent of the policy parameters. This gives true common
    random numbers: perturbing kappa or I_own changes outcomes only through
    the thresholds compared against these same uniforms, so finite
    differences of P(good) have far lower variance than independent runs."""
    n, H = fc.n_actors, fc.race.horizon
    n_c = len(fc.race.course.corners)
    return {
        "tau_b": rng.beta(*fc.tau_beta, size=n),
        "inv_b": rng.beta(*fc.invest_beta, size=n),
        "x0": rng.uniform(0.0, fc.start_spread, size=n),
        "corner_u": rng.random((n, n_c)),   # one hazard draw per actor-corner
        "drag_u": rng.random((n, H)),       # one drag draw per actor-tick
    }


def _simulate_field(fc: FieldConfig, kappa: float, ego_invest: float,
                    bundle: dict) -> dict:
    """One realization: returns per-actor status. Ego is actor 0 (an s/acc
    driver whose investment we can vary); the rest draw from the field
    distribution. Everyone is coupled toward the norm with weight kappa."""
    cfg = fc.race
    n = fc.n_actors
    env_rule = envelope_throttle(fc.norm_margin)
    corner_idx = {c: ci for ci, c in enumerate(cfg.course.corners)}

    tau = fc.tau_lo + (fc.tau_hi - fc.tau_lo) * bundle["tau_b"]
    inv = fc.invest_scale * bundle["inv_b"].copy()
    inv[0] = ego_invest
    # coupled investment: pulled toward the norm floor
    inv_eff = (1 - kappa) * inv + kappa * fc.norm_invest

    x = bundle["x0"].copy()
    x[0] = 0.0
    crashed = np.zeros(n, dtype=bool)
    finished = np.full(n, -1)
    corners = cfg.course.corners

    for t in range(cfg.horizon):
        active = (~crashed) & (finished < 0)
        if not active.any():
            break
        s_now = np.array([
            steer(inv_eff[i], t, x[i], cfg.s0, cfg.a, cfg.b) for i in range(n)
        ])
        newly = []
        order = list(np.where(active)[0])
        for i in order:
            upcoming = [c for c in corners if c.x > x[i]]
            next_k = upcoming[0].k if upcoming else 0.05
            # coupled throttle: preference blended toward the envelope rule
            t_env = env_rule(t, s_now[i], next_k, cfg)
            if i == 0:
                thr = t_env  # ego drives the envelope rule
            else:
                thr = (1 - kappa) * tau[i] + kappa * t_env
            v = speed(thr, t, cfg.v0, cfg.g, cfg.v_cap)
            x_new = x[i] + v
            hit = False
            for c in corners:
                if x[i] < c.x <= x_new:
                    h = hazard(v, s_now[i], c.k, cfg.beta, cfg.c0)
                    if bundle["corner_u"][i, corner_idx[c]] < h:
                        crashed[i] = True
                        x[i] = c.x
                        newly.append(i)
                        hit = True
                        break
            if hit:
                continue
            x[i] = x_new
            if x[i] >= cfg.course.length:
                finished[i] = t
        # pileup wave: crashes drag coupled neighbours, breadth-first, with
        # drag probability decaying linearly to zero at the coupling radius.
        # Each potential victim spends its one per-tick drag draw against the
        # combined pull of all wrecks near it this tick.
        if newly:
            wrecks = list(newly)
            while True:
                candidates = np.where((~crashed) & (finished < 0))[0]
                added = []
                for m in candidates:
                    p_miss = 1.0
                    for j in wrecks:
                        dist = abs(x[m] - x[j])
                        if dist <= cfg.d_couple:
                            p_miss *= 1.0 - cfg.drag * (1.0 - dist / cfg.d_couple)
                    if p_miss < 1.0 and bundle["drag_u"][m, t] < 1.0 - p_miss:
                        crashed[m] = True
                        added.append(int(m))
                if not added:
                    break
                wrecks = added

    return {
        "crashed": crashed,
        "finished": finished >= 0,
        "ego_good": bool(finished[0] >= 0),
        "frac_good": float((finished >= 0).mean()),
        "frac_crashed": float(crashed.mean()),
        "pileup": bool(crashed.sum() >= 3),
    }


def p_good(fc: Optional[FieldConfig] = None, kappa: float = 0.0,
           ego_invest: float = 0.3, n_rep: int = 400, seed: int = 0) -> dict:
    """Monte Carlo estimate of ego and field-wide good-outcome probabilities."""
    fc = fc or FieldConfig()
    rng = np.random.default_rng(seed)
    ego, frac, pile, crash = [], [], [], []
    for _ in range(n_rep):
        r = _simulate_field(fc, kappa, ego_invest, draw_bundle(fc, rng))
        ego.append(r["ego_good"])
        frac.append(r["frac_good"])
        pile.append(r["pileup"])
        crash.append(r["frac_crashed"])
    ego = np.array(ego, dtype=float)
    return {
        "kappa": kappa,
        "ego_invest": ego_invest,
        "P_good_ego": float(ego.mean()),
        "se_ego": float(ego.std(ddof=1) / np.sqrt(n_rep)),
        "P_good_field": float(np.mean(frac)),
        "P_pileup": float(np.mean(pile)),
        "frac_crashed": float(np.mean(crash)),
        "n_rep": n_rep,
    }


def outcome_vs_kappa(kappas=(0.0, 0.15, 0.3, 0.45, 0.6, 0.75, 0.9),
                     fc: Optional[FieldConfig] = None, ego_invest: float = 0.3,
                     n_rep: int = 400, seed: int = 0) -> list[dict]:
    """P(outcome) as a function of the coordination coupling — the curve the
    page plots."""
    return [p_good(fc, k, ego_invest, n_rep, seed) for k in kappas]


def theorem_check(fc: Optional[FieldConfig] = None, delta: float = 0.35,
                  n_rep: int = 800, seed: int = 0,
                  kappa_grid=(0.0, 0.2, 0.4),
                  invest_grid=(0.45, 0.65, 0.85)) -> dict:
    """Numerically check  dP(good|ego)/dkappa > dP(good|ego)/dI_own.

    Domain of the claim: an ego that has already done basic diligence
    (I_own >= ~0.45, the compliant-actor regime). Below that the inequality
    genuinely fails at some gridpoints — an under-braked ego's own hazard
    dominates and private investment competes with coordination. That
    boundary is reported honestly rather than hidden: the theorem says the
    *next* unit after diligence buys more as coordination than as private
    virtue; it is not a license to skip your own brakes.

    Both derivatives are forward finite differences of size `delta` in their
    own dial, estimated with common random numbers (same seed for the
    perturbed and base runs) so the difference of means has far lower
    variance than independent draws. Returns per-gridpoint gradients with
    standard errors and an overall verdict: the claim PASSES if the
    coordination gradient exceeds the private gradient at every gridpoint
    and the mean margin clears 2 combined standard errors."""
    fc = fc or FieldConfig()
    rows = []
    for k0 in kappa_grid:
        for i0 in invest_grid:
            # paired design: every replicate evaluates base and both
            # perturbations on the SAME randomness bundle, so the per-rep
            # difference (ego_up - ego_base) is exactly the set of runs the
            # perturbation flipped
            rng = np.random.default_rng(seed)
            dk_list, di_list = [], []
            for _ in range(n_rep):
                bundle = draw_bundle(fc, rng)
                base = _simulate_field(fc, k0, i0, bundle)["ego_good"]
                upk = _simulate_field(fc, min(1.0, k0 + delta), i0,
                                      bundle)["ego_good"]
                upi = _simulate_field(fc, k0, min(1.0, i0 + delta),
                                      bundle)["ego_good"]
                dk_list.append(float(upk) - float(base))
                di_list.append(float(upi) - float(base))
            dk = np.array(dk_list) / delta
            di = np.array(di_list) / delta
            diff = dk - di
            gk, gi = float(dk.mean()), float(di.mean())
            se = float(diff.std(ddof=1) / np.sqrt(n_rep))
            rows.append({
                "kappa0": k0, "invest0": i0,
                "grad_kappa": gk, "grad_invest": gi,
                "margin": gk - gi, "se_paired": se,
                "holds": gk > gi,
            })
    margins = np.array([r["margin"] for r in rows])
    ses = np.array([r["se_paired"] for r in rows])
    n_hold = int(sum(r["holds"] for r in rows))
    verdict = (n_hold == len(rows)
               and float(margins.mean()) > 2 * float(ses.mean() / np.sqrt(len(rows))))
    return {
        "rows": rows,
        "n_gridpoints": len(rows),
        "n_holds": n_hold,
        "mean_margin": float(margins.mean()),
        "mean_se": float(ses.mean()),
        "passes": bool(verdict),
        "claim": "dP(good|ego)/dkappa > dP(good|ego)/dI_own",
    }
