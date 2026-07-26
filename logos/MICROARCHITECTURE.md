# LOGOS microarchitecture

**One model.** LOGOS is a single system with tower-structured internals, not a
dispatcher in front of separately served models. A dispatcher over hosted models
is commercial routing; it works, it is not the research question, and it forfeits
every property below. If a design in this family can be implemented by putting a
proxy in front of N checkpoints, it is not LOGOS.

This document specifies what a tower is, where routing happens, what the
distributed inference pattern costs, what the KV cache actually looks like, how a
tower is added to a trained system, and the smallest experiment on one RTX 3090
that could distinguish this from a dense model and from a standard MoE.

It also states plainly where the design collapses into known MoE, because a
Mixture-of-Towers that is an MoE with different vocabulary is not a contribution.

---

## 1. What is a tower?

The candidates, and why four of them fail the "one model" test:

| candidate | verdict |
|---|---|
| independently served models + dispatcher | **rejected** — this is a proxy, not an architecture; no shared trunk, no shared KV, no joint training signal |
| per-layer FFN experts, token-level top-k | **this is MoE.** Switch, GLaM, Mixtral, DeepSeek-MoE. Well-studied, works, not ours |
| shared backbone + per-domain LoRA adapters | **rejected as the primary** — adapter capacity is a rounding error against a 10T claim; useful as a cheap tower *variant*, not as the unit |
| full parallel stacks merged at intervals | viable but expensive; merging at intervals reintroduces per-merge communication |
| **shared trunk → routed vertical slice → shared head** | **the design** |

A **tower is a vertical slice**: a contiguous stack of complete transformer
layers, each with its own attention *and* FFN parameters, which a routed sequence
traverses end to end.

```
            tokens
              │
      ┌───────▼────────┐
      │  shared trunk  │   L_t layers, dense, all sequences
      │  (embed + L_t) │   builds the representation the router reads
      └───────┬────────┘
              │
         ┌────▼────┐
         │ router  │      learned, reads pooled trunk state
         └────┬────┘
     ┌────────┼────────┬────────┐
     ▼        ▼        ▼        ▼
  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────┐
  │tower│  │tower│  │tower│  │tower│   L_w layers each,
  │  0  │  │  1  │  │  2  │  │  N-1│   full attention + FFN
  └──┬──┘  └──┬──┘  └──┬──┘  └──┬──┘
     └────────┴────┬───┴────────┘
                   ▼
           ┌───────────────┐
           │ shared head   │   L_h layers + unembed
           └───────────────┘
```

**The distinction from MoE is the axis of the slice, and it is not cosmetic.**
MoE routes *horizontally*: the decision is remade at every layer, and an expert
owns one FFN at one depth. LOGOS routes *vertically*: the decision is made once,
and a tower owns a complete multi-layer computation path.

Three consequences follow, one of them decisive.

---

## 2. Routing: once, per segment, learned

**Not per token.** Token-level routing is what makes MoE's memory and
communication behaviour what it is, and adopting it would collapse this design
into MoE immediately.

**Not majority voting.** Voting is dead — see the variant ledger, Slot 2. It was
a scaffold that leaked into experiments; the design has always specified a
learned router.

The router is a small learned network over the pooled trunk representation,
emitting a distribution over towers. Training follows established MoE practice
because those problems are solved and there is nothing to gain by re-deriving
them:

- **top-k with k=1 or 2**, straight-through or Gumbel for differentiability
- **load-balancing auxiliary loss**, or the loss-free bias-correction approach,
  because expert collapse is the standard failure and it is not exotic
- **a shared/always-on tower** in the DeepSeek-MoE sense, carrying the
  general-purpose competence every domain needs, so specialised towers are not
  forced to relearn common structure

Routing granularity is **per segment** — a sequence, or a bounded span within
one. This is the parameter that decides everything downstream, and §4 is why.

---

## 3. What is genuinely novel, stated so it can be attacked

Two of the three claims below are engineering facts that can be computed. One is
an empirical claim that needs an experiment and might be false.

### 3.1 Communication: one dispatch instead of L round trips (fact)

This is the strongest claim and it is arithmetic.

