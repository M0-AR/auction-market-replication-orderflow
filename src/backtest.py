"""Backtest core — next_open fills, stop-first, R-multiples, contract-correct costs.

Pessimistic and point-in-time: signals computed on bar i execute at open[i+1].
If stop and target both touched in one bar, stop wins (stop-first).
"""
from __future__ import annotations
import json
from dataclasses import dataclass, asdict
import numpy as np


@dataclass
class FillConfig:
    tick_value_usd: float = 0.50      # MNQ $0.50/tick
    slip_ticks_per_side: float = 1.0
    commission_per_side_usd: float = 0.60
    spread_ticks_per_side: float = 0.0

    def cost_per_side(self) -> float:
        return (self.slip_ticks_per_side + self.spread_ticks_per_side) * self.tick_value_usd \
            + self.commission_per_side_usd

    def round_turn(self) -> float:
        return 2.0 * self.cost_per_side()


@dataclass
class Trade:
    entry_idx: int
    entry_price: float
    stop_price: float
    target_price: float
    direction: str  # long only in v1.0
    exit_idx: int = -1
    exit_price: float = 0.0
    exit_reason: str = ""
    r_mult: float = 0.0
    pnl_net: float = 0.0


def backtest_long_signals(opens, highs, lows, closes, signals, stops, targets, cfg: FillConfig):
    """Run long-only next-open backtest. signals[i]=True means enter at open[i+1]."""
    trades: list[Trade] = []
    n = len(closes)
    for i in range(n - 1):
        if not signals[i]:
            continue
        entry = float(opens[i + 1])
        stop = float(stops[i])
        tgt = float(targets[i])
        risk_pts = entry - stop
        if risk_pts <= 0:
            continue
        exit_price, exit_idx, reason = entry, i + 1, "eod"
        for j in range(i + 1, n):
            hit_stop = lows[j] <= stop
            hit_tgt = highs[j] >= tgt
            if hit_stop and hit_tgt:
                exit_price, exit_idx, reason = stop, j, "stop-first"
                break
            if hit_stop:
                exit_price, exit_idx, reason = stop, j, "stop"
                break
            if hit_tgt:
                exit_price, exit_idx, reason = tgt, j, "target"
                break
        gross_pts = exit_price - entry
        r = gross_pts / risk_pts
        pnl_net = gross_pts / 0.25 * cfg.tick_value_usd - cfg.round_turn()  # MNQ 0.25 tick
        trades.append(Trade(i + 1, entry, stop, tgt, "long", exit_idx, exit_price, reason, r, pnl_net))
    return trades


def summarize(trades: list[Trade]) -> dict:
    if not trades:
        return {"n": 0, "pf_gross": 0.0, "pf_net": 0.0, "win_rate": 0.0,
                "expect_R": 0.0, "maxDD_R": 0.0, "total_R": 0.0, "total_net": 0.0}
    rs = np.array([t.r_mult for t in trades])
    wins = rs[rs > 0].sum()
    losses = -rs[rs <= 0].sum()
    pf = float(wins / losses) if losses > 0 else float("inf")
    nets = np.array([t.pnl_net for t in trades])
    wins_n = nets[nets > 0].sum()
    loss_n = -nets[nets <= 0].sum()
    pf_net = float(wins_n / loss_n) if loss_n > 0 else float("inf")
    eq = np.cumsum(rs)
    maxdd = float(np.max(np.maximum.accumulate(eq) - eq)) if len(eq) else 0.0
    return {"n": len(trades), "pf_gross": round(pf, 3), "pf_net": round(float(pf_net), 3),
            "win_rate": round(float((rs > 0).mean()), 3), "expect_R": round(float(rs.mean()), 3),
            "maxDD_R": round(maxdd, 3), "total_R": round(float(rs.sum()), 3),
            "total_net": round(float(nets.sum()), 2)}


def save_run(path: str, payload: dict):
    with open(path, "w") as f:
        json.dump(payload, f, indent=2)
