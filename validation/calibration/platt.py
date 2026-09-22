"""Platt scaling of the psychohistory detectors as calibrated questions.

`logos/DECISION_TOWER.md` §4: at n between 10 and 24 the calibrator is the cheap
one, a logistic fit of the detector's own score, read as a reliability table and
Murphy's decomposition against the base rate. Three fits:

  detector  `major_player_signal/results.json` `operator_led_score` -> endogenous.
            Three of the ten roster events are scored there; the other seven need
            weekly caches under `major_player_signal/data/` and
            `gamestop_counterfactual/data/`, which are not in the tree, so the fit
            reports its n and the unscorable keys by name.
  battery   `early_warning_battery/results/<key>.json` `z` -> endogenous, all ten.
  bnr       `bifurcation_mix/classification_table.md`, 24 rows: a two-feature
            logit on (f_existing, log a_abrupt) for the SUBSTANTIVE B-vs-R reading,
            beside the hard STRUCTURAL thresholds from `classify.py`.

Every probability is leave-one-out: a row is scored by a fit that never saw it.
Targets are Platt's smoothed ones, so a separable roster fits finite slopes.

Run:  python -m validation.calibration.platt      (from the repo root)
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
VAL = os.path.dirname(HERE)
ROOT = os.path.dirname(VAL)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
BIF = os.path.join(VAL, "bifurcation_mix")
if BIF not in sys.path:
    sys.path.insert(0, BIF)

from steering_envelope.validate.fit import fit_logit, predict_logit  # noqa: E402

DETECTOR_RESULTS = os.path.join(VAL, "backtests", "major_player_signal", "results.json")
DETECTOR_DATA = os.path.join(VAL, "backtests", "major_player_signal", "data")
GME_DATA = os.path.join(VAL, "backtests", "gamestop_counterfactual", "data")
BATTERY_RESULTS = os.path.join(VAL, "backtests", "early_warning_battery", "results")
BNR_TABLE = os.path.join(BIF, "classification_table.md")

# The ten-row roster, `early_warning_battery/roster.md`: 1 endogenous, 0 exogenous.
ROSTER = {
    "gme_wsb_weekly": 1, "superstonk_2021": 1, "crypto_2021peak": 1, "crypto_luna2022": 1,
    "europe_energy2022": 1, "wsb_meme_2021": 1,
    "askecon_infl2022": 0, "askecon_tariff25": 0, "europe_covid2020": 0, "crypto_ftx2022": 0,
}
# `major_player_signal/results.json` event id -> roster key.
DETECTOR_KEYS = {
    "gamestop": "gme_wsb_weekly",
    "askecon_tariff_2025": "askecon_tariff25",
    "askecon_inflation_2022": "askecon_infl2022",
}


class CalibrationError(Exception):
    pass


# ----------------------------------------------------------------------------
# Platt scaling
# ----------------------------------------------------------------------------

def platt_targets(y) -> np.ndarray:
    """Platt (1999) smoothed targets: (N+ + 1)/(N+ + 2) for a positive,
    1/(N- + 2) for a negative, so a separable sample fits a finite slope."""
    y = np.asarray(y, dtype=float)
    n_pos = float(np.sum(y == 1))
    n_neg = float(np.sum(y == 0))
    return np.where(y == 1, (n_pos + 1.0) / (n_pos + 2.0), 1.0 / (n_neg + 2.0))


def fit_platt(scores, y) -> dict:
    """Logistic fit on [1, score] against the smoothed targets."""
    s = np.asarray(scores, dtype=float)
    X = np.column_stack([np.ones_like(s), s])
    out = fit_logit(X, platt_targets(y))
    out["params"] = np.asarray(out["params"], dtype=float)
    return out


def predict_platt(params, scores) -> np.ndarray:
    s = np.asarray(scores, dtype=float)
    return predict_logit(np.asarray(params, dtype=float), np.column_stack([np.ones_like(s), s]))


def features_of(X, y, fit=fit_logit) -> tuple:
    """(params, fit record) for a general design matrix with smoothed targets."""
    rec = fit(np.asarray(X, dtype=float), platt_targets(y))
    return np.asarray(rec["params"], dtype=float), rec


def loo(X, y) -> np.ndarray:
    """Leave-one-out probabilities: row i scored by a fit on every other row.
    X carries its intercept column."""
    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(y)
    if n < 3:
        raise CalibrationError(f"leave-one-out needs at least 3 rows, got {n}")
    p = np.empty(n)
    for i in range(n):
        keep = np.arange(n) != i
        params, _ = features_of(X[keep], y[keep])
        p[i] = predict_logit(params, X[i:i + 1])[0]
    return p


# ----------------------------------------------------------------------------
# Readings
# ----------------------------------------------------------------------------

def murphy(p, y, bins: int = 5) -> dict:
    """Brier and Murphy's decomposition over equal-width probability bins:
    brier = reliability - resolution + uncertainty (exact when binned by the
    binned mean, which is what the table reports)."""
    p = np.asarray(p, dtype=float)
    y = np.asarray(y, dtype=float)
    n = len(y)
    base = float(y.mean())
    edges = np.linspace(0.0, 1.0, bins + 1)
    which = np.clip(np.searchsorted(edges, p, side="right") - 1, 0, bins - 1)
    rel = res = 0.0
    p_binned = np.empty(n)
    for b in range(bins):
        m = which == b
        if not m.any():
            continue
        pb, ob = float(p[m].mean()), float(y[m].mean())
        p_binned[m] = pb
        rel += m.sum() * (pb - ob) ** 2
        res += m.sum() * (ob - base) ** 2
    unc = base * (1.0 - base)
    return {
        "n": int(n),
        "base_rate": base,
        "brier": float(np.mean((p - y) ** 2)),
        "brier_binned": float(np.mean((p_binned - y) ** 2)),
        "reliability": rel / n,
        "resolution": res / n,
        "uncertainty": unc,
        "log_score": float(-np.mean(y * np.log(np.clip(p, 1e-9, 1)) +
                                    (1 - y) * np.log(np.clip(1 - p, 1e-9, 1)))),
        "base_rate_brier": unc,
    }


def reliability_table(p, y, bins: int = 5) -> list[dict]:
    p = np.asarray(p, dtype=float)
    y = np.asarray(y, dtype=float)
    edges = np.linspace(0.0, 1.0, bins + 1)
    which = np.clip(np.searchsorted(edges, p, side="right") - 1, 0, bins - 1)
    rows = []
    for b in range(bins):
        m = which == b
        rows.append({
            "bin": f"[{edges[b]:.1f}, {edges[b + 1]:.1f}{']' if b == bins - 1 else ')'}",
            "n": int(m.sum()),
            "mean_p": float(p[m].mean()) if m.any() else None,
            "observed": float(y[m].mean()) if m.any() else None,
        })
    return rows


def auc(scores, y) -> float:
    s = np.asarray(scores, dtype=float)
    y = np.asarray(y, dtype=bool)
    pos, neg = s[y], s[~y]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    wins = sum(float(a > b) + 0.5 * float(a == b) for a in pos for b in neg)
    return wins / (len(pos) * len(neg))


# ----------------------------------------------------------------------------
# The three inputs
# ----------------------------------------------------------------------------

def detector_scores() -> dict:
    """`operator_led_score` per roster key from results.json; names what is
    not scorable and why."""
    with open(DETECTOR_RESULTS) as f:
        res = json.load(f)
    scored = {}
    for event, key in DETECTOR_KEYS.items():
        if event in res and "operator_led_score" in res[event]:
            scored[key] = float(res[event]["operator_led_score"])
    caches = os.path.isdir(DETECTOR_DATA) and os.path.isdir(GME_DATA)
    missing = sorted(k for k in ROSTER if k not in scored)
    return {
        "scores": scored,
        "labels": {k: ROSTER[k] for k in scored},
        "unscorable": missing,
        "reason": (None if not missing else
                   "no operator_led_score in results.json; re-run detector.py once the "
                   "weekly caches exist" if caches else
                   "no operator_led_score in results.json and the weekly caches under "
                   "major_player_signal/data/ and gamestop_counterfactual/data/ are not in "
                   "the tree, so detector.py cannot be re-run here"),
    }


def battery_scores(field: str = "z") -> dict:
    """The early-warning battery's `z` (or `ews_score`) per roster key."""
    scores, labels = {}, {}
    for key, label in ROSTER.items():
        path = os.path.join(BATTERY_RESULTS, key + ".json")
        if not os.path.exists(path):
            continue
        with open(path) as f:
            d = json.load(f)
        if d.get("status") != "OK" or field not in d:
            continue
        scores[key] = float(d[field])
        labels[key] = label
    return {"scores": scores, "labels": labels, "field": field}


