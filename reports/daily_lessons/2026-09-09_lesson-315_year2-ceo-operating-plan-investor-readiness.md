# Lesson 315 — The Year 2 Operating Plan: 90-Day Execution Cadence, Investor Readiness, and the CEO's Forward Guidance

**Date:** 2026-09-09
**Session Type:** Daily Lesson
**Lesson Number:** 315 / ongoing
**Topic:** Closing the Loop — From First Customer to Investor-Ready Company in 9 Months
**Curriculum Arc:** Year 2 Launch Module — Lesson 12/12 (Capstone: CEO Operating Plan and Series A Threshold)

---

## Opening Question

*Fourteen lessons ago, the Year 2 Launch Module opened with a single diagnostic: "Does the product generate real signal, or just plausible-looking data?" The module since then has covered the full arc — market landscape, signal performance, commercial packaging, the trial pipeline, the sales conversation, trial management, customer success, renewal architecture, and the scaling transition.*

**"You are on September 9, 2026. You have one paying institutional customer, a documented 90-day success framework running, and a playbook that does not yet exist as a written document. The 10-customer target is Q2 2027 — seven months away. What does the CEO do in the next 90 days, week by week, to ensure that target is on track rather than aspirational?"**

This is not a theoretical question. The Year 2 Launch Module has built out every component of the commercial engine. This lesson assembles those components into an operating plan — the CEO's actual calendar and priority stack for Q4 2026.

---

## I. The State of Play: September 9, 2026

Before building the 90-day plan, the CEO needs an honest accounting of where the company stands. No aspirational framing. Actual status.

### The GRI Platform

The Databricks platform is production-grade. The bronze/silver/gold pipeline is running. The GRI produces weekly scores for at least Mexico, Turkey, and Brazil — the coverage universe the first customer is paying for. The signal has been validated against at least one market event in the past 12 months where the GRI moved meaningfully before the market. The track record is documented in `reports/daily_lessons` and `reports/weekly_lectures`.

**Platform status: functional and defensible.**

### The Commercial Position

One paying institutional customer. The trial was converted. The 90-day customer success framework is running. The first monthly touchpoint is either complete or imminent. The customer has not yet been asked for reference permission — that conversation is month three.

The sales playbook — the ICP, discovery framework, demo template, objection library, trial activation sequence, conversion script, and customer success framework — exists in twelve separate lesson files. It does **not** exist as a single, consolidated written document.

**Commercial status: proof of concept, not repeatable engine.**

### The Pipeline

The prospect pipeline is either empty or contains 1–3 exploratory conversations that have not yet reached the discovery call stage. There is no inbound infrastructure — no public signal archive with regular publication cadence, no Substack subscriber list, no Snowflake Marketplace listing, no prime brokerage conversation initiated.

**Pipeline status: pre-zero. The machine has not been started.**

### The Investor Position

The company is not investor-ready. The ten-customer threshold for a credible Series A conversation has not been reached. The track record of paid subscriptions is too short (under 90 days) to calculate LTV, NRR, or CAC with any statistical validity. There is no cap table update required, no external capital needed, and no investor conversation worth having.

**Investor status: build the business first.**

This accounting is not a failure assessment. It is a map. The 90-day plan starts from this exact position, not from where the company wishes it were.

---

## II. The 90-Day Operating Plan: September–November 2026

### Week 1 (September 9–15): Consolidation and Playbook

**The single most important deliverable of week one is the Prospectra Institutional Sales Playbook, Version 1.0.**

Not a new concept — every component has been built in Lessons 309–314. The task is consolidation: take the ICP (Lesson 314), the discovery framework (Lesson 314), the demo template (Lessons 310–311), the objection library (Lesson 311), the trial activation sequence (Lesson 311), the conversion script (Lesson 312), and the customer success framework (Lesson 313), and write them into a single document.

Format: a Google Doc, not a Notion wiki. It should be printable. It should be something a new salesperson can read in 90 minutes and use on a call the next day. Target length: 15–20 pages.

**The week-one deliverable is this document, not a plan to create this document.**

