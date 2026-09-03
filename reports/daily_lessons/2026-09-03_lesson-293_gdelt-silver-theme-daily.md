# Lesson 293 — The GDELT Silver Layer Part 3: Theme Daily Table

**Date:** 2026-09-03
**Session Type:** Daily Lesson
**Lesson Number:** 293 / ongoing
**Topic:** GDELT Silver Layer — Building `gdelt_silver.theme_daily` from the GKG for Sector-Level Signals
**Curriculum Arc:** Databricks Build Module — Lesson 5 (Silver Part 3: GKG themes → sector tilts, commodity pressure, election risk)

---

## Opening Question

*You now have two Silver tables. `country_daily_tension` tells you Russia is at tension_zscore -2.8. `country_pair_daily` tells you the Russia–Ukraine directed pair has an escalation_flag = True. You know who is tense, and you know the bilateral dynamic driving it.*

**But which sector do you tilt? Which commodity do you buy? Which ETF goes long?**

The country-level signal tells you geography. The bilateral signal tells you relationship. Neither tells you *theme* — whether this Russia escalation is about energy supply (→ long European natural gas, utilities short), military confrontation (→ long defense ETFs, long gold), or trade sanctions (→ long agricultural commodities if Russian wheat is at risk, short European industrials exposed to Russian inputs).

The same Russia tension_zscore of -2.8 has completely different portfolio implications depending on whether GDELT's global news coverage is clustering around energy themes, military themes, or diplomatic/sanctions themes. The theme layer is what converts a geography signal into a sector tilt.

This lesson builds `gdelt_silver.theme_daily`. After this table is running, your Silver Layer is complete: three tables, three signal types — country-level, bilateral, thematic. Lesson 294 joins them into the Gold Layer and produces the Geopolitical Risk Index.

---

## I. The GDELT Global Knowledge Graph: What It Is

The GDELT Event database (what you ingested in Lessons 289–292) records *what happened* — actions between actors. The GDELT Global Knowledge Graph (GKG) records *what was written about it* — the themes, organizations, people, and emotional tone embedded in the news articles covering those events.

**The GKG is GDELT's most powerful and underused layer.**

Every 15 minutes, GDELT processes hundreds of thousands of news articles globally and extracts:

| GKG Field | What It Captures |
|---|---|
| `V2Themes` | Controlled-vocabulary themes (e.g., `TAX_FREETRADEAGREEMENT`, `ENERGY_OIL`, `CRISISLEX_C07_WEAPONS_VIOLENCE`) |
| `V2Locations` | All geographic references in the article |
| `V2Persons` | Named individuals mentioned |
| `V2Organizations` | Named organizations |
| `V2Tone` | Emotional tone: positive score, negative score, polarity, activity reference density |
| `V2EnhancedThemes` | Extended taxonomy with location context (e.g., "ENERGY_OIL in Russia") |
| `Counts` | Numeric counts mentioned in articles (casualty counts, refugee numbers, etc.) |
| `SourceCommonName` | The news outlet |

For investment purposes, the signal lives in **`V2Themes` + `V2Tone` + `V2Locations`**. Everything else is enrichment.

### The GKG Theme Taxonomy

GDELT's theme vocabulary contains ~3,000 controlled-vocabulary terms. For investment-relevant signals, you care about approximately 60 of them — the ones that map to investable asset classes.

The taxonomy is organized in clusters. The most investment-relevant:

**Energy Themes:**
- `ENERGY_OIL` — Crude oil references
- `ENERGY_GAS` — Natural gas references
- `ENERGY_NUCLEAR` — Nuclear energy
- `ENERGY_ALTERNATIVE` — Renewables
- `WB_1529_OIL_GAS_AND_MINING` — World Bank: oil/gas/mining
- `OPEC` — OPEC-specific references

**Conflict Themes:**
- `CRISISLEX_C07_WEAPONS_VIOLENCE` — Armed violence
- `MILITARY` — Military operations
- `TERROR` — Terrorism
- `SANCTION` — Sanctions activity
- `UNGP_PEACE_STABILITY` — Peace/stability references

**Trade Themes:**
- `WB_696_TRADE` — Trade broadly
- `TAX_FREETRADEAGREEMENT` — FTAs
- `EMBARGO` — Trade embargoes
- `TARIFF` — Tariff references

**Financial/Monetary:**
- `ECON_INFLATION` — Inflation coverage
- `ECON_RECESSION` — Recession
- `ECON_DEBT` — Debt
- `WB_2176_MONETARY_POLICY` — Central bank / monetary policy
- `CURRENCY_CRISES` — Currency crisis coverage

