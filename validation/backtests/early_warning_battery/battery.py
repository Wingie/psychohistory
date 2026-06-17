#!/usr/bin/env py -3.12
"""
EARLY-WARNING FALSIFICATION BATTERY  (multi-cascade, empirical).

Turns the single-cascade early-warning test (validation/temporal/
test_early_warning.py) into a BATTERY across a labeled roster of Reddit
cascades, and tests the framework's *dissociation* prediction:

    ENDOGENOUS, self-reinforcing cascades  -> critical slowing down: a rise in
        variance and lag-1 autocorrelation in the pre-onset window. Framework
        predicts AUC (pre-onset window vs base-rate null) meaningfully > 0.5.
    EXOGENOUS shocks (unexpected announcements) -> NO early warning. Framework
        predicts AUC ~ 0.5 (chance). These are the controls.

PROSECUTOR'S-FALLACY GUARD (Boettiger): "the indicator rose before the cascade"
is worthless alone, because indicators rise before many non-events. We build a
BASE RATE by sliding the identical detector over every non-onset window of equal
length and report where the pre-onset window sits in that null (percentile, AUC).

STRICT INFORMATION CUTOFF: each event's EWS score uses ONLY pre-onset buckets
(the lead window immediately before onset and its equal-length baseline before
that). The base-rate null windows exclude the cascade lead window.

AGGREGATE: distribution of AUC across endogenous vs exogenous events; the
separation (mean diff) and a Mann-Whitney U test (computed from scratch, numpy
only). Verdict: SUPPORTS / INCONCLUSIVE / CONTRADICTS, and whether the
endogenous-vs-exogenous dissociation holds.

Run:  py -3.12 battery.py
Reads data/<key>.json (bare [["date",count],...]) produced by harvest.py.
Writes results/<key>.json, results/_aggregate.json, and prints a table.
"""
import json, os, math, datetime, itertools
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
RES = os.path.join(HERE, "results")
os.makedirs(RES, exist_ok=True)

# Roster: key -> (onset, label, window, freq, human_name, source_note)
# window = EWS rolling window length in buckets (months unless weekly).
# Mirrors harvest.ROSTER; onset/label/window are the analysis knobs.
# All series are WEEKLY density (posts/hour) from the SEARCH endpoint, because
# the AGGREGATE endpoint is unreliable (all-zero for wallstreetbets; global 422
# timeouts). window = EWS rolling window length in WEEKS.
EVENTS = [
    # ---- ENDOGENOUS (framework predicts an early-warning rise) ----
    ("gme_wsb_weekly",   dict(onset="2021-01-25", label="endogenous", window=6, freq="week",
                              name="GameStop squeeze (r/wallstreetbets)")),
    ("superstonk_2021",  dict(onset="2021-06-07", label="endogenous", window=6, freq="week",
                              name="Superstonk June-2021 run-up (r/Superstonk)")),
    ("crypto_2021peak",  dict(onset="2021-05-03", label="endogenous", window=6, freq="week",
                              name="Crypto 2021 peak (r/CryptoCurrency)")),
    ("crypto_luna2022",  dict(onset="2022-05-09", label="endogenous", window=6, freq="week",
                              name="Luna/UST collapse (r/CryptoCurrency)")),
    ("europe_energy2022",dict(onset="2022-09-05", label="endogenous", window=6, freq="week",
                              name="Europe energy crisis (r/europe) [known positive]")),
    ("wsb_meme_2021",    dict(onset="2021-06-01", label="endogenous", window=6, freq="week",
                              name="WSB mid-2021 AMC/meme surge (r/wallstreetbets)")),
    # ---- EXOGENOUS controls (framework predicts NO early warning) ----
    ("askecon_infl2022", dict(onset="2022-02-07", label="exogenous", window=6, freq="week",
                              name="Inflation surge (r/AskEconomics) [known null]")),
    ("askecon_tariff25", dict(onset="2025-04-07", label="exogenous", window=6, freq="week",
                              name="Tariff shock (r/AskEconomics) [known null]")),
    ("europe_covid2020", dict(onset="2020-03-02", label="exogenous", window=6, freq="week",
                              name="COVID lockdown shock (r/europe)")),
    ("crypto_ftx2022",   dict(onset="2022-11-07", label="exogenous", window=6, freq="week",
                              name="FTX collapse announcement (r/CryptoCurrency)")),
]


