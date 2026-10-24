"""tests for score.py. run from the skill folder: python3 scripts/test_score.py"""
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from score import compute  # noqa: E402

TODAY = date(2026, 11, 1)


def item(title, kind, due, **extra):
    return {"course": "TST 101", "title": title, "type": kind, "due": due, **extra}


class ScoreTest(unittest.TestCase):
    def test_two_big_projects_beat_three_tiny_quizzes(self):
        projects = [item("project a", "project", "2026-11-20"), item("project b", "project", "2026-11-21")]
        quizzes = [item(f"quiz {n}", "quiz", "2026-11-20") for n in range(3)]

        projects_score = compute(projects, TODAY)["score"]
        quizzes_score = compute(quizzes, TODAY)["score"]

        self.assertGreater(projects_score, quizzes_score)

    def test_submitted_item_does_not_count(self):
        items = [item("exam 1", "exam", "2026-11-10", weight_pct=25, submitted=True)]

        result = compute(items, TODAY)

        self.assertEqual(result["score"], 0)
        self.assertEqual(result["priority"], [])
        self.assertIsNone(result["hell_week"])

    def test_empty_list_scores_zero(self):
        result = compute([], TODAY)

        self.assertEqual(result["score"], 0)
        self.assertEqual(result["hours_next_14_days"], 0)


if __name__ == "__main__":
    unittest.main()
