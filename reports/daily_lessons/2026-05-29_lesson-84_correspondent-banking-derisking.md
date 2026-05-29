# Lesson 84: Correspondent Banking & De-Risking — The Quiet Fragmentation of Global Finance

**Date:** May 29, 2026
**Session Type:** Daily Lesson
**Topic:** Correspondent Banking & De-Risking — How Compliance Costs and Geopolitical Risk Are Quietly Severing the Arteries of Global Trade
**Lesson Number:** 84 of ongoing curriculum

---

## Opening Question

*A Somali-American family in Minneapolis wants to send $500 to relatives in Mogadishu. To do so, they walk into a Dahabshiil money transfer office. The money arrives in two hours. Meanwhile, no US commercial bank will touch that transaction — because the last four major banks that tried to maintain Somali correspondent banking relationships closed them between 2011 and 2014, citing regulatory compliance costs. The question: if the most sophisticated financial system in human history cannot route $500 to Mogadishu through formal channels, what does that tell you about the architecture of globalization — and what does it mean when the same dynamic starts affecting not just Somalia but Jamaica, the Cayman Islands, and entire Pacific island nations?*

This is the correspondent banking crisis. It is not dramatic. There are no market crashes, no headlines. It is the slow, compliance-driven withdrawal of global banks from entire economies — and it is reshaping the financial architecture of the developing world with implications that extend to every portfolio with emerging market or frontier exposure.

---

## Core Concept: What Is Correspondent Banking?

### The Basic Architecture

When you wire money from a US bank account to a bank in Peru, the transaction does not travel in a straight line. Your bank almost certainly has no direct relationship with the Peruvian bank on the other end. Instead, the transaction routes through a chain of **correspondent banks** — large international banks that maintain accounts on behalf of smaller, local banks and process payments on their behalf.

The structure:

```
YOUR BANK (small US bank)
    ↓  (sends payment instruction + funds via CHIPS/Fedwire)
CORRESPONDENT BANK (e.g., Citibank, JPMorgan, Deutsche Bank)
    ↓  (routes through its global network, possibly through another correspondent)
LOCAL BANK (Banco de Crédito del Perú)
    ↓  (credits recipient account)
RECIPIENT
```

