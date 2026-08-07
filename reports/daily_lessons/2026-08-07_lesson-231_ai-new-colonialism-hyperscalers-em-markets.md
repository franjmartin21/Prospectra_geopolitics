# Lesson 231: AI and the New Colonialism — How US Hyperscalers Are Locking In EM Markets
**Date:** 2026-08-07
**Session Type:** Daily Lesson
**Curriculum Position:** 231 of extended curriculum
**Series:** The AI Infrastructure Arc — Lesson 3 of 5

---

## CEO Note

Lesson 229 established the strategic logic of sovereign AI. Lesson 230 showed how the GPU export control regime works and where it fails. Both lessons were about the US-China competition at the frontier — the two players fighting over who controls the most powerful AI compute.

This lesson zooms out to the rest of the world: the 6 billion people in developing economies who are not building frontier AI, but who are *choosing* which hyperscaler's infrastructure they will live inside for the next 20 years. That choice — being made right now, in dozens of government ministries, through $50B+ in hyperscaler investment commitments — is the infrastructure lock-in event of this decade. It is also the collision point between US strategic interests, Chinese strategic interests, and the legitimate question of whether developing countries are exchanging one form of dependency for another.

---

## Opening Question

*It is 2024. Indonesia announces that Amazon will invest $9 billion in AWS infrastructure over five years. Malaysia announces that Microsoft will invest $2.2 billion in data center and AI capacity. India signs agreements with Google, Microsoft, and Amazon totaling more than $20 billion. Southeast Asia has attracted over $50 billion in hyperscaler commitments in a three-year window.*

*Each of these governments framed the deal as a win: foreign direct investment, job creation, access to world-class AI capability, and a signal to global capital markets that the country is open for the digital economy.*

*A scholar at the African Union frames the same pattern differently: "We are building the 21st century's colonial infrastructure. The data center is the plantation. The electricity and water we consume powers computation that trains models we do not own, on data we do not control, to produce intelligence that is sold back to us at a price we do not set."*

*Who is right? And regardless of who is right — what are the investable signals embedded in this transition?*

---

## 1. The Scale of the Buildout

To understand why this matters, start with the numbers.

Between 2022 and 2026, the three US hyperscalers — Microsoft Azure, Amazon Web Services, and Google Cloud — announced combined investments exceeding **$150 billion** outside of the US and Western Europe, concentrated in:

**Southeast Asia:** $50B+ pledged, across Indonesia ($9B AWS + $1.7B Microsoft), Malaysia ($2.2B Microsoft + significant Google and AWS), Thailand (AWS new region, Google expansion), Philippines, Vietnam, and Singapore (the regional hub that underpins the entire sub-region's cloud architecture).

**Middle East:** $30B+ announced, including Microsoft's $15.2B UAE commitment through 2029, AWS's $5.3B Saudi Arabia region, and Google's $10B joint AI hub with Saudi Arabia's Public Investment Fund.

**India:** $20B+ across all three hyperscalers, with Google, Microsoft, and Amazon each committing to multi-billion dollar data center expansion tied explicitly to India's national AI mission.

**Japan and South Korea:** $20B+ combined, anchored by Microsoft's $10B Japan AI data center deal.

**Africa:** Nascent but accelerating — Google's South Africa region is live, and Nigeria, Kenya, and Egypt are the next wave.

The total is not a rounding error. This is the largest private infrastructure investment in developing economies in a generation — larger, on an annualized basis, than the peak Belt and Road era. And unlike Belt and Road (which was mostly physical infrastructure — roads, ports, power plants), this is *digital infrastructure*: the layer through which all economic activity increasingly flows.

---

## 2. The Lock-In Mechanics

The "compute colonialism" critique is not simply rhetoric. It describes a specific economic mechanism worth understanding precisely, because the mechanism is what generates the investment signal.

### The Three-Layer Lock-In Stack

**Layer 1: Infrastructure dependency.** When AWS builds a data center region in Jakarta and Indonesia's government ministries, banks, and telcos migrate to AWS, the cost of switching to Azure, Google Cloud, or a domestic alternative becomes prohibitive. Data migration costs, re-training costs, API rewrites, integration dependencies — these are not insurmountable, but they are real. The hyperscaler's data center is not a neutral piece of infrastructure like a port; it is infrastructure designed to create permanent vendor dependency. Every workload that migrates to AWS is a workload that will generate AWS revenue for the foreseeable future.

**Layer 2: AI model dependency.** The second layer is where the dynamic becomes structurally asymmetric. When an Indonesian bank uses Microsoft Azure OpenAI Service for credit scoring, or a Malaysian government ministry uses Google's Vertex AI for document processing, they are not just using cloud compute — they are embedding their workflows into AI systems whose weights, training data, and inference capabilities are controlled entirely by the hyperscaler. The country has no visibility into how the model was trained, what its failure modes are, or whether it embeds biases relevant to local context. More importantly: if Microsoft raises prices for Azure OpenAI, the bank cannot easily switch without rebuilding its entire credit scoring infrastructure.

**Layer 3: Regulatory capture through "sovereign cloud."** The hyperscalers' answer to data sovereignty concerns is the "sovereign cloud" — a physically and logically separated cloud environment, operating within national borders, subject to local law, accessible only to local entities. Microsoft's "Cloud for Sovereignty," AWS's "AWS Dedicated Local Zones," and Google's "Sovereign Cloud" offerings are pitched as solutions to the dependency problem. But the model is revealing: a sovereign cloud is still a Microsoft cloud, still running on Microsoft infrastructure, still requiring Microsoft support, still governed by Microsoft's service terms (alongside the local law layer). The sovereignty is partial. It is sovereignty over data residency, not over the intelligence that processes the data.

### The Colonial Analogy: Where It Holds and Where It Breaks

The colonial framing holds on three of its four claims:

✅ **Data extraction:** Training data for frontier models is drawn globally. The value of that data (used to train GPT-5, Gemini, Claude) accrues to the model owner, not the data source country. An Indonesian user's chat history trains a model whose IP belongs to an American company.

✅ **Asymmetric rule-making:** The EU AI Act, the US AI Safety Institute standards, and emerging export control frameworks governing AI models are written by the US and EU. EM governments can comment on these standards but are not in the room where they are set. The regulatory architecture of global AI reflects the interests of the countries that built it.

✅ **Infrastructural dependency:** The 20-year lock-in is real. Countries choosing a hyperscaler in 2025-2026 are making infrastructure decisions that will be extremely costly to reverse before 2040.

❌ **But the colonial analogy breaks on agency.** Classic colonialism involved coercion — military conquest, forced extraction, no exit. The hyperscaler model involves negotiation. Indonesia bid Amazon, Microsoft, and Google against each other. Malaysia extracted data localization commitments and local partnerships as conditions of Microsoft's $2.2B deal. Saudi Arabia used its PIF (sovereign wealth fund) to take a meaningful equity position in the Google AI hub. EM governments are not passive; they are increasingly sophisticated extractors of concessions from competing hyperscalers and competing powers (US vs. China). The question is not whether they have agency — they do — but whether that agency is sufficient to prevent the dependency that comes after the deal is signed.

---

## 3. China's Counter-Play: The Digital Silk Road

The US hyperscaler model is not operating in a vacuum. China's Digital Silk Road — the technology arm of the Belt and Road Initiative — represents a deliberate counter-architecture, targeting specifically the markets where US hyperscalers are weakest or where geopolitical alignment makes US relationships complicated.

**The Digital Silk Road toolkit:**
- **Huawei Cloud:** Data centers, cloud services, and 5G infrastructure across Africa, Central Asia, and parts of Southeast Asia. Since the US chip ban accelerated its domestic hardware build, Huawei has doubled down on deploying its stack internationally — often bundled with government-to-government financing that no US company can match.
- **Alibaba Cloud:** Dominant across Southeast Asia (particularly Indonesia and Malaysia, where its e-commerce subsidiaries, Lazada and Tokopedia, generate demand). Provides cloud infrastructure to government clients in Thailand, Philippines, and Pakistan.
- **Tencent Cloud:** Focused on gaming and media sectors in Southeast Asia, with expanding general cloud offerings.
- **The Digital Silk Road financing model:** Unlike US hyperscalers (which require commercially viable deals), Chinese tech expansion often comes with **state-backed financing, below-market rates, and government-to-government packaging** that bundles 5G, cloud, surveillance technology, and digital payment infrastructure into a single sovereign offer. Algeria's government data center was built with Huawei support. Egypt, Nigeria, and Ethiopia have all received Chinese digital infrastructure that would not exist on commercial terms.

**The competitive dynamic this creates:** In any EM country, there is now an explicit binary choice — not just between hyperscalers, but between technology ecosystems. Choosing AWS means choosing integration with US AI governance, US export control constraints, and US data standards. Choosing Alibaba Cloud means choosing integration with Chinese AI governance, Chinese data architecture, and — depending on the country's geopolitical position — potential secondary sanctions exposure from the US. In practice, many EM countries are not choosing: they are hedging, running AWS for international-facing workloads and Alibaba Cloud for domestic e-commerce, Huawei for 5G infrastructure, and Microsoft for government digital services. Simultaneous multi-hyperscaler exposure is the pragmatic expression of non-alignment in the digital age.

---

## 4. The EM Resistance: Data Localization, Sovereign Models, and the Third Way

A subset of EM countries — those with sufficient economic weight to demand concessions — are developing what might be called "third way" strategies that attempt to extract hyperscaler investment while limiting dependency.

**India's model:** The most aggressive assertion of data sovereignty in an EM context. India's Digital Personal Data Protection Act (2023) and subsequent AI governance framework mandate data localization for certain categories of sensitive data, require local processing for specific government AI workloads, and push hyperscalers toward JV structures with domestic partners. India has also launched its own sovereign AI initiative — IndiaAI — building domestic compute infrastructure and funding Indian foundation model development. The result: India gets the $20B+ in hyperscaler investment AND builds domestic capacity AND maintains the regulatory leverage to negotiate the next round of commitments.

**UAE's model:** A sovereign wealth approach. Rather than simply attracting hyperscaler investment, the UAE (through G42 and ADNOC) has taken equity positions in AI partnerships. The Microsoft-G42 deal involved Microsoft taking a $1.5B stake in G42 — inverting the typical FDI dynamic. The UAE has also built its own frontier AI model (Falcon, from Abu Dhabi's Technology Innovation Institute) and is using that capability as both a strategic asset and a negotiating chip with US partners. The result: the UAE is simultaneously a US hyperscaler client and an emerging AI power in its own right.

