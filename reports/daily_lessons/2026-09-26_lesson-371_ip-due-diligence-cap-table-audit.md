# Lesson 371 — IP Due Diligence & Cap Table Audit: Investor Readiness
**Date:** 2026-09-26  
**Session Type:** Daily Lesson  
**Topic:** IP Due Diligence & Cap Table Audit — Preparing for Series A  
**Sequence:** Lesson 371 of ongoing curriculum  
**Arc:** Company Building → Investor Readiness

---

## Opening Question

You've built a methodology, signed a client, and filed early fundraising paperwork.

**Here is what happens the moment a serious Series A investor says yes:**

They open a data room. Before they wire a dollar, their attorneys audit every document you've ever signed about who owns what. They call this **legal due diligence** — and for a data intelligence company, IP due diligence is the single most lethal kill zone in the process.

*The question isn't whether you've built something real. The question is whether you can prove you own it — cleanly, completely, and without gaps.*

Most founders who fail due diligence don't fail because they lied. They fail because they never built the paper trail to prove the truth.

---

## Part I — What "Clean IP" Means to a Series A Investor

When a sophisticated VC or growth-equity investor says they want **clean IP**, they mean a specific, auditable chain of ownership:

```
Idea → Work → IP → Prospectra (the Delaware entity)
```

Every link in that chain must be documented. A gap at any point means the IP may not actually belong to the company — and therefore may not belong to the investors who are about to buy equity in it.

### The Four Questions Every Investor Asks

**1. Was every person who touched the IP an employee or a contractor with a signed Invention Assignment Agreement?**

This is the most common failure point. A co-founder, a freelance developer, an early advisor who "helped design the model" — if any of these people touched the GRI methodology or signal architecture *without* signing an invention assignment, the IP may be legally theirs, not Prospectra's.

The legal default in most U.S. jurisdictions: **work created by an independent contractor does NOT automatically belong to the company**, even if you paid for it. You must have a signed agreement that says otherwise.

**2. Was there any IP created before the Delaware entity was incorporated (March 14, 2026)?**

If the GRI methodology was designed before Prospectra Inc. existed, it was created by Bolo as an individual. To transfer it to the company, you need a formal **IP Assignment Agreement** signed by Bolo (and any other founder) assigning all pre-incorporation IP to Prospectra Inc.

Without this, the IP exists in a legal grey zone: the individual created it, the company uses it, but the ownership was never formally transferred.

**3. Do any third-party licenses constrain your freedom to operate?**

If any component of the GRI methodology, signal architecture, or Databricks pipeline incorporates open-source code with a restrictive license (GPL, AGPL), a third-party data feed with limited commercial rights, or licensed analytical frameworks — investors need to know. Some licenses (particularly copyleft licenses) can require you to open-source your own code, which would destroy the trade secret protection lesson 370 described.

**4. Has any IP-related dispute occurred — even informally?**

A prior employer claim ("that methodology was developed on company time"), a contractor dispute, a co-founder who left unhappy — any of these create contingent legal liability that investors will price or walk away from.

---

## Part II — How to Run a Cap Table Audit

The cap table audit is different from the IP audit but runs in parallel. Investors are buying equity; they need to know exactly what they're buying into.

### The Cap Table Stack

A clean Series A cap table has five layers:

| Layer | What It Covers |
|-------|---------------|
| Common stock | Founder shares (Bolo 45%, Eli 45% per PROJECT_FOUNDATION.md) |
| Option pool | 10% option pool — what's been granted, vested, and outstanding |
| SAFEs / convertible notes | Any prior financing that converts at Series A |
| Warrants | Any warrants issued (advisors, service providers) |
| Series A (new) | What investors are buying |

An investor's attorneys will check every one of these layers for:
- Valid board approval for all issuances
- 83(b) elections filed within 30 days of founder stock grants (critical for tax — if you missed this, fix it now before the round)
- Proper vesting schedules documented
- Any side letters or pro-rata rights
- Co-founder alignment: Eli at 45% means Eli's signature is required on major corporate decisions. Has she been formally engaged? Do her shares have a vesting schedule or are they fully vested? This is a question investors will ask.

### The 83(b) Election — The Silent Time Bomb

If founder shares were granted with a vesting schedule, the founders should have filed an 83(b) election with the IRS within **30 days** of the grant date. This election locks in the tax basis at grant (near zero) rather than at vest (potentially high).

Missed 83(b) elections are unfixable after 30 days. If this was missed at Prospectra's March 2026 incorporation, the tax exposure is a known issue that must be disclosed to investors — not hidden. A good attorney can help structure around it, but not if you pretend it didn't happen.

### The Eli Question

Project Foundation shows: Bolo 45% / Eli 45% / 10% option pool.

Before any Series A process, this question needs a clear answer:
- Is Eli actively involved in Prospectra's current direction (the geopolitical intelligence platform)?
- Does she understand and agree with the pivot from the original mining AI mission?
- Do her 45% shares vest over time, or are they already fully vested?

A Series A investor acquiring, say, 20% of the company is effectively buying into a structure where Eli (at 45%) is the largest shareholder and has significant control rights. If Eli is not aligned, not reachable, or actively hostile, that is a deal-killer. Investors will ask for this directly.

---

## Part III — How IP Disputes Actually Play Out in Data Analytics

**The MSCI Index Litigation (2012–2020)**

One of the most instructive IP disputes in data intelligence. MSCI sued ISS (Institutional Shareholder Services) over the use of MSCI's governance framework in ISS's proxy advice products. The core dispute: did ISS's analytical work product belong to MSCI because it was built on MSCI's licensed data? After eight years of litigation, the case settled — but the lesson is that **the IP boundary between licensed data, derived analysis, and proprietary methodology is exactly where disputes happen**. Prospectra's use of GDELT (public) as the foundation for a proprietary GRI (yours) is legally clean, but it must be documented.