Parallel task: set up the Prospectra Substack. Draft the first weekly signal post using this week's GRI data — what moved, why, what the investment implication is. Publish it. The publication cadence begins in week one, not "eventually."

**Databricks task:** Build `prospectra.gold.prospect_pipeline` with the `acquisition_channel` column (Lesson 314). Every future prospect entry requires a channel attribution at the time of entry, not retroactively.

---

### Week 2 (September 16–22): Prospecting Sprint and First 20

The ICP from the sales playbook identifies the target universe: EM-focused long-only funds and credit funds, $500M–$5B AUM, US/UK/Switzerland/Singapore. The task this week is to build the first 20-prospect list.

**How to build the first 20:**
- LinkedIn Sales Navigator search: EM fund managers at firms with AUM in the ICP range, with geopolitical risk or country risk in their stated investment process or public commentary
- Eurasia Group client lists (published in event materials and conference agendas)
- Conference attendee lists from Emerging Markets Forum, ACI annual conferences, Cambridge Finance events
- Funds that have made public statements about EM political risk — Bloomberg, Reuters, FT quotes from PMs on geopolitical risk

For each prospect, document: fund name, AUM (estimated), coverage geography, PM/analyst contact, how they were found (channel attribution). This is the seed data for `prospectra.gold.prospect_pipeline`.

**First outreach emails go out in week two.** Using the personalized outreach template from Lesson 310 — leading with a specific observation about their fund's coverage universe and a brief mention of the most significant GRI movement in their geography in the past month.

**Week two target:** 20 prospects identified and documented in Databricks. 10 outreach emails sent.

---

### Week 3 (September 23–29): Customer #1 Month-One Touchpoint

The first paying customer's month-one check-in falls in late September. The month-one agenda (Lesson 313):

> "Let's look at what moved this month — Mexico, Turkey, Brazil — and I want to understand whether any of those movements intersected with conversations you were having internally."

Prepare for this call with the month-one GRI movement summary: pull the weekly scores for all three countries across September, identify the single most significant movement, and build a one-page narrative around it before the call. The goal is to identify the proof moment — the week where a GRI movement corresponded to something real in the customer's investment process.

**If the proof moment is found:** document it immediately in `customer_success_tracker.month1_proof_moment_description`. It is the most valuable asset the company will have in the next sales conversation.

**If the proof moment is not found:** ask directly what the customer was watching in September that generated the most internal conversation. Then check whether the GRI was moving during that period. If it was and the customer didn't notice, the failure is delivery and communication — fix the alert mechanism. If it was not moving, the failure is coverage — evaluate whether a fourth country needs to be added.

**Parallel task:** Outreach follow-up on week two emails. Discovery calls scheduled for any responses received.

---

### Week 4 (October 1–6): Substack Post #4 and First Event Moment Trigger

By week four, the Substack has published four consecutive weekly signal posts. The subscriber list is small — 20–50 people at most. But the archive exists. Four published posts is enough to say "we publish consistently" in a prospecting email. Twelve posts is enough for a prospect to evaluate the analytical framework independently.

**The event moment trigger:** If any significant geopolitical event occurred in September that the GRI flagged in advance — an election surprise, a sanctions announcement, a commodity supply disruption, a central bank emergency move — week four is the time to publish the event moment piece: "What the Prospectra GRI showed in the three weeks before [event]."

The event moment piece goes to: the Substack list, all 20 prospects in the pipeline with a personalized note ("Given [their geography] is in your coverage universe..."), and LinkedIn.

If no significant event occurred, the week-four task is to identify the most significant GRI movement in September across the full 10-country coverage universe and write the "what the GRI is telling us right now" piece — forward-looking, specific, and falsifiable.

---

### Month 2 (October): Trials and Discovery Cadence

The goal for October is to have at least two active trials running simultaneously by the end of the month. Given the 28-day trial length and the time required to move a prospect from first contact to trial start (2–4 weeks), any trial that starts in October required a prospecting contact in September. The week two and three outreach is what makes October trials possible.

