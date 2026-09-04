# Lesson 299 — Automating the CEO Morning Note: Closing the Phase 1 Loop

**Date:** 2026-09-04
**Session Type:** Daily Lesson
**Lesson Number:** 299 / ongoing
**Topic:** Databricks Build Module — Autonomous Morning Note Generator
**Curriculum Arc:** Databricks Build Module — Lesson 11 (closing the loop: data → signal → dashboard → alert → decision)

---

## Opening Question

*You have built the pipeline. You have built the signal generator. You have built the dashboard. Every morning, the GRI runs, scores countries, classifies signals, and populates five charts that Bolo can read in 90 seconds.*

Here is the question that determines whether this is a system or a collection of parts:

**"If Bolo never opens the dashboard — if he forgets, or travels, or simply gets pulled into meetings — does anything reach him?"**

The dashboard is a pull mechanism. It waits to be consulted. The CEO Morning Note delivered by email is a push mechanism — it finds Bolo regardless of whether he remembered to look. A system with only a pull mechanism has a failure mode: the days it matters most are often the days the operator is busiest.

Lesson 299 closes the Phase 1 architecture by specifying the logic that transforms GRI signal output into a structured morning note, writes it to Delta, and delivers it to Bolo's inbox every day before he starts work.

---

## I. The Full Phase 1 Architecture (Complete)

Before writing a single line of code, map the complete chain. After this lesson, Phase 1 is closed:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        PHASE 1 — COMPLETE ARCHITECTURE                  │
├──────────────────┬──────────────────────────────────────────────────────┤
│  DATA LAYER      │  GDELT + Yahoo Finance → Bronze Delta tables          │
│  (Lesson 291)    │  Daily ingestion via Databricks Workflow              │
├──────────────────┼──────────────────────────────────────────────────────┤
│  SIGNAL LAYER    │  Bronze → Silver → Gold GRI pipeline                  │
│  (Lessons 292-   │  Event scaling → tone weighting → z-score →           │
│   296)           │  risk regime classification → active alerts            │
├──────────────────┼──────────────────────────────────────────────────────┤
│  VALIDATION      │  IR calculation → Outcome classification →             │
│  (Lesson 295)    │  Position sizing parameters                            │
├──────────────────┼──────────────────────────────────────────────────────┤
│  DASHBOARD       │  5-chart AI/BI monitor → choropleth + alerts +         │
│  (Lesson 298)    │  IR tile + timeline + equity curve                     │
├──────────────────┼──────────────────────────────────────────────────────┤
│  MORNING NOTE    │  THIS LESSON: autonomous note generator →              │
│  (Lesson 299)    │  reads Gold tables → writes structured summary →        │
│                  │  pushes to Delta → CEO email includes it               │
└──────────────────┴──────────────────────────────────────────────────────┘
```

The morning note is the final output stage. It is the system speaking to its operator in plain language: *here is what the world looks like today, here is whether the signal is working, here is what we recommend*.

---

## II. What the Morning Note Must Contain

The CEO Morning Note is not a data dump. It is a decision-ready brief. It must be writable in under 3 seconds of reading time — Bolo should be able to absorb it before his first coffee is finished.

**Mandatory elements (in this order):**

### Element 1 — Signal Status Line (1 sentence)
The single most important fact about today's GRI output.

```
Format: "GRI signal shows [N] countries in CRISIS, [M] ELEVATED, [K] in de-escalation."
Example: "GRI signal shows 2 countries in CRISIS (TUR, EGY), 3 ELEVATED (BRA, ZAF, IDN), 1 de-escalating (RUS)."
```

### Element 2 — IR Health Line (1 sentence)
The current state of signal reliability.

```
Format: "IR 90d: [X.XX] — [GREEN/YELLOW/AMBER/RED]: [action implication]."
Example: "IR 90d: 0.41 — YELLOW: directional signal valid, size positions conservatively."
```

### Element 3 — CEO Recommendation (1 sentence, max 2)
What to do, or what to watch, based on today's signal. This is the CEO's judgment call — not just the data.

```
Format: "[Action/Hold/Watch] — [brief thesis]."
Example: "Hold existing risk-off FX hedges (TRY/USD short) — no new entries until IR confirms above 0.5 or TUR z-score > 3.0."
```

### Element 4 — Alert Flag (conditional, 1 sentence)
Triggered ONLY if something exceptional happened overnight: new CRISIS signal, IR drop below 0.2, or pipeline freshness failure.

```
Format: "⚠ ALERT: [specific trigger]. Action required."
Example: "⚠ ALERT: Pakistan entered CRISIS regime overnight (z=2.71). Review exposure to KSE-100 and PKR positions."
```

If nothing exceptional happened: omit this element entirely. Silence on Element 4 is the correct output on a normal day.

---

## III. The Automation Logic — Python Specification

The CEO morning note generator runs as the final task in the Databricks Workflow, after the GRI pipeline completes. It is a Databricks Notebook task.

### Notebook: `notebooks/ceo_morning_note_generator.py`

```python
# CEO Morning Note Generator — Lesson 299
# Runs daily after GRI pipeline completes.
# Reads Gold layer, computes structured summary, writes to Delta, emails Bolo.

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, lit
from datetime import date, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

