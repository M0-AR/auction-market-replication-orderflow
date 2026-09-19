"""exp05 — BENCHMARK field on the SAME public bars as exp04 (no cherry-pick).

Candidates (frozen, all on identical data/costs):
  1 creamer-proxy (VA + fib + bullish + participation proxy)
  2 fib-only (discount + 886, no VA/participation)
  3 va-only (outside VA + bullish, no fib)
  4 random (p=0.02/bar, seed 7 — the 'monkey' luck floor per sharpebench)
  5 buy-hold benchmark (per-bar close-to-close)
Standards (docs/SOURCES.md §K): Bailey-Lopez DSR/PSR/MinTRL, White RC (2000),
Hansen SPA studentized (SPA-type), CSCV-PBO, Romano-Wolf noted as TODO-full.
Field = strategies × bars; PBO input transposed (bars × strategies).
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
import numpy as np
from math import erf, sqrt, log

os.makedirs("results", exist_ok=True)
SEED = 7
rng = np.random.default_rng(SEED)

# ---- load same public bars as exp04 ----
import pandas as pd
bars = None
prov = ""
for p in ("data/cache/nq_f_5m_60d.csv", "data/cache/stooq_nq_f_daily.csv"):
    if os.path.exists(p):
        try:
            bars = pd.read_csv(p, index_col=0, parse_dates=True)
            prov = f"cache {p}, n={len(bars)}"
            break
        except Exception:
            pass
if bars is None:
    import yfinance as yf
    bars = yf.download("NQ=F", period="60d", interval="5m", progress=False, auto_adjust=True)
    prov = f"yfinance live NQ=F 5m, n={len(bars)}"
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
print("exp05 field on:", prov)

from indicators import volume_profile, fib_zone, in_discount, outside_value_area

LOOK = 30
names = ["creamer-proxy", "fib-only", "va-only", "random", "buy-hold"]
rets = np.zeros((len(names), N))  # per-bar simple returns scaled to risk unit ~ ATR
atr = np.maximum(H - L, np.abs(C - np.roll(C, 1)))
atr[0] = atr[1:].mean()
unit = atr  # 1R ≈ 1 ATR move

# buy-hold per-bar
rets[4, 1:] = (C[1:] - C[:-1]) / unit[1:]

rand_fire = rng.random(N) < 0.02
for i in range(LOOK, N - 1):
    c = C[i - LOOK:i]; v = V[i - LOOK:i]
    poc, vah, val = volume_profile(c, v)
    sw, sh = float(np.min(L[i - LOOK:i])), float(np.max(H[i - LOOK:i]))
    if sh <= sw:
        continue
    zone = fib_zone(sw, sh, "long")
    px = float(C[i])
    bull = C[i] > O[i]
    disc = in_discount(px, zone) and px > zone["l886"]
    out = outside_value_area(px, vah, val)
    hi_med = V[i] >= np.median(v)
    entry_next = (O[i + 1] - C[i]) / unit[i + 1]  # gap to next open in R-ish
    # next-bar directional payoff proxy in R units (honest: bar-path, not fills)
    move = (C[i + 1] - O[i + 1]) / unit[i + 1]
    if disc and out and bull and hi_med:
        rets[0, i + 1] = move  # creamer-proxy
    if disc and bull:
        rets[1, i + 1] = move  # fib-only
    if out and bull:
        rets[2, i + 1] = move  # va-only
    if rand_fire[i]:
        rets[3, i + 1] = move if rng.random() < 0.5 else -move * 0.8


def sharpe(x):
    x = np.asarray(x, float)
    return float(x.mean() / x.std() * sqrt(252 * 78)) if x.std() > 0 else 0.0  # 5m ~78/day


def moments(x):
    x = np.asarray(x, float)
    m, s = x.mean(), x.std()
    sk = float(((x - m) ** 3).mean() / s ** 3) if s > 0 else 0.0
    ku = float(((x - m) ** 4).mean() / s ** 4) if s > 0 else 3.0
    return m, s, sk, ku


def Phi_inv(p):
    from math import sqrt as sq
    # Acklam approximation
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00, 3.754408661907416e+00]
    pl, pu = 0.02425, 1 - 0.02425
    if p < pl:
        q = sq(-2 * log(p))
        return (((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)
    if p <= pu:
        q = p - 0.5; r = q * q
        return (((((a[0]*r+a[1])*r+a[2])*r+a[3])*r+a[4])*r+a[5])*q / (((((b[0]*r+b[1])*r+b[2])*r+b[3])*r+b[4])*r+1)
    q = sq(-2 * log(1 - p))
    return -(((((c[0]*q+c[1])*q+c[2])*q+c[3])*q+c[4])*q+c[5]) / ((((d[0]*q+d[1])*q+d[2])*q+d[3])*q+1)


def psr(sr_obs, T, sk, ku, sr0=0.0):
    # Bailey-Lopez PSR with non-normal correction
    if T < 2:
        return 0.0
    num = (sr_obs - sr0) * sqrt(T - 1)
    den = sqrt(max(1 - sk * sr_obs + (ku - 1) / 4 * sr_obs ** 2, 1e-9))
    z = num / den
    return 0.5 * (1 + erf(z / sqrt(2)))


SR = np.array([sharpe(r) for r in rets])
T = N
K = len(names) - 1  # candidates vs benchmark (exclude buy-hold from trial count? include: K=4 tried + winner)
Ntrials = 4
trials_std = float(np.std(SR[:4])) or 0.5
gamma = 0.5772156649
exp_max = trials_std * ((1 - gamma) * Phi_inv(1 - 1 / Ntrials) + gamma * Phi_inv(1 - 1 / (Ntrials * np.e))) if Ntrials > 1 else 0.0
w = names.index("creamer-proxy")
m, s, sk, ku = moments(rets[w])
dsr = psr(SR[w], T, sk, ku, sr0=exp_max)
psr0 = psr(SR[w], T, sk, ku, sr0=0.0)
# MinTRL for SR* at 95%: TRL = 1 + (1-sk*SR+((ku-1)/4)SR^2) * (Phi^-1(0.95)/SR)^2  (periods) — Bailey-Lopez
z95 = Phi_inv(0.95)
minTRL = None
if abs(SR[w]) > 1e-9:
    minTRL = float(1 + (1 - sk * SR[w] + (ku - 1) / 4 * SR[w] ** 2) * (z95 / SR[w]) ** 2)

# White RC-lite + Hansen SPA-type vs buy-hold: loss diff = strat - bench per bar
bench = rets[4]
B = 500
mean_block = 20
rc_p, spa_p = {}, {}
for j in range(4):
    f = rets[j] - bench
    t_obs_rc = sqrt(N) * f.mean()
    denom = f.std() or 1.0
    t_obs_spa = sqrt(N) * f.mean() / denom
    # stationary bootstrap: geometric block lengths
    p = 1.0 / mean_block
    cnt_rc = cnt_spa = 0
    for b in range(B):
        idxs = []
        while len(idxs) < N:
            start = rng.integers(0, N)
            Lblk = int(rng.geometric(p)) + 1
            idxs.extend([(start + k) % N for k in range(Lblk)])
        idxs = np.array(idxs[:N])
        fb = f[idxs] - f.mean()  # recenter under null (RC)
        t_rc = sqrt(N) * fb.mean()
        t_spa = sqrt(N) * fb.mean() / (fb.std() or 1.0)
        # max over single model = itself here; field-max handled below
        if t_rc >= t_obs_rc:
            cnt_rc += 1
        if t_spa >= t_obs_spa:
            cnt_spa += 1
    rc_p[names[j]] = round((cnt_rc + 1) / (B + 1), 4)
    spa_p[names[j]] = round((cnt_spa + 1) / (B + 1), 4)

# field-max RC (all 4 vs bench jointly): max t across candidates
f_all = np.stack([rets[j] - bench for j in range(4)])
t_max_obs = float(np.max(np.sqrt(N) * f_all.mean(axis=1)))
cnt = 0
for b in range(B):
    idxs = []
    while len(idxs) < N:
        start = rng.integers(0, N)
        Lblk = int(rng.geometric(p)) + 1
        idxs.extend([(start + k) % N for k in range(Lblk)])
    idxs = np.array(idxs[:N])
    fb = f_all[:, idxs] - f_all.mean(axis=1, keepdims=True)
    if float(np.max(np.sqrt(N) * fb.mean(axis=1))) >= t_max_obs:
        cnt += 1
rc_field_p = round((cnt + 1) / (B + 1), 4)

# PBO-lite: 4 folds, candidate-by-fold Sharpe, CSCV symmetric halves
F = 4
fold_len = N // F
perf = np.zeros((F, 4))
for f_ in range(F):
    seg = rets[:4, f_ * fold_len:(f_ + 1) * fold_len]
    for j in range(4):
        perf[f_, j] = sharpe(seg[j])
# all symmetric IS/OOS half-splits of folds (CSCV): choose 2 of 4 as IS
import itertools
below = tot = 0
for is_folds in itertools.combinations(range(F), F // 2):
    is_f = np.array(is_folds); oos_f = np.array([f_ for f_ in range(F) if f_ not in is_folds])
    is_mean = perf[is_f].mean(axis=0); oos_mean = perf[oos_f].mean(axis=0)
    winner = int(np.argmax(is_mean))
    if oos_mean[winner] < np.median(oos_mean):
        below += 1
    tot += 1
pbo_lite = round(below / tot, 3) if tot else 1.0

out = {"spec": "v1.0", "exp": "exp05", "provenance": prov, "seed": SEED,
       "sharpe_5m_ann": {names[j]: round(float(SR[j]), 3) for j in range(5)},
       "creamer": {"PSR_vs_0": round(psr0, 4), "DSR_trials4": round(dsr, 4),
                   "SR0_noise_ceiling": round(float(exp_max), 3), "MinTRL_periods": minTRL,
                   "skew": round(sk, 3), "kurt": round(ku, 3)},
       "RC_lite_p_vs_buyhold": rc_p, "SPAtype_p_vs_buyhold": spa_p,
       "RC_field_max_p": rc_field_p, "PBO_lite_4fold": pbo_lite,
       "LIMITS": "bar-path R proxy (not filled trades); B=500 demo bootstrap (use 5000 for paper); RW step-down TODO-full"}
print(json.dumps(out, indent=2))
with open("results/run-v1.0-exp05-benchmarks-seed7.json", "w") as f:
    json.dump(out, f, indent=2)
print("saved results/run-v1.0-exp05-benchmarks-seed7.json")
