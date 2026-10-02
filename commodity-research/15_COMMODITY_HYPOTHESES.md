# 15 — Commodity Hypotheses (pre-registered)

> Generated from `commodity/config/hypotheses.yaml` (source of truth; edit there, never here).
> Grids are fixed before testing. Status columns show the latest pipeline run and its data class;
> runs on SYNTHETIC data never confer research status.

## H01 — A_TSMOM (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `tsmom` · **grid:** `{"lookback": [126, 252]}`
- **Economic Rationale:** Slow information diffusion and hedging-pressure persistence produce time-series momentum (Moskowitz, Ooi and Pedersen 2012)
- **Feature:** trailing return of the chained tradable index
- **Signal:** sign of trailing return
- **Entry:** sign change
- **Exit:** opposite sign
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** positive excess return, positive skew
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `WEAK`, final `NOT-RESEARCH (SYNTHETIC)`

## H02 — A_TSMOM (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `tsmom_12_1` · **grid:** `{}`
- **Economic Rationale:** 12-1 momentum skips the last month to avoid short-term reversal
- **Feature:** 12-month return excluding the last month
- **Signal:** sign
- **Entry:** sign change
- **Exit:** opposite sign
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** similar to H01
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `WEAK`, final `NOT-RESEARCH (SYNTHETIC)`

## H03 — B_TREND (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `ma_trend` · **grid:** `{"n": [50, 150, 200]}`
- **Economic Rationale:** Equity moving-average trend filter transfer test; trend persistence in futures
- **Feature:** distance to n-day moving average of the ratio-equivalent index
- **Signal:** sign
- **Entry:** cross above/below the MA
- **Exit:** opposite cross
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** positive Sharpe
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `REJECTED`, final `NOT-RESEARCH (SYNTHETIC)`

## H04 — B_TREND (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `ma_cross` · **grid:** `{"fast": [50], "slow": [150, 200]}`
- **Economic Rationale:** Golden/death cross transfer test from equities
- **Feature:** fast vs slow moving average
- **Signal:** sign of difference
- **Entry:** cross
- **Exit:** opposite cross
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** positive Sharpe
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `WEAK`, final `NOT-RESEARCH (SYNTHETIC)`

## H05 — C_BREAKOUT (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `donchian` · **grid:** `{"entry": [55, 252], "exit": [20, 55]}`
- **Economic Rationale:** Breakouts capture regime shifts in supply/demand (CTA practice; folklore until tested)
- **Feature:** N-day channel of the index
- **Signal:** breakout state
- **Entry:** close beyond N-day high/low
- **Exit:** M-day opposite channel
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** positive Sharpe
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `WEAK`, final `NOT-RESEARCH (SYNTHETIC)`

## H06 — C_BREAKOUT (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `vol_breakout` · **grid:** `{"k": [1.0, 1.5, 2.0], "hold": [5, 10]}`
- **Economic Rationale:** Large ATR-scaled moves signal information arrival that continues
- **Feature:** 1-day return divided by ATR%
- **Signal:** direction of the shock
- **Entry:** abs(return) > k x ATR
- **Exit:** time stop (hold days)
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** short-horizon continuation
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `REJECTED`, final `NOT-RESEARCH (SYNTHETIC)`

## H07 — A_TSMOM (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `roc` · **grid:** `{"lookback": [21, 63]}`
- **Economic Rationale:** Shorter-horizon momentum
- **Feature:** rate of change
- **Signal:** sign
- **Entry:** sign change
- **Exit:** opposite sign
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** weaker than 12-month momentum
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `REJECTED`, final `NOT-RESEARCH (SYNTHETIC)`

## H08 — Q_EQUITY_TRANSFER (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `trend_template` · **grid:** `{}`
- **Economic Rationale:** Minervini trend template transfer test (long-only). The equity mechanism (institutional accumulation, earnings drift) has no direct commodity analogue
- **Feature:** MA stack + 52-week high/low proximity
- **Signal:** 1 when template is true
- **Entry:** template true
- **Exit:** template false
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** unknown
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR, or no better than H03
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `REJECTED`, final `NOT-RESEARCH (SYNTHETIC)`

## H09 — Q_EQUITY_TRANSFER (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `vcp_breakout` · **grid:** `{"entry": [55]}`
- **Economic Rationale:** VCP transfer test: volatility contraction then breakout (long-only). In supply-shock markets volatility often expands with rallies
- **Feature:** three successively tighter ranges near the 52-week high
- **Signal:** long on 55-day breakout
- **Entry:** breakout after contraction
- **Exit:** close below 50-day MA
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** unknown
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR, or no better than H05
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `REJECTED`, final `NOT-RESEARCH (SYNTHETIC)`

## H10 — D_MEAN_REVERSION (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `mean_reversion` · **grid:** `{"z": [1.5, 2.0, 2.5], "hold": [5]}`
- **Economic Rationale:** Liquidity-provision reversal after extreme short-term moves (weak prior for futures)
- **Feature:** 5-day return z-score
- **Signal:** fade the extreme
- **Entry:** abs(z) > threshold
- **Exit:** 5-day time stop
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** small positive at short horizon
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `REJECTED`, final `NOT-RESEARCH (SYNTHETIC)`

