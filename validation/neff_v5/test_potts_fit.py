"""Tests for potts_fit.py on synthetic systems with known couplings.

Run on CPU: python -m pytest validation/neff_v5 -q
"""
import datetime as dt
import itertools
import os
import subprocess
import sys

import numpy as np
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import potts_fit as PF  # noqa: E402
import run_v5  # noqa: E402

J_TRUE = np.array([
    [0.0, 0.8, 0.5, 0.0],
    [0.8, 0.0, 0.0, 0.0],
    [0.5, 0.0, 0.0, -0.8],
    [0.0, 0.0, -0.8, 0.0],
])
H_TRUE = np.array([0.1, -0.2, 0.0, 0.2])


def sample_ising(J, h, T, seed):
    """Exact draws by enumerating all 2^K states; returns 0/1 states."""
    states = np.array(list(itertools.product([-1.0, 1.0], repeat=len(h))))
    logp = states @ h + 0.5 * np.einsum("si,ij,sj->s", states, J, states)
    p = np.exp(logp - logp.max())
    p /= p.sum()
    idx = np.random.default_rng(seed).choice(len(states), size=T, p=p)
    return ((states[idx] + 1) // 2).astype(np.int64)


@pytest.fixture(scope="module")
def planted():
    return sample_ising(J_TRUE, H_TRUE, 2000, seed=1)


def test_planted_four_block_sign_and_support(planted):
    fit = PF.fit_couplings(planted)
    assert fit["converged"]
    J = fit["J"]
    iu = np.triu_indices(4, k=1)
    strong = np.abs(J_TRUE[iu]) >= 0.5
    assert np.all(np.sign(J[iu][strong]) == np.sign(J_TRUE[iu][strong]))
    assert np.all(np.abs(J[iu][strong]) > 0.3)
    assert np.all(np.abs(J[iu][~strong]) < 0.1)
    assert np.allclose(J, J.T)
    assert np.all(np.diag(J) == 0)
    assert fit["nlpl"] < fit["nlpl_fields_only"]


def test_planted_readout_top_pairs_and_ratio(planted):
    r = PF.readout(planted, labels=["a", "b", "c", "d"], k=10, seed=0)
    top = {frozenset((p["a"], p["b"])) for p in r["top_couplings"][:3]}
    assert top == {frozenset("ab"), frozenset("cd"), frozenset("ac")}
    assert r["obs_over_null_mass"] > 5
    assert r["null_pctile_of_obs"] == 1.0


def test_potts_q3_support():
    K, q = 4, 3
    A = np.eye(q) - 1.0 / q
    J4 = np.zeros((K, K, q, q))
    J4[0, 1] = J4[1, 0] = 1.2 * A
    J4[2, 3] = J4[3, 2] = 1.0 * A
    states = np.array(list(itertools.product(range(q), repeat=K)))
    logp = np.array([sum(J4[i, j][s[i], s[j]] for i in range(K) for j in range(i + 1, K))
                     for s in states])
    p = np.exp(logp - logp.max())
    p /= p.sum()
    S = states[np.random.default_rng(3).choice(len(states), size=2000, p=p)]
    st = PF.fit_couplings(S)["strength"]
    assert st[0, 1] > 0.8 and st[2, 3] > 0.8
    assert max(st[0, 2], st[0, 3], st[1, 2], st[1, 3]) < 0.2


def test_shuffled_data_sits_at_the_null(planted):
    rng = np.random.default_rng(5)
    ratios, pct = [], []
    for s in range(12):
        S = PF.shuffle_columns(planted, rng)
        r = PF.readout(S, k=12, seed=s)
        ratios.append(r["obs_over_null_mass"])
        pct.append(r["null_pctile_of_obs"])
    assert 0.6 < float(np.mean(ratios)) < 1.4
    assert 0.2 < float(np.mean(pct)) < 0.8


def test_shuffle_keeps_marginals(planted):
    S = PF.shuffle_columns(planted, np.random.default_rng(0))
    assert np.array_equal(np.sort(S, axis=0), np.sort(planted, axis=0))


def test_same_seed_same_output(planted):
    a = PF.readout(planted, k=5, seed=11)
    b = PF.readout(planted, k=5, seed=11)
    assert a == b
    na = PF.fitted_null(planted, k=5, seed=11)["masses"]
    nb = PF.fitted_null(planted, k=5, seed=11)["masses"]
    nc = PF.fitted_null(planted, k=5, seed=12)["masses"]
    assert np.array_equal(na, nb)
    assert not np.array_equal(na, nc)


@pytest.mark.parametrize("bad, err", [
    (np.zeros(10, dtype=int), ValueError),
    (np.zeros((10, 3, 2), dtype=int), ValueError),
    (np.zeros((10, 1), dtype=int), ValueError),
    (np.zeros((3, 4), dtype=int), ValueError),
    (np.full((10, 3), 0.5), TypeError),
    (-np.ones((10, 3), dtype=int), ValueError),
])
def test_wrong_input_is_refused(bad, err):
    with pytest.raises(err):
        PF.fit_couplings(bad)


def test_out_of_range_state_and_label_mismatch_refused(planted):
    with pytest.raises(ValueError):
        PF.fit_couplings(planted + 1, q=2)
    with pytest.raises(ValueError):
        PF.readout(planted, labels=["a", "b"], k=2)
    with pytest.raises(ValueError):
        PF.discretize(np.ones((5, 3)), method="zscore")
    with pytest.raises(ValueError):
        PF.discretize(np.array([[1.0, np.nan], [2.0, 3.0]]))


def test_discretize_diff_and_quantiles():
    M = np.array([[1, 5], [3, 5], [2, 9], [4, 1]], dtype=float)
    assert PF.discretize(M).tolist() == [[1, 0], [0, 1], [1, 0]]
    S3 = PF.discretize(np.arange(30, dtype=float).reshape(15, 2), q=3, method="level")
    assert set(S3.ravel().tolist()) == {0, 1, 2}


def test_daily_block_matrix_counts_by_block():
    lo = dt.date(2021, 1, 1)
    part = {"u1": 7, "u2": 7, "u3": 2}
    ev = [("u1", lo), ("u2", lo), ("u3", lo + dt.timedelta(days=2)),
          ("ghost", lo), ("u1", lo + dt.timedelta(days=9))]
    M, blocks = run_v5.daily_block_matrix(ev, part, lo, lo + dt.timedelta(days=3))
    assert blocks == [2, 7]
    assert M.tolist() == [[0, 2], [0, 0], [1, 0]]


def test_runner_records_missing_harvests_as_no_data(tmp_path, monkeypatch):
    monkeypatch.setattr(run_v5, "WSB_DATA", str(tmp_path / "none"))
    monkeypatch.setattr(run_v5, "WIKI_DATA", str(tmp_path / "none"))
    assert {r["status"] for r in run_v5.run_wsb_v4(2, 0)} == {"NO_DATA"}
    assert run_v5.run_wiki(2, 0)[0]["status"] == "NO_DATA"


def test_summary_reports_event_and_calm_arms_apart():
    runs = [
        dict(substrate="wiki", arm="event", status="OK", obs_over_null_mass=3.0,
             sparsity=0.0, null_pctile_of_obs=1.0, coupling_mass=0.3, null_mass_mean=0.1,
             null_mass_p90=0.2, nnz_pairs=3),
        dict(substrate="wiki", arm="event", status="OK", obs_over_null_mass=2.0,
             sparsity=0.5, null_pctile_of_obs=0.9, coupling_mass=0.6, null_mass_mean=0.3,
             null_mass_p90=0.7, nnz_pairs=1),
        dict(substrate="wiki", arm="calm", status="OK", obs_over_null_mass=0.0,
             sparsity=1.0, null_pctile_of_obs=0.0, coupling_mass=0.0, null_mass_mean=0.1,
             null_mass_p90=0.2, nnz_pairs=0),
        dict(substrate="wiki", arm="calm", status="TRIVIAL_PARTITION"),
        dict(substrate="ecosystem", status="OK", obs_over_null_mass=2.8,
             sparsity=0.48, null_pctile_of_obs=1.0, coupling_mass=2.21, null_mass_mean=0.78,
             null_mass_p90=1.15, nnz_pairs=10),
    ]
    s = run_v5.summarize(runs)
    assert s["wiki"]["n_runs"] == 4 and s["wiki"]["n_ok"] == 3
    assert s["wiki"]["by_arm"]["event"]["median_obs_over_null_mass"] == 2.5
    assert s["wiki"]["by_arm"]["calm"]["median_obs_over_null_mass"] == 0.0
    assert s["wiki"]["by_arm"]["calm"]["n_ok_all_zero_fit"] == 1
    assert s["wiki"]["by_arm"]["event"]["pooled_obs_over_null_mass"] == pytest.approx(0.9 / 0.4)
    assert s["wiki"]["by_arm"]["event"]["frac_ok_above_null_p90"] == 0.5
    assert s["wiki"]["by_arm"]["calm"]["n_runs"] == 2
    assert "by_arm" not in s["ecosystem"]


def test_block_top_articles_skip_focal_and_rank_by_members():
    contribs = {"u1": [{"title": "Focal"}, {"title": "A"}, {"title": "A"}, {"title": "B"}],
                "u2": [{"title": "A"}, {"title": "C"}],
                "u3": [{"title": "D"}]}
    part = {"u1": 0, "u2": 0, "u3": 1}
    out = run_v5.block_top_articles(contribs, part, "Focal", n=2)
    assert out == {"b0": ["A", "B"], "b1": ["D"]}


LOUVAIN_PROBE = """
import json, random, sys
import networkx as nx
sys.path.insert(0, sys.argv[1])
import common as C
rng = random.Random(7)
names = [f"editor_{i:03d}" for i in range(60)]
G = nx.Graph()
for i in range(60):
    for j in range(i + 1, 60):
        if rng.random() < (0.10 if i // 15 == j // 15 else 0.06):
            G.add_edge(names[i], names[j], weight=rng.randint(1, 4))
G.add_nodes_from(f"lurker_{i:03d}" for i in range(100))
part, mod, K = C.louvain_giant_component(G)
print(json.dumps([sorted(part.items()), round(mod, 12), K]))
"""


def test_louvain_partition_does_not_depend_on_hash_seed():
    pytest.importorskip("networkx")
    pytest.importorskip("community")
    common_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline_v03")
    outs = set()
    for h in ("0", "1", "2", "3", "4", "5"):
        env = dict(os.environ, PYTHONHASHSEED=h)
        r = subprocess.run([sys.executable, "-c", LOUVAIN_PROBE, common_dir], env=env,
                           capture_output=True, text=True, check=True)
        outs.add(r.stdout)
    assert len(outs) == 1


def test_wiki_coedit_graph_drops_the_focal_article_under_its_current_title():
    pytest.importorskip("networkx")
    pytest.importorskip("matplotlib")
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "wikipedia"))
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "pipeline_v03"))
    import neff_collapse_wiki as NW
    rec = dict(title="Queen Elizabeth II", resolved_title="Elizabeth II",
               editor_contribs={"u1": [{"title": "Elizabeth II"}, {"title": "Liz Truss"}],
                                "u2": [{"title": "Elizabeth II"}],
                                "u3": [{"title": "Liz Truss"}]})
    assert NW.focal_titles(rec) == {"Queen Elizabeth II", "Elizabeth II"}
    G = NW.coedit_graph(rec["editor_contribs"], NW.focal_titles(rec))
    assert sorted(G.edges()) == [("u1", "u3")]
