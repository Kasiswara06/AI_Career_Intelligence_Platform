import pandas as pd
from typing import List, Dict, Any
from config import JOBS_CSV
from database.database import get_all_jobs, insert_job, save_job_match_history
from ai_models.job_matching import analyze_job_match_full

DEFAULT_BENCHMARK_JOBS = [
    {
        "id": 1,
        "job_title": "AI / Machine Learning Engineer",
        "company": "TechCorp Innovations",
        "location": "Bangalore / Remote",
        "experience_level": "1-3 Years",
        "qualification": "B.Tech / M.Tech in CS or AI",
        "salary_range": "$90,000 - $130,000",
        "required_skills": "Python, Machine Learning, PyTorch, SQL, Docker, FastAPI",
        "job_description": "We are seeking a passionate AI/ML Engineer to design, train, and deploy scalable deep learning models. Candidate must be proficient in Python, PyTorch/TensorFlow, SQL database optimization, Docker containerization, and REST API deployment."
    },
    {
        "id": 2,
        "job_title": "Senior Full Stack Python Developer",
        "company": "CloudScale Systems",
        "location": "San Francisco, CA / Remote",
        "experience_level": "2-5 Years",
        "qualification": "B.S. in Computer Science",
        "salary_range": "$110,000 - $150,000",
        "required_skills": "Python, React, Django, PostgreSQL, AWS, Git",
        "job_description": "Join our cloud engineering team building real-time analytics platforms. Key requirements include strong mastery of Python, Django/FastAPI, React.js frontend, PostgreSQL database management, AWS cloud infrastructure, and CI/CD pipelines."
    },
    {
        "id": 3,
        "job_title": "Data Scientist & Analytics Lead",
        "company": "DataMind Analytics",
        "location": "New York, NY / Hybrid",
        "experience_level": "0-2 Years",
        "qualification": "Bachelor's degree in Statistics or CS",
        "salary_range": "$85,000 - $120,000",
        "required_skills": "Python, SQL, Pandas, Scikit-Learn, Statistics, Tableau",
        "job_description": "Analyze multi-terabyte datasets to derive predictive business intelligence. Requires proficiency in Python, SQL data extraction, Pandas/NumPy data wrangling, Scikit-Learn modeling, and executive dashboard visualization."
    }
]

def fetch_available_jobs() -> List[Dict[str, Any]]:
    """Loads jobs from Database or fallback CSV / benchmark list."""
    jobs = get_all_jobs()
    if jobs:
        return jobs

    if JOBS_CSV.exists():
        try:
            df = pd.read_csv(JOBS_CSV)
            records = df.to_dict("records")
            if records:
                return records
        except Exception:
            pass

    return DEFAULT_BENCHMARK_JOBS

def rank_candidate_against_jobs(
    resume_text: str,
    extracted_skills: List[str] = None,
    experience_years: float = 1.0,
    user_id: int = 1
) -> List[Dict[str, Any]]:
    """
    Ranks all available job descriptions against candidate resume using all-MiniLM-L6-v2 embeddings.
    """
    jobs = fetch_available_jobs()
    ranked_jobs = []

    for job in jobs:
        title = job.get("job_title", job.get("title", "Software Developer"))
        jd_text = job.get("job_description", job.get("description", ""))
        company = job.get("company", "Tech Enterprise")
        
        match_result = analyze_job_match_full(
            resume_text=resume_text,
            job_description=jd_text,
            extracted_skills=extracted_skills,
            job_title=title,
            experience_years=experience_years
        )
        
        match_result["job_id"] = job.get("id", job.get("job_id", 1))
        match_result["job_title"] = title
        match_result["company"] = company
        match_result["location"] = job.get("location", "Remote")
        match_result["experience_level"] = job.get("experience_level", job.get("experience", "1-3 Years"))
        match_result["salary_range"] = job.get("salary_range", job.get("salary", "$80,000 - $120,000"))
        match_result["qualification"] = job.get("qualification", "B.Tech / B.S.")
        match_result["job_description"] = jd_text

        # Save match audit to DB
        try:
            save_job_match_history(
                user_id=user_id,
                job_id=match_result["job_id"],
                resume_score=match_result["resume_score"],
                ats_score=match_result["ats_score"],
                match_pct=match_result["match_percentage"],
                matching_skills=match_result["matching_skills"],
                missing_skills=match_result["missing_skills"],
                recommended_skills=match_result["additional_recommended_skills"]
            )
        except Exception:
            pass

        ranked_jobs.append(match_result)

    # Sort by match percentage descending
    ranked_jobs.sort(key=lambda x: x["match_percentage"], reverse=True)
    return ranked_jobs
