# Tier 0: what runs on the owned 3090

**This is a run plan, not a funding document.** Owner decision, 2026-07-25:
funding is a consequence of experiments succeeding on this card, not a
precondition for attempting them. The order is F9 runs -> it produces a real
result -> the result is the argument. Pricing a rung inside a ledger is
engineering; a pitch written before there is a run is not.

Derived from the round-2 audit (`REVIEW_ROUND2.md`) and the sealed design in
`F9_PREREGISTRATION.md`. Figures marked **[derived]** were independently
computed and are shown with their arithmetic; **[repo estimate]** carries
`GAPS.md` forward without re-derivation.

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

**F9 moves from 718 to ~1,400 GPU-h.** The full line-by-line re-derivation is
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

## The ladder that fits the owned card

Each rung names the hardware, the GPU-hours, the electricity, and the decision the run settles.

Where a figure was independently derived in this audit it is marked **[derived]**. Where it is the repository's own estimate carried forward without independent re-derivation it is marked **[repo estimate]**. Where it is unknown it says so.

### Tier 0: one consumer GPU (RTX 3090 or 4090, 24 GB). Owned.

| Falsifier | GPU-h | What the run decides |
|---|---|---|
| **F9** logos-harness, the observation bound | **1,403 [derived]** | Whether grounded trajectories beat disagreement-gated self-play beat unfiltered self-play beat nothing, at matched token counts. This is the paper's terminal thesis and the only experiment in the ledger with a pre-committed kill condition. Design, power analysis and the line-by-line budget: `F9_PREREGISTRATION.md` §8.1. Breakdown below. |
| **F13 limb (b)** calibrated-confidence weighting with no adjudication | **12.7 [derived]**, inside F9's total | Whether the gain sits in the debate protocol rather than in the observation channel (Zhu et al. arXiv:2601.19921 Theorem 1). `logos.tex` §15 scopes F13 as "an arm of F9"; the previous budget on this page could not pay for it, so the paper claimed an arm that did not exist. Now costed: `F9_PREREGISTRATION.md` §8.2. **Limb (a) is NOT an F9 arm** and is not priced here: it needs models whose pretraining corpora, objectives and alignment histories genuinely differ, which no 350M stand-in trained for this harness supplies. It is a separate rung on this same card, below. |
| **F13 limb (a)** debate between towers of genuinely different pretraining lineage | **not yet derived** | Whether corpus-level difference between towers is exploitable in a way persona-level difference is not, which is `logos.tex` §15's F13 limb (a) and the paper's least defended claim. **It runs on this card**, and an earlier version of this page wrongly implied it could not: distinct lineage is a property of how a model was trained, not of the hardware it runs on, and Qwen, Llama, DeepSeek, Mistral and Gemma already have it, having been pretrained by different organisations on different corpora under different objectives with different alignment histories. That is arguably a better instrument than five towers from one lab, which would share data-collection pipelines and filtering decisions and be less independent than they look. The run is several existing open-weight models of **different pretraining lineage**, quantized and stepped sequentially in 24 GB, no gradient step anywhere. **Distinct lineage is the treatment variable:** two models from the same lab, or two finetunes of one base checkpoint, do not count as distinct and may not fill a slot. **Limitation, stated:** this tests the diversity claim at the level of independently trained open-weight models, not at tower scale inside one architecture, and the ensemble under test is not a Mixture-of-Towers. **The GPU-hour figure is not derived and none is asserted here.** Sequential quantized inference is cheap against every training line on this page, but cheap is not derived, and the derivation is owed before this rung is scheduled. What is genuinely out of reach on this card is the 5 x 2.8T ensemble itself, which is **F2**, not F13. |
| **F3** Quantile Balancing and Causal Dual Bias in a real 1B / 64-expert loop | 72 to 120 [repo estimate] | Whether the two blog-sourced load balancers do what the vendor blog says. Note: an at-scale run already exists (32B-A5B, 1e22 FLOPs, 64 routed experts, reported by Open Athena), so F3 is a downscale replication at 83x less compute, not a first test. The paper does not know this. |
| **F10** router-swap cost | 96 [repo estimate] | Whether Branch-Adapt-Route's linear-update-cost economics survive router retraining after each expert swap. If they do not, the ensemble loses its main advantage over a monolith. |
| **F4** Delta-Attention-Residual checkpoint conversion | 48 [repo estimate] | Whether existing checkpoints convert without destabilising, which is what makes the mechanism deployable at all. |
| **F5** codebook collapse on real hidden states | 0 marginal | Falls out of F9 free, and the collapse monitor specified in `F9_PREREGISTRATION.md` §6 uses the same participation-ratio primitive, so this is now a genuine by-product rather than a promissory one. |

