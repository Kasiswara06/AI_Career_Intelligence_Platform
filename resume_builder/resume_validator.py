import logging

logger = logging.getLogger(__name__)

def validate_resume_data(resume_dict: dict) -> dict:
    """
    Validates profile completeness for resume building.
    Returns status dict with boolean valid flag and list of missing key profile sections.
    """
    missing = []
    if not resume_dict.get("full_name") or resume_dict.get("full_name") == "Candidate Name":
        missing.append("Full Name")
    if not resume_dict.get("email") or "@" not in resume_dict.get("email"):
        missing.append("Email Address")
    if not resume_dict.get("education"):
        missing.append("Education Details")
    if not resume_dict.get("skills"):
        missing.append("Technical Skills")

    warnings = []
    if not resume_dict.get("experience"):
        warnings.append("No work experience listed (Fresher mode active)")
    if not resume_dict.get("projects"):
        warnings.append("No projects listed in profile")
    if not resume_dict.get("certifications"):
        warnings.append("No certifications listed in profile")

    return {
        "is_valid": len(missing) == 0,
        "missing_critical": missing,
        "warnings": warnings
    }
