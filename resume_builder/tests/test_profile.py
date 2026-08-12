import unittest
from database.database import get_user_profile, update_user_profile, create_user

class TestProfile(unittest.TestCase):
    def test_profile_retrieval(self):
        profile = get_user_profile(1)
        self.assertIsInstance(profile, dict)

    def test_profile_update(self):
        res = update_user_profile(1, {"city": "Hyderabad", "country": "India"})
        self.assertTrue(res)

if __name__ == "__main__":
    unittest.main()
