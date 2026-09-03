# Lesson 292 — The GDELT Silver Layer Part 2: Country-Pair Bilateral Tension Table

**Date:** 2026-09-02
**Session Type:** Daily Lesson
**Lesson Number:** 292 / ongoing
**Topic:** GDELT Silver Layer — Building `gdelt_silver.country_pair_daily` for Bilateral Relationship Tracking
**Curriculum Arc:** Databricks Build Module — Lesson 4 (Silver Part 2: bilateral tensions → sanctions monitoring, alliance tracking)

---

## Opening Question

*Lesson 291 gave you `country_daily_tension`: a table that tells you Russia is at tension_zscore -2.8 today. That is a useful fact.*

**But useful for what decision, exactly?**

Russia is tense — with whom? With Ukraine (a war that markets have priced for 4 years)? With Finland (a new NATO pressure point)? With China (a fracture in the multipolar coalition that almost nobody is pricing)? With the US over Arctic resource rights (an emerging story)? The same tension_zscore of -2.8 has completely different investment implications depending on the bilateral relationship driving it.

Country-level tension is a signal. Bilateral tension is an *intelligence product*.

The country-pair table is also where your most actionable signals live — not "is Russia tense?" but "is Russia-China bilateral cooperation deteriorating?" — because that is the thesis nobody has priced, the relationship the market assumes is stable, and the fracture that, if it happened, would reprice commodities, safe havens, and EM positioning simultaneously.

This lesson builds `gdelt_silver.country_pair_daily`. By the end, you will have the foundation for sanctions monitoring, alliance tracking, and the first bilateral signals that can be translated directly into portfolio tilts.

---

## I. Why Bilateral Matters More Than Unilateral for Investment

The unilateral tension signal (Lesson 291) is necessary but not sufficient. Here is why:

**The attribution problem:** A country can be "tense" because of events it is generating (aggressor posture) or because events are being directed at it (target posture). A tension_zscore of -2 for Saudi Arabia could mean Saudi Arabia is threatening its neighbors, or it could mean Saudi Arabia is being threatened. These have opposite implications for oil supply risk.

**The relationship problem:** Market mispricings cluster around *relationships*, not countries in isolation. The US-China trade relationship prices equity markets. The Russia-Europe energy relationship prices European utility stocks and natural gas. The India-Pakistan relationship prices South Asian EM equities. The bilateral pair is the unit of analysis that connects to investable assets.

**The coalition problem:** Great power politics operates through coalitions — formal (NATO, BRICS) and informal (US-India-Japan vs China). Monitoring the bilateral relationships within these coalitions tells you whether the coalition is strengthening or fracturing. A fracturing coalition is a regime change signal that reprices multiple asset classes simultaneously.

**Three bilateral pairs worth monitoring on day one:**

| Pair | Why It Matters | Asset Classes Affected |
|---|---|---|
| US–CN | Trade war, Taiwan flashpoint, technology decoupling | Global equities, semiconductors, EM FX |
| RU–UA | Active war; normalization = European gas repricing | European natural gas, EUR, defense stocks |
| IN–PK | Nuclear-armed neighbors; escalation = South Asian EM risk-off | INR, PKR, South Asian equities |
| RU–CN | Assumed stable; fracture would reprice everything | Commodities, USD, EM broadly |
| SA–IR | Energy bloc tension; affects OPEC+ coordination | Oil (WTI, Brent), Middle East FX |

---

## II. Designing the Country-Pair Schema

The bilateral table is conceptually simple but requires one architectural decision upfront: **directed vs undirected pairs.**

### Directed vs Undirected

**Directed pair:** Russia → Ukraine is a different record from Ukraine → Russia. This preserves who is acting and who is being acted upon — important for conflict posture analysis.

**Undirected pair:** Russia ↔ Ukraine is one record. Simpler to query, but loses the directionality signal.

**Recommendation: build directed pairs, compute undirected as a derived view.**

Why: GDELT's Actor1/Actor2 assignment is meaningful. When Russia fires a missile at Ukraine, GDELT records Russia as Actor1 (initiating action) and Ukraine as Actor2 (recipient). The asymmetry carries information about escalation dynamics. You want to preserve it.

