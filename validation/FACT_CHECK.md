# FACT_CHECK.md — Checklist category G (factual & citation claims)

Verification of the outstanding factual and citation claims in `psychohistory.tex`.
Each row: claim as stated in the paper, verdict (PASS / FIX-NEEDED), correct value, source URL.
Verified 2026-06-15 via web search against primary/authoritative sources.

Summary: 18 items checked — **17 PASS, 1 FIX-NEEDED** (the one fix is a precision tightening on the ~94% figure, not a factual error; see item 1.7).

---

## 1. SVB running example (lines 62, 64, 162–164)

| # | Claim in paper | Verdict | Correct value / note | Source |
|---|----------------|---------|----------------------|--------|
| 1.1 | SVB sold its AFS securities at a **~$1.8B loss** and launched a capital raise on **Mar 8 2023** | PASS | Mar 8 2023: sold ~$21B AFS portfolio at $1.8B after-tax loss; announced ~$2.25B capital raise. | https://www.americanbanker.com/news/svb-financial-sells-securities-at-a-1-8b-loss-launches-capital-raise |
| 1.2 | **~$42B** attempted withdrawal / run | PASS | Customers tried to withdraw **$42B in a single day** (Mar 9), leaving ~$1B negative cash position. | https://www.fdic.gov/news/speeches/2023/spmar2723.html |
| 1.3 | **FDIC seizure Mar 10 2023** | PASS | Mar 10 2023: CA DFPI closed SVB ($209B assets at YE2022), appointed FDIC as receiver. | https://www.fdic.gov/news/speeches/2023/spmar2723.html |
| 1.4 | **Sunday Mar 12 2023** joint systemic-risk-exception all-deposit backstop | PASS | Mar 12 2023 joint Treasury/Fed/FDIC statement invoked the systemic-risk exception; all depositors (insured + uninsured) made whole. | https://uk.practicallaw.thomsonreuters.com/w-038-8246 |
| 1.5 | ~$15B unrealized HTM losses ≈ tangible common equity | PASS (supporting fundamental) | ~$15B unrealized losses on HTM book, on the order of SVB's equity; consistent with the sector-wide ~$620B HTM hole reported at the time. | https://fortune.com/2023/03/10/svb-collapse-fdic-takeover-martin-gruenberg-620-billion-hole-banks-balance-sheet/ |
| 1.6 | Standard deposit insurance did **not** select the no-run equilibrium; the discretionary systemic-risk exception did | PASS | Correct: because deposits were overwhelmingly uninsured, the standard FDIC cap was non-binding; the no-run outcome was selected by the discretionary Mar 12 systemic-risk exception (a one-off, not a standing rule). | https://www.federalregister.gov/documents/2023/11/29/2023-25813/special-assessment-pursuant-to-systemic-risk-determination |
| 1.7 | **"roughly ninety-four percent of SVB's deposits were uninsured"** (line 164) | **FIX-NEEDED (tighten)** | The 94% figure is **correct for U.S. domestic deposits as of Dec 31 2022** per SVB's own 2022 10-K, cited by the FDIC/Fed post-mortems. Headline figures commonly stated are "more than 90%" (≈$151B uninsured of ~$173B). **The 94% number is defensible but should be qualified** as "~94% of *domestic* deposits as of year-end 2022 (>90% overall)" to avoid overstatement. Keep "~94%" but add the year-end-2022 / domestic qualifier, or soften to "roughly 90%." | https://time.com/6262009/silicon-valley-bank-deposit-insurance/ ; https://www.consumerfinance.gov/about-us/newsroom/statement-of-cfpb-director-rohit-chopra-on-recouping-losses-to-the-deposit-insurance-fund-from-protecting-uninsured-depositors-of-silicon-valley-bank-and-signature-bank/ |

## 2. Continental Illinois disconfirming case (line 64)

| # | Claim in paper | Verdict | Correct value / note | Source |
|---|----------------|---------|----------------------|--------|
| 2.1 | **Continental Illinois 1984** was a comparably large run **not** arrested by a cheap fixed-point announcement; required a sustained, expensive open-bank assistance program | PASS | Largest US bank failure to that date (~$40B assets, 7th-largest US bank); May 1984 depositor run; FDIC provided Open Bank Assistance (May 17 1984), then a permanent rescue injecting ~$4.5B and taking ~80% equity; coined "too big to fail." Expensive, sustained — exactly the paper's contrast. | https://www.federalreservehistory.org/essays/continental-illinois |

## 3. AI-scenario "real-ish" numbers (lines 456, 469)

| # | Claim in paper | Verdict | Correct value / note | Source |
|---|----------------|---------|----------------------|--------|
| 3.1 | Cost per token falls **"by roughly an order of magnitude per year (a documented industry trend)"** | PASS | Well-supported and if anything conservative. Epoch AI finds LLM inference price drops of ~9–900x/year depending on task, median ~50x/yr (rising to ~200x/yr post-Jan-2024). ~10x/yr is a defensible floor; no change needed, though it could note it is task-dependent. | https://epoch.ai/data-insights/llm-inference-price-trends |
| 3.2 | Frontier model releases are frequent, **"order monthly"** release cadence | PASS | Defensible. Median gap between frontier releases fell from ~170 days (2023) to ~85 (2024) to ~58 (2025) to ~49 (2026 YTD) — i.e. trending into the ~monthly range; 2026 flagships now update every few weeks. "Order monthly" is reasonable; "every 1–2 months" would be the most precise phrasing. | https://officechai.com/ai/frontier-labs-are-releasing-new-models-faster-than-ever-shows-data/ |

