"""Tests for the Platt calibration of the detectors. numpy + scipy only."""
import os
import sys

import numpy as np
import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from validation.calibration import platt as P  # noqa: E402


def test_a_planted_slope_is_recovered():
    rng = np.random.default_rng(0)
    s = rng.normal(size=400)
    p = 1 / (1 + np.exp(-(0.5 + 2.0 * s)))
    y = (rng.uniform(size=400) < p).astype(float)
    rec = P.fit_platt(s, y)
    a, b = rec["params"]
    assert rec["converged"]
    assert abs(a - 0.5) < 0.3 and abs(b - 2.0) < 0.4


def test_smoothed_targets_keep_a_separable_sample_finite():
    s = np.array([-3.0, -2.0, -1.0, 1.0, 2.0, 3.0])
    y = np.array([0, 0, 0, 1, 1, 1], dtype=float)
    t = P.platt_targets(y)
    assert np.allclose(t[y == 1], 4 / 5) and np.allclose(t[y == 0], 1 / 5)
    rec = P.fit_platt(s, y)
    assert np.all(np.isfinite(rec["params"])) and abs(rec["params"][1]) < 20


def test_loo_never_scores_a_row_it_fitted_on():
    # An outlier row that the in-sample fit bends toward and the LOO fit cannot see.
    s = np.array([-2.0, -1.5, -1.0, -0.5, 0.5, 1.0, 1.5, 2.0, 6.0])
    y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 0], dtype=float)
    X = np.column_stack([np.ones_like(s), s])
    p_in = P.predict_platt(P.fit_platt(s, y)["params"], s)
    p_loo = P.loo(X, y)
    assert p_loo[-1] > p_in[-1]          # the fit that never saw the outlier is surer it is positive
    with pytest.raises(P.CalibrationError):
        P.loo(X[:2], y[:2])


def test_murphy_identity_holds_on_the_binned_brier():
    rng = np.random.default_rng(1)
    p = rng.uniform(size=200)
    y = (rng.uniform(size=200) < p).astype(float)
    m = P.murphy(p, y, bins=5)
    assert abs(m["brier_binned"] - (m["reliability"] - m["resolution"] + m["uncertainty"])) < 1e-9
    assert m["uncertainty"] == pytest.approx(m["base_rate"] * (1 - m["base_rate"]))
    assert 0 <= m["brier"] <= 1


def test_the_twenty_four_rows_parse_with_the_features_named():
    rows = P.bnr_rows()
    assert len(rows) == 24
    assert {r["substrate"] for r in rows} == {"wiki", "wsb"}
    assert all(r["substantive"] in ("B", "R") for r in rows)
    X = P.bnr_design(rows)
    assert X.shape == (24, 3) and np.all(X[:, 0] == 1.0)
    assert np.allclose(X[:, 2], np.log([r["a_abrupt"] for r in rows]))


def test_the_detector_fit_reports_its_n_and_the_unscorable_keys():
    d = P.detector_scores()
    assert set(d["scores"]) <= set(P.ROSTER)
    assert set(d["scores"]) | set(d["unscorable"]) == set(P.ROSTER)
    if d["unscorable"]:
        assert d["reason"]
    fit = P.detector_fit()
    assert fit["n"] == len(d["scores"])
    assert fit["unscorable"] == d["unscorable"]


def test_a_single_label_roster_is_not_fitted():
    out = P._score_fit("one label", {"a": 1.0, "b": 2.0, "c": 3.0}, {"a": 1, "b": 1, "c": 1}, 5)
    assert out["fit"] is None and "both labels" in out["reason"]


def test_the_battery_reads_all_ten_and_the_bnr_fit_reads_the_thresholds():
    b = P.battery_scores("z")
    assert set(b["scores"]) == set(P.ROSTER)
    r = P.bnr_fit()
    assert r["n"] == 24 and len(r["p_loo"]) == 24
    assert r["features"] == ["1", "f_existing", "log(a_abrupt)"]
    assert r["hard_threshold"]["brier"] == pytest.approx(1 - r["hard_threshold"]["accuracy"])
