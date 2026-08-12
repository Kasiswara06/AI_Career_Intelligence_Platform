from typing import List, Dict, Any
from ai_models.career_recommendation import recommend_career_path
from ai_models.course_recommendation import recommend_courses
from ai_models.salary_prediction import predict_salary

def get_career_and_course_recommendations(skills: List[str], education: List[str] = None, experience_years: float = 0.0) -> Dict[str, Any]:
    """Generates career predictions and course recommendations for missing skills."""
    careers = recommend_career_path(skills, education, experience_years)
    
    top_missing_skills = []
    if careers:
        top_missing_skills = careers[0].get("missing_skills", [])
    
    courses = recommend_courses(top_missing_skills)

    # Estimate salary for top recommendation
    salary_est = {}
    if careers:
        top_role = careers[0]["career_role"]
        salary_est = predict_salary(top_role, experience_years)

    return {
        "career_recommendations": careers,
        "course_recommendations": courses,
        "salary_estimate": salary_est
    }
