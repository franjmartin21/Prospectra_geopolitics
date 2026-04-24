# Databricks Build Session — B-02: Market Data Feed
**Date:** April 24, 2026
**Session Type:** CEO Databricks Directive
**Priority:** URGENT — April 27 Deadline
**Blocking:** B-03 (News Sentiment), B-04 (Correlation Engine), Copper Position Open

---

## CEO Directive

B-02 is the most important build task in the project right now. Without market data in Delta Lake, the entire Phase 2 intelligence layer is blocked. The correlation engine (B-04) cannot run without both GDELT event counts (B-01, done) and asset price series (B-02, not done). The copper thesis candidate cannot be formally opened until we can run the correlation analysis.

**Target: B-02 live by April 27. No exceptions. The 3-month clock is running.**

---

## Context: Why This Session Exists

The April 23 portfolio review identified Brent at $94/bbl. As of April 24, Brent is at $105/bbl — driven by Israel threats on Iranian energy infrastructure and renewed Hormuz interference. The energy position nearly triggered its close condition at $87 on April 20, then recovered to $94, and is now at $105.

This $18 swing in 4 days could and should have been tracked automatically. Instead it was caught manually. The alert logic (close energy position if Brent < $85 for 3 consecutive sessions after May 3) must be automated in Databricks before the OPEC+ meeting on May 3. That is the primary urgency driver.

---

## Build Spec: B-02 Market Data Feed

### Architecture: Medallion Pattern (Bronze → Silver → Gold)

Use Databricks Delta Lake with Unity Catalog. Three layers:
- **Bronze**: Raw daily data as-ingested (append-only, no transformation)
- **Silver**: Normalized time series, metadata-tagged, cleaned
- **Gold**: Portfolio signal table — the input layer for B-04 Correlation Engine

---

### Data Source 1: Yahoo Finance (via `yfinance`)

**Library:** `pip install yfinance`
**Schedule:** Daily at 6pm ET (after US market close)
**Lookback on first run:** January 1, 2025 to present (15+ months of history)

**Instruments to ingest:**

| Ticker | Asset Class | Thesis Connection | Position Side |
|---|---|---|---|
| `XOM` | Energy Equity | Long Energy thesis | LONG |
| `CVX` | Energy Equity | Long Energy thesis | LONG |
| `LNG` | Energy Equity | Long Energy thesis | LONG |
| `BNO` | Brent ETF | Energy price tracking | SIGNAL |
| `USO` | WTI ETF | Energy price tracking | SIGNAL |
| `GLD` | Gold ETF | Long Gold thesis | LONG |
| `IAU` | Gold ETF | Long Gold thesis (alt) | LONG |
| `EUAD` | European Defense ETF | Long European Defense | LONG |
| `AGRO3.SA` | Brazil Agri Equity | Long Brazil Agri thesis | LONG |
| `SLCE3.SA` | Brazil Agri Equity | Long Brazil Agri thesis | LONG |
| `BRL=X` | FX: USD/BRL | Brazil BRL exposure | SIGNAL |
| `COPX` | Copper Miners ETF | Copper thesis candidate | WATCH |
| `CPER` | Copper ETF | Copper thesis candidate | WATCH |
| `SCCO` | Copper Miner | Copper thesis candidate | WATCH |
| `FCX` | Copper Miner | Copper thesis candidate | WATCH |
| `DX-Y.NYB` | USD Index (DXY) | Gold wrong-if condition | SIGNAL |
| `EURUSD=X` | EUR/USD FX | European thesis | SIGNAL |
| `SPY` | S&P 500 | Market benchmark | BENCHMARK |
| `TLT` | Long US Treasury | Rate sensitivity | BENCHMARK |

**Bronze table schema:**

```python
bronze_schema = StructType([
    StructField("ticker", StringType(), False),
    StructField("date", DateType(), False),
    StructField("open", DoubleType(), True),
    StructField("high", DoubleType(), True),
    StructField("low", DoubleType(), True),
    StructField("close", DoubleType(), False),
    StructField("volume", LongType(), True),
    StructField("adj_close", DoubleType(), True),
    StructField("ingested_at", TimestampType(), False),
    StructField("source", StringType(), False)
])
```

**Ingestion notebook (`01_ingest_yahoo_finance.py`):**

