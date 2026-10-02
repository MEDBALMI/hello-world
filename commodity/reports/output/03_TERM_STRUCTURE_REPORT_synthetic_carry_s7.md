# 03 Term Structure Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `CARRY`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

## GC
- Backwardation share: 0.47; mean carry -0.039; carry autocorr(21d) 0.24
- IC carry→fwd 21d: -0.011 (t -0.22, n 371); IC CM slope: -0.066
- Realised vol in backwardation 0.14 vs contango 0.14

## SI
- Backwardation share: 0.45; mean carry -0.036; carry autocorr(21d) 0.33
- IC carry→fwd 21d: -0.010 (t -0.19, n 371); IC CM slope: -0.171
- Realised vol in backwardation 0.28 vs contango 0.27

## HG
- Backwardation share: 0.53; mean carry 0.024; carry autocorr(21d) 0.35
- IC carry→fwd 21d: 0.019 (t 0.37, n 371); IC CM slope: 0.055
- Realised vol in backwardation 0.24 vs contango 0.23

## CL
- Backwardation share: 0.67; mean carry 0.324; carry autocorr(21d) -0.39
- IC carry→fwd 21d: -0.082 (t -1.58, n 371); IC CM slope: 0.087
- Realised vol in backwardation 0.35 vs contango 0.36

## NG
- Backwardation share: 0.38; mean carry -0.259; carry autocorr(21d) -0.10
- IC carry→fwd 21d: -0.059 (t -1.13, n 371); IC CM slope: 0.032
- Realised vol in backwardation 0.49 vs contango 0.50

## Roll-rule comparison (per commodity)
| root | rule | total_return_ann | price_return_ann(CM30) | roll_return_ann | roll_cost_ann | rolls_per_year | sharpe | sortino | calmar | max_dd |
|---|---|---|---|---|---|---|---|---|---|---|
| GC | ROLL_A | -0.119 | -0.062 | -0.057 | 0.008 | 6.003 | -0.744 | -1.234 | -0.115 | -0.976 |
| GC | ROLL_B | -0.117 | -0.062 | -0.055 | 0.008 | 6.003 | -0.729 | -1.210 | -0.113 | -0.974 |
| GC | ROLL_C | -0.117 | -0.062 | -0.055 | 0.008 | 6.003 | -0.726 | -1.205 | -0.113 | -0.974 |
| GC | ROLL_D | -0.117 | -0.062 | -0.055 | 0.008 | 6.003 | -0.727 | -1.206 | -0.113 | -0.974 |
| GC | ROLL_E | -0.117 | -0.062 | -0.055 | 0.008 | 6.003 | -0.730 | -1.211 | -0.114 | -0.974 |
| GC | ROLL_F | -0.115 | -0.062 | -0.053 | 0.004 | 2.647 | -0.716 | -1.187 | -0.112 | -0.972 |
| SI | ROLL_A | -0.113 | -0.033 | -0.081 | 0.021 | 5.003 | -0.257 | -0.432 | -0.108 | -0.990 |
| SI | ROLL_B | -0.117 | -0.033 | -0.084 | 0.021 | 5.003 | -0.269 | -0.449 | -0.111 | -0.991 |
| SI | ROLL_C | -0.115 | -0.033 | -0.083 | 0.021 | 5.003 | -0.263 | -0.440 | -0.110 | -0.990 |
| SI | ROLL_D | -0.116 | -0.033 | -0.083 | 0.021 | 5.003 | -0.265 | -0.443 | -0.110 | -0.991 |
| SI | ROLL_E | -0.114 | -0.033 | -0.081 | 0.021 | 5.003 | -0.258 | -0.432 | -0.108 | -0.990 |
| SI | ROLL_F | -0.099 | -0.033 | -0.066 | 0.010 | 2.291 | -0.207 | -0.347 | -0.096 | -0.983 |
| HG | ROLL_A | 0.066 | 0.043 | 0.023 | 0.002 | 5.003 | 0.391 | 0.638 | 0.099 | -0.684 |
| HG | ROLL_B | 0.068 | 0.043 | 0.025 | 0.002 | 5.003 | 0.402 | 0.656 | 0.102 | -0.688 |
| HG | ROLL_C | 0.068 | 0.043 | 0.025 | 0.002 | 5.003 | 0.401 | 0.655 | 0.102 | -0.687 |
| HG | ROLL_D | 0.069 | 0.043 | 0.026 | 0.002 | 5.003 | 0.404 | 0.660 | 0.104 | -0.687 |
| HG | ROLL_E | 0.070 | 0.043 | 0.027 | 0.002 | 5.003 | 0.409 | 0.668 | 0.106 | -0.681 |
| HG | ROLL_F | 0.060 | 0.043 | 0.018 | 0.001 | 2.098 | 0.370 | 0.605 | 0.091 | -0.684 |
| CL | ROLL_A | 0.352 | 0.036 | 0.315 | 0.010 | 12.006 | 1.139 | 1.951 | 0.536 | -0.786 |
| CL | ROLL_B | 0.345 | 0.036 | 0.309 | 0.010 | 12.038 | 1.122 | 1.917 | 0.521 | -0.792 |
| CL | ROLL_C | 0.344 | 0.036 | 0.308 | 0.010 | 12.038 | 1.119 | 1.912 | 0.517 | -0.795 |
| CL | ROLL_D | 0.345 | 0.036 | 0.308 | 0.010 | 12.038 | 1.120 | 1.913 | 0.518 | -0.795 |
| CL | ROLL_E | 0.354 | 0.036 | 0.318 | 0.010 | 12.006 | 1.145 | 1.962 | 0.548 | -0.775 |
| CL | ROLL_F | 0.352 | 0.036 | 0.316 | 0.005 | 5.228 | 1.139 | 1.951 | 0.544 | -0.776 |
| NG | ROLL_A | -0.364 | -0.053 | -0.311 | 0.065 | 12.006 | -0.436 | -0.700 | -0.305 | -1.000 |
| NG | ROLL_B | -0.363 | -0.053 | -0.311 | 0.065 | 12.038 | -0.434 | -0.697 | -0.305 | -1.000 |
| NG | ROLL_C | -0.365 | -0.053 | -0.312 | 0.065 | 12.006 | -0.436 | -0.701 | -0.306 | -1.000 |
| NG | ROLL_D | -0.365 | -0.053 | -0.312 | 0.065 | 12.006 | -0.435 | -0.699 | -0.306 | -1.000 |
| NG | ROLL_E | -0.368 | -0.053 | -0.316 | 0.066 | 12.006 | -0.444 | -0.715 | -0.308 | -1.000 |
| NG | ROLL_F | -0.336 | -0.053 | -0.283 | 0.031 | 5.551 | -0.383 | -0.618 | -0.285 | -1.000 |