## H11 — F_CARRY (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `carry` · **grid:** `{"col": ["carry", "carry_12m"]}`
- **Economic Rationale:** Theory of storage / hedging pressure: backwardation signals scarcity and pays roll yield (Koijen et al. 2018; Gorton, Hayashi and Rouwenhorst 2013)
- **Feature:** annualised nearby carry (TS1) or seasonal-neutral 12-month carry (TS9)
- **Signal:** long backwardation, short contango
- **Entry:** carry sign change
- **Exit:** opposite sign
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** positive in energy/base metals; about zero in gold where carry is mechanical
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `WEAK`, final `NOT-RESEARCH (SYNTHETIC)`

## H12 — E_TERM_STRUCTURE (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `carry_z` · **grid:** `{"threshold": [0.0, 1.0]}`
- **Economic Rationale:** Carry relative to its own history captures changes in tightness (TS6)
- **Feature:** carry z-score (252 days)
- **Signal:** sign beyond threshold
- **Entry:** abs(z) > threshold
- **Exit:** abs(z) < threshold
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** positive
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `REJECTED`, final `NOT-RESEARCH (SYNTHETIC)`

## H13 — G_MOM_CARRY (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `mom_carry` · **grid:** `{"lookback": [126, 252]}`
- **Economic Rationale:** Momentum and carry are distinct premia; agreement filters noise
- **Feature:** momentum sign and carry sign
- **Signal:** trade only when both agree
- **Entry:** agreement
- **Exit:** disagreement
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** higher Sharpe than either alone
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR, or not better than H01 and H11 out-of-sample
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `WEAK`, final `NOT-RESEARCH (SYNTHETIC)`

## H14 — H_TREND_CARRY (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `trend_carry_filter` · **grid:** `{"n": [150, 200]}`
- **Economic Rationale:** Avoid trend trades fighting strong carry (roll-yield drag)
- **Feature:** MA trend + carry beyond 10%
- **Signal:** trend unless carry strongly opposite
- **Entry:** trend
- **Exit:** trend reversal or carry conflict
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** improves H03
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR, or not better than H03
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `WEAK`, final `NOT-RESEARCH (SYNTHETIC)`

## H15 — I_POSITIONING (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `cot_contrarian` · **grid:** `{"hi": [0.9, 0.95], "lo": [0.1, 0.05]}`
- **Economic Rationale:** Crowded managed-money positioning reverses (market belief; mixed evidence)
- **Feature:** managed-money net / OI, 3-year percentile
- **Signal:** fade extremes
- **Entry:** percentile beyond bounds
- **Exit:** back inside bounds
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** unknown sign
- **Data Required:** CFTC disaggregated COT aligned to release (Friday 15:30 ET -> next session)
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `REJECTED`, final `NOT-RESEARCH (SYNTHETIC)`

## H16 — I_POSITIONING (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `cot_momentum` · **grid:** `{}`
- **Economic Rationale:** Speculator flows are trend-following; positioning changes persist
- **Feature:** 4-week change in managed-money net
- **Signal:** sign
- **Entry:** sign change
- **Exit:** opposite sign
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** unknown
- **Data Required:** CFTC disaggregated COT
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `REJECTED`, final `NOT-RESEARCH (SYNTHETIC)`

## H17 — I_POSITIONING (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `trend_cot` · **grid:** `{"hi": [0.9]}`
- **Economic Rationale:** Avoid trend trades when positioning is already crowded in the trend direction
- **Feature:** MA200 trend + managed-money percentile
- **Signal:** trend unless crowded
- **Entry:** trend
- **Exit:** reversal or crowding
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** improves H03 drawdowns
- **Data Required:** CFTC disaggregated COT
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR, or not better than H03
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `REJECTED`, final `NOT-RESEARCH (SYNTHETIC)`

## H18 — K_MACRO (type B, GLOBAL)

- **Commodities:** GC · **strategy:** `macro_real_yield` · **grid:** `{}`
- **Economic Rationale:** Real yields are gold's opportunity cost (Erb and Harvey 2013); test whether CHANGES are predictive, not only contemporaneous
- **Feature:** 63-day change in 10y TIPS real yield
- **Signal:** long gold after a real-yield decline
- **Entry:** sign change
- **Exit:** opposite sign
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** positive only if a lagged relation exists
- **Data Required:** FRED DFII10 with availability timestamps
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `REJECTED`, final `NOT-RESEARCH (SYNTHETIC)`

## H19 — K_MACRO (type B, GLOBAL)

- **Commodities:** GC, HG, CL · **strategy:** `macro_usd` · **grid:** `{}`
- **Economic Rationale:** Commodities are priced in USD; a weaker USD raises non-US demand
- **Feature:** 63-day change in the broad USD index
- **Signal:** long after USD decline
- **Entry:** sign change
- **Exit:** opposite sign
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** regime-dependent
- **Data Required:** FRED DTWEXBGS
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `REJECTED`, final `NOT-RESEARCH (SYNTHETIC)`

