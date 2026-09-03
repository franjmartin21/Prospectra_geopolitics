# Lesson 296 — Market Data Pipeline: Building the Asset Returns Layer for GRI Validation

**Date:** 2026-09-03
**Session Type:** Daily Lesson
**Lesson Number:** 296 / ongoing
**Topic:** Databricks Build Module — The Market Data Pipeline: yfinance → Bronze → Silver → Gold validation layer
**Curriculum Arc:** Databricks Build Module — Lesson 8 (the last missing layer: connecting geopolitical signal to tradeable asset returns)

---

## Opening Question

*You have the GRI. You have the formula. You have the validation methodology.*

**But you cannot run a single backtest yet.**

The entire validation architecture from Lessons 294 and 295 — the event study, the factor quintile spread, the commodity theme signal — requires one thing that the Databricks platform does not yet have: **daily asset return data joined to country identifiers.**

Without it, your GRI is a geopolitical score floating in a vacuum. With it, the GRI becomes testable. The question it must answer: does elevated geopolitical risk, measured *before* the fact, predict adverse moves in the financial assets most directly exposed to that risk?

Today you build the bridge. The market data pipeline is the final structural piece before validation can begin.

---

## I. What You're Building — The Architecture

The market data layer sits parallel to the GRI in the Gold layer. It is not downstream of the GRI — it is an independent data stream that joins to the GRI at validation time.

```
GDELT Pipeline                    Market Data Pipeline
───────────────                   ────────────────────
Bronze (raw events)               Bronze (yfinance raw OHLCV)
    ↓                                 ↓
Silver (aggregations)             Silver (returns, z-scored)
    ↓                                 ↓
Gold (GRI score)          ←JOIN→  Gold (country_asset_daily_returns)
    ↓
Validation Layer
    ├── event_study_results
    ├── factor_quintile_returns
    └── commodity_theme_signal
```

The join key is `(country_iso3, event_date)`. The `country_asset_mapping` table is the lookup that connects FIPS/ISO country codes from GDELT to the yfinance ticker symbols for equity ETFs, FX pairs, and commodity futures.

**Why build it this way:**
- Separation of concerns: geopolitical signal and market data are independent. If yfinance data quality degrades, it does not corrupt the GRI. If GDELT coverage changes, it does not affect market return calculations.
- Reusability: the market data pipeline will be used for validation today, for live signal generation tomorrow, and for portfolio performance attribution in Phase 3.
- Auditability: you can query market returns independently of GRI scores, essential for honest backtesting.

---

## II. The Country-to-Asset Mapping Table

This is the most important manual step in the entire build. Everything downstream depends on getting this right.

The table lives at: `geopolitics.gold.country_asset_mapping`

### Build the Schema First

```sql
-- Run in Databricks SQL or a notebook cell
CREATE TABLE IF NOT EXISTS geopolitics.gold.country_asset_mapping (
  country_iso3       STRING     NOT NULL,
  country_name       STRING,
  asset_id           STRING     NOT NULL,   -- yfinance ticker symbol
  asset_type         STRING     NOT NULL,   -- 'equity_etf', 'fx', 'commodity', 'cds_proxy'
  primary_signal     BOOLEAN    DEFAULT TRUE,
  data_source        STRING     DEFAULT 'yfinance',
  fx_pair_base       STRING,                -- e.g. 'USD' for USDBRL
  notes              STRING,
  added_date         DATE
)
USING DELTA
COMMENT 'Maps GDELT country ISO3 codes to tradeable instruments for GRI validation'
;
```

### Populate the Top 15 Countries by GDELT Volume

Insert this as a batch — these are the countries that appear most frequently in GDELT event data and therefore generate the most GRI signal:

