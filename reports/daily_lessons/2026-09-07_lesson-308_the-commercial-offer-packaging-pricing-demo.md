# Lesson 308 — The Commercial Offer: Packaging, Pricing, and the 30-Minute Demo

**Date:** 2026-09-07
**Session Type:** Daily Lesson
**Lesson Number:** 308 / ongoing
**Topic:** The Commercial Offer — How to Package, Price, and Pitch a Geopolitical Signal Product
**Curriculum Arc:** Year 2 Launch Module — Lesson 5 (From Publisher to Revenue)

---

## Opening Question

*Lesson 307 built the publishing architecture — weekly GRI notes, LinkedIn + Substack, a conversion funnel. It ended with the moment a subscriber sends a message: "This is interesting. Can we talk?"*

**"You've published 4 weeks of GRI Weekly Notes. A subscriber emails you: 'This is really interesting — can we get on a call?' What do you say back? And what happens in that 30-minute meeting?"**

Most people in this position wing it. They say yes, they show up, they share their screen, they talk about the GDELT pipeline, they explain the GRI formula, they run out of time, they say "I'll follow up with a deck" — and they never hear back.

The reason is not that the product is weak. The reason is that the meeting had no architecture. A 30-minute demo is not a tour. It is a structured argument that ends in a specific ask. If you do not know what the ask is before you open your laptop, you are not doing a demo — you are doing a product walkthrough for someone who will now use your methodology to brief their in-house quant team.

This lesson builds the commercial architecture: what the product actually is, how to price it, how to run the demo, and how to handle the objections that will end the conversation if you are not ready for them.

---

## I. What the Buyer Is Actually Buying

This is the most important thing to understand before the call, and most founders get it wrong.

**They are not buying a dashboard.** They are not buying a CSV. They are not buying access to GDELT. They are buying four things:

### 1. Signal Reliability — The Track Record

A systematic investor needs to know: over a defined period, using a defined methodology, how often was the directional call correct, and what was the magnitude of the alpha opportunity? This is the first question every professional buyer asks, often before the first call.

**The implication:** Your track record is not a nice-to-have. It is the literal product. If you do not have a dated, scored call history before the conversation begins, you are not selling a signal product — you are selling a pitch deck.

The good news: by Week 5 of publishing, you have five dated, public, falsifiable calls. That is more than most competitors put in writing. Bring them. Show them. Do not bury them in slide 9.

### 2. Delivery Mechanism — Data, Not Document

Professional buyers do not use PDFs as inputs to portfolio decisions. They use data. Their question, often unspoken: *Can this feed my system?*

At the minimum, this means: can they query the GRI scores directly? Can they export the signal log as a structured file? Does the data have consistent schema, documented methodology, and version control?

At the maximum — which is where the enterprise tier goes — it means a live API or direct Databricks catalog access (Delta Sharing) so their data engineers can plug the GRI directly into their own pipeline.

**The implication:** Before the first commercial call, ensure that `prospectra.gold.gri_weekly`, `prospectra.gold.investment_signals`, and `prospectra.gold.public_signal_log` can be exported as clean CSVs or accessed via Delta Sharing. If the answer is "you'd have to email us for the data," you are a newsletter, not a data product.

### 3. Analyst Access — The CEO's Interpretation

This is the moat most data vendors do not have, and it is also the thing that does not scale. Use it deliberately.

In the early commercial stage, what buyers are paying for is not just the data — it is the CEO's framing of what the data means for their portfolio this month. The monthly analyst call, the custom country brief, the 20-minute "what's happening with the Saudi-Russia dynamic and what does it mean for Brent?" conversation — this is the highest-value, least-scalable product you have. It is also the one that most convincingly separates Prospectra from a Python notebook anyone could run themselves.

**Pricing implication:** Analyst access is a pricing tier, not a feature. It belongs in the Enterprise package. Never give it away at the Professional level. The moment it becomes infinite and free, it becomes a support burden and destroys margin.

### 4. Institutional Trust — The Relationship Account

In the data vendor business, no serious buyer switches to a new data vendor after one conversation. The buying cycle is typically 3–6 months from first contact to signed contract for a systematic fund. In that window, trust is built by showing up consistently, being right when the market tests you, being honest when a call goes wrong, and never overpromising.

**The implication:** The first call is not a sales call. It is the first deposit into a relationship account. The ask at the end of the first call should be small: a trial, a second conversation, a specific question they want you to answer with the data. Not a contract.

---

## II. The Three-Tier Product Architecture

Every commercial data product needs a clear pricing ladder. The ladder serves two purposes: it anchors the buyer's expectation ("What am I choosing between?") and it allows you to upgrade rather than re-pitch as the relationship matures.

