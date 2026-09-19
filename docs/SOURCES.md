# SOURCES — every claim verified online Sept 2026 (one-at-a-time Exa + searxng + webfetch)

> Rule: no file in this repo may state a fact without a row here. Re-check dates are the fetch date.
> Exa `websearch` used first (one call at a time, no parallel), then `searxng_web_search`,
> then `webfetch` DuckDuckGo-lite fallback + GitHub direct. `agent-reach doctor` attempted
> 2026-09-19: CLI `agent-reach: command not found` — documented, fell back to the three above.

## A. Validation methodology (backtest → forward → live)

| Claim used in SPEC | Source | Published | Verified |
|---|---|---|---|
| 50–100+ backtest trades, PF>1.3, DD<15%, 15–20% forward tolerance, 50/75/100% staged sizing | TradeZella — Backtesting vs Forward Testing: When to Go Live (2026) https://www.tradezella.com/blog/backtesting-vs-forward-testing | 2026-06-19 | 2026-09-19 Exa |
| Walk-forward 70/30, OOS freeze, 30d demo + 90d micro, N≥100–200, param×30≤N | ForexMechanics — Backtesting and forward testing methodology https://forexmechanics.com/traders-workshop/backtesting-forward-testing/ | 2026-04-29 | 2026-09-19 Exa |
| Point-in-time, fill realism, costs, OOS, forward checklist | ChartMini — Backtesting Validation Checklist https://chartmini.com/blog/backtesting-trading-strategies-the-complete-guide-to-validating-your-edge-in-2026-2026 | 2026-01-08 | 2026-09-19 Exa |
| Frozen-spec protocol, go/hold/reject, 3-price reconciliation | Traderizz — How to Forward Test https://traderizz.com/guides/forward-testing-trading-strategy | 2026-08-16 | 2026-09-19 Exa |
| 2yr minute data, PF>1.5 start, 2wk+ paper, WFO, Monte Carlo, 200–500 trades | LuxAlgo — How to Validate Strategies Using Data https://www.luxalgo.com/blog/how-to-validate-trading-strategies-using-data/ | 2026-04-07 | 2026-09-19 Exa |
| 1000+ trades, 1-tick slip min, IS 70–80% + OOS, WFR>0.5, stop rules | TradingWyckoff — Complete Guide to Validate a Strategy [2026] https://tradingwyckoff.com/en/algorithmic-trading/validate-trading-strategy-guide/ | 2026-01-21 | 2026-09-19 Exa |
| PBO<0.5, WFOOS Sharpe≥0.8×IS, kill-switch, demotion rules | AIFinHub — Backtest to Paper to Live: Deployment Playbook https://aifinhub.io/articles/backtest-to-paper-to-live-playbook/ | 2026-04-22 | 2026-09-19 Exa |

## B. Auction Market Theory + Volume Profile

| Claim | Source | Published | Verified |
|---|---|---|---|
| AMT balance↔imbalance, VA 70%, POC magnet, VAH/VAL, 80% rule, open types | NexusFi Academy — Auction Market Theory https://nexusfi.com/a/market-structure/auction-market-theory | 2026-06-18 | 2026-09-19 Exa |
| Balance vs imbalance, TPO vs volume, HVN/LVN, IB, day types | WeMasterTrade — AMT + Market/Volume Profile Guide https://wemastertrade.com/market-profile-volume-profile-and-auction-market-theory-explained/ | 2026-04-13 | 2026-09-19 Exa |
| POC/VA/HVN/LVN anatomy, D/P/b shapes, naked POC | Oyamori — Volume Profile Trading https://oyamori.com/learning/volume-profile-trading/ | 2026-07-21 | 2026-09-19 Exa |
| POC magnet, VAH/VAL, HVN sticky / LVN fast, naked POC 2–3 ATR | Quantum-Algo — Volume Profile Guide 2026 https://www.quantum-algo.com/blog/guides/volume-profile-trading-complete-guide/ | 2026-04-20 | 2026-09-19 Exa |
| 70% Steidlmayer 1985/1986 origin, VA migration, 80% rule | NexusFi — Volume Profile Blueprint https://nexusfi.com/a/market-structure/volume-profile | 2026-06-01 | 2026-09-19 Exa |
| Freeze feed/session/range/rows/algorithm; POC≠fair-value by definition | TradersSecondBrain — Volume Profile Analysis https://traderssecondbrain.com/guides/volume-profile-analysis | 2026-05-11 | 2026-09-19 Exa |
| Failed auction = trapped breakout traders, low-vol cleanest | FinancialTechWiz — AMT Price Discovery (2026) https://www.financialtechwiz.com/post/auction-market-theory/ | 2026 | 2026-09-19 Exa |

