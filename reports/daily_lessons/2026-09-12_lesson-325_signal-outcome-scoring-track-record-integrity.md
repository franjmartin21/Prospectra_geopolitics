# Lesson 325 — Signal Outcome Scoring: The Protocol That Makes the Track Record Auditable

**Date:** 2026-09-12
**Session Type:** Daily Lesson
**Lesson Number:** 325 / ongoing
**Topic:** Signal Outcome Scoring — How to Evaluate, Record, and Publish Signal Results
**Curriculum Arc:** Live Operations Module — Lesson 10: Track Record Integrity

---

## Opening Question

*Signal #1 is live. The GRI delta scan protocol runs every Tuesday. The signal is on Substack. The track record schema is built. Then, 60 days from now, the signal's target date arrives.*

**"What exactly do you do on the day a signal closes — and what is the precise sequence of actions that makes the outcome record forensically credible to an institutional reviewer?"**

Most systematic research products fail not in the analysis but in the accounting. A fund manager reviewing your track record at Signal #26 will not simply accept a table of outcomes. They will ask: who decided the signal was correct? What price source was used? When was the outcome recorded — before or after it was clear which way the result fell? Could the outcome methodology have been manipulated after the fact?

The answer to these questions is not a policy document you write at Signal #26. It is the operational protocol you execute at Signal #2 — and identically at every signal after that. This lesson defines that protocol.

---

## I. The Three Failure Modes of Track Record Accounting

Before establishing the scoring protocol, understand the three failure modes that destroy institutional credibility when discovered.

### Failure Mode 1: Discretionary Outcome Timing

