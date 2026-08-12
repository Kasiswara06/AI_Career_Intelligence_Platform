import unittest
from utils.password_hash import hash_password, check_password
from utils.helper import is_valid_email, is_strong_password

class TestAuth(unittest.TestCase):
    def test_email_validation(self):
        self.assertTrue(is_valid_email("user@example.com"))
        self.assertFalse(is_valid_email("invalid_email"))

    def test_password_strength(self):
        is_strong, _ = is_strong_password("Secret123")
        self.assertTrue(is_strong)
        is_weak, _ = is_strong_password("123")
        self.assertFalse(is_weak)

    def test_password_hashing(self):
        pwd = "MySecurePassword123"
        hashed = hash_password(pwd)
        self.assertTrue(check_password(pwd, hashed))
        self.assertFalse(check_password("WrongPassword", hashed))

if __name__ == "__main__":
    unittest.main()
