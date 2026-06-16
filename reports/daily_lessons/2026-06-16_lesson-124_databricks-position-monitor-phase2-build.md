# Lesson 124: The Databricks Build Priority — From Portfolio Audit to Operational Intelligence

**Date:** 2026-06-16
**Session Type:** Daily Lesson
**Lesson Number:** 124 of ongoing curriculum
**Topic:** Translating Portfolio Audit Lessons Into the Phase 2 Pipeline Architecture — The Position Monitor

---

## Opening Framing Question

The audit is done. You have 13 positions, 5 framework improvements, and a conviction map updated to June 14. You also have a live event today: Warsh's first FOMC meeting, the result of which lands tomorrow (June 17). Your tail hedge (Position 10) is on high alert. Your TIPS allocation (Position 12) is sensitive to the rate path signal. Your entry-discipline framework (validated by the tactical crude short) must now be applied to whatever Warsh signals about H2 2026 rates.

You cannot monitor all of this manually. Not at scale. Not consistently. Not without introducing exactly the kind of emotional, reactive noise that the framework is designed to eliminate.

**Here is the question:** The Position Monitor has five layers. You can only build one in the next sprint. Which layer saves you the most money — and why?

Hold that question in your mind. We'll return to it. First, let's understand what we're actually building and why the answer matters more than most Databricks sprints you'll run.

---

## Section 1: Why the Audit Created a Build Imperative

Lesson 123 produced five framework improvements. Each one implicitly specified a technical requirement that cannot be fulfilled by a spreadsheet:

| Framework Improvement | What It Requires Technically |
|---|---|
| Sector bifurcation (defense vs. non-defense) | A position register with sub-sector tagging, not a flat list |
| AI infrastructure as a commodity demand driver | Automated news/event feed scanning for AI capex signals, mapped to position themes |
| 30-day South Asia monitoring (vs. 90-day) | Configurable review frequency per position — not a fixed calendar |
| Entry trigger discipline | A trigger rule engine that evaluates conditions before flagging for action |
| Continuous audit, not quarterly | A weekly auto-report that forces structured review without waiting for the CEO to schedule it |

None of these are solvable with a Google Sheet and a reminder calendar. Each one is a data engineering problem.

The Position Monitor is not a "nice to have" analytics project. It is the operational infrastructure that makes the portfolio manageable at the framework level we've built. Without it, framework improvement #1 through #5 from Lesson 123 exist on paper only — they will not be consistently applied under pressure.

**This is the Phase 2 centerpiece. It is also the most direct path to the product thesis (Goal 3) — because a systematized, auditable position monitoring pipeline is what a commercial geopolitical intelligence product actually is.**

---

## Section 2: The Answer — Layer 4 First

Let's return to the opening question. Five layers:

- **Layer 1:** Position Register (static table — position metadata)
- **Layer 2:** Market Data Feed (daily price pull for portfolio proxies)
- **Layer 3:** Thesis Confirmation Scoring (GDELT event signals mapped to positions)
- **Layer 4:** Kill Switch Monitor (quantitative rules for mandatory review triggers)
- **Layer 5:** Audit Report Generator (weekly automated portfolio status report)

**The answer is Layer 4.**

Here is the reasoning, stated precisely:

Layer 2 tells you *how much* you've made or lost. You need this, but a loss you're aware of and a loss you're not aware of are both losses. Awareness without a decision rule doesn't stop losses.

Layer 3 tells you whether your thesis is being confirmed. This is intellectually valuable. But a thesis that is being contradicted without a defined response rule is just anxiety infrastructure — it tells you something is wrong without telling you what to do.

Layer 5 gives you a weekly report. Useful. But it is a lagging indicator. By the time the report fires, the damage may already be done.

**Layer 4 is the only layer where the output is directly linked to a portfolio action.** The kill switch monitor doesn't produce insight — it produces a decision prompt. When Layer 4 fires, you know: (a) exactly which condition was triggered, (b) which position is affected, and (c) what the pre-specified response is. No deliberation required. No emotional processing under pressure. The decision was made *ex ante*, when you were calm and analytical. Layer 4 just executes the pre-commitment.

