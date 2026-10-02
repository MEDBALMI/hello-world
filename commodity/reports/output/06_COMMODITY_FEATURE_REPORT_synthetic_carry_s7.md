# 06 Commodity Feature Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `CARRY`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

Spearman IC vs next-21d tradable return, non-overlapping monthly samples.

| root | feature | ic | t | p | n |
|---|---|---|---|---|---|
| GC | ret_63 | 0.008 | 0.149 | 0.882 | 368 |
| GC | ret_252 | -0.021 | -0.392 | 0.695 | 359 |
| GC | tsmom_12_1 | -0.009 | -0.174 | 0.862 | 359 |
| GC | dist_ma_200 | -0.021 | -0.406 | 0.685 | 362 |
| GC | carry | -0.011 | -0.219 | 0.827 | 371 |
| GC | carry_z | -0.005 | -0.094 | 0.925 | 365 |
| GC | slope_cm | -0.066 | -1.269 | 0.205 | 366 |
| GC | carry_12m | 0.021 | 0.398 | 0.691 | 371 |
| GC | z_ret_5 | 0.137 | 2.650 | 0.008 | 369 |
| GC | trend_template | -0.028 | -0.542 | 0.588 | 371 |
| GC | vcp_contraction | 0.058 | 1.111 | 0.267 | 371 |
| GC | season_score | -0.119 | -2.257 | 0.025 | 359 |
| GC | mm_z | -0.029 | -0.554 | 0.580 | 359 |
| GC | DFII10_chg_63 | 0.057 | 1.099 | 0.273 | 368 |
| GC | DTWEXBGS_chg_63 | 0.027 | 0.511 | 0.609 | 368 |
| SI | ret_63 | -0.008 | -0.151 | 0.880 | 368 |
| SI | ret_252 | 0.041 | 0.768 | 0.443 | 359 |
| SI | tsmom_12_1 | 0.030 | 0.561 | 0.575 | 359 |
| SI | dist_ma_200 | 0.036 | 0.689 | 0.491 | 362 |
| SI | carry | -0.010 | -0.189 | 0.850 | 371 |
| SI | carry_z | 0.040 | 0.762 | 0.447 | 365 |
| SI | slope_cm | -0.171 | -2.376 | 0.019 | 190 |
| SI | carry_12m | -0.064 | -1.233 | 0.218 | 371 |
| SI | z_ret_5 | 0.058 | 1.110 | 0.268 | 369 |
| SI | trend_template | -0.085 | -1.641 | 0.102 | 371 |
| SI | vcp_contraction | -0.096 | -1.845 | 0.066 | 371 |
| SI | season_score | 0.014 | 0.264 | 0.792 | 359 |
| SI | mm_z | -0.077 | -1.459 | 0.145 | 359 |
| SI | DFII10_chg_63 | -0.004 | -0.083 | 0.934 | 368 |
| SI | DTWEXBGS_chg_63 | -0.048 | -0.917 | 0.360 | 368 |
| HG | ret_63 | 0.007 | 0.142 | 0.887 | 368 |
| HG | ret_252 | 0.021 | 0.401 | 0.689 | 359 |
| HG | tsmom_12_1 | 0.007 | 0.135 | 0.893 | 359 |
| HG | dist_ma_200 | 0.018 | 0.342 | 0.732 | 362 |
| HG | carry | 0.019 | 0.372 | 0.710 | 371 |
| HG | carry_z | -0.035 | -0.676 | 0.500 | 365 |
| HG | slope_cm | 0.055 | 1.049 | 0.295 | 366 |
| HG | carry_12m | 0.088 | 1.700 | 0.090 | 371 |
| HG | z_ret_5 | -0.030 | -0.570 | 0.569 | 369 |
| HG | trend_template | 0.046 | 0.879 | 0.380 | 371 |
| HG | vcp_contraction | 0.061 | 1.166 | 0.244 | 371 |
| HG | season_score | -0.103 | -1.950 | 0.052 | 359 |
| HG | mm_z | -0.022 | -0.417 | 0.677 | 359 |
| HG | DFII10_chg_63 | 0.075 | 1.446 | 0.149 | 368 |
| HG | DTWEXBGS_chg_63 | -0.000 | -0.002 | 0.998 | 368 |
| CL | ret_63 | 0.098 | 1.889 | 0.060 | 368 |
| CL | ret_252 | 0.102 | 1.931 | 0.054 | 359 |
| CL | tsmom_12_1 | 0.100 | 1.890 | 0.060 | 359 |
| CL | dist_ma_200 | 0.061 | 1.166 | 0.245 | 362 |
| CL | carry | -0.082 | -1.576 | 0.116 | 371 |
| CL | carry_z | -0.096 | -1.839 | 0.067 | 365 |
| CL | slope_cm | 0.087 | 1.664 | 0.097 | 366 |
| CL | carry_12m | 0.108 | 2.088 | 0.037 | 371 |
| CL | z_ret_5 | -0.009 | -0.164 | 0.870 | 369 |
| CL | trend_template | 0.091 | 1.754 | 0.080 | 371 |
| CL | vcp_contraction | 0.037 | 0.704 | 0.482 | 371 |
| CL | season_score | 0.024 | 0.461 | 0.645 | 359 |
| CL | mm_z | 0.051 | 0.966 | 0.335 | 359 |
| CL | DFII10_chg_63 | 0.018 | 0.350 | 0.726 | 368 |
| CL | DTWEXBGS_chg_63 | -0.098 | -1.881 | 0.061 | 368 |
| NG | ret_63 | 0.016 | 0.310 | 0.757 | 368 |
| NG | ret_252 | -0.046 | -0.866 | 0.387 | 359 |
| NG | tsmom_12_1 | -0.044 | -0.838 | 0.403 | 359 |
| NG | dist_ma_200 | -0.082 | -1.556 | 0.121 | 362 |
| NG | carry | -0.059 | -1.132 | 0.258 | 371 |
| NG | carry_z | -0.057 | -1.096 | 0.274 | 365 |
| NG | slope_cm | 0.032 | 0.607 | 0.544 | 366 |
| NG | carry_12m | 0.026 | 0.504 | 0.615 | 371 |
| NG | z_ret_5 | -0.001 | -0.011 | 0.991 | 369 |
| NG | trend_template | 0.027 | 0.525 | 0.600 | 371 |
| NG | vcp_contraction | 0.020 | 0.393 | 0.694 | 371 |
| NG | season_score | 0.004 | 0.071 | 0.943 | 359 |
| NG | mm_z | -0.048 | -0.915 | 0.361 | 359 |
| NG | DFII10_chg_63 | -0.096 | -1.850 | 0.065 | 368 |
| NG | DTWEXBGS_chg_63 | -0.101 | -1.943 | 0.053 | 368 |

