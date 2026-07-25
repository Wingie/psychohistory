# Round 3: the independent referee report on the LOGOS v0.3 structural pass

**Audit date:** 2026-07-25. **Stance:** adversarial, and independent of the process that wrote the v0.3 material.
**Scope:** `logos.tex` at commit `e8f9031`, `logos/LADDER_ARCHITECTURE.md`, `logos/GAPS.md`, `logos/PRIOR_ART_v03.md`, `logos/F9_PREREGISTRATION.md`, `logos/LOGOS_HARNESS.md`, `logos/TIER0_3090_PLAN.md`, read against `logos/REVIEW_ROUND2.md` for standard and format.
**Method:** every finding below was written by one pass and then handed to a second pass whose only job was to refute it. Findings that did not survive were dropped. Findings that survived weakened were downgraded and the weakening is recorded inline. Every number quoted as a recomputation was recomputed here, and every primary source quoted was fetched here.

---

## 0. Why this pass exists, and what it found that round 2 could not

Round 2 audited v0.2. Everything added at `e8f9031` is v0.3 material with no independent pass at all: `logos.tex` §3.3 (lineage), the second partition axis in §3.5, the three-case cost model in §11.1, the AIQ swap in §11.2, falsifiers F11 to F14, `GAPS.md` §4a, `LADDER_ARCHITECTURE.md` §1.5 and §5, `PRIOR_ART_v03.md` in full, and the `LOGOS_HARNESS.md` proposer interface. That material makes stronger structural claims than anything round 2 examined, and it was written fast by streams that mostly could not see each other's files. Round 2's opening said self-review is structurally blind to four defect classes. Three of those four are present again, and two new classes appear.

**New class one: a conditional result that hardens into a settled one as it propagates across files.** `logos.tex:247` states the lineage arithmetic correctly, with the quantifier that makes it true: a 98 percent common seed "is **one way** to guarantee" the residency fraction the data wall needs. `LADDER_ARCHITECTURE.md:144` states the supply-sensitivity honestly: "the trilemma is not a theorem about architectures. It is a function of which token-supply estimate is believed." Between those two correct sentences sit five restatements that drop both qualifiers, escalate to "no setting of `g` satisfies X-04, C-02 and F-04 at once", call it "the sharpest result in the programme", declare it "settled by arithmetic rather than by measurement", and then use it to take an architectural decision (`LADDER_ARCHITECTURE.md:152`, response 1, drop the diversity budget). **The register of record is the most careful document in the repository and the companions that amplify it are the least.** That is R-01.

**New class two: a gate that certifies nothing, because it passes by construction.** The harness installs five pre-run VOID conditions to protect F9. Three of them do not bind. The Phase-4 yield gate is an algebraic identity in Jensen-Shannon divergence and cannot fail (H-02). The S5 competence gate passes a uniformly random proposer with probability 0.4954 and is scored on the endpoint's own control battery (H-05). The check-2 fidelity audit is unattainable at its stated pass condition and insufficient at the rate it can actually certify (H-08). Round 2 had no gates to audit because the proposer interface did not exist. It exists now and its safeguards are the weakest part of it.

**The other two CRITICALs are arithmetic and corpus construction.** `logos.tex:613` says that after §2.2, §2.3 and §11.4 eroded the compute, token-fragmentation and data-wall motivations, the cost argument is the one thing left that "can be checked against an invoice". §11.1 case 3 is that argument and it derives a **capacity** conclusion from a **memory** proportionality; under the paper's own Proposition 1 convention it recovers none of the multiplexing loss it claims to recover (A-01). And the single loss-bearing free-text span in F9's training corpus has no specified generator, while the file's own exemplar of it states the adjudication the loop is about to make, and states it incorrectly (H-01).

**What round 3 did not find.** No hallucinated citation. No arithmetic error in §11.2's four defects of eta, in the PiKV collision analysis, in the size-axis cost arithmetic, in the MXFP4 density chain, or in the F9 cost ledger's headline components, every one of which reproduces. The honest-status language has not softened; `logos.tex:34`, `:880` and `LADDER_ARCHITECTURE.md:1131` are blunter than v0.2's. §6 lists the clean area in full, because a review that lists only faults is not useful and here it is large.

**Thirty-seven findings survived: 3 CRITICAL, 10 HIGH, 14 MEDIUM, 10 LOW.** Fifteen candidates were dropped after refutation and the seven most instructive are recorded in §7, including two where the brief that commissioned this review was itself wrong.

---

## 1. Severity index

Stream key: **R** the over-constraint result, **A** arithmetic, **F** falsifier construction, **H** harness and pre-registration, **P** prior art, **X** cross-file consistency.

| # | Finding | Severity | Where |
|---|---|---|---|
| R-01 | The over-constraint result is conditional on a point estimate from a factor-of-ten interval and on a bound read as an equality; five of seven restatements drop both qualifiers, and an architectural decision is taken on it | **CRITICAL** | `LADDER_ARCHITECTURE.md:16`, `:138`, `:142`, `:485`, `:1075`; `GAPS.md:138`, `:148` vs `logos.tex:247`, `LADDER_ARCHITECTURE.md:144` |
| A-01 | §11.1 case 3 derives a capacity conclusion from a memory proportionality; under Prop. 1's fixed sparsity it recovers none of case 2's multiplexing loss | **CRITICAL** | `logos.tex:609`, `:617`, `:925` vs `:127` |
| H-01 | The one loss-bearing free-text span in F9's corpus has no specified generator, and the file's own exemplar of it states the adjudication and states it wrongly | **CRITICAL** | `LOGOS_HARNESS.md:401`, `:427` vs `:141` |
| H-02 | The Phase-4 yield gate is an algebraic identity in Jensen-Shannon divergence and cannot fail; the VOID condition certifies nothing | **HIGH** | `LOGOS_HARNESS.md:546` |
| H-03 | Nothing in the parity checks tests anteriority; a card carrying the previous turn's verdict passes all three | **HIGH** | `LOGOS_HARNESS.md:293`, `:297`, `:301-307` |
| H-04 | The two proposer renderings are not in information parity and only one is gated; R-frame carries about 3.3 bits more per HP field | **HIGH** | `LOGOS_HARNESS.md:299`, `:309` vs `:297` |
| H-05 | S5 passes a random proposer half the time, is a forking path under an unfrozen roster, and is scored on the endpoint's own subtrahend | **HIGH** | `LOGOS_HARNESS.md:546`, `:283`, `:147` vs `:571` |
| P-01 | MatFormer claims and measures cross-size KV-cache sharing in its main text; the "unclaimed adjacency" verdict rests on a false negative about its own named neighbour | **HIGH** | `PRIOR_ART_v03.md:64`, `:78`, `:223` |
| F-01 | F13 limb (b)'s kill condition as printed in the paper is what the theorem the paper cites and accepts already predicts | **HIGH** | `logos.tex:915`, `:737`, `:1097` vs `LOGOS_HARNESS.md:81` |
| F-02 | F11's claim is the proposition §3.5 has already refuted by argument, and the threshold its kill condition names does not exist | **HIGH** | `logos.tex:911` vs `:271` |
| A-02 | §9.2's advantage requires each tower's pool to be a single low-latency locality; §9.1 says the reference deployment is a peer network and case 3 makes the dominant pool 192 accelerators | **HIGH** | `logos.tex:514`, `:516`, `:619` vs `:496`, `:609` |
| X-01 | Six figures disagree across five files, and three documents assert a disagreement with the paper that the paper no longer has | **HIGH** | `GAPS.md:10`, `:43`, `:50`, `:162`, `:165`; `F9_PREREGISTRATION.md:697`; `TIER0_3090_PLAN.md:89` vs `logos.tex:915` |
| F-03 | F10's restated AIQ criterion is not computable as stated: the cost domain renormalises across the swap, the CPT half contradicts the same subsection, and 0.02 sits below the per-slice standard error | **HIGH** | `logos.tex:673`, `:907` vs `:663`, `:648` |
| H-06 | Study 2 charges a 3x per-seed corpus multiplier that the FROZEN §5.3 rule forbids, and its A0 arm duplicates three Study 1 runs; 141 GPU-hours overcharged | **MEDIUM** | `F9_PREREGISTRATION.md:450`, `:496`, `:716` vs `:279`, `:283`, `:333` |
| H-07 | §8.4 banks a prefix-caching saving that §8.1 explicitly refuses to bank; 17.4 is 2x sensitive to it | **MEDIUM** | `F9_PREREGISTRATION.md:607` vs `:477` |
| H-08 | Check 2's pass condition is unattainable and its certifiable rate is insufficient; check 3 is vacuous under its natural instantiation | **MEDIUM** | `LOGOS_HARNESS.md:304`, `:305` |
| H-09 | `p_outcome` by "constrained decoding over single-token category labels" is not computable over a label set containing two-word labels | **MEDIUM** | `LOGOS_HARNESS.md:139` vs `:161` |
| H-10 | Neither exemplar trace's `yield` reproduces from its own printed vectors, and `o_observed` is not recoverable from the trace | **MEDIUM** | `LOGOS_HARNESS.md:433`, `:470`, `:424` |
| H-11 | The Tier-0 total is labelled at the 1B-class instantiation and contains an 8B-class line; "the same models F9 already loads" is false on two of three roster attributes | **MEDIUM** | `TIER0_3090_PLAN.md:157-167`, `:88`, `:105`, `:198` |
| A-03 | §9.2's correction is undone two sentences later: 960:1 is re-used as the reason for a latency property immediately after being retired as a latency ratio | **MEDIUM** | `logos.tex:516` vs `:512` |
| A-04 | §9.2 flags the insensitivity it has (layer count) and not the sensitivity it has (round-trip time); the crossover is about 1.7 ms and intra-datacentre dispatch is 17 to 24 microseconds | **MEDIUM** | `logos.tex:508`, `:510` |
| A-05 | §11.1's 21.9 GB per accelerator is computed at the flat-four-bit density §7.1 corrects; the true figure is 23.2 GB and all three derived percentages move | **MEDIUM** | `logos.tex:595` vs `:442` |
| X-02 | §11.1 computes on five towers, §3.5's criterion returns four, and the conclusion prints the five-tower "two thirds idle" as its headline; the four-tower figure is 58 percent | **MEDIUM** | `logos.tex:925`, `:607` vs `:271`; `LADDER_ARCHITECTURE.md:403` |
| X-03 | §11.1's comparator is a domain tower replicated and then used as a generalist; `LADDER_ARCHITECTURE.md:411` says it is not a competitor at all while `:403` says both instantiations are correct | **MEDIUM** | `logos.tex:599`, `:609` vs `LADDER_ARCHITECTURE.md:403`, `:411` |
| F-04 | F14 is uninterpretable unless F13 limb (a) first returns a nonzero lineage effect; both are budgeted as one rung with no conditional ordering, and a null F14 would read as support | **MEDIUM** | `logos.tex:915`, `:917`; `LOGOS_HARNESS.md:81` |
| F-05 | F12's kill condition is decided by an unstated choice within the survey's own 90 percent interval | **MEDIUM** | `logos.tex:913`, `:719` |
| P-02 | The Saunshi evidence table mixes two comparators inside one column and none of its derived percentages reproduces | **MEDIUM** | `PRIOR_ART_v03.md:106-114` |
| P-03 | "AIQ has no ratio" is false against the formula the same document reproduces, and §7.11's retraction of boundedness is not carried into the recommendation | **MEDIUM** | `PRIOR_ART_v03.md:168`, `:177` vs `:145`, `:295` |
| H-12 | The Phase-4 gates are declared Phase-0-only and two of the three parity checks they depend on are not | **LOW** | `LOGOS_HARNESS.md:551` vs `:307`, `:303` |
| H-13 | The MFU band on the F9 rung is stated three ways and none reproduces; the pre-registration's band is the superseded total rescaled | **LOW** | `F9_PREREGISTRATION.md:39`, `:690`; `TIER0_3090_PLAN.md:176-178` |
| H-14 | "The items are the ones already sealed" is asserted for a file that does not exist, in a document whose §11 says nothing has been lodged | **LOW** | `F9_PREREGISTRATION.md:606`, `:157` vs `:10`, `:664-676` |
| H-15 | The 94-window lifetime yield sums to 93 from its own breakdown | **LOW** | `LOGOS_HARNESS.md:363`; `logos.tex:809` |
| H-16 | The MDE 0.42 is quoted at an admitted N of 20 to 30 where it belongs to N = 35; the true range is 0.45 to 0.56 | **LOW** | `LOGOS_HARNESS.md:371`, `:602` |
| X-04 | `logos.tex`'s title block still reads "Draft v0.2" while four companions call the same file v0.3 | **LOW** | `logos.tex:20` vs `LADDER_ARCHITECTURE.md:16`, `GAPS.md:123` |
| A-06 | "Every input is a property of the analysis rather than an estimate" is contradicted in the same sentence by two estimates | **LOW** | `logos.tex:809` |
| P-04 | The two load-bearing negative-result sentences cite search-string counts that do not match §6, in opposite directions | **LOW** | `PRIOR_ART_v03.md:72`, `:195` vs `:238-251`, `:268-271` |
| P-05 | "All seven papers above" points at a section containing ten, inside the instruction that governs the citation obligation | **LOW** | `PRIOR_ART_v03.md:85` vs `:76-81` |
| P-06 | "Twenty-one fetches" heads a table of 28 rows recording 31 fetch events | **LOW** | `PRIOR_ART_v03.md:305` vs `:307-336` |