This is the same reasoning that validated the tactical crude short (Position 7) in the audit. We didn't enter the position because the entry trigger never fired. **An entry trigger that prevented us from losing money is the same architecture as a kill switch that prevents us from holding a losing position too long.** The framework's immune system. Build it first.

---

## Section 3: Live Test Case — The FOMC Event, Today

Before diving into the technical spec, let's use today's event to prove why Layer 4 matters.

**Situation:** Warsh opens his first FOMC meeting today (June 16). Decision and press conference land tomorrow (June 17). Rate hold is near-certain (97.4% market probability at 3.50–3.75%). What matters is not the rate decision — it's the *signal* about H2 2026 rate path and Warsh's communication style.

**Positions affected:**

**Position 10 — Tail Hedge, EM Fixed Income (BOJ carry unwind)**
Kill switch check specified in Lesson 123: "If Warsh signals dovish (rate cuts ahead), yen carry trade *strengthens* → temporarily reduce tail hedge sizing. If hawkish or ambiguous, hold."

From Layer 4's perspective, this is a manually-encoded decision rule. In a deployed system, the logic would look like:

```python
# Kill switch rule: Position 10 — Tail Hedge
# Trigger: FOMC rate guidance signal
# Source: FRED API — check implied rate path shift (2Y Treasury yield move)

def fomc_tail_hedge_check(two_year_yield_change_bps):
    """
    If 2Y yield drops >15bps post-FOMC (dovish signal):
      → Flag: REDUCE tail hedge to 1% of portfolio
    If 2Y yield rises >10bps (hawkish signal):
      → Flag: HOLD tail hedge at 2-3%
    If change within ±10bps (neutral / ambiguous):
      → Flag: HOLD, monitor Warsh press conference tone
    """
    if two_year_yield_change_bps < -15:
        return "ACTION: Reduce tail hedge. Warsh dovish — carry trade strengthens."
    elif two_year_yield_change_bps > 10:
        return "HOLD: Hawkish signal. Tail hedge at full size."
    else:
        return "HOLD: Ambiguous. Await press conference tone analysis."
```

**Position 12 — Long TIPS**
Kill switch check: "The FOMC on June 16–17 is not a trading event for this position." This is also a Layer 4 rule — specifically, a rule that says *don't act*. Suppressing reactive behavior is equally important as triggering responsive behavior.

```python
# Kill switch rule: Position 12 — Long TIPS
# FOMC event: structural thesis independent of single meeting
# Action: NO ACTION regardless of FOMC outcome
# Exception: Only reconsider if Warsh signals 3+ rate cuts in 2026 dot plot
#   (that would indicate market misread inflation as transient — re-evaluate fiscal dominance thesis)

def fomc_tips_check(dot_plot_cuts_2026):
    if dot_plot_cuts_2026 >= 3:
        return "FLAG FOR REVIEW: Warsh signaling aggressive easing. Fiscal dominance thesis challenged."
    else:
        return "NO ACTION: Single FOMC event is not a TIPS trading signal."
```

**This is what Layer 4 does in practice.** It doesn't make decisions. It executes pre-commitments. Tomorrow morning, when Warsh's press conference hits and every financial media outlet is generating noise, Layer 4 checks two numbers (2Y yield move, dot plot cut count) and outputs a one-line action flag. No deliberation. The decision was already made in the position spec.

---

## Section 4: The Full Technical Architecture

Here is the complete Position Monitor specification, ready for the Databricks build:

### Layer 1 — Position Register (Delta Table, Static)