**October operating rhythm:**
- Monday: Substack weekly signal post publishes. GRI delivery to Customer #1 by 8am their time.
- Tuesday: Prospecting follow-ups. Discovery calls scheduled for any responses to September outreach.
- Wednesday–Thursday: Discovery calls (the scheduled ones). Demo preparation for any discovery call that advances.
- Friday: Pipeline update in Databricks. `prospect_pipeline` updated with stage changes, next steps, and any new contacts identified.

**October target:** 2 active trials started. 10 new prospects added to the pipeline (cumulative 30). 5 discovery calls completed.

---

### Month 3 (November): Customer #1 Month-Three Evidence and Trial Conversions

November is the highest-stakes month of the 90-day plan for two reasons simultaneously.

**First:** Customer #1's month-three touchpoint. The Evidence conversation (Lesson 313) — the request for the evidence artifact and the first reference permission conversation. This conversation should be prepared with the one-page case study draft in hand: the GRI score history, the proof moment documented in month one, the integration artifact built in month two. The customer is being asked to review something that already exists, not to create something new. That is the difference between a conversation that takes 15 minutes and one that stalls indefinitely.

**Second:** The first October trials are reaching their conversion windows. Days 14, 21, and 28 of the October trials fall in November. The conversion conversations from Lesson 312 run their full sequence.

**November target:** Customer #1 reference permission obtained (Tier 1: case study customer). At least one of the October trials converts to a paying subscription (Customer #2). `customer_success_tracker` updated for both customers.

---

### The 90-Day Scorecard: What Success Looks Like by November 30

| Metric | Target | What It Proves |
|---|---|---|
| Sales Playbook V1.0 written | ✓ (week 1) | Process is transferable |
| Substack posts published | 12 | Consistent analytical cadence |
| Prospects in pipeline | 40+ | Enough top-of-funnel to hit 10 customers |
| Discovery calls completed | 8–10 | ICP qualification at scale |
| Trials started | 3–4 | Conversion engine running |
| Paying customers | 2 | First repeatability signal |
| Customer #1 reference tier | Tier 1 (case study) | Distribution asset activated |
| NRR on Customer #1 | >100% (no churn) | Unit economics positive |
| Snowflake Marketplace application | Initiated | Channel infrastructure started |

Hitting six or more of these eight targets by November 30 means Q2 2027's 10-customer target is on track. Missing more than three means the CEO must diagnose the specific bottleneck — top-of-funnel (not enough prospects), conversion (trials not closing), or delivery (customer success failing) — and address it before December.

---

## III. The Investor Readiness Threshold — And Why It Is Not Now

The 10-customer milestone (Lesson 314) is the minimum threshold for a credible Series A conversation. At this moment — one customer, September 2026 — no investor conversation is warranted.

This is not a judgment on the company's potential. It is a statement about the information asymmetry problem.

At one customer, you cannot calculate:
- **CAC** (one data point is not a cost-per-acquisition)
- **LTV** (no churn data, no renewal data)
- **NRR** (no renewals have occurred)
- **Trial-to-conversion rate** (one trial converted does not establish a rate)
- **Sales cycle length** (one deal is not a distribution)

An investor who hears Prospectra's story today sees a compelling thesis and a working product, but no evidence that the thesis is commercially repeatable. They cannot underwrite the risk without those metrics. An investor conversation at this stage either ends in a pass ("come back with more data") or in exploitative terms ("I'll take 30% at a $1.2M cap because you have no leverage").

**The right investor conversation happens at 10 institutional customers, not before.**

At 10 customers, you can present:
- Average ARR per customer ($35,000–$45,000 range, depending on expansion)
- Trial-to-conversion rate (a real number, based on 15–25 trials)
- Sales cycle length (median days from first contact to payment)
- NRR (based on the first cohort of customers reaching renewal)
- CAC by channel (because channel attribution was tracked from the start)
- LTV/CAC ratio (because you have both numbers)
- The case study reference customer (because you asked for permission in month three)
- The reference call customer (because the reference network has been deliberately built)

