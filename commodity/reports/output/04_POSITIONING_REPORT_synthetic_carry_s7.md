# 04 Positioning Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `CARRY`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

COT aligned to release (Friday 15:30 ET → next session); weekly data as-of Tuesday.

| root | IC mm_z | t | IC mm_chg_4w | t2 | share pct>0.9 |
|---|---|---|---|---|---|
| GC | -0.029 | -0.554 | -0.044 | -0.844 | 0.140 |
| SI | -0.077 | -1.459 | 0.043 | 0.828 | 0.114 |
| HG | -0.022 | -0.417 | 0.030 | 0.571 | 0.145 |
| CL | 0.051 | 0.966 | 0.046 | 0.884 | 0.130 |
| NG | -0.048 | -0.915 | 0.030 | 0.570 | 0.112 |

| id | family | type | strategy | params | train | val | WF | OOS |
|---|---|---|---|---|---|---|---|---|
| H15 | I_POSITIONING | A | cot_contrarian | {"hi": 0.9, "lo": 0.05} | -0.02 | 0.32 | -0.06 | -0.34 |
| H16 | I_POSITIONING | A | cot_momentum | {} | -0.78 | -0.64 | -0.77 | -0.44 |
| H17 | I_POSITIONING | A | trend_cot | {"hi": 0.9} | 0.40 | 0.91 | 0.65 | 0.12 |
