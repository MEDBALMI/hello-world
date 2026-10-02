# 10 Portfolio Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

Sleeves: REFERENCE SET (no hypothesis survived) - engineering demonstration only — ['H01|GC', 'H01|SI', 'H01|HG', 'H01|CL', 'H01|NG', 'H03|GC', 'H03|SI', 'H03|HG', 'H03|CL', 'H03|NG', 'H11|GC', 'H11|SI', 'H11|HG', 'H11|CL', 'H11|NG']

Average sleeve correlation: 0.02

## Allocation methods (10% portfolio vol target)
| method | cagr | ann_vol | sharpe | sortino | calmar | max_dd | max_sector_risk_share | sector_risk |
|---|---|---|---|---|---|---|---|---|
| equal | -0.013 | 0.100 | -0.079 | -0.126 | -0.027 | -0.469 | 0.484 | {"ENERGY": 0.484, "INDUSTRIAL": 0.151, "PRECIOUS": 0.366} |
| equal+sector_cap | -0.013 | 0.100 | -0.082 | -0.131 | -0.028 | -0.472 | 0.484 | {"ENERGY": 0.484, "INDUSTRIAL": 0.151, "PRECIOUS": 0.366} |
| equal_vol | -0.014 | 0.100 | -0.091 | -0.146 | -0.030 | -0.474 | 0.474 | {"ENERGY": 0.474, "INDUSTRIAL": 0.152, "PRECIOUS": 0.375} |
| equal_vol+sector_cap | -0.014 | 0.100 | -0.092 | -0.147 | -0.030 | -0.476 | 0.474 | {"ENERGY": 0.474, "INDUSTRIAL": 0.152, "PRECIOUS": 0.375} |
| risk_parity | -0.017 | 0.100 | -0.117 | -0.186 | -0.033 | -0.508 | 0.400 | {"ENERGY": 0.4, "INDUSTRIAL": 0.2, "PRECIOUS": 0.4} |
| risk_parity+sector_cap | -0.017 | 0.100 | -0.117 | -0.186 | -0.033 | -0.508 | 0.400 | {"ENERGY": 0.4, "INDUSTRIAL": 0.2, "PRECIOUS": 0.4} |
| corr_adjusted | -0.015 | 0.100 | -0.097 | -0.155 | -0.030 | -0.482 | 0.461 | {"ENERGY": 0.461, "INDUSTRIAL": 0.157, "PRECIOUS": 0.382} |
| corr_adjusted+sector_cap | -0.015 | 0.100 | -0.097 | -0.155 | -0.030 | -0.483 | 0.461 | {"ENERGY": 0.461, "INDUSTRIAL": 0.157, "PRECIOUS": 0.382} |

## Position sizing (H01 reference)
| sizing | cagr | ann_vol | sharpe | max_dd | max_root_vol_share |
|---|---|---|---|---|---|
| equal_notional | 0.029 | 0.139 | 0.276 | -0.629 | 0.329 |
| vol | 0.007 | 0.044 | 0.189 | -0.189 | 0.200 |
| atr | 0.003 | 0.026 | 0.139 | -0.120 | 0.201 |
