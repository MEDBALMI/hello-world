# 16 — Research Roadmap

> Status: **v0.1 (initial)** — written after Phases 1–2. The final prioritisation (Phase 20) will replace this after the commodity modules are complete. No strategies are ranked.

## Execution order
| Step | Phases | Output files | Gate to next step |
|---|---|---|---|
| 1 | 1 Foundations, 2 Equities vs commodities | 01, 02-A | ✅ done (v0.1) |
| 2 | 3 Market structure + 14 Term structure (theory & construction) | 02-B, 11 | Roll methodology agreed |
| 3 | 18 Data architecture (design only) + vendor evaluation | 03, SOURCE_REGISTER | Data source decision for per-contract history |
| 4 | 13 Positioning, 12 Seasonality (method sections) | 10, 12 | Point-in-time alignment rules written |
| 5 | Core modules: 5 Gold → 6 Crude → 7 Copper → 8 Silver → 9 NatGas → 10 Aluminium | 04–09 | Each module lists hypotheses + data needs |
| 6 | 11 Cross-commodity, 15 Technical transfer | inside 04–09, 15 | |
| 7 | 17 MCX implementation | 14 | Contract specs verified from MCX circulars |
| 8 | 16 Options | 13 | |
| 9 | 19 Hypotheses, 20 Prioritisation | 15, 16 v1 | → Data build & testing program |

Rationale: market structure and data construction come before commodity modules because every later hypothesis depends on correctly built return series and point-in-time data.

## Initial classification
### 1. MUST LEARN (before any testing)
- Contract identity, expiry, FND/LTD, roll mechanics (01 §D; 02 §B)
- Return decomposition: spot vs roll vs collateral (02 §A.2)
- Theory of storage: inventory ↔ convenience yield ↔ curve (01 §E)
- Point-in-time alignment of COT, EIA and macro releases (01#34, 36)
- MCX = global price × USDINR × duties/premia, with different expiries (→ 14)

### 2. MUST DATA (needed for almost every hypothesis)
- Per-contract daily OHLC/settle/volume/OI incl. expired contracts, with FND/LTD — core 6 commodities [OPEN-3.1]
- Risk-free rates (US T-bill/SOFR; India 91-day T-bill), USDINR reference rate
- CFTC COT (Legacy 1986+, Disaggregated 2006+), with release timestamps
- EIA weekly petroleum & NG storage (with release dates; vintages where possible)
- MCX per-contract bhavcopy history

### 3. MUST TEST (first candidates; details in 15 later)
- Quantify naive-vs-correct continuous-series bias per commodity [OPEN-3.3] — a *data-validation* test, not a strategy
- Return decomposition (spot vs roll) per core commodity [OPEN-1.2]
- Curve slope → subsequent excess returns, time-series, per commodity [OPEN-1.3]
- Time-series trend on correctly built series (baseline before any equity-style pattern tests)

### 4. LATER
- Commodity-specific fundamentals (inventory surprises, TC/RC, crack spreads)
- Equity pattern transfers (VCP, Cup & Handle, trend template)
- Options / volatility risk premium
- Secondary metals (Pt, Pd, Zn, Ni, Pb)
- Intraday data and execution modelling

### 5. CURRENTLY OUT OF SCOPE
- Agriculture (all)
- Live or paper trading
- Large data downloads and production code
- Physical commodity trading, OTC swaps

## Key risks to the program
| Risk | Impact | Mitigation |
|---|---|---|
| Cost/availability of per-contract history (esp. LME) | Blocks Phase 3 testing | Vendor evaluation early (step 3). EIA contracts 1–4 cover energy only up to 5 Apr 2024 (publication stopped) — not an ongoing fallback. MCX bhavcopy is free for MCX contracts |
| Small universe (6 core, ≤11 total) | Cross-sectional strategies have little breadth; high risk of overfitting | Prefer time-series tests; strict multiple-testing control; pool evidence across commodities |
| Regime breaks (financialisation ~2004, shale ~2010, US exports 2016, MCX regulatory changes, 2020/2022 shocks) | Unstable relationships | Sub-period tests, structural-break tests |
| Look-ahead in fundamentals/positioning | Inflated results | Release-timestamped tables; vintage data |
| MCX-specific costs (CTT, stamp duty, exchange fees, GST), expiry mismatch, lot changes | Global edge may not survive locally | Dedicated MCX cost model in 14 |
| Numbers quoted from memory | Spec errors | [V-S]/[V-2]/[VERIFY] tags; SOURCE_REGISTER status. Primary sites (CME, CFTC, MCX) blocked from this environment — full verification needs network access or manual check |
| CFTC COT program under review (May 2026 RFC on frequency/content) | Schema/history comparability | Track outcome (OPEN-1.6) |

## Consolidated open questions
| ID | Question | Where |
|---|---|---|
| OPEN-1.1 | Historical margin data availability (CME, MCX) | 01 |
| OPEN-1.2 | Spot vs roll contribution to long-run returns per commodity | 01 |
| OPEN-1.3 | Does curve slope predict time-series returns in our core 6? | 01, 11 |
| OPEN-1.4 | MCX positioning/participant data availability | 01, 10, 14 |
| OPEN-1.5 / 3.1 | Affordable per-contract history source | 01, 02 |
| OPEN-3.2 | Optimal roll offset per commodity | 02 |
| OPEN-3.3 | Size of naive roll-gap bias | 02 |
| OPEN-3.4 | Aluminium benchmark choice (LME vs CME vs MCX) | 02 |
| OPEN-1.6 | Outcome of CFTC 2026 COT review | 01, 10 |
| OPEN-3.5 | Negative-price handling (NYMEX & MCX crude, Apr 2020) | 02 |
| OPEN-3.6 | MCX bhavcopy earliest date / format history | 02, 14 |
