"""Shared helpers for the test ii' diagnostic variations.

Imports the FROZEN analysis functions from neff_collapse_wiki (coedit_graph,
blind_partition, block_bucket_matrix, neff_macro, neff_pearson,
collapse_for_partition, analyze_run, parse_ts) so every variation reuses the
exact same blocks/metric as the primary run. Does NOT modify any frozen file.
"""
import os
import sys
import json
import datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
WIKI = os.path.dirname(HERE)
DATA = os.path.join(WIKI, "data")
sys.path.insert(0, WIKI)

import neff_collapse_wiki as N  # noqa: E402  frozen analysis functions
import roster as R  # noqa: E402


def load_runs():
    files = sorted(f for f in os.listdir(DATA) if f.endswith(".json"))
    return [json.load(open(os.path.join(DATA, f), encoding="utf-8")) for f in files]


def frozen_partition(rec):
    """The pre-onset blind partition exactly as the primary run computes it."""
    G = N.coedit_graph(rec["editor_contribs"], rec["title"])
    part, mod, K = N.blind_partition(G)
    return part, mod, K, G


def onset_window(onset):
    """The frozen onset window used by analyze_run: [onset-3d, onset+POST+1d)."""
    return (onset - dt.timedelta(days=3),
            onset + dt.timedelta(days=R.POST_DAYS + 1))


def load_primary_result():
    return json.load(open(os.path.join(WIKI, "result_wiki_neff.json"), encoding="utf-8"))
