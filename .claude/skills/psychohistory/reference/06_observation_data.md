# L6 — Observation & data acquisition

The state `Xi` is **latent**. You never see it directly — you see noisy, aggregated,
sometimes adversarial *functions* of it. L6 is the lens between the world and the model, and
it is also the layer that **goes and gets the number** when the model is missing one.

---

## The observation operator

```
y = H(Xi) + eps,        eps ~ N(0, R)
```

- `H` is the **observation operator**: the (usually lossy, usually aggregating) map from the
  full latent state `Xi = (S, {rho_k}, {b_k}, W, Pi)` to what is actually measured.
- `eps ~ N(0, R)` is observation noise with covariance `R`. Bigger `R` = noisier feed.
- Observables are things like: **engagement metrics, surveys, prediction-market prices,
  mobility data, retail sales, official statistics (CPI, unemployment, GDP), search trends,
  order books.** Every one of them is `H(Xi)+eps` — none is `Xi`.

**Aggregation is the key property.** A single observed signal is a
**membership-weighted mixture of block states**:

```
y_signal = Σ_k  m_k · h_k(x_k)  +  eps
```

where `m_k` is block `k`'s membership weight in that signal. A national CPI print is a
weighted blend over consumption blocks; a "consumer confidence" number blends sentiment
across communities (L3). This is why a single aggregate can look calm while a block is
already critical — the mixture *averages away* the block signal (the L3/L5 cross-term). When
you read an observable, always ask **whose state, at what weight, is in this number.**

---

## Data-integrity questions — "is the government lying about the data?"

These are **adversarial / biased observations**, and they decompose cleanly into the operator:

- **Corrupted `H`** — the *definition* is gamed. (Reclassifying long-term unemployed out of
  the labor force; hedonic/substitution choices that bend CPI; redefining the boundary so the
  bad block falls outside the mixture.) The map itself is dishonest.
- **Biased `eps`** — the *noise has nonzero mean*: `E[eps] ≠ 0`. Systematic over/under-
  reporting, smoothing, strategic release timing. The map is fine; the realizations are
  shaded.

**Remedy: cross-source assimilation, NOT trusting one feed.** Triangulate multiple
*independent* observables of the same latent state and look for the disagreement structure:

- If official CPI says 3% but prediction markets, scanner/retail price data, and survey
  expectations cluster at 6%, the *spread* is the signal — one observable has a corrupted `H`
  or biased `eps`.
- Independence matters: two feeds that share a source (or share the gaming incentive) are one
  feed. Prefer observables with *different* `H` and *uncorrelated* `eps`.

**Tie to EnKF assimilation (conceptual).** This is exactly ensemble Kalman filtering: each
observable updates the state estimate weighted by its **inverse noise `R^-1`**. A trustworthy,
independent source has small `R` and pulls the estimate hard; a suspect source has large `R`
(down-weighted) — and a source you believe is *biased* (nonzero `E[eps]`) must be
**bias-corrected or excluded**, because the Kalman update assumes zero-mean noise and a biased
feed will silently drag the whole posterior. The posterior over `Xi` is the multi-source
consensus, with its variance honestly inflated by the disagreement. **Never collapse onto one
feed when its integrity is the question.**

---

## THE DATA-ACQUISITION PROTOCOL

The most operational part of L6. When a question needs a number the model **does not have**
— *"exactly how much of housing unaffordability is immigration?"*, "what is the actual
debt-to-GDP?", "what is country A's productivity vs B's?" — the skill must **GO GET IT.**
A missing magnitude is not a reason to hand-wave; it is a `WebSearch`/`WebFetch` task.

**Protocol (numbered, do in order):**

1. **Identify the precise quantity needed.** Not "housing data" — the *exact* number and
   units the model consumes (e.g. "share of the 2015–2024 real house-price increase in
   metro X attributable to immigration-driven demand, in percentage points"). State its role
   in the model: which layer/parameter it feeds.
2. **WebSearch for authoritative sources.** Prefer, in order: central banks (Fed, ECB, BoE,
   RBA), statistical agencies (BLS, Census, Eurostat, ONS, ABS), supranational bodies
   (**BIS, IMF, OECD**, World Bank), then **peer-reviewed studies** and reputable working
   papers (NBER, central-bank research series). Avoid op-eds and advocacy sites for
   magnitudes.
3. **WebFetch the best source** and extract the figure — the point estimate, its units, its
   time window, its geography, and any confidence interval / elasticity.
4. **Record the number WITH its source URL and date** (publication date *and* the data
   vintage). A number without a citation is not acquired; it is invented.
5. **Note uncertainty / disagreement across sources.** If two credible studies disagree,
   record the *range* and the reason (different identification, different region, different
   window). The spread becomes the model's input uncertainty (this IS the assimilation
   step).