**Political Transitions:**
- `ELECTIONS` — Election coverage
- `COUP` — Coup attempts
- `PROTEST` — Civil unrest

**Food/Agriculture:**
- `WB_2111_FOOD_SECURITY` — Food security
- `AGRICULTURE` — Agricultural sector
- `WB_864_CROPS` — Crop references

**Critical Minerals:**
- `WB_1530_METALS_AND_MINING` — Mining broadly
- `LITHIUM` — Lithium (where available in GKG)
- `RARE_EARTH_ELEMENTS` — Rare earth references

---

## II. Why Theme Signals Beat Country Signals for Sector Positioning

Consider two geopolitical events with identical country tension scores for "Middle East region":

**Event A:** Iran-Israel diplomatic standoff over nuclear enrichment talks. GDELT themes: `ENERGY_NUCLEAR`, `DIPLOMACY`, `MILITARY`, `WB_2176_MONETARY_POLICY`. Elevated: nuclear and military themes.

**Event B:** Houthi attacks on Red Sea shipping lanes. GDELT themes: `CRISISLEX_C07_WEAPONS_VIOLENCE`, `ENERGY_OIL`, `WB_696_TRADE`, `MILITARY`. Elevated: energy and trade themes.

Both events produce elevated "Middle East" tension. But the portfolio implications are opposite in several dimensions:

| Asset Class | Event A (Nuclear Diplomacy) | Event B (Red Sea Shipping) |
|---|---|---|
| WTI Crude | Modest upside (war risk premium) | Strong upside (supply disruption) |
| LNG / Natural Gas | Moderate upside | Limited (different route) |
| Shipping (BDRY) | Neutral | Strong upside (rate spike) |
| Defense ETFs (ITA) | Strong upside | Moderate |
| Israeli Shekel (ILS) | Downside | Neutral |
| USD | Safe haven bid | Safe haven bid |

The country signal says "Middle East is tense." The theme signal says which mechanism is active. Themes translate to sectors. Sectors translate to positions.

---

## III. Designing the Theme Daily Schema

The theme table has a different grain than the country and pair tables. Instead of Country × Date or Country Pair × Date, the grain is:

**Theme × Geography × Date**

Where "geography" can be: Global (no location), Regional (e.g., EUROPE), or Country-specific (e.g., Russia).

For operational simplicity and join performance, we build two variants:

| Table | Grain | Use Case |
|---|---|---|
| `theme_daily_global` | Theme × Date | Global sector sentiment (e.g., is ENERGY_OIL theme rising globally?) |
| `theme_daily_country` | Theme × Country × Date | Country-specific theme (e.g., is SANCTION theme rising for Russia specifically?) |

This lesson builds `theme_daily_global` as the primary table, with `theme_daily_country` as a downstream derivative. The global table is faster to build and 80% of the investment signal lives there.

### The Schema

| Column | Type | Definition | Investment Interpretation |
|---|---|---|---|
| `theme` | STRING | GDELT controlled-vocabulary theme code | The geopolitical mechanism (e.g., `ENERGY_OIL`) |
| `event_date` | DATE | Date | Join key |
| `article_count` | BIGINT | Articles mentioning this theme | Theme salience |
| `avg_tone` | FLOAT | Average V2Tone.NegativeScore for articles carrying this theme | Negative sentiment toward theme |
| `avg_positive` | FLOAT | Average V2Tone.PositiveScore | Positive sentiment toward theme |
| `polarity` | FLOAT | Average V2Tone.Polarity (positive − negative) | Net sentiment direction |
| `total_attention` | BIGINT | Sum of source diversity across articles | Weighted salience |
| `tone_zscore` | FLOAT | Std deviations from theme's 90-day average tone | Alert signal: is this theme spiking? |
| `attention_zscore` | FLOAT | Relative article count vs 90-day baseline | Coverage surge flag |
| `source_diversity` | FLOAT | Count of distinct outlets covering this theme | Breadth of coverage (vs concentrated) |
| `top_country` | STRING | FIPS of country most associated with this theme today | Geographic attribution |

**The `tone_zscore` column is your primary investment signal.** When `ENERGY_OIL` theme carries a `tone_zscore < -2`, the global news narrative around oil has turned sharply negative relative to its own baseline — which historically precedes (not follows) oil price volatility within 2–4 weeks.

---

## IV. The Theme Daily Notebook — Full Build

The GKG schema differs from the Events schema. The key column is `V2Themes`, which is a semicolon-delimited string of themes:

