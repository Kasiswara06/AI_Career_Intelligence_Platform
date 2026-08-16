from typing import Dict, Any
import streamlit as st
from database.database import get_user_profile, execute_query
from services.resume_service import get_user_active_resume
from services.project_service import fetch_user_projects
from services.certificate_service import fetch_user_certificates
from ai_models.ats_score import calculate_ats_score
from ai_models.course_recommendation import recommend_courses

def get_dashboard_summary(user_id: int) -> Dict[str, Any]:
    """
    Assembles real-time comprehensive statistics for the Milestone 4 User Dashboard:
    Profile details, resume status, ATS score, resume score, skill gaps, job matches,
    career recommendations, course recommendations, salary prediction, readiness score, and activities.
    """
    profile = get_user_profile(user_id) or {}
    active_resume = get_user_active_resume(user_id)
    projects = fetch_user_projects(user_id) or []
    certs = fetch_user_certificates(user_id) or []

    # 1. Profile completion & basic details
    full_name = profile.get("full_name") or st.session_state.get("user_name", "Candidate")
    profile_completion = int(profile.get("completion_percentage", 25 if profile else 0))

    # 2. Active Resume & ATS Scan
    ats_score = 0
    resume_score = 0
    detected_skills = []
    resume_summary = "No active resume uploaded yet. Upload a resume to enable AI analysis and ATS evaluation."
    
    if active_resume:
        ats_score = active_resume.get("ats_score", 0)
        resume_score = active_resume.get("resume_score", 0)
        raw_text = active_resume.get("raw_text", "")
        if raw_text:
            ats_data = calculate_ats_score(raw_text)
            ats_score = active_resume.get("ats_score") or ats_data.get("ats_score", 0)
            resume_score = active_resume.get("resume_score") or ats_data.get("resume_score", 0)
            if ats_data.get("detected_skills"):
                detected_skills = ats_data.get("detected_skills")
            if ats_data.get("summary"):
                resume_summary = ats_data.get("summary")
    elif profile.get("skills"):
        detected_skills = [s.strip() for s in profile.get("skills").split(",") if s.strip()]

    # 3. Skill Gap Analysis
    missing_skills = []
    skill_match_pct = 0.0
    skill_gap_pct = 0.0
    if detected_skills:
        target_jd_skills = ["Python", "SQL", "Machine Learning", "Data Analysis", "Git", "Docker", "Kubernetes", "AWS Cloud", "REST APIs", "PyTorch"]
        matching = [s for s in detected_skills if any(t.lower() in s.lower() or s.lower() in t.lower() for t in target_jd_skills)]
        missing = [t for t in target_jd_skills if not any(s.lower() in t.lower() or t.lower() in s.lower() for s in detected_skills)]
        missing_skills = missing[:5] if missing else []
        if target_jd_skills:
            skill_match_pct = round((len(matching) / len(target_jd_skills)) * 100, 1)
            skill_gap_pct = round(100.0 - skill_match_pct, 1)

    # 4. Job Match Ranking
    top_job_title = "N/A"
    top_job_company = "N/A"
    top_job_match_pct = 0.0
    
    try:
        db_matches = execute_query(
            "SELECT job_title, company, match_percentage FROM job_matching WHERE user_id = %s ORDER BY match_percentage DESC LIMIT 1",
            (user_id,), fetchone=True
        )
        if db_matches and isinstance(db_matches, dict):
            top_job_title = db_matches.get("job_title", top_job_title)
            top_job_company = db_matches.get("company", top_job_company)
            top_job_match_pct = float(db_matches.get("match_percentage", top_job_match_pct))
    except Exception:
        pass

    # 5. Career & Course Recommendations
    recommended_career = profile.get("qualification") or "AI / Software Engineer"
    career_growth = "Active Market Growth"
    rec_courses = recommend_courses(missing_skills) if missing_skills else []

    # 6. Expected Salary
    exp_years = float(profile.get("experience_years", 0) or 0)
    expected_salary = "N/A"
    min_salary = 0
    max_salary = 0
    predicted_salary_num = 0
    
    if active_resume or profile.get("skills"):
        if exp_years > 5:
            min_salary, predicted_salary_num, max_salary = 150000, 180000, 220000
            expected_salary = "$180,000 / yr"
        elif exp_years > 3:
            min_salary, predicted_salary_num, max_salary = 120000, 145000, 175000
            expected_salary = "$145,000 / yr"
        else:
            min_salary, predicted_salary_num, max_salary = 90000, 115000, 140000
            expected_salary = "$115,000 / yr"

    # 7. AI Career Readiness Score
    if active_resume or detected_skills:
        readiness_score = int(round((ats_score * 0.35) + (skill_match_pct * 0.35) + (profile_completion * 0.30)))
        readiness_score = min(max(readiness_score, 0), 98)
    else:
        readiness_score = 0

    # 8. Resume Improvements Count / Tips
    improvement_tips = []
    if active_resume:
        improvement_tips = [
            "Include quantitative metrics (e.g. 'Improved efficiency by 30%') in project descriptions.",
            "Add containerization & cloud skills to boost ATS compatibility.",
            "Publish live demo links for engineering projects."
        ]
    else:
        improvement_tips = ["Upload a resume to generate personalized AI improvement recommendations."]

    # 9. Recent Activities
    activities = []
    try:
        activities = execute_query(
            "SELECT action, details, created_at FROM activity_logs WHERE user_id = %s ORDER BY id DESC LIMIT 5",
            (user_id,), fetchall=True
        ) or []
    except Exception:
        pass

    return {
        "user_name": full_name,
        "profile_completion": profile_completion,
        "active_resume_filename": active_resume.get("filename") if active_resume else "No active resume",
        "has_active_resume": bool(active_resume),
        "active_resume": active_resume,
        "resume_score": resume_score,
        "ats_score": ats_score,
        "resume_summary": resume_summary,
        "detected_skills": detected_skills,
        "detected_skills_count": len(detected_skills),
        "missing_skills": missing_skills,
        "missing_skills_count": len(missing_skills),
        "skill_match_pct": skill_match_pct,
        "skill_gap_pct": skill_gap_pct,
        "improvement_tips": improvement_tips,
        "top_job_title": top_job_title,
        "top_job_company": top_job_company,
        "top_job_match_pct": top_job_match_pct,
        "recommended_career": recommended_career,
        "career_growth": career_growth,
        "recommended_courses": rec_courses,
        "course_count": len(rec_courses),
        "certifications_count": len(certs),
        "projects_count": len(projects),
        "expected_salary": expected_salary,
        "min_salary": min_salary,
        "max_salary": max_salary,
        "predicted_salary_num": predicted_salary_num,
        "readiness_score": readiness_score,
        "recent_activities": activities
    }