```python
import yfinance as yf
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, current_timestamp
from datetime import datetime, timedelta

spark = SparkSession.builder.getOrCreate()

TICKERS = [
    "XOM", "CVX", "LNG", "BNO", "USO",
    "GLD", "IAU", "EUAD",
    "AGRO3.SA", "SLCE3.SA", "BRL=X",
    "COPX", "CPER", "SCCO", "FCX",
    "DX-Y.NYB", "EURUSD=X",
    "SPY", "TLT"
]

BRONZE_TABLE = "prospectra.market_data.bronze_yahoo_ohlcv"

# Incremental: pull last 5 days if table exists, else full history from 2025-01-01
try:
    last_date = spark.sql(f"SELECT MAX(date) as max_date FROM {BRONZE_TABLE}").collect()[0]["max_date"]
    start_date = (last_date - timedelta(days=5)).strftime("%Y-%m-%d")
except Exception:
    start_date = "2025-01-01"

end_date = datetime.today().strftime("%Y-%m-%d")

for ticker in TICKERS:
    try:
        df_pd = yf.download(ticker, start=start_date, end=end_date, progress=False)
        df_pd = df_pd.reset_index()
        df_pd.columns = [c.lower().replace(" ", "_") for c in df_pd.columns]
        df_pd["ticker"] = ticker
        df_pd["ingested_at"] = datetime.utcnow()
        df_pd["source"] = "yahoo_finance"
        
        df_spark = spark.createDataFrame(df_pd)
        df_spark.write.format("delta").mode("append") \
            .option("mergeSchema", "true") \
            .saveAsTable(BRONZE_TABLE)
        print(f"✓ {ticker}: {len(df_pd)} rows loaded")
    except Exception as e:
        print(f"✗ {ticker}: {e}")
```

---

### Data Source 2: FRED API (Federal Reserve Economic Data)

**API Key:** Register free at https://fred.stlouisfed.org/docs/api/api_key.html
Store as Databricks secret: `dbutils.secrets.get(scope="prospectra", key="fred_api_key")`

**Library:** `pip install fredapi`
**Schedule:** Daily at 7pm ET (FRED updates ~6pm)

**Series to ingest:**

| FRED Series ID | Description | Investment Use |
|---|---|---|
| `DCOILBRENTEU` | Brent crude spot ($/bbl) | Energy position close rule |
| `DCOILWTICO` | WTI crude spot ($/bbl) | Energy price tracking |
| `GOLDAMGBD228NLBM` | Gold PM fix ($/troy oz) | Gold position tracking |
| `DEXBZUS` | BRL per USD exchange rate | Brazil FX exposure |
| `DEXUSEU` | USD per EUR | European thesis |
| `DTWEXBGS` | Broad USD Index (Fed) | Gold wrong-if condition |
| `CPIAUCSL` | US CPI (SA, monthly) | Stagflation signal |
| `FEDFUNDS` | Fed Funds Rate (effective) | Central bank thesis |
| `T10YIE` | 10-year breakeven inflation | Gold/stagflation signal |
| `T10Y2Y` | 10Y-2Y Treasury spread (yield curve) | Recession signal |
| `BAMLH0A0HYM2` | US HY OAS spread | Risk-off signal |
| `VIXCLS` | CBOE VIX | Market stress |

**Bronze table: `prospectra.market_data.bronze_fred_series`**

```python
bronze_fred_schema = StructType([
    StructField("series_id", StringType(), False),
    StructField("date", DateType(), False),
    StructField("value", DoubleType(), True),
    StructField("series_description", StringType(), True),
    StructField("units", StringType(), True),
    StructField("ingested_at", TimestampType(), False)
])
```

**Ingestion notebook (`02_ingest_fred_api.py`):**

