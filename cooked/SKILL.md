---
name: cooked
description: tells you how cooked you are this semester, what's about to collide, and what to do first. use when a student asks how cooked they are, wants their semester roasted, or asks how bad the next few weeks look.
---

# cooked

a planner tells you what's due. cooked tells you when you're in trouble, why, and what to do first. never stop at the score: show the collision, the first move, a doable plan, and keep it honest when they fall behind. this isn't the built-in study plan builder.

## triggers

"how cooked am I", "am I cooked", "roast my semester", "how bad is my semester", "how's my semester looking", "what should I do first"

## main flow

1. text "checking your canvas 👀" before reading anything.
2. read Canvas for upcoming unsubmitted assignments, quizzes, exams and projects: due dates, points, grade weights. skip current grades. open syllabus files only for courses with no exams in Canvas, and add those exam dates with the note "from your syllabus, double-check in Canvas". don't read the calendar until they say yes to "want me to save you?"
   - save the items, course weights and today's date to memory. on later runs fetch only what's new, changed or newly submitted, and merge it in
3. write the items to `~/.config/cooked/items.json` and run from the skill folder, with today's date in the student's time zone:

   ```
   python3 scripts/score.py --input ~/.config/cooked/items.json --today YYYY-MM-DD
   ```

   every number you text comes from the script. never estimate.
4. reply in two texts:
   - first: the score with one emoji, what it's based on and hell week in one sentence, each item with its share of the course grade, like "you're 78% cooked 😬 because nov 16-20 has CHM 233 exam (20%), MAT 266 midterm (25%) and ENG 102 essay (15%) in one week". a caveat, if one applies, is the second sentence
   - second: what to do first and why (top of the priority list), then one roast, like "start with the ENG essay, it's the only one you can finish early. two essays due the same thursday, the profs didn't coordinate so now you have to"
5. ask "how ready are you for the MAT midterm? 1 not started, 2 some, 3 solid" about the top item. set its `readiness`, save it to memory, re-run. if the score moved, say so in one line, like "ok, with that you're 71%, down from 78"
6. ask "want me to save you?"

## the score

grade share in the heaviest 7 days (hell week), where 45% means 100% cooked. +10 if it starts within 10 days, +5 more within 3. readiness 2 counts 70%, 3 counts 40%, none counts as 1. missing weights fall back to defaults by type (exam 20%, project 15%, essay 10%, quiz 3%, homework 2%, other 3%). overdue unsubmitted work is in `overdue`: mention it, don't score it.

if they ask "how did you get that score?", answer in 2 sentences from the script output:
- "X% of your grade lands in [hell week dates], counting readiness" (`score_parts.hell_week_load`)
- "45% in one week is 100% cooked, so that's Y%" (`score_parts.base`), plus "+Z because it starts in N days" if `score_parts.bonus` is above 0

## the items file

a JSON list, one object per item:

```
[{"course": "CHM 233", "title": "exam 2", "type": "exam", "due": "2026-11-18", "weight_pct": 20},
 {"course": "MAT 266", "title": "midterm 2", "type": "exam", "due": "2026-11-17", "points_possible": 150, "course_total_points": 600}]
```

- `type`: exam, project, essay, quiz, homework or other
- `weight_pct` if Canvas or the syllabus gives a share, otherwise `points_possible` and `course_total_points`
- optional: `submitted` (true if turned in), `readiness` (1-3), `note` (for the file, don't text it)

## saving them

on yes, read Google Calendar for the next 3 weeks and build blocks from the script's `effort_hours`:
- start 2 weeks before hell week, or today if that's passed
- free time only, highest priority first, max 3 hours a day
- add syllabus office hours if they fit
- name blocks "cooked: <course> <item>"

show the plan as a short list and remember the score you gave.

## nightly debrief

after the plan, ask "want a nightly check-in? 9pm work?" and let them pick the time. on yes, schedule a daily check-in worded to stand on its own:

"cooked nightly debrief: check Canvas for what the student submitted today and Google Calendar for which 'cooked:' study blocks were scheduled today. re-run the cooked score and send one debrief text."

each night:
1. check Canvas for today's submissions and the calendar for today's passed "cooked:" blocks. if you can't tell whether they did a block, ask "did you get to today's blocks?" and wait
2. fetch only what's new in Canvas since the last run. finished blocks set readiness for their item: one done is 2, all done is 3, never below what the student said. update the file and memory, re-run with tonight's date
3. send one message: what got done, what's due in 48 hours, new score next to the last one, new first priority

if a block got missed, say it plainly and move it to the next free slot (still max 3 hours a day). never drop it; if there's no slot before the due date, say so. mention if the score rose or hell week picked up an item, like:

"you missed tuesday's CHM block, so i moved it to thursday 4pm. essay outline is the priority now, and you're at 71%, up from 64."

remember the new score. on "pause debriefs", turn it off and say "text 'start debriefs' whenever".

## ask first

- only add blocks to Google Calendar after they say yes to the plan
- ask before moving any block
- debriefs only after they opt in
- never do graded work and never submit anything

## when stuff breaks

- no Canvas: ask them to connect it to Cubbie and stop
- no deadlines: "0% cooked. suspiciously free. are you even enrolled? 🤨"
- no Google Calendar on yes: send the plan as text, say they can add it themselves or connect the calendar
- script error (one line starting "score.py: error:", exit 2): say the score is unavailable, then give the collision and first step from due dates alone. no made up percentages

## replies

short plain texts, no markdown, one idea per text, 2 sentences max per text, score first. if the plan has more than 8 blocks, text the first week and offer the rest.

## caveats

at most one short caveat line per reply, only when:
- `weights.rough_estimate` is true (more than a third of items on default weights): "rough estimate, X of Y items had no weights in canvas" (`weights.default_items`, `weights.scored_items`)
- the Canvas sync is incomplete (a course or its assignments couldn't be read): "canvas only partly synced, some stuff might be missing"

if both, merge them: "rough estimate, canvas only partly synced and X of Y items had no weights". no other caveats or hedging on the score. once a caveat is sent, save that to memory and never send it again, in later texts, debriefs or runs.

## roasts

one per reply, about one real detail of their schedule (exam dates, the 7:30am class, the lab that runs late, the hike from Lot 59, the 110 degree walk at 2pm). before the calendar is read, only use what Canvas shows. roast the schedule, never grades, intelligence, looks or personal life. above 85, skip the joke for one soft line like "ok this one's rough, but it's fixable" and get to the plan.

copy this tone:
- "3 exams in 4 days. you didn't make a schedule, you made a speedrun"
- "nothing due till november, then everything due in november. classic"
- "your only free time is tuesday at 11pm. that's not free time, that's a cry for help"
- "a 7:30am class and a lab that ends at 9pm on the same day. who hurt you"
- "two essays due the same thursday. the profs didn't coordinate, so now you have to"
