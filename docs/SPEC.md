# SPEC v1.0 — Chris Creamer Robbins Micro Day-Trading Championship Strategy (Frozen)

> Freeze date: 2026-09-19. Source: user-provided transcript of IQCapital interview
> "Trading WORLD CHAMPION Reveals the Orderflow Strategy That Won the Robbins Cup (Step-by-Step)"
> + DuckDuckGo fallback verification 2026-09-19 confirming video IDs PL7LKUsCgIQ, WwC-N2irZdE,
> ftJ9XuIaOXY, channel @thraxxtrades, and public rebuild kouljihate/OrderFlow.
> Any change to entry/exit/filter below creates v1.1 (new file, never edit in place).
> Status: HYPOTHETICAL candidate — NOT verified profitable. See `docs/DISCLOSURE.md`.

## 0. Identity

- Trader: Chris Creamer, 26, Micro Day Trading Championship, Robbins World Cup, July, +100% in one month.
- Style: intraday only, first 90 minutes of New York open (sometimes Asia). MNQ orderflow on 5-min.
- Higher timeframes: 1H / 4H for value-up / value-down / sideways. 15m context, 5m execution, 1m optional.
- Nothing here is financial advice. Educational replication only.

## 1. Environment (pre-open, never while price is sprinting)

1.1 Market structure (Auction Market Theory):
- Mark value creation: prior daily / cash-session profiles (e.g. Mon→Tue→Wed building higher).
- Classify: value-up (higher highs + higher lows, POC/VA migrating up), value-down (inverse), or sideways/balanced.
- Do NOT fight structure: in value-up, prefer longs in discount; do not short premium to call tops.

1.2 Gamma regime (naive GEX, Tanuki Trade web platform, NQ/QQQ/NDX):
- Positive gamma = dealers sell rips / buy dips → volatility dampening, failed breakouts common, choppy killer.
- Negative gamma = dealers buy rips / sell dips → volatility amplifier, bigger/faster moves, squeeze risk.
- Record before open: regime sign, call wall, put wall, gamma-flip zone (line in sand pos↔neg).
- GEX is a modeled estimate (long-call / short-put dealer convention), NOT observed inventory, NOT direction.
  Levels shift daily/intraday (0DTE turnover); stale levels are worse than none. After ~11:00 ET settled-OI
  GEX is stale — needs flow-GEX (verified via FlashAlpha/ZeroGEX docs Sept 2026).

## 2. Location (where to do business)

2.1 Value + discount/premium:
- Below Value Area = discount (want to buy in value-up). Above = premium (expensive, do not chase).
- Must be OUTSIDE value area. Fib inside VA = skip.

2.2 Fibonacci zone (swing low→swing high in value-up):
- Levels: 0.705 / 0.788 / 0.886 (golden-pocket extension; transcript says 705/788/886).
- Zone must overlap discount AND sit outside VA.
- Require internal structure: a swing point + preferably a sweep before entering discount.
- 0.886 is final line: if sellers push THROUGH 0.886 and dominance cannot shift back up → INVALID, no trade.

2.3 Inefficiency / low-volume node confluence (optional boost):
- Fast Asia/London push with little time/volume spent = inefficient, low-volume node.
- Open drives down out of VAL into discount = location set, do NOT sell there (selling the buy zone).

## 3. Confirmation (footprint 5-min: volume-profile candle + delta-profile candle)

Definitions (verified Sept 2026 via NexusFi/OrderFlowLabs/WyckFlow):
- Bid volume (left) = aggressive sellers hitting bid. Ask volume (right) = aggressive buyers lifting ask.
- Delta per level = ask − bid. Bar delta = sum. Negative = seller aggression.
- POC per candle = price with most contracts. Imbalance = one side ≥3× (Chris uses 400% bold highlight).
- Absorption = heavy aggression at extreme + NO result (price stalls). Does NOT mean auto-reversal.
- Right side fill = aggressive buyer; left side = aggressive seller (passive limit on ask filled by aggressor).

