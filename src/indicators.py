"""Indicators for SPEC v1.0 — volume profile, fib zones, GEX stub, footprint absorption.

All functions are point-in-time safe: they only look at bars up to index i (inclusive).
No future data. Deterministic. Tested by exp00.
"""
from __future__ import annotations
import numpy as np
import pandas as pd


def volume_profile(close: np.ndarray, volume: np.ndarray, n_bins: int = 24, va_pct: float = 0.70):
    """Return POC price, VAH, VAL from a lookback window (histogram method).

    Expands from max-volume bin outward adding larger neighbor first until va_pct enclosed.
    Mirrors vendor 70% convention (TradingView 70%, Ninja 68% — we freeze 70 per SPEC).
    """
    lo, hi = float(np.min(close)), float(np.max(close))
    if hi <= lo:
        return float(close[-1]), hi, lo
    edges = np.linspace(lo, hi, n_bins + 1)
    vols, _ = np.histogram(close, bins=edges, weights=volume)
    poc_bin = int(np.argmax(vols))
    poc = float((edges[poc_bin] + edges[poc_bin + 1]) / 2)
    total = float(vols.sum()) or 1.0
    lo_b, hi_b = poc_bin, poc_bin
    enclosed = float(vols[poc_bin])
    while enclosed / total < va_pct and (lo_b > 0 or hi_b < n_bins - 1):
        up = float(vols[hi_b + 1]) if hi_b + 1 < n_bins else -1.0
        dn = float(vols[lo_b - 1]) if lo_b - 1 >= 0 else -1.0
        if up >= dn and hi_b + 1 < n_bins:
            hi_b += 1
            enclosed += up
        elif lo_b - 1 >= 0:
            lo_b -= 1
            enclosed += dn
        else:
            break
    return poc, float(edges[hi_b + 1]), float(edges[lo_b])


def fib_zone(swing_low: float, swing_high: float, direction: str = "long"):
    """Return dict of retracement prices for SPEC levels 705/788/886 + 50% equilibrium.

    Long: drawn low->high, discount = below 50%. Short: mirror.
    """
    rng = swing_high - swing_low
    if direction == "long":
        return {
            "swing_low": swing_low, "swing_high": swing_high,
            "eq50": swing_high - 0.50 * rng,
            "l705": swing_high - 0.705 * rng,
            "l788": swing_high - 0.788 * rng,
            "l886": swing_high - 0.886 * rng,
        }
    rng2 = swing_low - swing_high  # not used; keep symmetric API
    return {
        "swing_low": swing_low, "swing_high": swing_high,
        "eq50": swing_high + 0.50 * abs(swing_low - swing_high),
        "l705": swing_high + 0.705 * abs(swing_low - swing_high),
        "l788": swing_high + 0.788 * abs(swing_low - swing_high),
        "l886": swing_high + 0.886 * abs(swing_low - swing_high),
    }


def in_discount(price: float, zone: dict, direction: str = "long") -> bool:
    if direction == "long":
        return price < zone["eq50"]
    return price > zone["eq50"]


def outside_value_area(price: float, vah: float, val: float, direction: str = "long") -> bool:
    if direction == "long":
        return price < val  # discount must be BELOW VA for longs
    return price > vah


def gex_regime_stub(net_gex: float | None, config_allow_unknown: bool = False) -> str:
    """Stub: + -> 'positive' (choppy filter), - -> 'negative' (allow), None -> 'unknown'.

    Live GEX needs paid chain (Tanuki/ZeroGEX/FlashAlpha). Stub keeps pipeline honest:
    unknown blocks signals unless config explicitly allows (logged).
    """
    if net_gex is None:
        return "allow-unknown" if config_allow_unknown else "blocked-unknown"
    return "positive" if net_gex >= 0 else "negative"


def detect_absorption(
    bid: float, ask: float, price_progress_ticks: float,
    per_level_avg: float, imbalance_ratio: float = 4.0,
    size_mult: float = 2.0, max_progress_ticks: float = 2.0,
) -> bool:
    """3-condition WyckFlow-style absorption (SPEC §3): size 2x + cross-ratio + stall.

    Long case: sellers aggressive (bid >> ask) but price stalls (progress ~0).
    imbalance_ratio default 4.0 matches Chris 400% bold highlight.
    """
    big_side, small_side = (bid, ask) if bid >= ask else (ask, bid)
    if big_side < size_mult * max(per_level_avg, 1.0):
        return False
    if small_side <= 0:
        cross = float("inf")
    else:
        cross = big_side / small_side
    if cross < imbalance_ratio:
        return False
    return abs(price_progress_ticks) <= max_progress_ticks


def bar_delta(bid_vols: np.ndarray, ask_vols: np.ndarray) -> float:
    return float(np.sum(ask_vols) - np.sum(bid_vols))


def second_failure_higher(first_low: float, second_low: float, direction: str = "long") -> bool:
    """Second seller push must fail HIGHER (less penetration) for longs."""
    if direction == "long":
        return second_low > first_low
    return second_low < first_low
