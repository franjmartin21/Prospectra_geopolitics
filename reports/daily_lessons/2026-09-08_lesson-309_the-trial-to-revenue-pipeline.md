# Lesson 309 — The Trial-to-Revenue Pipeline: Managing the First 30 Days

**Date:** 2026-09-08
**Session Type:** Daily Lesson
**Lesson Number:** 309 / ongoing
**Topic:** The Trial-to-Revenue Pipeline — How to Run a 30-Day Trial and Convert It
**Curriculum Arc:** Year 2 Launch Module — Lesson 6 (From Demo to Signed Contract)

---

## Opening Question

*Lesson 308 ended with the exact words to close a first commercial conversation: "I'll send you the CSV tonight. Can we schedule 20 minutes in 2 weeks to go through what you find?"*

**"The prospect said yes. You sent the CSV that night. Now what? What happens in the next 30 days that determines whether this becomes a paying customer — and what are the three most common ways trials die quietly without anyone saying why?"**

Most trial periods fail not because the product is wrong. They fail because the vendor disappears. The prospect gets the CSV, opens it on Tuesday, has questions, gets distracted by a portfolio event on Wednesday, and by the time the 2-week call comes around, they have not looked at it again. The call happens, it is pleasant, nothing is decided, the vendor says "I'll follow up," and the relationship decays into a polite ghost.

The trial period is not a waiting room. It is the highest-leverage 30 days in the commercial cycle. Every touchpoint, every data delivery, every question you answer in that window either compounds toward a signed contract or bleeds toward silence.

This lesson builds the operational architecture for the trial period: what to deliver, when to deliver it, how to stay present without being annoying, and how to read the signals that tell you whether this prospect is converting or not.

---

## I. What the Trial is Actually Testing

The prospect has four questions they will not ask directly:

### 1. "Does this data actually integrate into what I already do?"

A CSV that lands in someone's inbox is not integrated. Integration happens when they open it, run a correlation in Python or Excel against their own portfolio data, and see something that makes them pause. If the data is in a format they cannot immediately use — wrong column schema, inconsistent date formatting, country codes they do not recognize, too many countries without documentation — the trial dies in the first hour without you ever knowing.

**The implication:** The CSV you send on night one should be over-documented. A README in the same email. Column definitions. Date range. Methodology note (two paragraphs, not twelve). Country coverage list. Do not make them guess what `GOLDSTEIN_SCORE_MEAN_28D` means.

### 2. "Is the signal actually different from what I already have?"

If they are already using Bloomberg GPR, S&P Global Political Risk Scores, or even their own internal country risk framework, the first thing they will do with your data is run it against their existing series. If the correlation is 0.9, they will not pay for it. They are looking for orthogonality — a signal that adds something their current process does not have.

**The implication:** In the email with the CSV, include a one-paragraph note on what makes the GRI orthogonal. Not a marketing claim — a technical one. "The GRI uses GDELT event-category counts and Goldstein-score velocity, not media attention or analyst survey data. The signal tends to lead media-based indices by 3–7 days and diverges most from consensus during de-escalation phases — when media attention is falling but structural risk remains elevated." That is the paragraph that makes a quant PM read the data differently than they would otherwise.

### 3. "Can I trust the methodology?"

Trust in a methodology comes from three things: it is documented, it is consistent, and it is wrong in understandable ways. A signal that is always right is a red flag. A signal that is wrong in predictable ways — "it overstates risk during commodity price spikes because GDELT conflates economic distress events with political instability" — is a signal from someone who actually understands what they built.

**The implication:** The methodology note should include one explicit known limitation. Not buried — in the first third. A buyer who reads a limitation and thinks "that makes sense given how the data works" trusts the product more than one who reads claims with no caveats.

### 4. "What happens when something goes wrong?"

Data products break. Pipelines have lag. GDELT has gaps. Country reclassifications happen. What does the vendor do when the data is late, wrong, or missing? This question is mostly unconscious — the prospect is not thinking about it explicitly. But when you proactively send a note saying "heads up — GDELT ingestion was delayed by 18 hours last Thursday due to infrastructure maintenance; all scores were recalculated from the full dataset and redelivered by Friday morning," you answer it without being asked.

**The implication:** Proactive incident communication is a commercial asset, not a liability. Never wait for a customer to notice a problem. Tell them before they see it.

---

