"""Test (iii') bifurcation-mix conjecture: classify each roster event B / N / R under
two independent, pre-registered rules (see PREREG.md, frozen BEFORE this ran), compute
the B-fraction under each, and the structural-vs-substantive inter-rater agreement.

STRUCTURAL rule (blind to early-warning / N_eff SCORE): keyed on
  f_existing = existing-community share of onset activity (V1 quantity), and
  a_abrupt   = onset/pre-onset mean-daily-activity ratio.
  B if f_existing >= SHARE_HI; else R if a_abrupt >= ABRUPT_HI; else N.

SUBSTANTIVE rule (blind to N_eff outcome): public-onset description, one-line rationale.

Run: py -3.12 validation/bifurcation_mix/classify.py
"""
import os
import json
import datetime as dt
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
VAL = os.path.dirname(HERE)
WIKI_DATA = os.path.join(VAL, "wikipedia", "data")
WIKI_V1 = os.path.join(VAL, "wikipedia", "diagnostics", "v1_newcomer_flood.json")
WSB_DATA = os.path.join(VAL, "reddit_wsb", "data")

# ---- frozen thresholds (committed in PREREG.md BEFORE this computation) ----
SHARE_HI = 0.20
ABRUPT_HI = 8.0
PI_B = 0.60

# Window params, mirrored from the two neff pipelines.
WIKI_POST_DAYS = 21
WIKI_BASELINE_DAYS = 90
WSB_PRE_GRAPH_DAYS = 90
WSB_POST_DAYS = 21


def parse_ts(ts):
    return dt.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").date()


# ----------------------------------------------------------------------------
# STRUCTURAL features
# ----------------------------------------------------------------------------
def wiki_structural():
    """Per Wikipedia event: f_existing (from V1, the frozen-partition quantity) and
    a_abrupt (onset/pre-onset focal-edit daily ratio from focal_revs)."""
    v1 = json.load(open(WIKI_V1))
    fexist = {r["title"]: r["f_existing"] for r in v1["rows"]}
    rows = []
    for fn in sorted(os.listdir(WIKI_DATA)):
        if not fn.endswith("__event.json"):
            continue
        d = json.load(open(os.path.join(WIKI_DATA, fn), encoding="utf-8"))
        title = d["title"]
        if title not in fexist:
            continue  # only the 14 OK (K>=3) events have a V1 f_existing
        onset = dt.date.fromisoformat(d["onset"])
        olo, ohi = onset, onset + dt.timedelta(days=WIKI_POST_DAYS)
        plo, phi = onset - dt.timedelta(days=WIKI_BASELINE_DAYS), onset
        on_edits = pre_edits = 0
        for rv in d["focal_revs"]:
            ts = rv.get("ts")
            if not ts:
                continue
            day = parse_ts(ts)
            if olo <= day < ohi:
                on_edits += 1
            elif plo <= day < phi:
                pre_edits += 1
        on_rate = on_edits / WIKI_POST_DAYS
        pre_rate = pre_edits / WIKI_BASELINE_DAYS
        a_abrupt = on_rate / pre_rate if pre_rate > 0 else float("inf")
        rows.append(dict(substrate="wiki", event=title,
                         f_existing=fexist[title], a_abrupt=a_abrupt,
                         on_edits=on_edits, pre_edits=pre_edits))
    return rows


def wsb_structural():
    """Per WSB cascade: f_existing (onset-window comments by pre-onset authors) and
    a_abrupt (onset/pre-onset comments-per-day ratio)."""
    rows = []
    for label, onset_iso in WSB_ONSETS.items():
        path = os.path.join(WSB_DATA, f"{label}__event.jsonl")
        if not os.path.exists(path):
            continue
        onset = dt.date.fromisoformat(onset_iso)
        plo, phi = onset - dt.timedelta(days=WSB_PRE_GRAPH_DAYS), onset
        olo, ohi = onset - dt.timedelta(days=3), onset + dt.timedelta(days=WSB_POST_DAYS + 1)
        pre_authors = set()
        pre_comments = 0
        on_comments = 0
        on_existing = 0
        on_rows = []  # (author) for onset window, second pass needs pre_authors first
        recs = []
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                r = json.loads(line)
                day = dt.datetime.fromtimestamp(int(r["t"]), dt.timezone.utc).date()
                recs.append((r["a"], day))
        for a, day in recs:
            if plo <= day < phi:
                pre_authors.add(a)
                pre_comments += 1
        for a, day in recs:
            if olo <= day < ohi:
                on_comments += 1
                if a in pre_authors:
                    on_existing += 1
        f_existing = on_existing / on_comments if on_comments else float("nan")
        on_days = (ohi - olo).days
        on_rate = on_comments / on_days
        pre_rate = pre_comments / WSB_PRE_GRAPH_DAYS
        a_abrupt = on_rate / pre_rate if pre_rate > 0 else float("inf")
        rows.append(dict(substrate="wsb", event=label,
                         f_existing=f_existing, a_abrupt=a_abrupt,
                         on_comments=on_comments, pre_comments=pre_comments))
    return rows


