# Lesson 305 — The Geopolitical Intelligence Market: Who Buys Signal and What They Pay For It

**Date:** 2026-09-06
**Session Type:** Daily Lesson
**Lesson Number:** 305 / ongoing
**Topic:** Market Landscape — The Geopolitical Risk Intelligence Industry
**Curriculum Arc:** Year 2 Launch Module — Lesson 1 (From Builder to Market)

---

## Opening Question

*Lesson 304 ended with a hard question: is what you built worth something to someone other than you?*

*Before you can answer that, you need to know who is already selling geopolitical intelligence, what they charge, what their customers actually pay for, and where the gaps are.*

**"You cannot find your market position without first understanding who owns the market. The geopolitical intelligence industry is $4–6 billion annually — and almost none of it looks like what you built. That is either a problem or an opportunity. Today you learn to tell the difference."**

---

## I. The Industry Structure: Four Layers

The geopolitical risk intelligence market has four distinct layers, each with different buyers, pricing, and product form factors.

### Layer 1 — Consulting & Narrative Intelligence
**Players:** Eurasia Group, Control Risks, Oxford Analytica, Verisk Maplecroft, S&P Global MI Political Risk, BMI (Fitch Group)

**What they sell:** Analyst-written country risk reports, event alerts, scenario planning, bespoke consulting retainers. Human-authored narrative at the center.

**Who buys:** Corporate treasury, supply chain teams at multinationals, legal & compliance, M&A due diligence. Some sovereign wealth funds and government agencies.

**Pricing:** $50K–$500K+ annual retainer for full-service access. Bespoke consulting: $10K–$50K per project. Individual country risk reports: $1K–$5K.

**Product form:** Reports (PDF), email alerts, analyst calls, proprietary portals. Not structured data. Not machine-readable. Not real-time.

**Their edge:** Deep analyst expertise, trusted brand, relationships, language coverage. Not quantitative.

**Their weakness:** High cost-per-insight, slow cycle time (weekly/monthly), not easily integrated into quant workflows.

---

### Layer 2 — Quant Risk Data Providers
**Players:** MSCI (Political Risk Indexes, ESG Controversy), Verisk (Global Terrorism Index), PRS Group (International Country Risk Guide — ICRG), Credendo, Coface.

**What they sell:** Structured country-level risk scores, updated monthly or quarterly. Machine-readable data feeds, API access. Designed for portfolio risk management, not alpha generation.

**Who buys:** Institutional asset managers (sovereign bond mandates, EM equity), banks (credit risk), insurers (political risk insurance underwriting), regulators (stress testing).

**Pricing:** ICRG starts ~$10K/year for academic; $50K–$200K institutional. MSCI Political Risk embedded in broader ESG/risk data licenses ($100K–$1M+).

**Product form:** Monthly score updates, spreadsheet/API delivery. Not event-driven. Not real-time. Not forward-looking signals.

**Their edge:** Deep historical archives, trusted methodology, regulatory acceptance.

**Their weakness:** Backward-looking (score reflects past stability, not emerging risk), low update frequency, not designed for trading or active positioning.

---

### Layer 3 — Financial Market Risk Overlays
**Players:** BlackRock Investment Institute (Geopolitical Risk Dashboard — GRD), JPMorgan (Geopolitical Compass), Bridgewater (proprietary internal), Two Sigma (proprietary), Acadian Asset Management.

**What they sell:** Mostly internal. BlackRock's GRD is published as free thought leadership — it is not a product, it is marketing and client retention. JPMorgan's Geopolitical Compass is sold to institutional clients as part of broader research packages.

**Who buys:** Institutional investors, family offices, internal portfolio managers.

**Pricing:** Embedded in research relationships (no standalone pricing for most). BlackRock GRD is free because its purpose is client retention, not revenue.

**Product form:** Periodic dashboards, thematic memos, internal model outputs. Not real-time data products.

**Their edge:** Integration with market views and portfolio flows, massive AUM-backed credibility.

**Their weakness:** Not independent (conflicted — they manage money with this intelligence). Not transparent methodology. Unavailable to smaller institutions.

---

