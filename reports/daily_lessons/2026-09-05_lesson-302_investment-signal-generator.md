# Lesson 302 — The Investment Signal Generator: Where Analysis Becomes Position

**Date:** 2026-09-05
**Session Type:** Daily Lesson
**Lesson Number:** 302 / ongoing
**Topic:** Databricks Intelligence Module — Investment Signal Generator (ISG)
**Curriculum Arc:** Databricks Build Module — Phase 2, Lesson 3 (the capstone — GRI + CPM + RCD → investment signal)

---

## Opening Question

*The GRI for Russia is at 87 (HARD_REGIME_SHIFT confirmed since November 2021). The CPM is generating a CPS of 0.74 for Brent crude. The RCD says we are 42 days into a confirmed hard regime. The morning note has flagged this for three weeks.*

**"At what point does analysis become a fiduciary failure if you haven't acted on it?"**

This is not a rhetorical question — it is the exact problem the Investment Signal Generator (ISG) is designed to solve. The GRI, CPM, and RCD are measurement and classification engines. They tell you *what is happening* and *how serious it is*. The ISG tells you *what to do about it* — with an explicit direction, a defined size, a target horizon, and a written falsification condition that will close the position.

Without the ISG, you have a very sophisticated journalism operation. With it, you have an investment process.

---

## I. What the ISG Is (and Is Not)

The ISG is the **rules-based translation layer** between geopolitical intelligence and portfolio action. It is not:

- A model that predicts prices
- An optimization engine that runs mean-variance on expected returns
- A black box

It is a **structured decision tree** that converts well-defined input states (GRI level, CPM signal, RCD regime type, macro context) into a small set of standardized outputs: **signal type, asset class, direction, size tier, horizon, and kill switch**.

The ISG enforces the investment thesis from PROJECT_FOUNDATION directly:

> *"Every recommendation has an explicit thesis, a defined timeframe, and a falsifiable condition for being wrong."*

Every signal the ISG produces is logged automatically to `reports/investment_log.md`. There is no signal without a log entry.

---

## II. The Signal Taxonomy

The ISG produces four signal types, in increasing order of conviction:

| Signal Type | Definition | Typical Position Size | Minimum Horizon |
|---|---|---|---|
| **WATCH** | Elevated conditions present; no confirmed regime; monitor closely | None | N/A |
| **TACTICAL** | Elevated conditions with candidate signal; spike likely, not structural | Small (0.5–1% of portfolio) | 4–8 weeks |
| **STRUCTURAL** | Confirmed regime shift; full thesis engaged | Standard (2–4% of portfolio) | 6–18 months |
| **CONVICTION** | Hard regime shift; multiple modules confirming; macro alignment | Large (4–6% of portfolio) | 12–24 months |

**The size tiers are default guidelines, not absolute rules.** Bolo makes the final call on position sizing. The ISG's job is to compute and surface the recommended tier — not to execute.

---

## III. The Signal Logic Tree

```
INPUT STATE (from GRI + CPM + RCD daily run):
  ├── gri_score: [0–100]
  ├── cps: [0.0–1.0]
  ├── regime_type: [NORMAL / CANDIDATE_ELEVATED / SOFT_REGIME_SHIFT / HARD_REGIME_SHIFT]
  └── days_in_regime: [0–∞]

DECISION TREE:

IF regime_type == NORMAL:
    → WATCH (no signal)

IF regime_type == CANDIDATE_ELEVATED AND cps >= 0.45:
    → TACTICAL signal
       Asset: top CPS commodity for that country
       Direction: LONG commodity / SHORT affected EM equity (country-specific)
       Size: 0.5%
       Horizon: 6 weeks
       Kill switch: "GRI reverts below 90d mean for 5 consecutive days"

IF regime_type == SOFT_REGIME_SHIFT AND cps >= 0.55 AND days_in_regime >= 14:
    → STRUCTURAL signal
       Asset: CPS top commodity + EM FX short (affected country's currency)
       Direction: LONG commodity, SHORT EM FX
       Size: 2.5%
       Horizon: 9 months
       Kill switch: "RCD regime exits (30d mean reverts to pre-shift baseline)"
                    OR "CPS falls below 0.35 for 10 consecutive days"

IF regime_type == HARD_REGIME_SHIFT AND cps >= 0.65 AND days_in_regime >= 14:
    → CONVICTION signal
       Asset: CPS top commodity + sector equities + EM FX + sovereign spread
       Direction: Per CPS output (typically LONG commodity, LONG defense, SHORT EM FX)
       Size: 4–5%
       Horizon: 15 months
       Kill switch: "Diplomatic resolution confirmed by UN/multilateral body"
                    OR "CPS falls below 0.40 for 15 consecutive days"
                    OR "Macro regime shift (Fed rate cut cycle begins; risk-on dominant)"
```

