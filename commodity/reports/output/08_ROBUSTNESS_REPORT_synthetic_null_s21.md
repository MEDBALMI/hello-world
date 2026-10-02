# 08 Robustness Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

All on TRAIN+VALIDATION (OOS untouched). Sharpe values.

| id | param_share_pos | cost_x2 | cost_x3 | lag_2 | lag_3 | missing_5% | roll_rules_min | roll_rules_max | sub1 | sub2 | sub3 | boot_lo | boot_hi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H01 | 0.50 | -0.10 | -0.27 | 0.02 | -0.04 | 0.04 | -0.12 | 0.08 | 0.01 | 0.13 | 0.08 | -0.23 | 0.39 |
| H02 | 1.00 | -0.11 | -0.32 | 0.10 | 0.04 | 0.06 | 0.02 | 0.12 | 0.16 | 0.05 | 0.11 | -0.19 | 0.44 |
| H03 | 0.00 | -1.14 | -1.77 | -0.57 | -0.69 | -0.54 | -0.58 | -0.45 | -0.46 | 0.18 | -1.18 | -0.82 | -0.16 |
| H04 | 1.00 | 0.08 | -0.01 | 0.17 | 0.17 | 0.20 | 0.14 | 0.19 | 0.02 | 0.12 | 0.35 | -0.14 | 0.52 |
| H05 | 0.67 | 0.17 | 0.10 | 0.30 | 0.31 | 0.28 | 0.16 | 0.37 | 0.34 | 0.49 | -0.06 | -0.05 | 0.60 |
| H06 | 0.17 | 0.22 | 0.16 | 0.28 | 0.20 | 0.21 | -0.13 | 0.28 | 0.21 | 0.78 | -0.58 | -0.12 | 0.65 |
| H07 | 0.00 | -0.72 | -1.19 | -0.16 | 0.05 | -0.28 | -0.25 | -0.14 | -0.35 | 0.45 | -0.79 | -0.55 | 0.10 |
| H08 | 0.00 | -0.39 | -0.67 | -0.22 | -0.20 | -0.09 | -0.14 | -0.02 | 0.01 | 0.03 | -0.32 | -0.44 | 0.21 |
| H09 | 0.00 | -0.19 | -0.30 | -0.01 | -0.00 | -0.12 | -0.08 | 0.17 | -0.14 | 0.22 | -0.32 | -0.48 | 0.27 |
| H10 | 0.00 | -0.54 | -0.81 | -0.33 | -0.27 | -0.23 | -0.26 | -0.18 | 0.15 | -0.31 | -0.61 | -0.55 | 0.06 |
| H11 | 1.00 | -0.10 | -0.44 | 0.19 | 0.17 | 0.13 | 0.23 | 0.34 | 0.05 | 0.37 | 0.29 | -0.11 | 0.56 |
| H12 | 1.00 | -0.19 | -0.54 | 0.15 | 0.02 | 0.07 | 0.14 | 0.21 | 0.44 | 0.08 | -0.02 | -0.14 | 0.49 |
| H13 | 1.00 | -0.12 | -0.44 | 0.17 | 0.11 | 0.11 | 0.10 | 0.20 | -0.00 | 0.37 | 0.21 | -0.14 | 0.53 |
| H14 | 1.00 | -0.31 | -0.69 | 0.02 | 0.13 | 0.04 | 0.01 | 0.08 | -0.11 | 0.34 | 0.01 | -0.26 | 0.43 |
| H15 | 0.00 | -0.39 | -0.58 | -0.17 | -0.17 | -0.20 | -0.29 | -0.20 | -0.44 | 0.30 | -0.45 | -0.60 | 0.18 |
| H16 | 0.00 | -0.87 | -1.31 | -0.44 | -0.48 | -0.37 | -0.45 | -0.41 | 0.33 | -0.73 | -0.86 | -0.76 | -0.02 |
| H17 | 0.00 | -0.59 | -0.91 | -0.33 | -0.13 | -0.24 | -0.42 | -0.27 | -0.56 | 0.06 | -0.33 | -0.59 | 0.02 |
| H18 | 0.00 | -0.31 | -0.36 | -0.12 | -0.11 | -0.16 | -0.28 | -0.22 | 0.15 | -0.15 | -0.77 | -0.59 | 0.06 |
| H19 | 0.00 | -0.52 | -0.74 | -0.21 | -0.18 | -0.31 | -0.33 | -0.29 | -0.38 | -0.05 | -0.49 | -0.64 | 0.00 |
| H20 | 0.00 | -0.46 | -0.75 | -0.26 | -0.01 | -0.14 | -0.32 | -0.16 | -0.39 | 0.05 | -0.15 | -0.49 | 0.18 |
| H21 | 0.00 | -0.37 | -0.55 | -0.18 | -0.12 | -0.25 | -0.25 | -0.16 | 0.12 | -0.21 | -0.49 | -0.56 | 0.19 |
| H22 | 0.00 | -0.53 | -0.82 | -0.26 | -0.04 | -0.24 | -0.34 | -0.22 | -0.18 | -0.07 | -0.41 | -0.60 | 0.13 |
| H23 | 1.00 | -0.21 | -0.57 | 0.10 | 0.05 | 0.07 | 0.07 | 0.16 | -0.09 | 0.42 | 0.13 | -0.19 | 0.50 |
| H24 | 0.00 | -0.52 | -0.60 | -0.47 | -0.49 | -0.42 | -0.47 | -0.30 | -0.30 | -0.71 | -0.30 | -0.78 | -0.10 |
| H25 | 0.00 | -0.50 | -0.79 | -0.20 | -0.13 | -0.19 | -0.36 | -0.20 | -0.61 | 0.21 | -0.20 | -0.55 | 0.16 |

