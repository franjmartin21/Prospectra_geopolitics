# Lesson 294 — The Gold Layer: Building the Geopolitical Risk Index (GRI)

**Date:** 2026-09-03
**Session Type:** Daily Lesson
**Lesson Number:** 294 / ongoing
**Topic:** Gold Layer — Building the Geopolitical Risk Index (GRI): Composite Formula, Weighting Methodology, and Validation Framework
**Curriculum Arc:** Databricks Build Module — Lesson 6 (Gold Layer Part 1: combining all three Silver tables into a single investment-grade risk score)

---

## Opening Question

*You have three Silver tables: `country_daily_tension` tells you who is tense. `country_pair_daily` tells you between whom and why. `theme_daily_global` tells you which sector mechanism is active.*

**But your portfolio manager doesn't read database rows. They read a number.**

When a PM asks "how risky is Brazil today relative to its own history?" or "which EM country should I be watching most carefully this week?" — they need a single, comparable, time-consistent score. Not three tables to manually inspect. Not a subjective judgment call. A number with a methodology they can audit, validate, and eventually trust.

The Geopolitical Risk Index (GRI) is that number. Building it correctly is the most analytically demanding step in this entire project. The GRI either carries predictive signal — in which case it becomes the core investment product — or it is elaborate noise — in which case everything built on top of it is worthless.

**This lesson builds the GRI and, more importantly, specifies the validation framework that tells you which of those two outcomes you are looking at.**

---

## I. What the GRI Is — and What It Isn't

### What It Is

The GRI is a composite score — one number per country per day — that measures the intensity and direction of geopolitical risk for that country relative to its own historical baseline. It is:

- **Normalized:** Scores are Z-scores, expressed in standard deviations from the country's own 90-day baseline. A GRI of +3 means the country is in a state of geopolitical stress 3 standard deviations above its own recent normal. This makes a 3 for Brazil comparable to a 3 for Germany.
- **Multi-source:** It combines country-level tension, bilateral conflict dynamics, and thematic sector risk into a single number — each source contributing a weighted share.
- **Forward-looking in design:** The weighting is calibrated not to summarize current risk (lagging) but to maximize the lead time before market pricing adjusts (leading). The validation framework tells you whether you achieved this.
- **Directional:** The GRI produces both a magnitude (how intense) and a direction signal (rising, falling, stable) based on week-over-week momentum.

### What It Isn't

- It is **not a prediction** that a crisis will occur. It is a probability-shifting input — when GRI is elevated, the distribution of potential outcomes shifts, and markets should price differently.
- It is **not comparable across time in absolute terms** — only in Z-score terms. A GRI of +2.5 in 2023 is not the same absolute level as +2.5 in 2026 if GDELT coverage has changed.
- It is **not self-sufficient** — it is one input to an investment process, not a trading signal by itself.

---

## II. The Weighting Methodology

### The Three Sources and Their Weights

The GRI draws from three Silver table signals. The proposed weighting is:

| Source | Signal Variable | Weight | Rationale |
|---|---|---|---|
| `country_daily_tension` | `tension_zscore` | 45% | Direct country-level conflict salience; the broadest-coverage signal |
| `country_pair_daily` | Bilateral conflict intensity (derived) | 35% | Bilateral dynamics are higher-precision: they identify the *mechanism*, not just the ambient stress level |
| `theme_daily_global` | Theme relevance score (country-geography-weighted) | 20% | Theme signal is global by construction; the geographic attribution is imprecise, so it carries less weight |

**Why 45/35/20?** This is a starting point, not a truth. The correct weighting is empirically determined by which combination produces the strongest lead relationship with EM FX and sovereign spread moves. The validation framework (Section V) tells you how to refine these weights. Begin with 45/35/20 as a calibrated prior — it reflects the precision hierarchy of the three signals.

### The Bilateral Intensity Score

The pair table doesn't have a single comparable metric — it has `escalation_flag`, `conflict_share`, `avg_goldstein_score`, and `avg_tone`. To roll it up to a country-level contribution, compute a **Bilateral Conflict Intensity (BCI)** per country per day:

```
BCI(country, date) =
    MAX over all pairs involving this country of:
        (conflict_share × |avg_goldstein_score| × escalation_flag_multiplier)

Where escalation_flag_multiplier = 1.5 if escalation_flag = True, else 1.0
```

The MAX (rather than mean) is deliberate: a country's risk profile is dominated by its worst bilateral relationship on any given day. Syria's overall GRI should be driven by its worst conflict pair, not an average that dilutes it with peaceful neighbors.

Then Z-score the BCI against the country's own 90-day history.

### The Theme Attribution Score

The theme signal is global, but you need to attribute it to a country. The method:

1. For each country with GRI > baseline, identify its **primary geopolitical concern** based on what is happening in its region (from the pair table).
2. Map that concern to a theme cluster: energy → `ENERGY_OIL`/`ENERGY_GAS`; conflict → `MILITARY`/`CRISISLEX_C07_WEAPONS_VIOLENCE`; trade → `EMBARGO`/`TARIFF`; political → `ELECTIONS`/`COUP`.
3. The **Theme Attribution Score (TAS)** for a country is the attention_zscore of its primary theme cluster — weighted by how concentrated that theme's geography is in the country's region.

For initial deployment: simplify. Use a flat 20% weight on the global `MILITARY` attention_zscore as a proxy for all countries. When you have the `theme_daily_country` table (Lesson 293, optional derivative), replace this with the country-specific theme weight. The simplification costs you precision; it does not cost you the ability to validate the model.

---

## III. The GRI Formula

```
GRI(country, date) =
    (0.45 × tension_zscore)
  + (0.35 × BCI_zscore)
  + (0.20 × TAS)

Where all components are pulled from the same event_date.
```

The result is a **weighted Z-score composite** — interpretable in standard deviation units above/below the country's own historical norm. A GRI of 0 means the country is at its own historical average risk level. A GRI of +2 is two standard deviations above its own norm — elevated, notable. A GRI of +3 or above is extreme — historically rare, typically associated with periods of imminent crisis.

### Adding Momentum

The GRI score alone captures level. **Momentum captures acceleration** — and markets respond more sharply to acceleration than level:

```
GRI_momentum(country, date) =
    GRI(country, date) - GRI(country, date - 7 days)
```

A GRI_momentum of +0.5 means the country's geopolitical risk has risen 0.5 standard deviations in the past week. When both GRI > 1.5 AND GRI_momentum > 0.3 simultaneously, the alert condition is most investment-relevant: the country is already elevated AND still rising.

### The Output Schema: `geopolitics.gold.country_gri`

| Column | Type | Definition |
|---|---|---|
| `country_code` | STRING | FIPS country code |
| `event_date` | DATE | Date |
| `tension_zscore` | FLOAT | Raw from country_daily_tension Silver table |
| `bci_zscore` | FLOAT | Bilateral Conflict Intensity, Z-scored |
| `tas` | FLOAT | Theme Attribution Score |
| `gri` | FLOAT | Composite GRI (weighted sum) |
| `gri_momentum_7d` | FLOAT | GRI change vs 7 days prior |
| `gri_percentile_90d` | FLOAT | GRI's percentile in country's own 90-day distribution |
| `alert_flag` | BOOLEAN | GRI > 1.5 AND momentum > 0.3 |
| `risk_regime` | STRING | `ELEVATED`, `CRISIS`, `DECLINING`, `STABLE` — categorical classification |
| `_gold_timestamp` | TIMESTAMP | Processing timestamp |

The `risk_regime` classification logic:
- `CRISIS`: GRI > 2.5 OR gri_percentile_90d > 95th percentile
- `ELEVATED`: GRI between 1.5 and 2.5 AND momentum > 0
- `DECLINING`: GRI > 1.0 AND momentum < -0.3 (stress is easing)
- `STABLE`: everything else

---

## IV. The Full Build: Gold Layer Notebook

