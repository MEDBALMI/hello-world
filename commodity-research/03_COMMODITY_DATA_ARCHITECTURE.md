# 03 — Commodity Data Architecture (Phase 18, design v1.0)

> Status: **design only, no implementation.** Target: PostgreSQL. Concepts → 01; series methodology → 02 Part B; curve features → 11.
> Timings and rules marked [VERIFY] are typical values to confirm when each source is ingested. They are deliberately not researched now.

---

## 1. Design principles

1. **The contract-day is the atomic unit.** All prices are stored per contract (root + delivery month / prompt), never only as continuous series.
2. **Raw is immutable.** Every vendor file is stored as received, with a batch ID. Corrections create new versions; nothing is overwritten.
3. **Separate raw → clean → derived.** Clean data carries quality flags. Derived data is reproducible from clean data plus versioned methods.
4. **Point-in-time everywhere.** Every non-price observation carries observation period, release timestamp, and vintage (§6).
5. **Research series ≠ P&L series** (02 §B.5). They live in different tables and are built by different, versioned processes.
6. **Global ≠ MCX.** CME, ICE, LME and MCX contracts are separate roots linked only through `commodity_id`.
7. **UTC timestamps, exchange-local trade dates.** `timestamptz` in UTC for every event time; `trade_date` = the exchange's official session/settlement date.
8. **Versioned specifications.** Contract specs, calendars, roll policies and cost models have validity periods or version IDs.

## 2. Layered architecture

```
 SOURCES ──► meta.ingestion_batch ──► raw.*  (as received, immutable, multi-source, multi-vintage)
                                        │ validation + source priority
                                        ▼
 ref.* (masters, specs, calendars) ──► clean.* (one golden row per key + quality flags)
                                        │ versioned methods (roll policy, CM method, cost model)
                                        ▼
                                      derived.* (roll schedule, research series, tradable returns, curve points, features)
                                        │
                                        ▼
                                      research / backtests (outside DB; results written to research.* run tables later)
 fund.*  pos.*  mkt.*  — point-in-time fundamental, positioning, FX/rates data, all with release timestamps
```

Schemas: `ref`, `meta`, `raw`, `clean`, `derived`, `fund`, `pos`, `mkt`.

## 3. Tables

Notation: **PK** primary key; FK foreign key; `ts` = timestamptz (UTC); `d` = date.

### 3.1 Reference (`ref`)

| Table | PK | Key fields | Notes / quality risks |
|---|---|---|---|
| `ref.exchange` | exchange_code | name, timezone (IANA), currency, settlement-time conventions | DST handling via IANA tz, never fixed offsets |
| `ref.commodity_master` | commodity_id | name, family (precious/energy/base), scope_tier (core/secondary), unit_physical | 11 commodities; agriculture absent by design |
| `ref.instrument_root` | root_id (e.g. `CME:GC`, `MCX:GOLDM`, `LME:CA`) | commodity_id FK, exchange_code FK, exchange_symbol, root_type (monthly_future / lme_prompt / spot_benchmark), is_benchmark, quote_currency, listed_from, delisted_on | Minis, micros and new contracts are separate roots |
| `ref.contract_spec_version` | (root_id, valid_from) | valid_to, multiplier, quote_unit, tick_size, tick_value, settlement_type (physical/cash), delivery_terms, listed_months, **liquid_months**, price_limit_rule, trading_hours, fnd_rule, ltd_rule, final_settlement_rule, source_ref | Specs change; P&L uses the version valid on the trade date (§5.10) |
| `ref.contract` | contract_id (surrogate); UNIQUE (root_id, contract_month, prompt_date) | contract_month (1st of delivery month), prompt_date (LME), listing_date, first_trade_date, **fnd**, **tender_start**, **ltd**, final_settlement_date, **delivery_risk_date** (computed, stored), settlement_type, spec_version_from FK | Dates stored **per contract**, as published, never recomputed from today's rule |
| `ref.symbol_map` | (source_id, vendor_symbol, valid_from) | contract_id FK / root_id FK | Vendor symbols differ and are recycled; mapping errors are a top risk |
| `ref.trading_calendar` | (exchange_code, d) | is_trading_day, session_open_ts, session_close_ts, settlement_ts, early_close, holiday_name | Needed to tell holidays from missing data |
| `ref.cftc_market_map` | (cftc_market_code, valid_from) | root_id FK | CFTC codes and names change over time |

