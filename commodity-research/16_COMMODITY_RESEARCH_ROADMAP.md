# 16 — Research Roadmap

> Status: **v0.2 (2026-10-02)** — updated after the quantitative-foundation stage (Phase 3 complete, data architecture designed). The final prioritisation (Phase 20) will replace this once the commodity modules exist. No strategies are ranked.

## Execution order and gates
| Step | Phases | Output | Status / gate |
|---|---|---|---|
| 1 | 1 Foundations, 2 Equities vs commodities | 01, 02-A | ✅ v0.1 |
| 2 | 3 Futures market structure | 02-B | ✅ v1.0. Research series vs P&L series separated; roll policy ROLL-A defined |
| 3 | 18 Data architecture (design) | 03 | ✅ v1.0 design. Handling rules, timestamp framework, minimum data, universe review |
| 4 | 14 Term structure (construction) | 11 | ✅ v0.1. Feature definitions only |
| **5 (next)** | **Data sourcing decision** | SOURCE_REGISTER, 03 §7 | **Gate:** vendor chosen for per-contract CME history (OPEN-3.1); LME decision (OPEN-3.4/8.1); MCX bhavcopy depth known (OPEN-3.6) |
| 6 | **Data pilot (validation only, no strategies)** | small DB build for GC, CL, MCX GOLD | **Gate:** validation rules V1–V8 pass; naive-vs-chained bias measured (OPEN-3.3); roll offsets calibrated (OPEN-3.2) |
| 7 | 13 Positioning, 12 Seasonality (method sections) | 10, 12 | COT alignment implemented per 03 §6 |
| 8 | Core modules: Gold → Crude → Copper → Silver → NatGas → Aluminium | 04–09 | Each lists hypotheses + data needs + timestamp table |
| 9 | Cross-commodity (11), technical transfer (15) | 04–09, 15 | |
| 10 | 17 MCX implementation | 14 | Specs, tender rules, costs, taxes |
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
- Then the first hypotheses: time-series carry (H-TS1), time-series trend on chained series (baseline)

### 4. LATER
- Fundamentals with vintages; COT features; seasonality tests
- Equity pattern transfers (VCP, Cup & Handle, trend template)
- Options / volatility premium; intraday execution; secondary-metal deep dives

### 5. CURRENTLY OUT OF SCOPE
- Agriculture; live or paper trading; production code; physical/OTC trading; cross-sectional commodity strategies as a primary line (03 §9)

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
| OPEN-6.1 | Historical release times | 03 |
| OPEN-6.2 | Fundamental-data vintages | 03 |
| OPEN-8.2 | Slippage calibration without intraday data | 03 |
| OPEN-9.1 | Measured effective breadth | 03 |
| OPEN-11.1–11.3 | NG seasonal adjustment; storage-cost assumptions; metals curve depth | 11 |