```python
# gdelt_gold_gri.py
# Databricks Gold Layer notebook
# Runs AFTER all three Silver pipelines complete (parallel Silver → sequential Gold)
# Depends on: country_daily_tension, country_pair_daily, theme_daily_global

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, avg, stddev, max as spark_max, min as spark_min,
    count, lit, when, expr, round as spark_round,
    current_timestamp, lag, percent_rank, ntile
)
from pyspark.sql.window import Window
from datetime import datetime, timedelta

spark = SparkSession.builder.getOrCreate()

TARGET_DATE = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
target_date_str = f"{TARGET_DATE[:4]}-{TARGET_DATE[4:6]}-{TARGET_DATE[6:8]}"

# --- Source tables ---
COUNTRY_TENSION_TABLE  = "geopolitics.silver.country_daily_tension"
COUNTRY_PAIR_TABLE     = "geopolitics.silver.country_pair_daily"
THEME_GLOBAL_TABLE     = "geopolitics.silver.theme_daily_global"
GRI_OUTPUT_TABLE       = "geopolitics.gold.country_gri"

# ============================================================
# STEP 1: Load today's country tension signal
# ============================================================

tension_today = (spark.read.table(COUNTRY_TENSION_TABLE)
    .filter(col("event_date") == lit(target_date_str))
    .select(
        "country_code",
        "event_date",
        "tension_zscore",
        "event_count",
        "avg_goldstein",
        "avg_tone",
    )
)

# ============================================================
# STEP 2: Build Bilateral Conflict Intensity (BCI) per country
# ============================================================

pair_today = (spark.read.table(COUNTRY_PAIR_TABLE)
    .filter(col("event_date") == lit(target_date_str))
)

# For each country appearing as either actor1 or actor2, compute BCI
# We union both actor perspectives, then take max per country

pair_actor1 = (pair_today
    .select(
        col("actor1_country_code").alias("country_code"),
        col("conflict_share"),
        col("avg_goldstein_score"),
        col("escalation_flag"),
    )
)

pair_actor2 = (pair_today
    .select(
        col("actor2_country_code").alias("country_code"),
        col("conflict_share"),
        col("avg_goldstein_score"),
        col("escalation_flag"),
    )
)

pair_both = pair_actor1.union(pair_actor2)

from pyspark.sql.functions import abs as spark_abs

pair_bci = (pair_both
    .withColumn("escalation_multiplier",
        when(col("escalation_flag") == True, 1.5).otherwise(1.0)
    )
    .withColumn("bci_raw",
        col("conflict_share") * spark_abs(col("avg_goldstein_score")) *
        col("escalation_multiplier")
    )
    .groupBy("country_code")
    .agg(
        spark_max("bci_raw").alias("bci_raw"),
    )
)

# Z-score the BCI against 90-day history
bci_90d_baseline = (spark.read.table(COUNTRY_PAIR_TABLE)
    .filter(col("event_date") >= expr(f"date_sub('{target_date_str}', 90)"))
    .withColumn("escalation_multiplier",
        when(col("escalation_flag") == True, 1.5).otherwise(1.0)
    )
    .withColumn("bci_raw",
        col("conflict_share") * spark_abs(col("avg_goldstein_score")) *
        col("escalation_multiplier")
    )
    # Compute per-country max per day first
    .groupBy("actor1_country_code", "event_date")
    .agg(spark_max("bci_raw").alias("bci_daily_max"))
    .groupBy("actor1_country_code")
    .agg(
        avg("bci_daily_max").alias("bci_mean_90d"),
        stddev("bci_daily_max").alias("bci_std_90d"),
    )
    .withColumnRenamed("actor1_country_code", "country_code")
)

pair_bci_zscored = (pair_bci
    .join(bci_90d_baseline, on="country_code", how="left")
    .withColumn("bci_zscore",
        when(col("bci_std_90d") > 0,
            (col("bci_raw") - col("bci_mean_90d")) / col("bci_std_90d")
        ).otherwise(lit(0.0))
    )
    .select("country_code", "bci_zscore")
)

# ============================================================
# STEP 3: Get the global MILITARY theme as TAS proxy
# ============================================================

theme_today = (spark.read.table(THEME_GLOBAL_TABLE)
    .filter(
        (col("event_date") == lit(target_date_str)) &
        (col("theme") == "MILITARY")
    )
    .select(
        col("attention_zscore").alias("military_attention_zscore"),
        col("tone_zscore").alias("military_tone_zscore"),
    )
)

# Single row — broadcast it as TAS for all countries
# (Simple proxy: replace with country-specific theme after theme_daily_country is built)
if theme_today.count() > 0:
    military_row = theme_today.collect()[0]
    tas_value = float(military_row["military_attention_zscore"] or 0.0)
else:
    tas_value = 0.0

# ============================================================
# STEP 4: Assemble GRI
# ============================================================

gri_today = (tension_today
    .join(pair_bci_zscored, on="country_code", how="left")
    .fillna({"bci_zscore": 0.0})
    .withColumn("tas", lit(tas_value))
    .withColumn("gri",
        (lit(0.45) * col("tension_zscore")) +
        (lit(0.35) * col("bci_zscore")) +
        (lit(0.20) * col("tas"))
    )
)

# ============================================================
# STEP 5: Add Momentum (requires reading yesterday's GRI)
# ============================================================

from pyspark.sql.functions import date_sub

prev_date_str = (datetime.strptime(target_date_str, "%Y-%m-%d") -
                 timedelta(days=7)).strftime("%Y-%m-%d")

try:
    gri_7d_ago = (spark.read.table(GRI_OUTPUT_TABLE)
        .filter(col("event_date") == lit(prev_date_str))
        .select(
            col("country_code"),
            col("gri").alias("gri_7d_ago"),
        )
    )
    gri_today = (gri_today
        .join(gri_7d_ago, on="country_code", how="left")
        .withColumn("gri_momentum_7d",
            when(col("gri_7d_ago").isNotNull(),
                col("gri") - col("gri_7d_ago")
            ).otherwise(lit(None))
        )
    )
except Exception:
    gri_today = gri_today.withColumn("gri_momentum_7d", lit(None).cast("double"))

# ============================================================
# STEP 6: Compute 90-day percentile rank and alert flags
# ============================================================

try:
    gri_90d_hist = (spark.read.table(GRI_OUTPUT_TABLE)
        .filter(col("event_date") >= expr(f"date_sub('{target_date_str}', 90)"))
        .select("country_code", "gri")
        .groupBy("country_code")
        .agg(
            avg("gri").alias("gri_mean_90d"),
            stddev("gri").alias("gri_std_90d"),
        )
    )
    gri_today = gri_today.join(gri_90d_hist, on="country_code", how="left")
    gri_today = gri_today.withColumn("gri_percentile_90d",
        when(col("gri_std_90d") > 0,
            # Approximate percentile using normal CDF proxy:
            # percentile = 50 + 50 * erf(zscore / sqrt(2))
            # Simplified: use gri_zscore_vs_90d normalized 0-100
            spark_round(
                50.0 + 50.0 * (col("gri") - col("gri_mean_90d")) /
                (col("gri_std_90d") * 1.96),
                1
            )
        ).otherwise(lit(50.0))
    )
except Exception:
    gri_today = (gri_today
        .withColumn("gri_percentile_90d", lit(50.0))
    )

# ============================================================
# STEP 7: Risk Regime Classification
# ============================================================

gri_today = (gri_today
    .withColumn("alert_flag",
        (col("gri") > 1.5) &
        (col("gri_momentum_7d") > 0.3)
    )
    .withColumn("risk_regime",
        when(col("gri") > 2.5, lit("CRISIS"))
        .when(
            (col("gri") >= 1.5) & (col("gri_momentum_7d") >= 0.0),
            lit("ELEVATED")
        )
        .when(
            (col("gri") > 1.0) & (col("gri_momentum_7d") < -0.3),
            lit("DECLINING")
        )
        .otherwise(lit("STABLE"))
    )
    .withColumn("_gold_timestamp", current_timestamp())
)

# ============================================================
# STEP 8: Round and write to Gold Delta table
# ============================================================

OUTPUT_COLS = [
    "country_code", "event_date",
    "tension_zscore", "bci_zscore", "tas",
    "gri", "gri_momentum_7d", "gri_percentile_90d",
    "alert_flag", "risk_regime",
    "_gold_timestamp",
]

gri_final = gri_today.select(OUTPUT_COLS)
gri_final = (gri_final
    .withColumn("gri",                spark_round("gri", 3))
    .withColumn("bci_zscore",         spark_round("bci_zscore", 3))
    .withColumn("gri_momentum_7d",    spark_round("gri_momentum_7d", 3))
    .withColumn("gri_percentile_90d", spark_round("gri_percentile_90d", 1))
)

(gri_final.write
    .format("delta")
    .mode("append")
    .option("mergeSchema", "false")
    .saveAsTable(GRI_OUTPUT_TABLE))

row_count = gri_final.count()
alert_count = gri_final.filter(col("alert_flag") == True).count()
crisis_count = gri_final.filter(col("risk_regime") == "CRISIS").count()
print(f"SUCCESS: GRI written for {target_date_str}")
print(f"  Countries scored: {row_count}")
print(f"  Alert flags raised: {alert_count}")
print(f"  Crisis-regime countries: {crisis_count}")
```