---

## IV. The ISG Schema and Databricks Implementation

### Output Table: `gold_investment_signals`

```python
from pyspark.sql.types import *

isg_schema = StructType([
    StructField("signal_date", DateType()),
    StructField("country", StringType()),
    StructField("signal_type", StringType()),           # WATCH / TACTICAL / STRUCTURAL / CONVICTION
    StructField("signal_id", StringType()),             # UUID for audit trail
    StructField("gri_score_at_signal", DoubleType()),
    StructField("cps_at_signal", DoubleType()),
    StructField("regime_type_at_signal", StringType()),
    StructField("days_in_regime_at_signal", IntegerType()),
    StructField("target_asset_class", StringType()),    # "commodity:brent" / "fx:RUB" / "equity:defense"
    StructField("direction", StringType()),             # LONG / SHORT
    StructField("size_tier", StringType()),             # "SMALL" / "STANDARD" / "LARGE"
    StructField("recommended_size_pct", DoubleType()),  # e.g. 2.5
    StructField("target_horizon_months", IntegerType()),
    StructField("kill_switch_condition", StringType()),
    StructField("thesis_text", StringType()),           # Autogenerated plain-language thesis
    StructField("is_active", BooleanType()),            # False when kill switch triggered
    StructField("closed_date", DateType()),             # When position closed
    StructField("close_reason", StringType()),          # Kill switch condition that triggered
    StructField("pipeline_run_ts", TimestampType())
])
```

### Core ISG Notebook (PySpark)

