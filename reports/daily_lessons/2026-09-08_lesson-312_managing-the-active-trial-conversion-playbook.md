# Lesson 312 — Managing the Active Trial: Day 0 Onboarding, the Day-14 Check-in, and Converting a Trial User to a Paid Subscriber

**Date:** 2026-09-08
**Session Type:** Daily Lesson
**Lesson Number:** 312 / ongoing
**Topic:** The Active Trial Playbook — What Happens Between "Trial Agreed" and "First Invoice Paid"
**Curriculum Arc:** Year 2 Launch Module — Lesson 9 (From Agreed Trial to Paying Subscriber)

---

## Opening Question

*Lesson 311 ended the call. The PM said yes. You confirmed the coverage universe — Mexico, Turkey, Brazil — and told them Day 0 materials arrive tomorrow morning.*

**"You hang up the phone. You have 24 hours to deliver Day 0 onboarding materials to your first institutional trial user. What goes in the package — and what is the single most important thing the trial user needs to believe by the end of Day 1 to make conversion likely?"**

Most founders answer this wrong too. They send a product tutorial, a feature list, and a "welcome to the trial" email. They think Day 0 is about showing the user how the product works.

Day 0 is not about the product. Day 0 is about making the user feel they made a good decision.

Between agreeing to a trial and actually using the product, buyers experience what behavioral economists call *purchase regret onset* — a quiet, low-level anxiety about whether they committed to something that will waste their time. A sophisticated institutional PM does not verbalize this. But they feel it. And if you do not address it in the first 24 hours, you will spend the next 28 days chasing someone who has quietly moved on to other priorities.

This lesson covers the complete playbook from trial start to paid conversion — the onboarding mechanics, the Day-14 check-in structure, the conversion conversation, the churn signals, and the Databricks table that tracks all of it.

---

## I. Day 0: The Onboarding Package (Sent Within 24 Hours of Trial Agreement)

The Day 0 package is not a tutorial. It is an activation document. Its goal is to deliver immediate value — something they can use today — while setting the conditions for the trial to succeed.

### What goes in the Day 0 package:

**1. The GRI Dashboard for Their Coverage Universe (Personalized)**

Pull GRI weekly scores for the exact countries they named on the call — Mexico, Turkey, Brazil in this case — for the past 52 weeks. Format as a clean table: date, country, GRI score, week-over-week change, top driving factor. Not a generic dashboard. Their data.

If you have built the parameterized GRI export notebook from Lesson 311's Databricks angle, this should take 10 minutes to generate. If you have not built it yet, build it before you send the first trial pack.

**2. One Signal Insight They Did Not Ask For**

Go one step beyond what they requested. If their main concern was Mexico, include a 3-paragraph note:

> *"Since we spoke — Mexico's GRI score this week moved from 62 to 67, driven by two developments: [development 1, with source], [development 2, with source]. Based on historical correlation in the Prospectra dataset, GRI movements of 5+ points in Mexico over a 2-week period have preceded peso depreciation of 1.5%+ within 30 days in 6 of 8 comparable historical episodes. Worth watching into next week's Banxico meeting."*

This is not a trading recommendation. It is a demonstration of the analytical layer on top of the raw GRI score. It answers the question the PM had in the back of their mind when they agreed to the trial: *"Will this actually tell me something I don't already know?"*

**3. The Methodology Card (One Page, Not a Whitepaper)**

A single-page PDF with:
- The three factor categories and their weights
- The primary data sources (GDELT event feed, FRED macro indicators, curated conflict/security sources)
- The update frequency and delivery schedule
- One specific case study: a GRI movement that preceded a notable market event, with the score chart and the timeline

The methodology card should be readable in under 3 minutes. If it takes longer, rewrite it until it doesn't.

**4. The Trial Operating Parameters**

