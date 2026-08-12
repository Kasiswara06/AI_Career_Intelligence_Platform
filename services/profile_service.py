import logging
from database.database import execute_query, get_user_projects, get_user_certificates

logger = logging.getLogger(__name__)

def calculate_profile_completion_details(user_id: int) -> dict:
    """
    Calculates dynamic profile completion breakdown based on required & optional sections.
    Section rules:
    - Personal Details: 15%
    - Education: 15%
    - Skills: 15%
    - Projects: 15% (At least 1 project)
    - Certificates: 15% (At least 1 certificate)
    - Active Resume: 15% (Exactly one active resume)
    - Professional Links: 10% (LinkedIn 4%, GitHub 4%, Portfolio 2%)
    """
    if not user_id:
        return {"percentage": 0, "checklist": {}}

    # Fetch records
    u = execute_query("SELECT full_name, email, mobile FROM users WHERE id = %s", (user_id,), fetchone=True) or {}
    p = execute_query("SELECT college, qualification, branch, skills, technical_skills, linkedin_url, github_url, portfolio_url FROM profiles WHERE user_id = %s", (user_id,), fetchone=True) or {}
    projects = get_user_projects(user_id)
    certs = get_user_certificates(user_id)
    active_resume = execute_query("SELECT id FROM resumes WHERE user_id = %s AND is_active = 1", (user_id,), fetchone=True)

    # Checklist evaluations
    has_personal = bool(u.get("full_name") and (u.get("email") or u.get("mobile")))
    has_education = bool(p.get("college") or p.get("qualification") or p.get("branch"))
    has_skills = bool((p.get("skills") or p.get("technical_skills") or "").strip())
    has_projects = len(projects) > 0
    has_certificates = len(certs) > 0
    has_resume = active_resume is not None
    has_linkedin = bool((p.get("linkedin_url") or "").strip())
    has_github = bool((p.get("github_url") or "").strip())
    has_portfolio = bool((p.get("portfolio_url") or "").strip())

    score = 0
    if has_personal: score += 15
    if has_education: score += 15
    if has_skills: score += 15
    if has_projects: score += 15
    if has_certificates: score += 15
    if has_resume: score += 15
    if has_linkedin: score += 4
    if has_github: score += 4
    if has_portfolio: score += 2

    score = min(100, score)

    return {
        "percentage": score,
        "checklist": {
            "Personal Details": has_personal,
            "Education": has_education,
            "Skills": has_skills,
            "Projects": {"status": has_projects, "count": len(projects)},
            "Certificates": {"status": has_certificates, "count": len(certs)},
            "Resume": has_resume,
            "LinkedIn": has_linkedin,
            "GitHub": has_github,
            "Portfolio": has_portfolio
        }
    }

def get_full_user_profile(user_id: int) -> dict:
    """
    Retrieves complete candidate profile data from database tables (users, profiles, resumes, projects, certificates).
    Returns structured dict with Personal Info, Education, Experience, Skills, Projects List, Certificates List, Active Resume, Links.
    """
    if not user_id:
        return {}

    # Query users table
    u = execute_query("SELECT * FROM users WHERE id = %s", (user_id,), fetchone=True) or {}

    # Query profiles table
    p = execute_query("SELECT * FROM profiles WHERE user_id = %s", (user_id,), fetchone=True) or {}

    # Query projects table
    projects_list = get_user_projects(user_id)

    # Query certificates table
    certificates_list = get_user_certificates(user_id)

    # Query single active resume table record
    active_resume = execute_query("SELECT * FROM resumes WHERE user_id = %s AND is_active = 1 ORDER BY uploaded_at DESC LIMIT 1", (user_id,), fetchone=True) or {}

    # Calculate completion
    completion_data = calculate_profile_completion_details(user_id)

    # Build full name & contact
    name = p.get("full_name") or u.get("full_name") or "Candidate Name"
    email = p.get("email") or u.get("email") or "candidate@example.com"
    phone = p.get("mobile") or p.get("mobile_number") or u.get("mobile") or ""
    
    city = p.get("city") or ""
    state = p.get("state") or ""
    country = p.get("country") or "India"
    pincode = p.get("pincode") or ""

    location_parts = [part for part in [city, state, country, pincode] if part]
    location_str = ", ".join(location_parts) if location_parts else "India"

    # Social links
    linkedin = p.get("linkedin_url") or p.get("linkedin") or ""
    github = p.get("github_url") or p.get("github") or ""
    portfolio = p.get("portfolio_url") or p.get("portfolio") or ""

    # Parse skills
    skills_raw = p.get("skills") or p.get("technical_skills") or ""
    soft_skills_raw = p.get("soft_skills") or ""
    
    tech_skills = []
    if isinstance(skills_raw, str) and skills_raw.strip():
        tech_skills = [s.strip() for s in skills_raw.replace(";", ",").split(",") if s.strip()]

    soft_skills = []
    if isinstance(soft_skills_raw, str) and soft_skills_raw.strip():
        soft_skills = [s.strip() for s in soft_skills_raw.replace(";", ",").split(",") if s.strip()]

    # Categorize skills dynamically
    tools_keywords = ["git", "github", "docker", "vs code", "vscode", "google cloud", "aws", "azure", "kubernetes", "postman", "jira"]
    tech_list = []
    tools_list = []

    for s in tech_skills:
        if any(tk in s.lower() for tk in tools_keywords):
            tools_list.append(s)
        else:
            tech_list.append(s)

    # Education parsing
    college = p.get("college") or p.get("university") or ""
    degree = p.get("qualification") or p.get("degree") or "Bachelor of Technology"
    specialization = p.get("branch") or p.get("specialization") or "Computer Science"
    cgpa = p.get("cgpa") or p.get("percentage") or ""
    grad_year = p.get("graduation_year") or p.get("passing_year") or ""

    # Experience parsing
    current_company = p.get("current_company") or ""
    current_role = p.get("current_role") or ""
    experience_years = float(p.get("experience_years") or 0.0)

    return {
        "user_id": user_id,
        "full_name": name,
        "email": email,
        "phone": phone,
        "dob": p.get("date_of_birth") or p.get("dob") or "",
        "gender": p.get("gender") or "",
        "address": p.get("address") or "",
        "city": city,
        "state": state,
        "country": country,
        "pincode": pincode,
        "location": location_str,
        "linkedin": linkedin,
        "github": github,
        "portfolio": portfolio,
        "college": college,
        "degree": degree,
        "specialization": specialization,
        "cgpa": cgpa,
        "graduation_year": grad_year,
        "current_company": current_company,
        "current_role": current_role,
        "experience_years": experience_years,
        "technical_skills": tech_list,
        "tools_and_technologies": tools_list,
        "soft_skills": soft_skills,
        "projects": projects_list,
        "certificates": certificates_list,
        "certifications_list": certificates_list,
        "active_resume": active_resume,
        "career_objective": p.get("career_objective") or "",
        "completion_percentage": completion_data["percentage"],
        "completion_checklist": completion_data["checklist"]
    }
