"""OBJ 1 - semantic_csd.py  (L2/L6 observation operator)

Vector belief-variance early-warning. The v0.2 pilots measured critical slowing
down on a SCALAR (posts/hour density) -- the zeroth moment of a scalar -- which
strips the belief vector and provably cannot see belief DISPERSION rising while
volume is flat (the exact failure mode that washed out the impersonal "tremor"
test). Here we embed raw post text with all-MiniLM-L6-v2 (CPU, local) and compute
SECOND-MOMENT signatures of the state vector:

  * rolling VARIANCE of cosine similarity between sequential posts (belief spread);
  * lag-1 AUTOCORRELATION of per-bucket centroids (centroid persistence / slowing);

then run the SAME detrended Kendall-tau detector used by the volume pilots on the
semantic-variance series, so the comparison is apples-to-apples.

Substrate: AskEconomics post text (validation/temporal/data/ask_econ.ndjson),
which spans 2025-03..2025-05 and straddles the 2025-04-02 "Liberation Day" tariff
onset -- one of the battery's labelled exogenous events. (The 2022 inflation onset
is NOT in this corpus; ask_econ.ndjson is 2025-only.) GME/WSB post text is not on
disk; reharvest_text.py attempts to pull it -- if that succeeds we also run here.

Embeddings cached to .npy keyed by post id. Pure transforms.
"""
import json
import os
import sys
import datetime as dt
from collections import defaultdict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import common as C

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL_NAME = "all-MiniLM-L6-v2"
_MODEL = None


def get_model():
    global _MODEL
    if _MODEL is None:
        from sentence_transformers import SentenceTransformer
        _MODEL = SentenceTransformer(MODEL_NAME, device="cpu")
    return _MODEL


# --------------------------------------------------------------- loaders -----
def load_ask_econ_posts():
    """Return list of {id, created_utc, date, text}. text = title + selftext."""
    out = []
    for fn in ["ask_econ.ndjson", "ask_econ_older.ndjson"]:
        path = os.path.join(C.VAL, "temporal", "data", fn)
        if not os.path.exists(path):
            continue
        for L in open(path, encoding="utf-8"):
            L = L.strip()
            if not L:
                continue
            o = json.loads(L)
            ts = o.get("created_utc")
            if not ts:
                continue
            txt = ((o.get("title") or "") + ". " + (o.get("selftext") or "")).strip()
            if len(txt) < 12:
                continue
            d = dt.datetime.utcfromtimestamp(int(ts)).date()
            out.append(dict(id=o.get("id", str(ts)), created_utc=int(ts),
                            date=d, text=txt[:2000]))
    # dedup by id, sort by time
    seen, dedup = set(), []
    for p in sorted(out, key=lambda x: x["created_utc"]):
        if p["id"] in seen:
            continue
        seen.add(p["id"])
        dedup.append(p)
    return dedup


def load_harvested_gme():
    path = os.path.join(HERE, "wsb_text_harvest.json")
    if not os.path.exists(path):
        return None
    recs = json.load(open(path, encoding="utf-8"))
    out = []
    for o in recs:
        ts = o.get("created_utc")
        txt = ((o.get("title") or "") + ". " + (o.get("selftext") or "")).strip()
        if not ts or len(txt) < 12:
            continue
        out.append(dict(id=o.get("id", str(ts)), created_utc=int(ts),
                        date=dt.datetime.utcfromtimestamp(int(ts)).date(),
                        text=txt[:2000]))
    return sorted(out, key=lambda x: x["created_utc"]) if out else None


# --------------------------------------------------------------- embedding ---
def embed_posts(posts, cache_key):
    cache = os.path.join(HERE, f"emb_{cache_key}.npy")
    idcache = os.path.join(HERE, f"emb_{cache_key}_ids.json")
    ids = [p["id"] for p in posts]
    if os.path.exists(cache) and os.path.exists(idcache):
        if json.load(open(idcache)) == ids:
            return np.load(cache)
    model = get_model()
    emb = model.encode([p["text"] for p in posts], batch_size=64,
                       show_progress_bar=False, normalize_embeddings=True)
    emb = np.asarray(emb, np.float32)
    np.save(cache, emb)
    json.dump(ids, open(idcache, "w"))
    return emb