## C. GEX / gamma walls / flip (naive vs inferred, Tanuki)

| Claim | Source | Published | Verified |
|---|---|---|---|
| GEX = dealer hedge proxy, +dampens / −amplifies, flip/walls/pinning | ZeroGEX — What Is GEX https://zerogex.io/education/what-is-gex-in-trading | 2026-07-07 | 2026-09-19 Exa |
| Walls = zones not barriers; flip = regime not signal; naive convention; stale intraday | InTheTalks — Misconceptions About GEX https://inthetalks.com/misconceptions-about-gamma-exposure-and-why-most-traders-get-gex-wrong/ | 2026-07-14 | 2026-09-19 Exa |
| Call/put wall mechanics, flip formula, unclenching acceleration | FlashAlpha — Call Wall, Put Wall & Gamma Flip https://flashalpha.com/articles/call-wall-put-wall-gamma-flip-options-levels-explained | 2026 | 2026-09-19 Exa |
| Settled vs flow-GEX, stale after 11–11:30AM, false flips | FlashAlpha — Complete Guide to Trading GEX https://flashalpha.com/articles/complete-guide-trading-gamma-exposure-gex | 2026-06-07 | 2026-09-19 Exa |
| Tape feel, OpEx pin/unpin, estimate-not-truth caveats | Nightglass — GEX: How Dealer Hedging Moves Market https://nightglass.trade/learn/gamma-exposure | 2026-07-22 | 2026-09-19 Exa |
| Zero-gamma 2–4% below spot, wall formula, 0DTE reshaped dynamics | ApexVol — GEX Explained https://apexvol.com/learn/gamma-exposure-explained | 2026-03-01 | 2026-09-19 Exa |
| Spot-shift curve, signed net vs total GEX, filter-not-signal | ZeroGEX — Complete Guide https://zerogex.io/education/gamma-exposure-explained | 2026-06-11 | 2026-09-19 Exa |
| Tanuki Trade = web GEX for TradingView, NETGEX/HVL/walls, 250+ symbols | TanukiTrade home http://tanukitrade.com/ | live | 2026-09-19 searxng |
| CBOE data expensive (~$300/mo claim in transcript), SPX-only, naive vs inferred | Transcript (Chris) + corroborated by GEX vendor docs above (convention + snapshot limits) | — | 2026-09-19 transcript |

## D. Footprint / orderflow (delta, absorption, imbalance 300–400%)

| Claim | Source | Published | Verified |
|---|---|---|---|
| Bid×ask cells, bar delta, 3:1 imbalance, absorption = passive beats aggressive, divergence entry | NexusFi — Footprint Charts https://nexusfi.com/a/platforms/footprint-charts | 2026-06-01 | 2026-09-19 Exa |
| 3:1+ imbalance, 800–1500 ES / 2000–4000 NQ absorption, stacked 3+, delta-div | FuturesHive — Footprint Complete Guide 2026 https://www.futureshive.com/blog/footprint-charts-complete-guide-2025 | 2025-01-16 | 2026-09-19 Exa |
| Support absorption bounce / buying-climax short / POC test | RevistaMIP/UTXO — How to Read Footprint https://www.revistamip.com/how-to-read-a-footprint-chart-for-futures-entries/ | 2026-07-01 | 2026-09-19 Exa |
| Bid×ask vs delta views, CVD limits, stacked = initiative, unfinished auction | OrderFlowLabs — Footprint Guide https://orderflowlabs.com/blogs/theblog/footprint-chart-guide | 2026-05-10 | 2026-09-19 Exa |
| Cluster 3k ES / 5k NQ, confluence 85% absorb+fail vs 48% single, 7-step checklist, lunch 30% | NexusFi — Advanced Footprint Patterns https://nexusfi.com/a/strategies/advanced-footprint-chart-patterns | 2026-06-07 | 2026-09-19 Exa |
| Diagonal read, 3-condition absorption (size 2× + cross-ratio + wick), unfinished magnet | WyckFlow — Footprint: Imbalance, Absorption https://wyckflow.com/blog/order-flow/footprint-imbalance-absorption-guide | 2026-06-11 | 2026-09-19 Exa |
| Exhaustion vs absorption, key-level-only, 50+ samples per setup | AlgoStorm — Footprint Charts https://algostorm.com/footprint-charts/ | 2025-01-30 | 2026-09-19 Exa |

