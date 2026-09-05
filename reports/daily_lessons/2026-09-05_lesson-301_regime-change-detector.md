# Lesson 301 — The Regime Change Detector: Identifying Structural Shifts in Geopolitical Relationships

**Date:** 2026-09-05
**Session Type:** Daily Lesson
**Lesson Number:** 301 / ongoing
**Topic:** Databricks Intelligence Module — Regime Change Detector (RCD)
**Curriculum Arc:** Databricks Build Module — Phase 2, Lesson 2 (data → signal → intelligence → positions)

---

## Opening Question

*The GRI flagged Iran at an elevated score for the entire period from 2018 through 2024. It also flagged Ukraine in February 2022 — briefly — before the invasion made every score irrelevant.*

Here is the question that opens Lesson 301:

**"If both Iran and Ukraine showed elevated GRI scores before their respective crises, why would a position taken on Iran's elevated score in 2018 have very different investment characteristics than a position taken on Ukraine's elevated score in January 2022?"**

The answer is not about the magnitude of the score. It is about whether the elevated score represents a **new regime** or a **continuation of a known regime**. Iran's elevation in 2018 was already priced — the market had baked in Iran risk for years. Ukraine in January 2022 was a structural shift arriving. The Regime Change Detector's job is to distinguish these two cases, because they require entirely different investment responses.

---

## I. What Is a Geopolitical Regime?

In statistical terms, a **regime** is a period during which a system's generating process remains stable. When the generating process changes — structurally, not temporarily — a regime transition occurs.

In geopolitical terms:
- A **spike** is a short-term elevation followed by mean reversion (a protest, a skirmish, a diplomatic incident that resolves)
- A **regime shift** is a structural change in the underlying geopolitical relationship that persists for months to years and does not revert to the previous baseline

**Historical examples of regime shifts (not spikes):**

| Event | Date | What changed structurally |
|---|---|---|
| Russia's annexation of Crimea | March 2014 | Russia–West relationship permanently reset; sanctions became structural |
| US-China trade war launch | January 2018 | Bilateral economic relationship entered persistent confrontation mode |
| Saudi-Iran proxy war escalation | September 2019 (Abqaiq attack) | Gulf security architecture structurally degraded |
| COVID travel restrictions | March 2020 | Global supply chain vulnerability exposed; permanent restructuring began |
| Russia's full invasion of Ukraine | February 2022 | European security architecture restructured; energy regime shift |
| US semiconductor export controls on China | October 2022 | Technology decoupling became structurally locked |

**The investment implication of correctly identifying a regime shift (vs a spike):**
- A **spike** warrants a short-duration tactical position (weeks to 2 months)
- A **regime shift** warrants a structural, long-horizon position (6–18+ months) — the kind the PROJECT_FOUNDATION thesis says is our actual edge

---

## II. Why the GRI Alone Is Insufficient

The GRI measures geopolitical risk intensity day-by-day. It is a **level signal**. What it does not measure is whether a given level represents:

1. A short-term spike around a normative baseline (revertible)
2. A new, higher baseline (structural — a regime shift has occurred)
3. A transition — the score is rising through what will become a new regime

These distinctions cannot be made from a single GRI reading. They require:
- **Time-series pattern recognition** — is the GRI trending or oscillating?
- **Changepoint detection** — is there a statistical break in the time series?
- **Persistence testing** — has the new elevated level sustained for long enough to constitute a regime?

The Regime Change Detector (RCD) applies exactly these three techniques.

---

## III. The RCD Architecture: Three Layers

### Layer 1 — Rolling Mean Comparison (Fast Signal)

The simplest test: has the 30-day rolling mean of the GRI broken above the 90-day rolling mean by a statistically significant margin, and has that break persisted for at least 10 trading days?

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window

w30 = Window.partitionBy("country").orderBy("date").rowsBetween(-30, 0)
w90 = Window.partitionBy("country").orderBy("date").rowsBetween(-90, 0)

