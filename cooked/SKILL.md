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
   - one roast (see roasts below)
5. ask "want me to save you?"

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

show the plan as a short list. only add it to Google Calendar after they say yes.

## roasts

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