spark = SparkSession.builder.getOrCreate()

TODAY = date.today()
YESTERDAY = TODAY - timedelta(days=1)  # GRI signal is based on yesterday's GDELT data
BOLO_EMAIL = "franjmartin21@gmail.com"
CEO_EMAIL = "ceo@prospectra.earth"

# ─────────────────────────────────────────────────────────────
# STEP 1: Read today's active alerts
# ─────────────────────────────────────────────────────────────
alerts_df = spark.sql(f"""
    SELECT
        country_iso3,
        signal_type,
        ROUND(gri_zscore, 2)      AS gri_zscore,
        direction,
        confidence,
        asset_class_signal,
        signal_date,
        valid_thru
    FROM geopolitics.gold.active_alerts
    WHERE signal_date = '{TODAY}'
    ORDER BY gri_zscore DESC
""")
alerts = alerts_df.collect()

crisis_countries    = [r.country_iso3 for r in alerts if r.signal_type in ('CRISIS', 'CRISIS_PEAK')]
elevated_countries  = [r.country_iso3 for r in alerts if r.signal_type == 'ELEVATED']
deescal_countries   = [r.country_iso3 for r in alerts if r.signal_type == 'DEESCALATION']

# ─────────────────────────────────────────────────────────────
# STEP 2: Read current IR health
# ─────────────────────────────────────────────────────────────
ir_row = spark.sql(f"""
    SELECT
        information_ratio_90d,
        CASE
            WHEN information_ratio_90d > 0.5 THEN 'GREEN'
            WHEN information_ratio_90d > 0.3 THEN 'YELLOW'
            WHEN information_ratio_90d > 0.2 THEN 'AMBER'
            ELSE 'RED'
        END AS ir_status,
        evaluation_date
    FROM geopolitics.gold.signal_validation_log
    ORDER BY evaluation_date DESC
    LIMIT 1
""").first()

ir_value  = round(ir_row.information_ratio_90d, 2) if ir_row else None
ir_status = ir_row.ir_status if ir_row else "UNKNOWN"

# ─────────────────────────────────────────────────────────────
# STEP 3: Check data freshness
# ─────────────────────────────────────────────────────────────
freshness_row = spark.sql(f"""
    SELECT
        MAX(event_date) AS latest_gri_date,
        DATEDIFF(CURRENT_DATE, MAX(event_date)) AS days_stale
    FROM geopolitics.gold.country_gri
""").first()

data_stale     = freshness_row.days_stale > 1 if freshness_row else True
latest_gri_date = freshness_row.latest_gri_date if freshness_row else None

# ─────────────────────────────────────────────────────────────
# STEP 4: Compose Element 1 — Signal Status Line
# ─────────────────────────────────────────────────────────────
def format_country_list(countries):
    if not countries:
        return "none"
    return ", ".join(countries[:5])  # cap at 5 to keep line readable

if crisis_countries:
    crisis_str = f"{len(crisis_countries)} in CRISIS ({format_country_list(crisis_countries)})"
else:
    crisis_str = "0 in CRISIS"

if elevated_countries:
    elevated_str = f"{len(elevated_countries)} ELEVATED ({format_country_list(elevated_countries)})"
else:
    elevated_str = "0 elevated"

