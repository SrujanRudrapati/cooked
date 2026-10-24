"""tests for score.py. run from the skill folder: python3 scripts/test_score.py"""
import sys
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from score import InputError, compute  # noqa: E402

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

    def test_readiness_3_lowers_the_score(self):
        not_started = [item("exam 2", "exam", "2026-11-20", weight_pct=25)]
        solid = [item("exam 2", "exam", "2026-11-20", weight_pct=25, readiness=3)]

        not_started_score = compute(not_started, TODAY)["score"]
        solid_score = compute(solid, TODAY)["score"]

        self.assertLess(solid_score, not_started_score)

    def test_readiness_outside_1_to_3_is_an_error(self):
        items = [item("exam 2", "exam", "2026-11-20", readiness=4)]

        with self.assertRaises(InputError):
            compute(items, TODAY)

    def test_counts_items_with_default_weights(self):
        items = [
            item("exam 2", "exam", "2026-11-20", weight_pct=25),
            item("quiz 4", "quiz", "2026-11-12"),
            item("lab 3", "homework", "2026-11-13", points_possible=10, course_total_points=500),
        ]

        weights = compute(items, TODAY)["weights"]

        self.assertEqual(weights, {"default_items": 1, "scored_items": 3, "rough_estimate": False})


if __name__ == "__main__":
    unittest.main()
