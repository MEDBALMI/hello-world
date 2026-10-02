# 09 Oos Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `CARRY`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

Splits: {'start': '1995-01-03', 'train_end': '2010-06-29', 'val_end': '2018-03-29', 'end': '2025-12-31'}. Parameters chosen on TRAIN only; OOS evaluated once.

| id | chosen | train | validation | walk_forward | OOS | OOS maxDD | machine_status |
|---|---|---|---|---|---|---|---|
| H01 | {"lookback": 126} | 0.29 | 0.80 | 0.70 | 0.04 | -0.13 | WEAK |
| H02 | {} | 0.10 | 1.07 | 0.74 | 0.32 | -0.11 | WEAK |
| H03 | {"n": 150} | 0.62 | 0.46 | 0.49 | 0.18 | -0.10 | WEAK |
| H04 | {"fast": 50, "slow": 200} | 0.36 | 0.67 | 0.41 | 0.49 | -0.09 | WEAK |
| H05 | {"entry": 252, "exit": 55} | 0.45 | 1.01 | 0.71 | 0.54 | -0.06 | WEAK |
| H06 | {"k": 2.0, "hold": 10} | -0.22 | 0.06 | -0.26 | 0.10 | -0.01 | REJECTED |
| H07 | {"lookback": 63} | 0.55 | 0.22 | 0.25 | -0.55 | -0.20 | REJECTED |
| H08 | {} | 0.61 | 0.98 | 0.86 | 0.32 | -0.04 | ROBUST |
| H09 | {"entry": 55} | 0.56 | 1.03 | 0.99 | 0.15 | -0.03 | WEAK |
| H10 | {"z": 2.5, "hold": 5} | 0.22 | -0.39 | -0.05 | -0.13 | -0.03 | REJECTED |
| H11 | {"col": "carry_12m"} | 1.01 | 1.05 | 1.28 | 1.14 | -0.06 | PROMISING |
| H12 | {"threshold": 1.0} | 0.03 | -0.62 | -0.29 | -0.42 | -0.14 | REJECTED |
| H13 | {"lookback": 126} | 0.15 | 0.36 | 0.41 | 0.05 | -0.07 | WEAK |
| H14 | {"n": 150} | 0.52 | 0.11 | 0.35 | 0.23 | -0.06 | WEAK |
| H15 | {"hi": 0.9, "lo": 0.05} | -0.02 | 0.32 | -0.06 | -0.34 | -0.09 | REJECTED |
| H16 | {} | -0.78 | -0.64 | -0.77 | -0.44 | -0.22 | REJECTED |
| H17 | {"hi": 0.9} | 0.40 | 0.91 | 0.65 | 0.12 | -0.09 | WEAK |
| H18 | {} | -0.38 | -0.73 | -0.45 | 0.32 | -0.17 | REJECTED |
| H19 | {} | 0.02 | -0.19 | 0.05 | -0.17 | -0.20 | REJECTED |
| H20 | {"n": 200, "mult": 1.25} | 0.53 | 0.69 | 0.57 | 0.10 | -0.12 | WEAK |
| H21 | {} | -0.28 | 0.88 | 0.48 | 0.48 | -0.09 | WEAK |
| H22 | {"n": 200} | 0.13 | 1.09 | 0.73 | 0.41 | -0.05 | WEAK |
| H23 | {} | 0.05 | 0.84 | 0.53 | 0.12 | -0.05 | WEAK |
| H24 | {"z_in": 2.0, "z_out": 0.5} | 0.12 | -0.86 | -0.24 | -0.18 | -0.13 | REJECTED |
| H25 | {"n_long": 2, "n_short": 2} | 0.42 | 1.45 | 1.03 | 0.37 | -0.11 | ROBUST |