# ----------------------------------------------------- semantic observables --
def bucket_indices(posts, freq="day"):
    """Return ordered list of (bucket_date, [post indices]) buckets."""
    buckets = defaultdict(list)
    for i, p in enumerate(posts):
        if freq == "week":
            d = p["date"] - dt.timedelta(days=p["date"].weekday())
        else:
            d = p["date"]
        buckets[d].append(i)
    return [(k, buckets[k]) for k in sorted(buckets)]


def semantic_series(posts, emb, freq="day", min_per_bucket=4):
    """For each time bucket compute:
      sem_var  = variance of pairwise cosine similarity within the bucket
                 (belief dispersion; high = beliefs spread out);
      centroid = mean embedding (renormalised).
    Returns (dates, sem_var[], centroids[NxD]) for buckets with >= min posts."""
    dates, sem_var, cents = [], [], []
    for d, idx in bucket_indices(posts, freq):
        if len(idx) < min_per_bucket:
            continue
        E = emb[idx]
        S = E @ E.T
        iu = np.triu_indices_from(S, k=1)
        sims = S[iu]
        sem_var.append(float(np.var(sims)))
        c = E.mean(axis=0)
        n = np.linalg.norm(c)
        cents.append(c / n if n > 0 else c)
        dates.append(d)
    return dates, np.asarray(sem_var), np.asarray(cents)


def centroid_ar1_series(centroids, sub=4):
    """Rolling lag-1 autocorrelation of the centroid trajectory: for each window
    of `sub` consecutive centroids, mean cosine between consecutive centroids
    (centroid persistence; rising => critical slowing of the belief mean)."""
    out = []
    for j in range(len(centroids) - sub + 1):
        w = centroids[j:j + sub]
        cs = [float(np.dot(w[k], w[k + 1])) for k in range(len(w) - 1)]
        out.append(float(np.mean(cs)) if cs else 0.0)
    return np.asarray(out)


# ------------------------------------------------------------- detector -------
def run_semantic_csd(posts, emb, onset_date, freq="day", label=""):
    dates, sem_var, cents = semantic_series(posts, emb, freq=freq)
    if len(dates) < 8:
        return dict(label=label, status="TOO_FEW_BUCKETS", n_buckets=len(dates))
    # pre-onset slice for the strict-cutoff CSD read
    pre_mask = [d < onset_date for d in dates]
    n_pre = sum(pre_mask)
    # detrended CSD on the SEMANTIC variance over the whole approach series,
    # and separately on the strictly-pre-onset slice (information cutoff).
    csd_full = C.detrended_csd(sem_var, sub=4, log=False)
    pre_var = sem_var[:n_pre] if n_pre >= 6 else None
    csd_pre = C.detrended_csd(pre_var, sub=4, log=False) if pre_var is not None else None

    # centroid AR1 trend (slowing of belief mean) over pre-onset slice
    cent_ar1 = centroid_ar1_series(cents, sub=4)
    pre_ar1 = cent_ar1[:max(0, n_pre - 3)]
    tau_ar1 = C.kendall_tau(list(pre_ar1)) if len(pre_ar1) >= 3 else float("nan")

    return dict(label=label, status="OK", freq=freq, onset=str(onset_date),
                n_buckets=len(dates), n_pre_buckets=int(n_pre),
                dates=[str(d) for d in dates],
                sem_var=[float(x) for x in sem_var],
                csd_full=csd_full, csd_pre=csd_pre,
                centroid_ar1_tau_pre=(None if np.isnan(tau_ar1) else float(tau_ar1)),
                sem_var_pre_mean=float(np.mean(sem_var[:n_pre])) if n_pre else None,
                sem_var_onset_mean=float(np.mean(sem_var[n_pre:])) if n_pre < len(sem_var) else None)