if deescal_countries:
    deescal_str = f"{len(deescal_countries)} de-escalating ({format_country_list(deescal_countries)})"
else:
    deescal_str = ""

element_1 = f"GRI signal shows {crisis_str}, {elevated_str}" + (f", {deescal_str}." if deescal_str else ".")

# ─────────────────────────────────────────────────────────────
# STEP 5: Compose Element 2 — IR Health Line
# ─────────────────────────────────────────────────────────────
ir_action_map = {
    "GREEN":   "signal working; weight recommendations at full parameters.",
    "YELLOW":  "signal directionally valid; size positions conservatively.",
    "AMBER":   "weak signal; treat as informational only; no new entries.",
    "RED":     "signal failing. DO NOT act on GRI signals. Run diagnostics.",
    "UNKNOWN": "IR unavailable; treat all signals as unvalidated."
}
element_2 = f"IR 90d: {ir_value if ir_value else 'N/A'} — {ir_status}: {ir_action_map.get(ir_status, '')}"

# ─────────────────────────────────────────────────────────────
# STEP 6: Compose Element 3 — CEO Recommendation
# ─────────────────────────────────────────────────────────────
def generate_recommendation(crisis_countries, elevated_countries, ir_status, data_stale):
    if data_stale:
        return "Pipeline stale — no signal-based action until data freshness confirmed."
    if ir_status == "RED":
        return "No new positions. Signal reliability below threshold — diagnose pipeline before trading."
    if ir_status == "UNKNOWN":
        return "Validate IR before any signal-based entries."
    if not crisis_countries and not elevated_countries:
        return "No active signals. Hold existing positions; monitor for new entries as GRI develops."
    if crisis_countries and ir_status in ("GREEN", "YELLOW"):
        top = crisis_countries[0]
        return (f"Maintain risk-off bias for {top}-linked assets. "
                f"Do not add new exposure; review existing hedges for extension past valid_thru date.")
    if elevated_countries and not crisis_countries and ir_status in ("GREEN", "YELLOW"):
        return (f"Monitor ELEVATED signals ({format_country_list(elevated_countries)}) for escalation to CRISIS. "
                f"No new entries until z-score crosses 2.5 threshold.")
    if ir_status == "AMBER":
        return "Informational posture only. Review signals but do not size positions on current IR."
    return "Hold current positions; no new signal-based entries today."

element_3 = generate_recommendation(crisis_countries, elevated_countries, ir_status, data_stale)

# ─────────────────────────────────────────────────────────────
# STEP 7: Compose Element 4 — Alert Flag (conditional)
# ─────────────────────────────────────────────────────────────
element_4 = None

if data_stale:
    element_4 = f"⚠ ALERT: GRI pipeline stale — latest data is {latest_gri_date}. Dashboard showing outdated signal. Investigate Databricks Workflow."
elif ir_status == "RED":
    element_4 = f"⚠ ALERT: IR has dropped below 0.20 (current: {ir_value}). Signal reliability threshold breached. Do not act on GRI outputs until root cause identified."
elif crisis_countries:
    new_crisis = crisis_countries  # In a more sophisticated version, compare to yesterday's alerts
    if len(new_crisis) > 0:
        alert_str = ", ".join(new_crisis[:3])
        element_4 = f"⚠ ALERT: Active CRISIS signal — {alert_str}. Review asset exposure before market open."

# ─────────────────────────────────────────────────────────────
# STEP 8: Assemble the note
# ─────────────────────────────────────────────────────────────
note_lines = [
    f"CEO Morning Note — {TODAY}:",
    element_1,
    element_2,
    element_3,
]
if element_4:
    note_lines.append(element_4)

note_text = "\n".join(note_lines)

# ─────────────────────────────────────────────────────────────
# STEP 9: Write to Delta (dashboard reads this)
# ─────────────────────────────────────────────────────────────
note_df = spark.createDataFrame(
    [(str(TODAY), note_text, ir_value, ir_status,
      len(crisis_countries), len(elevated_countries), len(deescal_countries))],
    ["note_date", "note_text", "ir_90d", "ir_status",
     "crisis_count", "elevated_count", "deescalation_count"]
).withColumn("_generated_utc", current_timestamp())

note_df.write.format("delta").mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("geopolitics.gold.ceo_morning_note")

