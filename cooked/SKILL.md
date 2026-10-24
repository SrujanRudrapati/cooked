---
name: cooked
description: tells you how cooked you are this semester, what's about to collide, and what to do first. use when a student asks how cooked they are, wants their semester roasted, or asks how bad the next few weeks look.
---

# cooked

a planner tells you what's due. cooked tells you when you're in trouble, why, and what to do before it's too late.

never just say "you're 87% cooked" and stop. show the collision, say what needs attention first, give a plan that's actually doable, and keep the plan honest when the student falls behind.

## when to use it

texts like:
- "how cooked am I"
- "am I cooked"
- "roast my semester"
- "how bad is my semester"
- "how's my semester looking"
- "what should I do first"

this isn't the built-in study plan builder. cooked scores the semester, finds the week where everything lands at once, and roasts you a little before it helps.

## what it does

1. read the student's Canvas for the rest of the semester: every course, assignment, quiz, exam and project, with due dates, points, grade weights and current grades. if a syllabus file lists exam dates that aren't in Canvas, add them too, with the note "from your syllabus, double-check in Canvas."
2. read the student's Google Calendar for the next 3 weeks so you know when they're actually free.
3. write the items to `~/.config/cooked/items.json` (format below) and run this from the skill folder, with today's date in the student's time zone:

   ```
   python3 scripts/score.py --input ~/.config/cooked/items.json --today YYYY-MM-DD
   ```

   every number you text comes from the script's output. don't estimate scores yourself.
4. reply in short texts, in this order:
   - "you're X% cooked" plus one emoji
   - the collision: hell week dates and what's in it, each with its share of the course grade. like "nov 16-20: CHM 233 exam (20%), MAT 266 midterm (25%), ENG 102 essay (15%)"
   - what to do first and why, from the top of the script's priority list. like "start with the ENG essay. it's the only one you can finish early, and it clears thursday"
   - one roast about one real detail of their schedule (see roasts below). above 85, keep it gentle
5. ask "want me to save you?"

## how the score works

- each thing counts by how much of its class grade it's worth, not just that it exists
- hell week is the 7 days with the most grade riding on them
- 45% of your grades landing in one week means 100% cooked
- if hell week starts in 10 days or less it's +10, and +5 more if it's 3 days out

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
- `note` is optional, use it for "from your syllabus, double-check in Canvas"

## saving them

on yes, build the plan from the script's `effort_hours`:
- start 2 weeks before hell week (or today, if that's already passed)
- put study blocks in the student's free calendar time, highest priority first
- no more than 3 hours of blocks a day
- add office hours from the syllabus if they fit
- name each block "cooked: <course> <item>" so you can find them later

show the plan as a short list. only add it to Google Calendar after they say yes. remember the score you just gave so the debrief can say if it went up or down.

## nightly debrief

after the plan, offer a daily debrief. one question: "want a nightly check-in? 9pm work?" let them pick the time. on yes, create a daily scheduled check-in at that time, worded so it makes sense on its own later:

"cooked nightly debrief: check Canvas for what the student submitted today and Google Calendar for which 'cooked:' study blocks were scheduled today. re-run the cooked score and send one debrief text."

each night:
1. check Canvas for what got submitted today, and the calendar for which "cooked:" blocks already passed today
2. if you can't tell whether they did a block, ask "did you get to today's blocks?" and wait for the answer
3. rebuild the items file from Canvas and re-run `scripts/score.py` with tonight's date
4. send one message: what got done, what's due in the next 48 hours, the new score next to the last one, and the new first priority

if a block got missed, don't pretend it's fine. say it plainly, find the next free slot (still max 3 hours a day), and ask before moving it on the calendar. if the new score is higher or hell week picked up an item, say that too. like:

"you missed tuesday's CHM block. moved it to thursday 4pm. essay outline is now the priority. score is 71%, up from 64."

remember the new score for tomorrow. if they text "pause debriefs", turn off the check-in and say how to bring it back ("text 'start debriefs' whenever").

note: we only move missed blocks forward, we never quietly drop them. if there's no free slot before the due date, say so instead of cramming a 4th hour into some day.

## roasts

one roast per reply, and it has to mention one real detail from their schedule: the exam dates, the 7:30am class, the lab that runs late, the hike from Lot 59, the 110 degree walk to class at 2pm. roast the schedule, not the person. never roast grades, intelligence, looks or personal life.

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
