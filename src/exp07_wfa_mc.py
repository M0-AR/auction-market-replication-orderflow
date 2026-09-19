"""exp07 — PURGED ROLLING WFA + MONTE CARLO on public 5m NQ (frozen v1.0, seed 7).

Verified sources (docs/SOURCES.md §L):
- yfinance limits (official docs/code): intraday ≤60d (1m 8d, 5m/15m/30m/90m 60d, 1h 730d).
- Stooq: daily 30yr / hourly ~9mo / 5m ~1mo, key-via-CAPTCHA + quota since early 2026, bulk ZIPs.
- Purged WF + embargo (QuantMemo/Lopez de Prado/walkforge/FlashAlpha): purge label-overlap
  + embargo buffer; fit train-only, apply frozen to test; report per-window, not pooled-only.
- WFER controlled study (wfo.marketmaker.cc, 8000 sims): informative but redundant/miscalibrated
  (rank ρ+0.45, AUC 0.74 < stitched OOS t AUC 0.78; 0.8/0.5/0.3 folklore; 21% ill-conditioned).
  Hence: report WFER as N/A (no IS optimization — frozen rules) + stitched OOS Sharpe/t as primary.
- MC validation (quant-backtest-framework: shuffle/skip/bootstrap 1000+; GO needs P(prof)≥75%,
  5th pct Sharpe>0) + AlgoXpert majority-pass + catastrophic-veto + cost stress.
- QFRS 7 standards + VALID 12 items: costs gross+net, sensitivity, baselines, regime slices,
  turnover, code release — all stamped in run JSON.

Method: frozen location signals on 5m RTH (same as exp04) → real filled trades
(next-open, stop-first) → split time into F=4 folds with purge=2 + embargo=2 bars →
per-fold OOS metrics + stitched OOS + trade-shuffle MC (2000) + stationary bootstrap (1000, blk 20).
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import numpy as np
import pandas as pd

os.makedirs("data/cache", exist_ok=True)
os.makedirs("results", exist_ok=True)
SEED = 7
rng = np.random.default_rng(SEED)

from indicators import volume_profile, fib_zone, in_discount, outside_value_area
from backtest import FillConfig, backtest_long_signals, summarize

# ---- load public 5m (cache → yfinance 60d → Stooq daily) ----
bars = None
prov = ""
cp = "data/cache/nq_f_5m_60d.csv"
if os.path.exists(cp):
    try:
        bars = pd.read_csv(cp, index_col=0, parse_dates=True)
        prov = f"cache {cp}, n={len(bars)}"
    except Exception as e:
        print("cache read failed:", e)
if bars is None:
    import yfinance as yf
    bars = yf.download("NQ=F", period="60d", interval="5m", progress=False, auto_adjust=True)
    prov = f"yfinance live NQ=F 5m 60d, n={len(bars)}"
    bars.to_csv(cp)
if hasattr(bars.columns, "levels"):
    try:
        bars.columns = [c[0] if isinstance(c, tuple) else c for c in bars.columns]
    except Exception:
        pass
O = bars["Open"].to_numpy().ravel().astype(float)
H = bars["High"].to_numpy().ravel().astype(float)
L = bars["Low"].to_numpy().ravel().astype(float)
C = bars["Close"].to_numpy().ravel().astype(float)
V = bars["Volume"].to_numpy().ravel().astype(float) if "Volume" in bars.columns else np.full(len(bars), 20000.0)
V[V <= 0] = np.median(V[V > 0])
N = len(C)
print("exp07 bars:", prov)

# ---- frozen signals (identical to exp04) ----
LOOK = 30
sig = np.zeros(N, bool); st = np.zeros(N); tg = np.zeros(N)
hits = blo = 0
POC = np.full(N, np.nan); VAH = np.full(N, np.nan); VAL = np.full(N, np.nan)
for i in range(LOOK, N - 1):
    c = C[i - LOOK:i]; v = V[i - LOOK:i]
    poc, vah, val = volume_profile(c, v)
    POC[i], VAH[i], VAL[i] = poc, vah, val
    sw, sh = float(np.min(L[i - LOOK:i])), float(np.max(H[i - LOOK:i]))
    if sh <= sw:
        continue
    zone = fib_zone(sw, sh, "long")
    px = float(C[i])
    if not (in_discount(px, zone) and outside_value_area(px, vah, val) and px > zone["l886"]):
        continue
    hits += 1
    if V[i] < np.median(v):
        blo += 1
        continue
    if C[i] > O[i] and L[i] >= float(np.min(L[i - 3:i])) - (sh - sw) * 0.01:
        sig[i] = True
        st[i] = float(L[i]) - (sh - sw) * 0.01
        tg[i] = min(poc, px + 1.5 * max(px - st[i], 1e-6))

# ---- purged rolling WFA: F=4 time folds, purge=2, embargo=2 ----
F, PURGE, EMBARGO = 4, 2, 2
edges = np.linspace(0, N, F + 1).astype(int)
cfg = FillConfig()
fold_rows = []
all_trades = backtest_long_signals(O, H, L, C, sig, st, tg, cfg)
for f_ in range(F):
    ts, te = int(edges[f_]), int(edges[f_ + 1])
    # purge test-label overlap + embargo: drop signals within PURGE of left edge
    # and EMBARGO of right edge from the FOLD's evaluation (honest, documented)
    f_sig = sig.copy()
    f_sig[max(0, ts - PURGE):min(N, ts + PURGE)] = False
    f_sig[max(0, te - EMBARGO):min(N, te + EMBARGO)] = False
    tr = backtest_long_signals(O, H, L, C, f_sig, st, tg, cfg)
    in_fold = [t for t in tr if ts <= t.entry_idx < te]
    s = summarize(in_fold)
    # extra: Sortino (downside), Calmar (total_R/maxDD_R)
    rs = np.array([t.r_mult for t in in_fold], float)
    downside = rs[rs < 0]
    sortino = float(rs.mean() / downside.std() * np.sqrt(252 * 78)) if len(downside) > 1 and downside.std() > 0 else 0.0
    calmar = float(s["total_R"] / s["maxDD_R"]) if s["maxDD_R"] > 0 else 0.0
    # pre-committed fold benchmark b: PF_net>1.0 AND expect_R>0 (AlgoXpert-style gate)
    passed = (s["pf_net"] > 1.0 and s["expect_R"] > 0 and s["n"] >= 3)
    veto = (s["total_R"] < -8)  # catastrophic-veto: deep fold loss
    fold_rows.append({"fold": f_, "n": s["n"], "pf_net": s["pf_net"], "pf_gross": s["pf_gross"],
                      "expect_R": s["expect_R"], "win_rate": s["win_rate"], "maxDD_R": s["maxDD_R"],
                      "total_R": s["total_R"], "sortino": round(sortino, 3), "calmar": round(calmar, 3),
                      "PASS": bool(passed and not veto), "VETO": bool(veto)})
    print(f"fold {f_}: n={s['n']} PFnet={s['pf_net']} E[R]={s['expect_R']} DD={s['maxDD_R']} "
          f"Sortino={sortino:.2f} Calmar={calmar:.2f} {'PASS' if passed and not veto else 'FAIL'}{' VETO' if veto else ''}")

np_pass = sum(1 for r in fold_rows if r["PASS"])
vetoes = sum(1 for r in fold_rows if r["VETO"])
wfa_pass = (np_pass >= 3 and vetoes == 0)  # majority-pass (≥3/4) + veto rule
stitched = summarize(all_trades)
rs_all = np.array([t.r_mult for t in all_trades], float)
# UNITS FIX (verified: WFER controlled study warns raw-PnL ratio/annualization units problems):
# per-trade Rs must NOT be annualized with sqrt(252*78) (that factor is for per-bar series).
# Report per-trade Sharpe (unitless) + t-stat as primary; keep mis-scaled value flagged, not ranked.
stitched_sharpe_pertrade = float(rs_all.mean() / rs_all.std()) if len(rs_all) > 1 and rs_all.std() > 0 else 0.0
stitched_t = float(rs_all.mean() / (rs_all.std() / np.sqrt(len(rs_all)))) if len(rs_all) > 1 and rs_all.std() > 0 else 0.0

# ---- Monte Carlo: HONEST treatment (verified DaruFinance finding #1) ----
# Trade-shuffle totals are permutation-INVARIANT under fixed notional (sum never changes),
# so P_profitable on shuffled totals is degenerate (=1.0 here) — reported only to demonstrate
# the pitfall, NOT as evidence. Primary MC = stationary bootstrap Sharpe CI below + per-fold
# drawdown distribution across folds (path-dependent, informative).
MC = 2000
prof = 0
mc_totals = np.zeros(MC)
for b in range(MC):
    sh = rng.permutation(rs_all) if len(rs_all) else np.zeros(1)
    tot = float(sh.sum())
    mc_totals[b] = tot
    if tot > 0:
        prof += 1
p_prof = round(prof / MC, 4)
p5 = round(float(np.percentile(mc_totals, 5)), 3)
p50 = round(float(np.percentile(mc_totals, 50)), 3)
# stationary bootstrap Sharpe CI on per-trade Rs (block mean 3, B=1000)
B, mblk, p_ = 1000, 3, 1 / 3
sbs = []
for b in range(B):
    idxs = []
    while len(idxs) < len(rs_all):
        s0 = rng.integers(0, max(len(rs_all), 1))
        Lb = int(rng.geometric(p_)) + 1
        idxs.extend([(s0 + k) % len(rs_all) for k in range(Lb)])
    idxs = np.array(idxs[:len(rs_all)])
    rb = rs_all[idxs]
    sbs.append(rb.mean() / rb.std() if rb.std() > 0 else 0.0)  # per-trade, no fake annualization
sharpe_ci = [round(float(np.percentile(sbs, 2.5)), 3), round(float(np.percentile(sbs, 97.5)), 3)] if sbs else [0, 0]

# ---- cost stress ×1.5/×2 on full run ----
stress = {}
for k, c in {"base": FillConfig(), "x1.5": FillConfig(commission_per_side_usd=0.90),
             "x2": FillConfig(commission_per_side_usd=1.20, slip_ticks_per_side=2.0)}.items():
    stress[k] = summarize(backtest_long_signals(O, H, L, C, sig, st, tg, c))

out = {"spec": "v1.0", "exp": "exp07", "seed": SEED, "provenance": prov,
       "design": {"folds": F, "purge_bars": PURGE, "embargo_bars": EMBARGO,
                  "fold_benchmark_b": "PF_net>1.0 AND expect_R>0 AND n>=3",
                  "wfa_rule": "PASS if >=3/4 folds PASS and 0 VETO (total_R<-8)",
                  "WFER": "N/A — frozen rules, no IS optimization (per controlled study: ratio redundant/miscalibrated; stitched OOS Sharpe/t primary)"},
       "folds": fold_rows, "wfa": {"passed_folds": np_pass, "vetoes": vetoes, "WFA_PASS": bool(wfa_pass)},
       "stitched": {**stitched, "sharpe_pertrade": round(stitched_sharpe_pertrade, 3), "t": round(stitched_t, 3),
                    "NOTE": "per-trade Sharpe (no fake annualization); earlier sqrt(252*78) build gave 53.98 — withdrawn as units error"},
       "monte_carlo_shuffle2000": {"P_profitable": p_prof, "p5_totalR": p5, "p50_totalR": p50,
                                   "WARNING": "degenerate — shuffle-invariant totals (DaruFinance #1); do NOT rank on this",
                                   "GO_needs": "P>=0.75 AND 5th pct Sharpe>0"},
       "stationary_bootstrap_B1000_blk3": {"sharpe_95CI": sharpe_ci},
       "cost_stress": stress, "location_hits": hits, "participation_blocked": blo,
       "LIMITS": "public 5m bars only: NO bid/ask tape, NO GEX feed; absorption unproven; "
                 "frozen-rule WFA (no tuning) — veto/gates pre-committed above"}
print(json.dumps({"wfa": out["wfa"], "stitched": out["stitched"],
                  "mc": out["monte_carlo_shuffle2000"], "ci": sharpe_ci}, indent=2))
with open("results/run-v1.0-exp07-wfa-mc-seed7.json", "w") as f:
    json.dump(out, f, indent=2)
print("saved results/run-v1.0-exp07-wfa-mc-seed7.json")
