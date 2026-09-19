"""exp00 — synthetic auction pipeline proof (seed 7). No edge claim.

Builds: value-up drift -> Asia/London inefficient push -> NY drive below VAL into
fib discount -> absorption (bid 4x ask, no progress) -> bullish close -> 2nd fail
higher -> flip long. Verifies detectors fire and backtest records exactly 1 trade.
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from indicators import volume_profile, fib_zone, in_discount, outside_value_area, detect_absorption, second_failure_higher
from backtest import FillConfig, backtest_long_signals, summarize, save_run

rng = np.random.default_rng(7)
N = 60
base = 18000.0
drift = np.arange(N) * 2.0  # guaranteed value-up
noise = rng.normal(0, 1.5, N)
closes = base + drift + np.cumsum(noise) * 0.3
opens = np.roll(closes, 1); opens[0] = base
highs = np.maximum(opens, closes) + np.abs(rng.normal(0, 1.5, N)) + 1.0
lows = np.minimum(opens, closes) - np.abs(rng.normal(0, 1.5, N)) - 1.0
vols = np.full(N, 22000.0)  # above 20k filter

# Profile first, then anchor swing so fib discount sits BELOW VAL (SPEC geometry):
# sw = VAL-60, sh = VAH+40 guarantees tgt=(705+788)/2 is discount + outside VA + above 886.
poc0, vah0, val0 = volume_profile(closes[:45], vols[:45])
sw, sh = float(val0 - 60.0), float(vah0 + 40.0)
zone = fib_zone(sw, sh, "long")
poc, vah, val = poc0, vah0, val0

# Force bar45-46 to sit in discount below VAL and above 886
tgt = (zone["l705"] + zone["l788"]) / 2
shift = tgt - closes[45]
closes[45:47] += shift
lows[45:47] = np.minimum(lows[45:47] + shift, closes[45:47] - 1.0)
highs[45:47] = np.maximum(highs[45:47] + shift, closes[45:47] + 6.0)
opens[46] = closes[45] - 2.0
closes[46] = closes[45] + 4.0  # bullish close after absorption

px = float(closes[46])
loc_ok = in_discount(px, zone) and outside_value_area(px, vah, val) and px > zone["l886"]
absorp = detect_absorption(bid=8000, ask=1500, price_progress_ticks=1.0, per_level_avg=2000.0)
fail2 = second_failure_higher(first_low=float(lows[45]), second_low=float(lows[45]) + 1.5)

signals = np.zeros(N, bool)
stops = np.zeros(N)
targets = np.zeros(N)
if loc_ok and absorp and fail2:
    signals[46] = True
    stops[46] = float(lows[45]) - 2.0
    targets[46] = poc  # first objective: reclaim toward POC/VA
    # ensure target reachable next bars
    highs[47:50] = np.maximum(highs[47:50], poc + 1.0)

cfg = FillConfig()
trades = backtest_long_signals(opens, highs, lows, closes, signals, stops, targets, cfg)
stats = summarize(trades)
print("exp00 synthetic:", {"loc_ok": loc_ok, "absorp": absorp, "fail2": fail2, **stats})
assert loc_ok and absorp and fail2, "pipeline must fire on synthetic setup"
assert stats["n"] == 1, "must record exactly 1 trade"
os.makedirs("results", exist_ok=True)
save_run("results/run-v1.0-exp00-synthetic-seed7.json",
         {"spec": "v1.0", "exp": "exp00", "seed": 7, "checks": {"loc_ok": True}, **stats})
print("saved results/run-v1.0-exp00-synthetic-seed7.json")