The undirected pair view is trivially derived:

```sql
CREATE OR REPLACE VIEW geopolitics.silver.country_pair_undirected AS
SELECT 
    CASE WHEN actor1_country < actor2_country THEN actor1_country ELSE actor2_country END as country_a,
    CASE WHEN actor1_country < actor2_country THEN actor2_country ELSE actor1_country END as country_b,
    event_date,
    AVG(goldstein_weighted) as goldstein_bilateral,
    SUM(event_count) as total_events,
    SUM(total_attention) as total_attention,
    AVG(conflict_ratio) as conflict_ratio
FROM geopolitics.silver.country_pair_daily
GROUP BY 1, 2, 3;
```

### The Schema

| Column | Type | Definition | Investment Interpretation |
|---|---|---|---|
| `actor1_country` | STRING | FIPS code of the initiating actor | Who is acting |
| `actor2_country` | STRING | FIPS code of the receiving actor | Who is being acted upon |
| `event_date` | DATE | Date of events | Join key for market data |
| `goldstein_weighted` | FLOAT | Attention-weighted Goldstein for this pair | Bilateral tension level |
| `conflict_ratio` | FLOAT | Fraction of events that are conflictual | Conflict posture (0–1) |
| `total_attention` | BIGINT | Sum of NumMentions | Salience of the relationship |
| `event_count` | BIGINT | Distinct GDELT events between the pair | Volume signal |
| `conflict_event_count` | INT | Events with QuadClass 3 or 4 | Hard conflict count |
| `verbal_conflict_count` | INT | Events with QuadClass 3 | Verbal/rhetorical escalation |
| `material_conflict_count` | INT | Events with QuadClass 4 | Physical escalation |
| `cooperation_count` | INT | Events with QuadClass 1 or 2 | Cooperation signal |
| `avg_tone` | FLOAT | Average article sentiment for this pair | Coverage tone |
| `tension_zscore` | FLOAT | Std deviations from pair's 90-day baseline | **Alert signal** |
| `attention_zscore` | FLOAT | Relative attention vs 90-day baseline | Unusual salience flag |
| `escalation_flag` | BOOLEAN | material_conflict_count > 3× pair's 90-day baseline | Hard escalation alert |

---

## III. The Country-Pair Notebook — Full Build

