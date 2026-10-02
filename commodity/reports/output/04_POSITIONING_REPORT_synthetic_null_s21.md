# 04 Positioning Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

COT aligned to release (Friday 15:30 ET → next session); weekly data as-of Tuesday.

| root | IC mm_z | t | IC mm_chg_4w | t2 | share pct>0.9 |
|---|---|---|---|---|---|
| GC | -0.030 | -0.567 | -0.014 | -0.269 | 0.119 |
| SI | -0.030 | -0.570 | -0.010 | -0.186 | 0.142 |
| HG | -0.043 | -0.822 | 0.000 | 0.006 | 0.098 |
| CL | -0.007 | -0.128 | -0.075 | -1.446 | 0.139 |
| NG | 0.011 | 0.200 | -0.013 | -0.244 | 0.129 |

| id | family | type | strategy | params | train | val | WF | OOS |
|---|---|---|---|---|---|---|---|---|
| H15 | I_POSITIONING | A | cot_contrarian | {"hi": 0.9, "lo": 0.05} | -0.06 | -0.45 | -0.06 | 0.34 |
| H16 | I_POSITIONING | A | cot_momentum | {} | -0.19 | -0.86 | -0.72 | -1.05 |
| H17 | I_POSITIONING | A | trend_cot | {"hi": 0.9} | -0.24 | -0.33 | -0.12 | 0.31 |
