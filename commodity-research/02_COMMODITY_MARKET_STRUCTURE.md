# 02 — Commodity Market Structure

> Status: **v1.0 (2026-10-02). Part A (Phase 2) v0.1 complete; Part B (Phase 3) complete.** Data-handling rules → 03 §5; timestamp framework → 03 §6; curve features → 11. Tags: [V-S]/[V-2]/[VERIFY] as defined in 00.
> Concept definitions are in **01** (referenced as `01#n`). Evidence labels: [FACT] [THEORY] [EMPIRICAL] [BELIEF] [OPEN] [HYPOTHESIS].

---

# PART A — Why commodities differ from equities (Phase 2)

## A.1 Comparison table

| Dimension | Equities | Commodity futures | Research consequence |
|---|---|---|---|
| **Underlying** | Claim on a firm's residual cash flows | Contract on a physical good of specified grade, place and date (01#5–6) | No "company" to analyse; the "fundamentals" are a physical balance sheet |
| **Ownership** | Perpetual ownership, voting rights | No ownership; a temporary obligation that expires | No buy-and-hold of one instrument; exposure has to be rolled |
| **Cash flows** | Dividends, buybacks, earnings growth | **None.** The commodity yields nothing; holding physical *costs* storage + financing | No compounding of earnings; long-only return has no structural growth engine [THEORY] |
| **Valuation** | DCF, multiples, earnings yield | No intrinsic value model. Anchors: marginal cost of production (long run), inventory/convenience yield (short run), real rates (gold) | Value-type signals are weak/ill-defined; "cheap vs cost curve" is a slow, noisy anchor [OPEN] |
| **Supply/demand** | Shares outstanding change slowly; demand = investor flows | Physical flows dominate: production, consumption, trade; short-run supply often inelastic | Fundamentals data are physical (EIA, LME stocks) and released on fixed calendars |
| **Inventory** | Not applicable (company inventory is an accounting item) | Central state variable linking spot, curve and volatility (01#36) | A whole factor family absent in equities |
| **Expiry** | None | Every contract expires; liquidity concentrates in front/active months | Continuous series must be **constructed** (Part B) |
| **Futures curve** | Equity index futures curve ≈ rates − dividends (mechanical, tiny) | Shape varies widely and carries information (contango/backwardation) | Curve features = primary new signal family (11) |
| **Leverage / margin** | Optional (margin account, ~2×); cash-equity is unlevered | Built-in: margin 3–15% of notional (01#11–14) | Size by notional × volatility; model fully-collateralised excess returns |
| **Seasonality** | Calendar effects weak, contested (Jan effect, etc.) | Real seasonality in fundamentals (gas, gasoline, Indian gold demand) — but mostly **priced into the curve** | Must test seasonal *excess* returns, not seasonal *prices* (12) |
| **Storage** | Not applicable | Cost and capacity drive carry and extreme events (WTI 2020) | Storage constraints = tail-risk regime |
| **Physical delivery** | Not applicable (settlement is just shares/cash) | Possible obligation; squeezes near expiry (LME nickel 2022, WTI 2020) | Backtests must exit before FND/LTD |
| **Roll yield** | None (index futures roll ≈ carry) | Significant component of long-run returns [EMPIRICAL: Erb & Harvey 2006; Gorton & Rouwenhorst 2006] | Separate spot vs roll in every return attribution |
| **Volatility** | Index ~15–20% annualised; single stocks 25–60% | Gold ~15%; crude ~30–40%; NG ~50–80%; copper ~20–25% (rough, regime-dependent) [VERIFY with data] | Vol-normalise; NG is a different beast |
| **Vol asymmetry** | Leverage effect: vol rises when prices fall | Often **inverse** for supply-shock commodities (vol rises in rallies — crude, NG; gold vol often up when price up) [EMPIRICAL claims, to test] | Volatility-contraction logic from equities may not transfer (Part A.3) |
| **Liquidity** | Thousands of names; liquidity spread across them | Few very liquid contracts; liquidity concentrated in front/benchmark months; deferred months thin | Small universe; roll costs; far-month data quality |
| **Participants** | Investors, funds, retail; insiders | Hedgers (producers/consumers), merchants, swap dealers, CTAs, macro funds (01#46–50) | Positioning data (COT) exist; no "insider" or earnings revision analogue |
| **Macro sensitivity** | Earnings growth, discount rates | USD, real rates (gold), global growth/China (copper, crude), inflation | Same macro variables, different signs and regime dependence |
| **Geopolitical sensitivity** | Mostly indirect | Direct and large (supply disruptions, sanctions, OPEC+, wars) | Jump risk; event-driven gaps; fat tails |
| **Information events** | Earnings, guidance (company-specific) | Scheduled data releases (EIA Wed/Thu, OPEC meetings, WASDE n/a, LME stocks daily) | Event calendar replaces earnings calendar |
| **Long-run drift** | Positive equity risk premium (well documented) | Average *individual* commodity futures excess return close to zero historically; diversified, rebalanced portfolios did better [EMPIRICAL: Erb & Harvey 2006; contrast Gorton & Rouwenhorst 2006 who report a positive premium] | **Do not assume a long-only "commodity premium".** Long bias assumptions from equities are dangerous |
| **Breadth** | Thousands of stocks → cross-sectional strategies have breadth | Our scope: 6 core (11 total). Academic cross-sectional studies use 20–30+ incl. agriculture | **Cross-sectional ranking strategies have very low breadth in our scope** — favour time-series tests [OPEN: how many independent bets do 11 metals/energy contracts give?] |
| **Technical behaviour** | Momentum (12-1), breakouts, bases driven partly by institutional accumulation and earnings drift | Time-series momentum/trend has long documented history across commodity futures [EMPIRICAL: Moskowitz, Ooi & Pedersen 2012; Hurst, Ooi & Pedersen 2017]; pattern-based (VCP, cup & handle) evidence: none known to us | Trend transfers *as a concept*; chart patterns are untested [OPEN] |

## A.2 The single biggest difference: what a "return" is

Equity total return = price change + dividends. Clean.

Commodity futures, fully collateralised, per period:

```
Total return  = Excess (futures) return + Collateral return (T-bill)
Excess return = return of the contract actually held, chained across rolls
             ≈ Spot return + Roll return        (an ex-post decomposition)
Roll return   ≈ − (slope of curve between held contract and spot) × time   (if curve shape unchanged)
```

Consequences [FACT/THEORY]:
- A commodity's spot price can rise while a long futures position loses money (persistent contango: e.g. natural gas and crude ETFs in 2009–2010 and 2020).
- Price charts on most retail platforms are **spot or naively-spliced front-month** series — neither is the return you would have earned.
- When comparing to equity strategies, compare **excess** returns (or add collateral to both sides consistently).

## A.3 Which equity concepts transfer — initial assessment (to be tested in Phase 15)

| Equity concept | Transfer status | Reasoning |
|---|---|---|
| Risk management, vol-based sizing, portfolio construction | **Transfers well** [FACT] | Mechanics are asset-agnostic; even more necessary given leverage and fat tails |
| Systematic backtesting discipline, OOS, walk-forward | **Transfers fully** | Additionally need roll handling and point-in-time fundamentals |
| Time-series trend following / moving-average rules | **Likely transfers** [EMPIRICAL support exists for diversified portfolios] | But single-commodity results are noisy; evidence is strongest at portfolio level; MA levels depend on continuous-series method (Part B) |
| Cross-sectional momentum / relative strength | **Partially** | Documented in broad commodity universes (e.g. Miffre & Rallis 2007) [EMPIRICAL]; our 6–11 commodity universe is too small for reliable cross-sectional ranking → treat as [OPEN] |
| 52-week-high / Minervini trend template | **Uncertain** | Requires a meaningful price level; back-adjusted levels are synthetic; ratio-adjusted needed. Mechanism (institutional accumulation + earnings drift) has no direct commodity analogue [HYPOTHESIS] |
| Breakouts (Donchian) | **Plausible** | Donchian breakouts are classic CTA rules (Turtle lineage) — but folklore ≠ evidence; test [BELIEF→HYPOTHESIS] |
| VCP / Cup & Handle | **Unknown, sceptical** | Built around equity supply/demand of shares (sellers exhausted, institutions accumulating). Commodity vol contractions may instead reflect inventory-buffered calm; vol often expands *with* rallies in supply-shock markets [HYPOTHESIS] |
| Volume confirmation | **Weak transfer** | Futures volume is dominated by roll cycles and spread trading; aggregate volume across contracts required [HYPOTHESIS] |
| Earnings/CANSLIM fundamentals | **Does not transfer** | No earnings. The *analogue* is "fundamental surprise" (inventory vs expectations, curve tightening) |
| Options as defined-risk overlay | **Transfers conceptually** | Different underlying (futures), different skew (often call skew in commodities) → 13 |
| Long-term buy-and-hold | **Does not transfer** | No cash flows; roll yield; mean-reverting real prices over very long horizons [EMPIRICAL claims, verify] |
| Time stops | **Likely transfers** | Asset-agnostic; but must interact with roll schedule |

**Key mental shift:** In equities, the edge is often *selecting* the right stock. In commodities (with our scope), the edge — if any — is likely in *timing exposure and harvesting structural premia* (trend, carry/curve, hedging pressure) on a handful of markets, with careful construction and risk control. [HYPOTHESIS — to be tested]

---

# PART B — Futures market structure (Phase 3, v1.0)

Concept definitions are in 01 (01#5, #15–30). Part B covers how they affect **returns and data**. The data rules that put this into practice (expiry, FND, illiquidity, missing data, negative prices, limits, spec changes) are in **03 §5**, and curve features are in **11**.

## B.1 Contract identity and lifecycle

Every analysis starts from **one row per (contract, trading day)**. A contract has a fixed lifecycle:

```
listing ──► (illiquid) ──► becomes active ──► FIRST NOTICE / TENDER ──► LAST TRADING DAY ──► final settlement / delivery
            deferred        front/liquid       delivery risk starts       trading stops        (physical or cash)
```

| Date | Definition | Who it binds | Physical-settled examples | Cash-settled examples |
|---|---|---|---|---|
| **First Notice Day (FND)** | First day a short may give delivery notice; longs can be assigned delivery | Longs in physical contracts | GC/SI/HG: last business day before delivery month [V-S for GC] | None |
| **Tender / delivery period** (MCX) | Days before expiry when positions in compulsory-delivery contracts are marked for delivery; extra margins apply | MCX bullion and base-metal longs and shorts | MCX Gold/Silver (compulsory delivery) [VERIFY in 14] | n/a |
| **Last Trading Day (LTD)** | Last day the contract trades | Everyone | GC: 3rd-last business day of delivery month; CL: rule tied to the 25th of the prior month [V-S]. For CL, delivery notices come *after* LTD | MCX Crude/NG: expiry close to the NYMEX expiry [V-2] |
| **Final settlement** | Physical delivery, or cash against a reference price | Holders at expiry | Delivery via warrant, receipt or pipeline | MCX Crude/NG: NYMEX settle × RBI rate [V-S] |

**Key derived field: `delivery_risk_date` = earliest of (FND, tender start, LTD).** Every traded position must be out by `delivery_risk_date − buffer`. For cash-settled contracts this is simply LTD. **Liquidity usually leaves a contract before that date**, so the roll date is set by liquidity *and* delivery risk (03 §5.1–5.3).

**Physical vs cash settlement — research consequences**
- *Physical:* the futures price converges to the deliverable physical price. That keeps curve shape tied to inventory (the information we want), but squeezes and delivery frictions can distort the last days before expiry.
- *Cash:* the price converges to a **reference price**. For MCX crude and natural gas the reference is another exchange's settlement, converted to rupees at an FX fixing. Convergence is therefore to *NYMEX × USDINR*, not to Indian physical prices. Expiry-week behaviour follows NYMEX liquidity, as shown by MCX crude going negative in April 2020.

## B.2 Three return concepts — never mix them

| Return | Definition | Tradeable? | Use |
|---|---|---|---|
| **Spot return** | % change of a spot or physical benchmark (LBMA gold, Henry Hub cash, LME cash) | Usually not directly | Describing the commodity; macro relationships |
| **Futures (excess) return** | % change of the *same* held contract between two settlements, chained across rolls | **Yes** | Signals' effect on P&L; strategy evaluation |
| **Total return** | Excess return + collateral (T-bill) return on the capital | Yes | Comparing with equities or funds |

Decomposition (ex post, per period):

```
r_futures  =  r_spot  +  r_roll                 where r_roll ≡ r_futures − r_spot (residual)
r_total    =  r_futures  +  r_collateral
```

Ex-ante carry (expected roll return if the curve shape is unchanged), from the two nearest liquid contracts:

```
carry_t = ln(F1_t / F2_t) × 365 / (T2 − T1 in days)       positive = backwardation
```

Facts that follow [THEORY/FACT]:
- **Gold:** futures ≈ spot × e^{(r − lease rate)T}, so long gold futures under-perform spot by roughly the financing rate. In 2023–24 that gap was roughly the US short rate. This is not a "loss to contango" in any economic sense, because a fully collateralised long earns that rate back as collateral return.
- **Crude, NG, base metals:** r_roll is large and changes over time (storage-driven). It dominates long horizons [EMPIRICAL: Erb & Harvey 2006].
- **Spot data cannot validate a futures strategy, and vice versa.** A signal that predicts spot returns may not predict futures returns (the carry already prices part of it).

## B.3 Contango, backwardation, basis, calendar spreads, term structure (return view)

| Concept | Return implication | Data implication |
|---|---|---|
| **Contango** (01#26) | Long held futures drift *down* toward spot if the curve is unchanged → negative r_roll. Near full carry it is mostly financing plus storage | Needs ≥2 contracts per date |
| **Backwardation** (01#27) | Positive r_roll for longs; associated with low inventory and high volatility [THEORY: storage] | Same |
| **Basis** (01#21) | Converges to ~0 at expiry for physical contracts. MCX vs COMEX basis = import duty + premium + FX + timing (→ 14) | Needs time-aligned spot and futures |
| **Calendar spread** (01#30) | P&L ≈ change in slope; the roll itself *is* a calendar-spread trade, so its bid-ask is a roll cost | Needs synchronous settlements for both legs |
| **Term structure** (01#29) | Level / slope / curvature move separately. Slope changes may carry information [HYPOTHESIS → 11] | Constant-maturity points (B.4) |

## B.4 Continuous-series methods — full evaluation

Running example, roll at close of Day 2 from contract A to B (contango):

| Day | A settle | B settle | Naive spliced | Panama (difference) | Ratio | Chained index (start 100) |
|---|---|---|---|---|---|---|
| 1 | 100.0 | 102.0 | 100.0 | 102.5 | 102.475 | 100.000 |
| 2 (roll) | 101.0 | 103.5 | 101.0 → switch | 103.5 | 103.5 | 101.000 |
| 3 | 101.4 | 104.0 | 104.0 | 104.0 | 104.0 | 101.488 |
| **Day-3 return shown** | | | **+2.97%** ✗ | +0.483% ✓ | +0.483% ✓ | +0.483% ✓ |
| **Day-2 return shown** | true +1.000% | | +1.000% | **+0.976%** ✗ | +1.000% ✓ | +1.000% ✓ |
| **Day-2 point change** | true +1.0 | | +1.0 | +1.0 ✓ | **+1.025** ✗ | n/a (index) |

The naive series books the 2.5-point contango gap as profit. Panama keeps points but distorts percentages. Ratio keeps percentages but distorts points. The chained index matches the held contract exactly.

### Method 1 — Unadjusted (naive spliced front month)
- **A. What it does:** concatenates whichever contract is "current".
- **B. Appropriate for:** showing actual historical price levels (charts, reference levels, "what did gold trade at in 2011").
- **C. Bias:** roll gaps booked as returns. That overstates long returns in contango markets and understates them in backwardation. Indicators fire false signals at rolls. If held to expiry, it includes expiry squeezes.
- **D. Backtesting:** **No.**
- **E. Actual P&L:** **No.**
- **F. Storage:** generate dynamically (a view over contract data plus the roll schedule).

### Method 2 — Back-adjusted, difference ("Panama")
"Panama" is the common name for difference back-adjustment; they are the same method.
- **A. What it does:** at each roll, adds (new − old) to all *earlier* prices so the series is continuous in points.
- **B. Appropriate for:** point-based indicators in one market (moving-average crossovers, Donchian channels, ATR in points). Dollar P&L of a 1-contract position, ignoring cost.
- **C. Bias:**
  - Percentage returns are wrong, and the error grows with distance from today.
  - Historical levels are fictional.
  - The series can go **negative** when cumulative roll gains are large (long backwardated histories such as crude).
  - **Not point-in-time:** every new roll shifts all past values. Level-dependent signals (absolute thresholds, % distance from a moving average) differ from what was observable then.
- **D. Backtesting:** only for signals that are *invariant to an additive shift* (e.g. price vs its own moving average crossover, channel breakouts). Not for % or volatility-scaled rules.
- **E. Actual P&L:** no (no roll costs, no position sizing, % wrong).
- **F. Storage:** **dynamic only.** Its values change with every roll.

### Method 3 — Ratio (proportional) back-adjustment
- **A. What it does:** at each roll, multiplies all earlier prices by new/old.
- **B. Appropriate for:** % returns, volatility, % distance to a moving average, 52-week-high logic, Minervini-style templates. These are scale-invariant signals.
- **C. Bias:**
  - Point/dollar changes are wrong and levels are fictional.
  - Undefined or unstable when prices are ≤ 0 or near 0.
  - Not point-in-time in level, but scale-invariant signals are unaffected, because a uniform multiplicative rescaling of the past leaves ratios unchanged.
- **D. Backtesting:** yes for **signals** built from scale-invariant transforms. Not for P&L.
- **E. Actual P&L:** no. Returns match the chained index only if rolls execute at the adjustment prices, and it carries no costs.
- **F. Storage:** **dynamic.** Can be cached, keyed by (roll policy version, data snapshot).

### Method 4 — "Perpetual" (rolling-weight blend)
- **A. What it does:** a weighted average of two nearby contracts with weights shifting gradually (e.g. linearly over the roll window or the contract cycle), smoothing the switch. Vendor definitions vary [VERIFY per vendor].
- **B. Appropriate for:** smooth visual series; signals sensitive to jump artefacts.
- **C. Bias:** maturity is not constant (it drifts within the cycle). Blending hides the roll. Returns are those of a portfolio that rolls a little every day, which no one trades at quoted prices.
- **D. Backtesting:** signals only, with caution; prefer Method 5 for features.
- **E. Actual P&L:** **No.**
- **F. Storage:** dynamic.

### Method 5 — Constant-maturity (CM) series
- **A. What it does:** interpolates (in log price, linear in days to expiry) between the two contracts bracketing a target tenor (e.g. 30, 90, 180, 365 days). It gives a price at fixed time-to-maturity every day.
- **B. Appropriate for:** **curve features** (slope, curvature, PCA), comparing curve shape through time, volatility by tenor, "spot-like" research series.
- **C. Bias:**
  - Not tradeable (it implies continuous rolling).
  - Interpolation error on sparse or illiquid curves; no extrapolation allowed.
  - Seasonal kinks (NG winter/summer) make linear interpolation misleading (→ 11 §4).
  - It *is* point-in-time if built only from that date's settlements.
- **D. Backtesting:** yes as a **feature input**. As a return series, only as an approximation for research, never as P&L.
- **E. Actual P&L:** **No.**
- **F. Storage:** **may be stored** (materialised), because values are point-in-time and do not change when new data arrive. Key them by method version.

### Method 6 — Chained held-contract returns (total-return index)
- **A. What it does:** each day, return = settle_t / settle_{t−1} − 1 of the **same** contract that is held under the roll policy. On roll day, return is computed on the old contract; the next day's return uses the new contract. Returns are compounded into an index.
- **B. Appropriate for:** the canonical **research return** of a passively rolled position; performance attribution; volatility estimates for sizing.
- **C. Bias:** depends on the roll policy (that is a choice, not a bias, as long as it is known in advance). It omits costs unless deducted. A daily-rebalanced unit-notional index differs slightly from a fixed-contract position. Undefined when settle_{t−1} ≤ 0 (03 §5.7).
- **D. Backtesting:** **Yes.** This is the base return series.
- **E. Actual P&L:** **close, not exact.** It becomes the realistic P&L series (B.5) once integer contracts, costs, limit events and cash are added.
- **F. Storage:** **stored**, versioned by roll policy. Values are point-in-time and never revised unless the source contract data are corrected.

### Method 7 — Forward-adjusted
Adjusts later prices instead of earlier ones, so current prices are wrong. **Do not use.**

### Summary matrix

| Method | Signals | Features | Backtest returns | Actual P&L | Store? |
|---|---|---|---|---|---|
| Unadjusted | ✗ (reference levels only) | ✗ | ✗ | ✗ | dynamic view |
| Panama / difference | shift-invariant only | ✗ | ✗ | ✗ | dynamic |
| Ratio | scale-invariant ✓ | ✗ | ✗ | ✗ | dynamic (cache) |
| Perpetual blend | caution | prefer CM | ✗ | ✗ | dynamic |
| Constant-maturity | ✓ | **✓ primary** | approx only | ✗ | **stored** |
| Chained held-contract | ✓ | ✓ | **✓ primary** | base for P&L | **stored** |
| Realistic traded P&L (B.5) | — | — | ✓ final | **✓** | **stored per backtest run** |

## B.5 Two separate concepts: RESEARCH PRICE SERIES vs REALISTIC TRADED P&L SERIES

### A. Research price series
**Purpose:** compute signals and features, and describe price behaviour. It need **not** be tradeable.
Members: ratio-adjusted, Panama, CM, perpetual, spot benchmarks, and the chained index used as a price input.

Rules:
- **R1.** Generated from clean per-contract data plus a **versioned** method/roll policy. Never hand-edited.
- **R2.** Every value records its source contract(s) and weights.
- **R3.** **Point-in-time integrity:** a signal at date t may only use series values as they would have been computed at t. Either (a) use transforms that are invariant to later back-adjustments (Panama → shift-invariant, ratio → scale-invariant), or (b) use point-in-time series (CM, chained), or (c) rebuild the series as of t ("vintage construction").
- **R4.** **Never used to compute P&L.**

### B. Realistic traded P&L series
**Purpose:** the money that could actually have been made or lost.

Rules:
- **P1. Held contract identified every day.** At every date the position maps to specific contract IDs (and integer lots in full backtests).
- **P2. Same-contract differencing.** P&L_t = (settle_t − settle_{t−1}) × multiplier_t × lots, for each held contract. No cross-contract differences, ever.
- **P3. Rolls are trades.** The roll executes on the scheduled date as a calendar-spread trade: sell old, buy new, at modelled prices (settle ± modelled half-spread per leg, or the spread-instrument cost). Both legs are logged.
- **P4. Eligibility.** A contract can be held only if it passes the liquidity filter on information available at t−1 and t < its `delivery_risk_date − buffer` (03 §5).
- **P5. Execution realism.**
  - Trades on a limit-locked day are deferred (03 §5.8).
  - Trades are not filled at prices that did not exist.
  - Execution timing is consistent with signal availability (03 §6).
- **P6. Costs.** Commission, exchange and clearing fees, taxes (e.g. MCX CTT and stamp duty → 14), slippage model in ticks (calibrated per contract and liquidity tier).
- **P7. Currency.** P&L is booked in contract currency and converted at a defined fixing with a known timestamp.
- **P8. Capital.** Returns are on account equity, not margin. Collateral interest is added separately and explicitly.
- **P9. Reproducibility.** The series can be regenerated exactly from clean data, roll schedule, cost model and position file, each versioned.

Two levels share the same held-contract engine:
- **Unit tradable return series** (per root, per roll policy, fractional notional, with an average cost estimate). This is the research benchmark for "what a passive long earned".
- **Backtest P&L** (integer lots, capital, sizing, full cost model). One output per backtest run.

## B.6 Roll policy

Rolls are set by the **roll policy** (versioned in `derived.roll_policy`, 03 §3.5). Recommended default, **ROLL-A**:
1. Universe of holdable contracts = the root's **liquid months** (11 §2), as of the date.
2. Roll **window** = the k business days ending `delivery_risk_date − buffer`. Defaults: buffer = 2 business days; k = 1 for research or up to 5 for realistic execution, with equal tranches.
3. Roll **earlier** if, on t−1 data, the next eligible contract's volume and OI both exceed the current one's for 2 consecutive days. Lagged, so there is no look-ahead.
4. The roll schedule is computed **once** from information available at each date and stored. Backtests read it; they never recompute it with future data.
5. Per-commodity N/k calibrated from lagged volume/OI crossover statistics [OPEN-3.2]; until calibrated use the defaults above.

Alternative policies (kept as separate versions, never mixed): S&P GSCI-style fixed window (5th–9th business day [V-S]), constant days-to-expiry, carry-optimised (that is a *strategy*, not a data convention).

## B.7 Artefact checklist (applies to every series)
- [ ] Built from per-contract data we hold; roll schedule fixed in advance.
- [ ] Returns use the same contract on both days.
- [ ] Positions exit before `delivery_risk_date − buffer`.
- [ ] Roll costs deducted (P&L series).
- [ ] Indicator transform is consistent with the adjustment method (B.4 matrix, R3).
- [ ] Negative or near-zero prices handled (03 §5.7).
- [ ] Limit-lock days flagged (03 §5.8).
- [ ] MCX series mapped to MCX contracts and expiries, never inferred from CME.

## B.8 Data sources
Moved to **03 §7** (single source of truth).

## B.9 Open research questions (Part B)
- [OPEN-3.1] Affordable per-contract history incl. expired contracts and FND/LTD metadata → 03 §8.
- [OPEN-3.2] Optimal roll offset and window per commodity from lagged volume/OI crossover.
- [OPEN-3.3] Size of naive-vs-chained bias per commodity (data-validation test, not a strategy).
- [OPEN-3.4] Aluminium benchmark (LME vs CME vs MCX).
- [OPEN-3.5] Negative prices → policy defined in 03 §5.7; test impact on 2020 crude.
- [OPEN-3.6] MCX bhavcopy earliest date and format history.
- [OPEN-3.7] MCX tender/delivery-period rules per bullion and base-metal contract and their history (sets `delivery_risk_date` for MCX).
