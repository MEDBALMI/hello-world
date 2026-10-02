# 06 Commodity Feature Report

> **SYNTHETIC DATA — ENGINEERING VALIDATION ONLY (scenario `NULL`).** No number in this report is evidence about real commodity markets. Real-market data sources are not reachable from the build environment (see 17_COMMODITY_DATA_SOURCES.md).

Spearman IC vs next-21d tradable return, non-overlapping monthly samples.

| root | feature | ic | t | p | n |
|---|---|---|---|---|---|
| GC | ret_63 | 0.078 | 1.506 | 0.133 | 368 |
| GC | ret_252 | 0.065 | 1.238 | 0.216 | 359 |
| GC | tsmom_12_1 | 0.066 | 1.254 | 0.211 | 359 |
| GC | dist_ma_200 | 0.042 | 0.801 | 0.423 | 362 |
| GC | carry | 0.050 | 0.969 | 0.333 | 371 |
| GC | carry_z | 0.066 | 1.252 | 0.212 | 365 |
| GC | slope_cm | 0.050 | 0.946 | 0.345 | 366 |
| GC | carry_12m | -0.027 | -0.528 | 0.598 | 371 |
| GC | z_ret_5 | 0.028 | 0.543 | 0.587 | 369 |
| GC | trend_template | 0.100 | 1.938 | 0.053 | 371 |
| GC | vcp_contraction | 0.074 | 1.425 | 0.155 | 371 |
| GC | season_score | -0.034 | -0.644 | 0.520 | 359 |
| GC | mm_z | -0.030 | -0.567 | 0.571 | 359 |
| GC | DFII10_chg_63 | 0.023 | 0.449 | 0.654 | 368 |
| GC | DTWEXBGS_chg_63 | -0.030 | -0.572 | 0.568 | 368 |
| SI | ret_63 | 0.067 | 1.277 | 0.202 | 368 |
| SI | ret_252 | 0.058 | 1.103 | 0.271 | 359 |
| SI | tsmom_12_1 | 0.059 | 1.110 | 0.268 | 359 |
| SI | dist_ma_200 | 0.074 | 1.414 | 0.158 | 362 |
| SI | carry | 0.027 | 0.520 | 0.603 | 371 |
| SI | carry_z | 0.073 | 1.387 | 0.166 | 365 |
| SI | slope_cm | -0.021 | -0.282 | 0.778 | 190 |
| SI | carry_12m | 0.088 | 1.697 | 0.091 | 371 |
| SI | z_ret_5 | -0.071 | -1.358 | 0.175 | 369 |
| SI | trend_template | -0.045 | -0.874 | 0.383 | 371 |
| SI | vcp_contraction | -0.008 | -0.155 | 0.877 | 371 |
| SI | season_score | -0.063 | -1.201 | 0.231 | 359 |
| SI | mm_z | -0.030 | -0.570 | 0.569 | 359 |
| SI | DFII10_chg_63 | 0.005 | 0.099 | 0.921 | 368 |
| SI | DTWEXBGS_chg_63 | 0.096 | 1.847 | 0.066 | 368 |
| HG | ret_63 | -0.020 | -0.386 | 0.700 | 368 |
| HG | ret_252 | -0.038 | -0.710 | 0.478 | 359 |
| HG | tsmom_12_1 | -0.008 | -0.153 | 0.879 | 359 |
| HG | dist_ma_200 | -0.047 | -0.887 | 0.376 | 362 |
| HG | carry | 0.020 | 0.384 | 0.701 | 371 |
| HG | carry_z | -0.029 | -0.559 | 0.576 | 365 |
| HG | slope_cm | -0.071 | -1.355 | 0.176 | 366 |
| HG | carry_12m | -0.076 | -1.473 | 0.142 | 371 |
| HG | z_ret_5 | 0.059 | 1.136 | 0.257 | 369 |
| HG | trend_template | 0.051 | 0.990 | 0.323 | 371 |
| HG | vcp_contraction | 0.088 | 1.693 | 0.091 | 371 |
| HG | season_score | -0.029 | -0.549 | 0.583 | 359 |
| HG | mm_z | -0.043 | -0.822 | 0.411 | 359 |
| HG | DFII10_chg_63 | 0.022 | 0.420 | 0.675 | 368 |
| HG | DTWEXBGS_chg_63 | 0.116 | 2.244 | 0.025 | 368 |
| CL | ret_63 | -0.020 | -0.379 | 0.705 | 368 |
| CL | ret_252 | -0.085 | -1.604 | 0.110 | 359 |
| CL | tsmom_12_1 | -0.075 | -1.426 | 0.155 | 359 |
| CL | dist_ma_200 | -0.014 | -0.273 | 0.785 | 362 |
| CL | carry | 0.004 | 0.083 | 0.934 | 371 |
| CL | carry_z | -0.030 | -0.566 | 0.571 | 365 |
| CL | slope_cm | 0.098 | 1.874 | 0.062 | 366 |
| CL | carry_12m | 0.076 | 1.472 | 0.142 | 371 |
| CL | z_ret_5 | 0.037 | 0.704 | 0.482 | 369 |
| CL | trend_template | 0.011 | 0.204 | 0.838 | 371 |
| CL | vcp_contraction | -0.051 | -0.989 | 0.323 | 371 |
| CL | season_score | 0.080 | 1.507 | 0.133 | 359 |
| CL | mm_z | -0.007 | -0.128 | 0.898 | 359 |
| CL | DFII10_chg_63 | -0.013 | -0.248 | 0.804 | 368 |
| CL | DTWEXBGS_chg_63 | -0.033 | -0.641 | 0.522 | 368 |
| NG | ret_63 | -0.016 | -0.306 | 0.760 | 368 |
| NG | ret_252 | 0.056 | 1.062 | 0.289 | 359 |
| NG | tsmom_12_1 | 0.078 | 1.484 | 0.139 | 359 |
| NG | dist_ma_200 | -0.036 | -0.691 | 0.490 | 362 |
| NG | carry | 0.039 | 0.757 | 0.449 | 371 |
| NG | carry_z | 0.008 | 0.161 | 0.872 | 365 |
| NG | slope_cm | 0.097 | 1.857 | 0.064 | 366 |
| NG | carry_12m | 0.127 | 2.466 | 0.014 | 371 |
| NG | z_ret_5 | -0.009 | -0.168 | 0.867 | 369 |
| NG | trend_template | -0.016 | -0.314 | 0.754 | 371 |
| NG | vcp_contraction | -0.008 | -0.147 | 0.883 | 371 |
| NG | season_score | 0.108 | 2.062 | 0.040 | 359 |
| NG | mm_z | 0.011 | 0.200 | 0.842 | 359 |
| NG | DFII10_chg_63 | 0.010 | 0.200 | 0.842 | 368 |
| NG | DTWEXBGS_chg_63 | -0.022 | -0.418 | 0.676 | 368 |

