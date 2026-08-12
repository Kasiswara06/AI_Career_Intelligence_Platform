import logging
from ai_models.interview_generator import (
    generate_personalized_interview_questions,
    evaluate_user_interview_answer
)
from ai_models.interview_feedback import generate_final_interview_report
from services.interview_preference_service import (
    get_user_interview_preference,
    save_user_interview_preference
)
from services.interview_history_service import (
    create_interview_session,
    update_interview_session_results,
    save_interview_question_response,
    get_user_interview_sessions_history
)
from utils.interview_utils import get_user_active_resume_data, clean_difficulty_str

logger = logging.getLogger(__name__)

def get_prepared_interview_questions(job_title: str = "Software Engineer", difficulty: str = "Medium") -> list:
    """Backwards compatible question generator."""
    domain = "Python Development" if "python" in job_title.lower() else "Software Development"
    return generate_personalized_interview_questions(
        domain=domain,
        target_role=job_title,
        difficulty=difficulty,
        count=5
    )

def prepare_personalized_user_interview(
    user_id: int,
    domain: str,
    target_role: str,
    difficulty: str = "Medium",
    question_type: str = "Mixed",
    count: int = 10
) -> dict:
    """
    Main service pipeline:
    1. Save user domain & role preferences
    2. Load candidate active resume details
    3. Generate personalized question set (Domain + Role + Resume + Difficulty)
    4. Create DB interview session
    """
    # 1. Save Preference
    save_user_interview_preference(user_id, domain, target_role, difficulty, question_type, count)

    # 2. Get Resume Data
    resume_data = get_user_active_resume_data(user_id)

    # 3. Clean difficulty string
    clean_diff = clean_difficulty_str(difficulty)

    # 4. Generate Personalized Questions
    questions = generate_personalized_interview_questions(
        domain=domain,
        target_role=target_role,
        resume_data=resume_data,
        difficulty=clean_diff,
        question_type=question_type,
        count=count
    )

    # 5. Create Session in DB
    session_id = create_interview_session(user_id, domain, target_role, clean_diff, len(questions))

    return {
        "session_id": session_id,
        "domain": domain,
        "target_role": target_role,
        "difficulty": clean_diff,
        "question_type": question_type,
        "count": len(questions),
        "questions": questions,
        "resume_data": resume_data
    }