## H20 — M_VOL_REGIME (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `vol_regime_trend` · **grid:** `{"n": [200], "mult": [1.25, 1.5]}`
- **Economic Rationale:** Trend signals are noisier in volatility spikes; halve exposure
- **Feature:** EWMA vol vs its 1-year median
- **Signal:** MA trend scaled by 0.5 in high vol
- **Entry:** trend
- **Exit:** reversal
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** lower drawdown than H03
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR, or not better than H03 risk-adjusted
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `REJECTED`, final `NOT-RESEARCH (SYNTHETIC)`

## H21 — P_SEASONALITY (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `seasonal` · **grid:** `{}`
- **Economic Rationale:** Seasonal demand (heating, driving, Indian festival gold) - but should be priced into the curve
- **Feature:** mean same-month return of PRIOR years
- **Signal:** sign
- **Entry:** month start
- **Exit:** month end
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** about zero (null expected)
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `REJECTED`, final `NOT-RESEARCH (SYNTHETIC)`

## H22 — P_SEASONALITY (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `seasonal_trend` · **grid:** `{"n": [200]}`
- **Economic Rationale:** Seasonality only when confirmed by trend
- **Feature:** seasonal sign + MA trend
- **Signal:** trade only when they agree
- **Entry:** agreement
- **Exit:** disagreement
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** small
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `REJECTED`, final `NOT-RESEARCH (SYNTHETIC)`

## H23 — N_MULTI_FACTOR (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `multi_factor` · **grid:** `{}`
- **Economic Rationale:** Diversify across trend, carry and positioning premia
- **Feature:** average of momentum, carry and COT-contrarian signs
- **Signal:** average in [-1, 1]
- **Entry:** continuous
- **Exit:** continuous
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** higher Sharpe than components
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR, or not better than the best single component
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `WEAK`, final `NOT-RESEARCH (SYNTHETIC)`

## H24 — L_RELATIVE_VALUE (type B, GLOBAL)

- **Commodities:** GC, SI · **strategy:** `gold_silver_rv` · **grid:** `{"z_in": [1.5, 2.0], "z_out": [0.5]}`
- **Economic Rationale:** Gold/silver ratio mean-reverts because both share monetary drivers (cointegration is not predictability - test it)
- **Feature:** z-score of the log ratio of tradable indices
- **Signal:** short rich leg / long cheap leg
- **Entry:** abs(z) > z_in
- **Exit:** abs(z) < z_out
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** positive if the ratio mean-reverts
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `REJECTED`, final `NOT-RESEARCH (SYNTHETIC)`

## H25 — C_XS_SELECTION (type C, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `xs_momentum` · **grid:** `{"n_long": [2], "n_short": [2]}`
- **Economic Rationale:** Cross-sectional momentum (Miffre and Rallis 2007) - low breadth here (03 s.9); architecture test
- **Feature:** 12-month return rank
- **Signal:** long top 2 / short bottom 2
- **Entry:** rank
- **Exit:** rank change
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** weak due to breadth
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `REGISTERED` · last run [SYNTHETIC]: machine `REJECTED`, final `NOT-RESEARCH (SYNTHETIC)`

## H26 — J_INVENTORY (type A, GLOBAL)

- **Commodities:** CL, NG · **strategy:** `None` · **grid:** `{}`
- **Economic Rationale:** Inventory deviations from seasonal norms move prices and the curve (theory of storage)
- **Feature:** inventory deviation from 5-year seasonal mean
- **Signal:** low inventory -> long
- **Entry:** release + 1 session
- **Exit:** next release
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** positive
- **Data Required:** EIA weekly crude stocks / NG storage with release timestamps (needs network or EIA API key)
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** OOS Sharpe <= 0, or DSR p > 0.10, or fails FDR
- **Status:** registry `DATA-LIMITED` · last run [SYNTHETIC]: machine `DATA-LIMITED`, final `NOT-RESEARCH (SYNTHETIC)`

## H27 — Q_EQUITY_TRANSFER (type A, GLOBAL)

- **Commodities:** GC, SI, HG, CL, NG · **strategy:** `None` · **grid:** `{}`
- **Economic Rationale:** Cup & Handle transfer test
- **Feature:** no validated objective detector yet (VCP proxy H09 is the closest tested pattern)
- **Signal:** n/a
- **Entry:** n/a
- **Exit:** n/a
- **Position Size:** volatility-targeted (10% annualised per instrument, EWMA hl 30d), capped 1x notional
- **Expected Effect:** unknown
- **Data Required:** individual contracts (settle, OHLC, volume, OI) and contract calendar
- **Test Period:** TRAIN + VALIDATION (first 75% of each root's history); expanding walk-forward
- **Oos Period:** final 25% of history (hold-out, evaluated once)
- **Failure Condition:** n/a
- **Status:** registry `DESIGN-LIMITED` · last run [SYNTHETIC]: machine `DESIGN-LIMITED`, final `NOT-RESEARCH (SYNTHETIC)`