df_regime = df_gri.withColumn(
    "gri_mean_30d", F.avg("gri_score").over(w30)
).withColumn(
    "gri_mean_90d", F.avg("gri_score").over(w90)
).withColumn(
    "gri_std_90d", F.stddev("gri_score").over(w90)
).withColumn(
    "regime_break_flag",
    F.when(
        (F.col("gri_mean_30d") - F.col("gri_mean_90d")) >
        (1.0 * F.col("gri_std_90d")),  # 1 std dev above 90d mean
        True
    ).otherwise(False)
)
```

This fires a **candidate signal**. It does not confirm a regime shift — it flags a candidate for deeper evaluation.

### Layer 2 — Changepoint Detection (Confirmation Signal)

A changepoint is the date at which a time series' statistical properties change. The PELT (Pruned Exact Linear Time) algorithm is the industry standard for offline changepoint detection. For streaming/daily use, the BOCPD (Bayesian Online Changepoint Detection) algorithm detects changes in near real-time.

**Databricks implementation using the `ruptures` library:**

```python
import ruptures as rpt
import numpy as np
import pandas as pd

def detect_changepoints_pandas(pdf: pd.DataFrame, min_segment_length: int = 30) -> pd.DataFrame:
    """
    Apply PELT changepoint detection to a country's GRI time series.
    Returns the DataFrame with a changepoint_detected column.
    """
    gri_array = pdf["gri_score"].values
    
    if len(gri_array) < min_segment_length * 2:
        pdf["changepoint_detected"] = False
        pdf["days_since_changepoint"] = None
        return pdf
    
    # PELT with RBF cost function (sensitive to mean + variance changes)
    algo = rpt.Pelt(model="rbf", min_size=min_segment_length).fit(gri_array)
    changepoints = algo.predict(pen=10)  # pen=10 is the regularization parameter
    
    # Convert changepoint indices to dates
    cp_dates = pdf["date"].iloc[[cp - 1 for cp in changepoints if cp < len(pdf)]].values
    
    pdf["changepoint_detected"] = pdf["date"].isin(cp_dates)
    
    # Days since most recent changepoint
    pdf = pdf.sort_values("date")
    last_cp = None
    days_since = []
    for _, row in pdf.iterrows():
        if row["changepoint_detected"]:
            last_cp = row["date"]
        days_since.append((row["date"] - last_cp).days if last_cp else None)
    pdf["days_since_changepoint"] = days_since
    
    return pdf

# Apply via Spark pandas UDF
from pyspark.sql.functions import pandas_udf, PandasUDFType
# Apply per-country using groupBy + applyInPandas
df_changepoints = df_gri.groupBy("country").applyInPandas(
    detect_changepoints_pandas,
    schema=df_gri.schema.add("changepoint_detected", "boolean").add("days_since_changepoint", "integer")
)
```

**Key parameter: `pen=10`**
The penalty parameter controls sensitivity. Lower values detect more changepoints (risk: false positives on temporary spikes). Higher values require more sustained change (risk: late detection). For geopolitical regimes, pen=10 is empirically appropriate — requires approximately 3 weeks of sustained deviation to confirm.

### Layer 3 — Persistence Filter (Regime Confirmation)

A changepoint is detected. The candidate regime has been flagged. Now: has the new level **persisted** long enough to constitute a confirmed regime shift?

```python
# Regime confirmed when:
# 1. Changepoint detected within last 90 days
# 2. GRI has remained elevated (>70th historical percentile) since changepoint
# 3. No mean reversion to pre-changepoint level

REGIME_CONFIRMATION_DAYS = 21  # 3 weeks of sustained elevation

