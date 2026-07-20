"""Domain study 5: AI — leading indicators only. There is no outcome data
for AI corners yet, and this module refuses to pretend otherwise.

What it does produce is the money chart: each historical domain's envelope
ratio z(log v/s), standardized within its own history, with its known
corners marked — and AI's trajectory on the same relative scale.

AI proxies: v = frontier training-compute growth (Epoch AI notable models:
slope of the yearly frontier, i.e. rolling max of log10 FLOP, over a
trailing 3-year window). s = normalized steering index from the curated
order-of-magnitude table (policy counts + eval institutions), plus the AIID
incident series shown for context only.

Standardization caveat, stated on the chart and in the JSON: z-scores are
within-domain, so the comparison says "how far outside its OWN historical
envelope each domain was", not that a unit of AI ratio equals a unit of
credit ratio.

Run `python -m steering_envelope.validate.ai_proxy`.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import aviation, datasets, finance, roads, style

RESULTS = Path(__file__).resolve().parent / "results"
FIGDIR = Path(__file__).resolve().parents[1] / "figures"


def _z(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    return (x - np.nanmean(x)) / np.nanstd(x, ddof=1)


def ai_series() -> pd.DataFrame:
    """AI envelope-ratio series 2014-present."""
    ep = datasets.load_epoch()
    cur = datasets.load_curated("ai_steering")
    # frontier = running max of log10 training FLOP by year
    fr = ep.groupby("year")["flop"].max().apply(np.log10).cummax()
    fr = fr[fr.index >= 2010]
    # v = OOMs/year over trailing 3y window -> growth factor per year
    v = fr.diff(3) / 3.0
    df = pd.DataFrame({"year": fr.index, "frontier_log10_flop": fr.values,
                       "v_ooms_per_year": v.values}).dropna()
    df = df.merge(cur, on="year", how="inner")
    # s: policies + strongly-weighted eval institutions, normalized to [~0.1, 1]
    s_raw = df["policy_cum"] + 50.0 * df["eval_orgs_cum"]
    df["s"] = 0.1 + 0.9 * s_raw / s_raw.max()
    # speed as a multiplicative factor per year (10^ooms), envelope ratio
    df["v_factor"] = 10.0 ** df["v_ooms_per_year"]
    df["log_ratio"] = np.log(df["v_factor"]) - np.log(df["s"])
    return df


def historical_ratios() -> dict:
    """z(log v/s) per historical domain plus its corner years."""
    out = {}

    r_df, _ = roads.build_panel()
    lr = np.log(r_df["v_pos"]) - np.log(r_df["s"] / r_df["s"].mean())
    # corners: the five worst deterioration years by rate increase
    worst = r_df.assign(d=r_df["rate"].diff()).nlargest(5, "d")["year"]
    out["roads"] = {"years": r_df["year"].tolist(), "z": _z(lr).tolist(),
                    "corners": sorted(int(y) for y in worst)}

    a_df, _ = aviation.build_panel()
    la = np.log(a_df["v_pos"]) - np.log(a_df["s"] / a_df["s"].mean())
    worst = a_df.assign(d=a_df["fatal_per_million"].diff()).nlargest(
        4, "d")["year"]
    out["aviation"] = {"years": a_df["year"].tolist(), "z": _z(la).tolist(),
                       "corners": sorted(int(y) for y in worst)}

    f_df = finance.build_panel()
    yearly = f_df.groupby("year").agg(v=("v", "mean"), s=("s", "mean"),
                                      crises=("event", "sum"))
    lf = yearly["v"] - np.log(yearly["s"] / yearly["s"].mean())
    corners = yearly[yearly["crises"] >= 3].index
    out["finance"] = {"years": [int(y) for y in yearly.index],
                      "z": _z(lf).tolist(),
                      "corners": [int(y) for y in corners]}
    return out


def run() -> dict:
    ai = ai_series()
    hist = historical_ratios()
    ai_z = _z(ai["log_ratio"])

    # where were the historical domains, in their own z units, when their
    # corners bit?
    corner_zs = []
    for dom, d in hist.items():
        zmap = dict(zip(d["years"], d["z"]))
        corner_zs.extend([zmap[y] for y in d["corners"] if y in zmap])

    res = {
        "name": "ai (leading indicators only)",
        "ai_current_year": int(ai["year"].iloc[-1]),
        "ai_current_z": float(ai_z[len(ai_z) - 1]),
        "ai_series": {
            "years": ai["year"].tolist(),
            "v_ooms_per_year": [round(float(x), 3)
                                for x in ai["v_ooms_per_year"]],
            "s": [round(float(x), 3) for x in ai["s"]],
            "z_log_ratio": [round(float(x), 3) for x in ai_z],
        },
        "historical_corner_z": {
            "mean": float(np.mean(corner_zs)),
            "min": float(np.min(corner_zs)),
            "max": float(np.max(corner_zs)),
            "values": [round(float(z), 3) for z in corner_zs],
        },
        "verdict": ("AI's envelope ratio sits {} its own historical mean; "
                    "historical corners bit at a mean of {:+.2f}z within "
                    "their domains. Within-domain z only; no cross-domain "
                    "unit equivalence claimed, and no outcome data exists "
                    "for AI yet.").format(
            "above" if ai_z[len(ai_z) - 1] > 0 else "below",
            float(np.mean(corner_zs))),
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "ai_proxy.json").write_text(json.dumps(res, indent=2))
    make_figure(ai, ai_z, hist, corner_zs)
    return res


def make_figure(ai, ai_z, hist, corner_zs):
    style.apply()
    import matplotlib.pyplot as plt

    FIGDIR.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(9.0, 5.4))

    colors = {"roads": style.C_BLUE, "aviation": style.C_GREEN,
              "finance": style.C_MAGENTA}
    for dom, d in hist.items():
        years = np.asarray(d["years"], dtype=float)
        # time re-based: years since domain start, so eras overlay
        ax.plot(years - years[0], d["z"], color=colors[dom], alpha=0.85,
                label=dom)
        zmap = dict(zip(d["years"], d["z"]))
        cx = [y - years[0] for y in d["corners"] if y in zmap]
        cy = [zmap[y] for y in d["corners"] if y in zmap]
        ax.scatter(cx, cy, s=42, color=colors[dom], marker="x", linewidth=2)

    ai_years = np.asarray(ai["year"], dtype=float)
    ax.plot(ai_years - ai_years[0], ai_z, color=style.C_YELLOW, linewidth=3,
            label="AI (2014- )")
    ax.scatter([ai_years[-1] - ai_years[0]], [ai_z[len(ai_z) - 1]], s=90,
               color=style.C_YELLOW, zorder=5)
    band = (float(np.min(corner_zs)), float(np.max(corner_zs)))
    ax.axhspan(band[0], band[1], color=style.C_MAGENTA, alpha=0.08)
    ax.axhline(float(np.mean(corner_zs)), color=style.C_MAGENTA,
               linewidth=1, linestyle="--")
    ax.set_xlabel("years since domain start")
    ax.set_ylabel("z(log v/s), within domain")
    ax.set_title("the money chart: every domain's envelope ratio, corners "
                 "marked (x); AI is the thick line", loc="left")
    ax.legend(loc="lower left", ncol=2)
    ax.text(0.99, 0.02,
            "within-domain z-scores; corner band = range of ratios at "
            "historical corners",
            transform=ax.transAxes, ha="right", fontsize=8,
            color=style.MUTED)
    fig.tight_layout()
    fig.savefig(FIGDIR / "ai_ratio.png")
    plt.close(fig)


if __name__ == "__main__":
    r = run()
    print(json.dumps({k: v for k, v in r.items() if k != "ai_series"},
                     indent=2, default=str))