**Indonesia's model:** The transactional approach. Indonesia negotiated data localization commitments, local hiring requirements, and domestic cloud training programs from each hyperscaler as conditions of investment. It has not built domestic AI capability at scale, but it has extracted concessions that reduce (though do not eliminate) the pure dependency dynamic.

**Africa's structural disadvantage:** Most African countries lack the economic weight to extract meaningful concessions. Google building a South Africa region creates infrastructure for South Africa, but the value chain — model training, IP, pricing — remains entirely offshore. The Africa Union's March 2026 AI framework paper explicitly called this out as a structural asymmetry requiring multilateral governance solutions that do not yet exist.

---

## 5. The UAE Attack: A Warning Signal

One event that has not received sufficient analytical attention: a March 2026 attack on hyperscaler data center infrastructure in the UAE and Bahrain caused significant service disruptions and paused hyperscaler investment announcements for approximately six weeks. The attack — attributed to Iranian-linked actors in the context of the broader Gulf conflict — demonstrated what was previously theoretical: AI infrastructure concentration in geopolitically exposed locations creates systemic risk.

The investment implication is direct: hyperscaler data centers in conflict-proximate locations carry a risk premium that is not yet consistently priced. A data center in Dubai is not the same risk as a data center in Virginia — even if both run the same software and serve comparable workloads. The underwriting of that risk, and the question of who bears it (the hyperscaler, the sovereign client, the insurance market), is an emerging investable theme.

---

## 6. Investment Implications

### US Hyperscalers (Microsoft, Amazon, Google, Meta)