```
TAX_FREETRADEAGREEMENT;ENERGY_OIL;WB_696_TRADE;MILITARY;CRISISLEX_C07_WEAPONS_VIOLENCE
```

Processing this requires a `split` + `explode` pattern in PySpark.

```python
# gdelt_gkg_silver_theme_daily.py
# Databricks notebook — runs daily, AFTER the GKG Bronze pipeline completes

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, avg, count, sum as spark_sum, when, lit,
    stddev, split, explode, trim, regexp_replace,
    current_timestamp, expr, round as spark_round,
    countDistinct, first
)
from datetime import datetime, timedelta

spark = SparkSession.builder.getOrCreate()

# --- Configuration ---
TARGET_DATE = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
GKG_BRONZE_TABLE = "geopolitics.bronze.gdelt_gkg"
THEME_GLOBAL_TABLE = "geopolitics.silver.theme_daily_global"

target_year  = int(TARGET_DATE[:4])
target_month = int(TARGET_DATE[4:6])
target_day   = int(TARGET_DATE[6:8])

# --- Investment-relevant themes: the 60 themes that map to asset classes ---
# Narrowing to this set reduces compute 70% without losing signal
INVESTMENT_THEMES = [
    # Energy
    "ENERGY_OIL", "ENERGY_GAS", "ENERGY_NUCLEAR", "ENERGY_ALTERNATIVE",
    "WB_1529_OIL_GAS_AND_MINING", "OPEC",
    # Conflict / Military
    "CRISISLEX_C07_WEAPONS_VIOLENCE", "MILITARY", "TERROR", "SANCTION",
    "UNGP_PEACE_STABILITY", "WAR",
    # Trade
    "WB_696_TRADE", "TAX_FREETRADEAGREEMENT", "EMBARGO", "TARIFF",
    # Financial / Monetary
    "ECON_INFLATION", "ECON_RECESSION", "ECON_DEBT",
    "WB_2176_MONETARY_POLICY", "CURRENCY_CRISES", "ECON_BANKRUPTCY",
    # Political
    "ELECTIONS", "COUP", "PROTEST", "POLITICAL_TRANSITION",
    # Food / Agriculture
    "WB_2111_FOOD_SECURITY", "AGRICULTURE", "WB_864_CROPS",
    # Critical minerals
    "WB_1530_METALS_AND_MINING", "RARE_EARTH_ELEMENTS",
    # Geopolitical structures
    "NATO", "BRICS", "UN_SECURITY_COUNCIL", "G7_G8", "G20",
    "WB_686_INTERNATIONAL_RELATIONS",
    # Climate / Environment
    "CLIMATE_CHANGE", "ENV_NATURALRESOURCE",
    # Health (systemic risk)
    "HEALTH_PANDEMIC", "DISEASE",
]

THEMES_SET = set(INVESTMENT_THEMES)
broadcast_themes = spark.sparkContext.broadcast(THEMES_SET)

# --- Step 1: Load yesterday's GKG Bronze ---
gkg_df = (spark.read.table(GKG_BRONZE_TABLE)
    .filter(
        (col("year") == target_year) &
        (col("month") == target_month) &
        (col("day") == target_day)
    )
    .filter(col("V2Themes").isNotNull())
    .filter(col("V2Tone").isNotNull())
    .select(
        "year", "month", "day",
        "GKGRECORDID",
        "SourceCommonName",
        "V2Themes",
        "V2Tone",
        "V2Locations",
    )
)

# --- Step 2: Parse V2Tone ---
# V2Tone format: "Tone,PositiveScore,NegativeScore,Polarity,ActivityReferenceDensity,SelfGroupReferenceDensity"
from pyspark.sql.functions import split as fsplit

gkg_with_tone = (gkg_df
    .withColumn("tone_parts", fsplit(col("V2Tone"), ","))
    .withColumn("tone_overall",    col("tone_parts").getItem(0).cast("float"))
    .withColumn("tone_positive",   col("tone_parts").getItem(1).cast("float"))
    .withColumn("tone_negative",   col("tone_parts").getItem(2).cast("float"))
    .withColumn("tone_polarity",   col("tone_parts").getItem(3).cast("float"))
    .drop("tone_parts")
)

# --- Step 3: Explode themes ---
# V2Themes is semicolon-delimited; each theme may have ",N" offset suffix → strip it
gkg_exploded = (gkg_with_tone
    .withColumn("raw_theme", explode(split(col("V2Themes"), ";")))
    # Theme entries look like "ENERGY_OIL,1" → keep only the name part
    .withColumn("theme", regexp_replace(trim(col("raw_theme")), ",\\d+$", ""))
    .filter(col("theme") != "")
    .drop("raw_theme")
)

# --- Step 4: Filter to investment-relevant themes ---
from pyspark.sql.functions import udf
from pyspark.sql.types import BooleanType

@udf(BooleanType())
def is_investment_theme(t):
    return t in broadcast_themes.value

gkg_filtered = gkg_exploded.filter(is_investment_theme(col("theme")))

# --- Step 5: Aggregate by theme × date ---
theme_agg = (gkg_filtered
    .groupBy("theme", "year", "month", "day")
    .agg(
        count("GKGRECORDID").alias("article_count"),

        # Tone signals
        avg("tone_overall").alias("avg_tone"),
        avg("tone_positive").alias("avg_positive"),
        avg("tone_negative").alias("avg_negative"),
        avg("tone_polarity").alias("polarity"),

        # Source diversity (distinct outlets)
        countDistinct("SourceCommonName").alias("source_diversity"),
    )
    .withColumn("event_date",
        col("year").cast("string")
        .concat(lit("-"))
        .concat(col("month").cast("string"))
        .concat(lit("-"))
        .concat(col("day").cast("string")))
    .withColumn("_silver_timestamp", current_timestamp())
)

# --- Step 6: 90-day rolling baseline for Z-scores ---
target_date_str = f"{TARGET_DATE[:4]}-{TARGET_DATE[4:6]}-{TARGET_DATE[6:8]}"

try:
    historical_theme = (spark.read.table(THEME_GLOBAL_TABLE)
        .filter(col("event_date") >= expr(f"date_sub('{target_date_str}', 90)"))
        .groupBy("theme")
        .agg(
            avg("avg_tone").alias("baseline_tone_90d"),
            stddev("avg_tone").alias("baseline_tone_stddev_90d"),
            avg("article_count").alias("baseline_articles_90d"),
            stddev("article_count").alias("baseline_articles_stddev_90d"),
        )
    )
    theme_agg = (theme_agg
        .join(historical_theme, on="theme", how="left")
        .withColumn("tone_zscore",
            when(col("baseline_tone_stddev_90d") > 0,
                (col("avg_tone") - col("baseline_tone_90d")) /
                col("baseline_tone_stddev_90d")
            ).otherwise(lit(None))
        )
        .withColumn("attention_zscore",
            when(col("baseline_articles_stddev_90d") > 0,
                (col("article_count") - col("baseline_articles_90d")) /
                col("baseline_articles_stddev_90d")
            ).otherwise(lit(None))
        )
    )
except Exception:
    theme_agg = (theme_agg
        .withColumn("baseline_tone_90d", lit(None).cast("double"))
        .withColumn("baseline_tone_stddev_90d", lit(None).cast("double"))
        .withColumn("baseline_articles_90d", lit(None).cast("double"))
        .withColumn("tone_zscore", lit(None).cast("double"))
        .withColumn("attention_zscore", lit(None).cast("double"))
    )

# --- Step 7: Round for cleanliness ---
theme_agg = (theme_agg
    .withColumn("avg_tone",          spark_round("avg_tone", 4))
    .withColumn("avg_positive",      spark_round("avg_positive", 4))
    .withColumn("avg_negative",      spark_round("avg_negative", 4))
    .withColumn("polarity",          spark_round("polarity", 4))
    .withColumn("tone_zscore",       spark_round("tone_zscore", 3))
    .withColumn("attention_zscore",  spark_round("attention_zscore", 3))
)

# --- Step 8: Write to Silver Delta table ---
(theme_agg.write
    .format("delta")
    .mode("append")
    .partitionBy("year", "month", "day")
    .option("mergeSchema", "false")
    .saveAsTable(THEME_GLOBAL_TABLE))

row_count = theme_agg.count()
print(f"SUCCESS: Theme Daily Silver written for {TARGET_DATE} — {row_count} theme records")
```