## E. Fibonacci discount/premium + 705/786/886

| Claim | Source | Published | Verified |
|---|---|---|---|
| 50% equilibrium, discount=buy / premium=sell, FVG/OB confirmation, HTF bias | MJHuddleston.org — ICT Premium and Discount https://michaeljhuddleston.org/notes/ict-premium-and-discount-zones-trade-smarter-with-smart-money-precision/ | 2026-04-03 | 2026-09-19 Exa |
| Golden pocket 0.618–0.65 vs OTE 0.62–0.79 sweet 0.705, stop conventions | LiquidityScan — Golden Pocket vs OTE https://liquidityscan.io/blog/golden-pocket-vs-ote-zone-how-the-two-fib-bands-differ | 2026-07-15 | 2026-09-19 Exa |
| OTE 0.705 = post-stop-hunt entry, 55–65% w/ BOS+FVG/killzone, RR 1:3–1:8 | BackTrex — ICT Fibonacci and Golden Pocket https://backtrex.com/en/blog/ict-fibonacci-golden-pocket-ote-setup | 2026-07-21 | 2026-09-19 Exa |
| Premium/discount + PD arrays, OTE 62–79%, multi-TF alignment | ICTFlow — Premium and Discount Zones https://ictflow.com/blog/ict-premium-discount-zones | 2026-04-05 | 2026-09-19 Exa |
| OTE = golden pocket repurposed, anchor-to-sweep rule, fib-as-confluence | Oyamori — SMC/ICT & Fibonacci https://oyamori.com/learning/smc-vs-fibonacci/ | 2026-07-30 | 2026-09-19 Exa |
| ICT fib settings 0.5/0.618/0.65/0.705/0.786, extensions −0.27/−0.62/−1/−2/−2.5/−4 | BackTrex — ICT Fibonacci settings https://backtrex.com/en/blog/ict-fibonacci-settings-levels-complete-guide | 2026-09-14 | 2026-09-19 Exa |

## F. Prop math (1.5R / 60–65% / PF 1.8 / DD room)

| Claim | Source | Published | Verified |
|---|---|---|---|
| 6% pass rate, trailing-EOD sizing, 2–4wk paper, max-loss-streak sizing | FundedFast — How to Pass Prop Challenge https://fundedfast.com/learn/prop-trading/how-to-pass | 2026-06-16 | 2026-09-19 Exa |
| 1–2% of DD room (not balance), daily 25–30% of room, 3-strike rule | PropTradingVibes — Risk Management Framework (2026) https://proptradingvibes.com/blog/risk-management-prop-trading | 2026-03-22 | 2026-09-19 Exa |
| Expectancy, PF 1.5–2.5 pro, MAE stop calibration, Kelly-quarter | NexusIndicator — Prop Payout Math https://www.nexusindicator.com/blog-posts/prop-firm-payout-math-expectancy-drawdown.html | 2026-06-04 | 2026-09-19 Exa |
| R-multiples, expectancy, ruin table, 1.5–2R minimum | PropScorer — Risk Management for Futures https://www.propscorer.com/academy/risk-management-futures | 2026-03-12 | 2026-09-19 Exa |
| Monte Carlo pass/breach, target:floor geometry, risk↑ can lower pass% | Economicium — Prop Profit Target Calculator https://economicium.com/prop-firm-profit-target-calculator/ | 2026-07-30 | 2026-09-19 Exa |