### Layer 4 — Alternative Data & Event Signal Providers
**Players:** Recorded Future (now Mastercard), Sayari Analytics, Tortoise Intelligence, Predata (now Thomson Reuters), GDELT Project (free/academic), Refinitiv (LSEG) News Analytics, RavenPack.

**What they sell:** Real-time event feeds, structured NLP signals from news and social media, entity-linked risk scores, sanctions/entity graph data. Machine-readable, API-first, designed for quant integration.

**Who buys:** Quant hedge funds, systematic macro traders, credit desks, compliance/sanctions screening.

**Pricing:** RavenPack: $50K–$500K/year depending on data depth. Recorded Future: $50K–$250K+. Refinitiv News Analytics: bundled into broader LSEG packages.

**Product form:** Real-time structured data feeds, API, Databricks/Snowflake native integrations in some cases.

**Their edge:** Machine-readable, real-time, high-signal density, built for systematic use.

**Their weakness:** Event signal without geopolitical context — they tell you *what* happened, not *why it matters* or *what it means for portfolio positioning*. Expensive. No investment recommendation layer.

---

## II. Where the Market Is Failing

After mapping four layers, three structural gaps emerge:

**Gap 1: The Missing Middle**
The market has two extremes: (1) expensive human narrative (Eurasia Group, $200K+), and (2) raw structured event data (RavenPack, $200K+). What does not exist at scale: a systematic, human-readable framework that bridges geopolitical signal to investment positioning at a price accessible to smaller allocators ($10K–$50K range).

**Gap 2: No "Why It Matters for Portfolios" Layer**
RavenPack tells you Iran attacked a tanker. It does not tell you what to do with Brent crude, EM tanker stocks, and USD/IRR. The investment implication layer is missing from all structured data providers. The narrative providers have it but it is slow and expensive. A product that systematically converts structured event signals into investment implications is genuinely underserved.

**Gap 3: Databricks-Native Delivery**
Zero major geopolitical intelligence vendors have a Databricks-native product. Institutional investors are increasingly running their data infrastructure on Databricks (or Snowflake). A geopolitical risk data product delivered as a Delta Lake table, a Databricks Marketplace listing, or a Databricks Asset Bundle (DAB) would be the *only* product of its kind. That is a distribution advantage, not just a technical one.

---

## III. The Prospectra Positioning Hypothesis

Based on this landscape, the most defensible and underserved position is:

**"The only systematic geopolitical investment signal platform built natively for data-driven allocators."**

Not trying to compete with Eurasia Group on analyst depth. Not trying to out-data RavenPack on event coverage. The unique position:
- Geopolitical signal → Investment implication, not just risk score
- Systematic and transparent methodology (auditable, unlike Bridgewater)
- Databricks-native delivery (no competitor has this)
- Forward-looking regime detection (GRI + Regime Change Detector), not backward-looking scores
- Price tier accessible to allocators who can't afford Bloomberg + Eurasia Group

The buyer: a $500M–$5B AUM systematic or macro-oriented fund with a Databricks or Snowflake data stack, currently spending $50K–$200K on data infrastructure, that has no structured geopolitical signal in their pipeline.

---

## IV. The Commercial Viability Decision Framework

Before deciding whether to build toward a product, apply three filters:

**Filter 1 — Will they pay?**
The market clearly pays. The question is whether the price point you can defensibly charge covers the cost of building and maintaining the product. At $25K–$75K ARR per customer, and assuming 10 early customers, that is $250K–$750K ARR. Achievable at Year 2 if pipeline quality holds.

**Filter 2 — Can you reach them?**
The buyer is a quant PM, head of research, or CTO at a systematic fund. This is a hard-to-reach, high-trust-required audience. Cold outreach converts poorly. The channel is: (1) publishing GRI as a public signal (credibility), (2) speaking at data-in-finance conferences, (3) direct relationships from Francisco's network as a Databricks SA (this is genuinely valuable — he has direct access to the exact buyer profile).

**Filter 3 — Can you defend it?**
What stops a RavenPack or Refinitiv from copying you? Short answer: not your technology (easily replicated with resources). Long answer: (1) the methodology and backtested track record (you are building this now), (2) the Databricks relationship moat if you can get marketplace listing, (3) the brand and trust of being early and publishing openly. Track records compound. Start now.

---

## V. Concrete Next Steps (Year 2 Priorities)

