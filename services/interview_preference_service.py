import logging
from database.database import execute_query
from utils.interview_utils import DOMAINS, TARGET_ROLES

logger = logging.getLogger(__name__)

def get_user_interview_preference(user_id: int) -> dict:
    """
    Fetches the saved domain, target role, experience level, difficulty, question type, and count preference for a user.
    Returns default values if no preference has been saved yet.
    """
    if not user_id:
        return {
            "domain": "Python Development",
            "target_role": "Python Developer",
            "experience_level": "Mid Level (2-5 yrs)",
            "difficulty": "Medium",
            "question_type": "Mixed",
            "question_count": 10
        }

    pref = execute_query(
        """
        SELECT domain, target_role, experience_level, difficulty, question_type, question_count
        FROM interview_preferences
        WHERE user_id = %s
        """,
        (user_id,),
        fetchone=True
    )

    if pref:
        return {
            "domain": pref.get("domain") or "Python Development",
            "target_role": pref.get("target_role") or "Python Developer",
            "experience_level": pref.get("experience_level") or "Mid Level (2-5 yrs)",
            "difficulty": pref.get("difficulty") or "Medium",
            "question_type": pref.get("question_type") or "Mixed",
            "question_count": pref.get("question_count") or 10
        }

    # Infer default preference from user profile if available
    profile = execute_query("SELECT current_role, skills, technical_skills, experience_years FROM profiles WHERE user_id = %s", (user_id,), fetchone=True) or {}
    role = profile.get("current_role") or "Python Developer"
    exp_yrs = float(profile.get("experience_years") or 0.0)
    
    exp_lvl = "Entry Level (0-2 yrs)" if exp_yrs < 2 else ("Mid Level (2-5 yrs)" if exp_yrs < 5 else ("Senior Level (5-8 yrs)" if exp_yrs < 8 else "Lead / Architect (8+ yrs)"))

    domain = "Python Development"
    role_lower = role.lower()
    if "data scientist" in role_lower or "science" in role_lower:
        domain = "Data Science"
    elif "data analyst" in role_lower or "analytics" in role_lower:
        domain = "Data Analytics"
    elif "machine learning" in role_lower or "ml" in role_lower:
        domain = "Machine Learning"
    elif "ai" in role_lower or "artificial" in role_lower:
        domain = "Artificial Intelligence"
    elif "web" in role_lower or "full stack" in role_lower:
        domain = "Web Development"
    elif "sql" in role_lower or "database" in role_lower:
        domain = "SQL & Database"

    return {
        "domain": domain,
        "target_role": role,
        "experience_level": exp_lvl,
        "difficulty": "Medium",
        "question_type": "Mixed",
        "question_count": 10
    }


def save_user_interview_preference(
    user_id: int,
    domain: str,
    target_role: str,
    experience_level: str = "Mid Level (2-5 yrs)",
    difficulty: str = "Medium",
    question_type: str = "Mixed",
    question_count: int = 10
) -> bool:
    """
    Saves or updates the user's interview domain preference in the database.
    """
    if not user_id:
        return False

    existing = execute_query("SELECT preference_id FROM interview_preferences WHERE user_id = %s", (user_id,), fetchone=True)

    if existing:
        query = """
        UPDATE interview_preferences
        SET domain = %s, target_role = %s, experience_level = %s, difficulty = %s, question_type = %s, question_count = %s, updated_at = CURRENT_TIMESTAMP
        WHERE user_id = %s
        """
        execute_query(query, (domain, target_role, experience_level, difficulty, question_type, question_count, user_id), commit=True)
    else:
        query = """
        INSERT INTO interview_preferences (user_id, domain, target_role, experience_level, difficulty, question_type, question_count)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        execute_query(query, (user_id, domain, target_role, experience_level, difficulty, question_type, question_count), commit=True)

    return True