A clear, brief statement of what the trial covers and what it does not:
- Coverage: Mexico, Turkey, Brazil (plus any regional context relevant to their mandate)
- Duration: 28 days, starting [date], ending [date]
- Deliverables: Weekly GRI score update (Monday morning), event annotation feed (on significant score movements), direct access to CEO for methodology questions
- Day-14 check-in call: already scheduled or "let me know your availability the week of [date]"
- No commitment at trial end — their decision, made with 28 days of data

**5. Your Personal Availability Signal**

End the Day 0 email with one sentence that most vendors never write:

> *"If the Mexico score moves significantly before the end of the week and you want a 15-minute call to discuss the drivers, just reply to this email — I will make myself available the same day."*

This is not a promise you make lightly. But for the first trial user, you keep it. The signal it sends — that there is a real person behind the product who will respond to a live signal event in real time — is worth more than the feature list.

---

## II. Trial Week 1: Passive Monitoring and Proactive Nudges

After Day 0, most founders go quiet and wait for feedback. This is the wrong posture. The trial is not a passive product evaluation — it is a 28-day managed engagement.

### What to do in Week 1:

**Monitor their engagement signals.** If you are delivering the GRI data via email or a shared dashboard, you have signals: did they open the email? Did they access the dashboard? Did they reply? Silence in Week 1 is not neutral — it is an early churn signal.

**Send one unsolicited signal note mid-week.** By Wednesday of Week 1, send a brief email:

> *Subject: Turkey GRI — notable movement this week*
> 
> *Turkey's GRI moved from 71 to 78 this week, the largest single-week move in 6 months. The primary driver is [specific event]. Given your exposure notes from our call, wanted to flag this before Friday.*
> 
> *Full data attached. Let me know if useful — happy to dig deeper on the Turkey political dynamics if helpful.*

This email does not ask for anything. It demonstrates that the service is active, that you are watching their coverage universe specifically, and that significant movements generate real-time alerts — not just weekly reports.

**Do not send more than one unsolicited note per week.** The goal is to show the signal is active, not to flood their inbox.

---

## III. The Day-14 Check-in: Structure and Purpose

The Day-14 check-in is the most important touchpoint in the trial. It is not a status update. It is the first real conversion conversation — even if you do not name it that.

By Day 14, a trial user has seen:
- The Day 0 onboarding package
- Two weekly GRI updates (Days 7 and 14)
- At least one mid-week signal note
- Any event-driven alerts if significant movements occurred

They now have enough data to have formed an early opinion. The Day-14 call is about surfacing that opinion — positive or negative — and using it to accelerate the path to a decision.

### The Day-14 call structure (20 minutes):

**Minutes 0–3: Anchor on the data, not the product**

> *"Thanks for the time. I wanted to check in rather than just send data. You've now had two full weekly updates. Before I ask anything — was there anything in the past two weeks that the GRI moved on that you found specifically relevant to your positioning?"*

The goal of this question is to get them to surface a moment where the signal was useful. If they can cite one — "yeah, the Turkey move was interesting because we had a conversation about our TUR exposure that same week" — you have your conversion anchor. When they convert, they will tell themselves it was because of that specific moment.

**Minutes 3–10: Three diagnostic questions**

1. *"Has the data been arriving in a format that's actually usable, or are there friction points in how you're receiving it?"* — You are listening for any operational issue that could kill the conversion for non-product reasons.

2. *"Of the three countries we set up — Mexico, Turkey, Brazil — which one has felt most directly relevant to a real decision or conversation in the past two weeks?"* — This tells you which geography to lead with in the conversion pitch.

3. *"Is there anything the GRI is capturing that you would want explained differently, or a data point you expected to see that you haven't seen?"* — This is the signal that they are engaging deeply enough to have product opinions. Product opinions are a strong buying signal.

**Minutes 10–16: The signal case**

Take their answer to question 1 — the moment where the GRI was relevant — and build a 3-minute narrative around it:

> *"The Turkey move you mentioned — I want to show you what was behind that score change. Three factors drove it: [X, Y, Z]. Here's the event annotation: [show or narrate the specific events]. What's interesting is that the last comparable move in Turkey's GRI — this was in Q2 2024 — preceded a 200bps widening in Turkish sovereign spreads within 6 weeks. I am not predicting that happens here. But the pattern is worth having in mind."*

You are not making a trading call. You are demonstrating that the signal has layers — and that someone who has your data as a regular input would have had a more complete picture going into the Turkey discussion than someone who didn't.

**Minutes 16–20: The soft conversion question**

> *"You've had two weeks with the data. We have two weeks left in the trial. I want to be direct: our standard annual subscription for a three-country coverage package at your cadence is $[price]. I'm not asking for a decision today — but I want to understand whether the signal is tracking toward being useful enough to justify that, or whether there's something specific it would need to do differently in the next two weeks to get there."*

This is the Day-14 close — not a hard ask, but a transparent statement of where you are heading and an invitation for them to tell you what they need to see before the trial ends.

Their answer tells you everything about where the conversion conversation goes next.

---

## IV. The Four Trial Outcomes — and What Each Requires

By Day 28, a trial ends in one of four outcomes. Each requires a different response.

### Outcome 1: Active Engagement + Verbal Conversion Signal

The user has been engaging with the data, cited specific moments of relevance, and has either said "we want to continue" or has been clearly building the case internally. This is the best outcome.

**What to do:** Send a one-page subscription proposal within 24 hours of the Day-28 call. Do not wait for them to ask. The proposal should include: coverage package, pricing, payment terms, and a specific "founding user" offer if you are still in the first cohort. Send a DocuSign or equivalent within 24 hours of verbal agreement — the longer the gap between verbal commitment and signature, the higher the dropout rate.

### Outcome 2: Positive Engagement but Needs Internal Approval

The PM is clearly interested but cannot commit without budget approval, compliance review, or sign-off from a CIO or head of research.

**What to do:** Ask the PM directly: *"What does the internal approval process look like — who needs to be involved, and what do they need to see to say yes?"* Then prepare exactly that document. If the CIO needs a methodology whitepaper, write it this week. If compliance needs a vendor questionnaire completed, complete it. Your job is to remove every internal friction point between the PM's interest and the approval. A trial that ends in "we need to go through procurement" is not a loss — it is a longer sales cycle with a defined next step.

### Outcome 3: Low Engagement + Polite Non-Response

The user received the Day 0 materials, may have looked at the data, but has not responded meaningfully to mid-week signals and went quiet before the Day-14 check-in.

**What to do:** Do not chase. Send one final email at Day 21:

> *"Week 3 of your trial — Mexico's GRI is at [score] this week, [up/down] from last week. [One sentence on driver]. Happy to jump on a quick call if useful. If the timing isn't right, no pressure — happy to discuss again when it makes sense."*

If they do not respond, note them as "low-engagement — revisit in 90 days" in `prospectra.gold.prospect_pipeline`. Do not invest further selling time in this trial. Move to the next name.

### Outcome 4: Explicit Decline at Day 28

The user tells you it is not useful, not the right fit, or not the right time. This is the rarest outcome in a well-run trial because you will usually detect it by Day 14.

**What to do:** Thank them, ask one question — *"What would have made it more useful?"* — and take meticulous notes. Log their answer in `call_log`. The most honest post-trial feedback you receive is worth more than a positive testimonial from a convert: it tells you exactly what the product is missing.

---

## V. Churn Signals During the Trial — What to Watch For

A trial user who will not convert almost always shows signals before Day 28. Learn to read them:

| Signal | Timing | Meaning |
|---|---|---|
| No acknowledgment of Day 0 package | Day 1-2 | High churn risk — re-send with a direct question ("Did this arrive okay?") |
| No engagement with first weekly report | Day 7 | Send mid-week note with a specific signal alert; do not wait for Day 14 |
| Declined Day-14 check-in without rescheduling | Day 14 | Near-certain non-conversion; send one last data point, then pause |
| Replied to ask for "more information" without engaging with existing data | Any day | Classic stall; ask directly what specific information would move the decision |
| Said "we'll discuss internally" and went quiet | Day 14-21 | Ask for the internal decision-maker's name and offer to get on a call with them |