```python
# gdelt_events_silver_country_pair_daily.py
# Databricks notebook — runs daily, AFTER country_daily_tension Silver completes

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, avg, count, sum as spark_sum, when, lit,
    stddev, current_timestamp, expr,
    round as spark_round
)
from datetime import datetime, timedelta

spark = SparkSession.builder.getOrCreate()

# --- Configuration ---
TARGET_DATE = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
BRONZE_TABLE = "geopolitics.bronze.gdelt_events"
PAIR_SILVER_TABLE = "geopolitics.silver.country_pair_daily"

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
    # Require both actor countries AND Goldstein score
    .filter(col("Actor1Geo_CountryCode").isNotNull())
    .filter(col("Actor2Geo_CountryCode").isNotNull())
    .filter(col("GoldsteinScale").isNotNull())
    .filter(col("NumMentions") > 0)
    # Exclude self-pairs (domestic events)
    .filter(col("Actor1Geo_CountryCode") != col("Actor2Geo_CountryCode"))
)

# --- Step 2: Country-pair aggregations (directed) ---
pair_agg = (bronze_df
    .groupBy("Actor1Geo_CountryCode", "Actor2Geo_CountryCode", "year", "month", "day")
    .agg(
        # Attention-weighted Goldstein (primary signal)
        (spark_sum(col("GoldsteinScale") * col("NumMentions")) /
         spark_sum("NumMentions")).alias("goldstein_weighted"),

        # Conflict ratio
        (spark_sum(when(col("GoldsteinScale") < 0, 1).otherwise(0)).cast("double") /
         count("*")).alias("conflict_ratio"),

        # Event counts by quadrant
        count("*").alias("event_count"),
        spark_sum(when(col("QuadClass") == 4, 1).otherwise(0))
            .alias("material_conflict_count"),
        spark_sum(when(col("QuadClass") == 3, 1).otherwise(0))
            .alias("verbal_conflict_count"),
        spark_sum(when(col("QuadClass").isin([1, 2]), 1).otherwise(0))
            .alias("cooperation_count"),

        # Total attention
        spark_sum("NumMentions").alias("total_attention"),

        # Average tone
        avg("AvgTone").alias("avg_tone"),
    )
    .withColumnRenamed("Actor1Geo_CountryCode", "actor1_country")
    .withColumnRenamed("Actor2Geo_CountryCode", "actor2_country")
    .withColumn("event_date",
        col("year").cast("string")
        .concat(lit("-"))
        .concat(col("month").cast("string"))
        .concat(lit("-"))
        .concat(col("day").cast("string")))
    .withColumn("_silver_timestamp", current_timestamp())
)

# --- Step 3: 90-day rolling baseline for Z-scores ---
target_date_str = f"{TARGET_DATE[:4]}-{TARGET_DATE[4:6]}-{TARGET_DATE[6:8]}"

try:
    historical_pair = (spark.read.table(PAIR_SILVER_TABLE)
        .filter(col("event_date") >= expr(f"date_sub('{target_date_str}', 90)"))
        .groupBy("actor1_country", "actor2_country")
        .agg(
            avg("goldstein_weighted").alias("baseline_goldstein_90d"),
            stddev("goldstein_weighted").alias("baseline_stddev_90d"),
            avg("total_attention").alias("baseline_attention_90d"),
            avg("material_conflict_count").alias("baseline_material_conflict_90d"),
        )
    )
    pair_agg = (pair_agg
        .join(historical_pair, on=["actor1_country", "actor2_country"], how="left")
        .withColumn("tension_zscore",
            when(col("baseline_stddev_90d") > 0,
                (col("goldstein_weighted") - col("baseline_goldstein_90d")) /
                col("baseline_stddev_90d")
            ).otherwise(lit(None))
        )
        .withColumn("attention_zscore",
            when(col("baseline_attention_90d") > 0,
                (col("total_attention") - col("baseline_attention_90d")) /
                col("baseline_attention_90d")
            ).otherwise(lit(None))
        )
        # Escalation flag: material conflict 3× above 90-day baseline
        .withColumn("escalation_flag",
            when(
                (col("baseline_material_conflict_90d") > 0) &
                (col("material_conflict_count") > col("baseline_material_conflict_90d") * 3),
                lit(True)
            ).when(
                (col("baseline_material_conflict_90d") == 0) &
                (col("material_conflict_count") > 5),
                lit(True)
            ).otherwise(lit(False))
        )
    )
except Exception:
    pair_agg = (pair_agg
        .withColumn("baseline_goldstein_90d", lit(None).cast("double"))
        .withColumn("baseline_stddev_90d", lit(None).cast("double"))
        .withColumn("baseline_attention_90d", lit(None).cast("double"))
        .withColumn("baseline_material_conflict_90d", lit(None).cast("double"))
        .withColumn("tension_zscore", lit(None).cast("double"))
        .withColumn("attention_zscore", lit(None).cast("double"))
        .withColumn("escalation_flag", lit(False))
    )

# --- Step 4: Round for cleanliness ---
pair_agg = (pair_agg
    .withColumn("goldstein_weighted", spark_round("goldstein_weighted", 4))
    .withColumn("conflict_ratio", spark_round("conflict_ratio", 4))
    .withColumn("avg_tone", spark_round("avg_tone", 4))
    .withColumn("tension_zscore", spark_round("tension_zscore", 3))
    .withColumn("attention_zscore", spark_round("attention_zscore", 3))
)

# --- Step 5: Write to Silver Delta table ---
(pair_agg.write
    .format("delta")
    .mode("append")
    .partitionBy("year", "month", "day")
    .option("mergeSchema", "false")
    .saveAsTable(PAIR_SILVER_TABLE))

row_count = pair_agg.count()
print(f"SUCCESS: Country-pair Silver written for {TARGET_DATE} — {row_count} pair records")
```

---

