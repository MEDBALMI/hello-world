# 02 — Commodity Market Structure

> Status: **Part A (Phase 2, Equities vs Commodities) v0.1 complete. Part B (Phase 3, curve & continuous-futures construction) v0.1 draft**: construction methods are covered because the database design depends on them. Empirical curve research (slope as a signal, PCA, etc.) lives in **11_COMMODITY_TERM_STRUCTURE.md**.
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

# PART B — Futures curve and continuous-series construction (Phase 3 draft)

## B.1 Curve shape recap
Definitions: contango/backwardation, carry, convenience yield → 01#22–30. Here we focus on how curve shape affects *returns* and *data*.

## B.2 Roll yield — worked example
Crude curve stable at: M1 = 80, M2 = 78 (backwardation, ~2.5%/month).
- Hold M2 for one month. If spot/curve shape unchanged, M2 becomes the new M1 and rolls *up* to 80 → +2.56% with no spot change.
- Contango (M1 = 80, M2 = 82): same logic gives −2.4%/month.
- Caveat [FACT]: this is only realised if the curve shape stays the same. "Roll yield" is an ex-ante carry estimate, not a guaranteed return.

## B.3 Why naive front-month backtests mislead
1. **Artificial jumps.** On roll day the series switches from M1 to M2. In contango (M2 > M1), the chart jumps up; in backwardation, down. A naive return calculation books this as P&L, but no trader earned it.
   - Example: CL Dec at 70.00, Jan at 71.20 on roll day → naive series shows +1.7% "return". Actual held-position return that day ≈ the Dec contract's move (could be −0.3%).
2. **Systematic bias.** In markets that are usually in contango (NG, often crude, gold always mildly), the naive series *overstates* long returns by the sum of roll gaps — the exact opposite of the roll losses a real long position suffered.
3. **Expiry distortions.** The last days of a contract can have thin liquidity, squeezes and delivery effects (WTI 20 Apr 2020: May contract −$37.63 while June ≈ +$20). A series that holds M1 to expiry includes untradeable prices.
4. **Indicator artefacts.** Moving averages, ATR, 52-week highs, and breakout levels computed across unadjusted roll gaps trigger false signals.
5. **Volume/OI artefacts.** Per-contract volume collapses before roll; continuous-series volume jumps.

## B.4 Continuous-series construction methods

| Method | How | Preserves | Distorts | Use for |
|---|---|---|---|---|
| **Unadjusted / spliced** | Concatenate the "current" contract | Actual historical price levels | Returns at roll (gaps) | Charting reference only; never P&L |
| **Back-adjusted (difference) — "Panama"** | At each roll, add (new − old) gap to all *earlier* prices | Point/dollar changes; MA crossovers in points | % returns; historical levels; can go **negative** (crude, NG) | Point-based P&L simulation in a single market; not for % returns or ratio indicators |
| **Ratio-adjusted (proportional)** | At each roll, multiply earlier prices by new/old | % returns; no negatives | Point changes, historical levels; dollar P&L | % return series, volatility, MAs on % basis, 52-wk-high style logic |
| **Return-chained total-return index** (recommended for P&L) | Compute daily return of the *held* contract (same contract on both days), chain into an index | Exactly the tradeable excess return | Levels are an index, not a price | **Backtest P&L, performance, risk** |
| **Constant-maturity / "perpetual"** | Interpolate between two contracts to a fixed time-to-maturity (e.g. 30, 90 days); weights shift daily | Smooth, no roll jumps, comparable through time | Not directly tradeable (implicit daily roll); interpolation error | **Features/signals** (curve points, slope), research on spot-like dynamics |
| **Forward-adjusted** | Adjust *later* prices instead of earlier | Earliest levels | Current levels (unusable live) | Rarely; avoid |

Notes [FACT]:
- Back-adjusted series change every time a new roll is appended → stored "historical prices" are not stable. Never store adjusted series as source data; generate them as views.
- Ratio-adjusted and return-chained series give identical % returns *if* rolls are executed at the same prices used for adjustment.
- "Perpetual" in vendor terminology (e.g. some data vendors) usually means constant-maturity weighting; check each vendor's exact definition [VERIFY per vendor].

## B.5 Roll schedules