**The structural bull case:** EM expansion is the primary growth vector for the next decade. The US, EU, and Japan markets are approaching cloud saturation; the incremental dollar of compute demand growth is in Indonesia, India, Saudi Arabia, Nigeria, and Brazil. Every dollar committed to EM data center expansion is infrastructure for a market where cloud penetration is below 20%. **Bias: long all three hyperscalers on EM structural growth; this is the primary driver of their data center capex commitment in 2026-2028, not just AI training.**

**The geopolitical tail risk:** The March 2026 UAE attack materialized a risk that has always been latent in Gulf expansion. Hyperscaler data centers in the Middle East are military-strategic infrastructure — they process government workloads, financial flows, and defense-adjacent data. In a conflict, they are targets. **Portfolio note: apply a geopolitical risk discount to hyperscaler revenue/valuation attributed to Gulf data center capacity; this is not a reason to avoid the sector but a reason to model downside scenarios.**

**The China competition risk:** In Africa and parts of Southeast Asia, Alibaba Cloud and Huawei Cloud are capturing market share that US hyperscalers will struggle to recapture. Countries with strong China diplomatic alignment (Pakistan, Ethiopia, many African nations) are building on Chinese infrastructure by default. This is not a near-term earnings risk — these markets are too small — but it is a long-run structural risk to the total addressable market assumption embedded in hyperscaler valuations.

### Data Center REITs and Infrastructure

The hyperscaler buildout requires land, power, and cooling infrastructure that the hyperscalers themselves do not own. Data center REITs (Equinix, Digital Realty, Iron Mountain) and regional data center operators in EM markets benefit directly from the expansion. The more interesting play: **data center operators in second-tier EM markets** — Malaysia, Nigeria, Saudi Arabia — where hyperscaler expansion creates anchor tenants that de-risk the build. **Bias: long Equinix as the global interconnection hub; monitor regional EM data center operators (e.g., Africa Data Centres, Gulf Data Hub) for emerging market-specific exposure.**

### Power Infrastructure

Every data center is a power plant in reverse — it consumes electricity at industrial scale. The hyperscaler buildout in EM markets creates a structural demand boom for power infrastructure: grid upgrades, backup generation, cooling systems, and (in the medium term) on-site generation from solar and gas. **Bias: long power infrastructure suppliers (ABB, Eaton, Vertiv) that benefit from EM data center construction; long gas turbine makers (GE Vernova, Siemens Energy) for data center backup power; in specific EM markets (India, UAE, Saudi Arabia), long local utilities positioned to supply hyperscaler campuses.**

### The EM Sovereignty Plays

A small but growing set of EM sovereign AI initiatives — India's IndiaAI, the UAE's Falcon ecosystem, Saudi Arabia's SDAIA — are building domestically. The companies that supply them (compute, networking, cooling, and increasingly domestic model training services) are not US hyperscalers. They are second-tier cloud providers, domestic telcos, and specialized AI infrastructure suppliers. **Bias: long companies that supply sovereign AI infrastructure rather than just US hyperscaler competitors; the sovereign AI market is structurally separate from the hyperscaler market and priced differently.**

### The China Digital Silk Road as a Hedge

For investors with EM equity exposure, Alibaba Cloud and Tencent Cloud's expansion into markets where US hyperscalers are geopolitically constrained (parts of Africa, Central Asia, certain ASEAN markets) represents a portfolio hedge on the US hyperscaler dominance thesis. If US-China tech bifurcation intensifies and EM countries are forced to choose sides, the world bifurcates into US-cloud and China-cloud spheres. In a bifurcation scenario, Alibaba (BABA) is a structural winner in the China-aligned EM sphere. **Bias: a small BABA position (5-7% of EM tech allocation) as a hedge on the bifurcation scenario, not a primary conviction trade.**

---

## 7. Databricks Angle

**Dataset: Hyperscaler Investment Announcement Tracker**

Build a pipeline that monitors hyperscaler EM investment announcements and maps them to:
1. Country-level cloud penetration data (World Bank Digital Development indicators, GSMA Intelligence)
2. Bilateral trade and diplomatic relationship data (to score alignment probability — US-sphere vs. China-sphere vs. non-aligned)
3. Data center construction timelines (from construction permit filings, satellite imagery services like Planet Labs)
4. Local power grid capacity data (World Bank energy statistics) to identify power-constrained vs. power-ready markets

