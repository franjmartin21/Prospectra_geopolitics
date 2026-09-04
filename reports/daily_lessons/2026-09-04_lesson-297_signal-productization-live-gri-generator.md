# Lesson 297 — Signal Productization: Building the Live GRI Signal Generator

**Date:** 2026-09-04
**Session Type:** Daily Lesson
**Lesson Number:** 297 / ongoing
**Topic:** Databricks Build Module — Signal Productization: From Backtest to Live Daily Signal
**Curriculum Arc:** Databricks Build Module — Lesson 9 (the live layer: translating GRI scores into actionable daily signals with position sizing logic)

---

## Opening Question

*Your backtest is either running or complete. You have t-statistics in front of you — or you're about to.*

Here is the question that separates analysts from investors:

**"The GRI has signal at the 22-day horizon for EM FX. Now what?"**

Most people answer this by going back to the spreadsheet. They tweak parameters, run more regressions, look for ways to make the number bigger. This is the quant trap: the analytical loop that feels like progress but produces no investment outcomes.

The CEO's answer is different: **build the production signal.** A signal that exists only in a notebook is not a signal. It is a research artifact. A signal that runs daily, outputs a structured recommendation, and has a defined decision rule — that is a signal.

This lesson specifies the live signal generator: the component that transforms the daily GRI output into a structured investment view, delivered to Bolo each morning.

---

## I. Architecture: The Signal Generator Layer

The signal generator sits immediately downstream of the Gold layer GRI:

```
GDELT Bronze → GDELT Silver → Gold (GRI) → Signal Generator → Alert / Output
                                    ↑
Market Data Bronze → Market Data Silver ─┘ (for regime context)
```

It is a single Databricks notebook — `gri_signal_generator` — that runs daily after `gdelt_gold_gri` completes. It reads the GRI table, applies the signal rules, and outputs a structured signal table plus an alert.

**Output tables:**

| Table | Content |
|---|---|
| `geopolitics.gold.daily_signal` | One row per country, per day: signal type, direction, strength, confidence |
| `geopolitics.gold.signal_history` | Append-only log of every signal ever generated — audit trail |
| `geopolitics.gold.active_alerts` | Current open alerts (signals not yet resolved) |

---

## II. The Signal Rules: Translating GRI Into a View

The signal generator does not try to be clever. It applies a rule set derived from the validation findings. Rules are defined *before* you see daily output, and changed only with explicit justification logged in the investment log — not based on how you feel about last week's price action.

### Rule Set v1 (base case — to be recalibrated after validation):

```python
# Signal rule definitions
# Adjust thresholds based on your actual Tier 1 validation results

SIGNAL_RULES = {

    # CRISIS signal: GRI z-score extreme + momentum positive
    "CRISIS": {
        "condition": "gri_zscore > 2.5 AND gri_momentum_7d > 0",
        "direction": "risk_off",
        "assets": {
            "equity_etf":  {"view": "short_bias",  "horizon_days": 22, "size": "half"},
            "fx":          {"view": "short_bias",  "horizon_days": 22, "size": "full"},
            "commodity":   {"view": "long_bias",   "horizon_days": 10, "size": "half"},  # energy only
        },
        "safe_haven_add": True,   # adds GLD / DXY long signal
        "confidence": "medium",   # validated at p < 0.05 in Tier 1 (assumed)
    },

    # ELEVATED signal: GRI z-score elevated but not extreme
    "ELEVATED": {
        "condition": "gri_zscore BETWEEN 1.5 AND 2.5 AND gri_momentum_7d > 0",
        "direction": "risk_off",
        "assets": {
            "equity_etf":  {"view": "neutral",     "horizon_days": 22, "size": None},
            "fx":          {"view": "short_bias",  "horizon_days": 10, "size": "quarter"},
            "commodity":   {"view": "neutral",     "horizon_days": 10, "size": None},
        },
        "safe_haven_add": False,
        "confidence": "low",
    },

    # DEESCALATION signal: GRI falling from elevated level
    "DEESCALATION": {
        "condition": "gri_zscore > 1.0 AND gri_momentum_7d < -0.2",
        "direction": "risk_on",
        "assets": {
            "equity_etf":  {"view": "long_bias",   "horizon_days": 22, "size": "quarter"},
            "fx":          {"view": "neutral",     "horizon_days": 10, "size": None},
        },
        "safe_haven_add": False,
        "confidence": "low",   # counter-trend signals are inherently lower confidence
    },

    # NORMAL: No signal. GRI within one standard deviation, no momentum trigger.
    "NORMAL": {
        "condition": "gri_zscore BETWEEN -1.0 AND 1.5",
        "direction": "neutral",
        "assets": {},
        "safe_haven_add": False,
        "confidence": None,
    },
}
```