That data package is what makes an investor conversation worth having. Everything before that is a pitch. Everything after that is a negotiation.

### The One Exception: Strategic Capital

If a macro advisory firm, a prime brokerage, or an institutional data company offers a strategic investment or acquisition conversation before the 10-customer threshold, the calculus changes. Strategic capital is not valued the same way as financial capital — the strategic investor is paying for a relationship, a distribution channel, or a competitive option, not just for the financial return. A conversation with a macro advisory firm that would give Prospectra access to their institutional client network is worth having at five customers, not just ten.

But the default is: build the business to 10 customers before any investor conversation.

---

## IV. The Forward Guidance: Q4 2026 Through Q2 2027

| Quarter | Primary Goal | Milestone Metric |
|---|---|---|
| Q4 2026 (Oct–Dec) | Build the commercial engine | 2–3 paying customers; playbook V1.0; Substack at 24 posts; Snowflake Marketplace initiated |
| Q1 2027 (Jan–Mar) | Scale the pipeline | 5–7 paying customers; first reference call customer (Tier 2); CAC by channel calculable |
| Q2 2027 (Apr–Jun) | Reach the threshold | 10 paying customers; NRR first cohort ≥100%; investor-ready data package assembled |

The quarterly goals are directional, not contractual. The CEO should revisit them at each quarter's end with honest accounting — the same accounting applied in Section I above.

**The one non-negotiable:** the 10-customer target is Q2 2027. If it is not on track by Q1 2027 (five or fewer customers by March), the CEO must identify which bottleneck is structural — and either fix it or revise the target with explicit reasoning. A revised target is not a failure. An unreflective miss is.

---

## V. The CEO's Weekly Operating Cadence (Ongoing)

Every week for the foreseeable future, the CEO's calendar has the same recurring structure:

**Monday (2 hours):**
- GRI weekly delivery to all paying customers by 8am their time
- Substack weekly signal post published
- Pipeline health check in Databricks: `prospectra.gold.prospect_pipeline` reviewed, stage changes updated
- Customer health check: `prospectra.gold.customer_success_tracker` reviewed for upcoming milestones and renewal flags
- Revenue engine dashboard: pipeline coverage ratio calculated — is it above 3x?

**Tuesday–Thursday (variable):**
- Prospecting outreach: 5–10 new contacts per week
- Discovery calls (scheduled from prior week outreach)
- Demo preparation (for any discovery calls advancing to demo)
- Active trial touchpoints (day 3, day 7, day 14 check-ins for any running trials)
- Databricks build tasks (from the current sprint — whatever the build backlog requires)

**Friday (1 hour):**
- Weekly decision log update: what was learned this week about the customer, the product, or the market that changes how the CEO thinks about the business
- Next week prep: what are the three most important things the company needs to accomplish next week, and in what order?