Required sequence (long example):
3.1 Candle pushes into discount, large lower wick, volume POC at low, delta deeply negative at low (sellers aggressive, no reward).
3.2 Candle closes bullish (dominance starts shifting).
3.3 Next candle opens, pulls back, sellers try again but fail HIGHER (second failure, less penetration).
3.4 Flip bullish + ask imbalances light up (buyers lifting offer aggressively) → ENTER on flip.
- Single bearish-close absorption alone is NOT entry. Must see shift + second failed push + flip.
- Anticipating ("we're in discount, must go up") without confirmation = BAD loss by definition.

## 4. Execution / invalidation / targets / management

4.1 Entry: on bullish flip after second seller failure in discount.
4.2 Stop: other side of failed sellers (below second-failure low). Invalid = sellers reclaim below first-failure extreme.
4.3 Targets (systematic): swing highs/lows first (market takes stops), NOT arbitrary R. Orders cluster at
    psychological/swing levels (Level 2). POC / VAH / call wall = trail points on the way.
4.4 Management with footprints (bid×ask + delta):
- Want: buyer aggression → price progression. Trail behind that aggression.
- Red flag: heavy buyer effort below VA with no re-entry into VA → move to breakeven / cut.
- First objective: reclaim back INTO value area. Fail to reclaim → BE/cut. Reclaim → hold toward POC/swing.
- Typical outcome per Chris: 1.5–2R (full TP sometimes 6R), win ~60–65%, profit factor ~1.8 (fluctuates).
  1.5R is the prop-firm math: $2k DD / $3k target on 50k = 1.5R.

## 5. Hard filters (untouched = no trade)

- F5.1 Participation: MNQ 5-min ≥20,000 contracts. Below = dying volume / lunch grind → SKIP.
- F5.2 Time: ~first 90 min NY open only. Beyond → quality collapses (own journal finding) → hard shutoff.
- F5.3 Frequency: 0–2 trades/day typical. 3 losses in a row ≈ never valid setups → stop after 2 losses.
- F5.4 News: skip if red news hits as price enters zone (edge case, discretionary but logged).
- F5.5 0.886 breach without reclaim = invalidation (see 2.2).

## 6. Costs / fills (frozen for backtest)

- Next-open fills only (no same-bar fantasy). Stop-first on same-bar SL+TP一起 (pessimistic).
- Costs per side: commission + spread + 1-tick slippage minimum (2–3 ticks for market orders / thin book).
- Report gross AND net. Sensitivity: +50–100% costs must stay PF>1.0 or FAIL.
- Point-in-time only: developing POC/VAH/VAL that moved after the fact must NOT be used (store decision-time value).

## 7. Promotion gates (from 2026 validation literature, frozen)

- Backtest→Demo: n≥100 (target 200–500), PF>1.3 net, expectancy>0, DD<15%, 2+ regimes, WFA OOS positive, PBO<0.5, DSR>0.
- Demo→Micro: ≥30 trades / 30 days, expectancy within ±0.15R of backtest, adherence ≥85%, signal divergence <5–10%.
- Micro→Full: ≥60–100 trades / 90 days, expectancy within ±0.1R, DD within 1.25× backtest, discipline held.
- Go = advance under limits. Hold = missing evidence. Reject = expectancy≤0 net, costs eat edge, or fills unavailable.
- Emergency pause: hard DD/loss limit, corrupted data, broker malfunction, regime event outside protocol.

## 8. What v1.0 does NOT claim

- No tick-level absorption proof on free data (needs CME bid/ask tape: Tradovate/CQG/Kinetick + ATAS/Sierra/NT8).
- No live GEX proof (needs paid CBOE/SPX chain or Tanuki/ZeroGEX/FlashAlpha feed; naive ≠ inferred).
- No 100% repeat (July competition = single regime, small-n; variance + trailing-DD math dominates prop outcomes).
- Personal-account 1% risk ≠ prop 1% of balance (prop risk is % of DD room, not balance).

## 9. Version log

- v1.0 2026-09-19: frozen from transcript + Sept-2026 source sweep. Next change → docs/SPEC-v1.1.md.
