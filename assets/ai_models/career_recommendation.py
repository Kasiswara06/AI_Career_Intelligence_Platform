from typing import List, Dict, Any

CAREER_PROFILES = [
    {
        "role": "AI / ML Engineer",
        "required_skills": ["python", "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "sql"],
        "min_experience": 0,
        "industry_demand": "Very High",
        "career_growth": "35% YoY growth",
        "roadmap": [
            "Master Python & Math for Machine Learning",
            "Build ML models with Scikit-Learn & PyTorch",
            "Deploy AI models via APIs (FastAPI/Streamlit)",
            "Learn MLOps, Model Monitoring & Scaling"
        ]
    },
    {
        "role": "Data Scientist",
        "required_skills": ["python", "sql", "pandas", "numpy", "statistics", "machine learning", "data visualization"],
        "min_experience": 0,
        "industry_demand": "High",
        "career_growth": "28% YoY growth",
        "roadmap": [
            "Learn Data Analysis & Wrangling with Pandas",
            "Master SQL for Data Extraction",
            "Study Statistical Modeling & A/B Testing",
            "Build ML predictive models & interactive dashboards"
        ]
    },
    {
        "role": "Full Stack Developer",
        "required_skills": ["javascript", "react", "node.js", "html", "css", "sql", "git", "rest api"],
        "min_experience": 0,
        "industry_demand": "High",
        "career_growth": "22% YoY growth",
        "roadmap": [
            "Master HTML, CSS & Modern JavaScript",
            "Build Frontend UI with React or Next.js",
            "Develop Backend REST APIs with Node.js/Python",
            "Connect Relational & NoSQL Databases"
        ]
    },
    {
        "role": "DevOps / Cloud Engineer",
        "required_skills": ["docker", "kubernetes", "aws", "linux", "ci/cd", "terraform", "python", "git"],
        "min_experience": 1,
        "industry_demand": "Very High",
        "career_growth": "30% YoY growth",
        "roadmap": [
            "Master Linux System Administration & Shell Scripting",
            "Containerize applications with Docker & Kubernetes",
            "Implement CI/CD pipelines with GitHub Actions / Jenkins",
            "Learn Cloud Infrastructure with AWS / Azure & Terraform"
        ]
    },
    {
        "role": "Data Engineer",
        "required_skills": ["python", "sql", "spark", "hadoop", "airflow", "sql", "etl", "aws"],
        "min_experience": 1,
        "industry_demand": "High",
        "career_growth": "25% YoY growth",
        "roadmap": [
            "Master SQL & Relational/NoSQL Database Design",
            "Build Scalable Data Pipelines with Apache Spark & Airflow",
            "Design Data Warehouses on AWS Redshift / Snowflake",
            "Implement Real-time Streaming with Kafka"
        ]
    }
]

def recommend_career_path(skills: List[str], education: List[str] = None, experience_years: float = 0.0) -> List[Dict[str, Any]]:
    """
    Analyzes education, skills, experience to predict matching career paths,
    providing roadmaps, industry demand, and growth rate.
    """
    user_skills_lower = set([s.lower().strip() for s in skills])
    recommendations = []

    for profile in CAREER_PROFILES:
        req_skills = profile["required_skills"]
        matching_count = len(user_skills_lower.intersection(set(req_skills)))
        total_req = len(req_skills)
        match_percentage = round((matching_count / total_req) * 100, 1) if total_req > 0 else 0

        # Adjust score slightly based on experience
        readiness = min(100.0, match_percentage + (experience_years * 5))

        recommendations.append({
            "career_role": profile["role"],
            "match_score": match_percentage,
            "readiness_score": round(readiness, 1),
            "matching_skills": list(user_skills_lower.intersection(set(req_skills))),
            "missing_skills": [s for s in req_skills if s not in user_skills_lower],
            "industry_demand": profile["industry_demand"],
            "career_growth": profile["career_growth"],
            "roadmap": profile["roadmap"]
        })

    # Sort by match score descending
    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    return recommendations
