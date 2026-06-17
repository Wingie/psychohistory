# Comment-Concordance Check: lethain models vs the ACTUAL r/AskEconomics expert answers

This upgrades the earlier lethain-model validation from *"agrees with textbook
economics"* (a self-judged concordance with the framework's own reading) to
*"agrees with the real top vetted answer"* on each r/AskEconomics thread. We
harvested the comment threads for all 100 posts and scored the 88 posts that
carry a per-post lethain model against the actual approved answer.

## Method

- **Harvest** (`harvest.py`): pulled comments for all 100 posts via the Arctic
  Shift API (`arctic-shift.photon-reddit.com/api/comments/search?link_id=<id>`;
  the base-36 id without the `t3_` prefix). All 100 threads returned data, 0
  errors. Raw comments cached to `data/<id>.json`.
- **Extract the vetted answer** (`extract.py`): r/AskEconomics removes most
  popular non-expert takes, so the raw top-scored comment is the *wrong* target.
  The vetted answer is written by a flaired contributor, so we select the
  substantive (>=120 char), non-removed, non-AutoMod, non-mod-note comment by a
  **`Quality Contributor` / `AE Team` / `REN Team`** author, preferring
  top-level; Reddit score is only a weak tiebreak. We fall back to the best
  surviving substantive comment when no flaired contributor is present in the
  snapshot.
- **Score** (`score.py`): each post with both a model and a retrieved answer was
  read by hand and judged AGREE / PARTIAL / DISAGREE, or NA when the snapshot
  yielded no real vetted answer (a moderation note, a clarifying question, a bare
  link, or an off-topic aside).

### Honesty about the harvest

Arctic Shift archives each thread close to its posting time, so the snapshot
sometimes predates the full approved answer or froze scores early. 68/88 posts
resolved to a genuinely flaired-contributor comment; the remaining 20 used the
non-expert fallback. **12 posts (NA)** had no usable answer in the snapshot at
all (e.g. `1qy91q0` = "cigarettes were cheaper on base"; `1p9y341` = a mod's
"please link the SEC filings"; `1pt2wou` = "don't bypass top-level moderation").
Those are excluded from the concordance rate rather than charitably counted.

## Counts

| Verdict   | All 88 | Among the 76 with a real answer |
|-----------|:------:|:-------------------------------:|
| AGREE     |   38   |   38  (50%)                     |
| PARTIAL   |   27   |   27  (36%)                     |
| DISAGREE  |   11   |   11  (14%)                     |
| NA        |   12   |    -                            |

- **Posts that got a real expert answer: 76 / 88.**
- Of those 76: **50% AGREE, 36% PARTIAL, 14% DISAGREE.**

## Comparison to the earlier textbook-economics check (48 / 40 / 0)

The earlier `lethain_models.jsonl` check scored **48 AGREES / 40 PARTIAL / 0
DISAGREE** against established economics and the framework's own reading. Its
own `honesty` field flagged the limitation: it was *"compared to established
economics ... NOT to the thread's actual top comments."*

Scoring against the **real** answers does what we suspected it would: it surfaces
genuine mismatches. **Zero disagreements became eleven.** And the disagreements
are not noise — **10 of the 11 DISAGREEs were rated `AGREES` by the old check.**
The textbook check was systematically over-confident exactly where the model's
abstract conclusion and the expert's concrete answer pull in opposite directions.

| | Old (vs textbook) | New (vs real answers, among 76) |
|---|:---:|:---:|
| AGREE | ~55% (48/88) | 50% (38/76) |
| PARTIAL | ~45% (40/88) | 36% (27/76) |
| DISAGREE | **0%** | **14% (11/76)** |

The headline AGREE share barely moved, but the previously-empty DISAGREE bucket
is now populated, and the PARTIAL/AGREE split tightened — i.e. the real check is
strictly more discriminating.

## The most interesting DISAGREEMENTs

A clear pattern: **5 of the 11 disagreements come from the `concentration/bubble`
template**, and most are cases where the framework treats wealth/price
concentration as a structurally-guaranteed runaway while the expert's actual
answer *deflates that very mechanism* or assigns it the *opposite valence*.

1. **`1qvem06` "Could we close the billionaire borrowing loophole?"** — Model:
   untaxed-borrowing-driven concentration is structurally guaranteed (Pareto).
   Expert (Uptons_BJs): the buy-borrow-die loophole "isn't a great strategy" —
   2% APR compounds for life and back-of-envelope math shows selling + paying
   cap-gains often wins. The model's central mechanism is exactly what the
   expert deflates. (Same story for `1m11gep`: ZhanMing — collateral loans only
   *delay* tax and are capped by margin-call risk.)

