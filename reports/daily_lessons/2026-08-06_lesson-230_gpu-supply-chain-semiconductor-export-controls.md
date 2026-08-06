# Lesson 230: The GPU Supply Chain — How Semiconductor Export Controls Actually Work and What They Miss
**Date:** 2026-08-06
**Session Type:** Daily Lesson
**Curriculum Position:** 230 of ongoing extended curriculum
**Series:** The AI Infrastructure Arc — Lesson 2 of 5

---

## CEO Note

Lesson 229 established the strategic logic of sovereign AI and the political economy of the data center buildout. We framed the GPU as the critical enabling technology — the thing that makes AI training possible at scale, and therefore the thing that every major government wants to control or acquire.

This lesson goes one layer deeper: into the mechanics of the export control regime that has become the central instrument of the US-China AI competition. How do semiconductor export controls actually work? What do they achieve? And critically — what do they miss? Because the gap between what the controls are supposed to do and what they actually accomplish is itself an investable signal.

---

## Opening Question

*It is October 2022. The Biden administration announces the most sweeping semiconductor export controls in US history — blocking the sale of advanced AI chips (specifically NVIDIA's A100 and H100 GPU series) to China. The stated goal: prevent China from using US-origin technology to build military AI systems, advance its nuclear program, or develop capabilities that could undermine American national security.*

*Four years later, China's largest AI labs are training frontier models within 6–8 months of US capability. Huawei is shipping 1.6 million domestically manufactured AI chips per year. A Chinese lab (DeepSeek) produced a frontier model that briefly collapsed NVIDIA's market cap by $600 billion when it demonstrated that world-class AI could be built with far less compute than previously assumed. And the Trump administration — after multiple rounds of escalation — ultimately negotiated a deal allowing H200 GPU exports to China with volume caps and tariffs.*

*The question is not whether export controls were a mistake. The question is: what did they accomplish, what did they fail to accomplish, and what does the gap between the two tell us about where the AI competition actually stands?*

---

## 1. The Architecture of Semiconductor Export Controls

Before evaluating their effectiveness, we need to understand the mechanism. Export controls on semiconductors are not a simple ban — they are a layered system of rules, thresholds, and enforcement mechanisms that operate across the entire global supply chain.

### The Legal Framework

US semiconductor export controls operate primarily through the **Export Administration Regulations (EAR)**, administered by the Department of Commerce's Bureau of Industry and Security (BIS). The key tools:

**The Entity List:** A list of foreign companies and individuals that cannot receive US-origin goods, software, or technology without a specific license (which is almost always denied for Chinese defense-adjacent entities). Adding a company to the Entity List effectively cuts it off from US semiconductor supply chains — not just chips, but also the software tools (EDA software like Cadence and Synopsys) needed to design chips.

**Performance Thresholds:** Rather than banning specific named chips, BIS defines thresholds based on chip performance metrics — specifically, total processing performance (TPP) measured in operations per second and memory bandwidth. Any chip exceeding the threshold requires an export license to ship to covered countries. This is designed to be technology-agnostic (future chips automatically fall under controls as capabilities increase), but it creates an obvious engineering challenge: what happens at the threshold?

**The Foreign Direct Product Rule (FDPR):** The most powerful extraterritorial tool. It states that if a product anywhere in the world was made using US technology (including US-origin semiconductor manufacturing equipment or software), the US claims jurisdiction over it. This is why TSMC — a Taiwanese company — cannot ship chips to Huawei without a US license: the photolithography machines and design software used to fabricate those chips are US-origin, triggering FDPR.

**Entity-Specific vs. Jurisdiction-Wide Controls:** Some controls target specific companies (Huawei, SMIC, certain military-affiliated AI labs). Others apply to entire countries — China, Russia, Iran, and others are in a higher scrutiny category for advanced technology exports.

### The Specific Technology Being Controlled

The controls target chips with high **compute density** (GPUs, AI accelerators) and the manufacturing technology needed to produce them at advanced nodes (sub-7nm process nodes, specifically the EUV lithography machines made by ASML, a Dutch company that has accepted controls under US pressure).

The October 2022 controls targeted:
- NVIDIA A100 and H100 GPUs (then the industry standard for AI training)
- AMD MI200 series
- Advanced computing chips exceeding ~4,800 TFLOPS BF16 performance
- Semiconductor manufacturing equipment for advanced node production
- EDA software essential for chip design

---

## 2. The H20 Saga: A Case Study in Policy Instability

NVIDIA's response to the October 2022 controls illustrates both the ingenuity and the limits of export control enforcement.

**The original workaround: the A800 and H800.** Within months of the October 2022 controls, NVIDIA released China-specific variants of its banned chips — the A800 (a downgraded A100) and H800 (a downgraded H100) — that fell just below the performance thresholds. These were not banned chips; they were chips redesigned to not be banned chips. This was entirely legal. The performance hit was meaningful (~20-30% reduced capability) but not fatal for most AI workloads.

**October 2023: BIS tightened the thresholds**, closing the loophole that had made the A800 and H800 compliant. Both chips were now covered. NVIDIA again responded with a China-specific product: the **H20**, engineered to fall under the new, tighter threshold. The H20 was a real chip — $10,000-15,000 per unit, sufficient for inference workloads and some training tasks — and generated **$4.6 billion in quarterly revenue** from China before it became the subject of the next control escalation.

**April 2025: The H20 license requirement.** The Commerce Department declared the H20 noncompliant and required export licenses (effectively a ban). NVIDIA took a $5.5B write-down on already-shipped inventory.

**July 2025: Reversal.** The Trump administration, facing industry lobbying and the argument that China would simply shift to Huawei alternatives, reversed course — export licenses for H20 were to be granted.

**December 2025 – January 2026: The H200 deal.** Trump announced that H200 GPUs (a step below the top-of-the-line Blackwell architecture) could be sold to China — with a **volume cap of approximately 1 million units** and a **25% tariff** on advanced AI chips meeting specific performance thresholds. This represented a partial retreat from the escalation trajectory: the US government acknowledging that total denial was not achievable, and negotiating terms rather than maintaining a prohibition that was being circumvented anyway.

**The policy lesson:** Export controls on specific products are vulnerable to threshold engineering, product substitution, and political reversal. The H20 saga is a four-year demonstration of the whack-a-mole dynamic between BIS and NVIDIA's product team.

---

## 3. What Export Controls Have Actually Achieved

Despite the whack-a-mole dynamic, the controls have had real effects — just not the ones that are easiest to see.

**What worked:**

**1. Imposed real compute costs on Chinese AI labs.** Chinese companies have been training on A800s, H800s, and H20s — which are meaningfully worse than H100s, H200s, and B200/B300 (Blackwell) chips for large-scale training runs. The performance gap at the very frontier of capability is real. DeepSeek V4 Pro was assessed at roughly **8 months behind the frontier** in May 2026. GLM-5.2 (Zhipu AI) was comparable to a US model released about 6 months earlier. The gap is closing — but it exists.

**2. Slowed China's ability to build the largest training clusters.** A single Blackwell B200 cluster at the frontier scale (100,000+ GPU training runs) is not currently achievable in China using domestic hardware. Huawei's Ascend 910C delivers approximately **one-third the BF16 throughput of NVIDIA's B200**. To match a 30,000 B200 cluster, China would need ~90,000 Ascend 910Cs — before accounting for interconnect efficiency losses that compound the gap. The cluster-scale training infrastructure that produced GPT-4, Claude 3, and Gemini Ultra is not yet replicable in China at the same scale.

**3. Forced a divergent architectural path.** Compute constraint has driven Chinese AI labs toward **efficiency-first architectures** — smaller models trained on better data, inference-time compute, distillation techniques. DeepSeek's Mixture of Experts (MoE) architecture activates only a fraction of model parameters per inference step, dramatically reducing compute requirements. This was not pure innovation — it was necessity. The export control regime forced an architectural divergence that may ultimately prove to be a strategic liability *or* a genuine innovation forcing mechanism (the jury is still out).

**4. Accelerated China's domestic chip development — at a cost.** The controls have made Huawei's Ascend series strategically essential for China's AI ambitions. This has driven massive investment: Huawei plans 1.6 million Ascend chip dies in 2026 (600,000 Ascend 910C + ramp in newer products). SMIC is manufacturing these at 7nm — technically possible, but manufacturing yield and cost efficiency remain well below TSMC's equivalent nodes.

**What has not worked:**

**1. Stopping chip acquisition through third countries.** The smuggling problem is severe. In 2024, a single ring bought **$390 million worth of servers containing banned NVIDIA GPUs**, shipping them through Malaysia. This is not an isolated case — it is the visible tip of a large-scale diversion operation. The Entity List covers specific buyers; it cannot prevent brokers, shell companies, and re-export schemes operating through Singapore, UAE, Southeast Asia, and other jurisdictions.

**2. Preventing domestic Chinese capability development.** The controls explicitly accelerated the build-out of China's domestic semiconductor industry. SMIC has advanced to 7nm. CXMT is scaling DRAM production. Yangtze Memory Technologies (YMTC) was expanding NAND flash before additional controls tightened access to US equipment. In 2025-2026, China's domestic share of its own AI chip market is projected to reach **50%** — driven partly by genuine technological progress and partly by government mandates requiring large tech firms to source domestically.

**3. Stopping Chinese AI progress.** The capability gap exists — but it is narrowing faster than the architects of the control regime expected. The export control framework was designed on the assumption that compute scale was the primary determinant of AI capability. DeepSeek's efficiency breakthrough challenged that assumption: a technically constrained team produced a frontier model for dramatically lower cost by rethinking architecture rather than scaling hardware.

---

## 4. China's Three-Pronged Response

China has not passively accepted the export control regime. It has mounted a systematic response across three dimensions:

**Dimension 1: Domestic substitution (Huawei, Cambricon, Biren, Enflame)**
The Ascend 910C is the flagship, but it is not alone. Cambricon produces AI inference chips used in edge devices. Biren Technology released a GPU-class chip (BR100) competitive with older-generation NVIDIA products. The ecosystem is nascent but accelerating. Government mandates requiring Alibaba, Tencent, Baidu, and ByteDance to procure domestically for at least a portion of their AI workloads have created a captive demand floor that justifies continued domestic investment even at current performance deficits.

**Dimension 2: Counter-controls on critical materials (China's chokepoint lever)**
China's most powerful retaliation tool is export controls on the materials needed to manufacture semiconductors. China controls **80%+ of global gallium** production, **60%+ of germanium**, and dominant shares of the rare earth elements essential for chip manufacturing and AI hardware. In June 2026, **zero shipments** of gallium, dysprosium, terbium, or yttrium left China to Japan — a direct signal of willingness to use critical mineral export controls as a retaliatory instrument. This is China's version of the FDPR: if the US can claim jurisdiction over anything that touched US technology, China can claim jurisdiction over anything that needs Chinese minerals.

**Dimension 3: Open-source and efficiency-first strategy**
China's leading AI labs have increasingly open-sourced their models (DeepSeek's R1 was released under an open-source license). This serves multiple strategic purposes: (1) it accelerates global adoption of Chinese AI architectures, building ecosystem lock-in; (2) it makes it harder to restrict Chinese AI capabilities through export controls (you can't export-control a GitHub repo); (3) it pressures US frontier model providers by commoditizing the inference layer. The US-China Commission's March 2026 report ("Two Loops") analyzed this as a deliberate strategy to reinforce China's industrial dominance through open-source diffusion.

---

## 5. Investment Implications

**NVIDIA: Volatile but Structurally Dominant**
The H200 volume cap deal (~1 million units annually) is a bearish constraint on what would otherwise be China demand, but it is better than the alternative of a complete prohibition. NVIDIA's Blackwell B200/B300 series faces no near-term competitive threat in the US, EU, Gulf, and allied markets. The domestically substituted Chinese market is a manageable loss. **Core bias: long NVIDIA on non-China sovereign and enterprise demand; size for regulatory volatility on China exposure.** The risk that matters most is not China — it is the efficiency-first architectural shift. If inference-time compute and efficient architectures permanently reduce the need for large training clusters, NVIDIA's data center TAM is structurally smaller than the current bull case implies.

**ASML: The Chokepoint Chokepoint**
ASML is the single most critical non-US company in the export control regime. Its EUV lithography machines are essential for sub-7nm chip manufacturing — no EUV, no advanced chips. The Netherlands government (under US pressure) has blocked ASML from shipping EUV machines to China since 2019. Without EUV, SMIC is manufacturing Huawei's Ascend chips using a clever workaround — multiple exposures with older Deep UV (DUV) machines, achieving 7nm-equivalent density at much lower yield and much higher cost. This is a genuine constraint on China's chip scaling. **Bias: long ASML as the structural chokepoint of the entire competition; its geopolitical exposure is a *feature* — it becomes more essential as both sides escalate.**

**Rare Earth and Critical Minerals (China's Retaliation Vector)**
China's June 2026 zero gallium/dysprosium/yttrium export to Japan is not a one-off signal — it is a demonstration of a standing coercive capability. Companies that use gallium in GaN (gallium nitride) power semiconductors — essential for data center power efficiency and EV charging — face supply chain vulnerability. **Bias: long companies with secured non-Chinese gallium sourcing (Vital Metals, Australian Strategic Materials) and companies providing gallium recycling/recovery technology.** Separately: the rare earth constraint is a secondary threat to NVIDIA's data center power supply infrastructure — a bearish tail risk that compounds the chip shortage scenario.

**AMD: The Structural Beneficiary of Diversification**
AMD's MI300X has gained market share as customers hedge Nvidia concentration. In China, AMD faces the same export controls as Nvidia. Outside China, AMD benefits from customers' desire to not be 100% Nvidia-dependent. **Bias: long AMD as a structural hedge on Nvidia concentration; the investment thesis is diversification demand, not AMD outpacing Nvidia on capability.**

**Domestic Chinese AI Hardware Ecosystem (Illiquid / High Risk)**
Cambricon (688256.SS) is the only publicly listed pure-play Chinese AI chip company. Valuation is stretched relative to current revenue; the investment case is a bet on domestic substitution mandate driving captive demand. **Bias: avoid at current valuations; monitor for structural pullback if domestic substitution pace disappoints government targets.** The more interesting exposure is through Chinese internet companies (Alibaba, Tencent, Baidu) that own domestically mandated AI hardware procurement as a cost burden — these companies are paying a domestic substitution premium that reduces near-term margins but arguably builds strategic resilience.

**Portfolio-Level Signal: The Regime Endgame**
The H200 volume cap deal reveals something important about the export control endgame: total denial is not sustainable. The US ultimately negotiated terms rather than maintained a prohibition — a pattern that suggests the final equilibrium is not "China cannot get advanced chips" but "China gets some advanced chips, at higher cost, with constraints." This is a meaningful difference. The investment implication: don't price in a permanent technology embargo. Price in a permanent technology cost advantage for US-based AI infrastructure relative to China — a sustained but not absolute gap.

---

## 6. Databricks Angle

**Dataset: BIS Entity List + Export License Decision Data**
The BIS maintains a public Entity List (downloadable CSV) updated regularly. Every addition to the Entity List is an event with investable implications: companies lose US chip supply, are forced to domestic substitution, and often face equity devaluation. Building an automated Entity List change detector — scraping BIS, parsing additions and removals, mapping to equity tickers — creates a leading indicator for Chinese semiconductor equity impact.

**Pipeline Idea: Export Control Regime Tracker**

Build a pipeline that monitors:
1. BIS Federal Register notices (RSS/scraping) for new entity additions, rule changes, and threshold modifications
2. NVIDIA/AMD SEC filings for China revenue disclosures (10-Q quarterly, geography breakdowns)
3. Chinese customs data (available through CEIC, Wind, and Refinitiv) for chip import volumes by country of origin
4. Huawei annual report disclosures for Ascend production and sales volumes

**Feature Engineering:**
- "Policy gap" metric: time between US control announcement and Chinese workaround emergence (measurable from product launch data)
- "Substitution velocity": rate at which Chinese AI chip market share shifts from US to domestic (quarterly)
- "Enforcement intensity index": entity additions per quarter as a proxy for BIS escalation posture
- Rare earth export control severity score: shipment data vs. prior quarter by mineral and destination country

**Investment Signal Application:**
- Spike in entity additions → leading indicator for Chinese tech equity selloff (1-4 week lag observable historically)
- Declining US chip imports to China + rising domestic chip shipments → signal for domestic Chinese semiconductor equity re-rating
- Zero gallium shipments to Japan (as in June 2026) → alert for GaN power semiconductor supply chain risk, trigger for rare earth commodity tracking

---

## 7. Reflection Questions

1. **The H200 volume cap deal allows China to import approximately 1 million H200 GPUs per year. Huawei is producing approximately 1.6 million Ascend chip dies per year — but at roughly 1/3 the performance of Blackwell B200. Doing the rough math: at what total chip volume does China's total AI compute capacity (US-sourced + domestic) become comparable to US domestic AI compute capacity? What assumptions does your calculation require, and which ones are most fragile?**

2. **China's critical mineral export controls (gallium, germanium, rare earths) represent the mirror image of US semiconductor export controls — using upstream material supply as a coercive instrument. The US semiconductor controls target China's *access to advanced technology*; China's mineral controls target the West's *access to manufacturing inputs*. Which is the more durable form of leverage? Which side is more exposed to substitution over a 5-year horizon?**

3. **DeepSeek's efficiency-first architecture was (partly) a response to compute constraint imposed by export controls. The US semiconductor export control regime was designed on the premise that more compute = more AI capability. If China's forced efficiency innovation produces architectures that are genuinely more efficient than US approaches — requiring less hardware to achieve equivalent capability — has the export control regime inadvertently advantaged China by forcing it to solve a problem that the US, with abundant compute, had no incentive to solve? How would you answer this as a long-horizon investor?**

---

## Questions for Next Session (Spaced Repetition)

- *From Lesson 229 (Sovereign AI):* The UAE and Saudi Arabia are building sovereign AI infrastructure with US chips and US hyperscaler partners. Given the H200 volume cap deal, does the Gulf now have *more* reliable access to advanced US chips than China? What does this reveal about the US strategic logic — is the chip control regime about denying China, or about binding the Gulf to US technology infrastructure?
- *From Lesson 221 (Critical Minerals):* Gallium is essential for GaN power semiconductors used in AI data center power delivery and EV charging. China exported zero gallium to Japan in June 2026. What is the 12-month investment thesis on companies with secured non-Chinese gallium supply?
- *From this lesson:* The BIS has tightened, loosened, and re-tightened chip controls in a 4-year cycle. Is the current H200 volume cap deal a stable equilibrium or a temporary detente before the next escalation? What events would trigger the next tightening?

---

## Series Position

**AI Infrastructure Arc Progress:**
- ✅ Lesson 229: Sovereign AI and the New Compute Geography
- ✅ Lesson 230: The GPU Supply Chain — How Semiconductor Export Controls Actually Work and What They Miss *(this lesson)*
- ⬜ Lesson 231: AI and the New Colonialism — How US Hyperscalers Are Locking In EM Markets
- ⬜ Lesson 232: The Energy Trilemma of AI — Power, Water, Carbon in the Compute Age
- ⬜ Lesson 233: Frontier Models as Strategic Assets — What Happens When AGI Is National Property

---

*CEO — Prospectra Geopolitics & Investment Project*
*Session delivered: 2026-08-06 | Lesson 230 of extended curriculum | AI Infrastructure Arc, Lesson 2 of 5*