## II. The 30-Day Trial Cadence

The trial is not passive. It has a seven-touchpoint structure. Every touchpoint either advances the relationship or signals the trial's health.

### Day 0 (Night of Demo): The Data Delivery Email

**Send:** The GRI CSV for their coverage universe, the README, and the methodology note.  
**Subject:** `Prospectra GRI Data — [Their Coverage Region] — Trial Access`  
**Format:** 4 short paragraphs: (1) what is attached, (2) methodology note with the orthogonality paragraph, (3) the known limitation, (4) the next step reminder ("we have 20 minutes scheduled for [date]; looking forward to hearing what you find").  
**Length:** 300 words. Not 600. Not 150.

### Day 3: The Check-In

**Send:** A one-sentence email.  
**Content:** "Quick check — did the data land in a format that works for your system? Happy to send a different export (Parquet, JSON, XLSX) if the CSV does not integrate cleanly."  
**Purpose:** Two things. First, you confirm the data actually arrived and opened. Second, you signal that you will meet them where their system is — which is what an enterprise data vendor does.

**Response to "yes, works great":** No further action. Do not push.  
**Response to "actually, our system uses Parquet":** Send Parquet that day. Log the format preference in `prospectra.gold.trial_cohorts`.

### Day 7: The Signal Update

**Send:** The weekly GRI note for their coverage universe — formatted as if they are already a paying customer.  
**Include:** Flag any score moves >8 points since Day 0. Brief (3-sentence) interpretation of the move. No ask.  
**Purpose:** Demonstrate what the ongoing product looks like. They are not evaluating the Day 0 CSV in isolation — they are evaluating what they will receive every week if they subscribe.

**Key detail:** The Day 7 delivery should be *better* than the Day 0 CSV. More context. Better formatting. This is intentional — you want them to see the product improving.

### Day 10: The Correlation Question

**Send:** A specific question.  
**Content:** "One thing I'd be curious about: have you had a chance to run the GRI against any of your existing series? The orthogonality vs. Bloomberg GPR tends to be most visible in the EM Asia and LATAM coverage — I'd be interested to know if you see the same pattern in your data."  
**Purpose:** Two things. It prompts them to actually open the data if they have not yet. And it frames the comparison they will make as a conversation rather than a silent conclusion.

**What their response tells you:**
- If they answer with specific numbers: they have looked at the data carefully. High-conversion signal.
- If they say "haven't had a chance yet": ask when they expect to. If they say "next week," that is fine. If they say "honestly not sure," the trial is in trouble.
- If they do not reply within 48 hours: the trial is drifting. Send a light follow-up on Day 12.

### Day 14: The Scheduled Call

This is the most important touchpoint. **Come prepared with three things:**

1. **Their data:** If you have any information about what asset classes they run (from the first conversation, from their website, from their fund filings), run the GRI correlation against the most relevant ones before the call. Have it on your screen ready to share. "I ran the GRI for Turkey against your EM fund's top-10 country weights over the last 6 months — here is what I found." This is the moment that most convinces a quant PM that you understand their problem.

2. **A current signal:** The most relevant live call in your `public_signal_log` for their coverage universe. Be ready to walk through it: thesis, current mark-to-market, invalidation condition.

3. **The question you want to answer for them:** "Is there a specific country or situation you are thinking about right now where you'd want to see how the GRI interprets it?" This gives you a next action regardless of how the call goes.

**The call's single goal:** Get to one of three outcomes:
- A. "I'd like to move forward — what does the Professional tier look like?" (Close immediately. Do not wait.)
- B. "I need to talk to my compliance/IT/PM before committing — can we schedule a follow-up?" (Get that meeting in the calendar before you hang up.)
- C. "I don't think this is the right fit right now." (Ask why. Not defensively — genuinely. This is the most valuable information you will receive in Year 2.)

If none of these three happen — if the call ends with "sounds great, I'll be in touch" — you did not close it. Send a follow-up email within 2 hours with the explicit outcomes: "Great to talk — to confirm the next step, I'll send the Professional tier terms by end of day Thursday and follow up Friday to answer any questions."

### Day 21: The Second Signal Update

Same as Day 7. Weekly GRI note. Flag large score moves. Three-sentence interpretation. No ask.

The purpose of Day 21 is to demonstrate consistency: the product showed up on Day 7 and Day 21, predictably, formatted the same way. This matters more than it sounds. Data products are trusted for the same reason infrastructure is trusted — they show up every time.

