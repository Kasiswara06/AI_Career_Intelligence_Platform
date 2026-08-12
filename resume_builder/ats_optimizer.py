import logging
from ai_models.ats_optimizer import evaluate_resume_ats_scores as ai_eval_ats

logger = logging.getLogger(__name__)

def evaluate_resume_ats_scores(resume_dict: dict, full_resume_text: str, target_role: str = "AI Engineer", job_description: str = "") -> dict:
    """
    Evaluates detailed ATS scores, keywords, strengths, weaknesses, and actionable suggestions.
    Delegates to ai_models.ats_optimizer.evaluate_resume_ats_scores.
    """
    return ai_eval_ats(resume_dict=resume_dict, full_resume_text=full_resume_text, target_role=target_role, job_description=job_description)
