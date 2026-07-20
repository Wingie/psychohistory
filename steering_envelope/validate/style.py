"""Shared dark figure style for the validation suite, matched to the site's
instrument aesthetic. Categorical palette validated (CVD + contrast) against
the dark surface with the dataviz six-check validator."""

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

SURFACE = "#0d1322"
PAGE = "#070b14"
INK = "#d7e0ef"
MUTED = "#65748f"
GRID = "#232c40"

# validated categorical order — assign in this fixed order, never cycle
C_BLUE = "#3987e5"
C_GREEN = "#008300"
C_MAGENTA = "#d55181"
C_YELLOW = "#c98500"
SERIES = [C_BLUE, C_GREEN, C_MAGENTA, C_YELLOW]


def apply():
    plt.rcParams.update({
        "figure.facecolor": PAGE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": PAGE,
        "text.color": INK,
        "axes.edgecolor": GRID,
        "axes.labelcolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.size": 10,
        "axes.titlesize": 11,
        "lines.linewidth": 2.0,
        "legend.frameon": False,
        "figure.dpi": 130,
    })