### Tier 1 — Signal Feed (Free, Public)
**What it is:** The weekly GRI note (LinkedIn + Substack). No login, no account, no commitment.
**Who it's for:** Anyone interested in geopolitical macro. Researchers, journalists, students, practitioners building trust.
**Commercial function:** Top of funnel. No revenue. Unbounded reach. Track record builder.

### Tier 2 — Professional ($500–$1,500/month)
**What it is:**
- Full GRI data table (all countries, weekly, downloadable CSV + API endpoint)
- Investment signal archive (all dated calls, current status, mark-to-market)
- Regime classification feed (weekly)
- Monthly CEO brief (written, ~800 words, specific to their asset class focus)
**Who it's for:** Individual portfolio managers, family offices, boutique systematic funds, macro research teams
**Commercial function:** The entry point for people who read the weekly note and want the data layer underneath it

### Tier 3 — Enterprise ($3,000–$8,000/month, annual contract)
**What it is:**
- Everything in Professional
- Delta Sharing access — live read access to `prospectra.gold.*` tables directly in their Databricks workspace
- Commodity Pressure Model output for custom country/commodity pairs they specify
- Monthly 60-minute analyst call (CEO + their PM team)
- Custom alert: email/Slack notification when GRI moves >10 points for their coverage universe
- Dedicated signal card: one custom investment thesis per month, built specifically for their portfolio mandate
**Who it's for:** Systematic funds $100M+ AUM, EM specialist equity/FX funds, commodity trading firms
**Commercial function:** High-value anchor customer. One enterprise client = $36K–$96K ARR. Three clients = initial commercial viability.

### Pricing Rationale

Data product pricing is not cost-plus. It is value-based. The question is: what is a correct directional call worth to a buyer?

A fund with $200M AUM running a 0.5% tactical overlay that the GRI signal informs:
- A correct call generating 0.7% excess return = $1.4M in alpha
- Annual signal cost should be <5% of alpha generated to pass a quant PM's ROI filter
- 5% of $1.4M = $70,000 per year as the maximum justifiable spend

**Implication:** The Professional tier at $12K/year and the Enterprise tier at $60K/year are not aggressive — they are below the theoretical ROI ceiling. The constraint is not price. It is proof that the signal generates that alpha. Which is why the track record is the product.

---

## III. The 30-Minute Demo: Exact Structure

The demo has five segments. Print this and put it on your desk before every first call.

### Minutes 0–5: The Relationship Segment
- Ask: "What is your current approach to incorporating geopolitical risk into portfolio decisions?" (Not "What do you know about us?" — make them talk about their problem first.)
- Listen for: What they don't have, what they've tried that didn't work, what asset classes they care about
- Do not pitch. Note what they say. You will use it in minutes 10–20.

### Minutes 5–15: The Data Story
Open your screen. Show these three things in order:

1. **The pipeline** (30 seconds): One slide or one image. GDELT → Bronze → Silver → Gold → Signal. "This is the infrastructure. It runs every day, unattended. Today's GRI scores were generated this morning from last night's GDELT data."

2. **The GRI score** (2 minutes): Show the live dashboard or the Databricks output. Pick the country most relevant to what they told you in minutes 0–5. Walk through what drove the score change this week. Use specific GDELT event categories, not vague descriptions.

3. **The signal card** (2 minutes): Show the most recent investment signal card. Read the thesis out loud: asset class, direction, 12-month horizon, invalidation condition. Then show the mark-to-market. "This call was issued 6 weeks ago. Here is where it stands today."

What you are demonstrating: the methodology is systematic, the output is specific, and the track record is real.

### Minutes 15–25: The Track Record
This is the most important segment. Show the `public_signal_log` — all dated calls, their status, their current mark-to-market.

Do not cherry-pick. Show everything, including calls that are underperforming or that have not resolved. Explain your monitoring approach: "When an invalidation condition is approached, we either close the call or update the thesis with explicit reasoning. We do not quietly archive bad calls."

The reason you do this: **institutional buyers have seen too many selective backtests.** A vendor who shows their losses is a vendor who can be trusted. A vendor who only shows wins is a marketing firm.

If you have 4–6 weeks of public calls, you probably have 4–6 signal entries. That is enough. Five honest calls with clear reasoning is more credible than 50 calls with no falsification criteria.

### Minutes 25–28: The Offer
Based on what they said in minutes 0–5, make a specific offer — not a general pitch:

*"Based on what you described — you're running a commodities overlay and you're primarily focused on [Middle East / EM Asia / Latin America] — I'd suggest starting with a 30-day trial of the Professional tier. You'd get the full GRI data table and the signal archive. I'll send you a CSV of the last 3 months of GRI scores for your coverage universe tonight so you can run your own correlation analysis before we talk again. If after 30 days you think the signal adds something your process doesn't have, we can talk about the data layer integration."*