**Critical design principle:** Size labels ("full", "half", "quarter") are deliberately relative, not absolute. The signal generator does not specify dollar amounts — that is Bolo's decision. The signal specifies direction and relative conviction. This preserves the human-in-the-loop constraint from the PROJECT_FOUNDATION.md: the CEO recommends, Bolo executes.

---

## III. The Signal Generator Notebook

```python
# /Workflows/signal/gri_signal_generator.py
# Depends on: gdelt_gold_gri, market_data_silver
# Output: geopolitics.gold.daily_signal, geopolitics.gold.active_alerts
# Schedule: daily @ 08:00 UTC (30 minutes after gdelt_gold_gri completes)

from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import StringType, DoubleType, DateType, BooleanType
from datetime import datetime, timedelta

spark = SparkSession.builder.getOrCreate()

TODAY = datetime.utcnow().date()
SIGNAL_DATE = (TODAY - timedelta(days=1)).strftime("%Y-%m-%d")  # yesterday's GRI → today's signal

print(f"Generating signals for GRI date: {SIGNAL_DATE}")

# ============================================================
# STEP 1: Load GRI scores for signal date
# ============================================================

gri = spark.read.table("geopolitics.gold.country_gri") \
           .filter(F.col("event_date") == F.lit(SIGNAL_DATE)) \
           .select(
               "country_iso3",
               "event_date",
               "gri",
               "gri_zscore",
               "gri_momentum_7d",
               "risk_regime",
               "tension_score",
               "bilateral_escalation_flag",
               "thematic_score",
           )

print(f"GRI rows loaded: {gri.count()} countries")

# ============================================================
# STEP 2: Classify each country into signal category
# ============================================================

signals = (gri
    .withColumn("signal_type",
        F.when(
            (F.col("gri_zscore") > 2.5) & (F.col("gri_momentum_7d") > 0),
            F.lit("CRISIS")
        ).when(
            (F.col("gri_zscore") > 2.5) & (F.col("gri_momentum_7d") <= 0),
            F.lit("CRISIS_PEAK")    # z-score extreme but momentum turning — possible de-escalation
        ).when(
            (F.col("gri_zscore") >= 1.5) & (F.col("gri_zscore") <= 2.5) & (F.col("gri_momentum_7d") > 0),
            F.lit("ELEVATED")
        ).when(
            (F.col("gri_zscore") > 1.0) & (F.col("gri_momentum_7d") < -0.2),
            F.lit("DEESCALATION")
        ).otherwise(F.lit("NORMAL"))
    )
    .withColumn("direction",
        F.when(F.col("signal_type").isin("CRISIS", "CRISIS_PEAK", "ELEVATED"), F.lit("risk_off"))
         .when(F.col("signal_type") == "DEESCALATION", F.lit("risk_on"))
         .otherwise(F.lit("neutral"))
    )
    .withColumn("confidence",
        F.when(F.col("signal_type") == "CRISIS", F.lit("medium"))
         .when(F.col("signal_type") == "CRISIS_PEAK", F.lit("low"))
         .when(F.col("signal_type") == "ELEVATED", F.lit("low"))
         .when(F.col("signal_type") == "DEESCALATION", F.lit("low"))
         .otherwise(F.lit(None).cast(StringType()))
    )
    .withColumn("signal_date", F.lit(TODAY.isoformat()))
    .withColumn("valid_thru",
        # Signal is valid for the horizon of the underlying rule
        # CRISIS/ELEVATED → 22 trading days ≈ calendar 31 days
        F.when(F.col("signal_type").isin("CRISIS", "ELEVATED"),
            F.date_add(F.col("signal_date"), 31)
        ).when(F.col("signal_type") == "CRISIS_PEAK",
            F.date_add(F.col("signal_date"), 15)
        ).when(F.col("signal_type") == "DEESCALATION",
            F.date_add(F.col("signal_date"), 22)
        ).otherwise(F.lit(None).cast(DateType()))
    )
)

# ============================================================
# STEP 3: Write daily_signal table (overwrite today's rows)
# ============================================================

(signals
    .filter(F.col("signal_type") != "NORMAL")  # only write non-trivial signals
    .write
    .format("delta")
    .mode("overwrite")
    .option("replaceWhere", f"signal_date = '{TODAY.isoformat()}'")
    .saveAsTable("geopolitics.gold.daily_signal"))

crisis_count   = signals.filter(F.col("signal_type").isin("CRISIS", "CRISIS_PEAK")).count()
elevated_count = signals.filter(F.col("signal_type") == "ELEVATED").count()
deesc_count    = signals.filter(F.col("signal_type") == "DEESCALATION").count()

print(f"Signals generated: {crisis_count} CRISIS | {elevated_count} ELEVATED | {deesc_count} DEESCALATION")

# ============================================================
# STEP 4: Append to signal_history (audit trail — never overwrite)
# ============================================================

(signals
    .withColumn("_generated_utc", F.current_timestamp())
    .write
    .format("delta")
    .mode("append")
    .saveAsTable("geopolitics.gold.signal_history"))

# ============================================================
# STEP 5: Build active_alerts — only countries with open signals
# ============================================================

# A country is in active alert if it has a CRISIS or ELEVATED signal
# with valid_thru in the future, and the country has NOT had a NORMAL
# reading for 3+ consecutive days since the signal was triggered.

# For v1: simplified — any country with a current CRISIS or ELEVATED signal
# is in active alert. De-escalation closes the alert.

active = (signals
    .filter(F.col("signal_type").isin("CRISIS", "CRISIS_PEAK", "ELEVATED"))
    .select(
        "country_iso3",
        "signal_type",
        "direction",
        "gri_zscore",
        "gri_momentum_7d",
        "risk_regime",
        "signal_date",
        "valid_thru",
        "confidence",
    )
    .withColumn("alert_triggered_date", F.col("signal_date"))
)

(active.write
    .format("delta")
    .mode("overwrite")
    .option("replaceWhere", f"signal_date = '{TODAY.isoformat()}'")
    .saveAsTable("geopolitics.gold.active_alerts"))

print(f"Active alerts written: {active.count()} countries")

# ============================================================
# STEP 6: Print signal summary (this becomes the CEO morning email)
# ============================================================

print("\n" + "="*60)
print(f"GRI SIGNAL SUMMARY — {TODAY.isoformat()}")
print("="*60)

summary = signals.filter(F.col("signal_type") != "NORMAL") \
                 .orderBy(F.col("gri_zscore").desc()) \
                 .select("country_iso3", "signal_type", "direction", "gri_zscore",
                         "gri_momentum_7d", "risk_regime", "confidence") \
                 .toPandas()

if summary.empty:
    print("No active signals today. All countries reading NORMAL.")
else:
    print(summary.to_string(index=False))

print("="*60)
```

