"""Domain study 1: US roads — the literal steering case.

Panel: US, annual, 1926-2023 (VMT series begins 1921; the first five years
feed the growth window). v = trailing 5-year annualized VMT growth.
s = cumulative steering-stack index (curated interventions with a 5-year
phase-in). Event = deterioration year: fatalities per 100M VMT rise
year-over-year. Pre-registered in the module README; run
`python -m steering_envelope.validate.roads`.

Also reports a +-50% weight-jitter robustness check on the curated steering
weights (the LR conclusion should not hinge on the hand-coded weights).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from . import datasets, fit, style

RESULTS = Path(__file__).resolve().parent / "results"
FIGDIR = Path(__file__).resolve().parents[1] / "figures"


def build_panel():
    df = datasets.load_us_roads()
    df = df.dropna(subset=["vmt", "rate"]).reset_index(drop=True)
    df = df[df["year"] >= 1921].reset_index(drop=True)
    df["v"] = (df["vmt"] / df["vmt"].shift(5)) ** (1 / 5) - 1.0
    df["event"] = (df["rate"].diff() > 0).astype(float)
    df = df.dropna(subset=["v"]).reset_index(drop=True)
    events = datasets.load_curated("us_road_steering")
    df["s"] = datasets.steering_index(events, df["year"].values)
    # growth can be slightly negative (1932, 1942-45, 1974, 1979, 2008, 2020):
    # shift to a positive speed scale before logging
    df["v_pos"] = 1.0 + df["v"]
    return df, events


def run(n_jitter: int = 200, seed: int = 0) -> dict:
    df, events = build_panel()
    # primary: continuous level fit of log fatality rate on z(log v), z(log s)
    # (with the built-in first-difference robustness fit); secondary: the
    # binary deterioration-year logit, reported even though it is weak
    res = fit.continuous_comparison(
        df["v_pos"], df["s"], np.log(df["rate"]), years=df["year"].values,
        name="roads (US)")
    res["secondary_binary"] = fit.domain_comparison(
        df["v_pos"], df["s"], df["event"], years=df["year"].values,
        name="roads (US, deterioration years)")

    # weight-jitter robustness: does p(s|v) survive re-weighting the stack?
    rng = np.random.default_rng(seed)
    ps = []
    for _ in range(n_jitter):
        jittered = events.copy()
        jittered["weight"] = jittered["weight"] * rng.uniform(
            0.5, 1.5, len(jittered))
        s_j = datasets.steering_index(jittered, df["year"].values)
        r = fit.continuous_comparison(df["v_pos"], s_j, np.log(df["rate"]),
                                      name="jitter")
        ps.append(r["lr_p_s_given_v"])
    res["jitter_p_s_given_v_frac_below_0.1"] = float(
        np.mean(np.array(ps) < 0.1))
    res["panel_years"] = [int(df["year"].min()), int(df["year"].max())]

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "roads.json").write_text(json.dumps(res, indent=2))
    make_figure(df)
    return res


def make_figure(df):
    style.apply()
    import matplotlib.pyplot as plt

    FIGDIR.mkdir(exist_ok=True)
    figfile = FIGDIR / "roads.png"
    fig, axes = plt.subplots(2, 1, figsize=(8.2, 6.4), sharex=True)

    ax = axes[0]
    ax.plot(df["year"], df["rate"], color=style.C_BLUE)
    ax.set_ylabel("deaths per 100M VMT")
    ax.set_title("US roads: the fatality rate fell 20x while volume exploded",
                 loc="left")
    bad = df[df["event"] == 1]
    ax.scatter(bad["year"], bad["rate"], s=14, color=style.C_MAGENTA,
               zorder=3, label="deterioration year")
    ax.legend(loc="upper right")

    ax = axes[1]
    ratio = np.log(df["v_pos"]) - np.log(df["s"] / df["s"].mean())
    ax.plot(df["year"], (ratio - ratio.mean()) / ratio.std(),
            color=style.C_YELLOW)
    ax.axhline(0, color=style.GRID, linewidth=1)
    ax.set_ylabel("z(log v/s)")
    ax.set_xlabel("year")
    ax.set_title("the envelope ratio: speed growth over steering stack",
                 loc="left")
    fig.tight_layout()
    fig.savefig(figfile)
    plt.close(fig)


if __name__ == "__main__":
    r = run()
    print(json.dumps({k: v for k, v in r.items() if k != "loro_auc"},
                     indent=2, default=str))
    print("LORO AUC:", r.get("loro_auc"))