```python
# Databricks notebook cell
from pyspark.sql import SparkSession
from datetime import date

spark = SparkSession.builder.getOrCreate()

mappings = [
    # (country_iso3, country_name, asset_id, asset_type, primary_signal, fx_pair_base, notes)
    # ---- United States ----
    ("USA", "United States", "SPY",     "equity_etf", True,  None,  "S&P 500 ETF — US as geopolitical actor"),
    ("USA", "United States", "UUP",     "fx",         False, "USD", "USD Bullish ETF — safe haven proxy"),
    # ---- Russia ----
    ("RUS", "Russia",        "RSXJ",    "equity_etf", True,  None,  "VanEck Russia Small-Cap (RSX delisted 2022; use RSXJ or proxy)"),
    ("RUS", "Russia",        "TTF=F",   "commodity",  True,  None,  "TTF gas futures — primary Russian energy exposure"),
    ("RUS", "Russia",        "BZ=F",    "commodity",  False, None,  "Brent crude — secondary Russian energy exposure"),
    # ---- China ----
    ("CHN", "China",         "FXI",     "equity_etf", True,  None,  "iShares China Large-Cap ETF"),
    ("CHN", "China",         "MCHI",    "equity_etf", False, None,  "iShares MSCI China ETF — broader coverage"),
    ("CHN", "China",         "CNH=X",   "fx",         True,  "USD", "USD/CNH offshore renminbi"),
    ("CHN", "China",         "HG=F",    "commodity",  True,  None,  "Copper futures — China demand proxy"),
    # ---- Iran ----
    ("IRN", "Iran",          "BZ=F",    "commodity",  True,  None,  "Brent — primary Iran geopolitical exposure; no direct equity instrument"),
    # ---- Saudi Arabia ----
    ("SAU", "Saudi Arabia",  "KSA",     "equity_etf", True,  None,  "iShares MSCI Saudi Arabia ETF"),
    ("SAU", "Saudi Arabia",  "BZ=F",    "commodity",  True,  None,  "Brent crude — Saudi supply exposure"),
    # ---- Israel ----
    ("ISR", "Israel",        "EIS",     "equity_etf", True,  None,  "iShares MSCI Israel ETF"),
    ("ISR", "Israel",        "ILS=X",   "fx",         True,  "USD", "USD/ILS — shekel FX"),
    # ---- Ukraine ----
    ("UKR", "Ukraine",       "ZW=F",    "commodity",  True,  None,  "Wheat futures — Ukraine is largest wheat exporter"),
    ("UKR", "Ukraine",       "ZC=F",    "commodity",  False, None,  "Corn futures — secondary Ukraine agricultural exposure"),
    # ---- Turkey ----
    ("TUR", "Turkey",        "TUR",     "equity_etf", True,  None,  "iShares MSCI Turkey ETF"),
    ("TUR", "Turkey",        "TRY=X",   "fx",         True,  "USD", "USD/TRY — lira, one of most GRI-sensitive EM FX pairs"),
    # ---- Brazil ----
    ("BRA", "Brazil",        "EWZ",     "equity_etf", True,  None,  "iShares MSCI Brazil ETF"),
    ("BRA", "Brazil",        "BRL=X",   "fx",         True,  "USD", "USD/BRL — real, highly reactive to political risk"),
    # ---- India ----
    ("IND", "India",         "INDA",    "equity_etf", True,  None,  "iShares MSCI India ETF"),
    ("IND", "India",         "INR=X",   "fx",         True,  "USD", "USD/INR"),
    # ---- Pakistan ----
    ("PAK", "Pakistan",      "PAK",     "equity_etf", True,  None,  "Global X MSCI Pakistan ETF"),
    ("PAK", "Pakistan",      "PKR=X",   "fx",         False, "USD", "USD/PKR — limited liquidity data"),
    # ---- Mexico ----
    ("MEX", "Mexico",        "EWW",     "equity_etf", True,  None,  "iShares MSCI Mexico ETF"),
    ("MEX", "Mexico",        "MXN=X",   "fx",         True,  "USD", "USD/MXN — peso, near-shoring sensitive"),
    # ---- South Africa ----
    ("ZAF", "South Africa",  "EZA",     "equity_etf", True,  None,  "iShares MSCI South Africa ETF"),
    ("ZAF", "South Africa",  "ZAR=X",   "fx",         True,  "USD", "USD/ZAR — rand, commodity-currency with political risk overlay"),
    # ---- Nigeria ----
    ("NGA", "Nigeria",       "NGE",     "equity_etf", True,  None,  "Global X MSCI Nigeria ETF"),
    ("NGA", "Nigeria",       "NGN=X",   "fx",         False, "USD", "USD/NGN — naira, limited yfinance coverage"),
    # ---- Global commodities (not country-specific) ----
    ("_GBL", "Global",       "GLD",     "commodity",  True,  None,  "SPDR Gold ETF — safe haven; responds to any CRISIS-regime GRI"),
    ("_GBL", "Global",       "GC=F",    "commodity",  False, None,  "Gold futures — alternative to GLD"),
    ("_GBL", "Global",       "^VIX",    "commodity",  True,  None,  "VIX — control variable for global risk-on/off"),
    ("_GBL", "Global",       "DX=F",    "fx",         True,  "USD", "DXY Dollar Index futures — dollar safe haven signal"),
]

from pyspark.sql.types import (
    StructType, StructField, StringType, BooleanType, DateType
)

schema = StructType([
    StructField("country_iso3",   StringType(),  False),
    StructField("country_name",   StringType(),  True),
    StructField("asset_id",       StringType(),  False),
    StructField("asset_type",     StringType(),  False),
    StructField("primary_signal", BooleanType(), True),
    StructField("fx_pair_base",   StringType(),  True),
    StructField("notes",          StringType(),  True),
])

data = [(m[0], m[1], m[2], m[3], m[4], m[5], m[6]) for m in mappings]

df = spark.createDataFrame(data, schema=schema) \
          .withColumn("data_source", F.lit("yfinance")) \
          .withColumn("added_date",  F.lit(date.today().isoformat()))

(df.write
   .format("delta")
   .mode("overwrite")
   .option("overwriteSchema", "true")
   .saveAsTable("geopolitics.gold.country_asset_mapping"))

print(f"Mapping table written: {df.count()} rows")
```

