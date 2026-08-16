import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Base Directory
BASE_DIR = Path(__file__).resolve().parent

# Ensure project root and assets directory are in sys.path for ai_models resolution
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(BASE_DIR / "assets") not in sys.path:
    sys.path.insert(0, str(BASE_DIR / "assets"))

# Load environment variables from .env file
load_dotenv(BASE_DIR / ".env", override=True)

# Application Settings
APP_NAME = "AI Resume Screening & Career Intelligence Platform"
APP_VERSION = "1.0.0"
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-career-ai-key-2026")

# Database Configurations
DB_TYPE = os.getenv("DB_TYPE", "mysql") # 'mysql' or 'sqlite'
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "ai_career")

# SQLite File Path
SQLITE_DB_PATH = BASE_DIR / "database" / "ai_career.db"

# Assets & Static Paths
ASSETS_DIR = BASE_DIR / "assets"
STATIC_DIR = BASE_DIR / "static"
CSS_DIR = STATIC_DIR / "css"
JS_DIR = STATIC_DIR / "js"
UPLOADS_DIR = STATIC_DIR / "uploads"

# Specific Upload Subdirectories
RESUME_UPLOAD_DIR = UPLOADS_DIR / "resumes"
CERT_UPLOAD_DIR = UPLOADS_DIR / "certificates"
PROFILE_UPLOAD_DIR = UPLOADS_DIR / "profile"
REPORTS_UPLOAD_DIR = UPLOADS_DIR / "reports"

# Ensure directories exist
for directory in [
    ASSETS_DIR / "logo", ASSETS_DIR / "icons", ASSETS_DIR / "images", ASSETS_DIR / "animations", ASSETS_DIR / "backgrounds",
    CSS_DIR, JS_DIR,
    RESUME_UPLOAD_DIR, CERT_UPLOAD_DIR, PROFILE_UPLOAD_DIR, REPORTS_UPLOAD_DIR,
    BASE_DIR / "reports" / "pdf", BASE_DIR / "reports" / "excel", BASE_DIR / "reports" / "analytics"
]:
    directory.mkdir(parents=True, exist_ok=True)

# Dataset Paths
DATASET_DIR = BASE_DIR / "datasets"
JOBS_CSV = DATASET_DIR / "jobs.csv"
SALARY_CSV = DATASET_DIR / "salary.csv"
SKILLS_CSV = DATASET_DIR / "skills.csv"
COURSES_CSV = DATASET_DIR / "courses.csv"
INTERVIEW_CSV = DATASET_DIR / "interview_questions.csv"

# Model Paths
MODEL_DIR = BASE_DIR / "ai_models"
RANDOM_FOREST_MODEL = MODEL_DIR / "random_forest.pkl"
TFIDF_MODEL = MODEL_DIR / "tfidf.pkl"
MINILM_MODEL_NAME = "all-MiniLM-L6-v2"

# Security & Upload Limits
ALLOWED_RESUME_EXTENSIONS = [".pdf", ".docx", ".txt"]
ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png"]
MAX_FILE_SIZE_MB = 10
