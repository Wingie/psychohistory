"""Domain study 2: commercial aviation.

Panel: world, annual, 1975-2019 (departures begin 1970; five years feed the
growth window; post-2019 is excluded because the pandemic collapse in
departures makes the growth proxy meaningless). v = trailing 5-year
annualized growth of registered carrier departures (World Bank IS.AIR.DPRT).
s = cumulative oversight-stack index (curated milestones, 5-year phase-in).
Outcome (continuous primary): log fatal airliner accidents per million
flights (OWID/ASN). Secondary binary: deterioration years.

Run `python -m steering_envelope.validate.aviation`.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from . import datasets, fit, style

RESULTS = Path(__file__).resolve().parent / "results"
FIGDIR = Path(__file__).resolve().parents[1] / "figures"


def build_panel():
    rate = datasets.load_owid_aviation()
    dep = datasets.load_wb_departures()
    df = rate.merge(dep, on="year", how="inner").sort_values("year")
    df = df[df["year"] <= 2019].reset_index(drop=True)
    df["v"] = (df["departures"] / df["departures"].shift(5)) ** (1 / 5) - 1.0
    df["v_pos"] = 1.0 + df["v"]
    df = df.dropna(subset=["v", "fatal_per_million"]).reset_index(drop=True)
    events = datasets.load_curated("aviation_steering")
    df["s"] = datasets.steering_index(events, df["year"].values)
    df["event"] = (df["fatal_per_million"].diff() > 0).astype(float)
    return df, events


def run(n_jitter: int = 200, seed: int = 0) -> dict:
    df, events = build_panel()
    res = fit.continuous_comparison(
        df["v_pos"], df["s"], np.log(df["fatal_per_million"]),
        years=df["year"].values, name="aviation (world)")
    res["secondary_binary"] = fit.domain_comparison(
        df["v_pos"], df["s"], df["event"], years=df["year"].values,
        name="aviation (deterioration years)")

    rng = np.random.default_rng(seed)
    ps = []
    for _ in range(n_jitter):
        jittered = events.copy()
        jittered["weight"] = jittered["weight"] * rng.uniform(
            0.5, 1.5, len(jittered))
        s_j = datasets.steering_index(jittered, df["year"].values)
        r = fit.continuous_comparison(
            df["v_pos"], s_j, np.log(df["fatal_per_million"]), name="jitter")
        ps.append(r["lr_p_s_given_v"])
    res["jitter_p_s_given_v_frac_below_0.1"] = float(
        np.mean(np.array(ps) < 0.1))
    res["panel_years"] = [int(df["year"].min()), int(df["year"].max())]

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "aviation.json").write_text(json.dumps(res, indent=2))
    make_figure(df)
    return res


def make_figure(df):
    style.apply()
    import matplotlib.pyplot as plt

    FIGDIR.mkdir(exist_ok=True)
    fig, axes = plt.subplots(2, 1, figsize=(8.2, 6.4), sharex=True)

    ax = axes[0]
    ax.plot(df["year"], df["fatal_per_million"], color=style.C_BLUE)
    ax.set_yscale("log")
    ax.set_ylabel("fatal accidents / M flights")
    ax.set_title("aviation: rate falls as the oversight stack accumulates",
                 loc="left")

    ax = axes[1]
    ax.plot(df["year"], df["s"], color=style.C_GREEN, label="steering stack s")
    ax.plot(df["year"], 1 + 10 * df["v"], color=style.C_YELLOW,
            label="1 + 10x departure growth v")
    ax.set_xlabel("year")
    ax.legend(loc="upper left")
    ax.set_title("speed and steering, same window", loc="left")
    fig.tight_layout()
    fig.savefig(FIGDIR / "aviation.png")
    plt.close(fig)


if __name__ == "__main__":
    r = run()
    print(json.dumps({k: v for k, v in r.items()
                      if k not in ("loro_r", "secondary_binary")},
                     indent=2, default=str))
    print("LORO r:", r.get("loro_r"))
    print("binary p(s|v):", r["secondary_binary"]["lr_p_s_given_v"])
