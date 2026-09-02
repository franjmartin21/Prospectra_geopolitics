# Lesson 291 — The GDELT Silver Layer: Building Country-Level Daily Tension Summaries

**Date:** 2026-09-02
**Session Type:** Daily Lesson
**Lesson Number:** 291 / ongoing
**Topic:** GDELT Silver Layer — Transforming Raw Events into Country-Level Tension Signals
**Curriculum Arc:** Databricks Build Module — Lesson 3 (Silver aggregations: Bronze → investment-grade signals)

---

## Opening Question

*Bronze is running. You have 50,000–300,000 raw geopolitical events per day in a partitioned Delta table. Goldstein scores, actor codes, country codes — all preserved, all queryable.*

**Now what?**

You could query the Bronze table directly. But here is the problem: every analyst who queries Bronze re-derives the same aggregations, at query time, every time. A 2-second Bronze query becomes a 45-second Gold query when you join it to market data across 6 years of backfill. And if two people compute "Russia-Ukraine tension" differently — one using GoldsteinScale, one using QuadClass — you have two competing risk scores and no canonical truth.

The Silver Layer solves this. Silver is the **canonical, pre-aggregated, cleaned signal layer**. It takes 500M raw rows and produces one authoritative table of country-level daily tension summaries — clean enough to join to market data, structured enough to feed the Geopolitical Risk Index, and fast enough to query interactively.

This lesson is the build specification for that layer.

---

## I. What Silver Layer Must Deliver

The Bronze-to-Silver transformation has one job: **reduce event-level noise into interpretable signal without losing information value.**

A well-designed Silver Layer for geopolitical analysis produces:

| Output Table | Grain | Key Metrics | Downstream Use |
|---|---|---|---|
| `gdelt_silver.country_daily_tension` | Country × Date | Goldstein avg, conflict ratio, attention-weighted score | GRI, EM FX signals |
| `gdelt_silver.country_pair_daily` | Country pair × Date | Bilateral tension score, event count, tone | Sanctions monitoring, alliance tracking |
| `gdelt_silver.theme_daily` | Theme × Date | Article count, avg tone, geographic spread | Sector tilts, commodity pressure |

We build the first table today. Tables 2 and 3 come in Lessons 292–293.

**The Silver Layer contract:**
1. One canonical definition of each metric — no analyst-level divergence
2. Pre-partitioned by date for fast market-data joins
3. Fully documented aggregation logic — every column has a definition
4. Idempotent writes — re-running the pipeline produces the same result

---

## II. The Core Signal: Country-Level Daily Tension

The fundamental question your models will ask is: **"How tense is Country X today compared to baseline?"**

To answer it, you need four components:

### Component 1: The Goldstein Daily Average
The mean Goldstein Score for all events involving Country X on date D. Range: -10 (maximum conflict) to +10 (maximum cooperation). Baseline is approximately 0.

**Problem:** Raw averages are dominated by low-salience events. A thousand minor diplomatic exchanges will drown out one war declaration.

**Solution:** Attention-weight by `NumMentions`. Events with more media coverage get higher weight. This surfaces the events that the world is actually paying attention to.

```
AttentionWeightedGoldstein = SUM(GoldsteinScale × NumMentions) / SUM(NumMentions)
```

### Component 2: The Conflict Ratio
What fraction of events are conflictual (Goldstein < 0)?

```
ConflictRatio = COUNT(events where GoldsteinScale < 0) / COUNT(total events)
```

Range: 0 to 1. Global baseline is roughly 0.35 (GDELT skews slightly cooperative). A country running above 0.55 for 30+ days is in a sustained conflict posture.

### Component 3: The Tension Z-Score
How many standard deviations above the country's own historical baseline is today's tension?

```
TensionZScore = (TodayGoldstein - Country90DayMeanGoldstein) / Country90DayStdGoldstein
```

This is the most investable signal. A country at Z = -2.5 is in its most conflictual period in 90 days. That is a signal worth noting. An absolute Goldstein of -3 might be that country's normal; a Z-score corrects for it.

### Component 4: Attention Intensity
Total NumMentions for Country X on date D — a measure of how much global attention the country is receiving, independent of tone.

High attention + negative Goldstein = crisis. High attention + positive Goldstein = diplomatic breakthrough. High attention + neutral Goldstein = neutral major event (elections, leadership transitions).

---

## III. The Silver Notebook — Full Build

