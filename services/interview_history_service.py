import json
import logging
from database.database import execute_query

logger = logging.getLogger(__name__)

def create_interview_session(
    user_id: int,
    domain: str,
    target_role: str,
    difficulty: str,
    total_questions: int
) -> int:
    """
    Creates a new record in interview_sessions and returns the session_id.
    """
    if not user_id:
        return 0

    execute_query(
        """
        INSERT INTO interview_sessions (user_id, domain, target_role, difficulty, total_questions)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (user_id, domain, target_role, difficulty, total_questions),
        commit=True
    )
    
    session = execute_query(
        "SELECT session_id FROM interview_sessions WHERE user_id = %s ORDER BY created_at DESC LIMIT 1",
        (user_id,),
        fetchone=True
    )
    return session.get("session_id", 0) if session else 0


def update_interview_session_results(
    session_id: int,
    score: int,
    technical_score: int,
    communication_score: int,
    readiness_score: int
) -> bool:
    """
    Updates final scores for an interview session.
    """
    if not session_id:
        return False

    execute_query(
        """
        UPDATE interview_sessions
        SET score = %s, technical_score = %s, communication_score = %s, readiness_score = %s
        WHERE session_id = %s
        """,
        (score, technical_score, communication_score, readiness_score, session_id),
        commit=True
    )
    return True


def save_interview_question_response(
    session_id: int,
    user_id: int,
    question: str,
    domain: str,
    target_role: str,
    category: str,
    difficulty: str,
    model_answer: str,
    explanation: str = "",
    example: str = "",
    key_points: list = None,
    interview_tip: str = "",
    user_answer: str = "",
    user_score: int = 0,
    feedback: str = ""
) -> bool:
    """
    Saves an answered question in interview_questions table with complete model answer details.
    """
    kp_json = json.dumps(key_points) if isinstance(key_points, list) else str(key_points or "")

    execute_query(
        """
        INSERT INTO interview_questions
        (session_id, user_id, role, domain, target_role, category, question, question_type, difficulty,
         model_answer, explanation, example, key_points, interview_tip, user_answer, user_score, score, feedback)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            session_id, user_id, target_role, domain, target_role, category, question, category, difficulty,
            model_answer, explanation, example, kp_json, interview_tip, user_answer, user_score, user_score, feedback
        ),
        commit=True
    )
    return True


def get_user_interview_sessions_history(user_id: int) -> list:
    """
    Fetches all completed interview sessions for the user.
    """
    if not user_id:
        return []

    return execute_query(
        """
        SELECT session_id, domain, target_role, difficulty, total_questions, score, technical_score, communication_score, readiness_score, created_at
        FROM interview_sessions
        WHERE user_id = %s
        ORDER BY created_at DESC
        """,
        (user_id,),
        fetchall=True
    ) or []


def get_session_questions(session_id: int) -> list:
    """
    Fetches all questions and answers associated with a session.
    """
    if not session_id:
        return []

    res = execute_query(
        """
        SELECT question_id, session_id, domain, target_role, category, question, question_type, difficulty,
               model_answer, explanation, example, key_points, interview_tip, user_answer, user_score, feedback
        FROM interview_questions
        WHERE session_id = %s
        """,
        (session_id,),
        fetchall=True
    )
    if res is not None:
        return res

    return execute_query(
        "SELECT * FROM interview_questions WHERE session_id = %s",
        (session_id,),
        fetchall=True
    ) or []


def delete_interview_session(session_id: int) -> bool:
    """
    Deletes an interview session and all its stored questions.
    """
    if not session_id:
        return False

    execute_query("DELETE FROM interview_questions WHERE session_id = %s", (session_id,), commit=True)
    execute_query("DELETE FROM interview_sessions WHERE session_id = %s", (session_id,), commit=True)
    return True


def save_question_bookmark(user_id: int, question_id: int, question: str, domain: str, target_role: str, model_answer: str) -> bool:
    """
    Stars / bookmarks a question into saved_interview_questions table.
    """
    if not user_id or not question:
        return False

    existing = execute_query(
        "SELECT saved_id FROM saved_interview_questions WHERE user_id = %s AND question = %s",
        (user_id, question),
        fetchone=True
    )
    if not existing:
        execute_query(
            """
            INSERT INTO saved_interview_questions (user_id, question_id, question, domain, target_role, model_answer)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (user_id, question_id or 0, question, domain, target_role, model_answer),
            commit=True
        )
    return True


def remove_question_bookmark(user_id: int, question: str) -> bool:
    """
    Unstars / removes a bookmarked question.
    """
    if not user_id or not question:
        return False

    execute_query(
        "DELETE FROM saved_interview_questions WHERE user_id = %s AND question = %s",
        (user_id, question),
        commit=True
    )
    return True


def get_saved_questions(user_id: int) -> list:
    """
    Fetches all bookmarked / starred questions for the user.
    """
    if not user_id:
        return []

    return execute_query(
        """
        SELECT saved_id, question_id, question, domain, target_role, model_answer, created_at
        FROM saved_interview_questions
        WHERE user_id = %s
        ORDER BY created_at DESC
        """,
        (user_id,),
        fetchall=True
    ) or []