df_confirmed = df_changepoints.withColumn(
    "regime_confirmed",
    F.when(
        (F.col("days_since_changepoint").between(1, 90)) &
        (F.col("gri_score") > F.col("gri_pct70_historical")) &
        (F.col("gri_mean_30d") > F.col("gri_pre_changepoint_mean") * 1.15),  # 15% above prior regime
        True
    ).otherwise(False)
).withColumn(
    "regime_type",
    F.when(F.col("regime_confirmed") & (F.col("gri_score") > F.col("gri_pct85_historical")), "HARD_REGIME_SHIFT")
     .when(F.col("regime_confirmed"), "SOFT_REGIME_SHIFT")
     .when(F.col("regime_break_flag"), "CANDIDATE_ELEVATED")
     .otherwise("NORMAL")
)
```

---

## IV. The Output Schema: `gold_regime_detection`

```python
schema = StructType([
    StructField("date", DateType()),
    StructField("country", StringType()),
    StructField("gri_score", DoubleType()),
    StructField("regime_type", StringType()),         # NORMAL / CANDIDATE_ELEVATED / SOFT_REGIME_SHIFT / HARD_REGIME_SHIFT
    StructField("regime_start_date", DateType()),      # When the current regime began
    StructField("days_in_regime", IntegerType()),      # Duration of current regime
    StructField("pre_regime_gri_mean", DoubleType()),  # Baseline GRI before shift
    StructField("regime_magnitude", DoubleType()),     # % elevation above prior regime baseline
    StructField("affected_commodities", ArrayType(StringType())),  # CPM modules that should activate structural mode
    StructField("investment_horizon_flag", StringType()),  # "tactical" / "structural" / "monitor"
    StructField("pipeline_run_ts", TimestampType())
])
```

---

## V. Connecting the RCD to the CPM (The Critical Integration)

When the RCD detects a confirmed regime shift for a country, it sends a flag to the CPM that changes how that country's GRI input is weighted:

**In spike mode (no regime shift):**
- CPM uses the current-day GRI score
- Position horizon: tactical (weeks)
- CPS normalization: uses full 180-day window

**In regime shift mode (SOFT or HARD confirmed):**
- CPM uses the **regime-adjusted GRI** — the delta above the new regime baseline, not the historical baseline
- Position horizon: structural (6–18 months)
- CPS normalization: uses only post-regime-shift data (new baseline)
- Morning note flags: "STRUCTURAL MODE — [country] regime shift confirmed [date]"

This prevents the CPM from under-counting persistent risk (as it would if it kept normalizing against a pre-shift baseline) and over-counting tactical spikes (as it would if it applied structural weights to every elevation).

---

## VI. Calibration — The Two Failure Modes to Engineer Against

**Failure Mode 1: False positive (detecting a regime shift that isn't one)**
- Example: COVID lockdown GRI spike in March 2020 briefly looks like a regime shift for every country simultaneously, but it reverts within 12 months
- Defense: Require the regime shift to be country-specific or regionally contained, not universal. A universal spike (>50% of tracked countries simultaneously elevated) is more likely a global shock than a structural bilateral shift

**Failure Mode 2: False negative (missing a real regime shift until it's fully priced)**
- Example: Russia-Ukraine escalation in late 2021 — the signs were present 6–8 weeks before February 24, but a persistence requirement of 21 days was not satisfied
- Defense: For the highest-supply-weight countries (Russia, China, Saudi Arabia, Ukraine), reduce the persistence requirement to 14 days. The asymmetric cost of missing a true regime shift in a high-weight country justifies higher sensitivity

```python
HIGH_PRIORITY_COUNTRIES = {
    "Russia", "China", "Saudi Arabia", "Ukraine", "Iran", "United States"
}