### 3.2 Metadata (`meta`)

| Table | PK | Key fields |
|---|---|---|
| `meta.data_source` | source_id | name, type (exchange/vendor/agency), licence terms, priority per data type, url |
| `meta.ingestion_batch` | batch_id | source_id, retrieved_at_ts, file_name, checksum, row_count, parser_version |
| `meta.quality_event` | event_id | table_name, key (jsonb), d, rule_id, severity, description, action_taken, resolved_by, created_at_ts |
| `meta.method_version` | method_id | kind (roll_policy / cm_method / cost_model / validation_rules), params (jsonb), created_at, notes |

### 3.3 Raw (`raw`) — immutable

| Table | PK | Key fields | Frequency / source |
|---|---|---|---|
| `raw.contract_daily` | (source_id, batch_id, contract_id, trade_date) | open, high, low, close, settle, volume, open_interest, oi_reported_for_date, any vendor flags, as-received text | Daily; exchange files / vendors / MCX bhavcopy |
| `raw.spot_daily` | (source_id, batch_id, benchmark_id, obs_ts) | value, currency, fixing name (e.g. LBMA AM/PM) | Daily or intraday fixings |
| `raw.fund_release` | (source_id, batch_id, series_code, period_end, release_ts) | value as published | Weekly/monthly agency data |
| `raw.cot` | (source_id, batch_id, report_type, cftc_market_code, as_of_date) | all report columns as published | Weekly |

### 3.4 Clean (`clean`) — one golden row per key

| Table | PK | Key fields | Notes |
|---|---|---|---|
| `clean.contract_daily` | (contract_id, trade_date) | open, high, low, close, **settle**, volume, open_interest, oi_asof_date, settle_available_ts, chosen_source_id, quality_flags (bitmask), limit_state (none/up/down/locked), is_settle_only, is_stale | Main price table. `settle_available_ts` drives availability (§6) |
| `clean.spot_daily` | (benchmark_id, obs_ts) | value, currency, available_ts | LBMA, LME cash, Henry Hub cash, etc. |
| `clean.contract_intraday` *(later)* | (contract_id, bar_ts) | OHLCV, bid/ask samples | Only for cost calibration and execution studies |

### 3.5 Derived (`derived`) — reproducible, versioned

| Table | PK | Key fields | Stored or dynamic |
|---|---|---|---|
| `derived.roll_schedule` | (policy_id, root_id, roll_date) | from_contract_id, to_contract_id, tranche_weight, reason (calendar/liquidity), info_asof_date | **Stored** (fixed in advance) |
| `derived.held_contract` | (policy_id, root_id, trade_date) | contract_id, weight (blending during multi-day rolls), days_to_delivery_risk | Stored |
| `derived.tradable_return` | (policy_id, cost_model_id, root_id, trade_date) | contract_id(s), settle_prev, settle, point_change, multiplier, gross_return, roll_flag, roll_cost, net_return, return_basis (price / notional-floor), flags | **Stored**: the unit *realistic P&L* building block (02 §B.5) |
| `derived.cm_curve_point` | (cm_method_id, root_id, trade_date, tenor_days) | log_price, contract_lo_id, contract_hi_id, weight, extrapolated (must be false), quality | **Stored** (point-in-time) |
| `derived.research_series` | — | — | **Dynamic views/functions**: unadjusted, Panama, ratio, perpetual. Optional cache keyed by (method_id, data_snapshot_id) |
| `derived.feature_definition` | feature_id | formula text, inputs, method_ids, lookback, availability rule | |
| `derived.feature_value` | (feature_id, entity_id, as_of_date) | value, **available_ts**, input_snapshot_id | Stored; `available_ts` = max(input available_ts) + buffer |

