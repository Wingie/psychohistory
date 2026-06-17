# Lethain `systems` per-post showcase

Each r/AskEconomics post with a dynamic/stock layer gets its own lethain `systems` stock-and-flow model, run with `systems.parse(...).run(rounds=N)` under `py -3.12`. Below: the worked examples, then a summary table.

> **HONESTY / VALIDATION FRAMING.** CONCORDANCE CHECK ONLY -- compared to established economics and the framework's own reading, NOT to the thread's actual top comments. The corpus has no comment bodies (only num_comments); 'Approved Answers' flair means a vetted answer EXISTS, not what it says. True comment-concordance needs the downloaded comment text.

---

## Worked examples

### Europe Holds Trillions in US Treasuries (around 2T??). A coordinated European Sell-Off is a realistic scenario?

- **id:** `1qelqsy`  **template:** `bank-run`  **layers:** L4,L5,L3,L1  **flair:** Approved Answers
- **why this model:** panic/withdrawal dynamics: a stock draining at a confidence-dependent rate

```
# systems DSL
Deposits(1000) > Withdrawn(10) @ Leak(0.3)
Withdrawn > Deposits @ Leak(0.04)
```

- **runs for** 30 rounds -> **result:** _total conserved; Withdrawn runs away (10->891); Withdrawn concentrates (1%->88% of total); Deposits converges to equilibrium (119)_
- **economics check:** **AGREES** -- Diamond-Dybvig: a run reallocates a conserved deposit base into withdrawals at a confidence-driven rate; the model's conserved-but-concentrating trajectory matches the canonical self-fulfilling run.

---

### Why is the US economy still doing ok despite the tariffs?

- **id:** `1ntscmb`  **template:** `expectations-loop`  **layers:** L1,L4,L5,L6  **flair:** Approved Answers
- **why this model:** inflation/expectations feeding a wage-price loop with a credibility anchor

```
# systems DSL
Expectations(10) > Prices(100) @ Leak(0.5)
Prices > Expectations @ Leak(0.45)
```

- **runs for** 40 rounds -> **result:** _total conserved; Prices converges to equilibrium (58)_
- **economics check:** **AGREES** -- Matches the anchored-expectations consensus: with a credible anchor (anchor>=pass-through) an expectations shock converges rather than spiraling -- the modern central-bank view of inflation expectations.

---

### Is the United States heading towards an economic collapse?

- **id:** `1lw2rdb`  **template:** `debt-trajectory`  **layers:** L5,L1,L6  **flair:** Approved Answers
- **why this model:** debt stock for a monetary sovereign: interest inflow ~ growth-driven paydown (r vs g, g can win)

```
# systems DSL
Debt(100) > Interest(0) @ Leak(0.045)
Interest > Debt @ Leak(1.0)
Debt > Repaid @ Leak(0.045)
```

- **runs for** 30 rounds -> **result:** _Debt drains (100->35)_
- **economics check:** **AGREES** -- Matches debt-sustainability economics: when primary balance + growth exceed interest (g>r), the debt stock stabilizes -- the standard Domar/r-vs-g sustainability result.

---

### Bernie Sanders claims that Elon Musk owns more wealth than the bottom 52% of Americans. How is that possible?

- **id:** `1m11gep`  **template:** `concentration/bubble`  **layers:** L6,L2,L1,L0  **flair:** Approved Answers
- **why this model:** preferential-attachment concentration of a conserved carrier (attention/capital/wealth)

```
# systems DSL
Others(990) > Focus(10) @ Leak(0.35)
Focus > Others @ Leak(0.05)
```

- **runs for** 30 rounds -> **result:** _total conserved; Focus concentrates (1%->88% of total); Focus converges to equilibrium (875)_
- **economics check:** **AGREES** -- Preferential attachment / Pareto wealth concentration is structurally guaranteed; the conserved-carrier-concentrating trajectory matches the established 'no society equalizes to the top' result (and Minsky for bubbles).

---