---

## IV. Position Sizing Logic — The Decision Bridge

The signal generator outputs *direction* and *relative size*. Converting that to actual position sizing requires one more layer: the **portfolio constraint table**, which Bolo maintains and updates manually.

```sql
-- geopolitics.gold.portfolio_constraints
-- Bolo updates this manually when risk appetite changes

CREATE TABLE IF NOT EXISTS geopolitics.gold.portfolio_constraints (
    constraint_id       STRING,
    asset_class         STRING,         -- 'equity_etf', 'fx', 'commodity'
    max_position_pct    DOUBLE,         -- of total portfolio; e.g. 0.05 = 5%
    size_full           DOUBLE,         -- 'full' signal → this % of portfolio
    size_half           DOUBLE,
    size_quarter        DOUBLE,
    currency            STRING,         -- 'USD'
    notes               STRING,
    effective_date      DATE,
    _updated_by         STRING
)
USING DELTA;

-- Example initial values:
INSERT INTO geopolitics.gold.portfolio_constraints VALUES
    ('C001', 'equity_etf', 0.20, 0.10, 0.05, 0.025, 'USD', 'ETF positions; max 20% total equity book', '2026-09-04', 'Bolo'),
    ('C002', 'fx',         0.15, 0.075, 0.037, 0.019, 'USD', 'FX book; 15% max notional', '2026-09-04', 'Bolo'),
    ('C003', 'commodity',  0.20, 0.10, 0.05, 0.025, 'USD', 'Commodity book; max 20%', '2026-09-04', 'Bolo');
```