---

## V. The Validation Framework — Does the GRI Actually Work?

This section is more important than the build. **Building the GRI is easy. Knowing whether it works is hard.**

### The Core Validation Question

Does an elevated GRI, measured *before* a market event, predict that event? Or does the GRI simply respond to events that markets have already priced?

There are three possible relationships:
1. **Leading** — GRI rises before market prices move. This is the signal you want.
2. **Coincident** — GRI and prices move together. This is interesting but not tradeable.
3. **Lagging** — GRI rises after markets have already moved. This is elaborate noise.

The empirical test distinguishes them.

### Validation Dataset: What You Need

**Market targets (dependent variables):**
- EM FX spot rates (BRL/USD, TRY/USD, ZAR/USD, MXN/USD, INR/USD, COP/USD — start with 6)
- EM sovereign spreads (EMBI): country-specific CDS or EMBI spread
- Commodity prices where geographically relevant: WTI (Middle East GRI), Brent (Russia/OPEC GRI), wheat futures (Ukraine/Russia GRI)
- VIX as a global risk control variable

**Data sources:** FRED API (for USD pairs and some sovereign spreads), Yahoo Finance (for spot FX, commodities). Databricks can pull both via Python libraries.

**Minimum dataset:** 90 days of GRI history × 6 currencies. At 90 observations, you can run meaningful lag correlations, though statistical power is limited. The 180-day mark is when the analysis becomes reliable.

