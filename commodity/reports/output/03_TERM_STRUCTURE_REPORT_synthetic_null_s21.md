# 03 Term Structure Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

## GC
- Backwardation share: 0.50; mean carry 0.009; carry autocorr(21d) 0.25
- IC carry→fwd 21d: 0.050 (t 0.97, n 371); IC CM slope: 0.050
- Realised vol in backwardation 0.15 vs contango 0.14

## SI
- Backwardation share: 0.46; mean carry -0.038; carry autocorr(21d) 0.32
- IC carry→fwd 21d: 0.027 (t 0.52, n 371); IC CM slope: -0.021
- Realised vol in backwardation 0.27 vs contango 0.27

## HG
- Backwardation share: 0.53; mean carry 0.026; carry autocorr(21d) 0.37
- IC carry→fwd 21d: 0.020 (t 0.38, n 371); IC CM slope: -0.071
- Realised vol in backwardation 0.23 vs contango 0.24

## CL
- Backwardation share: 0.34; mean carry -0.274; carry autocorr(21d) -0.40
- IC carry→fwd 21d: 0.004 (t 0.08, n 371); IC CM slope: 0.098
- Realised vol in backwardation 0.32 vs contango 0.32

## NG
- Backwardation share: 0.67; mean carry 0.370; carry autocorr(21d) 0.02
- IC carry→fwd 21d: 0.039 (t 0.76, n 371); IC CM slope: 0.097
- Realised vol in backwardation 0.48 vs contango 0.47

## Roll-rule comparison (per commodity)
| root | rule | total_return_ann | price_return_ann(CM30) | roll_return_ann | roll_cost_ann | rolls_per_year | sharpe | sortino | calmar | max_dd |
|---|---|---|---|---|---|---|---|---|---|---|
| GC | ROLL_A | -0.001 | -0.010 | 0.009 | 0.002 | 6.003 | 0.071 | 0.116 | -0.001 | -0.749 |
| GC | ROLL_B | 0.001 | -0.010 | 0.011 | 0.002 | 6.003 | 0.083 | 0.136 | 0.002 | -0.733 |
| GC | ROLL_C | 0.001 | -0.010 | 0.011 | 0.002 | 6.003 | 0.085 | 0.139 | 0.002 | -0.726 |
| GC | ROLL_D | 0.001 | -0.010 | 0.011 | 0.002 | 6.003 | 0.085 | 0.140 | 0.002 | -0.726 |
| GC | ROLL_E | -0.001 | -0.010 | 0.008 | 0.002 | 6.003 | 0.067 | 0.109 | -0.002 | -0.732 |
| GC | ROLL_F | 0.004 | -0.010 | 0.013 | 0.001 | 2.550 | 0.100 | 0.165 | 0.005 | -0.741 |
| SI | ROLL_A | -0.103 | -0.009 | -0.093 | 0.024 | 5.003 | -0.230 | -0.387 | -0.100 | -0.976 |
| SI | ROLL_B | -0.100 | -0.009 | -0.091 | 0.024 | 5.003 | -0.221 | -0.371 | -0.098 | -0.974 |
| SI | ROLL_C | -0.101 | -0.009 | -0.091 | 0.024 | 5.003 | -0.223 | -0.373 | -0.098 | -0.974 |
| SI | ROLL_D | -0.101 | -0.009 | -0.092 | 0.024 | 5.003 | -0.224 | -0.375 | -0.098 | -0.975 |
| SI | ROLL_E | -0.104 | -0.009 | -0.095 | 0.024 | 5.003 | -0.237 | -0.396 | -0.101 | -0.977 |
| SI | ROLL_F | -0.090 | -0.009 | -0.081 | 0.011 | 2.291 | -0.186 | -0.313 | -0.089 | -0.968 |
| HG | ROLL_A | -0.017 | -0.032 | 0.015 | 0.013 | 5.003 | 0.051 | 0.088 | -0.019 | -0.892 |
| HG | ROLL_B | -0.026 | -0.032 | 0.006 | 0.013 | 5.003 | 0.014 | 0.025 | -0.028 | -0.913 |
| HG | ROLL_C | -0.025 | -0.032 | 0.007 | 0.013 | 5.003 | 0.019 | 0.032 | -0.027 | -0.911 |
| HG | ROLL_D | -0.025 | -0.032 | 0.007 | 0.013 | 5.003 | 0.019 | 0.032 | -0.027 | -0.912 |
| HG | ROLL_E | -0.024 | -0.032 | 0.008 | 0.013 | 5.003 | 0.021 | 0.036 | -0.026 | -0.912 |
| HG | ROLL_F | -0.018 | -0.032 | 0.014 | 0.006 | 2.291 | 0.046 | 0.079 | -0.020 | -0.884 |
| CL | ROLL_A | -0.198 | 0.079 | -0.277 | 0.003 | 12.006 | -0.423 | -0.686 | -0.180 | -0.999 |
| CL | ROLL_B | -0.200 | 0.079 | -0.280 | 0.003 | 12.038 | -0.430 | -0.695 | -0.182 | -0.999 |
| CL | ROLL_C | -0.199 | 0.079 | -0.278 | 0.003 | 12.038 | -0.426 | -0.690 | -0.181 | -0.999 |
| CL | ROLL_D | -0.199 | 0.079 | -0.278 | 0.003 | 12.038 | -0.426 | -0.689 | -0.181 | -0.999 |
| CL | ROLL_E | -0.201 | 0.079 | -0.280 | 0.003 | 12.006 | -0.431 | -0.698 | -0.182 | -0.999 |
| CL | ROLL_F | -0.195 | 0.079 | -0.274 | 0.001 | 5.261 | -0.413 | -0.672 | -0.177 | -0.999 |
| NG | ROLL_A | 0.206 | -0.076 | 0.282 | 0.075 | 12.006 | 0.664 | 1.155 | 0.247 | -0.925 |
| NG | ROLL_B | 0.205 | -0.076 | 0.281 | 0.075 | 12.006 | 0.661 | 1.151 | 0.246 | -0.922 |
| NG | ROLL_C | 0.207 | -0.076 | 0.284 | 0.075 | 12.006 | 0.667 | 1.160 | 0.250 | -0.920 |
| NG | ROLL_D | 0.207 | -0.076 | 0.283 | 0.075 | 12.006 | 0.666 | 1.159 | 0.250 | -0.920 |
| NG | ROLL_E | 0.211 | -0.076 | 0.288 | 0.074 | 12.006 | 0.675 | 1.179 | 0.258 | -0.912 |
| NG | ROLL_F | 0.248 | -0.076 | 0.324 | 0.036 | 5.584 | 0.749 | 1.309 | 0.308 | -0.911 |
