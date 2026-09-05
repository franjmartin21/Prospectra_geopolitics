# Lesson 303 — The Auditable Investment Track Record: Closing the Loop

**Date:** 2026-09-05
**Session Type:** Daily Lesson
**Lesson Number:** 303 / ongoing
**Topic:** Phase 3 Launch — Building an Auditable Track Record That Compounds
**Curriculum Arc:** Databricks Build Module — Phase 3, Lesson 1 (from signal to outcome to learning)

---

## Opening Question

*The ISG has now been live for several weeks. It has produced 14 signals — directional views on Brent crude, EUR/USD, copper, and two EM sovereign spreads. Some of those views are still open. Some have expired. You don't actually know which ones were right.*

**"If you can't measure whether your signals are generating alpha, are you running an investment process or an expensive opinion service?"**

This is the threshold between a tool and a framework. A tool generates signals. A framework tracks them, measures them, learns from them, and improves. The Auditable Investment Track Record is what makes the entire Prospectra system a framework — and it is what eventually makes it worth something commercially.

Without it, you have a very good information feed. With it, you have a track record — and track records compound.

---

## I. Why Track Records Are Strategically Irreplaceable

Track records are not bureaucratic housekeeping. They serve three distinct and irreplaceable functions:

### 1. Signal Quality Measurement
You cannot improve what you do not measure. The ISG translates GRI/CPM/RCD inputs into directional positions. Whether those positions are systematically correct, systematically early, or systematically wrong in specific regime types — you will only know if you record outcomes against positions.

Over 12–18 months of signal data, you can answer:
- Does a Hard Regime Shift (RCD) + CPS > 0.65 (CPM) reliably predict commodity price increases within 90 days?
- Does GRI level 80+ in a producer country reliably expand sovereign spreads?
- Which asset class responds most predictably to geopolitical signals? With what lag?

These are empirical questions. The track record is the dataset that answers them.

### 2. Accountability and Falsification
Every ISG signal includes a kill switch — a specific condition that closes the position. Recording when those conditions are triggered (or when they should have been) is how you enforce intellectual honesty. Without outcome tracking, you will unconsciously remember your wins and forget your losses. This is not a character flaw — it is a universal cognitive bias. The track record is the structural solution.

### 3. Commercial Value Creation
If Prospectra ever moves to commercial stage (Goal 3, PROJECT_FOUNDATION §3), the track record *is the product*. Not the methodology. Not the dashboards. The demonstrated, auditable, falsifiable record of geopolitical signal → investment outcome. A three-year track record with documented methodology is fundable. A 90-day track record with no documentation is a pitch deck.

Every lesson we log now is compounding toward that asset.

---

## II. The Structure of an Auditable Investment Log

The `reports/investment_log.md` file, referenced throughout the ISG lesson, needs a specific schema to be analytically useful — not just humanly readable.

### Required Fields Per Log Entry

| Field | Type | Purpose |
|---|---|---|
| `signal_id` | String (e.g., ISG-2026-047) | Unique identifier for retrieval and cross-referencing |
| `date_issued` | Date | When the signal was generated |
| `source_signals` | Struct | GRI level + CPM CPS score + RCD regime type at time of issue |
| `asset_class` | Enum | COMMODITY / FX / EM_EQUITY / EM_SOVEREIGN / DM_EQUITY |
| `instrument` | String | Specific instrument (e.g., Brent crude, USD/BRL, Brazil 5Y CDS) |
| `direction` | Enum | LONG / SHORT / UNDERWEIGHT / OVERWEIGHT |
| `size_tier` | Enum | S1 / S2 / S3 (small/medium/full position) |
| `thesis` | Text | One paragraph: why this position, what structural dynamic drives it |
| `horizon` | Integer | Target holding period in days (min 180, per investment philosophy) |
| `kill_switch` | Text | The specific, observable condition that closes this position |
| `date_closed` | Date | When the position was exited (null if still open) |
| `close_reason` | Enum | KILL_SWITCH_TRIGGERED / HORIZON_EXPIRED / THESIS_INVALIDATED / SIGNAL_REVERSAL |
| `outcome_direction` | Enum | WIN / LOSS / DRAW / STILL_OPEN |
| `asset_return_pct` | Float | Actual asset class return over holding period |
| `notes` | Text | Post-mortem: was the thesis right? Was the timing right? What would you do differently? |

The most important field is the last one: `notes`. This is where the framework learns.

