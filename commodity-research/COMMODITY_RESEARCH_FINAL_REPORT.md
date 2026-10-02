# Commodity Research — Final Report (implementation stage)

> Date: 2026-10-02. Code: `../commodity/` (run instructions in `commodity/README.md`). Reports: `commodity/reports/output/`.
> **Read first:** every market-data host (CME, CFTC, EIA, FRED, MCX, LME, LBMA, Yahoo, Stooq) is unreachable from the
> build environment, and paid data needs your approval. **No strategy has been tested on real market data.** All
> results below are *engineering validation* on synthetic markets with known properties. They show the system works
> and that its statistics accept true effects and reject noise. They say **nothing** about real commodity markets.

## 1. Executive summary
- **Built:** the full pipeline from §A–AN of the master prompt, apart from what needs real data.
  - PostgreSQL schema with provenance.
  - Ingestion adapters: MCX bhavcopy, vendor/DataMine CSV, CFTC, FRED, EIA.
  - Contract calendars and a roll engine with 6 rules.
  - Research and tradable series; curve engine; feature engine.
  - 14 automated validation tests.
  - 27 pre-registered hypotheses.
  - Research runner: TRAIN → VALIDATION → walk-forward → single OOS.
  - Robustness battery; multiple-testing controls.
  - Portfolio construction; MCX implementation analysis; paper trading; 12 reports.
  - CLI and a pytest suite (25 tests).
- **Machinery verified on synthetic data:**
  - No-edge worlds (seeds 7 and 21, 31 years, 5 markets): **no hypothesis accepted**.
  - Planted-carry world: the carry hypothesis **detected** (deflated-Sharpe p 0.003, sign-flip p 0.005, passes FDR, OOS Sharpe 1.14). Unrelated families rejected.
- **Bugs found and fixed by these runs:**
  1. Convexity drift in the synthetic null.
  2. Near-zero synthetic prices that the validation tests had missed (an extreme-move test was added).
  3. An unstable risk-parity solver.
  4. A circular-shift permutation test that is invalid for persistent signals. It caused a true Sharpe-1 carry effect to be missed; replaced by a block sign-flip test.
  5. Deflated Sharpe using raw rather than effective trials.
- **Status of real research:** blocked on data access. Every hypothesis is `NOT TESTED (DATA-BLOCKED)` on real markets.

## 2. Data architecture (implemented)
- **Schema:** `commodity/database/schema.sql`, built on the 03 design and your table list.
  - commodities, contract_specs (versioned), contracts, contract_calendar, exchange_calendar.
  - raw → daily_contract_prices / daily_contract_volume_oi.
  - roll_rules, roll_events, research_series, tradable_series, curve_data, curve_features.
  - fundamental / positioning / macro / fx / rates.
  - strategy_definitions / signals, backtest_runs / trades / metrics, data_quality, source_registry, paper_*, audit_log.
- **Provenance:** every table carries source, download_ts, version, data_ts, processed_ts and quality_status.
- **Re-runs:** loads use COPY plus `ON CONFLICT`, so they are idempotent.
- **Source of truth:** individual contracts. Continuous series are derived.
  - Ratio, Panama and unadjusted views are generated dynamically.
  - Tradable returns and constant-maturity points are stored, versioned by roll rule.
  - Research series and the P&L series are separate code paths.

## 3. Data quality
- **Validation tests T1–T14** (`validation/checks.py`) return PASS / FAIL / OPEN as JSON/CSV plus the `data_quality` table.
- **Synthetic runs:** 65 PASS, 5 OPEN, 0 FAIL in each run.
  - The OPENs are T3 cross-source settlement checks; that needs a second source.
- **Self-tests:** injected defects are all caught (T1, T2, T3, T4, T5, T8). A deliberately leaky feature fails T14.
- **Real data:** not yet ingested. The acceptance tests in 17 §7 still apply.

## 4. Commodity characteristics
Not measurable without data. Driver → feature → data-status matrix: `18_COMMODITY_MODULE_SPECS.md`.

## 5. Term structure
- **Engine output:** F1–F3, constant-maturity 30/60/90/180/365-day prices, carry, CM slope and curvature, seasonal-neutral 12-month carry.
- **Report 03:** roll-rule comparison per commodity, splitting return into price return (CM30), roll return, roll cost and turnover.
- **Synthetic finding (engineering):** ROLL_F (carry-aware) roughly halves rolls and roll costs. GC: 2.6 vs 6.0 rolls a year.
- **Real findings:** pending data.

## 6. Seasonality
Report 05: month-of-year tables, Kruskal–Wallis test, and a count of months with |t| > 2 against the ~0.5 expected by chance. Real findings pending.

## 7. Positioning
- **Alignment:** COT is aligned to its release (Friday 15:30 ET → next session); T14 checks the timing.
- **Features:** managed-money net/OI, 3-year percentile, z-score and 4-week change.
- **Hypotheses:** H15–H17.
- **Real findings:** pending CFTC ingestion (`ingest-cot`).

## 8. Macro
- **Hypotheses:** H18 (lagged real-yield change → gold) and H19 (USD).
- **Report 06:** lists contemporaneous and lagged (predictive) correlations side by side, with split-half stability.
- **Real findings:** pending FRED ingestion.

