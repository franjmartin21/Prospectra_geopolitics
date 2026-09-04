# Lesson 298 — Databricks AI/BI Dashboard: Building the Signal Monitoring Layer

**Date:** 2026-09-04
**Session Type:** Daily Lesson
**Lesson Number:** 298 / ongoing
**Topic:** Databricks Build Module — AI/BI Dashboard for GRI Signal Monitoring
**Curriculum Arc:** Databricks Build Module — Lesson 10 (the visibility layer: turning a pipeline into a command center)

---

## Opening Question

*The signal generator is built. Every morning it produces a structured table: which countries are in CRISIS, which are ELEVATED, which are de-escalating, and what the IR is doing.*

Here is the question that separates a pipeline from a product:

**"If Bolo opens his laptop at 7am and has 90 seconds before his first call, what does he see — and does it tell him what matters?"**

A dashboard that requires scrolling, drilling, or interpretation under time pressure is not a dashboard. It is a data portal. The CEO's standard is different: **the five most important things about the current state of the world should be visible, interpreted, and actionable in one screen, without clicking.**

This lesson specifies exactly that: five charts, one screen, zero ambiguity.

---

## I. Dashboard Design Philosophy

Before writing a single SQL query, commit to these three constraints:

### Constraint 1 — One screen, no scroll
The monitoring dashboard must be designed for a 1440×900 viewport (a 13-inch laptop). If information requires scrolling, it is not on the monitoring dashboard — it belongs in a drill-through report. Every visual element on the main view should be immediately readable.

### Constraint 2 — Signal, not data
The dashboard does not show raw GDELT event counts. It shows *interpreted* outputs: GRI scores, signal classifications, IR health, active alerts. The transformation from raw data to signal already happened in the pipeline. The dashboard renders the signal, not the data.

### Constraint 3 — Red is real
Color coding on this dashboard has exactly one meaning: red means something requires attention. Never use red for decorative contrast, gradient shading, or to make a chart look more sophisticated. If everything is red, nothing is red. The dashboard earns its authority by being conservative with alarm.

---

## II. The Five Charts

### Chart 1 — GRI World Map (Full Width, Top)

**What it shows:** A choropleth world map where each country's fill color represents its current GRI z-score.

**Color scale:**
```
z < 0.0:     Deep teal       (below historical baseline)
0.0–1.0:     Light grey      (NORMAL regime)
1.0–1.5:     Amber           (watch list — elevated but no signal)
1.5–2.5:     Orange          (ELEVATED signal)
> 2.5:       Red             (CRISIS signal)
```

**Key design decision:** The map does NOT show every country equally. Countries without significant GDELT event data (often small Pacific islands, Bhutan, etc.) should render in a neutral grey rather than blue/teal — their "low" GRI score is an artifact of data absence, not genuine low risk. Filter to countries with at least 50 GDELT events in the trailing 30 days before rendering their GRI score.

**SQL backing query:**
```sql
-- Chart 1: GRI World Map data feed
SELECT
    g.country_iso3,
    g.event_date,
    g.gri,
    g.gri_zscore,
    g.risk_regime,
    g.event_count_30d,
    CASE
        WHEN g.event_count_30d < 50 THEN 'INSUFFICIENT_DATA'
        WHEN g.gri_zscore < 0.0 THEN 'BELOW_BASELINE'
        WHEN g.gri_zscore < 1.0 THEN 'NORMAL'
        WHEN g.gri_zscore < 1.5 THEN 'WATCH'
        WHEN g.gri_zscore < 2.5 THEN 'ELEVATED'
        ELSE 'CRISIS'
    END AS display_regime
FROM geopolitics.gold.country_gri g
WHERE g.event_date = CURRENT_DATE - INTERVAL 1 DAY  -- yesterday's GRI = today's signal
ORDER BY g.gri_zscore DESC
```

---

### Chart 2 — Active Alerts Table (Left Panel, Middle)

**What it shows:** A structured table listing all countries currently in CRISIS or ELEVATED signal, sorted by z-score descending.

