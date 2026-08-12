import unittest
from ai_models.resume_parser import extract_email, extract_phone, extract_skills

class TestResume(unittest.TestCase):
    def test_extract_email(self):
        text = "Contact me at john.doe@example.com for software engineering positions."
        self.assertEqual(extract_email(text), "john.doe@example.com")

    def test_extract_phone(self):
        text = "Call +1-555-123-4567 or email me."
        phone = extract_phone(text)
        self.assertIn("555", phone)

    def test_extract_skills(self):
        text = "Proficient in Python, SQL, React, and Machine Learning."
        skills = extract_skills(text)
        self.assertIn("python", skills)
        self.assertIn("sql", skills)

if __name__ == "__main__":
    unittest.main()