---

## V. Why the UDF Filter Pattern?

You'll notice Step 4 uses a broadcast UDF to filter themes rather than a SQL `IN` clause. At 40+ themes, the `IN` clause performs fine — but the UDF pattern illustrates a critical Databricks engineering concept: **broadcast variables for large lookup sets.**

When the lookup set grows (say, to 500+ themes for a richer taxonomy), broadcasting it avoids re-transmitting the set to each executor on every filter operation. Get used to this pattern; you'll use it in the Gold Layer when joining geopolitical country codes to currency pairs, which involves a ~250-row lookup that Spark would otherwise handle inefficiently.

For this lesson's 40-theme list: the `IN` clause is fine. The UDF is teaching you the pattern for when the list grows.

Equivalent SQL approach (simpler, adequate for 40 themes):

```python
# After explode, filter with SQL IN instead of UDF:
theme_list_str = "', '".join(INVESTMENT_THEMES)
gkg_filtered = gkg_exploded.filter(
    col("theme").isin(INVESTMENT_THEMES)
)
```

Use the SQL approach in production. The UDF version is for when you move to 200+ themes.

---

## VI. Validation Queries for the Theme Table

```sql
-- 1. Coverage check: how many themes captured per day?
SELECT year, month, day,
       COUNT(DISTINCT theme) as theme_count,
       SUM(article_count) as total_articles
FROM geopolitics.silver.theme_daily_global
GROUP BY year, month, day
ORDER BY year DESC, month DESC, day DESC
LIMIT 30;
-- Expect 35–42 themes per day (not all themes are in every day's news)

-- 2. The daily sector alert: themes spiking negatively
SELECT theme, event_date,
       article_count, avg_tone, tone_zscore,
       attention_zscore, source_diversity
FROM geopolitics.silver.theme_daily_global
WHERE event_date = current_date() - INTERVAL 1 DAY
  AND tone_zscore < -1.5
  AND attention_zscore > 1.0
ORDER BY tone_zscore ASC;

-- 3. Energy theme trend: ENERGY_OIL over 90 days
SELECT event_date, avg_tone, polarity,
       article_count, tone_zscore, attention_zscore
FROM geopolitics.silver.theme_daily_global
WHERE theme = 'ENERGY_OIL'
  AND event_date >= current_date() - INTERVAL 90 DAY
ORDER BY event_date DESC;

-- 4. SANCTION theme surge detection (pre-announcement signal)
SELECT event_date, article_count,
       avg_tone, tone_zscore, attention_zscore, source_diversity
FROM geopolitics.silver.theme_daily_global
WHERE theme = 'SANCTION'
  AND event_date >= current_date() - INTERVAL 60 DAY
ORDER BY event_date DESC;

-- 5. Cross-theme correlation view: when does MILITARY spike alongside ENERGY_OIL?
-- (Manual inspection first; correlation analysis comes in Gold Layer)
SELECT t1.event_date,
       t1.tone_zscore as military_zscore,
       t2.tone_zscore as energy_oil_zscore,
       t1.article_count as military_articles,
       t2.article_count as oil_articles
FROM geopolitics.silver.theme_daily_global t1
JOIN geopolitics.silver.theme_daily_global t2
  ON t1.event_date = t2.event_date
WHERE t1.theme = 'MILITARY'
  AND t2.theme = 'ENERGY_OIL'
  AND t1.event_date >= current_date() - INTERVAL 90 DAY
ORDER BY t1.event_date DESC;

-- 6. ELECTION theme monitor: political transition risk
SELECT event_date, avg_tone, tone_zscore,
       article_count, attention_zscore, source_diversity
FROM geopolitics.silver.theme_daily_global
WHERE theme = 'ELECTIONS'
  AND event_date >= current_date() - INTERVAL 180 DAY
  AND attention_zscore > 1.5
ORDER BY attention_zscore DESC;
```