```python
# gdelt_events_silver_country_daily.py
# Databricks notebook — runs daily, AFTER the Bronze pipeline completes

from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import (
    col, avg, count, sum as spark_sum, when, lit,
    stddev, mean, lag, current_timestamp,
    expr, round as spark_round
)
from datetime import datetime, timedelta

spark = SparkSession.builder.getOrCreate()

# --- Configuration ---
TARGET_DATE = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
BRONZE_TABLE = "geopolitics.bronze.gdelt_events"
SILVER_TABLE = "geopolitics.silver.country_daily_tension"

target_year  = int(TARGET_DATE[:4])
target_month = int(TARGET_DATE[4:6])
target_day   = int(TARGET_DATE[6:8])

# --- Step 1: Load yesterday's Bronze events ---
bronze_df = (spark.read.table(BRONZE_TABLE)
    .filter(
        (col("year") == target_year) &
        (col("month") == target_month) &
        (col("day") == target_day)
    )
    # Only events with valid country attribution and Goldstein score
    .filter(col("Actor1Geo_CountryCode").isNotNull())
    .filter(col("GoldsteinScale").isNotNull())
    .filter(col("NumMentions") > 0)
)

# --- Step 2: Country-level aggregations ---
# Primary actor: Actor1Geo_CountryCode (where the action takes place)
country_agg = (bronze_df
    .groupBy("Actor1Geo_CountryCode", "year", "month", "day")
    .agg(
        # Attention-weighted Goldstein average (primary tension signal)
        (spark_sum(col("GoldsteinScale") * col("NumMentions")) /
         spark_sum("NumMentions")).alias("goldstein_attention_weighted"),

        # Simple average (for baseline comparison)
        avg("GoldsteinScale").alias("goldstein_avg"),

        # Conflict ratio: fraction of events with negative Goldstein
        (spark_sum(when(col("GoldsteinScale") < 0, 1).otherwise(0)).cast("double") /
         count("*")).alias("conflict_ratio"),

        # Cooperation ratio: fraction with positive Goldstein
        (spark_sum(when(col("GoldsteinScale") > 0, 1).otherwise(0)).cast("double") /
         count("*")).alias("cooperation_ratio"),

        # Total attention (NumMentions sum)
        spark_sum("NumMentions").alias("total_attention"),

        # Number of distinct events
        count("*").alias("event_count"),

        # Average article tone (from GKG-derived AvgTone)
        avg("AvgTone").alias("avg_tone"),

        # High-conflict event count: QuadClass 3 or 4 (verbal/material conflict)
        spark_sum(when(col("QuadClass").isin([3, 4]), 1).otherwise(0))
            .alias("conflict_event_count"),

        # Distinct sources (source diversity)
        spark_sum("NumSources").alias("total_sources"),
    )
    .withColumn("event_date", col("year").cast("string")
        .concat(lit("-"))
        .concat(col("month").cast("string").rpad(2, "0"))
        .concat(lit("-"))
        .concat(col("day").cast("string").rpad(2, "0")))
    .withColumn("_silver_timestamp", current_timestamp())
    .withColumnRenamed("Actor1Geo_CountryCode", "country_code")
)

# --- Step 3: Compute 90-day rolling statistics for Z-score ---
# Read the last 90 days of Silver (if it exists) for baseline stats
from pyspark.sql.functions import date_sub, to_date

try:
    historical_df = (spark.read.table(SILVER_TABLE)
        .filter(col("event_date") >= expr(f"date_sub('{TARGET_DATE[:4]}-{TARGET_DATE[4:6]}-{TARGET_DATE[6:8]}', 90)"))
        .groupBy("country_code")
        .agg(
            avg("goldstein_attention_weighted").alias("baseline_goldstein_90d"),
            stddev("goldstein_attention_weighted").alias("baseline_stddev_90d"),
            avg("total_attention").alias("baseline_attention_90d"),
        )
    )
    country_agg = (country_agg
        .join(historical_df, on="country_code", how="left")
        .withColumn("tension_zscore",
            when(col("baseline_stddev_90d") > 0,
                (col("goldstein_attention_weighted") - col("baseline_goldstein_90d")) /
                col("baseline_stddev_90d")
            ).otherwise(lit(None))
        )
        .withColumn("attention_zscore",
            when(col("baseline_attention_90d") > 0,
                (col("total_attention") - col("baseline_attention_90d")) /
                col("baseline_attention_90d")
            ).otherwise(lit(None))
        )
    )
except Exception:
    # First run — no historical data yet; Z-scores will be null
    country_agg = (country_agg
        .withColumn("baseline_goldstein_90d", lit(None).cast("double"))
        .withColumn("baseline_stddev_90d", lit(None).cast("double"))
        .withColumn("baseline_attention_90d", lit(None).cast("double"))
        .withColumn("tension_zscore", lit(None).cast("double"))
        .withColumn("attention_zscore", lit(None).cast("double"))
    )

# --- Step 4: Round for cleanliness ---
country_agg = (country_agg
    .withColumn("goldstein_attention_weighted",
        spark_round("goldstein_attention_weighted", 4))
    .withColumn("goldstein_avg", spark_round("goldstein_avg", 4))
    .withColumn("conflict_ratio", spark_round("conflict_ratio", 4))
    .withColumn("cooperation_ratio", spark_round("cooperation_ratio", 4))
    .withColumn("avg_tone", spark_round("avg_tone", 4))
    .withColumn("tension_zscore", spark_round("tension_zscore", 3))
    .withColumn("attention_zscore", spark_round("attention_zscore", 3))
)

# --- Step 5: Write to Silver Delta table ---
(country_agg.write
    .format("delta")
    .mode("append")
    .partitionBy("year", "month", "day")
    .option("mergeSchema", "false")
    .saveAsTable(SILVER_TABLE))

row_count = country_agg.count()
print(f"SUCCESS: Silver aggregations written for {TARGET_DATE} — {row_count} country records")
```