Backtest outputs (positions, trades, integer-lot P&L) belong to a later `research.*` schema, one set per run. **Out of scope now.**

### 3.6 Fundamentals, positioning, market reference (`fund`, `pos`, `mkt`)

| Table | PK | Key fields | Notes |
|---|---|---|---|
| `fund.series_master` | series_id | source_id, name, category (inventory / production / consumption / trade / macro / etf / central_bank), commodity_id (nullable), region, units, frequency, seasonal_adj flag, release_rule text, revision_policy | Replaces separate wide tables for inventory, production, etc. |
| `fund.release` | release_id | series_id, period_start, period_end, **scheduled_release_ts**, **actual_release_ts**, release_ts_quality (exact / typical / assumed) | One row per publication event |
| `fund.observation` | (series_id, period_end, vintage_ts) | value, release_id FK, is_first_release, is_latest | **Point-in-time vintages**; backtests use first-release unless explicitly testing revisions |
| `pos.cot` | (report_type, root_id, as_of_date, futures_only_flag) | release_ts, category longs/shorts/spreads (disaggregated and legacy columns), open_interest, n_traders, report_version | Tuesday data, Friday release (§6) |
| `pos.exchange_positioning` *(later)* | (venue, root_id, d) | LME COTR, MCX participant-wise OI | OPEN-1.4 |
| `mkt.fx_fixing` | (pair, fixing_name, d) | value, fixing_ts, available_ts | e.g. RBI/FBIL USDINR reference rate for MCX conversion |
| `mkt.rate_daily` | (rate_id, d) | value, available_ts | US 3M T-bill / SOFR; India 91-day T-bill; TIPS real yields |
| `mkt.etf_holdings` | (etf_id, holdings_date) | ounces/tonnes, available_ts | Issuer data; date conventions vary |

### 3.7 Relationships (core)

```
commodity_master 1─* instrument_root 1─* contract_spec_version
                                  1─* contract 1─* clean.contract_daily
instrument_root 1─* roll_schedule / held_contract / tradable_return / cm_curve_point
commodity_master 1─* fund.series_master 1─* fund.release 1─* fund.observation
instrument_root 1─* pos.cot (via ref.cftc_market_map)
exchange 1─* trading_calendar ; exchange 1─* instrument_root
```

## 4. Mapping from the originally proposed table list

| Proposed | Design decision |
|---|---|
| commodity_master | `ref.commodity_master` + `ref.instrument_root` (commodity ≠ tradeable root) |
| commodity_contracts | `ref.contract` + `ref.contract_spec_version` |
| commodity_prices / _ohlcv / _volume / _open_interest | **Merged** into `clean.contract_daily` (same key; splitting adds joins and sync risk) |
| commodity_futures_curve | View over `clean.contract_daily` by date + `derived.cm_curve_point` |
| commodity_rolls | `derived.roll_schedule` + `derived.held_contract` |
| commodity_inventory / production / consumption / trade / etf_flows | `fund.series_master` categories + `fund.observation` (long format, vintages) |
| commodity_cot | `pos.cot` |
| commodity_macro / fx / rates | `fund.*` (released statistics) vs `mkt.*` (market fixings) |
| commodity_seasonality | **Not a table.** Seasonal features are `derived.feature_value` |
| commodity_features | `derived.feature_definition` + `derived.feature_value` |

## 5. Data-handling rules

### 5.1 Contract expiry
- Stored per contract (`ltd`, `final_settlement_date`) from exchange calendars, not inferred.
- Research and P&L series **never hold a contract into its final `buffer` days**. Expiry-day prices remain in clean data (they are real) but are flagged `in_expiry_window`.
- Cash-settled contracts (MCX crude/NG): delivery risk = LTD. Still roll before expiry, because liquidity and the reference-price mechanics dominate the last days.