Churn signals compound. If you see two of these in the first two weeks, do not continue investing hours in this trial. Note them, send the week-3 note above, and focus on the next prospect.

---

## Investment Implications

### Trial Economics as a Framework for Evaluating Early-Stage Data Businesses

The trial-to-conversion dynamic described above maps directly to how sophisticated investors evaluate early-stage B2B data companies. The specific metrics matter:

**Trial conversion rate as the first proof point of product-market fit.** An institutional data company that converts more than 40% of trials to paid subscriptions has demonstrated meaningful product-market fit. Below 25% typically indicates either a product gap, a pricing problem, or a fundamental mismatch between the product's actual capability and the buyer's expectation set during the sales conversation.

**Time-to-conversion as a leading indicator of customer lifetime value.** Customers who convert quickly — within the trial window, without internal approval delays — have higher lifetime value on average than customers who take 90+ days to convert after a trial. The correlation is not perfectly causal, but the mechanism is intuitive: fast converters are buyers who immediately see the product solving a real problem. They are less likely to churn in year two because their original conviction was clear. Slow converters are buyers who converted for softer reasons — peer pressure, sunk-cost logic, FOMO — and are more likely to re-evaluate at renewal.

**The expansion revenue signal within the trial.** A trial user who asks to *expand* their coverage universe during the trial — "can you add India to the GRI reports?" — is a significantly better conversion signal than one who simply says "looks interesting." The ask for expansion is a revealed preference: they are already thinking about what the product looks like as a permanent part of their workflow. In evaluating early-stage data companies, ask the founder: "Of your trials that converted, how many asked for scope expansion during the trial?" A meaningful percentage (>20%) suggests the product has genuine pull.

**The reference customer as the only marketing asset that matters in institutional sales.** The first paying institutional customer — especially one willing to say publicly, even informally, that they use the product — is worth 10x their ARR in marketing value. Before spending on any marketing channel, the first imperative is to get one named institutional reference customer who will take a call from a prospect. When evaluating early-stage data companies, ask: "Do you have one customer who will take a reference call?" If the answer is no after 12+ months of operation, that is a deep signal about product-market fit.

---

## Databricks Angle

**Build: `prospectra.gold.trial_engagement_tracker`**

The trial engagement tracker is the operational heartbeat of the sales process. It tracks every touchpoint and engagement signal for each active trial, giving you a live view of which trials are converting and which are at risk.

```sql
CREATE TABLE IF NOT EXISTS prospectra.gold.trial_engagement_tracker (
  trial_id STRING,
  prospect_id STRING,              -- FK to prospect_pipeline
  trial_start_date DATE,
  trial_end_date DATE,
  coverage_countries ARRAY<STRING>,
  
  -- Engagement signals
  day0_package_opened BOOLEAN,
  day0_response_received BOOLEAN,
  week1_report_engaged BOOLEAN,
  week2_report_engaged BOOLEAN,
  midweek_note_responses INT,
  
  -- Day-14 check-in
  day14_checkin_completed BOOLEAN,
  day14_cited_specific_use_case BOOLEAN,
  day14_conversion_signal STRING,   -- 'strong', 'moderate', 'weak', 'absent'
  day14_internal_approval_needed BOOLEAN,
  
  -- Expansion signals
  coverage_expansion_requested BOOLEAN,
  expansion_countries_requested ARRAY<STRING>,
  
  -- Outcome
  trial_status STRING,              -- 'active', 'converted', 'declined', 'ghosted', 'approval_pending'
  conversion_date DATE,             -- populated on conversion
  decline_reason STRING,
  
  -- Metadata
  last_updated TIMESTAMP
)
USING DELTA
COMMENT 'Trial engagement tracker — real-time view of active trial health and conversion signals';
```