---

## 2. The over-constraint result: verdict

### R-01 · The finding is a sensitivity analysis, not a result, and it hardens as it propagates

**Claim as written.** `LADDER_ARCHITECTURE.md:16`:

> "**The over-constraint is new and it is the sharpest result in the programme.** `GAPS.md` §4a and `../logos.tex` §3.3 establish `f ≤ 1-g`, hence a unique-corpus requirement bounded by `5.6e13 * (5 - 4g)`, which is **2.8e14 at `g = 0`** and **6.05e13 at `g = 0.98`** against a central supply estimate near **6e13**, and **no setting of `g` satisfies X-04, C-02 and F-04 at once.**"

Restated at `LADDER_ARCHITECTURE.md:142` ("No setting of `g` satisfies all three"), `:485` ("the bound is what §1.5 shows makes the argument **unwinnable**"), `:1075` ("**settled by arithmetic rather than by measurement** ... §1.5's trilemma is not waiting on a run"), and `GAPS.md:148` ("There is no setting of `g` at which all three are satisfied").

**What checks out, and it is more than the brief for this review assumed.**

*The supply figure is not an unverified survey number.* `logos.tex:94` states the effective stock at about `3e14` with a 90 percent interval of `1` to `10e14`, embedding "a roughly fivefold epoch multiplier", hence a unique quality-filtered stock near `6e13` with an interval of about `2` to `20e13`. Fetched `https://epoch.ai/publications/will-we-run-out-of-data-limits-of-llm-scaling-based-on-human-generated-data`: "The total effective stock of human-generated public text data is on the order of **300 trillion tokens, with a 90% confidence interval of 100T to 1000T**." Fetched `https://arxiv.org/html/2211.04325v2` §2.3.2 on the multiplier: "the upper extreme of 15x would require a very inefficient training procedure with a large number of epochs that does not correspond to common practices. **For this reason we reduce it to 5x.**" Dividing 300T by 5 gives 60T and dividing the interval gives 20T to 200T. **`logos.tex:94` reproduces the primary source exactly, including the interval.** That leg of the brief's suspicion is refused, and it also repairs round 2's class-two defect at the same line, which was that the premise carried no citation at all.

*The bound `f ≤ 1-g` is derived, and derived correctly.* `logos.tex:710` defines the shared core as "public, licensed, non-personal data" and residency-bound shards as its complement, so *shared implies not residency-bound* holds by definition; a seed consuming fraction `g` is necessarily core; therefore the residency-bound fraction cannot exceed `1-g`. Substituting into Eq. (residency) gives `5.6e13(1+4(1-g)) = 5.6e13(5-4g)`, and both endpoints reproduce: `5.6e13 x 1.08 = 6.048e13` and `5.6e13 x 5 = 2.8e14`.

**Where it fails. Two places, and the second decides the verdict.**

**(a) The verdict is a function of a point estimate inside a factor-of-ten interval.** Writing `S` for unique supply and `r` for tokens per total parameter, the `g` at which the data wall is met is `g* = (5 - S/(r x 2.8e12))/4`. Recomputed here across the survey's own 90 percent interval at `r = 20`:

| `S` | `S/(rN)` | `g*` |
|---:|---:|---:|
| `2e13` (90% lower) | 0.357 | **1.161, unsatisfiable at any `g`, including `g = 1`** |
| `6e13` (central) | 1.071 | 0.982 |
| `1e14` | 1.786 | 0.804 |
| `2e14` (90% upper) | 3.571 | 0.357 |

Across the interval the verdict runs from "the data wall blocks the architecture at every setting, decomposed or not" to "any branch consuming more than 36 percent of the token budget is fine". `LADDER_ARCHITECTURE.md:144` states this correctly and in terms, and is contradicted by `:16`, `:142`, `:485` and `:1075` in the same file, and by `GAPS.md:148`, which is the file the finding is attributed to.

**(b) The bound is read as an equality, and the parameter it is written in is the wrong one.** `f ≤ 1-g` is an **upper** bound on the requirement. `LADDER_ARCHITECTURE.md:138` converts it into a necessity: "X-04, the data wall, **needs** `g` at or above about 0.98 for the decomposed requirement to reach the central supply estimate at all. **Below that the token argument for towers is dead** against that estimate."

Demonstration. The requirement `5.6e13(1+4f)` meets `6e13` if and only if `f ≤ 0.02`. Take `g = 0.20` and `f = 0.02`. The constraint holds, `0.02 ≤ 0.80`. The requirement is `5.6e13 x 1.08 = 6.05e13`, met. So `g = 0.20`, a branch consuming 80 percent of each tower's budget, which `LADDER_ARCHITECTURE.md:130` itself calls "genuinely divergent" at the shallower `g = 0.50`, satisfies the data wall. **`g ≥ 0.98` suffices; it is not needed.** Below 0.98 the token argument is not dead, it is undetermined. The table at `LADDER_ARCHITECTURE.md:127` carries the correct column header, "**Bound** on unique-corpus requirement", and then `:138` reads that column as the value: at `g = 0.50` it prints "1.68e14, 2.80x over" when the actual requirement at `g = 0.50` is anywhere from `5.6e13` to `1.68e14` depending on a quantity the row does not carry.

**The refutation pass, and the weakening it forced.** The rescue is that `f` and `g` are not independent in substance: Eq. (residency) models every tower's corpus as a core shared by all five plus a private shard, so `f` is functionally *the fraction each tower reads alone*, and `f = 0.02` means the towers share 98 percent of their tokens whenever they branched. That rescue works and it costs the finding its strongest form. **The substantive conflict survives: a corpus overlap high enough to meet the supply estimate is a corpus overlap high enough to kill the diversity claim.** What does not survive is that the conflict is about `g`, or that §3.3 added anything to it. `logos.tex:719` states the whole conflict without `g`: "against the central unique-stock figure of about `6e13`, the decomposed requirement is already at the estimate at `f = 0` and exceeds it for `f` above about `0.02`." Round 2 recorded that as X-04, MEDIUM. §3.3's contribution is an upper bound on `f`, and the constraint that binds is a *lower* bound demanded by the diversity claim, about which `f ≤ 1-g` says nothing.

**The third leg fails and is recorded as such.** The brief argued that `D_opt = 20N` is Chinchilla, dense, and that F1 exists precisely because applying it to a sparse model is unjustified, so the second input is unverified. Checked against primary sources: Kimi K2 is 15.5T tokens over 1.04T total parameters (`arXiv:2507.20534`), which is 14.9 tokens per total parameter; DeepSeek-V3 is 14.8T over 671B (`arXiv:2412.19437`), which is 22.1. Recomputing `g*` at the central supply estimate: `r = 14.9` gives `g* = 0.890`, and `r = 22.1` gives `g* = 1.008`, unsatisfiable at any `g`. **Correcting the token law does not dissolve the finding; at DeepSeek-V3's observed ratio it makes X-04 strictly unsatisfiable.** Round 2 §6.1 had already reached this and it is confirmed here independently. The brief's second leg is wrong and this report says so.

**Verdict, plainly.** The over-constraint result **does not survive as a result.** It survives as a sensitivity analysis whose verdict is set by a point estimate inside a factor-of-ten interval, restated in a parameter that adds a bound in the wrong direction, and whose substance was already on the books as round 2's X-04 at MEDIUM. It is not "the sharpest result in the programme", it is not "settled by arithmetic rather than by measurement", and an architectural decision (`LADDER_ARCHITECTURE.md:152`, "This document adopts response 1", which deletes the third of `logos.tex` §3.1's three motivations) should not have been taken on it.

**Fix.** Three edits.
1. In `GAPS.md:148` and `LADDER_ARCHITECTURE.md:16`, `:142`, `:485` and `:1075`, replace "no setting of `g` satisfies all three" with the conditional form `:144` already states, and carry the sensitivity table above rather than the single central row.
2. Replace "the data wall **needs** `g ≥ 0.98`" with "`g ≥ 0.98` **guarantees** the data wall is met; below it the outcome is set by the corpus and not by the schedule", and relabel the `g` table's third column as a worst case.
3. Restate the trilemma in `f`, or in an explicit corpus-overlap parameter, rather than in `g`, and grade it at the severity round 2 gave X-04 until a supply measurement exists. `LADDER_ARCHITECTURE.md:150`'s response 3, dispute the supply estimate, is then not the third option but the only unblocked one, and §10's un-digitised-archive argument is where it is already made.

---

## 3. The cost model and the dispatch argument

### A-01 · §11.1 case 3 derives capacity from memory, and recovers nothing

**Claim as written.** `logos.tex:609`:

> "Allocating the 320 accelerators in the same proportion gives pools of $192, 64, 32, 16, 16$, and **because both the memory floor and the allocation are proportional to $N_i$, every pool sits at the same $320/106 = 3.02$ times its own floor. Capacity share again equals load share, so the multiplexing loss of case 2 is recovered**"

**What checks out.** The sizing is exact. Shares `(0.60, 0.20, 0.10, 0.05, 0.05)` on 14T give `8.4/2.8/1.4/0.7/0.7`T; at 4.25 bits those weigh `4.4625/1.4875/0.74375/0.371875/0.371875` TB, totalling **7.4375 TB**, matching the paper's 7.44 and the same 106-accelerator floor. Pools `192/64/32/16/16` sum to 320. Every pool sits at the same multiple of its own memory floor and that multiple is `320/106.25 = 3.012` (the paper's 3.02 divides by the rounded 106; the equality across pools is the claim and it holds).

**Why the conclusion is wrong.** Memory-floor proportionality is about *bytes resident*. "Capacity share equals load share" is about *tokens per second*. The step between them is not taken and does not hold.

Demonstration, in the paper's own units. Decode cost per token is proportional to activated parameters, which is the content of `logos.tex:101`, Eq. (3). Proposition 1 at `:127` defines "fixed sparsity $s = N_{\mathrm{act}}/N_{\mathrm{total}}$" **per tower** and derives training compute `6 s N_total D` from it. Carrying that convention into case 3, pool `i` has `A_i = 320 p_i` accelerators each at `F` FLOP/s, and its tower activates `N_act,i = s x 1.4e13 x p_i`. Its aggregate token rate is

```
R_i  =  A_i F / (2 N_act,i)  =  320 p_i F / (2 s x 1.4e13 x p_i)  =  320 F / (2 s x 1.4e13)
```

which is **independent of `i`**. Every pool in case 3 has the same throughput regardless of its share. The busiest pool carries 0.60 of the load with 0.20 of the throughput, so the fleet saturates at `L_max = R/0.60 = 5R/3 = C/3`, **exactly case 2's answer**. Case 3 recovers nothing. Mean utilisation stays at `1/3` and two thirds of the fleet is still idle while the Code pool queues.

Case 3 works only under the opposite convention, activated parameters held *constant* across towers so that the 8.4T tower is three times sparser. Then `R_i` is proportional to `A_i` and hence to `p_i`, capacity share does equal load share, and the argument goes through. That is a legitimate mixture-of-experts design, more experts at unchanged top-`k`, but it is never stated, it contradicts Proposition 1's fixed-`s` convention, and it changes what `:609` claims: under it, "a tower three times the size" buys resident knowledge and no additional compute per token.

**The refutation pass.** Three attempts, none successful. (i) *Perhaps memory headroom is what matters.* No: headroom above the floor buys replicas of tower `i`, each serving at a rate proportional to `1/N_act,i`, giving the same cancellation. (ii) *Perhaps serving is memory-bandwidth-bound rather than FLOP-bound.* That is the paper's own regime at `:357` and it makes the finding **stronger**, since bytes moved per token in a sparse forward pass is also proportional to activated parameters. (iii) *Perhaps `LADDER_ARCHITECTURE.md:411` licenses the step.* It does the opposite, and honestly: "Serving capacity within a domain is **taken** proportional to accelerators assigned once the residency floor is met" is stated there as an assumption. `logos.tex:609` states the identical step as a derivation with a "because" clause that carries memory. The companion is candid where the paper is not.