## G. Chris Creamer identity + public rebuilds (webfetch DuckDuckGo-lite 2026-09-19)

| Claim | Source |
|---|---|
| Interview video (transcript source) | https://www.youtube.com/watch?v=PL7LKUsCgIQ (2026-08-11) |
| Chris own win video July 2026 Micro Day +100% | https://www.youtube.com/watch?v=WwC-N2irZdE (2026-08-30) |
| Rebuild-with-Claude video | https://www.youtube.com/watch?v=ftJ9XuIaOXY (2026-08-25) |
| Channel @thraxxtrades — orderflow futures, prop payouts | https://www.youtube.com/@thraxxtrades |
| Public Streamlit rebuild: Volume Profile + GEX + Fib 705/788/886 + journal + 20k filter + 2-loss shutoff + 1.5RR | https://github.com/kouljihate/OrderFlow (README fetched 2026-09-19) — Tradovate MNQ/NQ + sample-data fallback |
| Transcript mirror | https://youtube2text.diguardia.org/v/trading-world-champion-reveals-the-orderflow-strategy-that-won-the-robbins-cup-PL7LKUsCgIQ |

## H. Research-infra (searxng 2026-09-19)

| Claim | Source |
|---|---|
| backtrader high-perf fork, vectorbt/QSTrader institutional frames, tick→daily | https://github.com/cloudquant/backtrader; QuantStart python libs; LuxAlgo python-for-trading; arXiv 2608.11232 Backtrader-Bench |
| Workspace template mirrored | `/home/md/src/a-trading/trader-math-verify/` (QFRS, next_open, DSR/PBO, SPEC/DISCLOSURE/PUBLIC_REPORT/PAPER) |

## I. Explicitly UNCONFIRMED (do not cite as fact)

- Exact Robbins division name/month ("Micro Day Trading Championship, July") beyond transcript + Chris title — treat as transcript-claim until Robbins official standings linked.
- "$9 50k / $1 10k challenge" mid-roll ad pricing — ad copy, not strategy.
- Tanuki pricing/plan tiers — homepage fetched, no pricing scraped; do not quote.
- Any PF/win% universality (60–65% / 1.8 PF = Chris journal, single regime, small-n until reproduced).

## J. Public futures data ladder (Exa 2026-09-19 + searxng + webfetch-lite)

| Claim used (exp04) | Source | Published | Verified |
|---|---|---|---|
| Yahoo: daily + limited intraday (no ticks, shallow intraday) | MarketData Hub — Best Free Sources of Historical Market Data (2026) https://marketdata-hub.com/guide/best-free-historical-market-data-sources | 2026-06-22 (upd 2026-09-17) | 2026-09-19 Exa |
| yfinance broke after Yahoo Feb-2025 redesign; Stooq swap (decades daily, delayed 5m/60m, no key, `stooq.com/q/d/l/?s=NVDA.US&i=d`) | DeepCharts — Why did the yfinance library break? https://deepcharts.substack.com/p/why-did-the-yfinance-python-library | 2025-05-06 | 2026-09-19 Exa |
| Stooq NQ.F quote + free historical DB (daily/hourly/5-min archives) | https://stooq.com/q/?c=1m&s=nq.f ; https://stooq.com/q/d/?s=nq.f ; https://stooq.com/db/h/ | live (upd 2026-09-10) | 2026-09-19 Exa+searxng |
| Paid Level1 truth (tick trades+bid/ask, 47–448GB): Portara/CQG ENQ | Portara — Historical E Mini Nasdaq 100 Intraday https://portaracqg.com/futures/int/enq | 2022-12-03 (live) | 2026-09-19 Exa |
| NQ datasets: Prat617/nq-futures-stats (CME), Databento CME NQ catalog, Barchart NQ*0, BacktestMarket 5m, FirstRate 1m/5m, Kaggle TradingView NQ | webfetch-lite `free intraday futures data Stooq 5 minute NQ` 2026-09-19 (10 hits incl. github.com/Prat617/nq-futures-stats, databento.com/catalog/cme/GLBX.MDP3/futures/NQ, barchart NQ*0, backtestmarket 5m, firstratedata 1m/5m, kaggle NQ) | 2026-09-19 | webfetch |
| r/algotrading data thread (L1/L2/fundamental/options cost debate) | https://www.reddit.com/r/algotrading/comments/1et9k3v/where_do_you_get_your_data_for_backtesting_from/ | 2024-08-16 | 2026-09-19 searxng |