```python
from fredapi import Fred
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, current_timestamp
import pandas as pd
from datetime import datetime

spark = SparkSession.builder.getOrCreate()
fred = Fred(api_key=dbutils.secrets.get(scope="prospectra", key="fred_api_key"))

FRED_SERIES = {
    "DCOILBRENTEU": ("Brent Crude Spot", "USD/bbl"),
    "DCOILWTICO": ("WTI Crude Spot", "USD/bbl"),
    "GOLDAMGBD228NLBM": ("Gold PM Fix", "USD/troy_oz"),
    "DEXBZUS": ("BRL per USD", "BRL/USD"),
    "DEXUSEU": ("USD per EUR", "USD/EUR"),
    "DTWEXBGS": ("Broad USD Index", "index"),
    "CPIAUCSL": ("US CPI SA", "index"),
    "FEDFUNDS": ("Fed Funds Rate", "pct"),
    "T10YIE": ("10Y Breakeven Inflation", "pct"),
    "T10Y2Y": ("10Y-2Y Treasury Spread", "pct"),
    "BAMLH0A0HYM2": ("US HY OAS Spread", "bps"),
    "VIXCLS": ("CBOE VIX", "index"),
}

FRED_TABLE = "prospectra.market_data.bronze_fred_series"
START_DATE = "2025-01-01"

rows = []
for series_id, (description, units) in FRED_SERIES.items():
    try:
        s = fred.get_series(series_id, observation_start=START_DATE)
        for date, value in s.items():
            rows.append({
                "series_id": series_id,
                "date": date.date(),
                "value": float(value) if pd.notna(value) else None,
                "series_description": description,
                "units": units,
                "ingested_at": datetime.utcnow()
            })
        print(f"✓ {series_id}: {len(s)} observations")
    except Exception as e:
        print(f"✗ {series_id}: {e}")

df_spark = spark.createDataFrame(rows)
df_spark.write.format("delta").mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(FRED_TABLE)
print(f"Total rows written: {len(rows)}")
```

---

### Silver Layer: Normalized Time Series

**Notebook: `03_transform_silver_market_data.py`**

Goal: One unified time series table with all instruments, normalized, tagged with metadata. This is the input to B-04.

```python
# Silver table: prospectra.market_data.silver_daily_prices
# Columns: date, instrument, instrument_type, close_price, pct_change_1d, pct_change_5d,
#          pct_change_20d, asset_class, thesis_name, position_side, updated_at

INSTRUMENT_METADATA = {
    # ticker: (instrument_type, asset_class, thesis_name, position_side)
    "XOM": ("equity", "energy", "long_energy", "LONG"),
    "CVX": ("equity", "energy", "long_energy", "LONG"),
    "LNG": ("equity", "energy", "long_energy", "LONG"),
    "BNO": ("etf", "energy", "long_energy", "SIGNAL"),
    "GLD": ("etf", "gold", "long_gold", "LONG"),
    "IAU": ("etf", "gold", "long_gold", "LONG"),
    "EUAD": ("etf", "equity", "long_eu_defense", "LONG"),
    "AGRO3.SA": ("equity", "equity", "long_brazil_agri", "LONG"),
    "SLCE3.SA": ("equity", "equity", "long_brazil_agri", "LONG"),
    "BRL=X": ("fx", "currency", "long_brazil_agri", "SIGNAL"),
    "COPX": ("etf", "commodity", "copper_candidate", "WATCH"),
    "CPER": ("etf", "commodity", "copper_candidate", "WATCH"),
    "DCOILBRENTEU": ("macro", "energy", "long_energy", "SIGNAL"),
    "DCOILWTICO": ("macro", "energy", "long_energy", "SIGNAL"),
    "GOLDAMGBD228NLBM": ("macro", "gold", "long_gold", "SIGNAL"),
    "DEXBZUS": ("macro", "currency", "long_brazil_agri", "SIGNAL"),
    "T10YIE": ("macro", "rates", "macro_signal", "SIGNAL"),
    "T10Y2Y": ("macro", "rates", "macro_signal", "SIGNAL"),
    "VIXCLS": ("macro", "risk", "macro_signal", "SIGNAL"),
    "SPY": ("etf", "equity", "benchmark", "BENCHMARK"),
}
```

---

### Gold Layer: Position Alert Logic

**Notebook: `04_position_alerts.py`** — Build this immediately after silver layer is live.

This is the highest-priority output from B-02. The energy position nearly closed on April 20 ($87/bbl) without any automated alert. This must not happen again.

**Alert rules to implement:**

