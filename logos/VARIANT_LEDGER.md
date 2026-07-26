# The LOGOS variant ledger

LOGOS is not a point in design space. It is a family, and this document is the
record of which members of that family have been built, measured, and killed.

The architecture has roughly a dozen slots — how disjointness is decided, how
towers compose, where trajectories come from, when a gate fires, what substrate
a claim is measured on. Each slot admits several concrete fillings, and the
falsifier suite is the filter that decides between them. A variant that dies
under the filter is not a mistake to be tidied away; it is a measurement of the
design space, and it is the reason the surviving configuration can be built on
with confidence rather than merely believed.

What follows is therefore written forward. **Variants tried, what the eval
framework did to them, what survived, and what is still live.** There will be
further variants with different accuracies and efficiencies; the point of the
ledger is that each one arrives with its predecessors' cause of death attached.

**Honest status.** LOGOS has zero runs at its designed scale. Every number below
comes from nano-scale probes on one RTX 3090 (24 GB, compute capability 8.6) or
from measurements over real corpora on CPU. Nothing here settles a 2.8T claim.
What it settles is which mechanisms are worth spending a 2.8T budget on.

---

## Slot 1 — How is domain disjointness decided? (falsifier F11)

F11 asks whether the domains that towers specialise in are separate enough that
routing between them pays. Two operationalisations have been built and both are
dead.

| variant | kind | verdict | evidence |
|---|---|---|---|
| token-type Jaccard, merge at 0.30 | model-free, lexical | **killed** | Python vs English prose J = 0.3246, above the frozen threshold — the criterion demands that code and prose be merged into one tower. Four unrelated corpora span only 0.26–0.32; the measure has no dynamic range to spend. |
| normalized compression distance (LZMA, 64 MB dict) | model-free, structural | **killed** | Under a project-disjoint null, separation is +0.0168 and the distributions overlap. |
| gradient conflict / cross-perplexity transfer | **model-relative** | **live, untested** | Forced by the failure mode of both predecessors; see below. |

### Why Jaccard died

It measures vocabulary sharing. Code and prose share a vocabulary — identifiers
are English words, comments are English sentences, prose quotes code. The
distinction that matters for routing is structural, and a set-membership test
over token types is blind to all of it.

### Why NCD died, and why the first reading of it was wrong

NCD asks the structural question directly: if knowing corpus A helps compress
corpus B, they share exploitable regularity. A first measurement appeared to
vindicate it — within-domain 0.8749, between-domain 0.9648, separation +0.0899
with no overlap — and was briefly recorded as showing that *the criterion was
broken but the architecture was fine*.

That reading does not survive its own null. The baseline had been computed by
splitting each corpus's document list in half, which puts files from the same
project on both sides. Same-project files share authorship, house style, local
identifier vocabulary, licence headers, and sometimes literally copied blocks,
so the "within-domain" figure was measuring **within-project redundancy** —
much tighter than genuine within-domain variation, and every separation computed
against it is inflated by the difference.

Re-measured on real corpora (`D:/code`, four domains, size-balanced,
deduplicated, project-stratified) with a null in which **no project appears on
both sides**:

```
mean within-domain (naive, document split)     0.9095
mean within-domain (project-disjoint)          0.9673      inflation +0.0578
mean between-domain                            0.9841
separation vs naive null                       +0.0746
separation vs project-disjoint null            +0.0168
complete separation under honest null          False
```

Project straddle fractions in the naive split ran 33–100%, so the inflation was
structural rather than marginal. The overlap is explicit: **markdown and Python
sit at 0.9661, closer together than JavaScript sits to itself across projects at
0.9814.** A criterion that rates two different domains as more alike than one
domain is to itself cannot be used to decide tower boundaries.

The diagnosis is **saturation, not absence of structure.** Every distance lands
between 0.95 and 0.99. A general-purpose compressor at 3 MB per corpus finds
almost no exploitable cross-corpus regularity in any pairing, so it has no
resolution left to answer the question with. This is a fact about LZMA's reach,
not a finding about domains.

