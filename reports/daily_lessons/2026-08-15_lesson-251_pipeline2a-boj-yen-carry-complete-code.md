# Lesson 251: Pipeline 2-A Complete Code — BOJ Yen Carry Unwind Monitor
**Date:** 2026-08-15 (Saturday)
**Session Type:** Engineering Phase — Pipeline Build Sprint
**Curriculum Position:** 251 — Engineering Phase, Session 14
**Pipeline 4 Deadline:** August 15, 2026 — TODAY (no confirmation received as of this session)
**Pipeline 2-A Deadline:** September 12, 2026 — **28 days**
**Pipeline 2-B Deadline:** October 3, 2026 — 49 days
**Pipeline 3 Deadline:** October 31, 2026 — 77 days

---

## CEO Note — Status Update

Pipeline 4's deadline is today. No confirmation email from Bolo has arrived at `ceo@prospectra.earth`. The task has not changed: run the Pipeline 4 notebook, send the composite score + screenshot to `ceo@prospectra.earth`. Today is the day.

This session delivers the complete build code for Pipeline 2-A — the BOJ/Yen Carry Unwind Monitor. The spec was delivered in Lesson 246. Today you build it. September 12 is 28 days away. That is enough time to build, test, and go live — but not enough time to start slowly.

**Priority order for today:**
1. Run Pipeline 4 and email the output (if not yet done)
2. Open a new Databricks notebook: `pipeline2a_boj_carry_monitor.py`
3. Paste Cells 1–10 from this lesson in sequence
4. Run and debug each cell
5. Email the first Cell 10 output to `ceo@prospectra.earth`

---

## CEO Opening Question

The yen carry trade is the largest structural funding trade in global capital markets — estimated notional exposure between $3 and $5 trillion. The true number is uncertain because the trade operates across bank balance sheets, hedge funds, insurance companies, and retail investors (especially Japanese retail via "Mrs. Watanabe" FX accounts) in ways that don't consolidate in any single reporting framework.

**Before writing a single line of code, answer this:**

In August 2024, the BOJ raised its policy rate by 25 basis points — a small move by historical standards. Within two weeks: Brazilian equities fell 8%, Korean semiconductor stocks fell 12%, the VIX spiked from 15 to 65 intraday, and the yen appreciated 7% against the dollar.

**Which variable fired first? And which variable should Pipeline 2-A monitor as its primary signal?**

(a) The BOJ rate decision — the catalyst
(b) The USDJPY appreciation rate — the transmission mechanism
(c) EM equity outflows — the downstream consequence
(d) The VIX spike — a coincident risk-off indicator

The answer to this question determines the architecture of the entire pipeline. If you chose (a), you've built a policy monitoring pipeline: 3–6 months of lead time, low false positive rate once the BOJ actually acts, but highly susceptible to false starts when the BOJ hints and does nothing. If you chose (b), you've built an FX momentum pipeline: fast, responsive, but triggered by any USDJPY move whether carry-related or not (a strong US payrolls report also moves USDJPY). If you chose (c), you've built a damage-assessment pipeline: accurate about what already happened, useless for portfolio protection. If you chose (d), you've built a general risk-off monitor that will fire on every geopolitical shock whether carry-related or not.

**The correct answer is that all four matter — but they fire in sequence:**

1. **BOJ policy signal** fires first — weeks to months ahead (slow-moving precondition)
2. **USDJPY momentum** fires second — days to weeks (primary transmission mechanism)
3. **Cross-asset divergence** fires coincidentally — confirms whether unwind is global or local
4. **EM/risk asset outflows** fire last — 1–3 day lag (validates the thesis, too late to protect but useful for sizing the exit)

Pipeline 2-A is built to detect the sequence, not just any single signal. A pipeline that detects Stage 2 (USDJPY momentum) without Stage 1 (BOJ policy precondition) will generate false positives every time USD weakens for non-carry reasons. A pipeline that detects Stage 1 without Stage 2 will keep you in defensive posture for months while the BOJ deliberates. The multi-layer architecture is not complexity for its own sake — it is the minimum necessary to separate carry signal from carry noise.

---

## Why This Signal Matters for the Prospectra Portfolio

The yen carry trade creates a hidden correlation structure in global markets. Assets that look uncorrelated in normal conditions become highly correlated during carry unwinds because they are all owned by the same pool of carry-funded capital.

**The 2024 episode proved the point:**
- Brazilian real estate investment trusts (nothing to do with Japan)
- Korean semiconductor stocks (a tech play, not an FX play)
- Mexican peso (an EM currency with strong fundamentals)
- Australian government bonds (a "risk-on" fixed income asset)

All sold simultaneously in August 2024. Not because their fundamentals changed. Because the margin call on carry positions required liquidating whatever was liquid. This is the mechanism Warren Buffett was describing when he said "it's only when the tide goes out that you see who's been swimming naked." The tide in this case was borrowed yen.

**For the Prospectra portfolio, this creates two obligations:**

1. **Know when carry risk is building** — so positions in EM equities, high-yield bonds, and commodity-linked assets are sized appropriately for the hidden correlation they carry

2. **Know when to hedge** — the portfolio's EM and commodity overweights are partially carry-funded by other market participants. When those participants are forced to sell, our positions will be caught in the liquidation even if our thesis is right

Pipeline 2-A is the early warning system for both.

---

## Complete Pipeline 2-A Code — 10 Cells

### Cell 1: Setup and Configuration

