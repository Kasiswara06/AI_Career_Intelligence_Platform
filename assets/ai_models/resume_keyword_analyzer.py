import re
import logging

logger = logging.getLogger(__name__)

# Essential Keywords Map per Target Job Role (Section 3 requirement)
ROLE_KEYWORDS_MAP = {
    "Python Developer": ["python", "django", "flask", "fastapi", "sql", "git", "rest api", "pytest", "docker", "oop"],
    "Data Analyst": ["python", "sql", "excel", "tableau", "power bi", "pandas", "numpy", "statistics", "data visualization", "etl"],
    "Data Scientist": ["python", "r", "sql", "machine learning", "pandas", "scikit-learn", "deep learning", "statistics", "data mining", "tableau"],
    "Machine Learning Engineer": ["python", "machine learning", "deep learning", "scikit-learn", "tensorflow", "pytorch", "docker", "mlops", "git", "sql"],
    "AI Engineer": ["python", "ai", "machine learning", "nlp", "llm", "tensorflow", "pytorch", "langchain", "prompt engineering", "git"],
    "NLP Engineer": ["python", "nlp", "spacy", "nltk", "transformers", "bert", "huggingface", "machine learning", "deep learning", "git"],
    "Software Engineer": ["python", "java", "c++", "data structures", "algorithms", "git", "sql", "rest api", "object-oriented programming", "system design"],
    "Full Stack Developer": ["javascript", "react", "node.js", "html", "css", "python", "sql", "mongodb", "git", "rest api"],
    "Backend Developer": ["python", "java", "node.js", "sql", "postgresql", "mongodb", "rest api", "docker", "redis", "microservices"],
    "Data Engineer": ["python", "sql", "spark", "hadoop", "etl", "airflow", "snowflake", "bigquery", "postman", "docker"],
    "Cloud Engineer": ["aws", "azure", "google cloud", "terraform", "docker", "kubernetes", "linux", "bash", "networking", "ci/cd"],
    "DevOps Engineer": ["docker", "kubernetes", "jenkins", "git", "ci/cd", "linux", "aws", "terraform", "ansible", "python"]
}

def analyze_target_role_keywords(resume_text: str, target_role: str = "AI Engineer", job_description: str = "") -> dict:
    """
    Analyzes resume text against Target Role keywords and optional Job Description.
    Extracts Detected Keywords (✓), Missing Keywords (•), and calculates Keyword Match %.
    Does NOT add missing skills to resume automatically (Section 10 requirement).
    """
    clean_text = resume_text.lower() if resume_text else ""
    
    # 1. Target role baseline keywords
    target_kws = ROLE_KEYWORDS_MAP.get(target_role, ["python", "sql", "git", "problem solving", "software engineering", "data analysis"])

    # 2. Add extra keywords from JD if provided
    if job_description and job_description.strip():
        jd_words = re.findall(r'\b[a-zA-Z]{3,}\b', job_description.lower())
        jd_unique = list(dict.fromkeys(jd_words))
        # Pick top tech-like terms
        extra_jd = [w for w in jd_unique if len(w) >= 3 and w in ["python", "sql", "java", "docker", "aws", "react", "cloud", "api", "git", "pandas", "ml", "ai"]][:8]
        target_kws = list(dict.fromkeys(target_kws + extra_jd))

    detected = []
    missing = []

    for kw in target_kws:
        pattern = r'\b' + re.escape(kw) + r'\b'
        if re.search(pattern, clean_text):
            detected.append(kw.capitalize())
        else:
            missing.append(kw.capitalize())

    total = len(target_kws) if target_kws else 1
    match_pct = int((len(detected) / total) * 100)
    match_pct = min(max(match_pct, 50), 98)

    return {
        "target_role": target_role,
        "match_score": match_pct,
        "detected_keywords": detected,
        "missing_keywords": missing,
        "recommended_skills_to_learn": missing[:6]
    }

def analyze_resume_keywords(resume_text: str, target_jd: str = "") -> dict:
    """Helper alias for keyword analysis."""
    return analyze_target_role_keywords(resume_text, "AI Engineer", target_jd)

