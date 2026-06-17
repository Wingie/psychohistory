window.PSYCHO_DATA = {
"coverage": {
"total": 100,
"modelable": 93,
"structural": 66,
"scope": {
"NEEDS-DATA": 22,
"PARTIAL": 60,
"NORMATIVE-AS-VALENCE": 5,
"TAUTOLOGY": 7,
"MODELED": 6
},
"layers": {
"L6": 63,
"L2": 12,
"L1": 93,
"L0": 36,
"L4": 34,
"L5": 21,
"L3": 21
}
},
"readings": [
{
"rank": 1,
"id": "1m11gep",
"title": "Bernie Sanders claims that Elon Musk owns more wealth than the bottom 52% of Americans. How is that possible?",
"score": 2824,
"active_layers": [
"L6",
"L2",
"L1",
"L0"
],
"dominant_mechanism": "An observation-operator (H) reconciliation: the claim hinges on which definition of 'wealth' (net worth incl. negative-equity bottom deciles vs gross assets) the statistic uses, sitting on top of a genuine L2 wealth-concentration stock.",
"scope_verdict": "NEEDS-DATA",
"reading": "The live question is a measurement question, not a dynamics question: the factor-of-ten discrepancy resolves at H, the observation operator, depending on whether the bottom strata are counted by net worth (debt drives the denominator low) or gross assets. L6 fetches the Fed DFA series and the exact net-vs-gross convention; once pinned, the underlying L2 phenomenon (attention/wealth preferential attachment) is real and structurally guaranteed (no society equalizes to the founder). The 'extremely problematic' aside is an L0 valence the framework resolves per-block rather than ruling on.",
"skill_horizon": "structural/no horizon (a measurement identity, not a forecast)",
"key_falsifier": "If recomputing the Fed bottom-50% net worth with the same debt-inclusive convention Sanders used does NOT reproduce a figure below Musk's net worth, the reconciliation is wrong and the claim is simply an error.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1m11gep/bernie_sanders_claims_that_elon_musk_owns_more/"
},
{
"rank": 2,
"id": "1teyzn5",
"title": "Why are UK salaries so uncompetitive at a global level?",
"score": 2317,
"active_layers": [
"L1",
"L6"
],
"dominant_mechanism": "Slow-stock divergence: a decade-plus of flat UK productivity/output-per-hour and a depreciated real exchange rate vs a US tech-sector wage premium, comparative statics over the wage stock.",
"scope_verdict": "PARTIAL",
"reading": "This is an L1 stock-and-flow question: UK nominal salaries lag because the productivity stock (output per hour) stagnated post-2008, GBP real terms fell, and US FAANG comp reflects a winner-take-all tech rent the UK labour market does not capture. The framework models the SHAPE cleanly (productivity + FX + sector-mix differential) but the magnitudes -- exactly when divergence began and how much each channel contributes -- are L6 numbers to fetch (ONS productivity series, OECD comp levels).",
"skill_horizon": "quarters-to-years for the trend (slow stock); the divergence is persistent, not mean-reverting",
"key_falsifier": "If UK output-per-hour growth actually tracked the US over 2008-2024, the productivity-stock explanation collapses and the gap must be FX/sector-rent only.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1teyzn5/why_are_uk_salaries_so_uncompetitive_at_a_global/"
},
{
"rank": 3,
"id": "1ncv5bf",
"title": "Nvidia is worth over $4T. Adjusted for inflation, that's $2.5T in the year 2000. How is this not a bubble?",
"score": 2143,
"active_layers": [
"L2",
"L4",
"L5",
"L1"
],
"dominant_mechanism": "Endogenous attention over-concentration on one topic (AI compute) coupled to a reflexive price-belief loop in the imitative/strategic-complements regime.",
"scope_verdict": "PARTIAL",
"reading": "Bubble formation is L2 attention concentration plus an L4 reaction map; the decisive test is monotone (fundamental earnings drift, agents avoid crowded trades) vs imitative (agents pile in because price is rising). Nvidia has a genuine L1 earnings stock unlike pure manias, so it is a mixed regime -- partly fundamental drift, partly imitative cascade -- which is bistable and has no unique publishable fixed point. The framework forecasts the TRANSITION RISK (is it pre-critical?) not the crash date; near criticality the branch is unforecastable by construction.",
"skill_horizon": "no horizon for the branch/date; transition-risk diagnosable while cross-block synchrony (does it jump from AI-trade block to retail broadly?) stays readable",
"key_falsifier": "If forward earnings/datacenter-capex actually grow into the multiple (P/E compresses without a price fall), the imitative-bubble reading is falsified -- it was monotone fundamental drift.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1ncv5bf/nvidia_is_worth_over_4t_adjusted_for_inflation/"
},
{
"rank": 4,
"id": "1oghgwl",
"title": "ELI5 The richest person in 1993 had a networth of just 8 billion dollars and in 2025, richest person has 500 billion dollars. What is the root cause of the rise in this inequality? Is it a good thing or bad?",
"score": 1871,
"active_layers": [
"L0",
"L2",
"L1"
],
"dominant_mechanism": "A normative query ('good or bad') resolved as a per-block valence field, riding on an L2 attention/wealth preferential-attachment process (winner-take-all platform scale).",
"scope_verdict": "NORMATIVE-AS-VALENCE",
"reading": "The 'root cause' half is L2: digital winner-take-all markets let one node capture a global user base, so top wealth scales with addressable population in a way 1993 industrials could not -- concentration is the rich-get-richer fixed point. The 'good or bad' half is never ruled in the absolute; per the Normativity Rule it is a classifier over (block, scale): capital-holding and meritocratic-ideology blocks read it positive, wage-labor and egalitarian blocks negative, and the sign flips with block size (load-bearing at nation scale for incentives, destabilizing at family scale). Output the valence table, not a verdict.",
"skill_horizon": "structural/no horizon (concentration is a guaranteed fixed point; valence distribution is stable per block)",
"key_falsifier": "If top-wealth growth turns out NOT to track platform/market-scale (e.g. the richest are non-scalable asset holders), the winner-take-all attention mechanism is the wrong root cause.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1oghgwl/eli5_the_richest_person_in_1993_had_a_networth_of/"
},
{
"rank": 5,
"id": "1lw2rdb",
"title": "Is the United States heading towards an economic collapse?",
"score": 1733,
"active_layers": [
"L5",
"L1",
"L6"
],
"dominant_mechanism": "Slow-stock drift (debt/GDP, dependency ratio) plus proximity to a critical transition; the question asks for branch-prediction the framework explicitly refuses near criticality.",
"scope_verdict": "NEEDS-DATA",
"reading": "Decompose into L1 slow stocks (debt/GDP >100%, worker:retiree ratio, graduate unemployment) which drift reliably and are NOT collapse by themselves, and L5 early-warning state. The honest move is to report predictability as a state variable: forecast THAT a transition is near (rising variance + lag-1 autocorrelation + cross-block synchrony) rather than which branch. Current indicator values are L6 fetches. Flag the prosecutor's fallacy (the asker conditions on a feared outcome) and the N-/R-tipping blind spots: many recessions arrive with no precursor, so absence of warning is not absence of risk.",
"skill_horizon": "days-to-weeks only if pre-critical signals are present; otherwise base-rate beyond a quarter -- no skill on 'collapse' as a branch",
"key_falsifier": "Sustained low cross-block variance and autocorrelation in financial/labor blocks over the next several quarters falsifies any 'imminent transition' reading.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1lw2rdb/is_the_united_states_heading_towards_an_economic/"
},
{
"rank": 6,
"id": "1ok5wfc",
"title": "Are SNAP benefits essentially subsidies for corporations who don't pay a living wage?",
"score": 1404,
"active_layers": [
"L1",
"L0",
"L6"
],
"dominant_mechanism": "Tax/transfer incidence on the wage stock: who captures the benefit depends on labor-supply and labor-demand elasticities, an L1 comparative-statics question with an L0 framing.",
"scope_verdict": "PARTIAL",
"reading": "The 'subsidy to employers' claim is a statement about incidence: a wage subsidy accrues to firms only to the degree labor supply is elastic and demand inelastic; if SNAP raises reservation wages it can do the opposite. The framework models the SHAPE (incidence runs on the elasticity ratio) but the sign and size are L6 elasticities to fetch. The asker's premise that 'most recipients have paid employment' is itself a NEEDS-DATA sub-claim. The 'living wage' framing is an L0 valence resolved per block, not a structural fact.",
"skill_horizon": "structural/no horizon (a comparative-statics incidence claim, not a time-series forecast)",
"key_falsifier": "If empirical SNAP-incidence studies show the benefit raises reservation wages and tightens low-wage labor supply, the 'corporate subsidy' direction is reversed and the reading fails.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1ok5wfc/are_snap_benefits_essentially_subsidies_for/"
},
{
"rank": 7,
"id": "1otrmkp",
"title": "How can Denmark afford everything that America can't?",
"score": 1321,
"active_layers": [
"L1",
"L0"
],
"dominant_mechanism": "Fiscal stock-and-flow comparison: Denmark's high broad-based tax-to-GDP, low debt stock, and small defense flow versus US composition -- 'afford' is an accounting/political-economy choice, not a hard constraint.",
"scope_verdict": "PARTIAL",
"reading": "Route to L1: build a stock-flow comparison of the two fiscal regimes -- Denmark funds via high, flat-ish, broad consumption+income taxation (not just 'tax the rich'), runs surpluses, carries low debt, and spends less on defense and health-admin overhead. 'Afford' is largely a composition-and-political-will variable, not a binary capacity. The framework models the structure crisply; the exact tax-wedge, deadweight, and transferability-to-US-scale magnitudes are L6 numbers. Underneath sits an L0 valence about which social-contract block the spending serves.",
"skill_horizon": "structural/no horizon (institutional comparative statics)",
"key_falsifier": "If Denmark's outcomes actually rest on a non-transferable special factor (e.g. homogeneity, EU integration, hidden debt) rather than tax composition, the 'just a fiscal-choice' framing is wrong.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1otrmkp/how_can_denmark_afford_everything_that_america/"
},
{
"rank": 8,
"id": "1qy91q0",
"title": "Why can the US government successfully run a massive grocery chain for the military (commissaries), but municipal-run grocery stores for the public often fail?",
"score": 1286,
"active_layers": [
"L1",
"L3"
],
"dominant_mechanism": "Institution-as-block with differing objective functions and backing stocks: appropriated subsidy + captive eligibility-gated demand + national procurement scale versus thin-margin self-funded single-store municipal operations.",
"scope_verdict": "PARTIAL",
"reading": "This is the canonical L1 + qualitative ('LLM'd and lethained') institutional comparison. The commissary works because its stocks differ on every axis: funding (appropriated subsidy + bulk national procurement vs thin self-funded margin), customer base (fixed eligibility-gated captive demand vs open competitive), objective function (retention/morale, not profit), and failure cost (absorbed by DoD vs store closes). The insight is the difference in incentive structure and backing stocks, not a magnitude. L3 enters because the military customer base is a cohesive block lowering demand variance.",
"skill_horizon": "structural/no horizon (institutional comparative statics)",
"key_falsifier": "A municipal store matched on subsidy, procurement scale, and captive demand that still fails would falsify the incentive-structure explanation and point to management/local factors.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1qy91q0/why_can_the_us_government_successfully_run_a/"
},
{
"rank": 9,
"id": "1q37pg4",
"title": "Why isn't Russia collapsing?",
"score": 1159,
"active_layers": [
"L5",
"L1",
"L6"
],
"dominant_mechanism": "A repeatedly-failed collapse prediction: war-economy slow stocks (reserves, FX, labor) draining slowly while the predicted critical transition keeps not arriving -- a base-rate/prosecutor's-fallacy case.",
"scope_verdict": "NEEDS-DATA",
"reading": "The framing exposes the prosecutor's fallacy directly: 'collapse imminent for 3 years' conditions on a feared branch without a null model or base rate. L1 says a war economy can run on draining stocks (reserves, NWF, labor, equipment) for a long time -- decline is a slow flow, not a cliff. L5: there is no rising-variance precursor visible, and crucially N-/R-tipping (a sanctions-rate shock or noise excursion) would give NO warning, so 'not collapsing yet' is not evidence of stability. The true state of reserves, inflation, and frontline supply are L6 fetches before any forecast.",
"skill_horizon": "quarters for the slow-drain trajectory; no horizon for a sudden-collapse branch (no readable precursor)",
"key_falsifier": "Observing a sustained, sharp rise in cross-sector financial variance + autocorrelation (genuine B-tipping precursor) would upgrade the reading from 'slow drain, no imminent transition' to 'pre-critical.'",
"url": "https://www.reddit.com/r/AskEconomics/comments/1q37pg4/why_isnt_russia_collapsing/"
},
{
"rank": 10,
"id": "1mbd77e",
"title": "Bill Gates Wants To 'Tax The Robots' That Take Your Job - And Some Say It Could Fund Universal Basic Income To Replace Lost Wages... Is this a good idea?",
"score": 1117,
"active_layers": [
"L0",
"L1",
"L4"
],
"dominant_mechanism": "A normative policy query ('good idea?') resolved as a per-block valence field, over an L1 tax-base/automation-incidence stock and an L4 behavioral (Lucas) response to taxing capital.",
"scope_verdict": "NORMATIVE-AS-VALENCE",
"reading": "'Good idea' is never ruled absolutely; it is a classifier over blocks: displaced-labor and egalitarian blocks read it positive (replaces lost wages), capital/automation-deploying and growth-ideology blocks negative (taxing productivity-enhancing capital distorts the investment margin -- the classic Lucas/L4 behavioral-response objection that firms re-optimize against the announced tax). L1 carries the real structural fact: a robot tax is a capital-input tax whose incidence and base-erosion depend on automation elasticity. Output the valence table plus the structural-necessity note (inequality from automation is a guaranteed dispersion), not a verdict.",
"skill_horizon": "structural/no horizon (normative classifier + comparative statics)",
"key_falsifier": "If automation turns out to be gross-complementary to labor at the margin (raising not lowering wages), the premise 'replace lost wages' dissolves and the valence map shifts.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1mbd77e/bill_gates_wants_to_tax_the_robots_that_take_your/"
},
{
"rank": 11,
"id": "1ojw4vs",
"title": "If I had $500B, bought a single piece of cake from my friend for half a trillion dollars, then cleaned his glasses in exchange for half a trillion, would the nation's economy increase by one trillion that year?",
"score": 993,
"active_layers": [
"L6"
],
"dominant_mechanism": "Pure accounting identity: whether the two transactions are 'counted' is a property of the observation operator H (GDP as sum of final expenditures), exercising no forward dynamics.",
"scope_verdict": "TAUTOLOGY",
"reading": "This touches ONLY H, the definitional/measurement map, not the state evolution Xi. The honest one-liner: by the expenditure definition of GDP these would in principle add to measured output, but they are final-vs-intermediate and imputation edge cases, and the question is about the accounting convention, not about any transport, block, reflexivity, or criticality dynamics. Recommend DROP from the modelable count -- it teaches the engine nothing about dynamics.",
"skill_horizon": "n/a (definitional, no dynamics, no horizon)",
"key_falsifier": "n/a -- a tautology about an accounting identity has no empirical content to falsify; only the convention itself could be misstated.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1ojw4vs/if_i_had_500b_bought_a_single_piece_of_cake_from/"
},
{
"rank": 12,
"id": "1qp0jvw",
"title": "Why does Trump want a weaker US dollar?",
"score": 927,
"active_layers": [
"L1",
"L4"
],
"dominant_mechanism": "Slow-stock trade-balance logic (a weaker dollar cheapens exports / dearer imports to shrink the trade deficit and reshore manufacturing) coupled to L4 expectations management of FX.",
"scope_verdict": "MODELED",
"reading": "The framework gives a real structural answer at L1: a weaker dollar raises export competitiveness and import prices, nominally improving the trade balance and supporting tradable-sector employment -- the stated policy rationale -- while eroding purchasing power and risking the reserve-currency premium (the cross-term). L4 enters because FX levels are partly expectational and 'wanting' a weaker dollar is itself a signal that can move markets reflexively. The mechanism is well-specified; this is a why-question with a clean structural answer, not a magnitude forecast.",
"skill_horizon": "structural/no horizon for the rationale; FX path itself is near-random-walk (no skill on the level)",
"key_falsifier": "If a weaker dollar empirically failed to improve the trade balance (J-curve persists, Marshall-Lerner fails) the stated rationale is internally incoherent and the reading is wrong.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1qp0jvw/why_does_trump_want_a_weaker_us_dollar/"
},
{
"rank": 13,
"id": "1p9y341",
"title": "Can corporations like Starbucks really afford to pay significantly more?",
"score": 905,
"active_layers": [
"L1",
"L6"
],
"dominant_mechanism": "A firm stock-and-flow accounting question: 'afford' depends on whether you draw from net income alone or from total revenue/cost structure -- the asker's per-employee profit arithmetic frames the answer.",
"scope_verdict": "PARTIAL",
"reading": "Route to L1 firm accounting. The asker's net-income/headcount division understates the true lever: raises come from total labor-cost share of revenue and price pass-through, not just residual profit-per-employee, and 'afford' also depends on competitive labor markets and automation substitution at the new wage. The framework models the SHAPE (the right denominator is the cost structure, and incidence/pass-through governs feasibility); the exact revenue, labor-share, and price-elasticity numbers are L6 fetches before the $25 claim can be adjudicated.",
"skill_horizon": "structural/no horizon (firm comparative statics, not a time forecast)",
"key_falsifier": "If Starbucks' labor share and price-elasticity data show meaningful pass-through room without demand loss, the asker's 'completely unreasonable' conclusion is falsified.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1p9y341/can_corporations_like_starbucks_really_afford_to/"
},
{
"rank": 14,
"id": "1lcu5sg",
"title": "Is Trump lying about the economic data his administration is publishing?",
"score": 898,
"active_layers": [
"L6",
"L1"
],
"dominant_mechanism": "Data-integrity at the observation operator: distinguishing adversarial/biased H (deliberate misreporting) from honest measurement noise plus routine revisions in a multi-source signal.",
"scope_verdict": "NEEDS-DATA",
"reading": "This is the second half of L6: data integrity under possibly-adversarial observation. The framework separates three things the asker conflates: (1) honest revision noise (initial payroll prints are routinely revised), (2) genuine measurement divergence across sources (BLS vs SS claims vs enlistment each measure different Xi-components through different H), and (3) deliberate misreporting. Resolving 'lying' requires fetching the actual revision series and methodology and testing whether discrepancies exceed the historical revision band. Flag: cross-source contradictions are expected even with honest H, so contradiction alone is not proof of lying (prosecutor's-fallacy analogue at the data layer).",
"skill_horizon": "structural/no horizon (an integrity audit of H, not a forecast)",
"key_falsifier": "If the cited discrepancies all fall within the historical revision/sampling band of an honest H, the 'lying' hypothesis is not supported.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1lcu5sg/is_trump_lying_about_the_economic_data_his/"
},
{
"rank": 15,
"id": "1mwi4vm",
"title": "If I pay my friend $5 to slap me in the face, and then he pays me $5 to slap him in the face, have we technically raised GDP?",
"score": 879,
"active_layers": [
"L6"
],
"dominant_mechanism": "Pure accounting tautology: whether the reciprocal $5 services count is a property of the observation operator H (GDP = sum of final expenditures on services), with no forward dynamics.",
"scope_verdict": "TAUTOLOGY",
"reading": "Touches ONLY H, the definitional map -- not transport, blocks, reflexivity, or criticality. The honest one-liner: yes, by the definition of GDP as the sum of final expenditures, two $10 of reported service transactions would add to measured output -- a tautology about the accounting identity, not a prediction about any dynamics. Recommend DROP from the modelable count; it exercises no mechanism in Xi's evolution.",
"skill_horizon": "n/a (definitional, no dynamics)",
"key_falsifier": "n/a -- an accounting identity has no empirical content to break; only the stated convention could be misdescribed.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1mwi4vm/if_i_pay_my_friend_5_to_slap_me_in_the_face_and/"
},
{
"rank": 16,
"id": "1otajn6",
"title": "If, hypothetically, I were a Tesla shareholder, why would I want to vote yes to a generous pay increase for Elon Musk?",
"score": 825,
"active_layers": [
"L4",
"L1"
],
"dominant_mechanism": "A coordination/reflexivity game: the milestone-gated stock package is positive-EV for existing holders IFF the conditions that trigger it ($8.5T cap, robotaxi/robot milestones) also enrich them -- a fixed point where retention-of-CEO belief is self-fulfilling.",
"scope_verdict": "MODELED",
"reading": "The framework gives a clean L4 answer: the package is dilutive in isolation (L1: more shares to Musk = smaller slice each) but is structured so the stock only vests if the company grows ~6x, so a rational holder votes yes iff they believe (a) Musk's continued alignment is necessary to reach those milestones and (b) the value created exceeds the dilution. It is a coordination problem with a self-fulfilling component: if enough holders expect his retention to drive the cap, voting yes is individually rational -- a reflexive fixed point, not pure dilution arithmetic. Holders who reject the premise (Norwegian fund) sit at the other equilibrium.",
"skill_horizon": "structural/no horizon (a decision-theoretic/coordination structural claim)",
"key_falsifier": "If the milestones are reachable without Musk (or the dilution exceeds plausible milestone value at any belief), the 'rational yes' fixed point disappears and only the no-vote is rational.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1otajn6/if_hypothetically_i_were_a_tesla_shareholder_why/"
},
{
"rank": 17,
"id": "1q9gmz7",
"title": "Why has the Covid pandemic seemingly killed off 24-hour stores for good? If they thought it was profitable for businesses to remain open before, what has changed after to make them all suddenly realize that it no longer is?",
"score": 780,
"active_layers": [
"L1",
"L3",
"L4"
],
"dominant_mechanism": "A coordination/equilibrium shift: Covid was an exogenous shock that moved firms from a high-coverage Nash equilibrium (stay open because rivals do) to a low one, with the L1 cost stock (overnight labor) now exceeding thin overnight margins.",
"scope_verdict": "PARTIAL",
"reading": "Two layers combine. L1: the overnight shift was always marginal, and a higher post-Covid labor-cost stock plus shifted demand tipped its margin negative. L3/L4: '24-hour' was partly a coordination equilibrium -- stores stayed open because competitors did; the pandemic provided common-knowledge cover to defect simultaneously, and once a block of firms closed, the equilibrium relocated and did not snap back (hysteresis). 'Suddenly realize' is the signature of a coordinated equilibrium jump, not a simultaneous independent recalculation. Magnitudes (overnight margin, labor-cost delta) are L6.",
"skill_horizon": "structural/no horizon for the mechanism; the new equilibrium is hysteretic (won't revert without another shock)",
"key_falsifier": "If overnight hours returned to pre-Covid levels once labor costs/demand normalized, the hysteretic-equilibrium-shift reading is wrong and it was a transient cost response.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1q9gmz7/why_has_the_covid_pandemic_seemingly_killed_off/"
},
{
"rank": 18,
"id": "1pe4wai",
"title": "The current admin is pushing illegal immigration as a very big (if not the biggest) cause of unaffordability in the housing market. How true is such a claim?",
"score": 721,
"active_layers": [
"L6",
"L1",
"L0"
],
"dominant_mechanism": "A magnitude-decomposition question: what share of housing unaffordability is attributable to immigration-driven demand versus supply constraints (zoning, rates, construction) -- answerable only by fetching an elasticity/decomposition.",
"scope_verdict": "NEEDS-DATA",
"reading": "This is the rubric's canonical L6 example: 'how true / how big a cause' demands a number, not a mechanism alone. L1 frames it -- housing price is set by a demand stock (population/household formation, of which immigration is one inflow) against a supply stock dominated by zoning, interest rates, and construction capacity -- but the SHARE attributable to undocumented immigrants (typically renters, often in non-marginal segments) is an L6 decomposition to fetch and cite. Flag the L0 framing: 'biggest cause' is a politically loaded attribution that the data layer must adjudicate against supply-side elasticities, which most evidence weights far more heavily.",
"skill_horizon": "structural/no horizon (a causal-share decomposition, not a forecast)",
"key_falsifier": "A well-identified decomposition showing immigration-driven demand contributes a large share relative to supply constraints would overturn the supply-dominant prior.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1pe4wai/the_current_admin_is_pushing_illegal_immigration/"
},
{
"rank": 19,
"id": "1ndzf5p",
"title": "Why is China able to create high quality EVs for so much cheaper than the US?",
"score": 689,
"active_layers": [
"L1",
"L6"
],
"dominant_mechanism": "Slow-stock industrial comparative statics: vertically integrated battery supply chain, scale, subsidized capital, lower labor cost, and supplier-cluster economies versus US cost structure.",
"scope_verdict": "PARTIAL",
"reading": "Route to L1 industrial stock-flow. China's EV cost advantage is a stack of structural factors: domestic control of the battery/cathode supply chain (CATL/BYD vertical integration), enormous production scale, state-subsidized capital and infrastructure, lower labor cost, and dense supplier clusters lowering coordination cost. The framework models the SHAPE (which stocks differ and why) cleanly and answers the 'can the US replicate' tail qualitatively (some factors are policy-transferable, others -- accumulated supply-chain depth and scale -- are slow stocks taking years). Exact per-vehicle cost-decomposition magnitudes are L6 fetches.",
"skill_horizon": "structural/no horizon for the explanation; years-to-decade for any US catch-up (slow stock accumulation)",
"key_falsifier": "If teardown cost-decompositions show the gap is dominated by a single transferable factor (e.g. only subsidy, not supply-chain depth), the multi-stock 'hard-to-replicate' reading is overstated.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1ndzf5p/why_is_china_able_to_create_high_quality_evs_for/"
},
{
"rank": 20,
"id": "1tuvg5m",
"title": "Why is Canada the only G7 country that has fallen into recession?",
"score": 683,
"active_layers": [
"L5",
"L3",
"L1",
"L6"
],
"dominant_mechanism": "Two questions: an L1/L6 country-specific diagnosis (rate-sensitive household debt, housing, trade exposure) and an L3/L5 contagion/'harbinger' question of whether one block's transition predicts others'.",
"scope_verdict": "NEEDS-DATA",
"reading": "Split it. The 'why Canada' part is L1 + L6: Canada's high household-debt stock and variable-rate mortgage exposure make it unusually rate-sensitive, plus trade/commodity exposure -- the structural shape is clear but the two-quarter contraction magnitudes are L6 fetches. The 'harbinger for the US' part is the interesting L3/L5 question: whether Canada is a correlated leading block or an idiosyncratic one. The framework's discipline: a single block tipping is only a harbinger if cross-block coupling W is high (synchrony rising); if Canada is tipping on an idiosyncratic rate-sensitivity not shared by the US, it is NOT a precursor. Flag prosecutor's fallacy and the N-/R-tipping blind spot. Determining W (are G7 business cycles synchronizing now?) needs data.",
"skill_horizon": "quarters for the slow stocks; harbinger horizon depends entirely on measured cross-block synchrony -- no skill on the US branch without it",
"key_falsifier": "If US/other-G7 indicators show no rising co-movement with Canada (low W), the 'harbinger' reading is falsified -- Canada's recession is idiosyncratic, not a leading indicator.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1tuvg5m/why_is_canada_the_only_g7_country_that_has_fallen/"
},
{
"rank": 21,
"id": "1pirjdh",
"title": "Why does it seem like so many countries are going through a housing crisis simultaneously?",
"score": 683,
"active_layers": [
"L1",
"L3",
"L5",
"L6"
],
"dominant_mechanism": "A common slow-stock driver (post-GFC low rates + chronic supply-inelastic zoning) acts as a shared exogenous forcing that synchronizes otherwise weakly-coupled national housing blocks.",
"scope_verdict": "PARTIAL",
"reading": "This is the cross-block synchrony signature: distinct national blocks (LA, Amsterdam, Dublin) with different internal structure all tip the same way, which under the framework points to a shared global driver rather than K independent causes. The slow stocks are supply inelasticity, a decade of cheap capital chasing a fixed asset, and demand concentration into superstar cities; China/Japan are the control cases (mass supply build / demographic demand collapse). The mechanism (common forcing -> apparent N_eff collapse) is modeled, but the magnitude split between rates vs zoning vs migration per country is a number.",
"skill_horizon": "Structural/slow-stock (years); housing stocks move slowly so comparative statics are reliable, no short-horizon branch forecast needed.",
"key_falsifier": "Find a Western country with the same rate environment and migration inflow but no affordability crisis because supply stayed elastic — that isolates supply as the load-bearing variable and refutes the 'universal demand-side cause' reading.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1pirjdh/why_does_it_seem_like_so_many_countries_are_going/"
},
{
"rank": 22,
"id": "1rwfndk",
"title": "Why is unblocking the Straight of Hormuz so important economically to the US if only 2.5% of its oil come from there and it's a net exporter of oil?",
"score": 679,
"active_layers": [
"L1",
"L2",
"L4"
],
"dominant_mechanism": "Oil is a globally-fungible price-set commodity, so a marginal-barrel shock at Hormuz propagates through one world price regardless of any single country's import share.",
"scope_verdict": "MODELED",
"reading": "The questioner's intuition (low US import share => low exposure) confuses physical sourcing with price exposure: under a single global clearing price, US producers and consumers face the world marginal barrel, so a 20% supply chokepoint moves the price everyone pays. There is also a reflexive/expectations channel (L4) — the threat alone repriced futures before any physical disruption. The accounting fact (fungibility + one price) gives a clean structural answer with no missing number.",
"skill_horizon": "Structural for the mechanism; the price magnitude has no skill horizon (branch depends on whether the blockage actually occurs).",
"key_falsifier": "Observe a Hormuz disruption that leaves US domestic prices decoupled from the world price (i.e. a genuine regional price island) — that would refute the global-fungibility model.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1rwfndk/why_is_unblocking_the_straight_of_hormuz_so/"
},
{
"rank": 23,
"id": "1lqxmcq",
"title": "Are there any clear cut predictions we can confirm will happen now that Trump's Bill is passed?",
"score": 677,
"active_layers": [
"L1",
"L4",
"L5",
"L6"
],
"dominant_mechanism": "A passed fiscal bill changes slow-stock parameters (theta_S) deterministically, but macro outcomes are reflexive and near-criticality so only first-order accounting effects are 'clear cut'.",
"scope_verdict": "PARTIAL",
"reading": "The honest answer separates two registers: the mechanical line-item changes (specific taxes/spending move by legislated amounts — L1 comparative statics, near-certain) versus the macro consequences (deficit path, growth, rates), which are reflexive and branch-dependent and thus NOT clear-cut. The framework explicitly caps resolution at the equilibrium set when behavior responds (Lucas point). Naming the specific provisions and their direct first-order incidence is modeled; the aggregate magnitudes need data and remain unpredictable.",
"skill_horizon": "Short for direct accounting effects (1-2 yr, mechanical); near-zero for macro outcomes (reflexive + pre-critical fiscal regime).",
"key_falsifier": "A direct legislated provision (e.g. a scheduled rate change) fails to produce its first-order accounting effect — that would break even the 'clear cut' tier.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1lqxmcq/are_there_any_clear_cut_predictions_we_can/"
},
{
"rank": 24,
"id": "1ou0ole",
"title": "Every economics expert is saying Japan is on a steep decline. But accounts from people living in Japan seem to be saying the opposite...",
"score": 651,
"active_layers": [
"L1",
"L6",
"L0"
],
"dominant_mechanism": "Aggregate-stock indicators (GDP, yen) and lived per-capita welfare are different observation operators H on the same state, so they can legitimately diverge.",
"scope_verdict": "PARTIAL",
"reading": "The apparent contradiction is an observation-operator mismatch: 'steep decline' reads aggregate/nominal stocks (total GDP, exchange rate) while 'life is affordable' reads per-capita real welfare and price stability — both are correct measurements of Ξ through different H. Japan's slow stocks (shrinking labor force, high public debt, deflationary stability) make per-capita stagnation coexist with high lived quality. The 'good model for post-growth?' clause is a latent L0 valence question resolved per block. Structure is clear; the welfare comparison needs the actual per-capita real series.",
"skill_horizon": "Structural/slow-stock (decadal demographic trend is highly predictable).",
"key_falsifier": "Per-capita real consumption in Japan turns out to be falling sharply (not just aggregate GDP) — that would collapse the 'aggregate vs per-capita divergence' reading into genuine decline.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1ou0ole/every_economics_expert_is_saying_japan_is_on_a/"
},
{
"rank": 25,
"id": "1qdegdr",
"title": "Why didn't the Trump tariffs send the US into a recession?",
"score": 600,
"active_layers": [
"L1",
"L4",
"L5",
"L6"
],
"dominant_mechanism": "Tariffs are a slow-stock price shock whose recessionary transmission depends on magnitude, pass-through timing, and whether the economy was near a critical threshold — none of which were sufficient here.",
"scope_verdict": "NEEDS-DATA",
"reading": "Econ-101 predicts the sign (tariffs raise prices, dampen activity) but not the magnitude or whether it crosses a recession threshold; absorption channels (importer margin compression, inventory front-running, FX moves, exemptions, delayed pass-through) can swallow a sub-critical shock. The framework's point: a small B-tipping push in a smooth regime produces drift, not a cascade. Answering 'why no recession' requires the actual effective tariff rate, pass-through estimates, and growth buffer — numbers L6 must fetch.",
"skill_horizon": "Short (quarters) for pass-through, once the effective rate is known.",
"key_falsifier": "Data show the effective tariff rate and pass-through were large enough that standard multipliers predicted a recession that did not occur — that would refute the 'sub-critical shock absorbed' explanation and point to a missing channel.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1qdegdr/why_didnt_the_trump_tariffs_send_the_us_into_a/"
},
{
"rank": 26,
"id": "1n40vso",
"title": "Why didn't the US government bail out the people instead of the banks and investors in the 2008 GFC? Wouldn't the money have trickled up anyways?",
"score": 591,
"active_layers": [
"L0",
"L1",
"L4",
"L5"
],
"dominant_mechanism": "A bank bailout targets the critical node (the payment/credit system at a cascade point) for maximal leverage, whereas distributing to households is slower and does not directly arrest the reflexive run.",
"scope_verdict": "PARTIAL",
"reading": "This is the prediction-control duality: in a critical financial cascade, intervening at the maximally-susceptible node (interbank/credit system) is the minimal-intervention/maximal-leverage move that halts the run, the same logic as the SVB deposit guarantee. Bailing out households is a slower L1 stock transfer and would not have stopped the reflexive freeze in time, even if funds eventually 'trickled up.' There is a real L0 valence dimension — different blocks judge who deserved rescue oppositely — and a counterfactual magnitude (would household transfers have recapitalized banks fast enough?) that needs data.",
"skill_horizon": "Structural for the mechanism; the counterfactual outcome has no skill horizon.",
"key_falsifier": "Evidence that an equivalently-sized, equally-fast household transfer would have recapitalized the banking system and stopped the cascade just as well — that would refute the 'critical-node leverage' justification.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1n40vso/why_didnt_the_us_governement_bail_out_the_people/"
},
{
"rank": 27,
"id": "1mp2mhc",
"title": "Can we trust the economic data coming out of this White House?",
"score": 588,
"active_layers": [
"L6",
"L4",
"L0"
],
"dominant_mechanism": "This is the data-integrity half of the observation operator: if H becomes biased/adversarial (politically captured), the estimate of Ξ degrades and eventually diverges from ground-truth observables.",
"scope_verdict": "PARTIAL",
"reading": "Squarely an L6 observation-integrity question: the concern is adversarial H (gutted statistical agencies + political incentive to skew). The framework says a biased observation operator corrupts assimilation, and the tell is when official y diverges from independent on-the-ground proxies (private price indices, card-spend data, alternative employment series). The questioner's own examples (gas $1.98, '1500%') are L4 cheap-talk noise, not data. Verifiable claim about agency staffing/methodology changes is fetchable; whether the headline numbers are actually skewed needs cross-checking against independent series.",
"skill_horizon": "Short — divergence becomes detectable within a few release cycles once independent proxies are compared.",
"key_falsifier": "Official series continue to track independent private-sector measures (e.g. Truflation, ADP, card spend) within normal error — that would refute the 'data is skewed' hypothesis.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1mp2mhc/can_we_trust_the_economic_data_coming_out_of_this/"
},
{
"rank": 28,
"id": "1rpjcdi",
"title": "Why has Russia not become an economic wonderland?",
"score": 584,
"active_layers": [
"L1",
"L0",
"L3"
],
"dominant_mechanism": "Resource endowment is a stock; converting it to prosperity requires institutions (rule of law, property rights, diversified investment) whose absence produces the resource-curse / extractive-equilibrium attractor.",
"scope_verdict": "PARTIAL",
"reading": "The post's premise (great inputs => should be rich) omits the binding constraint: institutional quality is the slow stock that converts endowment into broad prosperity. Russia sits in an extractive/rentier equilibrium (resource curse, weak property rights, capital flight, kleptocratic capture) that is a stable institutional fixed point, not a transient. This is L1 stocks plus qualitative 'LLM'd and lethained' reasoning over the incentive structure, with an L0 valence undertone in 'wonderland.' Structure is well-modeled; quantifying the institutional drag is a data exercise.",
"skill_horizon": "Structural/decadal — institutional equilibria are persistent and slow-moving.",
"key_falsifier": "A resource-rich state with comparably weak institutions that nonetheless achieved broad, diversified prosperity — that would refute institutions-as-the-binding-constraint.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1rpjcdi/why_has_russia_not_become_an_economic_wonderland/"
},
{
"rank": 29,
"id": "1me2lc5",
"title": "I ran the federal agency that was cracking down on junk fees – until I was fired. I'm Rohit Chopra, former head of the CFPB. AMA. [Crosspost]",
"score": 583,
"active_layers": [
"L6",
"L0"
],
"dominant_mechanism": "This is an AMA announcement, not a question with dynamics — it touches only the observation/discourse layer (a source offering testimony), not the forward model.",
"scope_verdict": "TAUTOLOGY",
"reading": "No forecastable question is posed; it is an invitation-to-discuss post. The only framework hook is L6 (a primary source on enforcement/junk-fee data) and a latent L0 valence on consumer-protection policy. There is no transport, block, reflexivity, or criticality dynamic to model, so per the §5 rule it touches only the discourse/observation map, not Ξ's evolution. Recommend DROP from a serious dynamics-coverage run; the embedded sub-topics (junk fees, surveillance pricing) would each route to L1/L6 if asked as actual questions.",
"skill_horizon": "None (no dynamical claim).",
"key_falsifier": "N/A — no predictive claim is made that could be falsified.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1me2lc5/i_ran_the_federal_agency_that_was_cracking_down/"
},
{
"rank": 30,
"id": "1sski6f",
"title": "Is it true that USPS was actually doing quite well and turning a profit before the federal government forced it to fund retirement plans in advance which held it back economically?",
"score": 574,
"active_layers": [
"L1",
"L6"
],
"dominant_mechanism": "A pure firm-accounting question: USPS's operating result vs the 2006 PAEA prefunding mandate is a stock-and-flow fact decomposable into operating income and the pension/RHB accrual.",
"scope_verdict": "NEEDS-DATA",
"reading": "This is an L1 stock-flow accounting claim that is settled by fetching the numbers: USPS operating income before vs after the 2006 prefunding mandate, and how much of reported losses were the accelerated retiree-health accrual versus genuine operating shortfall (secular mail-volume decline). The structure is clear (separate operating P&L from the legislated prefunding charge); the verdict hinges on the actual figures, so L6 must acquire them and the answer is likely 'partly true' (prefunding inflated losses but volume decline is real).",
"skill_horizon": "None needed — this is a historical-accounting verification, not a forecast.",
"key_falsifier": "The audited figures show USPS operating losses were large even excluding the prefunding charge — that would refute the 'profitable but for prefunding' claim.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1sski6f/is_it_true_that_usps_was_actually_doing_quite/"
},
{
"rank": 31,
"id": "1melydj",
"title": "Did boomers actually ruin the economy for younger generations?",
"score": 562,
"active_layers": [
"L0",
"L1",
"L2"
],
"dominant_mechanism": "A normative/generational-blame frame over a real slow-stock substrate: cohort-sized demographic stocks plus asset-price concentration shifted relative positions, which different blocks read with opposite valence.",
"scope_verdict": "NORMATIVE-AS-VALENCE",
"reading": "'Ruin' is an L0 valence word, so the answer is a per-block valence table, not a verdict: young/renter blocks read boomer-era asset appreciation and zoning as wealth-hoarding (negative), while owner/older blocks read it as earned and frame youth outcomes as effort-driven (the mother's view). Underneath sits real L1/L2 structure — a large cohort that bought housing/equities cheap and benefited from their subsequent appreciation (attention/wealth concentration), plus policy persistence (zoning, tax treatment). The structural fact is intergenerational relative-position shift; the verdict is a classifier over (block, scale), not a moral ruling.",
"skill_horizon": "Structural/slow-stock for the demographic and asset-position trends.",
"key_falsifier": "Controlling for cohort size and asset timing, younger cohorts show no relative-position disadvantage in wealth/housing access — that would refute the structural basis of the grievance.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1melydj/did_boomers_actually_ruin_the_economy_for_younger/"
},
{
"rank": 32,
"id": "1ntscmb",
"title": "Why is the US economy still doing ok despite the tariffs?",
"score": 546,
"active_layers": [
"L1",
"L4",
"L5",
"L6"
],
"dominant_mechanism": "Same as rank 25: a sub-critical price shock absorbed by margin/inventory/FX buffers and lagged pass-through, so the predicted Econ-101 sign appears without crossing a recession threshold.",
"scope_verdict": "NEEDS-DATA",
"reading": "Econ-101 gives the correct sign but the question is magnitude and timing: pass-through is lagged and partial (front-loaded imports, importer margin absorption, exemptions, FX offset), so a sub-critical shock yields slow drift not a cascade — consistent with stable consumer spending. The framework's smooth-regime reading: small theta_S nudge => bounded response, no tipping. Quantifying 'still ok' requires the effective tariff rate, realized pass-through, and the real-spending series, which L6 must fetch.",
"skill_horizon": "Short (quarters) — pass-through fully materializes with a lag, so the horizon is the lag length.",
"key_falsifier": "Inflation/spending deteriorate sharply with the expected lag, showing the effect was merely delayed not absorbed — that would refute the 'sub-critical, buffered' reading.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1ntscmb/why_is_the_us_economy_still_doing_ok_despite_the/"
},
{
"rank": 33,
"id": "1pakkzv",
"title": "Do billionaires really not pay taxes?",
"score": 545,
"active_layers": [
"L6",
"L1",
"L0"
],
"dominant_mechanism": "A measurement-frame question: 'pay taxes' depends on whether the base is realized income or unrealized net-worth gains, an observation-operator choice that drives the whole dispute.",
"scope_verdict": "NEEDS-DATA",
"reading": "The OP's mechanism (unrealized gains untaxed until realized; buy-borrow-die against appreciating collateral) is essentially correct and is an L6 definitional/measurement issue — the '40%/low rate' fight is entirely about which H you apply (income base vs net-worth base). Settling 'how much do they actually pay' as an effective rate on income vs on wealth requires fetched numbers (e.g. ProPublica/JCT effective-rate estimates). There is an L0 'fair share' valence and an L1 incidence layer, but the core is a number L6 must acquire.",
"skill_horizon": "None needed — definitional plus a fetchable effective-rate statistic.",
"key_falsifier": "Authoritative effective-rate data show billionaires' tax/realized-income ratio is in line with top earners AND the buy-borrow-die channel is empirically negligible — that would refute the 'effectively low via unrealized gains' claim.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1pakkzv/do_billionaires_really_not_pay_taxes/"
},
{
"rank": 34,
"id": "1tvsvqg",
"title": "Why is Egypt so poor?",
"score": 537,
"active_layers": [
"L1",
"L3",
"L6"
],
"dominant_mechanism": "Same resource/endowment-vs-institutions logic as Russia: visible assets (Suez, tourism, youth) are stocks, but per-capita prosperity is governed by productivity, institutions, and the denominator of a large/young population.",
"scope_verdict": "PARTIAL",
"reading": "The premise lists gross assets but omits per-capita denominators and productivity: Suez revenue and tourism are real but small relative to ~100M people, the 'young population' is a dependency/jobs liability without capital and institutions, and statist subsidies, FX mismanagement, military economic capture, and food-import dependence pin a low-productivity equilibrium. This is L1 stocks plus block/institutional reasoning ('LLM'd and lethained'); the structure is clear, the per-capita magnitudes (Suez share of GDP, productivity gap) need data.",
"skill_horizon": "Structural/decadal — development-trap equilibria are persistent.",
"key_falsifier": "Decompose GDP and find Suez+tourism per capita are actually large enough that the binding constraint is not productivity/institutions but something else — that would refute the 'gross assets small per-capita + institutional trap' reading.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1tvsvqg/why_is_egypt_so_poor/"
},
{
"rank": 35,
"id": "1oyk88f",
"title": "Why is social security taxed?",
"score": 526,
"active_layers": [
"L1",
"L6"
],
"dominant_mechanism": "A tax-accounting/design question: taxing benefits is a means-graduated clawback equivalent to a lower net schedule, plus a historical financing-rule artifact.",
"scope_verdict": "TAUTOLOGY",
"reading": "This is essentially a definitional/accounting question about how the net benefit schedule is implemented — taxing benefits above income thresholds is arithmetically a way to means-test/claw back without rewriting the gross formula, and it routes revenue back to the trust funds. The OP's own 'why not just pay the net amount' is the answer: it is the same net outcome reached through the tax code (administrative/political path-dependence), so it touches the observation/accounting map, not any dynamic. Minor L1 trust-fund-financing flavor; no transport/block/reflexivity/criticality dynamics to model.",
"skill_horizon": "None (definitional/accounting).",
"key_falsifier": "N/A — definitional; the only check is the statutory thresholds and trust-fund routing, which are documented fact, not a prediction.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1oyk88f/why_is_social_security_taxed/"
},
{
"rank": 36,
"id": "1py8xoq",
"title": "Isn't the stat \"The top 1% pay over 40% of the Federal Income Taxes\" an overblown talking point?",
"score": 504,
"active_layers": [
"L6",
"L1",
"L0"
],
"dominant_mechanism": "A statistic-framing dispute: the 40% share, the income share, and the effective rate are three different observation operators on the same distribution, and the rhetorical force comes from picking one.",
"scope_verdict": "NEEDS-DATA",
"reading": "The OP has already done back-of-envelope L1/L6 work; resolving it requires the actual numbers (top-1% income share, federal-income-tax share, and — critically — share of ALL federal taxes including regressive payroll, plus the effective rate). The framework reading: '40% of income tax paid' and 'X% effective rate' are different H applied to one distribution, and the talking point's punch is operator-selection. Verifiable with fetched IRS/CBO data; there is an L0 'is it fair' valence resolved per block. Needs the cited figures to upgrade to MODELED.",
"skill_horizon": "None needed — a static distributional fact, fetchable.",
"key_falsifier": "Authoritative data show the top 1% effective rate and total-federal-tax share are both high relative to their income share — that would support (not refute) the talking point and refute the 'overblown' framing.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1py8xoq/isnt_the_stat_the_top_1_pay_over_40_of_the/"
},
{
"rank": 37,
"id": "1s8i4wk",
"title": "Why isn't the remaining 80% of global oil production enough?",
"score": 500,
"active_layers": [
"L1",
"L2",
"L4",
"L5"
],
"dominant_mechanism": "Oil demand is highly price-inelastic, so losing the marginal ~20% does not cut consumption 20% — it forces a large price spike to clear the market, amplified by a reflexive panic-hoarding channel.",
"scope_verdict": "MODELED",
"reading": "The '80% should be plenty' intuition ignores inelasticity: with steep short-run demand, a 20% supply loss clears not by everyone using 20% less but by a disproportionate price jump that rations demand, and the framework adds an L4/L5 reflexive layer — anticipation drives hoarding/futures spikes (attention concentration) that overshoot the physical shortfall. The 'societal free-fall' media framing is the criticality narrative; the honest reading is large price effect (modeled via inelasticity) but the recession-branch magnitude is data-dependent. Mechanism is cleanly modeled.",
"skill_horizon": "Structural for the price-mechanism; the realized magnitude has a short, data-gated horizon.",
"key_falsifier": "Short-run oil demand turns out to be elastic enough that a 20% supply loss clears with only a proportional ~20% price move and no overshoot — that would refute the inelasticity-amplification reading.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1s8i4wk/why_isnt_the_remaining_80_of_global_oil/"
},
{
"rank": 38,
"id": "1p3bp0u",
"title": "If you take a dollar bill and burn it, is that equivalent to giving 1 dollar to the federal government?",
"score": 496,
"active_layers": [
"L1",
"L6"
],
"dominant_mechanism": "Pure monetary-accounting identity: destroying base money marginally reduces liabilities/seigniorage in a way loosely analogous to the gift-card case, but routes through the central-bank balance sheet, not the Treasury.",
"scope_verdict": "TAUTOLOGY",
"reading": "This is a definitional/accounting question touching only H, not any dynamics. Burning a note retires a central-bank liability and confers a tiny seigniorage-style benefit, but the gift-card analogy is imperfect: the gain accrues to the monetary authority's balance sheet (and only indirectly the Treasury via remittances), and at the individual scale it is just forgone purchasing power. No transport, blocks, reflexivity, or criticality — per §5 recommend DROP from a dynamics-coverage run; the honest one-liner is 'approximately, by accounting identity, but to the central bank not the Treasury, and the effect is negligibly small.'",
"skill_horizon": "None (accounting identity).",
"key_falsifier": "N/A — definitional; the only correction is the balance-sheet routing, not a forecast.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1p3bp0u/if_you_take_a_dollar_bill_and_burn_it_is_that/"
},
{
"rank": 39,
"id": "1tni0we",
"title": "Why does the US stock market keep reacting to the President's announcements when they're clearly always bullshit?",
"score": 485,
"active_layers": [
"L4",
"L2",
"L3",
"L5"
],
"dominant_mechanism": "Announcements are reflexive control inputs: even non-credible cheap talk moves prices because each trader must act on what they expect OTHERS will do, making the reaction a coordination fixed point, not a belief in truth.",
"scope_verdict": "MODELED",
"reading": "This is the cleanest L4 reflexivity post in the batch: markets react not because the statement is believed true but because the payoff-relevant variable is the aggregate response, so traders front-run the expected reaction (Keynesian beauty contest / MFG fixed point). With a non-negligible-measure player (the President) as a genuine control input, even 'always bullshit' tweets carry option value on a small probability of being real, which is enough to reprice. The framework also flags the imitative/bistable regime: this is exactly where forecasting the branch fails and volatility is structural, not irrational. Stability erodes because announcements are unpredictable control inputs, lowering the skill horizon toward zero.",
"skill_horizon": "Near-zero for the branch (which way any given tweet moves the market) — structural for the mechanism (that announcements WILL move it).",
"key_falsifier": "Observe repeated identical announcements that stop moving prices entirely despite no change in their probability of being real — that would refute the 'expectation-of-others' reflexive-coordination mechanism in favor of pure naive belief.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1tni0we/why_does_the_us_stock_market_keep_reacting_to_the/"
},
{
"rank": 40,
"id": "1qpawsj",
"title": "If Jack Welch's strategy was ultimately unsuccessful, why do people keep trying to replicate it?",
"score": 485,
"active_layers": [
"L4",
"L0",
"L1",
"L3"
],
"dominant_mechanism": "Imitative dynamics with misaligned horizons: the strategy is a locally-dominant move in a principal-agent / short-horizon payoff game, so it is individually rational to copy even if collectively/long-run ruinous — a bistable imitation equilibrium.",
"scope_verdict": "PARTIAL",
"reading": "The puzzle dissolves under L4 imitation in the imitative (not monotone) regime: cost-cutting/shareholder-max delivers reliable short-horizon gains that are rewarded by the manager's actual payoff function (tenure, options, market applause) even when the firm's long-run value erodes — survivorship and attention concentration on Welch's peak (L2/L3 prestige-copying) reinforce it. This is a multiple-equilibria coordination problem where the privately-optimal branch differs from the socially-optimal one, so it is copied despite GE's collapse. There is an L0 valence on 'unsuccessful' (shareholders vs workers vs long-run firm read it oppositely) and an L1 accounting substrate; magnitudes (how often it succeeds vs fails) need data.",
"skill_horizon": "Structural for the imitation mechanism; firm-level outcome is branch-unpredictable (bistable).",
"key_falsifier": "Evidence that the Welch playbook reliably destroys shareholder value over the relevant manager horizon AND managers are penalized for it — that would remove the private incentive and refute the 'rational short-horizon imitation' explanation.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1qpawsj/if_jack_welchs_strategy_was_ultimately/"
},
{
"rank": 41,
"id": "1mfsig9",
"title": "Is it still possible to gather truthful economic data after trump fired the statistician?",
"score": 471,
"active_layers": [
"L6",
"L4",
"L1"
],
"dominant_mechanism": "This is an observation-operator integrity question: a major player perturbs H itself, so the issue is biased/adversarial observation, not the underlying dynamics Xi.",
"scope_verdict": "PARTIAL",
"reading": "Routes to L6 (data integrity half): the worry is that the observation operator y=H(Xi)+eps is being corrupted at source by an agent of non-negligible measure, not that the economy changed. Structurally, single-print manipulation is detectable because independent observers (private payrolls, surveys, market-implied measures, revisions) cross-check the official series; durable falsification requires capturing all of them, which is hard. L4 enters because cooked data is also a control input (reflexive signalling), but credibility erodes once the divergence from independent proxies is visible.",
"skill_horizon": "structural; no time horizon — a statement about observability, not a forecast of a trajectory",
"key_falsifier": "Official series continue to track independent private/market-implied proxies within historical revision bands (would show H integrity intact); conversely a persistent unexplained wedge would confirm capture.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1mfsig9/is_it_still_possible_to_gather_truthful_economic/"
},
{
"rank": 42,
"id": "1sbrjv5",
"title": "Did the CBO really find that adopting a single payer system in the US would comprehensively cover all Americans at a fraction of the administrative cost that currently exists in the US?",
"score": 463,
"active_layers": [
"L6",
"L1"
],
"dominant_mechanism": "A claim-verification plus stock-flow accounting question: does the cited CBO administrative-cost decomposition exist and does the dollar-flow arithmetic hold.",
"scope_verdict": "PARTIAL",
"reading": "L6 (verify the number against the cited 2020 CBO source) over an L1 stock-flow model of the healthcare-spending stock and its administrative-overhead leakage. The framework can model the structure — lower payer-side administration and monopsony procurement reduce the overhead fraction, an L1 comparative static — but the headline 'fraction of the cost' depends on the specific CBO option and assumptions, which is an acquired number with wide branch sensitivity. Total-cost outcome also hinges on utilization/induced-demand elasticities not in the admin-cost line.",
"skill_horizon": "structural comparative-static; no trajectory horizon",
"key_falsifier": "The cited CBO report's option does not show the claimed administrative-overhead reduction, or net total spending rises once utilization response is included.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1sbrjv5/did_the_cbo_really_find_that_adopting_a_single/"
},
{
"rank": 43,
"id": "1ll7677",
"title": "How true is it that American farms would be able to find American workers for the right wage instead of relying on undocumented migrants?",
"score": 457,
"active_layers": [
"L1",
"L0",
"L6"
],
"dominant_mechanism": "A labor-supply stock question: at some reservation wage domestic supply clears, so the real issue is the wage/price level and who bears it, not a binary 'won't work'.",
"scope_verdict": "PARTIAL",
"reading": "L1 stock-flow over farm labor: a labor supply curve always clears at some wage, so 'Americans won't do these jobs' is really 'not at the current undocumented-labor wage with these conditions'. Structure is clear — raising the reservation-wage clearing point raises labor cost, passed to prices or absorbed in margins/mechanization. L0 valence (fairness of poverty wages) splits by block. Exact elasticity of domestic supply and pass-through magnitude need L6 data.",
"skill_horizon": "structural; magnitude horizon needs the labor-supply elasticity",
"key_falsifier": "Historical wage-shock episodes (e.g. Bracero termination, post-enforcement local markets) show domestic supply did NOT respond at higher wages even after adjustment, breaking the clearing-wage claim.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1ll7677/how_true_is_it_that_american_farms_would_be_able/"
},
{
"rank": 44,
"id": "1ralt3g",
"title": "Is everyone really saving that little?",
"score": 448,
"active_layers": [
"L6",
"L1",
"L3"
],
"dominant_mechanism": "An aggregate-statistic question whose answer is a distribution, not a point: 'everyone' conflates a heavy-tailed savings distribution with its mean/median.",
"scope_verdict": "NEEDS-DATA",
"reading": "Routes to L6 — the question asks for a number (US savings rates / median savings) and the honest answer is a distribution shape, not a single figure. L1 supplies the mechanism: US higher gross incomes face higher consumption norms, healthcare/education/housing cost structures, and easier credit, so high income with low net saving is consistent. L3 matters because 'everyone' is not one block — savings behavior is highly heterogeneous across cohorts, so aggregate framing hides bimodality. Resolves to PARTIAL once distributional data is fetched.",
"skill_horizon": "structural once data acquired; no trajectory horizon",
"key_falsifier": "Distributional data showing US median savings/net-worth is NOT low relative to income (i.e. the low-saving claim is a tail artifact) would overturn the premise.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1ralt3g/is_everyone_really_saving_that_little/"
},
{
"rank": 45,
"id": "1ski1dy",
"title": "Is Donald Trump accelerating the US dollar's demise as the world reserve currency?",
"score": 441,
"active_layers": [
"L4",
"L3",
"L5",
"L1"
],
"dominant_mechanism": "Reserve-currency status is a coordination/network equilibrium (everyone holds dollars because everyone else does); the question is whether policy shocks move the system off that fixed point.",
"scope_verdict": "PARTIAL",
"reading": "L4 dominates: reserve-currency status is a self-fulfilling coordination fixed point with strong incumbency (deep markets, network externalities, no liquid alternative), so it is sticky and bistable, not monotone. L3/L5 ask whether enough blocks (central banks, trade invoicers) synchronize a move to tip the equilibrium — possible but slow, and the Yuan/Euro lack the depth/openness to be a Schelling point. Erosion-at-the-margin (de-dollarization in specific corridors) is real and modelable; wholesale 'demise' is a branch near a coordination cliff, not datable. L1 anchors via fiscal/debt fundamentals.",
"skill_horizon": "low-resolution multi-year; tau* short for the tipping branch (coordination = bistable, branch unpredictable)",
"key_falsifier": "A sustained, broad-based fall in dollar share of reserves AND invoicing AND debt issuance toward a single rival (not just diversification) would signal the fixed point breaking.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1ski1dy/is_donald_trump_accelerating_the_us_dollars/"
},
{
"rank": 46,
"id": "1ph25t0",
"title": "Why do social security benefits adjust annually with inflation, but minimum wage does not?",
"score": 441,
"active_layers": [
"L1",
"L4",
"L0"
],
"dominant_mechanism": "An institutional-design difference: SS COLA is statutorily indexed (automatic stabilizer) while the minimum wage requires discrete legislative action, a difference in the control architecture, not economics.",
"scope_verdict": "PARTIAL",
"reading": "Institutional question -> L1 plus qualitative incentive reasoning. The structural answer is the indexing mechanism: SS benefits carry a legislated automatic COLA (a built-in feedback controller), whereas the federal minimum wage is set by discrete statute with no auto-index, so it erodes in real terms between legislative acts. L4 explains why this persists — minimum wage is a contested coordination/distributional choice kept as a discretionary lever, while SS indexing is a credibility commitment to a large retiree block. L0 valence over who benefits from each design.",
"skill_horizon": "structural; no trajectory horizon",
"key_falsifier": "Evidence that the minimum wage IS federally auto-indexed, or that SS COLA is discretionary, would break the indexing-mechanism explanation.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1ph25t0/why_do_social_security_benefits_adjust_annually/"
},
{
"rank": 47,
"id": "1ljsdsn",
"title": "Would a tax plan like Zohran Mamdani cause wealthy New Yorkers to flee?",
"score": 423,
"active_layers": [
"L4",
"L1",
"L6",
"L3"
],
"dominant_mechanism": "A threshold/coordination migration question: out-migration is continuous in the tax delta, so the issue is whether this specific increment crosses a behavioral breakpoint, governed by the migration elasticity.",
"scope_verdict": "NEEDS-DATA",
"reading": "The premise (taxes generally don't drive millionaire exodus) is the prior; the question is whether a 2% income + corporate-rate increment is the marginal break. L1 stock-flow over the high-earner tax base with an L6 migration/avoidance elasticity is the core — the sign and size depend entirely on that fetched elasticity, which empirically is small for sub-national millionaire migration. L4/L3 add a mild reflexive/herding term (flight can be a coordinated expectation), but the literature shows weak responsiveness. Resolves to PARTIAL once the elasticity is cited.",
"skill_horizon": "structural once elasticity fetched; capped by elasticity uncertainty",
"key_falsifier": "Panel evidence of large net out-migration of top earners after comparable state/city tax increments (e.g. high-tax-state studies) would overturn the low-elasticity prior.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1ljsdsn/would_a_tax_plan_like_zohran_mamdani_cause/"
},
{
"rank": 48,
"id": "1mgcu0w",
"title": "If what Trump is doing for the U.S economy is not working. What would?",
"score": 409,
"active_layers": [
"L1",
"L0",
"L6"
],
"dominant_mechanism": "A slow-stock policy question (debt/deficit dynamics) entangled with a normative 'fix' framing whose target differs by block.",
"scope_verdict": "PARTIAL",
"reading": "L1 is the core: 'lowering the debt' is a stock equation requiring primary-balance improvement (revenue up and/or spending down) plus favorable r-minus-g; tariffs and regressive tax shifts don't structurally close it. The framework gives the shape — debt/GDP path depends on growth, rates, and primary balance — but 'fix the economy' embeds an L0 objective (whose welfare?) that splits by block, and concrete magnitudes need L6. No single dynamics-driven 'the answer'; the honest output is the stock identity and the trade-off frontier.",
"skill_horizon": "structural comparative-static; no trajectory horizon",
"key_falsifier": "A demonstrated policy mix that lowers debt/GDP without improving the primary balance or the growth-rate gap would break the stock identity framing.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1mgcu0w/if_what_trump_is_doing_for_the_us_economy_is_not/"
},
{
"rank": 49,
"id": "1qvem06",
"title": "Could we close the billionaire borrowing loophole?",
"score": 405,
"active_layers": [
"L1",
"L0",
"L4"
],
"dominant_mechanism": "A tax-design asymmetry (buy-borrow-die: unrealized gains back consumption but escape realization) that is closable in principle via mechanism choice, with behavioral response as the binding constraint.",
"scope_verdict": "PARTIAL",
"reading": "L1 over the realization-based income tax: the post correctly identifies a structural asymmetry where collateralized borrowing monetizes unrealized appreciation without a realization event. Closing it is a mechanism-design problem (deemed-realization on pledged assets, loan-as-realization, or mark-to-market for liquid holdings) — the structure is clear, and each option's yield depends on L6 (asset-liquidity, valuation, avoidance elasticity). L0 valence over fairness is the framing energy, but the engine answers the positive 'can it be designed' as yes-with-leakage. L4: any rule reshapes behavior (Lucas), so static revenue estimates overstate.",
"skill_horizon": "structural; magnitude needs avoidance-elasticity data",
"key_falsifier": "A formal showing that every realization-trigger design is either trivially avoidable or constitutionally/administratively infeasible would refute 'closable'.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1qvem06/could_we_close_the_billionaire_borrowing_loophole/"
},
{
"rank": 50,
"id": "1p1ma0n",
"title": "Why are people saying Russias economy is doing badly?",
"score": 404,
"active_layers": [
"L6",
"L1"
],
"dominant_mechanism": "Headline aggregates (GDP growth, inflation target) are a low-dimensional projection of H that hides war-economy composition; the perceived contradiction is an observation-operator artifact.",
"scope_verdict": "NEEDS-DATA",
"reading": "L6: the apparent paradox is that the chosen observables (1% growth, 4% inflation target) under-represent the state — military Keynesianism inflates GDP while crowding out civilian capacity, sanctioned access, labor shortages, frozen reserves, and fiscal-buffer depletion don't show in those two prints. L1 supplies the mechanism (war spending as a stock drain, deferred-cost accumulation). The honest answer needs fetched indicators (budget deficit, NWF balance, rates, non-defense output). Resolves to PARTIAL once acquired.",
"skill_horizon": "structural once data fetched; no clean trajectory horizon",
"key_falsifier": "Broad civilian-sector indicators (real non-defense output, household consumption, fiscal buffers) showing healthy non-war growth would validate the 'doing fine' read.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1p1ma0n/why_are_people_saying_russias_economy_is_doing/"
},
{
"rank": 51,
"id": "1q49qjf",
"title": "Why haven't weekly working hours gone drastically down in the past 100 years or so, despite drastic increases in productivity?",
"score": 397,
"active_layers": [
"L1",
"L0"
],
"dominant_mechanism": "Productivity gains split between leisure and consumption via an income/substitution choice; preferences and rising consumption norms (and bargaining/distribution) absorb most gains into output rather than fewer hours.",
"scope_verdict": "PARTIAL",
"reading": "L1 labor-leisure model: higher productivity raises the real wage, which has offsetting income (take leisure) and substitution (work more, leisure is now costlier) effects, so hours need not fall proportionally. Structurally, consumption aspirations ratcheted up, status competition is positional, and the productivity-wage gap (distribution) means workers didn't capture all gains. L0 enters because 'should we have more leisure' is a per-block valence. Hours DID fall substantially earlier (60->40); the slowdown is the preference + distribution story. Magnitude split needs data.",
"skill_horizon": "structural; no trajectory horizon",
"key_falsifier": "Evidence that real wages tracked productivity fully AND hours stayed flat purely from a backward-bending supply preference (not distribution) would refine the mechanism toward pure preferences.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1q49qjf/why_havent_weekly_working_hours_gone_drastically/"
},
{
"rank": 52,
"id": "1rabrz1",
"title": "Isn't property tax a tax on unrealized gains?",
"score": 393,
"active_layers": [
"L1",
"L0"
],
"dominant_mechanism": "A definitional/conceptual equivalence question: property tax is a levy on the asset's assessed value (a base-definition / accounting convention), structurally close to but not identical with a tax on the gain.",
"scope_verdict": "TAUTOLOGY",
"reading": "Largely a question about H, the definitional/measurement map: property tax is assessed on total market value (a stock), so when value rises the bill rises — functionally it already taxes the holder on appreciation they haven't realized, which is the conceptual point. The distinction from a 'wealth/unrealized-gains tax' is definitional: property tax bases on gross value not net gain, is local and rate-stable, and applies to an illiquid, observable asset. There is little dynamics here — it is a comparison of two tax-base definitions, not a forecast. The honest answer is the equivalence-with-caveats, an accounting/identity statement.",
"skill_horizon": "none — definitional, not a trajectory",
"key_falsifier": "Not falsifiable as dynamics; it is a definitional claim. A material structural difference (e.g. property tax legally bases only on realized improvements) would dissolve the equivalence.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1rabrz1/isnt_property_tax_a_tax_on_unrealized_gains/"
},
{
"rank": 53,
"id": "1nn7am1",
"title": "Why are Republican states generally poorer and more prone to wealth inequality than Democrat states in America?",
"score": 387,
"active_layers": [
"L6",
"L1",
"L0"
],
"dominant_mechanism": "A premise-laden correlational claim that first needs the number verified, then a confounded stock-level explanation (history, sectoral mix, urbanization), not a causal partisan one.",
"scope_verdict": "NEEDS-DATA",
"reading": "L6 first: the premise asserts a magnitude/correlation that must be measured and the direction of causality checked (cost-of-living-adjusted income often narrows or reverses the gap). L1 then supplies confounded structural drivers — historical legacies, urbanization/agglomeration, industry composition, education stocks — which co-vary with partisanship rather than being caused by it. L0 lurks because the framing is normatively loaded. Without the cited cross-state data and a CoL adjustment the causal claim is unsupported. Resolves to PARTIAL once measured.",
"skill_horizon": "structural once data fetched; no trajectory horizon",
"key_falsifier": "Cost-of-living-adjusted state income/inequality data showing no robust partisan gap (i.e. the effect is urbanization/CoL, not party) would overturn the premise.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1nn7am1/why_are_republican_states_generally_poorer_and/"
},
{
"rank": 54,
"id": "1rqg8nr",
"title": "What will happen if Strait of Hormuz remains blocked?",
"score": 384,
"active_layers": [
"L5",
"L1",
"L6"
],
"dominant_mechanism": "An exogenous supply shock to a chokepoint: a fast oil-price spike propagating through energy-dependent blocks, an externally-triggered (rate-induced) shock, not a slow bifurcation with early warning.",
"scope_verdict": "PARTIAL",
"reading": "L5 but with the honesty rail flagged: this is an exogenous/rate-induced shock (a chokepoint closure), NOT a slow B-tipping event, so early-warning variance/autocorr signals do NOT apply — the trigger is a discrete external event. Structure is clear: ~20-25% of seaborne oil and major LNG transits Hormuz, so a sustained block spikes prices, which propagates to import-dependent blocks (Asia hardest), stokes inflation and recession risk. Magnitude and duration depend on SPR releases, spare capacity, demand destruction, and how long it stays closed — L6 numbers. 'Global economy collapse' overstates; severe but bounded and policy-buffered.",
"skill_horizon": "short event-driven horizon; trajectory depends on duration (branch-sensitive)",
"key_falsifier": "A prolonged full closure that does NOT materially raise global oil/LNG prices (e.g. rapid rerouting/spare capacity fully absorbs it) would refute the shock-propagation reading.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1rqg8nr/what_will_happen_if_strait_of_hormuz_remains/"
},
{
"rank": 55,
"id": "1neyz6r",
"title": "Why is Canadian productivity so low?",
"score": 381,
"active_layers": [
"L1",
"L6"
],
"dominant_mechanism": "A productivity-level puzzle driven by slow capital/investment and industry-composition stocks (low business R&D and capital intensity, resource/real-estate tilt, weak competition), not a single cause.",
"scope_verdict": "PARTIAL",
"reading": "L1 over the productivity stock: leading structural candidates are low business investment per worker (capital shallowing), weak business R&D and ICT diffusion despite US-similar retail, a resource- and real-estate-heavy industry mix, small domestic market with limited competition, and interprovincial trade barriers. The framework organizes these as comparative statics on the capital/innovation stocks; which dominates is an empirical decomposition (L6). The post correctly rules out the easy answers, so the residual is a multi-factor stock explanation needing data to weight.",
"skill_horizon": "structural; no trajectory horizon",
"key_falsifier": "A growth-accounting decomposition showing Canadian capital-per-worker and R&D intensity match the US (i.e. the gap is pure TFP residual with no structural correlate) would break the capital-shallowing explanation.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1neyz6r/why_is_canadian_productivity_so_low/"
},
{
"rank": 56,
"id": "1onxzqn",
"title": "Why are most economists supporters of capitalism?",
"score": 380,
"active_layers": [
"L0",
"L6",
"L1"
],
"dominant_mechanism": "A normative-belief-distribution question resolved as the valence field across the economist block, plus the structural fact that the profession's models price decentralized allocation.",
"scope_verdict": "NORMATIVE-AS-VALENCE",
"reading": "L0 Normativity Rule: 'support capitalism' is a valence field, not an absolute, and the framing conflates 'market-based mixed economy' with laissez-faire. Per-block: the economist block reads markets positively because its training/models (price signals, gains from trade, incentive efficiency) make decentralized allocation the default, while acknowledging market failures (the same models justify intervention). The philosopher-vs-economist contrast is a difference in the objective function each discipline optimizes (efficiency/positive vs justice/normative). L6 would fetch the actual survey distribution (most economists favor regulated markets, not pure capitalism). Output the per-block valence, not a verdict.",
"skill_horizon": "structural classifier over (block, framing); no trajectory",
"key_falsifier": "Survey data showing economists do NOT disproportionately favor market allocation relative to the general public would overturn the valence claim.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1onxzqn/why_are_most_economists_supporters_of_capitalism/"
},
{
"rank": 57,
"id": "1ogzbh1",
"title": "How can the S&P500 return 8% annually but US GDP only grows 2-3%? Is this sustainable?",
"score": 363,
"active_layers": [
"L1",
"L6"
],
"dominant_mechanism": "A category reconciliation: equity total return (earnings growth + dividends + multiple + buybacks, global revenue, survivorship) is not the same quantity as domestic real GDP growth, so there is no paradox to explain.",
"scope_verdict": "PARTIAL",
"reading": "Partly definitional (an H/accounting clarification) and partly L1: the 8% vs 2-3% comparison conflates two different objects. Equity total return = real earnings growth + dividend yield + buybacks + valuation change, in nominal terms, from globally-diversified multinationals, with index survivorship — none of which equals US real GDP. The sustainable part of the gap is dividends/buybacks (cash return) plus nominal vs real; the unsustainable part would be permanent multiple expansion or a rising profit share, which are bounded. So 'sustainable' resolves to: the cash-return component yes, indefinite re-rating no. Magnitudes (profit-share path) need L6.",
"skill_horizon": "structural decomposition; no trajectory horizon for the sustainable cash component",
"key_falsifier": "A long-run decomposition showing S&P real return came mostly from permanent multiple expansion or ever-rising profit share (not earnings + payout) would flag it as unsustainable rather than reconciled.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1ogzbh1/how_can_the_sp500_return_8_annually_but_us_gdp/"
},
{
"rank": 58,
"id": "1pptx2t",
"title": "High US Salaries vs Scandinavian Welfare, Who Actually Ends Up Richer Over a Lifetime?",
"score": 359,
"active_layers": [
"L6",
"L1",
"L0"
],
"dominant_mechanism": "A lifetime net-resource comparison whose answer is a distribution conditional on the percentile, requiring fetched data on taxes, transfers, and the value of in-kind welfare.",
"scope_verdict": "NEEDS-DATA",
"reading": "Explicitly asks for empirical lifetime studies -> L6. L1 frames it: lifetime outcome = disposable income net of taxes PLUS the imputed value of in-kind benefits (healthcare, education, insurance) MINUS US out-of-pocket on those, and the answer flips with the percentile — the US median/top often ends richer in disposable terms while the bottom and risk-exposed do better under Scandinavian insurance. So there is no scalar answer; it is a distribution conditional on income rank and risk realization. L0 (which outcome is 'better') splits by block. Resolves to PARTIAL once the cited comparative studies are fetched.",
"skill_horizon": "structural once data fetched; no trajectory horizon",
"key_falsifier": "Comparative lifetime-wealth studies showing one system dominates at EVERY percentile (no rank-dependent crossover) would overturn the distributional answer.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1pptx2t/high_us_salaries_vs_scandinavian_welfare_who/"
},
{
"rank": 59,
"id": "1lggl7a",
"title": "What do you think will happen when Trump appoints a loyalist to the Fed Chair in 2026?",
"score": 357,
"active_layers": [
"L4",
"L1",
"L5"
],
"dominant_mechanism": "Central-bank credibility is a reflexive expectations anchor (a coordination fixed point); a loyalist appointment that loosens policy de-anchors inflation expectations, the Nixon/Burns analogue.",
"scope_verdict": "PARTIAL",
"reading": "L4 dominates: monetary policy works through anchored expectations, a self-fulfilling fixed point. A credibly-independent CB holds the low-inflation equilibrium; a perceived loyalist who eases for political reasons can shift the system to a high-expectations equilibrium (bistable/imitative regime), raising term premia and inflation expectations even before realized inflation moves — markets price the regime, not just the rate. L1 anchors the fiscal/rate stocks; L5 flags that de-anchoring can be a fast non-equilibrium transition once credibility breaks. The Nixon-Burns precedent is the structural template. Branch and timing are not datable; the direction is.",
"skill_horizon": "directional/structural; tau* short for the de-anchoring branch (reflexive, bistable)",
"key_falsifier": "A loyalist appointment followed by NO rise in long-term inflation expectations, term premia, or breakevens would refute the credibility-channel mechanism.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1lggl7a/what_do_you_think_will_happen_when_trump_appoints/"
},
{
"rank": 60,
"id": "1sxc5rj",
"title": "Why does it seem like America is able to infinitely spend money?",
"score": 356,
"active_layers": [
"L1",
"L4"
],
"dominant_mechanism": "Reserve-currency exorbitant privilege plus deep demand for safe dollar assets lets the US run large deficits at low rates — a slow-stock fiscal-capacity story bounded by, not exempt from, debt dynamics.",
"scope_verdict": "PARTIAL",
"reading": "L1 fiscal-capacity stock: the US sustains large deficits because global demand for dollar safe assets (reserve-currency privilege, deep liquid Treasury market) keeps borrowing costs low and lets it borrow in its own currency, so the constraint is the r-minus-g debt dynamic and inflation, not a hard budget line. L4 enters via the self-fulfilling 'safe asset' status — it holds because everyone treats Treasuries as the safe asset (a coordination fixed point, also the L45 reserve-currency link). 'Infinitely' is the misconception: the limit is inflation and confidence, not literal solvency. The Dutch contrast is the absence of that privilege and an own-currency printer.",
"skill_horizon": "structural; no clean trajectory horizon (the binding limit is a confidence/inflation tipping branch)",
"key_falsifier": "A sustained spike in real Treasury yields / falling foreign demand with no policy change would show the privilege eroding and the 'infinite spending' premise breaking.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1sxc5rj/why_does_it_seem_like_america_is_able_to/"
},
{
"rank": 61,
"id": "1rgl2gd",
"title": "Does the fact that America in 2025 has for the first time in 90 years net negative migration indicate a massive brain drain happening?",
"score": 350,
"active_layers": [
"L1",
"L6",
"L3"
],
"dominant_mechanism": "A slow-stock (human-capital flow) question gated on a single number — the composition, not just sign, of net migration.",
"scope_verdict": "NEEDS-DATA",
"reading": "Net-negative migration is a stock-flow drift on the labor/human-capital stock (L1), but 'brain drain' is a claim about the skill-composition of the outflow, which only L6 data resolves: a headcount drop driven by enforcement-induced low-skill exit is the opposite of a high-skill brain drain. The block layer matters because emigration concentrates in specific professional/national communities rather than diffusing uniformly. Until the composition number is fetched, the sign of the welfare effect is undetermined.",
"skill_horizon": "structural on the stock direction; the brain-drain branch needs the composition figure before any horizon applies",
"key_falsifier": "Decomposed migration data showing the outflow is dominated by low-skill/undocumented departures (or normal retiree expat flows) rather than high-human-capital workers.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1rgl2gd/does_the_fact_that_america_in_2025_has_for_the/"
},
{
"rank": 62,
"id": "1mlrjzl",
"title": "Are tariffs actually a tax on the consumer?",
"score": 343,
"active_layers": [
"L1",
"L6"
],
"dominant_mechanism": "Tariff incidence splits between consumer and foreign producer as a function of relative supply/demand elasticities — a comparative-statics result on a slow stock.",
"scope_verdict": "PARTIAL",
"reading": "The structure is fully modeled: incidence is shared by the standard elasticity rule, so the user's intuition is correct — inelastic-demand goods push incidence onto consumers, elastic-demand goods onto producers (L1). Which side bears more in any specific case is a magnitude that requires the actual elasticities and pass-through estimates (L6). The clean structural answer is 'it depends on elasticities, not no-ifs-ands-or-buts'; the empirical 2018-19 finding of near-complete pass-through is a data point, not a law.",
"skill_horizon": "structural/no horizon — comparative-statics holds whenever the elasticities do",
"key_falsifier": "Empirical pass-through studies showing tariff incidence is invariant to demand elasticity across goods (i.e. always ~100% consumer regardless of elasticity).",
"url": "https://www.reddit.com/r/AskEconomics/comments/1mlrjzl/are_tariffs_actually_a_tax_on_the_consumer/"
},
{
"rank": 63,
"id": "1r6sy65",
"title": "Why are wages so much lower in Europe/UK?",
"score": 333,
"active_layers": [
"L1",
"L3"
],
"dominant_mechanism": "Cross-country wage gaps are driven by differing institutional stocks (productivity, labor-market structure, public-vs-private pay setting) that bind tightly for high-skill professions and loosely at the wage floor.",
"scope_verdict": "PARTIAL",
"reading": "This is institutional L1 reasoning: doctor pay diverges far more than minimum wage because the high end is set by market scarcity, licensing cartels, and private financing (US) vs centralized public payor scales (EU), while the floor is anchored by similar subsistence/regulation in both blocks (L3). The structure explains the pattern — top-of-distribution pay tracks the financing model and bargaining structure, not aggregate productivity alone. Exact magnitudes (the $500k vs €200k gap after tax/debt/PPP) require data.",
"skill_horizon": "structural on the mechanism; magnitudes need PPP and sectoral-pay data",
"key_falsifier": "Evidence that European specialist-physician pay gaps vanish after PPP and net-of-debt adjustment, implying no structural institutional driver.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1r6sy65/why_are_wages_so_much_lower_in_europeuk/"
},
{
"rank": 64,
"id": "1omchky",
"title": "Is Gabe Newell's claim that 'piracy is almost always a service problem and not a pricing problem' true?",
"score": 333,
"active_layers": [
"L1",
"L2",
"L6"
],
"dominant_mechanism": "Piracy is a substitution decision where the effective price of the legal good includes friction (service quality), so convenience can dominate sticker price.",
"scope_verdict": "PARTIAL",
"reading": "Structurally, the legal product competes against free piracy on total cost = price + access friction; lowering friction (Steam/streaming) can beat lowering price, which is the kernel of truth in Newell's claim (L1). There is an attention/availability component — frictionless distribution concentrates demand on the legal channel (L2). Whether service 'almost always' dominates pricing is an empirical magnitude claim needing willingness-to-pay and pirate-conversion data (L6); the honest verdict is 'service is a real and often dominant margin, but the universal quantifier is unproven'.",
"skill_horizon": "structural on the substitution mechanism; the 'almost always' magnitude needs elasticity data",
"key_falsifier": "Natural experiments showing pirate-to-buyer conversion responds strongly to price cuts but not to service/availability improvements.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1omchky/is_gabe_newells_claim_that_piracy_is_almost/"
},
{
"rank": 65,
"id": "1tnbfk3",
"title": "Germany is #3 globally but grew only 10% in 10 years. As someone living here, it feels stuck. Is it just me?",
"score": 330,
"active_layers": [
"L1",
"L5",
"L6"
],
"dominant_mechanism": "Slow-stock stagnation: aging demographics, fiscal-rule-constrained investment, and an export/energy-dependent industrial model losing its input-cost advantage.",
"scope_verdict": "PARTIAL",
"reading": "The drivers are L1 stocks — demographic aging shrinking the labor stock, the Schuldenbremse capping public-investment flow, and an industrial model built on cheap Russian gas plus China export demand, both of which inverted. There is a mild L5 element (is the export model near a structural break rather than a temporary dip?), and the precise growth-decomposition needs data (L6). The structural answer: this is deeper than the energy shock — it is a stock-and-institution problem — but whether it tips into decline or reforms out is a branch, not a forecast.",
"skill_horizon": "structural on the diagnosis; the reform-vs-decline branch is not forecastable beyond near-term policy signals",
"key_falsifier": "Growth decomposition attributing the slowdown almost entirely to the transient energy shock, with demographics and investment contributing negligibly.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1tnbfk3/germany_is_3_globally_but_grew_only_10_in_10/"
},
{
"rank": 66,
"id": "1n6vwi7",
"title": "In France, employment protection makes firing hard — what effect does this have on the labor market?",
"score": 330,
"active_layers": [
"L1",
"L4"
],
"dominant_mechanism": "High firing costs raise the option-value cost of hiring, shifting the labor market toward insider protection, lower turnover, and dualization (temp/youth exclusion).",
"scope_verdict": "PARTIAL",
"reading": "Standard L1 comparative statics: raising the cost of separation raises the shadow cost of a new hire, lowering both firing and hiring flows and producing insider/outsider dualization — protected permanent insiders and a buffer of precarious temp/youth contracts. There is an L4 reflexivity element: firms anticipating the un-fireability re-optimize toward automation, fixed-term contracts, and reluctance to expand. The structure is well-modeled and signed; the magnitude of the youth-unemployment and productivity cost needs data.",
"skill_horizon": "structural on direction; magnitudes need French labor-flow data",
"key_falsifier": "Cross-country evidence that strict employment protection has no detectable effect on hiring rates, youth unemployment, or temp-contract share.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1n6vwi7/in_france_i_understand_its_very_hard_to_fire_an/"
},
{
"rank": 67,
"id": "1lhc8rs",
"title": "Why does US college cost so much?",
"score": 328,
"active_layers": [
"L1",
"L2",
"L6"
],
"dominant_mechanism": "Cost growth driven by subsidized-credit-fueled demand, inelastic prestige supply, administrative-cost (Baumol + bloat) accumulation, and declining state appropriation per student.",
"scope_verdict": "PARTIAL",
"reading": "Multiple L1 stock/flow channels compound: the Bennett-hypothesis loop where federal loan availability shifts demand into inelastic prestige supply, falling state funding per student shifting cost to tuition, and administrative cost accumulation (L1 + Baumol). An L2 element exists — prestige is a positional/attention good where concentration justifies price. Decomposing which channel dominates the post-1970s continued rise needs data (L6); the structure names the mechanisms but not their shares.",
"skill_horizon": "structural on the channels; relative weights need cost-decomposition data",
"key_falsifier": "Decomposition showing tuition growth is fully explained by genuine instructional-quality input-cost inflation, with no role for subsidized credit or administrative bloat.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1lhc8rs/why_does_us_college_cost_so_much/"
},
{
"rank": 68,
"id": "1putgf6",
"title": "New Mexico recently announced free universal child care. What do economists think about this policy?",
"score": 325,
"active_layers": [
"L0",
"L1",
"L6"
],
"dominant_mechanism": "A subsidy policy with a measurable fiscal cost (L1) and a value-laden 'good policy?' framing whose verdict splits by block.",
"scope_verdict": "PARTIAL",
"reading": "On L1, universal childcare is a stock-flow program: fiscal cost (here funded by a sovereign-wealth/oil-revenue stock unique to NM) against returns in female labor-force participation and child-development human capital — a generally favorable cost-benefit in the literature but contingent on the funding stock's durability. There is an L0 valence split (fiscal-conservative vs egalitarian blocks read it oppositely) and the magnitude of the LFP/cost numbers needs data (L6). The structural answer: plausibly net-positive, but its replicability hinges on NM's idiosyncratic Permanent Fund, not the policy alone.",
"skill_horizon": "structural on the cost-benefit shape; magnitudes and durability need NM fiscal data",
"key_falsifier": "Evidence that universal (vs targeted) childcare subsidies show no labor-force or child-outcome gains net of cost, or that the NM fund cannot sustain the flow.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1putgf6/new_mexico_recently_announced_that_they_will/"
},
{
"rank": 69,
"id": "1o54rfj",
"title": "Is there any merit to the claim that 'economists were wrong about Trump's tariffs'?",
"score": 312,
"active_layers": [
"L6",
"L4",
"L1"
],
"dominant_mechanism": "A claim about forecast accuracy that is settled by comparing predicted vs realized outcomes — an observation-operator/data question, complicated by reflexive forecasting.",
"scope_verdict": "NEEDS-DATA",
"reading": "At core this is L6: 'were economists wrong' is adjudicated by the realized inflation, growth, and trade-balance data against what was predicted, plus what counterfactual was claimed. There is an L4 wrinkle — many predictions were conditional ('if sustained, then'), and policy walk-backs change the realized path, so apparent 'wrongness' can be a moved goalpost rather than a model failure. Until the specific predictions and outcomes are pulled, the merit-of-the-claim is data-gated; structurally, consumer-incidence and deadweight-loss predictions remain robust.",
"skill_horizon": "none until the predicted-vs-realized data is fetched",
"key_falsifier": "A like-for-like record showing mainstream tariff predictions (inflation, incidence, growth) systematically diverged from realized data in the direction the critics claim.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1o54rfj/is_there_any_merit_to_the_claim_that_economists/"
},
{
"rank": 70,
"id": "1sm1r4l",
"title": "Doesn't it make sense for public transport to be free to use and completely tax funded?",
"score": 299,
"active_layers": [
"L0",
"L1",
"L6"
],
"dominant_mechanism": "Fare-free transit is a pricing/subsidy tradeoff: zero fares internalize positive externalities but remove the demand-rationing and revenue signal, raising congestion and fiscal load.",
"scope_verdict": "PARTIAL",
"reading": "L1 captures the core: fares serve rationing and revenue roles, so removing them shifts cost to the tax stock and can induce overcrowding and substitution from walking/cycling rather than cars — the externality case for free transit is real but the optimal subsidy is rarely 100% (cost-effectiveness often favors better service over zero fares). There is an L0 valence component (regressive-funding vs equity-access framings differ by block). The downsides the user asks for are structural; their magnitude (ridership elasticity, fiscal cost) needs data.",
"skill_horizon": "structural on the tradeoff; optimal fare level needs elasticity/cost data",
"key_falsifier": "Evidence that fare-free systems achieve large car-substitution and net welfare gains with no congestion or fiscal-sustainability penalty.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1sm1r4l/doesnt_it_make_sense_for_public_transport_to_be/"
},
{
"rank": 71,
"id": "1q15un1",
"title": "Is it accurate to say billionaires like Elon Musk aren't hoarding money because their net worth is tied into companies?",
"score": 297,
"active_layers": [
"L0",
"L1",
"L2"
],
"dominant_mechanism": "Distinguishing illiquid equity wealth (a claim on productive assets) from liquid hoarded cash — a stock-composition fact, wrapped in a valence dispute.",
"scope_verdict": "PARTIAL",
"reading": "The L1 fact is correct: billionaire net worth is mostly equity, a marketable claim on productive capital, not a vault of idle cash, so 'liquidate to end homelessness' misunderstands that selling transfers ownership and depresses price rather than unlocking face value. But the post overstates the rebuttal — equity is collateralizable (borrow-against-stock funds consumption) and concentration of ownership has real distributional and attention/power effects (L2). The L0 valence split is the live dispute: 'not hoarding' is structurally true, 'therefore unproblematic' is the per-block value claim the framework resolves as a table, not a verdict.",
"skill_horizon": "structural on the stock-composition fact; the 'is it fine' question is per-block valence",
"key_falsifier": "Showing that large-holder equity is in practice liquidatable at scale near mark-to-market value without materially moving price or control — collapsing the hoarding/equity distinction.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1q15un1/it_is_accurate_to_say_billionaires_like_elon_musk/"
},
{
"rank": 72,
"id": "1tcca1b",
"title": "Is the claim that Zohran Mamdani reduced a $12B deficit to zero without cutting services true, and is it replicable?",
"score": 294,
"active_layers": [
"L6",
"L1"
],
"dominant_mechanism": "A factual accounting claim about a specific budget gap and how it was closed — verifiable only by fetching the actual budget documents.",
"scope_verdict": "NEEDS-DATA",
"reading": "The truth of 'reduced $12B to zero without cuts' is pure L6: it requires the actual budget — whether the gap was a projected-out-year shortfall closed by revenue/reserves/accounting reclassification rather than a realized deficit, and whether 'no service cuts' survives scrutiny. Structurally (L1), legally-balanced-budget jurisdictions close gaps every year via revenue, reserves, and timing, so the headline is usually a framing of routine balancing, not a unique strategy. Replicability is undeterminable until the actual levers are identified from data.",
"skill_horizon": "none until the budget documents are pulled",
"key_falsifier": "Budget records showing the gap was a real structural deficit eliminated by durable spending efficiencies with no revenue increases, reserve draws, or out-year reclassification.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1tcca1b/is_the_claim_that_zohran_mamdani_reduced_a_12/"
},
{
"rank": 73,
"id": "1lq0f3i",
"title": "BBB Tax Cuts: how do these tax cuts help normal people all that much?",
"score": 290,
"active_layers": [
"L1",
"L0",
"L6"
],
"dominant_mechanism": "A distributional incidence question: the per-decile after-tax change is a stock/flow accounting result that the user has already tabulated.",
"scope_verdict": "PARTIAL",
"reading": "The user's own table is the L1 answer: the cuts are regressive in level — large gains concentrate at the top, the middle gets modest relief, and the bottom is net-negative once safety-net cuts and tariffs are netted in. There is an L0 valence layer ('help normal people' is a fairness frame whose sign differs by block) and the exact figures need source verification (L6). Structurally the distributional shape is clear from the incidence accounting; the question answers itself once 'help' is defined as net-of-offsets after-tax income.",
"skill_horizon": "structural on the distributional shape; exact figures need scored-incidence data",
"key_falsifier": "An independent distributional score showing the bottom quintiles gain materially after netting safety-net and tariff offsets, contradicting the tabled signs.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1lq0f3i/bbb_tax_cuts_can_someone_explain_to_me_how_these/"
},
{
"rank": 74,
"id": "1lqy8dj",
"title": "Per capita GDP in the US is $88k. Why don't people make more money?",
"score": 284,
"active_layers": [
"L1",
"L6"
],
"dominant_mechanism": "GDP-per-capita is not take-home pay; the gap is the accounting wedge of capital share, depreciation, intermediate non-wage uses, and the labor-share split.",
"scope_verdict": "PARTIAL",
"reading": "This is mostly an L1 accounting clarification with a near-tautological core: GDP/capita measures value added per person, but labor compensation is only ~55-60% of it, and the rest is capital income, depreciation, taxes, and retained earnings — every dollar does end up somewhere, but 'somewhere' includes capital and government, not only wages. Median income also sits below the mean because of right-skew. The structural answer is clean; the precise labor-share and median-vs-mean figures are L6 data. Not a pure tautology because the labor-share split is a real distributional dynamic, not just definitional.",
"skill_horizon": "structural/no horizon — an accounting decomposition that holds by construction",
"key_falsifier": "A reconciliation showing the GDP-to-median-wage gap cannot be accounted for by capital share, depreciation, taxes, and skew — implying missing/unexplained income.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1lqy8dj/per_capita_gdp_in_the_us_is_88k_why_dont_people/"
},
{
"rank": 75,
"id": "1pbpd7l",
"title": "How can renting property ever be cheaper than owning?",
"score": 284,
"active_layers": [
"L1",
"L4"
],
"dominant_mechanism": "Rent vs own is an asset-pricing/user-cost comparison where the landlord's return comes substantially from expected appreciation, so rent can sit below full ownership cost.",
"scope_verdict": "PARTIAL",
"reading": "The user's 'rent must cover all costs plus profit' intuition misses the L1 user-cost-of-capital point: a landlord's total return includes expected capital appreciation, so they can rationally rent below the owner-occupier's full carrying cost (mortgage interest + opportunity cost of equity + maintenance + taxes + depreciation) and still profit via the asset's price gain. Renting also strips the illiquidity and concentration risk the user noted. There is a mild L4 expectations element (rents/prices reflect anticipated appreciation). The structure fully explains how rent < own; which is cheaper in a given market needs local price-to-rent data.",
"skill_horizon": "structural on the user-cost mechanism; the local verdict needs price-to-rent ratios",
"key_falsifier": "Demonstrating that in markets with zero expected appreciation, rents still systematically exceed full owner user-cost — refuting the appreciation channel.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1pbpd7l/how_can_renting_property_ever_be_cheaper_than/"
},
{
"rank": 76,
"id": "1o3dckx",
"title": "Why is Europe losing relevancy in the Economy?",
"score": 283,
"active_layers": [
"L1",
"L5",
"L6"
],
"dominant_mechanism": "Relative decline driven by slow-stock divergence: lower productivity/tech-frontier investment, demographic aging, energy costs, and fragmented capital markets versus US scale.",
"scope_verdict": "PARTIAL",
"reading": "The GDP-share fall is largely an L1 relative-growth story — the US pulled ahead via tech-sector scale, deeper capital markets, and faster productivity, while Europe carries aging demographics, higher energy costs, regulatory/market fragmentation, and thinner venture/scale-up financing. Part of the headline share drop is also a currency/denomination artifact (L6 caveat: USD-denominated shares move with the exchange rate). There is a faint L5 question of whether this is a structural break; the diagnosis is structural, the decomposition into real-vs-FX and per-channel weights needs data.",
"skill_horizon": "structural on the divergence drivers; real-vs-currency decomposition needs data",
"key_falsifier": "Showing the share decline is overwhelmingly a USD-appreciation accounting effect that disappears in PPP or constant-currency terms.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1o3dckx/why_is_europe_losing_relevancy_in_the_economy/"
},
{
"rank": 77,
"id": "1qoyyig",
"title": "Is trickle down economics pretty much a lie?",
"score": 282,
"active_layers": [
"L0",
"L1",
"L6"
],
"dominant_mechanism": "A claim about whether top-end tax cuts raise broad growth/wages — an empirical magnitude question wrapped in a valence frame, plus an MPC/velocity argument.",
"scope_verdict": "PARTIAL",
"reading": "'Trickle-down' is not a model economists hold; the testable L1 content is whether supply-side top tax cuts boost aggregate growth and wages enough to broadly benefit lower deciles — the weight of evidence finds weak growth effects and rising top-share concentration, which is the kernel making the user's skepticism well-founded. The user's MPC argument (lower earners have higher marginal propensity to consume, so redistribution downward raises velocity/demand) is a real L1 channel, valid in demand-constrained regimes. There is an L0 valence frame and the magnitudes need study data (L6). Structurally: the redistribution-up-raises-all-boats claim is weakly supported; the verdict is 'mostly unsupported, not a literal lie'.",
"skill_horizon": "structural on the channels; the empirical strength needs tax-cut growth-incidence studies",
"key_falsifier": "Robust evidence that top-bracket tax cuts produce broad-based wage and growth gains that reach lower deciles more than equivalent bottom-targeted transfers.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1qoyyig/is_trickle_down_economics_pretty_much_a_lie/"
},
{
"rank": 78,
"id": "1tkkm6c",
"title": "Are Jeff Bezos' claims about taxing the bottom 50% realistic and what would be its effects?",
"score": 282,
"active_layers": [
"L6",
"L1",
"L0"
],
"dominant_mechanism": "The factual share-of-tax numbers are an L6 lookup (already partly done); the 'effects of zeroing bottom-50% income tax' is an L1 fiscal/incidence comparative static.",
"scope_verdict": "PARTIAL",
"reading": "The cited shares are L6 facts the user already sourced and are roughly right for federal income tax — but the framing is misleading because federal income tax is only ~42% of revenue; payroll, state, and consumption taxes fall heavily on the bottom 50%, so they are not near-untaxed overall. The L1 effect of zeroing their income tax is small lost revenue (the point Bezos makes) but the distributional and incentive effects depend on offsets. There is an L0 valence layer (fairness framings differ by block). Structure is clear; precise revenue-loss and total-incidence figures need the full data.",
"skill_horizon": "structural on the incidence logic; magnitudes need full tax-incidence (not just income-tax) data",
"key_falsifier": "Comprehensive incidence data showing the bottom 50% truly bear a trivial share of ALL taxes (not just federal income tax), validating the 'they barely pay' framing.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1tkkm6c/are_jeff_bezos_claims_about_taxing_the_bottom_50/"
},
{
"rank": 79,
"id": "1u1yn5y",
"title": "Why can't the Singapore economic model be replicated by developing countries today?",
"score": 275,
"active_layers": [
"L1",
"L3",
"L4"
],
"dominant_mechanism": "Singapore's path depended on non-replicable initial conditions (entrepôt geography, small scale, state capacity, Cold War timing) — a path-dependence/institutional-stock argument.",
"scope_verdict": "PARTIAL",
"reading": "L1/L3 institutional reasoning: Singapore combined idiosyncratic stocks — a strategic port chokepoint, city-state scale that makes top-down governance tractable, unusually high state capacity and low corruption, and favorable Cold War FDI timing — none of which a large, fragmented developing country can simply adopt. There is an L4 element (the 'developmental state' coordination equilibrium requires credible commitment most polities can't sustain). The structure explains non-replicability as path-dependence on initial conditions and scale, not policy secret; the question is institutional, so verdict is PARTIAL with magnitudes/counterfactuals unquantified.",
"skill_horizon": "structural on the non-replicability mechanism; no quantitative forecast",
"key_falsifier": "A large, populous developing country reproducing Singapore-level growth purely by copying its policies, with no comparable geography, scale, or state-capacity endowment.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1u1yn5y/why_cant_the_singapore_economic_model_lee_kuan/"
},
{
"rank": 80,
"id": "1s27xrf",
"title": "What's going to happen with the US national debt?",
"score": 275,
"active_layers": [
"L1",
"L5",
"L4",
"L6"
],
"dominant_mechanism": "Debt sustainability is a slow-stock trajectory (debt/GDP vs r-g) whose tail risk is a reflexive confidence/criticality event, not a mechanical default.",
"scope_verdict": "PARTIAL",
"reading": "L1 sets the baseline: debt sustainability turns on the r-g differential and primary balance, and a sovereign that borrows in its own fiat currency does not face involuntary default — the 'insolvent' headline misuses the term. The real tail risk is L5/L4: a reflexive loss-of-confidence event (rising rates → higher debt service → more issuance) is a critical, bistable transition, not a smooth forecastable path, and the likely realized path is inflation/financial-repression/restructuring-by-stealth rather than hard default. Current indicator values and the CBO trajectory are L6 data. Near this kind of confidence tipping the branch is not forecastable — only the rising-risk state is.",
"skill_horizon": "slow-stock trajectory forecastable years out; the confidence-tipping branch has near-zero horizon once approached",
"key_falsifier": "A disorderly hard default on USD-denominated US debt occurring without any prior inflation/repression channel — or debt/GDP stabilizing with no policy change despite an adverse r-g gap.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1s27xrf/whats_going_to_happen_with_the_us_national_debt/"
},
{
"rank": 81,
"id": "1osn5iu",
"title": "Why don't we just tax consumption instead of various income sources?",
"score": 274,
"active_layers": [
"L1",
"L4",
"L0"
],
"dominant_mechanism": "A comparative-statics fiscal claim (consumption vs income tax) gated by a political-economy coordination problem: the efficient design is unpublishable as policy because losing blocks veto it.",
"scope_verdict": "PARTIAL",
"reading": "L1 confirms the structural shape: a VAT does avoid the intertemporal investment distortion and raises compliance via supply-chain cross-checking, and a per-capita rebate can in principle restore progressivity. But 'why does no one campaign for it' is an L4 question, not an L1 one: the rebate makes the regressivity fixable on paper yet the transition redistributes visibly across blocks (asset-rich vs wage-poor, savers vs spenders) and the losing coalition is concentrated enough to block, so the equilibrium policy is not the efficient one. Magnitudes (optimal rate, rebate size, evasion delta) need data.",
"skill_horizon": "structural/no horizon (regime-stable comparative statics; political adoption is a bistable coordination branch, not forecastable)",
"key_falsifier": "A developed economy shifting to a VAT-dominant system with per-capita rebate and showing no investment-distortion gain or no compliance improvement over the prior income-tax regime.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1osn5iu/why_dont_we_just_tax_consumption_instead_of/"
},
{
"rank": 82,
"id": "1lyzv92",
"title": "When did \"socialism is when the gov't does stuff\" stop being a joke and how people actually interpret it?",
"score": 273,
"active_layers": [
"L0",
"L6"
],
"dominant_mechanism": "A definitional/labeling question about how a term maps to referents — it touches the observation operator H (what gets counted as 'socialism'), not the forward dynamics.",
"scope_verdict": "TAUTOLOGY",
"reading": "The user's textbook definition (socialism = worker ownership of the means of production; capitalism = private ownership) is correct as the analytic definition, and yes, state involvement is an orthogonal axis — you can have a market-socialist economy with little state, or a heavily-regulated capitalist one. The popular 'socialism is when the government does stuff' usage is a definitional drift in H, the labeling map, driven by Cold-War rhetorical conflation, not a claim about any system's dynamics. There is no transport, block, or criticality content to model; the answer is a clarification of the measurement convention plus a per-block note that the conflation is itself a valence marker.",
"skill_horizon": "none (definitional)",
"key_falsifier": "Demonstrating a rigorous, non-rhetorical economic literature that uses extent-of-government-activity as the defining criterion of socialism rather than ownership of the means of production.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1lyzv92/when_did_socialism_is_when_the_govt_does_stuff/"
},
{
"rank": 83,
"id": "1no9q00",
"title": "Is there ANY developed country that has \"solved\" housing?",
"score": 265,
"active_layers": [
"L1",
"L0",
"L6"
],
"dominant_mechanism": "Housing affordability is a slow stock-and-flow (supply elasticity vs demand/credit), and 'solved' is a valence threshold that different blocks set at different points.",
"scope_verdict": "PARTIAL",
"reading": "L1 gives the structure: affordability is set by the gap between housing supply flow (permitting + construction, constrained by land-use rules) and demand inflow (population, household formation, credit). Cases that come closest (e.g. high-elasticity-supply or strong-social-housing regimes) differ on those parameters, not on a magic policy. 'Solved' is an L0 threshold — owner blocks read rising prices as wealth, renter/young blocks read them as exclusion — so no single country reads as solved to all blocks. A cross-country ranking of price-to-income and supply elasticity is the L6 number that would sharpen 'closest to solved.'",
"skill_horizon": "structural (mechanism is regime-stable; specific-country ranking needs data)",
"key_falsifier": "A developed country with persistently flat real price-to-income in housing despite inelastic supply and rising credit — which would break the supply-elasticity mechanism.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1no9q00/is_there_any_developed_country_that_has_solved/"
},
{
"rank": 84,
"id": "1ruclib",
"title": "How long would the Hormuz Straits need to be shut for till oil reaches $200?",
"score": 264,
"active_layers": [
"L1",
"L6",
"L4",
"L5"
],
"dominant_mechanism": "A specific price magnitude driven by reserve-buffer drawdown stocks and by markets pricing in the expected duration — the answer is a number conditioned on a reflexive expectation.",
"scope_verdict": "NEEDS-DATA",
"reading": "The structure is clear: price spikes when the strategic-reserve buffer stocks (the user's own table) can no longer bridge the supply outage, and the market is currently pricing a short-conflict branch (L4 — the price IS the aggregate expectation of duration). But the actual $200 threshold is a number: it depends on the demand elasticity of crude, the true drawdown rates, spare OPEC capacity, and how much of the strait's ~20% of global flow is actually interdicted. Those must be fetched before any duration estimate is honest. Near a supply-shock tipping point (L5) the branch is amplified and not cleanly forecastable.",
"skill_horizon": "days-to-weeks at best, collapsing toward zero as the conflict approaches a criticality (price becomes branch-sensitive)",
"key_falsifier": "A prolonged (multi-month) full closure that fails to push Brent toward $200, indicating elasticity/spare-capacity buffers far larger than assumed.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1ruclib/how_long_would_the_hormuz_straits_need_to_be_shut/"
},
{
"rank": 85,
"id": "1oxkf5n",
"title": "Why do microfinance institutions have 90%+ repayment rates when borrowers have zero collateral and weak legal enforcement?",
"score": 263,
"active_layers": [
"L4",
"L3",
"L1"
],
"dominant_mechanism": "Repayment is sustained as a fixed point of a repeated game: progressive (escalating) lending and joint-liability blocks make the continuation value of future credit exceed the one-shot default payoff.",
"scope_verdict": "MODELED",
"reading": "This is a clean L4 reflexivity/repeated-game result. Bulow-Rogoff says a one-shot rational borrower defaults; the repair is that MFIs convert it into a repeated game where progressive lending makes each repayment a purchase of a larger future loan, so the discounted continuation value dominates the default payoff — the high-repayment state is a self-enforcing equilibrium, not an enforcement outcome. Joint-liability/group lending adds an L3 block layer: peers internalize each other's default risk, lowering the effective monitoring cost. The Dasgupta-Mookherjee progressive-lending account is one consistent fixed-point story; dynamic incentives are the accepted core. The 'why not the developed-country poor' puzzle resolves on the same model: the continuation value of small escalating loans is too low where larger formal credit is already accessible, so the equilibrium doesn't bind.",
"skill_horizon": "structural (the equilibrium is regime-stable while the repeated-game conditions — small loans, credible exclusion, durable lender — hold)",
"key_falsifier": "An MFI using strict progressive lending and group liability that nonetheless sees repayment collapse to Bulow-Rogoff one-shot-default levels without an exogenous shock breaking the repeated-game structure.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1oxkf5n/why_do_microfinance_institutions_have_90/"
},
{
"rank": 86,
"id": "1pimxpz",
"title": "Why was Paul Samuelson so Wrong about USSR?",
"score": 259,
"active_layers": [
"L6",
"L1"
],
"dominant_mechanism": "An observation-operator failure: the Soviet growth statistics fed into the textbook were biased/adversarial measurements of a latent economy that was stagnating beneath the reported aggregates.",
"scope_verdict": "PARTIAL",
"reading": "This is primarily an L6 data-integrity story. Samuelson's optimistic editions extrapolated official Soviet output series — measurements H(Xi)+eps where eps was systematically positive because the producing state was also the reporting state, and because gross-output targets masked quality, hidden inflation, and unsellable production. L1 supplies the missing mechanism: a command economy lacks the price signal that allocates capital efficiently, so measured 'growth' was input accumulation, not productivity, and it hit diminishing returns. The wrongness was shared (many Western economists trusted the same series) and the same measurement bias colored early reads of other command economies. Resolving 'how biased exactly' needs the revised post-1991 output reconstructions.",
"skill_horizon": "structural/retrospective (a diagnosis of past measurement failure, not a forward forecast)",
"key_falsifier": "Archival evidence that Soviet output statistics in the 1970s-80s were accurate and that the economy was in fact growing at the reported rates, which would shift the error from L6 to L1 model choice.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1pimxpz/why_was_paul_samuelson_so_wrong_about_ussr/"
},
{
"rank": 87,
"id": "1o919po",
"title": "Why is the military-industrial complex perceived as very powerful but it seems but a small 'industry'?",
"score": 259,
"active_layers": [
"L1",
"L2",
"L3"
],
"dominant_mechanism": "A mismatch between economic size (small L1 stock — market cap) and influence (concentrated L2 attention/political salience plus a cohesive L3 lobbying block).",
"scope_verdict": "PARTIAL",
"reading": "L1 confirms the premise: the top contractors are genuinely small by market cap relative to tech. But power and economic size are different operators. Influence is L2/L3: defense spending is geographically concentrated and salience-amplified (jobs in many congressional districts, single-buyer government dependence, revolving-door networks), so a small industry occupies an outsized share of political attention and forms a tight, low-N_eff lobbying block. Market cap also understates the flow — annual procurement budgets, not equity value, are the relevant stock, and much capacity sits in privately-held or diversified firms. Quantifying the influence-per-dollar needs lobbying and budget-share data.",
"skill_horizon": "structural (the size/influence decoupling is regime-stable)",
"key_falsifier": "Showing that defense-sector political influence scales with its market cap rather than with procurement-budget concentration and district-level employment — i.e. that the L2/L3 amplification isn't present.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1o919po/why_is_the_militaryindustrial_complex_perceived/"
},
{
"rank": 88,
"id": "1rrjxcv",
"title": "Does the US economy get any benefit from bombing Iran?",
"score": 259,
"active_layers": [
"L1",
"L6",
"L4"
],
"dominant_mechanism": "A net-flows accounting question (oil export gains vs cost-of-living and risk costs) confounded by a reflexive premise about who buys whose oil.",
"scope_verdict": "PARTIAL",
"reading": "L1 sets up the ledger, but the user's premise is partly mis-specified: the US is a net crude exporter only marginally and oil is a globally-priced commodity, so disrupting Iranian supply raises the world price the US consumer also pays — the cost-of-living channel works against the export-gain channel. A 'stronger dollar from oil sales' is not a clean mechanism; supply shocks typically raise prices and risk premia broadly. L6 is needed for the actual magnitudes (US net oil export position, price pass-through, conflict-risk premium). The honest structural answer is that any export benefit is small and likely swamped by higher input costs and instability, so net economic benefit is at best ambiguous and probably negative.",
"skill_horizon": "weeks (event-driven; price branch is shock-sensitive)",
"key_falsifier": "Data showing US real income rising on net during a Hormuz-region oil disruption — i.e. export-revenue gains exceeding the domestic price-pass-through cost — which would invert the sign.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1rrjxcv/does_the_us_economy_get_any_benefit_from_bombing/"
},
{
"rank": 89,
"id": "1qelqsy",
"title": "Europe Holds Trillions in US Treasuries. A coordinated European Sell-Off is a realistic scenario?",
"score": 259,
"active_layers": [
"L4",
"L5",
"L3",
"L1"
],
"dominant_mechanism": "A coordination game on a large reserve stock: a coordinated dump is a bistable equilibrium that is self-defeating because the seller eats its own capital loss and has no equivalent reserve substitute.",
"scope_verdict": "PARTIAL",
"reading": "This is an L4/L5 reflexivity-and-criticality question over an L1 stock. 'Coordinated European sell-off' presumes Europe is a single block (L3) — it is many holders (central banks, private funds, pension funds) with divergent incentives, so the effective N is not 1 and coordination is hard. Even coordinated, the action is largely self-defeating: dumping ~$2T crashes the price of the very asset being sold (mark-to-market loss to the seller), spikes EUR via FX, and lacks a deep enough alternative reserve asset to rotate into — so the dump equilibrium is unstable absent a non-economic (geopolitical) trigger. Magnitudes of price impact and the realistic coordinating fraction need data.",
"skill_horizon": "structural for the mechanism; near-zero for the branch (whether a geopolitical trigger fires is not forecastable)",
"key_falsifier": "A large coordinated official European Treasury sale executed without commensurate self-inflicted capital loss or FX backlash, showing a viable reserve substitute exists — which would make the dump a stable, not bistable-unstable, strategy.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1qelqsy/europe_holds_trillions_in_us_treasuries_around_2t/"
},
{
"rank": 90,
"id": "1opdldj",
"title": "If the rich tend to have their money invested, shouldn't someone's accumulated wealth not really matter to the rest of us?",
"score": 253,
"active_layers": [
"L1",
"L0",
"L4"
],
"dominant_mechanism": "A stock-vs-flow confusion: invested wealth does keep circulating (the user is right about the flow), but concentration matters via claims on real resources, valence, and the coordinated-divestment tail.",
"scope_verdict": "PARTIAL",
"reading": "L1 validates the core intuition: wealth is not a scrooge-mcduck hoard removed from the economy — invested capital funds businesses and recirculates, so the 'money sitting idle' worry is largely wrong. What concentration still buys is (a) a larger claim on future real output and decision rights (ownership = control, not just idle balance), (b) the user's own L4 point — synchronized divestment of a large holder is a coordination/criticality risk that the dispersed-circulation argument doesn't cover, and (c) L0 valence: egalitarian blocks read the claim-and-control concentration as unfair regardless of circulation. So the honest answer is: yes it circulates, but 'doesn't matter' is too strong because control rights, the tail-coordination risk, and per-block valence remain.",
"skill_horizon": "structural (regime-stable; the circulation fact and the control-rights caveat are both stable)",
"key_falsifier": "Evidence that concentrated equity ownership confers no disproportionate control over real-resource allocation and carries no coordinated-divestment systemic risk — reducing wealth concentration to a pure accounting label.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1opdldj/if_the_rich_tend_to_have_their_money_invested_or/"
},
{
"rank": 91,
"id": "1rmuy51",
"title": "If US consumers shouldered much of the tariff cost but importers are suing the gov't for the cost of tariffs... Is the US consumer not paying several times over?",
"score": 253,
"active_layers": [
"L1",
"L6"
],
"dominant_mechanism": "A tariff-incidence accounting question: who bears each leg (consumer pass-through, importer refund, taxpayer-funded litigation/interest) — partly a definitional double-counting check, partly a real magnitude.",
"scope_verdict": "PARTIAL",
"reading": "L1 incidence accounting untangles this. The consumer bears the tariff via price pass-through; if importers win refunds, that returns money to importers, not consumers, and the refund + accrued interest is funded from general taxation that consumers-as-taxpayers also fund — so there IS a real sense of paying on multiple legs, but it is not pure triple-counting: the first leg (higher prices) and the litigation/refund leg (tax-funded) hit different ledgers and different incidence shares, and refunds may or may not be passed back through to consumer prices. The exact double-burden magnitude needs the pass-through share, refund totals, and interest figures (L6). The structure is real; it's not merely a tautology because pass-through and refund-passthrough are behavioral, not definitional.",
"skill_horizon": "structural (incidence logic is regime-stable; magnitudes need data)",
"key_falsifier": "Evidence that tariff refunds are fully passed back into lower consumer prices, which would collapse the 'paying twice' framing into a wash.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1rmuy51/if_the_us_consumers_shouldered_much_of_the_tariff/"
},
{
"rank": 92,
"id": "1ou2m7n",
"title": "Trump has promised $1-2k in tariff rebate cheques: isn't this an insanely expensive way to buy support for protectionism of niche industries?",
"score": 252,
"active_layers": [
"L0",
"L4",
"L1"
],
"dominant_mechanism": "A normative 'insanely expensive way to buy support' judgment that resolves as a per-block valence field over a political-economy reflexive transfer.",
"scope_verdict": "NORMATIVE-AS-VALENCE",
"reading": "The 'insanely expensive / inefficient' framing is an L0 valence claim and is resolved per block, not in the absolute. Structurally (L1) the scheme recycles tariff revenue (itself a consumer-borne tax) back as visible cheques — a wash-to-negative in aggregate welfare given deadweight loss, so efficiency-minded blocks read it as negative. But it is an L4 political-economy move: protected-industry blocks and cheque-receiving households read it as positive (concentrated benefit + salient transfer), while diffuse-cost blocks barely perceive the loss. The 'buying support' verdict is exactly the predicted valence distribution: positive for protected + rebate-receiving blocks, negative for efficiency/fiscal-hawk blocks, near-neutral-perceived for the diffuse consumer who pays. Output is the table, not a ruling.",
"skill_horizon": "structural (valence map is stable while the protectionist coalition holds)",
"key_falsifier": "Survey/voting data showing the rebate generated no net political support among protected-industry or recipient blocks — which would break the L4 'buying support' mechanism.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1ou2m7n/trump_has_promised_12k_in_tarrif_rebate_cheques/"
},
{
"rank": 93,
"id": "1stqb7s",
"title": "Why didn't the US/West move manufacturing to allies like Mexico, Brazil, or India instead of China in the 1990s?",
"score": 251,
"active_layers": [
"L1",
"L3",
"L4"
],
"dominant_mechanism": "Path-dependent agglomeration: China's combination of labor-supply scale, state-built infrastructure, and a self-reinforcing supplier-cluster fixed point won over comparably-democratic but un-clustered alternatives.",
"scope_verdict": "PARTIAL",
"reading": "The premise — that Brazil/India had 'the same infrastructure' — is the error L1 corrects: China offered a far larger disciplined labor pool, deliberate state infrastructure investment (ports, power, special economic zones), and policy stability for exporters that the alternatives lacked at the time. The deeper mechanism is L4/L3 agglomeration: once a critical mass of suppliers co-located, each new entrant's best response was to join the existing cluster (a self-reinforcing fixed point with high switching costs), so the early lead compounded into a winner-take-most outcome that India/Mexico couldn't contest later. Quantifying the relative wage, infrastructure, and cluster-density gaps needs data.",
"skill_horizon": "structural (the agglomeration lock-in is regime-stable; it is now slowly eroding as costs rise)",
"key_falsifier": "Evidence that in the early 1990s Brazil/India matched China on labor scale, export infrastructure, and policy stability yet were passed over for non-economic reasons — which would shift the cause away from the agglomeration/L1 account.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1stqb7s/why_didnt_the_us_or_other_western_countries_move/"
},
{
"rank": 94,
"id": "1p98lc4",
"title": "If real wages and purchasing power are up since the 1950s, why do most households now need 2 incomes?",
"score": 251,
"active_layers": [
"L1",
"L6"
],
"dominant_mechanism": "Composition shift in the consumption basket: positional/inelastic goods (housing, education, childcare, healthcare) outran the broad real-wage index, so the median basket got more expensive even as average purchasing power rose.",
"scope_verdict": "PARTIAL",
"reading": "L1 dissolves the apparent paradox: aggregate real wages and purchasing power for tradable manufactured goods (cars, electronics, appliances) did rise, but the cost of positional and supply-constrained goods — housing near jobs, education, childcare, healthcare — rose far faster, and these are exactly the goods a household must buy. Two earners also bid up the very positional goods (housing) whose price is set by household, not individual, income — a partial L4 reflexive loop. Plus female labor-force participation rose for non-coercive reasons, so 'need' conflates choice and constraint. The precise decomposition (which basket components ate the gains) is an L6 data pull and would upgrade this toward MODELED.",
"skill_horizon": "structural (the composition-shift mechanism is regime-stable; magnitudes need data)",
"key_falsifier": "A real-wage-deflated basket that holds housing, education, childcare, and healthcare at constant shares and still shows the median single income unable to cover the 1950s-equivalent basket — which would move the cause off composition shift.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1p98lc4/if_since_the_1950s_realterm_wages_are_up_and/"
},
{
"rank": 95,
"id": "1pt2wou",
"title": "Why is Dubai so rich without oil?",
"score": 251,
"active_layers": [
"L1",
"L3"
],
"dominant_mechanism": "An institutional/stock story: Dubai converted early oil revenue and a deliberate regulatory regime (free zones, no income tax, logistics hub, property/finance) into a self-funding trade-and-services entrepôt — agglomeration plus rule-design, not a copyable trick.",
"scope_verdict": "PARTIAL",
"reading": "L1 institutional reasoning: Dubai's own oil is now minor, but it bootstrapped early oil money into ports (Jebel Ali), an airline/aviation hub, free zones with foreign-ownership and zero income tax, and a real-estate/finance sector — a services entrepôt whose income is trade, tourism, and capital flows, partly backstopped by Abu Dhabi's oil within the UAE federation. 'Why can't others copy it' has an L3/agglomeration answer: the model needs first-mover hub status, a stable rule-of-law-for-capital reputation, geographic position between East and West, and a federation backstop — a bundle that is hard to replicate once incumbents hold the network. Sustainability depends on continued capital-attraction and the regional oil backstop; exact fiscal dependence needs data.",
"skill_horizon": "structural (the entrepôt model is regime-stable while hub status and the federation backstop hold)",
"key_falsifier": "Fiscal data showing Dubai's economy is in fact directly oil-revenue-dependent rather than services/trade-funded, which would refute the diversified-entrepôt account.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1pt2wou/why_is_dubai_so_rich_without_oil/"
},
{
"rank": 96,
"id": "1pyzvf0",
"title": "I keep hearing that wages haven't kept up with inflation, is that true?",
"score": 249,
"active_layers": [
"L6",
"L1"
],
"dominant_mechanism": "A direct empirical magnitude question — the answer is a number (real-wage and component-cost time series) that L6 must fetch.",
"scope_verdict": "NEEDS-DATA",
"reading": "This is a clean L6 data-acquisition question: 'is it true' resolves only by fetching the real-wage series (nominal wages deflated by CPI) and comparing eras. The L1 structure to apply once the number is in hand mirrors rank 94: aggregate real wages have generally risen modestly, but specific baskets (housing especially) outpaced them, so the felt answer depends on which deflator and which decile. Until the median-real-wage and housing-cost-share figures are retrieved and cited, the honest verdict is NEEDS-DATA; with them it upgrades to PARTIAL/MODELED.",
"skill_horizon": "none until data fetched (then structural)",
"key_falsifier": "Authoritative real-median-wage data showing wages clearly outpacing a housing-weighted cost-of-living index across the compared period, contradicting the 'haven't kept up' claim.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1pyzvf0/i_keep_hearing_that_wages_havent_kept_up_with/"
},
{
"rank": 97,
"id": "1nkimiv",
"title": "Why is the US job market purported so badly online while the US has such a low unemployment rate?",
"score": 247,
"active_layers": [
"L6",
"L2",
"L3"
],
"dominant_mechanism": "An observation-operator mismatch: the aggregate unemployment number averages away block-level distress, and L2 attention concentrates the loudest negative experiences online.",
"scope_verdict": "PARTIAL",
"reading": "This is the canonical L6 'whose state is in this number' case. The 4.1% headline is a membership-weighted aggregate; it averages over blocks, so segments (recent grads, tech/white-collar after layoffs, gig/underemployed) can be in distress while the mean stays calm — the L3/L5 signal is washed out of the L6 print. Layer L2 explains the online skew: negative job-search experiences are high-salience and over-represented in feeds (rich-get-richer attention on grievance), so perceived conditions concentrate on the worst cases. The reconciliation is structural; quantifying the gap needs sector-level unemployment, underemployment (U-6), and hires/quits data.",
"skill_horizon": "structural (the aggregate-vs-block divergence mechanism is regime-stable)",
"key_falsifier": "Sector- and cohort-level labor data showing uniform health across all blocks (no concentrated pockets of high unemployment/underemployment), which would make the online narrative pure attention artifact with no real block signal.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1nkimiv/why_is_the_us_job_market_purported_so_badly/"
},
{
"rank": 98,
"id": "1lt944q",
"title": "Medicaid cuts from the BBB bill: how come a 10% cut in Medicaid be so catastrophic?",
"score": 243,
"active_layers": [
"L1",
"L5"
],
"dominant_mechanism": "A nonlinear threshold/cascade: a marginal cut to the payer concentrates on the operating margin of safety-net providers, so a small spending percentage triggers disproportionate coverage loss and hospital failures.",
"scope_verdict": "PARTIAL",
"reading": "The user's '2% of total health spend' framing is the L1 denominator error: the cut is ~10% of Medicaid, but it does not spread evenly across the $5T system — it lands on a specific stock (Medicaid enrollees and the providers most exposed to them). L5 supplies the nonlinearity: safety-net and rural hospitals run on thin margins where Medicaid is a large revenue share, so a cut that pushes them below break-even causes closures (a threshold effect), and coverage losses compound through eligibility-churn and work-requirement administrative friction rather than scaling linearly with dollars. So a small share of total spending maps to a large coverage/closure effect because the impact is concentrated and threshold-driven, not diffuse. Exact 16M-coverage and closure figures depend on the specific provisions and elasticities.",
"skill_horizon": "structural for the mechanism; the closure-cascade branch is threshold-sensitive (PARTIAL on magnitude)",
"key_falsifier": "Evidence that the cut is absorbed proportionally across providers with no margin-threshold concentration — i.e. coverage and hospital-solvency losses scale linearly with the dollar cut rather than nonlinearly.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1lt944q/medicaid_cuts_from_the_bbb_bill_that_just_passed/"
},
{
"rank": 99,
"id": "1r0uzks",
"title": "Why did Russia lose so much of its technological expertise after the collapse of the USSR?",
"score": 241,
"active_layers": [
"L1",
"L3",
"L5"
],
"dominant_mechanism": "A state-dependent capability collapse: Soviet high-tech was state-funded and concentrated in defense blocks, so when the funding stock and institutions evaporated the human-capital network dispersed (brain drain) faster than markets could rebuild it.",
"scope_verdict": "PARTIAL",
"reading": "The user's own hypothesis is largely the L1 answer: Soviet technological strength was state-driven, narrowly concentrated in defense/space, and not embedded in self-sustaining commercial firms, so when the funding stock collapsed the supporting institutions (design bureaus, research cities) lost their inflow. L3/L5 adds the network-collapse mechanism: expertise lives in connected teams, and the 1990s shock dispersed those blocks at once (emigration of skilled workers, sector exit, loss of supplier chains) — a critical de-synchronization where the human-capital network fell below the density needed to reproduce itself, which is far easier to destroy than to rebuild. Magnitudes (emigration counts, R&D spending drop) need data.",
"skill_horizon": "structural/retrospective (mechanism is regime-stable; it is a post-hoc explanation, not a forecast)",
"key_falsifier": "Evidence that Russian high-tech human capital and R&D institutions remained intact and funded through the 1990s, locating the capability loss in something other than funding/network collapse.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1r0uzks/why_did_russia_lose_so_much_of_its_technological/"
},
{
"rank": 100,
"id": "1tgq9kg",
"title": "Since 2019 California's GDP grew 40% vs 15.1% nationally. Reasons, and is it political leadership?",
"score": 237,
"active_layers": [
"L6",
"L1",
"L0"
],
"dominant_mechanism": "A decomposition-and-attribution question: the growth gap is mostly a sectoral-composition number (tech/AI concentration) that L6 must fetch before any political-leadership attribution (L0) can be tested.",
"scope_verdict": "NEEDS-DATA",
"reading": "The headline gap is real but the cause is an L6 decomposition before it is anything else: California's GDP is heavily weighted toward tech/software/AI and high-value services, which boomed post-2019 (and nominal figures partly reflect asset/valuation and price effects), so the gap is plausibly sector-composition, not policy. The 'is it political leadership' clause is an L0 attribution/valence question that cannot be answered until the growth is decomposed by sector and the counterfactual (how a similarly tech-heavy state under different leadership grew) is examined; absent that, attributing it to leadership is a prosecutor's-fallacy risk. Verdict is NEEDS-DATA: fetch the sectoral GDP decomposition and real-vs-nominal split, after which it upgrades to PARTIAL.",
"skill_horizon": "none until decomposition fetched (then structural)",
"key_falsifier": "A sectoral decomposition showing California's outperformance is broad-based across industries rather than concentrated in tech/AI — which would weaken the composition explanation and revive the policy-attribution hypothesis.",
"url": "https://www.reddit.com/r/AskEconomics/comments/1tgq9kg/since_2019_californias_gdp_has_grown_by_40_versus/"
}
]
};
