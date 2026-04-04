# Geopolitics & Investment Learning Project

## Project Purpose
A structured, AI-directed learning program combining geopolitics education with investment analysis. The user is simultaneously building a Databricks project that operationalizes these concepts.

## Learning Philosophy
- Lessons follow the Socratic method: explain, then challenge with questions
- Each concept connects to a real investment implication (macro, sector, or asset class)
- Spaced repetition: revisit prior concepts when new events are relevant
- Progressive depth: start with frameworks, build to current events analysis

## Session Types

### 1. Daily Lesson (`/lesson`)
- 15-20 minute structured lesson on a curriculum topic
- Ends with 2-3 reflection questions and a "market connection" — how this concept affects portfolio decisions
- Save output to: `reports/daily_lessons/YYYY-MM-DD_<topic>.md`

### 2. Weekly Geopolitics Briefing (`/briefing`)
- Search for the top 5 geopolitical events of the past 7 days
- For each event: what happened, why it matters geopolitically, investment implications (currencies, commodities, equities, bonds)
- Save output to: `reports/weekly_lectures/YYYY-MM-DD_weekly_briefing.md`

### 3. Deep Dive (`/deepdive <topic>`)
- 30-45 minute lecture on a specific topic (e.g., "dollar hegemony", "China-Taiwan strait", "OPEC+ dynamics")
- Save output to: `reports/market_analysis/YYYY-MM-DD_<topic>.md`

## Curriculum Sequence (in order)
1. Foundations of Geopolitical Analysis (realism, liberalism, power theory)
2. Geography as Destiny (Mackinder, Spykman, sea power vs land power)
3. The Dollar System & Bretton Woods Legacy
4. Energy Geopolitics (oil, gas, critical minerals)
5. Trade Wars & Supply Chain Geopolitics
6. China's Rise & the Multipolar Transition
7. European Fragmentation & NATO Dynamics
8. Emerging Market Political Risk
9. Technology & Semiconductor Geopolitics
10. Geopolitical Frameworks for Portfolio Construction

## Report Format
All reports must include:
- Date, session type, topic
- Key concepts covered
- Investment implications section
- Questions for next session (spaced repetition hook)
- Databricks relevance note (how this could inform the analytical project)

## Databricks Project Context
The user is building a Databricks project that merges geopolitics and investment data. Lessons should flag:
- Relevant datasets (e.g., GDELT for event data, FRED for macro, Bloomberg/Yahoo Finance for asset prices)
- Analytical frameworks that could be operationalized as pipelines
- Features that could be engineered from geopolitical events
