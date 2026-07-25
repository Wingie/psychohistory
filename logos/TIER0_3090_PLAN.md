# Tier 0: what runs on the owned 3090

**This is a run plan, not a funding document.** Owner decision, 2026-07-25:
funding is a consequence of experiments succeeding on this card, not a
precondition for attempting them. The order is F9 runs -> it produces a real
result -> the result is the argument. Pricing a rung inside a ledger is
engineering; a pitch written before there is a run is not.

Derived from the round-2 audit (`REVIEW_ROUND2.md`) and the design in
`F9_PREREGISTRATION.md`, which is a commitment artifact and is **not yet
lodged**. Figures marked **[derived]** were independently computed and are
shown with their arithmetic; **[repo estimate]** carries `GAPS.md` forward
without re-derivation.

**The register of record is `../logos.tex` §15, and it now carries fourteen
falsifiers.** Seven run on one consumer accelerator: F3, F4, F9 and F10 as
independent experiments, F5 and F13 limb (b) falling out of F9, and F14 sharing
an instrument with F13 limb (a), which runs on that card too but is not an F9
arm. **F11 and F12 need no accelerator at all** and appear nowhere on this page:
F11 is a corpus-overlap measurement against the partition criterion of
`logos.tex` **§3.5**, F12 is a residency classification against §11.4's
`eq:residency`, and both are the cheapest tests of the paper's remaining
motivation for towers. The lineage parameter those two sit downstream of is
§3.3, and the 400x extrapolation the whole ladder is a bet on is **§3.4**.

**One metric note, so this page does not contradict the paper.** `logos.tex`
§11.2 **retires** eta rather than demoting it, and reports **AIQ** as the
primary scalar with **APGR** and **CPT(50%)** as the secondary pair. F10's
criterion on this page is therefore read on AIQ: a warm-started router fails
F10 if, on any domain carrying at least 5% of evaluation traffic, its post-swap
AIQ falls more than 0.02 below its pre-swap AIQ, or its CPT(50%) rises by more
than ten percentage points of calls. Stated on eta it was unmeasurable whenever
eta was negative or undefined.

---

## Correction that moved every number on this page

The throughput this plan was originally priced against was wrong, and it was
wrong in the direction that flattered the plan. `LOGOS_HARNESS.md` gave 18k to
30k tok/s at 350M, interpolated from 4090, A30 and L20 runs and never measured
on a 3090. At 2.526 GFLOP/token, 30k tok/s demands 75.8 TFLOP/s sustained,
above the card's dense BF16-with-FP32-accumulate peak of **71 TFLOPS** (NVIDIA
GA102 whitepaper, Appendix A Table 9, p.44; the 142 figure applies only with
2:4 structural sparsity, which does not apply here). The same table lists
FP16/BF16/TF32/INT8/INT4 and no FP8 row, which independently confirms that
this card runs bf16 and FlashAttention-2 and cannot run FP8.

`LOGOS_HARNESS.md` §5.4 now carries the replacement, still arithmetic and
still not a measurement: **about 9.1k tok/s at 350M** and **about 29k tok/s at
125M**.

```
python3: 1.0e9/2.90e4/3600 =  9.579 GPU-h per 1e9 tokens at 125M
         1.0e9/9.10e3/3600 = 30.525 GPU-h per 1e9 tokens at 350M
         F9 per-run: 125M/1.0e9 =  9.579 GPU-h (planned at 4.12  on the old figure, x2.32)
                     350M/2.0e9 = 61.050 GPU-h (planned at 23.15 on the old figure, x2.64)
```

**F9 moved from 718 to ~1,400 GPU-h here, and then to ~1,700 under the second
correction below.** The full line-by-line re-derivation is
`F9_PREREGISTRATION.md` §8.1. Three things happened at once and only one of
them is the throughput: the throughput correction (+2.3x to +2.6x on every
training line), the round-accounting fix that cut the collapse sub-study from a
mis-derived 33 runs to 9 (which reduces cost), and two lines that had no budget
at all before, trajectory generation derived rather than guessed, and F13 limb
(b), which `logos.tex` §15 scopes as an arm of F9.

