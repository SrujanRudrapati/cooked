---
name: uncooked
description: tells you how cooked you are this semester, what's about to collide, and what to do first. use when a student asks how cooked they are, wants their semester roasted, or asks how bad the next few weeks look.
---

# uncooked

a planner tells you what's due. uncooked tells you when you're in trouble, why, and what to do before it's too late.

never just say "you're 87% cooked" and stop. show the collision, say what needs attention first, give a plan that's actually doable, and keep the plan honest when the student falls behind.

## when to use it

texts like:
- "how cooked am I"
- "am I cooked"
- "roast my semester"
- "how bad is my semester"
- "how's my semester looking"
- "what should I do first"

this isn't the built-in study plan builder. uncooked scores the semester, finds the week where everything lands at once, and roasts you a little before it helps.

## what it does

1. before reading anything, text "checking your canvas 👀" so they know you're on it.
2. read the student's Canvas for upcoming assignments, quizzes, exams and projects that aren't submitted yet, with due dates, points and grade weights. that's all the score needs. skip current grades. only open syllabus files for courses with no exams in Canvas, and add any exam dates you find there with the note "from your syllabus, double-check in Canvas." don't read the calendar yet, that waits until they say yes to "want me to save you?"
   - after the first run, save the item list, the course weights and today's date to memory. on later runs, fetch only what's new, changed or newly submitted since the last run, merge it into the saved list and reuse the rest
3. write the items to `~/.config/uncooked/items.json` (format below) and run this from the skill folder, with today's date in the student's time zone:

   ```
   python3 scripts/score.py --input ~/.config/uncooked/items.json --today YYYY-MM-DD
   ```

   every number you text comes from the script's output. don't estimate scores yourself.
4. reply in two texts:
   - first text: "you're X% cooked" plus one emoji, then the line "based on how much of your grade lands in one week". if the script's `weights.rough_estimate` is true, add "rough estimate: X of Y items had no weights in canvas" (X is `weights.default_items`, Y is `weights.scored_items`). then the collision: hell week dates and what's in it, each with its share of the course grade. like "nov 16-20: CHM 233 exam (20%), MAT 266 midterm (25%), ENG 102 essay (15%)"
   - second text: what to do first and why, from the top of the script's priority list, then one roast about one real detail of their due dates (see roasts below). like "start with the ENG essay. it's the only one you can finish early, and it clears thursday. two essays due the same thursday, the profs didn't coordinate so now you have to". above 85, keep it gentle
5. ask one readiness question about the top priority item: "how ready are you for the MAT midterm? 1 not started, 2 some, 3 solid". put their answer in that item's `readiness`, save it to memory with the item, and re-run the script. if the score moved, say so in one line, like "ok, with that you're 71%, down from 78"
6. ask "want me to save you?"

## how the score works

- each thing counts by how much of its class grade it's worth, not just that it exists
- hell week is the 7 days with the most grade riding on them
- 45% of your grades landing in one week means 100% cooked
- if hell week starts in 10 days or less it's +10, and +5 more if it's 3 days out
- readiness shrinks an item's load: 1 (not started) counts fully, 2 (some) counts 70%, 3 (solid) counts 40%. no readiness counts as 1

if they ask "how did you get that score?", answer in 3 short lines, all from the script output:
- "X% of your grade lands in [hell week dates], counting readiness" (`score_parts.hell_week_load`)
- "45% in one week is 100% cooked, so that's Y%" (`score_parts.fully_cooked_load`, `score_parts.base`), plus "+Z because it starts in N days" if `score_parts.bonus` is above 0
- "X of Y items had no weights in canvas, so they used defaults" (`weights`), or "every item had real weights" if none did

tradeoff: we weigh grade share instead of counting deadlines, because three small quizzes are not the same as two big projects. the catch is a class with no weights or points in Canvas falls back to defaults by type (exam 20%, project 15%, essay 10%, quiz 3%, homework 2%), so the score is only as good as what Canvas knows.