| Rule | Description | Pros | Cons / risks |
|---|---|---|---|
| Fixed days before FND/LTD | e.g. roll 5 business days before FND (physical) or LTD (cash-settled) | Deterministic, no look-ahead | May roll before/after liquidity actually shifts |
| Index-style fixed window | e.g. S&P GSCI roll: 5th–9th business day of month, 20%/day `[VERIFY]` | Mirrors investable indices | Front-running of known index rolls (documented by Mou 2010 [EMPIRICAL, verify]) |
| Volume or OI crossover | Roll when next contract's volume/OI exceeds current | Follows liquidity | **Look-ahead** if using same-day volume/OI (OI is published T+1); must lag by ≥1 day |
| Active-months only | Gold: Feb/Apr/Jun/Aug/Oct/Dec; copper: Mar/May/Jul/Sep/Dec | Matches where liquidity is | Must be encoded per commodity and per era |
| Curve-optimal ("carry-optimised") | Choose contract on curve with best roll yield | Can improve returns | It's a *strategy*, not a data convention; keep separate |

Our default (proposed, to confirm in 03/11): **deterministic roll N business days before FND (physical) or LTD (cash), restricted to the commodity's liquid months**, with N chosen per commodity from historical volume/OI crossover statistics measured with a lag.

## B.6 Expiry gaps & contract-switch artefacts — checklist for any series
- [ ] Is the series built from per-contract data that we hold?
- [ ] Is the roll date known *before* it happens (no future volume/OI)?
- [ ] Are returns computed within the same contract on both days?
- [ ] Are roll costs (calendar-spread bid-ask) deducted?
- [ ] Are last-N-days-before-expiry prices excluded from the held series?
- [ ] For indicators: is the adjustment method consistent with the indicator type (points vs %)?
- [ ] Are negative prices (2020 WTI) handled (log returns undefined)?
- [ ] For MCX: are contract expiries and liquidity months mapped for MCX, separately from CME?

## B.7 Basis, convenience yield, storage, inventory, calendar spreads
Concepts → 01#21–25, 30, 36. Empirical relationships (slope ↔ inventory, slope → returns) → 11. Short form [THEORY: storage]: low inventory → high convenience yield → backwardation → higher spot volatility; high inventory → full carry contango, capped by storage cost/capacity.

## B.8 Data sources for contract-level history (preliminary — see SOURCE_REGISTER)
| Source | Coverage | Cost | Notes |
|---|---|---|---|
| CME DataMine | Official CME/COMEX/NYMEX per-contract EOD & intraday | Paid | Gold standard for US contracts |
| ICE Data | Brent and ICE contracts | Paid | |
| LME | Official prices, stocks | Licensed/paid | LME 3M structure differs from monthly futures |
| Vendors (Norgate, CSI Data, Barchart, Databento, Refinitiv/LSEG, Bloomberg) | Varies | Paid (wide price range) | Check each for per-contract (not only continuous) history and roll calendars [OPEN-3.1] |
| EIA | Spot and futures contracts 1–4 for WTI, Henry Hub, products | Free | Only first few contracts; good for slope features in energy |
| MCX bhavcopy / historical data | Per-contract daily for MCX | Free on website (format changes over time) [VERIFY] | Needs scraping/cleaning; check depth of history |
| Nasdaq Data Link (ex-Quandl) | Historic free futures datasets (CHRIS) | — | Free continuous datasets were discontinued `[VERIFY]`; do not depend on them |

## B.9 Open research questions (Part B)
- [OPEN-3.1] Which affordable vendor provides per-contract daily history (incl. expired contracts and FND/LTD) for GC, SI, HG, CL, NG, aluminium (CME ALI or LME)?
- [OPEN-3.2] Optimal N (days before FND/LTD) per commodity, measured from lagged volume/OI crossover.
- [OPEN-3.3] Size of roll-gap bias in naive vs correct series for each core commodity (quantifies how wrong naive backtests are).
- [OPEN-3.4] Benchmark choice for aluminium: LME (global benchmark, licensed data, 3M forward structure) vs CME aluminium (less liquid) vs MCX. Needs a decision before database build.
- [OPEN-3.5] Handling of negative prices in return and log-return calculations.