WSB_ONSETS = {
    "GME_squeeze_jan2021": "2021-01-25",
    "GME_leg2_feb2021": "2021-02-24",
    "AMC_meme_jun2021": "2021-06-02",
    "GME_runup_nov2021": "2021-11-02",
    "market_selloff_jan2022": "2022-01-24",
    "market_drop_may2022": "2022-05-09",
    "svb_collapse_mar2023": "2023-03-10",
    "regional_bank_may2023": "2023-05-01",
    "aug2024_vix_spike": "2024-08-05",
    "gme_kitty_may2024": "2024-05-13",
}


def structural_label(f_existing, a_abrupt):
    if f_existing >= SHARE_HI:
        return "B"
    if a_abrupt >= ABRUPT_HI:
        return "R"
    return "N"


# ----------------------------------------------------------------------------
# SUBSTANTIVE table (committed BEFORE the B-fraction is seen; blind to N_eff outcome)
# label -> (BNR, one-line rationale keyed only to the PUBLIC onset description)
# ----------------------------------------------------------------------------
SUBSTANTIVE = {
    # --- Wikipedia ---
    "Bitcoin": ("B", "Coinbase-IPO price peak culminating a multi-month reflexive bull run; slow control-parameter (price/leverage) drift toward a fold."),
    "Boeing 737 MAX": ("R", "Ethiopian Airlines crash and abrupt worldwide grounding; a sudden fatal accident, no slow public drift."),
    "Credit Suisse": ("B", "UBS emergency takeover ending a years-long, publicly tracked balance-sheet/confidence deterioration; slow build to a fold."),
    "Diego Maradona": ("R", "Sudden death; an unanticipated one-off external shock."),
    "Donald Trump": ("B", "Capitol storming after weeks of escalating contested-election mobilization; a slow-building reflexive crisis culminating."),
    "Evergrande Group": ("B", "Default crisis after months of visible liquidity deterioration and missed-payment warnings; textbook slow fold."),
    "Joe Biden": ("R", "Election called; a scheduled-but-discrete outcome resolving on a near-fixed date, treated as a sudden state switch."),
    "Kobe Bryant": ("R", "Helicopter-crash death; sudden unanticipated external shock."),
    "NATO": ("R", "Spike driven by the surprise Russian invasion of Ukraine; sudden exogenous shock."),
    "Notre-Dame de Paris": ("R", "Cathedral fire; one-off physical accident, no slow drift."),
    "Queen Elizabeth II": ("R", "Death; an anticipated-someday but discrete sudden event with no slow public control-parameter drift."),
    "Suez Canal": ("R", "Ever Given grounding blocking the canal; sudden physical accident."),
    "Twitter": ("R", "Musk acquisition CLOSE; a discrete deal-closing event (the drift was the months-long saga, but the onset spike is the sudden close)."),
    "Volodymyr Zelenskyy": ("R", "Spike on the surprise invasion; sudden exogenous shock to a wartime leader's profile."),
    # --- r/wallstreetbets ---
    "GME_squeeze_jan2021": ("B", "Canonical endogenous reflexive short squeeze built over weeks of coordinated WSB buying; the paradigm slow-fold social bubble."),
    "GME_leg2_feb2021": ("B", "Second GME leg, a reflexive re-inflation of the same endogenous bubble."),
    "AMC_meme_jun2021": ("B", "AMC/meme second wave, endogenous coordinated meme-stock bubble re-inflating."),
    "GME_runup_nov2021": ("B", "Late-2021 meme runup, endogenous reflexive coordination."),
    "market_selloff_jan2022": ("R", "Jan 2022 tech selloff driven by the exogenous rate-hike/Fed-pivot macro shock; sudden external trigger."),
    "market_drop_may2022": ("R", "Broad market drop with the LUNA/UST collapse; the LUNA leg is a fast death-spiral, the WSB surge is a reaction to an external crash."),
    "svb_collapse_mar2023": ("R", "SVB failed in a 48-hour bank run after a sudden deposit-flight trigger; rapid run, the WSB surge reacts to an abrupt external collapse."),
    "regional_bank_may2023": ("R", "First Republic / regional-bank crisis; reaction to a sudden external bank-failure shock."),
    "aug2024_vix_spike": ("R", "Aug 2024 carry-unwind VIX crash; a sudden one-day external volatility shock."),
    "gme_kitty_may2024": ("R", "Roaring Kitty's surprise return tweet; a single discrete exogenous trigger that reignited attention overnight."),
}


def cohens_kappa(labels_a, labels_b, cats):
    n = len(labels_a)
    if n == 0:
        return float("nan"), 0.0
    agree = sum(1 for a, b in zip(labels_a, labels_b) if a == b)
    po = agree / n
    pe = 0.0
    for c in cats:
        pa = sum(1 for x in labels_a if x == c) / n
        pb = sum(1 for x in labels_b if x == c) / n
        pe += pa * pb
    kappa = (po - pe) / (1 - pe) if (1 - pe) > 1e-12 else float("nan")
    return kappa, po


