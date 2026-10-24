# uncooked

we built this at devhacks after one of us checked canvas at 11pm and found three exams in four days.

a planner tells you what's due. cooked tells you when you're in trouble, why, and what to do first. it's a skill for Cubbie, the assistant that lives in your iMessage.

## install

text this link to Cubbie:

https://github.com/SrujanRudrapati/cooked/tree/main/cooked

then text "how cooked am I".

## what a conversation looks like

```
you: how cooked am i

cubbie: you're 78% cooked 😬

cubbie: nov 17-20: MAT 266 midterm (15%), CHM 233 exam (12%), ENG 102 essay (8%)

cubbie: start with the MAT midterm. it's the biggest piece of that week and it hits first, on tuesday

cubbie: you have a 3 day gap and then three things in four days. you didn't make a schedule, you made a speedrun

cubbie: want me to save you?

you: yes

cubbie: here's the plan, 3 hrs a day max:
- mon nov 9, 2-4pm: MAT midterm practice, Hayden Library
- tue nov 10, 7-8:30pm: CHM exam review
- wed nov 11, 3-4pm: MAT office hours
- thu nov 12, 1-3pm: essay outline at the MU
...
add these to your calendar?
```

## how the score works

- each thing counts by how much of its class grade it's worth
- hell week is the 7 days with the most grade riding on them
- 45% of your grades landing in one week = 100% cooked
- +10 if hell week starts within 10 days, +5 more if it's 3 days out

we count grade share, not deadlines. three tiny quizzes are not the same as two big projects. all the math lives in `cooked/scripts/score.py` so Cubbie never makes up a number.

## when you fall behind

every night (9pm unless you pick another time) cooked checks Canvas for what you turned in and your calendar for which study blocks already passed. if it can't tell, it just asks. then you get one text: what you got done, what's due in the next 48 hours, your new score, and what to do next.

if you skipped a block it says so. no "great job today!" when you didn't do anything. it moves the block to your next free slot, asks before touching your calendar, and tells you if hell week just got worse. text "pause debriefs" to make it stop.

## what it doesn't do yet

- pass/fail classes. it still counts them by grade share, which overstates how much they matter
- classes not on Canvas. if your prof runs everything off a personal site, cooked can't see it unless it's in a syllabus file
- group projects. it plans like you're doing the whole thing alone, which, honestly, might be accurate
- it never does your graded work or submits anything for you

## screenshot

<!-- TODO: swap in a real screenshot from a Cubbie chat -->
![cooked in iMessage](docs/screenshot.png)

## running it locally

```
cd cooked
python3 scripts/score.py --sample
python3 scripts/test_score.py
```

python 3.12, standard library only. nothing to install.
