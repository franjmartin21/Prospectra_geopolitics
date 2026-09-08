# Lesson 310 — The Prospect Pipeline: Finding, Qualifying, and Approaching the First 10 Trial Candidates

**Date:** 2026-09-08
**Session Type:** Daily Lesson
**Lesson Number:** 310 / ongoing
**Topic:** The Prospect Pipeline — How to Fill the Top of the Funnel for an Institutional Data Product
**Curriculum Arc:** Year 2 Launch Module — Lesson 7 (From Trial System to Prospect Engine)

---

## Opening Question

*Lesson 309 built the complete trial management architecture: Day 0 through Day 28, every touchpoint, the contract, the conversion signals. You can now run a trial with discipline.*

**"You've published 4 weeks of GRI Weekly Notes. You have the demo ready, the one-page terms ready, and the trial cohorts table live. Your entire conversion process is designed and built. Now: where does the first conversation come from? Right now — not hypothetically — write down the names of three specific people you know personally who you believe would take a 30-minute meeting about a geopolitical risk signal."**

If you can name three, you have a funnel. If you cannot, you have a product without a distribution channel, and that is the most common reason technically excellent data products never reach commercial viability.

The trial pipeline is the engine. The prospect pipeline is the fuel. Lesson 309 told you how to convert a conversation. This lesson tells you how to get the conversation.

---

## I. The Fundamental Problem of Institutional Sales Prospecting

Most founders of data and research products believe the hardest part is building the product. It is not. The hardest part is finding the people with authority, budget, and a specific problem that matches what you built — and reaching them in a way that earns 30 minutes of their time.

Institutional buyers of financial data have four characteristics that make prospecting different from any other B2B market:

### 1. They are unreachable through normal channels
A PM at a $500M systematic fund does not answer cold LinkedIn messages, respond to email blasts, or attend marketing webinars. They do not have a "vendor intake" form. Their calendar is managed by an assistant who screens requests. A cold approach that does not carry prior context — a mutual connection, a published piece of analysis they have already read, a prior professional relationship — will not be read.

### 2. They are decision-makers, not evaluators
In most software sales, you sell to an evaluator who sells internally to a decision-maker. In institutional data sales, the PM is often the decision-maker AND the evaluator. There is no champion problem — if the PM thinks your signal is credible, the deal moves. But there is also no multiple-stakeholder nurture path. If the PM is not interested, the deal is dead.

### 3. Their budget cycle matters
A fund with a January–December fiscal year has data budget conversations in September–November. Approaching them in February means your trial converts in April — but the contract does not start until the next budget cycle in January. You can spend 9 months with a "willing to buy" prospect who cannot formally commit until January. Understanding budget cycles prevents working hard on prospects who have already closed their spend for the year.

### 4. Their credibility bar is high and their patience for hype is zero
They have been pitched bad data products by confident founders. They have seen backtests that do not hold in live trading. They have bought signals that decayed. Their default posture toward a new, unfamiliar data vendor is skepticism. The thing that moves them out of skepticism is not a great pitch — it is a specific piece of analysis that was correct, in writing, before the event happened.

This is why the public signal log is the most important prospecting asset you have. It is the thing you cannot fake retroactively.

---

## II. The Three Sources of Conversations

### Source 1 — Inbound from the Public Signal

Someone reads the weekly GRI note on LinkedIn or Substack and messages you. This is the highest-quality lead because the qualification has already happened: they sought you out, they found the analysis credible enough to reach out, and they are coming with context.

**The conversion rate from inbound message to trial:** typically 40–60% in institutional research markets. These are pre-qualified buyers. Never let an inbound message go unanswered for more than 4 hours.

**The operational task:** Read every like, share, and comment on the GRI Weekly Notes. Not to manage vanity metrics — to identify who is engaging. A "like" from a VP Portfolio Manager at a systematic fund is not a vanity metric. It is a warm lead. Their name goes into `prospectra.gold.prospect_pipeline` with engagement score = 3 (strong signal, no outreach yet).

**The patience required:** Inbound from a Substack with 200 subscribers takes 8–16 weeks of consistent publishing to materialize. You will not get inbound in week 4. You may not get it in week 8. The publishing is not primarily about inbound — it is about credibility. When you reach out to a prospect through any other channel, the first thing they do is Google you. If your weekly GRI notes show up, the conversation starts differently.

