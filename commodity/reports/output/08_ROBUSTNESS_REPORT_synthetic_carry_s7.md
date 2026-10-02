# 08 Robustness Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `CARRY`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

All on TRAIN+VALIDATION (OOS untouched). Sharpe values.

| id | param_share_pos | cost_x2 | cost_x3 | lag_2 | lag_3 | missing_5% | roll_rules_min | roll_rules_max | sub1 | sub2 | sub3 | boot_lo | boot_hi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H01 | 1.00 | 0.29 | 0.12 | 0.44 | 0.40 | 0.41 | 0.29 | 0.54 | 0.44 | 0.15 | 0.80 | 0.10 | 0.78 |
| H02 | 1.00 | 0.32 | 0.21 | 0.45 | 0.47 | 0.37 | 0.32 | 0.43 | -0.21 | 0.38 | 1.07 | 0.11 | 0.78 |
| H03 | 1.00 | 0.37 | 0.17 | 0.58 | 0.60 | 0.48 | 0.34 | 0.68 | 0.74 | 0.51 | 0.46 | 0.21 | 0.91 |
| H04 | 1.00 | 0.44 | 0.41 | 0.49 | 0.42 | 0.41 | 0.39 | 0.50 | 0.38 | 0.34 | 0.67 | 0.10 | 0.78 |
| H05 | 1.00 | 0.62 | 0.60 | 0.68 | 0.67 | 0.55 | 0.64 | 0.70 | 0.23 | 0.65 | 1.01 | 0.29 | 0.97 |
| H06 | 0.00 | -0.17 | -0.20 | -0.19 | -0.23 | -0.17 | -0.34 | -0.08 | -0.05 | -0.34 | 0.06 | -0.48 | 0.25 |
| H07 | 0.50 | 0.12 | -0.19 | 0.30 | 0.26 | 0.36 | 0.29 | 0.51 | 0.83 | 0.28 | 0.22 | 0.09 | 0.75 |
| H08 | 1.00 | 0.60 | 0.46 | 0.65 | 0.61 | 0.64 | 0.75 | 0.83 | 0.48 | 0.72 | 0.98 | 0.33 | 1.10 |
| H09 | 1.00 | 0.67 | 0.60 | 0.71 | 0.63 | 0.61 | 0.57 | 0.75 | 0.10 | 0.94 | 1.03 | 0.37 | 1.08 |
| H10 | 0.33 | -0.18 | -0.37 | 0.12 | 0.06 | 0.01 | -0.08 | 0.03 | 0.23 | 0.21 | -0.39 | -0.36 | 0.33 |
| H11 | 0.50 | 0.97 | 0.91 | 1.00 | 1.05 | 0.88 | 0.97 | 1.02 | 0.55 | 1.46 | 1.05 | 0.68 | 1.34 |
| H12 | 0.00 | -0.42 | -0.66 | -0.20 | -0.26 | -0.23 | -0.22 | -0.17 | -0.09 | 0.13 | -0.62 | -0.53 | 0.18 |
| H13 | 1.00 | -0.03 | -0.28 | 0.18 | 0.15 | 0.15 | 0.12 | 0.27 | 0.07 | 0.22 | 0.36 | -0.12 | 0.55 |
| H14 | 1.00 | 0.12 | -0.13 | 0.49 | 0.48 | 0.29 | 0.24 | 0.50 | 0.47 | 0.57 | 0.11 | 0.06 | 0.75 |
| H15 | 0.50 | -0.04 | -0.17 | -0.02 | -0.10 | 0.12 | 0.09 | 0.12 | 0.38 | -0.40 | 0.32 | -0.25 | 0.41 |
| H16 | 0.00 | -1.10 | -1.44 | -0.62 | -0.76 | -0.79 | -0.76 | -0.71 | -0.60 | -0.96 | -0.64 | -1.09 | -0.39 |
| H17 | 1.00 | 0.39 | 0.21 | 0.51 | 0.54 | 0.51 | 0.56 | 0.60 | 0.46 | 0.34 | 0.91 | 0.21 | 0.91 |
| H18 | 0.00 | -0.65 | -0.81 | -0.53 | -0.54 | -0.47 | -0.51 | -0.49 | -0.71 | -0.05 | -0.73 | -0.85 | -0.09 |
| H19 | 0.00 | -0.21 | -0.38 | 0.11 | 0.03 | -0.12 | -0.07 | -0.04 | -0.27 | 0.31 | -0.19 | -0.41 | 0.29 |
| H20 | 1.00 | 0.41 | 0.23 | 0.56 | 0.62 | 0.50 | 0.56 | 0.61 | 0.65 | 0.42 | 0.69 | 0.19 | 0.95 |
| H21 | 1.00 | -0.03 | -0.17 | 0.05 | 0.08 | 0.04 | 0.10 | 0.17 | -0.63 | 0.04 | 0.88 | -0.25 | 0.44 |
| H22 | 1.00 | 0.29 | 0.12 | 0.42 | 0.47 | 0.37 | 0.47 | 0.51 | -0.09 | 0.32 | 1.09 | 0.12 | 0.81 |
| H23 | 1.00 | 0.08 | -0.15 | 0.28 | 0.30 | 0.26 | 0.24 | 0.37 | -0.12 | 0.19 | 0.84 | -0.03 | 0.67 |
| H24 | 0.00 | -0.30 | -0.36 | -0.27 | -0.29 | -0.23 | -0.31 | -0.21 | -0.27 | 0.50 | -0.86 | -0.58 | 0.13 |
| H25 | 1.00 | 0.64 | 0.50 | 0.78 | 0.74 | 0.75 | 0.58 | 0.77 | 0.32 | 0.51 | 1.45 | 0.41 | 1.11 |

