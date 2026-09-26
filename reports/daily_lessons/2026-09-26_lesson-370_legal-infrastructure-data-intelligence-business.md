# Lesson 370 — Legal Infrastructure for a Data Intelligence Business
**Date:** 2026-09-26  
**Session Type:** Daily Lesson  
**Topic:** Legal Infrastructure for a Data Intelligence Business  
**Sequence:** Lesson 370 of ongoing curriculum  
**Arc:** Company Building → Operational Excellence

---

## Opening Question

You've built the product. You've signed your first client. You have a proprietary methodology, a live GRI model, and a growing dataset.

**Here is the question that determines whether any of it is defensible:**

*Who owns what — and can you prove it?*

Most early-stage companies treat legal infrastructure as a compliance checkbox. A data intelligence business like Prospectra cannot afford that mistake. Your assets — the GRI methodology, the signal architecture, the analytical frameworks — are your entire business. If you don't protect them correctly from day one, a client can reverse-engineer your model, a departing employee can take it, or a competitor can copy it without recourse. Legal infrastructure is not overhead. It is the lock on the vault.

---

## Part I — The Four Legal Pillars for a Data Intelligence Company

Every data intelligence business needs four interlocking legal systems. Most early-stage founders build one or two and leave the rest to chance.

### 1. Intellectual Property Protection

**What you're protecting:** The GRI methodology, signal architecture, analytical frameworks, weighting models, and any proprietary indices.

**How you protect it:**

**Trade Secrets — your primary tool.** Trade secret law protects any confidential business information that provides a competitive advantage. Unlike patents, there's no registration, no expiration, and no public disclosure. The requirement is that you take *reasonable measures* to maintain secrecy.

For Prospectra this means:
- Every document describing the GRI methodology is marked **CONFIDENTIAL — TRADE SECRET**
- Access to the full methodology is restricted to the minimum necessary people
- All employees and contractors sign NDAs *before* getting access
- You maintain an internal document (a "trade secret register") identifying your key IP assets

**Copyright — automatic but weak.** The code, written reports, and dashboard designs are automatically copyright-protected from creation. This matters, but it doesn't stop someone from independently developing a similar methodology. Don't rely on it as your primary protection.

**Patents — probably wrong for you, at least now.** Patent protection for data models and analytical methods is difficult, expensive ($30K–$80K+), and takes 2–4 years. The disclosure requirement (you must publish the method to get the patent) can destroy trade secret protection. For Prospectra's current stage, patent protection is not the priority.

**Trademarks — protect the brand.** "Prospectra," "GRI" (as your index brand), and any other product names should be registered with the USPTO. Filing cost is ~$350 per class. Do this when you have revenue. It prevents a competitor from appropriating your brand equity.

### 2. Client Agreements

**The two agreements that govern every client relationship:**