**The trial health query — run weekly to flag at-risk trials:**

```sql
WITH trial_health AS (
  SELECT
    tet.trial_id,
    tet.prospect_id,
    tet.trial_start_date,
    tet.trial_end_date,
    tet.trial_status,
    pp.prospect_name,
    pp.fund_name,
    pp.fund_aum_usd_bn,
    
    -- Days elapsed and remaining
    DATEDIFF(CURRENT_DATE(), tet.trial_start_date) AS days_elapsed,
    DATEDIFF(tet.trial_end_date, CURRENT_DATE()) AS days_remaining,
    
    -- Engagement score (0-5)
    (CASE WHEN tet.day0_package_opened THEN 1 ELSE 0 END +
     CASE WHEN tet.day0_response_received THEN 1 ELSE 0 END +
     CASE WHEN tet.week1_report_engaged THEN 1 ELSE 0 END +
     CASE WHEN tet.week2_report_engaged THEN 1 ELSE 0 END +
     CASE WHEN tet.day14_cited_specific_use_case THEN 1 ELSE 0 END) AS engagement_score,
    
    -- Risk flag
    CASE
      WHEN tet.day14_conversion_signal = 'absent' AND DATEDIFF(CURRENT_DATE(), tet.trial_start_date) >= 14 THEN 'HIGH_RISK'
      WHEN NOT tet.day14_checkin_completed AND DATEDIFF(CURRENT_DATE(), tet.trial_start_date) >= 16 THEN 'HIGH_RISK'
      WHEN tet.day14_conversion_signal = 'weak' THEN 'MEDIUM_RISK'
      WHEN tet.day14_conversion_signal IN ('strong', 'moderate') THEN 'ON_TRACK'
      ELSE 'MONITORING'
    END AS trial_risk_status
    
  FROM prospectra.gold.trial_engagement_tracker tet
  JOIN prospectra.gold.prospect_pipeline pp ON tet.prospect_id = pp.prospect_id
  WHERE tet.trial_status = 'active'
)
SELECT
  trial_risk_status,
  prospect_name,
  fund_name,
  fund_aum_usd_bn,
  days_elapsed,
  days_remaining,
  engagement_score,
  day14_conversion_signal
FROM trial_health
ORDER BY trial_risk_status DESC, days_remaining ASC;
```

**The conversion funnel summary:**

```sql
-- Full funnel: from trial start to converted
SELECT
  DATE_TRUNC('month', trial_start_date) AS cohort_month,
  COUNT(*) AS trials_started,
  SUM(CASE WHEN trial_status = 'converted' THEN 1 ELSE 0 END) AS converted,
  SUM(CASE WHEN trial_status = 'declined' THEN 1 ELSE 0 END) AS declined,
  SUM(CASE WHEN trial_status = 'ghosted' THEN 1 ELSE 0 END) AS ghosted,
  SUM(CASE WHEN trial_status = 'approval_pending' THEN 1 ELSE 0 END) AS pending,
  ROUND(100.0 * SUM(CASE WHEN trial_status = 'converted' THEN 1 ELSE 0 END) / COUNT(*), 1) AS conversion_rate_pct,
  AVG(CASE WHEN trial_status = 'converted' THEN DATEDIFF(conversion_date, trial_start_date) END) AS avg_days_to_conversion
FROM prospectra.gold.trial_engagement_tracker
GROUP BY DATE_TRUNC('month', trial_start_date)
ORDER BY cohort_month DESC;
```

**Immediate build tasks:**
1. Create `prospectra.gold.trial_engagement_tracker` with the schema above
2. Build the parameterized GRI export notebook: given `(country_list, lookback_days)`, generate a formatted weekly GRI report ready to send to a trial user within 10 minutes of setup
3. Set up a Monday-morning notebook that runs the trial health query and flags at-risk trials — this becomes your weekly sales operations dashboard

---

## Key Concepts Covered