```python
# ═══════════════════════════════════════════════════════════
# Pipeline 2-A: BOJ Yen Carry Unwind Monitor
# Prospectra Geopolitics & Investment Project
# Deadline: September 12, 2026
# Dependencies: fredapi, yfinance, pyspark
# Output: geopolitics.pipeline2a_carry_risk (Delta table)
# ═══════════════════════════════════════════════════════════

import subprocess
subprocess.run(["pip", "install", "fredapi", "yfinance", "--quiet"], check=True)

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, lit, when, lag, abs as spark_abs,
    avg, first, round as spark_round, current_date
)
from pyspark.sql.window import Window
from pyspark.sql.types import (
    StructType, StructField, DateType, FloatType, StringType, BooleanType
)
import pandas as pd
import numpy as np
from fredapi import Fred
import yfinance as yf
import datetime

spark = SparkSession.builder.appName("Pipeline2A_CarryMonitor").getOrCreate()

# ── FRED credentials ──
FRED_API_KEY = dbutils.secrets.get(scope="prospectra", key="fred_api_key")
fred = Fred(api_key=FRED_API_KEY)

# ── Time window ──
TODAY         = datetime.date.today()
LOOKBACK_DAYS = 90   # 90-day window for trend and regime analysis
START_DATE    = (TODAY - datetime.timedelta(days=LOOKBACK_DAYS)).strftime("%Y-%m-%d")
END_DATE      = TODAY.strftime("%Y-%m-%d")

# Daily date index for resampling monthly series
daily_index = pd.date_range(start=START_DATE, end=END_DATE, freq="D")

# ── CEO Judgmental Estimate (update each session) ──
# As of August 15, 2026:
# BOJ in active normalization cycle (policy rate ~0.75%). USDJPY ~148.
# Carry trade partially unwound post-Aug 2024. Remaining exposure is cautious.
# Primary risk: any BOJ surprise hike > 25bps triggers second unwind wave.
CEO_CARRY_ESTIMATE = 3.2   # Range: 1.0 (carry fully safe) to 5.0 (unwind underway)

print(f"Pipeline 2-A: BOJ Yen Carry Unwind Monitor")
print(f"Run date:          {TODAY}")
print(f"Lookback window:   {LOOKBACK_DAYS} days ({START_DATE} → {END_DATE})")
print(f"CEO carry estimate: {CEO_CARRY_ESTIMATE}/5.0")
print(f"FRED key loaded:   {'yes' if FRED_API_KEY else 'NO — check secret scope'}")
```

---

### Cell 2: Layer 1 — BOJ Policy Signal (Interest Rate Differential)

```python
# Layer 1: US-Japan interest rate differential
# WIDE differential (US >> Japan) = carry trade attractive = LOW carry risk
# NARROW differential (converging) = carry trade stressed = HIGH carry risk

# ── Fetch FRED data ──
fed_funds_s  = fred.get_series("DFF",
                   observation_start=START_DATE, observation_end=END_DATE)
japan_rate_s = fred.get_series("IRSTCI01JPM156N",  # Japan short-term policy rate (monthly)
                   observation_start=START_DATE, observation_end=END_DATE)

fed_df  = pd.DataFrame({"date": fed_funds_s.index.astype(str),
                         "fed_rate": fed_funds_s.values})
jpn_raw = pd.DataFrame({"date": japan_rate_s.index, "japan_rate": japan_rate_s.values})

# Monthly → daily (forward-fill)
jpn_df = (jpn_raw.set_index("date")
          .reindex(daily_index, method="ffill")
          .reset_index()
          .rename(columns={"index": "date"}))
jpn_df["date"] = jpn_df["date"].astype(str)

rates_df = pd.merge(fed_df, jpn_df, on="date", how="inner").dropna()
rates_df["rate_differential"] = rates_df["fed_rate"] - rates_df["japan_rate"]

rates_sdf = spark.createDataFrame(rates_df)

# ── Policy Signal Score (1–5 scale) ──
# >4.5% differential: carry very attractive  → score 1 (LOW risk)
# 3.0–4.5%:          moderate carry          → score 2
# 1.5–3.0%:          narrowing carry         → score 3
# 0.0–1.5%:          near-parity             → score 4
# Negative:          Japan rate > US rate    → score 5 (CRITICAL)
rates_sdf = rates_sdf.withColumn(
    "policy_signal_score",
    when(col("rate_differential") > 4.5, 1.0)
    .when(col("rate_differential") > 3.0, 2.0)
    .when(col("rate_differential") > 1.5, 3.0)
    .when(col("rate_differential") > 0.0, 4.0)
    .otherwise(5.0)
)

# ── 10-day narrowing trend ──
w10 = Window.orderBy("date").rowsBetween(-10, -10)
rates_sdf = rates_sdf.withColumn(
    "differential_10d_ago", first(col("rate_differential")).over(w10)
).withColumn(
    "differential_10d_change",
    col("rate_differential") - col("differential_10d_ago")
).withColumn(
    "differential_narrowing",
    when(col("differential_10d_change") < -0.15, True).otherwise(False)
)

rates_sdf.createOrReplaceTempView("layer1_policy")

print("── Layer 1: BOJ Policy Signal ──")
rates_sdf.orderBy(col("date").desc()).select(
    "date", "fed_rate", "japan_rate", "rate_differential",
    "policy_signal_score", "differential_narrowing"
).show(7)
```

---

### Cell 3: Layer 2 — FX Signal (USDJPY Momentum)