## Cross-commodity / macro relationships (monthly)
Contemporaneous ≠ predictive: the lagged column is the tradable one.

| relationship | n | contemp_corr | contemp_p | lagged_corr (predictive) | lagged_p | contemp_corr_first_half | contemp_corr_second_half |
|---|---|---|---|---|---|---|---|
| GC vs SI | 371 | -0.052 | 0.314 | -0.005 | 0.920 | -0.133 | 0.033 |
| GC vs HG | 371 | -0.036 | 0.484 | -0.002 | 0.969 | -0.073 | -0.001 |
| HG vs CL | 371 | -0.050 | 0.340 | 0.035 | 0.507 | -0.086 | 0.001 |
| CL vs NG | 371 | 0.025 | 0.627 | -0.018 | 0.731 | -0.003 | 0.064 |
| GC vs dDFII10 | 370 | 0.005 | 0.931 | 0.063 | 0.228 | 0.057 | -0.057 |
| SI vs dDFII10 | 370 | 0.009 | 0.863 | -0.030 | 0.562 | 0.026 | -0.013 |
| GC vs dDTWEXBGS | 370 | 0.075 | 0.151 | -0.036 | 0.488 | -0.025 | 0.185 |
| HG vs dDTWEXBGS | 370 | -0.023 | 0.661 | -0.001 | 0.990 | -0.086 | 0.039 |
| CL vs dDTWEXBGS | 370 | -0.040 | 0.441 | -0.079 | 0.127 | -0.164 | 0.084 |