**Query 2 is your daily sector signal screen.** Themes with `tone_zscore < -1.5` AND `attention_zscore > 1.0` are the geopolitical themes that (a) have turned sharply more negative than their own 90-day baseline AND (b) are attracting more coverage than usual. This is the intersection where mispricing lives.

**Query 5 is your cross-theme correlation prototype.** When `MILITARY` and `ENERGY_OIL` spike simultaneously, the market implication is oil supply disruption risk (the military event threatens supply). When `MILITARY` spikes without `ENERGY_OIL`, the implication is defense spending. The co-movement is the mechanism — and the Gold Layer will formalize this into a Commodity Pressure Model.

---

## VII. Theme × Country Combination: The High-Value Derivative

The global theme table gives you "ENERGY_OIL coverage is unusually negative globally." That is useful. But more useful: "ENERGY_OIL coverage is unusually negative *and geographically concentrated in the Persian Gulf.*"

This is the `theme_daily_country` derived table. It requires joining the GKG's `V2Locations` field to the theme explosion:

```python
# gdelt_gkg_silver_theme_daily_country.py
# Builds AFTER theme_daily_global is written
# More compute-intensive — run on a medium cluster

# V2Locations format: "LocType#LocName#CountryCode#ADM1Code#ADM2Code#Lat#Lon#FeatureID;..."
# We extract CountryCode (position 2, 0-indexed) from each location entry

from pyspark.sql.functions import split as fsplit, explode, col, regexp_extract

gkg_with_locations = (gkg_df
    # Explode V2Locations (semicolon-delimited)
    .withColumn("loc_raw", explode(fsplit(col("V2Locations"), ";")))
    # Extract country code: 3rd field in "#"-delimited location string
    .withColumn("country_code",
        fsplit(col("loc_raw"), "#").getItem(2)
    )
    .filter(col("country_code").isNotNull())
    .filter(col("country_code") != "")
)

# Then re-explode themes and join — produces Theme × Country × Date grain
# (Full code follows same pattern as theme_daily_global)
# Salience filter: only country-theme combinations with article_count >= 5
```

