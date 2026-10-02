# 06 Commodity Feature Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

Spearman IC vs next-21d tradable return, non-overlapping monthly samples.

| root | feature | ic | t | p | n |
|---|---|---|---|---|---|
| GC | ret_63 | 0.010 | 0.189 | 0.851 | 368 |
| GC | ret_252 | -0.017 | -0.314 | 0.754 | 359 |
| GC | tsmom_12_1 | -0.005 | -0.100 | 0.920 | 359 |
| GC | dist_ma_200 | -0.013 | -0.238 | 0.812 | 362 |
| GC | carry | -0.010 | -0.191 | 0.849 | 371 |
| GC | carry_z | -0.006 | -0.119 | 0.906 | 365 |
| GC | slope_cm | -0.071 | -1.360 | 0.175 | 366 |
| GC | carry_12m | 0.015 | 0.291 | 0.771 | 371 |
| GC | z_ret_5 | 0.138 | 2.678 | 0.008 | 369 |
| GC | trend_template | -0.056 | -1.079 | 0.281 | 371 |
| GC | vcp_contraction | 0.017 | 0.324 | 0.746 | 371 |
| GC | season_score | -0.117 | -2.225 | 0.027 | 359 |
| GC | mm_z | -0.049 | -0.921 | 0.357 | 359 |
| GC | DFII10_chg_63 | 0.048 | 0.916 | 0.360 | 368 |
| GC | DTWEXBGS_chg_63 | 0.018 | 0.344 | 0.731 | 368 |
| SI | ret_63 | 0.001 | 0.023 | 0.982 | 368 |
| SI | ret_252 | 0.042 | 0.785 | 0.433 | 359 |
| SI | tsmom_12_1 | 0.032 | 0.610 | 0.542 | 359 |
| SI | dist_ma_200 | 0.038 | 0.723 | 0.470 | 362 |
| SI | carry | -0.010 | -0.191 | 0.848 | 371 |
| SI | carry_z | 0.031 | 0.592 | 0.554 | 365 |
| SI | slope_cm | -0.178 | -2.482 | 0.014 | 190 |
| SI | carry_12m | -0.073 | -1.397 | 0.163 | 371 |
| SI | z_ret_5 | 0.067 | 1.278 | 0.202 | 369 |
| SI | trend_template | -0.088 | -1.703 | 0.089 | 371 |
| SI | vcp_contraction | -0.094 | -1.815 | 0.070 | 371 |
| SI | season_score | 0.005 | 0.091 | 0.928 | 359 |
| SI | mm_z | -0.076 | -1.437 | 0.152 | 359 |
| SI | DFII10_chg_63 | 0.004 | 0.077 | 0.939 | 368 |
| SI | DTWEXBGS_chg_63 | -0.045 | -0.867 | 0.386 | 368 |
| HG | ret_63 | -0.029 | -0.552 | 0.581 | 368 |
| HG | ret_252 | -0.048 | -0.916 | 0.361 | 359 |
| HG | tsmom_12_1 | -0.066 | -1.255 | 0.210 | 359 |
| HG | dist_ma_200 | -0.052 | -0.982 | 0.327 | 362 |
| HG | carry | 0.007 | 0.127 | 0.899 | 371 |
| HG | carry_z | -0.037 | -0.701 | 0.484 | 365 |
| HG | slope_cm | 0.022 | 0.424 | 0.671 | 366 |
| HG | carry_12m | 0.029 | 0.558 | 0.577 | 371 |
| HG | z_ret_5 | -0.035 | -0.666 | 0.506 | 369 |
| HG | trend_template | 0.027 | 0.515 | 0.607 | 371 |
| HG | vcp_contraction | 0.038 | 0.736 | 0.462 | 371 |
| HG | season_score | -0.101 | -1.926 | 0.055 | 359 |
| HG | mm_z | -0.016 | -0.296 | 0.768 | 359 |
| HG | DFII10_chg_63 | 0.082 | 1.581 | 0.115 | 368 |
| HG | DTWEXBGS_chg_63 | 0.000 | 0.005 | 0.996 | 368 |
| CL | ret_63 | 0.073 | 1.408 | 0.160 | 368 |
| CL | ret_252 | 0.063 | 1.189 | 0.235 | 359 |
| CL | tsmom_12_1 | 0.064 | 1.207 | 0.228 | 359 |
| CL | dist_ma_200 | 0.009 | 0.166 | 0.868 | 362 |
| CL | carry | -0.080 | -1.547 | 0.123 | 371 |
| CL | carry_z | -0.102 | -1.950 | 0.052 | 365 |
| CL | slope_cm | 0.105 | 2.006 | 0.046 | 366 |
| CL | carry_12m | 0.123 | 2.388 | 0.017 | 371 |
| CL | z_ret_5 | -0.005 | -0.099 | 0.921 | 369 |
| CL | trend_template | 0.010 | 0.195 | 0.846 | 371 |
| CL | vcp_contraction | -0.033 | -0.627 | 0.531 | 371 |
| CL | season_score | 0.015 | 0.289 | 0.773 | 359 |
| CL | mm_z | 0.030 | 0.562 | 0.574 | 359 |
| CL | DFII10_chg_63 | 0.019 | 0.372 | 0.710 | 368 |
| CL | DTWEXBGS_chg_63 | -0.092 | -1.763 | 0.079 | 368 |
| NG | ret_63 | 0.020 | 0.381 | 0.703 | 368 |
| NG | ret_252 | -0.058 | -1.105 | 0.270 | 359 |
| NG | tsmom_12_1 | -0.051 | -0.964 | 0.336 | 359 |
| NG | dist_ma_200 | -0.069 | -1.307 | 0.192 | 362 |
| NG | carry | -0.078 | -1.507 | 0.133 | 371 |
| NG | carry_z | -0.062 | -1.179 | 0.239 | 365 |
| NG | slope_cm | -0.006 | -0.110 | 0.913 | 366 |
| NG | carry_12m | -0.052 | -1.004 | 0.316 | 371 |
| NG | z_ret_5 | 0.012 | 0.239 | 0.811 | 369 |
| NG | trend_template | 0.025 | 0.474 | 0.636 | 371 |
| NG | vcp_contraction | -0.006 | -0.113 | 0.910 | 371 |
| NG | season_score | -0.001 | -0.027 | 0.978 | 359 |
| NG | mm_z | -0.022 | -0.417 | 0.677 | 359 |
| NG | DFII10_chg_63 | -0.082 | -1.583 | 0.114 | 368 |
| NG | DTWEXBGS_chg_63 | -0.112 | -2.152 | 0.032 | 368 |