**This offer is low-commitment, data-first, and respects that they need to validate the signal themselves.** A buyer who says no to this is not a buyer yet — and that is fine.

### Minutes 28–30: The One Ask
End with one specific next action, not "I'll follow up with a deck":
- "I'll send you the CSV tonight. Can we schedule 20 minutes in 2 weeks to go through what you find?"

One action. One follow-up meeting scheduled. Nothing else.

---

## IV. Handling the Four Killer Objections

Every first commercial conversation will surface one or more of these. You need a prepared response for each.

### Objection 1: "Your dataset is too small / track record is too short."
**Response:** "You're right that 6 weeks of live calls is early. Here's what I'd ask: look at the specific falsification criteria on each call. Most vendors with 5 years of track record have calls so vague that they can't be wrong. We have 6 weeks of calls that can be checked daily. The question isn't whether 6 weeks is enough — it's whether the methodology is sound enough to scale into a longer track record. The trial answers that question."

**The underlying point:** Falsifiability at 6 weeks is more epistemically honest than unfalsifiability at 5 years.

### Objection 2: "We already have Bloomberg/Refinitiv for geopolitical risk."
**Response:** "Bloomberg's GPR index measures media attention, not diplomatic event structure. It does not produce directional investment calls — it produces an anxiety index. What we produce is a scored signal with a specific falsifiable thesis. If you're using Bloomberg GPR as a signal input today, I'd be curious what correlation you're seeing between GPR spikes and your actual asset class outcomes. My guess is it's noisier than you'd like."

**The underlying point:** You are not competing with Bloomberg. You are filling a gap Bloomberg explicitly does not fill.

### Objection 3: "Our quants could build this themselves."
**Response:** "Probably, yes. GDELT is public. Databricks is what you use. The question is: would they? Building this took 4 months of weekend and evening time from someone who already knew both Databricks and geopolitical analysis deeply. What is that 4 months worth to your quant team, and what would they not build in that same time? We're selling the built version, not the blueprint."

**The underlying point:** Make-vs-buy is a real question. Your answer is the opportunity cost of the quant team's time plus the 4-month head start on the track record.

### Objection 4: "What's the Sharpe?"
**Response:** "We don't have enough live history for a meaningful Sharpe. What we do have is the falsification rate — the percentage of our directional calls that resolved correctly within the stated time horizon — and the mark-to-market on active calls. I'd rather give you 6 real data points than a backtest Sharpe optimized to look attractive. The trial gives you 30 days to run your own attribution analysis."

**The underlying point:** An honest answer here is more credible than a manufactured Sharpe. Use it.

---

## Investment Implications

### The Data Product Pricing Premium

Understanding how data businesses price has direct investment implications in the technology and financial data sector.

**The pricing power thesis:** Data businesses that own proprietary, non-replicable datasets trade at 8–15x revenue multiples vs. 3–5x for SaaS businesses. The difference is switching cost. A customer who builds their workflow around a proprietary dataset (Bloomberg terminal users, MSCI index users, FactSet subscribers) faces prohibitive switching costs — their entire data infrastructure would need to be rebuilt. This is why Bloomberg can charge $24,000/year per terminal and retain customers for decades.

**The implication for Prospectra:** The moat is not the GDELT access (public) or the Databricks pipeline (replicable). The moat is the **public_signal_log** — a dated, auditable, live call history that cannot be recreated retroactively. This is the proprietary dataset. Every week it grows, the switching cost for a customer who has integrated it into their process grows with it.

**The investor framework:** When evaluating data businesses (MSCI, FactSet, Verisk, Morningstar), look for:
1. Is the core dataset proprietary or replicable?
2. Does the customer integrate the data into their own workflow (high switching cost) or consume it episodically (low switching cost)?
3. Is there a compounding track record element (the dataset improves as it ages, like a credit bureau or a systematic signal log)?

Businesses with all three characteristics support 12–20x revenue multiples. Businesses with only #1 are at risk of commodity competition. Businesses with #1 + #2 + #3 are structurally defensible — which is exactly what Prospectra is building.

---

## Databricks Angle

**Immediate build: Delta Sharing setup**
Before the first enterprise demo, configure Delta Sharing on `prospectra.gold.*` tables. This takes 2–3 hours but transforms your enterprise pitch: instead of "we can give you a CSV," you say "we can give you live, query-ready access directly in your Databricks workspace." This is the technical detail that closes enterprise deals.

