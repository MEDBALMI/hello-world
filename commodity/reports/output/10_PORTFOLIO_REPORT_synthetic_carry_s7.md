# 10 Portfolio Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `CARRY`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

Sleeves: surviving hypotheses — ['H08|GC', 'H08|SI', 'H08|HG', 'H08|CL', 'H08|NG', 'H11|GC', 'H11|SI', 'H11|HG', 'H11|CL', 'H11|NG', 'H25|GC', 'H25|SI', 'H25|HG', 'H25|CL', 'H25|NG']

Average sleeve correlation: 0.04

## Allocation methods (10% portfolio vol target)
| method | cagr | ann_vol | sharpe | sortino | calmar | max_dd | max_sector_risk_share | sector_risk |
|---|---|---|---|---|---|---|---|---|
| equal | 0.104 | 0.100 | 1.036 | 1.671 | 0.558 | -0.185 | 0.547 | {"ENERGY": 0.547, "INDUSTRIAL": 0.17, "PRECIOUS": 0.283} |
| equal+sector_cap | 0.098 | 0.100 | 0.984 | 1.586 | 0.528 | -0.185 | 0.500 | {"ENERGY": 0.5, "INDUSTRIAL": 0.189, "PRECIOUS": 0.311} |
| equal_vol | 0.079 | 0.098 | 0.826 | 1.251 | 0.391 | -0.201 | 0.557 | {"ENERGY": 0.557, "INDUSTRIAL": 0.152, "PRECIOUS": 0.292} |
| equal_vol+sector_cap | 0.073 | 0.097 | 0.775 | 1.166 | 0.364 | -0.201 | 0.500 | {"ENERGY": 0.5, "INDUSTRIAL": 0.173, "PRECIOUS": 0.327} |
| risk_parity | 0.064 | 0.096 | 0.693 | 1.042 | 0.273 | -0.234 | 0.462 | {"ENERGY": 0.462, "INDUSTRIAL": 0.154, "PRECIOUS": 0.385} |
| risk_parity+sector_cap | 0.064 | 0.096 | 0.693 | 1.042 | 0.273 | -0.234 | 0.462 | {"ENERGY": 0.462, "INDUSTRIAL": 0.154, "PRECIOUS": 0.385} |
| corr_adjusted | 0.074 | 0.097 | 0.787 | 1.189 | 0.373 | -0.200 | 0.514 | {"ENERGY": 0.514, "INDUSTRIAL": 0.169, "PRECIOUS": 0.317} |
| corr_adjusted+sector_cap | 0.071 | 0.097 | 0.757 | 1.139 | 0.357 | -0.199 | 0.500 | {"ENERGY": 0.5, "INDUSTRIAL": 0.175, "PRECIOUS": 0.325} |

## Position sizing (H01 reference)
| sizing | cagr | ann_vol | sharpe | max_dd | max_root_vol_share |
|---|---|---|---|---|---|
| equal_notional | 0.076 | 0.149 | 0.564 | -0.499 | 0.333 |
| vol | 0.022 | 0.045 | 0.513 | -0.161 | 0.201 |
| atr | 0.012 | 0.027 | 0.461 | -0.090 | 0.203 |
