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
LOGOS coded   20     B  / token   ~52,000x   <- HYPOTHETICAL, at d=8192

MEASURED, 2026-08-04, at the size actually running (d_model=1024, Qwen3-0.6B):
raw payload is 2 x 1024 = 2048 B/token and the codebook ships 10 B/token, so
the real ratio is **204.8x**, recorded in
`probe_results/tower_handoff_run1_randomproj.json` (`compression_vs_raw`). The
52,000x above is arithmetic for a d=8192 model nobody has run, and the
"40k tokens -> 400 KB per hop" line below inherits the same hypothetical. Both
are kept because the SCALING argument holds -- the ratio grows with d_model --
but neither is a measurement and neither should be quoted as one.
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
      - agentosaurus.com via b9agent in flowstate-agents
3. **What does a tower emit — a finished answer, or an intermediate state another
   tower continues from?** "Build on and correct" implies the latter, which is a
   much stronger requirement on the codebook.
      - from my understanding of papers its like both like how does adaptinve thinking work
      - if i have low budget only the 12b tower, if i have high, maybe 70bm, if i have ultra pro pax trhinking -> then it can loop over the towers continious,ty more towers again and again, the output when it is satisfied is the "ANSWER" right?
4. **Action heads** — screenshot in, browser control out. A tower with a different
   head, or a modality path spliced at the encoder per `MULTIMODAL.md`?
      - yes its the ultiumate goal
5. **Is the size ladder per-domain or global?** Each domain with its own
   277M → 70B, or one ladder all domains escalate through?
      - who cares? but lower sizes have to be more specialized as they are smaller and can hold less knowlesge
      - ibn the end iots about the user what he ops the distriburted system to learn to be an expert on
      - example -> i would like the suystem to prediuct m,e the weather

---

# What the owner's answers settle, 2026-08-03

Each answer closes a design question and opens an engineering one. Taken
together they are more specific than anything the paper contains.

## 1. The codebook is a continuously-trained shared artifact

Answer: trained continuously, shared across towers by its nature, with towers
updating locally on their own data and the network taking a **full update** on a
period (the owner said "everyday").

That is federated learning, and it is a harder object than a codec. Three
consequences that follow immediately:

- **Codes drift, so a tower's understanding of another tower's output has a
  shelf life.** Between syncs, tower A encodes with codebook version `t` while
  tower B decodes with version `t` too — fine. Across a sync boundary, in-flight
  work is encoded against a version that no longer exists. Every message needs a
  **codebook version stamp**, and a receiver that cannot honour it must be able
  to say so rather than silently mis-decode. Silent mis-decode is the worst
  available failure here because it produces fluent, wrong continuations.
- **Local update + periodic global merge is exactly the setting where codebook
  collapse is documented.** Local drift concentrates usage on a subset of
  entries; the standard mitigations (dead-code re-initialisation, EMA updates,
  usage-balanced commitment) are per-node and interact badly with averaging.
  `evis.py` already has a `codebook_utilisation` gate — that instrument is now
  load-bearing and needs to run per node and after every merge.
- **"Full update" needs a definition.** Averaging codebooks across nodes is not
  the same as averaging weights: entry `k` on node A and entry `k` on node B are
  not the same concept unless something keeps them aligned. Either the merge is
  index-aligned by construction (all nodes start from one book and only ever
  update in place) or it needs an assignment step. This is the single most
  under-specified part of the design and it should be settled before code.

## 2. The comms layer already exists: agentosaurus.com via b9agent

Answer: `agentosaurus.com` via **b9agent** in `flowstate-agents`.

This is the biggest practical finding in the whole re-analysis, because it means
the distributed substrate is **not** a greenfield build. `backend/beta9` is
already a serverless GPU runtime with a gateway, worker agents, Tailscale VPN
networking between heterogeneous machines, and inference routing. That is the
routing/comms layer the paper describes as unbuilt.

So the work is not "build a P2P network". It is:

- a **codec at the b9agent boundary** — encode to codes before the hop, decode
  after
- a **tower registry** — which tower, which size, which domain, which codebook
  version, on which node
- the **routing/escalation policy**, which is the only genuinely new component

`parallax_bench.py` and `swarm_sim.py` simulate scheduling and incentives with
no sockets. Beta9 has the sockets. They should meet.

## 3. Adaptive thinking: budget sets the ceiling, satisfaction ends the loop

Answer, in the owner's words: *"if i have low budget only the 12b tower, if i
have high, maybe 70b, if i have ultra pro max thinking then it can loop over the
towers continuously, more towers again and again, the output when it is
satisfied is the ANSWER."*

So a tower emits **both**: an intermediate state while the loop continues, and a
finished answer when it stops. The loop is the mechanism, and it has two
controls:

- **budget** — a ceiling on which towers may be reached, set per request
- **satisfaction** — the halt criterion, evaluated per iteration

This is test-time compute scaling across a network rather than within one model,
and it makes two things concrete that were vague before. First, the halt
criterion is now the highest-value unbuilt component, not the router: with a
budget ceiling in place, choosing *when to stop* is what decides both cost and
quality. Second, `tower-growth.md`'s unresolved tension is resolved by this
answer — *"LoRA stages buy capacity; full-tower stages buy compute. 'More
thinking' points at the latter."* Looping over whole towers is compute. The
owner's design buys thinking, not capacity.