**The card is the constraint, and the model size is the lever.** A 125M run is
9.579 GPU-h against 61.050 at 350M, a factor of 6.37, so the powered five-arm
n = 8 ordering study costs 383.1 GPU-h, less than seven 350M runs. This is why
`LOGOS_HARNESS.md` §5.1 now makes **125M the powered screen and 350M the
confirmatory replicate**, inverting the original phase order. Run at 350M
throughout, the same study would be 2,442 GPU-h and would not fit on this card
at a defensible electricity bill.

---

## The second correction, which moved every number again: the proposers could not run

The throughput correction above priced the right experiment wrong. This one priced the wrong experiment. **F9 as specified could not run at all**, and two documents disagreed about why without either noticing: `LOGOS_HARNESS.md` §7 Phase 4 generated proposals from "at least two distinct open models", while `F9_PREREGISTRATION.md` §8.1 generated them from "two 350M-class stand-in towers" and derived the whole 137.9 GPU-hour generation ledger at 350M throughput. Distinct open models **cannot read** an observation rendered as RQ-VAE codes, because those identifiers live inside one model's vocabulary and embedding table. And 350M stand-ins have to be **trained first**, out of a budget that never paid for it, and two models trained the same way on the same data are the homogeneous pair that round-2 finding C-02 says returns a martingale. `LADDER_ARCHITECTURE.md` §10 had already logged the conflict as unresolved.

The repair is `LOGOS_HARNESS.md` §2.2: **one observation, two renderings.** Frozen open-weight models of distinct lineage read a structured observation card (or the raw frame, if the proposer is a vision-language model); the learner reads RQ-VAE codes. The RQ-VAE is off the proposal path entirely. **What that does to this page:**

- **Generation is re-priced against inference on frozen open models and becomes roster-dependent.** It is linear in proposer size: 196.9 GPU-h at 0.5B-class, **393.9 at the 1B-class planning instantiation**, 3,151.0 at 8B-class (`F9_PREREGISTRATION.md` §8.1).
- **F9 moves from 1,402.6 to 1,683.6 GPU-h** at the planning instantiation, with a roster band of 1,467.6 to 4,707.2. **This page no longer asserts a single F9 total**, because the roster is not frozen and asserting one would be inventing it.
- **F13 limb (b) re-costs from 12.7 to 36.3 GPU-h** at the planning instantiation, and its position in the run order below was not executable at all: it scored a battery presented as RQ-VAE codes while sitting ahead of the RQ-VAE.
- **F13 limb (a) and F14 acquire a derived cost for the first time: 17.4 GPU-h** (`F9_PREREGISTRATION.md` §8.4). The instrument they need is the inventory the repair installs, so the derivation this page owed is paid.
- **`../logos.tex` §15 now disagrees with this page on two figures**: it prices limb (b) at 12.7 and calls limb (a) not derived. Both were right against the withdrawn stand-ins. The paper is the register of record, this page does not overwrite it, and the edits are owed there.

---

## The ladder that fits the owned card

Each rung names the hardware, the GPU-hours, the electricity, and the decision the run settles.

Where a figure was independently derived in this audit it is marked **[derived]**. Where it is the repository's own estimate carried forward without independent re-derivation it is marked **[repo estimate]**. Where it is unknown it says so.

### Tier 0: one consumer GPU (RTX 3090 or 4090, 24 GB). Owned.