**Deployment decision for Bolo:** Build `theme_daily_global` first and validate it over 30 days before adding `theme_daily_country`. The global table is 95% of the investment signal and 20% of the compute cost. Do not over-engineer before you have 90 days of history to validate the signal.

---

## VIII. Connecting All Three Silver Tables: The Signal Matrix

With all three Silver tables complete, you have a 3-axis signal matrix:

| Axis | Table | Grain | Question Answered |
|---|---|---|---|
| Geography | `country_daily_tension` | Country × Date | *Who* is tense? |
| Relationship | `country_pair_daily` | Country Pair × Date | *Between whom* is the tension? |
| Mechanism | `theme_daily_global` | Theme × Date | *What kind* of tension is it? |

The power is at the intersection. An alert fires on all three axes simultaneously:

1. **Country alert:** Saudi Arabia tension_zscore < -2 (country is in elevated conflict)
2. **Pair alert:** Saudi Arabia–Houthi (Yemen) escalation_flag = True (bilateral mechanism identified)
3. **Theme alert:** `ENERGY_OIL` tone_zscore < -2 AND `CRISISLEX_C07_WEAPONS_VIOLENCE` attention_zscore > 2 (sector mechanism confirmed: energy supply + armed violence)

When all three fire simultaneously on an overlapping geography/theme combination, the signal quality is highest. This is the multi-axis confirmation logic the Gold Layer will formalize.

**Historical example — Red Sea crisis (November 2023 onward):**

The Houthi attacks on Red Sea shipping began November 19, 2023. One week prior, GDELT would have shown:
- Yemen `tension_zscore` rising for 10+ days (country alert)
- Saudi Arabia–Yemen and US–Yemen bilateral conflict ratios rising (pair alert)
- `CRISISLEX_C07_WEAPONS_VIOLENCE` and `WB_696_TRADE` themes both rising in attention (theme alert: armed attacks on trade routes)

The multi-axis signal fired before the first Houthi attack on a commercial vessel. Shipping rates (BDRY) rose 40% in the following 3 weeks. The signal was there; the Gold Layer is what would have surfaced it as an actionable view.

---

## IX. Investment Implications

The theme daily table unlocks four specific investment signals not available from the country or pair tables:

