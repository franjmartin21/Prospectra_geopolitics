# Lesson 328 — The Distribution Protocol: Getting Signals in Front of Institutional Readers

**Date:** 2026-09-13
**Session Type:** Daily Lesson
**Lesson Number:** 328 / ongoing
**Topic:** The Distribution Protocol — From Published Signal to Institutional Subscriber
**Curriculum Arc:** Live Operations Module — Lesson 13: The Outreach Engine

---

## Opening Question

*You've published Signal #2. The write-up follows the six-section structure from Lesson 327 to the letter. The thesis is precise, the evidence bullets cite specific GDELT queries, the falsification condition is named, and the track record table is live. The post is institutional-grade by every internal standard.*

**"It receives 40 views and zero paid conversions. The analysis is correct. The product is real. Nobody institutional has seen it. What do you do differently for Signal #3 — and why does the answer have almost nothing to do with the quality of the analysis?"**

The failure mode here is one of the most common in systematic research: treating publication as distribution. Publishing on Substack is not distribution. It is existence. A post that exists but is unread by the specific people who could become paid subscribers has no commercial value. A track record that accumulates in a database that no institutional reader has been directed to does not compound. The write-up protocol from Lesson 327 solved the last-mile translation problem. This lesson solves the prior problem: who reads it, and how do they find it?

The answer requires a distribution protocol that is as systematic as the analytical process — not spray-and-pray social posting, but a structured outreach engine matched to the specific institutional profile of Prospectra's target subscriber.

---

## I. Who You Are Actually Targeting

The first step in distribution is precision on the target. "Institutional readers" is not specific enough to build an outreach protocol.

Prospectra's specific target is a small, well-defined set of institutional roles:

**Target Profile A — The Macro PM at a Multi-Strategy Hedge Fund**
- Role: manages a discretionary macro or EM book, 1–5 PMs per fund
- Pain: drowns in macro commentary; starved for systematic, falsifiable geopolitical signals
- Decision criteria: signal legibility, track record format, methodology reproducibility
- Budget authority: $5,000–$50,000/year for specialized research; can approve independently or with one layer of approval
- Where they can be found: LinkedIn (job title search), hedge fund websites (partner bios), macro research conference attendee lists

**Target Profile B — The EM Allocator at a Family Office or Endowment**
- Role: allocates to EM equities, currencies, and sovereign debt across 10–30 countries
- Pain: geopolitical risk is the largest unquantified risk in their book; they have no systematic framework for it
- Decision criteria: country coverage, signal frequency, compatibility with existing risk systems
- Budget authority: research budget of $20,000–$100,000/year; decision typically at CIO level with one recommendation
- Where they can be found: allocator networks (CAIA, ILPA directories), LP databases (PitchBook, eFront), endowment investment committee meeting minutes (public for university endowments)

**Target Profile C — The Quant Analyst at a Systematic Fund**
- Role: builds factor models and event-driven signals; evaluates external data and research products for signal value
- Pain: geopolitical data is hard to systematize; most products are qualitative and can't be backtested
- Decision criteria: data reproducibility, API/integration availability, methodology documentation, backtested evidence of signal value
- Budget authority: data budget approval typically requires showing positive backtested Sharpe improvement; $10,000–$100,000/year
- Where they can be found: AlphaSignal, Quant Research Alliance forums, "alternative data" conference attendee lists

**The mistake to avoid:** spending any outreach energy on Profile D — the general-audience macro curious reader. This person reads Morning Brew, follows macro Twitter, and might pay $20/month for a newsletter. They are not the target. Acquiring 1,000 Profile D subscribers at $20/month ($240K ARR at maturity, 18 months away) is strictly worse than acquiring 20 Profile A/B/C subscribers at $500/month ($120K ARR, but achievable in 6 months and expanding to $600K at 100 subscribers). Optimize the outreach engine for the right target from Signal #1.

---

## II. The Outreach Engine — Structure

The distribution protocol runs on a fixed weekly cadence, parallel to the analytical process. It is not a burst campaign at launch and then silence — it is a weekly machine that adds new contacts and activates existing ones every cycle.