MoE with expert parallelism performs an **all-to-all at every layer** — tokens
are dispatched to expert devices and gathered back, twice per MoE layer. For a
model with `L` routed layers and hidden size `d`, per token:

```
MoE   :  2 · L · d · bytes        (dispatch + combine, every layer)
LOGOS :  2 ·     d · bytes        (one dispatch after the trunk, one gather)
```

At `d = 8192`, bf16, `L = 32` routed layers:

```
MoE   :  2 × 32 × 8192 × 2  =  1.05 MB per token
LOGOS :  2 ×  1 × 8192 × 2  =  32.8 KB per token
                                 ────────────────
                                 32× less traffic
```

The reduction factor is exactly `L_w`, the tower depth. It gets *better* as
towers get deeper, which is the opposite of MoE's scaling.

**Why this matters more than it looks.** All-to-all at every layer is why MoE
inference wants a fat homogeneous interconnect — NVLink, InfiniBand, one
datacentre. LOGOS routes once, so after the trunk a sequence lives entirely on
one device for the whole tower. That makes the architecture viable on
**heterogeneous, geographically distributed, commodity-interconnect compute**,
which is precisely the deployment story the sovereign-AI thesis needs and which
token-level MoE cannot support.

This is the claim to lead with, because it is checkable without training
anything.

### 3.2 KV cache: per-tower, not per-expert (fact, with a caveat)

Attention lives inside towers, so KV structure differs from MoE in kind.

In MoE, attention is dense and shared; only FFNs are sparse. **KV cache is
therefore full dense cost** — Mixtral caches like a dense model of its depth.

In LOGOS with per-segment routing, a sequence occupies exactly one tower, so it
caches:

```
KV(sequence) = trunk layers (L_t) + one tower's layers (L_w) + head (L_h)
```

which is the KV of a *dense model of depth* `L_t + L_w + L_h`, while the
parameter count is `trunk + N · tower + head`. **N× the parameters at 1× the KV
and 1× the per-token FLOPs.**

**The caveat that kills the naive version.** This holds only for per-segment
routing. Under token-level routing a sequence's tokens scatter across all towers,
every tower needs KV for its subset, and the total returns to dense — plus
fragmentation. Per-segment routing is not a simplification here; it is what the
KV argument rests on.

**And the honest cost:** batching. A server holding N towers can only batch
together sequences routed to the same tower, so effective batch size per tower is
roughly `B/N` under uniform routing. This is a real throughput penalty and it is
the strongest objection to the design. Mitigations — tower-affinity scheduling,
holding hot towers resident, admission control that batches by route — are
scheduling problems, not architecture problems, but they must be measured, not
asserted.

### 3.3 Depth-coherent specialisation (empirical, and might be false)

The claim: because a tower owns a contiguous multi-layer path, it can develop
**circuits that span layers** and are specific to its domain, which per-layer
expert routing cannot form because no expert owns two consecutive depths for the
same token.

This is the only part of the design that is a genuine research bet, and it is
the part most likely to be wrong. It has a clean falsifier — §6.

---

## 4. Adding a tower to a trained system

The paper's bootstrapping ladder requires that a tower be added without
retraining everything. The mechanism is **sparse upcycling**: initialise new
towers from an existing trained checkpoint's corresponding layers, then train the
router and let the copies diverge under a load-balancing pressure.

Concretely, growth from `N` towers to `N+1`:

1. **Clone** tower weights from the tower whose routing load is highest, or from
   the shared tower for a genuinely new domain.
2. **Freeze the trunk and head initially.** They encode the representation the
   router reads; perturbing them invalidates the routing already learned.
3. **Train the router with the new tower admitted at low probability**, raised on
   a schedule, so the system does not collapse routing onto the fresh copy.
4. **Unfreeze the trunk last**, at reduced learning rate, once routing is stable.

Two towers initialised identically will not diverge without a pressure that
rewards divergence. The load-balancing loss supplies it; whether it supplies
*enough* is an open question, and "the clone never differentiates" is a real
failure mode to watch for, not a hypothetical.

