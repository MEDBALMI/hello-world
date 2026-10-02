# 07 Strategy Research Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `CARRY`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

**Research breadth:** 27 hypotheses registered, 25 tested, 48 parameter combinations. White reality-check p (best of all trials) = 0.024 (best: H11|{"col": "carry_12m"}).

Machine status counts: {'WEAK': 13, 'REJECTED': 9, 'ROBUST': 2, 'PROMISING': 1, 'DATA-LIMITED': 1, 'DESIGN-LIMITED': 1}

| id | family | type | strategy | params | train | val | WF | OOS | DSR p | perm p | FDR | machine_status | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H01 | A_TSMOM | A | tsmom | {"lookback": 126} | 0.29 | 0.80 | 0.70 | 0.04 | 0.46 | 0.00 | True | WEAK | NOT-RESEARCH (SYNTHETIC) |
| H02 | A_TSMOM | A | tsmom_12_1 | {} | 0.10 | 1.07 | 0.74 | 0.32 | 0.53 | 0.00 | True | WEAK | NOT-RESEARCH (SYNTHETIC) |
| H03 | B_TREND | A | ma_trend | {"n": 150} | 0.62 | 0.46 | 0.49 | 0.18 | 0.28 | 0.00 | True | WEAK | NOT-RESEARCH (SYNTHETIC) |
| H04 | B_TREND | A | ma_cross | {"fast": 50, "slow": 200} | 0.36 | 0.67 | 0.41 | 0.49 | 0.46 | 0.01 | True | WEAK | NOT-RESEARCH (SYNTHETIC) |
| H05 | C_BREAKOUT | A | donchian | {"entry": 252, "exit": 55} | 0.45 | 1.01 | 0.71 | 0.54 | 0.17 | 0.00 | True | WEAK | NOT-RESEARCH (SYNTHETIC) |
| H06 | C_BREAKOUT | A | vol_breakout | {"k": 2.0, "hold": 10} | -0.22 | 0.06 | -0.26 | 0.10 | 1.00 | 0.65 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H07 | A_TSMOM | A | roc | {"lookback": 63} | 0.55 | 0.22 | 0.25 | -0.55 | 0.51 | 0.00 | True | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H08 | Q_EQUITY_TRANSFER | A | trend_template | {} | 0.61 | 0.98 | 0.86 | 0.32 | 0.07 | 0.00 | True | ROBUST | NOT-RESEARCH (SYNTHETIC) |
| H09 | Q_EQUITY_TRANSFER | A | vcp_breakout | {"entry": 55} | 0.56 | 1.03 | 0.99 | 0.15 | 0.08 | 0.00 | True | WEAK | NOT-RESEARCH (SYNTHETIC) |
| H10 | D_MEAN_REVERSION | A | mean_reversion | {"z": 2.5, "hold": 5} | 0.22 | -0.39 | -0.05 | -0.13 | 0.98 | 0.23 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H11 | F_CARRY | A | carry | {"col": "carry_12m"} | 1.01 | 1.05 | 1.28 | 1.14 | 0.00 | 0.00 | True | PROMISING | NOT-RESEARCH (SYNTHETIC) |
| H12 | E_TERM_STRUCTURE | A | carry_z | {"threshold": 1.0} | 0.03 | -0.62 | -0.29 | -0.42 | 1.00 | 0.33 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H13 | G_MOM_CARRY | A | mom_carry | {"lookback": 126} | 0.15 | 0.36 | 0.41 | 0.05 | 0.86 | 0.01 | True | WEAK | NOT-RESEARCH (SYNTHETIC) |
| H14 | H_TREND_CARRY | A | trend_carry_filter | {"n": 150} | 0.52 | 0.11 | 0.35 | 0.23 | 0.61 | 0.01 | True | WEAK | NOT-RESEARCH (SYNTHETIC) |
| H15 | I_POSITIONING | A | cot_contrarian | {"hi": 0.9, "lo": 0.05} | -0.02 | 0.32 | -0.06 | -0.34 | 0.96 | 0.16 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H16 | I_POSITIONING | A | cot_momentum | {} | -0.78 | -0.64 | -0.77 | -0.44 | 1.00 | 0.94 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H17 | I_POSITIONING | A | trend_cot | {"hi": 0.9} | 0.40 | 0.91 | 0.65 | 0.12 | 0.27 | 0.00 | True | WEAK | NOT-RESEARCH (SYNTHETIC) |
| H18 | K_MACRO | B | macro_real_yield | {} | -0.38 | -0.73 | -0.45 | 0.32 | 1.00 | 0.95 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H19 | K_MACRO | B | macro_usd | {} | 0.02 | -0.19 | 0.05 | -0.17 | 0.99 | 0.30 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H20 | M_VOL_REGIME | A | vol_regime_trend | {"n": 200, "mult": 1.25} | 0.53 | 0.69 | 0.57 | 0.10 | 0.25 | 0.00 | True | WEAK | NOT-RESEARCH (SYNTHETIC) |
| H21 | P_SEASONALITY | A | seasonal | {} | -0.28 | 0.88 | 0.48 | 0.48 | 0.94 | 0.13 | False | WEAK | NOT-RESEARCH (SYNTHETIC) |
| H22 | P_SEASONALITY | A | seasonal_trend | {"n": 200} | 0.13 | 1.09 | 0.73 | 0.41 | 0.46 | 0.00 | True | WEAK | NOT-RESEARCH (SYNTHETIC) |
| H23 | N_MULTI_FACTOR | A | multi_factor | {} | 0.05 | 0.84 | 0.53 | 0.12 | 0.74 | 0.01 | True | WEAK | NOT-RESEARCH (SYNTHETIC) |
| H24 | L_RELATIVE_VALUE | B | gold_silver_rv | {"z_in": 2.0, "z_out": 0.5} | 0.12 | -0.86 | -0.24 | -0.18 | 1.00 | 0.78 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H25 | C_XS_SELECTION | C | xs_momentum | {"n_long": 2, "n_short": 2} | 0.42 | 1.45 | 1.03 | 0.37 | 0.06 | 0.00 | True | ROBUST | NOT-RESEARCH (SYNTHETIC) |
| H26 | J_INVENTORY | A | – | – | – | – | – | – | – | – | – | DATA-LIMITED | NOT-RESEARCH (SYNTHETIC) |
| H27 | Q_EQUITY_TRANSFER | A | – | – | – | – | – | – | – | – | – | DESIGN-LIMITED | NOT-RESEARCH (SYNTHETIC) |

_Machine status = what the acceptance rules would assign; Status = final label (synthetic data can never produce research status)._