| Falsifier | GPU-h | What the run decides |
|---|---|---|
| **F9** logos-harness, the observation bound | **1,684 [derived] at the 1B-class proposer instantiation; band 1,468 to 4,707 across the roster** | Whether grounded trajectories beat disagreement-gated self-play beat unfiltered self-play beat nothing, at matched token counts. This is the paper's terminal thesis and the only experiment in the ledger with a pre-committed kill condition. Design, power analysis and the line-by-line budget: `F9_PREREGISTRATION.md` §8.1. Breakdown below. **The band is the proposer roster and nothing else**: the seven training and probe lines are 1,251.6 GPU-h regardless. |
| **F13 limb (b)** calibrated-confidence weighting with no adjudication | **36.3 [derived]** at the planning instantiation, inside F9's total (was 12.7 against the withdrawn stand-ins) | Whether the gain sits in the debate protocol rather than in the observation channel (Zhu et al. arXiv:2601.19921 Theorem 1). `logos.tex` §15 scopes F13 as "an arm of F9" and prices it at 12.7 GPU-hours, which was correct against 350M stand-ins and is now stale. Re-costed: `F9_PREREGISTRATION.md` §8.2. **Limb (a) is still NOT an F9 arm**, but it is no longer unpriced, and it now shares the F9 proposer inventory rather than needing a separate one. |
| **F13 limb (a)**, planned as one rung with **F14** | **17.4 [derived]** | Whether corpus-level difference between towers is exploitable in a way persona-level difference is not, which is `logos.tex` §15's F13 limb (a) and the paper's least defended claim, plus F14's contrast against continued-pretraining branches of one base. **It runs on this card and, after the proposer repair, on the same models F9 already loads.** Distinct lineage is a property of how a model was trained, not of the hardware it runs on, and Qwen, Llama, DeepSeek, Mistral and Gemma already have it. **Distinct lineage is the treatment variable:** two models from the same lab, or two finetunes of one base checkpoint, do not count as distinct and may not fill a slot. **The figure is derived in `F9_PREREGISTRATION.md` §8.4**: 2,000 items x 12 pairs x 2 agents x 1,300 tokens = 6.24e7 tokens, at a four-model 7-to-8B-class roster, 14.51 GPU-h plus 20% slack. It scales linearly in roster size, item count and pair count. **Limitation, unchanged:** this tests the diversity claim at the level of independently trained open-weight models, not at tower scale, and the ensemble under test is not a Mixture-of-Towers. What is genuinely out of reach on this card is the 5 x 2.8T ensemble itself, which is **F2**, not F13. **What is still not derivable here is availability**: F14's condition needs a published continued-pretrain of a base that is also on the roster, and whether one exists under an acceptable licence is not a compute question. |
| **F3** Quantile Balancing and Causal Dual Bias in a real 1B / 64-expert loop | 72 to 120 [repo estimate] | Whether the two blog-sourced load balancers do what the vendor blog says. Note: an at-scale run already exists (32B-A5B, 1e22 FLOPs, 64 routed experts, reported by Open Athena), so F3 is a downscale replication at 83x less compute, not a first test. The paper does not know this. |
| **F10** router-swap cost | 96 [repo estimate] | Whether Branch-Adapt-Route's linear-update-cost economics survive router retraining after each expert swap. If they do not, the ensemble loses its main advantage over a monolith. |
| **F4** Delta-Attention-Residual checkpoint conversion | 48 [repo estimate] | Whether existing checkpoints convert without destabilising, which is what makes the mechanism deployable at all. |
| **F5** codebook collapse on real hidden states | 0 marginal | Falls out of F9 free, and the collapse monitor specified in `F9_PREREGISTRATION.md` §6 uses the same participation-ratio primitive, so this is now a genuine by-product rather than a promissory one. |

**One thing limb (a) does not need, recorded so it is not read in.** Distributed serving of a 2.8T ensemble across a peer swarm is not the instrument above and is not what blocks anything on this page; memory is not the obstacle there either (2.8T at 4.25 bits is 1.488 TB, about 68 cards at 22 GB usable, with an active path of 26.6 to 48.3 GB depending on which N_act bracket is taken), and the actual obstacle is that MoE all-to-all dispatch is data-dependent and per-layer so Petals' pipeline-parallel cost model does not transfer, which is precisely what `ARCHITECTURE_REVIEW.md` finding **F-13** (the review finding, not falsifier F13) records as never re-derived. That stays a finding and does not become a new falsifier.

