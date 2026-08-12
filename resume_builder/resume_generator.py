import logging
from resume_builder.profile_to_resume import convert_profile_to_resume_dict

logger = logging.getLogger(__name__)

def generate_standard_resume_sections(user_id: int, target_role: str = "AI Engineer") -> dict:
    """
    Generates standardized resume section content from DB profile data.
    Enforces exact ordering:
    1. Header / Contact Information
    2. Professional Summary
    3. Technical Skills
    4. Education
    5. Experience / Internships
    6. Projects
    7. Certifications
    8. Achievements
    """
    resume_dict = convert_profile_to_resume_dict(user_id, target_role=target_role)

    # Format complete plain text resume
    full_text_blocks = []
    
    # 1. Header
    if resume_dict.get("header"):
        full_text_blocks.append(resume_dict["header"])
        full_text_blocks.append("-" * 50)

    # 2. Professional Summary
    if resume_dict.get("summary"):
        full_text_blocks.append("PROFESSIONAL SUMMARY")
        full_text_blocks.append(resume_dict["summary"])
        full_text_blocks.append("")

    # 3. Technical Skills
    if resume_dict.get("skills"):
        full_text_blocks.append("TECHNICAL SKILLS")
        full_text_blocks.append(resume_dict["skills"])
        full_text_blocks.append("")

    # 4. Education
    if resume_dict.get("education"):
        full_text_blocks.append("EDUCATION")
        full_text_blocks.append(resume_dict["education"])
        full_text_blocks.append("")

    # 5. Experience / Internships
    if resume_dict.get("experience"):
        full_text_blocks.append("PROFESSIONAL EXPERIENCE")
        full_text_blocks.append(resume_dict["experience"])
        full_text_blocks.append("")

    # 6. Projects
    if resume_dict.get("projects"):
        full_text_blocks.append(resume_dict["projects"])
        full_text_blocks.append("")

    # 7. Certifications
    if resume_dict.get("certifications"):
        full_text_blocks.append("CERTIFICATIONS")
        full_text_blocks.append(resume_dict["certifications"])
        full_text_blocks.append("")

    # 8. Achievements
    if resume_dict.get("achievements"):
        full_text_blocks.append("ACHIEVEMENTS")
        full_text_blocks.append(resume_dict["achievements"])
        full_text_blocks.append("")

    plain_resume_text = "\n".join(full_text_blocks)

    return {
        "user_id": user_id,
        "target_role": target_role,
        "sections": resume_dict,
        "full_text": plain_resume_text
    }
