"""Acceptance tests for the steering-envelope module.

The preset-distribution tests pin the Python port to the JS v0.2 reference
outcome distributions (e/acc ~60% crash+pileup; saxxer plurality
convoy/arrived) within Monte Carlo error. The mean-field test checks the
coordination-dominates-private-virtue theorem on its stated domain. The fit
tests check the statistical machinery on synthetic data with known truth.
"""

import numpy as np
import pytest

from steering_envelope.model import (
    GOOD, Outcome, PRESETS, RaceConfig, hazard, monte_carlo, speed, steer,
)
from steering_envelope.meanfield import theorem_check
from steering_envelope.society import proof_table
from steering_envelope.validate import fit


# ----------------------------------------------------------------------------
# hazard law primitives
# ----------------------------------------------------------------------------

def test_hazard_monotone_and_centered():
    assert hazard(10, 10, 1.0) == pytest.approx(0.5)  # ratio 1 = the edge
    assert hazard(12, 10, 1.0) > hazard(8, 10, 1.0)   # faster is riskier
    assert hazard(10, 14, 1.0) < hazard(10, 8, 1.0)   # more grip is safer
    assert hazard(10, 10, 1.3) > hazard(10, 10, 0.7)  # tighter is riskier


def test_speed_and_steer_laws():
    cfg = RaceConfig()
    assert speed(1.0, 0, cfg.v0, cfg.g, cfg.v_cap) == pytest.approx(cfg.v0)
    assert speed(1.0, 200, cfg.v0, cfg.g, cfg.v_cap) == cfg.v_cap  # saturates
    assert steer(0.5, 10, 20.0) > steer(0.5, 10, 0.0)  # learning-by-doing
    assert steer(0.9, 10, 0.0) > steer(0.1, 10, 0.0)   # investment


# ----------------------------------------------------------------------------
# v0.2 reference outcome distributions (within MC error)
# ----------------------------------------------------------------------------

def test_eacc_crash_pileup_share():
    d = monte_carlo(PRESETS["eacc"], n=2000, seed=123)
    assert 0.54 <= d["P_bad"] <= 0.68, d
    assert d["CRASHED"] > 0.05 and d["PILEUP"] > 0.05


def test_saxxer_plurality_convoy_arrived():
    d = monte_carlo(PRESETS["saxxer"], n=2000, seed=123)
    top = max((o.value for o in Outcome), key=lambda k: d[k])
    assert top in ("CONVOY", "ARRIVED"), d
    assert d["P_good"] > 0.7, d


def test_stopper_hands_over_the_wheel():
    d = monte_carlo(PRESETS["stopper"], n=2000, seed=123)
    assert d["SHOTGUN"] + d["HELD"] > 0.6, d


def test_policy_ordering():
    seeds = dict(n=2000, seed=123)
    bad = {k: monte_carlo(PRESETS[k], **seeds)["P_bad"]
           for k in ("eacc", "dacc", "saxxer")}
    assert bad["saxxer"] < bad["dacc"] < bad["eacc"], bad


# ----------------------------------------------------------------------------
# mean field: coordination dominates private virtue (after diligence)
# ----------------------------------------------------------------------------

@pytest.mark.slow
def test_meanfield_theorem_check():
    tc = theorem_check(n_rep=600, seed=11)
    assert tc["n_holds"] >= 8, tc  # at most one noise-flip on the 3x3 grid
    assert tc["mean_margin"] > 0, tc


# ----------------------------------------------------------------------------
# kitchen proof view: s/acc wins only via the K dial
# ----------------------------------------------------------------------------

@pytest.mark.slow
def test_proof_table_honesty():
    natural = proof_table(n=800, seed=4)
    zero_k = proof_table(
        n=800, seed=4,
        coordination={k: 0.0 for k in
                      ("eacc", "dacc", "saxxer", "wacc", "stopper")})
    wins_nat = natural["win_counts"].get("saxxer", 0)
    wins_zero = zero_k["win_counts"].get("saxxer", 0)
    assert wins_nat >= 2, natural["win_counts"]
    assert wins_zero <= 1, zero_k["win_counts"]
    # nobody else clearly beats saxxer anywhere under natural K
    others = {k: v for k, v in natural["win_counts"].items()
              if k not in ("saxxer", "tie")}
    assert all(v == 0 for v in others.values()), natural["win_counts"]


# ----------------------------------------------------------------------------
# fit machinery on synthetic truth
# ----------------------------------------------------------------------------

def _synthetic_panel(beta_v, beta_s, n=3000, seed=0):
    rng = np.random.default_rng(seed)
    zv = rng.normal(size=n)
    zs = rng.normal(size=n)
    logit = -2.0 + beta_v * zv + beta_s * zs
    y = rng.random(n) < 1 / (1 + np.exp(-logit))
    return np.exp(zv), np.exp(zs), y.astype(float)


def test_fit_detects_steering_term_when_present():
    v, s, y = _synthetic_panel(beta_v=0.8, beta_s=-0.8)
    r = fit.domain_comparison(v, s, y, name="synth")
    assert r["lr_p_s_given_v"] < 0.01
    assert r["beta"]["full_v"] > 0.5 and r["beta"]["full_s"] < -0.5
    assert r["auc"]["full"] > r["auc"]["v"]


def test_fit_rejects_steering_term_when_absent():
    v, s, y = _synthetic_panel(beta_v=0.8, beta_s=0.0)
    r = fit.domain_comparison(v, s, y, name="synth-null")
    assert r["lr_p_s_given_v"] > 0.1  # decoration is detected as decoration


def test_ratio_constraint_accepted_when_true():
    # p is uniform under a true constraint, so aggregate over seeds instead
    # of trusting one draw
    ps = []
    for seed in range(3):
        v, s, y = _synthetic_panel(beta_v=0.7, beta_s=-0.7, seed=seed)
        r = fit.domain_comparison(v, s, y, name="synth-ratio")
        ps.append(r["lr_p_ratio_ok"])
    assert np.median(ps) > 0.05, ps  # constraint costs nothing when true


def test_auc_sane():
    y = np.array([0, 0, 1, 1], dtype=bool)
    assert fit.auc(np.array([0.1, 0.2, 0.8, 0.9]), y) == 1.0
    assert fit.auc(np.array([0.9, 0.8, 0.2, 0.1]), y) == 0.0


# ----------------------------------------------------------------------------
# cached-data smoke tests (skip when the cache has not been fetched)
# ----------------------------------------------------------------------------

def _has_cache(fname):
    from steering_envelope.validate.datasets import DATA
    return (DATA / fname).exists()


@pytest.mark.skipif(not _has_cache("JSTdatasetR6.dta"),
                    reason="JST cache not fetched")
def test_finance_panel_builds():
    from steering_envelope.validate.finance import build_panel
    df = build_panel()
    assert df["event"].sum() > 50
    assert df["country"].nunique() == 18


@pytest.mark.skipif(not _has_cache("us_roads_wiki.json"),
                    reason="roads cache not fetched")
def test_roads_panel_builds():
    from steering_envelope.validate.roads import build_panel
    df, _ = build_panel()
    assert len(df) > 90
    assert df["rate"].iloc[0] > 5 * df["rate"].iloc[-1]  # the 20x decline
