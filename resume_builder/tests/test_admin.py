import unittest
from services.admin_service import get_admin_kpi_metrics, get_admin_users_list, get_login_activity_logs
from auth.authorization import is_admin_user
from utils.security import sanitize_user_dict_for_admin, FORBIDDEN_EXPOSURE_FIELDS

class TestAdmin(unittest.TestCase):
    def test_admin_kpi_metrics(self):
        metrics = get_admin_kpi_metrics()
        self.assertIsInstance(metrics, dict)
        self.assertIn("total_users", metrics)
        self.assertIn("total_logins", metrics)
        self.assertIn("total_resumes", metrics)
        self.assertIn("total_analyses", metrics)

    def test_zero_password_exposure(self):
        """CRITICAL SECURITY TEST: Verifies that passwords are NEVER returned in admin users list or log dicts."""
        users = get_admin_users_list()
        self.assertIsInstance(users, list)
        for u in users:
            for forbidden_key in FORBIDDEN_EXPOSURE_FIELDS:
                self.assertNotIn(forbidden_key, u, f"CRITICAL SECURITY VIOLATION: '{forbidden_key}' exposed in admin user dictionary!")

    def test_security_scrubbing(self):
        raw_dict = {
            "user_id": 1,
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "SecretPassword123",
            "password_hash": "$2b$12$eImiTXuWVxfM37uY4JANjO5E.5zK",
            "token": "secret_token_123"
        }
        clean = sanitize_user_dict_for_admin(raw_dict)
        self.assertNotIn("password", clean)
        self.assertNotIn("password_hash", clean)
        self.assertNotIn("token", clean)
        self.assertIn("full_name", clean)
        self.assertIn("email", clean)

    def test_login_activity_logs(self):
        logs = get_login_activity_logs(limit=5)
        self.assertIsInstance(logs, list)
        for log in logs:
            self.assertNotIn("password", log)
            self.assertNotIn("password_hash", log)

if __name__ == "__main__":
    unittest.main()
