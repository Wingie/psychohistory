"""The Sustenance Ledger: v0.3 society layer in Steering Envelope units.

The race model says ARRIVED or PILEUP; this layer says what that does to
dinner. The anchor metric is hours-per-week-of-essentials per tribe: how many
hours of your labour buy the food, shelter and energy your household needs.
GDP can live in a drawer; hours-for-dinner is the headline.

Structure
---------
* An essentials basket: food / shelter / energy. Food and energy deflate as
  capability deploys, gated by access (concentration hoards the deflation).
  Shelter is land: it refuses to deflate, and rises with concentration.
* Eight labour channels with different automation exposure and
  tech-complementarity; steering investment I buys floors (wage floors,
  retraining, competition policy) that bound displacement.
* Eight tribes = weighted bundles of channels + market exposure + communal
  buffer + a country price factor. Tribes encode country, economic level,
  consumerism vs makerism, and communal sub-sects.
* Emergent-exchange regime switch: past ~60 h/week the market has failed that
  tribe and sustenance migrates to non-market channels (verified-human work,
  care, craft, local food, compute shares, mutual aid). The communal buffer
  sets how soft that landing is.

Coupling to the race
--------------------
`world_from_outcome` turns a race outcome (+ dials) into a world trajectory:
capability deployed, concentration, floors coverage, shock sequence. The
field's norms — not just yours — set the world the tribes live in, which is
why the coordination dial K is the only way a virtuous policy reaches the
kitchen: floors_world = (1-K)*field + K*yours.

All numeric baselines are toy calibrations chosen for ordinal realism
(a Gulf rentier buys essentials in fewer hours than a Lagos street vendor),
not measured quantities; see validate/ for where the model meets real data.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from .model import Outcome

DECADES = 6  # simulation horizon: six "decades" (race ticks aggregated)

REGIME_SWITCH_HOURS = 60.0  # past this, dinner migrates off-market


# ----------------------------------------------------------------------------
# labour channels: (automation exposure, tech complementarity)
# exposure: how much of the channel capability can displace
# complement: how much capability multiplies the channel's earning power
# ----------------------------------------------------------------------------

LABOUR_CHANNELS: dict[str, tuple[float, float]] = {
    "manual_routine":       (0.85, 0.10),   # warehouse, assembly
    "manual_dexterous":     (0.45, 0.25),   # trades, repair
    "clerical_routine":     (0.90, 0.15),   # back office, dispatch
    "analytic_professional": (0.60, 0.55),  # law, medicine, engineering
    "interpersonal_care":   (0.20, 0.30),   # care, teaching, presence
    "creative_symbolic":    (0.70, 0.40),   # media, design, code-as-craft
    "land_based":           (0.30, 0.35),   # farming, fishing
    "rentier_capital":      (0.05, 0.90),   # ownership income
}


@dataclass(frozen=True)
class Tribe:
    name: str
    channels: dict            # weights over LABOUR_CHANNELS, sum to 1
    market_exposure: float    # share of sustenance bought at market prices
    communal_buffer: float    # softness of the >60h landing (mutual aid)
    price_factor: float       # local basket cost level
    h0: float                 # baseline hours/week of essentials


TRIBES: tuple[Tribe, ...] = (
    Tribe("salaried professional (Amsterdam)",
          {"analytic_professional": 0.8, "clerical_routine": 0.2},
          market_exposure=0.95, communal_buffer=0.15, price_factor=1.35, h0=16),
    Tribe("gig / warehouse worker (US metro)",
          {"manual_routine": 0.6, "clerical_routine": 0.2,
           "interpersonal_care": 0.2},
          market_exposure=1.00, communal_buffer=0.10, price_factor=1.25, h0=30),
    Tribe("street vendor (Lagos)",
          {"manual_dexterous": 0.4, "land_based": 0.2,
           "interpersonal_care": 0.2, "manual_routine": 0.2},
          market_exposure=0.85, communal_buffer=0.35, price_factor=0.80, h0=48),
    Tribe("smallholder farmer (rural India)",
          {"land_based": 0.75, "manual_dexterous": 0.25},
          market_exposure=0.55, communal_buffer=0.45, price_factor=0.65, h0=52),
    Tribe("Gulf rentier citizen",
          {"rentier_capital": 0.6, "clerical_routine": 0.3,
           "analytic_professional": 0.1},
          market_exposure=0.70, communal_buffer=0.25, price_factor=1.10, h0=9),
    Tribe("maker / artisan (EU)",
          {"manual_dexterous": 0.5, "creative_symbolic": 0.35,
           "land_based": 0.15},
          market_exposure=0.75, communal_buffer=0.30, price_factor=1.20, h0=22),
    Tribe("online creator (global, verified-human)",
          {"creative_symbolic": 0.85, "interpersonal_care": 0.15},
          market_exposure=0.95, communal_buffer=0.20, price_factor=1.00, h0=26),
    Tribe("congregation / commune (any country)",
          {"interpersonal_care": 0.4, "land_based": 0.3,
           "manual_dexterous": 0.3},
          market_exposure=0.40, communal_buffer=0.70, price_factor=0.85, h0=34),
)

# essentials basket shares (food, shelter, energy)
BASKET = {"food": 0.38, "shelter": 0.44, "energy": 0.18}


# ----------------------------------------------------------------------------
# world trajectory: race outcome + dials -> the world tribes live in
# ----------------------------------------------------------------------------

@dataclass
class World:
    cap: np.ndarray           # deployed capability in [0,1] per decade
    shock: np.ndarray         # recession shock in [0,1] per decade
    concentration: np.ndarray  # gains concentration in [0,1] per decade
    floors: float             # field-wide floors coverage in [0,1]
    outcome: Outcome


def _ramp(target_decade: float, level: float = 1.0) -> np.ndarray:
    """Smooth deployment ramp reaching `level` at `target_decade`."""
    d = np.arange(DECADES, dtype=float)
    return level * np.clip(d / max(target_decade, 0.5), 0.0, 1.0) ** 1.5


def world_from_outcome(outcome: Outcome, dials: dict,
                       finish_decade: float = 3.0,
                       field_crashed: bool = False) -> World:
    """Map a race outcome + policy dials to a world trajectory.

    dials: T, I, D, W, K in [0,1] (your policy); field_I = ambient field's
    steering investment. Floors that reach the kitchen are the field's
    norms, so your I arrives only through K (wisdom W makes both your
    floors and the coordination channel more effective).
    """
    I = dials.get("I", 0.3)
    W = dials.get("W", 0.0)
    K = dials.get("K", 0.0)
    field_I = dials.get("field_I", 0.41)
    w_mult = 1.0 + 0.6 * W
    # wisdom multiplies the effectiveness of YOUR floors and of coordination;
    # it cannot upgrade the ambient field's norms without the K channel
    k_eff = min(1.0, K * w_mult)
    floors = min(1.0, (1 - k_eff) * field_I + k_eff * min(1.0, I * w_mult))

    shock = np.zeros(DECADES)
    conc_gain = 1.0

    if outcome in (Outcome.ARRIVED, Outcome.CONVOY):
        cap = _ramp(finish_decade)
        if outcome == Outcome.ARRIVED:
            conc_gain = 1.25   # a solo winner concentrates more than a convoy
        else:
            conc_gain = 0.85
    elif outcome == Outcome.SHOTGUN:
        cap = _ramp(finish_decade)
        conc_gain = 1.6        # someone else's transition: you hold no shares
        floors = min(1.0, field_I * 0.8)  # their floors, not yours; K is moot
    elif outcome == Outcome.CRASHED:
        crash_d = max(1, int(round(finish_decade)))
        cap = _ramp(finish_decade + 2, level=0.7)
        cap[crash_d:] = np.minimum(cap[crash_d:], 0.55)
        shock[crash_d:min(DECADES, crash_d + 2)] = 0.30
        conc_gain = 1.0
    elif outcome == Outcome.PILEUP:
        crash_d = max(1, int(round(finish_decade)))
        cap = _ramp(finish_decade + 3, level=0.5)
        cap[crash_d:] = np.minimum(cap[crash_d:], 0.35)
        shock[crash_d:min(DECADES, crash_d + 3)] = 0.55
        conc_gain = 0.9
    else:  # HELD
        cap = _ramp(DECADES * 2.0, level=0.35)
        conc_gain = 0.7

    if field_crashed and outcome in (Outcome.ARRIVED, Outcome.HELD):
        # the field wrecked even though your label stayed clean; the world
        # still eats a recession
        fd = max(1, int(round(finish_decade)))
        shock[fd:min(DECADES, fd + 2)] = np.maximum(
            shock[fd:min(DECADES, fd + 2)], 0.25)

    concentration = np.clip(
        0.25 + conc_gain * 0.6 * cap * (1.0 - 0.8 * floors), 0.0, 0.95)
    return World(cap=cap, shock=shock, concentration=concentration,
                 floors=floors, outcome=outcome)


# ----------------------------------------------------------------------------
# kitchen: hours-per-week-of-essentials per tribe
# ----------------------------------------------------------------------------

def _basket_cost(world: World) -> np.ndarray:
    """Basket cost index per decade, relative to 1.0 at baseline. Food and
    energy deflate with deployed capability, gated by access (concentration
    hoards the deflation). Shelter is land: floor at baseline, rising with
    concentration."""
    access = 1.0 - 0.55 * world.concentration
    food = 1.0 - 0.55 * world.cap * access
    energy = 1.0 - 0.65 * world.cap * access
    shelter = 1.0 + 0.75 * world.concentration - 0.10 * world.floors
    shelter = np.maximum(shelter, 1.0)  # refuses to deflate
    return (BASKET["food"] * food + BASKET["energy"] * energy
            + BASKET["shelter"] * shelter)


def _channel_wage(name: str, world: World) -> np.ndarray:
    """Wage index per decade for one labour channel, relative to baseline.
    Complementarity lifts it with capability; exposure displaces it, bounded
    below by floors; recessions shock it."""
    expo, compl = LABOUR_CHANNELS[name]
    lift = 1.0 + 0.9 * compl * world.cap
    displaced = 0.9 * expo * world.cap * (1.0 - 0.75 * world.floors)
    wage = lift - displaced
    floor_level = 0.45 + 0.40 * world.floors
    wage = np.maximum(wage, floor_level)
    return wage * (1.0 - world.shock)


def tribe_hours(tribe: Tribe, world: World) -> dict:
    """Hours/week of essentials per decade for one tribe, plus regime-switch
    bookkeeping. Market hours move with basket cost over tribe wage; the
    non-market share of sustenance is insulated. Past REGIME_SWITCH_HOURS the
    excess is softened by the communal buffer (mutual aid absorbs what the
    market abandoned) — the tribe has partially exited the wage economy."""
    wage = sum(w * _channel_wage(c, world) for c, w in tribe.channels.items())
    # transfers funded out of the transition's gains, reaching tribes via floors
    wage = wage + 0.25 * world.floors * world.cap
    cost = _basket_cost(world)
    m = tribe.market_exposure
    raw = tribe.h0 * (m * cost / np.maximum(wage, 0.15) + (1.0 - m))
    switched = raw > REGIME_SWITCH_HOURS
    softened = np.where(
        switched,
        REGIME_SWITCH_HOURS + (raw - REGIME_SWITCH_HOURS)
        * (1.0 - tribe.communal_buffer),
        raw,
    )
    return {
        "tribe": tribe.name,
        "hours": softened,
        "raw_hours": raw,
        "regime_switch": bool(switched.any()),
        "worst": float(softened.max()),
        "best": float(softened.min()),
    }


def kitchen_table(outcome_dist: dict, dials: dict,
                  finish_decade: float = 3.0) -> list[dict]:
    """Probability-weighted kitchen outcomes: for each tribe, expected
    hours-per-week trajectory under a race outcome distribution (as returned
    by model.monte_carlo), plus worst/best decade of the expected path."""
    fc_frac = outcome_dist.get("field_crash_frac", {})
    worlds = []
    for o in Outcome:
        p = outcome_dist.get(o.value, 0.0)
        if p <= 0:
            continue
        f = fc_frac.get(o.value, 0.0)
        if f > 0 and o in (Outcome.ARRIVED, Outcome.HELD):
            worlds.append((p * (1 - f),
                           world_from_outcome(o, dials, finish_decade)))
            worlds.append((p * f,
                           world_from_outcome(o, dials, finish_decade,
                                              field_crashed=True)))
        else:
            worlds.append((p, world_from_outcome(o, dials, finish_decade)))
    rows = []
    for tribe in TRIBES:
        hours = np.zeros(DECADES)
        p_switch = 0.0
        for p, w in worlds:
            r = tribe_hours(tribe, w)
            hours += p * r["hours"]
            p_switch += p * (1.0 if r["regime_switch"] else 0.0)
        rows.append({
            "tribe": tribe.name,
            "hours": hours,
            "worst": float(hours.max()),
            "best": float(hours.min()),
            "p_regime_switch": float(p_switch),
        })
    return rows


def blend_dist(yours: dict, field: dict, w: float) -> dict:
    """Influence-weighted mixture of two monte_carlo outcome distributions:
    the world outcome is yours with weight w, the ambient field's with
    weight 1-w."""
    out = {}
    for o in Outcome:
        out[o.value] = w * yours.get(o.value, 0.0) \
            + (1 - w) * field.get(o.value, 0.0)
    out["mean_t_end"] = w * yours["mean_t_end"] \
        + (1 - w) * field["mean_t_end"]
    fy, ff = yours.get("field_crash_frac", {}), field.get("field_crash_frac", {})
    out["field_crash_frac"] = {
        o.value: w * fy.get(o.value, 0.0) + (1 - w) * ff.get(o.value, 0.0)
        for o in Outcome
    }
    return out


def proof_table(policies: Optional[dict] = None, n: int = 2000,
                seed: int = 0, coordination: Optional[dict] = None) -> dict:
    """The PROOF view: for each tribe, which worldview minimizes worst-decade
    hours and which maximizes the best decade. `coordination` maps preset
    name -> K; the honesty check is run by calling this twice, once with each
    worldview's natural K and once with K forced to 0 — s/acc should win most
    rows only in the first case."""
    from .model import PRESETS, monte_carlo

    policies = policies or {k: PRESETS[k]
                            for k in ("eacc", "dacc", "saxxer", "wacc",
                                      "stopper")}
    coordination = coordination or {"eacc": 0.0, "dacc": 0.2, "saxxer": 0.7,
                                    "wacc": 0.5, "stopper": 0.0}
    dial_map = {
        "eacc": dict(I=0.06, W=0.0),
        "dacc": dict(I=0.25, W=0.0),
        "saxxer": dict(I=0.85, W=0.2),
        # w/acc's bet is judgment, not floors: low I, max W
        "wacc": dict(I=0.30, W=1.0),
        "stopper": dict(I=0.50, W=0.0),
    }
    # the world the tribes live in is mostly the field's doing: your race
    # distribution enters only in proportion to your influence share, and
    # coordination K is precisely the dial that raises that share. This is
    # the mean-field coupling (meanfield.py) surfaced at kitchen level: at
    # K=0 a virtuous policy improves its own lane, not the world.
    OWN_SHARE = 0.15
    from .model import PRESETS as _P
    field_dist = monte_carlo(_P["field"], n=n, seed=seed)

    per_policy = {}
    for name, pol in policies.items():
        K = coordination.get(name, 0.0)
        dist = monte_carlo(pol, n=n, seed=seed, coordination=K)
        dials = dict(dial_map.get(name, {"I": pol.invest, "W": 0.0}))
        dials["K"] = K
        k_eff = min(1.0, K * (1.0 + 0.6 * dials.get("W", 0.0)))
        w_you = OWN_SHARE + (1.0 - OWN_SHARE) * k_eff
        world_dist = blend_dist(dist, field_dist, w_you)
        # each worldview arrives on its own clock (w/acc alone is slow)
        finish_decade = float(
            np.clip(world_dist["mean_t_end"] / 10.0, 1.5, 5.0))
        per_policy[name] = kitchen_table(world_dist, dials, finish_decade)
    rows = []
    tie_margin = 0.5  # hours/week; anything closer is an honest tie
    for ti, tribe in enumerate(TRIBES):
        worst = {name: per_policy[name][ti]["worst"] for name in per_policy}
        best = {name: per_policy[name][ti]["best"] for name in per_policy}
        ranked = sorted(worst, key=worst.get)
        clear = worst[ranked[1]] - worst[ranked[0]] > tie_margin
        rows.append({
            "tribe": tribe.name,
            "min_worst_decade": ranked[0] if clear else "tie",
            "max_best_decade": min(best, key=best.get),  # fewest hours = best
            "worst": worst,
            "best": best,
        })
    wins = [r["min_worst_decade"] for r in rows]
    counts = {k: wins.count(k) for k in per_policy}
    counts["tie"] = wins.count("tie")
    return {
        "rows": rows,
        "win_counts": counts,
        "per_policy": per_policy,
    }