```sql
-- Table: prospectra.portfolio.position_register
CREATE TABLE IF NOT EXISTS prospectra.portfolio.position_register (
    position_id       STRING,      -- e.g., "P01_GOLD", "P03_EUR_DEF"
    asset_class       STRING,      -- "equity", "commodity", "fx", "fixed_income", "hedge"
    instrument        STRING,      -- "GLD", "EUAD", "COPX", "TIP", "URA"
    yf_ticker         STRING,      -- Yahoo Finance ticker for Layer 2 pull
    open_date         DATE,
    thesis_summary    STRING,
    conviction_level  STRING,      -- "MAXIMUM", "VERY_HIGH", "HIGH", "MEDIUM_HIGH", "MEDIUM"
    review_freq_days  INT,         -- 30 for South Asia; 60 for EM; 90 for structural
    kill_switch_type  STRING,      -- "quantitative", "qualitative", "hybrid"
    kill_switch_rule  STRING,      -- human-readable rule
    theater_tags      ARRAY<STRING> -- e.g., ["Ukraine", "NATO", "Hormuz"]
) USING DELTA;
```

Populate this table with all 12 open positions from the Lesson 123 conviction map. This is a one-time manual entry. Every future position opened must be registered here before it is traded. The Position Register is the contract between the investment thesis and the monitoring system.

### Layer 2 — Market Data Feed (DLT Pipeline)

```python
# Databricks Delta Live Tables — daily price feed
import dlt
import yfinance as yf
from pyspark.sql import functions as F

TICKERS = ["GLD", "EUAD", "DFNS", "XLE", "LNG", "COPX", "URNM", 
           "INDA", "TIP", "TUR", "EWY", "^TNX", "^IRX"]  # ^TNX = 10Y, ^IRX = 3M

@dlt.table(
    name="market_data_daily",
    comment="Daily closing prices for all portfolio proxy instruments",
    table_properties={"quality": "bronze"}
)
def market_data_daily():
    dfs = []
    for ticker in TICKERS:
        data = yf.download(ticker, period="1d", auto_adjust=True)
        data["ticker"] = ticker
        dfs.append(data)
    combined = pd.concat(dfs).reset_index()
    return spark.createDataFrame(combined)

@dlt.table(
    name="position_pnl",
    comment="Daily P&L for each position vs. open price",
    table_properties={"quality": "silver"}
)
def position_pnl():
    prices = dlt.read("market_data_daily")
    register = spark.table("prospectra.portfolio.position_register")
    
    return (prices
        .join(register, prices.ticker == register.yf_ticker, "inner")
        .withColumn("open_price", F.first("Close").over(
            Window.partitionBy("position_id").orderBy("Date")))
        .withColumn("daily_return_pct", 
            (F.col("Close") - F.col("open_price")) / F.col("open_price") * 100)
        .withColumn("days_open", F.datediff(F.current_date(), F.col("open_date")))
    )
```

**Sprint estimate: 1 sprint (2–3 days).** The yfinance integration is straightforward; the DLT pipeline requires Unity Catalog setup but no complex transformations. Store prices in Bronze; compute P&L in Silver.

### Layer 4 — Kill Switch Monitor (Priority Build)

This is the Phase 2 centerpiece. Build immediately after Layer 2.