```python
# Layer 2: USDJPY level and momentum
# HIGH USDJPY (e.g. 155) = JPY weak = carry trade working = LOW risk
# LOW USDJPY (e.g. 135) = JPY strong = carry trade squeezed = HIGH risk
# FALLING USDJPY rapidly = active carry unwind = CRITICAL

usdjpy_raw = yf.download("USDJPY=X", start=START_DATE, end=END_DATE, progress=False)
usdjpy_df  = usdjpy_raw["Close"].reset_index()
usdjpy_df.columns = ["date", "usdjpy"]
usdjpy_df["date"] = pd.to_datetime(usdjpy_df["date"]).dt.date.astype(str)

usdjpy_sdf = spark.createDataFrame(usdjpy_df)
w_asc      = Window.orderBy("date")

# ── Rolling returns ──
usdjpy_sdf = (usdjpy_sdf
    .withColumn("usdjpy_5d_return",
        (col("usdjpy") - lag("usdjpy", 5).over(w_asc))
        / lag("usdjpy", 5).over(w_asc) * 100)
    .withColumn("usdjpy_20d_return",
        (col("usdjpy") - lag("usdjpy", 20).over(w_asc))
        / lag("usdjpy", 20).over(w_asc) * 100)
)

# ── FX Signal Score ──
# Level score: where is USDJPY right now?
# Momentum adjustment: is it falling fast? (active unwind)
usdjpy_sdf = usdjpy_sdf.withColumn(
    "fx_level_score",
    when(col("usdjpy") > 150, 1.0)
    .when(col("usdjpy") > 145, 2.0)
    .when(col("usdjpy") > 140, 3.0)
    .when(col("usdjpy") > 135, 4.0)
    .otherwise(5.0)
).withColumn(
    "fx_momentum_adj",
    when(col("usdjpy_5d_return") < -3.0, 1.5)   # Rapid JPY appreciation → add 1.5
    .when(col("usdjpy_5d_return") < -1.5, 0.75)  # Moderate JPY appreciation → add 0.75
    .when(col("usdjpy_5d_return") >  2.0, -0.5)  # Rapid JPY weakening → subtract 0.5 (carry thriving)
    .otherwise(0.0)
).withColumn(
    "fx_signal_score",
    spark_round(
        spark_abs(
            when(col("fx_level_score") + col("fx_momentum_adj") > 5.0, 5.0)
            .when(col("fx_level_score") + col("fx_momentum_adj") < 1.0, 1.0)
            .otherwise(col("fx_level_score") + col("fx_momentum_adj"))
        ),
        2
    )
).withColumn(
    "yen_appreciation_flag",
    when(col("usdjpy_5d_return") < -2.0, True).otherwise(False)
)

usdjpy_sdf.createOrReplaceTempView("layer2_fx")

print("── Layer 2: USDJPY FX Signal ──")
usdjpy_sdf.orderBy(col("date").desc()).select(
    "date", "usdjpy", "usdjpy_5d_return",
    "fx_level_score", "fx_momentum_adj", "fx_signal_score", "yen_appreciation_flag"
).show(7)
```

---

### Cell 4: Layer 3 — Cross-Asset Confirmation (VIX + EM Stress)

```python
# Layer 3: Cross-asset signals that confirm (or deny) a carry unwind
# Carry unwinds do not happen in isolation — they coincide with:
#   - VIX spike (risk-off)
#   - EM equity selloff (carry-funded EM positions being liquidated)
#   - High-yield bond weakness (leveraged carry participants deleveraging)

tickers = {
    "^VIX":   "vix",
    "EEM":    "em_equities",    # iShares MSCI EM ETF
    "HYG":    "high_yield",     # iShares HY Corporate Bond ETF
    "GLD":    "gold",           # SPDR Gold Shares (safe-haven confirmation)
}

cross_frames = []
for ticker, label in tickers.items():
    raw  = yf.download(ticker, start=START_DATE, end=END_DATE, progress=False)
    temp = raw["Close"].reset_index()
    temp.columns = ["date", label]
    temp["date"] = pd.to_datetime(temp["date"]).dt.date.astype(str)
    cross_frames.append(temp)

from functools import reduce
cross_df = reduce(lambda l, r: pd.merge(l, r, on="date", how="outer"), cross_frames)
cross_df = cross_df.sort_values("date").ffill().dropna()

cross_sdf = spark.createDataFrame(cross_df)

for asset in ["em_equities", "high_yield", "gold"]:
    cross_sdf = cross_sdf.withColumn(
        f"{asset}_5d_return",
        (col(asset) - lag(asset, 5).over(Window.orderBy("date")))
        / lag(asset, 5).over(Window.orderBy("date")) * 100
    )

# ── Individual sub-scores ──
cross_sdf = (cross_sdf
    .withColumn("vix_score",
        when(col("vix") < 15,  1.0)
        .when(col("vix") < 20, 2.0)
        .when(col("vix") < 25, 3.0)
        .when(col("vix") < 35, 4.0)
        .otherwise(5.0))
    .withColumn("em_stress_score",
        when(col("em_equities_5d_return") >  1.0,  1.0)
        .when(col("em_equities_5d_return") > -1.0,  2.0)
        .when(col("em_equities_5d_return") > -3.0,  3.0)
        .when(col("em_equities_5d_return") > -5.0,  4.0)
        .otherwise(5.0))
    .withColumn("hy_stress_score",
        when(col("high_yield_5d_return") >  0.5,  1.0)
        .when(col("high_yield_5d_return") > -0.5,  2.0)
        .when(col("high_yield_5d_return") > -1.5,  3.0)
        .when(col("high_yield_5d_return") > -2.5,  4.0)
        .otherwise(5.0))
)

# ── Cross-Asset Composite ──
# Equal weight: VIX, EM stress, HY stress
cross_sdf = cross_sdf.withColumn(
    "cross_asset_score",
    spark_round(
        (col("vix_score") + col("em_stress_score") + col("hy_stress_score")) / 3.0,
        2
    )
)

cross_sdf.createOrReplaceTempView("layer3_cross_asset")

print("── Layer 3: Cross-Asset Confirmation ──")
cross_sdf.orderBy(col("date").desc()).select(
    "date", "vix", "vix_score",
    "em_equities_5d_return", "em_stress_score",
    "high_yield_5d_return",  "hy_stress_score",
    "cross_asset_score"
).show(7)
```

