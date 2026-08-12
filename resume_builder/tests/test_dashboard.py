import unittest
from services.dashboard_service import get_dashboard_summary

class TestDashboard(unittest.TestCase):
    def test_dashboard_summary(self):
        summary = get_dashboard_summary(1)
        self.assertIsInstance(summary, dict)
        self.assertIn("user_name", summary)
        self.assertIn("ats_score", summary)
        self.assertIn("resume_score", summary)
        self.assertIn("skill_match_pct", summary)
        self.assertIn("expected_salary", summary)
        self.assertIn("readiness_score", summary)

if __name__ == "__main__":
    unittest.main()