**Monthly (1 × 2-hour block):**
- Customer touchpoint calls (one per paying customer)
- Lesson delivery (if the automated session doesn't fire) — the CEO is always learning, not just executing
- Framework audit: is anything in the investment thesis or the commercial thesis being invalidated by new information? What changes?

---

## Investment Implications

### The B2B Data Company Operating Plan as an Investment Lens

The 90-day operating plan above is not just an execution framework for Prospectra. It is a template for evaluating whether any early-stage B2B data company is being run with the discipline that creates institutional value.

**The playbook consolidation test:** A company that has closed three customers but cannot produce a written sales playbook is operating on founder intuition. That is a significant execution risk at Series A — because the first sales hire will fail, the founder will be blamed, and the root cause will remain unaddressed. When evaluating early-stage B2B data companies as investments, ask for the sales playbook before the financial model. A founder who produces one immediately has built a scalable process. A founder who needs two weeks to produce one is working from memory.

**The prospecting cadence as a leading indicator:** Revenue lags prospecting by 6–10 weeks (the time from first contact to trial start to conversion). A company reporting consistent revenue growth should have been running consistent prospecting cadence 6–10 weeks before each revenue quarter. If a company cannot show their prospecting activity log for Q2 when asked about Q3 revenue growth, the growth is more likely event-driven than system-driven.

**The Substack/content archive as a credibility asset:** A B2B data company that has published 52 weekly analytical pieces — consistently, on schedule, with a documented track record of what called right and what missed — has created an asset that cannot be faked. It demonstrates analytical discipline, methodological transparency, and product confidence. It is also the primary inbound acquisition channel for the next 50 customers. Investors should ask: "Does this company have a public body of analytical work I can evaluate?" If the answer is no, the company is relying entirely on private demos to prove product quality — a much weaker credibility signal.

---

## Databricks Angle

**Build: `prospectra.gold.ceo_weekly_operations`**

The CEO's weekly operating cadence is a process. Processes that are not tracked are not managed. The following table tracks the CEO's weekly execution against the 90-day plan.

```sql
CREATE TABLE IF NOT EXISTS prospectra.gold.ceo_weekly_operations (
  week_start_date DATE,
  
  -- Monday delivery (non-negotiable)
  gri_delivery_on_time BOOLEAN,
  substack_post_published BOOLEAN,
  substack_post_topic STRING,
  
  -- Pipeline health
  prospects_in_pipeline INT,
  active_trials INT,
  paying_customers INT,
  pipeline_coverage_ratio DECIMAL(5,2),
  
  -- Prospecting activity
  new_contacts_this_week INT,
  outreach_emails_sent INT,
  discovery_calls_completed INT,
  demos_delivered INT,
  
  -- Trial management
  trial_activations_this_week INT,
  trial_conversions_this_week INT,
  trial_day14_conversations_completed INT,
  
  -- Customer success
  monthly_touchpoints_completed INT,
  customer_proof_moments_documented INT,
  reference_permission_conversations INT,
  
  -- Build progress
  databricks_tasks_completed STRING,    -- brief description of what was built
  databricks_tasks_deferred STRING,     -- what was planned but not done, and why
  
  -- Weekly reflection
  most_important_learning STRING,       -- one sentence: what changed about how the CEO thinks
  next_week_priority_1 STRING,
  next_week_priority_2 STRING,
  next_week_priority_3 STRING,
  
  -- Metadata
  last_updated TIMESTAMP
)
USING DELTA
COMMENT 'CEO weekly operating cadence tracker — the executive dashboard for a founder running a revenue-stage company';
```

**The weekly health query — 30 seconds every Friday:**

```sql
WITH last_4_weeks AS (
  SELECT *
  FROM prospectra.gold.ceo_weekly_operations
  ORDER BY week_start_date DESC
  LIMIT 4
)
SELECT
  week_start_date,
  paying_customers,
  active_trials,
  new_contacts_this_week,
  pipeline_coverage_ratio,
  gri_delivery_on_time,
  substack_post_published,
  trial_conversions_this_week,
  most_important_learning
FROM last_4_weeks
ORDER BY week_start_date DESC;
```

If `gri_delivery_on_time` is FALSE for any week: that is the most important diagnostic in the table. Delivery reliability is the foundation. Everything else is downstream of it.

If `pipeline_coverage_ratio` drops below 2.0 for two consecutive weeks: the prospecting cadence must increase immediately, not "next quarter." A pipeline that falls below 2x coverage at current close rates cannot sustain one new customer per month.

If `substack_post_published` is FALSE for any week: break the streak investigation. Was there a legitimate reason (a major customer crisis, a platform outage)? Or was it deprioritized? If deprioritized: the CEO chose short-term execution over long-term inbound infrastructure. One week is acceptable. Two weeks is a pattern.

**Immediate build tasks for week one:**
1. Create `prospectra.gold.ceo_weekly_operations` with the schema above
2. Enter the week of September 9, 2026 as the first row — with honest values for each field (most will be zeroes, and that is the point)
3. Set a recurring Monday notebook in Databricks that pre-populates the week's row with calculated metrics from existing tables (`prospect_pipeline`, `customer_success_tracker`, `revenue_engine_dashboard`) so the CEO only needs to fill in the qualitative fields

---

## Key Concepts Covered

1. **The honest state of play** — a no-framing assessment of where the company stands on September 9, 2026 across platform, commercial position, pipeline, and investor readiness
2. **The 90-day operating plan** — week-by-week priorities from September 9 through November 30, with specific deliverables, not intentions
3. **The playbook consolidation imperative** — why week one's most important task is a 15-page document, not a new prospecting strategy
4. **The investor readiness threshold** — why the Series A conversation does not happen before 10 institutional customers, and what data package makes that conversation worth having
5. **The strategic capital exception** — the one scenario where investor conversations make sense before the 10-customer threshold
6. **The CEO's weekly operating cadence** — the Monday/Tuesday–Thursday/Friday structure that runs the commercial and analytical engines simultaneously
7. **`prospectra.gold.ceo_weekly_operations`** — the Databricks table that makes the operating cadence auditable and traceable

---

## Reflection Questions

1. **The week-one test:** It is Monday morning, September 14. The Prospectra Institutional Sales Playbook Version 1.0 is either done or it is not. If it is done, what specifically did it take to finish it — and what did you learn about the sales process by writing it down? If it is not done, what is the specific reason it did not happen in the allotted week? Name the blocker. Now ask: is that blocker structural (a real competing priority) or behavioral (it was uncomfortable to formalize something that has been intuitive)? Different blockers require different responses.

2. **The pipeline coverage math:** The 10-customer target is Q2 2027 — seven months away. You have one customer. You need nine more. At a trial-to-conversion rate of 50% (a reasonable early assumption), nine customers require 18 trials. At a prospect-to-trial rate of 25% (also reasonable), 18 trials require 72 qualified prospects. You have seven months to identify, qualify, and advance 72 prospects to trial. That is approximately 10 new qualified prospects per month. Is your current prospecting cadence generating 10 qualified prospects per month? If not, what is the gap — and is it a targeting problem (not finding enough ICPs), a conversion problem (not getting enough discovery calls), or a capacity problem (not enough hours in the week)?

3. **The forward guidance exercise:** Write the CEO's Q2 2027 operating review as if it is June 30, 2027, and Prospectra has hit 10 institutional customers. What happened in Q4 2026, Q1 2027, and Q2 2027 that made it possible? Now write the same review from the scenario where Prospectra reached only five customers by Q2 2027. What went wrong — and was it foreseeable on September 9, 2026? The second exercise is more valuable than the first: the obstacles that would produce five customers instead of ten are visible today. Naming them now is the only way to act on them before they materialize.

---

## Questions for Next Session (Spaced Repetition Hook)

- Is the Prospectra Institutional Sales Playbook V1.0 a written document as of September 16? If yes, what was the hardest part to write — and what did the difficulty reveal about the sales process? If no, when specifically will it be done?
- What is the GRI score for Mexico, Turkey, and Brazil this week? Which country showed the largest movement, and what is the investment implication of that movement?
- Has the first Substack post been published? If yes, what was the subscriber response? If no, what is the specific publish date and topic for the first post?

---

## Databricks Relevance Note

**The Operating Data as a Company Health Signal**

The `ceo_weekly_operations` table is not just an execution tracker. It is a longitudinal dataset of how an early-stage revenue-stage company was actually run — week by week, deliverable by deliverable, learning by learning.

After 52 weeks of entries, this table tells a story that no investor deck can tell: the actual cadence of execution, the weeks where delivery slipped and why, the moments where the most important learning changed the company's direction. It is the audit trail of decision quality, not just decision outcomes.

That audit trail is the foundation of the framework audit that runs quarterly (referenced in `PROJECT_FOUNDATION.md`, Section 6). Were the decisions made each week consistent with the investment thesis and the commercial architecture built in this curriculum? Where did the CEO deviate from the plan, and was the deviation justified? A company with 52 weeks of honest weekly operating data can answer those questions rigorously. A company without it is working from memory and narrative.

Build the table in week one. Enter week one's data honestly. The compounding value of that practice begins with the first row.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 315 | September 9, 2026 | Year 2 Launch Module — Capstone*