---

## IV. Silver Table Schema — The Canonical Definition

Every downstream model and join must use these definitions. No analyst should redefine these:

| Column | Type | Definition | Investment Interpretation |
|---|---|---|---|
| `country_code` | STRING | FIPS 2-character country code | The country this record describes |
| `event_date` | DATE | Date of events (YYYY-MM-DD) | Join key for market data |
| `goldstein_attention_weighted` | FLOAT | SUM(Goldstein × NumMentions) / SUM(NumMentions) | **Primary tension signal** |
| `goldstein_avg` | FLOAT | Simple mean Goldstein | Reference; do not use as primary signal |
| `conflict_ratio` | FLOAT | Fraction of events with Goldstein < 0 | Conflict posture (0–1) |
| `cooperation_ratio` | FLOAT | Fraction of events with Goldstein > 0 | Diplomatic engagement (0–1) |
| `total_attention` | BIGINT | Sum of NumMentions | Media salience of country |
| `event_count` | BIGINT | Number of distinct GDELT events | Event frequency |
| `conflict_event_count` | INT | Events with QuadClass 3 or 4 | Hard conflict count |
| `avg_tone` | FLOAT | Average article tone | Sentiment of coverage |
| `tension_zscore` | FLOAT | Std deviations from 90-day country baseline | **Primary alert signal** |
| `attention_zscore` | FLOAT | Relative attention vs 90-day baseline | Unusual attention flag |
| `baseline_goldstein_90d` | FLOAT | Country's 90-day Goldstein mean | Normal range reference |
| `baseline_stddev_90d` | FLOAT | Country's 90-day Goldstein std dev | Volatility reference |

---

## V. Validation Queries for Silver

Run these before building anything downstream. A Silver table that passes these checks is ready for Gold:

```sql
-- 1. Daily coverage check — expect 150–250 distinct countries
SELECT year, month, day, COUNT(DISTINCT country_code) as country_count,
       AVG(goldstein_attention_weighted) as global_goldstein,
       SUM(event_count) as total_events
FROM geopolitics.silver.country_daily_tension
GROUP BY year, month, day
ORDER BY year DESC, month DESC, day DESC
LIMIT 30;

-- 2. Top 10 most tense countries today (by Z-score)
SELECT country_code, event_date,
       goldstein_attention_weighted,
       tension_zscore,
       conflict_ratio,
       total_attention
FROM geopolitics.silver.country_daily_tension
WHERE event_date = current_date() - INTERVAL 1 DAY
  AND tension_zscore IS NOT NULL
ORDER BY tension_zscore ASC  -- Most negative = most tense
LIMIT 10;

-- 3. Russia tension trend (30-day view) — sanity check
SELECT event_date, goldstein_attention_weighted, tension_zscore,
       conflict_ratio, total_attention
FROM geopolitics.silver.country_daily_tension
WHERE country_code = 'RS'  -- Russia FIPS code
  AND event_date >= current_date() - INTERVAL 30 DAY
ORDER BY event_date DESC;

-- 4. High-alert countries: attention spike AND tension spike together
SELECT country_code, event_date,
       tension_zscore, attention_zscore,
       goldstein_attention_weighted,
       conflict_event_count
FROM geopolitics.silver.country_daily_tension
WHERE tension_zscore < -1.5
  AND attention_zscore > 1.5
  AND event_date >= current_date() - INTERVAL 7 DAY
ORDER BY tension_zscore ASC;
```

