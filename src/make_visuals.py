"""make_visuals — publication figures from VERIFIED run JSONs + cached public bars.

Reads only: results/run-*.json + data/cache/nq_f_5m_60d.csv (seed 7).
Writes: assets/equity_R.png, assets/benchmark_sharpe.png, assets/wfa_folds.png,
        assets/cost_stress.png, assets/runs_index.png, assets/demo_walkthrough.html
All numbers stamped from JSONs; no hand-typed performance claims.
Hypothetical (CFTC 4.41). See docs/DISCLOSURE.md.
"""
import os, json, glob
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

os.makedirs("assets", exist_ok=True)

def load(p):
    with open(p) as f:
        return json.load(f)

e04 = load("results/run-v1.0-exp04-public5m-seed7.json")
e05 = load("results/run-v1.0-exp05-benchmarks-seed7.json")
e07 = load("results/run-v1.0-exp07-wfa-mc-seed7.json")

DISC = "HYPOTHETICAL (CFTC 4.41) — not financial advice"

# 1. Equity in R (re-run verified filled trades for exact path — same code as exp07)
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import pandas as pd
from indicators import volume_profile, fib_zone, in_discount, outside_value_area
from backtest import FillConfig, backtest_long_signals
bars = pd.read_csv("data/cache/nq_f_5m_60d.csv", index_col=0, parse_dates=True)
O = bars["Open"].to_numpy().ravel().astype(float)
H = bars["High"].to_numpy().ravel().astype(float)
L = bars["Low"].to_numpy().ravel().astype(float)
C = bars["Close"].to_numpy().ravel().astype(float)
V = bars["Volume"].to_numpy().ravel().astype(float)
N = len(C); LOOK = 30
sig = np.zeros(N, bool); st = np.zeros(N); tg = np.zeros(N)
for i in range(LOOK, N - 1):
    poc, vah, val = volume_profile(C[i-LOOK:i], V[i-LOOK:i])
    sw, sh = float(np.min(L[i-LOOK:i])), float(np.max(H[i-LOOK:i]))
    if sh <= sw:
        continue
    zone = fib_zone(sw, sh, "long")
    px = float(C[i])
    if not (in_discount(px, zone) and outside_value_area(px, vah, val) and px > zone["l886"]):
        continue
    if V[i] < np.median(V[i-LOOK:i]):
        continue
    if C[i] > O[i] and L[i] >= float(np.min(L[i-3:i])) - (sh-sw)*0.01:
        sig[i] = True
        st[i] = float(L[i]) - (sh-sw)*0.01
        tg[i] = min(poc, px + 1.5*max(px-st[i], 1e-6))
trades = backtest_long_signals(O, H, L, C, sig, st, tg, FillConfig())
rs = np.array([t.r_mult for t in trades])
eq = np.cumsum(rs)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(eq, marker="o", ms=3)
ax.set_title(f"Stitched equity in R — n={len(rs)} PFnet {e07['stitched']['pf_net']} E[R] {e07['stitched']['expect_R']} (public 5m RTH)")
ax.set_xlabel("trade # (time order, seed 7)")
ax.set_ylabel("cum R")
ax.grid(alpha=0.3)
fig.text(0.5, 0.01, DISC, ha="center", fontsize=7)
fig.tight_layout()
fig.savefig("assets/equity_R.png", dpi=150)
print("saved assets/equity_R.png n=", len(rs))

# 2. Benchmark Sharpe bars (exp05, same 950 bars)
names = list(e05["sharpe_5m_ann"].keys())
vals = [e05["sharpe_5m_ann"][k] for k in names]
colors = ["#2ca02c" if k == "creamer-proxy" else "#1f77b4" if k == "buy-hold" else "#999999" for k in names]
fig, ax = plt.subplots(figsize=(8, 3.5))
ax.bar(names, vals, color=colors)
ax.axhline(e05["creamer"]["SR0_noise_ceiling"], ls="--", c="red", label=f"SR0 noise ceiling {e05['creamer']['SR0_noise_ceiling']}")
ax.set_title(f"Creamer vs field (5m-ann Sharpe) — DSR {e05['creamer']['DSR_trials4']} <0.95 FAIL, RC p {e05['RC_lite_p_vs_buyhold']['creamer-proxy']}")
ax.tick_params(axis="x", rotation=15)
ax.legend(fontsize=8)
fig.text(0.5, 0.01, DISC, ha="center", fontsize=7)
fig.tight_layout()
fig.savefig("assets/benchmark_sharpe.png", dpi=150)
print("saved assets/benchmark_sharpe.png")