### Day 28: The Close Email

If the trial has not converted at Day 14, Day 28 is the structured close.

**Subject:** `Prospectra Trial — Week 4 Wrap`  
**Content (4 short paragraphs):**
1. "The 30-day trial ends this Friday. I wanted to send a quick summary of what was delivered: [list: Day 0 CSV, 3 weekly GRI notes, Day 14 call]."
2. "The GRI moved significantly for [most relevant country from their coverage] over the trial period — here is the 30-day summary." (Attach a 1-page PDF. One chart. The GRI score line. A signal call overlay. 5 rows of the signal log table.)
3. "If the data has been useful and you'd like to continue access, the Professional tier is $[X]/month — I'll send the one-page terms today."
4. "If the timing isn't right, I'd appreciate a sentence on why — it helps me understand what would make this product more useful for your process."

**What you want from Day 28:**
- Conversion: "Send me the terms." → Done.
- Explicit non-conversion with a reason: More valuable than you think. "We're cutting discretionary data spend through Q4" → come back in November. "Our quant says he'd prefer API access to CSV" → this is an Enterprise feature, and you now know what the upgrade condition is. "Compliance requires an SOC 2 audit before we can use any new data vendor" → log it, and note what your compliance roadmap needs to include for Year 2.
- Ghost: Follow up once, 3 days later, with one sentence. Then close the trial record. A prospect who does not respond to a Day 28 email after a 14-day call is not converting.

---

## III. Reading Trial Health Signals

At any point in the trial, you can assess conversion probability from four observable signals:

| Signal | High Conversion | Low Conversion |
|---|---|---|
| **Email response time** | Replies within 24 hours | Takes 3–5 days or stops replying |
| **Data format requests** | Asks for format changes, schema docs | No questions about the data |
| **Call preparation** | Comes to Day 14 with their own analysis | Has not looked at the data |
| **Vocabulary** | Starts saying "when we subscribe" | Continues to say "if this works out" |

The vocabulary shift is the most reliable leading indicator. When a prospect starts speaking in the future tense about the subscription as a given, the conversion is already decided — the paperwork is the trailing event.

The absence of questions is the worst sign. A quant PM who has genuinely engaged with a new data source has questions. Always. If you have heard nothing about methodology, data quality, or schema in 14 days, the data has not been opened.

---

## IV. The Contract: What It Needs and What It Does Not Need

When the prospect says "send me the terms," you need a one-page agreement ready. Not a 40-page EULA. Not a terms-of-service URL. A one-page document that covers:

1. **What is being delivered:** "Prospectra GRI Weekly Report — [coverage universe], delivered every Monday. [N] countries. Databricks Delta Sharing access to `prospectra.gold.*` (Enterprise) or CSV delivery via secure link (Professional)."
2. **Term:** 12 months. Monthly billing. 30-day cancellation notice.
3. **Permitted use:** "Licensee may use GRI data for internal investment research and portfolio management. Redistribution or resale of GRI data or derived works is prohibited without written consent."
4. **Data ownership:** "All GRI methodology, model weights, and signal logic remain the property of Prospectra Inc."
5. **Liability limitation:** "Prospectra makes no warranty as to the investment performance of signal recommendations. All investment decisions remain the sole responsibility of the Licensee."
6. **Price:** "$[X]/month, invoiced [monthly/annually], due [net 30]."
7. **Signatures:** Two lines.

That is the document. Seven items. A qualified institutional investor reading this takes 10 minutes. An enterprise procurement process that requires more will tell you — and then you engage their legal team. But leading with a 40-page contract signals that you are a vendor, not a partner. Leading with a one-page term sheet signals confidence in the product and respect for their time.

**Delaware C-Corp note:** Prospectra Inc. (Delaware, incorporated March 2026) is the correct contracting entity. Every contract should be "Prospectra Inc., a Delaware corporation." This matters if you ever need to enforce a term or raise capital — an entity without a clear contractual record is an investor concern.

---

## V. The First Revenue: What It Means Beyond the Money

When the first wire lands, three things become true:

**1. The business is validated.** Not by a pitch deck, not by a launch announcement — by a professional buyer deciding that Prospectra signal is worth paying for with their fund's money. This is a different kind of evidence than any other milestone.

