# 07 Strategy Research Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

**Research breadth:** 27 hypotheses registered, 25 tested, 48 parameter combinations. White reality-check p (best of all trials) = 0.770 (best: H11|{"col": "carry_12m"}).

Machine status counts: {'REJECTED': 21, 'WEAK': 4, 'DATA-LIMITED': 1, 'DESIGN-LIMITED': 1}

| id | family | type | strategy | params | train | val | WF | OOS | DSR p | perm p | FDR | machine_status | status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| H01 | A_TSMOM | A | tsmom | {"lookback": 126} | -0.21 | -0.09 | -0.42 | -0.26 | 0.98 | 0.28 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H02 | A_TSMOM | A | tsmom_12_1 | {} | -0.60 | 0.50 | -0.15 | 0.05 | 0.99 | 0.53 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H03 | B_TREND | A | ma_trend | {"n": 150} | -0.26 | -0.03 | -0.47 | -0.28 | 0.98 | 0.20 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H04 | B_TREND | A | ma_cross | {"fast": 50, "slow": 200} | -0.12 | 0.16 | -0.21 | 0.31 | 0.91 | 0.33 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H05 | C_BREAKOUT | A | donchian | {"entry": 252, "exit": 55} | -0.07 | 0.30 | -0.02 | 0.02 | 0.83 | 0.25 | False | WEAK | NOT-RESEARCH (SYNTHETIC) |
| H06 | C_BREAKOUT | A | vol_breakout | {"k": 2.0, "hold": 10} | 0.04 | 0.18 | 0.07 | 0.18 | 0.80 | 0.29 | False | WEAK | NOT-RESEARCH (SYNTHETIC) |
| H07 | A_TSMOM | A | roc | {"lookback": 63} | -0.12 | -0.05 | -0.38 | -0.86 | 0.95 | 0.02 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H08 | Q_EQUITY_TRANSFER | A | trend_template | {} | -0.10 | 0.31 | 0.08 | -0.57 | 0.82 | 0.03 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H09 | Q_EQUITY_TRANSFER | A | vcp_breakout | {"entry": 55} | 0.28 | 0.51 | 0.42 | -0.25 | 0.29 | 0.01 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H10 | D_MEAN_REVERSION | A | mean_reversion | {"z": 2.5, "hold": 5} | 0.34 | -0.41 | 0.01 | 0.26 | 0.80 | 0.12 | False | WEAK | NOT-RESEARCH (SYNTHETIC) |
| H11 | F_CARRY | A | carry | {"col": "carry_12m"} | 0.37 | 0.17 | 0.43 | 0.84 | 0.41 | 0.04 | False | WEAK | NOT-RESEARCH (SYNTHETIC) |
| H12 | E_TERM_STRUCTURE | A | carry_z | {"threshold": 1.0} | -0.07 | -0.64 | -0.34 | -0.19 | 0.99 | 0.42 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H13 | G_MOM_CARRY | A | mom_carry | {"lookback": 126} | -0.32 | -0.45 | -0.41 | -0.10 | 1.00 | 0.43 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H14 | H_TREND_CARRY | A | trend_carry_filter | {"n": 150} | -0.25 | -0.39 | -0.53 | -0.07 | 1.00 | 0.27 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H15 | I_POSITIONING | A | cot_contrarian | {"hi": 0.9, "lo": 0.05} | 0.04 | 0.19 | -0.06 | -0.18 | 0.79 | 0.14 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H16 | I_POSITIONING | A | cot_momentum | {} | -0.79 | -0.62 | -0.76 | -0.15 | 1.00 | 0.96 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H17 | I_POSITIONING | A | trend_cot | {"hi": 0.9} | -0.26 | 0.18 | -0.35 | -0.36 | 0.96 | 0.15 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H18 | K_MACRO | B | macro_real_yield | {} | -0.29 | -0.53 | -0.32 | 0.65 | 1.00 | 0.91 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H19 | K_MACRO | B | macro_usd | {} | -0.18 | -0.31 | -0.18 | -0.29 | 0.99 | 0.31 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H20 | M_VOL_REGIME | A | vol_regime_trend | {"n": 200, "mult": 1.25} | -0.29 | 0.07 | -0.44 | -0.52 | 0.98 | 0.23 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H21 | P_SEASONALITY | A | seasonal | {} | -0.53 | -0.01 | -0.23 | 0.14 | 1.00 | 0.76 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H22 | P_SEASONALITY | A | seasonal_trend | {"n": 200} | -0.58 | 0.11 | -0.42 | -0.18 | 1.00 | 0.58 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H23 | N_MULTI_FACTOR | A | multi_factor | {} | -0.48 | 0.20 | -0.18 | 0.16 | 0.99 | 0.28 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H24 | L_RELATIVE_VALUE | B | gold_silver_rv | {"z_in": 2.0, "z_out": 0.5} | 0.22 | -0.78 | -0.25 | -0.22 | 0.97 | 0.74 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H25 | C_XS_SELECTION | C | xs_momentum | {"n_long": 2, "n_short": 2} | -0.18 | 0.26 | -0.17 | -0.13 | 0.92 | 0.11 | False | REJECTED | NOT-RESEARCH (SYNTHETIC) |
| H26 | J_INVENTORY | A | – | – | – | – | – | – | – | – | – | DATA-LIMITED | NOT-RESEARCH (SYNTHETIC) |
| H27 | Q_EQUITY_TRANSFER | A | – | – | – | – | – | – | – | – | – | DESIGN-LIMITED | NOT-RESEARCH (SYNTHETIC) |

_Machine status = what the acceptance rules would assign; Status = final label (synthetic data can never produce research status)._