The signal generator can optionally join to this table and output dollar-equivalent recommendations. But the CEO position: **do not automate the final sizing decision.** The signal says how much conviction the data supports. Bolo decides whether to act, given personal tax situation, existing positions, and liquidity constraints that the model cannot see.

---

## V. The Morning Alert — Closing the Loop

The signal generator's `print()` output flows into the Databricks job notification. But that is a passive format — Bolo has to open the job run to see it. To close the loop actively, the CEO session reads the `daily_signal` table each morning and includes it in the morning email.

**What the morning signal summary looks like:**

```
GRI SIGNAL SUMMARY — 2026-09-04
═══════════════════════════════════

CRISIS (risk-off):
  TUR  GRI z-score: 3.14  momentum: +0.38  regime: CRISIS
        → Suggested: short TRY/USD (half), short TUR ETF (quarter)
        → Horizon: 22 days | Confidence: medium
        → Safe haven add: GLD / DXY long (quarter)

ELEVATED (risk-off):
  BRA  GRI z-score: 1.72  momentum: +0.21  regime: ELEVATED
        → Suggested: short BRL/USD (quarter)
        → Horizon: 10 days | Confidence: low

DEESCALATION (risk-on):
  ISR  GRI z-score: 1.15  momentum: -0.31  regime: ELEVATED → declining
        → Suggested: long EIS ETF (quarter)
        → Horizon: 22 days | Confidence: low

NORMAL: 192 countries — no signal

═══════════════════════════════════
Active alerts total: 3 countries
GRI Health Check: Information Ratio (rolling 90d) = 0.41 [WEAK SIGNAL]
```

The **IR health check** is the most important line. It tells Bolo whether to weight the signal heavily or treat it as informational. At IR < 0.3, the signal is noise — read it, but don't act on it. At IR > 0.5, the signal has earned its place in the decision process.

---

## VI. What Comes After This Build

The signal generator is the boundary between Phase 1 (data and measurement) and Phase 2 (intelligence and signal). You have now built the full Phase 1 architecture:

```
Phase 1 — COMPLETE (in architecture; Bolo to validate in Databricks):
✓ GDELT Bronze: raw event ingestion
✓ GDELT Silver: country/bilateral/thematic aggregations
✓ Gold (GRI): composite risk score, z-scored, with regime classification
✓ Market Data Bronze/Silver: yfinance OHLCV → daily returns, forward windows
✓ Validation Layer: event study, factor quintile, commodity theme signal
✓ Signal Generator: daily GRI → structured risk-off/risk-on signal
✓ Portfolio Constraints: human-maintained sizing table

Phase 2 — NEXT (to be directed by CEO based on validation results):
□ GRI Weight Recalibration (if validation weak — Outcome B/C)
□ Walk-Forward Validation Framework (if Outcome D — overfitting suspected)
□ Sovereign CDS Integration (higher-conviction signal than ETF/FX)
□ Signal Generator v2 (incorporates macro regime overlay — VIX, DXY, yield curve)
□ Databricks AI/BI Dashboard (CEO + Bolo monitoring layer)
```

**The CEO decision rule:** When the validation run is complete and the IR is confirmed:
- IR > 0.5 → proceed to Phase 2 signal expansion and begin tracking live signals in the investment log
- IR 0.2–0.5 → recalibrate GRI weights before Phase 2; the signal exists but is not strong enough to trade on
- IR < 0.2 → diagnose failing components per the Lesson 295 Honest Verdict Framework before any further Phase 2 work

---

## Investment Implications

**The signal generator is the instrument that converts analysis into accountability.**

Once the signal generator is live, every morning the CEO has a position: "The GRI says TUR is in CRISIS regime, the view is risk-off on TRY/USD." That view is logged, timestamped, and will be evaluated against what TRY/USD actually does over the next 22 days. There is no escape from the score.

This is the structural advantage of building the infrastructure before issuing recommendations: the framework forces discipline. A human analyst can shift their conviction after the fact and tell themselves they were "always kind of cautious on that one." A timestamped signal record cannot be revised. It says what it said.

