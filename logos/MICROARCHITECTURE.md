# LOGOS microarchitecture

**One distributec p2p training and inference framework scalable to 100T scale depending on hardware available.** 
LOGOS is a distributed system with tower-structured communiation through a learned RQVAE codebook, an trajectoty generation on real workld observations, data acquisition and tower training system, where smaller system bits of it are as acaopable and for larger more complex
loing riunning tasks it the distributed system has a internal routing and comms layer over multiupkle towers or self sufficient nodes
dispatcher in front of separately served models but a system. 
- multimodality
- action heads for screenshot in browser control out 
- continued finetuning to create speciualized towers of different sizes
- ask owner what it is again a

- Domain axis — towers as whole models on their own machines.  KV cannot be shared (separately-learned projections aren't commensurable). but towers must learn to communicate with other efficeintly overrt netwoerks with compressed so then can biuild on and correct opther towers work,.
- Size axis — tiers distilled from one parent: 277M on a phone → 7B → 70B. KV does carry, because they share lineage. Escalation is the sequence. This fits "inference a bit locally and submit to another tower" precisely, and it's where adaptive depth is legal.

-======  EVERYTHING WRONG AND CRAP 0 OWNERS WANT RENALAYSIS after this point! -----
---

# Re-analysis, 2026-08-03

The deleted text described a **different object**: one model on one device, with
towers as vertical slices of its layers. The definition above is a **distributed
p2p system** whose towers are whole models on their own machines, joined by a
learned compressed channel. Re-analysed against that. Where the old text was
wrong it is quoted, so the inversion is visible rather than silent.

| old claim | verdict |
|---|---|
| a tower is a vertical slice; "models + dispatcher" rejected | **half wrong** — the rejection hit *proxies* and still stands; the slice describes one tower's internals, not the system |
| routing once, per segment, learned | **survives, and grows** — the router must also pick a SEQUENCE and a DEPTH |
| one dispatch instead of L round trips | **survives and understates itself ~1600×** once the channel is compressed. This is the spine |
| the KV retraction | **survives, and finally reads correctly** |
| depth-coherent specialisation is the research bet | **demoted** — specialisation comes from data, not from owning contiguous depths |
| sparse upcycling to add a tower | **replaced** by continued finetuning on new data |
| batching collapses at B/N | **mostly dissolves** — each pool batches its own tower |
| dense/MoE/MoT at matched FLOPs decides it | **no longer decisive** — the codebook decides it |
| build comms instrumentation first | **still right, more so** |

## What a tower is, and why this is not a proxy

The old table rejected "independently served models + dispatcher" as *"a proxy,
not an architecture; no shared trunk, no shared KV, no joint training signal."*

**That objection was correct, and it does not hit this design.** It assumed the
only things that could pass between towers were a trunk activation or a KV
cache, so anything lacking both had to be a proxy. The learned codebook is a
third channel and it is the entire difference:

- A **proxy** picks a backend and forwards bytes. Nothing about the channel is
  learned; no backend can act on another's partial work.
- **LOGOS** towers emit and consume codes in a **jointly learned** representation,
  so a tower can take another tower's compressed output, build on it, and correct
  it. The channel itself is trained.

The joint training signal the old text demanded is real — it lives in the
codebook and the comms layer instead of in a shared trunk. This cannot be
assembled from N checkpoints and a load balancer, which was the old text's own
test.

The vertical-slice picture still describes a **single tower's internals**, and
the size axis where tiers share lineage. It never described the system.

## The router decides more than "which"

Per-segment rather than per-token still holds, and network dispatch strengthens
it: per-token routing over a WAN is a latency bill, not a design. What the old
text lacked:

- **which** tower — domain axis
- **which sequence** — "build on and correct other towers' work"
- **how deep** — "smaller system bits of it are as capable", so easy work stops
  early and long-running complex tasks escalate. Adaptive depth is legal on the
  size axis, where lineage is shared

The router must also see the **whole conversation**, not a 128-token pooled
prefix. That is compatible with the paper's causality rule (`logos.tex:316` —
position on the input side is free, position on the target side is the error)
provided the routed unit is a step whose tokens the router was not scored on.

## Communication — the spine, and it undersells itself

The old arithmetic stands:

```
MoE   :  2 · L · d · bytes     (dispatch + combine, every layer)
LOGOS :  2 ·     d · bytes     (one dispatch, one gather)
```

At `d = 8192`, bf16, `L = 32`: 1.05 MB/token against 32.8 KB/token, **32×**.
`CommsLedger` measured 3.43× / 10.28× / 27.44× at L = 4 / 12 / 32.

**But 32.8 KB/token is the UNCOMPRESSED figure and this design does not ship it.**
With a residual quantiser at 8 codebooks × 1024 entries — 80 bits, 10 bytes per
token, out and back:

```
MoE            1.05 MB / token
LOGOS raw     32.8   KB / token       32×
LOGOS coded   20     B  / token   ~52,000×
```

At the sizes that matter, that is the difference between impossible and routine:

```
 40k tok × 16384 dim × 2 B  =  1.3 GB per hop     unshippable
128k tok × 16384 dim × 2 B  =  4.2 GB per hop     unshippable
 40k tok × 10 B             =  400 KB per hop     routine
```

**So the codebook is not a compression nicety bolted onto a working system — it
is the component that decides whether the system exists.** That is the largest
correction here: the old document treated communication as an advantage to be
measured, when it is the load-bearing mechanism to be built.

Two consequences, neither optional:

1. **Routing must survive compression.** If the router cannot route on the code,
   towers cannot live on separate machines. This is verdict 3 of
   `logos/experiments/latentmoe_bench.py` — routing preservation ≥ 80%,
   `I(route_x; route_z)/H(route_x)`, label-free. Built, and **never run**.
