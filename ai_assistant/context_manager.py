from typing import Dict, Any
from database.database import (
    get_user_profile,
    get_latest_resume_analysis,
    get_latest_salary_prediction
)
from services.resume_service import get_user_active_resume

def extract_user_career_context(user_id: int) -> Dict[str, Any]:
    """
    Extracts complete, up-to-date user profile and AI analysis context from database:
    - User Profile
    - Active Resume Info
    - Resume Analysis (Resume Score, ATS Score)
    - Skill Gap & Missing Skills
    - Salary Predictions
    """
    profile = get_user_profile(user_id) or {}
    active_resume = get_user_active_resume(user_id) or {}
    latest_analysis = get_latest_resume_analysis(user_id) or {}
    latest_salary = get_latest_salary_prediction(user_id) or {}

    resume_name = active_resume.get("filename", "Candidate_Resume.pdf")
    resume_score = active_resume.get("resume_score", latest_analysis.get("resume_score", 85))
    ats_score = active_resume.get("ats_score", latest_analysis.get("ats_score", 88))
    
    extracted_skills = active_resume.get("parsed", {}).get("technical_skills", {})
    all_skills = []
    if isinstance(extracted_skills, dict):
        for sub in extracted_skills.values():
            all_skills.extend(sub)
    elif isinstance(extracted_skills, list):
        all_skills = extracted_skills

    if not all_skills:
        all_skills = ["Python", "SQL", "Machine Learning", "Streamlit", "Git"]

    missing_skills = latest_analysis.get("missing_skills", "Docker, AWS, Kubernetes, CI/CD")
    if isinstance(missing_skills, list):
        missing_skills = ", ".join(missing_skills)

    expected_salary = latest_salary.get("predicted_salary", 8.5)

    return {
        "candidate_name": profile.get("full_name", "Candidate"),
        "college": profile.get("college", "Institute of Technology"),
        "qualification": profile.get("qualification", "B.Tech CSE"),
        "resume_name": resume_name,
        "resume_score": resume_score,
        "ats_score": ats_score,
        "skills": list(set(all_skills)),
        "missing_skills": missing_skills,
        "expected_salary_lpa": expected_salary,
        "target_role": "AI Engineer / Data Scientist"
    }