**Notes on specific tickers:**
- RSX (VanEck Russia ETF) was delisted in 2022 following sanctions. Use RSXJ for pre-2022 historical data; after 2022, use Brent crude (BZ=F) as the primary Russia instrument. Your validation code should handle this gracefully.
- For countries without liquid ETFs (Nigeria, Pakistan), FX pairs are the primary instrument but yfinance FX coverage is inconsistent. Flag these as `primary_signal = FALSE` until you verify data quality.
- TTF gas futures (`TTF=F`) are not on yfinance; use ICE data or proxy via the United States Natural Gas Fund (`UNG`) for US validation, European Natural Gas ETF (`GASL`) for European exposure. Note this limitation in the mapping table.

---

## III. The yfinance Bronze Pipeline

Install yfinance in your Databricks cluster libraries first:
```
PyPI package: yfinance==0.2.40
```
(Pin the version — yfinance API changes frequently; version drift has broken many production notebooks.)

### The Bronze Notebook: `gdelt_market_bronze`

```python
# /Workflows/market_data/market_data_bronze.py
# Pulls daily OHLCV data from yfinance for all tickers in country_asset_mapping
# Writes to: geopolitics.bronze.market_data_raw
# Schedule: daily @ 06:30 UTC (after US close, before GDELT Gold runs)

import yfinance as yf
import pandas as pd
from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import (
    StructType, StructField, StringType, FloatType, LongType, DateType, TimestampType
)
from datetime import datetime, timedelta

spark = SparkSession.builder.getOrCreate()

# ============================================================
# STEP 1: Get the list of tickers to fetch
# ============================================================

tickers_df = spark.read.table("geopolitics.gold.country_asset_mapping") \
                  .select("asset_id", "country_iso3", "asset_type") \
                  .distinct()

ticker_list = [row["asset_id"] for row in tickers_df.collect()]
print(f"Fetching {len(ticker_list)} tickers: {ticker_list}")

# ============================================================
# STEP 2: Determine date range
# ============================================================

# Check the max date already in the Bronze table
try:
    existing_max = spark.read.table("geopolitics.bronze.market_data_raw") \
                             .agg(F.max("price_date")).collect()[0][0]
    start_date = (existing_max + timedelta(days=1)).strftime("%Y-%m-%d") if existing_max else "2019-01-01"
except Exception:
    start_date = "2019-01-01"  # Full history load on first run

end_date = datetime.now().strftime("%Y-%m-%d")

print(f"Fetching data from {start_date} to {end_date}")

if start_date >= end_date:
    print("No new data needed — Bronze is current.")
    dbutils.notebook.exit("UP_TO_DATE")

# ============================================================
# STEP 3: Fetch via yfinance (batch download)
# ============================================================

raw = yf.download(
    tickers=ticker_list,
    start=start_date,
    end=end_date,
    group_by="ticker",
    auto_adjust=True,       # adjusts for splits and dividends
    progress=False,
    threads=True,
)

# yfinance returns a MultiIndex DataFrame when multiple tickers are fetched
# Reshape to long format: (date, ticker, open, high, low, close, volume)

records = []
fetch_ts = datetime.utcnow()

for ticker in ticker_list:
    try:
        if len(ticker_list) > 1:
            df_t = raw[ticker].dropna(how="all")
        else:
            df_t = raw.dropna(how="all")

        for dt, row in df_t.iterrows():
            records.append({
                "asset_id":        ticker,
                "price_date":      dt.date().isoformat(),
                "open_price":      float(row.get("Open",   None) or 0),
                "high_price":      float(row.get("High",   None) or 0),
                "low_price":       float(row.get("Low",    None) or 0),
                "close_price":     float(row.get("Close",  None) or 0),
                "volume":          int(row.get("Volume",   0) or 0),
                "_fetch_timestamp": fetch_ts.isoformat(),
            })
    except Exception as e:
        print(f"WARNING: Failed to fetch {ticker}: {e}")

print(f"Fetched {len(records)} raw price rows across {len(ticker_list)} tickers")

# ============================================================
# STEP 4: Write to Bronze Delta table
# ============================================================

if records:
    pdf = pd.DataFrame(records)
    sdf = spark.createDataFrame(pdf)

    (sdf.write
        .format("delta")
        .mode("append")
        .option("mergeSchema", "false")
        .saveAsTable("geopolitics.bronze.market_data_raw"))

    print(f"SUCCESS: {len(records)} rows written to geopolitics.bronze.market_data_raw")
else:
    print("WARNING: No data fetched — check ticker symbols and yfinance connectivity")
```