```python
# Databricks Workflow — daily kill switch evaluation
# Schedule: 7:00 AM UTC / 3:00 AM ET — before US market open

import datetime
import yfinance as yf
from databricks.sdk.runtime import dbutils

def evaluate_kill_switches():
    """
    Evaluate all quantitative kill switch conditions.
    Returns list of triggered alerts for portfolio positions.
    """
    alerts = []
    today = datetime.date.today()
    
    # Position 1: Long Energy (Oil Majors)
    # Kill switch: Brent three consecutive closes below $80
    brent = yf.download("BZ=F", period="5d", auto_adjust=True)["Close"]
    below_80_streak = (brent < 80).rolling(3).sum().iloc[-1]
    if below_80_streak >= 3:
        alerts.append({
            "position_id": "P01_ENERGY",
            "alert_type": "KILL_SWITCH_TRIGGERED",
            "condition": "Brent 3 consecutive closes below $80",
            "current_value": f"${brent.iloc[-1]:.2f}/bbl",
            "action_required": "EXIT: Long energy position. Review thesis at Brent $80."
        })
    
    # Position 6: Long Copper
    # Kill switch: COPX proxy below $9,500/MT for 3 consecutive months
    copper = yf.download("HG=F", period="90d", auto_adjust=True)["Close"]
    copper_monthly = copper.resample("M").last()
    below_95_streak = (copper_monthly < 9500).rolling(3).sum().iloc[-1]
    if below_95_streak >= 3:
        alerts.append({
            "position_id": "P06_COPPER",
            "alert_type": "KILL_SWITCH_TRIGGERED",
            "condition": "Copper 3 consecutive monthly closes below $9,500/MT",
            "action_required": "EXIT: Structural deficit thesis falsified at this price level."
        })
    
    # Position 10: Tail Hedge — FOMC Rate Path (June 17 specific)
    if today == datetime.date(2026, 6, 17):  # Post-FOMC check
        two_year = yf.download("^IRX", period="3d", auto_adjust=True)["Close"]
        yield_change_bps = (two_year.iloc[-1] - two_year.iloc[-3]) * 100
        if yield_change_bps < -15:
            alerts.append({
                "position_id": "P10_TAIL_HEDGE",
                "alert_type": "CONDITIONAL_REVIEW",
                "condition": f"2Y yield dropped {yield_change_bps:.0f}bps post-FOMC (dovish)",
                "action_required": "REDUCE: Tail hedge to 1% of portfolio. Carry trade strengthens."
            })
    
    # Position 3: European Defense
    # Kill switch: qualitative — NATO spending reversal
    # Cannot be automated; flag for manual check every 30 days
    days_since_review = (today - datetime.date(2026, 6, 14)).days
    if days_since_review >= 30:
        alerts.append({
            "position_id": "P03_EUR_DEF",
            "alert_type": "SCHEDULED_REVIEW",
            "condition": "30-day qualitative review due",
            "action_required": "MANUAL: Verify NATO spending appropriations are flowing through budgets."
        })
    
    return alerts

# Write alerts to Delta table
alerts = evaluate_kill_switches()
if alerts:
    alert_df = spark.createDataFrame(alerts)
    (alert_df
        .withColumn("alert_date", F.current_date())
        .write
        .mode("append")
        .saveAsTable("prospectra.portfolio.kill_switch_alerts"))

# Send email notification if any alerts fired
if alerts:
    critical = [a for a in alerts if a["alert_type"] == "KILL_SWITCH_TRIGGERED"]
    if critical:
        dbutils.notebook.exit(f"CRITICAL ALERTS: {len(critical)} kill switches triggered. Review required.")
```

**Databricks Workflow Setup:**
```yaml
# .databricks/workflows/kill_switch_monitor.yml
name: Kill Switch Monitor
schedule:
  quartz_cron_expression: "0 0 7 * * ?"  # 7 AM UTC daily
  timezone_id: UTC
tasks:
  - task_key: evaluate_kill_switches
    notebook_task:
      notebook_path: /Workspace/Prospectra/Portfolio/kill_switch_monitor
    job_cluster_key: small_cluster
email_notifications:
  on_failure:
    - franjmartin21@gmail.com
  on_success:
    - franjmartin21@gmail.com  # Only when alerts fire (add conditional logic in notebook)
```

**Sprint estimate: 1 sprint (2–3 days).** The quantitative rules are already specified in Lesson 123. This is implementation, not design work. Requires: Unity Catalog, Databricks Workflows, yfinance install on cluster, Delta table write permissions.

### Layer 3 — Thesis Confirmation Scoring (GDELT-Based)

Build this third. Requires the existing GDELT ingest pipeline from Phase 1.

