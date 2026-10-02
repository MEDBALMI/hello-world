# 01 Data Health Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

Tests T1–T14 per root (PASS/FAIL/OPEN). Totals: {'PASS': 65, 'OPEN': 5}.

| root | T1 | T2 | T3 | T4 | T5 | T6 | T7 | T8 | T9 | T10 | T11 | T12 | T13 | T14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CL | PASS | PASS | OPEN | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| GC | PASS | PASS | OPEN | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| HG | PASS | PASS | OPEN | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| NG | PASS | PASS | OPEN | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |
| SI | PASS | PASS | OPEN | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS | PASS |

**OPEN** items require a second source or point-in-time vintages (T3 cross-source settlement, T14 revised-only macro).

Machine-readable: `validation_synthetic_null_s7.csv` (+ `data_quality` table).
