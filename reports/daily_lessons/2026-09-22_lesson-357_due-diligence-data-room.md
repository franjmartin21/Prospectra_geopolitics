# Lesson 357 — The Due Diligence Process: Surviving the Hard Questions After the Seed Pitch

**Date:** 2026-09-22
**Session Type:** Daily Lesson
**Lesson Number:** 357 / ongoing
**Topic:** Investor Due Diligence — The Data Room, the Hard Questions, and How a Research Business Gets Underwritten
**Curriculum Arc:** Live Operations Module — Lesson 42: Capital Raising Mechanics

---

## Opening Question

*Yesterday you built the pitch. You know the core claim, the narrative arc, the 12-slide structure, and how to handle the hardest objections. You walk into the meeting, deliver it cleanly, and the investor says the words every founder wants to hear:*

*"This is interesting. We'd like to take a closer look."*

**What happens next? And are you ready for it?**

Most founders treat the pitch as the main event. It is not. The pitch gets you a ticket to the real evaluation — due diligence. This is where investors stop listening to your story and start verifying it. They pull the financials, stress-test the customer claims, interrogate the product, check your references, and try to find the version of reality that your pitch didn't mention.

For most consumer startups, this process takes 2–4 weeks. For a research/data business selling to institutional clients, it can take 6–10 weeks — because the buyers' own compliance and procurement processes layer on top of the investor's diligence.

**The founders who close rounds are not the ones who pitched best. They are the ones who were ready when the diligence questions came.**

---

## Part I — What Due Diligence Actually Is

Due diligence is an investor's attempt to answer three questions before wiring money:

**1. Is the traction real?**
Every claim in the pitch deck — revenue, customer count, NRR, engagement — will be verified against source documents. Contracts, invoices, bank statements, usage logs. If the pitch said "$12K MRR from 4 institutional subscribers," the diligence process will ask for signed contracts from all four and a bank statement showing the transfers.

**2. Is the team capable?**
Investors back people as much as products. They will reference-check founders, look for prior track records, and probe for the specific competency gaps that could kill the business. For a technical research product, the key question is always: *Can this team build what it says it's building, and do they understand the domain deeply enough to defend it against competitors?*

**3. Is there a real market?**
The market size claim in the pitch will be challenged. Not the TAM number — no one believes TAM slides — but the bottom-up demand evidence. How many firms actually buy geopolitical research? What do they pay? Who are the decision-makers? Has the team spoken to enough of them to have genuine conviction?

---

## Part II — The Data Room: Building It Before You Need It

A data room is a structured, secure folder (typically on DocSend or Google Drive with access controls) that gives investors the documents they need to complete diligence efficiently. **You should have a data room ready before you take the first pitch meeting.** Not because you'll share it on day one — you won't — but because building it forces you to surface problems in your own story before an investor does.

### Standard Data Room Structure for an Early-Stage Research Business

**Tier 1 — Always Shared Early**
- Pitch deck (the same version you presented)
- Executive summary (2-page narrative version of the pitch)
- Financial model (12–18 months of P&L, revenue by customer, burn rate, hiring plan)
- Cap table (current ownership, any outstanding SAFEs or convertible notes)

**Tier 2 — Shared After Initial Interest Confirmed**
- Customer contracts (signed agreements, redacted if NDA required)
- Revenue evidence (invoices or bank statements matching the MRR claim)
- Product demo or product walkthrough video
- Team bios and LinkedIn profiles
- Any IP documentation (if applicable)

**Tier 3 — Shared in Final Stages**
- Full financial history (all bank statements, tax filings if applicable)
- Customer reference contacts (investors will call them)
- Legal documents (incorporation, option grants, any litigation disclosures)
- Technical architecture documentation

### The Prospectra Data Room — What Needs to Exist

| Document | Status | Prospectra-Specific Notes |
|---|---|---|
| Pitch deck | Build when ready | Built in Lesson 356 |
| Financial model | Build now | Monthly revenue by subscriber, cost breakdown |
| Cap table | Exists (Bolo 45% / Eli 45% / 10% pool) | Confirm no outstanding instruments |
| Customer contracts | Build with each customer | Even a $3K pilot needs a signed SOW |
| Usage/engagement data | Export from Databricks | Logins, reports accessed, API calls — shows product is used, not just paid for |
| Product demo | Build as a recorded walkthrough | Dashboard + signal output + methodology explanation |
| Market sizing backup | Document the bottom-up analysis | # of hedge funds × % that buy research × average spend |
| Team references | Identify 2–3 per founder now | Should be people who've seen you work, not just friends |

---