### What survives, and why it is forced

Both dead variants asked a **model-free** question — do these corpora share
words, do they share compressible regularity. Routing does not pay when corpora
are dissimilar in the abstract; it pays when **one expert's parameters do not
substitute for another's.** That is a property of a learner, not of text.

This is the same move the paper already makes in §12, where yield is defined as
`−log P_M(o | context, a)` — surprisal relative to the model, not entropy of the
source. F11 must be operationalised the same way. The leading candidate is
**gradient conflict**: train one model, compute per-domain gradients, measure
their cosine similarity. Domains that want opposite parameter updates are
domains worth separating, and the measure carries its own null — within-domain
gradient cosine — so the threshold calibrates rather than being chosen after the
fact. A cross-perplexity transfer matrix (fine-tune on A, measure Δ perplexity
on B against held-out A) answers the same question asymmetrically and is the
natural second.

**Provenance note.** The original structural result was not reproducible from
any committed code: `f11_structural.py` was untracked, and the LZMA dictionary
setting that produced the reported numbers existed only as an unsaved edit to a
file that reads `zlib` on disk. That is the same class of defect as a moved
threshold. The compressor is now a named, pinned parameter written into every
result record.

---

## Slot 2 — How do towers compose?

| variant | verdict | evidence |
|---|---|---|
| majority vote | **killed** | E-LAD run 4: with heterogeneous member quality (two strong, four mediocre) the ensemble scored *below* the best single member at every scale. A weak majority outvotes a strong minority. Voting was never in the design; it was a scaffold that leaked into experiments. |
| confidence router (max softmax) | measured, not evidence | Captures ~98% of a perfect domain router's gain **on a substrate that does not qualify** — see Slot 6. |
| **learned router** | **the design** | Untested at any scale. |

Voting is dead and should not reappear. The paper has always specified a learned
router; the composition experiments that used voting were testing something the
architecture does not propose.

---

## Slot 3 — Where do trajectories come from? (falsifier F9, §12)

This is the slot that decides whether anything is left past the human-data wall,
and it is the one where the framing needed the most repair.

| variant | loop | verdict |
|---|---|---|
| unfiltered hard pseudo-labels, argmax decoding | closed | **killed, but for the wrong reason** |
| self-consistency–filtered self-training | closed | **killed — worst arm measured** |
| disagreement-gated self-training | closed | **killed** |
| distillation from a stronger model | open (other model) | works; diffuses a frontier, does not advance one |
| adjudicated / verified trajectories | open (verifier) | **only surviving arm** |

### The measurement

Eight seeds, paired within seed, token counts matched exactly at 6000 supervised
positions per arm, sampling rather than argmax, on the Zipfian substrate.

```
arm                     acc      vs floor       t
A0_floor             0.5903         --          --
A3_grounded          0.5962      +0.0059     +12.34
A1_unfiltered        0.5828      -0.0075     -18.11
A2_gated             0.5763      -0.0140     -23.27
A1p_self_consistent  0.5621      -0.0282     -49.57
grounded vs closed-filtered      +0.0341     +69.36
```

**Only the arm with an exogenous signal improves.** Every closed loop degrades,
and the self-consistency–filtered arm — built the way working self-training
methods build it, and the one the sharpening literature predicts *should* gain —
is the worst of the four. Filtering is not merely insufficient here; it is worse
than not filtering.

The frequency bands rule out the obvious reading:

```
                       head      b2      b3    tail
A0_floor             0.6793  0.0078  0.0047  0.0032
A3_grounded          0.6861  0.0078  0.0041  0.0038
A1p_self_consistent  0.6470  0.0056  0.0035  0.0021
```

This is not a failure to learn the tail. A1' **loses the head it was most
confident about**, despite accepted-label precision of 0.8435 against a Bayes
ceiling of 0.8503 — near-optimal labels, and training on them still costs
accuracy. A3 gains in both head and tail.