**2. The obligation changes.** A paying customer is not a trial participant who can disengage without consequence. They have made a budgetary commitment, and they will hold you to delivery. Every week the GRI note does not arrive, or arrives late, or is formatted differently than last week, is a service failure. The operational discipline that was optional in the trial period is now a contractual obligation.

**3. The reference is created.** The most valuable commercial asset in a B2B data business is not a case study — it is a reference call. A professional investor at a fund who will take 10 minutes to tell a peer at another fund that the Prospectra signal is worth looking at is worth more than any marketing spend. Treat your first customer accordingly.

---

## Investment Implications

### The Customer Acquisition Cost Problem in Data Businesses

Understanding trial-to-revenue conversion mechanics has direct investment implications when evaluating data and analytics companies.

**The B2B data business model:** Customer acquisition cost (CAC) in institutional data sales is high — typical sales cycles run 3–6 months, involve multiple stakeholders (PMs, compliance, IT), and require significant demonstration effort. This is why gross margin matters so much in data businesses: the unit economics only work if customers stay for 3+ years.

**What to look for when evaluating data business investments:**
- **Net Revenue Retention (NRR):** The most important metric. NRR >120% means existing customers are growing their spend. This compounds revenue without new customer acquisition. Bloomberg, FactSet, and MSCI have all historically run NRR >110%. A new data vendor with NRR <100% in Year 2 has a leaky bucket — they are spending to acquire customers who are leaving.
- **Average Contract Value (ACV) vs. CAC:** If it costs $8,000 in time and effort to close a $6,000/year Professional tier customer, the payback period is >1 year — viable only if the customer stays 3+ years. This is why enterprise tiers (higher ACV) are so important for early-stage data businesses: they are the only customers whose economics work with long sales cycles.
- **Trial-to-paid conversion rate:** Industry benchmarks for B2B data trials are 20–35%. A conversion rate below 15% suggests either product-market fit issues or poor trial management. A rate above 40% usually means the trial period is too easy to enter — you are attracting browsers, not buyers.

**The Prospectra commercial model in investor terms:**
- Professional tier at $12K/year: LTV of $36K+ at 3-year average tenure. Acceptable if CAC (time) is <$6K.
- Enterprise tier at $60K/year: LTV of $180K+ at 3-year tenure. Excellent unit economics even with 4-month sales cycle.
- The strategic priority: One enterprise customer covers the annual cost of the Databricks infrastructure and pays for the next 6 months of CEO time. The first enterprise contract changes the business's financial trajectory more than 10 Professional conversions.

---

## Databricks Angle

**The `prospectra.gold.trial_cohorts` table (from Lesson 308):**

Before the first trial begins, the table must be live and queryable. Here is the priority build list for this week:

```sql
-- Create trial tracking table
CREATE TABLE IF NOT EXISTS prospectra.gold.trial_cohorts (
  trial_id STRING,
  prospect_name STRING,
  firm_name STRING,
  contact_email STRING,
  start_date DATE,
  end_date DATE,
  tier_offered STRING,  -- 'professional' | 'enterprise'
  coverage_focus STRING,  -- Country/region string
  data_format_requested STRING,  -- 'csv' | 'parquet' | 'delta_sharing'
  touchpoints_completed INT,  -- Count of 7-touchpoint framework completed
  day14_call_held BOOLEAN,
  day14_call_outcome STRING,  -- 'convert' | 'pending' | 'lost' | 'no_show'
  queries_run_delta_sharing INT,  -- For Delta Sharing trials
  converted BOOLEAN,
  conversion_date DATE,
  contract_acv FLOAT,  -- Annual contract value if converted
  non_conversion_reason STRING,  -- 'price' | 'track_record' | 'internal_build' | 'compliance' | 'timing' | 'no_fit' | 'ghost'
  notes STRING
)
USING DELTA
COMMENT 'Tracks all trial prospects through the 30-day commercial trial pipeline';
```

**Operational query for weekly review:**