---

### Cell 5: Layer 4 — JGB Yield (BOJ Normalization Structural Signal)

```python
# Layer 4: Japan Government Bond 10-year yield
# Rising JGB yields = BOJ normalization accelerating = structural carry pressure
# Historically held near-zero under YCC; BOJ scrapped YCC in 2024
# JGB yield is the slowest-moving but most structurally significant signal

try:
    jgb_series = fred.get_series(
        "IRLTLT01JPM156N",    # Japan long-term gov bond yield (monthly, FRED)
        observation_start=START_DATE,
        observation_end=END_DATE
    )
    jgb_df = pd.DataFrame({"date": jgb_series.index, "jgb_10y": jgb_series.values})
    jgb_df = (jgb_df.set_index("date")
              .reindex(daily_index, method="ffill")
              .reset_index()
              .rename(columns={"index": "date"}))
    jgb_df["date"] = jgb_df["date"].astype(str)

    jgb_sdf = spark.createDataFrame(jgb_df)

    # ── JGB Signal Score ──
    # Below 0.5%: YCC-era or near-YCC conditions (carry fully intact)
    # 0.5–1.0%:   Early normalization
    # 1.0–1.5%:   Active normalization (pressure building)
    # 1.5–2.0%:   Carry squeeze territory
    # Above 2.0%: Structural carry collapse
    jgb_sdf = jgb_sdf.withColumn(
        "jgb_signal_score",
        when(col("jgb_10y") < 0.5,  1.0)
        .when(col("jgb_10y") < 1.0, 2.0)
        .when(col("jgb_10y") < 1.5, 3.0)
        .when(col("jgb_10y") < 2.0, 4.0)
        .otherwise(5.0)
    )
    jgb_sdf.createOrReplaceTempView("layer4_jgb")

    print("── Layer 4: JGB Yield Signal (FRED) ──")
    jgb_sdf.orderBy(col("date").desc()).select(
        "date", "jgb_10y", "jgb_signal_score"
    ).show(7)

except Exception as e:
    print(f"JGB data unavailable ({e}). Falling back to policy rate proxy.")
    # Fallback: use Layer 1 policy score as JGB proxy (correlated)
    spark.sql("""
        CREATE OR REPLACE TEMP VIEW layer4_jgb AS
        SELECT date, policy_signal_score AS jgb_signal_score
        FROM layer1_policy
    """)
    print("Layer 4 fallback active — using policy rate proxy.")
```

---

### Cell 6: Composite Carry Risk Score

```python
# Composite Score: weighted average of all four layers
# Weights reflect timing and reliability:
#   Layer 1 (Policy Rate Differential): 25% — slow-moving, high structural confidence
#   Layer 2 (USDJPY Momentum):          40% — primary transmission mechanism, most actionable
#   Layer 3 (Cross-Asset Confirmation): 25% — confirms or denies the carry hypothesis
#   Layer 4 (JGB Yield):                10% — structural signal, monthly resolution

composite_raw = spark.sql(f"""
    SELECT
        l1.date,
        l1.fed_rate,
        l1.japan_rate,
        l1.rate_differential,
        l1.policy_signal_score,
        l1.differential_narrowing,
        l2.usdjpy,
        l2.usdjpy_5d_return,
        l2.fx_signal_score,
        l2.yen_appreciation_flag,
        l3.vix,
        l3.cross_asset_score,
        l3.em_equities_5d_return,
        l3.hy_stress_score,
        l4.jgb_signal_score
    FROM layer1_policy      l1
    JOIN layer2_fx          l2 ON l1.date = l2.date
    JOIN layer3_cross_asset l3 ON l1.date = l3.date
    JOIN layer4_jgb         l4 ON l1.date = l4.date
    WHERE l1.date >= '{START_DATE}'
    ORDER BY l1.date DESC
""")

# ── Weighted composite ──
composite_df = composite_raw.withColumn(
    "p2a_composite_score",
    spark_round(
        col("policy_signal_score") * 0.25
        + col("fx_signal_score")   * 0.40
        + col("cross_asset_score") * 0.25
        + col("jgb_signal_score")  * 0.10,
        2
    )
)

# ── 10-day smoothed signal (reduces day-to-day noise) ──
w_smooth = Window.orderBy("date").rowsBetween(-9, 0)
composite_df = composite_df.withColumn(
    "p2a_10d_avg",
    spark_round(avg(col("p2a_composite_score")).over(w_smooth), 2)
)

# ── Regime change detection ──
composite_df = composite_df.withColumn(
    "score_1d_change",
    col("p2a_composite_score") - lag("p2a_composite_score", 1).over(Window.orderBy("date"))
)

composite_df.createOrReplaceTempView("p2a_composite")

print("── Pipeline 2-A Composite Carry Risk Score ──")
composite_df.select(
    "date", "rate_differential", "usdjpy", "vix",
    "policy_signal_score", "fx_signal_score",
    "cross_asset_score",   "jgb_signal_score",
    "p2a_composite_score", "p2a_10d_avg"
).show(10)
```

---

### Cell 7: Regime Classification

