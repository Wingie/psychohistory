# Multimodality in LOGOS: encoders, codebooks, and why towers help

Multimodality is core to the architecture's motivation, and the first design
drafted for it here was wrong in a way worth recording, because the error is a
natural one.

**The dead variant: predict raw bytes.** Byte-level tokenisation is used
throughout this harness for a good reason — a learned vocabulary fitted on one
domain mix would smuggle back the lexical prior that killed the Jaccard variant
of F11 — and bytes are modality-agnostic, so a PDF, a waveform and a source file
are all one stream with no per-modality machinery. That reasoning is sound for
*text* domains and collapses for real modalities:

- JPEG, PNG and MP3 bytes are **entropy-coded**, hence close to incompressible.
  A model learns essentially nothing from them, its gradients approach noise, and
  a separation measure would report them as spectacularly distinct from
  everything — including from a second sample of themselves. That is an absence
  of signal, not a modality difference.
- WAV is raw PCM and does carry learnable structure, but next-*byte* prediction
  over PCM is sample-level waveform modelling. It is not how any working system
  represents audio, and nothing measured on it transfers.

No production multimodal model predicts raw bytes. Modalities are **embedded into
the model's latent space**, and the architecture question is *how*.

---

## The three families

**1. Continuous projection.** A modality encoder (CLIP ViT, Whisper) produces
embeddings; a connector — linear, MLP, Q-Former, or gated cross-attention — maps
them into the LLM's latent space, where they enter as soft tokens. LLaVA,
Flamingo, BLIP-2, Qwen-VL. The model *consumes* modality tokens and emits text.
Cheapest, preserves a pretrained LLM, but cannot generate other modalities
without a separate decoder.

**2. Discrete tokenisation, early fusion.** A VQ-VAE/VQGAN quantises the input
into codes from a learned codebook; the codes join the text vocabulary and one
transformer runs a single next-token objective over the merged stream. Chameleon,
Emu3, Unified-IO. This is the family that can *generate* every modality.

**3. Patch-direct.** Raw patches through a linear projection, no encoder at all
(Fuyu). Simplest; one fewer component to train and maintain.

### Verified specifics

**Chameleon** (arXiv 2405.09818): image codebook of **8,192**, **1,024 tokens per
512×512 image**, total vocabulary **65,536**, one shared softmax and one
transformer with *no separate image/text encoders*. Its stated tokenizer weakness
is reconstructing images containing a lot of text, which caps OCR-style tasks.

**RQ-VAE** (arXiv 2203.01941): residual quantisation to depth **D = 4** with a
**single codebook of K = 16,384 shared across all depths**. Each step codes the
residual of the last, so the partial sum refines coarse-to-fine. Depth-D RQ has
the partition capacity of a flat VQ with `K^D` codes — about 7.2 × 10¹⁶ here —
which is why a small shared codebook suffices. A 256×256 image becomes an
**8×8×4** code map: 64 spatial positions rather than VQ-GAN's 256, a 4× spatial
compression at equal total codes. The **RQ-Transformer** then factorises
prediction into a *spatial* transformer over positions and a *depth* transformer
over the D codes at each position.

---

## The finding that matters for this architecture

Chameleon's central difficulty is not compute. It is the **logit drift problem**:
modalities with *significantly varying entropy* drive norm growth until it
exceeds bf16 range and training diverges, and it is worst when image generation
is in the mix. Their fixes were QK-norm (essential at both 7B and 34B), a z-loss
of 1e-5, dropout 0.1 at 7B, and post-attention norm reordering at 34B — which is
incompatible with dropout, so the two scales needed different recipes.

**A first draft of this section claimed the fix is towers. It is not, and the
claim does not survive towers being modality-blind.** If towers do not correspond
to modalities, they do not give any modality its own parameters, so they cannot
be what addresses an entropy mismatch between modalities.

What addresses it is the **encoder**. Chameleon's verified property is that it has
*no separate image/text encoders* — discrete codes drawn from wildly different
entropy distributions pass straight through one shared softmax, which is the
direct cause of the drift. A design that encodes each modality into a shared,
normalised latent space before anything is predicted does not create the
condition in the first place. The lesson is a constraint on the **encoder
contract**, not an argument for the tower layout: whatever the per-modality
encoders are, their outputs must be comparable in scale and entropy, because
that comparability is what buys stability.