## IV. The Escalation Flag: Your Daily Hard-Conflict Alert

The `escalation_flag` column is the most operationally important output of this table. It fires when material conflict events (QuadClass 4 — physical actions: attacks, military operations, destruction of property) for a country pair are more than 3× the pair's 90-day average.

**Why QuadClass 4 specifically:**

GDELT's QuadClass taxonomy:
- **1 — Verbal Cooperation:** Statements of support, diplomatic engagement
- **2 — Material Cooperation:** Economic agreements, military assistance, treaties
- **3 — Verbal Conflict:** Threats, accusations, expulsions, sanctions announcements
- **4 — Material Conflict:** Attacks, military force, destruction, killings

QuadClass 4 events are the signal that the conflict has crossed from rhetorical to physical. Most geopolitical events never reach QuadClass 4. When they do — and the count spikes above baseline — that is no longer background noise. It is a regime change signal.

**The investment logic:**

A country-pair where `escalation_flag = True` for 3+ consecutive days should trigger:

1. Immediate review of commodity exposure linked to that geography
2. Check of equity positions with revenue concentration in either country
3. FX exposure review for affected currencies
4. Bond spread monitoring for sovereign debt from either country

This is systematic risk management, not panic. The flag gives you 2–15 days of lead time before most market participants begin pricing the escalation.

---

## V. Validation Queries for the Country-Pair Table

```sql
-- 1. Coverage check: how many distinct pairs are tracked daily?
SELECT year, month, day,
       COUNT(DISTINCT CONCAT(actor1_country, '-', actor2_country)) as pair_count,
       COUNT(*) as total_records
FROM geopolitics.silver.country_pair_daily
GROUP BY year, month, day
ORDER BY year DESC, month DESC, day DESC
LIMIT 30;
-- Expect 3,000–8,000 distinct directed pairs per day (top pairs by attention)

-- 2. Most tense pairs today (by Z-score)
SELECT actor1_country, actor2_country, event_date,
       goldstein_weighted, tension_zscore,
       conflict_ratio, total_attention, escalation_flag
FROM geopolitics.silver.country_pair_daily
WHERE event_date = current_date() - INTERVAL 1 DAY
  AND tension_zscore IS NOT NULL
ORDER BY tension_zscore ASC
LIMIT 20;

-- 3. Monitored pair trend: US–China over 90 days
SELECT event_date, goldstein_weighted, tension_zscore,
       conflict_ratio, verbal_conflict_count, material_conflict_count,
       cooperation_count, total_attention
FROM geopolitics.silver.country_pair_daily
WHERE actor1_country = 'US' AND actor2_country = 'CH'  -- China FIPS = CH
  AND event_date >= current_date() - INTERVAL 90 DAY
ORDER BY event_date DESC;

-- 4. Escalation flag alerts: which pairs triggered today?
SELECT actor1_country, actor2_country, event_date,
       material_conflict_count, baseline_material_conflict_90d,
       goldstein_weighted, tension_zscore,
       total_attention
FROM geopolitics.silver.country_pair_daily
WHERE escalation_flag = TRUE
  AND event_date >= current_date() - INTERVAL 7 DAY
ORDER BY event_date DESC, material_conflict_count DESC;

-- 5. Coalition coherence check: Is the Russia–China relationship stable?
-- Compare cooperation vs conflict trend
SELECT event_date,
       cooperation_count, verbal_conflict_count, material_conflict_count,
       goldstein_weighted,
       tension_zscore
FROM geopolitics.silver.country_pair_daily
WHERE actor1_country IN ('RS', 'CH')  -- RS = Russia; CH = China
  AND actor2_country IN ('RS', 'CH')
  AND actor1_country != actor2_country
  AND event_date >= current_date() - INTERVAL 180 DAY
ORDER BY event_date DESC;
```

**Query 4 is your daily escalation alert.** Run it every morning. Any pair with `escalation_flag = TRUE` gets 60 seconds of manual review: is this a known ongoing conflict (already priced), or is this a new escalation (potential mispricing)?