def run():
    results = {"model": MODEL_NAME, "askeconomics": None, "gme_wsb": None}

    # ---- AskEconomics 2025 tariff onset ----
    posts = load_ask_econ_posts()
    emb = embed_posts(posts, "ask_econ")
    onset = C.to_date("2025-04-02")  # Liberation Day tariff announcement
    rec = run_semantic_csd(posts, emb, onset, freq="day", label="askecon_tariff2025")
    rec["n_posts"] = len(posts)
    rec["corpus_span"] = f"{posts[0]['date']}..{posts[-1]['date']}"
    rec["volume_csd_comparison"] = (
        "v0.2 battery scored askecon_tariff2025 as exogenous via the operator/volume "
        "detectors; the impersonal volume-CSD did not give a reliable pre-onset warning "
        "(battery endogenous mean AUC ~0.5). See csd_pre.score below for the semantic read.")
    results["askeconomics"] = rec

    # ---- GME/WSB (only if reharvest succeeded) ----
    gme = load_harvested_gme()
    if gme:
        emb_g = embed_posts(gme, "wsb_gme")
        onset_g = C.to_date("2021-01-25")
        recg = run_semantic_csd(gme, emb_g, onset_g, freq="day", label="gme_wsb_2021")
        recg["n_posts"] = len(gme)
        recg["corpus_span"] = f"{gme[0]['date']}..{gme[-1]['date']}"
        results["gme_wsb"] = recg
    else:
        results["gme_wsb"] = dict(status="PENDING_REHARVEST",
                                  note="WSB post text not on disk; run reharvest_text.py. "
                                       "If the Arctic Shift search harvest succeeds it writes "
                                       "wsb_text_harvest.json and this block runs automatically.")

    with open(os.path.join(HERE, "result_semantic_csd.json"), "w") as f:
        json.dump(results, f, indent=2)
    make_figure(results)
    return results


def make_figure(results):
    recs = [r for r in [results["askeconomics"], results["gme_wsb"]]
            if r and r.get("status") == "OK"]
    if not recs:
        return
    fig, axes = plt.subplots(1, len(recs), figsize=(6.5 * len(recs), 4.3), squeeze=False)
    for ax, rec in zip(axes[0], recs):
        dts = [dt.date.fromisoformat(s) for s in rec["dates"]]
        ax.plot(dts, rec["sem_var"], "-o", ms=3, color="#16a085",
                label="semantic variance (belief dispersion)")
        ax.axvline(dt.date.fromisoformat(rec["onset"]), ls="--", c="r",
                   alpha=0.7, label="onset")
        sc = rec["csd_pre"]["score"] if rec.get("csd_pre") else float("nan")
        ax.set_title(f"{rec['label']}  pre-onset semantic-CSD tau-sum={sc:.2f}", fontsize=9)
        ax.set_ylabel("Var(cosine sim) per bucket")
        ax.tick_params(axis="x", rotation=40, labelsize=7)
        ax.legend(fontsize=8)
    fig.suptitle("OBJ1: semantic critical-slowing-down (embedding variance)", fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(HERE, "figure_semantic_csd.png"), dpi=110)
    plt.close(fig)


if __name__ == "__main__":
    r = run()
    for key in ("askeconomics", "gme_wsb"):
        rec = r[key]
        if rec and rec.get("status") == "OK":
            pre = rec.get("csd_pre") or {}
            full = rec.get("csd_full") or {}
            print(f"{rec['label']:20s} buckets={rec['n_buckets']} pre={rec['n_pre_buckets']} "
                  f"semCSD_pre.score={pre.get('score')} (tv={pre.get('tau_var')},ta={pre.get('tau_ar1')}) "
                  f"semCSD_full.score={full.get('score')} "
                  f"sem_var pre={rec['sem_var_pre_mean']:.4f} onset={rec.get('sem_var_onset_mean')}")
        else:
            print(f"{key:20s} {rec.get('status') if rec else 'None'}")