**The Bloomberg Data License Disputes**

Bloomberg has pursued multiple financial institutions for using Bloomberg Terminal data (licensed for personal use) in automated systems (not covered by standard terminal licenses). The principle: a license that permits use A does not implicitly permit use B. If Prospectra ever licenses any Bloomberg, Refinitiv, or FactSet data feeds, the data license terms must be reviewed against the specific use case before building a pipeline on top of them.

**The "Departing Employee" Pattern**

The most common IP dispute in the analytics industry doesn't involve external parties — it involves a key person leaving. A senior analyst who designed the signal weighting model leaves to join a competitor. Within six months, the competitor launches a suspiciously similar product.

You have three levels of recourse:
1. **Trade secret misappropriation** (if they took documents or used confidential methodology)
2. **Breach of NDA** (if they disclosed confidential information)
3. **Breach of non-solicitation** (if they recruited your clients or staff)

The degree to which you can enforce any of these depends entirely on whether the agreements were in place *before* the person started. This is why the legal infrastructure from lesson 370 is not bureaucracy — it is the specific legal standing to protect the business when someone behaves badly.

---

## Part IV — Building Prospectra's IP Due Diligence Package

A practical checklist for what should be in the data room before any Series A process:

**IP Documents**
- [ ] List of all IP assets (trade secret register)
- [ ] Signed invention assignment agreements for every contributor
- [ ] IP assignment from founder(s) covering all pre-incorporation work
- [ ] GDELT and all third-party data source license terms
- [ ] Open-source license audit for all code dependencies
- [ ] Research disclaimers on all client-facing output

**Cap Table Documents**
- [ ] Full cap table (Carta, Pulley, or equivalent cap table management software)
- [ ] All stock issuance records with board approvals
- [ ] 83(b) election filings (or documentation of the miss and legal advice received)
- [ ] Any SAFEs, convertible notes, or side letters
- [ ] Vesting schedules for all grants
- [ ] Written evidence of Eli's informed agreement with the current company direction

**Corporate Documents**
- [ ] Certificate of Incorporation (Delaware)
- [ ] Current bylaws
- [ ] Board minutes (all major decisions)
- [ ] List of all contracts with clients and contractors

**The Single Most Valuable Thing You Can Do Now**

Hire a startup-specialized attorney to conduct a **formation audit** — a review of every document from incorporation to present. This costs $3K–$8K and takes two to four weeks. It will surface every gap before investors do. Every gap an investor finds is a negotiating lever. Every gap you find first is a problem you can fix quietly.

---

## Investment Implications

**For Prospectra as an investable company:**
A clean IP and cap table audit directly determines the Series A valuation achieved — not because investors discount on principle, but because gaps create legal risk and legal risk is priced. A company that walks into a data room with a complete, audited IP package signals maturity. It removes one of the largest sources of deal friction.

**For the data intelligence industry as a sector:**
The companies in this space (geopolitical risk intelligence, financial data analytics, alternative data providers) trade at 8–15x ARR at Series A if they have clean IP and defensible methodologies. The valuation gap between "clean" and "messy" deals in this space is 2–3x — not because the product is different but because the legal risk affects the investor's exit math.

---

## Databricks Angle

**Immediate relevance:** 
- Your Databricks pipelines ingest GDELT (public), Yahoo Finance (public), and FRED (public). The transformation logic — the GRI scoring engine, the signal generator, the regime change detector — is your IP. Document this in a `data_provenance` table in the bronze tier (as suggested in lesson 370).
- Any Databricks notebook, job, or feature engineering code should be tracked in git with clear authorship — this becomes part of your IP chain.

**Pipeline idea:**
Build a `code_provenance` table in Unity Catalog that records: notebook name, author, date created, last modified, and a brief description of what IP it implements. This creates an auditable record that the analytical logic was created *by Prospectra personnel under invention assignment* and not imported from a third party without license. It's a five-line delta table and it dramatically simplifies the IP audit.

---

## Reflection Questions

1. **The gap audit:** List every person (employee, contractor, advisor) who has contributed to the GRI model or signal architecture since the project began in April 2026. For each person, identify whether a signed invention assignment agreement exists. What's the gap count?

2. **The pre-incorporation IP question:** The GRI concept and analytical framework were developed before March 14, 2026. Has there been a formal IP assignment from Bolo to Prospectra Inc.? If not, this is the single highest-priority legal task before any fundraising conversation.

3. **The Eli question:** Prospectra's original mission was mining AI. The project has pivoted fully to geopolitical intelligence. Has Eli been formally briefed on this pivot? Does she have a defined role, or is she a passive shareholder? What is her current stance — and have you documented it?

---

## Questions for Next Session

- What does the Series A investor conversation actually look like day-by-day — from first meeting to term sheet to close?
- How do you build a data room that makes due diligence fast and friction-free?
- What are the most common legal surprises that kill late-stage deals — and how do you prevent them?

---

## CEO Note

Lesson 370 laid out the legal infrastructure Prospectra needs. Today's lesson answers the harder question: *how does an investor actually check whether you built it?*

The Eli alignment question is the single most underaddressed strategic risk I see in the Prospectra structure. Bolo is building. Eli holds 45% of the equity. The two are not yet formally re-engaged around the current direction. This is not a problem today. It becomes a problem the moment a Series A term sheet is on the table and investors ask Eli to sign a shareholder approval. Surface this conversation early — before it has stakes.

*CEO — Prospectra Geopolitics & Investment Project*