**Severity.** CRITICAL on the paper's own accounting. `:613` says the cost argument is what is left after the other three motivations were eroded and that it is valuable because "a cost argument can be checked against an invoice". `:609` calls case 3 "the case that justifies it". `:925` reprints it in the conclusion. And `LADDER_ARCHITECTURE.md:444` reaches only **parity** for its own case 3 ("Throughput parity with the fungible fleet") and puts the strict win on the size axis instead, so the paper claims a strict win where its companion claims a tie.

**Fix.** State the sparsity convention case 3 assumes. If activated parameters scale with total parameters, delete "capacity share again equals load share" and the recovery claim, and say case 3 buys per-domain parameter allocation at no throughput improvement. If activated parameters are held constant, say so, say the larger towers are correspondingly sparser, and rewrite "three times the size" as "three times the resident parameters at unchanged activated compute". Either way replace the "because" clause at `:609`.

### A-02 · §9.2's advantage needs each tower's pool to be local, and §9.1 says it is not

**Claim as written.** `logos.tex:514`: "A **Mixture-of-Towers** routes a whole query to one tower. That is *one* dispatch per query. **The round trip is paid once at admission and decoding then runs local to the tower's own pool.**" `:619` calls the resulting claim "the sturdier of the two because it does not depend on the traffic mix at all."

**Why it does not hold as stated.** The premise is that the monolith's dispatch crosses the wide-area peer network and the tower's does not, and nothing establishes the asymmetry. `logos.tex:496` says the reference deployment "distributes layers across nodes owned by independent parties in the manner of Petals", and `:183` says each tower "is internally a heterogeneous mixture-of-experts". A tower is therefore itself a sparse model whose experts must be dispatched to, `:599` puts a tower's pool at 64 accelerators, and case 3 at `:609` raises the dominant pool to **192**. If those accelerators are peers in the pool §9.1 describes, the tower pays the same 60 serial round trips per token that the monolith does and the three-orders-of-magnitude gap is zero.

Demonstration from the paper's own numbers. A 2.8T tower at 4.25 bits is 1.4875 TB, needing at least `1.4875e12/70e9 = 21.3` accelerators and served on 64, that is 8 eight-accelerator nodes. The 14T monolith needs 106 and is priced at 320, that is 40 nodes, roughly two racks. Both are single-facility deployments at 2026 scale. The distinction §9.2 rests on is not "one fits in a locality and the other does not"; it is a deployment choice, and case 3 makes it worse by putting 60 percent of traffic on a pool that is itself 60 percent of the monolith's footprint.

**The refutation pass, and the weakening.** `:619` does hedge, "it is a statement about deployability **under a given topology** and says nothing about quality", and `:518` concedes the arithmetic "narrows it and does not close it". That hedging survives the finding and is why this is HIGH rather than CRITICAL. What does not survive is `:514`, which asserts locality as a property rather than as the premise it is, and `:516`'s "**is why** an ensemble tolerates a wide-area heterogeneous pool that a monolith of equal total size does not", a causal claim conditional on a premise stated nowhere.

**Fix.** Add the premise at `:514` as a premise: the comparison holds when each tower's serving pool is one low-latency locality and the monolith's expert set is not, and that is a deployment assumption rather than a consequence of the architecture. Note at `:609` that case 3's 192-accelerator Code pool is where the assumption is least comfortable.

### A-03 · The 960:1 conflation is corrected and then re-committed two sentences later

**Claim as written.** `logos.tex:512` retires it explicitly: "An earlier version of this section quoted ``960 against one'' as though it were the latency ratio; **that conflated invocation count with serial depth**". Then `logos.tex:516`: "**Nine hundred and sixty dispatches per token against one per query is the entire difference, and it is why an ensemble tolerates a wide-area heterogeneous pool** that a monolith of equal total size does not."

**Why it is wrong.** Tolerating a wide-area pool is a latency property. `:512` has just established that the latency ratio is 60:1 per token and 30,000:1 per 500-token response, and that 960:1 is a bandwidth and load count. `:516` then makes 960:1 the reason for the latency property, four lines after retiring it as a latency ratio. Both corrected figures are in the section; the uncorrected sentence survived the correction.

**The refutation pass.** Could "the entire difference" summarise bandwidth and latency together, with "is why" carrying only the bandwidth half? It cannot: the clause it governs is wide-area tolerance, which `:510` prices exclusively in round-trip latency (0.60 s and 1.80 s per token) and never in bandwidth. Survives unweakened.

**Fix.** "Sixty serial round trips per token against one per query is the difference that decides serviceability, and 960 expert invocations per token against one is the difference that decides bandwidth."

### A-04 · §9.2 flags the insensitivity it has and not the sensitivity it has

**Claim as written.** `logos.tex:508`: "That layer count is an assumption rather than a figure ... **but the conclusion is insensitive to it within a factor of two.**" `:510`: "At 10~ms per round trip that is 0.60~s per token ... at 30~ms it is 1.80~s per token ... **Neither is an interactive serving rate.**"

**What checks out.** The layer-count insensitivity is real. DeepSeek-V3's 61-layer stack with the first three dense gives 58 mixture-of-experts layers (`arXiv:2412.19437`), so `16 x 60 = 960` is the right order, and at 30 or 120 layers the per-token latency is 0.30 s or 1.20 s at 10 ms, still not interactive.

**What is missing.** The conclusion is highly sensitive to the round-trip time and that sensitivity is never stated. Taking 10 tokens per second as an interactive floor, the claim requires a round trip above `100 ms / 60 = 1.67 ms`. Measured intra-datacentre round trips for exactly this workload are two orders below: NVSHMEM IBGDA reports a **24.3 microsecond** round trip for mixture-of-experts all-to-all with a CPU proxy at **18.0** and a device-initiated backend at **16.7** (`arXiv:2604.00317`). At 24 microseconds, 60 serial round trips is **1.46 ms per token, about 690 tokens per second**. The dispatch argument is therefore an argument about wide-area networks and not about sparse dispatch, and the reader is given no way to see how narrow the scope is.

**The refutation pass, and the weakening.** The paper does scope every instance of the claim to wide-area, at `:506`, `:516` and `:619`, which is why this is MEDIUM and not a defect in the conclusion. What survives is that a stated insensitivity sits next to an unstated sensitivity of the opposite sign, and the unstated one is what decides whether the architecture's second surviving justification applies to a given deployment.

**Fix.** One sentence after `:510`: the crossover is a round trip of roughly 1.7 ms, intra-datacentre dispatch measures 17 to 24 microseconds, and the argument is about the network the pool spans rather than about sparse dispatch as such.

### A-05 · §11.1 prices per-accelerator weights at the density §7.1 corrects

**Claim as written.** `logos.tex:595`: "Taking sixty-four at face value gives **21.9~GB of weights per accelerator**, which is 31 percent of a usable 70~GB, 18 percent of a usable 125~GB, and 13 percent of a usable 170~GB."

**Why it is wrong.** `logos.tex:442` corrects exactly this density: "K3's MXFP4 weights occupy about **1.49~TB rather than the widely quoted 1.4~TB**." Recomputed: `1.4e12/64 = 21.875` GB is the flat-four-bit figure and `1.4875e12/64 = 23.242` GB is the corrected one. All three derived percentages move: 33 percent of 70 GB, 18.6 of 125, 13.7 of 170. The paper commits four sections later the error it names in §7.1, in the paragraph that anchors the 320-accelerator figure the rest of §11.1 runs on.

**The refutation pass, and the weakening.** The 320 extrapolation is unaffected, being `64 x (14/2.8) = 320`, which cancels the density, so no downstream number changes. MEDIUM rather than higher, and it survives because §11.1 is the paper's checkable section and round 2 raised A-05 against precisely this class of slip.

**Fix.** 23.2 GB, and 33, 19 and 14 percent, at the true 4.25-bit density of §7.1.

### X-02 · The conclusion's headline idleness figure is computed on the partition §3.5 rejects

**Claim as written.** `logos.tex:925`: "under skewed traffic and uniform sizing the ensemble is strictly worse, **losing two thirds of a 320-accelerator fleet to idleness**", derived at `:607` on five towers.

**What checks out.** The five-tower arithmetic is exact: mean utilisation is `Σp_i/(k p_max) = 1/(5 x 0.60) = 1/3`, recomputed here.

**Why it is inconsistent.** `logos.tex:271` says the paper's own criterion returns **four** towers, with Mathematics and Logic merged. Recomputed on four towers with those two merged out of the same shares, `(0.60, 0.20, 0.15, 0.05)`, mean utilisation is `1/(4 x 0.60) = 0.4167`: **58 percent idle, not 67**, and a throughput penalty of 2.4 rather than 3. The conclusion prints the five-tower figure with no note, and §11.1's three caveats at `:611` do not include the tower count.

`LADDER_ARCHITECTURE.md:403` handles this correctly and is the model for the fix. It computes on four domains at `(0.55, 0.20, 0.15, 0.10)`, gets a factor of 2.20 and 54.5 percent idle (both recomputed and correct here), and says "Quote the paper's figures when citing the paper. Quote §5.3's when reasoning about the four-domain partition the criterion actually returns. **Do not interleave them.**" The paper does not carry that instruction.

**The refutation pass, and the weakening.** The inconsistency is disclosed once, at `:271`, so it is not hidden. **Weakened from a hidden inconsistency to a disclosed one whose numerical consequence is not disclosed and which propagates unflagged into the conclusion**, where a reader who skipped §3.5 will meet it.

**Fix.** One clause at `:607` and at `:925`: on the four-tower partition the criterion returns, the same skew gives 58 percent idle and a factor of 2.4.

### X-03 · §11.1's comparator is a domain tower used as a generalist, and the companions disagree about it

**Claim as written.** `logos.tex:599`: "**Five replicas of a single 2.8T tower is also 320 accelerators.**" `:609`: "A replica fleet is $n$ copies of one model, so **every domain gets the same parameter count** whether it carries 60 percent of traffic or 5."

**Why it does not cohere.** "Tower" in this paper is a domain-specialised model (`:183`). Five replicas of one *tower* is a fleet that serves one domain. `:609` then uses that fleet as though it served all five: the comparator is a domain model in its name and a generalist in its use.

`LADDER_ARCHITECTURE.md:411` names the defect and fixes it: "Comparator is a fungible fleet of 320 accelerators of a **generalist model** of the same per-instance size ... §11.1's stated baseline of five replicas of one 2.8T tower covers only one domain and so **is not a competitor to an ensemble at all**." But `:403`, eight lines earlier in the same section, says of the two instantiations: "**Both are the same argument evaluated at different assumed skews on different domain counts.**" Those cannot both hold.

**The refutation pass.** Could "tower" at `:599` be read loosely as "2.8T model"? The next sentence blocks it: "A Code request cannot consume an idle **Life-Sciences accelerator**, because the weights resident on it are the wrong weights." The replica fleet is being contrasted with domain-resident weights, so it must be a generalist, which makes the word "tower" wrong. Survives.

**Fix.** At `logos.tex:599`, "five replicas of a single 2.8T **generalist** of the same size". In `LADDER_ARCHITECTURE.md`, reconcile `:403` with `:411`.

---

## 4. Falsifier construction

### F-01 · F13 limb (b)'s printed kill condition is what the cited theorem already predicts

**Claim as written.** `logos.tex:915`, F13's falsifying observation, limb (b): "**Calibrated-confidence weighting alone lifting ensemble accuracy without any environment adjudication**, which would locate the gain in the protocol rather than in the observation channel." Costed at 36.3 GPU-hours.

**Why it does not bind.** The paper states the same proposition as an accepted published result. `logos.tex:737`: "**Weighting each agent's contribution by a calibrated confidence that is positively correlated with correctness turns the belief process into a strict submartingale, so expected correctness strictly increases** \cite{zhu2026debate}." The bibliography at `:1097` records it as "**Proves the confidence-weighted submartingale (Thm.~1)**". `LOGOS_HARNESS.md:81` says so in terms: "Limb (b) is **Zhu et al. Theorem 1 run as an arm of F9**." A falsifier whose kill condition is a theorem the paper cites, accepts, and restates in its own body cannot return a surprise.

**The refutation pass, and the weakening it forced.** There is a real experiment nearby and the paper knows it. `logos.tex:753`: "the calibration that buys that correlation is itself purchased with external supervision ... **The exogenous signal moves from the debate into the calibrator; it is not removed.**" `LOGOS_HARNESS.md:81` records the same steelman and requires "the confidence-calibration supervision identical across arms" with its cost "as a separate ledger line". So the intended limb (b) is not "does confidence weighting help" but "does it help **once the calibrator's own exogenous supervision is charged**", which is a genuine test.

**The finding therefore weakens from "the falsifier is dead" to "the falsifier as printed in `logos.tex` is dead and the live version exists only in the companion."** `:915`'s "without any environment adjudication" is satisfied by an off-the-shelf calibrated model that carries exogenous signal inside its weights. The register of record carries the dead wording.

