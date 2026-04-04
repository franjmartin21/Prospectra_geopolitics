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

7. If PASSED, update `PROJECT_FOUNDATION.md` curriculum table: mark the completed lesson as "Completed" with date.

8. Commit the changes: `git add PROGRESS.md PROJECT_FOUNDATION.md && git commit -m "Quest complete: L-0X [Lesson Title] — [Score]/5 quiz pass"`

9. Report the result to Bolo clearly:
   - Score, XP awarded, new total, current rank
   - If passed: confirm next lesson is unlocked
   - If failed: specify what to review and that retake is available

Be a fair but uncompromising examiner. A 3/5 is a fail. Do not soften this.