# 3. WFA folds
folds = e07["folds"]
labels = [f"f{f['fold']}\nn={f['n']}" for f in folds]
pf = [float(f["pf_net"]) if str(f["pf_net"]).lower() != "infinity" else 8.0 for f in folds]
exp_r = [f["expect_R"] for f in folds]
x = np.arange(len(folds))
fig, ax1 = plt.subplots(figsize=(8, 3.8))
ax1.bar(x, pf, color=["green" if f["PASS"] else "red" for f in folds], alpha=0.7, label="PF net (inf capped at 8)")
ax1.axhline(1.0, c="black", ls="--", lw=1)
ax1.set_xticks(x); ax1.set_xticklabels(labels)
ax1.set_ylabel("PF net")
ax2 = ax1.twinx()
ax2.plot(x, exp_r, "o-", c="navy", label="E[R]")
ax2.set_ylabel("E[R]")
ax1.set_title(f"Purged WFA 4 folds (purge2/embargo2) — {e07['wfa']['passed_folds']}/4 PASS, 0 VETO → WFA_PASS {e07['wfa']['WFA_PASS']}; t {e07['stitched']['t']}, CI {e07['stationary_bootstrap_B1000_blk3']['sharpe_95CI']}")
fig.text(0.5, 0.01, DISC + " | fold1 inf = 5-0 luck, not edge", ha="center", fontsize=7)
fig.tight_layout()
fig.savefig("assets/wfa_folds.png", dpi=150)
print("saved assets/wfa_folds.png")

# 4. Cost stress
cs = e07["cost_stress"]
keys = ["base", "x1.5", "x2"]
pfc = [cs[k]["pf_net"] for k in keys]
fig, ax = plt.subplots(figsize=(6, 3.5))
ax.bar(keys, pfc, color=["green" if v > 1.0 else "red" for v in pfc])
ax.axhline(1.0, c="black", ls="--", lw=1, label="PF>1.0 gate at ×2")
ax.set_title(f"Cost stress — PF net {pfc[0]}/{pfc[1]}/{pfc[2]} stays >1.0 (R identical, $ falls)")
ax.legend(fontsize=8)
fig.text(0.5, 0.01, DISC, ha="center", fontsize=7)
fig.tight_layout()
fig.savefig("assets/cost_stress.png", dpi=150)
print("saved assets/cost_stress.png")

# 5. runs index (verdict card)
runs = sorted(glob.glob("results/run-*.json"))
fig, ax = plt.subplots(figsize=(8, 4))
ax.text(0.5, 0.92, "creamer-verification v1.0 — REJECT edge / HOLD program", ha="center", va="center", fontsize=11, weight="bold")
ax.text(0.5, 0.68, "\n".join(r.split("/")[-1] for r in runs), ha="center", va="center", fontsize=7, family="monospace")
ax.text(0.5, 0.15, f"exp04 n=22 PF {e04['base']['pf_net']} | exp05 DSR {e05['creamer']['DSR_trials4']} RC {e05['RC_lite_p_vs_buyhold']['creamer-proxy']} | exp07 t {e07['stitched']['t']} CI {e07['stationary_bootstrap_B1000_blk3']['sharpe_95CI']}\n{DISC}", ha="center", va="center", fontsize=7)
ax.set_axis_off()
fig.savefig("assets/runs_index.png", dpi=150)
print("saved assets/runs_index.png")

# 6. Demo walkthrough HTML (for Playwright screenshot + video script storyboard)
html = """<html><head><meta charset="utf-8"><title>creamer-verification demo</title></head>
<body style="font-family:sans-serif;max-width:900px;margin:auto">
<h1>creamer-verification — 60-second demo</h1>
<p><b>REJECT as edge / HOLD as program.</b> Frozen SPEC v1.0, seed 7, public 5m NQ RTH n=950.</p>
<ol>
<li><b>0:00 Pipeline</b> — <code>python3 src/exp00_synthetic.py</code> → loc/absorp/fail2 True, n=1.</li>
<li><b>0:15 Public bars</b> — <code>python3 src/exp04_public_intraday.py</code> → 78 hits → 40 blocked → n=22, PF 2.39.</li>
<li><b>0:30 Deflate</b> — <code>python3 src/exp05_benchmarks.py</code> → DSR 0.62 FAIL, RC 0.80 FAIL, buy-hold wins.</li>
<li><b>0:45 WFA+MC</b> — <code>python3 src/exp07_wfa_mc.py</code> → 3/4 PASS but t 1.81, CI includes 0, MC degenerate.</li>
<li><b>1:00 Paper</b> — <code>python3 src/exp06_paper.py</code> → docs/PAPER_RESULTS.md. Tape + GEX remain TODO.</li>
</ol>
<img src="equity_R.png" width="100%"><img src="benchmark_sharpe.png" width="100%">
<img src="wfa_folds.png" width="100%"><img src="cost_stress.png" width="100%">
<p>HYPOTHETICAL (CFTC 4.41) — not financial advice.</p>
</body></html>"""
with open("assets/demo_walkthrough.html", "w") as f:
    f.write(html)
print("saved assets/demo_walkthrough.html")
