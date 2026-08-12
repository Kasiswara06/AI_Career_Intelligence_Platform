from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from config import TFIDF_MODEL

def train_and_save_tfidf(corpus: list[str]):
    """Trains a TF-IDF vectorizer model and serializes to disk."""
    vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
    vectorizer.fit(corpus)
    with open(TFIDF_MODEL, "wb") as f:
        pickle.dump(vectorizer, f)
    return vectorizer

def load_tfidf_vectorizer():
    """Loads pre-trained TF-IDF vectorizer model."""
    if TFIDF_MODEL.exists():
        try:
            with open(TFIDF_MODEL, "rb") as f:
                return pickle.load(f)
        except Exception:
            pass
    return TfidfVectorizer(stop_words='english')