## 4. Asimov canon attributions

| # | Claim in paper | Verdict | Correct value / note | Source |
|---|----------------|---------|----------------------|--------|
| 4.1 | Two psychohistory axioms (population large; population ignorant of the predictions) from the *Foundation* (1951) / Encyclopedia Galactica frame | PASS | Both axioms are canonical Seldon premises: sufficiently large population + population ignorant of the analysis results. *Foundation* assembled 1951 from 1942–44 stories. | https://en.wikipedia.org/wiki/Psychohistory_(fictional) |
| 4.2 | Gas / kinetic-theory analogy attributed to **Foundation and Earth (1986)**, not Prelude | PASS (with minor nuance) | The gas/kinetic-theory analogy (cannot predict one molecule, can predict the mass) is genuinely Asimov's standing image for psychohistory and *is* restated in *Foundation and Earth* (1986). Note: the analogy recurs across the corpus including the prequels; attributing it specifically to *Foundation and Earth* is accurate but not exclusive. No fix required. | https://en.wikipedia.org/wiki/Foundation_(novel_series) |
| 4.3 | **"Franchise" (1955)** — Multivac predicts an election from one representative voter | PASS | Pub. Aug 1955 (*If*). Multivac selects a single citizen (Norman Muller) and reconstructs the full election result from his answers. | https://en.wikipedia.org/wiki/Franchise_(short_story) |
| 4.4 | **"The Evitable Conflict" (1950)** — the Machines manage the world economy, accepting small individual harms for the aggregate | PASS | Pub. 1950. Four regional positronic "Machines" run the world economy as a feedback controller, tolerating minor harm to individuals to protect humanity in aggregate. | https://en.wikipedia.org/wiki/The_Evitable_Conflict |
| 4.5 | **"All the Troubles of the World" (1958)** — Multivac predicts crime; wishes to die | PASS | Pub. Apr 1958 (*Super-Science Fiction*). Multivac forecasts crimes before they occur (pre-empted by law enforcement); when asked what it wants, answers "I want to die." | https://en.wikipedia.org/wiki/All_the_Troubles_of_the_World |
| 4.6 | **"The End of Eternity" (1955)** — the Eternals / Minimum Necessary Change; abolishing Eternity leads to the Galactic Empire | PASS | 1955 novel. Organization "Eternity" edits history via the Minimum Necessary Change; its very existence had erased the Galactic Empire; abolishing Eternity releases a risk-taking humanity that founds the Empire. | https://en.wikipedia.org/wiki/The_End_of_Eternity |

## 5. Bibliography spot-check (newer entries)

| # | Entry | Verdict | Correct value / note | Source |
|---|-------|---------|----------------------|--------|
| 5.1 | `clune2013` — Clune, Mouret, Lipson, "The evolutionary origins of modularity," Proc R Soc B, 280(1755):20122863, 2013 | PASS | Exact match: authors, journal, vol 280, issue 1755, art. 20122863, 2013 (DOI 10.1098/rspb.2012.2863). | https://royalsocietypublishing.org/doi/10.1098/rspb.2012.2863 |
| 5.2 | `franciswonham1976` — Francis & Wonham, "The internal model principle of control theory," Automatica, 12(5):457–465, 1976 | PASS | Exact match: Automatica vol 12, pp 457–465, 1976. | https://www.sciencedirect.com/science/article/abs/pii/0005109876900066 |
| 5.3 | `page1954` — E.S. Page, "Continuous inspection schemes," Biometrika, 41(1–2):100–115, 1954 (CUSUM) | PASS | Exact match: Biometrika 41(1–2):100–115, 1954; founding CUSUM paper. | https://academic.oup.com/biomet/article-abstract/41/1-2/100/456627 |
| 5.4 | `sims2003` — C.A. Sims, "Implications of rational inattention," J. Monetary Economics | PASS | Exact match: JME 50(3):665–690, 2003. (Paper cites by key; venue/year correct.) | https://www.sciencedirect.com/science/article/abs/pii/S0304393203000291 |
| 5.5 | `goldsteinpauzner2005` — Goldstein & Pauzner, "Demand-deposit contracts and the probability of bank runs," J. Finance, 60(3):1293–1327, 2005 | PASS | Exact match: J. Finance 60(3):1293–1327, 2005 (DOI 10.1111/j.1540-6261.2005.00762.x). | https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2005.00762.x |
| 5.6 | `morrisshin1998` — Morris & Shin, "Unique equilibrium in a model of self-fulfilling currency attacks," AER, 88(3):587–597, 1998 | PASS | Exact match: AER 88(3):587–597, 1998. | https://www.aeaweb.org/aer/ (EconPapers: https://econpapers.repec.org/RePEc:aea:aecrev:v:88:y:1998:i:3:p:587-97) |

---

### Note on the single FIX (item 1.7)
The "~94% uninsured" claim is **not wrong**: 94% is the figure from SVB's 2022 10-K for U.S. domestic deposits at year-end 2022, and it is the number FDIC/Fed reports use. The recommended fix is precision only — qualify it as "~94% of domestic deposits at year-end 2022 (>90% overall)," or soften to "roughly 90%," so it cannot be read as an exact whole-bank figure. The paper's analytical point (uninsured deposits dominated, so standard insurance did not select no-run) is fully correct as written.