# ---------- EWS core (adapted from test_early_warning.py) ----------
def ar1(x):
    n = len(x)
    if n < 3:
        return float("nan")
    x = np.asarray(x, float)
    m = x.mean()
    v = ((x - m) ** 2).sum()
    if v == 0:
        return 0.0
    c = ((x[:-1] - m) * (x[1:] - m)).sum()
    return float(c / v)


def variance(x):
    return float(np.var(x)) if len(x) > 1 else 0.0


def window_score(vals, i, window):
    """Composite EWS score for the lead window ending at index i (exclusive),
    relative to the equal-length baseline before it. Higher = stronger warning.
    Returns (score, detail) or None.

    This is the ORIGINAL detector from validation/temporal/test_early_warning.py
    (variance + AR1 RISE relative to an immediately-preceding equal baseline).
    Kept for back-compat; see window_score_csd for the literature-standard
    detrended critical-slowing-down detector used as the battery's PRIMARY."""
    lead = vals[i - window:i]
    base = vals[i - 2 * window:i - window]
    if len(lead) < window or len(base) < window:
        return None
    v_lead, v_base = variance(lead), variance(base)
    a_lead, a_base = ar1(lead), ar1(base)
    dv = (v_lead - v_base) / (v_base + 1e-9)
    da = a_lead - a_base
    if math.isnan(da):
        da = 0.0
    return dv + da, dict(var_lead=v_lead, var_base=v_base, ar1_lead=a_lead, ar1_base=a_base)


# ---------- literature-standard detrended CSD detector (PRIMARY) ----------
def kendall_tau(y):
    """Kendall rank-correlation of y vs time index. Standard EWS trend statistic
    (Dakos et al. 2012). Returns tau in [-1,1]; nan if <3 points."""
    n = len(y)
    if n < 3:
        return float("nan")
    s = 0
    for a in range(n):
        for b in range(a + 1, n):
            d = y[b] - y[a]
            s += (d > 0) - (d < 0)
    denom = n * (n - 1) / 2.0
    return s / denom if denom else float("nan")