## Regime analysis
| id | regime | sharpe_true | sharpe_false |
|---|---|---|---|
| H01 | vol_high | 0.23 | 0.18 |
| H01 | backwardation | 0.24 | 0.17 |
| H01 | uptrend | 0.32 | -0.12 |
| H01 | real_yield_rising | 0.15 | 0.26 |
| H01 | usd_rising | 0.27 | 0.16 |
| H02 | vol_high | 0.22 | 0.15 |
| H02 | backwardation | 0.18 | 0.19 |
| H02 | uptrend | -0.24 | 0.01 |
| H02 | real_yield_rising | 0.20 | 0.19 |
| H02 | usd_rising | 0.19 | 0.19 |
| H03 | vol_high | 0.21 | 0.27 |
| H03 | backwardation | 0.30 | 0.23 |
| H03 | uptrend | 0.30 | 0.01 |
| H03 | real_yield_rising | 0.21 | 0.29 |
| H03 | usd_rising | 0.24 | 0.26 |
| H04 | vol_high | 0.23 | 0.17 |
| H04 | backwardation | 0.13 | 0.27 |
| H04 | uptrend | 0.17 | -0.15 |
| H04 | real_yield_rising | 0.14 | 0.27 |
| H04 | usd_rising | 0.17 | 0.24 |
| H05 | vol_high | 0.34 | 0.21 |
| H05 | backwardation | 0.35 | 0.20 |
| H05 | uptrend | 0.10 | -0.00 |
| H05 | real_yield_rising | 0.35 | 0.21 |
| H05 | usd_rising | 0.25 | 0.30 |
| H06 | vol_high | -0.07 | -0.03 |
| H06 | backwardation | -0.10 | -0.11 |
| H06 | uptrend | -0.09 | -0.09 |
| H06 | real_yield_rising | 0.17 | -0.28 |
| H06 | usd_rising | -0.16 | -0.02 |
| H07 | vol_high | 0.14 | 0.25 |
| H07 | backwardation | 0.22 | 0.14 |
| H07 | uptrend | 0.27 | -0.02 |
| H07 | real_yield_rising | 0.21 | 0.18 |
| H07 | usd_rising | 0.21 | 0.18 |
| H08 | vol_high | 0.21 | 0.16 |
| H08 | backwardation | 0.21 | 0.21 |
| H08 | uptrend | 0.17 | -0.32 |
| H08 | real_yield_rising | 0.29 | 0.04 |
| H08 | usd_rising | 0.19 | 0.20 |
| H09 | vol_high | 0.16 | 0.25 |
| H09 | backwardation | 0.34 | 0.08 |
| H09 | uptrend | 0.26 | -0.37 |
| H09 | real_yield_rising | 0.38 | -0.01 |
| H09 | usd_rising | 0.32 | 0.12 |
| H10 | vol_high | 0.01 | -0.02 |
| H10 | backwardation | -0.17 | 0.16 |
| H10 | uptrend | 0.11 | -0.01 |
| H10 | real_yield_rising | -0.01 | 0.03 |
| H10 | usd_rising | -0.14 | 0.10 |
| H11 | vol_high | 0.61 | 0.31 |
| H11 | backwardation | 0.38 | 0.53 |
| H11 | uptrend | 0.12 | 0.05 |
| H11 | real_yield_rising | 0.41 | 0.48 |
| H11 | usd_rising | 0.42 | 0.47 |
| H12 | vol_high | -0.07 | -0.11 |
| H12 | backwardation | 0.02 | -0.29 |
| H12 | uptrend | -0.12 | -0.04 |
| H12 | real_yield_rising | 0.05 | -0.20 |
| H12 | usd_rising | 0.01 | -0.15 |
| H13 | vol_high | 0.08 | 0.11 |
| H13 | backwardation | 0.08 | -0.13 |
| H13 | uptrend | 0.27 | -0.37 |
| H13 | real_yield_rising | 0.18 | 0.01 |
| H13 | usd_rising | 0.22 | 0.01 |
| H14 | vol_high | 0.08 | 0.27 |
| H14 | backwardation | 0.16 | 0.00 |
| H14 | uptrend | 0.24 | -0.19 |
| H14 | real_yield_rising | 0.22 | 0.13 |
| H14 | usd_rising | 0.23 | 0.13 |
| H15 | vol_high | 0.07 | -0.01 |
| H15 | backwardation | 0.26 | -0.14 |
| H15 | uptrend | -0.22 | 0.36 |
| H15 | real_yield_rising | 0.15 | -0.06 |
| H15 | usd_rising | 0.09 | 0.00 |
| H16 | vol_high | -0.18 | -0.50 |
| H16 | backwardation | -0.33 | -0.32 |
| H16 | uptrend | -0.34 | -0.32 |
| H16 | real_yield_rising | -0.37 | -0.30 |
| H16 | usd_rising | -0.42 | -0.27 |
| H17 | vol_high | 0.22 | 0.29 |
| H17 | backwardation | 0.25 | 0.27 |
| H17 | uptrend | 0.05 | 0.06 |
| H17 | real_yield_rising | 0.25 | 0.26 |
| H17 | usd_rising | 0.36 | 0.18 |
| H18 | vol_high | -0.25 | -0.77 |
| H18 | backwardation | -0.75 | -0.26 |
| H18 | uptrend | -0.63 | -0.43 |
| H18 | real_yield_rising | 0.09 | -1.00 |
| H18 | usd_rising | -0.95 | -0.17 |
| H19 | vol_high | -0.11 | 0.05 |
| H19 | backwardation | -0.18 | 0.18 |
| H19 | uptrend | 0.36 | -0.51 |
| H19 | real_yield_rising | -0.29 | 0.20 |
| H19 | usd_rising | -0.47 | 0.29 |
| H20 | vol_high | 0.25 | 0.27 |
| H20 | backwardation | 0.28 | 0.25 |
| H20 | uptrend | 0.09 | 0.01 |
| H20 | real_yield_rising | 0.23 | 0.29 |
| H20 | usd_rising | 0.33 | 0.20 |
| H21 | vol_high | 0.05 | 0.05 |
| H21 | backwardation | 0.05 | 0.08 |
| H21 | uptrend | -0.02 | -0.37 |
| H21 | real_yield_rising | 0.18 | -0.07 |
| H21 | usd_rising | -0.02 | 0.10 |
| H22 | vol_high | 0.20 | 0.19 |
| H22 | backwardation | 0.23 | 0.20 |
| H22 | uptrend | -0.15 | -0.36 |
| H22 | real_yield_rising | 0.27 | 0.13 |
| H22 | usd_rising | 0.20 | 0.20 |
| H23 | vol_high | 0.15 | 0.11 |
| H23 | backwardation | 0.21 | -0.16 |
| H23 | uptrend | -0.11 | -0.17 |
| H23 | real_yield_rising | 0.30 | -0.01 |
| H23 | usd_rising | 0.28 | 0.05 |
| H24 | vol_high | -0.43 | 0.18 |
| H24 | backwardation | -0.37 | 0.02 |
| H24 | uptrend | -0.52 | 0.04 |
| H24 | real_yield_rising | -0.26 | -0.09 |
| H24 | usd_rising | -0.36 | -0.03 |
| H25 | vol_high | 0.36 | 0.27 |
| H25 | backwardation | 0.37 | 0.28 |
| H25 | uptrend | 0.06 | -0.11 |
| H25 | real_yield_rising | 0.38 | 0.26 |
| H25 | usd_rising | 0.36 | 0.29 |
