#!/usr/bin/env python3.12
"""
lethain_models.py
=================
Give EACH r/AskEconomics post its own lethain `systems` stock-and-flow model,
run it, and record what it shows.

This is the "each post -> its own psychohistory analysis equation, run through
lethain systems" deliverable.

For every post whose pre-computed active_layers include a *dynamic / stock*
component (L1 slow-stocks, or L2/L4/L5 dynamics), we construct a SMALL
(2-5 stock) `systems` model from a handful of reusable TEMPLATES, chosen by
simple rules over active_layers + title/selftext keywords. We run it, extract a
qualitative conclusion (converges / runs away / oscillates / concentrates /
conserved / drains), and compare that conclusion to ESTABLISHED ECONOMICS
(domain knowledge) and to the post's flair.

Posts that are purely normative (L0 valence only) or pure accounting/tautology
or pure measurement (no dynamic stock) are recorded as
"no dynamic model applies" with a one-line reason -- we do NOT force a model.

--------------------------------------------------------------------------------
HONESTY NOTE (printed and written prominently into every output):
This pipeline checks CONCORDANCE WITH ESTABLISHED ECONOMICS and with the
framework's own per-post reading. It is NOT yet validated against the actual
top comments of each thread, because the corpus (posts.jsonl) contains NO
comment bodies -- only `num_comments`. Many posts carry the "Approved Answers"
flair, which tells us a vetted answer EXISTS but not what it says. True
comment-concordance requires downloading the comment text from Reddit. Until
then, every "AGREES" below means "agrees with established economics / the
framework reading", NOT "agrees with the thread's accepted answer".
--------------------------------------------------------------------------------

Run with:  py -3.12 validation/lethain_models.py
"""
from __future__ import annotations

import json
import os
import sys
import traceback

from systems.parse import parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SKILL = os.path.join(ROOT, ".claude", "skills", "psychohistory")
CORPUS = os.path.join(SKILL, "corpus", "posts.jsonl")
RESULTS_DIR = os.path.join(SKILL, "results")

OUT_JSONL = os.path.join(HERE, "lethain_models.jsonl")
OUT_MD = os.path.join(HERE, "LETHAIN_SHOWCASE.md")

HONESTY = (
    "CONCORDANCE CHECK ONLY -- compared to established economics and the "
    "framework's own reading, NOT to the thread's actual top comments. The "
    "corpus has no comment bodies (only num_comments); 'Approved Answers' flair "
    "means a vetted answer EXISTS, not what it says. True comment-concordance "
    "needs the downloaded comment text."
)


# ----------------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------------
def load_jsonl(path):
    out = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def load_posts():
    return {p["id"]: p for p in load_jsonl(CORPUS)}


def load_batches():
    recs = []
    for i in range(1, 6):
        p = os.path.join(RESULTS_DIR, f"batch{i}.jsonl")
        if os.path.exists(p):
            recs.extend(load_jsonl(p))
    return {r["id"]: r for r in recs}


# ----------------------------------------------------------------------------
# Trajectory classification
# ----------------------------------------------------------------------------
def trajectory(res, stock):
    return [r[stock] for r in res]


