# Lesson 56 — Export Controls as Strategic Weapon: BIS, Entity Lists, and the Technology Denial Architecture

**Date:** May 19, 2026
**Session Type:** Daily Lesson
**Lesson Number:** 56 / Extended Curriculum
**Topic:** How Export Controls Became America's Sharpest Geopolitical Tool — and Why They May Be Cutting Both Ways

---

## Opening Question

*On October 7, 2022, the Biden administration published a set of export control regulations that one former NSC official called "the most aggressive unilateral export control action the United States has taken since the Cold War." The rules blocked China's access to the most advanced semiconductors, semiconductor manufacturing equipment, and the U.S. persons who design and operate them. The explicit goal: deny China the computational power needed to develop frontier AI, advanced weapons systems, and next-generation military electronics.*

*By October 2025 — three years later — Huawei had released the Ascend 910C, a domestically-designed AI chip that many analysts rated competitive with Nvidia's H100. China's semiconductor investment had reached record highs. The ITIF published a report titled "Backfire: Export Controls Helped Huawei and Hurt U.S. Firms." Nvidia had lost tens of billions in potential Chinese revenue. And the Trump administration had quietly reversed many of the restrictions — replacing prohibition with a 25 percent revenue tax paid to the U.S. Treasury.*

Here is the question: **When a nation-state uses export controls as a strategic weapon — not just to prevent proliferation, but to actively strangle a rival's technological development — what are the conditions under which it succeeds? And when does denial accelerate the very capability it is trying to prevent?**

Hold that question through this entire lesson. It is the most important diagnostic question in technology geopolitics today.

---

## I. The Architecture: How Export Controls Actually Work

Before understanding export controls as strategy, you need to understand the plumbing. It is not intuitive, and most commentary skips it entirely.

### The Bureau of Industry and Security (BIS)

Export controls in the U.S. are administered by the Bureau of Industry and Security, a division of the Department of Commerce. BIS administers the **Export Administration Regulations (EAR)** — a dense body of law governing what can be exported, to whom, under what conditions, and with what licenses.

BIS is not the State Department (which handles defense articles under ITAR — International Traffic in Arms Regulations). BIS handles *dual-use* items: commercial technology with potential military applications. This distinction matters enormously: in the semiconductor and AI era, virtually all advanced technology is dual-use.

### The Commerce Control List (CCL)

Every technology subject to export control gets an **Export Control Classification Number (ECCN)** — a five-character alphanumeric code that defines:
- What category the item is (1=materials, 3=electronics, 4=computers, 5=telecom/information security)
- What reasons for control apply (NS=national security, AT=anti-terrorism, EI=encryption)

Examples that matter for our analysis:
- **3A001**: Semiconductors and integrated circuits — the foundational chip category
- **3B001**: Semiconductor manufacturing equipment — the machines that make chips
- **4A090**: Advanced computing chips — the specific ECCN Nvidia's A100/H100 fall under
- **4E091**: AI model weights — *created in January 2025; the first time the EAR controlled trained AI models, not just hardware*

If a technology has an ECCN, it requires a **license** to export to certain destinations. For items in the most sensitive categories to "Country Group D:1" (which includes China), the license policy is typically **presumption of denial** — Treasury is unlikely to issue the license.

Items without an ECCN, or items not on the CCL, are classified "EAR99" — generally freely exportable. The history of the last decade in semiconductor controls is largely the story of BIS moving items from EAR99 (or low-restriction ECCNs) onto the CCL with tighter controls.

### The Entity List

The Entity List is BIS's most powerful blunt instrument. It is a list of foreign persons, companies, and organizations to which **all items subject to the EAR** require a license — with a **presumption of denial**. Getting on the Entity List is, for a technology company, approximately equivalent to being cut off from the global technology supply chain.

**The Entity List is not a sanction.** It is an export control tool. The distinction matters: being on the Entity List doesn't freeze your assets, prohibit U.S. persons from working with you in non-export contexts, or prevent you from selling your own products. But it means no U.S.-origin technology — hardware, software, or (critically, as we'll see) foreign-made products that used U.S. technology in their production — can reach you without a license that won't be issued.

As of May 2026, the Entity List contains over **600 Chinese entities**, including Huawei, SMIC, CXMT, YMTC, dozens of AI companies, defense contractors, surveillance technology firms, and university research labs with PLA connections.