### Validation Test 1: Cross-Correlation Analysis (Rolling Lag)

For each country, compute the cross-correlation between GRI and the 5-day forward return of the local currency vs USD:

```python
# Pseudocode — run in Databricks notebook after joining GRI and FX data

from scipy.stats import pearsonr
import pandas as pd

def compute_lag_correlations(gri_series, fx_series, max_lag=20):
    """
    Compute Pearson correlation between GRI at t and FX return at t+lag
    for lag in range [0, max_lag].
    Returns dict: {lag: correlation, p_value}
    """
    results = {}
    for lag in range(0, max_lag + 1):
        gri_aligned   = gri_series[:-lag] if lag > 0 else gri_series
        fx_shifted     = fx_series[lag:]   if lag > 0 else fx_series
        if len(gri_aligned) < 30:
            continue
        corr, pval = pearsonr(gri_aligned, fx_shifted)
        results[lag] = {"correlation": corr, "p_value": pval}
    return results
```

**What you are looking for:**
- Correlation at lag=0 (coincident): expected ~0.2–0.4 for most EM currencies
- Correlation peaks at lag=5–15 (leading): this is signal. If the correlation is highest at lag 10, GRI is a 10-day leading indicator for FX moves.
- Correlation decays at lag=20+ (the signal fades)

**Threshold for "signal found":** Peak correlation > 0.25 AND p-value < 0.05 at a lag between 3 and 20 days. Anything shorter than 3 days is probably coincident (news and FX moving together intraday). Anything past 20 days loses practical investment relevance.