### The Schema Philosophy

Notice that "outcome" is not simply WIN/LOSS. A position can expire at horizon with a positive return (WIN), but the thesis can still be wrong — the asset moved for unrelated reasons. Conversely, a position can be closed by kill-switch at a loss while the underlying thesis turns out to be correct over a longer horizon. The `notes` field is where you distinguish *was I right?* from *did I make money?* These are different questions.

The long-horizon investor tracks both, and prioritizes understanding the first.

---

## III. Databricks Track Record Analytics Layer

The track record becomes analytically powerful when it lives in Databricks as a structured delta table — not just a markdown file.

### Architecture

```
reports/investment_log.md
        ↓ (ingestion via CEO morning note pipeline)
investment_log_bronze (raw log entries, append-only)
        ↓ (parsing + enrichment)
investment_log_silver (structured schema above + asset price joins)
        ↓ (signal performance analytics)
investment_log_gold (signal quality metrics by regime type, asset class, horizon)
```

The Gold layer produces the metrics you actually want:

```python
# Gold Layer: Signal Performance by Input State
SELECT
    rcd_regime_type,
    asset_class,
    direction,
    COUNT(*) as n_signals,
    SUM(CASE WHEN outcome_direction = 'WIN' THEN 1 ELSE 0 END) / COUNT(*) as win_rate,
    AVG(asset_return_pct) as avg_return,
    PERCENTILE(asset_return_pct, 0.25) as p25_return,
    PERCENTILE(asset_return_pct, 0.75) as p75_return,
    AVG(DATEDIFF(date_closed, date_issued)) as avg_holding_days
FROM investment_log_silver
WHERE outcome_direction != 'STILL_OPEN'
GROUP BY rcd_regime_type, asset_class, direction
ORDER BY avg_return DESC
```

This table answers the core question: **under which input conditions does each asset class signal most reliably generate positive returns?**

Over time, this feeds back into the ISG — you can weight signals by historically demonstrated reliability rather than pure rules-based logic. This is how the system earns the right to increase conviction (size tier) on specific signal types.

### Signal Decay Analysis

A critical metric the Gold layer should produce is signal decay: how does the win rate change as a function of time-in-position?

```python
# Signal Decay: Win Rate by Days-in-Position Bucket
SELECT
    FLOOR(DATEDIFF(date_closed, date_issued) / 30) * 30 as days_in_position_bucket,
    COUNT(*) as n_signals,
    AVG(CASE WHEN outcome_direction = 'WIN' THEN 1.0 ELSE 0.0 END) as win_rate,
    AVG(asset_return_pct) as avg_return
FROM investment_log_silver
WHERE outcome_direction != 'STILL_OPEN'
GROUP BY 1
ORDER BY 1
```

If win rates peak at 90–180 days and decay after 12 months, you know the optimal holding horizon for geopolitical signals. If they peak at 12+ months, your intuition about long-horizon advantage is correct. The data tells you.

---

## IV. The Feedback Loop Architecture

The track record is not a static archive. It is a live input to the ISG. The feedback architecture works as follows:

```
[New Geopolitical Event]
        ↓
[GRI + CPM + RCD update]
        ↓
[ISG Signal Generation]
        ↓
[Log Entry Created — investment_log.md + investment_log_bronze]
        ↓
[Position Held Over Horizon]
        ↓
[Kill Switch Check (daily)]
        ↓
[Position Closed — date_closed, close_reason, outcome written]
        ↓
[Gold Layer Updated — signal performance metrics refreshed]
        ↓
[ISG Calibration — quarterly review of size tier thresholds and confidence weights]
        ↓
[Repeat — next signal now enters a more calibrated system]
```

This is a compounding loop. Every closed position makes the next signal slightly more precise. After 24 months of data, the ISG is no longer a rules-based system with arbitrary thresholds — it is an empirically-calibrated signal generator with historically validated conviction levels.

This is the difference between Month 1 Prospectra and Year 2 Prospectra.

---

## V. Investment Implications

Track record architecture has direct investment implications that are easy to miss:

**Alpha Attribution Problem:** Most active managers cannot tell you whether their returns came from geopolitical insight, macro timing, sector rotation, or noise. They mix signals and can't decompose returns. The Prospectra track record is designed to avoid this from day one — every position is tagged to a specific signal type (GRI-driven / CPM-driven / RCD-regime / composite), enabling clean attribution.

