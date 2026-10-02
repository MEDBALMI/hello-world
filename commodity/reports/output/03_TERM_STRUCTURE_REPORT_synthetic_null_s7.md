# 03 Term Structure Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

## GC
- Backwardation share: 0.47; mean carry -0.039; carry autocorr(21d) 0.24
- IC carry→fwd 21d: -0.010 (t -0.19, n 371); IC CM slope: -0.071
- Realised vol in backwardation 0.14 vs contango 0.14

## SI
- Backwardation share: 0.46; mean carry -0.036; carry autocorr(21d) 0.33
- IC carry→fwd 21d: -0.010 (t -0.19, n 371); IC CM slope: -0.178
- Realised vol in backwardation 0.28 vs contango 0.27

## HG
- Backwardation share: 0.53; mean carry 0.024; carry autocorr(21d) 0.35
- IC carry→fwd 21d: 0.007 (t 0.13, n 371); IC CM slope: 0.022
- Realised vol in backwardation 0.24 vs contango 0.23

## CL
- Backwardation share: 0.65; mean carry 0.324; carry autocorr(21d) -0.39
- IC carry→fwd 21d: -0.080 (t -1.55, n 371); IC CM slope: 0.105
- Realised vol in backwardation 0.36 vs contango 0.37

## NG
- Backwardation share: 0.38; mean carry -0.259; carry autocorr(21d) -0.10
- IC carry→fwd 21d: -0.078 (t -1.51, n 371); IC CM slope: -0.006
- Realised vol in backwardation 0.49 vs contango 0.49

## Roll-rule comparison (per commodity)
| root | rule | total_return_ann | price_return_ann(CM30) | roll_return_ann | roll_cost_ann | rolls_per_year | sharpe | sortino | calmar | max_dd |
|---|---|---|---|---|---|---|---|---|---|---|
| GC | ROLL_A | -0.058 | -0.008 | -0.050 | 0.003 | 6.003 | -0.322 | -0.533 | -0.067 | -0.840 |
| GC | ROLL_B | -0.055 | -0.008 | -0.048 | 0.003 | 6.003 | -0.306 | -0.507 | -0.065 | -0.828 |
| GC | ROLL_C | -0.055 | -0.008 | -0.047 | 0.003 | 6.003 | -0.303 | -0.502 | -0.064 | -0.827 |
| GC | ROLL_D | -0.055 | -0.008 | -0.047 | 0.003 | 6.003 | -0.304 | -0.503 | -0.065 | -0.828 |
| GC | ROLL_E | -0.055 | -0.008 | -0.048 | 0.003 | 6.003 | -0.307 | -0.508 | -0.065 | -0.828 |
| GC | ROLL_F | -0.056 | -0.008 | -0.049 | 0.001 | 2.647 | -0.314 | -0.520 | -0.066 | -0.826 |
| SI | ROLL_A | -0.036 | -0.004 | -0.032 | 0.006 | 5.003 | 0.013 | 0.021 | -0.038 | -0.941 |
| SI | ROLL_B | -0.040 | -0.004 | -0.035 | 0.006 | 5.003 | 0.001 | 0.002 | -0.041 | -0.944 |
| SI | ROLL_C | -0.040 | -0.004 | -0.035 | 0.006 | 5.003 | 0.002 | 0.003 | -0.041 | -0.945 |
| SI | ROLL_D | -0.040 | -0.004 | -0.036 | 0.006 | 5.003 | -0.000 | -0.000 | -0.042 | -0.945 |
| SI | ROLL_E | -0.035 | -0.004 | -0.031 | 0.006 | 5.003 | 0.017 | 0.028 | -0.037 | -0.938 |
| SI | ROLL_F | -0.028 | -0.004 | -0.023 | 0.003 | 2.324 | 0.043 | 0.071 | -0.030 | -0.921 |
| HG | ROLL_A | 0.048 | 0.027 | 0.022 | 0.002 | 5.003 | 0.320 | 0.523 | 0.088 | -0.559 |
| HG | ROLL_B | 0.051 | 0.027 | 0.024 | 0.002 | 5.003 | 0.330 | 0.539 | 0.094 | -0.554 |
| HG | ROLL_C | 0.051 | 0.027 | 0.024 | 0.002 | 5.003 | 0.330 | 0.539 | 0.094 | -0.553 |
| HG | ROLL_D | 0.051 | 0.027 | 0.025 | 0.002 | 5.003 | 0.332 | 0.543 | 0.095 | -0.553 |
| HG | ROLL_E | 0.053 | 0.027 | 0.026 | 0.002 | 5.003 | 0.338 | 0.552 | 0.098 | -0.552 |
| HG | ROLL_F | 0.043 | 0.027 | 0.017 | 0.001 | 2.098 | 0.300 | 0.491 | 0.080 | -0.555 |
| CL | ROLL_A | 0.154 | -0.081 | 0.235 | 0.087 | 12.006 | 0.600 | 1.045 | 0.187 | -0.889 |
| CL | ROLL_B | 0.144 | -0.081 | 0.225 | 0.089 | 12.038 | 0.573 | 0.995 | 0.172 | -0.900 |
| CL | ROLL_C | 0.143 | -0.081 | 0.225 | 0.088 | 12.038 | 0.572 | 0.992 | 0.171 | -0.901 |
| CL | ROLL_D | 0.143 | -0.081 | 0.225 | 0.088 | 12.038 | 0.572 | 0.992 | 0.171 | -0.901 |
| CL | ROLL_E | 0.154 | -0.081 | 0.235 | 0.087 | 12.006 | 0.599 | 1.045 | 0.188 | -0.886 |
| CL | ROLL_F | 0.195 | -0.081 | 0.276 | 0.039 | 5.228 | 0.709 | 1.244 | 0.244 | -0.881 |
| NG | ROLL_A | -0.203 | 0.067 | -0.271 | 0.027 | 12.006 | -0.129 | -0.206 | -0.184 | -0.999 |
| NG | ROLL_B | -0.199 | 0.067 | -0.266 | 0.027 | 12.038 | -0.120 | -0.191 | -0.180 | -0.999 |
| NG | ROLL_C | -0.201 | 0.067 | -0.269 | 0.027 | 12.006 | -0.125 | -0.200 | -0.183 | -0.999 |
| NG | ROLL_D | -0.202 | 0.067 | -0.269 | 0.027 | 12.006 | -0.125 | -0.200 | -0.183 | -0.999 |
| NG | ROLL_E | -0.205 | 0.067 | -0.273 | 0.027 | 12.006 | -0.133 | -0.213 | -0.186 | -0.999 |
| NG | ROLL_F | -0.191 | 0.067 | -0.259 | 0.013 | 5.616 | -0.106 | -0.170 | -0.174 | -0.999 |