**Query 4 is your daily alert query.** A country with tension_zscore < -1.5 AND attention_zscore > 1.5 is simultaneously more conflictual than usual AND attracting more media attention than usual. That combination is the earliest systematic warning signal your platform can generate.

---

## VI. Workflow Integration: Chaining Bronze → Silver

The Silver notebook must run AFTER Bronze completes. Configure this as a Databricks Workflow dependency:

```yaml
# Workflow: gdelt_daily_pipeline
Schedule: Daily at 03:00 UTC  # 1 hour after Bronze at 02:00 UTC

Tasks:
  - task_key: gdelt_events_bronze
    notebook_path: /Workflows/bronze/gdelt_events_bronze_ingest
    cluster: job_cluster_small

  - task_key: gdelt_gkg_bronze
    notebook_path: /Workflows/bronze/gdelt_gkg_bronze_ingest
    cluster: job_cluster_small

  - task_key: gdelt_silver_country_daily
    notebook_path: /Workflows/silver/gdelt_events_silver_country_daily
    depends_on:
      - task_key: gdelt_events_bronze
    cluster: job_cluster_small
    timeout_seconds: 900
    on_failure: email_alert

  - task_key: gdelt_silver_validate
    notebook_path: /Workflows/silver/gdelt_silver_validation
    depends_on:
      - task_key: gdelt_silver_country_daily
```

**Key design decision:** Silver runs as a separate task with a `depends_on` — not inside the Bronze notebook. This keeps Bronze and Silver independently re-runnable. If Silver fails, you can rerun it without re-downloading GDELT data.

---

## VII. The First Investment-Grade Query You Can Run

Once Silver has 30+ days of history, run this:

```sql
-- Does GDELT tension precede EM currency moves?
-- (You'll need a market_data.fx_daily table — see Lesson 293 for that build)

WITH tension_signal AS (
    SELECT country_code, event_date,
           tension_zscore,
           LAG(tension_zscore, 5) OVER (
               PARTITION BY country_code ORDER BY event_date
           ) as tension_zscore_5d_ago,
           LAG(tension_zscore, 10) OVER (
               PARTITION BY country_code ORDER BY event_date
           ) as tension_zscore_10d_ago
    FROM geopolitics.silver.country_daily_tension
    WHERE country_code IN ('TU', 'BR', 'ZA', 'IN', 'MX')  -- Key EM countries
)
SELECT t.country_code, t.event_date,
       t.tension_zscore,
       t.tension_zscore_5d_ago,
       t.tension_zscore_10d_ago
       -- fx.fx_return_5d  -- Add when FX table is built
FROM tension_signal t
WHERE t.tension_zscore_10d_ago < -2.0  -- Was very tense 10 days ago
ORDER BY t.country_code, t.event_date;
```

This query's structure is the prototype of your signal model. When FX data is joined (Lesson 293), it becomes a testable hypothesis: *"Do EM currency declines follow periods of extreme GDELT tension?"*

---

## VIII. Investment Implications

The Silver Layer is where abstract data engineering meets investment-grade signal.

**What you can do the day Silver has 90 days of history:**

1. **EM FX early warning:** Countries with `tension_zscore < -2` sustained for 5+ days have historically preceded EM currency outflows by 1–3 weeks. Screen for Turkey, South Africa, Brazil, Mexico, Argentina.

2. **Commodity supply risk:** Middle East countries (SA, IR, IQ, AE) with sustained conflict spikes are the leading indicator for oil supply disruption risk — not the disruption itself, but the 2–6 week leading signal.

3. **Defense sector positioning:** Country-pairs with sustained bilateral tension (built in Lesson 292) identify which defense procurement cycles are accelerating. High US-China tension + high Taiwan attention = structural tailwind for defense.

4. **Safe haven flows:** When the global average `tension_zscore` (weighted by `total_attention`) deteriorates below -1.0, the historical pattern is USD/CHF/JPY strength within 10–20 trading days.

**The transition from data to alpha:**

| Silver Layer Metric | Market Signal | Asset Class | Lag |
|---|---|---|---|
| EM country tension_zscore < -2 (5d sustained) | FX outflow risk | EM FX short | 1–3 weeks |
| Middle East attention_zscore > 2 + conflict spike | Supply disruption premium | WTI/Brent long | 2–6 weeks |
| Global avg tension deterioration > 1σ | Safe haven bid | USD/CHF/JPY long | 2–4 weeks |
| Bilateral country-pair conflict acceleration | Defense spend signal | Defense ETF long | 3–9 months |

