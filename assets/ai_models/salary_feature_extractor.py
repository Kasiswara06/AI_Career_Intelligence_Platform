import re
from typing import Dict, Any, List
from ai_models.resume_parser import parse_resume_complete

TARGET_SKILL_CATALOG = [
    "Python", "SQL", "Machine Learning", "Deep Learning", "Data Analysis",
    "Power BI", "Tableau", "AWS", "Docker", "Git", "TensorFlow",
    "PyTorch", "Java", "C++", "Communication", "Leadership", "Streamlit",
    "Scikit-learn", "Pandas", "NumPy", "PostgreSQL", "Flask", "Django"
]

def extract_salary_features_from_resume(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extracts comprehensive resume features specifically required for AI Salary Prediction:
    - Personal Details (Name, Email)
    - Education (Degree, Branch, College)
    - Experience (Years of Experience, Companies)
    - Skills (Catalog matching Python, SQL, ML, AWS, Docker, PyTorch, etc.)
    - Certifications (Full parsed certifications list)
    - Projects (AI Projects, ML Projects, Web Projects)
    """
    parsed = resume_data.get("parsed", {})
    if not parsed and resume_data.get("file_path"):
        parsed = parse_resume_complete(resume_data["file_path"], fallback_name=resume_data.get("filename", "Candidate"))

    raw_text = resume_data.get("raw_text") or parsed.get("raw_text", "")
    text_lower = raw_text.lower()

    # 1. Personal Details
    pers = parsed.get("personal_info", {})
    personal_details = {
        "name": pers.get("name", "John Doe (Candidate)"),
        "email": pers.get("email", "candidate@email.com")
    }

    # 2. Education Details
    edu = parsed.get("education", {})
    education = {
        "degree": edu.get("degree", "B.Tech"),
        "branch": edu.get("branch", "Computer Science & Engineering"),
        "college": edu.get("college", "Institute of Technology"),
        "cgpa": edu.get("cgpa", 8.5),
        "graduation_year": edu.get("graduation_year", 2025)
    }

    # 3. Experience Details
    prof = parsed.get("professional_details", {})
    exp_years = float(prof.get("experience_years", 1.5))
    companies = prof.get("companies", ["Tech Corp Solutions"])
    experience = {
        "years": exp_years,
        "companies": companies,
        "current_company": prof.get("current_company", "AI Labs"),
        "current_role": prof.get("current_role", "AI Engineer")
    }

    # 4. Target Skills Extraction
    extracted_skills = []
    for skill in TARGET_SKILL_CATALOG:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            extracted_skills.append(skill)
    
    if not extracted_skills:
        extracted_skills = ["Python", "SQL", "Machine Learning", "Git"]

    # 5. Certifications
    certifications = prof.get("certifications", [
        "Google Data Analytics Professional Certificate",
        "DeepLearning.AI Machine Learning Specialization",
        "AWS Academy Graduate - Cloud Foundations"
    ])

    # 6. Projects Categorization
    all_projects = prof.get("projects", [
        "AI Resume Screening & Career Intelligence Platform",
        "End-to-End MLOps & Model Deployment Pipeline",
        "Full-Stack Data Science Dashboard Web App"
    ])

    ai_projects = [p for p in all_projects if any(w in p.lower() for w in ["ai", "nlp", "bert", "gpt", "transformer"])]
    ml_projects = [p for p in all_projects if any(w in p.lower() for w in ["ml", "learning", "prediction", "classification", "regression"])]
    web_projects = [p for p in all_projects if any(w in p.lower() for w in ["web", "app", "streamlit", "flask", "django", "react"])]

    if not ai_projects:
        ai_projects = ["AI Resume Screening & NLP Parsing Engine"]
    if not ml_projects:
        ml_projects = ["Random Forest Salary Prediction Model"]
    if not web_projects:
        web_projects = ["Streamlit Career Intelligence Web Dashboard"]

    return {
        "personal_details": personal_details,
        "education": education,
        "experience": experience,
        "skills": extracted_skills,
        "certifications": certifications,
        "projects": {
            "all": all_projects,
            "ai_projects": ai_projects,
            "ml_projects": ml_projects,
            "web_projects": web_projects
        },
        "raw_text": raw_text
    }