2. **`1q15un1` "Aren't billionaires not hoarding because their wealth is
   invested?"** — Model frames concentrated wealth as a problematic runaway.
   Expert (No_March): below the Solow golden rule, the rich's high savings are a
   *boon*, and you can't redistribute without destroying investment incentives.
   **Opposite valence on the identical fact.**

3. **`1ncv5bf` "Nvidia is worth $4T — how is this not a bubble?"** — Model
   ("concentration/bubble", Minsky) implies bubble dynamics. Expert (econheads):
   this is *explicitly not* a 2000-style bubble — Nvidia already earns large
   profits and holds a dominant position. Direct conflict in the conclusion.

4. **`1sbrjv5` single-payer CBO / `1mlrjzl` "are tariffs a tax on the consumer?"
   / `1ntscmb` GDP and imports** — three `fiscal-capacity` / `expectations-loop`
   cases where the expert's answer is a *methodological correction* the model's
   fixed-budget or anchored-price abstraction cannot represent. isntanywhere:
   "you can't hold the $100 fixed" — the exact fixed-pot assumption the
   fiscal-capacity template bakes in. syntheticcontrols: tariff incidence is
   *split by elasticity*, not a clean consumer tax. MachineTeaching: cutting
   imports does *not* mechanically raise GDP.

5. **`1qelqsy` "Could Europe coordinate a US-Treasury sell-off?"** — Model:
   Diamond-Dybvig bank-run (a self-fulfilling run on a conserved deposit base).
   Expert (Cutlasss): a coordinated sell-off crashes prices and the *seller*
   eats the loss — it's self-limiting and hurts Europe more than the US.
   **The canonical run logic the model invokes is precisely what does not apply.**

6. **`1nn7am1` "Why are red states poorer / more unequal?"** — Model accepts the
   premise and asserts guaranteed concentration. Expert (No_March): not convinced
   inequality is even higher in red states; the gap is largely omitted-variable
   bias (rural vs urban density). The model accepts a premise the expert rejects.

What these reveal: the framework's small library of conserved-carrier templates
("a stock concentrates / drains / converges") encodes a **direction and a
valence**. When the expert's answer is *also* about direction (slow grind vs
collapse, sustainable vs not), concordance is high. When the expert's answer is a
**premise-rejection, an incidence/accounting correction, or an opposite
valence** ("concentration is fine here", "this isn't a bubble", "the run doesn't
apply"), the template has no way to represent that and quietly disagrees — which
the old textbook check papered over as AGREES.

## Caveats (honest)

- **LLM-judged agreement is subjective.** AGREE/PARTIAL/DISAGREE were assigned by
  one reader (me). Several PARTIALs could defensibly be AGREE or DISAGREE; the
  14% DISAGREE rate is a floor on "genuine mismatch", not a precise figure.
- **The top comment is not always the definitive answer.** Arctic Shift snapshots
  are early; scores were sometimes frozen and the full approved answer sometimes
  hadn't posted yet. We mitigated this by selecting on contributor flair rather
  than raw score, but 20 posts fell back to a non-flaired comment and 12 are NA.
- **Many "expert" comments are short replies, not the headline answer.** The
  snapshot frequently caught a Quality Contributor's brief follow-up rather than
  their main essay; that biases some judgments toward a narrow sub-point.
- **This measures concordance-with-experts, not forecast skill.** Agreeing with
  the consensus explanation of *why* something happened is not the same as
  predicting *what happens next*. None of these threads were scored against a
  realized outcome. The skill-horizon question from the framework remains open.
- The `concentration/bubble` template's 5 disagreements suggest it is over-
  applied: it is selected for "anything about wealth/markets/billionaires" and
  then asserts a runaway-concentration conclusion that the experts often reject.

## Files

- `harvest.py` — harvester (Arctic Shift, all 100 posts cached to `data/`)
- `extract.py` — vetted-answer extraction (flair-based)
- `score.py` — per-post verdicts -> `concordance.jsonl`
- `concordance.jsonl` — one record per modelled post (id, title,
  expert_answer_gist, model_conclusion, verdict, justification, _meta)
- `data/<id>.json` — cached raw comments for all 100 posts