### 5.2 First notice day / delivery risk
- `delivery_risk_date = min(fnd, tender_start, ltd)` per contract, stored.
- Holding is ineligible from `delivery_risk_date − buffer` (default buffer = 2 business days).
- MCX compulsory-delivery contracts: use the tender/delivery-period start and any pre-expiry margin escalation [OPEN-3.7].

### 5.3 Roll dates
- Policy ROLL-A (02 §B.6). Schedules are computed with information as of each date (lagged volume/OI) and **stored before use**.
- Roll executed at settlement on the roll date(s) via a spread trade. Cost = cost_model(spread ticks × tick_value + fees).
- If the target contract fails eligibility on the scheduled date (illiquid, limit-locked, missing), roll the next eligible day. If none is eligible before `delivery_risk_date − buffer`, force the roll on the last eligible day and log a quality event.

### 5.4 Illiquid contracts
- **Liquid months** per root are defined in the spec (11 §2) and checked empirically.
- Liquidity filter on **t−1** data: volume ≥ V_min and OI ≥ OI_min (absolute, plus share of root total).
- Settlements on zero-volume days are often exchange-derived from spreads. They are flagged `is_settle_only`. Allowed for curve features with a quality weight; positions are never opened in them.
- Far-dated curve points beyond the last liquid contract are **not used** (no extrapolation).

### 5.5 Missing data
- Distinguish **holiday** (calendar closed) from **missing** (calendar open, no row) from **partial** (row without settle).
- **Never forward-fill or interpolate prices for P&L.** If the held contract's settle is missing, carry the position. The next valid settle gives a multi-day return; flag it.
- Display or feature series may forward-fill only with an explicit flag and max gap (e.g. 3 days). Longer gaps → feature is NULL.
- Cross-source fill (secondary vendor) is allowed if the source passes the cross-validation rule (§5.9); the source is recorded.

### 5.6 Contract changes (symbols, new contracts, redesigns)
- Vendor symbol changes are handled in `ref.symbol_map` with validity dates.
- A redesigned contract (different underlying, grade, location, reference price, or settlement type) becomes a **new root**. Series spanning roots carry a `structural_break` flag, and tests must run with and without the pre-break period.
- New mini/micro contracts are separate roots. They are not stitched into the main contract's history.

### 5.7 Negative and near-zero prices
- Stored as reported (e.g. NYMEX CL and MCX crude, 20 Apr 2020). Validation allows negatives only for roots flagged `allows_negative`.
- Log returns and ratio adjustment are invalid across non-positive prices. Policy:
  - P&L series use **point P&L** (P2). Returns are expressed on capital (or on the prior-day notional with a floor), not as price ratios.
  - Research return series: if |settle_{t−1}| < floor (e.g. 5% of the trailing 1-year median), set return basis = notional floor and flag the day.
  - The held series would normally have rolled out of a contract that close to expiry. A negative price in the *held* contract is itself a red flag for the roll policy.

### 5.8 Price-limit events
- Limit rules live in `contract_spec_version.price_limit_rule` (CME dynamic circuit breakers, MCX daily price range with relaxations) [VERIFY in 14].
- `limit_state` is detected from the rule and from high = low = settle at the limit.
- Backtest rule: **no fills at a limit-locked settle in the direction blocked by the limit.** Trades are deferred to the next session. Mark-to-market still uses the settle, with a flag. Count locked days per root as a risk statistic.

