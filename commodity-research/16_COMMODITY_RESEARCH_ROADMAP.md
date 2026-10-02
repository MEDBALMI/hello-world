# 16 — Research Roadmap

> Status: **v0.2 (2026-10-02)** — updated after the quantitative-foundation stage (Phase 3 complete, data architecture designed). The final prioritisation (Phase 20) will replace this once the commodity modules exist. No strategies are ranked.

## Execution order and gates
| Step | Phases | Output | Status / gate |
|---|---|---|---|
| 1 | 1 Foundations, 2 Equities vs commodities | 01, 02-A | ✅ v0.1 |
| 2 | 3 Futures market structure | 02-B | ✅ v1.0. Research series vs P&L series separated; ROLL-A = initial research assumption |
| 3 | 18 Data architecture (design) | 03 | ✅ v1.0 design. Handling rules, timestamp framework, minimum data, universe review |
| 4 | 14 Term structure (construction) | 11 | ✅ v0.1. Feature definitions only |
| **5 (current)** | **Phase 4: data acquisition & validation** | **17**, 03 §3.2b/§7, SOURCE_REGISTER | ✅ desk research v0.1. **Next actions (no purchase without approval):** (a) obtain quotes/trials: DataMine EOD, Norgate, CSI, Databento (OPEN-17.1); (b) MCX bhavcopy audit: earliest date, fields, symbol changes (OPEN-17.3); (c) LME aluminium go/no-go (OPEN-3.4, 17.5). **Gate:** one L4 source per market passes acceptance tests 1–7 (17 §7) |
| 6 | **Data pilot (validation only, no strategies)** | small DB build for GC, CL, MCX GOLD | **Gate:** validation rules V1–V8 pass; naive-vs-chained bias measured (OPEN-3.3); roll offsets calibrated (OPEN-3.2); first roll-rule comparison (OPEN-3.8) |
| 7 | 13 Positioning, 12 Seasonality (method sections) | 10, 12 | COT alignment implemented per 03 §6 |
| 8 | Core modules: Gold → Crude → Copper → Silver → NatGas → Aluminium | 04–09 | Each lists hypotheses + data needs + timestamp table |
| 9 | Cross-commodity (11), technical transfer (15) | 04–09, 15 | |
| 10 | 17 MCX research and implementation | 14 | Specs, tender rules, costs, taxes, **plus independent MCX research**: India-specific effects, USDINR, local liquidity and structure (03 §11.2) |
| 11 | 16 Options | 13 | |
| 12 | 19 Hypotheses, 20 Prioritisation | 15, 16 v1 | → testing program |

Steps 5–6 come **before Gold** because every module depends on reliable contract-level data and a validated roll engine. The pilot is a data-quality exercise. It is not a backtest.

## Classification
### 1. MUST LEARN
- Contract lifecycle and `delivery_risk_date` (02 §B.1)
- Research series vs realistic P&L series (02 §B.5)
- Which continuous method suits which purpose (02 §B.4 matrix)
- Information-availability framework (03 §6)
- MCX = NYMEX/COMEX/LME reference × USDINR × duties, with different expiries (→ 14)

### 2. MUST DATA (Essential, 03 §8.1)
- Per-contract daily data incl. expired contracts, per-contract calendars, spec history, trading calendars
- USD and INR short rates; USDINR reference fixing; cost-model inputs
- ≥ 20 years for global markets; all available MCX history

### 3. MUST TEST (data-validation tests first, then hypotheses)
- Naive vs chained-return bias per commodity [OPEN-3.3]
- Spot vs roll return decomposition per commodity [OPEN-1.2]
- Effective breadth of the 11-market universe [OPEN-9.1]
- Roll-rule comparison and sensitivity [OPEN-3.8]
- Then the first hypotheses: time-series carry (H-TS1), time-series trend on chained series (baseline)

### 4. LATER
- Fundamentals with vintages; COT features; seasonality tests
- Equity pattern transfers (VCP, Cup & Handle, trend template)
- Type B relative-value research (after type A foundations)
- Type C cross-sectional research: supported by the design, testing deferred
- Options / volatility premium; intraday execution; secondary-metal deep dives

### 5. CURRENTLY OUT OF SCOPE
- Agriculture; live or paper trading; production code; physical/OTC trading; testing type C cross-sectional strategies now (supported by the architecture, deferred; 03 §11.1)

## Key risks
| Risk | Mitigation |
|---|---|
| Per-contract history cost; **LME licensing** (base-metal cluster otherwise copper-only globally) | Steps 5–6 decide before modules |
| Thin effective breadth (~4–7 bets) | Time-series focus, pre-registration, long history, pooled panel tests with date-clustered errors, final hold-out |
| Regime breaks (2004 financialisation, shale, 2016 US exports, 2020, 2022, MCX rule changes) | Sub-period and structural-break tests |
| Look-ahead in fundamentals and positioning | 03 §6 mandatory; first-release vintages |
| Back-adjusted series used for P&L or level signals | 02 §B.5 rules R1–R4, P1–P9 |
| MCX costs, taxes, tender periods, expiry mismatch | 14 |
| CFTC COT program changes (2026 review) | OPEN-1.6 |
| Primary sites blocked from this environment | Verify at ingestion or manually |

## Consolidated open questions
| ID | Question | Where |
|---|---|---|
| OPEN-1.1 | Historical margins and price-limit histories | 01, 03 |
| OPEN-1.2 | Spot vs roll contribution per commodity | 01, 02 |
| OPEN-1.3 | Does carry predict time-series returns in our markets? | 11 |
| OPEN-1.4 | MCX/LME positioning data | 03 |
| OPEN-1.6 | Outcome of CFTC 2026 COT review | 01, 03 |
| OPEN-3.1 | Per-contract history vendor | 02, 03 |
| OPEN-3.2 | Roll offset/window per commodity | 02 |
| OPEN-3.3 | Naive vs chained bias | 02 |
| OPEN-3.4 / 8.1 | LME licensing; aluminium benchmark | 02, 03 |
| OPEN-3.5 | Negative-price impact on 2020 crude | 02, 03 §5.7 |
| OPEN-3.6 | MCX bhavcopy depth/format | 02, 03 |
| OPEN-3.7 | MCX tender/delivery-period rules | 02, 03 |
| OPEN-3.8 | Roll-rule comparison | 02, 03 |
| OPEN-11.4 | Cross-venue timestamp alignment (types B/C) | 03 |
| OPEN-6.1 | Historical release times | 03 |
| OPEN-6.2 | Fundamental-data vintages | 03 |
| OPEN-8.2 | Slippage calibration without intraday data | 03 |
| OPEN-9.1 | Measured effective breadth | 03 |
| OPEN-11.1–11.3 | NG seasonal adjustment; storage-cost assumptions; metals curve depth | 11 |