**Confound, stated rather than buried.** A1' and A3 differ in two ways at once:
provenance (self-generated versus ground truth) and composition (the
self-agreement filter accepts a Zipf-head-skewed subset, while A3 sees a
representative one). This run cannot separate them. The next run subsamples A3
to A1's key-frequency distribution. Until then the finding is **"the closed loop
degrades"**, not yet **"because it is closed"**.

Scope: one model size, one synthetic substrate, nano scale. It is evidence about
a mechanism, not about 2.8T towers.

### The correction that matters

An early run trained one arm on the model's own argmax outputs, saw it degrade,
and recorded "self-play degrades". That claim is wrong twice over.

First, it is not what self-play means. Unsupervised pretraining is training on
*exogenous* text; that loop was training on *endogenous* output. Conflating them
makes the claim read as an attack on self-supervised learning, which is how
every one of these models is built.

Second, the arm that died is the one nobody uses. Unfiltered hard
pseudo-labelling reinforces the network's own errors — a result published in
2019, with in-loop fixes (soft labels, confidence thresholds) that require **no
exogenous signal at all**. Every working self-training method filters: STaR,
RFT, ReST-EM, self-consistency. So that arm separates *hard labelling from
soft*, not *closed loop from open loop*, and cannot bear on the observation
bound.

### What the bound must not say

Three formulations were tried and discarded before one held:

- ~~"training on self-generated data degrades"~~ — **false.** Self-distillation
  improves generalization with provably zero new task information; born-again
  networks improve with no ground-truth term in the student objective.
- ~~"information gain is bounded by the entropy the external source injects"~~ —
  **wrong currency.** A deterministic verifier injects zero Shannon entropy.
  AlphaZero is given nothing but the rules of the game — a few kilobytes — and
  goes from random to superhuman. That formulation predicts AlphaZero is
  impossible. The right currency is information relative to a **computationally
  bounded** learner, which is exactly what §12's model-relative surprisal already
  encodes and what this restatement briefly lost.
- ~~"closed loop → collapse"~~ — **over-stated.** Under accumulation rather than
  replacement, test error has a finite upper bound independent of iteration
  count. The honest verb is **plateaus at a ceiling set by the base
  distribution's coverage**, degrading only when real data is discarded too.

### What survives

Closed-loop self-training is a **sharpening operator, not a source**. It
reallocates mass toward sequences the base already covers, and its reach is
governed by that coverage. It can raise measured performance with no new
information — and the ceiling is the adjudicator's, since verified iterative
retraining converges to the verifier's knowledge centre rather than to the truth.

