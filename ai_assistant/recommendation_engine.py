from typing import Dict, Any, List
from ai_models.course_recommendation import recommend_courses
from ai_models.salary_prediction import predict_salary

def generate_chat_recommendation(topic: str, missing_skills: List[str] = None) -> Dict[str, Any]:
    """Generates contextual in-chat course and salary recommendations based on discussion topic."""
    skills = missing_skills or ["Docker", "AWS", "React"]
    courses = recommend_courses(skills[:2])
    salary = predict_salary(job_role="Software Engineer", experience_years=2.0)

    return {
        "recommended_courses": courses,
        "salary_benchmark": salary,
        "action_item": f"Consider building a project highlighting {skills[0]} to improve your career match profile."
    }
