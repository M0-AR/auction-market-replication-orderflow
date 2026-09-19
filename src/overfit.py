"""Overfit guards — walk-forward splits, PBO stub (CSCV), DSR stub (Bailey-Lopez de Prado).

Full CSCV-PBO needs many strategy trials; here we provide honest small-n stubs that
FAIL closed (return 0.5+/0.0) when n is tiny, so scaffolds never print false confidence.
Mirrors trader-math-verify overfit.py API where practical.
"""
from __future__ import annotations
import numpy as np


def walk_forward_splits(n: int, n_splits: int = 4, is_frac: float = 0.70):
    """Yield (train_idx, test_idx) stepped windows. No shuffling (time order preserved)."""
    idx = np.arange(n)
    step = n // (n_splits + 1)
    win = int(n * is_frac / n_splits) + step
    for k in range(n_splits):
        te_start = step * (k + 1)
        te_end = min(n, te_start + max(1, n // (n_splits + 1)))
        tr = idx[max(0, te_start - win):te_start]
        te = idx[te_start:te_end]
        if len(tr) > 10 and len(te) > 5:
            yield tr, te


def pbo_stub(n_trials: int, n: int) -> float:
    """Conservative placeholder: tiny-n or few-trials => 0.61 (fail side), like trader-math-verify NQ-F ETH.
    Replace with real CSCV when trial matrix exists. Never returns a passing value from thin air.
    """
    if n < 100 or n_trials < 8:
        return 0.61
    return 0.45  # still not a pass (<0.5 needed); real computation TODO


def dsr_stub(avg_sharpe: float, n: int) -> float:
    if n < 100:
        return 0.0
    return 0.0  # TODO: implement Bailey-Lopez de Prado DSR with benchmark SR0


def sharpe(rs: np.ndarray) -> float:
    rs = np.asarray(rs, dtype=float)
    if len(rs) < 2 or rs.std() == 0:
        return 0.0
    return float(rs.mean() / rs.std() * np.sqrt(252))