**Columns:**
| Country | Signal | GRI z-score | Momentum | Regime | Signal Date | Valid Thru | Direction |
|---------|--------|-------------|----------|--------|-------------|------------|-----------|

**Design rule:** This table has a maximum of 10 rows visible without scroll. If more than 10 countries are in CRISIS/ELEVATED simultaneously, the dashboard is showing a global risk environment — add a "GLOBAL RISK ALERT" banner above the table.

**SQL backing query:**
```sql
-- Chart 2: Active Alerts
SELECT
    a.country_iso3,
    a.signal_type,
    ROUND(a.gri_zscore, 2)          AS gri_zscore,
    ROUND(a.gri_momentum_7d, 3)     AS momentum_7d,
    a.risk_regime,
    a.signal_date,
    a.valid_thru,
    a.direction,
    a.confidence,
    DATEDIFF(a.valid_thru, CURRENT_DATE) AS days_remaining
FROM geopolitics.gold.active_alerts a
WHERE a.signal_date = CURRENT_DATE
ORDER BY a.gri_zscore DESC
LIMIT 10
```

---

### Chart 3 — IR Rolling Health Metric (Right Panel, Middle)

**What it shows:** A single large KPI tile showing the current 90-day rolling Information Ratio of the GRI signal, with a traffic-light indicator and a small sparkline of IR over the past 180 days.

**Traffic light:**
```
IR > 0.5:    Green   — signal is working; weight recommendations accordingly
IR 0.3–0.5: Yellow  — signal has directional value; use with caution
IR 0.2–0.3: Amber   — weak signal; treat as informational only
IR < 0.2:   Red     — signal failing; do NOT act on GRI signals; diagnose root cause
```

**The critical line under the KPI:**
"GRI IR (90d rolling): **0.41 ↑** — Signal valid, confidence LOW. Do not size above quarter positions."

This line is the CEO's standing instruction. It tells Bolo not just the number but what to do with it. The dashboard is making a decision, not presenting data.

**SQL backing query:**
```sql
-- Chart 3: Rolling IR Sparkline
WITH daily_ir AS (
    SELECT
        evaluation_date,
        -- IR calculated in validation layer:
        -- signal_correct / total_signals where signal_correct = directional match
        information_ratio_90d,
        CASE
            WHEN information_ratio_90d > 0.5 THEN 'GREEN'
            WHEN information_ratio_90d > 0.3 THEN 'YELLOW'
            WHEN information_ratio_90d > 0.2 THEN 'AMBER'
            ELSE 'RED'
        END AS ir_status,
        LAG(information_ratio_90d, 1) OVER (ORDER BY evaluation_date) AS prev_ir
    FROM geopolitics.gold.signal_validation_log
    WHERE evaluation_date >= CURRENT_DATE - INTERVAL 180 DAYS
)
SELECT
    evaluation_date,
    information_ratio_90d,
    ir_status,
    CASE
        WHEN information_ratio_90d > prev_ir THEN '↑'
        WHEN information_ratio_90d < prev_ir THEN '↓'
        ELSE '→'
    END AS ir_direction
FROM daily_ir
ORDER BY evaluation_date DESC
```

---

### Chart 4 — Signal Timeline (Full Width, Bottom Left)

**What it shows:** A 90-day stacked bar chart showing, for each day: how many countries were in CRISIS, ELEVATED, DEESCALATION, and NORMAL signal state. The x-axis is date; the y-axis is country count. Stacked bars let Bolo see at a glance whether global risk is expanding, contracting, or stable.

**Why this matters:** A world where 3 countries are in CRISIS and the number is rising looks very different from one where 8 countries were in CRISIS last week and only 3 remain. The direction of the risk pool matters as much as its current size. The timeline makes this visible instantly.

**Annotation layer:** Mark key dates on the x-axis: "GRI deployed", "Validation run 1", any dates where a major geopolitical event made global news. This contextualizes the signal history.