### 5.9 Abnormal observations (validation rules; flag, never silently delete)
| Rule | Check |
|---|---|
| V1 OHLC consistency | low ≤ open, close, settle ≤ high (settle-only days exempt) |
| V2 Non-negativity | volume ≥ 0, OI ≥ 0; price > 0 unless `allows_negative` |
| V3 Jump vs own history | \|return\| > k × trailing σ (k ≈ 6) → review |
| V4 Cross-contract consistency | a jump in one contract not shared by adjacent months (spread jump > k × σ of spread) → likely bad print |
| V5 Staleness | unchanged settle with zero volume for > n days |
| V6 Cross-source | settle differs between sources by > 1 tick on liquid contracts |
| V7 Calendar | row on a closed day, or missing on an open day |
| V8 Spec | price not a multiple of the tick size valid on that date |
Actions: flag → quarantine (excluded from derived builds) → manual decision logged in `meta.quality_event`. Winsorising is allowed **only** inside feature definitions, documented; never on P&L data.

### 5.10 Changes in contract specifications
- P&L uses the multiplier and tick value valid on the trade date (`contract_spec_version`). Lot-size changes apply to contracts listed under the new spec. Never assume today's spec for history.
- Trading-hour changes alter settlement times → update `ref.trading_calendar` and `settle_available_ts`.
- Expiry-rule changes: per-contract dates are stored, so no special handling is needed beyond correct ingestion.

## 6. Timestamp / information-availability framework (mandatory)

### 6.1 Four required fields for every non-price observation
| Field | Meaning | Stored in |
|---|---|---|
| **OBSERVATION DATE** | Period the value describes (`period_start`, `period_end`; e.g. week ending Fri, month, quarter) | `fund.release`, `pos.cot.as_of_date` |
| **RELEASE DATE** | Date the value was first public | `fund.release.actual_release_ts` (date part) |
| **RELEASE TIME** | Exact time, in UTC (converted from source tz with DST) | `actual_release_ts`, plus `release_ts_quality` |
| **FIRST TRADABLE SESSION** | First session/decision point at which a strategy could act on the data | Computed per venue: `first_tradable(venue, available_ts)` |

Prices follow the same logic: `settle_available_ts` = official settlement time (+ publication lag).

### 6.2 Core rules
1. **As-of join only.** A feature value is usable at decision time τ iff `available_ts ≤ τ − latency_buffer` (default buffer = 1 minute for systematic; conservative mode = next session).
2. **Decision and execution are distinct.** Signal at decision time τ → execution at the first price *after* τ (next settle in daily tests, or next session open if modelled). Never use a settle that is computed at or before the information release as the execution price for a signal using that information.
3. **Use first-release vintages** unless testing revisions. If only revised history exists, flag the dataset `revised_only` and treat results as an **upper bound**.
4. **Unknown historical release times** → assume the end of the release date (`release_ts_quality = assumed`) → first tradable = next session.
5. **Cross-venue alignment:** convert both venues' settlement times to UTC before comparing (CME settles in the US afternoon; MCX closes late evening IST). The same calendar date is **not** the same information set.
6. **Holiday shifts:** use actual release timestamps (EIA, CFTC and others delay releases around holidays), never a fixed weekday rule alone.

### 6.3 Dataset timing table (typical; confirm at ingestion) [VERIFY]
| Dataset | Observation | Release (typical, local) | First tradable — CME daily-settle backtest | First tradable — MCX |
|---|---|---|---|---|
| CME settlements | trade date T | Metals ~13:30 ET, energy 14:30 ET (V-S for NG) | Signal for T+1 settle | MCX same evening (after ~19:00–00:00 IST, DST-dependent) |
| CME open interest | trade date T | Next morning (preliminary) | T+1 decision → T+2 settle (conservative) | T+1 evening |
| CFTC COT | Tuesday close | Friday 15:30 ET [V-S] | Following Monday settle | Monday session |
| EIA Weekly Petroleum Status | week ending Friday | Wednesday 10:30 ET | Wednesday settle (after release) | Wednesday ~20:00/21:00 IST |
| EIA Natural Gas Storage | week ending Friday | Thursday 10:30 ET | Thursday settle | Thursday evening IST |
| LME stocks | prior day | Next morning London | Same-day LME/COMEX settle | Same day |
| LBMA Gold/Silver Price | fixing time | 10:30 / 15:00 London (gold), 12:00 (silver) | Same day if before settle | Same day |
| RBI/FBIL USDINR reference | day | ~13:30 IST | Same day | Same-day MCX afternoon session |
| US Treasury / FRED rates | day | Evening / next business day | T+1 | T+1 |
| US CPI | month | ~2nd week, 08:30 ET | Same day | Same evening |
| China/India customs (imports) | month | ~1–3 weeks after month end | Release day | Release day |
| WGC Gold Demand Trends | quarter | ~4–5 weeks after quarter end | Release day (time often unknown → next session) | Next session |
| ETF holdings | holdings date | Issuer end-of-day / next morning | Next session | Next session |