```python
# Regime Classification: map composite score to a named carry risk state
# Each regime maps to specific portfolio actions in Cell 8

composite_df = composite_df.withColumn(
    "carry_risk_regime",
    when(col("p2a_composite_score") < 2.0,  "CARRY_FAVORABLE")    # Carry intact, no action
    .when(col("p2a_composite_score") < 2.75, "MODERATE_RISK")     # Pressure building, watch
    .when(col("p2a_composite_score") < 3.5,  "ELEVATED_RISK")     # BOJ active, reduce exposure
    .when(col("p2a_composite_score") < 4.25, "UNWIND_IMMINENT")   # Liquidation conditions met
    .otherwise("UNWIND_UNDERWAY")                                   # Active carry liquidation
).withColumn(
    "regime_color",
    when(col("carry_risk_regime") == "CARRY_FAVORABLE",  "GREEN")
    .when(col("carry_risk_regime") == "MODERATE_RISK",   "YELLOW")
    .when(col("carry_risk_regime") == "ELEVATED_RISK",   "ORANGE")
    .when(col("carry_risk_regime") == "UNWIND_IMMINENT", "RED")
    .otherwise("CRITICAL_RED")
).withColumn(
    "prev_regime",
    lag("carry_risk_regime", 1).over(Window.orderBy("date"))
).withColumn(
    "regime_changed",
    when(col("carry_risk_regime") != col("prev_regime"), True).otherwise(False)
)

# ── Severity flag: rapid escalation ──
# Single-day composite move > 0.5 = investigate immediately
composite_df = composite_df.withColumn(
    "rapid_escalation_flag",
    when(col("score_1d_change") > 0.5, True).otherwise(False)
)

print("── Pipeline 2-A: Regime Classification (last 14 days) ──")
composite_df.orderBy(col("date").desc()).select(
    "date", "p2a_composite_score", "p2a_10d_avg",
    "carry_risk_regime", "regime_color",
    "regime_changed", "rapid_escalation_flag"
).show(14)
```

---

### Cell 8: Investment Signal Generator

```python
# Investment Signals: what portfolio action each regime implies
# These are directional views for a 6–18 month investor, not day-trading signals

REGIME_SIGNALS = {
    "CARRY_FAVORABLE": {
        "em_equities":      "OVERWEIGHT",
        "jpy_fx":           "SHORT",        # Long USD, short JPY = carry trade on
        "high_yield":       "OVERWEIGHT",
        "gold":             "UNDERWEIGHT",
        "dm_equities":      "NEUTRAL",
        "position_sizing":  "FULL_RISK",
        "action":           "Carry trade intact. Maintain EM overweight and risk-on positioning. "
                            "JPY short is productive. Watch BOJ communications for any shift.",
    },
    "MODERATE_RISK": {
        "em_equities":      "NEUTRAL",
        "jpy_fx":           "REDUCE_SHORT",  # Trim 25% of JPY short
        "high_yield":       "NEUTRAL",
        "gold":             "SMALL_LONG",
        "dm_equities":      "SLIGHT_OVERWEIGHT",
        "position_sizing":  "75_PCT_RISK",
        "action":           "Carry pressure building. Reduce JPY short by 25%. "
                            "Trim EM overweight to neutral. Add small gold hedge.",
    },
    "ELEVATED_RISK": {
        "em_equities":      "UNDERWEIGHT",
        "jpy_fx":           "NEUTRAL",      # Close JPY short entirely
        "high_yield":       "UNDERWEIGHT",
        "gold":             "OVERWEIGHT",
        "dm_equities":      "SLIGHT_OVERWEIGHT",
        "position_sizing":  "50_PCT_RISK",
        "action":           "BOJ normalization active. Close JPY short entirely. "
                            "Rotate EM underweight → developed market equities. "
                            "Increase gold to 5–8% of portfolio. Raise cash to 15%.",
    },
    "UNWIND_IMMINENT": {
        "em_equities":      "DEFENSIVE",
        "jpy_fx":           "LONG",         # Flip to long JPY = carry hedge
        "high_yield":       "SELL",
        "gold":             "STRONG_OVERWEIGHT",
        "dm_equities":      "NEUTRAL",
        "position_sizing":  "25_PCT_RISK",
        "action":           "Carry unwind conditions fully met. Flip to long JPY. "
                            "Sell high yield entirely. Gold to 10–12% of portfolio. "
                            "Cash to 25–30%. DO NOT add new risk positions.",
    },
    "UNWIND_UNDERWAY": {
        "em_equities":      "SELL",
        "jpy_fx":           "MAX_LONG",     # Maximum JPY long
        "high_yield":       "SELL",
        "gold":             "MAX_LONG",
        "dm_equities":      "DEFENSIVE",
        "position_sizing":  "MAXIMUM_DEFENSIVE",
        "action":           "CARRY UNWIND ACTIVE. Full defensive posture. "
                            "Maximum JPY long. Sell all EM and HY immediately. "
                            "Gold maximum position. Wait for VIX > 40 to begin re-entry. "
                            "Re-entry criteria: USDJPY stabilized for 5 consecutive days.",
    },
}

# ── Today's signal output ──
today_row    = composite_df.orderBy(col("date").desc()).first()
today_regime = today_row["carry_risk_regime"]
today_score  = today_row["p2a_composite_score"]
today_10d    = today_row["p2a_10d_avg"]
today_usdjpy = today_row["usdjpy"]
today_vix    = today_row["vix"]
today_rdiff  = today_row["rate_differential"]

signal = REGIME_SIGNALS.get(today_regime, REGIME_SIGNALS["MODERATE_RISK"])

print(f"\n{'═'*65}")
print(f"  PIPELINE 2-A — BOJ YEN CARRY UNWIND MONITOR")
print(f"  Run Date: {TODAY}")
print(f"{'═'*65}")
print(f"  Composite Score:          {today_score:.2f} / 5.00")
print(f"  10-Day Smoothed:          {today_10d:.2f} / 5.00")
print(f"  Carry Risk Regime:        {today_regime}")
print(f"  CEO Estimate:             {CEO_CARRY_ESTIMATE:.2f}")
print(f"  Delta (Pipeline − CEO):   {today_score - CEO_CARRY_ESTIMATE:+.2f}")
print(f"{'─'*65}")
print(f"  USD/JPY:                  {today_usdjpy:.2f}")
print(f"  VIX:                      {today_vix:.1f}")
print(f"  US-Japan Rate Differential: {today_rdiff:.2f}%")
print(f"{'─'*65}")
print(f"  EM Equities:              {signal['em_equities']}")
print(f"  JPY Position:             {signal['jpy_fx']}")
print(f"  High Yield:               {signal['high_yield']}")
print(f"  Gold:                     {signal['gold']}")
print(f"  Risk Budget:              {signal['position_sizing']}")
print(f"{'─'*65}")
print(f"  ACTION: {signal['action']}")
print(f"{'═'*65}")
```

