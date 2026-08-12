import unittest
from ai_models.skill_gap import analyze_skill_gap
from ai_models.job_matching import calculate_job_match

class TestMatching(unittest.TestCase):
    def test_skill_gap_analysis(self):
        resume_text = "Experienced Python, SQL, and Machine Learning developer."
        jd_text = "Looking for a Python, SQL, Docker, and AWS engineer."
        res = analyze_skill_gap(resume_text, jd_text)
        self.assertGreater(res["skill_match_percentage"], 0)
        matching_lower = [s.lower() for s in res["matching_skills"]]
        missing_lower = [s.lower() for s in res["missing_skills"]]
        self.assertIn("python", matching_lower)
        self.assertIn("docker", missing_lower)

    def test_job_matching(self):
        resume_text = "Senior Software Developer proficient in Python and React."
        jd_text = "Software Developer needed for Python and React web application."
        match = calculate_job_match(resume_text, jd_text)
        self.assertGreater(match["match_percentage"], 50)

if __name__ == "__main__":
    unittest.main()
