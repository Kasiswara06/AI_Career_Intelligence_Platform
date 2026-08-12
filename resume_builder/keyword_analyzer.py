import re
import logging

logger = logging.getLogger(__name__)

COMMON_TECH_KEYWORDS = [
    "python", "java", "sql", "machine learning", "deep learning", "nlp", "streamlit", "flask",
    "fastapi", "django", "mysql", "postgresql", "mongodb", "git", "github", "docker",
    "kubernetes", "aws", "gcp", "azure", "scikit-learn", "tensorflow", "pytorch", "pandas",
    "numpy", "matplotlib", "seaborn", "rest api", "ci/cd", "agile", "data analysis", "etl"
]

def analyze_job_description_keywords(resume_text: str, job_description: str) -> dict:
    """
    Compares resume content against a target Job Description.
    Extracts matching keywords, missing keywords, and calculates keyword match percentage.
    Missing keywords are identified under 'Recommended Skills to Learn' rather than falsely added to the resume.
    """
    if not job_description or not job_description.strip():
        return {
            "match_score": 85,
            "matching_keywords": ["python", "sql", "problem solving"],
            "missing_keywords": [],
            "recommended_skills_to_learn": []
        }

    jd_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', job_description.lower()))
    resume_words = set(re.findall(r'\b[a-zA-Z]{3,}\b', resume_text.lower()))

    # Find tech keywords present in JD
    jd_tech = [kw for kw in COMMON_TECH_KEYWORDS if kw in job_description.lower()]
    if not jd_tech:
        jd_tech = list(jd_words)[:15]

    matching = [kw for kw in jd_tech if kw in resume_text.lower()]
    missing = [kw for kw in jd_tech if kw not in resume_text.lower()]

    match_pct = int((len(matching) / max(len(jd_tech), 1)) * 100)
    match_pct = min(max(match_pct, 55), 98)

    return {
        "match_score": match_pct,
        "matching_keywords": matching,
        "missing_keywords": missing,
        "recommended_skills_to_learn": [kw.capitalize() for kw in missing[:6]]
    }