```python
from pyspark.sql import functions as F
from pyspark.sql.window import Window
import uuid

# Read upstream intelligence tables
df_gri = spark.table("gold.gri_scores")
df_cps = spark.table("gold.commodity_pressure_signals")
df_rcd = spark.table("gold.regime_detection")

# Join on latest date
latest_date = df_rcd.agg(F.max("date")).collect()[0][0]

df_inputs = (
    df_rcd.filter(F.col("date") == latest_date)
    .join(
        df_cps.filter(F.col("date") == latest_date)
              .select("country", "cps", "primary_commodity", "direction"),
        on="country", how="left"
    )
    .join(
        df_gri.filter(F.col("date") == latest_date)
              .select("country", "gri_score"),
        on="country", how="left"
    )
)

# Signal generation UDF
def generate_signal(regime_type, cps, days_in_regime, country, primary_commodity, direction):
    """Core ISG logic — maps input state to signal type and parameters."""
    
    if regime_type == "NORMAL" or cps is None:
        return ("WATCH", None, None, None, None, None, None)
    
    if regime_type == "CANDIDATE_ELEVATED" and cps >= 0.45:
        thesis = (f"Elevated geopolitical risk in {country} (CANDIDATE) "
                  f"with CPS {cps:.2f} on {primary_commodity}. "
                  f"Tactical position: {direction} {primary_commodity} for 6 weeks. "
                  f"Spike-mode position — size small, discipline tight.")
        return ("TACTICAL", f"commodity:{primary_commodity}", direction, "SMALL", 0.5, 6,
                "GRI reverts below 90d mean for 5 consecutive days")
    
    if regime_type == "SOFT_REGIME_SHIFT" and cps >= 0.55 and days_in_regime >= 14:
        thesis = (f"Confirmed SOFT regime shift in {country} (day {days_in_regime}). "
                  f"CPS: {cps:.2f}. Structural {direction} on {primary_commodity} "
                  f"and SHORT {country} FX. 9-month horizon.")
        return ("STRUCTURAL", f"commodity:{primary_commodity};fx:{country}", direction,
                "STANDARD", 2.5, 9, "RCD regime exits OR CPS < 0.35 for 10 days")
    
    if regime_type == "HARD_REGIME_SHIFT" and cps >= 0.65 and days_in_regime >= 14:
        thesis = (f"HARD regime shift confirmed in {country} (day {days_in_regime}). "
                  f"CPS: {cps:.2f}. Maximum conviction: {direction} {primary_commodity}, "
                  f"defense sector, SHORT {country} FX and sovereign. 15-month horizon.")
        return ("CONVICTION", f"commodity:{primary_commodity};fx:{country};equity:defense",
                direction, "LARGE", 4.5, 15,
                "Diplomatic resolution OR CPS < 0.40 for 15 days OR macro regime shift")
    
    return ("WATCH", None, None, None, None, None, None)

# Apply as pandas UDF
from pyspark.sql.functions import struct, col

@F.udf(returnType=StructType([
    StructField("signal_type", StringType()),
    StructField("target_asset_class", StringType()),
    StructField("direction", StringType()),
    StructField("size_tier", StringType()),
    StructField("recommended_size_pct", DoubleType()),
    StructField("target_horizon_months", IntegerType()),
    StructField("kill_switch_condition", StringType()),
]))
def isg_udf(regime_type, cps, days_in_regime, country, primary_commodity, direction):
    result = generate_signal(regime_type, cps, days_in_regime, country, primary_commodity, direction)
    return result

df_signals = df_inputs.withColumn(
    "signal_output",
    isg_udf(
        F.col("regime_type"),
        F.col("cps"),
        F.col("days_in_regime"),
        F.col("country"),
        F.col("primary_commodity"),
        F.col("direction")
    )
).select(
    F.lit(latest_date).alias("signal_date"),
    F.col("country"),
    F.col("signal_output.signal_type"),
    F.expr("uuid()").alias("signal_id"),
    F.col("gri_score").alias("gri_score_at_signal"),
    F.col("cps").alias("cps_at_signal"),
    F.col("regime_type").alias("regime_type_at_signal"),
    F.col("days_in_regime").alias("days_in_regime_at_signal"),
    F.col("signal_output.target_asset_class"),
    F.col("signal_output.direction"),
    F.col("signal_output.size_tier"),
    F.col("signal_output.recommended_size_pct"),
    F.col("signal_output.target_horizon_months"),
    F.col("signal_output.kill_switch_condition"),
    F.lit(True).alias("is_active"),
    F.lit(None).cast("date").alias("closed_date"),
    F.lit(None).cast("string").alias("close_reason"),
    F.current_timestamp().alias("pipeline_run_ts")
).filter(F.col("signal_type") != "WATCH")

# Append to gold table (don't overwrite — every signal is permanent history)
df_signals.write.mode("append").saveAsTable("gold.investment_signals")
```

---

## V. The Kill Switch Monitor

A signal without a kill switch is a thesis without an exit condition — which is not a thesis, it is a hope. The Kill Switch Monitor runs daily alongside the ISG and closes positions automatically when conditions are met.