## Regime analysis
| id | regime | sharpe_true | sharpe_false |
|---|---|---|---|
| H01 | vol_high | 0.04 | 0.02 |
| H01 | backwardation | -0.21 | 0.20 |
| H01 | uptrend | -0.32 | 0.17 |
| H01 | real_yield_rising | 0.04 | 0.02 |
| H01 | usd_rising | -0.03 | 0.09 |
| H02 | vol_high | 0.16 | -0.07 |
| H02 | backwardation | -0.16 | 0.20 |
| H02 | uptrend | -0.24 | 0.11 |
| H02 | real_yield_rising | 0.13 | -0.03 |
| H02 | usd_rising | -0.17 | 0.26 |
| H03 | vol_high | -0.32 | -0.12 |
| H03 | backwardation | -0.29 | -0.16 |
| H03 | uptrend | -0.01 | -0.38 |
| H03 | real_yield_rising | -0.28 | -0.16 |
| H03 | usd_rising | -0.26 | -0.18 |
| H04 | vol_high | 0.05 | 0.09 |
| H04 | backwardation | -0.12 | 0.24 |
| H04 | uptrend | 0.04 | 0.05 |
| H04 | real_yield_rising | 0.11 | 0.03 |
| H04 | usd_rising | -0.04 | 0.18 |
| H05 | vol_high | 0.16 | 0.03 |
| H05 | backwardation | -0.05 | 0.22 |
| H05 | uptrend | 0.07 | 0.06 |
| H05 | real_yield_rising | 0.16 | 0.04 |
| H05 | usd_rising | 0.06 | 0.14 |
| H06 | vol_high | 0.14 | 0.03 |
| H06 | backwardation | 0.17 | 0.09 |
| H06 | uptrend | 0.14 | -0.05 |
| H06 | real_yield_rising | 0.05 | 0.17 |
| H06 | usd_rising | 0.11 | 0.08 |
| H07 | vol_high | -0.17 | -0.04 |
| H07 | backwardation | -0.28 | 0.04 |
| H07 | uptrend | 0.20 | -0.36 |
| H07 | real_yield_rising | -0.08 | -0.12 |
| H07 | usd_rising | -0.09 | -0.11 |
| H08 | vol_high | -0.04 | -0.12 |
| H08 | backwardation | 0.04 | -0.15 |
| H08 | uptrend | -0.10 | -0.44 |
| H08 | real_yield_rising | -0.07 | -0.07 |
| H08 | usd_rising | -0.10 | -0.02 |
| H09 | vol_high | -0.23 | 0.04 |
| H09 | backwardation | -0.10 | -0.02 |
| H09 | uptrend | -0.08 | -0.61 |
| H09 | real_yield_rising | -0.16 | -0.03 |
| H09 | usd_rising | -0.21 | 0.05 |
| H10 | vol_high | -0.22 | -0.01 |
| H10 | backwardation | -0.02 | -0.18 |
| H10 | uptrend | -0.27 | 0.01 |
| H10 | real_yield_rising | -0.09 | -0.15 |
| H10 | usd_rising | -0.23 | 0.01 |
| H11 | vol_high | 0.11 | 0.12 |
| H11 | backwardation | 0.06 | 0.08 |
| H11 | uptrend | 0.17 | -0.03 |
| H11 | real_yield_rising | 0.16 | 0.05 |
| H11 | usd_rising | -0.13 | 0.32 |
| H12 | vol_high | 0.11 | 0.07 |
| H12 | backwardation | 0.07 | 0.05 |
| H12 | uptrend | -0.10 | 0.20 |
| H12 | real_yield_rising | 0.12 | 0.03 |
| H12 | usd_rising | 0.11 | 0.03 |
| H13 | vol_high | 0.09 | 0.08 |
| H13 | backwardation | -0.13 | 0.14 |
| H13 | uptrend | -0.11 | 0.05 |
| H13 | real_yield_rising | 0.12 | 0.05 |
| H13 | usd_rising | -0.13 | 0.28 |
| H14 | vol_high | 0.13 | -0.06 |
| H14 | backwardation | -0.27 | 0.22 |
| H14 | uptrend | 0.01 | -0.13 |
| H14 | real_yield_rising | -0.02 | 0.09 |
| H14 | usd_rising | -0.08 | 0.14 |
| H15 | vol_high | -0.22 | 0.03 |
| H15 | backwardation | -0.18 | -0.01 |
| H15 | uptrend | -0.26 | 0.05 |
| H15 | real_yield_rising | -0.17 | -0.04 |
| H15 | usd_rising | -0.10 | -0.08 |
| H16 | vol_high | -0.28 | -0.08 |
| H16 | backwardation | -0.19 | -0.21 |
| H16 | uptrend | -0.19 | -0.24 |
| H16 | real_yield_rising | -0.21 | -0.16 |
| H16 | usd_rising | -0.43 | 0.05 |
| H17 | vol_high | -0.07 | -0.17 |
| H17 | backwardation | -0.35 | 0.10 |
| H17 | uptrend | -0.21 | -0.14 |
| H17 | real_yield_rising | -0.11 | -0.12 |
| H17 | usd_rising | -0.15 | -0.09 |
| H18 | vol_high | -0.23 | -0.28 |
| H18 | backwardation | -0.21 | -0.31 |
| H18 | uptrend | -0.55 | -0.02 |
| H18 | real_yield_rising | -0.29 | -0.23 |
| H18 | usd_rising | -0.24 | -0.28 |
| H19 | vol_high | -0.20 | -0.15 |
| H19 | backwardation | -0.13 | -0.20 |
| H19 | uptrend | -0.25 | -0.15 |
| H19 | real_yield_rising | -0.08 | -0.26 |
| H19 | usd_rising | 0.07 | -0.41 |
| H20 | vol_high | -0.02 | -0.13 |
| H20 | backwardation | -0.31 | 0.15 |
| H20 | uptrend | -0.22 | -0.07 |
| H20 | real_yield_rising | -0.06 | -0.08 |
| H20 | usd_rising | -0.13 | -0.01 |
| H21 | vol_high | -0.01 | -0.16 |
| H21 | backwardation | -0.10 | -0.09 |
| H21 | uptrend | -0.13 | -0.09 |
| H21 | real_yield_rising | 0.01 | -0.18 |
| H21 | usd_rising | -0.24 | 0.06 |
| H22 | vol_high | -0.02 | -0.21 |
| H22 | backwardation | -0.31 | 0.06 |
| H22 | uptrend | -0.29 | -0.15 |
| H22 | real_yield_rising | -0.03 | -0.18 |
| H22 | usd_rising | -0.24 | 0.02 |
| H23 | vol_high | 0.06 | 0.09 |
| H23 | backwardation | -0.16 | 0.14 |
| H23 | uptrend | -0.11 | 0.04 |
| H23 | real_yield_rising | 0.11 | 0.03 |
| H23 | usd_rising | -0.11 | 0.24 |
| H24 | vol_high | -0.48 | -0.15 |
| H24 | backwardation | -0.08 | -0.52 |
| H24 | uptrend | -0.66 | -0.04 |
| H24 | real_yield_rising | -0.35 | -0.27 |
| H24 | usd_rising | -0.08 | -0.51 |
| H25 | vol_high | -0.12 | -0.09 |
| H25 | backwardation | -0.21 | -0.00 |
| H25 | uptrend | 0.06 | -0.36 |
| H25 | real_yield_rising | -0.06 | -0.13 |
| H25 | usd_rising | -0.33 | 0.13 |