### Component 1 — The Contact List (built continuously)

Maintain a spreadsheet (or Databricks table) with the following schema:

| Field | Description |
|---|---|
| contact_id | UUID |
| name | Full name |
| role | Job title |
| firm | Firm name |
| profile | A / B / C |
| source | Where found (LinkedIn, conference, referral) |
| outreach_date | Date of first contact |
| follow_up_date | Scheduled follow-up |
| status | Cold / Warm / Trial / Paid |
| notes | Any response, context, or referral relationship |

**Weekly target:** Add 10–15 new contacts per week. At this rate, the list reaches 200 contacts by Signal #15, which is the minimum viable list size for meaningful conversion data.

**Where to find contacts:** LinkedIn job title search ("macro PM" + "EM" + hedge fund); conference attendee lists (Emerging Markets Investors Alliance, Global Fixed Income Institute, Bloomberg Buy-Side Forum); LP directories (NACUBO for endowments); referrals from existing warm contacts (the highest conversion path).

### Component 2 — The Cold Outreach Sequence

Every cold contact receives a four-message sequence over 6 weeks, sent via email or LinkedIn depending on accessibility. The sequence is short and structured — not a newsletter pitch.

**Message 1 (Signal #N week — Day 0):**
Subject: `Prospectra | Geopolitical Signal: [Country] — [Direction] | Signal #N`

> [Name],
>
> I run Prospectra Geopolitics & Investment, a systematic research product that translates geopolitical risk into directional investment signals with explicit falsification conditions. Our methodology uses GDELT event data combined with asset pricing analysis to identify countries where geopolitical risk is not yet priced into FX, sovereign debt, or equity markets.
>
> Signal #[N] published this week: [Country] | [Direction] | [90-day horizon]. The full post is [link]. The track record (N=[count]) is included.
>
> Given your focus on [EM / macro / systematic], I thought this approach might be relevant. Happy to share the methodology overview if useful.
>
> — [Name], CEO, Prospectra Geopolitics & Investment

Three rules for this message: (1) Subject line is identical in format to the signal post headline — it demonstrates the product's format discipline from the first contact. (2) The body names the specific signal published this week — not a generic pitch, a live data point. (3) No ask. No "would you like to subscribe." Just a signal and an offer of the methodology.

**Message 2 (3 weeks later — Day 21):**
> [Name],
>
> Following up briefly. Signal #[N] from three weeks ago [outcome update if any — "TRY has moved 6% in the direction of our thesis in the first 21 days"]. Signal #[N+1] published this week: [Country] | [Direction] | [link].
>
> Track record is now N=[count] signals, [X open, Y closed]. Would be happy to share a one-page methodology overview if that would be useful.

This message adds a live update on the prior signal. An institutional reader who ignored Message 1 will respond to a message that says "I told you Turkey would decline and it's already moved 6% in 21 days." The signal's performance is the follow-up content.

**Message 3 (Signal #N+2 week — Day 42):**
Short. Two sentences.
> [Name], adding Signal #[N+2] this week: [Country] | [Direction]. Track record at [link]. Worth a conversation if there's interest.

**Message 4 (Day 56 — Final):**
> [Name], last note on this. Our track record is now [count] signals over [X weeks]. Full scoring at [link]. Open to a conversation if this is ever useful for your process. I'll stop clobbering your inbox.

Message 4 closes the cold sequence. If there is no response after four contacts, the lead is marked "No Response" and deprioritized — not deleted. A no-response at Signal #5 may respond at Signal #26 when the track record has mass. Every contact stays in the database.

### Component 3 — The Warm Activation Protocol

A "warm" contact is someone who has responded to the cold sequence (even to say no), attended the same conference, been referred by an existing subscriber, or engaged with a Prospectra post. Warm contacts get a different protocol: shorter messages, direct updates on signal outcomes, and a meeting ask at the right moment.

**The right moment for a meeting ask:** when a signal closes correctly. "The Turkey signal I mentioned in October closed correctly — TRY down 18% in 90 days, within our modeled range. Happy to walk through the methodology for 30 minutes if you're interested." A correct call is the only marketing that works at the institutional level.

### Component 4 — The Content Distribution Ladder

Signal posts publish on Substack first. Simultaneously:

1. **LinkedIn post (300 words max):** Announce the signal, name the country and direction, link to the full post. No paywall teaser. Make the free version legible enough to demonstrate the product's quality — the reader who understands the format will want the next signal.

2. **Macro Twitter/X thread (5 tweets):** Structured thread: Tweet 1 = headline. Tweet 2 = the mechanism. Tweet 3 = the key evidence bullet. Tweet 4 = the falsification condition. Tweet 5 = track record update + link. This format demonstrates the analytical discipline in 280-character units — the most efficient advertisement for the product.

3. **One direct DM to 3–5 specific contacts:** On the day of signal publication, send the post link directly to 3–5 warm contacts with a one-line context: "Published Signal #[N] today — country you might find relevant given your EM book." Personal, not broadcast.

4. **Data community seeding:** Post the GDELT query methodology in the AlphaSignal Slack, the Quant Research Alliance forum, or relevant LinkedIn groups (Alternative Data Group, EM Investors Network). Not the signal — the method. "Here's how we query GDELT for our GRI computation, in case others are building similar frameworks." This builds the data-savvy credibility that reaches Profile C contacts.

---

## III. The Track Record as Distribution Asset

The single most powerful distribution asset is not the analytical process, not the Substack design, and not the LinkedIn following. It is the track record table.

At Signal #5, the track record is nascent — a promising start, nothing more.
At Signal #15, it is evidence — enough data to begin asserting signal quality.
At Signal #26 (the two-signal-per-week, quarterly target), it is a product demo — a self-selling document that answers every institutional due diligence question before it's asked.

The distribution engine must be designed to survive the period before the track record has mass. The cold outreach sequence, the LinkedIn posts, and the data community seeding are all early-period activities that build audience and relationships while the track record accumulates. When Signal #26 exists — six months of published, scored signals — the outreach email writes itself: "Here is 26 signals, here is the outcome record, here is the methodology. Would you like a trial subscription?"

**Implication for Signal timing:** The impulse to accelerate signal frequency to build the track record faster must be weighed against analytical rigor. A track record of 26 signals in 6 months at 65% accuracy is a product. A track record of 52 signals in 3 months at 50% accuracy is noise. The correct cadence is 1–2 signals per week when the GRI scan produces qualified candidates — not forced signal generation to accelerate the track record. The track record earns trust through process integrity, not volume.

---

## IV. The Institutional Pitch — When It's Time

At approximately Signal #20 with a positive track record, the outreach shifts from a content sequence to a direct pitch. The institutional pitch is a 30-minute video call with a specific agenda:

1. (5 min) What Prospectra is: systematic geopolitical signal generation using GDELT data and structured analytical process
2. (10 min) The methodology: GRI computation, 5-layer analytical process, six-section signal post structure, outcome scoring protocol
3. (10 min) The track record: walk through 3–4 signals in detail — the thesis, the evidence, the outcome, what the process got right and what it missed
4. (5 min) Subscription options: trial (3 signals, no commitment) → monthly → annual

The pitch never leads with pricing. It leads with methodology and track record. An institutional buyer who trusts the process will negotiate on price; one who doesn't trust it will not subscribe regardless of price.

**Trial offer:** Offer the first three signals of a trial free to qualified institutional leads. The cost is three signals' worth of research — approximately 6 hours of work. The value is a live-use test in a real portfolio context. An institutional PM who uses three trial signals and sees methodology in action converts at significantly higher rates than one who only reads about it.

---

## V. Investment Implications

The distribution protocol described here is the difference between a high-quality private research journal and a revenue-generating institutional product. Both involve the same analytical work. Only one has a systematic outreach engine.

For the broader investment thesis: **the productization value of Prospectra is only realized if the track record reaches institutional visibility.** A correct call that no institutional reader sees is equivalent, commercially, to a wrong call that no institutional reader sees. The analytical rigor accumulated over 328 lessons and months of GRI pipeline development is a necessary but not sufficient condition for commercial viability.

**The long-horizon investment parallel:** The distribution protocol is analogous to the investor relations function in a listed company. A company with excellent fundamentals but no IR function trades at a valuation discount because the institutional capital that should own it doesn't know the thesis. Prospectra needs its own IR function — a systematic, sustained engagement with the specific institutional readers who should be using the product. That function is this lesson.

**Asset class note:** The subscription pricing model ($500–$5,000/month for institutional subscribers) is structurally equivalent to a royalty stream — recurring, low-churn if the analytical quality holds, and compounding with each correctly-scored signal. The distribution protocol is the acquisition engine for that royalty stream. Build it like infrastructure, not like a campaign.

---

## Databricks Angle

**Contact List as Databricks Table**

The outreach contact list described in Section II should be maintained as a Delta table in Databricks, not a spreadsheet. The schema above translates directly to a Delta table with the following additions:

```python
# contact_outreach.py schema
# Table: prospectra.outreach.contacts

schema = """
contact_id STRING,          -- UUID
name STRING,
role STRING,
firm STRING,
profile STRING,             -- A, B, or C
source STRING,
outreach_date DATE,
last_contact_date DATE,
follow_up_date DATE,
status STRING,              -- Cold, Warm, Trial, Paid, No_Response
signal_refs ARRAY<STRING>,  -- signals sent to this contact
notes STRING,
created_at TIMESTAMP,
updated_at TIMESTAMP
"""
```

**The analytics this enables:**
- Which outreach source (LinkedIn, conference, referral) produces the highest warm-rate?
- Which signal topic (energy, FX, sovereign debt) produces the highest response rate from which profile?
- What is the average cold-to-warm conversion time by profile type?
- Which contacts have been in "Warm" status for >30 days without a trial offer?

At 200+ contacts, this table becomes a distribution analytics dashboard. The CEO reviews it weekly alongside the GRI scan — two infrastructure tools running in parallel.

**Relevant datasets:**
- `prospectra.outreach.contacts` (new table — build now)
- `prospectra.signals.published` (join on signal_refs to track which signals drive conversion)
- `prospectra.signals.outcomes` (join to identify which closed-correct signals should trigger direct outreach)

**Build sequence:** Build the contacts table schema in Databricks this week. Populate it manually from the first 20–30 contacts you have. By Signal #10, the table should have 100+ rows and the query analytics described above should be running automatically.

---

## Reflection Questions

1. **The target profile exercise.** Of the three institutional target profiles (Macro PM, EM Allocator, Quant Analyst), which does your current network give you the best access to? Not the best eventual customer — the best *starting* access. What does that imply about where to focus the first 30 contacts in the outreach list?

2. **The timing of the pitch.** The lesson argues that the institutional pitch should begin at approximately Signal #20 with a positive track record. Is this threshold too conservative, too aggressive, or correct for Prospectra's specific situation? What is the cost of pitching too early (before the track record has mass)? What is the cost of pitching too late?

3. **The free trial logic.** The lesson recommends a three-signal free trial for qualified institutional leads. What qualifies a lead for a free trial? Build a simple rubric: what three criteria must a lead meet before you invest 6 hours of research to run the trial sequence for them?

---

## Questions for Next Session

- **Spaced repetition — Lesson 325 & 327:** The outreach sequence in Message 2 uses a signal performance update ("TRY moved 6% in 21 days") as follow-up content. How does this interact with the outcome scoring protocol? If a signal is performing as expected mid-horizon, is it appropriate to communicate interim performance — or does interim performance create anchoring that compromises the objective outcome scoring?

- **Looking forward — Lesson 329:** The distribution engine generates inbound interest. The next question is pipeline management: how does Prospectra systematically track a prospect from cold outreach through trial to paid subscription, and what are the conversion gates at each stage? That is the CRM layer — the infrastructure that turns a contact list into a revenue forecast.

---

*Lesson 328 of the ongoing curriculum. CEO — Prospectra Geopolitics & Investment Project.*
*Next lesson: Lesson 329 — The CRM Layer: Pipeline Management from Cold to Paid*
