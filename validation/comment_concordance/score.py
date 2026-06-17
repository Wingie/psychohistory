# -*- coding: utf-8 -*-
import json
from extract import load, best_answer

BASE = "D:/code/psychohistory_v04_bundle"
posts = {json.loads(l)["id"]: json.loads(l)
         for l in open(BASE + "/.claude/skills/psychohistory/corpus/posts.jsonl", encoding="utf-8")}
models = {}
for l in open(BASE + "/validation/lethain_models.jsonl", encoding="utf-8"):
    d = json.loads(l)
    models[d["id"]] = d

# Manual verdicts from close reading of (model_conclusion vs extracted expert answer).
# (verdict, expert_gist <=1 line, justification: model claim vs expert claim).
# NA = retrieved comment is a mod/meta note or non-substantive reply -> no real vetted answer
#      recoverable from the snapshot.
V = {
 "1m11gep": ("DISAGREE", "ZhanMing: securities-backed loans don't avoid tax, only delay timing; collateralization is capped by volatility/margin-call risk -- the buy-borrow-die 'loophole' is overstated.", "Model frames wealth as a conserved carrier that inexorably concentrates (Pareto guaranteed); the expert deflates the very untaxed-compounding mechanism the runaway-concentration story leans on."),
 "1teyzn5": ("PARTIAL", "RobThorpe (mod note): anecdotes are useless; the real driver is aggregate productivity, not individual workplaces.", "Model decomposes wage into productivity x bargaining (matches 'it's a productivity question'); but the retrieved comment is a methodological mod note, not the full decomposition."),
 "1ncv5bf": ("DISAGREE", "econheads: Nvidia is NOT 2000 dot-com -- it already earns large profits and holds a dominant position; valuation reflects real expected AI growth.", "Model template 'concentration/bubble' implies Minsky bubble dynamics; the expert explicitly argues this is NOT a bubble."),
 "1lw2rdb": ("AGREE", "MachineTeaching: US is not Venezuela/Greece, borrows cheaply, no imminent collapse; debt is a long-run tax/spending question.", "Model: debt stock stabilizes/drains (sustainable, g>r). Expert agrees -- no collapse, manageable."),
 "1ok5wfc": ("PARTIAL", "urnbabyurn: hungry workers are LESS productive, which would lower labor demand and wages, not raise them -- against the 'SNAP subsidizes low wages' framing.", "Model's fiscal-capacity financing-wedge framing is orthogonal to the expert's wage-incidence point; loosely compatible (no free lunch) but not the same claim."),
 "1otrmkp": ("PARTIAL", "raptorman: there is NO economic barrier for the US to fund Denmark-style welfare; it's politics/preferences, not affordability.", "Model's draining-Treasury 'financing wedge' implies an affordability constraint the expert says is NOT binding (it's political will). Model over-weights a fiscal constraint."),
 "1qy91q0": ("NA", "Retrieved comment is a one-line aside ('cigarettes were cheaper on base'), not the substantive answer.", "No usable expert answer retrieved."),
 "1q37pg4": ("AGREE", "RobThorpe: Russia isn't collapsing -- sanctions evadable, oil sells to China/India, military-spending share not that high; slow grind not collapse.", "Model: slow stock drain (not collapse). Matches 'strained but not collapsing'."),
 "1qp0jvw": ("PARTIAL", "thri54: a weaker dollar makes exports competitive / imports dearer; Trump wants it to cut the trade deficit.", "Model is a generic stock-drain proxy -- captures directional pressure but not the export/trade-deficit mechanism."),
 "1p9y341": ("NA", "Retrieved comment is a moderator request for SEC-filing links, not an answer.", "No usable expert answer retrieved."),
 "1lcu5sg": ("PARTIAL", "HOU_Civil_Econ: revisions are normal and publicly announced (not manipulation); real concern is DOGE-driven data-quality loss.", "Model's fiscal-capacity template is off-topic to a data-integrity question; only loosely 'system under strain'."),
 "1otajn6": ("NA", "Retrieved comment (score 1) gives a generic incentive-plan rationale; plausibly an answer but low-signal and template-mismatched.", "Concentration/bubble template doesn't engage the shareholder-incentive question; treated as NA."),
 "1q9gmz7": ("AGREE", "No-Let-6057: 24h closures predate COVID (Walmart cut hours since 2015) to reallocate labor to stocking; COVID was a trigger, not the cause.", "Model: slow stock drain = a gradual margin/efficiency adjustment, matching 'long-run trend, COVID just a trigger'."),
 "1pe4wai": ("PARTIAL", "MachineTeaching: housing unaffordability is about zoning (SFH-only over ~75% of US), not immigration.", "Model fiscal-capacity template misses the zoning/supply mechanism the expert actually cites; only weak overlap that supply binds."),
 "1ndzf5p": ("NA", "Retrieved comment (score 1) is a narrow aside on Chinese licensing lotteries, not the main cost answer.", "No usable top vetted answer retrieved."),
 "1tuvg5m": ("PARTIAL", "MetaCalm: Canada's recession driven by US tariffs plus an immigration/housing slowdown after curbing inflows.", "Model generic stock-drain captures the 'contraction' direction only; no mechanism."),
 "1pirjdh": ("AGREE", "flavorless_beef: housing crises are about zoning/supply (construction stays low even post-shock, e.g. Spain).", "Model wage-decomposition's 'gap = supply/institutions' decomposition aligns with the zoning-constraint answer."),
 "1rwfndk": ("NA", "Retrieved comment is a tangent about students not knowing US oil rank, not the economic answer.", "No usable expert answer retrieved."),
 "1lqxmcq": ("AGREE", "welovepoots: 'there are no predictions, only models+assumptions that are inevitably wrong'; treat forecasts cautiously.", "Model explicitly claims direction-only, no specific mechanism -- the same epistemic humility the expert urges."),
 "1ou0ole": ("PARTIAL", "ReaperReader: GDP measures output, not quality-of-life; Japan's 'decline' is a GDP-vs-living-standard confusion.", "Model fiscal-capacity template doesn't capture the GDP-vs-QoL distinction; only loosely 'aggregate not as bad as headlines'."),
 "1qdegdr": ("AGREE", "flavorless_beef: economists never predicted recession-from-tariffs; consensus was 'hurts growth + raises prices', which happened.", "Model generic-stock-drain (gradual growth drag, not collapse) matches 'slower growth, no recession'."),
 "1n40vso": ("DISAGREE", "MachineTeaching: 2008 bailouts were asset purchases later sold back at a PROFIT (not free money); govts actually gave citizens cash (SNAP/EITC/rebates).", "Model generic-stock-drain offers nothing matching the expert's counterintuitive central claims (bailouts profitable, citizens got the cash); template is silent/non-concordant with the actual answer."),
 "1mp2mhc": ("AGREE", "flavorless_beef: most likely data quality degrades / some series stop, but outright fabrication is hard and would be caught.", "Model generic-stock-drain = gradual degradation, not catastrophic failure. Matches in direction."),
 "1rpjcdi": ("PARTIAL", "Particular_Dot: resource-curse -- oil lets the regime neglect/oppress citizens, so no broad development.", "Model generic-stock-drain captures 'stagnation' but not the resource-curse/institutions mechanism."),
 "1sski6f": ("PARTIAL", "Cutlasss: USPS inefficiency is real but privatization wouldn't fix it; the binding constraint is the universal-service mandate + lagging price regulation + falling volume.", "Model fiscal-capacity 'financing wedge' partly aligns (revenue squeeze vs mandated outlays) but misses that the prefunding/privatization framing is wrong."),
 "1ntscmb": ("DISAGREE", "MachineTeaching: the claim that cutting imports mechanically raises GDP is WRONG -- imports are subtracted precisely so they don't distort GDP.", "Model expectations-loop (anchored prices converge) neither captures nor supports the GDP-accounting correction the expert actually makes."),
 "1pakkzv": ("NA", "Retrieved comment is a moderation note about an insufficient source link.", "No usable expert answer retrieved."),
 "1tvsvqg": ("NA", "Retrieved comment (score -1) just quibbles with 'poor'; not a vetted answer.", "No usable expert answer retrieved."),
 "1py8xoq": ("PARTIAL", "No_March: per-capita GDP/income correlates ~0.9 with HDI/welfare; growth matters despite the talking-point framing.", "Model concentration template (1% concentration guaranteed) is tangential to the tax-share question; the expert defends growth, not concentration."),
 "1s8i4wk": ("PARTIAL", "Jeff_Skilling: oil allocation is about pipeline/storage/transport to settlement hubs, not country 'richness'.", "Model generic-stock-drain captures the scarcity/rationing direction but misses the infrastructure-bottleneck mechanism."),
 "1tni0we": ("AGREE", "Downtown-Art: markets react via Bayesian updating + an uncertainty premium; efficient over time even if noisy short-run.", "Model 'converges to equilibrium' reading matches 'noisy short-run, efficient/anchored long-run'."),
 "1qpawsj": ("PARTIAL", "CxEnsign: the 'Jack Welch strategy' = shareholder primacy + conglomerate empire-building; good for Welch, ambiguous for shareholders.", "Model generic-stock-drain (strategy ultimately erodes value) loosely matches 'less obvious it's good for shareholders', but no mechanism."),
 "1mfsig9": ("AGREE", "raptorman: dangerous territory; data quality already reduced; whether future data stays unbiased is genuinely unknown.", "Model generic-stock-drain (trust/quality draining) matches the 'erosion, uncertain' tone."),
 "1sbrjv5": ("DISAGREE", "isntanywhere: the spending pot is NOT fixed; single-payer 'savings' largely assume admin cuts do nothing (contested) or come from rationing care -- expenditure isn't welfare.", "Model fiscal-capacity FIXES the effective tax take / treats spend as a fixed draining pot -- exactly the fixed-budget assumption the expert says is wrong."),
 "1ll7677": ("NA", "Retrieved comment is an off-topic tangent about European tomato/strawberry prices.", "No usable expert answer retrieved."),
 "1ralt3g": ("AGREE", "MachineTeaching: high earners do save; net savings are highly unequal and negative for the bottom half (savings minus debt).", "Model concentration/bubble (carrier concentrates; bottom holds ~negative share) matches 'savings concentrated at top, negative at bottom'."),
 "1ski1dy": ("PARTIAL", "UpsideVII: some in Trump's cabinet (Miran) explicitly aimed to restructure the dollar's role, but unclear Trump personally is causing a 'demise'.", "Model debt-trajectory (sustainable) loosely supports 'not imminent demise', but the expert's answer is about stated policy intent, not debt math."),
 "1ph25t0": ("PARTIAL", "flavorless_beef: minimum wage already sits near the 10th percentile; even inflation-indexed it'd bind for a small share -- indexing matters less than assumed.", "Model expectations-loop (anchored prices) is tangential to the institutional-design question; weak overlap."),
 "1ljsdsn": ("PARTIAL", "No_March: NYC is small so flight is plausible; commercial-property-tax stress since COVID; hedged, no strong claim.", "Model concentration template predicts wealth stays/concentrates; the expert allows flight IS plausible for a small jurisdiction -- mild tension, hedged."),
 "1mgcu0w": ("AGREE", "ZhanMing: you can't raise ~8% of GDP in taxes overnight without devastating the economy; fixing the deficit takes generations of staged stabilization.", "Model's staged debt-stabilization view matches 'multi-generational stabilization'."),
 "1qvem06": ("DISAGREE", "Uptons_BJs: the buy-borrow loophole isn't actually a great strategy -- 2% APR compounds for life; selling + paying cap-gains often wins.", "Model concentration/bubble treats untaxed-borrowing concentration as structurally guaranteed; the expert deflates the loophole's potency."),
 "1p1ma0n": ("PARTIAL", "RobThorpe: Russia's situation isn't as bad as portrayed; sanctions evadable; complex picture.", "Model expectations-loop (anchored prices converge) loosely fits 'inflation high but not spiraling', but the expert's answer is about sanctions evasion, not anchoring."),
 "1q49qjf": ("PARTIAL", "ZhanMing: you CAN still buy lower-quality (old cars, shared housing); rising quality/standards absorbed productivity gains instead of hours.", "Model wage-decomposition (gains -> wages/consumption) loosely matches 'gains went to higher standards, not leisure'."),
 "1nn7am1": ("DISAGREE", "No_March: NOT convinced inequality is higher in red states; the poverty/GDP gap is mostly omitted-variable bias (rural vs urban density).", "Model concentration/bubble accepts the premise and asserts concentration as structurally guaranteed; the expert challenges the premise (a composition artifact)."),
 "1rqg8nr": ("NA", "Retrieved comment (score 1) lists transit/insurance specifics that read as fabricated; not clearly the vetted answer.", "No clearly-vetted expert answer retrieved."),
 "1neyz6r": ("NA", "Retrieved comment is a clarifying question ('was that due to the Great Recession?'), not an answer.", "No usable expert answer retrieved."),
 "1ogzbh1": ("AGREE", "RobThorpe: real stock returns (~7%) exceed GDP growth because total return = capital growth (tracks GDP) PLUS profits; sustainable, not a contradiction.", "Model's conclusion 'no contradiction, sustainable' aligns with the expert."),
 "1pptx2t": ("AGREE", "UpsideVII: the right measure is disposable income incl. in-kind transfers (OECD); defers to the data rather than a verdict.", "Model concentration template doesn't contradict; expert defers to data showing higher US disposable income. Mildly concordant."),
 "1lggl7a": ("AGREE", "No_March: the Fed chair is 1 of 12 FOMC votes; structurally hard to capture the committee short-term, by design.", "Model generic-stock-drain (bounded effect, not a sudden regime break) matches 'limited short-term effect, institutional buffering'."),
 "1sxc5rj": ("PARTIAL", "MachineTeaching: the 'infinite spending' framing is off -- the US spends far more than peers on healthcare/pensions; update priors.", "Model debt-trajectory (sustainable, borrows cheaply) partly aligns with 'US can spend a lot', but the expert's point is about high spending levels, not sustainability."),
 "1rgl2gd": ("PARTIAL", "MachineTeaching: US economic MOBILITY is low vs Europe; high inequality can imply low mobility -- reframes the brain-drain question.", "Model generic-stock-drain (net outflow = drain) loosely fits 'outflow', but the expert reframes toward mobility."),
 "1mlrjzl": ("DISAGREE", "syntheticcontrols: tariff incidence is split between consumer and producer per elasticity; not simply 'a tax on the consumer', and producers often substitute.", "Model fiscal-capacity treats the tariff as a clean revenue inflow (a pure tax take); the expert emphasizes shared/elastic incidence, against the pure-consumer-tax framing."),
 "1r6sy65": ("AGREE", "MachineTeaching: EU/UK lower wages tie to supply/demand & regulatory limits (e.g. doctor-supply caps differ); structural.", "Model wage-decomposition (productivity x institutions) matches the structural/institutional explanation."),
 "1omchky": ("AGREE", "ZhanMing: much piracy IS a pricing constraint in poor regions, but in the rich world the friction is the ownership/service experience -- Gabe right where conversion is possible.", "Model offers weak structure but its nuanced 'service problem where it matters' conclusion isn't contradicted."),
 "1tnbfk3": ("AGREE", "MachineTeaching: Germany's stagnation is significantly over-regulation burdening investment/expansion.", "Model generic-stock-drain (structural growth drag) matches in direction."),
 "1n6vwi7": ("PARTIAL", "MachineTeaching: firing restrictions bind because leaving/ignoring the law is costly (asset seizure, suits); firms run at a loss rather than break rules.", "Model generic-stock-drain loosely captures 'labor-market rigidity', no mechanism."),
 "1lhc8rs": ("NA", "Retrieved comment is just an NBER paper link with no text.", "No usable expert answer text retrieved."),
 "1putgf6": ("AGREE", "No_March: childcare is expensive but concentrated in the 20s-30s before peak earnings; a consumption-smoothing argument FOR public funding.", "Model fiscal-capacity (must be funded) doesn't conflict; both accept it's a financing question, expert adds a pro-policy nuance."),
 "1o54rfj": ("AGREE", "flavorless_beef: real economists predicted 'hurts growth + raises prices, not recession' -- borne out; the 'economists were wrong' article is weak.", "Model generic-stock-drain (growth drag, not collapse) matches the consensus the expert defends."),
 "1sm1r4l": ("AGREE", "TheDismal_Scientist: free transit mostly subsidizes people already riding; efficient only if externalities exceed cost; targeted subsidies are cheaper.", "Model fiscal-capacity 'financing wedge' (outlays must be justified by the base/benefit) matches the cost-benefit logic."),
 "1q15un1": ("DISAGREE", "No_March: rich people's saving/investment is a BOON when savings are below the Solow golden rule; you can't redistribute without destroying investment incentives.", "Model concentration/bubble frames concentrated wealth as a problematic runaway; the expert argues it is beneficial here -- opposite valence on the same fact."),
 "1tcca1b": ("PARTIAL", "ReaperReader: pushes back on a wages-only framing and on treating constraints as non-binding; emphasizes real resource constraints and living standards.", "Model debt-trajectory accepts that the deficit was fixed/sustainable; the expert is more skeptical of the framing."),
 "1lq0f3i": ("AGREE", "flavorless_beef: CBO/Yale -- BBB plus tariffs leaves bottom deciles worse off and only the top ~20% net ahead; the tax cuts are regressive.", "Model fiscal-capacity 'who-pays / financing wedge' framing matches the distributional answer."),
 "1lqy8dj": ("AGREE", "MachineTeaching: GDP IS a measure of income; with a stable labor share, per-capita GDP and wages correlate -- the gap is labor-share/distribution.", "Model wage-decomposition (output -> wage via a share/leak) is literally this mechanism."),
 "1pbpd7l": ("AGREE", "lawrencekhoo: rent~own in equilibrium; renting is cheaper when people expect falling real prices (e.g. post-1990s Japan).", "Model's 'converges toward an arbitrage equilibrium' reading isn't contradicted; expert gives the no-arbitrage condition."),
 "1o3dckx": ("AGREE", "flavorless_beef: EU 'decline' is largely a USD-vs-PPP artifact + slow population growth + catch-up growth elsewhere; real divergence only post-2008/COVID.", "Model generic-stock-drain (relative-share decline) matches 'gradual, partly mechanical relative decline'."),
 "1qoyyig": ("AGREE", "flavorless_beef: 'trickle-down' has no rigorous definition -- it's a political term, not an economic theory; the question is malformed.", "Model explicitly claims direction-only / no specific mechanism, mirroring the expert's 'no well-defined mechanism here'."),
 "1tkkm6c": ("PARTIAL", "ZhanMing: the US is very progressive vs peers; a Europe-style VAT would raise revenue more equitably and could tax the asset-rich like Bezos better.", "Model generic-stock-drain captures 'redistribution shifts a stock' only weakly."),
 "1u1yn5y": ("AGREE", "MachineTeaching: Singapore's success is policy AND being a trade hub that attracted industry; not replicable because the preconditions (location + state capacity) aren't.", "Model generic-stock-drain (path-dependent, can't be re-run) matches 'not replicable, preconditions matter'."),
 "1s27xrf": ("AGREE", "MachineTeaching: money-printing gives govts more OPTIONS but doesn't make default impossible; insolvency framing is roughly fine.", "Model debt-trajectory (manageable stock, options exist, not automatic collapse) matches."),
 "1osn5iu": ("PARTIAL", "ZhanMing: consumption is the least-inefficient tax and can be made as progressive as income tax; the obstacle is path-dependency/tracking, not principle.", "Model concentration/bubble (wealth concentrates) is tangential; the expert's answer is about tax efficiency/feasibility, not concentration."),
 "1no9q00": ("PARTIAL", "Meeedick (self-described aspiring): Japan 'solved' housing via permissive zoning / transit-oriented planning.", "Model fiscal-capacity template misses the zoning-supply mechanism; the retrieved comment is also explicitly non-expert."),
 "1ruclib": ("PARTIAL", "sandyflame: the premise is wrong -- the strait isn't fully shut; Chinese/Indian tankers still pass, so price hasn't spiked as expected.", "Model generic-stock-drain captures 'price pressure if blocked' but the expert rejects the blockage premise."),
 "1oxkf5n": ("AGREE", "UpsideVII: microfinance repayment works via 'group lending' -- social pressure/support substitutes for collateral.", "Model's conclusion (a self-enforcing social mechanism sustains repayment, not collapse) isn't contradicted."),
 "1pimxpz": ("AGREE", "gorbachev: Samuelson over-extrapolated early USSR industrialization under a resource-allocation paradigm that ignored incentives/information.", "Model generic-stock-drain (early growth stock that later stalls as the mechanism is misjudged) matches in direction."),
 "1o919po": ("AGREE", "handsomeboh: defense firms are deliberately NOT very profitable (you don't want them profiting off taxpayers); small market cap despite a large GDP share.", "Model generic-stock-drain (small captured value relative to flow) matches 'large spending, small captured profit'."),
 "1rrjxcv": ("AGREE", "ReaperReader: no, governments often do economically stupid, self-harming things; don't assume an economic upside to bombing Iran.", "Model generic-stock-drain (no positive accumulation; if anything a drain) matches 'no benefit, possibly a loss'."),
 "1qelqsy": ("DISAGREE", "Cutlasss: a coordinated EU Treasury sell-off would crash prices and the SELLER eats the loss (pennies on the dollar) -- it hurts Europe more than the US; not a credible self-fulfilling weapon.", "Model bank-run (Diamond-Dybvig) treats it as a canonical self-fulfilling run; the expert says run logic does NOT apply (seller-punishing, self-limiting)."),
 "1opdldj": ("PARTIAL", "MachineTeaching: concentrated wealth CAN matter (rent-seeking, political capture) when institutions are weak -- it's not harmlessly invested.", "Model concentration/bubble AGREES in direction ('it matters'), but its mechanism is pure accumulation vs the expert's political-economy channel."),
 "1rmuy51": ("AGREE", "floodcontrol: consumers bore tariff costs via prices; relief returns money upstream, not to consumers directly; blanket tariffs are bad policy.", "Model generic-stock-drain (cost flows through, consumer net-loses) matches 'consumer effectively pays, no clean refund'."),
 "1stqb7s": ("AGREE", "ZhanMing: nobody 'picks' a country; firms buy from the most competitive source; Brazil/India/Mexico were too dictatorial/socialist/small then, China had the best macro inputs.", "Model's conclusion (market-driven, China dominated on cost) isn't contradicted; concordant in direction."),
 "1p98lc4": ("AGREE", "MachineTeaching: 'need' is subjective; you need dual income LESS today for a 1950s lifestyle; higher real incomes raise both standards and costs and the opportunity cost of not working.", "Model expectations-loop ('total conserved; prices converge') fits 'real gains are real, costs rise because standards rise -- a stable reframe, not a spiral'."),
 "1pt2wou": ("NA", "Retrieved comment is a moderation note ('don't bypass top-level moderation'), not an answer.", "No usable expert answer retrieved."),
 "1pyzvf0": ("DISAGREE", "MachineTeaching: the 'cheap-TVs-mask-expensive-essentials' claim is NONSENSE -- the CPI is weighted by actual spend; housing+food+medical dominate the basket.", "Model expectations-loop ('prices converge to a stable equilibrium', wages roughly keep up) sits awkwardly against the expert's emphasis that essentials genuinely rose and the naive-offset story is false."),
 "1nkimiv": ("AGREE", "MachineTeaching: nothing wrong -- unemployment is low; the online doom is selection/echo-chamber; only the recent-grad market is slightly worse.", "Model's conclusion 'labor market basically healthy' isn't contradicted."),
 "1lt944q": ("AGREE", "probablymagic: ~8-12M lose coverage; states fund 40% so a $100B cut = $166B of spending; Medicaid is cheaper per enrollee, amplifying coverage loss.", "Model fiscal-capacity (a draining program budget with a cost-share/financing wedge) matches the federal/state arithmetic."),
 "1r0uzks": ("AGREE", "MachineTeaching: USSR tech 'loss' was protectionist props collapsing + brain drain enabled (not caused) by the fall; narrow military/space expertise didn't translate to growth.", "Model generic-stock-drain (a propped stock that drains once support stops) closely matches."),
 "1tgq9kg": ("AGREE", "Thinklikeachef (non-flaired): CA growth is about its industry mix (tech/AI/biotech winners + talent clustering + network effects), not current political leadership.", "Model generic-stock-drain (clustering of a growth stock, leadership-independent) matches the structural-industry-mix story."),
}