def window_score_csd(vals, i, window, sub=4):
    """Critical-slowing-down score for the approach window ENDING at index i
    (exclusive), i.e. vals[i-window:i].

    Canonical recipe (Scheffer/Dakos): (1) DETREND by subtracting a Gaussian-ish
    moving average so we measure fluctuations, not level/trend; (2) compute
    rolling variance and rolling lag-1 AR over sub-windows sweeping the approach
    window; (3) score = Kendall-tau TREND of rolling-variance + Kendall-tau trend
    of rolling-AR1. Rising both => critical slowing down. Higher = stronger
    warning. Returns (score, detail) or None.

    Crucially this is COMPUTED ONLY ON vals[i-window:i] (strict info cutoff for
    the cascade case) and is robust to the absolute level, so a single post-onset
    super-spike inside a NULL window does not auto-win the way a raw variance
    ratio does."""
    seg = np.asarray(vals[i - window:i], float)
    if len(seg) < window or window < 6:
        return None
    # log1p compresses heavy tails (post-squeeze 2000/hr spikes) so variance is
    # not a single-point artifact; monotone, so trend structure is preserved.
    seg = np.log1p(seg)
    # detrend: subtract centered moving average (window 3)
    k = 3
    pad = np.pad(seg, (k // 2, k // 2), mode="edge")
    trend = np.convolve(pad, np.ones(k) / k, mode="valid")
    resid = seg - trend
    # rolling stats over sub-windows of length `sub`
    rv, ra = [], []
    for j in range(len(resid) - sub + 1):
        w = resid[j:j + sub]
        rv.append(float(np.var(w)))
        ra.append(ar1(w))
    ra = [0.0 if (x is None or math.isnan(x)) else x for x in ra]
    if len(rv) < 3:
        return None
    tv = kendall_tau(rv)
    ta = kendall_tau(ra)
    tv = 0.0 if math.isnan(tv) else tv
    ta = 0.0 if math.isnan(ta) else ta
    score = tv + ta
    return score, dict(tau_var=tv, tau_ar1=ta,
                       var_first=rv[0], var_last=rv[-1],
                       ar1_first=ra[0], ar1_last=ra[-1])


def to_date(s):
    return datetime.date.fromisoformat(str(s)[:10])


def load_series(key):
    path = os.path.join(DATA, key + ".json")
    if not os.path.exists(path):
        return None, None, "missing-file"
    ser = json.load(open(path))
    if not ser:
        return None, None, "empty"
    pairs = sorted((to_date(d), float(c)) for d, c in ser)
    dates = [d for d, _ in pairs]
    vals = [c for _, c in pairs]
    return dates, vals, None


def run_event(key, cfg):
    dates, vals, err = load_series(key)
    out = dict(key=key, name=cfg["name"], label=cfg["label"], onset=cfg["onset"],
               window=cfg["window"], freq=cfg["freq"])
    if err:
        out.update(status="NO_DATA", reason=err)
        return out
    nz = sum(1 for v in vals if v > 0)
    out.update(n_buckets=len(vals), nonzero=nz,
               span=f"{dates[0].isoformat()}..{dates[-1].isoformat()}",
               max=max(vals))
    w = cfg["window"]
    if len(vals) < 4 * w:
        out.update(status="INSUFFICIENT_DATA",
                   reason=f"{len(vals)} buckets; need >= {4*w}")
        return out
    if nz < 4 * w:
        out.update(status="INSUFFICIENT_COVERAGE",
                   reason=f"only {nz} nonzero buckets; coverage gap")
        return out
    casc = to_date(cfg["onset"])
    ci = next((k for k, d in enumerate(dates) if d >= casc), None)
    if ci is None or ci < w:
        out.update(status="ONSET_UNUSABLE",
                   reason=f"onset maps to index {ci}; need >= {w} prior buckets")
        return out

    def score_one(detector, need_hist):
        """Score the cascade approach window + build the base-rate null with the
        given detector. need_hist = buckets of history the detector needs."""
        if ci < need_hist:
            return None
        csc = detector(vals, ci, w)
        if csc is None:
            return None
        cscore, det = csc
        null = []
        lo, hi = ci - w, ci  # the cascade approach (lead) window
        for i in range(need_hist, len(vals) + 1):
            l_lo, l_hi = i - w, i
            if not (l_hi <= lo or l_lo >= hi):   # exclude overlap w/ cascade lead
                continue
            sc = detector(vals, i, w)
            if sc is not None:
                null.append(sc[0])
        if len(null) < 5:
            return None
        null = np.asarray(null, float)
        nm, nsd = float(null.mean()), float(null.std()) or 1e-12
        z = (cscore - nm) / nsd
        pct = float((null < cscore).mean())
        auc = float(np.mean(np.where(cscore > null, 1.0,
                                     np.where(cscore == null, 0.5, 0.0))))
        return dict(score=cscore, detail=det, null_mean=nm, null_sd=nsd,
                    n_null=int(len(null)), percentile=pct, z=float(z), auc=auc)

    # PRIMARY: detrended critical-slowing-down (Kendall-tau of rolling var+AR1)
    primary = score_one(window_score_csd, need_hist=w)
    # SECONDARY: original raw variance/AR1-rise detector (needs 2*w history)
    secondary = score_one(window_score, need_hist=2 * w)

    if primary is None:
        out.update(status="INSUFFICIENT_NULL",
                   reason="CSD detector could not form a >=5-window null")
        return out
    d = primary["detail"]
    out.update(status="OK",
               # primary CSD fields
               tau_var=d["tau_var"], tau_ar1=d["tau_ar1"],
               var_first=d["var_first"], var_last=d["var_last"],
               ar1_first=d["ar1_first"], ar1_last=d["ar1_last"],
               ews_score=primary["score"], null_mean=primary["null_mean"],
               null_sd=primary["null_sd"], n_null=primary["n_null"],
               percentile=primary["percentile"], z=primary["z"], auc=primary["auc"],
               detector="detrended_CSD_kendall_tau")
    if secondary is not None:
        out.update(auc_raw=secondary["auc"], percentile_raw=secondary["percentile"],
                   z_raw=secondary["z"])
    return out


# ---------- Mann-Whitney U (two-sided, normal approx with tie correction) ----
def mann_whitney(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    n1, n2 = len(a), len(b)
    if n1 == 0 or n2 == 0:
        return dict(U=None, p=None, note="empty group")
    allv = np.concatenate([a, b])
    order = allv.argsort()
    ranks = np.empty(len(allv), float)
    ranks[order] = np.arange(1, len(allv) + 1)
    # average ranks for ties
    sv = allv[order]
    i = 0
    while i < len(sv):
        j = i
        while j + 1 < len(sv) and sv[j + 1] == sv[i]:
            j += 1
        if j > i:
            avg = (ranks[order[i]] + ranks[order[j]]) / 2.0
            for k in range(i, j + 1):
                ranks[order[k]] = avg
        i = j + 1
    R1 = ranks[:n1].sum()
    U1 = R1 - n1 * (n1 + 1) / 2.0
    U2 = n1 * n2 - U1
    U = min(U1, U2)
    mu = n1 * n2 / 2.0
    # tie correction
    _, counts = np.unique(allv, return_counts=True)
    n = n1 + n2
    tie = (counts ** 3 - counts).sum()
    sigma = math.sqrt(n1 * n2 / 12.0 * ((n + 1) - tie / (n * (n - 1))))
    if sigma == 0:
        return dict(U=float(U), p=1.0, U1=float(U1), AUC_endo_gt_exo=float(U1 / (n1 * n2)))
    z = (U - mu) / sigma
    # two-sided p via erf
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return dict(U=float(U), U1=float(U1), z=float(z), p=float(min(1.0, p)),
                AUC_endo_gt_exo=float(U1 / (n1 * n2)))


def main():
    results = []
    for key, cfg in EVENTS:
        r = run_event(key, cfg)
        results.append(r)
        json.dump(r, open(os.path.join(RES, key + ".json"), "w"), indent=2)

    ok = [r for r in results if r["status"] == "OK"]
    endo = [r["auc"] for r in ok if r["label"] == "endogenous"]
    exo = [r["auc"] for r in ok if r["label"] == "exogenous"]

    print("=" * 104)
    print("EARLY-WARNING BATTERY  -- per-event results   (PRIMARY detector = detrended CSD, Kendall-tau)")
    print("=" * 104)
    hdr = (f"{'event':22s} {'label':10s} {'AUC':>6s} {'pct':>6s} {'z':>6s} "
           f"{'tauVar':>7s} {'tauAR1':>7s} {'AUCraw':>7s}  status")
    print(hdr); print("-" * len(hdr))
    for r in results:
        if r["status"] == "OK":
            print(f"{r['key']:22s} {r['label']:10s} {r['auc']:6.3f} "
                  f"{r['percentile']*100:5.1f}% {r['z']:6.2f} {r['tau_var']:7.3f} "
                  f"{r['tau_ar1']:7.3f} {r.get('auc_raw', float('nan')):7.3f}  OK")
        else:
            print(f"{r['key']:22s} {r['label']:10s} {'--':>6s} {'--':>6s} {'--':>6s} "
                  f"{'--':>7s} {'--':>7s} {'--':>7s}  {r['status']}: {r.get('reason','')}")

    agg = dict(n_endogenous=len(endo), n_exogenous=len(exo),
               endo_aucs=endo, exo_aucs=exo)
    print("\n" + "=" * 100)
    print("AGGREGATE  -- endogenous vs exogenous")
    print("=" * 100)
    if endo:
        agg["endo_mean_auc"] = float(np.mean(endo)); agg["endo_median_auc"] = float(np.median(endo))
        print(f"  endogenous  N={len(endo)}  mean AUC={np.mean(endo):.3f}  "
              f"median={np.median(endo):.3f}  AUCs={[round(x,3) for x in endo]}")
    if exo:
        agg["exo_mean_auc"] = float(np.mean(exo)); agg["exo_median_auc"] = float(np.median(exo))
        print(f"  exogenous   N={len(exo)}  mean AUC={np.mean(exo):.3f}  "
              f"median={np.median(exo):.3f}  AUCs={[round(x,3) for x in exo]}")
    if endo and exo:
        sep = float(np.mean(endo) - np.mean(exo))
        mw = mann_whitney(endo, exo)
        agg["separation_mean_auc"] = sep
        agg["mann_whitney"] = mw
        print(f"  SEPARATION (mean endo - mean exo): {sep:+.3f}")
        print(f"  Mann-Whitney U={mw['U']}  AUC[endo>exo]={mw.get('AUC_endo_gt_exo'):.3f}  "
              f"p(two-sided)={mw.get('p')}")

        # verdict
        endo_above = np.mean(endo) > 0.5
        dissociation = sep > 0.0
        if np.mean(endo) >= 0.65 and sep >= 0.15:
            verdict = "SUPPORTS"
        elif np.mean(endo) > 0.5 and sep > 0.0:
            verdict = "WEAK SUPPORT / INCONCLUSIVE"
        elif abs(sep) <= 0.1:
            verdict = "INCONCLUSIVE (no separation)"
        else:
            verdict = "CONTRADICTS"
        agg["endo_mean_above_half"] = bool(endo_above)
        agg["dissociation_holds"] = bool(dissociation)
        agg["verdict"] = verdict
        print(f"\n  endogenous mean AUC > 0.5 : {endo_above}")
        print(f"  dissociation (endo>exo)   : {dissociation}")
        print(f"  VERDICT                   : {verdict}")
    else:
        agg["verdict"] = "INSUFFICIENT_EVENTS"
        print("  Not enough usable events in one or both groups for an aggregate test.")

    # ---- window-sensitivity sweep (transparency; not used to pick the verdict) ----
    print("\n" + "=" * 100)
    print("WINDOW SENSITIVITY (primary CSD detector) -- reported for honesty, NOT tuned to")
    print("=" * 100)
    sweep = []
    for W in (6, 8, 10, 12):
        e, x, g = [], [], None
        for key, cfg in EVENTS:
            c = dict(cfg); c["window"] = W
            r = run_event(key, c)
            if r["status"] != "OK":
                continue
            if key == "gme_wsb_weekly":
                g = r["auc"]
            (e if r["label"] == "endogenous" else x).append(r["auc"])
        em = float(np.mean(e)) if e else float("nan")
        xm = float(np.mean(x)) if x else float("nan")
        row = dict(window=W, gme_auc=g, endo_mean=em, exo_mean=xm, separation=em - xm,
                   n_endo=len(e), n_exo=len(x))
        sweep.append(row)
        print(f"  W={W:2d}  GME_AUC={(g if g is not None else float('nan')):.3f}  "
              f"endo_mean={em:.3f}  exo_mean={xm:.3f}  sep={em - xm:+.3f}")
    agg["window_sensitivity"] = sweep
    agg["primary_window"] = EVENTS[0][1]["window"]

    json.dump(agg, open(os.path.join(RES, "_aggregate.json"), "w"), indent=2)
    print(f"\nSAVED per-event JSON + results/_aggregate.json")


if __name__ == "__main__":
    main()