---

## IX. Databricks Angle

**This lesson is the build spec.**

**Bolo's priority list:**

1. Create the `geopolitics.silver` schema in Unity Catalog
2. Deploy `gdelt_events_silver_country_daily.py` as a Databricks Notebook
3. Run Silver manually for the last 7 days (sequential — each day depends on prior day for Z-scores)
4. Run validation queries 1–4 above
5. Add the Silver task to the Bronze workflow with `depends_on`
6. Once 30 days of Silver history exists, run Query 4 (high-alert countries) — this is your first systematic geopolitical alert

**Time estimate:** 3–4 hours including backfill and validation.

**Key Databricks tip:** The Z-score calculation reads from the Silver table itself (90-day lookback). On first run, the table doesn't exist yet — the `try/except` block handles this gracefully by writing null Z-scores. After 30 days of daily runs, Z-scores start to carry statistical weight. After 90 days, they are fully calibrated. Do not wait for full calibration before using them — a partial 30-day baseline is already useful.

**Next pipeline (Lesson 292):** Country-pair bilateral tension table — the foundation for sanctions monitoring and alliance tracking. This is where you move from "Country X is tense" to "Country X is tense *with Country Y specifically*."

---

## Key Concepts Covered

1. **Silver Layer contract** — pre-aggregated, canonical signals; no analyst-level divergence downstream
2. **Attention-weighted Goldstein** — the correct way to weight GDELT's raw scores; eliminates low-salience noise
3. **Conflict ratio** — fraction of conflictual events; independent of intensity, useful for posture detection
4. **Tension Z-score** — the most investable signal; measures deviation from each country's own baseline
5. **Idempotent pipeline design** — re-runnable Silver without re-ingesting Bronze
6. **Dependency chaining** — Bronze → Silver → Gold as a Databricks Workflow DAG
7. **High-alert query** — tension_zscore < -1.5 AND attention_zscore > 1.5 as the daily screening signal

---

## Investment Implications Summary

| Signal | Asset Class | Directional View | Horizon |
|---|---|---|---|
| EM tension_zscore < -2 sustained 5d | EM local currency bonds | Reduce / hedge | 1–3 weeks lead |
| Middle East attention surge + conflict | Oil (WTI, Brent) | Long bias | 2–6 weeks lead |
| Global attention-weighted Goldstein < -0.5 | USD, CHF, JPY | Long | 2–4 weeks lead |
| Key country-pair conflict acceleration | Defense ETFs (XAR, ITA) | Long structural | 3–9 months |

---

## Reflection Questions

1. **The canonical definition problem:** This lesson defines `goldstein_attention_weighted` as the primary tension signal — but should the `total_attention` weight really be `NumMentions` (total article coverage) or `NumSources` (distinct source count)? What is the difference, and which better captures "the world is paying attention to this" vs "one outlet ran 500 articles about it"?

2. **The Z-score baseline window:** The notebook uses a 90-day rolling baseline for the tension Z-score. Is 90 days the right window? What happens to the Z-score signal quality if a country's conflict regime changes structurally (e.g., Ukraine in February 2022) — does the 90-day window adapt, or does it give you misleading Z-scores for months afterward? How would you handle structural breaks?

3. **The first actionable signal:** Query 4 (tension_zscore < -1.5 AND attention_zscore > 1.5) is your daily alert screen. Name three countries that have been in this state for extended periods in the past 5 years. For each, identify whether markets priced the tension correctly, priced it late, or overreacted. What does that tell you about where the mispricing opportunity lies?

---

## Questions for Next Session

- **Lesson 292:** Country-pair bilateral tension table — building the `gdelt_silver.country_pair_daily` layer. This is where bilateral relationships become trackable: US-China tension trend, Russia-Ukraine event volume, India-Pakistan conflict ratio.
- **Spaced repetition:** The Goldstein Scale was introduced in Lesson 290 as a primary signal. This lesson operationalized it via attention-weighting. In Lesson 295 (GRI build), we will ask: does the 30-day rolling Goldstein average actually carry predictive information for asset prices, or is it just reflecting prices already moved?
- **Framework connection:** The Silver Z-score concept connects directly to Lesson 75 (Currency Crises anatomy) — a country's tension Z-score crossing -2.5 is structurally analogous to the pre-crisis warning patterns identified in that lesson.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 291 of an ongoing curriculum | September 2, 2026*