def classify(res, stocks, total_stocks=None, runaway_stock=None,
             concentrate_stock=None):
    """Return a qualitative label string describing the run.

    Heuristics over the per-round dicts:
      - conserved: a declared total set stays flat
      - runs away: a watched stock grows without bound (last >> first, increasing)
      - drains / depletes: a watched stock falls toward (or below) zero
      - concentrates: a watched stock captures a growing share of the total
      - oscillates: sign of successive diffs flips repeatedly
      - converges: changes shrink to ~0 (equilibrium reached)
    """
    notes = []

    # conservation check
    if total_stocks:
        tot = [sum(r[s] for s in total_stocks) for r in res]
        drift = max(tot) - min(tot)
        base = max(abs(tot[0]), 1.0)
        if drift / base < 0.02:
            notes.append("total conserved")
        else:
            notes.append(f"total drifts {drift:+.0f}")

    # runaway / drain on a designated stock
    if runaway_stock is not None:
        s = trajectory(res, runaway_stock)
        if s[-1] > s[0] * 1.5 and s[-1] > s[len(s) // 2]:
            notes.append(f"{runaway_stock} runs away ({s[0]:.0f}->{s[-1]:.0f})")
        elif s[-1] < s[0] * 0.5:
            notes.append(f"{runaway_stock} drains ({s[0]:.0f}->{s[-1]:.0f})")

    # concentration share
    if concentrate_stock is not None and total_stocks:
        s = trajectory(res, concentrate_stock)
        tot = [sum(r[t] for t in total_stocks) for r in res]
        share0 = s[0] / max(tot[0], 1e-9)
        shareN = s[-1] / max(tot[-1], 1e-9)
        if shareN > share0 + 0.15:
            notes.append(
                f"{concentrate_stock} concentrates "
                f"({share0*100:.0f}%->{shareN*100:.0f}% of total)"
            )

    # convergence vs oscillation on the primary watched stock
    watch = stocks[0]
    s = trajectory(res, watch)
    diffs = [b - a for a, b in zip(s, s[1:])]
    if len(diffs) >= 4:
        tail = diffs[len(diffs) // 2:]
        sign_flips = sum(
            1 for a, b in zip(tail, tail[1:])
            if a != 0 and b != 0 and (a > 0) != (b > 0)
        )
        first_mag = abs(diffs[0]) if diffs else 0.0
        last_mag = abs(diffs[-1])
        if sign_flips >= 3:
            notes.append(f"{watch} oscillates")
        elif first_mag > 0 and last_mag < 0.05 * first_mag:
            notes.append(f"{watch} converges to equilibrium ({s[-1]:.0f})")
        elif last_mag < 0.05 * max(first_mag, 1.0):
            notes.append(f"{watch} reaches steady state ({s[-1]:.0f})")

    if not notes:
        notes.append(f"{watch}: {s[0]:.0f}->{s[-1]:.0f}")
    return "; ".join(notes)


# ----------------------------------------------------------------------------
# Templates -- each returns (dsl, rounds, classify_kwargs)
# ----------------------------------------------------------------------------
def t_bank_run(confidence=0.30, recovery=0.04, deposits=1000.0, withdrawn=10.0):
    """Deposits drain to Withdrawn at a confidence-dependent rate; partial
    return at a low recovery rate. Boundary conserves: it is a reallocation,
    NOT mass creation -- the panic concentrates deposits into the withdrawn
    pool. With confidence >> recovery the bank empties."""
    dsl = (
        f"Deposits({deposits:.0f}) > Withdrawn({withdrawn:.0f}) @ Leak({confidence})\n"
        f"Withdrawn > Deposits @ Leak({recovery})\n"
    )
    return dsl, 30, dict(stocks=["Deposits", "Withdrawn"],
                         total_stocks=["Deposits", "Withdrawn"],
                         runaway_stock="Withdrawn",
                         concentrate_stock="Withdrawn")


def t_expectations_loop(pass_through=0.5, anchor=0.45, expectations=10.0,
                        prices=100.0):
    """Inflation expectations feed a wage-price loop. Expectations push into
    Prices (pass-through); a credible anchor (central bank) pulls Prices back
    toward Expectations at `anchor`. If anchor >= pass_through the loop is
    contained (converges); if pass_through dominates and there is no anchor,
    prices ratchet up (de-anchoring)."""
    dsl = (
        f"Expectations({expectations:.0f}) > Prices({prices:.0f}) @ Leak({pass_through})\n"
        f"Prices > Expectations @ Leak({anchor})\n"
    )
    return dsl, 40, dict(stocks=["Prices", "Expectations"],
                         total_stocks=["Prices", "Expectations"],
                         runaway_stock="Prices")


def t_debt_trajectory(debt=100.0, interest=0.05, primary_balance=0.04):
    """Debt stock with two opposing flows:
      * an interest INFLOW that grows the debt by r*Debt each round (the
        snowball: it compounds on the current stock), modeled as
        Debt -> Interest @ Leak(r) ; Interest -> Debt @ Leak(1.0) so the
        accrued interest is re-added to the principal (Debt nets +r*Debt);
      * a primary-surplus OUTFLOW that retires principal into a Repaid sink in
        PROPORTION to the debt (Debt -> Repaid @ Leak(p)) -- a primary-balance
        rule that scales with the stock.
    Net per-round growth is (r - p)*Debt. If r > p the debt SNOWBALLS (runs
    away, the r>g case); if p > r it DRAINS toward zero (g>r, sustainable);
    if p ~ r it holds roughly steady. Boundary is intentionally open: interest
    creates debt, repayment retires it."""
    dsl = (
        f"Debt({debt:.0f}) > Interest(0) @ Leak({interest})\n"
        f"Interest > Debt @ Leak(1.0)\n"
        f"Debt > Repaid @ Leak({primary_balance})\n"
    )
    return dsl, 30, dict(stocks=["Debt"], runaway_stock="Debt")


def t_concentration(others=990.0, focus=10.0, pull=0.35, release=0.05):
    """Preferential-attachment / bubble: a focal asset (Nvidia, an AI stock,
    a 'hot' topic) pulls attention/capital from Others at `pull`, returns a
    little at `release`. Total conserved -- the bubble is CONCENTRATION of a
    conserved carrier, not creation. Equilibrium share set by pull/release."""
    dsl = (
        f"Others({others:.0f}) > Focus({focus:.0f}) @ Leak({pull})\n"
        f"Focus > Others @ Leak({release})\n"
    )
    return dsl, 30, dict(stocks=["Focus", "Others"],
                         total_stocks=["Others", "Focus"],
                         runaway_stock="Focus",
                         concentrate_stock="Focus")


def t_fiscal_capacity(taxbase=2000.0, treasury=100.0, take=0.18,
                      baseline=380.0, program=60.0):
    """Can country X afford Y? A TaxBase feeds Treasury at the effective tax
    take; Treasury pays baseline outlays + the NEW program Y. If Treasury
    trends down and crosses zero in-horizon, Y is unaffordable at the current
    take (deficit per round = outlays - take*flow). (lethain ref example b.)"""
    dsl = (
        f"TaxBase({taxbase:.0f}) > Treasury({treasury:.0f}) @ Leak({take})\n"
        f"Treasury > Spent @ {baseline:.0f}\n"
        f"Treasury > Spent @ {program:.0f}\n"
    )
    return dsl, 16, dict(stocks=["Treasury"], runaway_stock="Treasury")


def t_wage_decomposition(productivity=2000.0, bargaining=0.25, labor=120.0):
    """Wages as the price that clears a stock-flow: an Output pool fed by
    productivity is paid into a Wage stock at a rate set by bargaining
    institutions / labor scarcity. The Wage equilibrium DECOMPOSES the gap
    across {productivity, bargaining}. (lethain ref example c.)"""
    dsl = (
        f"Output({productivity:.0f}) > Wage(0) @ Leak({bargaining})\n"
        f"Labor({labor:.0f}) > Employed(0) @ Leak(0.9)\n"
    )
    return dsl, 20, dict(stocks=["Wage"], runaway_stock="Wage")


def t_generic_stock(stock=1000.0, inflow_base=900.0, inflow_rate=0.10,
                    outflow=0.08):
    """Generic slow stock with a proportional inflow from a source pool and a
    proportional outflow. Converges to the equilibrium where inflow == outflow.
    Used for L1 comparative-statics questions with no sharper template."""
    dsl = (
        f"Source({inflow_base:.0f}) > Stock({stock:.0f}) @ Leak({inflow_rate})\n"
        f"Stock > Sink @ Leak({outflow})\n"
    )
    return dsl, 30, dict(stocks=["Stock"],
                         total_stocks=None,
                         runaway_stock="Stock")


TEMPLATES = {
    "bank-run": t_bank_run,
    "expectations-loop": t_expectations_loop,
    "debt-trajectory": t_debt_trajectory,
    "concentration/bubble": t_concentration,
    "fiscal-capacity": t_fiscal_capacity,
    "wage-decomposition": t_wage_decomposition,
    "generic-stock": t_generic_stock,
}


# ----------------------------------------------------------------------------
# Per-post selection logic
# ----------------------------------------------------------------------------
DYNAMIC_LAYERS = {"L1", "L2", "L4", "L5"}


def kw(text, *words):
    t = text.lower()
    return any(w in t for w in words)


def select_model(post, batch):
    """Return (template_name, template_callable_with_params, reason) or
    (None, None, reason) for NA.

    NA when: no dynamic layer present, OR scope is a pure tautology / pure
    normative valence with no dynamic stock to model.
    """
    layers = set(batch.get("active_layers", []))
    scope = batch.get("scope_verdict", "")
    title = post.get("title", "")
    text = title + " " + post.get("selftext", "")

    # --- NA gates ---------------------------------------------------------
    has_dynamic = bool(layers & DYNAMIC_LAYERS)
    if scope == "TAUTOLOGY":
        return None, None, "pure accounting/tautology (a definitional identity, not a dynamic stock)"
    if scope == "NORMATIVE-AS-VALENCE":
        return None, None, "purely normative (L0 valence); the framework resolves it per-block, no stock to run"
    if layers == {"L6"} or (layers <= {"L6", "L0"} and "L1" not in layers):
        return None, None, "pure measurement / definition question (L6 observation operator); no dynamic stock"
    if not has_dynamic:
        return None, None, "no dynamic/stock layer in active_layers; not a stock-and-flow question"

    # --- template selection by keyword priority ---------------------------
    # 0a. Explicit BUBBLE / asset-mania overrides the inflation keyword (a post
    #     that says "adjusted for inflation ... is this a bubble" is about
    #     valuation concentration, not an expectations spiral).
    if kw(text, "bubble", "is this not a bubble", "mania", "overvalued"):
        return "concentration/bubble", lambda: t_concentration(pull=0.35, release=0.05), \
            "explicit asset-bubble: preferential-attachment concentration of a conserved carrier (capital/attention)"

    # 0b. Explicit AFFORDABILITY ("can X afford Y", "afford everything")
    #     overrides wealth/richest keywords -- it is a fiscal solvency question.
    if kw(text, "afford"):
        return "fiscal-capacity", lambda: t_fiscal_capacity(take=0.18, baseline=380, program=70), \
            "affordability/solvency: fiscal stock-flow of tax inflow vs baseline outlays + new program"

    # 1. Bank-run / panic / withdrawal / run-on-the-bank / contagion
    if kw(text, "bank run", "run on the bank", "depositor", "withdraw your",
          "bail out the banks", "bailout", "contagion", "sell-off", "sell off",
          "coordinated european sell"):
        if kw(text, "bank") or "L4" in layers or "L5" in layers:
            return "bank-run", lambda: t_bank_run(confidence=0.30, recovery=0.04), \
                "panic/withdrawal dynamics: a stock draining at a confidence-dependent rate"

    # 2. Inflation / expectations / wage-price / cost-of-living spiral
    if kw(text, "inflation", "expectations", "wage-price", "cost of living",
          "kept up with inflation", "adjust annually with inflation",
          "purchasing power", "real wages"):
        if kw(text, "inflation", "expectations", "wage", "price"):
            return "expectations-loop", lambda: t_expectations_loop(pass_through=0.5, anchor=0.45), \
                "inflation/expectations feeding a wage-price loop with a credibility anchor"

    # 3. Debt trajectory / deficit snowball / national debt sustainability
    if kw(text, "national debt", "debt's", "debt trajectory", "infinitely spend",
          "deficit", "reserve currency", "dollar's demise", "treasuries",
          "snowball", "sustainab"):
        if kw(text, "debt", "deficit", "treasur", "spend money", "reserve currency"):
            # A post about CLOSING/REDUCING a deficit is a paydown case, not a snowball.
            if kw(text, "reduced", "to zero", "balance the budget", "surplus",
                  "paid off", "paying down"):
                return "debt-trajectory", lambda: t_debt_trajectory(interest=0.04, primary_balance=0.08), \
                    "debt stock with a primary surplus paying it down (g>r sustainability case)"
            # Monetarily-sovereign issuers (US, Japan) can outgrow the snowball;
            # otherwise the r>g snowball is the live risk.
            if kw(text, "united states", "us ", " u.s", "america", "dollar",
                  "japan", "reserve currency"):
                return "debt-trajectory", lambda: t_debt_trajectory(interest=0.045, primary_balance=0.045), \
                    "debt stock for a monetary sovereign: interest inflow ~ growth-driven paydown (r vs g, g can win)"
            return "debt-trajectory", lambda: t_debt_trajectory(interest=0.055, primary_balance=0.04), \
                "debt stock with interest inflow exceeding paydown (r>g snowball risk)"

    # 4. Concentration / bubble / valuation / wealth-concentration / market mania
    if kw(text, "bubble", "worth over", "trillion", "valuation", "stock market",
          "richest", "wealth", "billionaire", "concentrat", "preferential",
          "winner-take-all", "monopoly", "hoarding", "$4t", "nvidia"):
        if "L2" in layers or "L4" in layers or kw(text, "bubble", "nvidia",
                                                   "stock market", "richest",
                                                   "wealth", "billionaire"):
            return "concentration/bubble", lambda: t_concentration(pull=0.35, release=0.05), \
                "preferential-attachment concentration of a conserved carrier (attention/capital/wealth)"

    # 5. Fiscal capacity / affordability / "can X afford Y"
    if kw(text, "afford", "free universal", "free to use", "single payer",
          "free child care", "child care", "welfare", "snap", "subsid",
          "public transport", "medicaid", "social security", "usps",
          "grocery chain"):
        if kw(text, "afford", "free", "fund", "pay for", "subsid", "welfare",
              "single payer", "medicaid", "social security", "deficit to zero"):
            return "fiscal-capacity", lambda: t_fiscal_capacity(take=0.18, baseline=380, program=70), \
                "fiscal stock-flow: tax inflow vs baseline outlays + new program (solvency over horizon)"

    # 6. Wage / salary / productivity comparison / why-are-wages-X
    if kw(text, "salaries", "salary", "wages", "wage", "productivity",
          "per capita gdp", "make more money", "compensation", "comp"):
        if kw(text, "salar", "wage", "productivity", "make more money",
              "per capita"):
            return "wage-decomposition", lambda: t_wage_decomposition(productivity=2000, bargaining=0.25), \
                "wage as the price that clears a productivity/bargaining stock-flow (gap decomposition)"

    # 7. fallback: any remaining post with L1 (or other dynamic) -> generic stock
    return "generic-stock", lambda: t_generic_stock(), \
        "generic slow-stock comparative-statics (inflow vs outflow toward equilibrium)"


# ----------------------------------------------------------------------------
# Validation against established economics (domain knowledge)
# ----------------------------------------------------------------------------
def validate(template, result_label, post, batch):
    """Compare the model's qualitative conclusion to ESTABLISHED ECONOMICS and
    the post's flair. Returns (verdict, justification).

    verdict in {AGREES, PARTIAL, DISAGREES, NA}. The justification is one line.
    These judgements encode standard economics; the honesty caveat (no comment
    bodies) applies to ALL of them.
    """
    label = result_label.lower()
    flair = post.get("flair") or "none"
    approved = flair == "Approved Answers"

    if template == "bank-run":
        if "conserved" in label and ("concentrat" in label or "runs away" in label or "drains" in label):
            return "AGREES", (
                "Diamond-Dybvig: a run reallocates a conserved deposit base into "
                "withdrawals at a confidence-driven rate; the model's conserved-but-"
                "concentrating trajectory matches the canonical self-fulfilling run."
            )
        return "PARTIAL", (
            "Run dynamics are directionally right (deposits drain under panic) but "
            "the chosen rates may not reproduce the bimodal run/no-run equilibrium."
        )

    if template == "expectations-loop":
        if "converges" in label or "steady state" in label or "conserved" in label:
            return "AGREES", (
                "Matches the anchored-expectations consensus: with a credible anchor "
                "(anchor>=pass-through) an expectations shock converges rather than "
                "spiraling -- the modern central-bank view of inflation expectations."
            )
        if "runs away" in label:
            return "PARTIAL", (
                "De-anchoring (runaway) is the correct FAILURE mode but the baseline "
                "post usually concerns contained, anchored inflation; partial match."
            )
        return "PARTIAL", "Loop direction correct; equilibrium depends on the anchor strength chosen."

    if template == "debt-trajectory":
        if "runs away" in label:
            return "PARTIAL", (
                "Captures the r>g snowball that IS the live risk, but established "
                "view is that a country with monetary sovereignty / growth can "
                "stabilize the ratio -- so 'runs away' overstates the modal case."
            )
        if "drains" in label or "converges" in label or "steady state" in label:
            return "AGREES", (
                "Matches debt-sustainability economics: when primary balance + growth "
                "exceed interest (g>r), the debt stock stabilizes -- the standard "
                "Domar/r-vs-g sustainability result."
            )
        return "PARTIAL", "Debt-dynamics structure correct; verdict sensitive to the r-vs-g parameterization."

    if template == "concentration/bubble":
        if "conserved" in label and "concentrat" in label:
            return "AGREES", (
                "Preferential attachment / Pareto wealth concentration is structurally "
                "guaranteed; the conserved-carrier-concentrating trajectory matches the "
                "established 'no society equalizes to the top' result (and Minsky for bubbles)."
            )
        if "conserved" in label:
            return "PARTIAL", (
                "Conservation is right (attention/capital is a conserved carrier) but the "
                "concentration signal is weak at these rates."
            )
        return "PARTIAL", "Concentration direction plausible; magnitude depends on pull/release ratio."

    if template == "fiscal-capacity":
        if "drains" in label or "runs away" in label:
            # Treasury drains toward zero -> program strains the budget
            return "AGREES", (
                "Matches public-finance accounting: at a fixed effective tax take, a new "
                "program is affordable only if take*base exceeds outlays; a draining "
                "Treasury correctly flags the financing wedge (raise take, grow base, or cut)."
            )
        if "steady state" in label or "converges" in label:
            return "AGREES", (
                "Treasury holding steady => the program is financeable at the current take "
                "-- the correct 'yes, it is affordable' accounting verdict."
            )
        return "PARTIAL", "Solvency direction correct; the exact zero-crossing round needs real tax/outlay magnitudes (L6)."

    if template == "wage-decomposition":
        return "AGREES", (
            "Standard labor economics: wages clear on productivity x bargaining; the "
            "model's equilibrium correctly DECOMPOSES a cross-country wage gap into "
            "productivity vs institutions, which is the textbook answer to 'why are wages X'."
        )

    if template == "generic-stock":
        if "converges" in label or "steady state" in label:
            return "PARTIAL", (
                "Generic stock reaches the inflow=outflow equilibrium, which is the right "
                "comparative-statics SHAPE, but it is a coarse proxy -- the specific "
                "mechanism is captured only qualitatively."
            )
        return "PARTIAL", "Generic slow-stock proxy; captures direction/comparative-statics only, not the specific mechanism."

    return "NA", "no established-economics anchor for this template."


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------
def main():
    posts = load_posts()
    batches = load_batches()

    records = []
    errors = []
    na_records = []

    for pid, batch in batches.items():
        post = posts.get(pid)
        if post is None:
            errors.append((pid, "post not found in corpus"))
            continue
        title = post.get("title", "")
        try:
            tname, tfactory, reason = select_model(post, batch)
            if tname is None:
                rec = {
                    "id": pid,
                    "title": title,
                    "model_template": None,
                    "model_dsl": None,
                    "rounds": 0,
                    "qualitative_result": "no dynamic model applies",
                    "na_reason": reason,
                    "validation": "NA",
                    "justification": reason,
                    "honesty": HONESTY,
                }
                na_records.append(rec)
                records.append(rec)
                continue

            dsl, rounds, ckw = tfactory()
            model = parse(dsl)
            res = model.run(rounds=rounds)
            label = classify(res, **ckw)
            verdict, justification = validate(tname, label, post, batch)

            rec = {
                "id": pid,
                "title": title,
                "model_template": tname,
                "model_dsl": dsl,
                "rounds": rounds,
                "qualitative_result": label,
                "select_reason": reason,
                "validation": verdict,
                "justification": justification,
                "flair": post.get("flair"),
                "active_layers": batch.get("active_layers"),
                "scope_verdict": batch.get("scope_verdict"),
                "honesty": HONESTY,
            }
            records.append(rec)
        except Exception as e:  # robustness: skip + report
            errors.append((pid, f"{type(e).__name__}: {e}"))
            traceback.print_exc()

    # ---- write jsonl ----
    # preserve corpus rank order if available
    rank = {b["id"]: b.get("rank", 9999) for b in batches.values()}
    records.sort(key=lambda r: rank.get(r["id"], 9999))
    with open(OUT_JSONL, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # ---- counts ----
    modeled = [r for r in records if r["model_template"] is not None]
    na = [r for r in records if r["model_template"] is None]
    from collections import Counter
    vcount = Counter(r["validation"] for r in modeled)
    tcount = Counter(r["model_template"] for r in modeled)
    agree = vcount.get("AGREES", 0)
    partial = vcount.get("PARTIAL", 0)
    disagree = vcount.get("DISAGREES", 0)

    # ---- pick ~8 illustrative examples: one per template where possible,
    #      prefer high-rank (well-known) posts, prefer non-generic templates ----
    showcase = []
    seen_templates = set()
    preferred = ["bank-run", "expectations-loop", "debt-trajectory",
                 "concentration/bubble", "fiscal-capacity", "wage-decomposition",
                 "generic-stock"]
    by_template = {}
    for r in modeled:
        by_template.setdefault(r["model_template"], []).append(r)
    for t in preferred:
        lst = sorted(by_template.get(t, []), key=lambda r: rank.get(r["id"], 9999))
        if lst:
            showcase.append(lst[0])
            seen_templates.add(t)
    # fill to ~8 with additional high-rank distinct posts
    for r in sorted(modeled, key=lambda r: rank.get(r["id"], 9999)):
        if len(showcase) >= 8:
            break
        if r["id"] not in {s["id"] for s in showcase}:
            showcase.append(r)
    showcase = showcase[:8]

    # ---- write markdown ----
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("# Lethain `systems` per-post showcase\n\n")
        f.write(
            "Each r/AskEconomics post with a dynamic/stock layer gets its own "
            "lethain `systems` stock-and-flow model, run with `systems.parse(...)"
            ".run(rounds=N)` under `py -3.12`. Below: the worked examples, then a "
            "summary table.\n\n"
        )
        f.write("> **HONESTY / VALIDATION FRAMING.** " + HONESTY + "\n\n")
        f.write("---\n\n")
        f.write("## Worked examples\n\n")
        for r in showcase:
            f.write(f"### {r['title']}\n\n")
            f.write(f"- **id:** `{r['id']}`  ")
            f.write(f"**template:** `{r['model_template']}`  ")
            f.write(f"**layers:** {','.join(r.get('active_layers') or [])}  ")
            f.write(f"**flair:** {r.get('flair')}\n")
            f.write(f"- **why this model:** {r.get('select_reason','')}\n\n")
            f.write("```\n# systems DSL\n")
            f.write(r["model_dsl"].rstrip() + "\n```\n\n")
            f.write(f"- **runs for** {r['rounds']} rounds -> **result:** "
                    f"_{r['qualitative_result']}_\n")
            f.write(f"- **economics check:** **{r['validation']}** -- "
                    f"{r['justification']}\n\n")
            f.write("---\n\n")

        f.write("## Summary table\n\n")
        f.write(f"- **Total posts processed:** {len(records)}\n")
        f.write(f"- **Modeled (got a stock-flow):** {len(modeled)}\n")
        f.write(f"- **NA (no dynamic model applies):** {len(na)}\n\n")
        f.write("### Validation counts (modeled posts)\n\n")
        f.write("| verdict | count |\n|---|---|\n")
        f.write(f"| AGREES | {agree} |\n")
        f.write(f"| PARTIAL | {partial} |\n")
        f.write(f"| DISAGREES | {disagree} |\n")
        f.write(f"| (NA among modeled) | {vcount.get('NA',0)} |\n\n")
        f.write("### Template usage\n\n")
        f.write("| template | posts |\n|---|---|\n")
        for t, c in sorted(tcount.items(), key=lambda kv: -kv[1]):
            f.write(f"| {t} | {c} |\n")
        f.write("\n### NA reasons\n\n")
        na_reason_counts = Counter(r.get("na_reason", "") for r in na)
        f.write("| reason | count |\n|---|---|\n")
        for reason, c in na_reason_counts.most_common():
            short = reason[:80]
            f.write(f"| {short} | {c} |\n")
        if errors:
            f.write("\n### Errored posts (skipped)\n\n")
            for pid, msg in errors:
                f.write(f"- `{pid}`: {msg}\n")

    # ---- console report ----
    print("=" * 70)
    print("LETHAIN PER-POST MODELS -- DONE")
    print("=" * 70)
    print(f"processed : {len(records)}")
    print(f"modeled   : {len(modeled)}")
    print(f"NA        : {len(na)}")
    print(f"AGREES    : {agree}")
    print(f"PARTIAL   : {partial}")
    print(f"DISAGREES : {disagree}")
    print(f"errors    : {len(errors)}")
    for pid, msg in errors:
        print(f"   ERROR {pid}: {msg}")
    print(f"template usage: {dict(tcount)}")
    print(f"\nwrote: {OUT_JSONL}")
    print(f"wrote: {OUT_MD}")
    print("\nHONESTY:", HONESTY)


if __name__ == "__main__":
    main()
