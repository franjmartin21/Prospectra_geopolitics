# Databricks Build Spec: Automated Geopolitical Regime Classifier
**Spec Date:** June 2, 2026
**Assigned by:** CEO — Prospectra Geopolitics & Investment Project
**Priority:** P0 — This is the Phase 2→3 bridge. Build this week.
**Reference lesson:** Lesson 90 — The Geopolitical Investment Clock
**Deadline:** June 9, 2026 (committed and pushed to repo)

---

## What This Builds

A weekly pipeline that classifies the current investment regime using two axes:
1. **Economic Regime** — which quadrant of the Investment Clock (Reflation / Recovery / Overheat / Stagflation)
2. **Geopolitical Fragmentation Score (GFS)** — Low / Medium / High

Output: a 2D regime classification updated weekly, with a confidence score and an alert when the regime probability shifts by >20%.

This is not a toy. It is the analytical backbone for every asset allocation decision in the portfolio. Every position in the investment log was opened under an assumed regime. This pipeline makes that assumption explicit, measurable, and automated.

---

## Architecture

### Layer 1 — Bronze (raw ingestion)

**Source 1: GDELT GKG (Global Knowledge Graph)**
- URL: `http://data.gdeltproject.org/gkg/YYYYMMDD.gkg.csv.zip`
- Frequency: daily
- Fields needed: `DATE`, `THEMES`, `TONE`, `LOCATIONS`, `NUMARTS`
- Filter: articles mentioning geopolitical themes: `WAR`, `SANCTION`, `CONFLICT`, `MILITARY`, `TRADE_DISPUTE`, `ENERGY_SECURITY`, `NUCLEAR`
- Output table: `bronze.gdelt_gkg_daily`

**Source 2: FRED (Federal Reserve Economic Data)**
- API: `https://fred.stlouisfed.org/docs/api/fred/`
- Series needed:
  - `T10Y2Y` — 10-year minus 2-year Treasury spread (yield curve)
  - `BAMLH0A0HYM2` — US High-Yield OAS (credit spread)
  - `NAPM` — ISM Manufacturing PMI
  - `CPIAUCSL` — CPI YoY (use `units=pc1`)
  - `UNRATE` — Unemployment rate
- Frequency: monthly (PMI, CPI, unemployment); daily (yield curve, credit spreads)
- Output table: `bronze.fred_macro_daily`

**Source 3: Yahoo Finance (via yfinance)**
- Tickers:
  - `GC=F` — Gold futures
  - `CL=F` — Crude oil futures
  - `DX-Y.NYB` — US Dollar Index
  - `^TNX` — 10-year Treasury yield
  - `^VIX` — VIX
  - `EEM` — iShares MSCI EM ETF
  - `SPY` — S&P 500
- Frequency: daily
- Output table: `bronze.market_prices_daily`

---

### Layer 2 — Silver (feature engineering)

**Economic regime features:**
```python
# yield_curve_signal: +1 (steepening/positive), 0 (flat), -1 (inverted)
yield_curve_signal = sign(T10Y2Y - T10Y2Y.rolling(4w).mean())

# pmi_signal: +1 (>52 and rising), 0 (48-52), -1 (<48 or falling)
pmi_signal = classify_pmi(NAPM, NAPM.diff())

# credit_spread_signal: +1 (tightening), 0 (stable), -1 (widening)
credit_spread_signal = -sign(BAMLH0A0HYM2.rolling(4w).diff())

# inflation_signal: +1 (rising above 3%), 0 (stable 1-3%), -1 (falling below 1%)
inflation_signal = classify_inflation(CPI_YOY)

# economic_regime_score: continuous -4 to +4
economic_regime_score = yield_curve_signal + pmi_signal + credit_spread_signal + inflation_signal

# economic_regime_quadrant: categorical
# score > 1: Recovery (rising growth, controlled inflation)
# score 0-1 + inflation_signal > 0: Overheat
# score < -1 + inflation_signal > 0: Stagflation
# score < -1 + inflation_signal <= 0: Reflation
economic_regime_quadrant = classify_quadrant(economic_regime_score, inflation_signal)
```

**Geopolitical fragmentation features:**
```python
# gdelt_tone_score: rolling 4-week average of GDELT global tone (negative = more conflict)
gdelt_tone_weekly = gdelt_gkg.groupby('week')['TONE'].mean()

# gdelt_conflict_intensity: normalized count of conflict/war/sanction theme articles
gdelt_conflict_weekly = gdelt_gkg[themes contains WAR|SANCTION|MILITARY].groupby('week')['NUMARTS'].sum()

# vix_signal: normalized (VIX - 20) / 10, clipped to [-2, +2]
vix_signal = clip((VIX - 20) / 10, -2, 2)

# em_dm_spread: EEM 30-day return minus SPY 30-day return (negative = fragmentation stress on EM)
em_dm_spread = EEM.pct_change(30) - SPY.pct_change(30)

# geopolitical_frag_score: composite 0–10
geopolitical_frag_score = normalize(
    -gdelt_tone_weekly * 0.4 +
    gdelt_conflict_weekly * 0.3 +
    vix_signal * 0.15 +
    -em_dm_spread * 0.15
)

# frag_level: Low (<3.5), Medium (3.5-6.5), High (>6.5)
frag_level = classify_frag(geopolitical_frag_score)
```

