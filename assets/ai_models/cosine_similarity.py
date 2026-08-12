import numpy as np
from typing import Union, List

def compute_cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    Computes mathematical Cosine Similarity between two 1D/2D embedding numpy arrays.
    Returns float score between 0.0 and 1.0.
    """
    v1 = np.asarray(vec1, dtype=np.float32).flatten()
    v2 = np.asarray(vec2, dtype=np.float32).flatten()

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)

    if norm1 == 0.0 or norm2 == 0.0:
        return 0.0

    similarity = np.dot(v1, v2) / (norm1 * norm2)
    return float(np.clip(similarity, 0.0, 1.0))

def compute_batch_cosine_similarity(query_vec: np.ndarray, candidate_matrix: np.ndarray) -> List[float]:
    """Computes cosine similarity of query vector against multiple candidate vectors."""
    q_vec = np.asarray(query_vec, dtype=np.float32).flatten()
    matrix = np.asarray(candidate_matrix, dtype=np.float32)

    q_norm = np.linalg.norm(q_vec)
    if q_norm == 0.0:
        return [0.0] * len(matrix)

    matrix_norms = np.linalg.norm(matrix, axis=1)
    matrix_norms[matrix_norms == 0.0] = 1e-10  # Prevent division by zero

    dot_products = np.dot(matrix, q_vec)
    similarities = dot_products / (matrix_norms * q_norm)
    return [float(s) for s in np.clip(similarities, 0.0, 1.0)]