The measured constraint from `chain_depth_init` still binds and is now
load-bearing rather than academic: naive repetition costs +0.3915 nats at the
first repeat and degrades monotonically. **A loop that returns to a tower must be
gated to a no-op at step 0 (ReZero), or more thinking makes the answer worse.**

## 4. Action heads are the goal, not a side quest

Answer: yes, screenshot in / browser control out is the ultimate goal.

`MULTIMODAL.md`'s contract already specifies the shape — per-modality encoder
into a shared latent space, shared trunk, router, towers, shared head,
per-modality de-tokeniser. Nothing is implemented. The relevant near-term note is
that an action head makes the **satisfaction criterion measurable**: a browser
task either reached the goal state or it did not. That is a real halt signal and
a real reward, and it is much better than any proxy the text corpus offers.

## 5. Small means SPECIALISED, and the user names the domain

Answer: *"lower sizes have to be more specialized as they are smaller and can
hold less knowledge… in the end it's about what the user wants the distributed
system to learn to be an expert on. Example: I would like the system to predict
me the weather."*

This inverts the usual reading of a distillation ladder. The 277M tier is not a
worse generalist — it is a **narrow expert**, and it is narrow *because* it is
small. Capacity forces specialisation rather than merely permitting it.

Two things follow, and the second retires an argument this project has been
having with itself all day:

- **The ladder is effectively per-domain**, whatever the org chart says: a small
  tier can only be small if it is narrow, so "one global 277M" is not a coherent
  object.
- **Specialisation is USER-DIRECTED, not emergent.** The user says what the
  system should become expert on; the system acquires trajectories for it and
  trains a tower. Every experiment from g8 to g17 tried to make specialisation
  *emerge* from a homogeneous corpus, and today's measurements say it does not
  and cannot — one tower carried the model, another took 29% of the gradient and
  cost +0.0068 nats to remove, and `break_symmetry` moved inter-tower cosine
  1.000004 → 1.000004. That whole line of work was answering a question the
  architecture does not ask.

**The weather example is therefore not a side experiment.** It is the worked
example of the entire system: a user names a domain, the trajectory-generation
layer acquires real-world observations for it, a tower is finetuned into an
expert, and the routing layer learns to reach it. `wip-specs/logos/kalshi-weather-shard.md`
is the first instance, and hermes is already fetching the data.

---

## What this makes the build order

1. **`latentmoe_bench` verdict 3** — does routing survive compression. Built,
   never run, and it gates whether towers can be distributed at all.
2. **Codebook versioning and merge semantics** — under-specified above, and
   everything downstream inherits it.
3. **The codec at the b9agent boundary**, since the transport already exists.
4. **The halt criterion**, which answer 3 promotes above the router.
5. **A ReZero gate on any repeated tower**, without which looping degrades.

And explicitly **not**: more emergent-specialisation arms on a homogeneous
corpus. Answer 5 retires that line.

---

## The grounding answer — how divergence is actually avoided, 2026-08-03

Owner: *"the smaller towers basically are getting distilled by the larger
towers, and the data generation using external environment data (weather,
satellite scans in real time over the cities) avoids codebook divergence, or the
data required to train larger arms."*

This answers the merge problem raised under question 1 above, and it answers it
differently on each axis.

**Size axis — alignment by construction.** A small tower distilled from a large
one inherits its teacher's representation. Same lineage, same referents; the
codes agree because the student was trained to match the teacher. This is the
same property that lets KV carry along the size axis, and it means no merge
step is needed there at all.

**Domain axis — alignment by shared external referent.** The failure mode raised
above was that entry `k` on node A and entry `k` on node B are not the same
concept unless something keeps them aligned. Continuously-arriving real-world
observation supplies that something: if every node trains against the same
weather over the same cities and the same satellite passes, the codes have a
**common external referent**. The book is pinned to reality rather than to
another node's weights, and reality does not drift.

**And the same stream solves the data problem, which is the binding constraint
at 100T.** The trajectory corpus is 251,992,064 tokens — 2.86% of Chinchilla for
a 0.6B model, and a rounding error against anything larger. Environmental
observation is unlimited, self-supervised (predict the next observation, no
labels and no synthetic-data pipeline), and **carries its own ground truth**,
because tomorrow scores yesterday's forecast. Every capability number this
project has produced is `gold_novel`, a proxy whose denominator the model itself
controls. A forecast that resolves is not a proxy.

**The limit, stated so it is not discovered later.** Grounding aligns the region
of code space that touches shared observation. A code for "SQL syntax error" has
no weather referent, so purely linguistic or domain-internal regions of the book
are still only aligned by the periodic merge. The anchor is strong where towers
observe the same world and absent where they do not, and a merge should know
which regions are which rather than averaging uniformly across both.

**Satellite imagery makes the multimodal encoder near-term.** Question 4's
action-head/multimodality path was filed as the ultimate goal. Real-time scans
over cities are images, so the per-modality encoder in `MULTIMODAL.md` is not a
later phase — it is how the grounding data enters the system in the first place.
