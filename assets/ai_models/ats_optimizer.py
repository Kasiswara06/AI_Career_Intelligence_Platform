import logging
from ai_models.resume_keyword_analyzer import analyze_target_role_keywords

logger = logging.getLogger(__name__)

def evaluate_resume_ats_scores(resume_dict: dict, full_resume_text: str, target_role: str = "AI Engineer", job_description: str = "") -> dict:
    """
    Evaluates comprehensive ATS scores, Detected Keywords, Missing Keywords, Completeness %,
    Strengths, Weaknesses, and Actionable AI Suggestions (Section 10 & 11 requirement).
    """
    kw_res = analyze_target_role_keywords(full_resume_text, target_role=target_role, job_description=job_description)

    # 1. Section Completeness Check
    has_summary = bool(resume_dict.get("summary", "").strip())
    has_skills = bool(resume_dict.get("skills", "").strip())
    has_edu = bool(resume_dict.get("education", "").strip())
    has_exp = bool(resume_dict.get("experience", "").strip())
    has_proj = bool(resume_dict.get("projects", "").strip())
    has_cert = bool(resume_dict.get("certifications", "").strip())
    has_links = bool(resume_dict.get("linkedin", "").strip() or resume_dict.get("github", "").strip() or resume_dict.get("portfolio", "").strip())

    sections_present = sum([has_summary, has_skills, has_edu, has_exp, has_proj, has_cert, has_links])
    completeness_pct = int((sections_present / 7.0) * 100)

    # 2. Sub-Score Calculations
    skills_score = 92 if has_skills else 50
    education_score = 95 if has_edu else 40
    experience_score = 88 if has_exp else 70
    projects_score = 90 if has_proj else 60
    formatting_score = 94 if len(full_resume_text) > 250 else 65
    keyword_score = kw_res.get("match_score", 85)

    # Overall ATS Score
    ats_score = int(
        (skills_score * 0.25) +
        (keyword_score * 0.25) +
        (education_score * 0.15) +
        (experience_score * 0.15) +
        (projects_score * 0.10) +
        (formatting_score * 0.10)
    )

    # 3. AI Strengths Analysis (Section 11 requirement)
    strengths = []
    if has_skills:
        strengths.append("Strong technical skill set structured for ATS parsers.")
    if has_proj:
        strengths.append("Relevant project experience with clear technologies listed.")
    if has_edu:
        strengths.append("Verified academic degree and specialization.")
    if has_cert:
        strengths.append("Industry certification credentials present in profile.")
    if keyword_score >= 80:
        strengths.append(f"High keyword alignment with target role ({target_role}).")

    if not strengths:
        strengths.append("Clean, readable baseline structure suitable for ATS parsers.")

    # 4. AI Weaknesses Analysis (Section 11 requirement)
    weaknesses = []
    if kw_res.get("missing_keywords"):
        missing_str = ", ".join(kw_res["missing_keywords"][:3])
        weaknesses.append(f"Missing target-role keywords: {missing_str}")
    if not has_proj:
        weaknesses.append("Missing project descriptions to showcase practical application.")
    if not has_links:
        weaknesses.append("Missing online portfolio / GitHub / LinkedIn profile links.")
    if not has_cert:
        weaknesses.append("No active certifications detected in profile.")

    # 5. AI Suggestions (Section 11 requirement)
    suggestions = [
        "Use strong action verbs (Developed, Implemented, Designed, Optimized) at the start of experience bullet points.",
        "Ensure technical skills are clearly categorized into Programming, Data & AI, Database, and Tools.",
        "Add measurable achievements or project outcomes where available (e.g. 'Improved efficiency by 20%')."
    ]
    if not has_links:
        suggestions.append("Add LinkedIn and GitHub links to boost candidate credibility.")
    if kw_res.get("missing_keywords"):
        suggestions.append(f"Consider acquiring recommended skills: {', '.join(kw_res['recommended_skills_to_learn'][:3])}.")

    return {
        "ats_score": ats_score,
        "resume_score": int((ats_score + keyword_score) / 2),
        "keyword_score": keyword_score,
        "skills_score": skills_score,
        "education_score": education_score,
        "experience_score": experience_score,
        "projects_score": projects_score,
        "formatting_score": formatting_score,
        "completeness_pct": completeness_pct,
        "detected_keywords": kw_res.get("detected_keywords", []),
        "missing_keywords": kw_res.get("missing_keywords", []),
        "recommended_skills_to_learn": kw_res.get("recommended_skills_to_learn", []),
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions
    }