REGIME_CONFIRMATION_DAYS_MAP = {
    country: 14 if country in HIGH_PRIORITY_COUNTRIES else 21
    for country in ALL_TRACKED_COUNTRIES
}
```

---

## VII. Historical Validation: Did the RCD Fire Before the Market Priced In the Shift?

The RCD's value proposition is early detection — firing before the commodity or equity repricing, not after. The backtesting framework for the RCD:

1. Reconstruct GDELT-based GRI for 2018–2024 (same as CPM backtest)
2. Apply RCD algorithm with current parameters
3. Compare RCD confirmation date vs. commodity/equity repricing date
4. **Success criterion:** RCD confirms regime shift ≥7 trading days before median analyst consensus identifies the structural shift as durable

Known historical anchors for validation:
- US-China trade war (Jan–Mar 2018): Did RCD fire on China by late January?
- Saudi Abqaiq attack (Sep 2019): Did RCD fire on Saudi Arabia before oil re-priced?
- Ukraine escalation (Nov 2021–Feb 2022): Did RCD fire before February 24?
- US semiconductor export controls (Oct 2022): Did RCD fire on China tech supply chain?

---

## Investment Implications

The Regime Change Detector directly addresses the core investment thesis: **most market participants react to geopolitics emotionally, late, and without a structural framework.** The RCD is the mechanism that forces structural classification before a position is taken.

**Investment decision tree with RCD:**

```
GRI elevated for [country]
        │
        ├─ RCD: NORMAL or CANDIDATE → Tactical position only (≤8 weeks), small size
        │
        ├─ RCD: SOFT_REGIME_SHIFT → Structural position initiation (6–12 month horizon)
        │         Apply to commodity positions, EM FX, sector equities
        │
        └─ RCD: HARD_REGIME_SHIFT → Maximum structural position
                  Review entire portfolio for exposure to affected country's supply chains
                  Consider hedges: OTM call options on affected commodities
```

**Expected alpha source:** The gap between RCD confirmation (typically 3–5 weeks into a genuine regime shift) and market consensus recognition (typically 8–12 weeks, often after the commodity has already moved significantly). That 3–8 week window is where the patient investor with a structural framework earns the position.

---

## Databricks Angle

**Build priority for this week (following CPM foundations):**

1. **Notebook 1:** `silver_gri_regime_rolling_means` — computes 30d/90d rolling means and preliminary break flags. ~30 lines PySpark.
2. **Notebook 2:** `silver_gri_changepoint_detection` — applies PELT via `ruptures` library using `groupBy().applyInPandas()`. Requires installing `ruptures` as a cluster library in Databricks (`pip install ruptures`). ~60 lines.
3. **Notebook 3:** `gold_regime_detection` — persistence filter, regime classification, affected_commodities mapping, investment_horizon_flag. ~50 lines.
4. **Integration:** Modify `gold_commodity_pressure_signals` to consume `gold_regime_detection` for regime-aware CPS weighting.

**Datasets needed:**
- `gold_gri_scores` (already exists from Phase 1)
- `supply_geography_weights` (new in CPM build)
- No new external data sources required — the RCD operates entirely on GRI time series

**Total estimated build:** 2 Databricks notebooks plus CPM integration. This is a 1.5-day build for Bolo running in parallel with the CPM notebooks.

**Key dependency to resolve:** The `ruptures` library must be added to the Databricks cluster's library configuration. In the Databricks UI: Compute → [cluster] → Libraries → Install New → PyPI → `ruptures`. Confirm version compatibility with the cluster's Python version before the build session.

---

## Questions for Next Session

1. **The PELT algorithm is applied offline (it uses the full historical window). What happens when you run it daily on a new data point — does the changepoint date for an existing regime shift stay stable, or does it drift backward as more data accumulates? Why does this matter for position timing?**

2. **The RCD uses a 15% threshold above the pre-shift baseline to confirm a regime shift. Is this threshold symmetric — should a 15% *decrease* in GRI for a previously elevated country confirm a regime *exit*, or should the exit threshold be different from the entry threshold? What does this imply for position unwinding?**

3. **The backtest above focuses on 2018–2024. What is the most important regime shift that occurred before 2018 that would have been ideal validation data — and what data availability constraints prevent you from using it?**

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 301 delivered 2026-09-05*
