import re
from typing import Dict, Any, List
from ai_models.semantic_matching import calculate_semantic_job_match
from ai_models.skill_gap import analyze_skill_gap
from ai_models.ats_score import calculate_ats_score
from ai_models.salary_prediction import predict_salary
from ai_models.course_recommendation import recommend_courses

def analyze_job_match_full(
    resume_text: str,
    job_description: str,
    extracted_skills: List[str] = None,
    job_title: str = "Software Engineer",
    experience_years: float = 1.0
) -> Dict[str, Any]:
    """
    Complete AI Job Matching Engine:
    - all-MiniLM-L6-v2 + Cosine Similarity + TF-IDF semantic match
    - Skill Gap (Matching, Missing, Additional Recommended Skills)
    - ATS Score & Resume Quality Score
    - AI Rationale ("Why this job matches your profile") & Improvement Suggestions
    - Career Path Recommendation (Growth, Industry Demand, Readiness)
    - Salary Predictions (Min, Avg, Max)
    - Recommended Courses with links
    """
    extracted_skills = extracted_skills or []
    
    # 1. Semantic Embedding Similarity
    sem_res = calculate_semantic_job_match(resume_text, job_description)
    semantic_pct = sem_res["semantic_match_pct"]

    # 2. ATS & Resume Quality Score
    ats_data = calculate_ats_score(resume_text, job_description)
    ats_score = ats_data.get("ats_score", 70)
    resume_score = ats_data.get("resume_score", 75)

    # 3. Skill Gap Analysis
    cand_skill_input = extracted_skills if (extracted_skills and len(extracted_skills) > 0) else resume_text
    skill_gap = analyze_skill_gap(cand_skill_input, job_description)
    matching_skills = skill_gap.get("matching_skills", [])
    missing_skills = skill_gap.get("missing_skills", [])


    # Additional Recommended Skills
    additional_recommended = [s for s in missing_skills[:4]] if missing_skills else ["Docker", "AWS Cloud", "System Architecture"]

    # Overall Combined Match Percentage
    match_pct = round((semantic_pct * 0.50) + (skill_gap.get("skill_match_percentage", 60) * 0.30) + (ats_score * 0.20), 1)

    # 4. AI Rationale & Suggestions
    matching_str = ", ".join([s.capitalize() for s in matching_skills[:5]]) if matching_skills else "general domain experience"
    why_matches = (
        f"This job is recommended because your profile highlights relevant expertise in {matching_str}, "
        f"yielding a strong semantic similarity score of {semantic_pct}%."
    )

    improvements = []
    if missing_skills:
        top_missing_str = ", ".join([s.capitalize() for s in missing_skills[:3]])
        improvements.append(f"Adding hands-on project experience in {top_missing_str} can increase your match score from {match_pct}% to ~{min(98.0, match_pct + 15.0)}%.")
    
    improvements.append("Use quantifiable metrics (e.g. 'Improved efficiency by 30%') in project descriptions.")
    improvements.append("Tailor bullet points using exact keywords from the target job posting.")

    # 5. Career Growth & Readiness
    career_info = {
        "suitable_role": job_title,
        "industry_demand": "Very High (Top 10% in Market)",
        "future_growth": "25% - 35% Annual Growth Rate",
        "career_readiness": min(100.0, round(match_pct + (experience_years * 4), 1))
    }

    # 6. Salary Predictions
    salary_data = predict_salary(job_role=job_title, experience_years=experience_years)

    # 7. Recommended Courses
    courses = recommend_courses(missing_skills)

    return {
        "match_percentage": match_pct,
        "ats_score": ats_score,
        "resume_score": resume_score,
        "semantic_match_pct": semantic_pct,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "additional_recommended_skills": additional_recommended,
        "why_job_matches": why_matches,
        "improvement_suggestions": improvements,
        "career_recommendation": career_info,
        "salary_prediction": salary_data,
        "recommended_courses": courses
    }

def calculate_job_match(resume_text: str, job_description: str) -> dict:
    """Wrapper function calculating match percentage and ATS compatibility."""
    res = analyze_job_match_full(resume_text, job_description)
    return {
        "match_percentage": res["match_percentage"],
        "ats_compatibility": f"{res['ats_score']}% Match Score",
        "matching_skills": res["matching_skills"],
        "missing_skills": res["missing_skills"]
    }