def bnr_rows() -> list[dict]:
    """The 24 rows of classification_table.md, both readings B or R only."""
    rows = []
    with open(BNR_TABLE) as f:
        for line in f:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != 7 or cells[0] in ("substrate", ""):
                continue
            if set(cells[0]) <= {"-", ":"}:
                continue
            substrate, event, f_existing, a_abrupt, structural, substantive, _ = cells
            if structural not in ("B", "R") or substantive not in ("B", "R"):
                continue
            rows.append({"substrate": substrate, "event": event,
                         "f_existing": float(f_existing), "a_abrupt": float(a_abrupt),
                         "structural": structural, "substantive": substantive})
    return rows


def bnr_design(rows) -> np.ndarray:
    return np.array([[1.0, r["f_existing"], math.log(r["a_abrupt"])] for r in rows])


# ----------------------------------------------------------------------------
# The three fits
# ----------------------------------------------------------------------------

def _score_fit(name: str, scores: dict, labels: dict, bins: int) -> dict:
    keys = sorted(scores)
    s = np.array([scores[k] for k in keys])
    y = np.array([labels[k] for k in keys], dtype=float)
    out = {"name": name, "n": len(keys), "keys": keys, "scores": s.tolist(),
           "labels": y.tolist(), "auc_raw": auc(s, y)}
    if len(keys) < 3 or y.min() == y.max():
        out["fit"] = None
        out["reason"] = ("needs at least 3 rows with both labels present; "
                         f"got {len(keys)} rows, labels {sorted(set(y.tolist()))}")
        return out
    rec = fit_platt(s, y)
    a, b = rec["params"].tolist()
    X = np.column_stack([np.ones_like(s), s])
    p_in = predict_platt(rec["params"], s)
    p_loo = loo(X, y)
    out.update({
        "fit": {"intercept": a, "slope": b, "converged": rec["converged"],
                "loglik": rec["loglik"]},
        "p_in_sample": p_in.tolist(),
        "p_loo": p_loo.tolist(),
        "in_sample": murphy(p_in, y, bins),
        "loo": murphy(p_loo, y, bins),
        "reliability_loo": reliability_table(p_loo, y, bins),
    })
    return out