### What the F9 rung is made of [derived]

| Line | GPU-h | moves with the roster? |
|---|---|---|
| Study 1, ordering, 125M / 1.0e9, five arms A0 to A4, n = 8, 40 runs | 383.1 | no |
| Study 2, collapse, 125M / 1.0e9, three arms, n = 3, R = 5 rounds inside the same token budget, 9 runs | 86.2 | no |
| Study 3, confirmatory, 350M / 2.0e9, three arms, n = 3, 9 runs | 549.5 | no |
| Outlier replacement reserve, 20% of training | 203.8 | no |
| **Trajectory generation, all arms, all studies** | **393.9** | **yes: 196.9 to 3,151.0** |
| tau_JS calibration pool plus S4 diversity plus S5 competence | 1.8 | yes: 0.9 to 14.5 |
| RQ-VAE training, frame tokenization, card-parity probes | 15.0 | no |
| Eval batteries, grounding and collapse probes | 12.0 | no |
| **F13 limb (b), confidence-weighted aggregation** | **36.3** | **yes: 18.1 to 290.1** |
| Day-one throughput and memory probe, learner training and proposer inference | 2.0 | no |
| **F9 total at the 1B-class planning instantiation** | **1,683.6** | band 1,467.6 to 4,707.2 |

```
python3: 383.1+86.2+549.5+203.8+393.9+1.81+15.0+12.0+36.3+2.0 = 1683.6
         fixed lines (training, RQ-VAE, eval, probe)          = 1251.6
         roster-dependent lines at 2 x 1.0B                    =  432.0
         the same three lines at 2 x 0.5B / 2 x 8.0B           =  216.0 / 3455.6
```

**Read the third row before anything else.** Study 3 is 33% of the F9 rung at
the planning instantiation and runs at n = 3, which supports no test statistic.
It is a scale sanity check, not a test. If the day-one probe confirms the
derived throughput, the frozen rule in `F9_PREREGISTRATION.md` §8.3 reduces
Study 3's tokens from 2.0e9 to 1.0e9 (549.5 to 274.7, saving 329.7 with its
reserve, and a further 56.3 of generation because halving the tokens halves the
traces) and takes the rung to `python3: 1683.6-329.7-56.3 = 1297.6`, about
**1,298 GPU-h**. Tokens are reduced before seeds are, always.

**And read the generation row second.** It is now the largest line after the
three studies, it is the only line that could plausibly double the rung, and it
is set by a choice this page has not made: which open models fill the proposer
slots. Small proposers are cheap and risk being too weak for their disagreement
to mean anything, which is what the new S5 competence gate exists to catch;
large ones are competent and can cost more in generation than the entire
training programme. **The roster freeze is scheduled before anything that
depends on it**, and the run order below reflects that.

### Tier 0 total

```
python3: F9 1683.6 + F3 (72 to 120) + F10 96 + F4 48 + F5 0 + F13(a)&F14 17.4
         = 1917.0 to 1965.0 GPU-h
         electricity: 1917.0*0.350 = 671.0 kWh -> EUR 201 ; 1965.0*0.350 = 687.8 kWh -> EUR 206
         rented:      1917.0*0.20  = $383      ; 1965.0*0.25 = $491
         with the Study-3 token reduction: 1531.0 to 1579.0 GPU-h,
         536 to 553 kWh, EUR 161 to EUR 166, $306 to $395
```

**That total now includes F13 limb (a) and F14 at 17.4 GPU-h**, which the previous version of this page left out because the cost was not derived. It is derived in `F9_PREREGISTRATION.md` §8.4 and it is in.