## Part III — The Hard Questions (And the Correct Answers)

Seed investors in research businesses have been burned before. They've backed market intelligence firms that couldn't renew clients because the product was "nice to have" rather than workflow-embedded. They will probe specifically for that failure mode.

Here are the six questions that will come up in every serious diligence process — and how to answer them correctly.

---

**Q1: "What does your product replace in the customer's workflow? What did they do before?"**

This is the most important question. Investors want to know if you're displacing a budget line or creating one. Displacing is easier to monetize; creating requires more sales work and longer adoption cycles.

*Correct Prospectra answer:* "Most institutional research desks either use a generalist political risk consultancy (Eurasia Group, Oxford Analytica — $25K–$100K/year for narrative reports with no analytical backbone), or they rely on their internal macro team to do geopolitical synthesis ad hoc. We replace the first and augment the second. For the clients currently using us, we've displaced approximately $X/year in subscriptions to narrative risk reports, and we've reduced the time their internal team spends on geopolitical synthesis by an estimated Y hours/week."

The key: you must have the data to back this answer. Ask your customers directly before the diligence process begins.

---

**Q2: "What's the renewal decision look like? Who decides, and what does the evaluation criteria look like?"**

This tests whether the founder understands the institutional buying cycle. Seed investors know that B2B research products often get bought by an individual champion but die at renewal when procurement, compliance, and the broader team weigh in.

*Correct Prospectra answer:* "The renewal decision sits with [specific title — e.g., Head of Macro Research / CIO]. We've mapped the renewal process at each account: it typically involves a 60-day internal evaluation, a usage review, and occasionally a compliance sign-off on the data sourcing. We've pre-positioned for renewals by providing quarterly impact summaries to each subscriber — showing which of our signals preceded which market moves."

The key: if you can't describe the renewal process at your existing customers, you don't understand your business well enough to raise capital for it.

---

**Q3: "Your track record shows X calls over Y months. How do you know it's the model and not luck?"**

This is the most intellectually serious question and the one that differentiates Prospectra from every political risk newsletter that claims alpha.

*Correct Prospectra answer:* "We've modeled this explicitly. Our baseline is random — what returns would you get if you took a directional position on every geopolitical event regardless of signal strength? Our model outperforms that baseline by X% over the evaluation period, with the strongest signal coming from [specific regime — e.g., conflict escalation + commodity supply chains]. We've also stress-tested the framework against out-of-sample historical events: the 2022 Russia sanctions, the 2024 TSMC production halt, the 2025 Gulf crisis. The methodology holds. We can share the validation notebook."

The key: you must actually have this analysis done. Not as a slide — as a notebook that an investor's technical team can audit.

---

**Q4: "Who is your best-positioned competitor, and why haven't they built this yet?"**

This tests whether you understand the competitive landscape honestly — and whether your moat is real or aspirational.

*Correct Prospectra answer:* "The most dangerous competitor is Bloomberg's macro risk team combined with their terminal distribution. They have the data infrastructure and the customer relationships. What they don't have is the methodology — Bloomberg sells data and analytics, not an opinionated, structured framework for translating geopolitical signals into portfolio positions. Their geopolitical products are narrative, not systematic. The second risk is a hedge fund building this internally — which some do. But proprietary builds don't get shared, and the institutional market for a shared, audited track record is real. The moat we're building is the track record itself: 18 months of documented calls with outcomes. That can't be bought or copied."

---

**Q5: "What happens to the business if one of your two founders leaves?"**

Seed investors hate key-man risk. For Prospectra, the specific fear is: Bolo leaves and Eli, who is not operationally active, remains. What happens?

*Correct Prospectra answer:* "The IP is in the system — the GDELT pipelines, the signal models, the Databricks architecture — not in the founders' heads. We've documented the methodology thoroughly enough that a senior data scientist could be onboarded. The customer relationships are distributed: I own some accounts, my co-founder owns others. We've also begun formalizing Eli's role in the business [if true], so the organization is not entirely dependent on one operator."

The honest version of this answer requires: documentation to actually exist, and Eli's role to be clarified. This is a management action, not just a pitch answer.

---

**Q6: "What does the $500K [or whatever the round size] actually buy you, specifically?"**

This is the use-of-proceeds question. Investors hate vague answers ("grow the team, improve the product"). They want a 12-month operating plan tied to the capital.

*Correct Prospectra answer:* "The $500K buys us 18 months of runway at our current cost structure, with capacity for two additional hires: a research analyst who owns the geopolitical coverage and frees Bolo to focus on product and distribution, and a sales/BD role targeting family offices and asset managers. By month 18 we expect to be at $25K MRR with 8–10 subscribers, which is the threshold for Series A conversations. If we hit $150K ARR with >100% NRR and a clear enterprise upsell path, we believe we can raise a $2–3M Series A at a reasonable valuation."

