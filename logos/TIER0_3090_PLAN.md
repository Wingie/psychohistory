# Tier 0: what runs on the owned 3090

**This is a run plan, not a funding document.** Owner decision, 2026-07-25:
funding is a consequence of experiments succeeding on this card, not a
precondition for attempting them. The order is F9 runs -> it produces a real
result -> the result is the argument. Pricing a rung inside a ledger is
engineering; a pitch written before there is a run is not.

Derived from the round-2 audit (`REVIEW_ROUND2.md`) and the sealed design in
`F9_PREREGISTRATION.md`. Figures marked **[derived]** were independently
computed in that audit; **[repo estimate]** carries `GAPS.md` forward without
re-derivation.

---

## The ladder that fits the owned card

Each rung names the hardware, the GPU-hours, the dollars, and the decision the money buys.

Where a figure was independently derived in this audit it is marked **[derived]**. Where it is the repository's own estimate carried forward without independent re-derivation it is marked **[repo estimate]**. Where it is unknown it says so.

### Tier 0: one consumer GPU (RTX 3090 or 4090, 24 GB). Owned.

| Falsifier | GPU-h | What the run decides |
|---|---|---|
| **F9** logos-harness, the observation bound | **718 [derived]** | Whether grounded trajectories beat disagreement-gated self-play beat unfiltered self-play beat nothing, at matched token counts. This is the paper's terminal thesis and the only experiment in the ledger with a pre-committed kill condition. Design and power analysis: `F9_PREREGISTRATION.md`. |
| **F3** Quantile Balancing and Causal Dual Bias in a real 1B / 64-expert loop | 72 to 120 [repo estimate] | Whether the two blog-sourced load balancers do what the vendor blog says. Note: an at-scale run already exists (32B-A5B, 1e22 FLOPs, 64 routed experts, reported by Open Athena), so F3 is a downscale replication at 83x less compute, not a first test. The paper does not know this. |
| **F10** router-swap cost | 96 [repo estimate] | Whether Branch-Adapt-Route's linear-update-cost economics survive router retraining after each expert swap. If they do not, the ensemble loses its main advantage over a monolith. |
| **F4** Delta-Attention-Residual checkpoint conversion | 48 [repo estimate] | Whether existing checkpoints convert without destabilising, which is what makes the mechanism deployable at all. |
| **F5** codebook collapse on real hidden states | 0 marginal | Falls out of F9 free, and the collapse monitor specified in `F9_PREREGISTRATION.md` §6 uses the same participation-ratio primitive, so this is now a genuine by-product rather than a promissory one. |

**Tier 0 total: 934 to 982 GPU-h.** On the owned card at 350 W (NVIDIA GA102 whitepaper, Appendix A Table 9) and EUR 0.30/kWh that is 327 to 344 kWh, about **EUR 98 to EUR 103 of electricity**. Rented at RTX-3090 community-cloud rates of $0.20 to $0.25/GPU-h, **$187 to $246**.

### Tier 0.5: two accelerators of DIFFERENT models

| Falsifier | GPU-h | What it decides |
|---|---|---|
| **F8** canary integrity under a realistic adversary | **unknown.** `GAPS.md` says "an afternoon of compute" and this audit did not re-derive it. The binding cost is not hours. | Whether the published AUROC of 1.0 (arXiv:2607.19490, 408 configurations) survives when the benign null is measured across two accelerators with independently compiled kernels and mixed MXFP4 / NVFP4 paths. The published result is against a static adversary on a homogeneous null; `logos.tex` §7 creates heterogeneous numerics and then leans on a detector that assumes them away. **The repository states it expects this to fire against itself.** |

The ask here is not money, it is access to one accelerator of a different model for a short window. A matched pair reproduces the published setting and settles nothing.


## The pre-committed kill conditions

Every rung has a pre-committed kill condition. They are written into `F9_PREREGISTRATION.md` §10 and into `logos.tex` §15, before the runs, not after.

**F9, K1: the bound is refuted.** The contrast A3 versus A1 fails superiority AND a two-one-sided-tests procedure declares equivalence at a margin of 1.243 sigma, about 6 accuracy points. Then grounding buys under 6 points over pure self-play on the easiest imaginable grounding substrate, where the semantics under test are printed on screen in four colours at 160x144. **Consequence, pre-committed:** `logos.tex` §12 is wrong as stated, the ordering sentence at `logos.tex:602` is struck, and the paper says that the strategy past the token wall is repetition plus synthesis, that Proposition 2's headroom is all there is, and that the observation-bound framing was wrong.

**F9, K2: the admission rule is refuted.** The collapse monitor fires on the grounded arm under the frozen three-statistic rule of `F9_PREREGISTRATION.md` §6. The third of the paper's three original claims falls.

**F9, K3: the Tier-C claim is refuted while the bound survives.** Grounding works and the disagreement gate contributes nothing. The claim `logos.tex:561` calls "the specific contribution" is dead, and the Mixture-of-Towers architecture loses its learning-from-disagreement justification and must be defended on update economics alone. **This is the outcome the design is worst powered to detect and the paper cares most about, and that asymmetry is disclosed in the pre-registration rather than found afterwards.**

**F2 ladder: the composition gap widens with scale.** If Delta(N) decreases monotonically across 1B, 7B and 24B, the 400x extrapolation is dead and the 5 x 2.8T architecture should not be built. The existing measurement is already Delta(7e9) = -1.4.

**F8: the canary detector fails on heterogeneous numerics.** `GAPS.md` states in advance: "We expect this to fire against us."

**And the non-negotiable one.** `F9_PREREGISTRATION.md` §9.4 pre-commits that a non-significant result below n = 8 is reported UNDERPOWERED, not negative. A programme that will not distinguish "we refuted it" from "we could not tell" has no kill condition at all.

If the kill conditions fire, the papers say so and the programme stops. The repository has already published four honest negatives (the early-warning battery at AUC 0.4996 with p = 0.915; the EnKF forward test tied with persistence; the neff_v3 magnitude endpoint SEALED NOT with two of four conditions failing; and the test-(i) conservation pilot contradicting at the wrong scale). That is the track record on which the pre-commitment above should be judged.

---