**Tier 0 total: 1,917 to 1,965 GPU-h at the 1B-class proposer instantiation.**
On the owned card at 350 W (NVIDIA GA102 whitepaper, Appendix A Table 9) and
EUR 0.30/kWh that is 671 to 688 kWh, about **EUR 201 to EUR 206 of
electricity**. Rented at RTX-3090 community-cloud rates of $0.20 to
$0.25/GPU-h, **$383 to $491**. The previous figures on this page, first 934 to
982 GPU-h and then 1,619 to 1,667, were priced off the withdrawn throughput and
the withdrawn stand-in proposers respectively, and both are superseded.

**Two bands sit on that total and they are independent.** The first is the MFU
assumption: the 9.1k and 29k tok/s figures assume 25% to 35% against the
71-TFLOPS dense ceiling, so at the low end the F9 rung is roughly 2,100 GPU-h
and at the high end roughly 1,450. The second is the proposer roster: at
0.5B-class proposers the F9 rung is 1,468 and at 8B-class it is 4,707, which is
a wider band than the MFU one and it is set by a decision rather than by a
measurement. **The day-one probe resolves the first and the roster freeze
resolves the second, and both happen before any arm.**

### Order on this card

Ordered by what a result unblocks, not by cost.

**The previous order on this page was not executable, and the defect is worth stating before the repaired table.** F13 limb (b) sat at position 2 and scored a battery presented as RQ-VAE codes, while the RQ-VAE was built at position 4. S4 and `tau_JS` sat at position 3 with the same dependency. Under the withdrawn stand-in proposers all three genuinely needed the codes, so the order was not merely mis-sorted, it was unrunnable in either direction: move them after the RQ-VAE and the cheapest kill shot stops being cheap and early, leave them before it and they have nothing to read. **The proposer repair dissolves it rather than reshuffling it.** Proposers read the §3.4 observation card, which is built from the Phase-0 dump, so every proposer-side gate depends on **Phase 0 and not on Phase 1**. The remaining ordering question is only where Phase 0 sits, and the answer is early and cheap, because it is CPU and I/O work.

