import logging
from typing import Dict, Any, Tuple
from utils.resume_loader import load_active_or_uploaded_resume
from ai_models.salary_feature_extractor import extract_salary_features_from_resume
from ai_models.random_forest_salary import predict_resume_salary_random_forest
from database.database import save_salary_prediction_record, log_activity

logger = logging.getLogger(__name__)

def run_ai_salary_prediction(user_id: int = 1, uploaded_file = None, target_job_role: str = "AI Engineer", location: str = "India / Remote") -> Dict[str, Any]:
    """
    Master orchestration service for AI Resume-Based Salary Prediction Engine:
    1. Loads active or uploaded resume
    2. Extracts structured features
    3. Runs Random Forest Salary Regression
    4. Persists record in MySQL/SQLite database
    5. Logs user activity
    """
    resume_info = load_active_or_uploaded_resume(user_id=user_id, uploaded_file=uploaded_file)
    if not resume_info.get("has_resume"):
        return {"has_resume": False}

    features = extract_salary_features_from_resume(resume_info)
    prediction = predict_resume_salary_random_forest(
        features=features,
        target_job_role=target_job_role,
        location=location
    )

    # Persist in database
    resume_id = resume_info.get("id", 1)
    save_salary_prediction_record(
        user_id=user_id,
        resume_id=resume_id,
        resume_score=resume_info.get("resume_score", 88),
        ats_score=resume_info.get("ats_score", 90),
        predicted_salary=prediction["expected_lpa"],
        minimum_salary=prediction["min_lpa"],
        maximum_salary=prediction["max_lpa"],
        confidence=prediction["confidence_score"],
        experience_level=prediction["experience_level"]
    )

    log_activity(
        user_id=user_id,
        action="Salary Prediction",
        details=f"Predicted salary range ₹ {prediction['min_lpa']} - {prediction['max_lpa']} LPA for resume '{resume_info.get('filename')}'"
    )

    return {
        "has_resume": True,
        "resume_info": resume_info,
        "features": features,
        "prediction": prediction
    }

def compare_two_resumes_salary(user_id: int, current_resume_info: Dict[str, Any], new_file) -> Dict[str, Any]:
    """
    Compares salary valuations between Current Active Resume and a New Uploaded Resume.
    Returns Old LPA, New LPA, and Percentage Improvement (% boost).
    """
    old_res = run_ai_salary_prediction(user_id=user_id, uploaded_file=None)
    new_res = run_ai_salary_prediction(user_id=user_id, uploaded_file=new_file)

    old_lpa = old_res.get("prediction", {}).get("expected_lpa", 6.5)
    new_lpa = new_res.get("prediction", {}).get("expected_lpa", 8.2)

    diff = round(new_lpa - old_lpa, 2)
    pct_gain = round(((new_lpa - old_lpa) / max(1.0, old_lpa)) * 100, 1)

    return {
        "old_resume_name": current_resume_info.get("filename", "Current Resume"),
        "new_resume_name": new_file.name,
        "old_lpa": old_lpa,
        "new_lpa": new_lpa,
        "diff_lpa": diff,
        "percentage_improvement": max(0.0, pct_gain),
        "old_prediction": old_res.get("prediction"),
        "new_prediction": new_res.get("prediction")
    }
