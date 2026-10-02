# 09 Oos Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

Splits: {'start': '1995-01-03', 'train_end': '2010-06-29', 'val_end': '2018-03-29', 'end': '2025-12-31'}. Parameters chosen on TRAIN only; OOS evaluated once.

| id | chosen | train | validation | walk_forward | OOS | OOS maxDD | machine_status |
|---|---|---|---|---|---|---|---|
| H01 | {"lookback": 252} | 0.08 | 0.08 | 0.09 | 0.52 | -0.11 | WEAK |
| H02 | {} | 0.10 | 0.11 | 0.05 | 0.37 | -0.09 | WEAK |
| H03 | {"n": 50} | -0.14 | -1.18 | -0.13 | -0.72 | -0.25 | REJECTED |
| H04 | {"fast": 50, "slow": 150} | 0.07 | 0.35 | 0.27 | 0.13 | -0.10 | WEAK |
| H05 | {"entry": 252, "exit": 55} | 0.42 | -0.06 | 0.20 | 0.21 | -0.06 | WEAK |
| H06 | {"k": 2.0, "hold": 5} | 0.55 | -0.58 | 0.32 | -0.04 | -0.01 | REJECTED |
| H07 | {"lookback": 63} | 0.05 | -0.79 | -0.15 | -0.18 | -0.19 | REJECTED |
| H08 | {} | 0.02 | -0.32 | -0.15 | -0.32 | -0.07 | REJECTED |
| H09 | {"entry": 55} | 0.04 | -0.32 | -0.05 | 0.03 | -0.07 | REJECTED |
| H10 | {"z": 2.5, "hold": 5} | -0.09 | -0.61 | -0.57 | -0.09 | -0.05 | REJECTED |
| H11 | {"col": "carry"} | 0.21 | 0.29 | 0.41 | 0.07 | -0.10 | WEAK |
| H12 | {"threshold": 1.0} | 0.25 | -0.02 | -0.23 | -0.81 | -0.18 | REJECTED |
| H13 | {"lookback": 252} | 0.20 | 0.21 | 0.28 | 0.41 | -0.08 | WEAK |
| H14 | {"n": 200} | 0.12 | 0.01 | 0.11 | 0.15 | -0.09 | WEAK |
| H15 | {"hi": 0.9, "lo": 0.05} | -0.06 | -0.45 | -0.06 | 0.34 | -0.04 | REJECTED |
| H16 | {} | -0.19 | -0.86 | -0.72 | -1.05 | -0.32 | REJECTED |
| H17 | {"hi": 0.9} | -0.24 | -0.33 | -0.12 | 0.31 | -0.12 | REJECTED |
| H18 | {} | 0.00 | -0.77 | -0.41 | -0.32 | -0.42 | REJECTED |
| H19 | {} | -0.21 | -0.49 | -0.30 | -0.18 | -0.25 | REJECTED |
| H20 | {"n": 200, "mult": 1.5} | -0.17 | -0.15 | -0.02 | 0.30 | -0.12 | REJECTED |
| H21 | {} | -0.05 | -0.49 | -0.37 | -0.16 | -0.14 | REJECTED |
| H22 | {"n": 200} | -0.12 | -0.41 | -0.23 | 0.12 | -0.08 | REJECTED |
| H23 | {} | 0.18 | 0.13 | 0.25 | 0.48 | -0.06 | WEAK |
| H24 | {"z_in": 2.0, "z_out": 0.5} | -0.52 | -0.30 | -0.52 | -0.32 | -0.27 | REJECTED |
| H25 | {"n_long": 2, "n_short": 2} | -0.19 | -0.20 | 0.03 | 0.42 | -0.08 | REJECTED |