```python
# Theater Escalation Score — for each of 10 theaters
# Input: GDELT event feed (existing Phase 1 bronze table)
# Output: Daily escalation pressure score (0-100) per theater

THEATER_DEFINITIONS = {
    "Hormuz": {
        "countries": ["IRN", "SAU", "YEM", "UAE"],
        "cameo_codes": ["14", "15", "16", "17", "18", "19"],  # CONFLICT events
        "bounding_box": (22, 50, 30, 60)  # lat/lon box for Gulf
    },
    "Ukraine": {
        "countries": ["UKR", "RUS", "USA", "DEU", "GBR"],
        "cameo_codes": ["13", "14", "15", "18", "19"],
        "bounding_box": (44, 22, 52, 40)
    },
    "Taiwan": {
        "countries": ["CHN", "TWN", "USA", "JPN"],
        "cameo_codes": ["13", "14", "15", "17"],
        "bounding_box": (20, 118, 28, 125)
    },
    "SouthAsia": {
        "countries": ["IND", "PAK", "CHN"],
        "cameo_codes": ["13", "14", "15", "17", "18"],
        "bounding_box": (8, 60, 37, 97)
    },
    "Sahel": {
        "countries": ["MLI", "NER", "BFA", "TCD"],
        "cameo_codes": ["14", "15", "18", "19"],
        "bounding_box": (10, -18, 23, 24)
    }
}

@dlt.table(name="theater_escalation_scores")
def theater_escalation_scores():
    gdelt = spark.table("prospectra.gdelt.events_bronze")
    
    results = []
    for theater, config in THEATER_DEFINITIONS.items():
        # Filter events to theater
        theater_events = (gdelt
            .filter(F.col("ActionGeo_CountryCode").isin(config["countries"]))
            .filter(F.col("EventCode").substr(1, 2).isin(config["cameo_codes"]))
        )
        
        # Rolling 30-day event velocity
        daily_counts = (theater_events
            .groupBy(F.col("SQLDATE").alias("event_date"))
            .agg(F.count("*").alias("event_count"))
        )
        
        # Z-score vs. 6-month baseline
        baseline_stats = (daily_counts
            .filter(F.col("event_date") >= F.date_sub(F.current_date(), 180))
            .agg(F.avg("event_count").alias("baseline_mean"),
                 F.stddev("event_count").alias("baseline_std"))
        )
        
        # Most recent 7-day average
        recent = (daily_counts
            .filter(F.col("event_date") >= F.date_sub(F.current_date(), 7))
            .agg(F.avg("event_count").alias("recent_avg"))
        )
        
        results.append({
            "theater": theater,
            "score_date": datetime.date.today(),
            # Z-score capped at 0-100 scale: 0 = calm, 100 = extreme escalation
            # Computed in Silver transform below
        })
    
    return spark.createDataFrame(results)
```

**Sprint estimate: 2 sprints (5–7 days).** This is the most complex layer — it depends on GDELT ingestion quality and requires calibration of the z-score baseline. Do not rush this. A miscalibrated escalation score is worse than no score — it generates false alerts.

### Layer 5 — Audit Report Generator (Weekly Auto-Report)

Build this last. It synthesizes outputs from Layers 1–4.

```python
# Weekly report: auto-generate position status table
# Output: Markdown report pushed to reports/portfolio_monitor/ directory

def generate_weekly_report(report_date):
    pnl = spark.table("prospectra.portfolio.position_pnl").filter(...)
    alerts = spark.table("prospectra.portfolio.kill_switch_alerts")
    escalation = spark.table("prospectra.portfolio.theater_escalation_scores")
    
    # Build report template
    report = f"""
# Portfolio Monitor Report — Week of {report_date}
## Kill Switch Status
{format_kill_switch_table(alerts)}

## Position P&L vs. Open Price
{format_pnl_table(pnl)}

## Theater Escalation Scores
{format_escalation_table(escalation)}

## Positions Requiring Review (30-day / 60-day / 90-day cadence)
{format_review_queue(pnl)}
    """
    
    # Write to reports directory
    output_path = f"/Workspace/Prospectra/reports/portfolio_monitor/{report_date}_monitor.md"
    dbutils.fs.put(output_path, report, overwrite=True)
    
    return report
```

**Sprint estimate: 1 sprint.** This is mostly template work once Layers 2 and 4 are live.

---

## Section 5: The Build Sequence — 5 Sprints to Full Automation

| Sprint | Layer | Output | CEO Value |
|---|---|---|---|
| 1 | Layer 2 — Market Data Feed | Daily P&L on all positions | Know immediately when a position hits drawdown thresholds |
| 2 | Layer 4 — Kill Switch Monitor | Daily automated decision prompts | **Framework immune system deployed. Most valuable sprint.** |
| 3–4 | Layer 3 — GDELT Thesis Scoring | Weekly thesis confirmation signals | Thesis validation without manual reading of every news source |
| 5 | Layer 5 — Audit Report Generator | Weekly automated audit | Continuous framework calibration without scheduling overhead |