| Priority | Action | Timeline |
|---|---|---|
| 1 | Publish GRI weekly note publicly (Substack or similar) | Week 1 |
| 2 | Apply to Databricks Marketplace Partner Program | Week 2 |
| 3 | Identify 5 target funds from Francisco's network | Week 2 |
| 4 | Build one-page product brief + methodology note | Week 3 |
| 5 | Offer 90-day free trial to 2 target funds | Month 2 |
| 6 | First paid customer or explicit no-go decision | Month 4 |

---

## Investment Implications

The geopolitical intelligence industry structure itself has investment implications:

**Verisk (VRSK):** Owns Verisk Maplecroft, Xactware, Wood Mackenzie. Pure-play data infrastructure with geopolitical risk as a growing segment. Long-horizon hold if data platform multiples continue compressing to reasonable levels.

**MSCI (MSCI):** ESG and political risk data licensing. Regulatory tailwinds (SFDR, CSRD) driving mandatory risk disclosure. Pricing power embedded in index licensing contracts.

**Mastercard (MA):** Acquired Recorded Future in 2024. Strategic: alternative data capabilities inside a payments network creates cross-sell into financial crime, supply chain risk, sovereign risk. Long-term optionality, not a near-term catalyst.

**Implication for Prospectra:** If the commercial product thesis holds, the exit path is acquisition by one of the major data providers (MSCI, Verisk, LSEG) or a quant fund looking to internalize the capability. Not a near-term driver — a 5-year option that requires the track record to be real.

---

## Databricks Angle

**Databricks Marketplace** is the most underutilized commercial channel in alternative data. The marketplace currently lists ~200 data products. Zero are geopolitical investment signal products. The technical requirement: package GRI outputs as a Delta Sharing dataset or a Databricks Asset Bundle (DAB) that a customer can install into their own workspace in under 10 minutes.

**Specific pipeline to build:**
- `geopolitics.gold.gri_weekly` → Delta Sharing endpoint
- `geopolitics.gold.regime_signals` → curated signal table with investment implications
- Delivery: Databricks Marketplace listing + optional API via Databricks Model Serving

**Target customer entry point:** A fund's data engineer installs the DAB, runs a sample notebook, sees the GRI scores and regime signals, and evaluates over 90 days. This removes the sales cycle friction entirely.

---

## Reflection Questions

1. **The competitive positioning:** Lesson 304 asked whether what you built is worth something to someone else. Having mapped the four layers of the market — where does Prospectra most naturally fit? And what is the one thing you could do in the next 30 days that would generate the most useful signal about whether your hypothesis is right?

2. **The distribution question:** Francisco has direct access to Databricks customers as a Solutions Architect. How do you navigate the professional and ethical dimensions of using that network for a commercial venture — and how do you frame Prospectra in those conversations without compromising your day job?

3. **The build vs. buy decision (from the buyer's perspective):** A $1B AUM systematic fund has a Databricks data engineer. Why wouldn't they just build what Prospectra built themselves using GDELT + FRED + a few notebooks? What would make them prefer to buy yours? How do you stress-test your answer?

---

## Questions for Next Session

- What is your honest assessment of the three filters (will they pay / can you reach them / can you defend it)?
- Have you identified one person in your network who fits the target buyer profile? If yes, what is stopping you from sending them the GRI for free for 90 days?
- What would you need to see in the backtested track record to feel confident presenting it to an outside party?

---

## Databricks Relevance Note

**Datasets:**
- Databricks Marketplace partner catalog (review existing data products to understand pricing and positioning)
- GDELT Project → public, free, already in your pipeline
- SEC EDGAR filings for competitor companies (VRSK, MSCI 10-K: how they describe their geopolitical data segments)

**Pipeline Idea:**
- Delta Sharing endpoint for GRI output — technical requirement for marketplace listing
- Customer onboarding DAB: a Databricks Asset Bundle that installs GRI tables + sample signal notebook into a customer workspace in one command

**Feature to engineer:**
- "Signal card" generator: for each regime signal, auto-generate a structured JSON object {signal_date, asset_class, direction, thesis, invalidation_condition, horizon_days} — this is the minimum viable data product a customer would evaluate

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 305 | September 6, 2026 | Year 2 Launch Module*