posts_l = [json.loads(l) for l in open(BASE + "/.claude/skills/psychohistory/corpus/posts.jsonl", encoding="utf-8")]
models_with = [pid for pid in models if (models[pid].get("model_dsl") or models[pid].get("model_template"))]

missing = [pid for pid in models_with if pid not in V]
assert not missing, ("UNJUDGED: " + str(missing))

out = []
for pid in models_with:
    m = models[pid]
    data = load(pid)
    ans, src = best_answer(data)
    verdict, gist, just = V[pid]
    out.append({
        "id": pid,
        "title": posts[pid]["title"],
        "expert_answer_gist": gist,
        "model_conclusion": (m.get("qualitative_result", "").strip() + " -- " + m.get("justification", "").strip()),
        "verdict": verdict,
        "justification": just,
        "_meta": {
            "answer_author": ans.get("author") if ans else None,
            "answer_score": ans.get("score") if ans else None,
            "answer_src": src,
            "old_validation": m.get("validation"),
            "model_template": m.get("model_template"),
        },
    })

with open("concordance.jsonl", "w", encoding="utf-8") as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

from collections import Counter
c = Counter(r["verdict"] for r in out)
print("TOTAL judged:", len(out))
print(dict(c))
print("real-answer posts (non-NA):", sum(1 for r in out if r["verdict"] != "NA"))
print("DISAGREE ids:", [r["id"] for r in out if r["verdict"] == "DISAGREE"])