| # | Work | GPU-h | Why here |
|---|---|---|---|
| 1 | **Freeze the proposer roster**: model ids, revisions, quantization, lineage attestation, per-file digests, into `proposers/roster.yaml` | **0** | It costs no GPU time and it sets three budget lines that span a factor of 16. Nothing below that touches a proposer is meaningful without it, and the probe on row 2 cannot measure proposer inference until it exists |
| 2 | Day-one probe: forward-backward at 125M and 350M, **and quantized proposer prefill and batched decode on the frozen roster** | 2 | Every other number on this page is arithmetic against a published ceiling. This is the only line that turns it into a measurement, and the frozen response to a shortfall is to reduce tokens, never seeds |
| 3 | **F13 limb (b), first pass, on a text battery**: the E-DIV **A5** arm of `LADDER_ARCHITECTURE.md` §7.3, which already shares its battery with K5 so the two are comparable | costed in that document, **not** a new line here; if E-DIV has not run, F9's own proposers can be screened on a text-only battery for **+13.4** | The cheapest kill shot against the paper's own thesis, and on a text battery it needs no emulator, no observation card and no RQ-VAE, so it can genuinely run before anything is built. **This is the row that used to be impossible.** It is a screen and not the verdict: K5 is adjudicated on the held-out battery at row 6 |
| 4 | **Phase 0**: headless frame and RAM dump, the observation-card renderer, and parity checks 1 and 2 of `LOGOS_HARNESS.md` §3.4 | **0 GPU** (CPU and I/O bound) | Everything on the proposer path reads the card, and the card is built here. The dump has to target 1.6M distinct battle observations for a gated arm, not the 100k the Phase-0 gate asks for |
| 5 | S4 proposer diversity, **S5 proposer competence**, and `tau_JS` calibration at q = 0.25, all over the outcome space `O` | 1.8 | Three VOID conditions for the price of a rounding error. A null on the gate arms is uninterpretable if the proposers were never diverse (S4) or were never competent (S5), and S4 alone does not catch the second |
| 6 | Proposer confidence calibration and **F13 limb (b) on the held-out battery in the proposer rendering: the K5 adjudication** | 36.3 | Needs Phase 0 and the calibrated proposers, and needs the RQ-VAE not at all. Run before any training arm, because if K5 fires the rest of F9 is answering the wrong question |
| 7 | **F13 limb (a) with F14**, debate between open-weight models of distinct pretraining lineage against personas and against continued-pretraining branches | **17.4** | Tests the paper's least defended claim, needs no gradient step, and reuses the row-1 inventory plus a capable-end roster. Derived at last (`F9_PREREGISTRATION.md` §8.4), so it is scheduled rather than deferred. It is still **not** an F9 arm |
| 8 | Phases 1 to 3: RQ-VAE at the frozen 90-position geometry, parity check 3, tokenizer, leak filter, text corpus | 15 | A failed reconstruction gate, a failed code-recoverability probe or a non-zero leak count voids everything downstream. No LM training until all pass. **Only the learner path waits here** |
| 9 | F9 Study 1, the powered screen, 125M, five arms, n = 8 | 383.1 + 112.5 generation | The only line in this ladder that yields a test statistic |
| 10 | F9 Study 2, collapse sub-study, R = 5 | 86.2 + 168.8 generation | Distinguishes a real negative from an insensitive monitor. Its generation is the largest of the three because every seed must generate its own multi-round corpus |
| 11 | F9 Study 3, confirmatory at 350M, n = 3 | 549.5 + 112.5, or 274.7 + 56.3 if row 2 fires the token-reduction rule | Largest line, no test statistic. Run last, and reduce it first if the probe disagrees |
| 12 | F3 and F10 on one shared 1B MoE trainer | 168 to 216 | Independent of F9 and share a harness |
| 13 | F4 checkpoint conversion | 48 | Independent |

**Rows 1 to 7 are the whole proposer-side programme and they cost 57.5 GPU-h plus whatever the text-battery screen is taken from.** Both of the programme's cheapest kill shots, K5 and the diversity conjecture, are settled before a single training run starts, which is the ordering the previous version wanted and could not express.

F5 does not appear because it has no line of its own: the collapse monitor of
`F9_PREREGISTRATION.md` §6 computes the same participation-ratio primitive on
real hidden states, so F5 falls out of rows 5 and 6 at 0 marginal GPU-h.

### Tier 0.5: two accelerators of DIFFERENT models

| Falsifier | GPU-h | What it decides |
|---|---|---|
| **F8** canary integrity under a realistic adversary | **unknown, and not derived in GPU-hours.** An earlier revision of `GAPS.md` costed this in wall-clock; that estimate is withdrawn, `GAPS.md` §5 now records that it was never re-derived in GPU-hours, and this audit did not re-derive it either. The binding cost is not hours. | Whether the published AUROC of 1.0 (arXiv:2607.19490, 408 configurations) survives when the benign null is measured across two accelerators with independently compiled kernels and mixed MXFP4 / NVFP4 paths. The published result is against a static adversary on a homogeneous null; `logos.tex` §7 creates heterogeneous numerics and then leans on a detector that assumes them away. **The repository states it expects this to fire against itself.** |

The binding constraint here is not GPU-hours and not money. It is one accelerator of a **different** model than the 3090, borrowed or rented for the duration of a null measurement. A matched pair reproduces the published setting and settles nothing, so a second 3090 does not unblock this rung.


## The pre-committed kill conditions

Every rung has a pre-committed kill condition. They are written into `F9_PREREGISTRATION.md` §10 and into `logos.tex` §15, before the runs, not after.