## Cross-commodity / macro relationships (monthly)
Contemporaneous ≠ predictive: the lagged column is the tradable one.

| relationship | n | contemp_corr | contemp_p | lagged_corr (predictive) | lagged_p | contemp_corr_first_half | contemp_corr_second_half |
|---|---|---|---|---|---|---|---|
| GC vs SI | 371 | -0.059 | 0.259 | -0.013 | 0.801 | -0.132 | 0.021 |
| GC vs HG | 371 | -0.029 | 0.575 | 0.001 | 0.979 | -0.075 | 0.017 |
| HG vs CL | 371 | -0.029 | 0.583 | 0.058 | 0.262 | -0.071 | 0.019 |
| CL vs NG | 371 | 0.034 | 0.513 | -0.016 | 0.760 | 0.006 | 0.057 |
| GC vs dDFII10 | 370 | -0.001 | 0.982 | 0.058 | 0.266 | 0.055 | -0.066 |
| SI vs dDFII10 | 370 | 0.013 | 0.809 | -0.028 | 0.586 | 0.030 | -0.009 |
| GC vs dDTWEXBGS | 370 | 0.071 | 0.173 | -0.040 | 0.447 | -0.026 | 0.179 |
| HG vs dDTWEXBGS | 370 | -0.022 | 0.670 | 0.002 | 0.976 | -0.084 | 0.036 |
| CL vs dDTWEXBGS | 370 | -0.047 | 0.367 | -0.088 | 0.090 | -0.156 | 0.060 |