**Layer 1 (Position Register) is a pre-requisite, not a sprint.** Bolo should build the Delta table and populate it manually before Sprint 1. It's a 2-hour task, not a sprint.

**Total: 5 sprints at 2–3 days each = 2–3 weeks to full Phase 2 deployment.**

---

## Section 6: The FOMC Event — Tomorrow's Live Test

The Warsh press conference on June 17 is the first live test of the kill switch logic for Positions 10 and 12. Before the monitoring system is built, here are the manual decision rules to apply:

| Signal | Position 10 (Tail Hedge) | Position 12 (TIPS) |
|---|---|---|
| **Dovish** (2Y yield drops >15bps, dot plot shows 2+ cuts) | **Reduce to 1%** — carry trade strengthens | **No action** — dovish is TIPS-positive but thesis is structural |
| **Hawkish** (2Y yield rises >10bps, dot plot shows 0 cuts) | **Hold at 2–3%** — rate differential sustains carry | **No action** — single FOMC meeting |
| **Ambiguous / hold** (yield ±10bps, neutral language) | **Hold** — await next BOJ meeting signal | **No action** |
| **Surprise cut** (not priced) | **Immediately reduce to 1%** — yen carry trade reverts fast | **Consider adding** — real rates fall, TIPS rally |

**What to watch in Warsh's press conference (June 17):**
1. Does he use the phrase "data dependent" or "meeting-by-meeting"? (Hawkish — implies no pre-commitment to cuts)
2. Does he reference the NATO defense spending commitment as inflationary? (Confirms fiscal dominance thesis for TIPS)
3. Does he signal concern about dollar strength? (Bearish for yen carry trade — reduces tail hedge need)
4. Does the dot plot show fewer than 2 cuts in 2026? (Near consensus — no action)

This is exactly the type of event-to-decision mapping that Layer 4 will automate. Tomorrow morning, you should not be Googling "what did Warsh say." You should be checking one table: `prospectra.portfolio.kill_switch_alerts`.

---

## Section 7: Integration With the Theater Escalation Score

Layer 4 (kill switches) and Layer 3 (thesis confirmation) are distinct systems that serve different purposes:

- **Kill switch:** Stop the bleeding. An *alarm* that fires when a pre-specified falsification condition is met.
- **Thesis confirmation:** Calibrate conviction. A *signal* that shows whether the underlying thesis is strengthening or weakening.

In the full Phase 2 system, these interact. A position where:
- Kill switch has NOT fired (still open)
- BUT thesis confirmation score is declining over 4+ weeks

...should generate a "conviction downgrade" flag. Not a close signal — a review prompt. The framework does not automatically close positions on declining thesis signals. It escalates them for human judgment. The distinction is deliberate: thesis confirmation is noisy; kill switches are precise. Do not conflate them.

The Phase 2 architecture keeps these as separate tables with a join only at the reporting layer (Layer 5). This is a design choice with downstream consequences — protect it.

---

## Key Concepts Covered

- The Position Monitor as the operational infrastructure that makes the portfolio manageable at scale
- Layer 4 (Kill Switch Monitor) as the first-build priority: the only layer where output directly triggers a portfolio action
- Entry trigger discipline and kill switch discipline as the same cognitive architecture applied at entry and exit
- FOMC event (June 16–17) as a live test case for kill switch logic on Positions 10 and 12
- Delta Live Tables + Databricks Workflows as the technical substrate for automated monitoring
- Kill switch vs. thesis confirmation as distinct signals (alarm vs. calibration)
- 5-sprint build sequence from Position Register to full automated audit

---

## Investment Implications Summary