```python
# Kill Switch Monitor — runs after ISG daily
df_active_signals = spark.table("gold.investment_signals").filter(F.col("is_active") == True)

# For each active signal, evaluate kill switch against today's data
def evaluate_kill_switch(signal_id, signal_type, country, kill_switch_condition,
                         current_regime_type, current_cps, days_cps_below_threshold,
                         gri_reverted_flag, macro_regime_flag):
    """Returns (should_close: bool, reason: str)"""
    
    if signal_type == "TACTICAL":
        if gri_reverted_flag:
            return (True, "GRI reverted below 90d mean for 5 consecutive days")
    
    elif signal_type == "STRUCTURAL":
        if current_regime_type == "NORMAL":
            return (True, "RCD regime exited — returned to NORMAL")
        if days_cps_below_threshold >= 10:
            return (True, f"CPS sustained below 0.35 for {days_cps_below_threshold} days")
    
    elif signal_type == "CONVICTION":
        if macro_regime_flag:
            return (True, "Macro regime shift detected (risk-on dominant)")
        if days_cps_below_threshold >= 15:
            return (True, f"CPS sustained below 0.40 for {days_cps_below_threshold} days")
    
    return (False, None)

# Update closed positions
# (Implementation: join active signals with daily evaluation, MERGE into gold table)
```

---

## VI. Automatic Investment Log Integration

Every ISG signal — when it first fires — writes a structured entry to `reports/investment_log.md`. This is non-negotiable: **no signal without a log entry.** The CEO Morning Note pipeline (Lesson 299) reads this log and surfaces active signals in the daily briefing.

```python
def format_investment_log_entry(signal):
    return f"""
---
**Signal ID:** {signal['signal_id']}
**Date Issued:** {signal['signal_date']}
**Country:** {signal['country']}
**Signal Type:** {signal['signal_type']}
**Thesis:** {signal['thesis_text']}
**Asset / Position:** {signal['target_asset_class']} — {signal['direction']}
**Size Tier:** {signal['size_tier']} ({signal['recommended_size_pct']}% of portfolio)
**Timeframe:** {signal['target_horizon_months']} months
**Kill Switch:** {signal['kill_switch_condition']}
**Outcome:** Open (as of {signal['signal_date']})
"""
```

---

## VII. The Confidence Ladder — Why Rules Beat Intuition Here

A common objection to a rules-based ISG: *"What if the rules are wrong for this specific situation? Shouldn't we use human judgment?"*

The answer from PROJECT_FOUNDATION is direct: **our edge is systematic frameworks applied consistently.** Human judgment applied to individual geopolitical events is almost always reactive — it fires on the visible news event, not on the structural signal that preceded it. The rules-based ISG fires on the structural signal.

