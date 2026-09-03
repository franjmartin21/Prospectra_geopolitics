# Lesson 290 — Building the GDELT Bronze Layer: First Pipeline in the Geopolitical Intelligence Stack

**Date:** 2026-09-02
**Session Type:** Daily Lesson
**Lesson Number:** 290 / ongoing
**Topic:** GDELT Ingestion Pipeline — Architecting and Deploying the Bronze Layer in Databricks
**Curriculum Arc:** Databricks Build Module — Lesson 2 (First pipeline: raw data ingestion)

---

## Opening Question

*Lesson 289 gave you the blueprint. The full platform architecture is on paper. Every table, every pipeline, every model, every dashboard — specified, sequenced, dependency-mapped.*

**Now: where do you actually start? And what does "done" look like for the first pipeline you build?**

The answer matters more than it sounds. Most Databricks projects stall not because the architecture was wrong, but because the first pipeline was built in the wrong order, or was built without a clear definition of done. You spend three weeks building something that doesn't unlock the next thing.

The GDELT Bronze Layer is the right place to start. It is the raw foundation of the entire geopolitical intelligence stack. Nothing downstream — no risk scores, no signal models, no correlation engines — can run without it. Build this first, build it properly, and the rest of the stack has a foundation to stand on.

This lesson is a working build specification. By the end, you will have a pipeline design you can drop into Databricks and run.

---

## I. What is GDELT, and Why Does It Come First?

**GDELT (Global Database of Events, Language, and Tone)** is the largest open-source geopolitical event database in existence. It monitors broadcast, print, and web news in 100+ languages and extracts structured event data in near real-time.

**Three primary tables drive our use case:**

| Table | Update Frequency | Content | Our Use |
|---|---|---|---|
| **Events** | Every 15 minutes | Who did what to whom, where, when (CAMEO coding) | Event detection, conflict monitoring |
| **GKG (Global Knowledge Graph)** | Every 15 minutes | Themes, sentiment, organizations, locations from each article | Sentiment scoring, theme extraction |
| **Mentions** | Every 15 minutes | Every article that mentions each event | Volume/attention signal |

**Why GDELT first:**
1. It is the primary source of geopolitical event signal. Without it, you have no geopolitical data.
2. It is free, publicly accessible, and has a well-documented schema.
3. It is the reference dataset against which market data correlations are built.
4. The Events + GKG combination is sufficient to build a Geopolitical Risk Index — the core output of Phase 2.

**The cost of skipping proper Bronze Layer design:**
If you load GDELT naively (full table dumps without partitioning or schema enforcement), you will hit performance problems the moment you try to run correlation queries. GDELT Events has 500M+ rows going back to 1979. You need to load it correctly from the start.

---

## II. Bronze Layer Design Principles

