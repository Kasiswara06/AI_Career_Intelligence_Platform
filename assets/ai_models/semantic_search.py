from typing import List, Dict, Any
from ai_models.all_minilm import compute_semantic_similarity, extract_keywords_tfidf

def semantic_search_jobs(query: str, job_list: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Performs semantic search over a list of jobs based on user query/resume text.
    Returns top_k matching jobs with similarity scores.
    """
    scored_jobs = []
    for job in job_list:
        job_text = f"{job.get('title', '')} {job.get('description', '')} {' '.join(job.get('required_skills', []))}"
        score = compute_semantic_similarity(query, job_text)
        job_copy = dict(job)
        job_copy["semantic_similarity_score"] = round(score * 100, 1)
        scored_jobs.append(job_copy)

    scored_jobs.sort(key=lambda x: x["semantic_similarity_score"], reverse=True)
    return scored_jobs[:top_k]