print(f"Morning note written to Delta: {note_text}")
```

---

## IV. Wiring the Note into the Daily Email

The CEO autonomous session (this session) already delivers the daily lesson to Bolo by email. The morning note is prepended to that email so it arrives in the same message, before the lesson body.

The email structure after Lesson 299:

```
Subject: CEO Lesson [N]/ongoing — [Topic Name]

─────────────────────────────────────────
CEO MORNING NOTE — [DATE]
─────────────────────────────────────────
[Element 1 — Signal Status]
[Element 2 — IR Health]
[Element 3 — Recommendation]
[Element 4 — Alert, if triggered]
─────────────────────────────────────────

[Full lesson body below]
```

This means Bolo gets one email, every morning, that contains:
1. The current state of the world (signal)
2. Whether the signal is trustworthy (IR)
3. What to do (recommendation)
4. Any alerts requiring immediate attention
5. The day's lesson (education)

That is the complete Phase 1 product.

---

## V. The Databricks Workflow — Final Task Graph

After this lesson, the complete Workflow task graph for Phase 1 is:

```
[Task 1] gdelt_ingestion_bronze
    ↓
[Task 2] market_data_ingestion_bronze
    ↓
[Task 3] gdelt_silver_transform
    ↓
[Task 4] gri_gold_pipeline
    ↓
[Task 5] signal_generator
    ↓
[Task 6] active_alerts_writer
    ↓
[Task 7] signal_validation_log_update
    ↓
[Task 8] ceo_morning_note_generator   ← THIS LESSON
    ↓