2. **Training and serving differ deliberately.** A lossy bottleneck is hostile to
   gradients. Train dense, where a hop is a memory copy; serve compressed, where
   it is a network. The codec still has to be trained *in*, not bolted on.

## The KV retraction predicted the design

> "KV cache: this claim was wrong, and the implementation refuted it… at equal
> total depth gives *identical* cache sizes."

Under the old one-model framing this removed an argument for towers. Here it is
simply why the domain axis needs a codebook: **KV was never going to be the
inter-tower channel**, because separately-learned projections are not
commensurable. The channel had to be something learned and compressed.

The old closing line — *"what the KV argument actually separates LOGOS from is
separately served models"* — is the part that inverts. Separately served models
*are* the domain axis now. What separates LOGOS from them is the learned channel,
not the cache.

KV sharing survives on the **size axis only**, and even there the published
evidence is a warning: `LADDER_ARCHITECTURE.md:220-241` records DroidSpeak
finding that at identical architecture and size, differing only by finetuning,
direct KV reuse was **not** sufficient and per-layer selective recomputation was
required.

## Depth-coherent specialisation is demoted

Old bet: a tower owning contiguous depths forms cross-layer circuits that
per-layer expert routing cannot.

Under this definition towers are whole models specialised by **continued
finetuning on different data**. Depth-coherence is not the mechanism; different
corpora are. Today's measurements force this rather than merely suggesting it:
`break_symmetry(1e-3)` moved inter-tower cosine 1.000004 → 1.000004, and at
12,999 steps one tower carried the model (+0.1928 nats to drop) while another
took 29% of the gradient and cost +0.0068. Towers fed the same data do not
diverge however their layers are arranged.

Not refuted — **relegated**, to a question about one tower's internals.

**The new central bet** is the second half of the communication claim: that a
compressed learned channel preserves enough for a tower to build on and correct
another tower's work. Falsifiable, cheap, unrun.

## Adding a tower

The old mechanism cloned the highest-load tower, froze trunk and head, admitted
at low probability. Its own stated risk was *"two towers initialised identically
will not diverge without a pressure that rewards divergence"* — now measured and
confirmed.

New mechanism: a tower is a copy of a parent finetuned on new data. Divergence
comes from the corpus, which removes that failure. What replaces the freeze/admit
schedule is **codebook stability** — adding a tower must not invalidate the codes
every existing tower already speaks. Open question 1.

## The batching objection mostly dissolves

Old: *"a server holding N towers can only batch sequences routed to the same
tower, so effective batch per tower is roughly B/N… the strongest objection."*

That assumes N towers co-resident on one server. On the domain axis each tower
owns its own pool, so each pool batches its own traffic and there is no B/N
division. What remains is ordinary load imbalance across pools — provisioning and
scheduling, and the reason `arch/critical_path.py` is right that a load vector is
first of all a latency signal. The objection returns intact on the size axis if
tiers share a box.

Two old objections survive and sharpen:

- **Router errors are unrecoverable** — worse here, since a misroute wastes a
  network round trip. Partly offset by the design's own answer: a later tower can
  *correct* an earlier one, a recovery path per-layer MoE lacks.
- **A sequence may need two domains** — now a feature, not a defect, since the
  router may compose a sequence.

## The decisive experiment has changed

The old plan — three-way dense / MoE / MoT at matched per-token FLOPs, ~45
GPU-hours — answers "is a vertical slice better than a horizontal one on one
card." It tests no load-bearing part of this definition.

In order now:

1. **Does routing survive compression?** `latentmoe_bench.py`, verdicts 1–3.
   Built, never run. If verdict 3 fails, towers cannot be distributed and the
   design needs rethinking before anything else is built.
2. **Can tower B build on tower A's codes?** Not designed anywhere. Nearest
   sketch is the steering-prefix injection in
   `probe_results/composition_experiment_design.md:192-229`. This is the "build
   on and correct" claim and it has no falsifier yet.
3. **Does a cascade need a zero-init gate?** Already measured: chaining costs
   +0.3915 nats at the first repetition and degrades monotonically
   (`chain_depth_init`). `logos.tex:1419` — *"a cascade is viable only if its
   second stage is gated to a no-op at step 0."* Nothing implements that gate.
4. Only then the specialisation questions.

## The old sequencing advice was right

> "build the communication instrumentation first, because it validates or kills
> the strongest claim for the least compute, and it needs no training run at all."

Still correct, and now enabling rather than merely strongest. `CommsLedger`
exists and counts bytes. What does not exist is that measurement **with the
codebook in the path** — the number that decides whether 100T is reachable on
available hardware.

## Open — needs the owner, do not guess

1. **Is the codebook shared and frozen, or trained continuously?** Towers are made
   by continued finetuning; the codebook is the shared language. If it keeps
   training, existing towers' codes drift. If it freezes, late towers inherit an
   alphabet chosen before they existed.
      - trained continuosuly, the book by its nature should be shareds over towers
      - like they can update themselves for a data and everyday every netwroskm shares and makes a fiuklkl update?
2. **Who runs the routing/comms layer?** Client-side inside the trust boundary
   (`logos.tex:675` keeps tokenisation, encoding and primary routing inside the
   operator boundary), on every node, or both?
3. **What does a tower emit — a finished answer, or an intermediate state another
   tower continues from?** "Build on and correct" implies the latter, which is a
   much stronger requirement on the codebook.
4. **Action heads** — screenshot in, browser control out. A tower with a different
   head, or a modality path spliced at the encoder per `MULTIMODAL.md`?
5. **Is the size ladder per-domain or global?** Each domain with its own
   277M → 70B, or one ladder all domains escalate through?
