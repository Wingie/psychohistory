"""Domain study 3: finance — the flagship binary test.

Panel: JST Macrohistory R6, 18 countries, 1875-2020, excluding the world
wars (1914-1918, 1939-1945) as in Schularick-Taylor 2012. v = trailing
5-year annualized real credit growth (tloans deflated by CPI). s = the
era-coded regulation/repression index (curated; honesty notes in
curated/README.md). Event = systemic crisis flag (crisisJST).

Step 1 reproduces the known result (credit booms predict crises: the v-only
logit has beta > 0 and beats chance). Step 2 is our addition: does the
steering term improve on it? Pre-registered falsifier: LR(full vs v) —
p > 0.1 here counts against s/acc.

Run `python -m steering_envelope.validate.finance`.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from . import datasets, fit, style

RESULTS = Path(__file__).resolve().parent / "results"
FIGDIR = Path(__file__).resolve().parents[1] / "figures"

WAR_YEARS = set(range(1914, 1919)) | set(range(1939, 1946))


def build_panel() -> pd.DataFrame:
    df = datasets.load_jst()
    df = df.dropna(subset=["tloans", "cpi", "crisisJST"]).copy()
    df["real_credit"] = df["tloans"] / df["cpi"]
    df = df.sort_values(["country", "year"])
    df["v"] = df.groupby("country")["real_credit"].transform(
        lambda x: (x / x.shift(5)) ** (1 / 5) - 1.0)
    eras = datasets.load_curated("finance_regulation_index")
    def era_s(year):
        row = eras[(eras["year_from"] <= year) & (year <= eras["year_to"])]
        return float(row["s_index"].iloc[0]) if len(row) else np.nan
    df["s"] = df["year"].map(era_s)
    df["event"] = (df["crisisJST"] > 0).astype(float)
    df = df.dropna(subset=["v", "s"])
    df = df[~df["year"].isin(WAR_YEARS)]
    df = df[np.isfinite(df["v"])]
    return df.reset_index(drop=True)


def run() -> dict:
    df = build_panel()
    res = fit.domain_comparison(
        df["v"], df["s"], df["event"], years=df["year"].values,
        log_v=False, log_s=False, name="finance (JST 18 countries)")
    res["panel_years"] = [int(df["year"].min()), int(df["year"].max())]
    res["countries"] = int(df["country"].nunique())

    # the Schularick-Taylor reproduction: v-only beta positive, AUC > 0.5
    zv = (df["v"] - df["v"].mean()) / df["v"].std(ddof=1)
    vfit = fit.fit_logit(np.column_stack([np.ones(len(df)), zv]),
                         df["event"].values)
    res["schularick_taylor_check"] = {
        "beta_v": float(vfit["params"][1]),
        "auc_v": res["auc"]["v"],
        "reproduced": bool(vfit["params"][1] > 0 and res["auc"]["v"] > 0.55),
    }

    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "finance.json").write_text(json.dumps(res, indent=2))
    make_figure(df)
    return res


def make_figure(df):
    style.apply()
    import matplotlib.pyplot as plt

    FIGDIR.mkdir(exist_ok=True)
    fig, axes = plt.subplots(2, 1, figsize=(8.2, 6.6), sharex=True)

    yearly = df.groupby("year").agg(
        v=("v", "mean"), s=("s", "mean"), crises=("event", "sum"))

    ax = axes[0]
    ax.bar(yearly.index, yearly["crises"], color=style.C_MAGENTA, width=1.0)
    ax.set_ylabel("systemic crises (count)")
    ax.set_title("finance: crises cluster where credit runs ahead of "
                 "regulation", loc="left")

    ax = axes[1]
    ax.plot(yearly.index, yearly["v"] * 100, color=style.C_YELLOW,
            label="mean real credit growth %/yr")
    ax.plot(yearly.index, yearly["s"] * 10, color=style.C_GREEN,
            label="regulation index x10")
    ax.axhline(0, color=style.GRID, linewidth=1)
    ax.set_xlabel("year")
    ax.legend(loc="upper left")
    ax.set_title("the quiet period (1945-72): high s, few crises",
                 loc="left")
    fig.tight_layout()
    fig.savefig(FIGDIR / "finance.png")
    plt.close(fig)


if __name__ == "__main__":
    r = run()
    print(json.dumps({k: v for k, v in r.items() if k != "loro_auc"},
                     indent=2, default=str))
    print("LORO AUC:", r.get("loro_auc"))