### Source 2 — Warm Introductions

Someone you know introduces you to someone who matches the buyer profile. This is the second-highest-quality lead channel and is dramatically underused by technical founders who are not comfortable asking for introductions.

**The Prospectra network map:**

Francisco's professional network has two unusually valuable clusters:

**Cluster A — Databricks customers.** As a Databricks Solutions Architect, Francisco has direct professional relationships with data engineers, quant researchers, and technical PMs at dozens of companies — many of which are in financial services. These are people who already use Databricks, which means the Delta Sharing conversation for the Enterprise tier is frictionless. A quant PM who already uses Databricks and learns that Prospectra GRI data is available via Delta Sharing already knows exactly how they would use it.

**The ask:** "I'm building a geopolitical risk signal product for systematic investors. The output is a weekly GRI score for 80 countries, delivered via Delta Sharing directly into Databricks. If you know anyone in systematic macro, EM equity, or commodity trading who might find that useful, I'd welcome an introduction." This is a specific, low-friction ask that takes 30 seconds to forward.

**Cluster B — Mexican and Latin American financial services network.** LATAM is an explicitly underserved market for institutional geopolitical risk data. Bloomberg's coverage of Mexican political risk (AMLO's successors, Pemex dynamics, near-shoring security issues) is generic. A GRI signal with granular Mexico, Colombia, Peru, Chile, and Brazil coverage from an operator who understands the region is a differentiated product for LATAM-focused funds and family offices.

**The introduction arc:** Map every person in your first-degree LinkedIn network who works in finance. Not only EM or systematic — anyone in finance. Some of them will have colleagues, clients, or former classmates who fit the buyer profile. The introduction request is always more effective when you send them a specific GRI note first: "I wrote this on Mexico's political risk dynamics post-election. If you know anyone who trades EM or thinks about LATAM macro, I'd appreciate an introduction."

### Source 3 — Targeted Cold Outreach (with Signal as Entry Point)

This is the lowest-conversion channel but the only one that scales without depending on your existing network. Executed correctly, it converts at 5–15% to a conversation. Executed incorrectly, it converts at 0% and damages your reputation.

**The rule:** Never send a cold outreach that does not include a specific, relevant, publicly-verifiable piece of analysis. The cold outreach is not an introduction to yourself. It is a delivery vehicle for a piece of analysis that is useful to the recipient regardless of whether they ever hire you.

---

## III. The Prospect Qualification Framework

Not every fund manager is a real prospect. Before investing time in outreach, score each prospect on five dimensions:

| Dimension | 3 Points | 1 Point | 0 Points |
|---|---|---|---|
| **Mandate match** | Systematic macro, EM equity/FX, commodities, quant multi-strat | Discretionary macro, global equity with EM sleeve | Fixed income only, domestic equity only |
| **AUM tier** | $100M–$5B | $5B+ (hard to sell to) or $20M–$100M (thin budget) | <$20M |
| **Contact seniority** | PM, CIO, Head of Research | Analyst, associate | Marketing, IR, admin |
| **Data sophistication** | Uses Python/R, Databricks, or similar | Uses Excel for data analysis | Opaque on process |
| **Geopolitical exposure** | Actively manages geopolitical risk in mandate | Aware of it, no formal process | Does not factor it in |

**Minimum viable prospect:** 9+ points. Below 9, the outreach investment is unlikely to produce a trial.

**The ideal first 10 prospects:** Score at least 12/15, mix of inbound (already have context) and warm intro (already have a relationship buffer), covering at least three distinct fund types so you learn which buyer profile converts fastest.

---

## IV. The Cold Outreach Architecture

When warm introductions are exhausted and inbound is insufficient, targeted cold outreach fills the gap. Here is the exact process:

### Step 1: Identify by name

The right prospect at a fund is usually the person with PM, Portfolio Manager, CIO, Head of Research, or Systematic Strategies in their title. LinkedIn Premium (or a free trial) is sufficient for this research. The fund's website often lists the team.

**Identify by fund first, person second.** Start with a list of 30 funds that match your mandate criteria. Then find one specific name at each.

### Step 2: Research before writing

Before any outreach, find one thing about their mandate that is publicly available: a conference talk they gave, a paper they co-authored, a Bloomberg interview, their firm's investor letter if it's public, or a fund filing. The outreach should contain a sentence that proves you spent 10 minutes on them before sending it.

