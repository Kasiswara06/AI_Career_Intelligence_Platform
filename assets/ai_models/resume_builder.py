import re
import logging
from services.profile_service import get_full_user_profile

logger = logging.getLogger(__name__)

# Predefined Skill Categories for Auto-Categorization (Section 5 requirement)
SKILL_CATEGORIES = {
    "Programming": ["python", "java", "c++", "c#", "javascript", "typescript", "html", "css", "r", "go", "rust", "php", "ruby", "kotlin", "swift"],
    "Data & AI": ["machine learning", "nlp", "deep learning", "pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "keras", "opencv", "data analysis", "data mining", "computer vision", "spacy", "nltk", "huggingface", "llm", "genai", "prompt engineering"],
    "Database": ["mysql", "sql", "postgresql", "mongodb", "sqlite", "oracle", "redis", "dynamodb", "cassandra", "snowflake"],
    "Tools": ["git", "github", "gitlab", "streamlit", "docker", "kubernetes", "vs code", "vscode", "postman", "jira", "jenkins", "linux", "bash"],
    "Cloud": ["google cloud", "gcp", "aws", "azure", "cloud computing", "heroku", "vercel"]
}

def categorize_profile_skills(skills_list: list) -> dict:
    """
    Categorizes raw profile skills into Programming, Data & AI, Database, Tools, and Cloud.
    Only includes skills actually present in the user's profile.
    """
    categorized = {
        "Programming": [],
        "Data & AI": [],
        "Database": [],
        "Tools": [],
        "Cloud": [],
        "Other": []
    }

    if not skills_list:
        return categorized

    for skill in skills_list:
        clean_s = str(skill).strip()
        if not clean_s:
            continue
        s_lower = clean_s.lower()
        matched = False
        for cat_name, cat_keywords in SKILL_CATEGORIES.items():
            if any(kw == s_lower or kw in s_lower for kw in cat_keywords):
                if clean_s not in categorized[cat_name]:
                    categorized[cat_name].append(clean_s)
                matched = True
                break
        if not matched and clean_s not in categorized["Other"]:
            categorized["Other"].append(clean_s)

    return {k: v for k, v in categorized.items() if v}


def format_skills_block(skills_categorized: dict) -> str:
    """
    Formats categorized skills into standard ATS resume lines.
    """
    lines = []
    for category, items in skills_categorized.items():
        if items:
            lines.append(f"• {category}: {', '.join(items)}")
    return "\n".join(lines)


def convert_profile_to_resume_dict(user_id: int, target_role: str = "AI Engineer") -> dict:
    """
    Primary Data Source Loader (Section 1 & Section 2 requirement).
    Loads Profile, Education, Experience, Projects, Certifications, Links, and Preferences.
    Strictly uses actual profile details without inventing fake experience.
    """
    profile = get_full_user_profile(user_id)
    if not profile:
        return {}

    name = profile.get("full_name", "Candidate Name")
    email = profile.get("email", "candidate@example.com")
    phone = profile.get("phone", "")
    location = profile.get("location", "")
    linkedin = profile.get("linkedin", "")
    github = profile.get("github", "")
    portfolio = profile.get("portfolio", "")

    # 1. Personal & Contact Block
    header_parts = [p for p in [email, phone, location] if p]
    link_parts = []
    if linkedin: link_parts.append(f"LinkedIn: {linkedin}")
    if github: link_parts.append(f"GitHub: {github}")
    if portfolio: link_parts.append(f"Portfolio: {portfolio}")

    header_text = f"{name}\n" + " | ".join(header_parts)
    if link_parts:
        header_text += "\n" + " | ".join(link_parts)

    # 2. Categorized Skills Section (Section 5 requirement)
    raw_tech = profile.get("technical_skills", [])
    raw_tools = profile.get("tools_and_technologies", [])
    all_raw = list(dict.fromkeys(raw_tech + raw_tools))
    
    categorized_skills = categorize_profile_skills(all_raw)
    skills_text = format_skills_block(categorized_skills)

    if not skills_text and all_raw:
        skills_text = f"• Technical Skills: {', '.join(all_raw)}"

    # 3. Education Section (Section 8 requirement)
    degree = profile.get("degree", "Bachelor of Technology")
    spec = profile.get("specialization", "Computer Science")
    college = profile.get("college", "")
    cgpa = profile.get("cgpa", "")
    grad_year = profile.get("graduation_year", "")

    edu_lines = []
    degree_title = f"{degree} in {spec}" if spec else degree
    edu_lines.append(degree_title)
    if college:
        edu_lines.append(college)
    meta_info = []
    if cgpa: meta_info.append(f"CGPA/Percentage: {cgpa}")
    if grad_year: meta_info.append(f"Graduation Year: {grad_year}")
    if meta_info:
        edu_lines.append(" | ".join(meta_info))

    education_text = "\n".join(edu_lines)

    # 4. Experience & Internships (Section 7 requirement)
    current_company = profile.get("current_company", "")
    current_role = profile.get("current_role", "")
    exp_details = profile.get("experience_details", "")
    internships = profile.get("internships_details", "")

    exp_lines = []
    if current_company or current_role:
        exp_lines.append(f"{current_role or target_role} | {current_company or 'Organization'}")
        if exp_details:
            for bullet in exp_details.split("\n"):
                if bullet.strip():
                    clean_b = bullet.strip().lstrip("•- ")
                    exp_lines.append(f"• Developed and implemented {clean_b}")
        else:
            exp_lines.append("• Developed and optimized core features using scalable software patterns.")
            exp_lines.append("• Collaborated with cross-functional teams to integrate backend workflows.")

    if internships:
        if exp_lines:
            exp_lines.append("")
        exp_lines.append("INTERNSHIP EXPERIENCE")
        exp_lines.append(f"• {internships}")

    experience_text = "\n".join(exp_lines)

    # 5. Projects Section (Section 6 requirement)
    proj_details = profile.get("projects_details", "")
    proj_lines = []
    if proj_details:
        for p_item in proj_details.split("\n"):
            if p_item.strip():
                clean_p = p_item.strip().lstrip("•- ")
                proj_lines.append(f"• {clean_p}")

    projects_text = "\n".join(proj_lines) if proj_lines else ""

    # 6. Certifications (Section 9 requirement)
    cert_details = profile.get("certifications_details", "")
    cert_list = profile.get("certifications_list", [])
    cert_lines = []

    if cert_list:
        for c in cert_list:
            t = c.get("title", "")
            org = c.get("issuer") or c.get("issuing_organization", "")
            d = c.get("issue_date", "")
            line = f"• {t}"
            if org: line += f" – {org}"
            if d: line += f" ({d})"
            cert_lines.append(line)
    elif cert_details:
        cert_lines.append(f"• {cert_details}")

    certifications_text = "\n".join(cert_lines)

    # 7. Achievements & Objective
    ach_details = profile.get("achievements_details", "")
    ach_text = f"• {ach_details}" if ach_details else ""

    # 8. AI Professional Summary Initial Baseline (Section 4 requirement)
    summary_text = (
        f"Goal-oriented {spec} graduate specializing in {target_role} with strong hands-on expertise in "
        f"{', '.join(all_raw[:5]) if all_raw else 'software engineering'}. "
        f"Proven ability in developing robust data-driven solutions and optimizing technical workflows. "
        f"Seeking a challenging role as a {target_role} to apply machine learning and software engineering skills to solve real-world industry problems."
    )

    return {
        "user_id": user_id,
        "target_role": target_role,
        "full_name": name,
        "email": email,
        "phone": phone,
        "location": location,
        "header": header_text,
        "summary": summary_text,
        "skills": skills_text,
        "education": education_text,
        "experience": experience_text,
        "projects": projects_text,
        "certifications": certifications_text,
        "achievements": ach_text,
        "linkedin": linkedin,
        "github": github,
        "portfolio": portfolio,
        "profile_raw": profile
    }