**A second defect, from the harness stream, which is separable and worse.** `LOGOS_HARNESS.md:81` claims the arm instantiates Zhu et al. Theorem 1, but the arm is two aggregation rules over **two heterogeneous frozen models at R = 1**, with no debate and no rounds, while the theorem is stated for agents "explicitly *homogeneous* and fully connected" (`LOGOS_HARNESS.md:41`) and concerns a submartingale **over debate rounds**. With no rounds there is no process. And with two proposers, "unweighted majority" is not a majority: it is `argmax P_M` (`:176`), so the contrast reduces to "trust the more confident of two models". That confidence-weighted ensembling beats uniform averaging is standard and has no bearing on whether external adjudication supplies novel information, yet `:81` reads a positive as locating "the gain in the protocol rather than in the observation channel" and hangs kill condition K5 on it.

**Fix.** Restate limb (b) in `logos.tex:915` as the companion states it, with the calibration supervision charged to the same ledger and held identical across arms, and with the pre-committed equivalence margin a null result needs (`GAPS.md:162` already established that requirement for F9's negatives). In `LOGOS_HARNESS.md:81`, either add rounds and a homogeneous-agent control so the theorem is instantiated, or restate limb (b) as an ensembling result and re-derive what K5 is licensed to kill.

### F-02 · F11's claim is what §3.5 has already refuted, and its threshold does not exist

**Claim as written.** `logos.tex:911`, F11: "**The five-way partition of §3.5 is justified:** Code, Life Sciences, Mathematics, Logic and Administration separate on at least two of the three axes"; falsifying observation, "Measured corpus overlap between the Mathematics and Logic corpora **at or above the level at which the criterion merges them**, i.e. the criterion returning four towers on real corpora and not five".

**Two defects.**

*The polarity is inverted against the paper's own position.* `logos.tex:271`: "**So the criterion says four towers, not five** ... and record that the architecture's own partition rule does not support it." F11's claim is therefore a proposition the paper has already rejected by argument, and F11's *falsifying* observation is the paper's own stated conclusion. A falsifier whose kill condition is the author's current belief cannot discriminate: it is pre-fired, and running it can only confirm.

*The threshold it names does not exist.* "The level at which the criterion merges them" refers to a number, and §3.5 supplies none. Axis P1 at `:264` reads "Two towers drawing on the same corpus contribute nothing to it" with no overlap statistic and no cut point; P2 and P3 are qualitative. The falsifying observation reduces to "the criterion fires when the criterion fires", and F11 is not computable from anything in the paper. `:271`'s own honest sentence, "Settling this needs corpus-overlap measurements rather than argument", is true, and the falsifier minted to carry it does not say what measurement or against what bar.

**The refutation pass.** Could F11 be read charitably as "Table 1 still prints five and the measurement decides"? That is the intent, but it is not what `:911` says, and the fix is one sentence rather than an argument. Survives.

**Fix.** Restate F11's claim as the paper's actual position, that the criterion returns four towers on real corpora, with the falsifying observation being measured Mathematics-Logic overlap **below a pre-registered threshold**, and register that threshold in §3.5 together with operational definitions for objective conflict and update cadence. Without a pre-registered number F11 is a research task, not a falsifier.

### F-03 · F10's restated criterion is not computable as stated

**Claim as written.** `logos.tex:673`: "A warm-started router fails F10 if, on any domain carrying at least five percent of evaluation traffic, its post-swap AIQ falls more than $0.02$ below its pre-swap AIQ, or its $\mathrm{CPT}(50\%)$ rises by more than ten percentage points of calls. **Both are defined on every evaluation set, including the ones where one tower dominates.**"

**Three defects.**

*(i) AIQ renormalises across the swap.* Eq. (`:648`) is `AIQ = 1/(c_max - c_min) ∫ R̃ dc`. A tower swap changes the pool's cost range, so pre- and post-swap AIQ are averages over different intervals. Demonstration: pre-swap towers priced `{1, 3}`, post-swap `{1, 5}`. A router with identical behaviour on `[1, 3]` and flat quality thereafter still shows a different AIQ, because the extra `[3, 5]` region is averaged in. At a 0.02 threshold that is not distinguishable from a routing regression. The criterion must fix a common cost domain and does not.

*(ii) The CPT half contradicts the same subsection ten lines earlier.* `:663` concedes: "APGR does **not** avoid it structurally ... $r(M_s) - r(M_w)$ **is zero if the designated endpoints score alike**." CPT(50%) is defined through PGR, so when that denominator is zero, PGR is undefined and CPT(50%) with it. `:673`'s "Both are defined on every evaluation set" is contradicted inside its own subsection.

*(iii) The 0.02 threshold sits below the per-slice standard error, and there is no multiplicity control.* AIQ inherits the quality scale, so on a domain slice of the size §11.2 itself uses (`:636` works its example on "a 50-item per-domain slice") with quality near 0.7, the standard error of a single quality estimate is `sqrt(0.7 x 0.3 / 50) = 0.065`, more than three times the threshold. The criterion fires on **any** qualifying slice, and §3.5's partition is now two-dimensional: with 4 domains crossed by 3 size tiers, 12 slices, and a per-slice probability of about 0.159 of a spurious drop past 0.02 under a normal approximation at that standard error, the probability an unchanged router fails F10 somewhere is `1 - 0.841^12 = 0.88`. As written the criterion fails a router that did not change, seven times in eight.

**The refutation pass, and the weakening.** Defect (iii)'s number depends on the slice size, which `:673` does not fix; a 5,000-item slice gives a standard error of 0.0065 and the threshold becomes usable. **Weakened to: the criterion is not computable without a stated minimum slice size, a common cost domain, and a multiplicity rule, none of which it has.** Still fatal as printed, and §11.2's own mandate at `:675` to report AIQ per domain is what makes the slices small.

**Fix.** Fix the cost domain to the union of pre- and post-swap operating ranges. Replace "Both are defined on every evaluation set" with the true statement, that CPT(50%) is defined whenever the designated endpoints differ in score, a condition `:663` already says must be checked in advance. Add a minimum slice size, a paired test at a pre-registered alpha, and a multiplicity correction, or set the 0.02 from a measured noise floor.

### F-04 · F14 is uninterpretable unless F13 limb (a) fires first

**Claim as written.** `logos.tex:917`, F14's falsifying observation: "Debate between two continued-pretraining branches of one base checkpoint **tracking the martingale measurably more closely** than debate between two independently pretrained models of matched size and matched benchmark quality." Instrument: "the same instrument as F13 limb (a) and costed with it at 17.4 GPU-hours." `GAPS.md:165` and `LOGOS_HARNESS.md:81` plan them as one rung.

**Why the pairing is unsafe.** F14 measures a *difference* between branch-pairs and independent-pairs. If F13 limb (a) fires, that is, if distinct pretraining lineage tracks the martingale as closely as personas and there is no lineage effect at all, then both arms of F14 track the martingale, the difference is zero, and F14 returns "not falsified". F14's claim at `:917` is that `λ = 1` and `λ = 0` "are interchangeable", so a null reads as **support** for the architecture. It would in fact be the corpse of the conjecture: they are interchangeable because neither has any diversity to preserve. Demonstration: set the true lineage effect to zero and the two arms are drawn from the same distribution by construction; the test is guaranteed to pass and the guaranteed pass is reported as good news.

*Second defect.* "Measurably more closely" carries no margin. Both F13(a) and F14 are equivalence-shaped in the direction the programme wants, and `GAPS.md:162` has already established for F9 that "a negative here is an equivalence claim, which needs a two-one-sided-tests procedure". Neither states a margin anywhere in `logos.tex`.

**The refutation pass.** The shared instrument is still efficient even if the interpretation is conditional, so the fix is an ordering rule and not a second budget. MEDIUM.

**Fix.** Pre-commit at `:917` that F14 is interpretable only conditional on F13 limb (a) returning a nonzero lineage effect, that a null F14 under a null F13(a) is reported as uninformative, and state the equivalence margin for both.

### F-05 · F12's kill condition is decided by an unstated choice inside the survey's interval

**Claim as written.** `logos.tex:913`: "A measured residency-bound fraction $f$ high enough that Eq.~(residency)'s $5.6\times10^{13}(1+4f)$ **exceeds the unique-token supply of \S2**".

**Why it does not bind.** §2 gives a central figure and a 90 percent interval spanning a factor of ten (`:94`). Recomputed: at the lower bound `2e13` the condition holds at `f = 0` and F12 fires unconditionally; at the central `6e13` it fires above `f ≈ 0.02`; at the upper bound `2e14` it needs `f > 0.643`. The falsifier's verdict is set by a choice `:913` does not make, and a pre-registered kill condition admitting three verdicts on one measurement is not pre-registered.

**The refutation pass, and the weakening.** `:719` and `GAPS.md:103` both name the central figure, so the intent is inferable. **Weakened to: the intent is inferable and the register of record does not state it**, the same defect class as F11. It also compounds R-01, since F12 inherits the unmeasured input the trilemma inherits.

**Fix.** Name the supply point in `:913`, or state the verdict as a function of it.

---

## 5. The harness, the proposer interface, and the pre-registration

### H-01 · The one loss-bearing free-text span has no specified generator, and the exemplar leaks the adjudication and is wrong

**Claims as written.** `LOGOS_HARNESS.md:141`: proposers return "free-text prediction and reasoning, which enters the trace (§5.3) **and enters nothing else**." `:401`: "**Loss is on thought and action**; if the action were decodable from the observation alone, the reasoning span would never be learned." `:427`, the exemplar trace:

> `thought: enemy Onix is rock and ground; water and grass hit 2x; my Squirtle knows water_gun`

**Why it fails.** §2.2 enumerates three proposer outputs and the §5.3 schema puts per-proposer text in `proposals[].predict`. The trace then carries a **separate, top-level `thought`** and a **top-level `action`**, and nothing in §2.2, §2.3 or §5.3 says who writes either. The `action` is the one executed, so it determines the adjudication, the outcome and the yield, and with two or more disagreeing proposers there is no stated selection rule. `:401` puts the training loss on both.

**Demonstration, from the file's own example.** P1's reasoning is "rock resists normal moves"; P2's is "type chart unknown". The `thought` at `:427` states a proposition **neither proposer produced**, and it is the answer: the type-effectiveness fact the adjudicator is about to confirm. The single most important loss-bearing span in F9's corpus is written by an unspecified oracle with outcome access. And it is **factually wrong**: Onix is Rock/Ground, Water is super-effective against both, so Water Gun against Onix is **4x**, not the 2x the thought asserts. The exemplar trains the learner on an incorrect statement about a held-out type pair, which is exactly what the primary endpoint measures. Separately, `O_A`'s effectiveness set `{no effect, not very, neutral, super}` has no 4x category, so the flagship example's true multiplier is not representable in the pre-committed outcome space.

**The refutation pass.** Could `thought` be an editorial gloss not actually in the corpus? `:401` forecloses it: loss is on `thought`. Could the wrongness be a typo with no design consequence? It is not: `:427` is the file's only worked instance of the span the design says must be load-bearing, and the design has no rule that would have caught it. Survives, and it is the reason this is CRITICAL rather than an erratum: F9 is the experiment `logos.tex:921` says would be run first.

**Fix.** Specify the generator. Require `thought` to be a verbatim copy of the *executed* proposer's `predict` field, with a compiler assertion that `thought ∈ {proposals[i].predict}`. Specify the action-selection rule explicitly (argmax of `P_M`, a pre-registered fixed proposer index, or a seeded coin flip with the seed in the trace). Forbid in `schema/validate.py` any span authored after `result` other than the mandatory `outcome` span. Correct the exemplar, and either add a 4x category to `O_A` or state that `super` conflates 2x and 4x and that the conflation is deliberate.

### H-02 · The Phase-4 yield gate is an algebraic identity and cannot fail

**Claim as written.** `LOGOS_HARNESS.md:546`, a pre-run VOID condition: "**Then:** admitted trajectories have **mean yield strictly above** the unfiltered control (**if not, the run is VOID, not negative**)."

**Why it certifies nothing.** Jensen-Shannon divergence *is* the excess entropy of the mixture: `H(P_M) = ½(H(P₁)+H(P₂)) + JS(P₁,P₂)`, exactly. Expected yield on an item, if outcomes track `P_M`, is `E[-ln P_M(o)] = H(P_M)`. So gating on `JS ≥ tau_JS` selects items of higher expected yield **by identity**, one nat of yield per nat of divergence. The gated set's mean yield exceeds the ungated set's by construction, for any two proposers including two random ones.

**Demonstration, on the file's own §5.3 vectors.** Computed here: `H(P_M) = 4.9420` bits and `½(H(P)+H(Q)) + JS = 4.9420` bits, identical to four decimal places. The second reading is worse: if "the unfiltered control" is A1/A2, whose pseudo-outcome is `argmax P_M` (`:176`), then its yield is the surprisal of the *mode*, the minimum over `O`, and the comparison is trivially won.

Note the units trap. The file separates nats (yield) from bits (JS) at `:174` precisely so nothing moves silently, and that separation is what hides the identity from its own authors.

**The refutation pass.** Could the gate still fire under gross miscalibration, when outcomes do not track `P_M`? Yes, and that is exactly what it would be detecting: a proposer-competence failure, which S4 and S5 already exist to catch. **Weakened to: the gate is a redundant competence check mislabelled as a check on the loop's mechanism**, and it is used as a VOID condition on the run. It cannot distinguish "the environment carried information the ensemble lacked" from "the two proposers disagreed", which is the distinction `logos.tex:786` step 2 says the gate exists to draw.

**Fix.** Replace with a test the mechanism can fail: compare the gated set's mean yield against the identity prediction `½ΣH + JS` computed on the same items. A shortfall is the informative signal, meaning the environment is *less* surprising than the ensemble's own disagreement predicts. Parity with the identity is the null.

### H-03 · Nothing tests anteriority; a card carrying last turn's verdict passes all three checks

**Claims as written.** `LOGOS_HARNESS.md:293`: the card carries "the **verbatim contents of the text box**, transcribed from the tile map." `:297`: "**No effectiveness verdict.** ... The card describes state and never adjudication, because a card that adjudicates makes the proposal trivial and the yield identically zero."

**Why the ban does not bind.** It is prose. Check 1 (`:303`) compares *field names*. Check 2 (`:304`) asks whether each card field "matches what the rendered frame displays". Check 3 (`:305`) asks whether the learner's codes recover the field. A card whose text-box field reads `IT'S SUPER EFFECTIVE!` passes all three: the field is on the certified list, it faithfully matches the frame, and Phase 1 certifies text legibility. **No gate anywhere in §3.4 asks whether a card field is a function of post-action state.** And no section specifies which frame within a turn enters the proposal pool: `:542` dumps "(frame, action, RAM-state) tuples" from scripted and random-walk play, and `:553` requires 1,612,904 distinct battle observations for a gated arm, a volume that pushes toward a permissive sampler.

**Demonstration, of why the audit cannot save it.** Suppose 0.2 percent of sampled frames carry a verdict string in the message box. In a 1,000-frame audit the expected count is 2 and `P(none appears) = 0.998^1000 = 0.135`, so there is a 13.5 percent chance the class is never seen. And if it *is* seen, check 2 scores it **correct**, because the card faithfully transcribes what the frame shows. The audit's pass criterion is orthogonal to the property being claimed.

**The refutation pass, and the weakening.** In Gen-I Red the bottom box is cleared to the FIGHT/PKMN/ITEM/RUN menu on a decision frame, so a *strict* decision-frame sampler probably does not carry the previous turn's verdict. **Weakened to: the defence is a property of a sampler the spec does not specify.** The spec's only stated constraint, "the legal action set, enumerated, exactly as offered on screen", is asserted and not implemented as a filter.

**Fix.** Add check 4, an anteriority assertion: `render_observation.py` takes as input only the pre-action `(frame, RAM)` tuple with the emulator state hash recorded, and `parity_check.py` asserts the card is byte-identical when regenerated from a state reloaded before any action is applied. Add a hard filter rejecting any frame whose text-box field is non-empty of game-message content or whose legal action set is empty. Both are computable in Phase 0.

### H-04 · The two renderings are not in information parity and only one is gated

**Claims as written.** `LOGOS_HARNESS.md:287`: "There are two, and **a run declares which it uses per proposer**." `:297`: "enemy HP is a bucket **because the screen shows a bar, not an integer**." `:299`: "**R-frame.** ... the raw 160x144 frame at native resolution." `:309`: parity "means they support the same field set **at the same resolution**."

**Why it fails.** All three §3.4 checks are defined over the card's field list. **No check of any kind is specified for R-frame**, which is by construction a superset: it carries the HP *bar*, the exact thing the card refuses to carry at bar resolution, and the card's stated justification for bucketing is what R-frame hands to the proposer.

**Demonstration, in bits.** The Gen-I HP bar is 6 tiles, 48 pixels, quantising HP into about 49 distinguishable states: `log2(49) = 5.61` bits. The card's bucket carries `log2(5) = 2.32` bits. An R-frame proposer receives about **3.3 bits more per HP field**, and with two slots about **6.6 bits more per observation**, on the exact variable the outcome space quantises (damage in quintiles of max HP, faint yes or no).

**Second demonstration, from the parity repair itself.** Check 3 *drops* card fields the learner's codes cannot carry. Dropping a field from the card does nothing to R-frame. If `status condition` is dropped, the R-text proposer cannot see the defender is asleep and the R-frame proposer can. On sleeping-defender items `JS(P1,P2)` is then inflated by a pure rendering artifact, so `tau_JS`'s calibration pool is enriched with rendering-asymmetry disagreement, S4 passes for the wrong reason, the gate preferentially admits exactly the items where the renderings differ, and `P_M` is the unweighted mean of a blind and a sighted predictor.

Also unaddressed: two R-frame proposers "nearest-neighbour upscaled to the model's expected input" (`:299`) receive different effective resolutions and different image-token budgets, which the file notices only as a *ledger* issue and never as an information issue.

**The refutation pass.** Could a run simply use R-text for both? Yes, and that is the fix, but `:287` makes the rendering a **per-proposer** declaration, so mixed pairs are permitted by the specification. Survives.

**Fix.** Make the rendering a run-level and not a per-proposer declaration, forbidding mixed pairs. If R-frame is used at all, require the frame be masked or quantised down to the certified field set at the certified resolution (bar to bucket) before it reaches the model, with a byte-level assertion that the served image is a deterministic function of the same field tuple the card is built from. Re-run S4 within-rendering.

### H-05 · S5 passes a random proposer half the time, is a forking path, and is scored on the endpoint's own subtrahend

**Claims as written.** `LOGOS_HARNESS.md:546`: "**S5** proposer competence, **each proposer strictly above chance on the control condition** or the experiment is VOID." `:283`: the probe is "a **10,000-item battery per condition** ... chance is exactly 0.25 in both conditions." `:147`: "the **roster is not frozen** in this document." S5's stated purpose, `:571`: "S4 alone was not enough, because **two incompetent proposers disagreeing at random satisfy it**."

**Four defects.**

*(i) "Strictly above chance" is a coin flip.* With `n = 10,000` and `p = 0.25` the standard deviation is 43.3 and a uniformly random proposer needs at least 2,501 correct: `P = 0.4954`. Two random proposers both pass with `P = 0.2454`, which is precisely the failure mode `:571` says S5 exists to prevent.

*(ii) With an unfrozen roster, S5 is a forking path.* VOID is not terminal when the roster is free; it is a re-roll. Three candidate pairs give `P(at least one passes by luck) = 0.5703`. Nothing logs the number of attempts.

*(iii) S5 uses the endpoint's own control items, and the bias has a sign.* The primary endpoint is `g = p_heldout - p_control`. S5 selects the corpus generators on `p_control` over the same battery. Because proposer text is loss-bearing (`:401`), selected-for-control-competence proposers inflate the learner's `p_control`, the **subtrahend**, so `g` is biased toward zero, that is toward the equivalence verdict. This is the hazard the file itself refuses elsewhere: "the margin is **not** widened to make kill condition K3 easier to declare, because that would make a false K3 easier to reach as well" (`:579`). S5 does to the endpoint what `:579` refuses to do to the margin.

*(iv) "The control condition" has two referents.* `:145` defines "the F13 **control** condition" as "Personas or system prompts over one model"; under that reading S5's "strictly above chance" has no defined chance level and is uncomputable. Under the §3.3 reading it is computable and biased.

**The refutation pass.** Could a competent 8B model clear a 0.25 chance level by so much that the binomial argument is academic? Probably, but that is an argument about the roster and the roster is not frozen; the gate is what is supposed to hold when the roster is bad. Survives.

**Fix.** Build a **disjoint** S5 gate battery, same construction and different items, never used to score the learner. Replace "strictly above chance" with a one-sided exact binomial lower confidence bound at a stated alpha and a minimum effect (for example `LCB99 > 0.35`), Bonferroni-corrected across roster members. Freeze the roster and log the S5 attempt count in the seal. Report each proposer's held-out accuracy alongside its control accuracy and require them matched within a pre-committed tolerance, since otherwise roster choice alone moves the headline endpoint.

### H-06 · Study 2 charges a corpus multiplier the FROZEN §5.3 rule forbids, and its A0 arm duplicates Study 1

**Claim as written.** `F9_PREREGISTRATION.md:450`: "Study 2  3 seeds x (A1 ungated + A3 gated), **corpora model-dependent** across R=5 rounds so **EACH SEED generates its own** : 3*(403226+403226/0.25) = 6,048,387", propagated to `:472` (168.8 GPU-hours).

**Why it contradicts its own frozen rule.** §5.3 is FROZEN in the opposite direction. `:279`: "`P_M` is the proposer ensemble's pre-action distribution over `O` ... computed once, at generation time, by `bootstrap/yield_score.py`, which **loads no training checkpoint**." `:283`: "**The learner never acts**; it reads traces afterwards." Confirmed upstream at `LOGOS_HARNESS.md` §2.2 ("gradient: none, anywhere, ever" on the proposer path). If no learner state enters the proposal, gate, action or admission path, **nothing in the admitted corpus can depend on the training seed, in round 1 or round 5**. §5.3's own reason 2 says exactly this and uses it to avoid an 8x multiplier in Study 1, and then §8.1 applies a 3x multiplier of the same kind to Study 2.

**Recomputation under the frozen rule** (one corpus per arm, shared across seeds, as Study 1 does):

```
Study 2 proposals = 403,226 (A1) + 403,226/0.25 (A3) = 2,016,130
2,016,130 * 960 / 9555 / 3600 = 56.27 GPU-h   (document: 168.80)
overcharge = 112.5 GPU-h
```

*Second defect, separable.* `:496` charges Study 2 as `A0, A1, A3` at 3 seeds, 9 runs, 86.2 GPU-hours. But `:333` freezes "**A0 trains the same 1.0e9 tokens at R = 1**", A0 has no trajectory data by construction, and Study 1 already runs A0 at 125M, `T = 1.0e9`, `R = 1`, seeds 1001 to 1008. Study 2's A0 at seeds 1001 to 1003 is the same run. Recomputed: 6 novel runs, `6 x 9.5785 = 57.47` against 86.21, an overcharge of 28.7 plus 5.7 in the 20 percent reserve. Corroborating internal contradiction: the reproduce line at `:716` passes `--rounds 5` to A0, which §6 says runs at `R = 1`.

**The refutation pass.** Three attempts, all failed. (i) "Model-dependent" meaning proposer-dependent still gives one corpus for all three seeds. (ii) Later rounds using the trained learner as a proposer is forbidden by §2.1 and `LOGOS_HARNESS.md` §2.2. (iii) Emulator state diverging per seed does not follow, since actions come from frozen proposers. Note this also undercuts `LOGOS_HARNESS.md` §2 step 7, "Disagreement shrinks where the environment has been explored": frozen proposers cannot learn, so their disagreement on a given observation is constant across rounds. Survives.

**Fix.** Re-derive Study 2 generation at 56.3 and Study 2 runs at 57.5, taking the F9 total from 1,683.6 to about **1,536.7**; state that A0 is reused from Study 1 at matched seed index; correct `:716`. If a seed-dependent mechanism does exist, state it, in which case §5.3's reason 2 collapses and Study 1 must be re-costed too.

### H-07 · §8.4 banks a prefix-caching saving that §8.1 explicitly refuses to bank

**Claims as written.** `F9_PREREGISTRATION.md:477` (§8.1): "**One saving that exists and is not taken.** ... a prefix cache pays it once ... **It is not taken because it requires the prompt to be a strict prefix in every proposer's template and this document has not verified that per roster.**" `:607` (§8.4), 130 lines later: "**With prefix caching** each agent processes the transcript once: about 400 tokens of item and protocol plus 2 agents x 3 rounds x 150 = **1,300 tokens per agent per item**."

Same unverified property, same document, opposite treatment, and §8.4's roster (four models at 7 to 8B) is *less* checked than §8.1's.

**Recomputation without the assumption**, each round re-prefilling the grown transcript:

```
round 1: prefill  400 + gen 150 =   550
round 2: prefill  700 + gen 150 =   850
round 3: prefill 1000 + gen 150 = 1,150
per agent per item = 2,550 tok  (claimed: 1,300)  = 1.96x
6.24e7 * 1.96 = 1.224e8 ; /1194.4/3600 = 28.5 h ; +20% = 34.2 GPU-h
```

The 17.4 figure is about **2x sensitive** to an assumption the same document declares unverified.

**The refutation pass, and the weakening.** Limb (a) is 2,000 items against 14.1M proposals, so caching is easier to arrange at that scale. But the stated blocker was template compatibility, not scale, and that blocker is roster-side and unchanged. **Survives at reduced severity: the fix is a disclosed band, not a changed headline.**

**Fix.** Apply §8.1's own rule to §8.4: quote 17.4 as the cached case and **34.2** as the uncached case, and make the day-one probe verify template prefix-compatibility per roster before either is committed.

### H-08 · Check 2 is unattainable and insufficient; check 3 is vacuous under its natural instantiation

**Claims as written.** `LOGOS_HARNESS.md:304`: "Pass condition: **100% on the four Phase-1 gate fields** and at least 99% overall" on 1,000 frames. `:305`: "fit a **linear probe** from the 90 collapsed codes ... above a floor pre-committed with the probe."

**Check 2, unattainable and insufficient.** At a realistic human or OCR keying error rate of 0.5 percent, `P(a clean 1,000-frame audit) = 0.995^1000 = 0.0067`. The gate fails 99.3 percent of the time for reasons unrelated to the card, which in practice means it will be rubber-stamped. And a passing audit bounds the true error at 0.3 percent by the rule of three, not at zero, so it misses a 0.2-percent-prevalence class 13.5 percent of the time, which is the H-03 hole.

**Check 3, vacuous.** The code representation is unspecified. Under the natural one-hot reading the input is `90 x 1,024 = 92,160` dimensions against about 1,000 frames; by Cover's theorem any labelling of 1,000 points in general position in 92,160 dimensions is linearly separable, so **every** field passes and no field is ever dropped. The "no more than the learner sees" half of parity is then never enforced. The 768-dimension summed-embedding reading is also unsafe in-sample at `n = 1,000`. There is no train/test split, no null, and "a floor pre-committed with the probe" is not a number.

**The refutation pass.** Could the audit be automated, making 0.5 percent pessimistic? `:307` says explicitly "the human audit is not GPU work", so it is human. Survives.

**Fix.** Check 2: pass condition as an upper 95 percent binomial bound on the card-error rate below a pre-committed threshold, dual independent audit with disagreement adjudication, and a sample separate from the Phase-1 selection sample (`:304` currently reuses one). Check 3: name the representation, use frozen k-fold cross-validation over frames, pre-commit the floor as the 95th percentile of a label-permutation null, and require probe capacity below `n`.

### H-09 · `p_outcome` as specified is not computable, and the shared event space is not shared

**Claims as written.** `LOGOS_HARNESS.md:139`: `p_outcome` is "obtained by **constrained decoding over single-token category labels** and renormalised over the label set." `:161`: the labels are `{no effect, not very, neutral, super}` crossed with 5 quintiles and `{yes, no}`. `:143`: "two models with different tokenizers share no event space over tokens ... Over `O` it is defined."

**Why it fails.** "no effect" and "not very" are two or more tokens in every standard byte-pair encoding, so there is no single-token read over this label set. Worse, the label-to-token map is per-model, so the claim that `O` restores a shared event space holds only if the mapping is verified injective in *every* roster tokenizer.

**Demonstration.** Under a first-token-only read in a byte-BPE where `"no"` is a token and `"not"` decomposes as `"no" + "t"`, the labels *no effect* and *not very* collapse to the same first token: that proposer's effective event space on the effectiveness axis has 3 cells and its partner's has 4, and `JS` is computed over a space one of the two cannot express. Under multi-token sequence scoring instead, the two-word labels carry an extra token's log-probability penalty relative to the one-word labels, with a per-tokenizer magnitude, injecting a systematic model-specific tilt toward two of the four categories before any knowledge is measured.

**Fix.** Use symbol labels (`A`/`B`/`C`/`D`, or digits) with a build-time assertion in `proposers/roster.yaml` that each label is exactly one token and prefix-free in every roster tokenizer, keep the human-readable gloss in the card text, and read the constrained token from the symbol. Add the assertion to `parity_check.py`.

### H-10 · Neither exemplar's `yield` reproduces, and `o_observed` is not recoverable from the trace

**Claim as written.** `LOGOS_HARNESS.md:424` states the file's own standard: "Earlier drafts printed 0.61 **against no distribution at all**." `:433` prints `yield: 2.31` and `:470` prints `yield: 1.04`.

**Demonstration, Substrate A.** The observed outcome is (eff = super, faint = no) per the `outcome` span. Under §2.3's rule (`P_M` the unweighted mean, floored at `ε = 1e-3`, in nats) the five reachable values are 4.089, 3.494, 2.910, **2.384**, 2.544 nats for damage buckets q1 to q5. **2.31 is none of them**; it implies `P_M = 0.0993`, which no cell of the printed vectors produces.

**Demonstration, Substrate B.** The four cells give 0.9343, 1.9512, 1.1893, 1.8289. **1.04 is none of them**; it implies `P_M = 0.3535`, which no cell produces. `realised: fires_vs_shuffle_true` also under-determines the cell, since `O_B` is the product space and the endo/exo half is not recorded in `result`.

**The structural half.** The trace records `hp_delta: -18` and never `o_observed`, and mapping `hp_delta` to a damage quintile needs the defender's max HP, which neither the trace nor the card carries (`:297`: "enemy HP is a bucket"). Minus 18 is quintile 4 at max HP 30, quintile 3 at 36, quintile 2 at 60, all plausible Onix values across levels. `yield_score.py`'s output is unauditable from the artifact it is stored in.

**Fix.** Add a mandatory `o_observed:` field naming the exact cell of `O`, plus the RAM-derived `max_hp` as a probe-label field. Add a `validate.py` assertion that `yield == -ln(floor(P_M)[o_observed])` to four decimal places. Recompute both exemplars.

### H-11 · The Tier-0 total mixes two rosters and is labelled with one of them

**Claim as written.** `TIER0_3090_PLAN.md:157-160`: "`F9 1683.6 + F3 (72 to 120) + F10 96 + F4 48 + F5 0 + F13(a)&F14 17.4 = 1917.0 to 1965.0`", and `:167`: "**Tier 0 total: 1,917 to 1,965 GPU-h at the 1B-class proposer instantiation.**"

**Why it is wrong.** 1,683.6 is the 1B-class F9 figure; 17.4 is explicitly the **8B-class** figure (`F9_PREREGISTRATION.md:619`: "at 2 x 8B ... = 17.4 [ASSERTED]"). At the 1B-class instantiation the same line is **2.2** (`:617`). Recomputed self-consistently at 1B: `1683.6 + 72 + 96 + 48 + 2.2 = 1901.8` to `1949.8`. The stated total is 15.2 GPU-hours high as labelled.

*Second defect.* `TIER0_3090_PLAN.md:105` says limb (a) "runs on this card and, after the proposer repair, **on the same models F9 already loads**", and then two sentences later specifies "**at a four-model 7-to-8B-class roster**". F9 loads **two** proposers of **1B** class (`F9_PREREGISTRATION.md:468`). Two of three roster attributes differ. `:198` contradicts itself within one cell: "reuses the row-1 inventory **plus a capable-end roster**".

**The refutation pass.** Is the label loose enough to survive? No: the same page at `:178-181` treats the roster as a named, decisive band, so a total labelled with a specific instantiation is a commitment. Survives.

**Fix.** Relabel as "F9 at the 1B-class instantiation plus limb (a) and F14 at a 7-to-8B-class roster", or give both self-consistent totals. State that limb (a) and F14 need a second, capable-end roster that row 1 does not cover, and schedule its freeze.

### X-01 · Six figures disagree across five files, and three documents assert a disagreement the paper no longer has

**Claims as written, all current.**

| Quantity | `logos.tex` | `GAPS.md` | `F9_PREREGISTRATION.md` | `TIER0_3090_PLAN.md` |
|---|---|---|---|---|
| F13 limb (b) | **36.3** (`:915`, `:921`, `:933`) | **12.7** (`:10`, `:164`) | 36.3 (`:503`, `:518`) | 36.3 (`:87`) |
| F13 limb (a) + F14 | **17.4** (`:915`, `:917`, `:921`) | "**cost not yet derived for either, and no figure is asserted here**" (`:10`, `:50`, `:165`) | 17.4 (`:536`, `:619`) | 17.4 (`:88`) |
| F9 total | not stated | **1,402.6** (`:43`, `:162`) | **1,683.6** (`:505`, `:508`) | 1,683.6 (`:157`) |
| Tier-0 programme | not stated | **1,619 to 1,667** (`:50`) | not stated | **1,917 to 1,965** (`:167`) |

**Why it matters, and the sharpest part.** Three documents assert that the *paper* is out of date, and it is not. `F9_PREREGISTRATION.md:697`: "**`logos.tex` §15 disagrees with this document on two figures and the paper has not been edited.** It prices F13 limb (b) at 12.7 GPU-hours and says limb (a)'s cost is not derived." `TIER0_3090_PLAN.md:89` says the same, and `LOGOS_HARNESS.md:600` records the edits as "owed there". Verified here: `grep -n "12\.7" logos.tex` returns **no matches**, and `grep -n "not derived" logos.tex` returns **no matches**. `logos.tex:915` carries 36.3 and 17.4, repeated at `:917`, `:921` and `:933`. The edits landed and three documents still record them as owed.

Meanwhile `GAPS.md`, which at `:110` and `:120` twice declares that it defers to the paper as "the register of record for F-numbers", is the one document that has not followed it. Its §0 status paragraph carries the withdrawn 12.7 and the withdrawn "not derived" side by side with a boxed "Superseded count, left standing so the drift is visible" note about a *different* number: the mechanism exists and was not applied here. `GAPS.md:43` and `:162` cite `F9_PREREGISTRATION.md` §8.1 for 1,402.6, and §8.1 does not contain it as a derivation; `:540` there contains it as a **withdrawal** ("priced against an instrument that could not be built and is superseded, not scaled").

**Recomputations.** 1,683.6 reproduces from its own components: `383.1 + 86.2 + 549.5 + 203.8 + 393.9 + 1.81 + 15.0 + 12.0 + 36.3 + 2.0 = 1683.61`. 1,402.6 reconstructs as the pre-repair total, `383.1 + 86.2 + 549.5 + 203.8 + 137.9 + 2.5 + 12.7 + 15.0 + 12.0 = 1402.7`, correct for the withdrawn instrument. `GAPS.md:50`'s 1,619 to 1,667 is `1402.6 + 72/120 + 96 + 48` with limb (a) omitted; the correct figure on current numbers is 1,917 to 1,965, or 1,901.8 to 1,949.8 once H-11 is applied. The difference between 1,402.6 and 1,683.6 is not the limb-(b) re-costing, since `1683.6 - 36.3 + 12.7 = 1660.0`, so the older figure is not recoverable from the current components.

**Fix.** Update `GAPS.md:10`, `:43`, `:50`, `:162` and `:165` to the register of record. Delete or invert the "the paper has not been edited" rails at `F9_PREREGISTRATION.md:697`, `TIER0_3090_PLAN.md:89` and `LOGOS_HARNESS.md:600`.

### The smaller harness items

**H-12 · The Phase-4 gates are declared Phase-0-only and two of the three checks they depend on are not.** `LOGOS_HARNESS.md:551`: "the Phase-4 gates (S4, S5, `tau_JS`) and F13 limb (b) depend on **Phase 0 only** ... Nothing on the proposal path waits for the Phase-1 RQ-VAE." But `:546` requires "the §3.4 parity checks pass" before any arm runs, and `:307` says check 3 "needs Phase 1", while check 1 diffs against "the field list **the Phase-1 reconstruction gate certifies**" (`:303`). Demonstration of the cost: if check 3 drops `status condition`, all 50,000 `tau_JS` calibration proposals were conditioned on a card that no longer exists, so `tau_JS` no longer admits `q = 0.25` and S4, S5 and the 36.3-hour limb (b) were all measured on a retired rendering. The ledger books that inference once. **Fix:** either pre-commit the card field set to the four Phase-1 target fields and forbid post-hoc drops, or state that S4, S5, `tau_JS` and limb (b) are Phase-1-blocked and price one re-calibration. Delete the "Phase 0 only" sentence either way. LOW because the fix is a scheduling statement.

**H-13 · The MFU band is stated three ways and none reproduces.** `F9_PREREGISTRATION.md:690` gives "roughly 1,200 to 1,800 GPU-h from the MFU assumption alone"; `TIER0_3090_PLAN.md:176-178` gives "roughly 2,100 ... roughly 1,450". These describe one quantity and do not overlap at either endpoint. The first is provably the superseded total rescaled: `1402.6 x (30/25) = 1683.1` and `1402.6 x (30/35) = 1202.2`. Recomputed correctly on 1,683.6 at the document's own 2.526 GFLOP per token and 71 TFLOPS: 25 percent MFU gives 7,027 tok/s and 2,180 GPU-hours, 35 percent gives 9,838 tok/s and 1,557, so the band is **1,557 to 2,181**. Separately at `:39` the quoted throughput band of 6.6k to 9.3k corresponds to MFU 23.5 to 33.1 percent, not the 25 to 35 percent stated at `:690`. **Fix:** state one pair and derive the other from it.

**H-14 · "The items are the ones already sealed", for a file that does not exist.** `F9_PREREGISTRATION.md:606` and `:157` assert that battery items are "already sealed" and "written to `logos-harness/eval/battery_v1.jsonl`". The same document says at `:10` "**Nothing in this document has been lodged** ... freezing happens at §11 and that has not occurred", every seal row at `:664-676` reads `*(fill at lodge)*`, and there is no `logos-harness/` directory in the repository. **Fix:** future tense, and "will be sealed at §11 before this limb runs".

**H-15 · The 94-window lifetime yield sums to 93.** `LOGOS_HARNESS.md:363`: "94 adjudicated windows ... (Wikipedia 14 event + 10 calm, WSB 10 + 10, neff_v2 15, neff_v3 10 + 12, neff_v4 12)". `14+10+10+10+15+10+12+12 = 93`. Consequence-free (`log10(5.6e13/9.3e5) = 7.78`, still 7.8 orders) but it is the headline count of the §4.3 recomputation whose whole point is that the earlier numbers were wrong, and `logos.tex:809` carries it into the paper.

**H-16 · The minimum detectable effect is quoted at the wrong N.** `LOGOS_HARNESS.md:602` gives "a single directional probe at **N = 20 to 30** with a minimum detectable effect **around 0.42 sigma**". 0.42 is the value at **N = 35** (`:371`, correct there: `2.4865/sqrt(35) = 0.4203`). At the planned admitted N the paired one-sided MDE is 0.556 at N=20, 0.497 at N=25, 0.454 at N=30, and under the Bonferroni-3 the file itself applies, 0.664, 0.594 and 0.542. §9 understates the design's own MDE by 8 to 58 percent. **Fix:** quote 0.45 to 0.56 (Bonferroni-3: 0.54 to 0.66) at N = 20 to 30, or say the probe is powered only at the unattritted N = 35.

---

## 6. Prior art, and the remaining items

### P-01 · MatFormer claims and measures the property `PRIOR_ART_v03.md` calls unclaimed

**Claim as written.** `PRIOR_ART_v03.md:64`: "every MatFormer submodel shares the same `W_k`/`W_v` and the same layer count, so the caches are trivially shape-compatible and approximately semantically aligned. **The paper does not mention KV cache compatibility or make any claim about it. This is the nearest unclaimed adjacency: the property exists in MatFormer by construction and nobody appears to have exploited it.**" Repeated at `:78` ("never claimed or measured") and `:223` ("latent and unexploited").

**Why it is wrong.** MatFormer claims it in its main text, cites a dedicated appendix subsection for it, and isolates the measurement in its own ablation row. From `https://arxiv.org/html/2310.07707v2`, beside Table 2, verbatim:

> "This additional speed-up can be primarily attributed to the more consistent nature of MatLM-based drafter and verifier models and is further boosted by **the ability to share attention cache across models from MatLM which is infeasible for the baselines** (see Appendix C.1)."

Appendix C.1 is titled "Speculative Decoding Attention Sharing". The measurement, from `https://ar5iv.labs.arxiv.org/html/2310.07707`, separates the shared-cache contribution as its own row: speculative-decoding speed-ups of Baseline 1.10x / 1.08x, MatLM 1.14x / 1.11x, and **MatLM plus shared attention cache 1.16x / 1.14x** on LAMBADA and TriviaQA, with a 1.5B draft and a 2.6B verifier. In a decoder-only transformer the attention cache *is* the key-value cache. So MatFormer is a published, measured instance of a key-value cache produced by a smaller sibling and consumed by a larger sibling of the same parent, across a size boundary, with no translation adapter and no re-prefill.

**The refutation pass, and the weakening.** Two rescues, one partly successful. (i) *Is the sharing trivial because the projections are literally shared weights?* No: MatFormer's submodels differ in feed-forward width, so hidden states diverge after the first layer and the K/V tensors genuinely differ; the separate ablation row is the evidence that the sharing is an approximation that had to be tested. (ii) *Does the residual novelty survive?* Partly. MatFormer varies feed-forward width at constant layer count and gets alignment by literal weight sharing rather than by an objective. **The "candidate contribution" verdict survives on two conjuncts only, differing depth and an explicit learned alignment objective, and the stated reason for it does not.** Everything else in `:64`'s sentence (one parent, no adapter, no re-prefill, small prefills large) is instantiated and measured in MatFormer.

Two consequences. §1.3's proximity ranking puts MatFormer third, below works that never cross a size boundary; for a mechanism defined by crossing one, it is first. And §1.2 carries DroidSpeak as the negative existence result at zero depth difference and has no positive one, which MatFormer supplies, so the section reads as more open than it is.

**Fix.** Rewrite `:64` to state that MatFormer claims and measures cross-submodel attention-cache sharing, with the citation and the two speed-up deltas. Move it to rank 1 in §1.3. Restate the residual novelty as exactly "depth-varying ladder plus a learned alignment objective". Delete "unclaimed adjacency", "latent and unexploited" and "never claimed or measured" from `:64`, `:78` and `:223`.

### P-02 · The Saunshi evidence table mixes two comparators in one column

**Claim as written.** `PRIOR_ART_v03.md:106-114` presents a three-row table with a column headed "iso-FLOP baseline", giving 11.2 on Closed Book QA, 26.7 on Math Word Problems and 35.7 on Reasoning Primitives, with derived gap fractions of 34 percent and 282 percent.

**Why it is wrong.** Fetched `https://arxiv.org/html/2502.17416v1` and `https://ar5iv.labs.arxiv.org/html/2502.17416`. Table 3 gives Base (12⊗1, 12x FLOPs) 8.2 / 26.7 / 35.7, Loop (12⊗2, 24x FLOPs) 9.3 / 34.3 / 51.2, and Baseline (24⊗1, 24x FLOPs) 11.2 / 29.3 / 47.5, with the source stating that "The Loop (12⊗2) model is iso-FLOP with the [24-layer] baseline (both have 24x FLOPs), while Base (12⊗1) is iso-**parameter** with the looped model". The document's single "iso-FLOP baseline" column therefore holds the 24-layer model in row 1 and the iso-*parameter* model in rows 2 and 3.

The derived column does not reproduce. Row 1 needs three numbers and shows two; with the real ones it is `(9.3-8.2)/(11.2-8.2) = 36.7` percent, not 34. Row 2 is `(34.3-26.7)/(29.3-26.7) = 292` percent, not 282. Row 3, left blank, is `(51.2-35.7)/(47.5-35.7) = 131` percent, the cleanest case of the loop beating the deeper model, omitted along with the 47.5 reference.

**The refutation pass, and the weakening.** Does §2.4's verdict ("zero novelty in the distinction") fall with the table? No. Under correct labels the qualitative claim holds in both directions: loop 9.3 below iso-FLOP 11.2 on closed-book QA, loop 34.3 above iso-FLOP 29.3 on math word problems. **Weakened to: the verdict stands, the evidence table does not.** It survives because a referee checking the cited source finds the column header does not match its contents, which is the C-04 failure mode this document exists to prevent, transplanted from "did not look" to "looked and mis-transcribed".

**Fix.** Reproduce all three rows verbatim with correct labels; correct 34 to 36.7, 282 to 292, and add the 131 percent row with its 47.5 reference.

### P-03 · "AIQ has no ratio" is false against the formula the same document reproduces

**Claim as written.** `PRIOR_ART_v03.md:168`: "**Avoided outright.** AIQ has **no ratio and no oracle** in it." `:177`: "Restate falsifier F10's criterion as a numeric threshold on AIQ, **which is bounded and defined on every evaluation set**".

**Why it is wrong.** Fetched `https://arxiv.org/html/2403.12031v2` §3.3: "AIQ(R_θ) = 1/(c_max − c_min) ∫[c_min to c_max] R̃_θ dc". The leading factor is a ratio, the document reproduces the exact formula at its own `:145`, and the denominator vanishes on a degenerate single-cost candidate set, so "defined on every evaluation set" is false against the formula the document itself prints. On boundedness, the RouterBench HTML contains no statement that AIQ is bounded, and the document's own `:295` concedes it ("not explicitly bounded in the paper ... rests on that inference, not on a stated theorem"); `:177` then reasserts "bounded" without the hedge, in the sentence a reader will act on.

**The refutation pass, and the weakening.** Does this overturn the §3.2 verdict that AIQ avoids eta's zero-denominator defect? No: eta's denominator vanishes under *quality* domination, AIQ's under *cost* degeneracy, and these are different events. **Weakened to: the verdict is substantively right and the stated reason is factually false**, introducing a second unremarked degenerate case. The three other RouterBench checks come back clean and are recorded in §7.

**Fix.** At `:168`, "no oracle term, and its only denominator is the cost span, nonzero whenever the candidate models differ in price". At `:177`, "bounded under normalised quality (an inference, not a stated theorem, see §7.11) and defined whenever the candidate set spans a nonzero cost range". Carry the `:295` hedge into `:148`.

### X-04, A-06, P-04, P-05, P-06 · The remaining low items

**X-04 · The paper's own version string is stale.** `logos.tex:20` reads `\date{July 2026. Draft v0.2, position paper (in review).}`. The commit introducing the audited material is titled "logos v0.3 structural pass", and four companions refer to the same file as v0.3, including `LADDER_ARCHITECTURE.md:16` and `GAPS.md:123`. The register of record does not know it is the register of a new version. One line.

**A-06 · "Every input is a property of the analysis rather than an estimate", next to two estimates.** `logos.tex:809` makes that claim and then, in the same sentence, prices a trajectory "**generously at $10^4$ tokens**", an estimate, against `D_opt = 5.6e13`, which `:169` has already declared "an order-of-magnitude placeholder; that is falsifier F1". Both estimates run conservative against the paper's own conclusion, so the 6-to-8-orders verdict is unaffected. **Fix:** delete the clause or restrict it to the window length and window count.

**P-04 · Two counting claims inside the load-bearing negatives, in opposite directions.** `:72` says "the **eleven** search strings in §6.1"; §6.1 at `:238-251` lists fourteen. `:195` says "the **five** search strings in §6.4"; §6.4 at `:268-271` lists four, so a fifth search is asserted that appears nowhere, against `:5`'s contract that "§6 lists every search string so the negative results are auditable".

**P-05 · "All seven papers above" points at a section containing ten.** `:85` instructs the v0.3 author to "cite and differentiate all seven papers above" while §1.2 presents ten and §1.3's ranked list at `:76-81` enumerates nine. There may be a defensible exclusion rule (blog, unverified) but it is never stated, and combined with P-01 the work most likely to fall off a "seven" list is the one most damaging to omit.

**P-06 · "Twenty-one fetches" heads a table of 28 rows.** `:305` against `:307-336`, where four rows record two fetch events each, giving 31.

---

## 7. What round 3 checked and found sound

The clean area is large, and several of the newest constructions are the most careful things in the repository.

### 7.1 Arithmetic that reproduces exactly

- **§11.2's four defects of eta all reproduce, three to the digit.** E1's zero-denominator probability: with towers at 0.90/0.20/0.20 the per-item violation probability is `0.10 x (1 - 0.8²) = 0.036` and `(1-0.036)^50 = 0.1599`, against the stated 0.161 from Monte Carlo. E3's winner's curse, recomputed here **exactly from the order statistics of Binomial(500, 0.70)** rather than by simulation: bias 1.156 at k=2, 2.110 at k=4, 2.918 at k=8, 3.339 at k=12, against 1.16, 2.10, 2.90, 3.31. E4: `1 - 0.75^5 = 0.7627` and `1 - 0.3^5 = 0.99757`, both exact. This is the best-verified passage in the v0.3 material.
- **The PiKV collision analysis is exactly right, including the counts.** Brute-forced every pair in `[2,32]²` here: **584 coprime and 377 shared-factor pairs, totalling 961**, and **zero pairs avoid a collision**, confirming the central point that coprimality is not the fix. The minimal case verifies: at `N_tok=2, N_exp=3` the map reaches four slots and two carry two pairs each. The disjoint-bitfield replacement at Eq. (`:546`) is injective as claimed.
- **The size-axis cost arithmetic is exact throughout.** `7e10 + 7e9 = 7.7e10`, `7.7e10/2.8e12 = 2.75%`, `7.7e10 x 4.25/8 = 40.9` GB, `6 x 7e10 x 1.4e12 = 5.88e23`, `6 x 7e9 x 1.4e11 = 5.88e21`, total `5.94e23`, and against `2.2` to `3.1e25` that is 1.92 to 2.70 percent. Every figure at `:281` reproduces.
- **The MXFP4 density chain is exact.** `2 x 1.4e13 = 28` TB; `1.4e13 x 4.25/8 = 7.4375` TB; NVFP4 at 4.5 bits gives 7.875 TB; the understatement factors are 6.25 and 12.5 percent; K3 at `2.8e12 x 4.25/8 = 1.4875` TB. The eight-part fit at `:67` reproduces: `8 x 192 - 1487.5 = 48.5` and `8 x 288 - 1487.5 = 816.5` GB against the stated 49 and 817.
- **Case 3's memory sizing is exact and its equal-multiple claim is true.** Recomputed per pool: `192/63.75 = 64/21.25 = 32/10.625 = 16/5.3125 = 3.0118`. Every pool genuinely sits at the same multiple of its own floor. (The paper's 3.02 divides by the rounded 106; the 0.3 percent difference has no consequence and is not counted as a finding.) The defect in case 3 is A-01 and it is not arithmetic.
- **Both utilisation figures reproduce.** `1/(5 x 0.60) = 1/3` for the paper, and `1/(4 x 0.55) = 0.4545` with `320/145.5 = 2.199` for `LADDER_ARCHITECTURE.md` §5.3.
- **Essentially the whole F9 cost ledger reproduces.** Independently recomputed and matching: 9.579 at 125M (`1e9/2.90e4/3600`), 61.050 at 350M, the ratio 6.3736, 383.14 for 40 runs, 549.45 for Study 3, 203.76 reserve, 12.02 eval, 1.814 pool, 393.87 generation, 622.60 at n=13, 1676.24 at n=35, the sample-size constant `2(1.6449+0.8416)² = 12.3654` and the resulting n of 8, 13, 20 and 35, the 1,683.61 total, the 1,467.6 / 2,547.4 / 4,707.2 roster band, the A6 head overhead (2,359,296 parameters, 0.259 percent, 76.8 GPU-hours), and every kWh, EUR and USD conversion. The 17.4 derivation reproduces line by line (`2000 x 12 x 2 x 1300 = 6.24e7` tokens at `9.555e12/8e9 = 1194.4` tok/s gives 14.517 hours, plus 20 percent), as does the 36.3 and its 18.1 / 108.8 / 290.1 roster band. The failures in this ledger are H-06, H-07 and H-11, which are derivation and labelling defects, not arithmetic ones.
- **The harness's own information-theoretic numbers reproduce.** Both `js_divergence` values in the §5.3 traces are exact from their own vectors (0.5467 bits on the 40-cell factorised joint, 0.1254 on `O_B`, 0.1017 for the label marginal); the §3.2 collapse table is internally exact; the cost band is exactly linear in proposer size; `1,612,904 / 403,226 = 4.0000` as `q = 0.25` requires; `ln(40/1e-3) = 10.5966`; and `d = 0.42` at N = 35 paired one-sided is right, with Bonferroni-3 giving 0.5020.
- **`LADDER_ARCHITECTURE.md` §5.4's cascade break-even is clean and checkable.** `e* = N_small/N_large` gives 7/64 = 0.109 and 0.277/7 = 0.040 as printed, and the three-tier worked point recomputes to 20.48B. Its own caveat, "every exit rate above is an assumption. None has been measured", is the right disclosure and is made.
- **The falsifier counts are consistent.** "Seven of the fourteen run on one consumer accelerator" resolves to F3, F4, F5, F9, F10, F13, F14; the remaining five plus F11 and F12 make fourteen. Round 2's X-08 undercount is genuinely discharged.