### Signal 1 — Commodity Sector Tilt (Energy)
When `ENERGY_OIL` or `ENERGY_GAS` `tone_zscore < -1.5` sustained for 5+ days, the news narrative around energy supply has turned sharply negative. Historically (validation point for Bolo's Databricks build): does this precede WTI/Brent price moves, or does it lag them? The lag analysis is Lesson 295's empirical work.

**Directional view (pending validation):** Long energy commodity ETFs (XLE, XOP) when `ENERGY_OIL` tone_zscore sustained < -1.5 for 5 days. Exit when tone_zscore returns above -0.5.

### Signal 2 — Defense Sector Structural Signal (Military)
`MILITARY` theme attention_zscore > 2 sustained for 10+ days signals a global news environment saturated with military conflict coverage. This is the macro environment where defense budget increases become politically easy to pass — which flows to defense contractor revenues with a 12–18 month lag.

**Directional view:** When `MILITARY` attention_zscore > 2 for 10+ days AND `SANCTION` attention_zscore > 1.5, long defense ETFs (ITA, XAR) with 12-month horizon.

### Signal 3 — Trade Disruption Signal
`EMBARGO` + `TARIFF` themes rising simultaneously (both attention_zscore > 1.5) is the pre-announcement pattern for major trade policy shifts. The 2018 US-China tariff escalation, the 2022 Russia commodity embargo, and the 2024 semiconductor export control package all showed this pattern 2–4 weeks before the formal announcement.

**Directional view:** When `EMBARGO` + `TARIFF` co-spike: reduce exposure to export-sensitive sectors (global industrials, semiconductor equipment), long domestic-demand sectors in the country being targeted.

### Signal 4 — Election Risk (Emerging Markets)
`ELECTIONS` theme attention_zscore > 2 in combination with `COUP` or `PROTEST` theme elevation signals contested political transition — the scenario EM currencies reprice most sharply. This is not elections generally (which markets price well) but contested elections with instability risk.

**Directional view:** When `ELECTIONS` attention_zscore > 2 AND `PROTEST` attention_zscore > 1.5 simultaneously: reduce long EM FX in affected region, increase USD allocation as hedge.

---

## X. Investment Implications Summary

| Theme Signal | Asset Class | Directional View | Horizon |
|---|---|---|---|
| `ENERGY_OIL` tone_zscore < -1.5 sustained 5d | WTI / Brent crude | Long (supply disruption premium) | 2–4 weeks |
| `ENERGY_GAS` tone_zscore < -2 in Europe-proximate geography | European natgas (TTF), EUR | Long gas / Short EUR | 2–6 weeks |
| `MILITARY` attention_zscore > 2 sustained 10d | Defense ETFs (ITA, XAR, DFEN) | Long structural | 6–18 months |
| `EMBARGO` + `TARIFF` co-spike | Export-sensitive equities | Reduce / hedge | 4–8 weeks |
| `ELECTIONS` + `PROTEST` co-spike (EM context) | EM FX of affected country | Short local / Long USD | 2–6 weeks |
| `ECON_INFLATION` attention_zscore > 2 (global) | Long-duration bonds | Reduce / hedge | 4–12 weeks |
| `CURRENCY_CRISES` theme elevated | EM sovereign spreads | Widen bias | 2–8 weeks |

---

## XI. Databricks Angle

**Bolo's build priority for this lesson:**

1. Confirm the GKG Bronze table (`geopolitics.bronze.gdelt_gkg`) has `V2Themes` and `V2Tone` populated — these are separate from the Events table. If the GKG Bronze pipeline (from Lesson 289) used `gdelt_gkg_raw` fields, verify the column names match.

2. Deploy `gdelt_gkg_silver_theme_daily.py` as a Databricks Notebook.

3. Run the UDF/`isin` filter with the 40-theme list. On first run, expect 35–42 themes to appear daily.

4. Run Validation Query 2 (daily sector alert) for yesterday's data. Read the output: which themes are at their most negative in 90 days? Does it match your intuition about what is happening in the world this week?

5. Run Validation Query 5 (MILITARY × ENERGY_OIL co-movement) for the last 90 days. Manually check: do the co-movement peaks correspond to dates when there were actual energy-relevant military events?

6. Add the theme task to the workflow DAG:

```yaml
# Updated workflow: gdelt_daily_pipeline
Tasks:
  - task_key: gdelt_events_bronze
    ...
  - task_key: gdelt_gkg_bronze
    ...
  - task_key: gdelt_silver_country_daily
    depends_on: [gdelt_events_bronze]
  - task_key: gdelt_silver_country_pair
    depends_on: [gdelt_silver_country_daily]
  - task_key: gdelt_silver_theme_daily
    notebook_path: /Workflows/silver/gdelt_gkg_silver_theme_daily
    depends_on: [gdelt_gkg_bronze]  # Depends on GKG Bronze, NOT Events Bronze
    cluster: job_cluster_medium     # Explode + UDF is more compute-intensive
    timeout_seconds: 1800
  - task_key: gdelt_silver_validate
    depends_on:
      - gdelt_silver_country_daily
      - gdelt_silver_country_pair
      - gdelt_silver_theme_daily    # All three Silver tables must complete before validation
```

**Critical note:** The theme pipeline depends on `gdelt_gkg_bronze`, NOT `gdelt_events_bronze`. These are separate GDELT data products (Events vs GKG). They can run in parallel after their respective Bronze tasks complete. This is a genuine parallel execution opportunity — country/pair Silver and theme Silver are independent pipelines that both write to Silver and both feed Gold.

**Time estimate:** 3–4 hours for deployment and 30-day backfill. The GKG backfill is more compute-intensive than the Events backfill due to the string parsing (split + explode on `V2Themes`). Use a Medium cluster (4–8 nodes) for the backfill.

**When theme Silver has 30 days of history:** Run Query 5 (MILITARY × ENERGY_OIL) and look at dates when both themes co-spiked. Cross-reference with WTI price moves. This is your first empirical signal validation — before Lesson 295's formal lag analysis.

---

## XII. The Silver Layer Is Complete

After this lesson's build, you have three fully operational Silver tables:

| Table | Status After This Lesson | Investment Signal Type |
|---|---|---|
| `country_daily_tension` | ✅ Complete | Country-level tension, EM FX precursor |
| `country_pair_daily` | ✅ Complete | Bilateral escalation, sanctions precursor, coalition monitor |
| `theme_daily_global` | ✅ Complete (this lesson) | Sector tilt, commodity pressure, election risk |

**Lesson 294 begins building the Gold Layer.**

The Gold Layer has one primary output: the **Geopolitical Risk Index (GRI)** — a single composite score per country per day that weights and combines all three Silver tables into an investment-grade risk measure. The GRI is what gets joined to market data, what powers the signal generator, and what becomes the core product of the Databricks platform.

The GRI build is the most analytically demanding step in the project. Before starting it, Lesson 294 will specify the weighting methodology, the composite formula, and the validation framework that tells you whether the GRI is actually carrying predictive information or is elaborate noise.

The 3-month clock: **you are now 5 Silver lessons into the Databricks build module.** Bronze is running, Silver is complete after this build. Gold Layer build starts next lesson. If the Gold Layer validates in Weeks 9–10, you are on schedule for Phase 3 dashboard productization in Weeks 11–12.

---

## Key Concepts Covered

1. **GKG vs Events data** — two distinct GDELT products; Events capture what happened between actors, GKG captures the thematic content of the news narrative covering those events
2. **V2Themes taxonomy** — ~3,000 controlled-vocabulary terms; investment-relevant universe is ~40–60 themes that map to asset classes
3. **Split + explode pattern** — the correct PySpark approach for semicolon-delimited multi-value columns; the performance consideration between UDF and `isin`
4. **V2Tone parsing** — six-field comma-delimited string; `tone_overall`, `tone_positive`, `tone_negative`, `polarity`; the difference between overall tone and polarity
5. **Theme grain vs country grain** — Theme × Date as the analytical unit; why global theme table precedes country-specific theme table
6. **Multi-axis confirmation logic** — country alert + pair alert + theme alert firing simultaneously; how the intersection improves signal quality
7. **Cross-theme correlation** — MILITARY + ENERGY_OIL co-movement as the prototype for the Commodity Pressure Model in the Gold Layer

---

## Reflection Questions

1. **The taxonomy problem:** GDELT's V2Themes taxonomy was built for general news analysis, not investment signals. Some critical investment themes are poorly represented (e.g., "lithium supply chain disruption" doesn't have a clean GDELT theme code). How would you extend the theme table to capture investment-relevant signals that GDELT doesn't natively tag? What data source would you join to fill the gap — and at what point does the engineering cost of a custom NLP layer exceed the value of the incremental signal?

