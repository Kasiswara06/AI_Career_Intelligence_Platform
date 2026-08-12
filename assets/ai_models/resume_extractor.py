import re
from typing import Dict, List, Any
from ai_models.resume_parser import (
    parse_resume_file, extract_email, extract_phone,
    extract_urls, extract_skills, extract_experience_years
)

def extract_education(text: str) -> List[str]:
    """Extracts education degrees and institutions from text."""
    degrees = []
    degree_keywords = ["B.Tech", "B.E.", "B.S.", "M.Tech", "M.S.", "Ph.D", "Bachelor", "Master", "Diploma", "B.C.A", "M.C.A"]
    for kw in degree_keywords:
        if re.search(r'\b' + re.escape(kw) + r'\b', text, re.IGNORECASE):
            degrees.append(kw)
    return list(set(degrees))

def extract_structured_resume(file_path_or_text: str) -> Dict[str, Any]:
    """
    Parses resume text or file path into a structured JSON dictionary.
    """
    if file_path_or_text.endswith(".pdf") or file_path_or_text.endswith(".docx") or file_path_or_text.endswith(".txt"):
        text = parse_resume_file(file_path_or_text)
    else:
        text = file_path_or_text

    email = extract_email(text)
    phone = extract_phone(text)
    linkedin, github, portfolio = extract_urls(text)
    skills = extract_skills(text)
    experience_years = extract_experience_years(text)
    education = extract_education(text)

    return {
        "raw_text": text,
        "email": email,
        "phone": phone,
        "linkedin": linkedin,
        "github": github,
        "portfolio": portfolio,
        "skills": skills,
        "experience_years": experience_years,
        "education": education,
    }
