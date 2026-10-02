# 18 — Commodity Module Specifications (Gold, Crude, Copper, Silver, Natural Gas, Aluminium)

> Status: v0.1 (2026-10-02). Implementation-oriented specification of the commodity modules (Phases 5–10)
> requested by the master execution prompt. **No empirical findings on real data exist yet**: every
> market-data host (CME, CFTC, EIA, FRED, MCX, LME, LBMA) is blocked from the build environment
> (17 §8; RESEARCH_LOG session 5). Where a driver needs data we do not hold, it is marked DATA-LIMITED.
> Concepts → 01/02; curve features → 11; hypotheses → `commodity/config/hypotheses.yaml` (rendered in 15).

Legend: ✅ implemented feature · 🟡 adapter implemented, data not yet ingested · ⛔ data not available / licensed.

| Driver | Gold | Crude (WTI) | Copper | Silver | Nat Gas | Aluminium |
|---|---|---|---|---|---|---|
| Trend / momentum / breakout (H01–H07) | ✅ | ✅ | ✅ | ✅ | ✅ | MCX only |
| Equity-pattern transfer (H08 trend template, H09 VCP proxy; H27 cup & handle DESIGN-LIMITED) | ✅ | ✅ | ✅ | ✅ | ✅ | MCX only |
| Curve: carry, CM slope/curvature (H11–H14) | ✅ (mostly financing) | ✅ | ✅ | ✅ | ✅ + seasonal 12m carry | ⛔ LME prompts (postponed) |
| COT positioning (H15–H17) | 🟡 CFTC 088691 | 🟡 067651 | 🟡 085692 | 🟡 084691 | 🟡 023651 | ⛔ (LME COTR) |
| Real yields (H18) | 🟡 FRED DFII10 | – | – | 🟡 | – | – |
| USD (H19) | 🟡 DTWEXBGS | 🟡 | 🟡 | – | – | – |
| Inventories (H26) | n/a (stock ≫ flow) | ⛔ EIA WPSR (API key/network) | ⛔ LME/COMEX/SHFE stocks | – | ⛔ EIA storage | ⛔ LME stocks |
| Refining / crack spreads | – | ⛔ needs RBOB/HO contracts (out of current scope) | – | – | – | – |
| Weather / HDD-CDD | – | – | – | – | ⛔ NOAA (not wired) | – |
| China / growth proxies | – | ⛔ | ⛔ (PMI, imports) | – | – | ⛔ |
| ETF flows / central banks | ⛔ (WGC licence) | – | – | ⛔ | – | – |
| Gold/silver ratio (H24, type B) | ✅ | – | – | ✅ | – | – |
| Seasonality (H21–H22) | ✅ | ✅ | ✅ | ✅ | ✅ | MCX only |
| MCX implementation (11_MCX report) | ✅ MCX_GOLD | ✅ MCX_CRUDEOIL | ✅ MCX_COPPER | ✅ MCX_SILVER | ✅ MCX_NATURALGAS | ✅ MCX_ALUMINIUM (no global benchmark) |

## Module-specific notes (what is different, as testable rules)
- **Gold:** carry ≈ financing − lease rate → carry signals are expected to be uninformative (H11 expected ~0); use `carry + r` (TS8) once rates are ingested. Key macro tests are *lagged* real-yield and USD changes (H18/H19); contemporaneous correlation alone is not tradeable (06 report separates the two).
- **Crude:** richest curve (12+ liquid months) → TS2/TS3 usable; negative-price handling (Apr 2020) is implemented (notional floor; test `test_negative_price_handled`). Inventory surprise (H26) is the highest-value missing dataset.
- **Copper:** COMEX HG active months Mar/May/Jul/Sep/Dec; LME cash–3M (TS10) is the better tightness gauge but is licensed → DATA-LIMITED. "Dr Copper" is treated as a hypothesis (cross-relationship table, lagged columns only).
- **Silver:** dual monetary/industrial driver → tested via gold/silver ratio RV (H24) and the same trend/carry set; thinner curve than gold.
- **Natural gas:** strong seasonal curve → raw F1/F2 carry is contaminated by seasonality; use `carry_12m` (TS9). Highest volatility → vol-targeting essential.
- **Aluminium:** global benchmark (LME) postponed by decision; research runs on MCX_ALUMINIUM only (standalone, INR) and is marked DATA-LIMITED for global conclusions.

## Open items (feed RESEARCH_LOG / roadmap)
- OPEN-18.1 EIA weekly inventories with release timestamps (API key = credential → user approval).
- OPEN-18.2 Weather (NOAA HDD/CDD) adapter for natural gas.
- OPEN-18.3 Crack-spread research needs RBOB/HO contracts (scope decision).
- OPEN-18.4 Objective Cup & Handle detector (H27) before testing.