6. **Feed it back into the relevant layer.** A productivity figure → L1; an elasticity →
   L4 reaction map; a stock magnitude → L1/L5 bifurcation parameter; a sentiment series →
   L3/L6 observable.

**Scope-verdict effect:** acquiring the number moves the verdict **NEEDS-DATA → PARTIAL**
(or **MODELED**, if the number was the only gap). Record the move explicitly in the reading.

### Worked mini-example (illustrative of the protocol)

> **Question:** "Exactly how much of housing unaffordability is immigration?"

1. **Quantity needed:** the share (percentage points) of the recent real house-price (or
   rent) increase in a named market attributable to immigration-driven housing demand, with
   a demand elasticity if available. Role: an L1 source term (demand inflow) and an L4
   reflexivity check (expectations), but first it is a pure magnitude.
2. **WebSearch:** `immigration contribution house price growth BIS OECD study percentage`,
   `central bank working paper immigration rents elasticity`. Filter to central-bank /
   statistical-agency / peer-reviewed hits.
3. **WebFetch** the strongest hit (e.g. a central-bank or NBER working paper estimating the
   elasticity of local house prices / rents to an immigration-induced population shock).
4. **Record (ILLUSTRATIVE — placeholder pending a real fetch):**
   - Figure: *"a 1% rise in a city's population from immigration is associated with ≈ a
     ~1% rise in rents / house prices in that city"* (an elasticity near unity is the
     order-of-magnitude many local studies report).
   - Source: `<central-bank or NBER working-paper URL>` — published `<YYYY-MM-DD>`, data
     vintage `<years>`, geography `<country/metros>`.
   - **Label clearly:** this exact figure is a placeholder demonstrating the protocol shape,
     **not** a verified citation. A real run MUST replace it with a fetched, URL-backed
     number.
5. **Uncertainty:** estimates vary widely by market, supply elasticity, and identification
   strategy (supply-constrained metros show larger effects; elastic-supply metros much
   smaller). Record the range, not a single hero number; flag that immigration is *one*
   demand term among many (rates, supply/zoning, investor demand).
6. **Feed back:** insert the elasticity as the immigration-demand inflow in the L1 housing
   stock-flow and re-run; report the *attributable share* as a band, with the residual
   explicitly assigned to the other drivers.

**Verdict transition:** before step 3 the question is **NEEDS-DATA**; after a real,
URL-cited fetch it becomes **PARTIAL** ("immigration plausibly explains an X–Y pp band of the
increase, with supply elasticity the dominant moderator; source: …"). The framework's
contribution is the *decomposition and the band*, never a false-precision single number.

---

## HOW THE SKILL USES THIS LAYER

- [ ] **Trigger:** cue words `how much, exactly, is the data, statistics show, measure,
      lying about data`, or any question whose answer hinges on a magnitude the model lacks.
- [ ] **Treat every observable as `y = H(Xi)+eps`:** ask whose block state, at what
      membership weight, is in the number (aggregation is lossy).
- [ ] **Data-integrity questions:** diagnose as corrupted `H` (gamed definition) vs biased
      `eps` (nonzero-mean reporting); **triangulate independent feeds** (EnKF-style, weight
      by `R^-1`, bias-correct or drop biased feeds) — never trust a single suspect source.
- [ ] **Missing number → run the acquisition protocol:** identify the exact quantity →
      WebSearch authoritative sources (central banks / stat agencies / BIS/IMF/OECD /
      peer-reviewed) → WebFetch → record figure **+ URL + date** → note cross-source spread →
      feed back into the owning layer.
- [ ] **Move the scope verdict** NEEDS-DATA → PARTIAL/MODELED once the number is fetched and
      cited; record the move.
- [ ] **Honesty:** a number without a source URL and date is not acquired. Report ranges and
      disagreement, not false precision. Clearly label any placeholder/illustrative figure.