**For the portfolio right now:** No GRI-based additions until the validation IR is confirmed above 0.3. The macro thesis (long real assets in a multipolar world) remains valid on structural reasoning. The GRI, if it works, amplifies that thesis with tactical precision — it tells you *when* the structural thesis is most acutely being repriced. But it cannot replace the thesis.

---

## Databricks Angle

**This lesson's build output:**
- `geopolitics.gold.daily_signal` — one row per actionable country per day
- `geopolitics.gold.signal_history` — append-only audit log (never overwrite)
- `geopolitics.gold.active_alerts` — currently open geopolitical risk signals
- `geopolitics.gold.portfolio_constraints` — Bolo's sizing table (manual)

**Pipeline addition:**
```
gdelt_gold_gri (08:00 UTC)
    → gri_signal_generator (08:30 UTC)
        → CEO morning email pull (09:00 UTC) ← the CEO autonomous session reads this
```

**Key engineering decision:** `signal_history` uses `append` mode, never `overwrite`. This is your audit trail. If you later recalibrate GRI weights, the historical signals remain as-generated, allowing you to retrospectively evaluate whether the old weight set was better or worse than the new one. Never rewrite history.

**Next Databricks session directive:** After running the first validation (market_data_bronze → market_data_silver → validation_event_study), bring the IR result back to the CEO session. The CEO will issue the Phase 2 directive based on Outcome A/B/C/D from Lesson 295. If IR > 0.3, the `gri_signal_generator` notebook above is the next thing to deploy.

---

## Key Concepts This Lesson

1. **Signal vs. research** — a result that lives in a notebook is a research artifact; a result that runs daily with defined rules and a timestamped output is a signal; only the latter can be audited and improved
2. **Rule-based signal generation** — signal rules are defined from theory *before* you see live output; changing rules based on recent performance is not calibration, it is curve-fitting
3. **The human-in-the-loop constraint** — the signal generator specifies direction and relative conviction; position sizing remains a human decision, preserving the CEO/Operator boundary in PROJECT_FOUNDATION.md
4. **Signal history append-only** — the audit trail that makes retrospective evaluation honest; if you can rewrite history, you cannot learn from mistakes
5. **IR as the live health metric** — the Information Ratio computed on the rolling 90-day window is the signal health indicator; it tells you, in real time, whether the GRI is still working as the world evolves

---

## Reflection Questions

1. **The timing problem at productization:** The signal generator runs at 08:30 UTC after the GRI completes. European equity markets open at 08:00 UTC (London). Asian markets have already closed. Does your signal actually reach Bolo in time to act on it for European market opens — and if not, should the pipeline schedule be moved earlier, or should the signal specify "valid from next market open" rather than "valid from today"?

2. **The regime change problem:** The signal rules above treat each day independently — a country either is or is not in CRISIS today. But geopolitical crises evolve: a country enters CRISIS, stays there for weeks, then de-escalates. If you short TRY/USD on the first CRISIS signal, should you exit at the defined 22-day horizon regardless of whether GRI is still elevated? Or should the exit rule be "close when GRI drops below z-score 1.5" rather than a fixed calendar date? What are the risks of each approach?

3. **The portfolio constraint table:** You've designed the portfolio constraint table as a manually maintained Delta table. This means Bolo updates it once and it stays fixed until changed. What event would cause you to change the `size_full` percentage for FX positions — a change in total portfolio size, a change in GRI validation strength, or a change in market liquidity for EM currency pairs? Who decides (CEO, Bolo, or both together) and what is the process for updating it?

---

## Questions for Next Session

- **Lesson 298:** The Databricks AI/BI Dashboard — building the visual monitoring layer for the signal generator. The CEO will specify the 5 key charts that need to be on the dashboard: GRI map, signal timeline, IR rolling metric, active alerts table, and validation equity curve.
- **Bolo's validation run:** As soon as the Tier 1 event study returns a result, bring the IR number to the CEO session. The Phase 2 directive depends on it.
- **Spaced repetition:** Revisit Lesson 63 (Multipolarity Premium) — does the current GRI signal, if validated, confirm the structural thesis that multipolar-world geopolitical risk is structurally elevated vs. the 2010–2019 baseline? If the GRI IR is positive, that is empirical evidence that geopolitical risk is being systematically mispriced. That is the entire investment thesis.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 297 delivered: 2026-09-04*
