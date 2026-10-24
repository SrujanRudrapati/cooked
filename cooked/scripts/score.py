#!/usr/bin/env python3
"""cooked: how bad is the rest of the semester.

reads a JSON list of Canvas items and prints one line of JSON with the cooked
score, hell week, priority list and effort hours. standard library only.

    python3 scripts/score.py --input items.json --today 2026-11-06
    python3 scripts/score.py --sample
"""
import argparse
import json
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

# share of the course grade (%) when Canvas gives no weight or points
DEFAULT_LOAD = {"exam": 20, "project": 15, "essay": 10, "quiz": 3, "homework": 2, "other": 3}
# study hours for an item at its type's default load
BASE_HOURS = {"exam": 6, "project": 8, "essay": 5, "quiz": 1, "homework": 1.5, "other": 1}
EFFORT_MIN_SCALE = 0.5
EFFORT_MAX_SCALE = 2.0
# how much of an item's load still counts: 1 not started, 2 some, 3 solid
READINESS_FACTOR = {1: 1.0, 2: 0.7, 3: 0.4}
# more than this share of items on default weights makes the score a rough estimate
ROUGH_ESTIMATE_SHARE = 1 / 3

FULLY_COOKED_LOAD = 45  # this much grade in one week = 100% cooked
HELL_WEEK_DAYS = 7
SOON_DAYS, SOON_BONUS = 10, 10
VERY_SOON_DAYS, VERY_SOON_BONUS = 3, 5
MAX_SCORE = 100

PLANNING_DAYS = 14
REASONS_FOR_TOP = 3
CAN_FINISH_EARLY = {"essay", "project", "homework", "other"}

SKILL_DIR = Path(__file__).resolve().parent.parent
SAMPLE_FILE = SKILL_DIR / "assets" / "sample_items.json"
SAMPLE_TODAY = "2026-11-06"


class InputError(ValueError):
    """the items file or a flag is wrong in a way the student can fix."""


def half_up(value: float) -> int:
    return math.floor(value + 0.5)


def parse_date(value: Any, label: str) -> date:
    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        raise InputError(f"{label} must be a date like 2026-11-18, got {value!r}") from None


def to_number(value: Any, label: str) -> float:
    if isinstance(value, bool):
        raise InputError(f"{label} must be a number, got {value!r}")
    try:
        return float(value)
    except (TypeError, ValueError):
        raise InputError(f"{label} must be a number, got {value!r}") from None


def item_load(raw: dict, kind: str, label: str) -> tuple[float, bool]:
    """the item's share of its course grade, and whether it fell back to the default."""
    if raw.get("weight_pct") is not None:
        return to_number(raw["weight_pct"], f"{label} weight_pct"), False
    points, total = raw.get("points_possible"), raw.get("course_total_points")
    if points is not None and total is not None:
        total_num = to_number(total, f"{label} course_total_points")
        if total_num > 0:
            return to_number(points, f"{label} points_possible") / total_num * 100, False
    return float(DEFAULT_LOAD[kind]), True