## 9. Technical findings / equity-method transfer
- **Implemented and pre-registered:**
  - Trend: H01–H07.
  - Trend template: H08.
  - VCP proxy: H09.
  - Volatility regime: H20.
  - Position-sizing study: equal notional vs volatility vs ATR.
- **Cup & Handle (H27):** DESIGN-LIMITED. There is no objective detector yet.
- **Transfer verdicts:** pending real data.

## 10. Strategy findings
None on real data.
- **Synthetic no-edge runs:** 0 accepted in both seeds.
  - Seed 7: 21 REJECTED, 4 WEAK, reality-check p 0.77.
  - Seed 21: 17 REJECTED, 8 WEAK, reality-check p 0.68.
- **Planted-carry run:**
  - H11 carry: PROMISING.
  - H08 trend template and H25 cross-sectional momentum: ROBUST. The planted premium follows a persistent curve state and so creates persistent drift; that is why they qualify here.
  - Nine families REJECTED.
  - Reality-check p = 0.024.

## 11. Robustness
- **Implemented checks:** every pre-registered parameter, costs ×2 and ×3, execution lag 2–3, 5% missing data, all six roll rules, three subperiods, regimes (volatility, carry sign, trend, real yields, USD), and block-bootstrap confidence intervals.
- **Rule:** a hypothesis that works at only one parameter value is capped at PROMISING.
  - Example: H11, where carry_12m works but nearby carry does not.

## 12. OOS
- **Splits** (fixed in `config/settings.yaml`): TRAIN 50%, VALIDATION 25%, OOS 25% (evaluated once).
- **Walk-forward:** expanding windows on TRAIN+VALIDATION.
- **Selection:** parameters are chosen on TRAIN only.

## 13. MCX
- **Implemented:**
  - Contract rules (bhavcopy expiry overrides the rule).
  - MCX cost model (CTT, stamp duty, exchange fees, GST; values marked VERIFY).
  - Decomposition of MCX returns into global return, lagged global return, USDINR and basis.
  - Liquidity and roll-cost statistics.
  - Strategy transfer using the same parameters on MCX contracts and costs.
- **Synthetic check:** the decomposition recovered the generator's structure (R² 0.94–0.98, USDINR β ≈ 1). This confirms the regression is wired correctly.
- **Real MCX findings:** pending the bhavcopy download (free, but the host is blocked from this environment).

## 14. Portfolio construction
- **Allocation methods:** equal, equal-volatility, risk parity (coordinate-descent ERC), correlation-adjusted.
- **Controls:** sector risk caps (50%) and a 10% portfolio volatility target.
- **Report 10:** sector risk shares and the sizing comparison. In synthetic data, volatility sizing cut the largest single-root risk share from 0.33 to 0.20.

## 15. Risk management
- **Controls in place:**
  - Volatility targeting and a leverage cap of 3×.
  - Per-instrument weight cap.
  - Sector risk caps.
  - ATR trailing stops and time stops.
  - Delivery-window exclusion.
  - Limit-lock and missing-data rules.
- **Paper engine alerts:** drawdown, leverage, missing price, roll due.

## 16–18. Strategies rejected / promising / production candidates (REAL data)
None of the 27 hypotheses has been tested on real data. No production candidates. By design, a result on synthetic data cannot earn research status.

## 19. Remaining data limitations
1. **Network:** every market-data host is blocked from this environment.
2. **Per-contract history for CME (GC, SI, HG, CL, NG):** needs a paid L4 source. Options are CME DataMine, Norgate or CSI (OPEN-17.1).
3. **LME aluminium and base metals:** licensed data, postponed by decision.
4. **EIA inventories:** an API key is optional — XLS download needs no key. Weather data (NOAA) not wired.
5. **MCX:** depth of bhavcopy history, tender rules and exact cost parameters are VERIFY items.
6. **Calendars:** exchange calendars are rule-based approximations. T2 and T6 will expose mismatches.
7. **Macro vintages:** FRED returns latest vintages only (fine for market yields; not for revised statistics).

## 20. Remaining research questions
OPEN items in 16 (roadmap), 17 §8 and 18. In addition:
- Is the block sign-flip permutation correctly calibrated on real data? Check with placebo signals.
- Statistical power for 5–11 markets given an effective trial count of about 4–5.

## 21. Paper-trading plan
1. Ingest real data.
2. `run --source db`.
3. Promote only hypotheses with status PRODUCTION-CANDIDATE into `config/paper.yaml`.
4. Run `paper` daily after settlement. Fills are simulated at the next settlement, using the same signal, sizing and roll code as the backtests.
5. Run at least 6 months of paper trading with monitoring of slippage and tracking error before any live decision. Going live requires your explicit approval.

**The reference book currently in `paper.yaml` is an engineering fixture, not a strategy.**

## 22. Future expansion
- Secondary metals (PL, PA; Zn, Ni, Pb once LME is licensed).
- RBOB/HO for crack spreads.
- NOAA HDD/CDD.
- Options and implied volatility (13).
- An intraday cost model.
- Cross-sectional research once breadth allows.
