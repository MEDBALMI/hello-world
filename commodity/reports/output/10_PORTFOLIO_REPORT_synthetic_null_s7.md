# 10 Portfolio Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

Sleeves: REFERENCE SET (no hypothesis survived) - engineering demonstration only — ['H01|GC', 'H01|SI', 'H01|HG', 'H01|CL', 'H01|NG', 'H03|GC', 'H03|SI', 'H03|HG', 'H03|CL', 'H03|NG', 'H11|GC', 'H11|SI', 'H11|HG', 'H11|CL', 'H11|NG']

Average sleeve correlation: 0.05

## Allocation methods (10% portfolio vol target)
| method | cagr | ann_vol | sharpe | sortino | calmar | max_dd | max_sector_risk_share | sector_risk |
|---|---|---|---|---|---|---|---|---|
| equal | -0.003 | 0.101 | 0.017 | 0.027 | -0.008 | -0.401 | 0.459 | {"ENERGY": 0.459, "INDUSTRIAL": 0.298, "PRECIOUS": 0.243} |
| equal+sector_cap | -0.003 | 0.101 | 0.024 | 0.039 | -0.007 | -0.390 | 0.459 | {"ENERGY": 0.459, "INDUSTRIAL": 0.298, "PRECIOUS": 0.243} |
| equal_vol | -0.004 | 0.101 | 0.007 | 0.011 | -0.010 | -0.419 | 0.441 | {"ENERGY": 0.441, "INDUSTRIAL": 0.325, "PRECIOUS": 0.235} |
| equal_vol+sector_cap | -0.004 | 0.101 | 0.010 | 0.016 | -0.010 | -0.410 | 0.441 | {"ENERGY": 0.441, "INDUSTRIAL": 0.325, "PRECIOUS": 0.235} |
| risk_parity | -0.006 | 0.099 | -0.011 | -0.017 | -0.016 | -0.366 | 0.400 | {"ENERGY": 0.4, "INDUSTRIAL": 0.2, "PRECIOUS": 0.4} |
| risk_parity+sector_cap | -0.006 | 0.099 | -0.011 | -0.017 | -0.016 | -0.366 | 0.400 | {"ENERGY": 0.4, "INDUSTRIAL": 0.2, "PRECIOUS": 0.4} |
| corr_adjusted | -0.004 | 0.101 | 0.010 | 0.016 | -0.010 | -0.415 | 0.440 | {"ENERGY": 0.44, "INDUSTRIAL": 0.302, "PRECIOUS": 0.258} |
| corr_adjusted+sector_cap | -0.004 | 0.101 | 0.012 | 0.019 | -0.009 | -0.411 | 0.440 | {"ENERGY": 0.44, "INDUSTRIAL": 0.302, "PRECIOUS": 0.258} |

## Position sizing (H01 reference)
| sizing | cagr | ann_vol | sharpe | max_dd | max_root_vol_share |
|---|---|---|---|---|---|
| equal_notional | -0.005 | 0.148 | 0.040 | -0.693 | 0.332 |
| vol | -0.001 | 0.045 | 0.001 | -0.359 | 0.201 |
| atr | -0.001 | 0.027 | -0.011 | -0.214 | 0.203 |