**Schema of `geopolitics.bronze.market_data_raw`:**

| Column | Type | Notes |
|---|---|---|
| `asset_id` | STRING | yfinance ticker |
| `price_date` | STRING | ISO date string (yyyy-MM-dd) |
| `open_price` | FLOAT | Adjusted open |
| `high_price` | FLOAT | Adjusted high |
| `low_price` | FLOAT | Adjusted low |
| `close_price` | FLOAT | Adjusted close |
| `volume` | LONG | Shares/contracts |
| `_fetch_timestamp` | STRING | UTC fetch time |

---

## IV. The Silver Transformation: Computing Daily Returns

The Silver notebook takes raw OHLCV and produces what the validation layer actually needs: **daily log returns, rolling z-scores, and forward return windows.**

### Silver Notebook: `market_data_silver`

```python
# /Workflows/market_data/market_data_silver.py
# Depends on: market_data_bronze, country_asset_mapping
# Output: geopolitics.silver.country_asset_returns
# Schedule: daily @ 07:00 UTC (30 minutes after Bronze completes)

from pyspark.sql import SparkSession, functions as F
from pyspark.sql.window import Window
from pyspark.sql.types import DoubleType
import math
from datetime import datetime, timedelta

spark = SparkSession.builder.getOrCreate()

TARGET_DATE = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

# ============================================================
# STEP 1: Load Bronze, cast types, join to mapping
# ============================================================

bronze = (spark.read.table("geopolitics.bronze.market_data_raw")
    .withColumn("price_date", F.to_date("price_date"))
    .filter(F.col("price_date") >= F.lit("2019-01-01"))
    .filter(F.col("close_price") > 0)
    .select("asset_id", "price_date", "close_price", "volume")
)

mapping = spark.read.table("geopolitics.gold.country_asset_mapping") \
               .select("asset_id", "country_iso3", "asset_type", "primary_signal")

# Join: one row per (asset_id, price_date, country_iso3)
joined = bronze.join(mapping, on="asset_id", how="inner")

# ============================================================
# STEP 2: Compute log daily returns
# ============================================================

# Window: per asset, ordered by date — for lag (previous close)
w_asset = Window.partitionBy("asset_id").orderBy("price_date")

joined = joined.withColumn("prev_close", F.lag("close_price", 1).over(w_asset))

joined = joined.withColumn("log_return",
    F.when(
        (F.col("prev_close").isNotNull()) & (F.col("prev_close") > 0),
        F.log(F.col("close_price") / F.col("prev_close"))
    ).otherwise(F.lit(None).cast(DoubleType()))
)

# ============================================================
# STEP 3: Compute rolling 90-day z-score of daily return
# ============================================================

w_90d = (Window.partitionBy("asset_id")
               .orderBy("price_date")
               .rowsBetween(-89, 0))  # rolling 90-day window

joined = (joined
    .withColumn("return_mean_90d", F.avg("log_return").over(w_90d))
    .withColumn("return_std_90d",  F.stddev("log_return").over(w_90d))
    .withColumn("return_zscore_90d",
        F.when(
            F.col("return_std_90d") > 0,
            (F.col("log_return") - F.col("return_mean_90d")) / F.col("return_std_90d")
        ).otherwise(F.lit(0.0))
    )
)

# ============================================================
# STEP 4: Compute forward return windows (5, 10, 22, 66 days)
# ============================================================
# These are computed as "how much did the price move from this date's close"
# over the next N trading days.
# NOTE: forward returns computed here use FUTURE data — this is correct for
# validation (the backtest looks back at historical forward returns).
# In live signal mode, forward returns will be NULL until time passes.

for fwd_days in [5, 10, 22, 66]:
    joined = joined.withColumn(
        f"fwd_log_return_{fwd_days}d",
        F.lead("log_return", fwd_days).over(w_asset)
        # This is a single forward day's return at +N; for a cumulative return,
        # we need a sum. For simplicity, use approximate: lead on the close_price
    )

# More accurate: cumulative forward return = log(close_at_T+N / close_at_T)
# Use lead on close_price, then compute log ratio
for fwd_days in [5, 10, 22, 66]:
    col_name = f"fwd_close_{fwd_days}d"
    joined = joined.withColumn(col_name, F.lead("close_price", fwd_days).over(w_asset))
    joined = joined.withColumn(
        f"fwd_log_return_{fwd_days}d",
        F.when(
            (F.col(col_name).isNotNull()) & (F.col("close_price") > 0),
            F.log(F.col(col_name) / F.col("close_price"))
        ).otherwise(F.lit(None).cast(DoubleType()))
    )
    # Drop the intermediate forward close column
    joined = joined.drop(col_name)

# ============================================================
# STEP 5: Write to Silver Delta table
# ============================================================

OUTPUT_COLS = [
    "asset_id", "country_iso3", "asset_type", "primary_signal",
    "price_date", "close_price", "log_return",
    "return_mean_90d", "return_std_90d", "return_zscore_90d",
    "fwd_log_return_5d", "fwd_log_return_10d",
    "fwd_log_return_22d", "fwd_log_return_66d",
]

silver_out = (joined
    .select(OUTPUT_COLS)
    .withColumn("_silver_timestamp", F.current_timestamp())
)

# Write mode: overwrite for full history (first run); append for incremental
# For simplicity, use overwrite with REPLACE WHERE for the target date only
(silver_out
    .filter(F.col("price_date") == F.lit(TARGET_DATE))
    .write
    .format("delta")
    .mode("append")
    .option("mergeSchema", "false")
    .saveAsTable("geopolitics.silver.country_asset_returns"))

count_written = silver_out.filter(F.col("price_date") == F.lit(TARGET_DATE)).count()
print(f"SUCCESS: {count_written} rows written to geopolitics.silver.country_asset_returns for {TARGET_DATE}")
```