### Validation Test 2: Alert Flag Backtesting

For every date in the last 90 days where `alert_flag = True` for a given country:
- What was the 5-day, 10-day, and 20-day forward FX return?
- Compare to the distribution of FX returns on non-alert days for the same country.

```sql
-- Alert flag backtest: do alert days predict larger FX moves?
SELECT
    g.country_code,
    g.event_date,
    g.gri,
    g.alert_flag,
    g.risk_regime,
    -- Join to FX returns (requires FX table in Databricks)
    fx.fx_return_5d,
    fx.fx_return_10d,
    fx.fx_return_20d
FROM geopolitics.gold.country_gri g
LEFT JOIN market_data.fx_returns fx
    ON g.country_code = fx.country_code
    AND g.event_date = fx.event_date
WHERE g.event_date >= current_date() - INTERVAL 90 DAYS
ORDER BY g.event_date DESC;
```

Then compute:
- Mean absolute FX return on alert days vs non-alert days
- The t-statistic for the difference

**Expected result if GRI has signal:** Alert-day 10-day forward absolute FX returns are meaningfully larger (e.g., 1.5–2× the non-alert baseline). If the difference is less than 20%, the signal is weak.

### Validation Test 3: Crisis-Regime Precision

For every country that entered `risk_regime = CRISIS` (GRI > 2.5) in the last 90 days: did a recognizable geopolitical event occur within 30 days? Manual verification for initial calibration.

This is a precision test: what fraction of CRISIS flags correspond to real events? Low precision means the model is too sensitive — lower the CRISIS threshold or tighten the filter.

### Validation Failure Modes — and What to Do

| Failure | Likely Cause | Fix |
|---|---|---|
| GRI is lagging (correlates best at lag=0 or negative lag) | Events are already in news prices by the time GDELT processes them | Shift to real-time GKG (15-minute feed) rather than daily aggregation |
| Alert precision too low (many alerts, few events) | Thresholds too loose OR weights favor high-volatility source | Raise GRI threshold for alert_flag to 2.0 or tighten momentum to > 0.5 |
| Low correlation with target currencies but high with commodities | GRI is picking up supply-side geopolitics but not EM political risk | Reweight: increase bilateral BCI weight, decrease tension_zscore weight |
| No significant correlation anywhere | 90-day sample too short OR GDELT coverage is too thin for target countries | Wait for 180-day history; add ACLED or news API data for thin-coverage countries |

---

## VI. Connecting to the Investment Framework

The GRI is the analytical translation of everything built across Lessons 1–293 into a single operational output. Specifically:

### From the Core Curriculum

**Lesson 9 (EM Political Risk):** The GRI makes Lesson 9's qualitative framework quantitative. The regime typology — competitive authoritarianism, fragile democracy, electoral uncertainty — maps to elevated ELECTIONS + PROTEST theme signals AND elevated BCI when the country has active bilateral disputes. The GRI should spike predictably around these political transition events.

**Lesson 75 (Currency Crises Anatomy):** Currency crises don't arrive suddenly — they arrive after a period of elevated geopolitical and economic stress that markets underprice. The GRI's 90-day momentum captures exactly this slow-building pressure. A currency crisis preceded by 60 days of GRI > 1.5 with rising momentum is structurally different from one that appears without warning. The GRI helps distinguish them prospectively.

**Lesson 4 (Energy Geopolitics):** When the GRI for Middle East countries spikes alongside ENERGY_OIL theme elevation, the historical pattern is a WTI supply disruption premium of 3–8% within 2–4 weeks. The GRI is not predicting this — it is measuring the geopolitical precondition that makes it more likely.

### The Investment Output: Signal-to-Position Logic

Once the GRI validates, the signal-to-position logic is:

```
IF GRI(country) > 1.5 AND GRI_momentum_7d > 0.3:
    → EM FX: reduce local currency exposure, increase USD
    → Sovereign spreads: expect widening; reduce duration in that country's bonds
    → Equities: reduce geographic tilt toward that country; rotate to USD-denominated assets

IF GRI(country) < -0.5 AND GRI_momentum_7d < -0.3:
    → EM FX: opportunistic local currency exposure as geopolitical risk premium unwinds
    → Sovereign spreads: expect tightening; add duration if credit quality supports it
    → Equities: EM recovery play in that country

IF ENERGY_OIL theme_zscore < -1.5 AND Middle East GRI > 1.5:
    → Commodities: long WTI/Brent with 4-week horizon
    → FX: long USD, long CHF as safe haven; short EUR if European energy exposure is high
```

**These are hypotheses, not rules.** The validation framework turns them into validated rules — or disproves them.

---

## VII. The Gold Layer DAG: Completing the Workflow Architecture

```yaml
# Complete gdelt_daily_pipeline workflow after Gold Layer added
Tasks:
  # Bronze Layer (parallel)
  - task_key: gdelt_events_bronze
    schedule: daily @ 2:00 UTC
    ...
  - task_key: gdelt_gkg_bronze
    schedule: daily @ 2:00 UTC
    ...

  # Silver Layer (parallel, after respective Bronze)
  - task_key: gdelt_silver_country_daily
    depends_on: [gdelt_events_bronze]
  - task_key: gdelt_silver_country_pair
    depends_on: [gdelt_silver_country_daily]
  - task_key: gdelt_silver_theme_daily
    depends_on: [gdelt_gkg_bronze]

  # Validation gate (all Silver must complete)
  - task_key: gdelt_silver_validate
    depends_on:
      - gdelt_silver_country_daily
      - gdelt_silver_country_pair
      - gdelt_silver_theme_daily

  # Gold Layer (after Silver validation passes)
  - task_key: gdelt_gold_gri
    notebook_path: /Workflows/gold/gdelt_gold_gri
    depends_on: [gdelt_silver_validate]
    cluster: job_cluster_medium
    timeout_seconds: 1800

  # GRI Validation (after Gold writes)
  - task_key: gdelt_gold_validate
    depends_on: [gdelt_gold_gri]
    # Runs the validation queries; fails job if zero CRISIS/ELEVATED countries appear
    # (indicates upstream data failure, not a quiet day)
```

**Estimated runtime after all Silver tasks complete:** 15–25 minutes. The GRI computation itself is fast; the lag correlation joins are the bottleneck.

---

## VIII. Databricks Build Instructions — Bolo's Checklist for This Lesson

1. **Create the Gold schema** if it doesn't exist: `CREATE SCHEMA IF NOT EXISTS geopolitics.gold MANAGED LOCATION 'abfss://...'`

2. **Deploy `gdelt_gold_gri.py`** as a Databricks Notebook at `/Workflows/gold/gdelt_gold_gri`.

3. **First run:** Execute manually for yesterday's date. The 90-day baseline reads will fail gracefully (table exists but is empty on first run — the `try/except` handles this). First-run GRI will have `gri_momentum_7d = NULL` and `gri_percentile_90d = 50.0` for all countries — this is correct and expected.

4. **Run the daily pipeline end-to-end** with the Gold task added. Confirm the DAG runs in the correct order: Bronze → Silver (parallel) → Silver validation → Gold.

5. **The first useful validation is at Day 30.** Until then: run the build daily, inspect the GRI output table manually for sense-checks (known high-risk countries should have higher GRI; known stable periods should show GRI near zero), but do not draw investment conclusions.

6. **At Day 30:** Run the cross-correlation analysis (Validation Test 1) for BRL/USD and TRY/USD — the two most GRI-sensitive currencies in the sample. If correlation > 0.25 at any lag between 3–20 days with p < 0.05, the signal is present.

7. **At Day 90:** Full validation battery. The lag analysis becomes meaningful at this sample size. The alert flag backtest requires enough alerts to compute means — at 90 days with 15–20 countries tracked, you should have 30–50 alert-day observations to work with.

**Time estimate for deployment:** 1–2 hours for the notebook and DAG update. The validation analysis at Day 30 is a 2–3 hour analytical session.

---

## IX. Investment Implications Summary

