# L1 — Slow stocks (the lethain/`systems` layer)

The quiet macro core. L1 is the stock-and-flow accounting beneath every question: debt,
fiscal capacity, demographics, wages, firm/industry balance sheets. It is low-dimensional,
slow, and **reliable** — it answers comparative-statics and accounting questions and is
deliberately **silent on individuals**. It supplies the *source terms* (inflows) and the
*totals* (conserved boundaries) that the faster layers (L2 attention, L3 blocks, L5
criticality) ride on top of.

> Rule of thumb: if the honest answer is "flows at rate x with attrition y imply stock z
> in two quarters," you are in L1 and you should just *build the stock-flow and run it*.

---

## The tool: lethain's `systems`

```
pip install systems
```
```python
from systems.parse import parse
```

### The DSL

Each line is a flow between stocks:

```
Source(initial) > Sink @ Rate(value)
```

- `Source(initial)` declares a **stock** named `Source` with an initial level. Declare the
  initial level **once** (the first time the stock appears); later lines reference it bare.
- `>` is a directed **flow** from the left stock to the right stock.
- `@ Rate(value)` sets the per-round transfer. `Leak(0.35)` moves a *fraction* of the
  source each round (proportional / outflow-limited). A bare conversion like `@ 40` moves a
  fixed quantity per round.
- `model.run(rounds=N)` returns a **list of per-round dicts**, one dict per round, keyed by
  stock name: `[{"Source": ..., "Sink": ...}, ...]`.

**Conservation:** total is conserved **iff every flow stays inside the modeled boundary**.
A flow whose sink is a modeled stock conserves; a flow to an unmodeled sink (or a stock
with only outflows and no return) leaks mass out of the boundary. This is the L1 analogue
of attention conservation (L2) — make the boundary explicit and you know exactly what is
conserved.

---

## (a) Attention reallocation — total conserved (verified example, E1)

This is the exact block run and plotted as `E1_conservation_lethain.png`. A panic topic
("BankTopic") drains salience from everything else and partially returns it; the two stocks
exchange mass but the **total is conserved** because both sinks are modeled.

```python
from systems.parse import parse

model = parse("""OtherTopics(990) > BankTopic(10) @ Leak(0.35)
BankTopic > OtherTopics @ Leak(0.05)
""")
res = model.run(rounds=30)
ot  = [r["OtherTopics"] for r in res]
bt  = [r["BankTopic"]   for r in res]
tot = [a + b for a, b in zip(ot, bt)]
# tot is flat across all 30 rounds: max(tot) - min(tot) ~ 0  -> attention is conserved,
# panic only REALLOCATES it. BankTopic equilibrates where 0.35*OT == 0.05*BT.
```

Read-off: salience is a **conserved carrier**; the "bubble of attention" is concentration,
not creation. L1 gives you the equilibrium split and the relaxation time; the *belief drift*
that picks the winner is L2's job.

---

## (b) Fiscal stock-flow — "can country X afford Y?"

"Afford" is an accounting question: a revenue stock with a tax **inflow** and a spending
**outflow**, asked whether the stock stays solvent over the horizon.

```python
from systems.parse import parse

# Treasury starts at 100 (units: $bn). Tax base feeds revenue; revenue funds the
# baseline budget AND the proposed program Y. Boundary = {TaxBase, Treasury, Spent}.
fiscal = parse("""TaxBase(2000) > Treasury(100) @ Leak(0.18)   # ~18% effective tax take
Treasury > Spent @ 380                                          # baseline outlays / round
Treasury > Spent @ 60                                           # NEW program Y / round
""")
res = fiscal.run(rounds=12)
treasury = [r["Treasury"] for r in res]
# If `treasury` trends DOWN and crosses 0 inside the horizon -> Y is unaffordable at the
# current take; the deficit = (380+60) - 0.18*TaxBase_flow per round. To "afford Y" you must
# either raise the Leak (tax rate), grow TaxBase, or cut the 380 baseline. L1 tells you the
# exact wedge; it does NOT tell you whether voters will tolerate any of those (that is L0/L4).
```

The verdict L1 returns is a number and a sign: *surplus / deficit per round, and the round
at which the stock hits zero.* Comparative statics on `Leak` and `TaxBase` answer
"what would make Y affordable."

---

## (c) Labor / wage comparison — "why are wages higher in country A?"

Wages are the *price that clears a stock-flow*: a labor-demand inflow (output per worker ×
capital intensity) against a labor-supply stock. To compare A vs B, build the same two-stock
sketch with different parameters and read the divergence — do **not** narrate; instantiate.

```python
from systems.parse import parse

def wage_sketch(name, productivity, labor_supply, bargaining_leak):
    # Output pool fills from productivity; it is paid out to the Wage stock at a rate
    # set by labor scarcity * bargaining institutions. Higher productivity OR tighter
    # supply OR stronger bargaining -> larger Wage stock at equilibrium.
    m = parse(f"""Output({productivity}) > Wage(0) @ Leak({bargaining_leak})
Labor({labor_supply}) > Employed(0) @ Leak(0.9)
""")
    return m.run(rounds=20)[-1]["Wage"]

A = wage_sketch("A", productivity=2400, labor_supply=100, bargaining_leak=0.30)
B = wage_sketch("B", productivity=1500, labor_supply=140, bargaining_leak=0.18)
# Wage_A > Wage_B is DECOMPOSED into its causes: the gap attributable to productivity
# (2400 vs 1500), to labor scarcity (100 vs 140), and to bargaining institutions
# (0.30 vs 0.18). That decomposition is the whole answer L1 owes you.
```