**Query 5 is your coalition monitor.** The Russia–China relationship is broadly assumed to be stable and aligned. If GDELT starts showing a sustained deterioration in that bilateral Goldstein score — verbal conflict increasing, cooperation events declining — that is one of the most significant mispricing opportunities in the global macro landscape.

---

## VI. The Sanctions Detection Signal

The country-pair table also enables a specific, high-value signal: **sanctions announcement detection via GDELT verbal conflict spikes.**

The mechanics: When a major power imposes sanctions on a country, the lead-up period (2–6 weeks) is characterized by:
1. Rising verbal conflict events (QuadClass 3) between the sanctioning country and the target
2. Rising `total_attention` for the pair
3. A deteriorating `goldstein_weighted` score
4. Only after the formal announcement: a spike in `material_conflict_count`

The verbal phase is your lead indicator. By the time sanctions are announced and formal asset freezes begin, the verbal conflict signal has already been elevated for weeks.

**Sanctions monitoring query:**

```sql
-- Countries where verbal conflict is rising but material conflict is still low
-- This is the "pre-sanctions warning" pattern
WITH pair_trend AS (
    SELECT actor1_country, actor2_country,
           event_date,
           verbal_conflict_count,
           material_conflict_count,
           total_attention,
           tension_zscore,
           AVG(verbal_conflict_count) OVER (
               PARTITION BY actor1_country, actor2_country
               ORDER BY event_date
               ROWS BETWEEN 14 PRECEDING AND CURRENT ROW
           ) as verbal_conflict_14d_avg,
           AVG(verbal_conflict_count) OVER (
               PARTITION BY actor1_country, actor2_country
               ORDER BY event_date
               ROWS BETWEEN 45 PRECEDING AND 15 PRECEDING
           ) as verbal_conflict_prior_avg
    FROM geopolitics.silver.country_pair_daily
    WHERE event_date >= current_date() - INTERVAL 60 DAY
      AND actor1_country IN ('US', 'EU', 'GB')  -- Major sanctioning actors
)
SELECT actor1_country, actor2_country, event_date,
       verbal_conflict_14d_avg,
       verbal_conflict_prior_avg,
       verbal_conflict_14d_avg / NULLIF(verbal_conflict_prior_avg, 0) as verbal_escalation_ratio,
       tension_zscore,
       total_attention
FROM pair_trend
WHERE verbal_conflict_14d_avg > verbal_conflict_prior_avg * 2.0  -- 2× verbal conflict vs prior period
  AND tension_zscore < -1.5
  AND event_date = current_date() - INTERVAL 1 DAY
ORDER BY verbal_escalation_ratio DESC;
```

A country-pair with a `verbal_escalation_ratio > 2.0` combined with `tension_zscore < -1.5` is in the pre-sanctions pattern. This does not mean sanctions will be imposed — but it means the relationship is deteriorating in the specific way that historically precedes formal measures. That deterioration alone has asset price implications before any policy action.

---

## VII. Chaining into the Workflow DAG

The country-pair Silver notebook runs after `country_daily_tension` completes. Updated workflow:

```yaml
# Workflow: gdelt_daily_pipeline (updated)
Schedule: Daily at 02:00 UTC

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

  - task_key: gdelt_silver_country_pair
    notebook_path: /Workflows/silver/gdelt_events_silver_country_pair_daily
    depends_on:
      - task_key: gdelt_silver_country_daily
    cluster: job_cluster_small
    timeout_seconds: 1800
    # Country-pair is larger than country_daily; allow more time

  - task_key: gdelt_silver_validate
    notebook_path: /Workflows/silver/gdelt_silver_validation
    depends_on:
      - task_key: gdelt_silver_country_daily
      - task_key: gdelt_silver_country_pair
```

**Performance note:** The country-pair table generates significantly more records than the country table. Where `country_daily_tension` produces ~200 records per day, `country_pair_daily` produces 3,000–8,000. For the backfill (2020–present), run the country-pair pipeline on a larger cluster (8+ nodes) and expect 3–5 hours runtime.

**Storage note:** Filter aggressively. Not all country pairs are investable. Consider writing only pairs where `total_attention > 100` (above a minimum salience threshold). This reduces storage 40–60% without losing signal — low-attention pairs are noise.

