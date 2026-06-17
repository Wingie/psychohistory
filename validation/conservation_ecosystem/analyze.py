"""Ecosystem-scale conservation test (pre-registration test (i)) - analysis step.

Reads weekly_counts.json (per-sub weekly submission counts) and tests, over a
pre-registered MANIA window vs a CALM baseline window of equal length:

  (a) TOTAL attention drift = (mean basket total in MANIA) / (mean in CALM) - 1.
      Pre-registered bound X = 15%. If the total balloons (>> +15%), conservation
      is CONTRADICTED at this scale.
  (b) COMPOSITION churn = total-variation distance between the CALM share vector
      and the MANIA share vector = 0.5 * sum_i |share_mania_i - share_calm_i|.
      Pre-registered floor Y = 40%.

Submission count is an ACTIVITY PROXY for attention-minutes. A finance/meme basket
is NOT the whole attention economy, so a balloon here can be genuine import from
outside the basket rather than a refutation of the global conservation claim.

Windows (8 weeks each, by Monday labels):
  CALM  : 2020-10-05 .. 2020-11-23 (8 Mondays, autumn 2020, pre-mania)
  MANIA : 2021-01-18 .. 2021-03-08 (8 Mondays, GME squeeze peak + aftermath)

Output: result.json, figure_ecosystem.png

Run:  py -3.12 analyze.py
"""
import json
import os
import datetime as dt

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTS = os.path.join(HERE, "weekly_counts.json")

X = 0.15   # drift bound
Y = 0.40   # composition churn floor

# 8-Monday windows (inclusive).
def mondays(start_iso, n):
    s = dt.date.fromisoformat(start_iso)
    return [(s + dt.timedelta(weeks=k)).isoformat() for k in range(n)]

CALM_WEEKS = mondays("2020-10-05", 8)    # 2020-10-05 .. 2020-11-23
MANIA_WEEKS = mondays("2021-01-18", 8)   # 2021-01-18 .. 2021-03-08


def load():
    data = json.load(open(COUNTS))
    subs = list(data.keys())
    # union of all week labels, sorted
    all_weeks = sorted({w for sub in data.values() for w in sub})
    # matrix [sub, week]
    M = np.zeros((len(subs), len(all_weeks)), dtype=float)
    widx = {w: j for j, w in enumerate(all_weeks)}
    for i, s in enumerate(subs):
        for w, c in data[s].items():
            M[i, widx[w]] = c
    return subs, all_weeks, M, widx


def window_totals(subs, M, widx, weeks):
    """Return (per-sub mean count vector over the window, total mean)."""
    cols = [widx[w] for w in weeks if w in widx]
    sub_means = M[:, cols].mean(axis=1)  # mean weekly count per sub
    return sub_means