**F9, K1: the bound is refuted.** The contrast A3 versus A1 fails superiority AND a two-one-sided-tests procedure declares equivalence at a margin of 1.243 sigma, about 6 accuracy points. Then grounding buys under 6 points over pure self-play on the easiest imaginable grounding substrate, where the semantics under test are printed on screen in four colours at 160x144. **Consequence, pre-committed:** `logos.tex` §12 is wrong as stated, its ordering sentence is struck, and the paper says that the strategy past the token wall is repetition plus synthesis, that Proposition 2's headroom is all there is, and that the observation-bound framing was wrong.

**F9, K2: the admission rule is refuted.** The collapse monitor fires on the grounded arm under the frozen three-statistic rule of `F9_PREREGISTRATION.md` §6. The third of the paper's three original claims falls.

**F9, K3: the Tier-C claim is refuted while the bound survives.** Grounding works and the disagreement gate contributes nothing. The claim `logos.tex` §12 calls "the specific contribution" is dead, and the Mixture-of-Towers architecture loses its learning-from-disagreement justification and must be defended on update economics alone.

**K3 is the outcome the design is worst powered to detect, it is the one the paper cares most about, and the corrected budget does NOT fix it.** This is the honest state of the rung after re-costing and it is stated here rather than left in the pre-registration. K3 is a conjunction of two equivalence declarations, and equivalence needs more seeds than superiority, not fewer. At n = 8 the tightest declarable margin is 1.243 sigma, about 6.2 accuracy points; superiority needs 1.584 sigma, about 7.9 points; a true gate effect between those two lands INCONCLUSIVE by construction, and that window is where H3 most plausibly lives.

```
python3: n = 12.365/(eps/sigma)^2 ; Study 1 cost = 5 arms * n * 9.579 GPU-h
         eps = 1.243 sigma (6.2 pts) -> n =  8 ->  383.1 GPU-h   [budgeted]
         eps = 1.000 sigma (5.0 pts) -> n = 13 ->  622.6 GPU-h
         eps = 0.600 sigma (3.0 pts) -> n = 35 -> 1676.2 GPU-h
```

Buying a 3-point verdict on the gate costs 1,676 GPU-h in Study 1 alone, which is more than the entire F9 rung as budgeted. **It is not bought, the pre-registration says so, and the margin is not widened to make K3 easier to declare** because widening it would make a false K3 easier to reach as well.

**F9, K5: the gain is in the protocol, not in the observation channel.** F13 limb (b) fires: calibrated-confidence weighting alone lifts ensemble accuracy on the held-out battery with no environment adjudication of any kind. Then the observation bound is not what limits the loop and `logos.tex` §12's central claim is in the wrong place. This is the cheapest kill shot available against the paper's own thesis, it costs **36.3 GPU-h** at the planning instantiation (the 12.7 in `logos.tex` §15 was priced against the withdrawn 350M stand-ins), and it runs on this card, on frozen open models, before any training arm. Recorded steelman: the calibrator itself is bought with external supervision, so limb (b) firing refutes the *channel* claim and not the *exogenous signal* claim.

**F2 ladder: the composition gap widens with scale.** If Delta(N) decreases monotonically across 1B, 7B and 24B, the 400x extrapolation is dead and the 5 x 2.8T architecture should not be built. The existing measurement is already Delta(7e9) = -1.4.

**F8: the canary detector fails on heterogeneous numerics.** `GAPS.md` states in advance: "We expect this to fire against us."

**And the non-negotiable one.** `F9_PREREGISTRATION.md` §9.4 pre-commits that a non-significant result below n = 8 is reported UNDERPOWERED, not negative. A programme that will not distinguish "we refuted it" from "we could not tell" has no kill condition at all.

If the kill conditions fire, the papers say so and the programme stops. The repository has already published four honest negatives (the early-warning battery at AUC 0.4996 with p = 0.915; the EnKF forward test tied with persistence; the neff_v3 magnitude endpoint SEALED NOT with two of four conditions failing; and the test-(i) conservation pilot contradicting at the wrong scale). That is the track record on which the pre-commitment above should be judged.

---