### Step 3: The email

**Subject:** `[Specific country or event] — geopolitical signal you may not have`

Do not make the subject about yourself. Make it about something they care about.

**Body (four sentences maximum):**

1. One sentence proving you researched them: "I follow your firm's EM work — your [Q2 letter / that Bloomberg interview / the conference talk] on [specific topic] is the best thing I've read on [subject] in the last quarter."

2. One sentence about what happened (the signal): "The Prospectra GRI scored [Country X] a 72 last Monday — the highest since [event] in [year] — driven by a specific shift in [event category]. That level has historically preceded [specific outcome] within 90 days."

3. One sentence about why this matters for them specifically: "Given your exposure to [relevant geography/sector], I thought the data point was worth a look."

4. The ask: "I publish the full methodology and weekly scores — happy to send this week's GRI note for your coverage universe if it would be useful."

**Total length:** Under 150 words. Do not pitch the product, the pricing, or the company story in the first email. Deliver value. Ask for permission to deliver more.

### Step 4: The follow-up cadence

- If no reply in 5 days: one follow-up, one sentence. "Just flagging this — happy to send the GRI data for [their coverage region] if useful. No commitment required."
- If no reply to the follow-up: close the prospect for 90 days. Tag in the pipeline: "Cold — retry Q4." Do not send a third email.
- If they reply with interest: you are in the demo/trial flow. Move to Lesson 308 immediately.
- If they reply with "not interested" or "we're covered": reply with "Understood — thank you for the response. I'll keep the weekly note coming in case anything in the GRI data becomes relevant." Then subscribe them (with consent) to the public signal list.

---

## V. The Pipeline Mathematics

To reach $100K ARR at a blended price of $18K/year (2 Enterprise at $36K, 4 Professional at $12K), you need 6 customers. Here is what that requires:

| Stage | Count | Rate | Required Input |
|---|---|---|---|
| Conversations (demo ready) | 18 | → trials at 50% | 18 qualified calls |
| Trials | 9 | → convert at 35% | 9 30-day trials |
| Paying customers | ~3 | — | First $36K–$54K ARR |
| Target (6 customers) | 6 | — | 2 pipeline cycles |

To get 18 qualified conversations, you need:
- 5–6 inbound leads (8–16 weeks of publishing)
- 4–5 warm introductions (network activation, 4–8 weeks)
- 8–10 targeted cold outreach responses (60–80 cold emails at 10–15% response rate)

**Timeline implication:** If you start outreach today (September 8), the math says:
- First trials start: October 2026
- First conversions: November 2026
- First meaningful ARR: December 2026 / January 2027

This is not pessimistic — it is what institutional B2B sales timelines look like. Founders who do not understand the math expect revenue in 6 weeks and give up at week 10. The math says 14–18 weeks to first meaningful ARR, assuming you work the pipeline consistently.

---

## VI. The 10-Name Exercise

The most valuable 30 minutes you will spend this week is not writing code. It is this:

Open a blank document. Write 10 names. For each name:
- Who they are (fund, role, AUM estimate)
- How you know them or how you will reach them (warm intro / cold / inbound)
- What they care about (geography, asset class, risk type)
- What GRI note would be most relevant to send them
- What your outreach angle is

This list is the Prospectra sales pipeline. It is a document, not a database — until you have worked all 10 names through at least one outreach attempt, you do not need CRM software. The list is the CRM.

When all 10 names have been contacted and outcomes logged (trial / declined / no response), do the exercise again with 10 new names.

**The honest question to ask yourself when building the list:** Is this person a real buyer, or are they someone I'm comfortable reaching out to? These are not the same thing. The person you are most comfortable contacting is often the one least likely to write a check.

---

## Investment Implications

### How Distribution Strategy Affects the Valuation of Data Businesses

Understanding institutional sales distribution has direct implications when valuing data and research companies at the pre-revenue or early-revenue stage.

**The distribution premium:** Two data businesses with identical products and signal quality will be valued completely differently based on their distribution architecture. A product with inbound-driven distribution (Substack → trial → contract) commands a higher multiple at the same ARR than one with direct outbound sales, because inbound signals product-market fit and organic growth. Investors call this "go-to-market efficiency" — but it is really a question of whether customers come to you or you hunt them.

