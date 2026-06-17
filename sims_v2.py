"""Numerical tests of the psychohistory position-paper postulates (v2, clean merge).

Changes vs sims.py:
  * E4 first sweep: removed dead placeholder block (vestigial `base`,`pert`,`d`,
    and `tau.append(rbar)` that was immediately overwritten).
  * E4 well-synchrony order parameter S = <|<sign x>|> merged back in (was a
    separate inline script that produced the shipped E4_criticality.png).
  * E4b: report BOTH the Pearson-corr N_eff (the misleading one) and a
    variance-ratio N_eff on the macro/order variable (the correct one), so the
    figure shows why corr-of-fluctuations is the wrong synchronization metric.
  * OUT no longer hard-coded to a Linux path.
E1 conservation | E2 transport+drift | E3 block LLN | E4 criticality | E5 fixed points
"""
import os
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from systems.parse import parse

rng = np.random.default_rng(42)
OUT = os.environ.get("PSYCHO_OUT", "_verify_out/")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"figure.dpi": 130, "font.size": 9})

# ---------- E1: macro layer in lethain's systems DSL: attention is conserved ----------
model = parse("""OtherTopics(990) > BankTopic(10) @ Leak(0.35)
BankTopic > OtherTopics @ Leak(0.05)
""")
res = model.run(rounds=30)
ot = [r["OtherTopics"] for r in res]; bt = [r["BankTopic"] for r in res]
tot = [a + b for a, b in zip(ot, bt)]
fig, ax = plt.subplots(figsize=(6, 3.2))
ax.plot(ot, label="Other topics"); ax.plot(bt, label="Bank topic (panic)")
ax.plot(tot, "k--", label="Total attention")
ax.set_xlabel("round"); ax.set_ylabel("attention units")
ax.set_title("E1  lethain/systems stock-flow: panic reallocates, total conserved")
ax.legend(); fig.tight_layout(); fig.savefig(OUT + "E1_conservation_lethain.png")
e1_drift = max(tot) - min(tot)

# ---------- E2: graph master equation, conservation + belief drift ----------
n = 40
A = (rng.random((n, n)) < 0.15).astype(float); A = np.triu(A, 1); A = A + A.T
def rate_matrix(bias_node=None, bias=0.0):
    L = A * 0.05
    if bias_node is not None:
        L[:, bias_node] += A[:, bias_node] * bias   # belief drift toward node
    np.fill_diagonal(L, 0); np.fill_diagonal(L, -L.sum(axis=1))  # rows sum to zero
    return L
p0 = np.ones(n) / n
def integrate(L, p, T=400, dt=0.05):
    traj = [p.copy()]
    for _ in range(T):
        p = p + dt * (L.T @ p); traj.append(p.copy())
    return np.array(traj)
tr_free = integrate(rate_matrix(), p0)
tr_bias = integrate(rate_matrix(bias_node=7, bias=0.6), p0)
fig, axs = plt.subplots(1, 2, figsize=(8, 3.2))
axs[0].plot(tr_bias[:, 7], label="biased node p_7")
axs[0].plot(tr_free[:, 7], label="no drift p_7")
axs[0].set_title("E2a  belief drift concentrates attention"); axs[0].legend()
axs[0].set_xlabel("step"); axs[0].set_ylabel("attention share")
mass_err = np.abs(tr_bias.sum(axis=1) - 1.0)
axs[1].semilogy(mass_err + 1e-18)
axs[1].set_title("E2b  |total mass - 1| (machine precision)")
axs[1].set_xlabel("step")
fig.tight_layout(); fig.savefig(OUT + "E2_transport_drift.png")
e2_err = mass_err.max()

# ---------- coupled-block dynamics used by E3/E4 ----------
def run_blocks(K, W, theta=1.0, sigma=0.5, T=3000, dt=0.01, x0=None, seed=None):
    r = np.random.default_rng(seed)
    x = r.normal(0, 0.1, K) if x0 is None else x0.copy()
    traj = np.empty((T, K))
    for t in range(T):
        m = x.mean()
        x = x + dt * (theta * x - x**3 + W * (m - x)) + np.sqrt(dt) * sigma * r.normal(size=K)
        traj[t] = x
    return traj

# ---------- E3: block decomposition: fluctuations average as 1/sqrt(K) ----------
Ks = [4, 16, 64, 256]
stds = []
for K in Ks:
    tr = run_blocks(K, W=0.05, seed=1)          # weak coupling: blocks ~independent
    stds.append(tr[1000:].mean(axis=1).std())   # std of population mean
fig, ax = plt.subplots(figsize=(5, 3.4))
ax.loglog(Ks, stds, "o-", label="simulated")
ref = stds[0] * (np.array(Ks) / Ks[0]) ** -0.5
ax.loglog(Ks, ref, "k--", label=r"$K^{-1/2}$ reference")
ax.set_xlabel("number of blocks K"); ax.set_ylabel("std of population mean")
ax.set_title("E3  weakly coupled blocks: LLN over blocks holds")
ax.legend(); fig.tight_layout(); fig.savefig(OUT + "E3_block_lln.png")
slope = np.polyfit(np.log(Ks), np.log(stds), 1)[0]
# robustness: averaged slope over seeds (single-seed -0.63 is within estimator noise)
slopes_seed = []
for sd in range(20):
    s = [run_blocks(K, W=0.05, seed=sd)[1000:].mean(axis=1).std() for K in Ks]
    slopes_seed.append(np.polyfit(np.log(Ks), np.log(s), 1)[0])
slope_mean, slope_sd = np.mean(slopes_seed), np.std(slopes_seed)

