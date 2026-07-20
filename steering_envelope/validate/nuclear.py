"""Domain study 4: civil nuclear power — a case study, not a fit.

Seven decades, ten INES>=4-class events. With N this small a logistic fit
would be numerology, so this module does only what the pre-registration
allows: decade-level event rates per reactor-year with Jeffreys (Gamma)
credible intervals, and the ordinal question — do high-v/s decades sit
above low-v/s decades in event rate?

Run `python -m steering_envelope.validate.nuclear`.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy import stats

from . import datasets, style

RESULTS = Path(__file__).resolve().parent / "results"
FIGDIR = Path(__file__).resolve().parents[1] / "figures"


def run() -> dict:
    df = datasets.load_curated("nuclear")
    # v: capacity added this decade relative to installed base (expansion
    # velocity); s: curated regulator-maturity index
    df = df.copy()
    df["rate_per_kry"] = 1000.0 * df["ines4plus_events"] / df["reactor_years"]
    base = df["reactor_years"] / 10.0  # rough installed reactors
    df["v"] = df["capacity_added_gw"] / np.maximum(base * 0.9, 1.0)
    df["ratio"] = df["v"] / df["s_regulator"]

    # Jeffreys interval for a Poisson rate: Gamma(k + 1/2, T)
    lo, hi = [], []
    for _, r in df.iterrows():
        g = stats.gamma(r["ines4plus_events"] + 0.5,
                        scale=1.0 / r["reactor_years"])
        lo.append(1000 * g.ppf(0.05))
        hi.append(1000 * g.ppf(0.95))
    df["rate_lo"], df["rate_hi"] = lo, hi

    # ordinal check: Spearman rank correlation of v/s vs event rate
    rho, p = stats.spearmanr(df["ratio"], df["rate_per_kry"])
    # split comparison: above-median ratio decades vs below
    med = df["ratio"].median()
    hi_side = df[df["ratio"] > med]
    lo_side = df[df["ratio"] <= med]
    rate_hi = hi_side["ines4plus_events"].sum() / hi_side["reactor_years"].sum()
    rate_lo = lo_side["ines4plus_events"].sum() / lo_side["reactor_years"].sum()

    res = {
        "name": "nuclear (world, decades)",
        "n_decades": int(len(df)),
        "events": int(df["ines4plus_events"].sum()),
        "spearman_ratio_vs_rate": {"rho": float(rho), "p": float(p)},
        "rate_per_kry_high_ratio": float(1000 * rate_hi),
        "rate_per_kry_low_ratio": float(1000 * rate_lo),
        "rate_ratio_high_over_low": float(rate_hi / rate_lo),
        "caveat": ("case study only: 7 decades, 9 events; consistent with "
                   "the envelope story (early fast-build/weak-regulator "
                   "decades carry the event burden) but cannot "
                   "discriminate hypotheses on its own"),
        "decades": df[["decade", "rate_per_kry", "v", "s_regulator",
                       "ratio"]].round(3).to_dict("records"),
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "nuclear.json").write_text(json.dumps(res, indent=2))
    make_figure(df)
    return res


def make_figure(df):
    style.apply()
    import matplotlib.pyplot as plt

    FIGDIR.mkdir(exist_ok=True)
    fig, axes = plt.subplots(2, 1, figsize=(8.2, 6.2), sharex=True)
    x = df["decade"] + 5

    ax = axes[0]
    ax.errorbar(x, df["rate_per_kry"],
                yerr=[np.maximum(df["rate_per_kry"] - df["rate_lo"], 0.0),
                      np.maximum(df["rate_hi"] - df["rate_per_kry"], 0.0)],
                fmt="o", color=style.C_BLUE, capsize=3, markersize=7)
    ax.set_ylabel("events / 1000 reactor-yr")
    ax.set_title("nuclear: INES>=4-class event rate by decade (90% CI)",
                 loc="left")

    ax = axes[1]
    ax.bar(x, df["ratio"], width=6, color=style.C_YELLOW)
    ax.set_xlabel("decade")
    ax.set_ylabel("v / s")
    ax.set_title("expansion velocity over regulator maturity", loc="left")
    fig.tight_layout()
    fig.savefig(FIGDIR / "nuclear.png")
    plt.close(fig)


if __name__ == "__main__":
    print(json.dumps(run(), indent=2, default=str))
