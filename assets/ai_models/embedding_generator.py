import numpy as np
import logging
from typing import List, Union

logger = logging.getLogger(__name__)

# Global model cache to avoid re-loading weights on every call
_SENTENCE_TRANSFORMER_MODEL = None

def get_sentence_transformer_model():
    """
    Lazy loads the 'all-MiniLM-L6-v2' SentenceTransformer model.
    Falls back gracefully if sentence_transformers is not installed.
    """
    global _SENTENCE_TRANSFORMER_MODEL
    if _SENTENCE_TRANSFORMER_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
            logger.info("Loading SentenceTransformer model 'all-MiniLM-L6-v2'...")
            _SENTENCE_TRANSFORMER_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception as e:
            logger.warning(f"Could not load SentenceTransformer ('all-MiniLM-L6-v2'): {e}. Utilizing fallback vectorizer.")
            _SENTENCE_TRANSFORMER_MODEL = False

    return _SENTENCE_TRANSFORMER_MODEL

def generate_embedding(text: str) -> np.ndarray:
    """
    Generates a dense vector embedding for a single text input string using all-MiniLM-L6-v2.
    If SentenceTransformer is unavailable, returns a normalized TF-IDF vector representation.
    """
    if not text or not text.strip():
        return np.zeros(384)

    model = get_sentence_transformer_model()
    if model:
        try:
            embedding = model.encode(text, convert_to_numpy=True)
            return embedding
        except Exception as e:
            logger.error(f"Error generating SentenceTransformer embedding: {e}")

    # Fallback: Count Vectorizer pseudo-embedding
    from sklearn.feature_extraction.text import TfidfVectorizer
    try:
        vectorizer = TfidfVectorizer(max_features=384)
        vec = vectorizer.fit_transform([text]).toarray()[0]
        # Pad to 384 dimensions if fewer features present
        if len(vec) < 384:
            vec = np.pad(vec, (0, 384 - len(vec)), mode='constant')
        return vec
    except Exception:
        return np.zeros(384)

def generate_batch_embeddings(texts: List[str]) -> np.ndarray:
    """Generates dense vector embeddings for a list of text strings."""
    model = get_sentence_transformer_model()
    if model:
        try:
            return model.encode(texts, convert_to_numpy=True)
        except Exception as e:
            logger.error(f"Batch embedding generation failed: {e}")

    return np.array([generate_embedding(t) for t in texts])