The key: the plan must be specific, dated, and internally consistent with the financial model.

---

## Part IV — The Reference Call (The Part Founders Forget)

Before an investor wires money, they call your customers. This is the highest-stakes part of the diligence process and the part founders are least prepared for.

**What investors ask customer references:**
1. "What specifically do you use the product for? Walk me through a use case from last month."
2. "What would happen if you had to cancel the subscription tomorrow?"
3. "What's missing? What would make this a 10x more valuable product?"
4. "Would you increase your spend if the product continued improving?"
5. "Would you recommend this to a peer at another firm?"

**The trap:** Founders often suggest reference contacts who will give glowing endorsements — the champion who bought the product, the contact they have the best relationship with. Investors know this. The most credible reference calls are the ones where the customer gives a mixed, honest assessment: "It's valuable, but the onboarding could be better. I'd renew, but I'd want to see X feature."

**Your job before the diligence process begins:** Have a direct, honest conversation with each customer about what they'll say on a reference call. Not to coach them — to know what's coming, and to have already fixed the problems they'd raise.

---

## Part V — The Term Sheet Isn't the Close

A common founder mistake: treating receipt of a term sheet as the finish line. It is not. Term sheets are non-binding letters of intent. Diligence continues after the term sheet is signed. Investors have pulled out of signed term sheets when diligence revealed inconsistencies with the pitch — overstated revenue, a key employee who was planning to leave, a customer relationship that was more fragile than presented.

**The close happens when money is in the bank account.**

Until then:
- Don't change your pitch based on what you think an investor wants to hear
- Don't sign commitments (new hires, office leases, vendor contracts) in anticipation of a round closing
- Keep running the business — investors lose confidence when a founder goes into "fundraising mode" and the operating metrics deteriorate during the diligence period

---

## Investment Implications

The due diligence process is not just relevant to Prospectra's capital raise — it is a model for how institutional investors evaluate any research or data product they buy.

**Asset class lens:** When evaluating investment in data/research companies (a growing category — Morningstar, FactSet, MSCI all trade at premium multiples), the key due diligence factors map directly to the above:
- **Revenue quality:** % subscription vs. one-time, NRR, contract length
- **Customer concentration:** What % of revenue comes from top 3 clients?
- **Moat:** Is the product workflow-embedded (switching cost = data migration) or discretionary (switching cost = none)?
- **Management depth:** Can the business survive a founder departure?

**Portfolio implication:** Data and research businesses with >110% NRR, <30% customer concentration, and multi-year contracts deserve premium multiples. Most institutional investors systematically underweight the moat quality of research businesses because they apply consumer-app churn assumptions to B2B data contracts. This is a persistent mispricing.

---

## Databricks Angle

**Dataset:** Build a diligence-readiness dashboard in Databricks that tracks:
- MRR by customer (with contract start date and renewal date)
- Usage metrics by customer (logins, API calls, reports generated)
- Signal performance log (each call, direction, timeframe, outcome)
- Track record validation model (backtested vs. baseline, confidence intervals)

This dashboard serves double duty: it makes diligence faster when the moment comes, and it is itself evidence of analytical rigor — showing it to an investor during the pitch signals that the team runs the business with the same discipline they apply to geopolitical analysis.

**Pipeline to build:** A "business health" Delta table that auto-populates from the customer database, pulls subscription and usage data, and generates a weekly snapshot report. This is the operational twin of the geopolitical signal pipeline — the same infrastructure applied to the business itself.

---

## Key Concepts Covered

- The three questions due diligence is designed to answer
- The three-tier data room structure and what Prospectra needs to build
- The six hard diligence questions and the correct answers for each
- The reference call — what investors ask and how to prepare
- Why the term sheet is not the close
- How due diligence methodology applies to investing in research/data businesses

---

## Questions for Next Session (Spaced Repetition Hook)

1. **For your existing customers (or prospective first customers):** What would each one say on a reference call today? Where are the gaps between their stated satisfaction and what they'd say to a third party?

2. **The track record validation question is the hardest.** Do you currently have the analytical framework to prove that Prospectra's signal outperforms a random baseline? What would it take to build that validation notebook this month?

3. **Stretch question:** If you had to do a full data room review today — pull every document, fill every gap — what's the single biggest hole? What would an investor find that you haven't yet fixed? That's the next management action.

---

*CEO — Prospectra Geopolitics & Investment Project*
*2026-09-22*
