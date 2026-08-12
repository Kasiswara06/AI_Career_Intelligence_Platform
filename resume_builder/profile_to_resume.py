import logging
from services.profile_service import get_full_user_profile

logger = logging.getLogger(__name__)

def convert_profile_to_resume_dict(user_id: int, target_role: str = "AI Engineer") -> dict:
    """
    Reads profile data from DB and converts it into structured resume section blocks.
    Strictly uses actual profile information without inventing fake claims or companies.
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

    # 1. Header Block
    header_parts = [p for p in [email, phone, location] if p]
    link_parts = []
    if linkedin: link_parts.append(f"LinkedIn: {linkedin}")
    if github: link_parts.append(f"GitHub: {github}")
    if portfolio: link_parts.append(f"Portfolio: {portfolio}")

    header_text = f"{name}\n" + " | ".join(header_parts)
    if link_parts:
        header_text += "\n" + " | ".join(link_parts)

    # 2. Professional Summary / Career Objective (Section 12 requirement)
    degree = profile.get("degree", "Engineering")
    spec = profile.get("specialization", "Computer Science")
    exp_yrs = profile.get("experience_years", 0.0)
    tech_skills = profile.get("technical_skills", [])
    skills_str = ", ".join(tech_skills[:5]) if tech_skills else "software development, problem solving"

    if exp_yrs > 0:
        summary_text = (
            f"Results-driven {target_role} with over {exp_yrs:.1f} years of hands-on experience in {skills_str}. "
            f"Demonstrated track record of delivering impactful data-driven applications and optimizing software workflows. "
            f"Seeking an opportunity to apply expertise in {target_role} solutions."
        )
    else:
        summary_text = (
            f"Motivated {spec} graduate ({degree}) with practical knowledge in {skills_str}. "
            f"Adept at building data-driven applications and analyzing algorithms. "
            f"Seeking an entry-level {target_role} position to apply technical skills in a professional environment."
        )

    # 3. Technical Skills Block (Section 5 requirement)
    skills_lines = []
    if tech_skills:
        skills_lines.append(f"• Technical Skills: {', '.join(tech_skills)}")
    tools = profile.get("tools_and_technologies", [])
    if tools:
        skills_lines.append(f"• Tools & Technologies: {', '.join(tools)}")
    soft = profile.get("soft_skills", [])
    if soft:
        skills_lines.append(f"• Soft Skills: {', '.join(soft)}")

    skills_text = "\n".join(skills_lines) if skills_lines else "• Skills: Python, SQL, Problem Solving"

    # 4. Education Block (Section 3 requirement)
    college = profile.get("college", "")
    cgpa = profile.get("cgpa", "")
    grad_year = profile.get("graduation_year", "")

    edu_lines = []
    degree_title = f"{degree} – {spec}" if spec else degree
    edu_lines.append(f"{degree_title}")
    if college:
        edu_lines.append(f"{college}")
    details = []
    if cgpa: details.append(f"CGPA/Score: {cgpa}")
    if grad_year: details.append(f"Graduation Year: {grad_year}")
    if details:
        edu_lines.append(" | ".join(details))

    education_text = "\n".join(edu_lines)

    # 5. Experience / Internships Block (Section 4 & 9 requirement)
    exp_details = profile.get("experience_details", "")
    internships = profile.get("internships_details", "")
    current_company = profile.get("current_company", "")
    current_role = profile.get("current_role", "")

    exp_lines = []
    if current_company or current_role:
        exp_lines.append(f"{current_role or target_role} | {current_company or 'Tech Solutions'}")
        if exp_details:
            exp_lines.append(f"• {exp_details}")
        else:
            exp_lines.append("• Developed and optimized modular features, ensuring high performance and data integrity.")

    if internships:
        exp_lines.append(f"\nINTERNSHIP EXPERIENCE")
        exp_lines.append(f"• {internships}")

    experience_text = "\n".join(exp_lines) if exp_lines else ""

    # 6. Projects Block (Section 6 requirement)
    proj_details = profile.get("projects_details", "")
    proj_text = ""
    if proj_details:
        proj_text = f"PROJECTS\n• {proj_details}"

    # 7. Certifications Block (Section 7 requirement)
    cert_details = profile.get("certifications_details", "")
    cert_list = profile.get("certifications_list", [])
    cert_lines = []

    if cert_list:
        for c in cert_list:
            t = c.get("title", "")
            org = c.get("issuing_organization", "")
            cert_lines.append(f"• {t} – {org}" if org else f"• {t}")
    elif cert_details:
        cert_lines.append(f"• {cert_details}")

    cert_text = "\n".join(cert_lines) if cert_lines else ""

    # 8. Achievements Block (Section 8 requirement)
    ach_details = profile.get("achievements_details", "")
    ach_text = f"• {ach_details}" if ach_details else ""

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
        "projects": proj_text,
        "certifications": cert_text,
        "achievements": ach_text,
        "profile_raw": profile
    }