## K. Benchmarks: DSR/PBO/RC/SPA/WFA/MC (Exa 2026-09-19 + searxng)

| Claim used (exp05/exp06) | Source | Published | Verified |
|---|---|---|---|
| DSR corrects selection bias + non-normality (needs N, var-SR, T, skew, kurt); PSR; SR0 noise ceiling | Bailey–Lopez de Prado — The Deflated Sharpe Ratio https://davidhbailey.com/dhbpapers/deflated-sharpe.pdf | — | 2026-09-19 Exa |
| MinervaScore: DSR+PBO+SPA+MinTRL+regime → 0–100 + seal≥80; AUROC 0.989 synth, ρ=0.013 forward (honest null) | arXiv 2608.23808 https://arxiv.org/pdf/2608.23808 | 2026-08-26 | 2026-09-19 Exa |
| sharpebench: DSR/PSR + RC + SPA + Romano-Wolf + pass^k + monkey luck floor; rank by deflated edge | https://github.com/general-liquidity/sharpebench ; PyPI sharpebench 0.8.0 | live | 2026-09-19 Exa |
| Controlled: naive FDR 1.000 vs DSR 0.001 / HL-Bonf 0.057 / BHY 0.007 / RC 0.022; noise ceiling ann 1.63; correlated-grid effective-N band; pair DSR+RC | MarketMaker.cc — Deflated Sharpe https://marketmaker.cc/en/blog/post/deflated-sharpe-multiple-testing/ + repo suenot/deflated-sharpe-search + paper site | 2026-06-29 | 2026-09-19 Exa |
| LLM-discovery: 453-stock PT universe, all LLM strats rejected, benchmarks certified; leaky SR-35 oracle survives DSR+PBO (guardrails needed) | arXiv 2608.27734 | 2026-08-27 | 2026-09-19 Exa |
| White RC / Hansen SPA formulas, stationary bootstrap, studentization + consistent recentering | MetricGate — RC/SPA Calculator https://metricgate.com/docs/reality-check-superior-predictive-ability/ | 2026-06-10 | 2026-09-19 Exa |
| ResearchGate corroboration: DSR/RC/SPA/PBO papers | searxng `Deflated Sharpe Ratio PBO White Reality Check Hansen SPA` (DSR paper, RC paper, charlatanism/PBO paper) | 2026-09-19 | searxng |
| AlgoXpert IS–WFA–OOS (plateaus, purged rolling WFA, majority-pass + veto, lock θ*) | arXiv 2603.09219 | — | 2026-09-19 Exa |
| WFO window lengths; EMA-crypto case; block bootstrap; single-unseen-period rule | arXiv 2602.10785 | — | 2026-09-19 Exa |
| WFER signal (ρ+0.45, AUC 0.74) but redundant vs stitched OOS Sharpe (AUC 0.78); folk 0.8/0.5/0.3 miscalibrated; anchored↔rolling bet | MarketMaker.cc WFO validity https://wfo.marketmaker.cc/ | — | 2026-09-19 Exa |
| 6.6B MC perms: ROI/PF Sharpe permutation-invariant; MDD path-dependent but no forward lift | DaruFinance Monte-Carlo paper https://github.com/DaruFinance/Monte-Carlo-paper (SSRN 6636018, rev May 2026) | 2026-05 | 2026-09-19 Exa |
| Rigorous 34-fold WF, p=0.34 honest null, regime dependence, full math + OSS | arXiv 2512.12924 | — | 2026-09-19 Exa |
| WFO pipeline code (rolling/anchored, WFER≥0.5, MC bootstrap 5th%>0) | MarketMaker.cc — Walk-Forward Optimization https://marketmaker.cc/en/blog/post/walk-forward-optimization/ | 2026-03-15 | 2026-09-19 Exa |
| GO/NO-GO framework (WF→MC→CPCV/DSR→stress; Quantopian 888-strat warning) | yakub268/quant-backtest-framework (GitHub) | live | 2026-09-19 Exa |
| Dual-engine WF backtester (DSR/PSR/MinTRL/MinBTL, PBO/CSCV, Rust-verified 1e-3) | DaruFinance/quant-research-framework (GitHub, 2026-03-04) | 2026-03-04 | 2026-09-19 Exa |
| agent-reach sweep attempted 2026-09-19: `agent-reach: command not found` (both sweeps) — no social votes fabricated | local shell | 2026-09-19 | shell |