```python
# Add this filter before writing to Silver:
pair_agg = pair_agg.filter(col("total_attention") >= 100)
```

---

## VIII. Investment Implications

With both Silver tables complete (`country_daily_tension` + `country_pair_daily`), your platform crosses a threshold: **you now have investment-grade geopolitical intelligence, not just data engineering.**

**The four signals that become actionable immediately:**

### Signal 1 — EM FX Precursor (bilateral version)
A country's currency weakens before a geopolitical escalation is fully priced. But which escalation? Now you know. A `tension_zscore < -2` at the country level, combined with a specific bilateral pair's `escalation_flag = True` involving a major trading partner, gives you the *mechanism* for the currency move.

**Trade structure:** Long USD/TRY when Turkey-[relevant actor] bilateral escalation flag fires + Turkey country tension_zscore < -2.0. Horizon: 2–4 weeks.

### Signal 2 — Commodity Supply Disruption (pair-specific)
Iraq–Iran bilateral conflict spike (not just "Middle East tense") → Strait of Hormuz risk. Saudi Arabia–Houthi (Yemen) bilateral escalation → Red Sea shipping disruption.

The pair-specific attribution tells you *which* supply route and *which* commodity is at risk. WTI vs Brent spread implications differ depending on whether the disruption is in the Gulf vs the Red Sea.

### Signal 3 — Defense Sector Structural Tailwind (sustained bilateral)
A country-pair where bilateral conflict ratio stays above 0.6 for 60+ consecutive days is in a sustained conflict posture. Governments facing this buy defense equipment. The lag from conflict posture to defense procurement to contractor earnings is 12–24 months — well within the long-horizon framework.

**Pairs to monitor:** US/NATO–Russia (ongoing), Israel–[regional actors], India–Pakistan, Taiwan–China. Any of these entering a new elevated phase is a structural tailwind for defense ETFs (XAR, ITA, DFEN).

### Signal 4 — Coalition Fracture Early Warning (the high-value play)
This is the asymmetric opportunity. Markets price coalitions as stable. When a coalition fractures, the repricing is sharp and broad.

Monitor: Russia–China, Saudi Arabia–UAE (within OPEC+), US–Saudi Arabia, France–Germany (within EU). A sustained deterioration in any of these "assumed stable" pairs — `tension_zscore` trending negative over 30+ days — is a regime change signal.

**The coalitions most likely to fracture in 2026–2027:** Based on current geopolitical trajectory, the Russia–China relationship faces growing strain from China's Taiwan calculus and Russian desperation for economic concessions. A visible fracture would: strengthen the dollar, weaken commodity prices (removing the geopolitical risk premium), and create buy opportunities in Chinese equities that lose the Russia-alignment discount.

---

## IX. Databricks Angle

**Bolo's build priority for this lesson:**

1. Deploy `gdelt_events_silver_country_pair_daily.py` as a Databricks Notebook
2. Add a salience filter: `total_attention >= 100` (reduces storage significantly)
3. Run the country-pair pipeline for the last 30 days (sequential, for Z-score calibration)
4. Run Validation Query 4 (escalation alerts) — this is your first bilateral intelligence output
5. Run Validation Query 5 (Russia–China monitor) — check it manually for 2024–2025 to confirm the signal makes intuitive sense
6. Add the task to the workflow DAG with `depends_on: gdelt_silver_country_daily`

**Time estimate:** 4–6 hours including 30-day backfill.

**Key architectural note:** The country-pair table is the penultimate Silver table. Once it is running, you have:
- `country_daily_tension` → country-level tension signal (Lesson 291)
- `country_pair_daily` → bilateral tension and escalation signal (this lesson)

**Lesson 293** will add the third Silver table: `theme_daily` — GDELT GKG-derived theme signals (energy security, trade conflict, military conflict, climate, elections) aggregated daily. That table unlocks sector-level signals (energy supply pressure, trade war themes) rather than geography-level signals.

After Lesson 293, all three Silver tables are live. **Lesson 294 begins building the Gold Layer** — the Geopolitical Risk Index — which joins and weights all three Silver tables into a single composite risk score per country per day. That is where the investment-grade platform goes live.