In the Medallion Architecture, the Bronze Layer is the **raw ingestion layer**. Its job is:
1. Ingest data exactly as it arrives from the source — no transformation, no cleaning
2. Preserve full fidelity (every field, even those you won't use yet)
3. Partition intelligently so downstream reads are fast
4. Track provenance — when was each file ingested, from what source URL

**The three rules of a good Bronze Layer:**
1. **Never transform in Bronze.** Transformations belong in Silver. Bronze is a durable record of what the source said.
2. **Always partition by date.** GDELT data is time-series. Every query you will ever run has a date filter. Partition by year/month/day from day one.
3. **Track ingestion metadata.** Add `_ingest_timestamp` and `_source_file` columns at load time. When a pipeline breaks at 3am six months from now, you will know exactly which files were processed.

---

## III. The GDELT Events Pipeline — Step by Step

### A. Source Structure

GDELT publishes two kinds of files:
- **15-minute files:** `http://data.gdeltproject.org/gdeltv2/YYYYMMDDHHMMSS.export.CSV.zip`
- **Daily master list:** `http://data.gdeltproject.org/gdeltv2/lastupdate.txt` — lists the three most recent 15-minute file URLs (Events, Mentions, GKG)

For our purposes, the **daily Events file** is sufficient to start. Moving to 15-minute updates is Phase 2.

**Daily Events file format:** Tab-separated, 61 columns, no header (the schema is fixed and published by GDELT).

### B. Databricks Pipeline Architecture

```
Source: GDELT public HTTP endpoints
         ↓
[Bronze Notebook] gdelt_events_bronze_ingest.py
  - Download daily file to DBFS / cloud storage
  - Parse tab-separated with enforced schema
  - Add _ingest_timestamp, _source_file columns
  - Write to Delta table: geopolitics.bronze.gdelt_events
  - Partition by: year, month, day
         ↓
Delta Table: geopolitics.bronze.gdelt_events
  - Append-only (never overwrite)
  - Partitioned by year/month/day
  - Full 61-column GDELT schema preserved
         ↓
[Bronze Notebook] gdelt_gkg_bronze_ingest.py
  - Same pattern for GKG table
  - Write to: geopolitics.bronze.gdelt_gkg
         ↓
Delta Table: geopolitics.bronze.gdelt_gkg
```

### C. The 61-Column Events Schema (Critical Fields)

You don't need to memorize all 61 columns. Know the critical ones cold:

| Column | Type | Description | Our Signal |
|---|---|---|---|
| `SQLDATE` | INT | Event date YYYYMMDD | Time axis for all joins |
| `Actor1Code` | STRING | CAMEO code for Actor 1 | Country/faction identification |
| `Actor2Code` | STRING | CAMEO code for Actor 2 | Country/faction identification |
| `EventCode` | STRING | CAMEO event code (e.g., "190" = Use of force) | Event classification |
| `EventRootCode` | STRING | Top-level CAMEO category | High-level event type |
| `GoldsteinScale` | FLOAT | Conflict/cooperation score (-10 to +10) | Tension index |
| `NumMentions` | INT | Total article mentions | Attention/salience weight |
| `NumSources` | INT | Number of distinct sources | Verification weight |
| `AvgTone` | FLOAT | Average sentiment of covering articles | Sentiment signal |
| `Actor1Geo_CountryCode` | STRING | Country where Actor 1 is located | Geographic filter |
| `Actor2Geo_CountryCode` | STRING | Country where Actor 2 is located | Geographic filter |
| `SOURCEURL` | STRING | URL of source article | Provenance |

**The Goldstein Scale is your primary tension signal.** A reading of -10 is maximum conflict (war). +10 is maximum cooperation. A 30-day rolling average of Goldstein scores by country pair gives you the baseline tension index.

### D. The Python Pipeline (Databricks Notebook)

```python
# gdelt_events_bronze_ingest.py
# Databricks notebook — runs daily via Workflow trigger

import requests
import zipfile
import io
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import lit, current_timestamp, input_file_name

spark = SparkSession.builder.getOrCreate()

# --- Configuration ---
TARGET_DATE = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")  # Yesterday's data
BRONZE_TABLE = "geopolitics.bronze.gdelt_events"
GDELT_URL = f"http://data.gdeltproject.org/gdeltv2/{TARGET_DATE}235900.export.CSV.zip"

# --- Schema Definition (61 GDELT Events columns) ---
GDELT_EVENTS_SCHEMA = StructType([
    StructField("GLOBALEVENTID", LongType(), True),
    StructField("SQLDATE", IntegerType(), True),
    StructField("MonthYear", IntegerType(), True),
    StructField("Year", IntegerType(), True),
    StructField("FractionDate", FloatType(), True),
    StructField("Actor1Code", StringType(), True),
    StructField("Actor1Name", StringType(), True),
    StructField("Actor1CountryCode", StringType(), True),
    StructField("Actor1KnownGroupCode", StringType(), True),
    StructField("Actor1EthnicCode", StringType(), True),
    StructField("Actor1Religion1Code", StringType(), True),
    StructField("Actor1Religion2Code", StringType(), True),
    StructField("Actor1Type1Code", StringType(), True),
    StructField("Actor1Type2Code", StringType(), True),
    StructField("Actor1Type3Code", StringType(), True),
    StructField("Actor2Code", StringType(), True),
    StructField("Actor2Name", StringType(), True),
    StructField("Actor2CountryCode", StringType(), True),
    StructField("Actor2KnownGroupCode", StringType(), True),
    StructField("Actor2EthnicCode", StringType(), True),
    StructField("Actor2Religion1Code", StringType(), True),
    StructField("Actor2Religion2Code", StringType(), True),
    StructField("Actor2Type1Code", StringType(), True),
    StructField("Actor2Type2Code", StringType(), True),
    StructField("Actor2Type3Code", StringType(), True),
    StructField("IsRootEvent", IntegerType(), True),
    StructField("EventCode", StringType(), True),
    StructField("EventBaseCode", StringType(), True),
    StructField("EventRootCode", StringType(), True),
    StructField("QuadClass", IntegerType(), True),
    StructField("GoldsteinScale", FloatType(), True),
    StructField("NumMentions", IntegerType(), True),
    StructField("NumSources", IntegerType(), True),
    StructField("NumArticles", IntegerType(), True),
    StructField("AvgTone", FloatType(), True),
    StructField("Actor1Geo_Type", IntegerType(), True),
    StructField("Actor1Geo_FullName", StringType(), True),
    StructField("Actor1Geo_CountryCode", StringType(), True),
    StructField("Actor1Geo_ADM1Code", StringType(), True),
    StructField("Actor1Geo_ADM2Code", StringType(), True),
    StructField("Actor1Geo_Lat", FloatType(), True),
    StructField("Actor1Geo_Long", FloatType(), True),
    StructField("Actor1Geo_FeatureID", StringType(), True),
    StructField("Actor2Geo_Type", IntegerType(), True),
    StructField("Actor2Geo_FullName", StringType(), True),
    StructField("Actor2Geo_CountryCode", StringType(), True),
    StructField("Actor2Geo_ADM1Code", StringType(), True),
    StructField("Actor2Geo_ADM2Code", StringType(), True),
    StructField("Actor2Geo_Lat", FloatType(), True),
    StructField("Actor2Geo_Long", FloatType(), True),
    StructField("Actor2Geo_FeatureID", StringType(), True),
    StructField("ActionGeo_Type", IntegerType(), True),
    StructField("ActionGeo_FullName", StringType(), True),
    StructField("ActionGeo_CountryCode", StringType(), True),
    StructField("ActionGeo_ADM1Code", StringType(), True),
    StructField("ActionGeo_ADM2Code", StringType(), True),
    StructField("ActionGeo_Lat", FloatType(), True),
    StructField("ActionGeo_Long", FloatType(), True),
    StructField("ActionGeo_FeatureID", StringType(), True),
    StructField("DATEADDED", LongType(), True),
    StructField("SOURCEURL", StringType(), True),
])

# --- Download and Parse ---
print(f"Downloading GDELT Events for {TARGET_DATE}...")
response = requests.get(GDELT_URL, timeout=120)
response.raise_for_status()

with zipfile.ZipFile(io.BytesIO(response.content)) as z:
    filename = z.namelist()[0]
    with z.open(filename) as f:
        content = f.read().decode("utf-8")

# Write to DBFS temp location
tmp_path = f"/tmp/gdelt_events_{TARGET_DATE}.csv"
with open(tmp_path, "w") as f:
    f.write(content)

# --- Load to Spark ---
df = (spark.read
    .option("sep", "\t")
    .option("header", "false")
    .schema(GDELT_EVENTS_SCHEMA)
    .csv(f"file://{tmp_path}"))

# Add provenance metadata
df = (df
    .withColumn("_ingest_timestamp", current_timestamp())
    .withColumn("_source_url", lit(GDELT_URL))
    .withColumn("_ingest_date", lit(TARGET_DATE))
    .withColumn("year", lit(int(TARGET_DATE[:4])))
    .withColumn("month", lit(int(TARGET_DATE[4:6])))
    .withColumn("day", lit(int(TARGET_DATE[6:8]))))

# --- Write to Bronze Delta Table ---
(df.write
    .format("delta")
    .mode("append")
    .partitionBy("year", "month", "day")
    .option("mergeSchema", "false")
    .saveAsTable(BRONZE_TABLE))

row_count = df.count()
print(f"SUCCESS: Loaded {row_count:,} events for {TARGET_DATE} to {BRONZE_TABLE}")
```

**What this pipeline does in plain language:**
1. Downloads yesterday's GDELT Events zip file from the public endpoint
2. Unzips and reads the tab-separated data with the enforced 61-column schema
3. Adds three metadata columns: ingest timestamp, source URL, ingest date
4. Adds year/month/day partition columns
5. Appends to the Bronze Delta table, partitioned for fast date-range queries

### E. Databricks Workflow Configuration

```yaml
# Workflow: gdelt_bronze_daily
Schedule: Daily at 02:00 UTC
Tasks:
  - task_key: gdelt_events_bronze
    notebook_path: /Workflows/bronze/gdelt_events_bronze_ingest
    cluster: job_cluster_small  # 2-4 nodes sufficient for daily files
    timeout_seconds: 1800
    on_failure: email_alert

  - task_key: gdelt_gkg_bronze
    notebook_path: /Workflows/bronze/gdelt_gkg_bronze_ingest
    depends_on: []  # Run in parallel with events
    cluster: job_cluster_small
    timeout_seconds: 1800
```

Run at 02:00 UTC daily — GDELT publishes the final daily file by ~01:00 UTC.

---

## IV. Historical Backfill Strategy

The GDELT archive goes back to 1979. You don't need all of it. Here is the recommended backfill window:

| Period | Rationale |
|---|---|
| **2020–present** | Core working dataset. Covers COVID supply chain shock, Ukraine war, post-pandemic commodity cycle. |
| **2015–2019** | Extended context: China's Belt and Road expansion, oil crash, Brexit, Trump tariff round 1. |
| **2010–2014** | Optional: Arab Spring, Eurozone crisis, commodity supercycle peak. |

**Backfill notebook pattern:**
```python
# Run once, not on the daily schedule
# Loop through date range, download and append each daily file
from datetime import date, timedelta

start_date = date(2020, 1, 1)
end_date = date(2026, 9, 1)  # Yesterday

current = start_date
while current <= end_date:
    date_str = current.strftime("%Y%m%d")
    # Call the same ingestion function with date_str as parameter
    ingest_gdelt_events(date_str)
    current += timedelta(days=1)
```

Run this as a separate Databricks Job with a large cluster (8–16 nodes) and expect it to take 2–4 hours for the full 2020–present backfill.

---

## V. Validation Queries

After the first ingestion run, validate with these queries before building anything downstream:

```sql
-- 1. Row count check — expect 50,000–300,000 events per day
SELECT year, month, day, COUNT(*) as event_count
FROM geopolitics.bronze.gdelt_events
GROUP BY year, month, day
ORDER BY year DESC, month DESC, day DESC
LIMIT 30;

-- 2. Schema validation — check critical columns for nulls
SELECT 
    COUNT(*) as total_rows,
    SUM(CASE WHEN SQLDATE IS NULL THEN 1 ELSE 0 END) as null_dates,
    SUM(CASE WHEN GoldsteinScale IS NULL THEN 1 ELSE 0 END) as null_goldstein,
    AVG(GoldsteinScale) as avg_goldstein,
    MIN(GoldsteinScale) as min_goldstein,
    MAX(GoldsteinScale) as max_goldstein
FROM geopolitics.bronze.gdelt_events
WHERE year = 2026;

-- 3. Country coverage — verify key countries are represented
SELECT Actor1Geo_CountryCode, COUNT(*) as events
FROM geopolitics.bronze.gdelt_events
WHERE year = 2026 AND month = 8
GROUP BY Actor1Geo_CountryCode
ORDER BY events DESC
LIMIT 20;

-- 4. Event type distribution — verify CAMEO coding
SELECT EventRootCode, COUNT(*) as events
FROM geopolitics.bronze.gdelt_events
WHERE year = 2026
GROUP BY EventRootCode
ORDER BY events DESC;
```

**What you're looking for:**
- Daily event counts in the 50K–300K range (typical for GDELT)
- Goldstein Scale average near 0 (global baseline)
- US, CN, RU, EU among the top countries (they dominate global news coverage)
- CAMEO root codes 01–20 present (CAMEO covers verbal/physical cooperation and conflict)

---

## VI. Investment Implications

This is not just a data engineering exercise. The GDELT Bronze Layer is the foundation of your geopolitical alpha generation system.

**What this pipeline unlocks, in sequence:**

**Week 1 (Bronze complete):** You have a queryable table of 500M+ geopolitical events. You can already run ad hoc analysis: "How did Ukraine-Russia event volume change in the 30 days before the February 2022 invasion? What did Goldstein scores look like?"

**Week 2–3 (Silver aggregation):** Daily country-level event summaries. This is where the Geopolitical Risk Index starts to take shape.

**Week 4–6 (Gold + models):** Country-level tension scores joined with asset price data. First correlation queries: does Goldstein Score deterioration for Russia precede energy price spikes? How much lead time does the signal have?

**Week 7–8 (Signal generation):** Automated alerts when country-pair tension scores cross thresholds. This is where the platform starts generating investment-grade signals.

**The pipeline you build today is the bottom of that stack. Every day it runs, it compounds. Every day you delay building it, you delay signal generation by one day.**

**Directional views enabled by this pipeline (once Silver/Gold complete):**
- **Energy prices:** GDELT tension scores for Middle East country pairs have historically led oil price volatility by 2–6 weeks
- **EM FX:** Conflict event spikes in EM countries precede currency outflows (classic risk-off mechanism)
- **Defense equities:** Sustained conflict event acceleration (high NumMentions × negative Goldstein) is a structural tailwind for defense contractors
- **Safe haven flows:** Global average Goldstein deterioration is a leading indicator for USD/CHF/JPY strength

---

## VII. Databricks Angle

**This lesson IS the Databricks angle.**

**Immediate build priority:**
1. Create the `geopolitics` Unity Catalog and `bronze` schema
2. Deploy `gdelt_events_bronze_ingest.py` as a Databricks Notebook
3. Run manual ingestion test for the last 7 days
4. Validate with the four queries above
5. Configure the daily Workflow trigger
6. Run the 2020–present backfill

**Time estimate for a Databricks SA:** 4–6 hours total, including backfill runtime.

**Cluster recommendation:** For daily ingestion, a `Standard_DS3_v2` or equivalent (14GB RAM, 4 cores) single-node cluster is sufficient. For backfill, use 8–16 nodes with auto-termination.

**Next pipeline (Lesson 291):** After Bronze is running, Lesson 291 will cover the Silver Layer — country-level daily aggregations that transform raw GDELT rows into the clean, queryable signals that feed the Geopolitical Risk Index.

---

## Key Concepts Covered

1. **GDELT structure** — Events, GKG, and Mentions tables; 15-minute update cadence; 61-column Events schema
2. **Medallion Architecture** — Bronze = raw, append-only ingestion with provenance metadata
3. **Goldstein Scale** — The primary tension signal (-10 conflict to +10 cooperation)
4. **Partitioning strategy** — Year/month/day partitioning for time-series query performance
5. **Pipeline architecture** — Download → schema enforce → metadata inject → Delta append
6. **Backfill strategy** — 2020–present window as the core working dataset
7. **Validation framework** — Four queries that confirm pipeline health before downstream build

---

## Investment Implications Summary

| Downstream Signal | Asset Class | Horizon |
|---|---|---|
| Middle East Goldstein deterioration | Oil (long), Airlines (short) | 2–6 weeks lead |
| EM conflict event spikes | EM FX (short local currency) | 1–4 weeks lead |
| Global tension index rising | USD/CHF/JPY (long), EM equities (short) | 4–12 weeks |
| Defense event volume acceleration | Defense sector ETFs (long) | 3–9 months |
| Russia-Ukraine event normalization | European natural gas (short) | Lagging, 6–18 months |

---

## Reflection Questions

1. **The Goldstein Scale aggregation problem:** If you compute a 30-day rolling average Goldstein score for the US-China actor pair, you will likely find it is close to 0 most of the time — because GDELT captures both cooperative and conflictual events. How would you design a Silver Layer aggregation that isolates the *conflict signal* specifically, filtering out diplomatic noise? What CAMEO codes and QuadClass values would you include?

2. **The attention weighting question:** GDELT's `NumMentions` column tells you how many articles covered each event. A small border skirmish between two minor countries covered extensively by global media might score higher attention than a significant diplomatic summit covered only regionally. How should attention weighting work in your risk index — and what are the risks of weighting by media coverage volume?

3. **The backfill calibration question:** When you run the 2020–present backfill and then query correlations between GDELT tension scores and energy prices, you will face a methodological problem: you are running an in-sample test on data your model was designed using. How do you design the backfill and analysis to avoid look-ahead bias in your early correlation work?

---

## Questions for Next Session

- Next lesson (291): Silver Layer aggregations — building country-level daily tension summaries from raw GDELT Events data
- Concept to revisit: How does CAMEO event coding map to real-world investment-relevant event categories? (Lesson 289 covered the framework; lesson 291 operationalizes it)
- Spaced repetition: Goldstein Scale was introduced here as a signal. Revisit in lesson 295 when building the Geopolitical Risk Index — does the 30-day rolling average carry predictive information, or is it too lagged?

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 290 of an ongoing curriculum | September 2, 2026*
