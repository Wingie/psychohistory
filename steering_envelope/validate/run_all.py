"""Run all five domain studies and write the combined summary
(results/summary.json + the per-domain table used by the page).

Run `python -m steering_envelope.validate.run_all`.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import ai_proxy, aviation, finance, fit, nuclear, roads

RESULTS = Path(__file__).resolve().parent / "results"


def main() -> dict:
    print("[1/5] roads ...")
    r_roads = roads.run()
    print("[2/5] aviation ...")
    r_avia = aviation.run()
    print("[3/5] finance ...")
    r_fin = finance.run()
    print("[4/5] nuclear ...")
    r_nuc = nuclear.run()
    print("[5/5] ai ...")
    r_ai = ai_proxy.run()

    # the pre-registered scoreboard: p(s|v) <= 0.1 in how many of the
    # fittable historical domains? (nuclear is a case study by design; roads
    # and aviation are judged on the stricter first-difference test, finance
    # on the panel logit)
    fittable = {
        "roads (differenced)": r_roads["diff"]["lr_p_s_given_v"],
        "aviation (differenced)": r_avia["diff"]["lr_p_s_given_v"],
        "finance (panel logit)": r_fin["lr_p_s_given_v"],
    }
    s_adds = {k: bool(p <= 0.1) for k, p in fittable.items()}
    v_adds = {
        "roads (differenced)": bool(
            r_roads["diff"]["lr_p_v_given_s"] <= 0.1),
        "aviation (differenced)": bool(
            r_avia["diff"]["lr_p_v_given_s"] <= 0.1),
        "finance (panel logit)": bool(r_fin["lr_p_v_given_s"] <= 0.1),
    }

    summary = {
        "domains": {
            "roads": r_roads, "aviation": r_avia, "finance": r_fin,
            "nuclear": r_nuc, "ai": {k: v for k, v in r_ai.items()
                                     if k != "ai_series"},
        },
        "scoreboard": {
            "p_s_given_v": fittable,
            "s_adds_power": s_adds,
            "v_adds_power": v_adds,
            "n_domains_s_adds": int(sum(s_adds.values())),
            "verdict": _verdict(s_adds, v_adds),
        },
    }
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "summary.json").write_text(
        json.dumps(summary, indent=2, default=str))
    return summary


def _verdict(s_adds: dict, v_adds: dict) -> str:
    ns, nv = sum(s_adds.values()), sum(v_adds.values())
    n = len(s_adds)
    if ns == 0:
        return ("FALSIFIED: the steering term is decoration; s/acc loses "
                "its empirical leg")
    if nv == 0:
        return "s dominates everywhere: the stopper position gains support"
    return (f"s adds predictive power in {ns}/{n} fittable domains and v "
            f"adds power in {nv}/{n}: both terms of the ratio carry "
            "signal — the envelope form survives")


if __name__ == "__main__":
    s = main()
    print(json.dumps(s["scoreboard"], indent=2))
