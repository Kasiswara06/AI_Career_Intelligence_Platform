import os
import sys
import pickle
from pathlib import Path

# Add project root directory to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from config import SALARY_CSV, SKILLS_CSV, RANDOM_FOREST_MODEL, TFIDF_MODEL

def train_salary_model():
    """Trains a Random Forest Regressor for salary prediction."""
    if not SALARY_CSV.exists():
        print(f"Salary dataset not found at {SALARY_CSV}")
        return

    df = pd.read_csv(SALARY_CSV)
    
    # Feature columns
    X = df[['experience_years', 'skill_count', 'project_count']]
    y = df['salary_lpa']

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Save model
    RANDOM_FOREST_MODEL.parent.mkdir(parents=True, exist_ok=True)
    with open(RANDOM_FOREST_MODEL, 'wb') as f:
        pickle.dump(model, f)
    print(f"Random Forest Salary Model trained and saved to {RANDOM_FOREST_MODEL}")

def train_tfidf_model():
    """Fits and saves a TF-IDF Vectorizer on skills vocabulary."""
    if not SKILLS_CSV.exists():
        print(f"Skills dataset not found at {SKILLS_CSV}")
        return

    df = pd.read_csv(SKILLS_CSV)
    skills_list = df['skill_name'].tolist()

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    vectorizer.fit(skills_list)

    TFIDF_MODEL.parent.mkdir(parents=True, exist_ok=True)
    with open(TFIDF_MODEL, 'wb') as f:
        pickle.dump(vectorizer, f)
    print(f"TF-IDF Model fitted and saved to {TFIDF_MODEL}")

if __name__ == "__main__":
    train_salary_model()
    train_tfidf_model()
