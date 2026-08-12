from ai_models.embedding_generator import generate_embedding
from ai_models.cosine_similarity import compute_cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import re

def compute_tfidf_similarity(text1: str, text2: str) -> float:
    """Computes TF-IDF cosine similarity between two text strings."""
    if not text1.strip() or not text2.strip():
        return 0.0
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        sim = (tfidf_matrix * tfidf_matrix.T).toarray()[0, 1]
        return float(sim)
    except Exception:
        return 0.0

def calculate_semantic_job_match(resume_text: str, job_text: str) -> dict:
    """
    Performs high-level semantic matching combining:
    1. Dense vector cosine similarity via all-MiniLM-L6-v2 SentenceTransformer (70% weight)
    2. TF-IDF keyword overlap (30% weight)
    """
    if not resume_text.strip() or not job_text.strip():
        return {
            "embedding_similarity": 0.0,
            "tfidf_similarity": 0.0,
            "semantic_match_pct": 0.0
        }

    resume_emb = generate_embedding(resume_text)
    job_emb = generate_embedding(job_text)

    embedding_sim = compute_cosine_similarity(resume_emb, job_emb)
    tfidf_sim = compute_tfidf_similarity(resume_text, job_text)

    # Blended semantic match score
    blended_score = (embedding_sim * 0.70) + (tfidf_sim * 0.30)
    match_pct = round(blended_score * 100, 1)

    return {
        "embedding_similarity": round(embedding_sim * 100, 1),
        "tfidf_similarity": round(tfidf_sim * 100, 1),
        "semantic_match_pct": match_pct
    }
