# 01 — Commodity Foundations (Phase 1)

> Status: **v0.2 — draft, conceptual; spec numbers checked 2026-10-02.** Contract numbers carry a verification tag: `[V-S]` = confirmed via search excerpt of the official exchange/regulator document (direct page fetch was blocked by the environment's network policy); `[V-2]` = confirmed by ≥2 secondary (broker) sources only; `[VERIFY]` = still unchecked. See SOURCE_REGISTER.md. No data has been downloaded yet.
>
> Format per concept: **A** simple · **B** technical · **C** example · **D** why it matters · **E** quant variable · **F** data needed · **G** pitfalls.
> Concepts that get a deep dive elsewhere are kept short here and cross-referenced (→ file).
>
> Evidence labels used throughout the program:
> **[FACT]** definitional / contractual / documented · **[THEORY]** accepted economic model · **[EMPIRICAL]** published test result (cite) · **[BELIEF]** market folklore, untested by us · **[OPEN]** open research question.

---

## Contents
- A. Instruments — 1 Spot · 2 Futures · 3 Forwards · 4 Options on futures
- B. Contract mechanics — 5 Futures contract · 6 Contract spec · 7 Contract size · 8 Tick size · 9 Tick value · 10 Notional
- C. Margin & leverage — 11 Initial margin · 12 Maintenance margin · 13 Mark-to-market · 14 Leverage
- D. Contract lifecycle — 15 Expiry · 16 Settlement · 17 Physical settlement · 18 Cash settlement · 19 Delivery · 20 Rollover
- E. Pricing & curve — 21 Basis · 22 Cost of carry · 23 Storage · 24 Financing · 25 Convenience yield · 26 Contango · 27 Backwardation · 28 Futures curve · 29 Term structure · 30 Calendar spreads
- F. Market activity — 31 Open interest · 32 Volume · 33 Positioning · 34 COT
- G. Physical fundamentals — 35 Seasonality · 36 Inventory · 37 Supply · 38 Demand · 39 Production · 40 Consumption · 41 Imports · 42 Exports · 43 Refining · 44 Transportation · 45 Warehousing
- H. Participants — 46 Physical vs financial · 47 Hedgers · 48 Producers · 49 Consumers · 50 Speculators
- I. Phase 1 summary: the five ideas that matter most

---

## A. Instruments

### 1. Spot market
- **A.** Buying/selling the physical commodity for (near-)immediate delivery.
- **B.** Spot = price for delivery within the market's standard settlement window (e.g. T+2 for London gold/silver "loco London"; "cash" prompt on LME). Many commodities have **no single spot price**: crude oil "spot" is a physical assessment (e.g. Platts/Argus Dated Brent) or simply the front futures month; natural gas spot is regional (Henry Hub daily cash). [FACT]
- **C.** LBMA Gold Price (twice-daily auction run by ICE Benchmark Administration) is the reference spot for gold. "Spot gold" on a retail terminal (XAU/USD) is an OTC quote, not an exchange price.
- **D.** Most "commodity charts" you see are not spot and not tradeable by you. You trade futures; spot matters as the anchor futures converge to.
- **E.** `spot_t`; `basis_t = spot_t − F_t`; spot return vs futures return gap.
- **F.** LBMA prices (gold/silver/PGMs), EIA spot series (WTI Cushing, Brent, Henry Hub), LME cash official prices.
- **G.** Treating a spot index or XAU/USD as if it were a tradeable return series. Spot returns ≠ futures returns (see 21, 26–27 and 02 §B).

### 2. Futures
- **A.** A standardised exchange-traded agreement to buy/sell a fixed quantity at a fixed price on a future date.
- **B.** Exchange-listed, centrally cleared (clearing house becomes counterparty to both sides), standardised quantity/quality/delivery, daily marked-to-market, margined. Zero cost to enter (besides margin, which is collateral, not a price). [FACT]
- **C.** Buying 1 COMEX Gold (GC) Dec contract at $2,600 = obligation to take 100 oz at $2,600 in Dec unless closed before.
- **D.** This is the instrument we will trade and backtest. A futures position's P&L is the change in that specific contract's price, not the spot price.
- **E.** Per-contract daily settle, OHLC, volume, OI; derived returns must be computed **within** a contract.
- **F.** Contract-level (not continuous) daily history per expiry. See 03 / 11.
- **G.** Thinking a futures contract is an "asset you own". It is a **derivative with an expiry**; there is no long-term buy-and-hold of a single contract.

### 3. Forwards
- **A.** Same economic idea as futures but private, customised, bilateral.
- **B.** OTC contract; no daily MTM (unless collateral agreement), counterparty credit risk, non-standard size/date. LME contracts are structurally forward-like (daily prompt dates, settled at prompt) although exchange-traded and cleared. [FACT]
- **C.** A copper fabricator agrees with a trader to buy 500 t for delivery on 15 March at a fixed price.
- **D.** Physical hedgers mostly use forwards/physical contracts; their hedging spills into futures. LME behaviour (prompt-date structure, "tom-next" spreads) only makes sense with a forward mindset.
- **E.** Rarely directly; LME 3M forward is the benchmark price for base metals.
- **F.** LME 3M and cash prices (licensed).
- **G.** Assuming LME prices behave like CME monthly contracts. LME's benchmark is a *rolling constant-maturity* 3-month forward — a different object.

### 4. Options on futures
- **A.** The right, not the obligation, to buy (call) or sell (put) a futures contract at a strike.
- **B.** Underlying is a futures contract (not spot). Exercise delivers a futures position (CME standard monthly options typically expire a few days *before* the underlying futures' expiry/notice period). Priced by Black-76 (forward-based). [FACT] → full treatment in 13.
- **C.** Buy a GC Feb 2,700 call: on exercise you receive a long Feb GC futures at 2,700.
- **D.** Implied vol / skew carry information; options are also a defined-risk implementation. Deferred until futures are understood.
- **E.** ATM IV, 25Δ risk reversal, IV − RV (variance risk premium), IV term structure.
- **F.** Options settlement prices by strike/expiry (CME DataMine — paid), or vendor IV surfaces.
- **G.** Using the spot-equity Black-Scholes model; ignoring that the option's underlying month may differ from the front month.

---

## B. Contract mechanics

### 5. Futures contract (identity)
- **A.** Each futures contract is one specific delivery month: "Gold Dec-2026" and "Gold Feb-2027" are different instruments.
- **B.** Identified by root + month code + year (CME month codes: F G H J K M N Q U V X Z = Jan…Dec). Each has its own price, volume, OI, first notice day, last trade day. [FACT]
- **C.** `GCZ26` = COMEX gold Dec 2026; `CLF27` = NYMEX WTI Jan 2027.
- **D.** All correct backtesting starts from per-contract series. "Gold futures price" without a month is ambiguous.
- **E.** Primary key: (`root`, `contract_month`) → see 03 data architecture.
- **F.** Contract calendar: listing date, FND, LTD, settlement type, per contract.
- **G.** Storing only a "continuous" series and losing the contract identity → impossible to reconstruct rolls, carry, or audit.

### 6. Contract specification
- **A.** The rulebook for a contract: what, how much, which quality, where, when, how priced.
- **B.** Fields: underlying & grade, unit, size, price quotation, tick, listed months, trading hours, daily limits, termination rule, settlement method, delivery location/procedure, position limits. Published by exchange; can change over time. [FACT]
- **C.** NYMEX WTI (CL): 1,000 bbl, light sweet crude delivered at Cushing, Oklahoma; physical delivery (or EFRP). `[V-S: NYMEX Rulebook Ch. 200]`
- **D.** Specs define tick value, P&L, delivery risk, expiry dates — everything mechanical in a backtest.
- **E.** Static/time-versioned attributes table (`commodity_contracts`, valid_from/valid_to).
- **F.** Exchange rulebook chapters (CME Rulebook Ch. per product; MCX contract launch circulars).
- **G.** Assuming specs are static. They change (e.g. MCX revises lot sizes, CME adds weekly/micro contracts, price-limit rules change). Version them.

### 7. Contract size
- **A.** Quantity of the commodity per contract.
- **B.** Multiplier converting quoted price to money. [FACT] Examples: GC 100 troy oz `[V-S]`; SI 5,000 oz `[V-S]`; HG 25,000 lb `[V-2]`; CL 1,000 bbl `[V-S]`; NG 10,000 MMBtu `[V-S]`; LME Copper/Aluminium 25 t `[V-S: lme.com]`; MCX Gold 1 kg, quoted ₹/10 g `[V-2]`; MCX Crude 100 bbl `[VERIFY]`; MCX Natural Gas 1,250 MMBtu (Mini 250) `[V-2]`.
- **C.** GC at $2,600/oz × 100 oz = $260,000 notional per contract.
- **D.** Determines position-sizing granularity. Big contract sizes make small accounts unable to size positions precisely (minis/micros exist for this).
- **E.** `multiplier` field; used in P&L = Δprice × multiplier × contracts.
- **F.** Spec history incl. changes.
- **G.** Mixing quote unit and contract unit (MCX gold is quoted per 10 g but the lot is 1 kg → multiplier 100).

### 8. Tick size
- **A.** Smallest allowed price move.
- **B.** Minimum price fluctuation set by exchange. [FACT] e.g. GC $0.10/oz `[V-S]`; CL $0.01/bbl `[VERIFY]`; NG $0.001/MMBtu `[V-S: NYMEX Rulebook Ch. 220]`; HG $0.0005/lb `[V-2]`.
- **C.** CL can go from 75.40 to 75.41, not 75.405.
- **D.** Sets the floor on bid-ask spread → minimum transaction cost. Matters for short-horizon strategies.
- **E.** `tick_size`; `spread_in_ticks`; cost model = k × tick_value.
- **F.** Spec; ideally historical bid-ask (intraday) to calibrate k.
- **G.** Assuming 1-tick fills in fast markets or illiquid deferred months.

### 9. Tick value
- **A.** Money gained/lost per contract for a one-tick move.
- **B.** tick_value = tick_size × multiplier. [FACT] GC $10 `[V-S]`; CL $10 `[VERIFY]`; NG $10 (derived from V-S tick × size); HG $12.50 `[V-2]`; SI (0.005 × 5,000) $25 `[V-S]`; MCX Gold ₹1/10 g × 100 = ₹100 `[V-2]`; MCX Natural Gas ₹0.10 × 1,250 = ₹125 `[V-2]`.
- **C.** A 50-tick adverse move in CL = $500 per contract.
- **D.** Converts price noise into money; basis of slippage/cost modelling.
- **E.** `tick_value` (currency-tagged).
- **F.** Spec history.
- **G.** Forgetting the currency (₹ vs $) when combining MCX and CME in one portfolio.

### 10. Notional value
- **A.** Total market value controlled by one contract.
- **B.** notional = price × multiplier (× FX if converting). Position risk should be measured on notional and volatility, not margin. [FACT]
- **C.** CL at $75 × 1,000 = $75,000 notional, while initial margin might be ~$6,000.
- **D.** Volatility-targeted sizing (standard in CTA research) uses notional × vol.
- **E.** `notional_t`; `risk_t = notional_t × σ_t`; contracts = target_risk / (notional × σ).
- **F.** Prices, specs, FX.
- **G.** Sizing by margin ("I can afford 5 contracts") → extreme and unequal risk across commodities.

---

## C. Margin & leverage

### 11. Initial margin
- **A.** Good-faith deposit required to open a futures position.
- **B.** Set by the clearing house (CME SPAN/SPAN 2; MCX uses SPAN + extreme-loss and additional margins set under SEBI framework) to cover a high-percentile 1–2-day loss. It is **collateral, not a cost**; changes with volatility. [FACT]
- **C.** Clearing raises CL margin after a volatility spike (e.g. Mar 2020, Mar 2022).
- **D.** Determines capital efficiency and margin-call risk; margin hikes can force deleveraging (a possible price-impact channel [HYPOTHESIS]).
- **E.** `margin_pct = IM / notional`; margin change events as features.
- **F.** Historical margin files (CME publishes current; history is patchy; MCX circulars). **[OPEN]** availability of clean historical margin series.
- **G.** Treating margin as the capital "at risk"; assuming margin is constant in backtests.

### 12. Maintenance margin
- **A.** Minimum equity to keep a position open; fall below → margin call back to initial.
- **B.** CME: maintenance < initial for speculators. Indian exchanges compute margins somewhat differently (SPAN + ELM; mark-to-market settled daily; peak-margin rules). [FACT, MCX detail → 14]
- **C.** IM $6,000, MM $5,500; a $600 loss triggers a call to restore $6,000.
- **D.** Cash management/funding rules for the live system; not usually a signal.
- **E.** Used in simulation of cash/margin utilisation.
- **F.** Spec / clearing circulars.
- **G.** Ignoring it in portfolio simulation → strategies that look fine but would have been liquidated.

### 13. Mark-to-market (MTM)
- **A.** Every day, gains and losses are paid in cash based on the settlement price.
- **B.** Daily variation margin = (settle_t − settle_{t−1}) × multiplier × position. Uses the **official settlement price**, which is not the last trade. [FACT]
- **C.** Long 1 GC: settle moves 2,600 → 2,585 → $1,500 debited today.
- **D.** Backtests should use settlement prices (consistent with MTM); path-dependence of cash matters.
- **E.** Daily P&L series per contract; settlement vs close difference as data-quality check.
- **F.** Daily settlement prices per contract.
- **G.** Mixing "close" (last trade) and "settle" across vendors; using different session cut-offs between markets (e.g. MCX close ≈ 23:30 IST vs CME settle 13:30 ET) when computing cross-market correlations.

### 14. Leverage
- **A.** Controlling large notional with small capital.
- **B.** Implicit leverage = notional / margin (often 10–20×). **Economically relevant leverage** = portfolio notional / account equity, which the trader chooses. A fully collateralised futures position (notional = equity in T-bills) has no leverage. [FACT]
- **C.** $100k account, 1 GC ($260k notional) = 2.6× economic leverage regardless of the $15k margin.
- **D.** Futures returns in research are usually computed **unlevered / fully collateralised**: excess return over cash (see 24 and 02 §B.6).
- **E.** `gross_leverage = Σ|notional| / equity`.
- **F.** Prices, specs, equity curve.
- **G.** "Commodities are risky because of leverage" — leverage is a choice; volatility is the property of the commodity.

---

## D. Contract lifecycle

### 15. Expiry
- **A.** The date the contract stops trading.
- **B.** Last Trading Day (LTD) set by spec rule. Before LTD, physically settled contracts usually have a **First Notice Day (FND)** when shorts can start delivering; speculators exit before FND. Examples `[VERIFY]`: CL terminates 3 business days before the 25th calendar day of the month preceding delivery; NG 3 business days before the first day of the delivery month; GC FND = last business day of the month before the delivery month; GC LTD = third-last business day of the delivery month (12:30 CT). [FACT] `[V-S: NYMEX Ch. 200, Ch. 220; COMEX Ch. 113; CME gold FAQ]`. MCX Gold expiry: 5th of the contract month (or previous trading day) `[V-2]`.
- **C.** CL Dec contract stops trading around 19–20 November.
- **D.** Defines roll dates; liquidity migrates *before* expiry; prices can behave abnormally in the last days (April 2020 WTI at −$37.63 on 20 Apr 2020, day before expiry).
- **E.** `days_to_expiry`, `days_to_FND`; roll-date flags.
- **F.** Per-contract FND/LTD calendar (historical, since rules change).
- **G.** Rolling on LTD instead of before FND; using an expiry rule from today on 1990s contracts.

### 16. Settlement
- **A.** (i) Daily official price; (ii) how the contract is finally closed out at expiry.
- **B.** Daily settlement price determined by exchange methodology (VWAP in a closing window, etc.). Final settlement = physical delivery or cash against an index. [FACT]
- **C.** NG daily settlement: active month = VWAP of CME Globex trades 14:28:00–14:30:00 ET; other months settled from calendar-spread VWAPs in the same window; fallbacks if no trades `[V-S: CME NG Daily Settlement Procedure]`. CME energy settles at 14:30 ET, so CME-vs-MCX comparisons must align to this time.
- **D.** Defines the price series for backtests and the obligations at expiry.
- **E.** `settle`, `settlement_type`.
- **F.** Settlement method docs.
- **G.** See 13 (close vs settle).

### 17. Physical settlement
- **A.** At expiry, sellers deliver real commodity; buyers pay and receive it.
- **B.** Delivery via exchange-approved warehouse receipts/warrants/pipeline transfer, approved brands/refiners, delivery points. [FACT] Examples: CL (Cushing), GC (COMEX-approved vaults, bars of approved refiners), LME (warrants in LME-licensed warehouses), MCX Gold (compulsory delivery, 995 purity) `[V-2]`; GC minimum 995 fineness `[V-S]`.
- **C.** A speculator holding long CL into expiry must take 1,000 bbl at Cushing — impossible without storage → forced selling (2020).
- **D.** Physical settlement ties futures to physical supply/demand (convergence). It is why curve shape tells you about physical scarcity.
- **E.** Delivery notices / stocks as features (COMEX delivery reports, LME warrant data).
- **F.** CME daily delivery notices; COMEX warehouse stocks; LME stocks & cancelled warrants.
- **G.** Ignoring delivery risk in backtests that hold contracts to expiry.

### 18. Cash settlement
- **A.** At expiry, no delivery; difference is paid in cash vs a reference price.
- **B.** Final settlement = index/reference price (e.g. ICE Brent settles against ICE Brent Index; MCX Crude and MCX Natural Gas final settlement ("Due Date Rate") = NYMEX CL / NG front-month settlement on the MCX contract's last trading day × last available RBI USDINR reference rate, rounded to tick `[V-S: MCX contract-spec PDFs]`). [FACT] Consequence: MCX crude also went negative on 20 Apr 2020 (April contract settled at −₹2,884/bbl, per Business Standard/PTI).
- **C.** MCX Crude long at expiry receives/pays difference vs final settlement price.
- **D.** Removes delivery risk but introduces **reference-price risk** and different convergence behaviour.
- **E.** `settlement_type`; final settlement reference.
- **F.** Spec; reference series.
- **G.** Assuming cash-settled contracts converge to the same price as the physical benchmark at the same time (MCX contracts expire on different dates from CME).

### 19. Delivery
- **A.** Physical handover process.
- **B.** Notice → allocation (often to oldest long) → payment → title transfer (warrant/receipt). Delivery grade, location optionality usually belongs to the short ("cheapest-to-deliver"). [FACT]
- **C.** LME short chooses which warehouse/brand to deliver → long can receive metal in an unwanted location (queues: e.g. Vlissingen/Detroit aluminium queues ~2012–2014).
- **D.** Delivery frictions drive spreads and basis distortions.
- **E.** Delivery volumes; queue lengths; cancelled-warrant ratios.
- **F.** Exchange delivery reports; LME stock reports.
- **G.** Ignoring quality/location optionality when interpreting curve.

### 20. Contract rollover
- **A.** Closing the expiring contract and opening the next one to keep exposure.
- **B.** Roll = sell near / buy far (for a long). The P&L of a long-term futures strategy = sum of within-contract P&L across all held contracts. The *price gap* between contracts at the roll is **not** P&L. Rolls cost a spread (calendar spread trade) and require a schedule (e.g. fixed days before FND, volume/OI crossover). [FACT] → deep dive 02 §B, 11.
- **C.** Long GCZ26 at 2,600, roll to GCG27 at 2,615: you did not gain or lose $15/oz from the roll itself.
- **D.** Most data errors in commodity backtests come from mishandled rolls.
- **E.** Roll calendar; roll yield; roll cost.
- **F.** Per-contract prices around roll dates; volume/OI by contract.
- **G.** Using a naive "front-month continuous" series and treating roll gaps as returns.

---

## E. Pricing & curve (short — deep dive in 02 §B and 11)

### 21. Basis
- **A.** Difference between spot (or local cash) price and a futures price.
- **B.** basis = S − F (sign convention varies; document it). Goes to ~0 at expiry for physically settled contracts (convergence), except when delivery frictions break it. Also used for **location/quality basis** (e.g. WTI Midland vs Cushing; MCX vs international). [FACT]
- **C.** Spot gold 2,590, Dec futures 2,610 → basis −20.
- **D.** Basis risk = hedge imperfect. MCX-vs-COMEX is effectively a basis trade (→ 14).
- **E.** `basis_t`, `basis_t / S_t` annualised; z-score.
- **F.** Spot + futures per contract, aligned timestamps.
- **G.** Comparing prices sampled at different times/timezones.

### 22. Cost of carry
- **A.** Cost of holding the physical until a future date — explains why futures usually sit above spot for storable goods.
- **B.** Theory of storage [THEORY] (Kaldor 1939; Working 1949; Brennan 1958): F(t,T) = S·e^{(r + u − y)(T−t)}, r = financing, u = storage, y = convenience yield. Arbitrage enforces an **upper bound** (full carry) for storable goods; there is no symmetric lower bound because you cannot short physical you don't own → backwardation can be deep.
- **C.** Gold: r = 4.5%, storage ≈ 0.1%, y ≈ 0 → 1-year future ≈ spot × e^{0.046}.
- **D.** Lets you decompose the curve into "mechanical" (rates) and "informational" (convenience yield) parts.
- **E.** Implied carry = ln(F2/F1)/(T2−T1); **implied convenience yield** = r + u − implied carry.
- **F.** Multiple contract prices, risk-free curve (SOFR/T-bill), storage estimates.
- **G.** Calling all contango "bearish". For gold, contango ≈ interest rates — it's mechanical, not a signal.

### 23. Storage cost
- **A.** Cost to warehouse/insure the commodity.
- **B.** Physical cost u; small for precious metals (high value density), large for crude/natural gas, constrained by **capacity** (NG storage caverns, Cushing tank space). When storage nears full, contango can blow out beyond normal carry. [FACT/THEORY]
- **C.** 2020: tank space scarcity → super-contango in WTI.
- **D.** Storage scarcity regimes produce extreme curve and price behaviour.
- **E.** Inventory as % of capacity (Cushing utilisation, NG storage vs capacity).
- **F.** EIA storage/capacity data.
- **G.** Assuming storage costs are constant/linear.

### 24. Financing cost
- **A.** Interest you forgo (or pay) by tying money up in the commodity.
- **B.** Component r of carry; in futures returns, the **collateral return** (T-bill yield on cash backing the position). Total return of a collateralised futures index = excess (futures) return + collateral return. [FACT]
- **C.** 2022–24: 5% rates → much of gold's contango = rates.
- **D.** Compare strategies on **excess return** (futures P&L only) to avoid crediting yourself for T-bill income; or add collateral explicitly. In India, idle margin can earn via approved collateral/liquid funds — a design choice. [OPEN for MCX]
- **E.** `r_t` (3M T-bill/SOFR; for India 91-day T-bill/MIBOR).
- **F.** FRED (DTB3, SOFR), RBI.
- **G.** Comparing commodity futures excess returns to equity total returns.

### 25. Convenience yield
- **A.** The benefit of physically having the commodity now (e.g. keeping a refinery running), which can make spot worth more than futures.
- **B.** Implied, not observed: y = r + u − implied carry. Rises when inventories are low [THEORY + EMPIRICAL: Fama & French 1987; Gorton, Hayashi & Rouwenhorst 2013 find curve slope and inventory are linked].
- **C.** Copper inventory squeezes → spot premium (cash-to-3M backwardation on LME).
- **D.** Core concept linking curve to fundamentals; the curve is a free, daily inventory proxy.
- **E.** Implied convenience yield series; change in it.
- **F.** Curve + rates + storage assumption.
- **G.** Treating it as a measurable quantity rather than a residual (garbage-in if storage/rates are wrong).

### 26. Contango
- **A.** Later-dated futures priced higher than nearer ones (upward-sloping curve).
- **B.** F(T2) > F(T1) for T2 > T1. Normal for well-supplied storables; a **long** rolled position tends to lose the slope as each contract "rolls down" toward spot, *if the curve shape is stable* (negative roll yield). [FACT/THEORY] → 02 §B, 11.
- **C.** NG in spring: each next-month contract higher.
- **D.** A buy-and-roll long in persistent contango can lose money even if spot is flat (e.g. USO in 2009/2020).
- **E.** slope = ln(F2/F1)·(365/Δdays); sign → regime flag.
- **F.** Front + second (+ more) contracts daily.
- **G.** "Contango = bearish signal". Contango predicts negative *roll* return; it does not by itself predict spot direction. [OPEN] whether slope predicts total futures returns in our 6 commodities.

### 27. Backwardation
- **A.** Later-dated futures priced lower than nearer ones (downward-sloping curve).
- **B.** F(T2) < F(T1). Associated with tight current supply/low inventory and high convenience yield. Long rolled position earns positive roll yield if shape persists. Keynes' "normal backwardation" (1930) [THEORY] posits futures below expected spot due to hedging pressure — *different* concept from curve backwardation.
- **C.** Crude in 2022: steep backwardation after supply shock.
- **D.** The carry strategy (Koijen et al. 2018 [EMPIRICAL]) is long backwardated / short contango across commodities.
- **E.** Same slope variable; % of time in backwardation.
- **F.** As 26.
- **G.** Confusing curve backwardation with Keynes' normal backwardation.

### 28. Futures curve
- **A.** All prices of the same commodity across delivery months at one date.
- **B.** Snapshot F(t, T_1…T_n). Shape (level, slope, curvature) changes daily. [FACT]
- **C.** CL curve on a date: 75.2, 74.8, 74.4, … (backwardated).
- **D.** The richest market-implied, daily, near-free fundamental signal available.
- **E.** Level, slope, curvature (PCA on log-curve), constant-maturity points.
- **F.** Daily settlements for every listed contract.
- **G.** Using illiquid far-month settlements (often model/marked, stale).

### 29. Term structure
- **A.** The *shape* of the curve and how it changes over time.
- **B.** Often expressed in constant-maturity terms (interpolate 1M, 3M, 6M, 12M) so shapes are comparable across dates. [FACT] → 11.
- **C.** "WTI 1M–12M spread moved from +$8 backwardation to −$2 contango in 6 weeks."
- **D.** Changes in term structure may carry information beyond levels. [HYPOTHESIS]
- **E.** CM slopes, Δslope, curve PCA factors.
- **F.** Full-curve history.
- **G.** Interpolating across a seasonal curve (NG) as if it were smooth → artefacts.

### 30. Calendar spreads
- **A.** Simultaneously long one month and short another of the same commodity.
- **B.** Spread price = F(T1) − F(T2). Exchanges list spreads as instruments; margins are lower (offsets). Spread P&L ≈ change in curve slope, largely hedged against level. [FACT]
- **C.** Long CL Dec / short CL Jun = bet on tightening (backwardation rising).
- **D.** Separate tradeable strategy class; also the *roll trade* itself.
- **E.** Spread series; spread z-scores.
- **F.** Per-contract prices (synchronous).
- **G.** Computing spread "returns" as % of a near-zero spread price.

---

## F. Market activity

### 31. Open interest (OI)
- **A.** Number of contracts currently open (not yet closed or delivered).
- **B.** Each contract has a long and a short; OI counts each pair once. Rises when new positions open, falls when closed. Per contract and aggregate. Reported with a 1-day lag on CME. [FACT]
- **C.** OI in GC Dec falls as traders roll into Feb; aggregate may be unchanged.
- **D.** Liquidity indicator; roll timing; aggregate OI growth has been studied as a predictor (Hong & Yogo 2012 [EMPIRICAL]).
- **E.** Aggregate OI, ΔOI, OI-weighted roll indicator, OI share by contract.
- **F.** Per-contract OI daily (note publication lag).
- **G.** Look-ahead: today's OI is known tomorrow. Interpreting ΔOI at a single contract level during roll periods.

### 32. Volume
- **A.** Number of contracts traded in a period.
- **B.** Per-contract and aggregate; electronic + pit/block/EFP may be reported separately. [FACT]
- **C.** CL is among the most heavily traded commodity futures in the world; exact average daily volume to be measured from data `[VERIFY]` rather than quoted.
- **D.** Liquidity, cost estimation, roll timing. Equity "volume confirmation" ideas are *not* obviously transferable (volume is distorted by roll periods). [HYPOTHESIS to test in 15]
- **E.** Aggregate volume across contracts; volume share by contract; volume z-score ex-roll windows.
- **F.** Per-contract daily volume.
- **G.** Using a continuous series' volume which jumps at roll; ignoring rolling-related volume spikes.

### 33. Positioning
- **A.** Who is long/short and how much.
- **B.** Aggregate holdings by trader category (from COT), ETF holdings, dealer positioning. Positioning is a *state*, not a flow; its predictive value is disputed. [FACT/OPEN]
- **C.** Managed money net long gold at multi-year high.
- **D.** Possible crowding/contrarian or trend-confirming signal. → 10.
- **E.** Net position / OI, z-scores, percentiles, Δ over k weeks.
- **F.** CFTC COT history (Legacy from 1986, Disaggregated from 2006), ETF holdings.
- **G.** Assuming "extreme = reversal" without testing; release-lag look-ahead.

### 34. COT (Commitments of Traders)
- **A.** Weekly CFTC report of futures positions by trader type.
- **B.** Positions as of **Tuesday close**, released **Friday 15:30 ET** (delayed by holidays) `[V-S: cftc.gov]`. **Watch:** CFTC request for comment (91 FR 24207, 5 May 2026) is reviewing COT *frequency and content* — the schema and history may change; see OPEN-1.6. Reports: Legacy (commercial/non-commercial), Disaggregated (producer/merchant, swap dealers, managed money, other reportables), TFF (financial futures). Futures-only and futures+options versions. Covers US exchanges only — **not LME, not MCX** (LME publishes its own COTR since 2014; SEBI/MCX publish limited participant-wise OI data `[VERIFY]`). [FACT] → 10.
- **C.** Friday's report describes positions held three days earlier.
- **D.** Only systematic, long-history positioning dataset.
- **E.** As 33; must timestamp to release time.
- **F.** CFTC historical compressed files (cftc.gov).
- **G.** Aligning COT to Tuesday instead of the Friday release (classic look-ahead bias). Category labels are self-classified and can be misleading (swap dealers hold index investor exposure).

---

## G. Physical fundamentals

### 35. Seasonality
- **A.** Regular calendar patterns in demand, supply, or prices.
- **B.** Fundamental seasonality (NG heating/cooling, gasoline driving season, refinery maintenance, Indian festival/wedding gold demand) is real [FACT]; **price** seasonality should be largely priced into the curve (seasonal futures prices) and is a weak/contested predictor [OPEN]. → 12.
- **C.** NG winter contracts trade at a premium to summer contracts every year — that is curve seasonality, not a free return.
- **D.** Must separate "seasonal fundamentals" (in curve) from "seasonal excess returns" (tradeable only if not priced).
- **E.** Month-of-year dummies, seasonal inventory deviation, seasonal vol.
- **F.** Long per-contract history (≥20 years) for meaningful tests; fundamentals data.
- **G.** Plotting average monthly returns over 15 years and calling it an edge (tiny samples, multiple testing).

### 36. Inventory
- **A.** How much commodity is stored.
- **B.** Buffer between supply and demand; low inventories → high convenience yield, backwardation, higher volatility [THEORY: storage; EMPIRICAL: Gorton, Hayashi & Rouwenhorst 2013]. Visible (exchange/government-reported) vs invisible (unreported, e.g. Chinese bonded stocks) inventories. [FACT]
- **C.** EIA weekly US crude stocks; LME/COMEX/SHFE metal stocks; EIA NG storage.
- **D.** Most direct observable fundamental for energy/base metals. Not meaningful for gold (above-ground stocks ≈ 60+ years of mine supply).
- **E.** Inventory deviation from 5-yr seasonal average; surprise vs consensus; days-of-cover.
- **F.** EIA (weekly, long history), LME/COMEX/SHFE stocks, point-in-time vintages.
- **G.** Revisions and partial coverage (exchange stocks ≠ total stocks); using revised data as of first release date.

### 37. Supply
- **A.** How much is available to the market.
- **B.** Supply = production + recycling/scrap + inventory drawdown + net imports. Short-run supply is inelastic for mined metals (mines take 10+ years) and oil (shale is the more elastic exception, months). [FACT/THEORY]
- **C.** Gold supply ≈ mine production + recycling (World Gold Council).
- **D.** Supply shocks drive large moves (disruptions, OPEC+ cuts).
- **E.** Supply growth YoY; disruption events (dummy).
- **F.** EIA, IEA (paid), WGC, ICSG (copper), IAI (aluminium), USGS.
- **G.** Using annual data revised years later as if known in real time.

### 38. Demand
- **A.** How much is consumed or bought.
- **B.** Industrial/consumption demand (energy, base metals) vs asset/store-of-value demand (gold, partly silver). Driven by GDP, industrial production, prices, policy, China. [FACT/THEORY]
- **C.** Kilian (2009) decomposes oil price shocks into supply, aggregate demand, and oil-specific demand. [EMPIRICAL]
- **D.** Demand shocks are usually observed with lag → price often leads data.
- **E.** PMIs, IP, China imports, ETF flows, central-bank purchases.
- **F.** Macro data with release dates (point-in-time).
- **G.** Using data that price had already discounted.

### 39. Production
- **A.** Output from mines, wells, smelters.
- **B.** Primary supply; mine vs refined production differ (copper concentrate vs cathode). [FACT]
- **C.** US crude field production (EIA weekly estimate + monthly 914 survey).
- **D.** Medium-term driver; weekly estimates are noisy/rounded.
- **E.** Production YoY, surprises.
- **F.** EIA, USGS, ICSG, IAI, WGC.
- **G.** Mixing estimate and survey series.

### 40. Consumption
- **A.** Actual use.
- **B.** "Apparent consumption" = production + imports − exports − Δinventory — an estimate with errors. [FACT]
- **C.** China apparent copper consumption.
- **D.** Real demand indicator, but lagged and revised.
- **E.** Apparent consumption YoY.
- **F.** National statistics, ICSG, EIA product supplied.
- **G.** Treating apparent consumption as measured consumption.

### 41. Imports
- **A.** Commodity entering a country.
- **B.** Customs data (monthly); China imports are a key demand proxy for copper ore/concentrate, crude, and India's gold imports drive local premiums/discounts. [FACT]
- **C.** India gold imports surge pre-festival; China crude imports.
- **D.** Demand proxy; policy-driven (import duty changes in India alter MCX gold vs global).
- **E.** Imports YoY, deviation from seasonal norm.
- **F.** China GACC, India Ministry of Commerce/DGCI&S, EIA.
- **G.** Imports ≠ consumption (stockpiling, re-exports).

### 42. Exports
- **A.** Commodity leaving a country.
- **B.** Same as imports, other side; US crude/LNG exports since 2015–16 transformed US balances. [FACT]
- **C.** US LNG exports link Henry Hub to global gas.
- **D.** Structural break risk in historical relationships.
- **E.** Exports, export capacity utilisation.
- **F.** EIA, customs.
- **G.** Using pre-2016 NG/crude relationships without regime break.

### 43. Refining
- **A.** Turning crude into products (oil); also smelting/refining for metals.
- **B.** Oil: refinery runs/utilisation drive crude demand; **crack spread** = product value − crude cost. Metals: smelters convert concentrate to metal; TC/RCs = fees smelters charge miners (low TC/RC = tight concentrate). [FACT]
- **C.** 3-2-1 crack spread (3 crude → 2 gasoline + 1 distillate).
- **D.** Refining margins and utilisation tell you about crude demand; TC/RCs about copper concentrate tightness. → 05, 06.
- **E.** Crack spread levels/z; utilisation vs seasonal norm; TC/RC.
- **F.** RBOB/HO/CL futures; EIA utilisation; TC/RC (benchmark annual + spot assessments — mostly paid).
- **G.** Using spot TC/RC data you don't actually have point-in-time.

### 44. Transportation
- **A.** Moving commodities from where produced to where used.
- **B.** Pipelines, tankers, rail; bottlenecks create location spreads (WTI–Brent, Henry Hub vs European TTF). Freight rates affect arbitrage. [FACT]
- **C.** 2011–2013: WTI traded >$20 below Brent due to Cushing pipeline bottleneck.
- **D.** Explains why "the" price of oil/gas isn't unique; important for choosing benchmarks.
- **E.** Location spreads (Brent−WTI), freight indices.
- **F.** Futures for both benchmarks; Baltic indices (paid).
- **G.** Treating Brent and WTI as interchangeable in long histories.

### 45. Warehousing
- **A.** Storage facilities, especially exchange-approved ones.
- **B.** Exchange warehouse rules determine deliverable supply; LME load-out rules and queues, cancelled warrants (metal earmarked for removal) are signals of physical demand. [FACT]
- **C.** LME cancelled warrants jump → metal being withdrawn → often tightening cash-3M spread.
- **D.** Warehouse mechanics can dominate short-term spreads (squeezes).
- **E.** Cancelled-warrant ratio; on-warrant stocks; Δ.
- **F.** LME daily stocks (licensed), COMEX daily stocks (free), SHFE weekly.
- **G.** Reading exchange stocks as total market inventory.

---

## H. Participants

### 46. Physical vs financial participants
- **A.** Physical: produce/consume/handle the commodity. Financial: trade for return or as part of portfolios.
- **B.** Since ~2004 "financialisation" (index investors, ETFs, CTAs) increased co-movement across commodities and with equities [EMPIRICAL: Tang & Xiong 2012; disputed in magnitude]. [FACT/EMPIRICAL]
- **C.** GLD and other ETFs hold large gold stocks; CTAs trade all liquid futures by trend.
- **D.** Regime break risk: pre-2004 data may represent a different market.
- **E.** Regime dummy; ETF holdings; CTA trend proxies.
- **F.** ETF holdings history (issuer/WGC), COT.
- **G.** Pooling 1980–2025 without testing for structural breaks.

### 47. Hedgers
- **A.** Participants using futures to reduce existing price risk.
- **B.** Long physical (producers) hedge by shorting; short physical (consumers) by buying. Hedging pressure theory [THEORY: Keynes 1930; Hirshleifer; EMPIRICAL: de Roon, Nijman & Veld 2000] — speculators earn a premium for absorbing hedgers' risk.
- **C.** Airline buys jet fuel/heating oil futures; miner sells gold forward.
- **D.** Basis for risk-premium explanations of commodity returns.
- **E.** Hedging pressure = (commercial short − long)/OI.
- **F.** COT.
- **G.** Assuming all "commercials" hedge (they also speculate, and swap dealers are classified as commercial in Legacy COT).

### 48. Producers
- **A.** Those who extract/make the commodity.
- **B.** Natural short exposure; hedge more when prices are high / curve favourable (behaviour varies). OPEC+ is a producer cartel that sets policy. [FACT]
- **C.** Shale producers hedging into rallies.
- **D.** Producer hedging may cap rallies in deferred months [HYPOTHESIS].
- **E.** Producer/merchant short positions (Disaggregated COT).
- **F.** COT; company hedge disclosures (low frequency).
- **G.** Using producer positioning as a simple contrarian signal without testing.

### 49. Consumers
- **A.** Those who use the commodity as input.
- **B.** Natural short the commodity price (they pay); hedge by buying futures. Includes refiners, utilities, fabricators, jewellers. [FACT]
- **C.** Indian jeweller hedges gold inventory on MCX.
- **D.** Consumer behaviour (e.g. Indian/Chinese gold demand) is price-sensitive — demand falls on spikes [EMPIRICAL claims by WGC; to verify].
- **E.** Consumer-side positions (merchants in COT), local premiums/discounts.
- **F.** COT, WGC, local premium data.
- **G.** Same as 47.

### 50. Speculators
- **A.** Traders who take price risk without an underlying physical exposure.
- **B.** CTAs/managed futures (trend), discretionary macro, prop/HFT, retail. Provide liquidity/risk-bearing; often trend-following in aggregate. Managed Money in Disaggregated COT. [FACT]
- **C.** Managed money adds to gold longs as price breaks out.
- **D.** We are speculators: our edge must come from risk premia, behavioural patterns, or information processing that others under-exploit — not from "commodities going up".
- **E.** MM net position, Δ, z-scores.
- **F.** COT.
- **G.** Believing speculators are the "dumb money" or "smart money" without evidence.

---

## I. Phase 1 summary — five ideas that matter most

1. **You trade contracts, not commodities.** Every return series must be built from per-contract data with an explicit roll rule (5, 15, 20).
2. **Futures excess return ≈ spot price change + roll yield.** Roll yield depends on curve shape; it can dominate long-run returns [EMPIRICAL: Erb & Harvey 2006]. Spot charts are not tradeable returns (1, 26, 27).
3. **The curve is information.** Carry, storage, convenience yield and inventories are linked by the theory of storage (22–25, 36). This is the main structural difference from equities.
4. **Timing of data matters.** COT (Tue→Fri), EIA weekly (Wed/Thu), OI (T+1), macro releases with revisions — everything must be point-in-time (31, 34, 36).
5. **Risk = notional × volatility, not margin.** Size by volatility; leverage is a choice (10, 14).

**Open research questions created in Phase 1**
- [OPEN-1.1] Availability/cost of clean historical margin data (CME, MCX).
- [OPEN-1.2] How much of each core commodity's long-run futures return came from roll yield vs spot change? (to compute in Phase 3/14)
- [OPEN-1.3] Does the curve slope predict total futures returns in our six core commodities individually (time-series), not only cross-sectionally?
- [OPEN-1.4] What MCX participant/positioning data exists and from when?
- [OPEN-1.5] What is the best free/low-cost source of contract-level history (see 02 §B.8 and SOURCE_REGISTER)?
- [OPEN-1.6] Outcome of the CFTC 2026 COT program review (frequency/content changes) and its effect on historical comparability.