## 7. Data sources (single source of truth; see SOURCE_REGISTER)
| Need | Primary | Alternatives | Status |
|---|---|---|---|
| CME per-contract daily (incl. expired) | CME DataMine (paid) | Norgate, CSI Data, Barchart, Databento, LSEG, Bloomberg | OPEN-3.1 |
| LME prices and stocks | LME (licensed) | Vendors redistributing LME | OPEN-3.4/8.1 |
| MCX per-contract daily | MCX bhavcopy (free) [V-2] | Vendors | OPEN-3.6 |
| Energy contracts 1–4 (history only, to 5 Apr 2024) | EIA [V-S] | — | Free validation set |
| COT | CFTC historical files | — | Free |
| EIA fundamentals | EIA (API) | — | Free; vintages limited |
| Rates / FX | FRED, US Treasury, RBI/FBIL | — | Free |
| Spot benchmarks | LBMA (via IBA licensing), EIA spot | World Bank / IMF monthly | Licence check |
| Specs, calendars, limits | Exchange rulebooks and circulars | Vendor metadata | Manual curation |

## 8. Minimum historical data before legitimate backtesting

### 8.1 Essential (no backtest without these)
| Item | Requirement |
|---|---|
| Per-contract daily settle, OHLC, volume, OI | Every contract of each root's liquid months **plus the next 2 deferred months**, including all expired contracts |
| Contract calendar | FND, tender start, LTD, settlement type, **per contract** |
| Contract spec history | Multiplier, tick, settlement type, limit rule, with validity dates |
| Exchange trading calendars | Holidays, settlement times |
| Risk-free rates | USD 3M T-bill (or SOFR spliced), INR 91-day T-bill |
| USDINR reference fixing | For MCX conversion and MCX-vs-global analysis |
| Cost model inputs | Tick sizes, fee schedules, MCX taxes, a slippage assumption per liquidity tier |
| **History length** | Global (CME): **≥ 20 years daily** per market (covers 2008, 2014–16, 2020, 2022; ≥ 2 rate cycles). Trend and carry tests ideally 30+ years. MCX: all available (~2005+) — used for **implementation validation**, not discovery |

Why 20 years: Sharpe ratio t-stat ≈ SR × √years. A true per-market SR of 0.4 needs ~25 years for t ≈ 2. Shorter samples cannot separate modest effects from noise per market. Pooling across markets helps only partly (§9).

### 8.2 Useful (needed for specific hypothesis families)
- Full listed curve (all months) → curve features beyond F1/F2 (11).
- CFTC COT (Legacy 1986+, Disaggregated 2006+) with release timestamps.
- EIA weekly petroleum and NG storage, with release timestamps.
- Exchange stocks: LME, COMEX, SHFE.
- Spot benchmarks: LBMA, LME cash, Henry Hub cash.
- Historical margins and price-limit events.
- Bid-ask samples or intraday bars to calibrate slippage.

### 8.3 Optional (later)
- Full intraday history; options settlements and IV surfaces (13); ETF holdings; macro vintages (ALFRED); freight, TC/RC, crack spreads; China data; alternative data.

