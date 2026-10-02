# 04 Positioning Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

COT aligned to release (Friday 15:30 ET → next session); weekly data as-of Tuesday.

| root | IC mm_z | t | IC mm_chg_4w | t2 | share pct>0.9 |
|---|---|---|---|---|---|
| GC | -0.049 | -0.921 | -0.050 | -0.961 | 0.140 |
| SI | -0.076 | -1.437 | 0.045 | 0.856 | 0.114 |
| HG | -0.016 | -0.296 | 0.021 | 0.403 | 0.145 |
| CL | 0.030 | 0.562 | 0.047 | 0.910 | 0.130 |
| NG | -0.022 | -0.417 | 0.028 | 0.528 | 0.112 |

| id | family | type | strategy | params | train | val | WF | OOS |
|---|---|---|---|---|---|---|---|---|
| H15 | I_POSITIONING | A | cot_contrarian | {"hi": 0.9, "lo": 0.05} | 0.04 | 0.19 | -0.06 | -0.18 |
| H16 | I_POSITIONING | A | cot_momentum | {} | -0.79 | -0.62 | -0.76 | -0.15 |
| H17 | I_POSITIONING | A | trend_cot | {"hi": 0.9} | -0.26 | 0.18 | -0.35 | -0.36 |