**Conviction Calibration:** The ISG currently uses three size tiers (S1/S2/S3) based on input signal strength. After 12+ months of data, those tiers can be recalibrated empirically. If S1 signals in Hard Regime Shift contexts have historically performed as well as S2 signals in Soft Regime contexts, you raise the S1 conviction weight. This is systematic improvement — not gut feel.

**Risk Model Input:** A well-structured track record also feeds a risk model. If you know the historical win rate distribution by signal type, you can estimate portfolio-level drawdown under the assumption that X% of current signals fail simultaneously. This is how you build geopolitical risk management, not just geopolitical signal generation.

---

## VI. Databricks Angle

**This session's build task:**

1. **Create `investment_log_bronze` Delta table** in your Databricks workspace:
   ```python
   CREATE TABLE IF NOT EXISTS geopolitical_intelligence.investment_log_bronze (
     signal_id STRING,
     date_issued DATE,
     gri_level FLOAT,
     cps_score FLOAT,
     rcd_regime_type STRING,
     asset_class STRING,
     instrument STRING,
     direction STRING,
     size_tier STRING,
     thesis STRING,
     horizon_days INTEGER,
     kill_switch STRING,
     date_closed DATE,
     close_reason STRING,
     outcome_direction STRING,
     asset_return_pct FLOAT,
     notes STRING,
     ingest_timestamp TIMESTAMP
   )
   USING DELTA
   LOCATION 'dbfs:/geopolitical_intelligence/investment_log_bronze/'
   ```

2. **Backfill from `reports/investment_log.md`** — parse the existing markdown log into structured rows and insert into bronze. Use a Python notebook with pandas + Delta Lake write.

3. **Build the Silver layer join** — for each closed signal entry, join to the `market_data_bronze` table to pull actual asset returns over the holding period (date_issued → date_closed). Compute `asset_return_pct` automatically rather than requiring manual entry.

4. **Build the first Gold view** — the signal performance by regime type table from Section III above. This becomes a live tile in the AI/BI dashboard.

**Relevant datasets:**
- Internal: `investment_log.md` (backfill source)
- Internal: `market_data_bronze` (asset return computation)
- Internal: `gri_gold`, `commodity_pressure_model_silver`, `regime_change_detector_silver` (input state reconstruction for historical signals)

---

## Key Concepts Covered

1. **Track record as strategic asset** — not admin, but the core product in a commercial context
2. **Auditable signal schema** — the 14 required fields and why each one exists
3. **Outcome vs. thesis accuracy** — the distinction that prevents self-deception
4. **Track record analytics architecture** — Bronze → Silver → Gold pipeline for signal performance
5. **Signal decay analysis** — finding the optimal holding horizon empirically
6. **Feedback loop architecture** — how outcome data recalibrates the ISG over time
7. **Alpha attribution** — designing for clean decomposition from day one

---

## Reflection Questions

1. The ISG currently assigns size tiers (S1/S2/S3) based on input signal strength alone. After 12 months of track record data, what additional factor would you incorporate into size tier determination — and what data would you need to compute it?

2. A signal is closed at horizon (180 days) with a +8% return on Brent crude. The thesis was "Russia sanctions will constrain Black Sea export capacity, tightening global supply." Russia actually resolved the sanctions dispute in Month 3, but OPEC+ independently cut production in Month 4, sustaining the price move. How would you classify this in the `notes` field, and what does it mean for ISG calibration?

3. The track record Gold layer shows that your win rate on FX signals in Hard Regime Shift contexts is 34% — statistically worse than random. What are the three possible explanations for this, and how would you test each one using existing data in your Databricks stack?

---

## Questions for Next Session (Spaced Repetition Hook)

- The feedback loop from track record → ISG calibration requires a minimum sample size before it becomes statistically meaningful. What is a reasonable threshold, and how does this change your approach to building conviction in Year 1 vs. Year 2?
- How does the Prospectra track record architecture compare to how institutional hedge funds document signal efficacy — and what are we doing better or worse?

---

## CEO Portfolio Note

The track record layer is Phase 3's most important deliverable — more important than the dashboards. Dashboards show you what's happening today. The track record shows you whether you've been right over time. One of these compounds. **Build the investment_log Delta table this week.** Every open ISG signal should be entered before the end of September. The 3-month clock from April is behind us — but the Year 1 success criteria (6+ months of tracked recommendations) still needs to be hit. Start the clock now.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Session date: 2026-09-05*