**One thing limb (a) does not need, recorded so it is not read in.** Distributed serving of a 2.8T ensemble across a peer swarm is not the instrument above and is not what blocks anything on this page; memory is not the obstacle there either (2.8T at 4.25 bits is 1.488 TB, about 68 cards at 22 GB usable, with an active path of 26.6 to 48.3 GB depending on which N_act bracket is taken), and the actual obstacle is that MoE all-to-all dispatch is data-dependent and per-layer so Petals' pipeline-parallel cost model does not transfer, which is precisely what `ARCHITECTURE_REVIEW.md` finding **F-13** (the review finding, not falsifier F13) records as never re-derived. That stays a finding and does not become a new falsifier.

### What the F9 rung is made of [derived]

| Line | GPU-h |
|---|---|
| Study 1, ordering, 125M / 1.0e9, five arms A0 to A4, n = 8, 40 runs | 383.1 |
| Study 2, collapse, 125M / 1.0e9, three arms, n = 3, R = 5 rounds inside the same token budget, 9 runs | 86.2 |
| Study 3, confirmatory, 350M / 2.0e9, three arms, n = 3, 9 runs | 549.5 |
| Outlier replacement reserve, 20% of training | 203.8 |
| Trajectory generation, all arms, all studies | 137.9 |
| tau_JS calibration pool plus S4 proposer diversity | 0.5 |
| RQ-VAE training plus frame tokenization | 15.0 |
| Eval batteries, grounding and collapse probes | 12.0 |
| F13 limb (b), confidence-weighted aggregation | 12.7 |
| Day-one throughput and memory probe | 2.0 |
| **F9 total** | **1,402.6** |

```
python3: 383.1+86.2+549.5+203.8+137.9+0.5+15.0+12.0+12.7+2.0 = 1402.6
```

**Read the third row before anything else.** Study 3 is 39% of the F9 rung and
runs at n = 3, which supports no test statistic. It is a scale sanity check,
not a test. If the day-one probe confirms the derived throughput, the frozen
rule in `F9_PREREGISTRATION.md` §8.3 reduces Study 3's tokens from 2.0e9 to
1.0e9 (549.5 to 274.7, saving 329.7 with its reserve) and takes the rung to
**1,073 GPU-h**. Tokens are reduced before seeds are, always.

### Tier 0 total

```
python3: F9 1402.6 + F3 (72 to 120) + F10 96 + F4 48 + F5 0
         = 1618.6 to 1666.6 GPU-h
         electricity: 1618.6*0.350 = 566.5 kWh -> EUR 170 ; 1666.6*0.350 = 583.3 kWh -> EUR 175
         rented:      1618.6*0.20  = $324      ; 1666.6*0.25 = $417
         with the Study-3 token reduction: 1288.9 to 1336.9 GPU-h,
         451 to 468 kWh, EUR 135 to EUR 140, $258 to $334
```

**That total excludes F13 limb (a)**, which runs on this card but whose GPU-hour cost is not derived. It is left out rather than guessed at, and the total will move when the derivation lands.

**Tier 0 total: 1,619 to 1,667 GPU-h.** On the owned card at 350 W (NVIDIA
GA102 whitepaper, Appendix A Table 9) and EUR 0.30/kWh that is 567 to 583 kWh,
about **EUR 170 to EUR 175 of electricity**. Rented at RTX-3090
community-cloud rates of $0.20 to $0.25/GPU-h, **$324 to $417**. The previous
figure on this page, 934 to 982 GPU-h and EUR 98 to EUR 103, was priced off the
withdrawn throughput and is superseded.

