import os
import logging

logger = logging.getLogger(__name__)

TEMPLATES = [
    "Modern ATS",
    "Professional",
    "Minimal",
    "Technical",
    "Fresher",
    "Experienced"
]

def render_resume_html_template(resume_dict: dict, template_name: str = "Modern ATS") -> str:
    """
    Renders styled HTML string for live preview and export across 6 ATS-friendly templates (Section 12 requirement).
    Avoids complex graphics, icons, or embedded text that interfere with ATS parsing.
    """
    name = resume_dict.get("full_name", "Candidate Name")
    email = resume_dict.get("email", "")
    phone = resume_dict.get("phone", "")
    loc = resume_dict.get("location", "")
    linkedin = resume_dict.get("linkedin", "")
    github = resume_dict.get("github", "")
    portfolio = resume_dict.get("portfolio", "")

    contact_parts = [p for p in [email, phone, loc] if p]
    contact_line = " | ".join(contact_parts)

    link_parts = []
    if linkedin: link_parts.append(f"LinkedIn: {linkedin}")
    if github: link_parts.append(f"GitHub: {github}")
    if portfolio: link_parts.append(f"Portfolio: {portfolio}")
    links_line = " | ".join(link_parts)

    summary = resume_dict.get("summary", "")
    skills = resume_dict.get("skills", "")
    education = resume_dict.get("education", "")
    experience = resume_dict.get("experience", "")
    projects = resume_dict.get("projects", "")
    certifications = resume_dict.get("certifications", "")
    achievements = resume_dict.get("achievements", "")

    # Theme Styling Configurations
    theme_color = "#1E293B"
    border_style = "2px solid #1E293B"
    font_family = "'Inter', Arial, sans-serif"
    header_align = "center"

    if template_name == "Modern ATS":
        theme_color = "#2563EB"
        border_style = "2px solid #2563EB"
        font_family = "'Helvetica Neue', Arial, sans-serif"
        header_align = "left"
    elif template_name == "Professional":
        theme_color = "#0F766E"
        border_style = "2px solid #0F766E"
        font_family = "Georgia, serif"
        header_align = "center"
    elif template_name == "Minimal":
        theme_color = "#475569"
        border_style = "1px solid #94A3B8"
        font_family = "Calibri, sans-serif"
        header_align = "left"
    elif template_name == "Technical":
        theme_color = "#0D9488"
        border_style = "2px solid #0D9488"
        font_family = "'Segoe UI', Roboto, sans-serif"
        header_align = "left"
    elif template_name == "Fresher":
        theme_color = "#7C3AED"
        border_style = "2px solid #7C3AED"
        font_family = "Arial, sans-serif"
        header_align = "center"
    elif template_name == "Experienced":
        theme_color = "#1E3A8A"
        border_style = "2px solid #1E3A8A"
        font_family = "Trebuchet MS, sans-serif"
        header_align = "left"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: {font_family}; margin: 24px; color: #0F172A; background: #FFFFFF; line-height: 1.5; font-size: 13px; }}
            .header {{ text-align: {header_align}; border-bottom: {border_style}; padding-bottom: 10px; margin-bottom: 16px; }}
            .name {{ font-size: 24px; font-weight: 800; text-transform: uppercase; color: #0F172A; margin: 0; letter-spacing: 0.5px; }}
            .contact {{ font-size: 12px; color: #475569; margin-top: 4px; }}
            .section-title {{ font-size: 14px; font-weight: 700; text-transform: uppercase; border-bottom: 1px solid #E2E8F0; padding-bottom: 3px; margin-top: 16px; margin-bottom: 8px; color: {theme_color}; letter-spacing: 0.5px; }}
            .content {{ font-size: 13px; color: #334155; white-space: pre-line; margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="name">{name}</div>
            <div class="contact">{contact_line}</div>
            {"<div class='contact'>" + links_line + "</div>" if links_line else ""}
        </div>
    """

    # Section Rendering Order depending on Template
    if template_name in ["Fresher", "Technical"]:
        # Put Education and Skills first for Freshers / Technical
        sections_order = [
            ("CAREER OBJECTIVE" if template_name == "Fresher" else "PROFESSIONAL SUMMARY", summary),
            ("TECHNICAL SKILLS", skills),
            ("EDUCATION", education),
            ("KEY PROJECTS", projects),
            ("PROFESSIONAL EXPERIENCE", experience),
            ("CERTIFICATIONS", certifications),
            ("ACHIEVEMENTS", achievements)
        ]
    else:
        # Standard Experienced / Modern ATS Order
        sections_order = [
            ("PROFESSIONAL SUMMARY", summary),
            ("TECHNICAL SKILLS", skills),
            ("PROFESSIONAL EXPERIENCE", experience),
            ("KEY PROJECTS", projects),
            ("EDUCATION", education),
            ("CERTIFICATIONS", certifications),
            ("ACHIEVEMENTS", achievements)
        ]

    for title, content in sections_order:
        if content and content.strip():
            html += f"""<div class="section-title">{title}</div><div class="content">{content}</div>"""

    html += """</body></html>"""
    return html
