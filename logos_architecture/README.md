# LOGOS Architecture — 10T Mixture-of-Towers for Psychohistory

> **Status:** Draft v0.1 — Under Review  
> **Machine Topology:** Editorial Mac (this machine) + Dedicated GPU Cluster (verification target)  
> **Date:** July 2026

## Overview

This folder contains the architectural specification and verification plan for a **10-trillion-parameter LOGOS-class Mixture-of-Towers (MoT)** system — the computational engine required to realise Psychohistory at scale.

The core psychohistory framework (see parent repo) establishes the mathematical foundations: Boltzmann-transport equations over opinion fields, Langevin noise, Lethain-style organisational dynamics, bifurcation analysis, and early-warning criticality detection. However, the **inference and simulation engine** needed to run these models over real civilisational-scale datasets demands a frontier-class neural architecture operating at ≥10T parameters.

This folder bridges that gap.

## Contents

| File | Description |
|------|-------------|
| [`LOGOS_PAPER.md`](./LOGOS_PAPER.md) | Full architectural paper: system design, theoretical foundations, and regulatory compliance |
| [`GPU_VERIFICATION_OPEN_ITEMS.md`](./GPU_VERIFICATION_OPEN_ITEMS.md) | Verification checklist and open items for the dedicated GPU machine |
| [`ARCHITECTURE_DIAGRAMS.md`](./ARCHITECTURE_DIAGRAMS.md) | Visual architecture diagrams (Mermaid) for the MoT, routing, and deployment topology |
| [`REFERENCES.bib`](./REFERENCES.bib) | Bibliography and key citations |

## Key Design Decisions

1. **5×2.8T MoT over monolithic 10T** — Bypasses the Chinchilla data wall; each tower trains on domain-specific 56T-token corpora
2. **Branch-Adapt-Route (BAR)** — Preserves domain specialisation through post-training without catastrophic forgetting
3. **Heterogeneous MoE + LatentMoE** — Dimensional compression for latency-sensitive distributed inference
4. **Petals-style P2P inference** — Decentralised compute with canary-trap integrity verification
5. **EU AI Act compliance** — Sovereign AI deployment with deterministic fallback routing

## Relationship to Psychohistory Core

```
psychohistory/
├── psychohistory.tex          # Mathematical framework (Boltzmann, bifurcation, LLN)
├── steering_envelope/         # Mean-field models, society simulations
├── validation/                # Empirical backtests (Reddit, Wikipedia, Lethain)
└── logos_architecture/        # ← THIS FOLDER: The 10T engine to run it all
    ├── LOGOS_PAPER.md         # Architecture specification
    ├── GPU_VERIFICATION.md    # What to verify on the GPU machine
    ├── ARCHITECTURE_DIAGRAMS  # Visual reference
    └── REFERENCES.bib         # Citations
```

## Next Steps

1. Review `LOGOS_PAPER.md` for architectural soundness
2. Review `GPU_VERIFICATION_OPEN_ITEMS.md` and prioritise verification experiments
3. Prepare the GPU machine environment per the verification plan
4. Begin Phase 1 micro-benchmarks (single-tower MoE routing)