## L. Full-verification sweep v2 (Exa one-at-a-time + searxng + webfetch-lite 2026-09-19)

| Claim used | Source | Verified |
|---|---|---|
| yfinance: intraday ≤60d; 1m→8d, 2m/5m/15m/30m/90m→60d, 1h/60m→730d; tz-aware intraday | yfinance official reference + `history.py` source (ranaroussi.github.io/yfinance) | 2026-09-19 Exa |
| yfinance intraday history outage Feb-2026 (issue #2706, Yahoo-side, recovered) | github.com/ranaroussi/yfinance/issues/2706 | 2026-02-25 / 2026-09-19 Exa |
| Stooq: daily/hourly/5-min bulk ZIPs (world 184/245/452MB); Q API `i=d/w/m/q/y/60/5`, daily 30yr+, hourly ~9mo, 5m ~1mo; key-via-CAPTCHA + daily quota since early 2026 | stooq.com/db/h + api-evangelist/stooq OpenAPI + DeepCharts tutorial | 2026-09-19 Exa |
| WFER controlled (8000 sims): ρ+0.45/AUC 0.74 but < stitched OOS t (AUC 0.78); folk 0.8/0.5/0.3 miscalibrated; 21% ill-conditioned; rolling↔anchored bet; max ~9 folds | wfo.marketmaker.cc + suenot/wfo-validity repo | 2026-09-19 Exa |
| Purged WF + embargo mechanics (label overlap + feature lookback + buffer); walkforge PurgedWalkForward (1.39×→1.03× overfit); GEX 11-window public validation example | QuantMemo purged harness + neeljshah/walkforge + FlashAlpha GEX WF + MQL5 unified pipeline + ARIA WFO gates | 2026-09-19 Exa |
| GO/NO-GO stack (WF Sharpe≥1/WR≥45%/DD≥-15% → MC P≥75%/5th Sharpe>0 → CPCV/DSR → stress) | yakub268/quant-backtest-framework | 2026-09-19 Exa |
| QFRS 7 reviewer-enforceable standards (audit: 0/41 full compliance; backtest 12.2%) | Springer Artif Intell Rev 10.1007/s10462-026-11664-w (2026-08-08) | 2026-09-19 Exa |
| VALID 12-item checklist (median paper 2.5/12); CPCV/PBO, permutation≥100, costs+sensitivity, baselines, bear-regime, turnover, code | orcajae/valid-framework (GitHub) | 2026-09-19 Exa |
| Plutus reproducibility (one-command `plutus check`, manifest+results contract) | algotrade-plutus/plutus-guideline | 2026-09-19 Exa |
| Honest-null template: 34-fold WF, 0.55% ann, p=0.34 reported (publication-bias correction) | arXiv 2512.12924 | 2026-09-19 Exa |
| QuantBench industrial benchmark (unified data + market sim + quant metrics) | arXiv 2504.18600 | 2026-09-19 Exa |
| Voting: WF/purge/CPCV corroboration (TradingView, Hillsdale, vectorbt, susanpotter, QuantInsti, RiskLab, r/algotrading bursty-regime) | 2026-09-19 searxng `walk-forward purged embargo backtest overfitting validation` | searxng |
| Voting: QFRS Springer + Brunel PDF + checklist tools (nexural, tradingstrategy.ai, FIN510 lab10 CSCV→PBO/PSR/DSR, Bailey PBO paper, validraft) | 2026-09-19 webfetch-lite `QFRS reporting standards VALID checklist` | webfetch |
| agent-reach v2 sweep: `command not found` again — documented, no fabrication | local shell 2026-09-19 | shell |