**MSCI's distribution model:** MSCI built its institutional franchise not by cold-calling PMs but by becoming the benchmark provider — embedding its index methodology so deeply into institutional portfolios (ETF benchmarks, performance attribution, risk systems) that removing it would require rebuilding the entire investment infrastructure. The distribution channel was the product itself. Every new fund that benchmarks to MSCI automatically becomes a customer.

**The Prospectra distribution question:** The most defensible distribution channel for Prospectra is not direct outreach — it is becoming embedded in the Databricks analytics stack of institutional customers. When a quant PM uses the GRI scores as a feature in their proprietary model, switching vendors means rewriting the model. This is the Delta Sharing thesis: the distribution channel and the switching cost are the same thing.

**Investor framework:** When evaluating early-stage data/research businesses, ask:
1. What percentage of revenue is inbound vs. outbound? (Inbound commands higher multiples)
2. Is the product embedded in the buyer's workflow, or consumed episodically? (Embedded commands higher multiples)
3. What is the sales velocity? (Time from first contact to signed contract — shorter signals better product-market fit)

A company with 60%+ inbound revenue, workflow-embedded data delivery, and a 45-day average sales cycle is worth 3–4x the multiple of a technically similar product with the inverse characteristics.

---

## Databricks Angle

**Build: `prospectra.gold.prospect_pipeline`**

Before making any outreach, create the prospect pipeline table. Without it, you are managing 10–60 active prospects in your head or in a spreadsheet — which means you will forget touchpoints, miss follow-ups, and lose track of who converted from which source.

```sql
CREATE TABLE IF NOT EXISTS prospectra.gold.prospect_pipeline (
  prospect_id STRING,
  full_name STRING,
  title STRING,
  firm_name STRING,
  email STRING,
  linkedin_url STRING,
  aum_tier STRING,           -- 'sub_100m' | '100m_1b' | '1b_5b' | '5b_plus'
  mandate_type STRING,       -- 'systematic_macro' | 'em_equity' | 'commodity' | 'quant_multi' | 'other'
  geography_focus STRING,    -- Primary geographic focus
  qualification_score INT,   -- 0-15 per the 5-dimension framework
  source STRING,             -- 'inbound' | 'warm_intro' | 'cold'
  introducer STRING,         -- If warm intro, who introduced
  first_touch_date DATE,
  last_touch_date DATE,
  touchpoint_count INT,
  stage STRING,              -- 'identified' | 'outreach_sent' | 'conversation' | 'trial' | 'converted' | 'closed_lost'
  outreach_response STRING,  -- 'no_reply' | 'interested' | 'declined' | 'later'
  trial_id STRING,           -- Foreign key to trial_cohorts if in trial
  notes STRING,
  budget_cycle_q4 BOOLEAN    -- True if their budget year closes Dec 31
)
USING DELTA
COMMENT 'Prospectra sales prospect pipeline — tracks all institutional outreach from identification to conversion';
```

**The pipeline dashboard query:**

```sql
-- Pipeline health by stage
SELECT
  stage,
  COUNT(*) AS prospect_count,
  AVG(qualification_score) AS avg_qual_score,
  AVG(touchpoint_count) AS avg_touches,
  COUNT(CASE WHEN source = 'inbound' THEN 1 END) AS inbound_count,
  COUNT(CASE WHEN source = 'warm_intro' THEN 1 END) AS warm_intro_count,
  COUNT(CASE WHEN source = 'cold' THEN 1 END) AS cold_count
FROM prospectra.gold.prospect_pipeline
GROUP BY stage
ORDER BY 
  CASE stage
    WHEN 'converted' THEN 1
    WHEN 'trial' THEN 2
    WHEN 'conversation' THEN 3
    WHEN 'outreach_sent' THEN 4
    WHEN 'identified' THEN 5
    WHEN 'closed_lost' THEN 6
  END;
```

**Connecting prospect pipeline to trial cohorts:**

When a prospect in `stage = 'conversation'` agrees to a trial, insert a record in `trial_cohorts` and link the `trial_id` back to `prospect_pipeline`. This gives you the full funnel: from first outreach to conversion, with every touchpoint logged. This is the data that tells you which source, which qualification score, and which mandate type converts fastest — information that compounds in value as the pipeline grows.