Key additions by year:
- **May 2019**: Huawei + 68 non-U.S. affiliates — the watershed moment
- **November 2020**: SMIC (China's largest foundry)
- **October 2022**: 31 companies in the initial October 7 rules; expanded significantly through 2023
- **December 2024**: 140 PRC entities added in a single action
- **March 2025**: 42 additional PRC entities
- **September 2025**: 23 more

---

## II. The Foreign Direct Product Rule — America's Extraterritorial Reach

This is the mechanism that makes U.S. export controls globally binding — and it is the most legally contested, geopolitically consequential aspect of the entire system.

### The Basic Logic

The **Foreign Direct Product Rule (FDPR)** says: if a foreign-made product was produced using U.S. technology, U.S. software, or U.S. equipment, that product is subject to U.S. export controls — even if it was designed and manufactured entirely outside the United States and by a non-U.S. company.

In other words: if ASML builds an EUV lithography machine in the Netherlands using components that incorporate U.S.-origin technology, that machine is subject to the EAR. ASML cannot sell that machine to an Entity-Listed Chinese company without a U.S. license — even though ASML is Dutch, the machine is Dutch, and the buyer is Chinese.

The FDPR was first used against Huawei in **August 2020** — an audacious step. At a stroke, it meant that TSMC (Taiwan), Samsung (South Korea), and virtually every other advanced chip foundry in the world could no longer produce chips *for Huawei* using their standard process equipment — because that equipment was built with U.S. technology.

The result was decisive: Huawei's smartphone division, which had been selling more phones than Samsung, was effectively cut off from TSMC's 5nm and 7nm processes. Its Kirin chipline — one of the world's most advanced mobile SoC series — was frozen. Huawei's smartphone market share collapsed from ~20% globally (Q1 2020) to single digits.

### The October 2022 Expansion

In October 2022, the FDPR was expanded dramatically:
- Applied not just to companies on the Entity List but to **all transactions** involving advanced chips (above defined performance thresholds) and semiconductor manufacturing equipment destined for China
- Extended to cover chips manufactured using U.S. equipment anywhere in the world, for any customer in China
- Added a **U.S. persons rule**: U.S. citizens and permanent residents working at Chinese semiconductor companies must stop providing support, even if they are in China working for a Chinese employer

The U.S. persons rule forced an exodus of American engineers from CXMT, SMIC, and other Chinese chip operations. Many of China's most advanced fab processes were being sustained by U.S. and Taiwan-trained engineers. Overnight, they had to leave or face liability.

**The FDPR's extraterritorial reach extends to:** ASML (Netherlands), Tokyo Electron (Japan), Lam Research (U.S., but it also binds its Japanese and European subsidiaries), KLA Corporation, Applied Materials, and effectively every company in the global semiconductor equipment industry — because every major equipment vendor uses U.S.-origin technology somewhere in its products.

This is the core of U.S. leverage: it does not need to control the entire supply chain directly. It needs only to control the *critical nodes* — design software (EDA tools from Cadence, Synopsys, Mentor), and manufacturing equipment — from which it can reach out and bind the entire global supply chain.

---

## III. The October 7, 2022 Watershed — What Actually Changed

The October 7, 2022 rules were not incremental. They represented a strategic doctrine shift: from export controls as a **proliferation prevention tool** (don't let adversaries get weapons-specific technology) to export controls as a **capability denial tool** (prevent the adversary from developing the technological foundation for military and economic power).

**What the rules did:**

| Action | Effect |
|---|---|
| Performance threshold: chips above 300 TFLOPS BF16 or 600 GFLOPS INT8 required license | Blocked all A100, H100, and equivalent chips from China |
| Expanded FDPR to semiconductor manufacturing equipment | ASML, TEL, AMAT, LAM, KLA cannot ship advanced tools to Chinese fabs |
| U.S. persons restriction | U.S. engineers must exit roles at Chinese advanced semiconductor companies |
| Added 31 entities to Entity List | Targeted advanced memory (YMTC), AI chips (Biren), and others |
| Controls on EDA software | Blocked Chinese chip designers from using Synopsys, Cadence tools for certain designs |

**The doctrine shift in plain language:** The October 2022 rules said, for the first time explicitly, that the goal is not to prevent China from obtaining specific weapons. The goal is to prevent China from *maintaining or advancing its position* in the foundational technologies underlying AI and advanced military systems. This is a profound escalation: you are not controlling arms, you are controlling the *foundation of future economic and military power*.

Former Commerce Under Secretary Alan Estevez described it as: "We want to maintain as large a lead as possible" in advanced computing. This is capability *maintenance* — not just proliferation prevention.

---

## IV. The Nvidia-China Revenue Problem: A Case Study in Policy Volatility (2022–2026)

No single story illustrates the complexity of export controls as strategic tools better than Nvidia's relationship with China over the past four years.

### Phase 1: The A100/H100 Block (October 2022)

When BIS published the October 2022 rules, Nvidia's A100 and H100 data center GPUs — its highest-margin products — were immediately restricted from sale to Chinese data centers. China had been roughly 20-25% of Nvidia's data center revenue. The company needed to respond.

**Nvidia's response:** Design downgraded chips that comply with the performance thresholds.

### Phase 2: The A800/H800 "Workaround" Chips (2023)

Nvidia released the A800 and H800 — versions of the A100/H100 with chip-to-chip interconnect bandwidth artificially reduced to fall below the BIS threshold. They had roughly the same compute performance as the restricted chips; only the interconnect was degraded.

BIS's reaction in **October 2023**: added the A800/H800 to the restricted list and lowered the performance threshold further. The cat-and-mouse game was explicit.

### Phase 3: The H20 — Designed for China, Restricted Anyway (2024–2025)

Nvidia designed the **H20** specifically for the Chinese market after the October 2023 action. The H20 was genuinely downgraded — roughly 15% of the compute performance of the H100. Chinese customers bought enormous volumes: ByteDance, Alibaba, Tencent, and Baidu placed massive orders. Nvidia reported that H20 demand from China was a multi-billion dollar business.

**April 2025**: The Trump administration — in a surprise escalation — added the H20 to the restricted list, citing concerns that even this downgraded chip, clustered in large numbers, could enable AI capabilities with national security implications.

The action forced Nvidia to book a **$5.5 billion inventory charge** — already-manufactured H20 chips that could no longer be shipped.

### Phase 4: The Revenue-Sharing Reversal (July–August 2025)

**July 2025**: Within three months, the Trump administration reversed the H20 restriction. The public rationale cited concerns about Chinese companies pivoting to Huawei Ascend chips and the U.S. ceding market share with no security benefit.

**August 2025**: The reversal came with an extraordinary condition — Nvidia would be granted export licenses for H20 sales to China in exchange for paying **15 percent of revenues** from those sales to the U.S. government.

**December 2025 / January 14, 2026**: The arrangement was extended and formalized. The Trump administration issued a Proclamation imposing a **25 percent "chip tax"** on revenues from advanced chip sales to China — applying to Nvidia (H200), AMD (MI308), and Intel. The January 14, 2026 proclamation formally established this as a revenue-sharing arrangement between chipmakers and the Treasury.

**The policy novelty is significant:** This is not a tariff on imports. It is not a sanction. It is a revenue-sharing arrangement — the U.S. government essentially becoming a 25% partner in American companies' China chip revenue. The legal authority is contested (Lawfare published an extensive analysis questioning whether the president has statutory authority for this specific mechanism). But as of May 2026, it is operative policy.

### The Scoreboard (as of May 2026)

| Metric | Outcome |
|---|---|
| Nvidia China revenue | Partially restored — H20 banned, then unbanned with 25% tax; H200 now available to China with 25% revenue share |
| Huawei Ascend 910C | Released; competitive with H100 in some benchmarks; SMIC-manufactured at 7nm (possibly 5nm) |
| Chinese AI compute capacity | Significantly constrained vs. potential, but growing rapidly via Huawei and domestic alternatives |
| U.S. chipmaker revenues | Nvidia lost ~$5.5B in H20 inventory write-down; long-term China exposure reduced and taxed |
| SMIC technical capability | Evidence of 7nm production; behind TSMC/Samsung, but closing gap faster than 2022 projections |

---

## V. The Huawei Arc: Did the Entity List Backfire?

The Huawei story is the most important long-run test case for whether technology denial through export controls can achieve its strategic objective.

### The Initial Result: Decisive

When Huawei was added to the Entity List in May 2019 and the FDPR was applied in August 2020, the effect was immediate and dramatic:
- TSMC stopped producing Huawei's Kirin chips
- Huawei's smartphone division lost access to advanced chip supply
- Google Services were removed from Huawei Android phones (separate action — Google had to comply because Huawei was on the Entity List)
- Huawei's global smartphone market share collapsed

For roughly two years (2020-2022), the controls appeared to have successfully degraded Huawei's smartphone business and its path to 5G dominance in consumer devices.

### The Adaptation: Unexpected Speed

**September 2023**: Huawei released the Mate 60 Pro — a smartphone with a domestically-manufactured 7nm chip (the Kirin 9000S, produced by SMIC). The chip used "deep ultraviolet" (DUV) lithography rather than EUV. DUV is older technology that ASML still ships to China. It is less efficient and more expensive than EUV, but it works. China's investment in 7nm via DUV demonstrated that the path to advanced chips is slower without EUV — but it exists.

**2024-2025**: Huawei released the Ascend 910B, 910C, and 910D AI accelerator chips. The 910C, benchmarked in early 2026, performed comparably to Nvidia's H100 in some AI inference tasks. In **May 2025**, BIS issued formal guidance warning that any use of Huawei Ascend 910B/C/D chips "risks violating U.S. export controls" — an acknowledgment that the chips were produced using processes that may have involved controlled technology, and that anyone using them globally could face BIS liability.

### The ITIF Assessment (October 2025)

The Information Technology and Innovation Foundation — a U.S. think tank with a generally pro-industry, skeptical view of overreach — published **"Backfire: Export Controls Helped Huawei and Hurt U.S. Firms"** in October 2025.

Key findings:
- Huawei's R&D intensity averaged **20% of revenue** from 2019-2023 — outpacing all competitors except Intel
- Huawei launched **Hubble Technology Investment**, a VC subsidiary with >$100M registered capital, to fund domestic semiconductor startups — accelerating the domestic chip ecosystem
- Controls forced Huawei to develop capabilities it would otherwise have simply purchased
- U.S. firms (Qualcomm, Intel, Broadcom, Qorvo) collectively lost billions in annual Chinese revenue with limited substitution
- Huawei's 5G infrastructure business — the original target of the Entity List action — remained largely intact, as 5G base stations don't require the same advanced chips as consumer devices

The honest assessment: **The Entity List action was partially successful as a near-term supply shock, but partially backfired as a long-run capability denial tool.** Huawei's smartphone business was damaged; its network infrastructure and AI chip ambitions were not stopped — and may have been accelerated by forcing domestic investment.

---

## VI. The AI Diffusion Framework and Model Weight Controls (2025)

The most novel export control development of the past three years is the extension of controls beyond *hardware* to *trained AI models themselves*.

### ECCN 4E091 — The First Control on AI Model Weights

In **January 2025**, BIS published the "Framework for Artificial Intelligence Diffusion" and created **ECCN 4E091**: a new export control classification that applies to the *weights* of large AI models — the billions of parameters that encode a trained model's capabilities.

This is unprecedented. For the entire history of export controls, controls applied to physical goods, hardware, or code that *enables* certain functions. Model weights are fundamentally different: they are data — the output of a computational process — that encode capability. The notion that a set of floating-point numbers can be an export-controlled item is conceptually novel and legally contested.

The controls under 4E091 apply to model weights with capabilities above certain thresholds — currently tied to training compute (FLOPS) and performance benchmarks on certain dual-use tasks. The practical effect: major U.S. AI labs (OpenAI, Google DeepMind, Anthropic, Meta) cannot distribute their most powerful model weights to parties in China or other controlled countries without a license.

### The Three-Tier AI Diffusion System

The AI Diffusion Framework organized the world into three tiers for AI chip and model export purposes:

**Tier 1 (18 trusted allies):** U.S., UK, Australia, Japan, South Korea, Netherlands, and others. Unrestricted access to advanced AI chips and model weights. These are countries with equivalent security controls and aligned foreign policy.

**Tier 2 (~120 countries):** Access allowed but with quantitative caps on advanced AI chip imports per entity, and requirements for AI security commitments (data protection, access controls, non-diversion guarantees). Can receive model weights if they adopt equivalent security standards.

**Tier 3 (China, Russia, and arms-embargoed countries):** Presumption of denial for advanced AI chips and model weights. The full controls apply.

### The Trump Modification (January 2026)

**January 13, 2026**: BIS issued a final rule modifying the AI Diffusion Framework — replacing the Biden-era "presumption of denial" for Tier 3 countries with a **case-by-case review standard** for certain chip exports. This softened the framework's hardest edges, consistent with the broader Trump shift toward revenue-extraction over prohibition.

The core controls — the Entity List, the FDPR, the fundamental chip performance thresholds — remained intact. What changed was the licensing posture for items at the margin of the threshold.

---

## VII. China's Counter-Architecture: Rare Earths and the Symmetric Response

What happens when the target of technology denial controls has its own leverage? China's October 2025 move is the answer.

### The Rare Earth Counterpunch

**October 9, 2025**: China tightened its rare-earth export rules to require case-by-case government review for exports of semiconductor and AI-critical materials, covering:
- Chips at 14nm-and-below logic (the advanced node range)
- 256-layer-and-above memory
- Related manufacturing equipment
- AI systems with potential military use

The explicit target: ASML, which holds a de facto monopoly on EUV lithography but depends on **Chinese-origin rare earths** for critical components — particularly dysprosium and terbium for the powerful electromagnets in EUV systems. ASML acknowledged the rules could create delays of "several weeks" in shipments.

This is the symmetric response to the FDPR: the U.S. used technological dominance in chip design and equipment (EDA software, deposition tools, photolithography) to bind the global supply chain. China is using materials dominance (rare earth processing — China controls ~85% of global rare earth refining) to bind the same supply chain from the other direction.

### The Dual Chokepoint Emerging

We are witnessing the emergence of a **dual-chokepoint world** in advanced manufacturing:

| U.S. Chokepoint | Chinese Chokepoint |
|---|---|
| EDA software (Cadence, Synopsys) | Rare earth elements (60-85% global processing) |
| Advanced semiconductor equipment (AMAT, Lam, KLA) | Gallium and germanium (>80% of global supply) |
| Advanced chips (Nvidia, AMD, Intel) | Magnet materials for motors/EV/defense |
| Cloud infrastructure (hyperscalers) | Critical battery minerals (lithium, cobalt refining) |
| AI model development (OpenAI, Anthropic) | Rare earth processing for EUV/defense systems |

Neither side can strangle the other completely — but both sides can impose meaningful costs. This is the structural endgame of technological decoupling: two partially-overlapping chokepoints, each with the ability to disrupt the other's supply chains, but neither with the ability to end the contest.

---

## VIII. Investment Implications — Navigating the Technology Denial Landscape

### The Equipment Company Paradox

Semiconductor equipment companies (AMAT, Lam, KLA, Teradyne, Tokyo Electron, ASML) face a paradox:
- Export controls reduce their addressable market in China (loss of revenue in near term)
- China's domestic investment response *creates demand* for the equipment they're allowed to sell (DUV machines, older-node equipment)
- The FDPR means their products are strategic tools, giving them regulatory moat against non-U.S. competitors
- But Chinese rare-earth countermeasures create input supply risk for ASML specifically

**Directional view:** Constructive on U.S. equipment companies with limited China exposure (KLA, Teradyne); cautious on ASML until rare-earth supply risk is resolved; constructive on Japanese equipment (Tokyo Electron, Advantest) as they benefit from allied-country carve-outs.

### The Chip Company Revenue Tax Trade

The Trump 25% chip revenue tax changes the investment calculus for Nvidia and AMD in China:
- Before: binary — either you can sell, or you can't
- Now: you can sell, but 25% goes to Treasury
- Nvidia's gross margins on data center products run ~70%+. A 25% revenue haircut is material but doesn't eliminate profitability
- **The real risk:** policy reversal. If a future administration re-prohibits sales (as happened in April 2025 with H20), the revenue disappears entirely. China exposure is now a political risk, not just a regulatory one.

**Directional view:** Nvidia and AMD are long-term structural buys on AI infrastructure demand; China revenue should be modeled as *optionally available with 25% haircut*, not as a reliable line item. The variance in that line is political, not commercial.

### The Chinese Domestic Chip Ecosystem

Huawei Ascend's progress and SMIC's 7nm capability mean the Chinese domestic semiconductor ecosystem is further along than the October 2022 restrictions anticipated. Investable plays for non-U.S. investors:
- **SMIC (0981.HK)**: China's leading foundry; beneficiary of massive domestic capex investment; Western-listed version carries U.S. Entity List risk (could affect custodians, clearing)
- **Cambricon Technologies**: Chinese AI chip designer; less prominent than Huawei's Ascend but in the same ecosystem
- **Semiconductor Materials/Equipment (Chinese)**: NAURA Technology, Kingsemi — receive enormous state subsidy; structurally overvalued relative to global peers but strategically important

**For U.S. investors**: These are *restricted* or practically inaccessible. For non-U.S. institutional investors (GCC SWFs, ASEAN funds, European EM funds without U.S. LP exposure), they represent high-risk, government-backstopped plays.

### The Allied Divergence Opportunity

Japan, the Netherlands, and South Korea have *aligned* their export controls with the U.S. — but they have not adopted the COINS Act framework for outbound investment controls. This creates:
- Japanese equipment companies (TEL, Advantest, Lasertec) that face the same China restrictions as their U.S. peers but whose home-country investors face no outbound investment restrictions
- ASML: Dutch; subject to export licensing aligned with the U.S.; European institutional investors can hold it freely without COINS Act concern

**Directional view:** Non-U.S. allied-country semiconductor equipment companies are among the best expressions of the technology decoupling thesis — they benefit from the strategic dynamic without the full U.S. regulatory overlay on their investor base.

### The Model Weight Controls Frontier

The extension of export controls to AI model weights (ECCN 4E091) creates a new investment signal:
- **AI safety compliance infrastructure**: Companies that can help U.S. AI labs demonstrate compliance with diffusion framework requirements (access controls, monitoring, audit trails) will see demand
- **Tier 2 country AI infrastructure**: Countries in the unrestricted-access tier (India, UAE, Saudi Arabia, Indonesia) are actively building AI infrastructure with full U.S. chip access — a structural advantage vs. China-tier countries
- **The "allied AI" premium**: AI infrastructure built in Tier 1 countries (Japan, South Korea, UK, Australia) using U.S. chips and model weights without restriction creates a geopolitical trust premium

---

## IX. Databricks Angle

**Export control enforcement creates measurable signals accessible via public data.**

BIS publishes enforcement actions, Entity List additions, and Federal Register rule updates. The temporal relationship between these publications and equity price movements is an underutilized signal.

**Pipeline: Export Control Signal Engine**

| Component | Data Source | Signal |
|---|---|---|
| Entity List additions | BIS official RSS + Federal Register scraping | Near-term: negative for affected company's Western partners; positive for their domestic competitors |
| FDPR rule changes | Federal Register ECCN/CCL amendments | Identify which foreign equipment companies face new restrictions on China sales |
| Nvidia/AMD China revenue disclosures | SEC 10-Q earnings filings | Track China revenue as % of total; quantify political risk exposure |
| BIS Chip Tax proclamation tracking | White House Executive Orders, Federal Register | New product categories facing the 25% revenue-sharing arrangement — forward indicator of which chipmakers face margin compression |
| China rare-earth export restriction announcements | MOFCOM press releases, GDELT event codes ECON_NATRES | Leading indicator of input supply risk for ASML, rare-earth dependent manufacturers |
| Huawei Ascend benchmark publications | Technical paper scraping (arXiv, Chinese Academy preprints) | Proxy for progress of Chinese domestic chip capability — trades against Nvidia/AMD China market share assumptions |

**Feature engineering ideas:**
- **"Technology Denial Index" by sector**: composite of Entity List additions, ECCN tightening, and licensing denial rates — measure of how restricted a given technology sector is
- **"Domestic Substitution Acceleration Score"**: rate of Chinese domestic patent filings, benchmark publications, and investment announcements in restricted sectors — leading indicator of when U.S. export controls stop working
- **"Allied Control Alignment Score"**: tracks whether Japan, Netherlands, South Korea are moving their controls in sync with the U.S. or diverging — signal for whether the FDPR extraterritorial reach is being undermined

---

## Key Concepts Covered

- The BIS/EAR architecture: ECCN classifications, Export Control Reform Act (ECRA), Entity List mechanics
- The Foreign Direct Product Rule (FDPR): extraterritorial reach — why Dutch and Japanese companies are bound by U.S. export controls
- October 7, 2022: the doctrine shift from proliferation prevention to capability denial
- The Nvidia-China revenue saga (2022–2026): A100 block → A800/H800 workaround → H20 restriction → revenue-sharing "chip tax"
- The Huawei arc: Entity List (2019) → Mate 60 Pro / Kirin 9000S (2023) → Ascend 910C (2025) — the limits of technology denial
- AI Diffusion Framework (January 2025): ECCN 4E091 for model weights; three-tier country system
- China's rare-earth counterpunch (October 2025): the symmetric response to the FDPR
- The dual-chokepoint world: U.S. equipment/software dominance vs. Chinese materials dominance
- Investment implications: equipment company paradox, chip revenue tax trade, allied divergence opportunity

---

## Investment Implications Summary

| Asset Class | Directional View | Reasoning |
|---|---|---|
| U.S. semiconductor equipment (KLA, Lam, AMAT) | Constructive; monitor China % | Entity List/FDPR moat; China domestic investment creates legacy-node demand; watch political risk |
| ASML | Cautious near-term | Rare-earth countermeasure creates input supply risk; EUV China ban already priced; watch rare-earth resolution |
| Nvidia / AMD | Long structural; China = political option, not base case | 25% chip tax reduces China margin; model China revenue as high-variance, not reliable; AI infrastructure demand secular |
| Huawei suppliers / SMIC | Inaccessible to U.S. investors; monitor as leading indicator | State-backed; structurally important; Ascend progress is the single most important signal for whether U.S. controls achieved their goal |
| Japanese semiconductor equipment (TEL, Advantest) | Constructive | Allied-aligned on exports; no COINS Act outbound restriction on their investor base; beneficiary of allied-country carve-outs |
| AI safety / compliance infrastructure | Emerging opportunity | AI Diffusion Framework creates compliance demand; Tier 2 country AI infrastructure build-out creates new demand |
| Chinese rare-earth/materials processors | Non-investable for U.S. institutions; monitor | Their export restriction power is the key geopolitical risk to model; watch MOFCOM announcements |

---

## Questions for Next Session

1. **The domestic substitution timeline**: The most important question in technology geopolitics is how long it takes China to domestically replicate each layer of the U.S. semiconductor stack. For EUV lithography — the genuine chokepoint — serious analysis suggests 10-15+ years. For chip design and EDA software, the timeline is shorter. For AI model training at frontier scale, it depends on compute access. Map the technology stack layer by layer: which controls are durable and which are time-limited? How should portfolio positioning shift as each layer becomes substitutable?

2. **The revenue-sharing precedent**: The Trump administration's 25% chip revenue tax is extraordinary — it essentially makes the U.S. government a financial partner in private companies' China sales. What is the legal authority? What happens if a future administration raises the rate to 50%? Is this model (revenue extraction over prohibition) more or less effective as a strategic tool than outright restriction? And what does it mean for the WTO framework on technology export controls?

3. **The FDPR allied-country problem**: The FDPR is the mechanism that makes U.S. controls extraterritorial. But the Netherlands (for ASML) and Japan (for TEL, Advantest, Shinko) have been increasingly willing to implement their own aligned restrictions voluntarily — to avoid being seen as circumvention routes. How does this "FDPR shadow" affect the competitive dynamics of allied semiconductor equipment companies vs. their U.S. counterparts? Does alignment on controls eventually merge into a unified allied technology bloc — and if so, what happens to companies in non-allied countries like South Korea or Taiwan when their geopolitical alignment is genuinely contested?

---

## Spaced Repetition Hook

This lesson completes the **three-pillar architecture of U.S. financial and technology coercion:**

| Lesson | Pillar | Tool | Target |
|---|---|---|---|
| **54** | Inbound control | CFIUS / FDI screening | Who can buy U.S. assets |
| **55** | Outbound control | OISP / COINS Act | Where U.S. capital can invest |
| **56** | Technology denial | BIS / Entity List / FDPR | What technology can leave the U.S. — and what foreign products using U.S. technology can reach adversaries |

Together, these three lessons describe a complete **economic siege architecture**: nothing strategically important can enter the U.S. uninspected; American capital cannot fund the adversary's development; and American technology — wherever it appears in the global supply chain — can be used to deny the adversary access to frontier capability.

China's counter-architecture is equally three-pillared: rare-earth and materials controls (counter to the FDPR); domestic technology development (counter to Entity List and chip bans); and alternative capital networks (Gulf SWFs, BRICS finance — counter to CFIUS and COINS Act). The strategic competition is now, explicitly, about who controls the chokepoints in the global technology and capital supply chains.

Also connect to **Lesson 10 (Technology and Semiconductor Geopolitics)**, **Lesson 29 (BRICS and De-Dollarization)**, **Lesson 45 (Taiwan: The $10 Trillion Chokepoint)**, and **Lesson 53 (Capital Markets Access as a Geopolitical Weapon)**.

---

*CEO — Prospectra Geopolitics & Investment Project*
*Lesson 56 of Extended Curriculum | May 19, 2026*