### 7.2 Primary sources verified here

- **The token-supply premise is faithful to Villalobos et al.**, and it is now cited, which repairs round 2's class-two defect at `logos.tex:94`. The 300T effective stock, the 100T-to-1000T interval, the 5x epoch cap and the back-out to a 6e13 central unique stock with a 2e13-to-2e14 interval all check out.
- **`D_opt = 20 N_total` is better supported at trillion scale than the paper's hedging implies**, confirming round 2 §6.1 independently: Kimi K2 at 14.9 and DeepSeek-V3 at 22.1 tokens per total parameter.
- **DeepSeek-V3's layer configuration is as §9.2 states**: 61 layers with the first three dense, hence 58 mixture-of-experts layers, so `16 x 60 = 960` is the right order.
- **RouterBench's constructions are as §11.2 describes them, on three of four checks.** The Oracle Router is a per-item maximum over `k` ("the one that always routes to the best-performing LLM"), so `logos.tex:666`'s chance-inflation critique is accurate; RouterBench does **not** state AIQ is bounded, which `logos.tex:664` discloses correctly; and the non-decreasing convex hull is the published construction, with the Zero Router built from the models' "collective non-decreasing convex hull". Only the "no ratio" claim fails, and it fails in the companion rather than in the paper.
- **DroidSpeak does not defeat the ladder-distillation novelty claim, and `PRIOR_ART_v03.md` handles it correctly.** `arXiv:2411.02820` requires that "the pair of models should share the same foundational model" and states it "does not support KV cache sharing across LLMs originating from different foundation models", so it never crosses a size boundary. The document's refusal to cite it as support, and its extraction of the damaging detail that DroidSpeak "selectively recomputes a few layers of the KV cache produced by another LLM", is the best-argued passage in that file. **The brief for this review named DroidSpeak as a direct negative; it is not, and this report says so.**
- **`arXiv:2604.00317` supplies the intra-datacentre round trip used in A-04**: 24.3 microseconds for mixture-of-experts all-to-all with IBGDA, 18.0 with a CPU proxy, 16.7 device-initiated.