[Dashboard auto-refresh: 09:00 UTC]
[CEO email: 06:00 UTC]
```

**Timing dependency:** The morning note generator (Task 8) must complete before the CEO email session runs. The Workflow should be scheduled to complete by 08:45 UTC so the email session, running at ~09:00 UTC, always finds a fresh note in the Delta table.

---

## VI. The Recommendation Engine — Design Principles

The `generate_recommendation()` function above is deliberately simple. That is correct for now. Here is the design philosophy:

### Principle 1 — The recommendation is a decision rule, not a prediction
The recommendation does not predict what will happen. It says: *given the current signal state and IR, what is the appropriate portfolio posture?* The distinction matters. Predictions can be wrong in ways that are embarrassing. Decision rules can be wrong in ways that are instructive.

### Principle 2 — The recommendation tree must be fully specified
There is no `else: raise Exception("unhandled case")` in a morning note generator. Every possible combination of inputs must map to a defined output. If the signal is in a state the recommendation engine hasn't seen before, the engine should default to the most conservative action, not fail silently or produce a blank.

### Principle 3 — The recommendation evolves as the IR evolves
Right now, with a young signal and uncertain IR, the recommendation engine is conservative: it mostly says "hold" and "monitor." As the IR climbs (or falls), the recommendation engine's output should shift accordingly. Version 2 of this engine (Phase 2) will include position-sizing parameters derived directly from the IR value — not just color categories but specific position-size multipliers.

### Principle 4 — The CEO takes responsibility for the recommendation
The recommendation is attributed to the CEO, not to the signal. This is not a distinction without a difference. If the GRI says CRISIS but the CEO's judgment says the underlying event is already priced in (or that GDELT data is being distorted by a media cycle), the CEO can override the recommendation. The morning note is the CEO's output, informed by the signal, not the signal's output filtered through a CEO label.

---

## Investment Implications

**Phase 1 is now complete. The question changes.**

For the past several weeks, the question has been: *can we build a system that produces geopolitical signals?* The answer, based on the completed pipeline, is yes.

The question that replaces it: *do the signals we produce correspond to real investment outcomes?*

This is an empirical question. The validation run (Lesson 295) set up the framework for answering it. The dashboard (Lesson 298) makes the answer visible. The morning note (this lesson) ensures the answer reaches Bolo every day whether he checks or not.

**The Phase 2 investment threshold:** The CEO will issue the first formal, sized recommendation from the GRI signal when two conditions are met simultaneously:
1. IR 90d > 0.40 (confirmed, not just current)
2. At least one country in CRISIS regime with z-score > 2.5 for 3+ consecutive days

Until both conditions are met, the portfolio posture is: observation and paper trading only. The system is live. The signal is running. We are accumulating the evidence that either earns or denies the signal its authority.

---

## Databricks Angle

**New table this lesson:**
- `geopolitics.gold.ceo_morning_note` — single-row Delta table, overwritten daily by Task 8
  - Schema: `note_date (DATE)`, `note_text (STRING)`, `ir_90d (DOUBLE)`, `ir_status (STRING)`, `crisis_count (INT)`, `elevated_count (INT)`, `deescalation_count (INT)`, `_generated_utc (TIMESTAMP)`

**New notebook:**
- `notebooks/ceo_morning_note_generator.py` — Task 8 in the Workflow

**Key Databricks build task for Bolo:**
1. Add the notebook as Task 8 in the existing Workflow, with dependencies on Tasks 6 and 7
2. Set the Workflow cluster to have the `smtplib` dependency available (or use the Databricks notification API instead of SMTP — see alternative below)
3. Test run in isolation: `dbutils.notebook.run("notebooks/ceo_morning_note_generator", 300)` — confirm the Delta table is written correctly before adding to the Workflow

**Alternative email delivery (no SMTP required):** Databricks has a native notification mechanism via the Workflow `on_success` email setting. The morning note text can be written to the notebook's final cell output, and Databricks will include the notebook output in the success email. This requires no SMTP setup and no credentials stored in the notebook. Trade-off: the email format is less controlled.

---

## Key Concepts This Lesson

1. **Push vs. pull mechanisms** — a dashboard is pull (Bolo must seek it); a daily email is push (the system finds Bolo); resilient systems include both, because the days that matter most are often the days the operator is busiest
2. **The recommendation as a decision rule** — the morning note doesn't predict; it says what posture is appropriate given current signal state and IR; this is the correct architecture for an investment system that operates under uncertainty
3. **Fully-specified decision trees** — every combination of inputs must produce a defined output; a recommendation engine that silently fails on edge cases is worse than no recommendation engine
4. **Phase 1 closure** — data → signal → validation → dashboard → morning note → email is the complete Phase 1 loop; the system now runs autonomously and communicates its state daily without human intervention
5. **The Phase 2 threshold** — the first formal sized recommendation requires IR > 0.40 sustained AND a CRISIS signal persisting 3+ days; until then, the system observes and paper trades

---

## Reflection Questions

1. **The override problem:** The recommendation engine in Step 6 is deterministic — given the same inputs, it always produces the same output. But markets are not deterministic, and sometimes the CEO's judgment should override a mechanical rule. How would you design a "CEO override" mechanism? Should overrides be logged separately from automatic recommendations, and should there be a limit on how often the CEO can override the system before the override itself becomes a signal?

2. **The note's own failure mode:** The morning note generator can itself fail (Databricks cluster down, Delta table locked, SMTP rejected). If it fails silently — no email arrives — Bolo receives no signal that the system is broken. What is the correct failure-mode behavior? Options: (a) send a "note generation failed" email from the Workflow `on_failure` setting; (b) build a health-check endpoint Bolo can query; (c) use a dead man's switch — if no email arrives by 09:30 UTC, Bolo assumes the system is down. Which of these, or which combination, is most operationally robust?

3. **The two-condition Phase 2 threshold:** The CEO has specified IR > 0.40 for 3+ days AND CRISIS signal for 3+ days as the entry conditions for Phase 2 sizing. Are these conditions independent? What happens if a CRISIS signal appears that drives the IR *down* (because the market moved in the opposite direction from the signal, suggesting the signal is wrong about this event type)? Should the conditions be AND, or should they be sequential (validate IR first, then size on signals)?

---

## Questions for Next Session

- **Lesson 300 — Milestone:** Phase 1 Architecture Review. Full audit of what was built, what the validation data actually shows, and the CEO's formal Phase 2 decision: proceed with signal-based recommendations, or return to signal improvement. This is the first formal framework audit since the Databricks build began. It will be structured as a board-level briefing, not a lesson.
- **Build priority for Bolo before Lesson 300:** Run the complete Workflow end-to-end, confirm Task 8 writes the morning note to Delta, and report the current IR value from `geopolitics.gold.signal_validation_log`. The Phase 2 decision depends on this number.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 299 delivered: 2026-09-04*
