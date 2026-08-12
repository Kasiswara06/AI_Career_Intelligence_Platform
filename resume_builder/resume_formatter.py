import logging
from resume_builder.template_manager import render_resume_html_template

logger = logging.getLogger(__name__)

def format_resume_as_plain_text(resume_dict: dict) -> str:
    """
    Formats structured resume dict as clean, plain text for TXT export.
    """
    lines = []
    lines.append(f"{resume_dict.get('full_name', '').upper()}")
    
    contact_parts = [p for p in [resume_dict.get('email'), resume_dict.get('phone'), resume_dict.get('location')] if p]
    if contact_parts:
        lines.append(" | ".join(contact_parts))

    link_parts = []
    if resume_dict.get("linkedin"): link_parts.append(f"LinkedIn: {resume_dict['linkedin']}")
    if resume_dict.get("github"): link_parts.append(f"GitHub: {resume_dict['github']}")
    if link_parts:
        lines.append(" | ".join(link_parts))

    lines.append("=" * 60)

    for sec, title in [
        ("summary", "PROFESSIONAL SUMMARY"),
        ("skills", "TECHNICAL SKILLS"),
        ("education", "EDUCATION"),
        ("experience", "PROFESSIONAL EXPERIENCE"),
        ("projects", "KEY PROJECTS"),
        ("certifications", "CERTIFICATIONS"),
        ("achievements", "ACHIEVEMENTS")
    ]:
        val = resume_dict.get(sec)
        if val:
            lines.append(f"\n{title}\n" + "-" * len(title))
            lines.append(val)

    return "\n".join(lines)
