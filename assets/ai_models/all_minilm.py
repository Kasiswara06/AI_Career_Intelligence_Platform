import numpy as np
import logging
from config import MINILM_MODEL_NAME
from ai_models.tfidf_model import calculate_tfidf_similarity

logger = logging.getLogger(__name__)
_model_instance = None

def get_minilm_model():
    """Lazy loads SentenceTransformer model with fallback handling."""
    global _model_instance
    if _model_instance is not None:
        return _model_instance

    try:
        from sentence_transformers import SentenceTransformer
        logger.info(f"Loading SentenceTransformer model: {MINILM_MODEL_NAME}")
        _model_instance = SentenceTransformer(MINILM_MODEL_NAME)
        return _model_instance
    except Exception as e:
        logger.warning(f"Could not load SentenceTransformer model ({e}). Using TF-IDF/Jaccard semantic fallback.")
        return None

def compute_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Computes cosine similarity between two vector embeddings."""
    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot_product / (norm_a * norm_b))

def calculate_semantic_similarity(text1: str, text2: str) -> float:
    """
    Computes semantic similarity score (0 - 100%) between resume text and job description
    using SentenceTransformer embeddings + Cosine Similarity.
    """
    if not text1 or not text2:
        return 0.0

    model = get_minilm_model()
    if model is not None:
        try:
            embeddings = model.encode([text1, text2])
            sim = compute_cosine_similarity(embeddings[0], embeddings[1])
            return round(max(0.0, min(100.0, sim * 100)), 2)
        except Exception as e:
            logger.error(f"Error computing SentenceTransformer similarity: {e}")

    # Fallback to TF-IDF Cosine Similarity
    return calculate_tfidf_similarity(text1, text2)
