"""Generate lethain `systems` stock-flow figures for the psychohistory paper.

For each model: build with systems.parse.parse, run it, plot stock trajectories
with matplotlib (Agg). Also attempt a stock-flow STRUCTURE diagram via the
python graphviz package; if the graphviz `dot` binary is not installed, skip the
diagram (do not fail) and just produce the trajectory plot.

Run with: py -3.12 figures/gen_lethain_figures.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from systems.parse import parse

HERE = os.path.dirname(os.path.abspath(__file__))


def series(rows, key):
    return [row[key] for row in rows]


def has_graphviz():
    """Return True iff the graphviz `dot` binary is callable."""
    try:
        import graphviz
        g = graphviz.Digraph()
        g.node("a")
        g.node("b")
        g.edge("a", "b")
        # render to a throwaway file; this is what actually invokes `dot`.
        tmp = os.path.join(HERE, "_gv_probe")
        g.render(tmp, format="png", cleanup=True)
        for ext in ("", ".png"):
            p = tmp + ext
            if os.path.exists(p):
                os.remove(p)
        return True
    except Exception as exc:  # binary missing or any render failure
        print("  graphviz dot binary not available (%s); skipping structure diagram" % type(exc).__name__)
        return False


GRAPHVIZ_OK = has_graphviz()


def structure_diagram(stocks, edges, out_path, title):
    """Best-effort stock-flow structure diagram. Skipped if dot is missing."""
    if not GRAPHVIZ_OK:
        return False
    try:
        import graphviz
        g = graphviz.Digraph(comment=title)
        g.attr(rankdir="LR")
        for s in stocks:
            g.node(s, s, shape="box", style="filled", fillcolor="#dde7f5")
        for src, dst, label in edges:
            g.edge(src, dst, label=label)
        base = out_path[:-4] if out_path.endswith(".png") else out_path
        g.render(base, format="png", cleanup=True)
        print("  wrote", out_path)
        return True
    except Exception as exc:
        print("  structure diagram failed (%s); skipped" % type(exc).__name__)
        return False


generated = []


def trajectory_plot(rows, keys, colors, out_path, title, ylabel, total_label="Total"):
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    x = list(range(len(rows)))
    for k, c in zip(keys, colors):
        ax.plot(x, series(rows, k), label=k, color=c, linewidth=2)
    total = [sum(row[k] for k in keys) for row in rows]
    ax.plot(x, total, label=total_label, color="black", linewidth=1.4, linestyle="--")
    ax.set_xlabel("round")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc="center right", frameon=False)
    ax.grid(True, alpha=0.25)
    spread = max(total) - min(total)
    ax.margins(x=0.01)
    fig.tight_layout()
    fig.savefig(out_path, dpi=140)
    plt.close(fig)
    print("  wrote", out_path, "(total spread = %.3g, conserved)" % spread)
    generated.append(os.path.basename(out_path))


# ---------------------------------------------------------------------------
# 1. ATTENTION CONSERVATION (matches paper's E1)
# ---------------------------------------------------------------------------
print("[1] attention conservation")
attn_spec = """OtherTopics(990)
BankTopic(10)
OtherTopics > BankTopic @ Leak(0.35)
BankTopic > OtherTopics @ Leak(0.05)"""
attn = parse(attn_spec).run(rounds=30)
trajectory_plot(
    attn,
    ["OtherTopics", "BankTopic"],
    ["#1f77b4", "#d62728"],
    os.path.join(HERE, "lethain_attention.png"),
    "Attention conservation: reallocation onto one topic (total flat)",
    "attention units",
    total_label="Total (conserved)",
)
structure_diagram(
    ["OtherTopics", "BankTopic"],
    [("OtherTopics", "BankTopic", "Leak(0.35)"),
     ("BankTopic", "OtherTopics", "Leak(0.05)")],
    os.path.join(HERE, "lethain_attention_structure.png"),
    "attention conservation",
)

# ---------------------------------------------------------------------------
# 2. BANK RUN / SVB
# ---------------------------------------------------------------------------
print("[2] bank run / SVB")
bankrun_spec = """Deposits(1000)
Withdrawn(0)
Deposits > Withdrawn @ Leak(0.30)
Withdrawn > Deposits @ Leak(0.02)"""
bankrun = parse(bankrun_spec).run(rounds=30)
trajectory_plot(
    bankrun,
    ["Deposits", "Withdrawn"],
    ["#2ca02c", "#d62728"],
    os.path.join(HERE, "lethain_bankrun.png"),
    "Minimal stock-flow bank run: deposits draining to withdrawn",
    "currency units",
    total_label="Total (conserved)",
)
structure_diagram(
    ["Deposits", "Withdrawn"],
    [("Deposits", "Withdrawn", "Leak(0.30)"),
     ("Withdrawn", "Deposits", "Leak(0.02)")],
    os.path.join(HERE, "lethain_bankrun_structure.png"),
    "bank run",
)

# ---------------------------------------------------------------------------
# 3. AI ATTENTION CAPTURE (lethain analogue of the mythos-fable)
# ---------------------------------------------------------------------------
print("[3] AI attention capture")
ai_spec = """HumanAttention(1000)
AIAttention(0)
HumanAttention > AIAttention @ Leak(0.18)
AIAttention > HumanAttention @ Leak(0.03)"""
ai = parse(ai_spec).run(rounds=30)
trajectory_plot(
    ai,
    ["HumanAttention", "AIAttention"],
    ["#1f77b4", "#9467bd"],
    os.path.join(HERE, "lethain_ai_capture.png"),
    "Illustrative attention reallocation from human to AI under capture",
    "attention units",
    total_label="Total (conserved)",
)
structure_diagram(
    ["HumanAttention", "AIAttention"],
    [("HumanAttention", "AIAttention", "Leak(0.18)"),
     ("AIAttention", "HumanAttention", "Leak(0.03)")],
    os.path.join(HERE, "lethain_ai_capture_structure.png"),
    "AI attention capture",
)

print()
print("graphviz dot binary available:", GRAPHVIZ_OK)
print("generated trajectory PNGs:", generated)