### 7.3 Constructions that are honest and hold

- **`logos.tex` §3.3 states the lineage arithmetic with the correct quantifier.** `:247`: a 98 percent common seed "**is one way to guarantee** that". That is exactly right and it is what the companions lose. The lineage table at `:239` is a genuine and unusual disclosure, and `:249`'s marking of two unverifiable inferences rather than asserting them is the standard round 2 asked for.
- **`LADDER_ARCHITECTURE.md:144` is the single most careful sentence in the v0.3 material.** R-01 is a finding against the four restatements that drop it, not against it.
- **The eta retirement is correctly framed as no contribution.** `logos.tex:644`: "Nothing in this subsection is a contribution." §11.2's E1 admission that APGR "does **not** avoid it structurally" is the right disclosure and is volunteered.
- **§4.5's router prior-art retraction is a real fix** and the correct response to round 2's C-04 method failure: `:335` says the round-2 audit "never examined the routing literature at all" and `:337` withdraws all novelty claims about the router.
- **The status language has not softened and in places has hardened.** `logos.tex:34`, `:880` and `LADDER_ARCHITECTURE.md:1131` ("No model has been trained. No adapter has been fitted ... The 3090 has not been switched on for any of this") are blunter than v0.2's equivalents. `LADDER_ARCHITECTURE.md:237` and `:478` both stop mid-argument to say the inputs are unmeasured. `F9_PREREGISTRATION.md:147` declines to name a proposer roster rather than assert an availability check it has not run. No claim of a measurement never taken was found in `logos.tex`; the two that appear are H-14 (a seal) and the stale-ledger statements of X-01.
- **`PRIOR_ART_v03.md` §7's thirteen self-declared gaps, and its instruction at `:193-:197` not to write "nobody has measured this" without a qualifier, are the correct standard**, and `GAPS.md:154` carries the provenance caveat forward rather than quietly relying on the document. That discipline is why P-01 is a finding about one verdict rather than about the file.
- **Remark `rem:nomerge` at `logos.tex:698` is the strongest new argument in the paper.** Key-value state has no merge function, a session ref must therefore advance fast-forward only under a single designated writer, and multi-writer access "is not a merge conflict, it is a silent-corruption path, because nothing errors". Correct, absent from the sources it builds on, and the kind of claim the paper should make more of.
- **`F9_PREREGISTRATION.md` §9.4's UNDERPOWERED rule and `:579`'s refusal to widen the equivalence margin are the right instincts**, correctly reasoned, and they are the standard against which H-05 is graded a failure.

