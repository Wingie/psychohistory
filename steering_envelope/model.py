"""The steering-envelope race model (Python port of the JS v0.2 artifact).

Two actors ("you" and "the field") drive a course of capability corners.
Each tick an actor moves at a speed set by its throttle and compounding
capability growth, and accumulates steering capacity from deliberate
investment and learning-by-doing. Crossing a corner draws a Bernoulli
control-loss event whose probability is logistic in the ratio of speed to
steering capacity, scaled by the corner's tightness:

    h = sigma( beta * ( (v * k) / (s * c0) - 1 ) )

Inside the envelope (v*k < s*c0) hazard is small; outside it saturates
toward 1. That single law is the object the validation suite tests on
historical data.

Outcomes (from "your" perspective):

    ARRIVED  you finish the course intact, clearly first
    CONVOY   you and the field finish intact, close together
    SHOTGUN  the field finishes while you are far behind: the transition
             happens, but someone else is driving
    CRASHED  you lose control at a corner, alone
    PILEUP   a crash while the actors are tightly coupled takes both out
    HELD     the horizon ends with nobody through and nobody crashed

The good set is {ARRIVED, CONVOY}; PILEUP is the systemic worst case.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Callable, Optional, Sequence

import numpy as np


# ----------------------------------------------------------------------------
# primitives
# ----------------------------------------------------------------------------

def sigma(x: float) -> float:
    """Numerically safe logistic."""
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    z = math.exp(x)
    return z / (1.0 + z)


def speed(throttle: float, t: int, v0: float = 1.0, g: float = 1.128,
          v_cap: float = 14.2) -> float:
    """Deployment velocity: throttle times compounding capability growth,
    saturating at the physical cap.  speed(T, t) = min(v_cap, v0 * T * g^t)."""
    return min(v_cap, v0 * throttle * (g ** t))


def steer(invest: float, t: int, dist: float, s0: float = 1.34,
          a: float = 1.43, b: float = 0.125) -> float:
    """Steering capacity: baseline + deliberate investment accruing with time
    + learning-by-doing from distance already driven.
    steer(I, t, d) = s0 + a*I*t + b*d."""
    return s0 + a * invest * t + b * dist


def hazard(v: float, s: float, k: float, beta: float = 5.36,
           c0: float = 1.0) -> float:
    """Control-loss probability at a corner of tightness k, at speed v with
    steering capacity s.  h = sigma(beta * ((v*k)/(s*c0) - 1))."""
    return sigma(beta * ((v * k) / (s * c0) - 1.0))


# ----------------------------------------------------------------------------
# course
# ----------------------------------------------------------------------------

@dataclass(frozen=True)
class Corner:
    x: float        # position along the course (capability threshold)
    k: float        # tightness (how unforgiving the transition is)
    name: str = ""


@dataclass(frozen=True)
class Course:
    length: float
    corners: tuple[Corner, ...]

    @staticmethod
    def default() -> "Course":
        """The v0.2 course: five corners of rising tightness ending in a
        hairpin just before the finish (the 'alignment corner')."""
        return Course(
            length=100.0,
            corners=(
                Corner(15.0, 0.35, "capability jump"),
                Corner(32.0, 0.50, "mass deployment"),
                Corner(50.0, 0.65, "economic rewiring"),
                Corner(70.0, 0.85, "strategic instability"),
                Corner(88.0, 1.10, "the hairpin"),
            ),
        )


# ----------------------------------------------------------------------------
# actor policies
# ----------------------------------------------------------------------------

@dataclass
class Policy:
    """A throttle/investment rule. `throttle` may be a constant in [0,1] or a
    callable (t, s_now, next_k, cfg) -> value; `invest` is a constant in
    [0,1]. `defense` shaves corner tightness (d/acc's armor channel);
    `wisdom` multiplies the investment learning rate a (w/acc's channel)."""
    throttle: float | Callable = 1.0
    invest: float = 0.0
    defense: float = 0.0
    wisdom: float = 1.0
    name: str = "actor"

    def throttle_at(self, t: int, s_now: float, next_k: float,
                    cfg: "RaceConfig") -> float:
        if callable(self.throttle):
            return float(np.clip(self.throttle(t, s_now, next_k, cfg), 0.0, 1.0))
        return float(np.clip(self.throttle, 0.0, 1.0))


def ramp_throttle(start: float = 0.25, rate: float = 0.045,
                  cap: float = 0.9) -> Callable:
    """The w/acc rule: hold back early and ramp the throttle only as time
    (judgment accumulation) makes higher speed responsible."""
    def rule(t: int, s_now: float, next_k: float, cfg: "RaceConfig") -> float:
        return min(cap, start + rate * t)
    return rule


def envelope_throttle(margin: float = 0.8) -> Callable:
    """The s/acc rule: the largest throttle whose resulting speed keeps the
    next corner inside the envelope with a safety margin —
    v <= margin * s * c0 / k. Constrain v to f(s); never faster than grip."""
    def rule(t: int, s_now: float, next_k: float, cfg: "RaceConfig") -> float:
        v_allowed = margin * s_now * cfg.c0 / max(next_k, 1e-9)
        v_full = cfg.v0 * (cfg.g ** t)
        if v_full <= 1e-12:
            return 1.0
        return min(1.0, v_allowed / v_full)
    return rule


# ----------------------------------------------------------------------------
# race configuration
# ----------------------------------------------------------------------------

class Outcome(str, Enum):
    ARRIVED = "ARRIVED"
    CONVOY = "CONVOY"
    SHOTGUN = "SHOTGUN"
    CRASHED = "CRASHED"
    PILEUP = "PILEUP"
    HELD = "HELD"


GOOD = frozenset({Outcome.ARRIVED, Outcome.CONVOY})
BAD = frozenset({Outcome.CRASHED, Outcome.PILEUP})


@dataclass
class RaceConfig:
    course: Course = field(default_factory=Course.default)
    horizon: int = 60           # ticks before HELD
    v0: float = 1.0
    g: float = 1.128            # capability compounding per tick
    v_cap: float = 14.2
    s0: float = 1.34
    a: float = 1.43             # investment -> steering rate
    b: float = 0.125            # learning-by-doing rate
    beta: float = 5.36          # hazard steepness
    c0: float = 1.0             # envelope normalization
    d_couple: float = 12.6      # coupling distance for pileups
    drag: float = 0.23          # P(coupled crash cascades into a pileup)
    convoy_window: int = 4      # ticks within which a joint finish is a convoy


@dataclass
class ActorState:
    x: float = 0.0
    crashed: bool = False
    finished_at: Optional[int] = None
    v: float = 0.0
    s: float = 0.0


@dataclass
class RaceResult:
    outcome: Outcome
    t_end: int
    you: ActorState
    field_: ActorState
    log: list = field(default_factory=list)


def _step(actor: ActorState, pol: Policy, t: int, cfg: RaceConfig,
          rng: np.random.Generator) -> None:
    """Advance one actor one tick; may set crashed/finished."""
    if actor.crashed or actor.finished_at is not None:
        return
    s_now = steer(pol.invest, t, actor.x, cfg.s0, cfg.a * pol.wisdom, cfg.b)
    upcoming = [c for c in cfg.course.corners if c.x > actor.x]
    next_k = upcoming[0].k if upcoming else 0.0
    thr = pol.throttle_at(t, s_now, max(next_k - pol.defense, 0.05), cfg)
    v = speed(thr, t, cfg.v0, cfg.g, cfg.v_cap)
    x_new = actor.x + v
    actor.v, actor.s = v, s_now
    # corners crossed during this tick
    for c in cfg.course.corners:
        if actor.x < c.x <= x_new:
            k_eff = max(c.k - pol.defense, 0.05)
            h = hazard(v, s_now, k_eff, cfg.beta, cfg.c0)
            if rng.random() < h:
                actor.crashed = True
                actor.x = c.x
                return
    actor.x = x_new
    if actor.x >= cfg.course.length:
        actor.finished_at = t


def run_race(you: Policy, field_pol: Policy, cfg: Optional[RaceConfig] = None,
             rng: Optional[np.random.Generator] = None) -> RaceResult:
    """Run one race and classify the outcome from `you`'s perspective."""
    cfg = cfg or RaceConfig()
    rng = rng or np.random.default_rng()
    you_s, fld_s = ActorState(), ActorState()

    for t in range(cfg.horizon):
        coupled = abs(you_s.x - fld_s.x) <= cfg.d_couple
        _step(you_s, you, t, cfg, rng)
        _step(fld_s, field_pol, t, cfg, rng)

        if you_s.crashed and fld_s.crashed:
            return RaceResult(Outcome.PILEUP, t, you_s, fld_s)
        if you_s.crashed:
            # a crash inside coupling distance drags the field down too
            if coupled and rng.random() < _drag_prob(cfg):
                fld_s.crashed = True
                return RaceResult(Outcome.PILEUP, t, you_s, fld_s)
            return RaceResult(Outcome.CRASHED, t, you_s, fld_s)
        if fld_s.crashed:
            if coupled and rng.random() < _drag_prob(cfg):
                you_s.crashed = True
                return RaceResult(Outcome.PILEUP, t, you_s, fld_s)
            fld_s.crashed = True  # field is out; race continues solo
        # finishes
        if you_s.finished_at is not None and fld_s.finished_at is not None:
            return RaceResult(Outcome.CONVOY, t, you_s, fld_s)
        if you_s.finished_at is not None:
            # wait up to convoy_window for the field
            if _projected_finish_within(fld_s, field_pol, t, cfg,
                                        cfg.convoy_window, rng):
                return RaceResult(Outcome.CONVOY, t, you_s, fld_s)
            return RaceResult(Outcome.ARRIVED, t, you_s, fld_s)
        if fld_s.finished_at is not None:
            if _projected_finish_within(you_s, you, t, cfg,
                                        cfg.convoy_window, rng):
                return RaceResult(Outcome.CONVOY, t, you_s, fld_s)
            return RaceResult(Outcome.SHOTGUN, t, you_s, fld_s)

    return RaceResult(Outcome.HELD, cfg.horizon, you_s, fld_s)


def _drag_prob(cfg: RaceConfig) -> float:
    """Probability a coupled crash cascades into a pileup."""
    return cfg.drag


def blend_policies(you: Policy, field_pol: Policy, kappa: float) -> Policy:
    """Coordination dial K: the field adopts your norms with weight kappa.
    Your wisdom multiplies the effectiveness of coordination (w/acc's claim:
    judgment makes agreements actually bind), saturating at full adoption.
    Throttle rules blend at call time so an adaptive (envelope) rule carries
    over to the field."""
    k_eff = float(np.clip(kappa * min(you.wisdom, 2.0), 0.0, 1.0))
    yt, ft = you.throttle, field_pol.throttle

    def mixed_throttle(t, s_now, next_k, cfg):
        fv = ft(t, s_now, next_k, cfg) if callable(ft) else ft
        yv = yt(t, s_now, next_k, cfg) if callable(yt) else yt
        return (1.0 - k_eff) * fv + k_eff * yv

    return Policy(
        throttle=mixed_throttle,
        invest=(1 - k_eff) * field_pol.invest + k_eff * you.invest,
        defense=(1 - k_eff) * field_pol.defense + k_eff * you.defense,
        wisdom=(1 - k_eff) * field_pol.wisdom + k_eff * you.wisdom,
        name=f"field(K={kappa:.2f})",
    )


def _projected_finish_within(actor: ActorState, pol: Policy, t: int,
                             cfg: RaceConfig, window: int,
                             rng: np.random.Generator) -> bool:
    """Simulate the trailing actor forward `window` ticks (with live corner
    draws) to see whether it also finishes — a near-joint finish is a convoy,
    not a solo arrival."""
    if actor.crashed:
        return False
    ghost = replace(actor)  # shallow copy of the dataclass
    for dt in range(1, window + 1):
        _step(ghost, pol, t + dt, cfg, rng)
        if ghost.crashed:
            return False
        if ghost.finished_at is not None:
            return True
    return False


# ----------------------------------------------------------------------------
# Monte Carlo
# ----------------------------------------------------------------------------

def monte_carlo(you: Policy, field_pol: Optional[Policy] = None,
                cfg: Optional[RaceConfig] = None, n: int = 4000,
                seed: int = 0, coordination: float = 0.0) -> dict:
    """Run n races; return outcome distribution plus summary probabilities.
    `coordination` (K) is the share of your norms the ambient field adopts."""
    cfg = cfg or RaceConfig()
    field_pol = field_pol or PRESETS["field"]
    if coordination > 0:
        field_pol = blend_policies(you, field_pol, coordination)
    rng = np.random.default_rng(seed)
    counts = {o: 0 for o in Outcome}
    fc_counts = {o: 0 for o in Outcome}
    t_ends = []
    for _ in range(n):
        r = run_race(you, field_pol, cfg, rng)
        counts[r.outcome] += 1
        if r.field_.crashed:
            fc_counts[r.outcome] += 1
        t_ends.append(r.t_end)
    dist = {o.value: c / n for o, c in counts.items()}
    dist["P_good"] = sum(counts[o] for o in GOOD) / n
    dist["P_bad"] = sum(counts[o] for o in BAD) / n
    dist["mean_t_end"] = float(np.mean(t_ends))
    # fraction of races, per outcome, where the field crashed anyway — a solo
    # field wreck disappears from your outcome label but not from the world
    dist["field_crash_frac"] = {
        o.value: (fc_counts[o] / counts[o] if counts[o] else 0.0)
        for o in Outcome
    }
    dist["n"] = n
    return dist


# ----------------------------------------------------------------------------
# presets (the four flags + the ambient field)
# ----------------------------------------------------------------------------

PRESETS: dict[str, Policy] = {
    # engine: floor it, safety is friction
    "eacc": Policy(throttle=1.0, invest=0.06, name="e/acc"),
    # armor: keep speed high but spend on making corners shallower
    "dacc": Policy(throttle=0.9, invest=0.25, defense=0.11, name="d/acc"),
    # steering: throttle bounded by grip, heavy investment in grip
    "saxxer": Policy(throttle=envelope_throttle(margin=0.70), invest=0.85,
                     name="s/acc"),
    # driver: judgment first — slow ramp, modest floors, wisdom makes every
    # unit of investment and coordination count for more
    "wacc": Policy(throttle=ramp_throttle(0.25, 0.045, 0.9), invest=0.3,
                   wisdom=1.6, name="w/acc"),
    # stopper: near-zero throttle
    "stopper": Policy(throttle=0.08, invest=0.5, name="stopper"),
    # the ambient field you race against
    "field": Policy(throttle=0.88, invest=0.41, name="field"),
}