def main():
    subs, all_weeks, M, widx = load()

    calm_vec = window_totals(subs, M, widx, CALM_WEEKS)
    mania_vec = window_totals(subs, M, widx, MANIA_WEEKS)

    calm_total = float(calm_vec.sum())
    mania_total = float(mania_vec.sum())
    drift = mania_total / calm_total - 1.0

    # composition shares
    calm_share = calm_vec / calm_vec.sum()
    mania_share = mania_vec / mania_vec.sum()
    tv_churn = 0.5 * float(np.abs(mania_share - calm_share).sum())

    # --- also report the "incumbent-only" basket (subs that existed in CALM) ---
    incumbent = calm_vec > 0
    inc_calm = calm_vec[incumbent].sum()
    inc_mania = mania_vec[incumbent].sum()
    inc_drift = float(inc_mania / inc_calm - 1.0)
    inc_calm_share = calm_vec[incumbent] / inc_calm
    inc_mania_share = mania_vec[incumbent] / inc_mania
    inc_churn = 0.5 * float(np.abs(inc_mania_share - inc_calm_share).sum())

    # verdict on full basket
    total_flat = abs(drift) < X
    churns = tv_churn > Y
    if drift > X:
        verdict = "CONTRADICTED"
        verdict_note = ("basket total ballooned by >X during the mania; aggregate "
                        "activity in this basket is NOT conserved at this scale")
    elif total_flat and churns:
        verdict = "SUPPORTED"
        verdict_note = ("total roughly flat within X while composition churns past Y")
    else:
        verdict = "INCONCLUSIVE"
        verdict_note = ("neither clean balloon nor clean flat-with-churn")

    result = {
        "test": "pre-registration (i) conservation / zero-sum attention, ECOSYSTEM scale",
        "proxy": "weekly submission count (activity proxy for attention-minutes)",
        "thresholds": {"X_drift_bound": X, "Y_churn_floor": Y},
        "basket": subs,
        "calm_window": {"weeks": CALM_WEEKS},
        "mania_window": {"weeks": MANIA_WEEKS},
        "per_sub_mean_weekly_calm": {s: round(float(v), 1) for s, v in zip(subs, calm_vec)},
        "per_sub_mean_weekly_mania": {s: round(float(v), 1) for s, v in zip(subs, mania_vec)},
        "calm_total_mean_weekly": round(calm_total, 1),
        "mania_total_mean_weekly": round(mania_total, 1),
        "total_drift": round(drift, 4),
        "total_drift_pct": round(drift * 100, 1),
        "composition_churn_TV": round(tv_churn, 4),
        "composition_churn_pct": round(tv_churn * 100, 1),
        "full_basket_verdict": verdict,
        "verdict_note": verdict_note,
        "incumbent_only": {
            "note": ("subset of subs that already existed in the CALM window "
                     "(drops amcstock/Superstonk which were born during the mania); "
                     "isolates redistribution among pre-existing channels from the "
                     "import created by brand-new subreddits"),
            "subs": [s for s, k in zip(subs, incumbent) if k],
            "drift": round(inc_drift, 4),
            "drift_pct": round(inc_drift * 100, 1),
            "churn_TV": round(inc_churn, 4),
            "churn_pct": round(inc_churn * 100, 1),
        },
        "scale_caveat": (
            "Submission count is an activity proxy for attention-minutes, not a "
            "direct measure. This finance/meme basket is NOT the whole attention "
            "economy; a balloon here can be genuine import of attention from outside "
            "the basket (people reallocating from non-finance subs and from offline) "
            "rather than a refutation of the GLOBAL sub-generational-budget claim. The "
            "pre-registered global test fixes the scale to the top-N platform total, "
            "which this single-ecosystem basket does not span."
        ),
    }
    json.dump(result, open(os.path.join(HERE, "result.json"), "w"), indent=2)

    # ---- figure: stacked area of basket weekly counts + total line ----
    span = [w for w in all_weeks]
    # keep only weeks in 2020-06 .. 2021-07 (all of them already are)
    Msel = M
    x = np.arange(len(span))
    fig, ax = plt.subplots(figsize=(13, 6.5))
    # order subs by total volume for a readable stack
    order = np.argsort(-Msel.sum(axis=1))
    bottom = np.zeros(len(span))
    colors = plt.cm.tab20(np.linspace(0, 1, len(subs)))
    for rank, i in enumerate(order):
        ax.fill_between(x, bottom, bottom + Msel[i], step="mid",
                        label=subs[i], color=colors[rank], alpha=0.85, linewidth=0)
        bottom = bottom + Msel[i]
    ax.plot(x, bottom, color="black", lw=2.0, label="BASKET TOTAL")

    # shade calm + mania windows
    def shade(weeks, color, txt):
        idx = [span.index(w) for w in weeks if w in span]
        if idx:
            ax.axvspan(min(idx) - 0.5, max(idx) + 0.5, color=color, alpha=0.12)
            ax.text((min(idx) + max(idx)) / 2, ax.get_ylim()[1] * 0.96, txt,
                    ha="center", va="top", fontsize=10, fontweight="bold")
    shade(CALM_WEEKS, "tab:blue", "CALM")
    shade(MANIA_WEEKS, "tab:red", "MANIA")

    # x ticks every 4 weeks
    tick_idx = list(range(0, len(span), 4))
    ax.set_xticks(tick_idx)
    ax.set_xticklabels([span[i][2:] for i in tick_idx], rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("weekly submissions (activity proxy for attention)")
    ax.set_xlabel("ISO week (Monday), 2020-06 .. 2021-07")
    ax.set_title(f"Finance/meme basket weekly submissions - drift {drift*100:+.0f}% "
                 f"(X={int(X*100)}%), churn {tv_churn*100:.0f}% (Y={int(Y*100)}%) "
                 f"-> {verdict}")
    ax.legend(ncol=2, fontsize=8, loc="upper left")
    ax.margins(x=0.01)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "figure_ecosystem.png"), dpi=130)

    # console summary
    print(json.dumps({k: result[k] for k in (
        "calm_total_mean_weekly", "mania_total_mean_weekly", "total_drift_pct",
        "composition_churn_pct", "full_basket_verdict")}, indent=2))
    print("incumbent-only drift%/churn%:", result["incumbent_only"]["drift_pct"],
          result["incumbent_only"]["churn_pct"])


if __name__ == "__main__":
    main()