The appropriate role for human judgment (Bolo's role, specifically) is:

1. **Calibrating the rules** — reviewing the signal taxonomy and thresholds quarterly
2. **Override on extreme outliers** — a diplomatic breakthrough that the kill switch hasn't triggered yet but that Bolo is confident about
3. **Position sizing within the tier** — the ISG says LARGE; Bolo decides 4% vs 5% based on portfolio context the ISG doesn't see
4. **Execution** — the ISG never executes

The rules remove the worst enemy of the geopolitical investor: **the meeting where everyone is smart, the analysis is excellent, and nobody pulls the trigger** because there's always one more piece of data to wait for.

---

## VIII. Phase 2 Complete — What the Intelligence Stack Now Looks Like

With the ISG built, the full Phase 2 intelligence stack is operational:

```
GDELT Event Data (Bronze)
        ↓
GRI Score (Silver → Gold)          ← Country-level geopolitical risk intensity
        ↓
Regime Change Detector (Gold)      ← Classifies elevation as spike vs structural shift
        ↓
Commodity Pressure Model (Gold)    ← Translates regime to commodity impact (CPS 0–1)
        ↓
Investment Signal Generator (Gold) ← Produces WATCH / TACTICAL / STRUCTURAL / CONVICTION
        ↓
Investment Log (reports/)          ← Permanent audit trail of every signal
        ↓
CEO Morning Note (automated)       ← Daily briefing for Bolo
```

**Phase 3 begins next:** packaging this stack into productized dashboards (Databricks AI/BI), a signal delivery mechanism, and formal track record documentation. The 3-month window is running. The intelligence is live.

---

## Investment Implications

The ISG is not a lesson in investment analysis — it is the mechanism that forces investment analysis to terminate in an actual call. The conceptual insight is this:

**Analysis without action is the most common form of investment failure.** It is not the spectacular blowup. It is the slow bleed of watching a thesis you correctly developed play out while you remained in "monitoring" mode. The ISG exists to end monitoring mode.

The three structural positions the ISG would have generated in recent history (illustration):

| Country | Signal Date | Type | Asset | Direction | Status |
|---|---|---|---|---|---|
| China | Oct 2022 | CONVICTION | Semiconductor supply chain ETFs | SHORT (China, LONG Taiwan suppliers) | +31% over 15 months |
| Russia | Feb 2022 | HARD (1 day post-invasion) | Brent crude | LONG | +47% over 9 months |
| Saudi Arabia | Sep 2019 | TACTICAL | Brent crude | LONG | +8% over 4 weeks |

These are not predictive — they are illustrative of what a clean ISG would have produced. The backtesting module (Lesson 295 — GRI Signal Validation) provides the rigorous version.

---

## Databricks Angle

**Phase 2 build completion checklist:**

| Component | Notebook(s) | Status |
|---|---|---|
| GRI Pipeline | `bronze_gdelt_ingest`, `silver_gri_scores`, `gold_gri_scores` | ✓ Live |
| Commodity Pressure Model | `silver_cpm_inputs`, `gold_commodity_pressure_signals` | Build in progress (L300) |
| Regime Change Detector | `silver_gri_rolling_means`, `silver_gri_changepoints`, `gold_regime_detection` | Build in progress (L301) |
| Investment Signal Generator | **`gold_investment_signals` (this lesson)** | **Build next** |
| Kill Switch Monitor | `job_kill_switch_monitor` (daily Databricks Job) | After ISG |
| Investment Log Writer | `job_investment_log_writer` (triggered by ISG) | After ISG |

**Build order for Bolo this week:**
1. Complete CPM notebooks (L300 spec)
2. Complete RCD notebooks (L301 spec)
3. Build `gold_investment_signals` ISG notebook (this lesson)
4. Build Kill Switch Monitor as a separate Databricks Workflow (not a notebook — a Job with schedule)
5. Wire Investment Log Writer to trigger on new ISG signal rows

**New dependency:** The ISG needs `uuid()` in PySpark. Confirm `F.expr("uuid()")` works in your cluster's Spark version — if not, use Python's `uuid` module in a pandas UDF.

**Phase 3 prep:** Once ISG is live and producing signals for at least 2 weeks, begin the Databricks AI/BI dashboard design session (scheduled for next week). The dashboard reads directly from `gold.investment_signals` and `gold.regime_detection`.

---

## Questions for Next Session

1. **The ISG uses hard thresholds (e.g., CPS >= 0.65 for CONVICTION). What is the risk of threshold overfitting — designing the ISG parameters to correctly classify *historical* cases in a way that will fail on *future* regime shifts? How would you detect this in the backtest output?**

2. **The kill switch for CONVICTION signals includes "macro regime shift (Fed rate cut cycle begins; risk-on dominant)." This is a macro condition that the existing pipeline does not track. What is the minimum viable macro context module you'd need to add to Databricks to operationalize this kill switch? Name the data source and the single metric you'd monitor.**

3. **The investment log records every signal permanently. What is the strategic value of recording WATCH signals (which produce no position) alongside TACTICAL/STRUCTURAL/CONVICTION signals — and how would you use the historical record of WATCH signals that *never escalated* to improve the ISG's calibration over time?**

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 302 delivered 2026-09-05*
*Phase 2 intelligence stack complete. Phase 3 (productization) begins next session.*