```sql
-- Enable Delta Sharing on GRI tables (run in Databricks Unity Catalog)
CREATE SHARE prospectra_enterprise_share;

ALTER SHARE prospectra_enterprise_share
ADD TABLE prospectra.gold.gri_weekly;

ALTER SHARE prospectra_enterprise_share
ADD TABLE prospectra.gold.investment_signals;

ALTER SHARE prospectra_enterprise_share
ADD TABLE prospectra.gold.public_signal_log;

-- Create recipient (one per customer)
CREATE RECIPIENT enterprise_customer_1;

-- Grant share to recipient
GRANT SELECT ON SHARE prospectra_enterprise_share TO RECIPIENT enterprise_customer_1;
```

**New table: `prospectra.gold.trial_cohorts`**
Track trial customers — start date, tier, coverage universe, engagement metrics (how many queries they ran, which tables they accessed). This table tells you which trials convert and why, which is the most important commercial learning in Year 2.

| Column | Description |
|---|---|
| `trial_id` | Unique trial identifier |
| `start_date` | Trial start |
| `end_date` | Trial end (30 days default) |
| `tier_offered` | Professional / Enterprise |
| `coverage_focus` | Country/region their portfolio focuses on |
| `queries_run` | Total queries against shared tables |
| `converted` | Boolean — did they become a paid customer? |
| `conversion_date` | If converted, when |
| `non_conversion_reason` | Structured field: Price / Track Record / Internal Build / No Fit / Other |

**Dataset:**
- `prospectra.gold.gri_weekly` — primary demo data source
- `prospectra.gold.investment_signals` — track record to show during the demo
- `prospectra.gold.public_signal_log` — the commercial moat table, shown in minutes 15–25

---

## Key Concepts Covered

1. **The four things a buyer is purchasing** — reliability (track record), delivery mechanism (data not document), analyst access, and institutional trust
2. **The three-tier product architecture** — Free (signal feed) / Professional ($500–1,500/mo) / Enterprise ($3,000–8,000/mo)
3. **Value-based pricing logic** — signal cost should be <5% of alpha generated; the track record is the proof, not the marketing
4. **The 30-minute demo structure** — five segments with exact time allocations and a single ask at the end
5. **The four killer objections** — track record length, Bloomberg competition, internal build, Sharpe — with specific responses
6. **Data product pricing premium** — why dated, auditable signal logs create structural pricing moats (the Bloomberg/MSCI lesson)

---

## Reflection Questions

1. **The trial offer:** Lesson 307 said "never pitch before the reader has seen the signal for 4 weeks." But objection #1 is that 6 weeks isn't enough track record. These two timelines are in tension — the earlier you have the demo conversation, the less track record you have; the longer you wait, the more credibility you have but the colder the relationship gets. How do you manage this tension in practice? What is the minimum viable track record for a first enterprise conversation?

2. **The professional identity question:** You are a Databricks Solutions Architect whose professional identity is deeply tied to Databricks. Your Enterprise tier now includes Delta Sharing — a Databricks feature. You are effectively using a Databricks capability as a competitive differentiator in a commercial pitch. Is this a conflict of interest, a synergy, or something in between? How do you describe Prospectra to a colleague who knows you professionally?

3. **The objection you haven't heard yet:** The four objections above are the ones you can predict. But every real sales process surfaces a fifth objection that is specific to that buyer's situation — their compliance requirements, their existing vendor relationships, their internal politics. What is the objection you would find most difficult to answer honestly? What would you say?

---

## Questions for Next Session (Spaced Repetition Hook)

- Have you configured Delta Sharing on the `prospectra.gold` catalog? If not, what is blocking it?
- Draft the exact email you would send to a subscriber who says "Can we talk?" — subject line, 3 sentences, and a proposed meeting time.
- Of the four killer objections, which one do you think is most likely to end a conversation with a systematic macro fund? Which is most likely to end one with a commodity trading firm?

---

## Databricks Relevance Note

**Immediate pipeline tasks:**
1. Configure Delta Sharing on `prospectra.gold.*` tables — required before any enterprise demo
2. Create `prospectra.gold.trial_cohorts` table with schema above
3. Test the Delta Sharing connection from a second Databricks workspace (use a personal/trial workspace as the "customer" workspace to simulate the demo experience)
4. Verify `prospectra.gold.public_signal_log` has all prior calls loaded with correct schema before the first demo

**The most important Databricks task this week:** Run the demo yourself. Open a fresh notebook in your Databricks workspace, connect to the shared tables as if you were a customer, query the GRI scores, pull the signal log, and time it. If it takes more than 3 minutes to get from "connected to workspace" to "I have a chart of GRI scores in front of me," the demo will fail. The bar for enterprise data integration is high.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 308 | September 7, 2026 | Year 2 Launch Module*