---

## 8. Findings that did not survive refutation

Recorded because the refutations are informative, and because two were premises of the brief that commissioned this review.

- **"The `D_opt = 20N` input is unjustified and dissolves the over-constraint."** Dropped. At Kimi K2's 14.9 and DeepSeek-V3's 22.1 tokens per total parameter, correcting the law moves `g*` from 0.982 to 0.890 or to 1.008, unsatisfiable at any `g`. **The input is sound and correcting it does not help the architecture.** F1's real content is that the law does not survive being keyed on *active* parameters (K2 at 484, V3 at 400 tokens per active parameter), which is not how `logos.tex:889` states it.
- **"DroidSpeak is a direct negative to the KV-ladder novelty claim."** Dropped on the primary source. The negative that does bite is MatFormer.
- **"F13 limb (b) is dead on arrival."** Weakened, not dropped, and it became F-01: the version printed in `logos.tex:915` is satisfied by a theorem the paper accepts, and the version specified in `LOGOS_HARNESS.md:81` is a genuine test. The finding is that the register of record carries the dead wording.
- **"Case 3's `3.02` is wrong; the true multiple is `3.01`."** Dropped as noise. The equality across pools is the load-bearing claim and it holds exactly.
- **"§9.2's 60 round trips per layer understates, because a layer's latency is the maximum over 16 peers."** Dropped as a finding and recorded as a note: it is true, `logos.tex:685` already says it, and it makes the paper's figure conservative in its own disfavour, which is the right direction.
- **"The 94-window lifetime yield double-counts overlapping windows."** Dropped. `REVIEW_ROUND2.md:666` documents pairwise overlaps up to 83 percent, so the count does include overlapping looks, but the effect makes the demonstrated yield look *larger* and the shortfall *smaller*, so it runs against the paper's own conclusion and cannot be a defect in it. (The separate 94-versus-93 arithmetic slip survives as H-15.)
- **"The §4.3 power calculation uses a paired formula on an unpaired contrast."** Dropped. `LOGOS_HARNESS.md:371` ties the calculation to "the three pairwise comparisons a four-arm ordering needs", and scoring the same episodes under four arms is a paired design.
- **"The shuffle adjudicator is not independent of the observation."** Dropped. `window_for()` spans `[onset-90d, onset+22d)`, so 80.4 percent of the adjudicator's input is the pre-onset window the proposer conditions on, but no mechanism was constructible by which sharing the window lets the proposer infer the verdict rather than the null's location. Worth one clarifying sentence at `:369` that "contamination-proof" means memorisation-proof only.
- **"The cost band and the generation row are inconsistent."** Dropped. The 38 GPU-hour-per-B gap between §0's totals and §8's generation row is fully absorbed by limb (b) at 36.3 plus about 1.8 for the `tau_JS` pool; the three totals are exactly collinear.