---

### Cell 9: Write to Delta Table

```python
# Persist today's output to Delta table for GSI integration
# This table feeds into Pipeline 4's composite GSI when Pipeline 2-A goes live

schema = StructType([
    StructField("run_date",               DateType(),    False),
    StructField("p2a_composite_score",    FloatType(),   True),
    StructField("p2a_10d_avg",            FloatType(),   True),
    StructField("carry_risk_regime",      StringType(),  True),
    StructField("policy_signal_score",    FloatType(),   True),
    StructField("fx_signal_score",        FloatType(),   True),
    StructField("cross_asset_score",      FloatType(),   True),
    StructField("jgb_signal_score",       FloatType(),   True),
    StructField("usdjpy",                 FloatType(),   True),
    StructField("vix",                    FloatType(),   True),
    StructField("rate_differential",      FloatType(),   True),
    StructField("ceo_estimate",           FloatType(),   True),
    StructField("delta_pipeline_vs_ceo",  FloatType(),   True),
    StructField("regime_changed",         BooleanType(), True),
    StructField("rapid_escalation_flag",  BooleanType(), True),
])

output_data = [{
    "run_date":              TODAY,
    "p2a_composite_score":   float(today_score),
    "p2a_10d_avg":           float(today_10d) if today_10d else float(today_score),
    "carry_risk_regime":     today_regime,
    "policy_signal_score":   float(today_row["policy_signal_score"]),
    "fx_signal_score":       float(today_row["fx_signal_score"]),
    "cross_asset_score":     float(today_row["cross_asset_score"]),
    "jgb_signal_score":      float(today_row["jgb_signal_score"]),
    "usdjpy":                float(today_usdjpy) if today_usdjpy else 0.0,
    "vix":                   float(today_vix)    if today_vix    else 0.0,
    "rate_differential":     float(today_rdiff)  if today_rdiff  else 0.0,
    "ceo_estimate":          float(CEO_CARRY_ESTIMATE),
    "delta_pipeline_vs_ceo": float(today_score) - float(CEO_CARRY_ESTIMATE),
    "regime_changed":        bool(today_row["regime_changed"]) if today_row["regime_changed"] is not None else False,
    "rapid_escalation_flag": bool(today_row["rapid_escalation_flag"]) if today_row["rapid_escalation_flag"] is not None else False,
}]

output_sdf = spark.createDataFrame(output_data, schema=schema)

(output_sdf
 .write
 .format("delta")
 .mode("append")
 .option("mergeSchema", "true")
 .saveAsTable("geopolitics.pipeline2a_carry_risk"))

total_rows = spark.table("geopolitics.pipeline2a_carry_risk").count()
print(f"Pipeline 2-A output written to: geopolitics.pipeline2a_carry_risk")
print(f"Total records in table:          {total_rows}")
print(f"Today's regime:                  {today_regime} ({today_score:.2f}/5.00)")
```

---

### Cell 10: Alert Logic and GSI Integration Status

```python
# Alert: email CEO if regime escalates above ELEVATED_RISK or changes unexpectedly
# GSI Integration: report current weight assignment for Pipeline 2-A in GSI formula

ALERT_THRESHOLD_REGIMES = {"UNWIND_IMMINENT", "UNWIND_UNDERWAY"}

# Pull yesterday's regime for change detection
try:
    yesterday_rows = spark.sql("""
        SELECT carry_risk_regime
        FROM geopolitics.pipeline2a_carry_risk
        WHERE run_date = date_sub(current_date(), 1)
        ORDER BY run_date DESC LIMIT 1
    """).collect()
    yesterday_regime = yesterday_rows[0]["carry_risk_regime"] if yesterday_rows else None
except Exception:
    yesterday_regime = None

regime_escalated = (
    today_regime in ALERT_THRESHOLD_REGIMES
    or (yesterday_regime is not None
        and today_regime != yesterday_regime
        and today_score >= 3.5)
)

print(f"\nAlert Evaluation:")
print(f"  Today:     {today_regime} ({today_score:.2f})")
print(f"  Yesterday: {yesterday_regime or 'N/A (first run)'}")
print(f"  Alert:     {'YES — send email' if regime_escalated else 'No'}")

if regime_escalated:
    print(f"\n⚠️  REGIME ALERT: {yesterday_regime} → {today_regime}")
    print(f"    Email: ceo@prospectra.earth")
    print(f"    Subject: PIPELINE 2-A ALERT — Carry Regime: {today_regime}")
    print(f"    Action: {signal['action']}")
    # To send email: configure SMTP credentials in dbutils.secrets scope "prospectra"
    # Key: "smtp_host", "smtp_user", "smtp_password"

# ── GSI Integration Status ──
print(f"\n{'─'*65}")
print(f"  GSI FORMULA — Pipeline 2-A Weight Assignment")
print(f"{'─'*65}")
print(f"  Pipeline 4 (Export Control Bifurcation): 40% of GSI")
print(f"  Pipeline 2-A (BOJ Carry Risk):           25% of GSI  ← LIVE when table populated")
print(f"  Pipeline 2-B (Iran Nuclear):             20% of GSI  ← Pending (Oct 3 deadline)")
print(f"  Pipeline 3 (US-China Diplomatic):        15% of GSI  ← Pending (Oct 31 deadline)")
print(f"{'─'*65}")
print(f"  Current P2-A score feeding GSI:  {today_score:.2f} × 0.25 = {today_score * 0.25:.2f} GSI points")
print(f"{'─'*65}")

print(f"\n── Pipeline 2-A complete. ──")
print(f"Notebook: pipeline2a_boj_carry_monitor.py")
print(f"Table:    geopolitics.pipeline2a_carry_risk")
print(f"Schedule: Daily at 07:00 UTC, market days")
print(f"Next milestone: Pipeline 2-A LIVE → September 12, 2026 ({28} days)")
```