def detector_fit(bins: int = 5) -> dict:
    d = detector_scores()
    out = _score_fit("detector operator_led_score", d["scores"], d["labels"], bins)
    out["unscorable"] = d["unscorable"]
    out["unscorable_reason"] = d["reason"]
    return out


def battery_fit(field: str = "z", bins: int = 5) -> dict:
    d = battery_scores(field)
    out = _score_fit(f"battery {field}", d["scores"], d["labels"], bins)
    out["field"] = field
    return out


def bnr_fit(bins: int = 5) -> dict:
    from classify import structural_label  # noqa: E402  (bifurcation_mix/classify.py)
    rows = bnr_rows()
    X = bnr_design(rows)
    y = np.array([1.0 if r["substantive"] == "B" else 0.0 for r in rows])
    params, rec = features_of(X, y)
    p_in = predict_logit(params, X)
    p_loo = loo(X, y)
    hard = np.array([1.0 if structural_label(r["f_existing"], r["a_abrupt"]) == "B" else 0.0
                     for r in rows])
    if not all(structural_label(r["f_existing"], r["a_abrupt"]) == r["structural"]
               for r in rows):
        raise CalibrationError("classify.py thresholds moved; the table is stale")
    return {
        "name": "bnr substantive B vs R",
        "n": len(rows),
        "features": ["1", "f_existing", "log(a_abrupt)"],
        "events": [f"{r['substrate']}/{r['event']}" for r in rows],
        "labels": y.tolist(),
        "fit": {"params": params.tolist(), "converged": rec["converged"],
                "loglik": rec["loglik"], "aic": rec["aic"]},
        "p_in_sample": p_in.tolist(),
        "p_loo": p_loo.tolist(),
        "in_sample": murphy(p_in, y, bins),
        "loo": murphy(p_loo, y, bins),
        "reliability_loo": reliability_table(p_loo, y, bins),
        "hard_threshold": {
            "rule": "B if f_existing >= SHARE_HI else R if a_abrupt >= ABRUPT_HI",
            "brier": float(np.mean((hard - y) ** 2)),
            "accuracy": float(np.mean(hard == y)),
        },
        "loo_accuracy_at_half": float(np.mean((p_loo >= 0.5) == (y == 1))),
        "auc_loo": auc(p_loo, y),
    }


# ----------------------------------------------------------------------------
# Report
# ----------------------------------------------------------------------------

def _fmt(x, nd=3):
    return "n/a" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{nd}f}"


def _murphy_rows(name: str, m: dict) -> str:
    return (f"| {name} | {m['n']} | {_fmt(m['brier'])} | {_fmt(m['brier_binned'])} | "
            f"{_fmt(m['reliability'])} | {_fmt(m['resolution'])} | {_fmt(m['uncertainty'])} | "
            f"{_fmt(m['log_score'])} |")