---

## 9. What round 3 could not check

- **Whether the pre-committed outcome space is constructible without reference to the observed outcome.** The design requires it be fixed before observation, and no instance of one exists in the repository. That is a construction question and it needs an example, not an argument. H-03 is the closest this pass could get.
- **Whether Branch-Adapt-Route strictly requires a common seed.** `logos.tex:249` marks this as a reading of `morrison2026bar` rather than a quoted claim, and this pass did not resolve it either. It is the premise that makes `λ ≥ 1` mandatory and therefore the premise the whole lineage section rests on. If it is false, the trilemma has a fourth exit nobody has looked for.
- **The three unfetchable sources.** `su2026qb` returns HTTP 403 to automated retrieval and the paper says so at `:1067`; `PRIOR_ART_v03.md` §7 names non-English literature as its largest blind spot, and both Quantile Balancing and Causal Dual Bias originate there.
- **The proposer roster.** It is not named anywhere (`F9_PREREGISTRATION.md:147`), `proposers/roster.yaml` does not exist, and there is no `logos-harness/` directory in the repository. Every figure that depends on roster identity, which is 17.4, 36.3 and the 18.1-to-290.1 band, is a cost for an instrument not shown to exist. That is disclosed inside the pre-registration and not where the numbers are consumed.
- **Anything requiring a run.** Nothing here has been executed. Every finding above is a defect in a document, and the paper's own `:935`, "Nothing here is a result", is the correct frame for reading all of it.

---

## 10. The three to fix first

1. **R-01.** It is one file's honest sentence against four of its own restatements, it costs three edits, and until it is fixed the repository is carrying an architectural decision (`LADDER_ARCHITECTURE.md:152`, drop the diversity budget) taken on a point estimate from a factor-of-ten interval.
2. **A-01.** §11.1 case 3 is the paper's last checkable argument by its own account at `:613`, it is reprinted in the conclusion, and it does not deliver what it claims. Either state the sparsity convention that makes it work, or withdraw the recovery claim.
3. **H-01.** F9 is the experiment the paper says it would run first, its training corpus is built from a span with no specified generator, and the only worked example of that span states the adjudication and states it incorrectly. This is cheap to fix and it invalidates the corpus if it is not.