---

## Investment Implications — The Yen Carry Trade in the Prospectra Portfolio

### Why This Signal Has Non-Linear Impact

The yen carry trade creates a hidden correlation that ordinary portfolio construction misses entirely. When you model a portfolio with EM equities, commodity producers, and high-yield bonds, you calculate their pairwise correlations based on historical data from normal market conditions. That correlation matrix does not include the correlation they develop *under carry unwind stress* — when they are all simultaneously owned by the same pool of JPY-funded capital and that capital is forced to liquidate.

The empirical evidence is unambiguous. In August 2024:

- **iShares MSCI Emerging Markets ETF (EEM):** -8.2% in 10 trading days
- **VanEck Semiconductor ETF (SMH):** -12.6% in 10 trading days
- **iShares iBoxx High Yield Corporate Bond ETF (HYG):** -3.1% in 10 trading days
- **Brazilian Bovespa Index:** -7.4% in 10 trading days
- **Mexican Peso (USD/MXN):** -6.8% appreciation (peso weakening) in 10 trading days

None of these assets had fundamental news that week. The BOJ's rate decision affected none of their underlying businesses directly. What happened is that they were collectively owned by a global pool of carry-funded investors who all received the same margin call at the same time and liquidated whatever they could sell quickly.

**For the Prospectra portfolio, this means:** Our structural overweight on EM equities and commodity-linked assets is not fully diversified. It contains an implicit short position on Japanese monetary normalization. If the BOJ moves faster than expected — or if any external shock triggers a broad risk-off event — these positions will sell off together even if our individual investment theses are correct.

Pipeline 2-A is the hedge against being right about the thesis but wrong about the timing of the carry unwind.

### The Three Investment Regimes Pipeline 2-A Defines

**Regime 1: CARRY_FAVORABLE / MODERATE_RISK (score 1.0–2.75)**

The BOJ is either dovish or moving slowly. The rate differential is wide. USDJPY is stable or weakening (carry working). This is the environment to run full EM and commodity overweights. There is no carry unwind risk in the near term. The only action is monitoring.

*Portfolio: Full risk. EM overweight, commodity overweight, JPY short as funding currency for currency-overlay strategies.*

**Regime 2: ELEVATED_RISK / UNWIND_IMMINENT (score 2.75–4.25)**

The BOJ is actively hiking. The rate differential is narrowing. USDJPY is falling or at risk of a sharp move. This is the environment to rotate out of carry-correlated assets. Not because the individual investment theses are wrong — but because the funding environment for those theses is deteriorating. The thesis doesn't matter if the position gets liquidated before it resolves.

*Portfolio: Reduce to 25–50% risk budget. Close JPY shorts. Rotate from EM and HY to developed market equities and gold. Raise cash.*

**Regime 3: UNWIND_UNDERWAY (score 4.25+)**

Active liquidation. All carry-correlated assets are selling regardless of fundamentals. The correct response is full defensive posture, long JPY, maximum gold, and patience. The unwind creates the buying opportunity — the EM and commodity theses don't disappear, they just go on sale. The CEO will flag the re-entry signal when VIX > 40 and USDJPY stabilizes.

*Portfolio: Maximum defensive. Sell EM and HY. Long JPY. Maximum gold. Wait for VIX > 40 as the capitulation signal, then begin staged re-entry.*

---

## Databricks Angle — Scheduling Pipeline 2-A as a Daily Job

**After the notebook runs successfully once, automate it:**

1. In Databricks, go to **Workflows → Create Job**
2. Task settings:
   - Task name: `p2a_boj_carry_monitor`
   - Type: Notebook
   - Source: Repos → your notebook path
   - Cluster: Use existing cluster or create a job cluster (cheaper)
3. Schedule: **Daily at 07:00 UTC** (before US market open)
4. Email notifications: Add `ceo@prospectra.earth` to "On Failure" and "On Success"

**The resulting automated output, stored daily in `geopolitics.pipeline2a_carry_risk`, feeds directly into the GSI formula.** Once Pipeline 2-A is live, the GSI calculation upgrades from CEO-estimate for Signal 2 to actual pipeline data — GSI v2.0 is activated.

**The carry risk timeline feeds directly into the data architecture:**

```
geopolitics.pipeline4_scores   (live now — P4 deadline today)
    ↓ 40% weight
geopolitics.pipeline2a_carry_risk  (live Sep 12)
    ↓ 25% weight
geopolitics.pipeline2b_iran_risk   (live Oct 3)
    ↓ 20% weight
geopolitics.pipeline3_uschina_risk (live Oct 31)
    ↓ 15% weight
→ geopolitics.gsi_composite         (full GSI v3.0 — November 2026)
```

**GDELT integration (later enhancement):** Add GDELT news sentiment on BOJ and JPY keywords as a Layer 5 signal. Pull 7-day article counts mentioning "Bank of Japan rate hike" or "yen appreciation" from GDELT's GKG table. High article volume + falling USDJPY = Type 1 confirmation signal. This adds an additional early-warning capability before the USDJPY actually breaks.