## Cross-commodity / macro relationships (monthly)
Contemporaneous ≠ predictive: the lagged column is the tradable one.

| relationship | n | contemp_corr | contemp_p | lagged_corr (predictive) | lagged_p | contemp_corr_first_half | contemp_corr_second_half |
|---|---|---|---|---|---|---|---|
| GC vs SI | 371 | -0.023 | 0.655 | -0.029 | 0.581 | -0.058 | 0.007 |
| GC vs HG | 371 | -0.048 | 0.360 | -0.054 | 0.298 | 0.005 | -0.092 |
| HG vs CL | 371 | -0.098 | 0.059 | 0.002 | 0.965 | -0.063 | -0.123 |
| CL vs NG | 371 | -0.104 | 0.045 | 0.006 | 0.914 | -0.055 | -0.138 |
| GC vs dDFII10 | 370 | 0.056 | 0.281 | 0.060 | 0.247 | 0.056 | 0.059 |
| SI vs dDFII10 | 370 | 0.066 | 0.205 | -0.024 | 0.649 | 0.054 | 0.080 |
| GC vs dDTWEXBGS | 370 | 0.044 | 0.399 | -0.023 | 0.665 | 0.062 | 0.029 |
| HG vs dDTWEXBGS | 370 | 0.003 | 0.961 | 0.105 | 0.043 | 0.020 | -0.019 |
| CL vs dDTWEXBGS | 370 | 0.134 | 0.010 | -0.036 | 0.488 | 0.143 | 0.130 |