| GRI Condition | Asset Class | Directional View | Horizon |
|---|---|---|---|
| Country GRI > 1.5, momentum > 0.3 | EM local currency (that country) | Reduce / short | 2–4 weeks |
| Country GRI > 1.5, momentum > 0.3 | Sovereign spreads (that country) | Widening bias | 2–8 weeks |
| Country GRI declining from > 2 to < 1.5 | EM FX (that country) | Opportunistic long | 3–6 weeks |
| CRISIS regime (GRI > 2.5) | USD, CHF, gold | Safe haven long | 2–6 weeks |
| Middle East GRI > 1.5 AND ENERGY_OIL tone_zscore < -1.5 | WTI, Brent | Long | 2–4 weeks |
| EM ELECTIONS + PROTEST co-elevation with GRI > 1.5 | EM FX of affected country | Short | 2–6 weeks |

---

## Key Concepts Covered

1. **The GRI as a composite Z-score** — why normalization to each country's own baseline makes cross-country comparisons meaningful; why absolute score levels are not comparable across time periods
2. **The 45/35/20 weighting prior** — the precision hierarchy of the three Silver signals and why bilateral BCI carries more weight than country-level tension despite being narrower
3. **Bilateral Conflict Intensity (BCI)** — the MAX-over-pairs construction; why the escalation_flag multiplier and the MAX operator both encode the same logic (worst-case dominance)
4. **Theme Attribution Score (TAS) — the global proxy** — why starting with a global military attention proxy is acceptable and when to graduate to the country-specific theme table
5. **The three validation tests** — cross-correlation lag analysis, alert flag backtesting, and crisis-regime precision; what constitutes "signal found" vs "noise"
6. **Validation failure modes** — how to diagnose and fix a non-performing GRI rather than accepting it as the ground truth
7. **Signal-to-position logic** — how GRI translates to directional views on EM FX, sovereign spreads, and commodity exposures; the explicit conditions that trigger each view

---

## Reflection Questions

1. **The weighting question:** The 45/35/20 weighting is a calibrated prior, not a derived result. What is the systematic method for finding the optimal weights? Specifically: if you run the validation framework and find the GRI performs best for FX prediction when the weight on bilateral BCI is 50% (not 35%), how do you update the model without overfitting to the validation period? What technique prevents data-snooping on the 90-day sample?

2. **The TAS simplification:** This lesson uses global MILITARY attention_zscore as the Theme Attribution Score for all countries — a deliberate simplification. In what scenario would this simplification produce a materially wrong GRI? Describe a specific country, date, and mechanism where the global military proxy fails to capture the country-specific geopolitical theme — and what the correct TAS would be in that case.

3. **The lag question (empirical):** Suppose at Day 30 you run Validation Test 1 and find the following for Brazil: correlation with BRL/USD at lag=0 is 0.35, at lag=5 is 0.28, at lag=10 is 0.18, at lag=15 is 0.09. Is the GRI a leading indicator for BRL/USD, a coincident indicator, or neither? What does this pattern tell you about the information efficiency of the BRL market with respect to Brazilian geopolitical risk — and what investment rule would you derive from it?

---

## Questions for Next Session

- **Lesson 295:** Lag Analysis in Practice — empirically validating the GRI's lead time using FRED FX data in Databricks. This is the quantitative finance session: Granger causality, rolling correlation windows, and the correct interpretation of lead-lag structures in financial data. The lesson delivers the actual Python/PySpark code for the full validation battery.
- **Spaced repetition:** Review Lesson 9 (EM Political Risk) before Lesson 295. The GRI should, if it is working, predict exactly the scenarios Lesson 9 described qualitatively: competitive authoritarian crises, contested elections, bilateral conflict escalations driving capital outflows. The validation will tell you whether the quantitative model captures the qualitative framework.
- **Build milestone:** After this lesson's deployment, you have a complete Bronze-Silver-Gold pipeline architecture. The platform is structurally complete. What remains is validation and productization. This is a significant milestone — the 3-month clock is on track.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 294 of an ongoing curriculum | September 3, 2026*
