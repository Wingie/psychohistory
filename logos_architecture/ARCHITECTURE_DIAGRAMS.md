# LOGOS Architecture — Visual Reference

## 1. System Overview: 5×2.8T Mixture-of-Towers

```mermaid
graph TD
    User([User Query]) --> MR["Master Router (RL-trained)"]
    MR --> CT["Code Tower (2.8T)"]
    MR --> LST["Life Sciences Tower (2.8T)"]
    MR --> MT["Mathematics Tower (2.8T)"]
    MR --> LT["Logic Tower (2.8T)"]
    MR --> AT["Administration Tower (2.8T)"]
    CT --> RA["Response Aggregator"]
    LST --> RA
    MT --> RA
    LT --> RA
    AT --> RA
    RA --> Out(["Merged Output (14T parameters)"])
```

## 2. Single Tower Internal Architecture

```mermaid
graph TD
    In([Input Tokens]) --> Embed["Embedding Layer"]
    Embed --> Block1["Interleaved Block 1"]
    
    subgraph Block1_Subgraph ["Interleaved Block (3:1 Ratio)"]
        KDA1["KDA Layer 1"] --> KDA2["KDA Layer 2"]
        KDA2 --> KDA3["KDA Layer 3"]
        KDA3 --> MLA1["MLA Layer 1"]
    end
    
    Block1 --> Block1_Subgraph
    Block1_Subgraph -.-> DAR["Delta Attention Residuals"]
    DAR -.-> BlockN["Further Blocks"]
    
    MLA1 --> HMoE["HMoE Routing at FFN"]
    
    subgraph HMoE_Subgraph ["Heterogeneous MoE"]
        LRE["Large Reasoning Experts"]
        MGE["Medium General Experts"]
        SSE["Small Syntactic Experts"]
    end
    
    HMoE --> HMoE_Subgraph
    HMoE_Subgraph --> LMoE["LatentMoE Compression (d -> ℓ -> d)"]
    LMoE --> BlockN
    BlockN --> OutHead["Output Head"]
```

## 3. Branch-Adapt-Route (BAR) Training Pipeline

```mermaid
flowchart TD
    DSM[("Shared Dense Seed Model")] --> Branch["Branching"]
    Branch --> Path1["Code Path"]
    Branch --> Path2["Life Sciences Path"]
    Branch --> Path3["Math Path"]
    Branch --> Path4["Logic Path"]
    Branch --> Path5["Admin Path"]
    
    subgraph Training_Pipeline ["Training Pipeline"]
        Path1 --> MT1["Mid-Training"] --> SFT1["SFT"] --> RL1["Domain-Specific RL"]
        Path2 --> MT2["Mid-Training"] --> SFT2["SFT"] --> RL2["Domain-Specific RL"]
        Path3 --> MT3["Mid-Training"] --> SFT3["SFT"] --> RL3["Domain-Specific RL"]
        Path4 --> MT4["Mid-Training"] --> SFT4["SFT"] --> RL4["Domain-Specific RL"]
        Path5 --> MT5["Mid-Training"] --> SFT5["SFT"] --> RL5["Domain-Specific RL"]
    end
    
    RL1 --> MoT["Unified MoT via Lightweight Router Tuning"]
    RL2 --> MoT
    RL3 --> MoT
    RL4 --> MoT
    RL5 --> MoT
    
    MoT --> Upgrade[("Continuous Tower Upgrade Path")]
```

## 4. LatentMoE Compression Flow

```mermaid
flowchart TD
    X["Token Hidden State (x_t ∈ R^d)"] --> Wd["W_down Projection"]
    Wd --> Z["Compressed Space (z_t ∈ R^ℓ)"]
    
    X --> Gate["Router Gating (g_j(x_t)) on full dimension d"]
    Gate --> Comb
    
    Z --> Exp["Expert Computation E_j(z_t) in compressed space"]
    Exp --> Comb["Weighted Combination"]
    
    Comb --> Wu["W_up Projection back to R^d"]
```

## 5. Quantile Balancing + Causal Dual Bias

```mermaid
flowchart TD
    Logits["Router logits s(i,j)"] --> QB["Quantile Balancing (QB)"]
    QB --> Params["Compute quantiles -> α(i), β(j)"]
    Params --> BiasUp["Bias update b(j)"]
    
    Logits --> CDB["Causal Dual Bias (CDB)"]
    CDB --> Dual["Dual variable β_t"]
    Dual --> Penalty["Penalty application"]
    
    BiasUp --> Balanced["Balanced Routing"]
    Penalty --> Balanced
    
    Balanced --> NoAux["No auxiliary losses in the path"]
```

## 6. Distributed Inference Topology

```mermaid
graph TD
    subgraph Sovereign ["Sovereign Cloud Zone"]
        Tok["Tokenizer"] --> Enc["KDA Encoder"]
        Enc --> IR["MoE Initial Router"]
    end
    
    subgraph P2P ["P2P Network Zone"]
        IR --> Petals["Petals Nodes (Heterogeneous GPUs)"]
        Petals --> FaaS["FaaSMoE Function Endpoints"]
    end
    
    subgraph Cache ["Sticky KV Cache Node"]
        SF["StateFlow Owner Selection"]
        PKV["PiKV Memory Management"]
    end
    
    FaaS <--> Cache
    
    subgraph Overlay ["Canary Trap Verification Overlay"]
        Verif["Cryptographic Module Hash Verification"]
    end
    
    P2P -.-> Overlay
```

## 7. Sovereign AI Compliance Flow

```mermaid
flowchart TD
    In([Incoming Query]) --> HR{"High-risk domain?"}
    HR -- Yes --> Mask["Apply Safety Gating Mask G_masked"]
    HR -- No --> DR
    Mask --> DR{"Data residency compliance?"}
    
    DR -- No --> DF["Deterministic Fallback"]
    DR -- Yes --> Hash{"Module hash verification?"}
    
    Hash -- Fail --> Abort([Abort Operation])
    Hash -- Pass --> Norm["Normal Routing"]
    
    Norm --> Exec["Tower Execution"]
    Exec --> Out([Response])
```

## 8. Psychohistory Integration Map

```mermaid
graph LR
    subgraph Framework ["Psychohistory Framework"]
        BT["Boltzmann Transport"]
        DM["Demographic Models"]
        MFT["Mean-Field Theory"]
        CI["Causal Inference"]
        PE["Policy & Ethics"]
    end
    
    subgraph LOGOS ["LOGOS 10T MoT"]
        CT["Code Tower (Simulation Engine)"]
        LST["Life Sciences Tower"]
        MT["Mathematics Tower"]
        LT["Logic Tower"]
        AT["Administration Tower"]
    end
    
    BT --> CT
    DM --> LST
    MFT --> MT
    CI --> LT
    PE --> AT
    
    CT --> SE["Steering Envelope"]
    LST --> SE
    MT --> SE
    LT --> SE
    AT --> SE
    
    SE --> CD["Crisis Detection"]
    SE --> PH["Prediction Horizons"]
```

## 9. Verification Phase Dependencies

```mermaid
gantt
    title Verification Phase Dependencies
    dateFormat X
    axisFormat %s
    
    section Independent
    Phase 0: Micro-benchmarks    :a1, 0, 10d
    
    section Dependent
    Phase 1: Tower Prototype     :a2, after a1, 15d
    Phase 2: MoT Integration     :a3, after a2, 20d
    Phase 3: P2P Distributed     :a4, after a3, 20d
    Phase 4: Psychohistory Integration :a5, after a3, 25d
```