This composes with the ladder claim: a layer that has produced `20N` tokens can
bootstrap a higher-parameter model, because upcycling needs a checkpoint and a
corpus, not a from-scratch budget.

---

## 5. What this costs to *not* be MoE

Stated adversarially, because the design should be attackable:

| objection | status |
|---|---|
| "This is MoE with per-sequence routing" | **Partly true, and that is the point.** The routing granularity and the slice axis are the difference, and they change the communication and KV arithmetic by construction. If depth-coherent specialisation (§3.3) also fails, what remains is *an MoE variant with a much better distributed-inference profile* — still useful, and a much smaller claim. |
| "Per-sequence routing wastes capacity — a sequence may need two domains" | Real. Mitigated by the shared/always-on tower and by allowing segment-level (not whole-sequence) granularity. Bounded by measurement, not argument. |
| "Batching collapses" | Real, quantified in §3.2, and the strongest objection. |
| "Router errors are unrecoverable" — a mis-routed sequence traverses the wrong tower entirely, with no per-layer chance to correct | Real and specific to vertical routing. MoE's per-layer re-decision is genuinely more forgiving. This is the price of one dispatch. |

---

## 6. The smallest experiment that decides it, on one RTX 3090

Measured throughput on this card: 13,877 tok/s at 350M, 37,905 tok/s at 125M,
micro-batch 4, AdamW (a floor — Muon is faster). FP8 is unavailable: GA102 is
compute capability 8.6 and the probe recorded `supports_fp8: False`, so the
published 25× speedrun figure does not transfer; 3.19× published / 2.57× measured
does.

**Three-way comparison at matched per-token FLOPs**, which is the only
comparison that means anything:

| arm | shape |
|---|---|
| **dense** | one stack, params = active params |
| **MoE** | shared attention, per-layer top-1 FFN experts, token routing |
| **MoT** | shared trunk, top-1 per-segment tower routing, full layers in towers |

Configuration: `d_model = 512`, 12 layers total (`L_t = 3`, `L_w = 7`,
`L_h = 2`), 4 towers, vocab 32k, context 1024. Active parameters ≈ 60M in all
three arms; total ≈ 60M / 150M / 190M.

Training corpus must have **real domain structure** — the ledger's Slot 6 records
that seed-only members and skewed vocabulary regions both failed as domain
proxies, and skewed vocabulary is frequency skew, not reasoning structure. Real
code / prose / structured-data corpora are available locally.

**Budget.** At the 125M-scale measured rate, ~2B tokens is ≈ 15 GPU-hours per
arm; three arms ≈ 45 GPU-hours, under two days on one card, and the arms can run
sequentially without contention.

### The falsifiers

1. **F-MoT-1, communication (fact-check, not a bet).** Instrument bytes moved per
   token. Expect exactly `L_w`× less than the MoE arm. If this does not hold the
   implementation is wrong, not the theory.
2. **F-MoT-2, depth-coherent specialisation (the real bet).** Measure whether
   tower layers develop *cross-layer* domain-specific structure that MoE experts
   at matched capacity do not. Operationalised as: per-domain gradient conflict
   between towers should exceed per-domain gradient conflict between MoE experts
   at the same layer — the same model-relative measure that F11 now needs
   (ledger, Slot 1), which is why building it serves both.
   **If MoT ≈ MoE here, §3.3 is dead** and the claim reduces to the systems
   argument.
3. **F-MoT-3, batching penalty.** Measure realised throughput under a realistic
   arrival mix. If the `B/N` penalty is not recoverable by tower-affinity
   scheduling, the systems advantage is partly refunded and must be restated.
4. **F-MoT-4, upcycling.** Grow 4 towers → 5. Does the clone differentiate, or
   does routing collapse back?

---

## 7. Honest status

Nothing in this document has been run. LOGOS has zero runs at any scale, and the
three-way comparison in §6 does not exist yet. §3.1 and §3.2 are arithmetic and
can be checked by instrumenting an implementation; §3.3 is a research bet with a
falsifier attached and is the part most likely to die.

The sequencing that follows from that: **build the communication instrumentation
first**, because it validates or kills the strongest claim for the least compute,
and it needs no training run at all.