**The token-wall corollary is not ours to claim.** That capability accrues where
verification is cheap is the received view — it is the premise of debate, it is
the "generator–verifier gap", it is stated as a law by Wei ("the ease of training
AI to solve a task is proportional to how verifiable the task is") together with
its consequence, a jagged capability edge, and the data-wall paper itself routes
the escape through verifiability. We cite it. We claim only the
architecture-specific derivation and the loop. We also inherit the standing
objection: verifiability makes a task trainable, not tractable, and graph
3-colouring is the counterexample a referee will raise.

**A fourth move exists past exhaustion, and the paper lists three.** Repeat,
self-synthesise, and ground are there; **distil from a stronger model** is not.
It genuinely expands a student's reasoning boundary and can exceed the
supervisor — but it diffuses a frontier rather than advancing one, which is
precisely why it is not a route past the wall *for the frontier operator*.

---

## Slot 4 — When does the competence gate fire?

| variant | verdict |
|---|---|
| disagreement gate between two models | **no-op below competence** |

Measured disagreement rate 0.9981 — with both models incompetent, they disagree
everywhere, so the gate admits everything and is equivalent to no gate at all.
This confirms the S5 competence-floor prediction and is the one genuinely useful
output of the first F9 run.

The same shape appears in the admission function: **R(C) is peaked, not
monotonic** — admission 1.000 below the band, 0.468 at accuracy 0.99, 0.000 by
accuracy 1.0. A gate that admits everything from the incompetent and nothing
from the saturated has a narrow operating window, and locating that window is a
design parameter rather than an afterthought.

---

## Slot 5 — What substrate can measure partial competence?

| variant | verdict | evidence |
|---|---|---|
| induction (copy the prefix) | **killed** | No partial-competence band exists. |
| noisy induction, principled Bayes ceiling | **killed** | Same failure; the ceiling helps, the transition does not. |
| Zipfian key→value recall | **live** | Under test. |

Induction is an algorithmic circuit: it either has formed or it has not. Measured
on this card, a 4-layer decoder goes from 0.5323 at warm-up step 120 to 0.6575 at
step 150 — through the entire Bayes ceiling of 0.6507 — in about thirty steps.

This is fatal for any experiment about *partial* knowledge, and the two
conditions a closed-loop arm needs turn out to be disjoint on it:

```
warm=120   acc 0.5323 (81.8% of Bayes)   self-consistency accepts 0.04%
warm=400   acc 0.6523 (100.3% of Bayes)  self-consistency accepts 33%
```

Below the transition the model is too incoherent to agree with itself, so the
filter accepts nothing; above it there is nothing left to learn. **The arm cannot
be run on this substrate at all** — not because the hypothesis is wrong, but
because the substrate has no regime in which the question is meaningful.

One diagnostic from that scan is worth keeping regardless of substrate: the
self-consistent labels have precision ≈ 0.65 at every threshold, which is the
model's own accuracy and the Bayes rate. **The filter recovers the model's
competence and never exceeds it** — sharpening with no information gain, visible
directly in the numbers.

Zipfian key→value recall replaces the circuit with memorisation. Frequent keys
are learned in hundreds of steps and rare ones take orders of magnitude longer,
so accuracy climbs smoothly over a long range and the model is *partially*
knowledgeable throughout — the state the experiment requires. Head-versus-tail
reporting by frequency band separates "sharpened what it knew" from "learned
something new", which is the distinction the whole observation bound rests on.

---

## Slot 6 — What counts as a domain in an experiment?

| variant | verdict |
|---|---|
| six members differing only by random seed | **killed** — no complementary expertise exists to route over; η = −0.347 |
| skewed regions of a single synthetic vocabulary | **killed** — not domains |
| genuinely distinct real corpora | **required** |

The second of these produced η = +0.967, and that number does not transfer.
Members trained on skewed regions of one vocabulary differ in word *frequency*,
not in reasoning structure. Real domain separation means coding versus creative
writing versus business-intelligence reporting versus formal verification versus
protein folding — tasks that differ in what reasoning is performed, not in which
tokens are common. The result is recorded as a killed experimental design, not as
support for the architecture.

---

## Slot 7 — What does the hardware actually permit?

| claim | status |
|---|---|
| 25× speedrun improvement | **not transferable** — requires FP8; GA102 is compute capability 8.6 and the probe recorded `supports_fp8: False` |
| transferable speedup | 3.19× published, **2.57× measured** |
| Muon (2D params only) + ModernFFN | adopted |
| throughput | 13,877 tok/s @ 350M, 37,905 tok/s @ 125M, micro-batch 4 |

The throughput figures used AdamW and are therefore a floor. Windows WDDM
oversubscribes into system RAM, so a 350M model at batch 8 reached 32.67 GiB on
a 24 GiB card without raising — memory fit must be checked by peak allocation,
not by waiting for an OOM that never comes.

---

## What is live

1. **F11 re-operationalised as a model-relative measure** — gradient conflict
   first, cross-perplexity transfer second, each with its within-domain null
   pre-registered before any between-domain number is looked at.
2. **F9-v3, the confound split** — rerun with A3 subsampled to A1's
   key-frequency distribution, so provenance is the only difference between the
   arms. This is what upgrades "the closed loop degrades" to "because it is
   closed", and it is cheap: the v2 run cost minutes on one card.
3. **The learned router**, on members that are actually complementary.

Each of these can kill a piece of the architecture. That is what they are for.