Output table: `silver.regime_features_weekly`

---

### Layer 3 — Gold (regime classification + alerts)

**Output schema:**
```
week_ending          DATE
economic_regime      STRING  -- Reflation/Recovery/Overheat/Stagflation
econ_confidence      FLOAT   -- 0-1, derived from score distance from threshold
frag_level           STRING  -- Low/Medium/High
frag_score           FLOAT   -- 0-10
regime_cell          STRING  -- e.g., "Overheat_High" (8 possible values)
prior_regime_cell    STRING  -- previous week
regime_changed       BOOLEAN
alert_message        STRING  -- populated when regime probability shift > 20%
```

**Alert logic:**
- If `regime_cell != prior_regime_cell`: alert = `"REGIME TRANSITION: {prior} → {current}. Review portfolio positioning."`
- If `econ_confidence < 0.3` (near threshold): alert = `"REGIME UNCERTAIN: {economic_regime} confidence low. Increase monitoring frequency."`

Output table: `gold.regime_classification_weekly`

---

## Portfolio Integration Table

Populate this table each week from the regime classification:

| Regime Cell | Overweight | Underweight | Notes |
|---|---|---|---|
| Overheat_High | Energy, Critical Minerals, Defense, Gold | Long-duration bonds, EM importers | Current regime |
| Overheat_Low | Diversified commodities, real assets | Cash | Integrated world version |
| Recovery_High | Defense, domestic champions, friend-shore EM | Global integration plays | |
| Recovery_Low | Global equities, EM carry | Commodities | |
| Stagflation_High | Gold, commodity producers, defense | Equities broadly | Worst regime |
| Stagflation_Low | Gold, cash | Bonds, equities | |
| Reflation_High | Gold, short EM (fragmentation exposed) | Duration bonds | |
| Reflation_Low | Duration bonds, EM growth | Commodities | |

---

## Notebook Structure

```
databricks/src/regime_classifier/
├── extract/
│   ├── gdelt_gkg_extract.py      # Download and parse GDELT GKG
│   ├── fred_extract.py           # FRED API pull
│   └── yfinance_extract.py       # Market price pull
├── pipeline/
│   ├── bronze.py                 # Raw ingestion, schema validation
│   ├── silver.py                 # Feature engineering
│   └── gold.py                  # Regime classification, alerts
├── dashboard/
│   └── regime_matrix.py          # Optional: Databricks AI/BI output
databricks/resources/regime_classifier/
├── job.yml                       # Weekly scheduled job
databricks/specs/
└── 2026-06-02_regime_classifier_pipeline.md  # This file
```

---

## Minimum Viable Build (Week 1)

Don't try to build everything at once. Ship in this order:

**Day 1–2:** Bronze layer. Get GDELT, FRED, and yfinance data flowing. Prove the data lands correctly in Delta tables.

**Day 3:** Silver layer. Calculate the 8 features. Verify they move in expected directions during known historical events (e.g., March 2020 = Stagflation/High; Q4 2021 = Recovery/Low; Q2 2022 = Stagflation/High).

**Day 4:** Gold layer. Regime classification + alert logic. Output a 12-week backfill of weekly regime readings back to April 2026 (project start).

**Day 5:** Commit, push, message the CEO. One paragraph: what's working, what's weird, what's next.

---

## Validation Test

The pipeline is working correctly if it classifies these reference periods correctly:

| Period | Expected Economic Regime | Expected Frag Level | Reason |
|---|---|---|---|
| Q1 2020 (COVID onset) | Stagflation→Reflation | High | PMI collapse, VIX spike, EM selloff |
| Q3 2021 | Recovery/Overheat | Low | Strong PMI, tight credit, inflation building |
| Q2 2022 (Ukraine + rate hikes) | Stagflation | High | CPI spike + PMI fall + geopolitical conflict surge |
| Q1 2024 | Recovery | Medium | Soft landing, PMI recovery, geopolitics active but stable |
| Q2 2026 (current) | Overheat/Recovery | High | Sticky inflation, positive growth, Iran + NATO dynamics |

If the classification on any of these is wrong, debug before moving to the Gold layer.

---

## What This Enables (When Built)

1. **Automated portfolio positioning check:** Every Monday, the regime output tells us whether our current positioning is aligned with the current regime. If we're positioned for Overheat but the regime is shifting to Stagflation, we get an alert before the market moves.

2. **Investment log validation:** Cross-reference every open position with the regime it was opened in. Identify positions that relied on regime assumptions that are no longer valid.

3. **The eventual product:** This regime classifier is the core intelligence layer of the Prospectra platform. Everything else — sector signals, country risk scores, FX pressure indicators — sits on top of this classification.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Spec issued June 2, 2026. Build deadline: June 9, 2026.*
