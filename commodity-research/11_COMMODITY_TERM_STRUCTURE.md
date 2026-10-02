# 11 — Commodity Term Structure (Phase 14 foundations)

> Status: **v0.1 — construction and feature definitions only.** No empirical results. Concepts → 01#21–30; series methods → 02 §B.4; storage/availability → 03.
> Purpose: define *exactly* how term-structure variables will be built, so later hypothesis tests (15) are reproducible and free of look-ahead.

## 1. What the curve can tell us (theory recap)
Theory of storage (01#22–25): low inventory → high convenience yield → backwardation → higher spot volatility. Hedging pressure (01#47) gives a risk-premium reading of the same curve.

So the curve is a daily, market-implied fundamental. Whether it **predicts** returns in our markets is open [OPEN-1.3]. Published evidence is mostly cross-sectional across broad universes [EMPIRICAL: Koijen et al. 2018; Szymanowska et al. 2014; Gorton, Hayashi & Rouwenhorst 2013].

## 2. Curve inputs per root (liquid months) [VERIFY when ingesting]
| Root | Listed | Liquid months (typical) | Curve depth usable | Notes |
|---|---|---|---|---|
| CME GC (gold) | many | Feb, Apr, Jun, Aug, Oct, Dec | ~2–4 liquid points | Curve ≈ financing − lease rate; carry mostly mechanical |
| CME SI (silver) | many | Mar, May, Jul, Sep, Dec | ~2–3 | Similar to gold; lease-rate spikes matter |
| CME PL / PA | quarterly-ish | PL: Jan, Apr, Jul, Oct; PA: Mar, Jun, Sep, Dec | 1–2 | Thin curves |
| CME HG (copper) | monthly | Mar, May, Jul, Sep, Dec (most active) | ~3–6 | Compare with LME cash–3M |
| CME CL (WTI) | monthly, years out | Every month | 12+ | Richest curve |
| CME NG | monthly, years out | Every month | 12+ | **Strong seasonal shape** (winter premium) |
| LME metals | daily prompts to 3M, then weekly/monthly [V-S] | Cash, 3M, 15M, 27M | Cash–3M key | Different structure: rolling prompt dates, not fixed months |
| MCX roots | usually 2–6 months listed | Near month dominant | 1–2 | Curve features mostly taken from global benchmarks |

## 3. Feature definitions
All features are computed from **settlements of date t** and become available at `settle_available_ts(t)` (03 §6). Sign convention: **positive = backwardation**.

| ID | Feature | Formula | Notes |
|---|---|---|---|
| TS1 | Nearby carry (annualised) | ln(F1/F2) × 365 / (T2 − T1) | F1, F2 = first two **eligible liquid** contracts (not in delivery window) |
| TS2 | CM slope | ln(CM_30 / CM_365) × 365/335 | From `derived.cm_curve_point`; requires a 365-day point without extrapolation |
| TS3 | CM curvature | ln CM_30 − 2 ln CM_180 + ln CM_365 | Deep curves only (CL, NG, LME) |
| TS4 | Slope change | TS1_t − TS1_{t−k}, k = 5, 20, 60 | Steepening/flattening |
| TS5 | Backwardation regime | 1[TS1 > 0]; rolling % of days in backwardation (60, 250 days) | Inversion = sign change |
| TS6 | Carry z-score | (TS1 − mean_250) / sd_250 | Rolling window, past data only |
| TS7 | Implied convenience yield | r_t + u − carry_t, with u = assumed storage cost | Sensitive to u assumption; report sensitivity |
| TS8 | Excess carry over financing | TS1 + r_t | Removes the mechanical rate component (key for gold/silver) |
| TS9 | Seasonal-neutral carry | ln(F_m,y / F_m,y+1): same calendar month, 12 months apart | For NG (and gasoline-linked crude seasonality) |
| TS10 | LME cash–3M spread | (Cash − 3M) / 3M, annualised | Base-metal tightness; compare with HG TS1 |
| TS11 | Curve PCA factors | Level/slope/curvature from rolling PCA on CM log-prices | Fit on past window only; sign-normalise loadings |
| TS12 | Realised roll return | r_futures − r_spot (02 §B.2) | Ex-post; for attribution, **not** a signal |

Rules:
- Use only contracts passing the liquidity filter (03 §5.4) on t−1 data. Settle-only points are flagged and down-weighted or excluded.
- **No extrapolation** beyond the deepest liquid contract. If a feature cannot be computed, it is NULL, never filled.
- Rolling statistics use strictly past data (window ends at t).

## 4. Seasonality in curves
- NG (and to a lesser degree crude products) have **predictable seasonal curve shapes**. A raw F1/F2 slope mixes seasonality with tightness: a November→December spread is "contango" every year.
- Remedies: (a) TS9 same-month 12-month spreads, (b) deseasonalise TS1 by subtracting its historical same-calendar-month mean (estimated on past data only), (c) build CM points with seasonal adjustment [OPEN-11.1: choose method].

## 5. Constant-maturity construction (method CM-1)
1. For target tenor τ, find eligible contracts with days-to-expiry bracketing τ.
2. Interpolate **log price linearly in days to expiry**. Use LTD (or `delivery_risk_date` for physical) as the maturity reference — be consistent.
3. If τ < shortest eligible maturity → use the shortest contract and flag it (no extrapolation in price, maturity mismatch recorded). If τ > longest eligible → NULL.
4. Store contract IDs, weights and flags (`derived.cm_curve_point`).

## 6. Data sufficiency per feature
| Feature family | Minimum data |
|---|---|
| TS1, TS4–TS6, TS8 | Two nearest liquid contracts daily (+ rates for TS8) |
| TS2, TS3, TS11 | Full liquid curve to ≥ 12 months (CL, NG, LME; limited for metals on CME) |
| TS7 | Curve + rates + storage-cost assumption |
| TS9 | ≥ 13 months of listed contracts |
| TS10 | LME cash and 3M (licensed) |

## 7. Candidate hypotheses (to formalise in 15; **not tested**)
- H-TS1: Time-series carry (TS1/TS8) predicts next-month excess returns per market.
- H-TS2: Changes in slope (TS4) carry information beyond the slope level.
- H-TS3: Curve regime (TS5) changes the behaviour of trend signals.
- H-TS4: Seasonally adjusted NG carry outperforms raw carry as a predictor.
- H-TS5: LME cash–3M (TS10) leads CME copper curve and price changes.

## 8. Open questions
- [OPEN-11.1] Best seasonal-adjustment method for NG curve features.
- [OPEN-11.2] Storage-cost assumptions per commodity for TS7.
- [OPEN-11.3] Whether metals curves on CME are deep enough for TS2/TS3, or whether LME is required.