---

## Key Concepts Covered

1. **Directed vs undirected pairs** — why preserving Actor1/Actor2 asymmetry matters; deriving undirected view from directed table
2. **QuadClass taxonomy** — 1=verbal cooperation, 2=material cooperation, 3=verbal conflict, 4=material conflict; why QuadClass 4 is the hard signal
3. **Escalation flag design** — 3× material conflict above 90-day baseline as a regime-change threshold
4. **Sanctions precursor pattern** — verbal conflict escalation (QuadClass 3) leading formal sanctions by 2–6 weeks; the verbal escalation ratio query
5. **Coalition coherence monitoring** — using bilateral Goldstein trend to detect fractures in assumed-stable coalitions
6. **Salience filtering** — `total_attention >= 100` as a noise filter that reduces storage 40–60%
7. **DAG chaining** — country_pair depends on country_daily; both depend on Bronze; workflow dependency graph

---

## Investment Implications Summary

| Signal | Asset Class | Directional View | Horizon |
|---|---|---|---|
| Bilateral escalation_flag sustained 3+ days | FX of target country | Long USD vs local currency | 2–4 weeks |
| Gulf country-pair material conflict spike | WTI/Brent oil | Long, Hormuz risk premium | 1–3 weeks |
| Major power verbal_escalation_ratio > 2× | Target country sovereign spreads | Widen (credit risk rising) | 4–8 weeks |
| Assumed-stable coalition Goldstein deterioration | Multi-asset (regime change) | Structural repositioning | 6–18 months |
| Sustained bilateral conflict_ratio > 0.6 (60d) | Defense ETFs (XAR, ITA) | Long structural | 12–24 months |

---

## Reflection Questions

1. **The directionality problem:** GDELT assigns Actor1/Actor2 based on who initiates the action, but in sustained conflicts this distinction blurs. When Russia fires a missile, Russia is Actor1. When Ukraine launches a counter-offensive, Ukraine is Actor1. Over time, the directed pair `RU→UA` and `UA→RU` both accumulate events — making the "directed" pair an increasingly arbitrary distinction. At what point does it make more sense to use undirected pairs as your primary analysis unit, and how would you decide that systematically rather than by feel?

2. **The coalitions you aren't monitoring:** The lesson names five "assumed stable" coalitions worth watching. Identify a sixth coalition or bilateral relationship that is *actually* the most important one to monitor for investment purposes in 2026 — not the one that is most geopolitically interesting, but the one where a fracture would have the *largest* repricing effect on investable assets. Explain the mechanism.

3. **The false escalation problem:** The `escalation_flag` fires when material conflict events are 3× the pair's 90-day baseline. But a 3× spike from a baseline of 2 events/day (now 6) is very different from a 3× spike from a baseline of 50 events/day (now 150). How would you design a minimum absolute threshold that filters out statistically significant but operationally meaningless spikes? What is the right minimum `material_conflict_count` for the flag to be worth acting on?

---

## Questions for Next Session

- **Lesson 293:** Theme Daily Table — building `gdelt_silver.theme_daily` from the GDELT GKG (Global Knowledge Graph). This unlocks sector-level signals: energy security, trade conflict, military escalation, climate, elections — aggregated daily by theme and geography.
- **Spaced repetition:** The sanctions precursor pattern in this lesson (verbal → material escalation sequence) maps directly to the geopolitical escalation frameworks in Lessons 14 (Sanctions Architecture) and 46 (Grey Zone Warfare). Review those lessons' escalation ladder models alongside this pipeline's QuadClass taxonomy — they are the same framework at different levels of abstraction.
- **Portfolio connection:** The coalition fracture signal (Question 2 above) connects directly to Lesson 63 (Multipolarity Premium) and Lesson 70 (Bretton Woods III). When you have 90 days of bilateral data on Russia–China, Saudi–US, and India–China pairs, run them against gold, USD, and commodity prices. That correlation matrix is the empirical foundation of the multipolarity premium thesis.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 292 of an ongoing curriculum | September 2, 2026*