1. **The Day 0 package structure** — personalized GRI data for their coverage universe, one proactive signal insight, methodology card, trial operating parameters, and a direct availability signal
2. **The proactive mid-week nudge** — why waiting for feedback is the wrong posture; how to use signal events to demonstrate value without asking for anything
3. **The Day-14 check-in structure** — anchor on data, three diagnostic questions, the signal case, and the soft conversion question
4. **The four trial outcomes** — active engagement, needs internal approval, low engagement, explicit decline — and the specific response each requires
5. **Churn signals during the trial** — the five behavioral patterns that predict non-conversion, and when to stop investing time in a low-engagement trial
6. **Trial economics as an investment framework** — trial conversion rate, time-to-conversion, expansion signals, and the reference customer as the critical first milestone
7. **`prospectra.gold.trial_engagement_tracker`** — the Databricks table and weekly health query that gives you live visibility into your trial funnel

---

## Reflection Questions

1. **The Day 0 package test:** Before running your first real trial, draft the entire Day 0 package as if the trial user is real. Use Mexico, Turkey, and Brazil as the coverage universe. Time how long it takes you to pull the personalized GRI data, write the proactive signal insight, and format the methodology card. If it takes more than 2 hours, what is the bottleneck — the GRI export notebook, the signal writing, or the formatting? That bottleneck is the first thing to automate.

2. **The Day-14 honest question:** The Day-14 call ends and the user says: "This has been interesting. I've been busy — I'll take another look at the data this week and let's reconnect at the end of the trial." You have 14 days of trial data showing they opened the Day 0 email but have not engaged with either weekly report. What do you do in the next 24 hours? What is the highest-leverage action to reverse the disengagement trajectory before Day 21?

3. **The conversion price test:** Section III says to disclose the annual subscription price on the Day-14 call. Some founders wait until Day 28 to name the price. What is the argument for Day 14? What is the argument for Day 28? Which one do you believe is right for Prospectra specifically, and why? (Hint: the answer depends on what you believe about the buyer's psychology when they are still in trial — does knowing the price make them more committed to evaluating seriously, or does it introduce a friction that causes them to mentally pre-decide before they have enough data?)

---

## Questions for Next Session (Spaced Repetition Hook)

- Have you built `prospectra.gold.trial_engagement_tracker` and run the trial health query against synthetic data?
- Have you drafted the Day 0 package for a hypothetical trial user (Mexico, Turkey, Brazil)? Did the GRI export notebook work in under 10 minutes?
- Of the four trial outcomes described — active engagement, needs approval, low engagement, explicit decline — which one do you currently have the weakest playbook for, and why?

---

## Databricks Relevance Note

**The Trial as a Data Product Test**

The 28-day trial period is not just a sales mechanism — it is a controlled experiment. Every trial user is a data source: their engagement signals, geographic interests, objections, and conversion behavior teach you what the product actually does well and what it does not.

After five trials, run this analysis:

```sql
-- Correlation between engagement signals and conversion
SELECT
  day14_conversion_signal,
  AVG(CASE WHEN day0_package_opened THEN 1.0 ELSE 0.0 END) AS pct_opened_day0,
  AVG(CASE WHEN coverage_expansion_requested THEN 1.0 ELSE 0.0 END) AS pct_requested_expansion,
  AVG(midweek_note_responses) AS avg_midweek_responses,
  COUNT(*) AS trial_count,
  SUM(CASE WHEN trial_status = 'converted' THEN 1 ELSE 0 END) AS converted
FROM prospectra.gold.trial_engagement_tracker
GROUP BY day14_conversion_signal
ORDER BY day14_conversion_signal DESC;
```

This query tells you which engagement signal is the strongest predictor of conversion. If coverage_expansion_requested is the highest predictor, you restructure the Day-14 call to make it easy for the user to request expansion — because that behavioral signal is more predictive than their words.

The trial data becomes the product roadmap. Build the tracker before the first trial, not after.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 312 | September 8, 2026 | Year 2 Launch Module*