The correspondent bank in the middle is the critical node. It holds **nostro accounts** (accounts of foreign banks denominated in the correspondent's currency — "our money held at your bank") and **vostro accounts** (accounts held by the foreign bank at the correspondent — "your money held at our bank"). These mirror accounts enable settlement without requiring every bank in the world to maintain direct bilateral relationships with every other bank.

**Scale:** The global correspondent banking network processes approximately $5–10 trillion in cross-border transactions per day. It is the capillary system of global trade — less visible than the arteries (CHIPS, SWIFT) but equally essential for blood to reach the extremities.

### The Three-Tier Hierarchy

```
TIER 1: GLOBAL CORRESPONDENT BANKS
  Citibank, JPMorgan, Deutsche Bank, HSBC, Standard Chartered, BNY Mellon
  → Maintain the most extensive global networks
  → Hold relationships with thousands of local banks worldwide
  → Are the "hubs" — their exit changes everything for connected spokes

TIER 2: REGIONAL CORRESPONDENTS
  Mid-sized international banks with regional specialization
  → E.g., a major Gulf bank acting as correspondent for smaller GCC banks
  → A Brazilian bank acting as correspondent for South American local banks
  → Often depend on Tier 1 correspondents themselves for dollar clearing

TIER 3: LOCAL BANKS
  The banks that actually hold customer accounts
  → Access global finance entirely through Tier 1/2 correspondents
  → No correspondent = no international wires = no trade finance
```

The cascade risk: when a Tier 1 correspondent exits a country or corridor, every Tier 3 bank that depended on it loses access unless a replacement Tier 1/2 bank steps in. In markets where few correspondents operate, replacement is not guaranteed.

---

## Historical Grounding: The Compliance-Risk Tsunami (2008–Present)

### The Regulatory Ratchet

The correspondent banking crisis is a product of regulatory decisions made with good intentions that produced deeply perverse outcomes. The sequence:

**2001 — USA PATRIOT Act:** Expanded Bank Secrecy Act requirements post-9/11. Banks must conduct due diligence on correspondent accounts, with enhanced due diligence for foreign banks from "jurisdictions of concern." The definition of "concern" is left largely to regulators and, critically, to banks' own compliance departments.

**2008–2012 — AML enforcement wave:** A series of landmark enforcement actions established that large banks would be held personally liable — and pay enormous fines — for failures in their correspondent relationships:
- **HSBC (2012): $1.92 billion fine** for processing Mexican drug cartel money through its US correspondent operations (facilitating $881 million in Sinaloa cartel transactions via its Mexican subsidiary's US accounts)
- **Standard Chartered (2012): $340 million** for Iran-related sanctions violations via correspondent channels
- **BNP Paribas (2014): $8.97 billion fine** — then the largest bank fine in US history — for processing transactions for Sudan, Iran, and Cuba through US correspondent accounts, deliberately stripping identifying information to evade detection

These fines sent a clear signal: the correspondent relationship is not just a revenue line. It is a liability. The cost of a single bad actor transacting through your correspondent network can exceed a decade of revenue from that relationship.

**2012–2016 — The De-Risking Wave:** Large correspondent banks began systematically reviewing their correspondent relationships and exiting those where:
- The jurisdiction was high-risk under FATF (Financial Action Task Force) criteria
- The local bank's AML/KYC standards were uncertain or difficult to verify
- The revenue from the relationship did not justify the compliance cost and potential liability
- The regulator had issued guidance or informal "suggestions" about certain corridors

The result was a wave of "de-risking" — a euphemism for terminating correspondent banking relationships for compliance reasons rather than credit reasons. This was not bankruptcy. The banks being cut off were solvent. They lost access to global finance because the regulatory risk of maintaining the relationship was higher than the economic value.

### The Scale of the Withdrawal

The data is stark. SWIFT data shows:

- **Number of active correspondent banking relationships globally declined by ~25% between 2011 and 2022**
- The decline was concentrated in specific regions: Caribbean (-60%), Pacific (-30%), Sub-Saharan Africa (-25%), MENA (-15%)
- The number of correspondent banks (the hubs) providing relationships declined even faster — a small number of Tier 1 banks account for an increasing share of remaining relationships, creating dangerous concentration

**Who got cut:**
- Small island developing states (Caribbean, Pacific) — where banking systems are inherently small and the economics of correspondent relationships are weakest
- High-risk jurisdictions per FATF: Somalia, Sudan, Yemen, North Korea, Iran
- "High-risk adjacent" jurisdictions: countries with perceived AML weaknesses even if not formally listed (Jamaica, Belize, multiple Pacific nations)
- Specific corridors: US-Cuba (even before sanctions relief), US-Somalia (completely severed by major banks by 2014), many US-MENA routes

### The Somalia Paradox — A Case Study in Perverse Outcomes

Somalia is the extreme case. By 2014, all major US banks had terminated their correspondent relationships with Somali money transfer operators (hawaladars). The stated reason: inability to verify that Somali hawaladars had adequate AML/KYC controls to prevent terrorist financing (al-Shabaab operated in Somalia).

The outcome was the opposite of the intended effect:
1. **Formal remittances collapsed.** Approximately $1.3 billion/year in remittances flow to Somalia — equivalent to ~25% of Somali GDP. These flows are a primary food security mechanism.
2. **Informal channels expanded.** Without formal bank channels, remittances moved through cash couriers, informal hawala networks, and cryptocurrency — all with less regulatory oversight than the formal channels that were shut down.
3. **Financial crime risk increased.** By forcing remittances underground, de-risking reduced transparency and made it harder, not easier, to identify suspicious flows.
4. **Humanitarian damage was severe.** The World Bank documented that disruption of Somali remittances contributed to food insecurity, as families could not receive money to purchase food.

The Somalia case is cited in every major policy paper on de-risking because it illustrates the core paradox: compliance-driven de-risking can increase the financial crime risks it was designed to reduce, while imposing enormous economic costs on innocent populations.

---

## The Geopolitical Dimension: When De-Risking Meets Sanctions

### From Compliance to Weaponization

The line between de-risking (banks exiting relationships because of compliance cost) and sanctions (governments directing banks to exit relationships because of geopolitical intent) is becoming increasingly blurred. This matters enormously for the investment framework.

**Pure de-risking** is a market failure caused by regulatory structure. It is theoretically correctable through regulatory reform, clearer guidance, or better AML technology.

**Sanctions-driven de-risking** is deliberate geopolitical policy. It uses the correspondent banking network as a transmission mechanism for economic coercion. When the US Treasury's OFAC designates an entity, every correspondent bank in the dollar system must refuse to process transactions involving that entity — or face the same BNP Paribas fate. This makes the correspondent banking system the enforcement mechanism for US (and to a lesser extent EU and UK) sanctions policy.

The 2026 landscape shows both dynamics operating simultaneously:

| Mechanism | Driver | Target | Reversibility |
|-----------|--------|--------|---------------|
| AML de-risking | Compliance cost/liability | Small economies, weak-AML jurisdictions | Theoretically reversible with regulatory reform |
| OFAC sanctions | US foreign policy | Iran, Russia, North Korea, Venezuela | Geopolitically determined |
| Secondary sanctions | US extraterritorial reach | Non-US banks that transact with sanctioned entities | Extremely high deterrence effect |
| FATF blacklisting | International AML standards body | Myanmar, Afghanistan, etc. | Requires compliance reform |

**Secondary sanctions are the most consequential instrument.** When the US threatens secondary sanctions — meaning the US will sanction foreign banks that do business with already-sanctioned entities — it extends the reach of US correspondent banking control beyond the dollar system itself. A Chinese bank that processes transactions for Iran faces the risk of losing its own US correspondent relationships (and thus dollar clearing access), even if the transaction itself was not dollar-denominated. This is why many Chinese banks have been cautious about openly serving Iranian entities despite China's official non-participation in Iran sanctions.

### The FATF Architecture — The AML Infrastructure as Geopolitical Tool

The **Financial Action Task Force (FATF)** is the intergovernmental body that sets global AML/CFT (counter-terrorist financing) standards. Founded in 1989 by the G7, it now has 40 member jurisdictions. Its grey list and black list are the primary instruments through which correspondent banking risk is formally structured.

**The FATF process:**
- **Grey list (Jurisdictions Under Increased Monitoring):** Countries with strategic AML/CFT deficiencies that have committed to reform. Banks interpret this as "elevated correspondent banking risk." Many Tier 1 correspondents exit grey-listed jurisdictions automatically or apply heavy compliance surcharges.
- **Black list (Non-Cooperative Jurisdictions):** Countries subject to enhanced countermeasures. Effectively means near-total exclusion from the dollar correspondent system (currently: North Korea, Iran, Myanmar in 2026).

**The geopolitical critique of FATF:** FATF is formally a technical standards body. In practice, its grey-listing decisions have significant geopolitical dimensions:
- Countries that are geopolitically disfavored by G7 governments face faster and harsher listing processes
- Countries with strong G7 political relationships receive more lenient treatment despite equivalent compliance gaps
- The US Treasury has significant influence over FATF agenda-setting and listing decisions
- FATF has been criticized for asymmetric treatment — Western jurisdictions with documented AML failures (UK "laundromat" problems, Delaware shell company opacity) face no listing risk, while developing country banking systems face existential consequences for similar or lesser failures

This critique does not require conspiracy to be valid. It is a structural critique: the institution's governance is dominated by the countries whose geopolitical preferences the listing decisions often happen to serve.

---

## The Pacific Case: De-Risking as Existential Threat

The Pacific island nations represent the most acute current crisis. A 2025 Pacific Islands Forum report documented:

- **Multiple Pacific island nations are at risk of losing all correspondent banking access** — meaning their banking systems would have no connection to global dollar clearing
- The number of correspondent banking relationships in the Pacific declined by ~30% over the prior decade
- Countries including Samoa, Tonga, Vanuatu, and others have lost correspondent relationships with major US and Australian banks
- The Pacific Islands Forum is in emergency negotiations to contract a "bridge" correspondent banking provider to prevent complete exclusion — final contracting expected mid-2026

The implication is staggering in its simplicity: **there are sovereign nations — UN member states — that are at risk of having no ability to receive or send international wire transfers in US dollars.** No trade finance. No remittances. No payment for imports. This is not a hypothetical risk. It is a 2026 operational problem.

For investors: frontier market exposure to Pacific, Caribbean, and sub-Saharan African banking systems carries a specific risk that standard credit analysis does not capture — the risk that the institution is solvent but cut off from global finance due to correspondent withdrawal.

---

## The Response: Alternatives to the Correspondent System

### The Fintech Layer: Partial Solutions

Several categories of companies have emerged to fill gaps left by correspondent bank withdrawal:

**Payment fintechs (Wise, Remitly, WorldRemit):** Built direct-to-consumer international payment systems that aggregate flows and route them through their own correspondent relationships — effectively creating a "super-agent" layer that can maintain relationships where individual small banks cannot. They provide cost-effective last-mile delivery to markets where banks have exited.

**Stablecoins and crypto corridors:** In markets where formal banking is unavailable, USDC and USDT have emerged as de facto international payment rails. Somalia, Sudan, and Venezuela have seen significant adoption of dollar stablecoins for exactly this reason — they provide dollar-denominated settlement without requiring correspondent banking access. This is an ironic outcome: the compliance crackdown that drove de-risking has accelerated adoption of the least regulated payment infrastructure.

**RippleNet and blockchain settlement:** Ripple's network (using XRP as a bridge asset or fiat-to-fiat pathways) has been adopted by several Gulf and Southeast Asian banks seeking to reduce reliance on traditional correspondent chains. The technology reduces settlement time and costs, but does not eliminate the underlying regulatory/sanctions compliance requirements.

**Regional correspondent hubs:** Some non-Western banks have stepped into vacated correspondent slots. UAE banks (FAB, Mashreq), Turkish banks (Ziraat, Halkbank), and Indian banks (State Bank of India) have expanded correspondent coverage in corridors vacated by US and European banks. This has created new geopolitical dynamics — the UAE has become an essential transit node for Russia-related dollar flows post-2022 sanctions, because UAE-based correspondents maintained relationships that Western banks exited.

### The UAE as the New Correspondent Hub — A Live Geopolitical Dynamic

The UAE correspondent banking situation is the clearest current example of how geopolitics is reshaping the correspondent network in real time.

Post-February 2022, as Western sanctions drove the exit of US and European correspondents from Russia-related banking:
- UAE banks maintained relationships with Russian entities, enabling dollar-denominated trade flows to continue via UAE intermediaries
- Dubai became a hub for Russian capital flight — Russian individuals and companies establishing UAE bank accounts and businesses
- The UAE's total trade with Russia expanded dramatically in 2022–2024, partly facilitated by correspondent banking availability

The US response was a multi-year pressure campaign on UAE banks: Treasury officials visited Abu Dhabi repeatedly, threatening secondary sanctions against UAE institutions that processed Russia-related transactions. Some UAE banks (particularly those with significant US correspondent exposure) began tightening; others — particularly those without heavy US exposure — maintained relationships.

**This is the fundamental tension:** The US uses its control of dollar correspondent banking to enforce sanctions extraterritorially. Countries that want to maintain dollar correspondent access must comply. Countries (or banks) willing to sacrifice dollar correspondent access can route transactions differently. The UAE, with its combination of dollar exposure and desire for geopolitical autonomy, is navigating this tension in real time — and its choices are reshaping which corridors are open.

---

## Investment Implications

**Frontier market financial sector equities:**
De-risking creates a specific risk premium in frontier market banking stocks that is rarely captured by standard credit analysis. A bank with strong balance sheet metrics can lose significant franchise value if its correspondent relationships narrow — constraining trade finance, remittance processing, and international transaction revenue. *Screen frontier market bank holdings for correspondent banking concentration risk: how many Tier 1 correspondents maintain relationships? What fraction of cross-border business depends on a single corridor?*

**Remittance-dependent economies:**
Countries where remittances represent >10% of GDP (Haiti ~20%, El Salvador ~24%, Honduras ~23%, Somalia ~25%) face macroeconomic vulnerability when correspondent de-risking disrupts remittance flows. Disruptions historically correlate with exchange rate pressure and current account deterioration. This is a specific tail risk for sovereign bonds of these countries.

**UAE and Gulf financial intermediaries:**
The UAE's emergence as the correspondent banking hub for non-aligned corridors has created real franchise value for UAE financial institutions — increased transaction volumes, expanded trade finance opportunity, higher margin non-dollar business. However, it also creates secondary sanctions exposure risk. Watch for US Treasury pressure on UAE correspondent banking as a leading indicator of whether this business model is sustainable.

**Payment fintechs and alternative rails:**
The structural de-risking trend is a multi-year tailwind for companies building payment infrastructure in underserved corridors. Wise (LSE: WISE), Remitly (NASDAQ: RELY), and their peers benefit from the systematic retreat of traditional correspondent banking. The risk is regulatory: if AML requirements are applied equally to fintechs, the competitive advantage narrows.

**Stablecoin infrastructure:**
The adoption of dollar stablecoins (USDC, USDT) in de-banked corridors is growing structurally. Tether reports that its largest user bases by adoption rate are in Turkey, Argentina, Vietnam, and Sub-Saharan Africa — exactly the markets experiencing correspondent banking stress. If stablecoin regulatory frameworks in the US provide clarity (the 2026 stablecoin bill debate is ongoing), this becomes a significant investable infrastructure theme.

**Long USD, selectively:**
In geopolitical stress scenarios, dollar correspondent banking exclusion creates flight-to-USD dynamics even among the affected parties — because the first thing any excluded party does is try to accumulate dollars through whatever formal or informal channels remain accessible. Perversely, de-risking may be net dollar-supportive in the short-to-medium term, even as it erodes dollar system legitimacy long-term.

---

## Databricks Angle

**Correspondent Banking Risk Intelligence Pipeline**

The correspondent banking network is partially observable in public data. A pipeline to track de-risking stress would combine:

**Data sources:**
- **BIS Locational Banking Statistics:** Bilateral cross-border bank exposure by country pair — published quarterly, tracks which country's banks hold claims on which other country's banks. Declining claims = correspondent withdrawal signal
- **World Bank CPMI (Committee on Payments and Market Infrastructures) data:** Tracks payment system volumes and correspondent relationships in participating countries
- **FATF grey/black list updates:** Published at each FATF plenary (three times per year) — direct correspondent banking risk trigger
- **SWIFT Analytics (partially public):** SWIFT publishes aggregate country-level transaction data
- **Remittance data (World Bank Remittances database, FRED):** Tracks remittance inflows by country — a lagging but confirmatory indicator of corridor health
- **GDELT event data:** News events coded "banking," "financial sanctions," "AML enforcement" by country as a leading indicator

**Pipeline concept:**
```python
# Correspondent Banking Risk Index
# Input: BIS bilateral banking data (quarterly)
# 
# For each country pair (home_country, correspondent_country):
#   - Track number_of_active_relationships over time
#   - Compute relationship_concentration = max(single_bank_share)
#   - Compute trend: (relationships_now - relationships_2y_ago) / relationships_2y_ago
#
# Join to:
#   - FATF listing status (binary flag)
#   - US/EU/UK sanctions activity (event count from GDELT)
#   - Remittance inflow trend (World Bank annual)
#
# Output: Correspondent Banking Vulnerability Score by country
#   Score inputs: relationship decline rate + concentration + FATF status + sanctions exposure
#
# Alert: Score > threshold → flag for investment thesis review
```

**Features to engineer:**
- Correspondent banking concentration ratio (# relationships / peak relationships)
- Corridor vulnerability index (vulnerability of country A to exit of Tier 1 correspondent B)
- FATF listing leading indicator (pre-listing AML enforcement action count)
- Remittance-corridor stress score (remittance-dependent country × corridor stress)
- UAE/non-aligned hub expansion rate (proxy for de-dollarization via alternative correspondent)

**Databricks pipeline architecture:**
- **Bronze:** Raw BIS data + GDELT events + FATF listing history (Delta Lake, quarterly update)
- **Silver:** Bilateral relationship delta table, country-level aggregations, FATF flags
- **Gold:** Correspondent Banking Vulnerability Score, country risk ranking, alert signals
- **Dashboard:** Databricks AI/BI panel showing top 10 most vulnerable corridors and trend lines

---

## Market Connection

| De-Risking Trend | Asset Class | Direction |
|------------------|-------------|-----------|
| Pacific/Caribbean corridor withdrawal | Frontier sovereign bonds | Negative — adds undisclosed risk premium |
| UAE as alternative hub | UAE financial sector equities | Conditionally positive (secondary sanctions risk cap) |
| Stablecoin adoption in de-banked markets | Stablecoin infrastructure | Structurally long if regulated |
| Payment fintech corridor expansion | WISE, RELY, similar | Structural tailwind — 3-5yr horizon |
| FATF grey-listing of new countries | EM local currency bonds of listed countries | Short on listing event, recover on reform |
| US secondary sanctions pressure on UAE | USD/AED exchange rate stability | Upside risk if UAE banking sector squeezed |
| Remittance disruption in high-remittance economies | Sovereign spreads (Haiti, Honduras, El Salvador) | Widening risk on major corridor disruption |

---

## Reflection Questions

1. **The Compliance Paradox:** The BNP Paribas $8.97 billion fine was designed to deter banks from violating sanctions. But the downstream effect was to accelerate de-risking, which has driven financial flows into informal channels (cash couriers, hawala, crypto) with less AML visibility than formal banking. Is the current AML regulatory framework making the global financial system safer or less safe from a financial crime standpoint? What regulatory redesign would preserve law enforcement capacity while reducing collateral damage to innocent economies?

2. **The UAE Dilemma:** The UAE has built significant franchise value by serving as the correspondent hub for corridors abandoned by US and European banks. The US is pressuring UAE banks with the threat of secondary sanctions. If you were the UAE central bank governor, how would you manage this tension? What is your BATNA (Best Alternative to Negotiated Agreement) if the US escalates to formal secondary sanctions on UAE banks?

3. **The Stablecoin Question:** USDC and USDT are filling correspondent banking gaps in de-banked markets. This is occurring largely outside the traditional AML/KYC framework that justified de-risking in the first place. Does the growth of stablecoin usage in Somalia, Sudan, and Venezuela represent a successful circumvention of a flawed policy, a dangerous expansion of financial crime risk, or both simultaneously? What regulatory framework would you design if you wanted to preserve the access benefits while retaining law enforcement visibility?

---

## Questions for Next Session (Spaced Repetition Hook)

- Lesson 83 (Global Clearing Architecture): How does the SWIFT messaging layer interact with correspondent banking relationships? If SWIFT is the instruction layer and correspondent banks are the execution layer, what happens when a country loses its correspondent relationships but retains SWIFT access — and vice versa?
- Lesson 74 (Financial Repression): Correspondent banking withdrawal creates financial repression-like outcomes in affected economies — limited access to international capital, forced reliance on domestic financial systems. What are the macroeconomic effects of a de facto closed capital account caused by correspondent withdrawal rather than by explicit policy?
- Lesson 65 (Geopolitics of Gold): Central bank gold repatriation is partly driven by the same fear underlying correspondent banking anxiety — the risk that financial assets held in Western jurisdictions can be weaponized. Is physical gold repatriation an analog to building domestic correspondent banking capacity?

---

## CEO Portfolio Note

Today's lesson completes an important arc: Lessons 79–84 have built a comprehensive picture of the infrastructure beneath global finance — from the repo market, through the shadow banking system, through derivatives clearing, through the global clearing architecture, and now through the correspondent banking network that connects it all to the real economy.

**The synthesis:**

The correspondent banking system is the capillary layer of global finance. Its systematic contraction — driven by compliance costs, regulatory pressure, and geopolitical sanctions — is creating a fragmented world where not all dollars are equally accessible, not all corridors are equally open, and not all financial institutions have equivalent access to the global system.

This fragmentation is **directionally consistent** with the structural thesis built across this curriculum: the world is moving from integrated to multi-bloc financial architecture. Correspondent banking de-risking is a different mechanism from CIPS expansion or gold reserve accumulation, but it is part of the same structural shift.

**Portfolio read-through:**
- **Frontier market exposure:** Any frontier or EM allocation must now include a corridor viability assessment — not just credit/macro analysis. An investment in a Somali mobile bank, a Caribbean financial institution, or a Pacific Island economy carries correspondent banking access risk that does not appear in P&L screens.
- **Alternative payment infrastructure:** The structural gap being created is an investable theme. The fintech and stablecoin infrastructure filling correspondent banking gaps is the infrastructure play on geopolitical financial fragmentation.
- **Sanctions divergence premium:** The premium on financial institutions that operate across blocs (UAE, Turkey, India) is real and growing. This bifurcation creates specific investment opportunities and specific political risks. Position sizes should reflect the binary risk — these institutions can rapidly lose franchise value if US secondary sanctions escalate.

The lesson: in geopolitical investing, the infrastructure is as important as the thesis. Know the plumbing.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Next lesson: Lesson 85 — The Architecture of Financial Sanctions: From Asset Freezes to Full Economic Isolation*