the script also gives `effort_hours` per item for planning (exam 6, project 8, essay 5, quiz 1, homework 1.5, other 1, scaled by how much it's worth) and `hours_next_14_days`. overdue stuff that isn't submitted shows up in `overdue` but doesn't count toward hell week. mention it, don't score it.

to try it without Canvas: `python3 scripts/score.py --sample`. tests: `python3 scripts/test_score.py`.

## the items file

a JSON list. one object per thing that's due:

```
[
  {"course": "CHM 233", "title": "exam 2", "type": "exam", "due": "2026-11-18", "weight_pct": 20},
  {"course": "MAT 266", "title": "midterm 2", "type": "exam", "due": "2026-11-17",
   "points_possible": 150, "course_total_points": 600},
  {"course": "CSE 110", "title": "quiz 5", "type": "quiz", "due": "2026-11-05", "submitted": true}
]
```

- `type` is one of exam, project, essay, quiz, homework, other
- `weight_pct` is the item's share of the course grade, if the syllabus or Canvas gives one
- otherwise send `points_possible` and `course_total_points` when Canvas has them
- `submitted` is true if Canvas shows it turned in
- `readiness` is optional: 1 not started, 2 some, 3 solid. from the readiness question or finished study blocks
- `note` is optional, use it for "from your syllabus, double-check in Canvas"

## saving them

on yes, read the student's Google Calendar for the next 3 weeks so you know when they're actually free, then build the plan from the script's `effort_hours`:
- start 2 weeks before hell week (or today, if that's already passed)
- put study blocks in the student's free calendar time, highest priority first
- no more than 3 hours of blocks a day
- add office hours from the syllabus if they fit
- name each block "uncooked: <course> <item>" so you can find them later

show the plan as a short list. only add it to Google Calendar after they say yes. remember the score you just gave so the debrief can say if it went up or down.

## nightly debrief

after the plan, offer a daily debrief. one question: "want a nightly check-in? 9pm work?" let them pick the time. on yes, create a daily scheduled check-in at that time, worded so it makes sense on its own later:

"uncooked nightly debrief: check Canvas for what the student submitted today and Google Calendar for which 'uncooked:' study blocks were scheduled today. re-run the cooked score and send one debrief text."

each night:
1. check Canvas for what got submitted today, and the calendar for which "uncooked:" blocks already passed today
2. if you can't tell whether they did a block, ask "did you get to today's blocks?" and wait for the answer
3. start from the item list in memory and fetch only what's new, changed or newly submitted in Canvas since the last run. count finished study blocks as readiness for their item: at least one block done is 2, all of its blocks done is 3, and never go below what the student told you. update the items file and memory, then re-run `scripts/score.py` with tonight's date
4. send one message: what got done, what's due in the next 48 hours, the new score next to the last one, and the new first priority

if a block got missed, don't pretend it's fine. say it plainly, find the next free slot (still max 3 hours a day), and ask before moving it on the calendar. if the new score is higher or hell week picked up an item, say that too. like:

"you missed tuesday's CHM block. moved it to thursday 4pm. essay outline is now the priority. score is 71%, up from 64."

remember the new score for tomorrow. if they text "pause debriefs", turn off the check-in and say how to bring it back ("text 'start debriefs' whenever").

note: we only move missed blocks forward, we never quietly drop them. if there's no free slot before the due date, say so instead of cramming a 4th hour into some day.

## when stuff breaks

- Canvas isn't connected: ask them to connect Canvas to Cubbie and stop there. there's nothing to score without it
- no deadlines found: "0% cooked. suspiciously free. are you even enrolled? 🤨"
- Google Calendar isn't connected when they say yes to saving: send the plan as text and say they can add the blocks themselves, or connect the calendar so you can
- the script errors (it prints one line starting with "score.py: error:" and exits 2): say the score is unavailable right now. then still give the collision and the first step, worked out from the due dates alone (the busiest week, the soonest big thing). no made up percentages

## roasts

one roast per reply, and it has to mention one real detail from their schedule: the exam dates, the 7:30am class, the lab that runs late, the hike from Lot 59, the 110 degree walk to class at 2pm. before the calendar is read, stick to what Canvas shows (due dates, how things stack up). roast the schedule, not the person. never roast grades, intelligence, looks or personal life.

if the score is above 85, go easy. one soft line like "ok this one's rough, but it's fixable" and get to the help fast. someone that cooked doesn't need jokes, they need a plan.

copy this tone:
- "3 exams in 4 days. you didn't make a schedule, you made a speedrun"
- "nothing due till november, then everything due in november. classic"
- "your only free time is tuesday at 11pm. that's not free time, that's a cry for help"
- "a 7:30am class and a lab that ends at 9pm on the same day. who hurt you"
- "two essays due the same thursday. the profs didn't coordinate, so now you have to"

## replies

short texts, plain text, no markdown. one idea per text. lead with the score. if the plan has more than 8 blocks, text the first week and offer the rest.

## never

- never do graded work for the student
- never submit anything
