Deliver a quiz to verify mastery of the most recently completed lesson, then update PROGRESS.md.

## Steps

1. Read `PROGRESS.md` to identify which lesson is in "OPEN — Quiz Pending" status. That is the lesson being tested. If no lesson is pending a quiz, tell Bolo no quiz is available and which lesson must be completed first.

2. Read the corresponding lesson file from `reports/daily_lessons/` to load the full lesson content.

3. Deliver a 5-question multiple choice quiz. Requirements:
   - Questions test conceptual understanding, NOT memorization of definitions
   - At least 2 questions must require applying the concept to a real-world scenario
   - At least 1 question must connect the lesson to investment implications
   - 4 answer choices per question (A, B, C, D)
   - Do NOT reveal answers — wait for Bolo's responses

4. After Bolo answers all 5 questions, score them:
   - Show the correct answer for each question with a 1-2 sentence explanation
   - Tally the score (X/5)

5. Determine outcome:
   - **4/5 or 5/5 → PASSED.** The lesson quest is CLOSED.
   - **3/5 or below → FAILED.** The quest stays OPEN. Tell Bolo which concepts to review. A retake is available after reviewing the lesson again.

6. If PASSED, update `PROGRESS.md`:
   - Change the lesson status from "OPEN — Quiz Pending" to "COMPLETED ✓"
   - Record the quiz score
   - Award XP: 100 XP base + 10 bonus if perfect (5/5)
   - Update LEARN XP total and TOTAL XP
   - Update the rank progress bar if a threshold was crossed
   - Unlock the next lesson (change status from LOCKED to LOCKED — await `/lesson`)
   - Check if any achievements were unlocked (First Blood, Scholar, Perfect Score) and mark them

7. If PASSED, assess and update the Knowledge Benchmarking section of `PROGRESS.md`.

   **How to assess the two scales:**

   Use the number of lessons passed, the quiz score, and the quality of answers demonstrated (did the answers show application and synthesis, or just recall?) to make a holistic judgment. Be honest — do not flatter.

   *General Population Percentile guide:*
   - 1–2 lessons passed, passing scores: Top 25% (most people have never systematically studied IR theory)
   - 3–5 lessons passed, consistent 4–5/5: Top 10%
   - 6–9 lessons passed, strong scores: Top 5%
   - 10–12 lessons passed with high accuracy + investment call track record: Top 1–2%

   *Academic Equivalent guide:*
   - 1 lesson passed: Undergrad Year 1 (introductory IR theory exposure)
   - 2–3 lessons passed: Undergrad Year 1–2 (frameworks + geography/economics intro)
   - 4–6 lessons passed: Undergrad Year 2–3 (applied frameworks, regional dynamics)
   - 7–9 lessons passed: Undergrad Final Year (synthesis across domains)
   - 10–11 lessons passed + strong INTEL track record: Graduate (MA/MSc) equivalent
   - 12 lessons passed + documented investment calls with right reasoning: Graduate equivalent with applied practitioner edge

   Update the "Current" values in the benchmark table and add a new row to the Benchmark History table with today's date, lessons passed, percentile, academic level, and a brief note on what drove the assessment.

8. If PASSED, update `PROJECT_FOUNDATION.md` curriculum table: mark the completed lesson as "Completed" with date.

9. Commit the changes: `git add PROGRESS.md PROJECT_FOUNDATION.md && git commit -m "Quest complete: L-0X [Lesson Title] — [Score]/5 quiz pass"`

10. Report the result to Bolo clearly:
    - Score, XP awarded, new total, current rank
    - **Knowledge benchmark update**: state the new population percentile and academic equivalent, and what specifically they need to do to move up the next level on each scale
    - If passed: confirm next lesson is unlocked
    - If failed: specify what to review and that retake is available

Be a fair but uncompromising examiner. A 3/5 is a fail. Do not soften the benchmark assessment — Bolo asked for an honest calibration against people who study this seriously. Give it.