L1's contribution is **the decomposition, not a point forecast**: it tells you which of
{productivity, supply, institutions} carries the gap. Which one *dominates* and whether it
is policy-movable is the L7 synthesis. (Numbers here are illustrative parameters; for a real
post, the magnitudes are an L6 data-acquisition job — go fetch productivity and
participation rates and cite them.)

---

## The L1 principle

- **Scope:** comparative statics and accounting. "Flows at rate x with attrition y imply
  stock z in N rounds." Solvency, affordability, deficit/surplus, the size and direction of
  a gap.
- **Reliable & low-dimensional:** few stocks, few rates, deterministic given parameters. No
  chaos, no horizon collapse — L1 has effectively an *infinite skill horizon* on its own
  variables (it is the slow manifold the fast layers perturb).
- **Silent on individuals:** L1 never says who panics or who gets the wage. It hands totals
  and source terms up to L2/L3/L4/L5.

---

## INSTITUTIONAL questions = "LLM'd and lethained"

Questions like *"why do military commissaries succeed where municipal groceries fail?"* are
**L1 + qualitative incentive reasoning**. Neither half alone suffices:

1. **Lethain it** — build a compact stock-flow comparison of the two institutions over the
   same boundary so the structural asymmetry is *quantitative*, not asserted.
2. **LLM it** — reason qualitatively over the incentive structure the stocks can't encode
   (procurement governance, soft-budget constraint, who bears the loss, demand elasticity).
3. The **synthesis is a Prime-Radiant (L7) job** — combine the two into one verdict and a
   falsifier.

### Commissary vs municipal grocery — stock-flow sketch

```python
from systems.parse import parse

def store(name, subsidy, captive_demand, scale_econ_cost, procurement_cost):
    # Cash stock fed by (subsidy inflow + sales from captive demand), drained by
    # (cost of goods at the procurement price) and (operating cost scaled by store size).
    m = parse(f"""Subsidy({subsidy}) > Cash(50) @ Leak(0.9)
Demand({captive_demand}) > Cash @ Leak(0.8)
Cash > COGS @ {procurement_cost}
Cash > Opex @ {scale_econ_cost}
""")
    res = m.run(rounds=24)
    return res[-1]["Cash"]

commissary = store("commissary",
    subsidy=120,            # appropriated subsidy inflow (taxpayer-funded)
    captive_demand=200,     # base members MUST shop here -> demand is inelastic & predictable
    scale_econ_cost=70,     # buys through DeCA central procurement -> low per-unit opex
    procurement_cost=90)    # bulk military procurement -> low COGS

municipal = store("municipal",
    subsidy=0,              # no structural subsidy (or politically capped)
    captive_demand=60,      # voluntary demand, competes with private grocers -> elastic
    scale_econ_cost=110,    # sub-scale single store -> high per-unit opex
    procurement_cost=130)   # no buying power -> pays near-retail wholesale

# commissary Cash stays positive (subsidy + captive demand + procurement scale all push in);
# municipal Cash trends negative (no subsidy, elastic demand, sub-scale, weak procurement).
```

The stock-flow makes the four structural levers explicit: **subsidy inflow, captive
(inelastic) demand, scale economies in opex, procurement cost**. The qualitative LLM layer
adds what the stocks omit: the commissary runs on a *captive customer base and a
soft-budget constraint* (loss absorbed by appropriation, not closure), while a municipal
grocery faces a *hard budget constraint and elastic, contestable demand*. Synthesis (L7):
the commissary "succeeds" because it is **not solving the same problem** — it is a subsidized
benefit with guaranteed demand, not a competitive retailer. Falsifier: remove the subsidy or
the captive base and its Cash stock collapses to the municipal trajectory.

This pattern — *small stock-flow for the conservable/accountable part, qualitative reasoning
for the incentive part, L7 to fuse them* — is the canonical "LLM'd and lethained" move and
recurs for every institutional-design question.

---

## HOW THE SKILL USES THIS LAYER

- [ ] **Trigger:** cue words `afford, wages, fiscal, GDP, cost, budget, deficit, revenue`,
      or any accounting / comparative-statics / "can X afford Y" / institutional-success
      question.
- [ ] **Build, don't narrate:** instantiate a `systems.parse` model — stocks for levels,
      `> @ Leak(r)` for proportional flows, `> @ k` for fixed flows. Run `model.run(rounds=N)`.
- [ ] **Make the boundary explicit** so you know what is conserved vs what leaks out; report
      conservation as a check (E1: total flat → conserved).
- [ ] **Read off the verdict as a number + sign:** surplus/deficit per round, the round the
      stock hits zero, the decomposition of a gap across parameters.
- [ ] **Hand up source terms & totals** to L2 (attention totals), L3 (block populations),
      L5 (the slow stock whose drift sets a bifurcation). L1 is the slow manifold.
- [ ] **If a magnitude is unknown** (a real tax rate, productivity figure, debt level),
      mark it and route to **L6 data-acquisition**; do not invent it. Scope = NEEDS-DATA
      until fetched.
- [ ] **Institutional questions:** pair the stock-flow with qualitative incentive reasoning
      ("LLM'd and lethained") and defer the fusion to **L7**.
- [ ] **Honesty:** L1 is reliable but **silent on individuals and on timing of fast events**.
      Never let an L1 stock-flow masquerade as a forecast of a panic, a crash, or a vote —
      those live on L4/L5.