2. **The tone vs attention question:** This lesson uses two signals from the theme table: `tone_zscore` (how negative is the coverage) and `attention_zscore` (how much coverage). A theme with very negative tone but low attention (a small outbreak in a minor country covered by two outlets) is very different from a theme with moderately negative tone but extremely high attention (the trade war story everyone is covering). How would you combine these two signals into a single composite "theme alert score" — and what is the investment logic behind your weighting choice?

3. **The lag empirical question:** This lesson asserts that `ENERGY_OIL` tone_zscore < -1.5 sustained for 5 days is a leading indicator for WTI price moves. But it might be lagging (WTI has already moved and the news is catching up) or coincident (both move together with no predictive value). How would you empirically determine the lag structure using the data you now have in Databricks? What statistical test would you run, and what result would tell you the signal is genuinely predictive vs merely correlated?

---

## Questions for Next Session

- **Lesson 294:** The Gold Layer — Building the Geopolitical Risk Index (GRI). This is the analytical core of the platform: a single composite risk score per country per day, weighted across all three Silver tables. The GRI is the investment-grade output. The lesson will specify the weighting formula, the normalization approach, and the first validation: does the GRI carry predictive information about EM FX moves at a 5, 10, and 20-day forward horizon?
- **Spaced repetition:** The theme signals in this lesson (ELECTIONS + PROTEST → EM FX risk) directly extend the framework in Lesson 9 (Emerging Market Political Risk) and Lesson 75 (Currency Crises anatomy). Review those lessons before Lesson 294 — the GRI weighting methodology draws on the escalation frameworks introduced there.
- **Framework connection:** The multi-axis confirmation logic (country + pair + theme simultaneously) maps to the intelligence tradecraft concept of *corroboration* — a signal gains credibility when confirmed through independent channels. In intelligence analysis, single-source signals are low confidence; multi-source corroborated signals are high confidence. Apply the same logic to the GRI: a GRI score driven by all three Silver tables is more reliable than one driven primarily by one table.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 293 of an ongoing curriculum | September 3, 2026*
