# Can the Robbins Micro +100% month be reproduced on public data?

> Independent, frozen-spec replication of a 4-step MNQ orderflow system
> (HTF value → VA/fib discount → footprint confirmation → 1.5R execution).
> Status 2026-09-19: **REJECT as edge on public bars / HOLD as research program.**
> No financial advice. See `docs/DISCLOSURE.md` before any number below.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![SPEC: v1.0 frozen](https://img.shields.io/badge/SPEC-v1.0%20frozen-blue.svg)](docs/SPEC.md)
[![Performance: HYPOTHETICAL](https://img.shields.io/badge/performance-HYPOTHETICAL-red.svg)](docs/DISCLOSURE.md)
[![Gates: UNVERIFIED](https://img.shields.io/badge/gates-UNVERIFIED-red.svg)](docs/PUBLIC_REPORT.md)

![Stitched equity in R plus benchmark, WFA and cost-stress panels](assets/demo_preview.png)

## Table of Contents

- [Research question](#research-question)
- [Answer in 30 seconds](#answer-in-30-seconds)
- [The system under test](#the-system-under-test)
- [Data](#data)
- [Method](#method)
- [Results](#results)
- [Why REJECT edge / HOLD program](#why-reject-edge--hold-program)
- [What would change the verdict](#what-would-change-the-verdict)
- [Reproduce](#reproduce)
- [Demo video](#demo-video)
- [Files](#files)

## Research question

A discretionary futures trader won the Robbins Micro Day-Trading Championship with roughly +100% in July, trading MNQ orderflow in the first 90 minutes of New York. The public interview lays out a 4-step method. **Does that method survive point-in-time, cost-aware, benchmark-deflated testing on public bars — or does it fail like most retail systems?**

Source: IQCapital whiteboard interview (`PL7LKUsCgIQ`, 2026-08-11) + trader's own July video. Full citation trail in `docs/SOURCES.md`.

## Answer in 30 seconds

| Test | Result |
|---|---|
| Location engine on public 5m NQ, n=950 RTH bars | 78 hits → 40 participation-blocked → **n=22, PF net 2.39, win 59%, +0.47R, DD 4.0R** — isolated profit |
| Same bars vs field (fib-only, VA-only, random, buy-hold) | Creamer Sharpe 3.06 vs **buy-hold 4.64**; **DSR 0.62 (<0.95 FAIL), RC p 0.87 FAIL, SPA p 0.79 FAIL** |
| Purged walk-forward, 4 folds | PF **1.43 / inf (5-0) / 0.44 / 7.63** → 3/4 pass, 0 vetoes — stable procedure |
| Significance of the 22 filled trades | Per-trade Sharpe 0.39, t 1.81, **bootstrap 95% CI [−0.08, 1.08] includes 0** — insignificant |
| Shuffle Monte Carlo P=1.0 | **Degenerate** (totals invariant under permutation) — reported as pitfall demo, not evidence |

Reading: an isolated profit factor without deflation is the naive winner. Standard multiple-testing and snooping corrections reject it. Stability without significance = hold the program, not an edge.

## The system under test

Frozen in `docs/SPEC.md` v1.0 (append-only; any rule change creates v1.1, never edits v1.0):

1. **Environment (pre-open).** HTF value-up/down/sideways from 1H/4H POC+VA migration + naive-GEX regime (positive gamma = choppy, fade-only; negative gamma = volatile, momentum-OK) + call/put walls + flip zone.
2. **Location.** Below the Value Area (discount in value-up) + fib 705/788/886 zone **outside** VA + swing/sweep structure. Push through 886 without reclaim = INVALID, no trade.
3. **Confirmation (5-min footprint).** Seller aggression at the low (negative delta, POC at low, 400% ask imbalances) + NO downside result → bullish close → pullback fails HIGHER → bullish flip → ENTER. Anticipating without confirmation = bad loss by definition.
4. **Execution.** Stop beyond the second failure; targets swing highs / POC / VAH; trail buyer aggression; move to breakeven on VA-reclaim failure. Journal baseline: 1.5–2R, ~60–65% win, PF ~1.8 (single regime until reproduced).
5. **Filters.** ≥20k MNQ contracts per 5-min bar, first 90 min of New York only, 0–2 trades/day, stop after 2 losses, skip red news.

Key disagreements in the literature are frozen as choices, not hidden: VA 70% convention with fixed rows/session; walls as zones (they break and accelerate in negative gamma); 3-condition absorption (size 2× + cross-ratio + wick); transcript fibs 705/788/886; risk sized on drawdown-room not balance. See `docs/SPEC.md` §1–5.

## Data

| Layer | Source | Bars | Proves? |
|---|---|---|---|
| Synthetic pipeline | seeded generator (seed 7) | 60 | Detectors fire, n=1 — no edge claim |
| Daily proxy | yfinance `NQ=F` (fallback `QQQ`) | ~130 | Location + R arithmetic only |
| **Public intraday** | **yfinance `NQ=F` 5m 60d, RTH 09:30–11:00 ET, cached `data/cache/nq_f_5m_60d.csv`** | **950 bars / 50 sessions** | Location + participation + R math — **NOT absorption/GEX** |
| Real tape | Tradovate/CQG MNQ bid×ask + paid GEX chain | — | TODO — the only true footprint/GEX test (see `src/exp02_live.py`) |

Free public bars cannot prove footprint absorption or dealer GEX — those need CME Level-1 tape + paid options chain. Every run stamps its provenance and limits in `results/run-*.json`.

## Method

- **Fills:** next-open only, stop-first on same-bar SL+TP contact (pessimistic). No same-bar fantasy.
- **Costs:** MNQ $0.50/tick, 1-tick slip + $0.60/side base; report gross AND net; ×1.5/×2 sensitivity must stay PF>1.0 or FAIL.
- **Point-in-time:** developing POC/VAH/VAL stored at decision bar, never revised with future bars. RTH and ETH never mixed.
- **Benchmarks (same 950 bars, no cherry-pick):** Bailey–López de Prado DSR/PSR (4 trials), White Reality Check + Hansen SPA vs buy-hold (stationary bootstrap), 4-fold CSCV PBO-lite, purged rolling WFA (purge 2 / embargo 2, pre-committed PF>1.0 & E[R]>0 & n≥3 + catastrophic veto), stationary-bootstrap Sharpe CI, cost stress.
- **Promotion gates:** backtest→demo needs n≥100, PF>1.3 net, DD<15%, 2+ regimes, WFA OOS positive, PBO<0.5, DSR>0. Demo→micro: 30 trades/30 days within ±0.15R, adherence ≥85%. Micro→full: 60–100 trades/90 days within ±0.1R. (`docs/SPEC.md` §7.)

## Results

> Figures regenerated by `python3 src/make_visuals.py` from `results/run-*.json`. HYPOTHETICAL (CFTC 4.41).

![Stitched equity in R — n=22 PF 2.39](assets/equity_R.png)
![Creamer vs field Sharpe — DSR 0.62 FAIL](assets/benchmark_sharpe.png)
![Purged WFA 4 folds — 3/4 PASS but insignificant](assets/wfa_folds.png)
![Cost stress — PF stays >1.0 at ×2](assets/cost_stress.png)
![Runs index — verdict card](assets/runs_index.png)

Full tables: `docs/PAPER_RESULTS.md` (generated by `src/exp06_paper.py`), `docs/PUBLIC_REPORT.md`.

## Why REJECT edge / HOLD program

- The location engine runs and survives doubled costs — that is real, but it is the **naive winner**: any isolated backtest looks good before deflation.
- Against the field on identical bars it loses: buy-hold Sharpe 4.64 > creamer 3.06; DSR 0.62, RC/SPA p ~0.8 — consistent with luck.
- Walk-forward is stable (3/4 folds pass, no vetoes) but insignificant (t 1.81, CI crosses zero; fold-2 `inf` is a 5-0 small-sample luck print).
- Shuffle-MC P=1.0 is a textbook degenerate statistic (permutation-invariant totals) — disclosed as a pitfall, not claimed as evidence.
- n=22 << 100-trade gate; absorption + GEX untested without paid tape/chain.

So: **reject the edge claim on public bars; hold the program** pending real tape + chain + holdout.

## What would change the verdict

In order: 1m NQ 2022–26 + 2026 holdout with tick-aware fills → 25k Monte Carlo → purged rolling WFA majority-pass + veto → 30-day / 30-trade replay with adherence ≥85% → 90-day micro paper within ±0.1R and DD within 1.25×. Only then consider staged sizing. No shortcuts. (`docs/PUBLIC_REPORT.md` §Next gates.)

## Reproduce

```bash
pip install -r requirements.txt
python3 src/exp00_synthetic.py       # pipeline proof: loc/absorp/fail2 True, n=1
python3 src/exp01_historical.py      # daily proxy arithmetic
python3 src/exp02_live.py            # dry-run harness (0 trades claimed; tape TODO)
python3 src/exp03_improved.py        # raw vs filtered + cost x1.5/x2
python3 src/exp04_public_intraday.py # PUBLIC 5m NQ 60d RTH (cached, seed 7)
python3 src/exp05_benchmarks.py      # DSR/RC/SPA/PBO-lite vs buy-hold, same bars
python3 src/exp07_wfa_mc.py          # purged WFA + bootstrap + cost stress
python3 src/exp06_paper.py           # builds docs/PAPER_RESULTS.md
python3 src/make_visuals.py          # rebuilds assets/*.png
```

Seed 7 everywhere. Every run writes `results/run-*.json` with SPEC version, params, n, PF gross/net, expectancy/R, maxDD, costs, provenance, and filter-skip reasons.

## Demo video

60-second walkthrough storyboard: `assets/demo_walkthrough.html` (preview above). To publish: record it + the five commands above with OBS at 720p (<10 MB), upload to YouTube, and embed the thumbnail link here. Recording script and upload steps: `docs/DEMO_VIDEO.md`.

| Time | Command | On screen |
|---|---|---|
| 0:00 | `python3 src/exp00_synthetic.py` | loc/absorp/fail2 True, n=1 |
| 0:15 | `python3 src/exp04_public_intraday.py` | 78 hits → 40 blocked → n=22, PF 2.39 |
| 0:30 | `python3 src/exp05_benchmarks.py` | DSR 0.62 FAIL, RC 0.80 FAIL |
| 0:45 | `python3 src/exp07_wfa_mc.py` | 3/4 PASS, t 1.81, CI includes 0 |
| 1:00 | `python3 src/exp06_paper.py` | `docs/PAPER_RESULTS.md` |

## Files

```
docs/SPEC.md  — frozen strategy, filters, costs, gates (v1.0, append-only)
docs/SOURCES.md — every factual claim with URL + verification date
docs/DISCLOSURE.md — hypothetical-performance notice (read first)
docs/PUBLIC_REPORT.md — verdict table + next gates
docs/PAPER.md docs/PAPER_RESULTS.md docs/REPRODUCIBILITY.md docs/DEMO_VIDEO.md
src/indicators.py src/backtest.py src/overfit.py
src/exp00_synthetic.py src/exp01_historical.py src/exp02_live.py src/exp03_improved.py
src/exp04_public_intraday.py src/exp05_benchmarks.py src/exp07_wfa_mc.py src/exp06_paper.py
src/make_visuals.py
data/README.md data/cache/nq_f_5m_60d.csv
results/run-*.json (7 runs, seed 7)
assets/equity_R.png assets/benchmark_sharpe.png assets/wfa_folds.png assets/cost_stress.png assets/runs_index.png assets/demo_preview.png
```

Related (not duplicated): [kouljihate/OrderFlow](https://github.com/kouljihate/OrderFlow) dashboard — this repo verifies that class of system; it does not fork it.

Contributing: `CONTRIBUTING.md` (SPEC frozen; seed 7; gross+net; cost sensitivity; preserve negatives). License MIT + CFTC-4.41 notice. Cite via `CITATION.cff`.
