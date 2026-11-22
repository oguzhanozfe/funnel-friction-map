import unittest
from project import analyze


class FunnelTests(unittest.TestCase):
    def test_pools_people_not_cohort_rates(self):
        result = analyze({"stages": ["Start", "Done"], "cohorts": {"A": [90, 81], "B": [10, 1]}})
        self.assertEqual(result["metrics"]["Completion (%)"], 82.0)
        self.assertEqual([r["Loss (%)"] for r in result["rows"]], [10.0, 90.0])

    def test_each_transition_has_its_own_denominator(self):
        rows = analyze({"stages": ["A", "B", "C"], "cohorts": {"Web": [10, 4, 3]}})["rows"]
        self.assertEqual((rows[1]["Entered"], rows[1]["Loss (%)"]), (4, 25.0))

    def test_empty_cohort_is_undefined(self):
        result = analyze({"stages": ["A", "B"], "cohorts": {"X": [0, 0]}})
        self.assertIsNone(result["metrics"]["Completion (%)"])
        self.assertIsNone(result["rows"][0]["Loss (%)"])

    def test_rejects_nonsequential_and_boolean_counts(self):
        for counts in ([4, 6], [True, 0], [4]):
            with self.subTest(counts=counts), self.assertRaises(ValueError):
                analyze({"stages": ["A", "B"], "cohorts": {"Web": counts}})