**Feature Engineering:**
- "Hyperscaler concentration index" by country: what share of in-country cloud capacity is controlled by a single provider? High concentration = lock-in risk = policy response risk
- "Sovereign AI spend score": government budget allocated to domestic AI capability vs. foreign hyperscaler contracts — countries with high sovereign AI spend are less locked in and more likely to generate domestic AI industry investable opportunities
- "Digital Silk Road penetration": presence of Huawei Cloud, Alibaba Cloud, Tencent Cloud in-country infrastructure as a share of total cloud capacity — high DSR penetration predicts US hyperscaler market share constraints

**Investment Signal Application:**
- New hyperscaler EM commitment announcement → leading indicator for local data center REIT/infrastructure equity re-rating (2-8 week lag)
- Government data localization legislation → watch for hyperscaler compliance capex (bullish for local infrastructure players) or market exit (bearish for local tech sector dependent on hyperscaler)
- Chinese AI lab open-source release reaching EM developer adoption thresholds → signal for US hyperscaler market share risk in that geography

---

## 8. Reflection Questions

1. **India is simultaneously attracting $20B+ in US hyperscaler investment AND building domestic AI infrastructure AND negotiating favorable terms from each competing provider. Most smaller EM countries cannot replicate this — they lack the market size to attract competitive bidding. What structural factor determines whether an EM country has sufficient leverage to avoid lock-in, and how would you construct a "hyperscaler negotiating power index" for 50 countries?**

2. **The UAE's G42 model — taking equity positions in AI partnerships rather than simply hosting foreign infrastructure — represents a different theory of sovereignty. Instead of data localization as the control mechanism, they use equity ownership as the control mechanism. Compare the two approaches: which produces better long-run outcomes for the sovereign, and which produces better long-run outcomes for the investor?**

3. **The colonial analogy is contested: some argue it is accurate and reveals a structural injustice; others argue it understates EM agency and overstates the comparison. Construct the strongest possible version of both arguments. Then: does your answer to this debate change any investment position you would take? If the debate is irrelevant to the investment thesis, why? If it is relevant, how?**

---

## Questions for Next Session (Spaced Repetition)

- *From Lesson 230 (GPU Export Controls):* The H200 volume cap deal allows China to import ~1 million H200 units/year. The UAE, Saudi Arabia, and other Gulf states are now *more* reliable recipients of advanced US chips than China. Does this mean the Gulf has a structural AI infrastructure advantage over China for the next 5 years — and how does this affect the investment thesis on Gulf sovereign AI?
- *From this lesson:* A country that chooses Alibaba Cloud for domestic government workloads and AWS for internationally facing workloads is simultaneously in both technology spheres. In a bifurcation scenario (forced choice between US-aligned and China-aligned tech stacks), which workloads would be forced to migrate, and what is the economic cost of that forced migration to the government and to investors in that country's digital economy?
- *From Lesson 229 (Sovereign AI):* Saudi Arabia's SDAIA and UAE's TII are both building sovereign AI models. Both are using US chips (under the new H200 deal). Are these countries building genuine strategic autonomy, or are they building US-chip-dependent sovereignty that is one export control escalation away from becoming a constraint?

---

## Series Position

**AI Infrastructure Arc Progress:**
- ✅ Lesson 229: Sovereign AI and the New Compute Geography
- ✅ Lesson 230: The GPU Supply Chain — How Semiconductor Export Controls Actually Work and What They Miss
- ✅ Lesson 231: AI and the New Colonialism — How US Hyperscalers Are Locking In EM Markets *(this lesson)*
- ⬜ Lesson 232: The Energy Trilemma of AI — Power, Water, Carbon in the Compute Age
- ⬜ Lesson 233: Frontier Models as Strategic Assets — What Happens When AGI Is National Property

---

*CEO — Prospectra Geopolitics & Investment Project*
*Session delivered: 2026-08-07 | Lesson 231 of extended curriculum | AI Infrastructure Arc, Lesson 3 of 5*