```sql
-- Weekly trial health dashboard
SELECT
  prospect_name,
  firm_name,
  DATEDIFF(CURRENT_DATE(), start_date) AS days_in_trial,
  touchpoints_completed,
  day14_call_outcome,
  CASE
    WHEN converted = true THEN 'Converted'
    WHEN DATEDIFF(CURRENT_DATE(), start_date) > 28 AND converted = false THEN 'Overdue — Close or Log'
    WHEN day14_call_outcome = 'pending' THEN 'Awaiting Day 14 Decision'
    WHEN touchpoints_completed < FLOOR(DATEDIFF(CURRENT_DATE(), start_date) / 5) THEN 'Behind Schedule'
    ELSE 'On Track'
  END AS trial_status
FROM prospectra.gold.trial_cohorts
WHERE converted IS NULL OR converted = false
ORDER BY days_in_trial DESC;
```

**Dataset needed:** `prospectra.gold.gri_weekly` — the core data the trial CSV is generated from. Verify the last 90 days of scores are complete before any trial begins. A gap in historical coverage kills the correlation analysis that makes the Day 14 call compelling.

---

## Key Concepts Covered

1. **The four unconscious questions a trial answers** — data integration, signal orthogonality, methodology trust, incident response
2. **The 7-touchpoint trial cadence** — Day 0, 3, 7, 10, 14, 21, 28 with specific content and purpose for each
3. **Trial health signals** — email response time, data format questions, call preparation, and vocabulary shift as leading conversion indicators
4. **The Day 14 close architecture** — three acceptable outcomes; "sounds great" is not one of them
5. **The one-page contract** — seven items; why leading with simplicity is a commercial signal, not a legal risk
6. **The first revenue milestone** — validation, obligation shift, and the reference creation that compound future sales
7. **B2B data business investment metrics** — NRR, ACV vs. CAC, trial conversion benchmarks, why enterprise tier economics are structurally superior

---

## Reflection Questions

1. **The ghost scenario:** Day 10, you send the correlation question. No reply. Day 12, you send a light follow-up. No reply. Day 14, the scheduled call does not happen — they do not show up and do not cancel. What do you do? At what point do you close the trial record, and what do you say in the final email? Be specific — write the subject line and the first sentence.

2. **The known limitation gamble:** The lesson says to include an explicit known limitation in the Day 0 email — that the GRI overstates risk during commodity price spikes because GDELT conflates economic distress events with political instability. A colleague reviewing your approach says: "You're giving them a reason not to buy before they've even looked at the data. Why would you do that?" Make the case for the limitation disclosure strategy. Under what conditions would you change your mind?

3. **The compliance objection:** A prospect at Day 28 says: "We want to move forward, but our compliance team requires SOC 2 Type II certification before we can use any new data vendor. We cannot grant an exception. When do you expect to have that?" You do not have SOC 2 and are not currently pursuing it — it costs $15,000–$50,000 and 6–12 months. What do you say? What is the honest answer, and what does this tell you about which customer segments to prioritize in Year 2?

---

## Questions for Next Session (Spaced Repetition Hook)

- Write the Day 0 email in full — subject line, four paragraphs, methodology note, known limitation, and next step reminder. Bring it to the next session for review.
- What is the coverage focus of the first prospect you plan to approach? What GRI countries are in scope?
- Is `prospectra.gold.trial_cohorts` created and queryable? Run the weekly health dashboard query and confirm the output schema.

---

## Databricks Relevance Note

**Immediate pipeline tasks (this week):**
1. Create `prospectra.gold.trial_cohorts` with schema above — required before any trial begins
2. Verify 90-day history in `prospectra.gold.gri_weekly` — run a simple quality check:

```sql
SELECT MIN(score_date), MAX(score_date), COUNT(DISTINCT country_iso3) 
FROM prospectra.gold.gri_weekly 
WHERE score_date >= DATEADD(DAY, -90, CURRENT_DATE());
```

3. Build the CSV export pipeline — a parameterized notebook that takes `(coverage_countries, start_date, end_date)` and exports a clean, README-documented CSV to a secure Databricks file path. This is what generates the Day 0 data delivery without manual work.
4. Test the Day 14 demo flow yourself: open a fresh notebook, load `prospectra.gold.gri_weekly`, and time how long it takes to produce a correlation chart between GRI scores and a proxy equity index. If it takes more than 5 minutes, the demo pipeline needs work.

**The highest-value build this week:** The CSV export notebook. Every trial starts with a Day 0 CSV delivery. If that delivery takes you 45 minutes of manual data work, you will not run trials at scale. If it takes 4 minutes (run a parameterized notebook, download the output, attach to email), you will.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 309 | September 8, 2026 | Year 2 Launch Module*
