import unittest
from models.user import User
from models.profile import Profile
from models.resume import Resume

class TestModels(unittest.TestCase):
    def test_user_model(self):
        user = User(id=1, full_name="Alice Smith", email="alice@example.com", mobile="1234567890", age=25)
        d = user.to_dict()
        self.assertEqual(d["full_name"], "Alice Smith")
        self.assertEqual(d["email"], "alice@example.com")

    def test_profile_model(self):
        profile = Profile(id=1, user_id=1, college="MIT", qualification="B.Tech")
        self.assertEqual(profile.college, "MIT")

if __name__ == "__main__":
    unittest.main()