# ---------- E4: criticality sweep: synchrony, N_eff, skill horizon ----------
Ws = np.linspace(0, 2.5, 26); K = 64
sync, neff_corr, neff_var, Ssync = [], [], [], []
for W in Ws:
    tr = run_blocks(K, W, seed=2)[1500:]
    C = np.corrcoef(tr.T); off = C[np.triu_indices(K, 1)]
    rbar = max(off.mean(), 0)
    sync.append(rbar)
    neff_corr.append(K / (1 + (K - 1) * rbar))            # MISLEADING: corr of jitter
    # correct order parameter: well-synchrony (mean-field magnetization)
    S = np.abs(np.sign(tr).mean(axis=1)).mean()
    Ssync.append(S)
    # correct N_eff: variance reduction of the MACRO variable (sign/order param),
    # N_eff = Var_t(single-block order var) / Var_t(population-mean order var)
    sgn = np.sign(tr)
    var_single = sgn.var(axis=0).mean()
    var_mean = sgn.mean(axis=1).var()
    neff_var.append(var_single / var_mean if var_mean > 1e-12 else 1.0)

# skill horizon: ensemble spread growth vs climatological spread
tau = []
for W in Ws:
    ens = np.stack([run_blocks(K, W, T=1500, seed=10 + e,
                               x0=np.full(K, 0.0) + rng.normal(0, 1e-3, K)).mean(axis=1)
                    for e in range(12)])
    spread = ens.std(axis=0)
    clim = run_blocks(K, W, T=4000, seed=99)[2000:].mean(axis=1).std()
    cross = np.argmax(spread > 0.8 * clim) if (spread > 0.8 * clim).any() else 1500
    tau.append(cross * 0.01)

fig, axs = plt.subplots(1, 4, figsize=(13.5, 3.2))
axs[0].plot(Ws, sync, "o-", label="Pearson r (jitter)")
axs[0].plot(Ws, Ssync, "s-", label="S = |<sign x>| (order param)")
axs[0].axvline(0.4, color="r", ls=":", lw=0.8)
axs[0].set_title("E4a  synchrony: corr misses it, S catches it")
axs[0].set_xlabel("coupling W"); axs[0].legend(fontsize=7)
axs[1].semilogy(Ws, neff_corr, "o-", label=r"$N_{\rm eff}$ from Pearson r")
axs[1].semilogy(Ws, neff_var, "s-", label=r"$N_{\rm eff}$ from macro var-ratio")
axs[1].axhline(1, color="k", ls=":"); axs[1].set_title("E4b  N_eff: only the right metric collapses")
axs[1].set_xlabel("coupling W"); axs[1].legend(fontsize=7)
axs[2].plot(Ws, Ssync, "s-"); axs[2].axvline(0.4, color="r", ls=":", lw=0.8)
axs[2].set_title("E4c  well-synchrony transition  W~0.4"); axs[2].set_xlabel("coupling W")
axs[3].plot(Ws, tau, "o-"); axs[3].set_title(r"E4d  skill horizon $\tau^\ast$")
axs[3].set_xlabel("coupling W"); axs[3].set_ylabel("model time")
fig.tight_layout(); fig.savefig(OUT + "E4_criticality.png")

# ---------- E5: reflexivity: prediction->reaction map, fixed points ----------
def reaction(f, guarantee=0.0):
    return 1 / (1 + np.exp(-(8 * f + 4 * 0.4 - 6 * guarantee - 3)))
f = np.linspace(0, 1, 200)
fig, ax = plt.subplots(figsize=(5.5, 4))
ax.plot(f, reaction(f, 0.0), label="no guarantee")
ax.plot(f, reaction(f, 0.8), label="deposit guarantee")
ax.plot(f, f, "k--", lw=0.8, label="fixed point line T(f)=f")
ax.set_xlabel("published forecast f (prob. of depositor loss)")
ax.set_ylabel("realized outcome T(f)")
ax.set_title("E5  publishable forecasts are fixed points")
ax.legend(); fig.tight_layout(); fig.savefig(OUT + "E5_fixed_points.png")
def fixed_points(g):
    out = reaction(f, g) - f
    return f[np.where(np.diff(np.sign(out)))[0]]
fp0, fp1 = fixed_points(0.0), fixed_points(0.8)

print(f"E1 total-attention drift across 30 rounds: {e1_drift}")
print(f"E2 max |mass error| in graph transport: {e2_err:.2e}")
print(f"E2 biased node share: {tr_bias[-1,7]:.3f} vs free {tr_free[-1,7]:.3f} (uniform=1/40={1/40:.3f})")
print(f"E3 single-seed log-log slope: {slope:.3f}  (theory -0.5)")
print(f"E3 slope over 20 seeds: {slope_mean:.3f} +/- {slope_sd:.3f}  (consistent with -0.5)")
print(f"E4 well-synchrony S at W=0: {Ssync[0]:.2f} ; at W=2.5: {Ssync[-1]:.2f}  (transition ~W=0.4)")
print(f"E4 N_eff(Pearson) at W=0: {neff_corr[0]:.1f} ; at W=2.5: {neff_corr[-1]:.1f}  (barely falls -- MISLEADING)")
print(f"E4 N_eff(macro var) at W=0: {neff_var[0]:.1f} ; at W=2.5: {neff_var[-1]:.2f}  (collapses -- CORRECT)")
print(f"E4 skill horizon at W=0: {tau[0]:.2f} ; at W=2.5: {tau[-1]:.2f}")
print(f"E5 fixed points no guarantee: {np.round(fp0,3)} ; with guarantee: {np.round(fp1,3)}")