---

## Key Concepts Summary

| Concept | Definition |
|---|---|
| **Yen carry trade** | Borrowing in low-yield JPY and investing in higher-yield assets. Profitable as long as JPY stays weak and rate differential is wide. Unravels violently when JPY strengthens. |
| **Carry-correlated assets** | Assets that look uncorrelated in normal conditions but sell together during carry unwinds because they share the same funding base. EM equities, HY bonds, and commodity-linked assets are all carry-correlated. |
| **USDJPY as signal** | The primary transmission mechanism of carry trade activity. Rapid USDJPY decline (JPY appreciation) is the most reliable leading indicator of carry unwind stress. |
| **Rate differential narrowing** | The slow-moving precondition. When the US-Japan rate differential narrows, the carry trade becomes less attractive even before an actual unwind. Pipeline 2-A monitors this as Layer 1. |
| **VIX as confirmation** | The VIX does not cause carry unwinds, but it confirms them. A carry unwind without a VIX spike is localized. A carry unwind with a VIX spike above 30 is systemic — all correlated assets sell simultaneously. |
| **The paper-trading window** | The same principle from Lesson 250 applies here: run Pipeline 2-A on live data for 30 days before incorporating it into the GSI formula. Track CEO estimate vs. pipeline reading daily. |
| **Re-entry signal** | VIX > 40 (capitulation) + USDJPY stable for 5 consecutive sessions = the conditions under which carry trades are fully liquidated and the next long entry in EM and HY is valid. |

---

## Reflection Questions

**Question 1 — The false signal problem:**
The USDJPY can fall for reasons completely unrelated to the carry trade: a weaker US jobs report, a geopolitical shock in Europe that drives dollar safe-haven flows down, or seasonal FX flow patterns from Japanese fiscal year-end. Pipeline 2-A uses USDJPY momentum as a 40% weight in its composite. Design an additional filter that reduces the weight of the FX signal when the USDJPY move appears to be driven by US macro factors rather than BOJ/carry dynamics. What variables would you use as the "context layer" to distinguish "JPY strengthening because BOJ is hiking" from "JPY strengthening because US economy is weakening"? Hint: consider the simultaneous behavior of the 2-year US Treasury yield.

**Question 2 — The August 2024 calibration:**
The pipeline's threshold structure (USDJPY > 150 = score 1, USDJPY 135–140 = score 4) was calibrated based on historical yen ranges. But the yen's equilibrium level shifts over time: in 2012, USDJPY was 80. In 2024, USDJPY was 160 at peak. The "danger zone" is not an absolute number — it is a level relative to the current equilibrium. Design a dynamic threshold system that adjusts the USDJPY scoring bands based on the 1-year historical range of USDJPY, rather than fixed absolute levels. How does this change the signal when USDJPY is in a long-term weakening trend vs. a long-term strengthening trend?

**Question 3 — Portfolio sizing under hidden correlation:**
The Prospectra portfolio is long EM equities and commodity-linked assets. Pipeline 2-A is in ELEVATED_RISK regime. The portfolio protocol says to "reduce EM overweight to underweight." But the CEO's EM thesis is still valid — the geopolitical conditions that make EM equities attractive have not changed. You are not selling because the thesis is wrong; you are selling because the carry unwind risk makes holding the position tactically untenable. Design a re-entry protocol: when carry risk subsides (Pipeline 2-A returns to MODERATE_RISK), how do you re-enter the EM position? Do you re-enter all at once or in stages? At what carry risk score do you return to full overweight? What evidence would tell you the EM thesis itself has also deteriorated (requiring a different response than a carry-hedge exit)?

---

## CEO Closing Note

Pipeline 2-A is the most consequential pipeline in the Prospectra analytical suite — not because carry unwinds are the biggest geopolitical risk (they are not), but because they are the risk that can make a correct thesis unprofitable.

You can be right about India's decade of growth. Right about Africa's critical mineral emergence. Right about the energy transition creating commodity supercycles. And still lose money on all three positions simultaneously if the yen carry trade unwinds while you hold them.

The September 12 deadline is firm. 28 days is enough time to build this pipeline, run it for 2 weeks of live calibration, and go live with confidence. The code is above. The architecture is clear. The investment logic is complete.

**Today's build task:**
1. Create a new Databricks notebook: `pipeline2a_boj_carry_monitor.py`
2. Paste Cells 1–10 in sequence
3. Run each cell and fix any authentication or data-pull errors
4. Send the Cell 10 output (composite score, regime, USD/JPY reading) to `ceo@prospectra.earth`

One notebook. Ten cells. September 12.

```
Engineering Sequence Status — August 15, 2026:

Pipeline 4:   [ ] LIVE — Deadline TODAY. Awaiting confirmation.
Pipeline 2-A: [ ] LIVE — Deadline September 12. 28 days. Code delivered above.
Pipeline 2-B: [ ] LIVE — Deadline October 3.   49 days. Spec in Lesson 247.
Pipeline 3:   [ ] LIVE — Deadline October 31.  77 days. Code in Lesson 249.

GSI v1.0 (CEO estimates only):         ACTIVE
GSI v2.0 (P4 live):                    Awaiting P4 confirmation
GSI v3.0 (P4 + P2-A live):             September 12
GSI v4.0 (All four pipelines live):    November 2026
```

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 251 | August 15, 2026 | Engineering Phase, Session 14*
*Pipeline 4 deadline: August 15, 2026 — TODAY*
*Pipeline 2-A deadline: September 12, 2026 — 28 days*
*Next lesson: Pipeline 2-B complete code — Iran Nuclear Threshold Monitor*