**The band on that total is wider than it looks.** The 9.1k and 29k tok/s
figures assume 25% to 35% MFU against the 71-TFLOPS dense ceiling. At the low
end of that band the F9 rung is roughly 1,800 GPU-h and at the high end roughly
1,200. The day-one forward-backward probe resolves it before any schedule is
committed, and it is the first thing that runs.

### Order on this card

Ordered by what a result unblocks, not by cost.

| # | Work | GPU-h | Why here |
|---|---|---|---|
| 1 | Day-one forward-backward throughput and memory probe, 125M and 350M | 2 | Every other number on this page is arithmetic against a published ceiling. This is the only line that turns it into a measurement, and the frozen response to a shortfall is to reduce tokens, never seeds |
| 2 | F13 limb (b), calibrated-confidence weighting, ungated scoring | 12.7 | The cheapest kill shot against the paper's own thesis. If it fires, the observation bound is not what limits the loop and the rest of F9 is answering the wrong question |
| 3 | S4 proposer diversity and tau_JS calibration at q = 0.25 | 0.5 | Both are VOID conditions. A null on the gate arms is uninterpretable if the stand-in proposers were never diverse, and neither costs anything to check first |
| 4 | Phases 0 to 3: frame dump, RQ-VAE at the frozen 90-position geometry, tokenizer, leak filter, text corpus | 15 | A failed RQ-VAE reconstruction gate or a non-zero leak count voids everything downstream. No LM training until both pass |
| 5 | F9 Study 1, the powered screen, 125M, five arms, n = 8 | 383.1 + 137.9 generation | The only line in this ladder that yields a test statistic |
| 6 | F9 Study 2, collapse sub-study, R = 5 | 86.2 | Distinguishes a real negative from an insensitive monitor |
| 7 | F9 Study 3, confirmatory at 350M, n = 3 | 549.5, or 274.7 if row 1 fires the token-reduction rule | Largest line, no test statistic. Run last, and reduce it first if the probe disagrees |
| 8 | F3 and F10 on one shared 1B MoE trainer | 168 to 216 | Independent of F9 and share a harness |
| 9 | F4 checkpoint conversion | 48 | Independent |
| 10 | F13 limb (a), debate between open-weight models of distinct pretraining lineage | not yet derived | Tests the paper's least defended claim and needs no gradient step, but it is unscheduled until its cost is derived rather than guessed. It is not an F9 arm and nothing in rows 1 to 9 covers it |

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

**F9, K5: the gain is in the protocol, not in the observation channel.** F13 limb (b) fires: calibrated-confidence weighting alone lifts ensemble accuracy on the held-out battery with no environment adjudication of any kind. Then the observation bound is not what limits the loop and `logos.tex` §12's central claim is in the wrong place. This is the cheapest kill shot available against the paper's own thesis, it costs 12.7 GPU-h, and it runs on this card. Recorded steelman: the calibrator itself is bought with external supervision, so limb (b) firing refutes the *channel* claim and not the *exogenous signal* claim.

**F2 ladder: the composition gap widens with scale.** If Delta(N) decreases monotonically across 1B, 7B and 24B, the 400x extrapolation is dead and the 5 x 2.8T architecture should not be built. The existing measurement is already Delta(7e9) = -1.4.

**F8: the canary detector fails on heterogeneous numerics.** `GAPS.md` states in advance: "We expect this to fire against us."

**And the non-negotiable one.** `F9_PREREGISTRATION.md` §9.4 pre-commits that a non-significant result below n = 8 is reported UNDERPOWERED, not negative. A programme that will not distinguish "we refuted it" from "we could not tell" has no kill condition at all.

If the kill conditions fire, the papers say so and the programme stops. The repository has already published four honest negatives (the early-warning battery at AUC 0.4996 with p = 0.915; the EnKF forward test tied with persistence; the neff_v3 magnitude endpoint SEALED NOT with two of four conditions failing; and the test-(i) conservation pilot contradicting at the wrong scale). That is the track record on which the pre-commitment above should be judged.

---