def render(results: dict) -> str:
    L = ["# Platt scaling of the detectors -- RESULTS", "",
         "Generated by `validation/calibration/platt.py`; numbers in `results.json`.",
         "Every leave-one-out (LOO) probability is from a fit that never saw its row.",
         "Targets are Platt's smoothed ones. Bins are five equal-width probability bins;",
         "`brier = reliability - resolution + uncertainty` holds for the binned Brier.",
         "The base-rate forecaster scores `uncertainty` exactly, so a row beats the base",
         "rate when its Brier is below that column.", ""]
    L += ["## Murphy table", "",
          "| fit | n | Brier | Brier (binned) | reliability | resolution | uncertainty (= base-rate Brier) | log score |",
          "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for key in ("detector", "battery_z", "battery_ews", "bnr"):
        r = results[key]
        if r.get("fit") is None:
            L.append(f"| {r['name']} | {r['n']} | not fitted: {r['reason']} | | | | | |")
            continue
        L.append(_murphy_rows(f"{r['name']}, in sample", r["in_sample"]))
        L.append(_murphy_rows(f"{r['name']}, LOO", r["loo"]))
    L.append("")
    d = results["detector"]
    L += ["## Detector (`operator_led_score`)", "",
          f"Scored rows: {', '.join(d['keys'])} (n = {d['n']}, raw AUC {_fmt(d['auc_raw'])})."]
    if d["unscorable"]:
        L.append(f"Unscorable: {', '.join(d['unscorable'])}. {d['unscorable_reason']}.")
    if d.get("fit"):
        L.append(f"Fit: p = sigmoid({_fmt(d['fit']['intercept'])} + "
                 f"{_fmt(d['fit']['slope'])} * score).")
        for k, s, p, y in zip(d["keys"], d["scores"], d["p_loo"], d["labels"]):
            L.append(f"- {k}: score {s:+.3f}, LOO p(endogenous) {_fmt(p)}, label {int(y)}")
    L.append("")
    for key, title in (("battery_z", "Battery `z`"), ("battery_ews", "Battery `ews_score`")):
        b = results[key]
        L += [f"## {title}", "",
              f"n = {b['n']}, raw AUC {_fmt(b['auc_raw'])}."]
        if b.get("fit"):
            L.append(f"Fit: p = sigmoid({_fmt(b['fit']['intercept'])} + "
                     f"{_fmt(b['fit']['slope'])} * {b['field']}).")
            L += ["", "| bin | n | mean p | observed |", "|---|---:|---:|---:|"]
            for row in b["reliability_loo"]:
                L.append(f"| {row['bin']} | {row['n']} | {_fmt(row['mean_p'])} | "
                         f"{_fmt(row['observed'])} |")
            L.append("")
            for k, s, p, y in zip(b["keys"], b["scores"], b["p_loo"], b["labels"]):
                L.append(f"- {k}: {b['field']} {s:+.3f}, LOO p {_fmt(p)}, label {int(y)}")
        L.append("")
    r = results["bnr"]
    L += ["## B-vs-R (bifurcation mix, 24 rows)", "",
          f"Features {r['features']}; params {[round(v, 3) for v in r['fit']['params']]}; "
          f"LOO AUC {_fmt(r['auc_loo'])}; LOO accuracy at 0.5: {_fmt(r['loo_accuracy_at_half'])}.",
          f"Hard thresholds (`{r['hard_threshold']['rule']}`): Brier "
          f"{_fmt(r['hard_threshold']['brier'])}, accuracy {_fmt(r['hard_threshold']['accuracy'])}.",
          "", "| bin | n | mean p | observed |", "|---|---:|---:|---:|"]
    for row in r["reliability_loo"]:
        L.append(f"| {row['bin']} | {row['n']} | {_fmt(row['mean_p'])} | {_fmt(row['observed'])} |")
    L += ["", "| event | f_existing | log a_abrupt | LOO p(B) | substantive |", "|---|---:|---:|---:|:---:|"]
    for ev, x, p, y in zip(r["events"], bnr_design(bnr_rows()), r["p_loo"], r["labels"]):
        L.append(f"| {ev} | {x[1]:.3f} | {x[2]:.2f} | {_fmt(p)} | {'B' if y else 'R'} |")
    L.append("")
    return "\n".join(L)


def main(out_dir: str = HERE) -> dict:
    results = {
        "detector": detector_fit(),
        "battery_z": battery_fit("z"),
        "battery_ews": battery_fit("ews_score"),
        "bnr": bnr_fit(),
    }
    with open(os.path.join(out_dir, "results.json"), "w") as f:
        json.dump(results, f, indent=1)
    text = render(results)
    with open(os.path.join(out_dir, "RESULTS.md"), "w") as f:
        f.write(text)
    print(text)
    return results


if __name__ == "__main__":
    main()