def parse_readiness(value: Any, label: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or value not in READINESS_FACTOR:
        raise InputError(f"{label} readiness must be 1, 2 or 3, got {value!r}")
    return int(value)


def effort_hours(kind: str, load: float) -> float:
    scale = min(EFFORT_MAX_SCALE, max(EFFORT_MIN_SCALE, load / DEFAULT_LOAD[kind]))
    return round(BASE_HOURS[kind] * scale, 1)


def normalize(raw: Any, index: int) -> tuple[dict, str | None]:
    label = f"item {index}"
    if not isinstance(raw, dict):
        raise InputError(f"{label} must be an object")
    missing = [key for key in ("course", "title", "due") if not raw.get(key)]
    if missing:
        raise InputError(f"{label} is missing {', '.join(missing)}")
    kind = str(raw.get("type", "other")).lower()
    warning = None
    if kind not in DEFAULT_LOAD:
        warning = f"{label} ({raw['title']}) has unknown type {kind!r}, counted as other"
        kind = "other"
    load, default_weight = item_load(raw, kind, label)
    readiness = parse_readiness(raw.get("readiness"), label)
    item = {
        "course": str(raw["course"]),
        "title": str(raw["title"]),
        "type": kind,
        "due": parse_date(raw["due"], f"{label} due"),
        "load": load,
        "cooked_load": load * READINESS_FACTOR[readiness or 1],
        "default_weight": default_weight,
        "readiness": readiness,
        "effort_hours": effort_hours(kind, load),
        "submitted": raw.get("submitted") is True,
        "note": raw.get("note"),
    }
    return item, warning


def find_hell_week(items: list[dict]) -> dict | None:
    """the 7-day window with the most grade riding on it. ties go to the earliest."""
    best = None
    for start in sorted({item["due"] for item in items}):
        end = start + timedelta(days=HELL_WEEK_DAYS - 1)
        inside = [item for item in items if start <= item["due"] <= end]
        total = sum(item["cooked_load"] for item in inside)
        if best is None or total > best["total_load"]:
            best = {"start": start, "items": inside, "total_load": total}
    return best


def cooked_score(hell_week: dict | None, today: date) -> dict:
    if hell_week is None:
        return {"score": 0, "base": 0, "bonus": 0}
    base = min(MAX_SCORE, half_up(hell_week["total_load"] / FULLY_COOKED_LOAD * 100))
    days_away = (hell_week["start"] - today).days
    bonus = (SOON_BONUS if days_away <= SOON_DAYS else 0) + (
        VERY_SOON_BONUS if days_away <= VERY_SOON_DAYS else 0
    )
    return {"score": min(MAX_SCORE, base + bonus), "base": base, "bonus": bonus}


def days_until(item: dict, today: date) -> int:
    return (item["due"] - today).days


def urgency(item: dict, today: date) -> float:
    # due today counts as 1 day so nothing divides by zero
    return item["cooked_load"] / max(1, days_until(item, today))


def reason_for(item: dict, items: list[dict], hell_items: list[dict], today: date) -> str:
    days = days_until(item, today)
    if item in hell_items and item["load"] == max(other["load"] for other in hell_items):
        return f"biggest piece of hell week ({round(item['load'], 1)}% of {item['course']})"
    if item["load"] == max(other["load"] for other in items):
        return f"biggest grade share left ({round(item['load'], 1)}% of {item['course']})"
    if item["due"] == min(other["due"] for other in items):
        return "due today" if days == 0 else f"due soonest, in {days} day{'s' if days != 1 else ''}"
    if item["type"] in CAN_FINISH_EARLY:
        return "can be finished early to clear the week"
    return "big grade share for how soon it's due"


def public_item(item: dict, today: date) -> dict:
    shown = {
        "course": item["course"],
        "title": item["title"],
        "type": item["type"],
        "due": item["due"].isoformat(),
        "days_until": days_until(item, today),
        "load": round(item["load"], 1),
        "effort_hours": item["effort_hours"],
    }
    if item["readiness"] is not None:
        shown = {**shown, "readiness": item["readiness"]}
    return {**shown, "note": item["note"]} if item["note"] else shown


def priority_list(items: list[dict], hell_items: list[dict], today: date) -> list[dict]:
    ranked = sorted(items, key=lambda it: (-urgency(it, today), it["due"], it["course"], it["title"]))
    return [
        {
            "rank": rank,
            **public_item(item, today),
            "reason": reason_for(item, items, hell_items, today) if rank <= REASONS_FOR_TOP else None,
        }
        for rank, item in enumerate(ranked, start=1)
    ]


def hell_week_summary(hell_week: dict | None, today: date) -> dict | None:
    if hell_week is None:
        return None
    dues = [item["due"] for item in hell_week["items"]]
    return {
        "start": min(dues).isoformat(),
        "end": max(dues).isoformat(),
        "days_until_start": (hell_week["start"] - today).days,
        "total_load": round(hell_week["total_load"], 1),
        "items": [public_item(item, today) for item in hell_week["items"]],
    }


def weights_summary(items: list[dict]) -> dict:
    defaults = sum(1 for item in items if item["default_weight"])
    return {
        "default_items": defaults,
        "scored_items": len(items),
        "rough_estimate": defaults > len(items) * ROUGH_ESTIMATE_SHARE,
    }


def compute(raw_items: Any, today: date) -> dict:
    if not isinstance(raw_items, list):
        raise InputError("input must be a JSON list of items")
    normalized = [normalize(raw, index) for index, raw in enumerate(raw_items)]
    open_items = [item for item, _ in normalized if not item["submitted"]]
    upcoming = sorted((it for it in open_items if it["due"] >= today), key=lambda it: it["due"])
    overdue = [item for item in open_items if item["due"] < today]
    hell_week = find_hell_week(upcoming)
    parts = cooked_score(hell_week, today)
    soon = [item for item in upcoming if days_until(item, today) <= PLANNING_DAYS]
    return {
        "today": today.isoformat(),
        "score": parts["score"],
        "score_parts": {"hell_week_load": round(hell_week["total_load"], 1) if hell_week else 0,
                        "fully_cooked_load": FULLY_COOKED_LOAD,
                        "base": parts["base"], "bonus": parts["bonus"]},
        "weights": weights_summary(upcoming),
        "hell_week": hell_week_summary(hell_week, today),
        "priority": priority_list(upcoming, hell_week["items"] if hell_week else [], today),
        "hours_next_14_days": round(sum(item["effort_hours"] for item in soon), 1),
        "overdue": [public_item(item, today) for item in overdue],
        "warnings": [warning for _, warning in normalized if warning],
    }


def load_items(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise InputError(f"no items file at {path}") from None
    except json.JSONDecodeError as err:
        raise InputError(f"{path} is not valid JSON ({err.msg}, line {err.lineno})") from None


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="score how cooked a semester is")
    parser.add_argument("--input", type=Path, help="JSON list of items")
    parser.add_argument("--today", help="today's date in the student's time zone, YYYY-MM-DD")
    parser.add_argument("--sample", action="store_true", help="use the bundled sample items")
    args = parser.parse_args(argv)
    if not args.sample and (args.input is None or args.today is None):
        parser.error("--input and --today are required (or use --sample)")
    return args


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    try:
        path = SAMPLE_FILE if args.sample else args.input
        today = parse_date(args.today or SAMPLE_TODAY, "--today")
        result = compute(load_items(path), today)
    except InputError as err:
        print(f"score.py: error: {err}", file=sys.stderr)
        return 2
    print(json.dumps(result, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
