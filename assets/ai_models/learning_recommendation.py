import pandas as pd
from config import COURSES_CSV

COURSE_CATALOG = [
    {
        "course_name": "Infosys Springboard: Artificial Intelligence & Machine Learning Masterclass",
        "platform": "Infosys Springboard",
        "duration": "6 Weeks",
        "difficulty": "Intermediate",
        "skills_covered": "Python, Machine Learning, Deep Learning, PyTorch",
        "link": "https://springboard.infosys.com"
    },
    {
        "course_name": "Google Cloud Skills Boost: Machine Learning Engineer Learning Path",
        "platform": "Google Cloud Skills Boost",
        "duration": "4 Weeks",
        "difficulty": "Intermediate",
        "skills_covered": "AWS, GCP, Docker, Kubernetes, Cloud AI",
        "link": "https://www.cloudskillsboost.google"
    },
    {
        "course_name": "NPTEL: Data Science & Big Analytics Foundations",
        "platform": "NPTEL",
        "duration": "8 Weeks",
        "difficulty": "Advanced",
        "skills_covered": "SQL, Python, Data Engineering, Algorithms",
        "link": "https://nptel.ac.in"
    },
    {
        "course_name": "Coursera: Deep Learning Specialization by Andrew Ng",
        "platform": "Coursera",
        "duration": "5 Weeks",
        "difficulty": "Advanced",
        "skills_covered": "TensorFlow, Neural Networks, Deep Learning",
        "link": "https://coursera.org"
    },
    {
        "course_name": "Udemy: Docker & Kubernetes - The Complete Guide",
        "platform": "Udemy",
        "duration": "3 Weeks",
        "difficulty": "Intermediate",
        "skills_covered": "Docker, Kubernetes, DevOps, Microservices",
        "link": "https://udemy.com"
    }
]

def get_recommended_courses(missing_skills: list = None) -> list:
    """Recommends online courses based on missing skills from Infosys Springboard, Coursera, NPTEL, etc."""
    if not missing_skills:
        return COURSE_CATALOG

    missing_lower = [s.lower() for s in missing_skills]
    filtered = []

    for course in COURSE_CATALOG:
        covered = course["skills_covered"].lower()
        if any(ms in covered for ms in missing_lower):
            filtered.append(course)

    return filtered if filtered else COURSE_CATALOG

def generate_learning_roadmap(missing_skills: list) -> list:
    """Generates a 4-phase structured learning roadmap."""
    return [
        {
            "phase": "Phase 1: Foundation (Weeks 1-2)",
            "focus": "Core Programming & Data Manipulation",
            "skills": "Python, SQL, Data Structures",
            "action": "Complete Infosys Springboard Python & SQL foundational modules."
        },
        {
            "phase": "Phase 2: Machine Learning & NLP (Weeks 3-4)",
            "focus": "Supervised Learning & Sentence Embeddings",
            "skills": "Scikit-learn, Sentence Transformers, Pandas",
            "action": "Build end-to-end regression & classification ML models."
        },
        {
            "phase": "Phase 3: MLOps & Cloud Deployment (Weeks 5-6)",
            "focus": "Containerization & Cloud Infrastructure",
            "skills": "Docker, Kubernetes, AWS, REST APIs",
            "action": "Containerize Streamlit app and deploy on cloud infrastructure."
        },
        {
            "phase": "Phase 4: Interview & Portfolio (Weeks 7-8)",
            "focus": "Mock Interview & Resume Optimization",
            "skills": "STAR Behavioral, Technical Architecture",
            "action": "Complete 10 mock interview sessions and update resume."
        }
    ]

def get_learning_recommendations(missing_skills: list = None) -> list:
    """Returns recommended courses formatted for learning recommendation components."""
    courses = get_recommended_courses(missing_skills)
    formatted = []
    for c in courses:
        formatted.append({
            "course_title": c.get("course_name") or c.get("course_title", "Online Masterclass"),
            "provider": c.get("platform") or c.get("provider", "E-Learning Platform"),
            "level": c.get("difficulty") or c.get("level", "Intermediate"),
            "skills_covered": c.get("skills_covered", "Technical Skills"),
            "url": c.get("link") or c.get("url", "#"),
            "duration": c.get("duration", "4 Weeks")
        })
    return formatted
