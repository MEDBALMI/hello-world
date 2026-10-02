# 09 Oos Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

Splits: {'start': '1995-01-03', 'train_end': '2010-06-29', 'val_end': '2018-03-29', 'end': '2025-12-31'}. Parameters chosen on TRAIN only; OOS evaluated once.

| id | chosen | train | validation | walk_forward | OOS | OOS maxDD | machine_status |
|---|---|---|---|---|---|---|---|
| H01 | {"lookback": 126} | -0.21 | -0.09 | -0.42 | -0.26 | -0.13 | REJECTED |
| H02 | {} | -0.60 | 0.50 | -0.15 | 0.05 | -0.17 | REJECTED |
| H03 | {"n": 150} | -0.26 | -0.03 | -0.47 | -0.28 | -0.15 | REJECTED |
| H04 | {"fast": 50, "slow": 200} | -0.12 | 0.16 | -0.21 | 0.31 | -0.08 | REJECTED |
| H05 | {"entry": 252, "exit": 55} | -0.07 | 0.30 | -0.02 | 0.02 | -0.06 | WEAK |
| H06 | {"k": 2.0, "hold": 10} | 0.04 | 0.18 | 0.07 | 0.18 | -0.00 | WEAK |
| H07 | {"lookback": 63} | -0.12 | -0.05 | -0.38 | -0.86 | -0.28 | REJECTED |
| H08 | {} | -0.10 | 0.31 | 0.08 | -0.57 | -0.09 | REJECTED |
| H09 | {"entry": 55} | 0.28 | 0.51 | 0.42 | -0.25 | -0.05 | REJECTED |
| H10 | {"z": 2.5, "hold": 5} | 0.34 | -0.41 | 0.01 | 0.26 | -0.02 | WEAK |
| H11 | {"col": "carry_12m"} | 0.37 | 0.17 | 0.43 | 0.84 | -0.08 | WEAK |
| H12 | {"threshold": 1.0} | -0.07 | -0.64 | -0.34 | -0.19 | -0.11 | REJECTED |
| H13 | {"lookback": 126} | -0.32 | -0.45 | -0.41 | -0.10 | -0.08 | REJECTED |
| H14 | {"n": 150} | -0.25 | -0.39 | -0.53 | -0.07 | -0.09 | REJECTED |
| H15 | {"hi": 0.9, "lo": 0.05} | 0.04 | 0.19 | -0.06 | -0.18 | -0.09 | REJECTED |
| H16 | {} | -0.79 | -0.62 | -0.76 | -0.15 | -0.18 | REJECTED |
| H17 | {"hi": 0.9} | -0.26 | 0.18 | -0.35 | -0.36 | -0.15 | REJECTED |
| H18 | {} | -0.29 | -0.53 | -0.32 | 0.65 | -0.13 | REJECTED |
| H19 | {} | -0.18 | -0.31 | -0.18 | -0.29 | -0.23 | REJECTED |
| H20 | {"n": 200, "mult": 1.25} | -0.29 | 0.07 | -0.44 | -0.52 | -0.18 | REJECTED |
| H21 | {} | -0.53 | -0.01 | -0.23 | 0.14 | -0.07 | REJECTED |
| H22 | {"n": 200} | -0.58 | 0.11 | -0.42 | -0.18 | -0.08 | REJECTED |
| H23 | {} | -0.48 | 0.20 | -0.18 | 0.16 | -0.06 | REJECTED |
| H24 | {"z_in": 2.0, "z_out": 0.5} | 0.22 | -0.78 | -0.25 | -0.22 | -0.13 | REJECTED |
| H25 | {"n_long": 2, "n_short": 2} | -0.18 | 0.26 | -0.17 | -0.13 | -0.15 | REJECTED |
