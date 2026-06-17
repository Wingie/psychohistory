"""Numerical tests of the psychohistory position-paper postulates.
E1 conservation (lethain systems lib) | E2 transport+drift | E3 block statistics
E4 criticality, synchrony, skill horizon, early warning | E5 reflexivity fixed points
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from systems.parse import parse

rng = np.random.default_rng(42)
OUT = "/mnt/user-data/outputs/"
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
    np.fill_diagonal(L, 0); np.fill_diagonal(L, -L.sum(axis=1))
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

# ---------- E4: criticality sweep: synchrony, N_eff, skill horizon, early warning ----------
Ws = np.linspace(0, 2.5, 26); K = 64
sync, neff, tau = [], [], []
for W in Ws:
    tr = run_blocks(K, W, seed=2)[1500:]
    C = np.corrcoef(tr.T); off = C[np.triu_indices(K, 1)]
    rbar = max(off.mean(), 0)
    sync.append(rbar)
    neff.append(K / (1 + (K - 1) * rbar))       # effective independent blocks
    # skill horizon: twin-run divergence (ensemble spread reaching saturation)
    base = run_blocks(K, W, seed=3)
    pert = run_blocks(K, W, seed=3, x0=base[0] + 1e-3)  # same noise seed, perturbed ic
    d = np.linalg.norm(run_blocks(K, W, seed=4) [ -1] * 0)  # placeholder removed below
    tau.append(rbar)  # placeholder; replaced by spread calc next loop
# proper skill horizon: ensemble spread growth vs climatological spread
tau = []
for W in Ws:
    ens = np.stack([run_blocks(K, W, T=1500, seed=10 + e,
                               x0=np.full(K, 0.0) + rng.normal(0, 1e-3, K)).mean(axis=1)
                    for e in range(12)])
    spread = ens.std(axis=0)
    clim = run_blocks(K, W, T=4000, seed=99)[2000:].mean(axis=1).std()
    cross = np.argmax(spread > 0.8 * clim) if (spread > 0.8 * clim).any() else 1500
    tau.append(cross * 0.01)
fig, axs = plt.subplots(1, 3, figsize=(10.5, 3.2))
axs[0].plot(Ws, sync, "o-"); axs[0].set_title("E4a  cross-block synchrony")
axs[0].set_xlabel("coupling W"); axs[0].set_ylabel(r"mean pairwise corr $\bar r$")
axs[1].semilogy(Ws, neff, "o-"); axs[1].set_title(r"E4b  $N_{\mathrm{eff}}=K/(1+(K-1)\bar r)$")
axs[1].set_xlabel("coupling W"); axs[1].axhline(1, color="k", ls=":")
axs[2].plot(Ws, tau, "o-"); axs[2].set_title(r"E4c  skill horizon $\tau^\ast$")
axs[2].set_xlabel("coupling W"); axs[2].set_ylabel("model time")
fig.tight_layout(); fig.savefig(OUT + "E4_criticality.png")

# early warning: ramp W slowly through the transition, watch variance & lag-1 ac of mean
T = 30000; dt = 0.01; K = 64
Wt = np.linspace(0.2, 2.2, T)
r = np.random.default_rng(7); x = r.normal(0, 0.1, K); means = np.empty(T)
for t in range(T):
    m = x.mean()
    x = x + dt * (1.0 * x - x**3 + Wt[t] * (m - x)) + np.sqrt(dt) * 0.5 * r.normal(size=K)
    means[t] = m
win = 2000
var = np.array([means[i - win:i].var() for i in range(win, T)])
ac1 = np.array([np.corrcoef(means[i - win:i - 1], means[i - win + 1:i])[0, 1]
                for i in range(win, T, 50)])
fig, axs = plt.subplots(3, 1, figsize=(7, 6), sharex=False)
axs[0].plot(Wt, means, lw=0.4); axs[0].set_title("E4d  population mean during slow ramp of coupling")
axs[0].set_xlabel("coupling W(t)")
axs[1].plot(Wt[win:], var, lw=0.8); axs[1].set_title("rolling variance (early warning)")
axs[1].set_xlabel("coupling W(t)")
axs[2].plot(Wt[win::50], ac1, lw=0.8); axs[2].set_title("rolling lag-1 autocorrelation (early warning)")
axs[2].set_xlabel("coupling W(t)")
fig.tight_layout(); fig.savefig(OUT + "E4d_early_warning.png")

# ---------- E5: reflexivity: prediction->reaction map, fixed points ----------
def reaction(f, guarantee=0.0):
    # fraction withdrawing after hearing forecast f of depositor loss
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

print(f"E1 total-attention drift across 30 rounds (lethain systems): {e1_drift}")
print(f"E2 max |mass error| in graph transport: {e2_err:.2e}")
print(f"E2 biased node share: {tr_bias[-1,7]:.3f} vs free {tr_free[-1,7]:.3f} (uniform=1/40={1/40:.3f})")
print(f"E3 log-log slope of std(pop mean) vs K: {slope:.3f} (theory -0.5)")
print(f"E4 N_eff at W=0: {neff[0]:.1f}/64 ; at W=2.5: {neff[-1]:.2f}")
print(f"E4 skill horizon at W=0: {tau[0]:.2f} ; at W=2.5: {tau[-1]:.2f}")
print(f"E5 fixed points no guarantee: {np.round(fp0,3)} ; with guarantee: {np.round(fp1,3)}")