The signal calls for a 60-day outcome evaluation. At day 60, the instrument has moved against the call. The analyst waits until day 75 — when the instrument has recovered — and scores the outcome at the day-75 price. No rule was violated (the signal didn't specify the exact hour of evaluation). But the outcome was selected from a favorable window.

**Why it destroys credibility:** An institutional analyst with a quantitative background will check the date-of-record in the Delta Lake transaction log against the actual evaluation date. If the outcome was committed on day 75 for a 60-day signal, the discrepancy is visible. One discrepancy creates a presumption of selection bias across the entire track record.

**The fix:** The outcome date is committed at signal publication. The timeframe (30 / 60 / 90 days) plus the publication date equals the evaluation date. This date is immutable. The scoring query runs on that date, not on the day you remember to run it.

### Failure Mode 2: Price Source Ambiguity

The signal called for a directional move in TRY/USD over 60 days. At day 60, there are at least four possible prices: opening, closing, VWAP, Bloomberg mid, and Reuters mid. The analyst uses whichever source produces the favorable outcome.

**Why it destroys credibility:** An institutional reviewer will attempt to replicate the outcomes from your stated instrument and price source. If the replication produces different win rates, the methodology is either undisclosed or gaming.

**The fix:** The price source is committed at signal publication, in the schema, as a static field. Before Signal #2, add a `price_source` field to `signal_track_record` specifying the exact source (e.g., `"Yahoo Finance daily close"`). Every signal uses the same source. If Yahoo Finance is unavailable on the evaluation date, the fallback is documented (e.g., `"Bloomberg composite close"`). The fallback hierarchy is written into the decisions document before Signal #2, not decided at evaluation time.

### Failure Mode 3: Directional Ambiguity on the Outcome

The signal called for TRY/USD SHORT (Turkish lira weakens). At day 60, TRY/USD has moved from 32.50 to 32.80 — a 0.9% move in the signaled direction. The analyst marks it correct. But 0.9% is within the instrument's daily volatility range: the signal called a directional move, and the price moved in the right direction, but not by more than random noise.

**Why it matters:** A track record where every move in the correct direction — regardless of magnitude — is scored as correct will produce inflated win rates. When an institutional reviewer applies a minimum-move threshold (common practice: the move must exceed the instrument's 30-day realized volatility divided by the square root of the timeframe), the win rate often drops materially.

**The fix:** Establish the significance threshold before Signal #2 and hold it. The threshold: a signal is scored as directionally correct only if the price move at the evaluation date exceeds `(30-day_realized_vol * sqrt(timeframe_days / 30)) / 2`. This is the minimum analytically significant move given the signal's timeframe. It is a generous threshold — half a standard-deviation move over the timeframe — but it eliminates the credibility risk of claiming wins on noise-level moves.

---

## II. The Outcome Scoring Protocol

The scoring protocol runs in four steps on the evaluation date. The sequence is non-negotiable.

### Step 1: Run the Automated Evaluation Query (Morning of Evaluation Date)

A Databricks job, scheduled against the evaluation dates committed in `signal_track_record`, surfaces each signal that reaches its evaluation date within the next 24 hours. This job runs every morning and generates an alert when an evaluation is due.

```python
# daily_outcome_alert.py
# Databricks workflow — runs every morning at 06:00
# Surfaces signals due for outcome evaluation within 48 hours

from pyspark.sql import functions as F
import datetime

track = spark.table("prospectra.gold.signal_track_record")

evaluation_window = (
    track
    .filter(F.col("outcome_direction_correct").isNull())
    .withColumn("eval_date",
        F.date_add(F.col("publication_date"), F.col("timeframe_days"))
    )
    .filter(
        F.col("eval_date").between(
            F.current_date(),
            F.date_add(F.current_date(), 2)
        )
    )
    .select(
        "signal_id", "country_name", "gri_sub_dimension",
        "instrument", "direction", "conviction",
        "publication_date", "timeframe_days", "eval_date",
        "falsifiability_condition", "forward_watch_event",
        "forward_watch_date"
    )
)

if evaluation_window.count() > 0:
    print("=== OUTCOME EVALUATIONS DUE IN NEXT 48 HOURS ===")
    evaluation_window.show(truncate=False)
else:
    print("No evaluations due in the next 48 hours.")
```

When this alert fires, the evaluation is due. Do not delay the evaluation. Do not check market news before running the price query. Run the price query first.

### Step 2: Fetch the Closing Price and Calculate the Move

```python
# outcome_scorer.py
# Run on the evaluation date for a specific signal
# Inputs: signal_id, instrument ticker, publication_date price, price_source

import yfinance as yf
import datetime

SIGNAL_ID = "SIG-001"           # replace with the signal being evaluated
TICKER = "TRYUSD=X"            # replace with the signal's instrument ticker
PUBLICATION_DATE = "2026-09-15" # replace with actual publication date
PRICE_SOURCE = "Yahoo Finance daily close"

# Fetch publication-date close (the "entry" price)
pub_date = datetime.datetime.strptime(PUBLICATION_DATE, "%Y-%m-%d")
pub_hist = yf.Ticker(TICKER).history(
    start=pub_date - datetime.timedelta(days=1),
    end=pub_date + datetime.timedelta(days=1)
)
entry_price = float(pub_hist["Close"].iloc[-1])

# Fetch today's close (evaluation date)
today = datetime.date.today().strftime("%Y-%m-%d")
eval_hist = yf.Ticker(TICKER).history(
    start=datetime.datetime.today() - datetime.timedelta(days=1),
    end=datetime.datetime.today() + datetime.timedelta(days=1)
)
eval_price = float(eval_hist["Close"].iloc[-1])

# Calculate directional move
price_change_pct = (eval_price - entry_price) / entry_price * 100
print(f"Entry price ({PUBLICATION_DATE}): {entry_price:.4f}")
print(f"Eval price  ({today}): {eval_price:.4f}")
print(f"Price change: {price_change_pct:.2f}%")
```

Record both prices and the move percentage. Write them into the scoring document (a plain text file in `reports/signal_outcomes/SIG-{N:03d}_outcome.md`) before determining the outcome direction.

### Step 3: Apply the Significance Threshold and Score the Direction

Only after recording the prices do you look up the signal's direction and apply the threshold.

```python
# Apply the significance threshold
# Signal was SHORT on TRY/USD — a SHORT is correct if TRY weakens (USD/TRY rises = positive pct)

SIGNAL_DIRECTION = "SHORT"      # from signal_track_record
VOL_30D_AT_SIGNAL = 0.12        # 12% annualized vol — from instrument_vol_30d_at_signal
TIMEFRAME_DAYS = 60

import math
significance_threshold = (VOL_30D_AT_SIGNAL * math.sqrt(TIMEFRAME_DAYS / 30)) / 2
print(f"Significance threshold: {significance_threshold * 100:.2f}%")

# SHORT is correct if price_change_pct > significance_threshold (instrument rose, signaled currency fell)
# LONG  is correct if price_change_pct > significance_threshold (instrument rose)
# Adjust direction logic per instrument convention

move_significant = abs(price_change_pct / 100) > significance_threshold
move_in_direction = (
    (SIGNAL_DIRECTION == "SHORT" and price_change_pct > 0) or
    (SIGNAL_DIRECTION == "LONG"  and price_change_pct > 0)
)
outcome_correct = move_significant and move_in_direction

print(f"Move significant (>{significance_threshold * 100:.1f}%): {move_significant}")
print(f"Move in signaled direction: {move_in_direction}")
print(f"Outcome: {'CORRECT' if outcome_correct else 'INCORRECT'}")
```

### Step 4: Commit the Outcome to the Schema and the Outcomes Document

Immediately after scoring, commit to both the Delta Lake table and the outcomes document. These two commits happen in the same work session, before any public statement about the outcome.

```python
# Commit the outcome to signal_track_record
from pyspark.sql import functions as F

(
    spark.table("prospectra.gold.signal_track_record")
    .filter(F.col("signal_id") == "SIG-001")
    .withColumn("outcome_direction_correct", F.lit(outcome_correct))
    .withColumn("outcome_price_change_pct",  F.lit(round(price_change_pct, 4)))
    .withColumn("outcome_notes", F.lit(f"Evaluated {today}. Entry: {entry_price:.4f}, Exit: {eval_price:.4f}. "
                                        f"Move: {price_change_pct:.2f}%. "
                                        f"Threshold: {significance_threshold*100:.2f}%. "
                                        f"Falsifiability event: [triggered/not triggered — note here]."))
    .write.format("delta")
    .mode("overwrite")
    .option("replaceWhere", "signal_id = 'SIG-001'")
    .saveAsTable("prospectra.gold.signal_track_record")
)

print("Outcome committed to signal_track_record.")
print(f"Delta Lake transaction timestamp: {datetime.datetime.utcnow().isoformat()}")
```

The transaction timestamp in the Delta Lake log is the forensic proof that the outcome was committed before any public announcement.

---

## III. The Outcome Publication Protocol

Once the outcome is committed to the database, the publication sequence follows.

### The Outcome Substack Note

Within 24 hours of the evaluation date, publish a brief Substack update for each closed signal. This note is not a retrospective analysis — it is a factual score. It contains:

1. **Signal reference:** Signal #N, country, sub-dimension, instrument, direction, conviction
2. **The outcome:** Correct or incorrect, price move percentage, evaluation date and price
3. **The falsifiability condition:** Did it trigger? When? (If not yet, explain)
4. **One sentence of honest analysis:** What the GRI framework got right, or what it missed

**What not to include:** Any explanation of why the outcome was "almost correct" or why market conditions were unusual. Either the call was correct by the pre-committed scoring rules or it wasn't. Post-hoc rationalization is the single fastest way to destroy institutional credibility. Incorrect calls are expected — approximately 30–40% of medium-conviction calls in a well-calibrated framework should be incorrect. An investor who never sees an incorrect call with clean accounting is more suspicious, not more confident.

The outcome note model:

```
SIGNAL #1 OUTCOME — TRY/USD SHORT | 60-Day Evaluation

Publication date: September 15, 2026
Evaluation date: November 14, 2026
Entry price: 32.50 | Exit price: 33.85 | Move: +4.15%
Significance threshold: +3.41% (required for outcome to count as directionally correct)
Outcome: CORRECT

Falsifiability condition (Erdoğan veto of central bank appointment by October 31):
→ Triggered October 22, 2026 — within timeframe.

Honest analysis: The GRI central bank independence sub-dimension identified a deteriorating condition in August. The falsifiability condition triggered on schedule. The price move exceeded the significance threshold. Signal #1 demonstrates the framework's mechanism — GRI deterioration → catalyst → FX repricing — in sequence. The 60-day timeframe was the appropriate duration; the market repriced within 40 days of publication.

Signal #1 track record status: 1 / 1 correct. Win rate: 100%. (Insufficient sample for statistical inference.)
```

The parenthetical at the end — "insufficient sample for statistical inference" — is non-negotiable at Signal #1. Never imply that a one-signal track record demonstrates anything. That humility, stated plainly, builds more credibility with institutional readers than any win rate could.

---

## IV. The Falsifiability Condition Audit

Every signal includes a falsifiability condition — a specific, named event that, if triggered within the timeframe, should have caused the price move the signal called. At outcome evaluation, the falsifiability audit asks two questions:

1. **Did the falsifiability condition trigger within the timeframe?**
2. **If the call was correct, did the price move follow the falsifiability trigger within 30 days?**

These are different questions and both matter. A signal can be directionally correct even if the falsifiability condition did not trigger (the market moved for a different reason). A signal can be directionally incorrect even if the falsifiability condition did trigger (the mechanism worked but the market had already priced it). Tracking the alignment between falsifiability trigger and price move is the data that allows you to audit whether the *mechanism* — not just the direction — is working.

Build this audit into the outcome notes field:

| Combination | Interpretation |
|---|---|
| Correct direction AND falsifiability triggered AND price move followed trigger | Framework working precisely — best case study |
| Correct direction BUT falsifiability NOT triggered | Directionally correct, mechanism unverified — note as luck-adjusted correct |
| Incorrect direction BUT falsifiability triggered | Framework identified the right mechanism; market didn't reprice in timeframe — extend the post-hoc watch |
| Incorrect direction AND falsifiability NOT triggered | The GRI delta did not translate into the expected outcome — analyze why in the outcome note |

The third and fourth combinations require a post-hoc watch note: "The falsifiability condition triggered but the market has not repriced as of the evaluation date. Extended watch: if the instrument reprices in the 60 days following the evaluation date, this signal will be re-classified as 'late-correct' in the analytical notes (not in the official track record)." The official track record never changes a committed outcome. The analytical notes document delayed repricing separately.

---

## V. The Quarterly Signal Review

At the end of every 13-week quarter, run a structured review of all signals closed in that quarter. The quarterly review produces three outputs:

1. **Win rate by conviction tier** — the calibration check. Are high-conviction signals outperforming medium and low conviction? If not, revise the conviction policy before the next quarter.

2. **Mechanism accuracy audit** — for each GRI sub-dimension that generated signals in the quarter, what was the win rate and average price move? Which sub-dimensions are performing above expectation and which are underperforming?

3. **One methodological decision for next quarter** — not a policy revision, not a framework rebuild. One specific, narrow change to the signal generation or scoring process that the data from this quarter justifies.

The quarterly review document, stored at `reports/signal_outcomes/quarterly_review_YYYY-QN.md`, is the longitudinal record of methodological evolution. At Signal #26, it is the evidence that the framework has a learning loop.

---

## Investment Implications

### The Outcome Protocol as a Pricing Signal to Institutional Buyers

The existence of a rigorous outcome scoring protocol — with pre-committed evaluation dates, a documented price source, a significance threshold, and Delta Lake timestamps — is itself a product differentiator. Most geopolitical research products do not maintain outcome records. Those that do rarely apply a significance threshold or document the price source.

The outcome protocol makes Prospectra's track record **independently auditable** — a characteristic that is unusual enough among non-quant research products that it becomes a sales point in itself. When a family office CIO asks "can I replicate your outcomes from the raw data?", the answer must be yes. The scoring protocol is the mechanism that makes that answer possible.

**Asset class implication:** EM currency managers and macro hedge funds — the primary institutional targets — are accustomed to quantitative track records. They will apply their own significance thresholds and price sources to your data. Building the scoring protocol to institutional standards now means their replication produces the same result as yours. That alignment is trust. Misalignment — even if unintentional — is a credibility crisis at the pitch.

---

## Databricks Angle

**Build: The Automated Outcome Alert and Scoring Pipeline**

The two Databricks jobs that operationalize this lesson:

**Job 1: Daily Outcome Alert** (already described in Step 1 above)
- Schedule: Daily, 06:00 AM
- Output: Slack/email notification when a signal evaluation is due within 48 hours
- Table: reads from `prospectra.gold.signal_track_record`

**Job 2: Quarterly Review Notebook** 
- Schedule: Manual trigger at quarter end (or January 1 / April 1 / July 1 / October 1)
- Output: Win rate table by conviction tier, by GRI sub-dimension, by region
- Table: reads from `prospectra.gold.signal_track_record` where `outcome_direction_correct IS NOT NULL`

**Schema additions to add before Signal #2:**

```sql
ALTER TABLE prospectra.gold.signal_track_record 
ADD COLUMNS (
    price_source           STRING,      -- e.g., 'Yahoo Finance daily close'
    entry_price            DOUBLE,      -- instrument price at publication date close
    eval_date              DATE,        -- publication_date + timeframe_days (immutable)
    outcome_eval_timestamp TIMESTAMP,   -- when the outcome was committed (auto-set by Databricks)
    falsifiability_triggered BOOLEAN,   -- did the named event trigger within timeframe?
    falsifiability_trigger_date DATE,   -- when it triggered (null if not triggered)
    late_correct_flag      BOOLEAN      -- market repriced after eval date (analytical note only)
);
```

Set `eval_date` as a computed column: `publication_date + INTERVAL timeframe_days DAYS`. Once committed at publication, this field is immutable in the analytical workflow (treat it as read-only even though Delta Lake technically allows updates).

The `outcome_eval_timestamp` field is set automatically by Databricks at the time of the outcome commit write. It is the forensic proof that the outcome was committed on or near the evaluation date, not retrospectively. An institutional analyst who asks "when did you record this outcome?" points to this field.

---

## Key Concepts Covered

1. **The three track record accounting failure modes** — discretionary outcome timing, price source ambiguity, and directional ambiguity — and the pre-committed policies that prevent them
2. **The significance threshold** — the minimum move required for a signal to be scored correct, calibrated to realized volatility and timeframe, applied identically to every signal
3. **The four-step outcome scoring protocol** — automated alert, price fetch, significance scoring, and schema commit — in strict sequence, with prices fetched before direction is evaluated
4. **The falsifiability condition audit** — the two-question framework for determining whether the GRI mechanism worked, not just whether the direction was correct
5. **The late-correct flag** — the analytical tool for tracking delayed repricing separately from the official track record without distorting the committed outcome
6. **The quarterly signal review** — the cadence and three outputs (win rate calibration, mechanism accuracy, one methodological decision) that build the learning loop into the track record
7. **Delta Lake as forensic infrastructure** — the transaction timestamp as proof of pre-publication commitment, the architectural choice that makes the track record independently auditable

---

## Reflection Questions

1. **The price source commitment:** Before Signal #2 launches, open `signal_track_record` and add the `price_source` and `entry_price` fields. For Signal #1, backfill the `entry_price` using the Yahoo Finance closing price on Signal #1's publication date. Then commit the price source policy to your decisions document: "All signals use Yahoo Finance daily close. If Yahoo Finance is unavailable, the fallback is [specify]." Write the fallback now — if you leave it undefined, you will face a judgment call at a critical moment.

2. **The significance threshold for Signal #1:** Apply the significance threshold formula to Signal #1 using the instrument's actual 30-day realized volatility at publication. Does Signal #1's current price move (as of today) exceed the threshold? If you were evaluating today, would Signal #1 be correct? Don't wait until the evaluation date to discover the answer — run this calculation now so you understand what "correct" actually requires given the instrument's volatility.

3. **The post-evaluation Substack note structure:** Write a template for the outcome note that will be published when Signal #1 closes. Fill in the fixed structure (all sections that are already known: signal reference, direction, instrument, publication date, evaluation date, falsifiability condition, and the significance threshold). Leave the outcome fields blank. The template should be ready to publish in under 30 minutes on evaluation day — all that changes is the prices and the scored outcome. Having the template ready removes the temptation to delay publication while crafting the narrative.

---

## Questions for Next Session (Spaced Repetition Hook)

- Have the schema additions (`price_source`, `entry_price`, `eval_date`, `outcome_eval_timestamp`, `falsifiability_triggered`) been added to `signal_track_record` before Signal #2 publication?
- Has Signal #1's `entry_price` been backfilled?
- Is the daily outcome alert job scheduled in Databricks (06:00 AM daily)?
- For Signal #1: has the falsifiability condition triggered yet? If so, has the price moved in the signaled direction within 30 days of the trigger?
- Has the price source policy been written into the decisions document — including the fallback hierarchy?

---

## Databricks Relevance Note

**Delta Lake as an Audit Trail**

The outcome scoring protocol depends on a technical property of Delta Lake that most analysts do not consciously use: every write operation appended to a Delta table is recorded in the transaction log with an immutable timestamp. When you commit an outcome to `signal_track_record`, the log records `commitTimestamp`, `operationParameters`, and the exact rows changed. That log entry cannot be altered without breaking the table's consistency guarantees.

For Prospectra, this is not just infrastructure — it is the credibility architecture. An institutional analyst who asks "how do I know you didn't record outcomes retrospectively?" can be shown the Delta Lake transaction log, which lists every write with its UTC timestamp, the user who initiated the write, and the rows affected. That forensic trail is the difference between a track record that requires trust and one that requires verification.

Build a quarterly notebook that queries the Delta Lake history: `DESCRIBE HISTORY prospectra.gold.signal_track_record` in Databricks SQL returns every transaction with timestamp and operation. Pair each outcome commit timestamp with the signal's `eval_date` and confirm the commit happened within 48 hours of the evaluation date. That report, run at Signal #26, is the auditor's verification that the track record was built in real time.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 325 | September 12, 2026 | Live Operations Module — Lesson 10: Track Record Integrity*