**Dataset needed:** `prospectra.gold.gri_weekly` — for generating the personalized outreach attachment (a 3-month GRI trend for the prospect's coverage geography, rendered as a 1-page PDF from a parameterized notebook).

---

## Key Concepts Covered

1. **The four institutional buyer characteristics** — unreachable through standard channels, PM-as-decision-maker, budget cycle dependency, and zero patience for hype
2. **The three prospect sources** — inbound from signal, warm introductions, targeted cold outreach — with conversion rates and timeline expectations
3. **The Databricks SA network leverage** — Francisco's Cluster A (Databricks customers) and Cluster B (LATAM finance) as the highest-quality warm intro sources
4. **The 5-dimension qualification framework** — mandate, AUM tier, seniority, data sophistication, geopolitical exposure — scored 0–15
5. **The cold outreach architecture** — research-first, signal-first, 150 words max, two-touch cadence
6. **The pipeline mathematics** — 18 conversations → 9 trials → 3–4 customers → $36–54K ARR per cycle
7. **Distribution strategy as a valuation input** — inbound vs. outbound mix, workflow embedding, sales velocity as multiple drivers

---

## Reflection Questions

1. **The network honesty test:** Write the 10-name list described in Section VI. Now separate it into two columns: (A) people you are genuinely comfortable reaching out to, and (B) people who are the most qualified prospects but whom you are less comfortable approaching. How large is the gap? What is the structural reason for the gap — is it the nature of the relationship, the perceived status difference, or something else? What is the cost, in ARR, of only working column A?

2. **The budget cycle calculation:** You plan to start outreach in the week of September 8. A prospect with a December 31 fiscal year who agrees to a trial in mid-October will complete the trial in mid-November. If the Day 14 call goes well and they want to move forward, they have approximately 6 weeks before their budget closes. What is the decision the prospect faces? What is the commercial argument for moving fast? And what happens if they say "I love this but budget is committed for the year — let's reconnect in January"? Write the response email.

3. **The inbound quality question:** Lesson 307 noted that you should not pitch before 4 weeks of published signal. But someone who reads week 1 and immediately messages "this is interesting — can we talk?" is arguably more qualified than someone who reads 10 weeks and eventually messages the same thing. The early responder had higher prior conviction. Does the 4-week rule hold for inbound? Should you treat a week-1 inbound differently from a week-8 inbound in terms of how quickly you move toward a trial offer?

---

## Questions for Next Session (Spaced Repetition Hook)

- Complete the 10-name list. Have all 10 names with qualification scores, source categories, and outreach angles. Bring it to the next session.
- Have you created `prospectra.gold.prospect_pipeline` with the schema above? If not, what is the blocker?
- Of the three prospect sources (inbound, warm intro, cold), which one do you expect to be largest for the first 10 trials? Does that match where you're spending your time today?

---

## Databricks Relevance Note

**Immediate pipeline tasks (this week):**
1. Create `prospectra.gold.prospect_pipeline` with the schema above — required before first outreach
2. Build the personalized GRI export notebook: parameterized by `(country_list, date_range)`, outputs a formatted PDF-ready CSV. This is the attachment in every outreach email.
3. Join `prospect_pipeline` to `trial_cohorts` using `trial_id` — this creates the full funnel view from first contact to revenue.

**The highest-value analytical task this week:** Run a query to identify which countries in `prospectra.gold.gri_weekly` have had the largest GRI score movements in the past 30 days. These are the countries you lead with in outreach — not because the signal is necessarily most important there, but because recency and magnitude are the two most powerful attention-grabbing attributes in an outreach email.

```sql
-- Top GRI movers last 30 days (use as outreach signal)
SELECT
  country_iso3,
  country_name,
  MIN(gri_score) AS score_30d_ago,
  MAX(gri_score) AS score_current,
  MAX(gri_score) - MIN(gri_score) AS score_change_30d,
  LAST_VALUE(gri_score) OVER (PARTITION BY country_iso3 ORDER BY score_date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS latest_score
FROM prospectra.gold.gri_weekly
WHERE score_date >= DATEADD(DAY, -30, CURRENT_DATE())
GROUP BY country_iso3, country_name
ORDER BY ABS(MAX(gri_score) - MIN(gri_score)) DESC
LIMIT 10;
```

The top 3 results from this query are your outreach hooks for the next two weeks.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 310 | September 8, 2026 | Year 2 Launch Module*