```python
ALERT_RULES = [
    {
        "name": "ENERGY_CLOSE_RULE",
        "description": "Close energy position if Brent closes below $85 for 3 consecutive sessions after May 3 OPEC+ meeting",
        "instrument": "DCOILBRENTEU",
        "condition": "rolling_3d_close_below_85_after_20260503",
        "action": "CLOSE_POSITION",
        "notify": "franjmartin21@gmail.com",
        "urgency": "HIGH"
    },
    {
        "name": "GOLD_WRONG_IF_MONITOR",
        "description": "Alert if DXY rises >5% in 30 days (precursor to wrong-if condition)",
        "instrument": "DTWEXBGS",
        "condition": "rolling_30d_pct_change_above_5",
        "action": "REVIEW_THESIS",
        "notify": "franjmartin21@gmail.com",
        "urgency": "MEDIUM"
    },
    {
        "name": "COPPER_ENTRY_SIGNAL",
        "description": "Flag if copper (COPX) drops >10% from 30-day high — potential entry opportunity",
        "instrument": "COPX",
        "condition": "pct_below_30d_high_exceeds_10",
        "action": "REVIEW_ENTRY",
        "notify": "franjmartin21@gmail.com",
        "urgency": "MEDIUM"
    }
]
```

---

## Sequence of Operations

Execute in this exact order. Do not start the next step until the previous one passes validation.

| Step | Task | Notebook | Validation Test |
|---|---|---|---|
| 1 | Create Unity Catalog schema `prospectra.market_data` | SQL cell | `SHOW TABLES IN prospectra.market_data` returns empty |
| 2 | Run Yahoo Finance bronze ingest | `01_ingest_yahoo_finance.py` | Table has >15,000 rows; all 19 tickers present |
| 3 | Run FRED bronze ingest | `02_ingest_fred_api.py` | Table has >12 series × 300+ observations |
| 4 | Build silver normalized table | `03_transform_silver_market_data.py` | All instruments have clean `pct_change_1d`, `pct_change_5d` columns; no nulls in `close_price` for trading days |
| 5 | Build position alert logic | `04_position_alerts.py` | Backtest: confirm energy alert would have fired April 20 when Brent hit $87 |
| 6 | Schedule daily jobs | Workflows UI | Yahoo Finance job runs 6pm ET; FRED job runs 7pm ET |

---

## Databricks Configuration Notes

- **Cluster:** Use a small cluster (4-core, Standard_DS3_v2 or equivalent). This is lightweight batch work — don't over-provision.
- **Storage:** Delta Lake with Unity Catalog. Use `prospectra` as catalog, `market_data` as schema.
- **Secrets:** Store FRED API key in Databricks Secrets (`scope: prospectra`). Never hardcode keys in notebooks.
- **Libraries:** Install `yfinance` and `fredapi` on the cluster via Libraries tab. Pin versions to avoid breaking changes.

---

## Connection to B-04 Correlation Engine

Once B-02 is live, the correlation engine becomes buildable. The first correlation test the CEO wants:

**Hypothesis:** GDELT conflict event count for Iran (B-01 output) has a measurable lag correlation with Brent crude price changes (B-02 output).

This is not a hypothetical — we lived through this causality in real time during April. The question is whether GDELT picked it up systematically. If yes, we have a real signal. If no, we need to understand why.

Target analysis:
- Pull GDELT daily Iran conflict event counts from B-01 Delta table
- Pull DCOILBRENTEU daily closing prices from B-02 Delta table
- Run cross-correlation with lags 0d, 1d, 3d, 5d, 10d
- Visualize in Databricks AI/BI dashboard
- If correlation coefficient >0.3 at any lag, flag as investable signal

This is B-04's first task. But it cannot start until B-02 is live.

---

## CEO Priority Note

The 3-month project deadline is April → July 2026. We are at week 3 of 12. Phase 1 (data plumbing) was supposed to be complete by the end of week 3 — which is this weekend. B-01 (GDELT) is done. B-02 is not. The entire Phase 2 intelligence layer is gated on this.

**Complete B-02 by April 27. B-03 News Sentiment by May 1. B-04 Correlation Engine by May 3.**

No slippage. If you hit a blocker, message me immediately. Don't let a technical issue sit.

---

## Questions for Next Databricks Session

1. What does the GDELT event count look like for Iran from February to April? Does it spike correctly when the Hormuz crisis started on March 4?
2. Are the Yahoo Finance historical prices returning accurate data for the Brazilian equities (AGRO3.SA, SLCE3.SA)? These are São Paulo exchange tickers and sometimes have data quality issues.
3. Which FRED series looks most like a leading indicator for Brent crude in the correlation analysis — conflict event count, VIX, or the HY spread?

---

**Databricks Relevance Score: HIGH**
*This session unblocks the entire analytical platform. B-02 is not optional infrastructure — it is the prerequisite for every investment signal we want to build.*

---

*Directive issued by CEO — Prospectra Geopolitics & Investment Project*
*April 24, 2026*
