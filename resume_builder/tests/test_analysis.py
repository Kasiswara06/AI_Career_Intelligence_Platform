import unittest
from ai_models.ats_score import calculate_ats_score
from ai_models.course_recommendation import recommend_courses
from ai_models.resume_analyzer import analyze_resume_complete

class TestAnalysis(unittest.TestCase):
    def test_ats_scoring(self):
        text = "Python SQL Machine Learning Data Science Developer"
        jd = "Seeking Python SQL Machine Learning developer"
        result = calculate_ats_score(text, jd)
        self.assertIn("ats_score", result)
        self.assertGreaterEqual(result["ats_score"], 0)

    def test_course_recommendations(self):
        missing = ["Docker", "Kubernetes"]
        courses = recommend_courses(missing)
        self.assertIsInstance(courses, list)
        self.assertGreater(len(courses), 0)

    def test_resume_analysis(self):
        text = "Python developer with experience in SQL and ML models."
        res = analyze_resume_complete(text)
        self.assertIn("resume_score", res)
        self.assertIn("ats_score", res)

if __name__ == "__main__":
    unittest.main()