## 9. Is the 11-market universe sufficient for time-series research? (review of earlier statement)

**Correction / refinement:** my earlier statement ("excluding agriculture leaves too few markets") applies mainly to **cross-sectional** strategies. For **time-series** research the universe is **adequate but thin**. The binding constraint is less the number of markets than **effective independence** and **data access**.

| Cluster | Markets | Expected within-cluster correlation | Note |
|---|---|---|---|
| Precious | Gold, Silver, Platinum, Palladium | High for Au–Ag; moderate for PGMs (industrial/auto exposure) | ~2 effective bets |
| Energy | Crude, Natural Gas | Low between them (NG regional/weather-driven) | ~2 effective bets |
| Base | Copper, Aluminium, Zinc, Nickel, Lead | Moderate–high (common China/industrial factor) | ~1.5–2.5 effective bets |

All correlations are [HYPOTHESIS] until measured [OPEN-9.1].

- **Effective breadth:** roughly 5–7 effective markets for asset returns. Strategy-return correlations (e.g. trend signals) are often lower than asset correlations, so breadth may be somewhat higher for strategies. Illustration: with N = 11 and average pairwise strategy correlation ρ, effective N = N / (1 + (N−1)ρ) → ρ = 0.1 gives 5.5; ρ = 0.2 gives 3.7.
- **Data access is the real constraint:**
  - **CME:** long, liquid, affordable history exists for 7 markets (GC, SI, PL, PA, HG, CL, NG).
  - **Aluminium, zinc, nickel, lead:** the global benchmark is **LME** (licensed, forward-style prompt structure). CME versions of these are thin.
  - **Without LME data, the base-metal cluster is represented only by copper globally.** MCX covers all five base metals, but with shorter history and INR/duty effects.
- **What the universe supports well:**
  - Per-market time-series tests with long histories.
  - **Pooled panel tests** across markets (with standard errors clustered by date, to avoid overstating power).
  - Regime and sub-period robustness.
  - Global → MCX implementation transfer.
- **What it supports poorly:**
  - Cross-sectional ranking (terciles of 11 = 3–4 names, dominated by clusters).
  - Exploratory searches with many parameters (multiple-testing risk is high relative to breadth).
- **Mitigations without adding agriculture:**
  1. Pre-register hypotheses and parameters.
  2. Prefer few-parameter, economically motivated rules.
  3. Use **time** (long histories, regime splits) as the main source of independent evidence.
  4. Replicate across venues (CME vs LME vs MCX). This is *not* independent evidence, but it does check implementation robustness.
  5. Reserve a final hold-out period untouched until the end.
  6. Within the existing scope, Brent alongside WTI adds a benchmark check rather than a new bet.

**Conclusion:** sufficient for a rigorous **time-series** program, provided we accept modest diversification, rely on long history, and treat LME data acquisition as a priority decision. It is not suited to cross-sectional commodity strategies as a primary research line.

## 10. Major unresolved data problems
| ID | Problem |
|---|---|
| OPEN-3.1 | Affordable per-contract history with expired contracts and FND/LTD metadata (vendor choice) |
| OPEN-3.4 / 8.1 | LME data licensing and cost; aluminium benchmark choice; whether to treat zinc/nickel/lead as MCX-only |
| OPEN-3.6 | MCX bhavcopy depth, format changes, symbol mapping |
| OPEN-3.7 | MCX tender/delivery-period rules and history |
| OPEN-1.1 | Historical margins and price-limit histories |
| OPEN-6.1 | Historical release *times* for EIA/WGC/customs before electronic archives |
| OPEN-6.2 | Point-in-time vintages for fundamental series (EIA revisions; ALFRED coverage) |
| OPEN-8.2 | Slippage calibration without intraday history |
| OPEN-9.1 | Measured correlation/effective-breadth of the 11 markets (asset and strategy level) |
| OPEN-1.6 | CFTC COT program changes (2026 review) |