**Important note on forward returns:** The forward return columns (`fwd_log_return_5d`, etc.) are computed from the full historical series and will be NULL for the most recent N trading days (because the future hasn't happened yet). This is correct behavior — the validation framework uses historical rows where forward returns are populated; the live signal layer uses only the current GRI score.

---

## V. The Validation Join: Connecting GRI to Asset Returns

With the Silver table built, the event study (Tier 1 from Lesson 295) now has all the data it needs. Here is the canonical validation query that starts the backtesting:

```sql
-- Tier 1 Event Study: Do GRI spikes predict adverse forward returns?
-- Run in Databricks SQL Warehouse after both Silver tables are populated

SELECT
    gri.country_iso3,
    gri.event_date                    AS signal_date,
    gri.gri,
    gri.gri_zscore                    AS gri_score,
    gri.gri_momentum_7d,
    gri.risk_regime,
    ret.asset_id,
    ret.asset_type,
    ret.fwd_log_return_5d,
    ret.fwd_log_return_10d,
    ret.fwd_log_return_22d,
    ret.fwd_log_return_66d,

    -- Classification: spike vs non-spike day
    CASE WHEN gri.gri > 2.0 THEN 'spike' ELSE 'non_spike' END AS gri_condition

FROM geopolitics.gold.country_gri AS gri

-- Join to asset returns for primary instruments only
INNER JOIN geopolitics.silver.country_asset_returns AS ret
    ON  gri.country_iso3 = ret.country_iso3
    AND gri.event_date   = ret.price_date  -- NOTE: signal_date aligns to same calendar date
    AND ret.primary_signal = TRUE

WHERE
    gri.event_date BETWEEN '2019-01-01' AND '2024-12-31'  -- in-sample period
    AND ret.fwd_log_return_22d IS NOT NULL                  -- exclude rows without forward data
    AND gri.country_iso3 != '_GBL'                         -- exclude global instruments from country-level test

ORDER BY
    gri.event_date DESC,
    gri.gri DESC
;
```

**Save the result of this query as a Delta table:**
```sql
CREATE TABLE geopolitics.gold.validation_event_study
AS
SELECT ... [the query above]
```

Then compute the test statistics in Python:

```python
# In a Databricks notebook cell
import pandas as pd
from scipy import stats

# Load validation table
val = spark.read.table("geopolitics.gold.validation_event_study").toPandas()

# Separate spike and non-spike populations
for horizon in ["fwd_log_return_5d", "fwd_log_return_10d", "fwd_log_return_22d"]:
    spike    = val[val["gri_condition"] == "spike"][horizon].dropna()
    no_spike = val[val["gri_condition"] == "non_spike"][horizon].dropna()

    t_stat, p_val = stats.ttest_ind(spike, no_spike, equal_var=False)

    print(f"\n{'─'*50}")
    print(f"Horizon: {horizon}")
    print(f"  Spike N={len(spike):,}  | Mean return: {spike.mean()*100:.3f}%")
    print(f"  Non-spike N={len(no_spike):,} | Mean return: {no_spike.mean()*100:.3f}%")
    print(f"  t-statistic: {t_stat:.3f} | p-value: {p_val:.4f}")
    print(f"  Signal: {'✓ FOUND (p<0.05)' if p_val < 0.05 else '✗ NOT FOUND (p≥0.05)'}")
```

**What to expect on first run:**
- At the 22-day horizon for FX instruments (TRY, BRL, ZAR), you should see spike returns approximately 1.5–2× larger in absolute value than non-spike returns.
- Equity ETFs will likely show weaker differentiation — global risk-on/off overwhelms country-specific geopolitical signal for most broad equity instruments.
- The VIX (^VIX) should show *positive* forward returns on spike days — GRI spikes co-occur with global risk-off episodes.

---

## VI. Updating the Workflow DAG

Add the two new market data tasks to the Databricks workflow YAML:

```yaml
# Full gdelt_daily_pipeline workflow (updated)
Tasks:
  # ── GDELT pipeline (unchanged) ──────────────────────────
  - task_key: gdelt_events_bronze
    schedule: daily @ 02:00 UTC
  - task_key: gdelt_gkg_bronze
    schedule: daily @ 02:00 UTC
  - task_key: gdelt_silver_country_daily
    depends_on: [gdelt_events_bronze]
  - task_key: gdelt_silver_country_pair
    depends_on: [gdelt_silver_country_daily]
  - task_key: gdelt_silver_theme_daily
    depends_on: [gdelt_gkg_bronze]
  - task_key: gdelt_silver_validate
    depends_on:
      - gdelt_silver_country_daily
      - gdelt_silver_country_pair
      - gdelt_silver_theme_daily
  - task_key: gdelt_gold_gri
    depends_on: [gdelt_silver_validate]

  # ── Market Data pipeline (NEW) ───────────────────────────
  - task_key: market_data_bronze
    notebook_path: /Workflows/market_data/market_data_bronze
    schedule: daily @ 06:30 UTC  # runs independently; after US close
    cluster: job_cluster_small   # single-node is sufficient; yfinance is I/O-bound
    timeout_seconds: 900

  - task_key: market_data_silver
    notebook_path: /Workflows/market_data/market_data_silver
    depends_on: [market_data_bronze]
    cluster: job_cluster_medium
    timeout_seconds: 1800

  # ── Validation (runs after BOTH GRI and Market Data are ready) ──
  - task_key: validation_event_study
    notebook_path: /Workflows/validation/validation_event_study
    depends_on:
      - gdelt_gold_gri
      - market_data_silver
    cluster: job_cluster_medium
    schedule: weekly @ 08:00 UTC Sunday  # weekly refresh of validation metrics
    timeout_seconds: 3600
```

**Key design decision:** Market data Bronze runs on its own schedule (06:30 UTC daily), independent of the GDELT pipeline. The validation task is scheduled weekly rather than daily — backtesting results don't meaningfully change day-to-day; running it weekly reduces compute cost while keeping the validation current.

---

## VII. Data Quality Checks to Build In

**yfinance is not a production-grade data source.** It has gaps, inconsistencies, and API rate limits. Build these quality checks before you trust the validation results.

```python
# Data quality notebook: run manually after first full history load

quality_checks = spark.sql("""
SELECT
    asset_id,
    COUNT(*) AS total_rows,
    COUNT(log_return) AS non_null_returns,
    MIN(price_date) AS earliest_date,
    MAX(price_date) AS latest_date,
    COUNT(*) - COUNT(log_return) AS null_return_count,
    AVG(ABS(log_return)) AS avg_abs_daily_return,

    -- Flag: if avg abs daily return > 5%, data is likely corrupt or split-adjusted incorrectly
    CASE WHEN AVG(ABS(log_return)) > 0.05 THEN 'SUSPECT' ELSE 'OK' END AS data_quality_flag

FROM geopolitics.silver.country_asset_returns
WHERE price_date >= '2019-01-01'
GROUP BY asset_id
ORDER BY data_quality_flag DESC, avg_abs_daily_return DESC
""")

quality_checks.show(50, truncate=False)
```

**Known issues to watch for:**
- **Currency pairs:** yfinance FX data has frequent gaps for EM pairs (PKR=X, NGN=X). Fill gaps with FRED data for major EM currencies.
- **ETF delistings:** RSX (Russia) was delisted in 2022. The Bronze notebook handles this gracefully (the fetch will return empty for that ticker after 2022), but the validation layer must account for the data gap.
- **Dividend adjustments:** `auto_adjust=True` in yfinance accounts for dividends — but if you switch to raw prices later, your historical returns will be wrong. Keep `auto_adjust=True` for all equity instruments; it is wrong only for FX pairs (no dividends) where it is a no-op.

---

## VIII. The First Validation Run — Bolo's Checklist

Execute in this order after deploying both notebooks:

1. **Run `market_data_bronze` manually** for the full history (start_date = "2019-01-01"). This will take 5–15 minutes depending on cluster size. Watch for rate limit warnings from yfinance — if you see them, add `time.sleep(1)` between ticker batches.

2. **Check Bronze quality** — query `geopolitics.bronze.market_data_raw` to confirm row counts: you should see approximately 1,700 rows per ticker (5 years × 252 trading days/year × 1.35 ≈ 1,700). Missing tickers appear as zero rows.

3. **Run `market_data_silver`** — the full history build will take 20–40 minutes (SparkSQL window functions over 5 years × 35 tickers × 252 days). Watch for null log returns on the first row per ticker (expected — no prior close).

4. **Run the validation SQL query** from Section V. The first result set is your ground truth. Save it. This is the baseline against which all future GRI weight changes and architecture decisions will be measured.

5. **Run the Python statistical test** from Section V. Record the t-statistics and p-values for each horizon in the Investment Log.

6. **File the results** in `reports/investment_log.md` under: "GRI Signal Validation — Initial Backtest Run — [date]."

**Expected total time for first run:** 2–3 hours of Databricks compute plus 1 hour of analysis.

---

## Investment Implications

The market data pipeline is the moment the project crosses from *analysis* to *signal generation.*

Everything before this lesson was building the geopolitical measurement apparatus. After this lesson, you have a testable system: a geopolitical risk score that can be compared against financial market outcomes — historically, and going forward.

**The honest statement of where we are:**
- The GRI *should* work — theory says geopolitical stress precedes market repricing, and GDELT captures geopolitical stress systematically.
- Whether it *does* work in practice is an empirical question the validation run will answer.
- If it works, you have a signal worth building a portfolio process around. If it doesn't, the diagnosis in Lesson 295 (Section IV — Honest Verdict Framework) tells you exactly how to fix it.

**For the portfolio:** No GRI-based position changes until the first validation run is complete. The macro thesis — long real assets, long USD safe haven in multipolar world, cautious EM duration — remains driven by structural reasoning, not GRI signal. The signal must earn its place.

---

## Databricks Angle

**This lesson's build output:**
- `geopolitics.gold.country_asset_mapping` — the lookup table (populate today, ~35 rows)
- `geopolitics.bronze.market_data_raw` — yfinance OHLCV history back to 2019
- `geopolitics.silver.country_asset_returns` — daily log returns, z-scores, forward return windows
- `geopolitics.gold.validation_event_study` — the first backtested GRI signal test

**Pipeline to deploy:**
```
market_data_bronze (daily @ 06:30 UTC)
    → market_data_silver (daily @ 07:00 UTC)
        → [validation_event_study: weekly @ Sunday 08:00 UTC]
```

**Key technical decision:** The forward return window computation (leads in PySpark) is computed over the full historical series. In production, you will need to manage the "future leakage" window — the most recent 66 trading days will have NULL forward returns because the future hasn't arrived. Build your validation queries to filter on `fwd_log_return_22d IS NOT NULL` to avoid silent distortions.

**Next Databricks session:** After the first validation run, the CEO will interpret the results and direct whether to proceed to signal productization (Phase 2) or refine the GRI weighting first.

---

## Key Concepts This Lesson

1. **Two-pipeline architecture** — GDELT pipeline (geopolitical signal) and market data pipeline (asset returns) are independent, joined only at the validation layer; separation maintains data integrity
2. **country_asset_mapping** — the critical lookup table mapping geopolitical actors (country ISO3) to tradeable instruments (yfinance tickers); getting this right determines what the validation can test
3. **Log returns** — `log(close_t / close_{t-1})` is the statistically correct return formulation for time-series analysis; it is additive across time (cumulative log return = sum of daily log returns)
4. **Forward return windows** — precomputed in Silver using PySpark `lead()` over ordered windows; NULL for the most recent N days by construction (the future)
5. **yfinance as a data source** — adequate for backtesting and validation; not suitable for production trading systems (gaps, rate limits, no SLA); Graduate to a commercial data vendor if the GRI produces strong signal

---

## Reflection Questions

1. **The join timing problem:** The GRI for `event_date = 2026-09-02` was computed from GDELT events published through end-of-day September 2. The yfinance close price for `price_date = 2026-09-02` is the US market close at 16:00 ET on September 2. Is this a look-ahead bias problem? On which dates (US vs. European vs. Asian markets) does the alignment break down — and how should your validation query handle countries whose primary instrument trades in a different timezone than GDELT's processing cadence?

2. **The RSX gap:** Russia's equity ETF (RSX) was delisted in March 2022 following sanctions. Your country_asset_mapping lists `RSXJ` as the alternative, but RSXJ was also suspended. For any GRI spike event in Russia *after* March 2022, you have geopolitical signal but no equity market instrument to validate against. How does this affect the statistical validity of Russia's contribution to the Tier 1 event study? Should Russia be included in the cross-sectional factor test (Tier 2), and if so, which instrument do you use as the primary signal?

3. **The global control problem:** The VIX (`^VIX`) and DXY (`DX=F`) are mapped as global instruments (`country_iso3 = '_GBL'`). When you run the event study and find that GRI spikes predict adverse EM FX returns, how do you isolate whether the GRI is driving those returns, or whether the GRI is simply a noisy proxy for global risk sentiment (which the VIX measures more directly and with less lag)? What statistical technique separates country-specific geopolitical signal from global risk-off signal — and what does finding it tell you about whether the GRI carries *incremental* predictive information beyond the VIX?

---

## Questions for Next Session

- **Lesson 297:** After the validation run — GRI result interpretation session. What did the backtest find? Strong signal, weak signal, or noise? The CEO will direct next steps based on results: either productization (signal generator → position sizing) or GRI weight recalibration.
- **Spaced repetition:** Revisit Lesson 75 (Currency Crises Anatomy) after reviewing the BRL/USD and TRY/USD results from the event study. The validation should confirm whether the GRI's 90-day momentum captures the "slow-building pressure" pattern described in that lesson — or whether it missed historical crises entirely.
- **Build checkpoint:** After the market data pipeline runs for 30 days, you will have out-of-sample data for the 2025–2026 period. The first truly honest validation will be: does the GRI trained on 2019–2024 still carry signal in 2025–2026, on data it never saw during calibration?

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 296 delivered: 2026-09-03*