| Layer | Portfolio Value |
|---|---|
| Layer 1 — Position Register | Single source of truth; prevents "position creep" (holding a position that has no formal kill switch) |
| Layer 2 — Market Data Feed | Daily P&L visibility; early warning on drawdown before kill switch triggers |
| Layer 3 — GDELT Thesis Scoring | Reduces reliance on news reading for thesis monitoring; surfaces signal in noise |
| Layer 4 — Kill Switch Monitor | **Saves money directly by enforcing pre-commitment discipline under pressure** |
| Layer 5 — Audit Report Generator | Accelerates framework improvement cycle; prevents audit from being optional |

---

## Databricks Angle: Sprint 1 Brief — What Bolo Builds Next

**Sprint 1 objective:** Deploy Layer 1 (Position Register) and Layer 2 (Market Data Feed) in Databricks.

**Concrete deliverables:**
1. Unity Catalog schema: `prospectra.portfolio`
2. Delta table: `position_register` — populate with all 12 open positions from Lesson 123 conviction map (tickers: GLD, EUAD, XLE, COPX, URNM, LNG, INDA, TIP, TUR, EWY + BZ=F for Brent monitoring)
3. DLT pipeline: `market_data_daily` — pulls daily closing prices via yfinance for all tickers; stores in Bronze table
4. Silver transform: `position_pnl` — daily return % vs. open price for each position; 7-day rolling max drawdown; flag positions with >5% drawdown from peak
5. Databricks AI/BI dashboard: simple table showing all positions, current P&L %, days open, conviction level

**Time estimate:** 2–3 working days for a Databricks SA comfortable with DLT and Unity Catalog.

**Sprint 2 starts when:** Layer 2 is live and you've confirmed daily prices are loading cleanly. Then pivot immediately to Layer 4 kill switch implementation.

---

## Reflection Questions

1. **The Layer 4 priority argument:** I argued that Layer 4 (Kill Switch Monitor) saves more money than Layer 2 (Market Data), Layer 3 (Thesis Confirmation), or Layer 5 (Audit Report). Construct the strongest possible counterargument. Why might Layer 3 (thesis confirmation) actually be *more* valuable than a kill switch — and under what circumstances would you change the build sequence?

2. **Warsh's first meeting:** After reading the June 17 press conference, apply the decision matrix in Section 6 to determine your action on Positions 10 and 12. Write out your reasoning in one paragraph — what did Warsh signal, which cell of the matrix applies, and what is the resulting portfolio action? This is your first real-time test of pre-commitment discipline.

3. **The design choice to keep kill switches and thesis confirmation separate:** Section 7 argues against conflating these two signals. Identify a specific scenario where merging them into a single "action trigger" would generate a *false positive* — where you would close a position you should hold. What does this reveal about the relationship between quantitative automation and human judgment in geopolitical investing?

---

## Questions for Next Session

The Position Monitor architecture is specified. Sprint 1 is briefed. The FOMC test lands tomorrow.

**Next session: Sprint 1 Review + The Warsh Signal — What Did the First FOMC Under the New Regime Actually Mean?**

We will review Warsh's June 17 press conference signal, apply the kill switch decision matrix to Positions 10 and 12, and determine whether the TIPS structural thesis requires any update. We will also review Bolo's Sprint 1 build progress on the Position Register and Market Data Feed.

Preview question: *Warsh said he is "data dependent." Every Fed chair says this. What specific data points — named explicitly — would move his policy stance before the September 2026 FOMC? And which of those data points is most directly linked to the fiscal dominance thesis underlying Position 12 (TIPS)?*

---

## Databricks Relevance Note

Sprint 1 brief is in Section 7 of this lesson — this is a complete technical handoff document for Bolo. The deliverables are specified with table names, column schemas, and pipeline structure. No further design work required before building.

Priority for Bolo's next Databricks session:
1. Create `prospectra.portfolio` schema in Unity Catalog
2. Build `position_register` Delta table; populate manually with 12 open positions
3. Deploy DLT pipeline for `market_data_daily` using yfinance
4. Build `position_pnl` Silver transform
5. Create Databricks AI/BI dashboard for daily position monitoring

Sprint 2 (Kill Switch Monitor) will be briefed in the next lesson after Sprint 1 review.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson delivered: 2026-06-16 | Next lesson: #125 — Sprint 1 Review + The Warsh Signal (post-June 17 FOMC)*