Towers may still help second-order — separate parameters mean separate norm
dynamics — but that is a conjecture, not the mechanism, and the communication
argument remains the systems case for Mixture-of-Towers.

It is also cheap insurance already taken: this harness's attention carries
`q_norm` and `k_norm` (`logos/probe/model.py`), so the one fix Chameleon calls
essential at every scale is present.

A second structural echo: RQ-VAE's **shared codebook reused across depths, with
residual refinement on top** is the same move as an always-on shared tower plus
specialised towers. Close enough to treat as a design constraint rather than a
coincidence — the shared component carries what is common, the specialised ones
carry the residual.

---

## The corrected shape

The trunk is not shared at the *input*. It is shared after embedding:

```
per-modality tokenizer / encoder      (RQ-VAE or projector, per file type)
              ↓
      shared latent space
              ↓
        shared trunk                  builds the representation the router reads
              ↓
           router
              ↓
    towers (specialised)
              ↓
        shared head
              ↓
per-modality de-tokenizer             (only if generating that modality)
```

### Towers are modality-blind, and that is the point

An earlier draft of this document assumed towers would correspond to modalities,
and then worried that this made the router trivial — read the file type, skip the
learned function. **That assumption was wrong, and dropping it removes the
problem rather than resolving it.**

Modality is an **input-encoding concern**. Everything above the encoder lives in
one latent space, and a tower never learns "this is a PDF"; it learns whatever
structure the latents carry. Concretely:

- **Towers are file-type independent.** They operate on embeddings, so the same
  tower serves a passage that arrived as PDF, as a screenshot, or as native text,
  provided those encode to similar latents.
- **The KV cache is over latent embeddings**, so it is shared across modalities
  by construction. This is a sharper version of the point the KV section of the
  microarchitecture spec was reaching for and got wrong: cache sharing does not
  distinguish this design from MoE, but it does distinguish it from separately
  served per-modality models, which cannot share a latent space at all.
- **The router stays non-trivial**, because it routes on semantic content rather
  than on a field that is known for free at the input. The learned-router claim
  survives intact.

Modality and domain are therefore orthogonal axes, not competing ones. Encoders
handle the first; towers and the router handle the second.

### What this changes about the experiments

Gradient conflict measured on **raw bytes** answers a question about byte
statistics. The version whose answer transfers measures it on **embedded
representations after the per-modality encoder**, in the shared latent space
where towers actually operate. The negative-control discipline survives — an
entropy-coded modality should show a collapsed within-domain baseline, and if it
does not, the measurement is not working — but the substrate does not.

Because towers are modality-blind, the quantity of interest is **conflict between
semantic domains in latent space**, whatever modality they arrived in. The text
measurements stand as the current reference — markdown against Python at 0.4808
(separable), JavaScript against TypeScript at 0.8024 (merge) — and the question
is whether domains that arrive through *different* encoders land far enough apart
in the shared space to be worth separate towers. If a PDF-derived text and a
native text of the same domain collapse to within the within-domain null, the
encoder is doing its job and the tower layout should ignore the distinction,
which is the outcome the design predicts.

---

## Streaming and agentic I/O

The same framing covers streaming input and output: a log tail, a screen-capture
frame sequence, and an emitted button press or mouse movement are all encoder and
decoder concerns, and none of them reach the towers as anything but latents. This
is the agentic loop — observation in, action out — and it is where trajectories
come from, which connects it directly to the observation bound of §12 and to the
F9 results.

It is out of scope at this budget and recorded so it is not mistaken for a gap.
Whether the tighter observation-action coupling such a loop needs emerges at
larger parameter counts is an open question this hardware cannot settle, and it
should be treated as a conjecture rather than a plan.

## Status

Nothing here is implemented. The per-modality encoders do not exist, and the
three-way dense/MoE/MoT comparison now running is text-only and unaffected by any
of it. What this document changes is which experiment is worth building next, and
it retires a byte-level multimodal plan that would have consumed GPU time
answering the wrong question.