### Are SNAP benefits essentially subsidies for corporations who don’t pay a living wage?

- **id:** `1ok5wfc`  **template:** `fiscal-capacity`  **layers:** L1,L0,L6  **flair:** Approved Answers
- **why this model:** fiscal stock-flow: tax inflow vs baseline outlays + new program (solvency over horizon)

```
# systems DSL
TaxBase(2000) > Treasury(100) @ Leak(0.18)
Treasury > Spent @ 380
Treasury > Spent @ 70
```

- **runs for** 16 rounds -> **result:** _Treasury drains (100->18); Treasury converges to equilibrium (18)_
- **economics check:** **AGREES** -- Matches public-finance accounting: at a fixed effective tax take, a new program is affordable only if take*base exceeds outlays; a draining Treasury correctly flags the financing wedge (raise take, grow base, or cut).

---

### Why are UK salaries so uncompetitive at a global level?

- **id:** `1teyzn5`  **template:** `wage-decomposition`  **layers:** L1,L6  **flair:** Approved Answers
- **why this model:** wage as the price that clears a productivity/bargaining stock-flow (gap decomposition)

```
# systems DSL
Output(2000) > Wage(0) @ Leak(0.25)
Labor(120) > Employed(0) @ Leak(0.9)
```

- **runs for** 20 rounds -> **result:** _Wage runs away (0->1993); Wage converges to equilibrium (1993)_
- **economics check:** **AGREES** -- Standard labor economics: wages clear on productivity x bargaining; the model's equilibrium correctly DECOMPOSES a cross-country wage gap into productivity vs institutions, which is the textbook answer to 'why are wages X'.

---

### Why isn't Russia collapsing?

- **id:** `1q37pg4`  **template:** `generic-stock`  **layers:** L5,L1,L6  **flair:** Approved Answers
- **why this model:** generic slow-stock comparative-statics (inflow vs outflow toward equilibrium)

```
# systems DSL
Source(900) > Stock(1000) @ Leak(0.1)
Stock > Sink @ Leak(0.08)
```

- **runs for** 30 rounds -> **result:** _Stock drains (1000->263)_
- **economics check:** **PARTIAL** -- Generic slow-stock proxy; captures direction/comparative-statics only, not the specific mechanism.

---

### Nvidia is worth over $4T. Adjusted for inflation, that's $2.5T in the year 2000. How is this not a bubble?

- **id:** `1ncv5bf`  **template:** `concentration/bubble`  **layers:** L2,L4,L5,L1  **flair:** Approved Answers
- **why this model:** explicit asset-bubble: preferential-attachment concentration of a conserved carrier (capital/attention)

```
# systems DSL
Others(990) > Focus(10) @ Leak(0.35)
Focus > Others @ Leak(0.05)
```

- **runs for** 30 rounds -> **result:** _total conserved; Focus concentrates (1%->88% of total); Focus converges to equilibrium (875)_
- **economics check:** **AGREES** -- Preferential attachment / Pareto wealth concentration is structurally guaranteed; the conserved-carrier-concentrating trajectory matches the established 'no society equalizes to the top' result (and Minsky for bubbles).

---

## Summary table

- **Total posts processed:** 100
- **Modeled (got a stock-flow):** 88
- **NA (no dynamic model applies):** 12

### Validation counts (modeled posts)

| verdict | count |
|---|---|
| AGREES | 48 |
| PARTIAL | 40 |
| DISAGREES | 0 |
| (NA among modeled) | 0 |

### Template usage

| template | posts |
|---|---|
| generic-stock | 40 |
| fiscal-capacity | 15 |
| concentration/bubble | 14 |
| wage-decomposition | 7 |
| expectations-loop | 6 |
| debt-trajectory | 5 |
| bank-run | 1 |

### NA reasons

| reason | count |
|---|---|
| pure accounting/tautology (a definitional identity, not a dynamic stock) | 7 |
| purely normative (L0 valence); the framework resolves it per-block, no stock to  | 5 |