def main():
    struct = wiki_structural() + wsb_structural()
    for r in struct:
        r["structural"] = structural_label(r["f_existing"], r["a_abrupt"])
        sub = SUBSTANTIVE.get(r["event"])
        r["substantive"] = sub[0] if sub else None
        r["substantive_rationale"] = sub[1] if sub else None

    # Substantive over the FULL roster (24): include events with no structural feature too.
    structural_events = {r["event"] for r in struct}
    all_substantive = dict(SUBSTANTIVE)

    # ---- B-fractions ----
    struct_labels = [r["structural"] for r in struct]
    n_struct = len(struct_labels)
    b_struct = sum(1 for x in struct_labels if x == "B")
    bfrac_struct = b_struct / n_struct if n_struct else float("nan")

    sub_labels_all = [v[0] for v in all_substantive.values()]
    n_sub = len(sub_labels_all)
    b_sub = sum(1 for x in sub_labels_all if x == "B")
    bfrac_sub = b_sub / n_sub if n_sub else float("nan")

    # ---- inter-rater agreement on events classifiable by BOTH ----
    both = [r for r in struct if r["substantive"] is not None]
    a3 = [r["structural"] for r in both]
    b3 = [r["substantive"] for r in both]
    kappa3, po3 = cohens_kappa(a3, b3, ["B", "N", "R"])
    a2 = ["B" if x == "B" else "notB" for x in a3]
    b2 = ["B" if x == "B" else "notB" for x in b3]
    kappa2, po2 = cohens_kappa(a2, b2, ["B", "notB"])

    verdict_struct = "SUPPORTED" if bfrac_struct >= PI_B else "REFUTED"
    verdict_sub = "SUPPORTED" if bfrac_sub >= PI_B else "REFUTED"

    out = dict(
        test="iii_prime_bifurcation_mix",
        pi_B=PI_B,
        thresholds=dict(SHARE_HI=SHARE_HI, ABRUPT_HI=ABRUPT_HI),
        roster=dict(n_wiki_structural=sum(1 for r in struct if r["substrate"] == "wiki"),
                    n_wsb_structural=sum(1 for r in struct if r["substrate"] == "wsb"),
                    n_structural_total=n_struct,
                    n_substantive_total=n_sub),
        structural=dict(B=struct_labels.count("B"), N=struct_labels.count("N"),
                        R=struct_labels.count("R"), n=n_struct,
                        B_fraction=bfrac_struct, verdict=verdict_struct),
        substantive=dict(B=sub_labels_all.count("B"), N=sub_labels_all.count("N"),
                         R=sub_labels_all.count("R"), n=n_sub,
                         B_fraction=bfrac_sub, verdict=verdict_sub),
        inter_rater=dict(n_both=len(both),
                         raw_agreement_3cat=po3, cohens_kappa_3cat=kappa3,
                         raw_agreement_binaryB=po2, cohens_kappa_binaryB=kappa2),
        per_event=sorted(struct, key=lambda r: (r["substrate"], -(r["f_existing"]
                          if r["f_existing"] == r["f_existing"] else -1))),
    )
    json.dump(out, open(os.path.join(HERE, "result_bifurcation_mix.json"), "w"), indent=2)

    # ---- table ----
    lines = []
    lines.append("| substrate | event | f_existing | a_abrupt | STRUCTURAL | SUBSTANTIVE | agree |")
    lines.append("|---|---|---:|---:|:---:|:---:|:---:|")
    for r in out["per_event"]:
        fe = f"{r['f_existing']:.3f}" if r["f_existing"] == r["f_existing"] else "nan"
        ab = f"{r['a_abrupt']:.1f}" if r["a_abrupt"] not in (float("inf"),) else "inf"
        ag = "=" if r["structural"] == r["substantive"] else "x"
        lines.append(f"| {r['substrate']} | {r['event']} | {fe} | {ab} | "
                     f"{r['structural']} | {r['substantive']} | {ag} |")
    table = "\n".join(lines)
    open(os.path.join(HERE, "classification_table.md"), "w", encoding="utf-8").write(table + "\n")

    print(table)
    print()
    print(f"STRUCTURAL  B-fraction = {bfrac_struct:.3f}  "
          f"(B={struct_labels.count('B')} N={struct_labels.count('N')} "
          f"R={struct_labels.count('R')} / n={n_struct})  -> {verdict_struct}")
    print(f"SUBSTANTIVE B-fraction = {bfrac_sub:.3f}  "
          f"(B={sub_labels_all.count('B')} N={sub_labels_all.count('N')} "
          f"R={sub_labels_all.count('R')} / n={n_sub})  -> {verdict_sub}")
    print(f"Inter-rater (n_both={len(both)}): raw 3-cat={po3:.3f} kappa3={kappa3:.3f} | "
          f"raw binaryB={po2:.3f} kappaB={kappa2:.3f}")
    print(f"pi_B = {PI_B}")


if __name__ == "__main__":
    main()