**Master Services Agreement (MSA):** The overarching contract governing the business relationship. It covers:
- Scope of services
- Payment terms and late fees
- Confidentiality obligations (both ways — you protect their data, they don't disclose your methodology)
- IP ownership (see below)
- Limitation of liability (critical — see below)
- Indemnification
- Dispute resolution
- Termination rights

**Order Form / Statement of Work (SOW):** Attached to the MSA. Specifies what the client is actually getting: which signals, which reports, how often, at what price, for how long.

**The three clauses that most founders under-negotiate:**

**Limitation of Liability.** This clause caps your financial exposure if something goes wrong. Without it, if a client trades on your GRI signal and loses money, they could theoretically sue you for the full trading loss. A standard LOL clause limits your liability to the fees paid in the prior 12 months. Non-negotiable for a signal business.

**Data License vs. Service Agreement.** Are you licensing data to the client (they own a copy) or providing a service (access terminates with the contract)? This is a fundamental business model question with major legal implications. Prospectra should be providing a *service* (access to the platform and signals), not licensing raw data. When the client cancels, they no longer have access. If you accidentally write an agreement that transfers data ownership to the client, you've permanently licensed your signals.

**IP Ownership Clause.** Any custom work you do for a client — custom reports, bespoke signal construction — must clearly state that Prospectra retains ownership of the underlying methodology, even if the output belongs to the client. Many clients will try to claim that custom work is "work for hire" and therefore their property. Reject this clause every time.

### 3. Employment and Contractor Agreements

**This is where early-stage companies make catastrophic mistakes.**

Every person who touches your IP — employees, contractors, advisors — needs a signed agreement *before* they start work that covers:

**Invention Assignment:** Any IP created by the person in the course of working for Prospectra belongs to Prospectra. This is non-negotiable. Without it, a contractor could argue they own the code they wrote for you.

**Non-Disclosure Agreement:** They cannot disclose your methodology, client relationships, or internal data to anyone outside the company.

**Non-Solicitation:** After leaving, they cannot recruit your employees or clients for 12–24 months. Note: Non-compete clauses (preventing someone from working for a competitor) are largely unenforceable in California and increasingly restricted elsewhere. Don't rely on them.

**The "moonlighting" trap.** If a contractor is simultaneously working for a competitor while building your GRI model, you have a serious problem. Your contractor agreement should require disclosure of any conflicting engagements.

### 4. Data Governance and Regulatory Compliance

As a data business, you have obligations related to the data you collect, process, and distribute.

**GDPR (if you have EU clients or process EU personal data).** The General Data Protection Regulation applies to any business handling EU residents' data, regardless of where the business is incorporated. For Prospectra, if you have EU institutional clients or process any personal data (even analyst emails), GDPR applies. Key requirements:
- Privacy policy
- Data processing agreements with clients
- Data subject rights procedures (access, erasure)
- Potentially a Data Protection Officer if processing at scale

**CCPA (California).** Similar to GDPR for California residents. Less stringent than GDPR but still requires a privacy policy and data subject rights procedures.

**Financial Data Regulatory Exposure.** This is the risk most data intelligence companies miss. If Prospectra's signals could be construed as **investment advice** — telling clients what to buy and sell — you may be required to register as an Investment Adviser with the SEC. The distinction:
- **Research and data** (what we sell): Not regulated. A research report that says "GRI for Iran rose 15% — this is historically associated with oil price increases" is data.
- **Investment advice** (what we don't sell): Telling a client "you should buy oil futures" based on our analysis crosses into regulated territory.

Prospectra's product positioning must consistently frame the GRI and signals as **data and analysis**, not investment advice. Every report should carry a **research disclaimer** to this effect.

---

## Part II — The Legal Build Sequence for Prospectra

**Now (pre-Series A):**
1. NDA + Invention Assignment for every person who touches the product
2. Client MSA template — get a startup-specialized attorney to draft this (cost: $3K–$8K one-time; this is not something to DIY)
3. Trade secret register — internal document listing your key IP assets
4. Research disclaimer on all output
5. Privacy policy on website

**At first institutional client:**
1. Negotiate and execute the MSA carefully — the first one sets the template for all future deals
2. Ensure limitation of liability and data license language are clean

**At Series A:**
1. Formal IP audit — attorney reviews all agreements to confirm IP ownership chain is clean
2. Trademark registration for Prospectra and GRI
3. Employment agreements for any new hires

**Year 2+ (commercial scale):**
1. Evaluate SEC investment adviser registration requirement as client base grows
2. Data licensing framework if you begin distributing bulk data to third parties
3. GDPR compliance if EU client count grows

---

## Part III — The Founder's Most Dangerous Assumption

"We'll deal with legal when we have problems."

The reason this is wrong for Prospectra specifically: **your IP is your only moat.**

A competitor can build a similar analytical platform. What they cannot easily replicate is:
1. Your proprietary methodology (protected by trade secrets + contracts)
2. Your track record (the auditable signal log)
3. Your client relationships (protected by non-solicitation agreements)

If you don't have the legal infrastructure protecting (1), a well-funded competitor can hire away a key person who knows your methodology, reverse-engineer your GRI model from your published signals, and enter your market with a defensible copy. This has destroyed multiple data intelligence businesses.

Legal infrastructure is insurance against the scenario where success attracts competition. Cheap insurance. A good startup attorney for one year of basic coverage costs $5K–$15K. The cost of not having it is the business.

---

## Investment Implications

**For Prospectra as an investment:**
Any sophisticated Series A investor will conduct an IP audit as part of due diligence. Clean IP ownership chain — every contractor has a signed invention assignment, all client agreements have proper data license language — is table stakes for closing a round. Missing agreements are a red flag that delays or kills deals.

**For the geopolitical intelligence industry more broadly:**
Data licensing disputes and regulatory exposure are structural risks for all independent research and intelligence firms. ACLED, GDELT, and similar open data providers face recurring questions about commercial use of their data. Bloomberg's data licensing agreements have been litigated. The valuation premium for data businesses with clean IP and proprietary (not licensed) methodologies is material.

---

## Databricks Angle

**Immediate relevance:** Your GDELT pipeline ingests public data. GDELT's terms of use permit commercial use — but any enriched, transformed, or aggregated output that you then sell (the GRI, for example) is *your* IP, not GDELT's. Document this in your trade secret register.

**Pipeline idea:** Build a data provenance layer in your Databricks bronze tier — a metadata table that records the source license, terms of use, and transformation history for every dataset that feeds into the GRI. This creates an auditable IP chain that will matter during due diligence and any future regulatory review.

---

## Reflection Questions

1. **The invention assignment question:** List every person (employee, contractor, advisor) who has touched the GRI methodology or signal architecture. Do all of them have signed invention assignment agreements with Prospectra? What's the gap?

2. **The data license vs. service question:** If a current client cancelled their subscription tomorrow, what access would they retain to historical Prospectra signals and reports? What does your current agreement say — and does it match your intent?

3. **The regulatory line question:** Read your last three signal write-ups. Do any of them contain language that could be construed as investment advice rather than data and analysis? What specific language would you change?

---

## Questions for Next Session

- How do you run a cap table audit and prepare for investor IP due diligence?
- What does a clean "IP ownership chain" look like to a Series A investor?
- How do competitor intelligence and competitive IP disputes actually play out in the data analytics industry?

---

## CEO Note

Lesson 369 covered financial controls. Today's lesson closes the operational infrastructure arc. Together, these three lessons (financial controls, legal infrastructure, and the earlier HR lessons) define the operating system of a fundable early-stage company.

The gap I'm watching: based on the curriculum to date, Prospectra has deep analytical architecture and a growing commercial engine. The weakest link is likely the legal stack — specifically whether every person who has touched the GRI has a signed invention assignment. This is the first thing an investor will check. Bolo should audit this before the next fundraising conversation.

*CEO — Prospectra Geopolitics & Investment Project*