**SQL backing query:**
```sql
-- Chart 4: 90-Day Signal Timeline
SELECT
    signal_date,
    COUNT(CASE WHEN signal_type = 'CRISIS'        THEN 1 END) AS crisis_count,
    COUNT(CASE WHEN signal_type = 'CRISIS_PEAK'   THEN 1 END) AS crisis_peak_count,
    COUNT(CASE WHEN signal_type = 'ELEVATED'      THEN 1 END) AS elevated_count,
    COUNT(CASE WHEN signal_type = 'DEESCALATION'  THEN 1 END) AS deescalation_count
FROM geopolitics.gold.signal_history
WHERE signal_date >= CURRENT_DATE - INTERVAL 90 DAYS
  AND _generated_utc = (
      -- Take only the first signal generation of each day
      -- (in case of reruns, we want the original signal, not the rerun)
      SELECT MIN(_generated_utc)
      FROM geopolitics.gold.signal_history sh2
      WHERE sh2.signal_date = signal_history.signal_date
  )
GROUP BY signal_date
ORDER BY signal_date
```

---

### Chart 5 — Validation Equity Curve (Bottom Right)

**What it shows:** A line chart showing the cumulative return of a hypothetical paper portfolio that followed every GRI signal from the validation period forward. This is the "does the signal make money" visualization.

**Design rule:** This chart must show the paper portfolio against a benchmark — typically a global equity index (MSCI World ETF / VT) or a simple buy-and-hold of the relevant asset class. A signal that outperforms the benchmark in trending markets but underperforms in flat markets is not a good signal — it is just a momentum strategy in disguise.

**What to show:**
- Blue line: GRI signal paper portfolio (cumulative return)
- Grey line: benchmark (MSCI World or VT)
- Shaded red periods: periods when GRI IR < 0.2 (signal was failing — did the portfolio reflect that?)

**The purpose of this chart:** Every week, Bolo and the CEO should look at this chart and ask: "Is the gap between the blue line and the grey line growing, shrinking, or reversing?" A growing gap is evidence the framework is working. A shrinking gap is an early warning. A reversal is a demand for root cause analysis before any further signal-based decisions.

**SQL backing query:**
```sql
-- Chart 5: Validation Equity Curve
WITH signal_returns AS (
    SELECT
        sv.evaluation_date,
        sv.asset_class,
        sv.forward_return_22d,
        sv.signal_direction,
        -- A long signal that returns positive = correct; short signal negative = correct
        CASE
            WHEN sv.signal_direction = 'risk_off' AND sv.forward_return_22d < 0 THEN ABS(sv.forward_return_22d)
            WHEN sv.signal_direction = 'risk_on'  AND sv.forward_return_22d > 0 THEN sv.forward_return_22d
            WHEN sv.signal_direction = 'risk_off' AND sv.forward_return_22d > 0 THEN -sv.forward_return_22d
            WHEN sv.signal_direction = 'risk_on'  AND sv.forward_return_22d < 0 THEN -ABS(sv.forward_return_22d)
            ELSE 0
        END AS pnl_contribution
    FROM geopolitics.gold.signal_validation_log sv
    WHERE sv.evaluation_date >= '2026-07-01'
)
SELECT
    evaluation_date,
    SUM(pnl_contribution)   AS daily_pnl,
    SUM(SUM(pnl_contribution)) OVER (ORDER BY evaluation_date) AS cumulative_pnl
FROM signal_returns
GROUP BY evaluation_date
ORDER BY evaluation_date
```

---

## III. Databricks AI/BI Dashboard — Build Steps

The Databricks AI/BI tool (formerly "Lakeview") is the native dashboard layer inside Databricks. It connects directly to Unity Catalog tables — no export, no Tableau license, no separate BI tool.

### Step-by-step build:

```
1. Open Databricks workspace → New → Dashboard (AI/BI)
2. Name: "GRI Signal Monitor — Live"
3. Connect to Unity Catalog: geopolitics.gold.*

For each chart:
4. Click "+ Add visualization"
5. Write the SQL query (exactly as specified above)
6. Choose chart type:
   Chart 1  → Map (choropleth)
   Chart 2  → Table (with conditional formatting)
   Chart 3  → Counter / KPI tile + sparkline
   Chart 4  → Bar chart (stacked)
   Chart 5  → Line chart (multi-series)

Layout:
7. Drag Chart 1 to full width (top row, spans 12 columns)
8. Chart 2 left panel (middle row, 6 columns)
9. Chart 3 right panel (middle row, 6 columns)
10. Chart 4 bottom left (bottom row, 8 columns)
11. Chart 5 bottom right (bottom row, 4 columns)

Refresh:
12. Set dashboard auto-refresh: every 24 hours at 09:00 UTC
    (30 minutes after signal generator runs)

Access:
13. Share dashboard link with Bolo's email (franjmartin21@gmail.com)
14. Set permissions: "Can View" (read-only; only the CEO session edits the SQL)
```

---

## IV. The Conditional Formatting Rule

For Chart 2 (Active Alerts Table), enable conditional row formatting:

```
Row background:
  signal_type = 'CRISIS'       → background #FFEDED (light red)
  signal_type = 'CRISIS_PEAK'  → background #FFF3ED (light orange)
  signal_type = 'ELEVATED'     → background #FFFBED (light amber)
  signal_type = 'DEESCALATION' → background #EDFFF3 (light green)

days_remaining column:
  < 5 days  → text color RED (signal expiring soon — decide whether to extend or close)
  5–14 days → text color AMBER
  > 14 days → text color DEFAULT
```

The "days remaining" column does something subtle but important: it tells Bolo whether a position opened on a signal is approaching its defined horizon. If you shorted TRY/USD on a CRISIS signal with a 22-day horizon, and it's day 20, the dashboard reminds you: this position's thesis has a clock. Decide before the clock runs out.

---

## V. Adding the CEO Morning Brief to the Dashboard

One additional element that elevates the dashboard from data display to command center: a **CEO Morning Note** text tile.

This is a plain text widget — manually updated by the CEO autonomous session each morning — that says, in 3 sentences, what the CEO thinks about today's signal.

Example:
```
CEO Morning Note — 2026-09-04:
GRI signal shows TUR and EGY in CRISIS regime, BRA ELEVATED.
IR 90d: 0.41 — directional signal valid but sized conservatively.
No new positions recommended; maintain existing risk-off FX hedges.
```

The CEO session writes this note to a single-row Delta table (`geopolitics.gold.ceo_morning_note`) each morning before the dashboard refreshes. The dashboard displays the latest row.

```python
# In the CEO autonomous session — writes the morning note
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp, lit
from datetime import date

spark = SparkSession.builder.getOrCreate()

note_text = """GRI signal shows TUR and EGY in CRISIS regime, BRA ELEVATED.
IR 90d: current — directional signal valid but sized conservatively.
No new positions recommended; maintain existing risk-off FX hedges."""

note_df = spark.createDataFrame([(date.today().isoformat(), note_text)],
                                 ["note_date", "note_text"]) \
               .withColumn("_generated_utc", current_timestamp())

note_df.write.format("delta").mode("overwrite").saveAsTable("geopolitics.gold.ceo_morning_note")
```

---

## Investment Implications

**The dashboard is the accountability mechanism made visible.**

When Bolo opens the dashboard each morning, he sees: where global geopolitical risk is concentrated, whether the signal is working, how many active alerts there are, and in 3 sentences, what the CEO recommends. That is it. That is the investment intelligence product.

The equity curve (Chart 5) is the most honest element. It does not allow selective memory about which signals "worked." It shows the cumulative result of following every signal the GRI generated, against a benchmark, from the beginning. That chart, updated daily, is the living answer to the question: "Is this framework worth using?"

