import logging
from database.database import execute_query

logger = logging.getLogger(__name__)

DOMAINS = [
    "Python Development",
    "Java Development",
    "Data Science",
    "Data Analytics",
    "Machine Learning",
    "Artificial Intelligence",
    "Deep Learning",
    "NLP",
    "Web Development",
    "Full Stack Development",
    "Backend Development",
    "Frontend Development",
    "SQL & Database",
    "Cloud Computing",
    "DevOps",
    "Cyber Security",
    "Software Testing",
    "Data Engineering",
    "Other"
]

TARGET_ROLES = [
    "Python Developer",
    "Java Developer",
    "Data Analyst",
    "Data Scientist",
    "Machine Learning Engineer",
    "AI Engineer",
    "NLP Engineer",
    "Full Stack Developer",
    "Backend Developer",
    "Frontend Developer",
    "Cloud Engineer",
    "DevOps Engineer",
    "Data Engineer",
    "Software Engineer",
    "Other"
]

EXPERIENCE_LEVEL_OPTIONS = ["Entry Level (0-2 yrs)", "Mid Level (2-5 yrs)", "Senior Level (5-8 yrs)", "Lead / Architect (8+ yrs)"]
DIFFICULTY_OPTIONS = ["🟢 Easy", "🟡 Medium", "🔴 Hard", "🔥 Mixed"]
QUESTION_TYPE_OPTIONS = ["Technical", "HR", "Behavioral", "Coding", "Scenario-Based", "Project-Based", "Resume-Based", "Mixed"]
QUESTION_COUNT_OPTIONS = [5, 10, 15, 20]

def clean_difficulty_str(diff: str) -> str:
    """Strips emoji prefix from difficulty string if present."""
    if not diff:
        return "Medium"
    for d in ["Easy", "Medium", "Hard", "Mixed"]:
        if d.lower() in diff.lower():
            return d
    return diff.strip()

def get_user_active_resume_data(user_id: int) -> dict:
    """
    Fetches the candidate's active uploaded resume text and structured profile details.
    Combines Resume, Profile, Skills, Education, Experience, Projects table records, Certifications table records.
    """
    if not user_id:
        return {}

    user = execute_query("SELECT full_name, email FROM users WHERE id = %s", (user_id,), fetchone=True) or {}
    profile = execute_query(
        """
        SELECT qualification, branch, college, university, graduation_year, cgpa,
               skills, technical_skills, soft_skills, experience_years, current_company,
               current_role, previous_companies, projects, certifications, career_objective
        FROM profiles WHERE user_id = %s
        """,
        (user_id,), fetchone=True
    ) or {}

    resume = execute_query(
        "SELECT filename, resume_name, extracted_text, uploaded_at FROM resumes WHERE user_id = %s AND is_active = 1 ORDER BY uploaded_at DESC",
        (user_id,), fetchone=True
    ) or execute_query(
        "SELECT filename, resume_name, extracted_text, uploaded_at FROM resumes WHERE user_id = %s ORDER BY uploaded_at DESC",
        (user_id,), fetchone=True
    ) or {}

    # Query projects table
    from database.database import get_user_projects, get_user_certificates
    projects_rows = get_user_projects(user_id)
    cert_rows = get_user_certificates(user_id)

    formatted_projects = []
    for p in projects_rows:
        p_str = f"Project: {p.get('project_name')} | Role: {p.get('project_role', 'Developer')} | Tech: {p.get('technologies', 'N/A')} | Desc: {p.get('description', '')}"
        if p.get('project_outcome'):
            p_str += f" | Outcome: {p.get('project_outcome')}"
        formatted_projects.append(p_str)

    projects_summary = "\n".join(formatted_projects) if formatted_projects else (profile.get("projects") or "")

    formatted_certs = []
    for c in cert_rows:
        c_title = c.get("certificate_name") or c.get("title", "")
        c_issuer = c.get("issuing_organization") or c.get("issuer", "")
        if c_title:
            formatted_certs.append(f"{c_title} (Issued by: {c_issuer})")

    certifications_summary = ", ".join(formatted_certs) if formatted_certs else (profile.get("certifications") or "")

    raw_skills = profile.get("technical_skills") or profile.get("skills") or ""
    skills_list = [s.strip() for s in raw_skills.split(",") if s.strip()]

    # Append technologies from projects if available
    for p in projects_rows:
        p_techs = [t.strip() for t in (p.get("technologies") or "").split(",") if t.strip()]
        for pt in p_techs:
            if pt.lower() not in [s.lower() for s in skills_list]:
                skills_list.append(pt)

    # If profile skills empty, try extracting from resume text
    extracted_text = resume.get("extracted_text", "") or ""
    if not skills_list and extracted_text:
        keywords = ["Python", "Java", "SQL", "Machine Learning", "Data Analysis", "React", "AWS", "Docker", "Git", "TensorFlow", "Pandas", "Scikit-Learn"]
        skills_list = [kw for kw in keywords if kw.lower() in extracted_text.lower()]

    res_name = resume.get("filename") or resume.get("resume_name") or "No active resume uploaded"

    return {
        "candidate_name": user.get("full_name") or "Candidate",
        "active_resume_file": res_name,
        "extracted_text": (extracted_text or "")[:3000],
        "skills": skills_list if skills_list else ["General Software Development"],
        "education": f"{profile.get('qualification') or ''} in {profile.get('branch') or ''} ({profile.get('college') or ''})".strip(" in ()"),
        "experience": f"{profile.get('experience_years') or 0} years as {profile.get('current_role') or 'Engineer'}",
        "projects": projects_summary,
        "projects_list": projects_rows,
        "certifications": certifications_summary,
        "certifications_list": cert_rows,
        "current_role": profile.get("current_role") or ""
    }

def get_badge_styles(domain: str, difficulty: str):
    """Returns CSS styles and icons for domain and difficulty badges."""
    diff_clean = clean_difficulty_str(difficulty)
    
    if diff_clean == "Easy":
        diff_color = "#10B981"
        diff_icon = "🟢"
    elif diff_clean == "Hard":
        diff_color = "#EF4444"
        diff_icon = "🔴"
    elif diff_clean == "Mixed":
        diff_color = "#8B5CF6"
        diff_icon = "🔥"
    else:
        diff_color = "#F59E0B"
        diff_icon = "🟡"

    return {
        "diff_color": diff_color,
        "diff_icon": diff_icon,
        "diff_clean": diff_clean
    }