**Portfolio implication for now:** The dashboard does not change the thesis. It makes the thesis testable in real time. Once the dashboard is live and the IR is confirmed (from Lesson 295's validation run), the CEO will issue the first formal signal-based recommendation and log it in the investment log. The validation data sets the position size parameters. The dashboard confirms, daily, whether those parameters remain valid.

---

## Databricks Angle

**Tables created this session:**
- `geopolitics.gold.ceo_morning_note` — single-row table, overwritten daily by CEO session
- (Dashboard references existing Gold layer tables; no new pipeline tables required)

**The dashboard as architecture documentation:** The five charts above collectively document what the GRI pipeline produces. If the pipeline breaks, the charts go blank — the dashboard is also a live health check for every upstream table.

**Suggested pipeline modification:** Add a data freshness check. If `country_gri` has no rows for CURRENT_DATE - 1 DAY, the dashboard should show a "PIPELINE STALE — DATA NOT REFRESHED" warning banner rather than silently showing old data. This prevents Bolo from making decisions on stale signal without realizing it.

```sql
-- Data freshness check (run at dashboard load)
SELECT
    MAX(event_date) AS latest_gri_date,
    DATEDIFF(CURRENT_DATE, MAX(event_date)) AS days_since_refresh,
    CASE
        WHEN DATEDIFF(CURRENT_DATE, MAX(event_date)) > 1 THEN 'STALE'
        ELSE 'FRESH'
    END AS data_status
FROM geopolitics.gold.country_gri
```

---

## Key Concepts This Lesson

1. **One-screen discipline** — a monitoring dashboard that requires navigation has failed; the constraint of one visible screen forces prioritization of signal over data
2. **Red is real** — conservative use of alarm color preserves the credibility of the dashboard; if everything looks urgent, nothing is
3. **The equity curve as accountability** — cumulative paper portfolio vs. benchmark is the single most honest measure of whether the framework is working; it cannot be revised after the fact
4. **CEO Morning Note** — the human interpretation layer above the mechanical signal; three sentences that translate GRI output into a portfolio stance, written by the CEO and visible to Bolo before market open
5. **Data freshness as a first-class concern** — a dashboard showing stale data with no warning is worse than no dashboard; the freshness check is a required element, not an enhancement

---

## Reflection Questions

1. **The benchmark problem:** The equity curve (Chart 5) compares the GRI signal portfolio to MSCI World. But the GRI signal generates risk-off signals on EM countries — the natural benchmark for an EM-focused risk-off signal is not MSCI World but MSCI EM or a VWO ETF. Does your choice of benchmark change whether the signal looks good? What is the honest benchmark for this particular signal type, and does it matter if Bolo's actual portfolio is a mix of US equities, EM FX, and commodities?

2. **The 90-second test:** If you showed the current dashboard mockup to someone who had never seen it and gave them 90 seconds, could they tell you (a) which country has the highest geopolitical risk today, (b) whether the signal is currently reliable, and (c) whether global risk is rising or falling over the past month? If not — which element fails the test, and what would you change?

3. **The CEO Morning Note as a single point of failure:** The CEO Morning Note is manually written by the CEO autonomous session each morning. If the autonomous session fails to run (network error, Databricks downtime, etc.), the note goes stale. Should the dashboard show the note's timestamp so Bolo knows if it's outdated? Or should the note include its own "if you're reading this and it's more than 24 hours old, the autonomous session is offline" warning built into the template?

---

## Questions for Next Session

- **Lesson 299:** Automating the CEO Morning Note — specifying the logic for the autonomous session to read the GRI signal table, compute the summary, write the morning note to Delta, and include it in the daily email. This closes the loop on the full Phase 1 architecture: data → signal → dashboard → alert → decision.
- **Validation priority:** The IR number from the first validation run remains the key dependency for Phase 2. Dashboard is built; signal is live. The only missing piece is whether the signal earns its authority. Bolo: run the validation.
- **Spaced repetition:** Revisit Lesson 295 (GRI Signal Validation) — the Outcome A/B/C/D framework. Now that the dashboard is specified, the question becomes: which of the five charts would look different under each outcome? A weak IR does not mean the dashboard is useless — it means Chart 3 shows red and Chart 5 shows underperformance. The dashboard is the honest witness regardless of what the signal does.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 298 delivered: 2026-09-04*
