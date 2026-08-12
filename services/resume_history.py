import logging
from typing import List, Dict, Any
from database.database import save_resume_history, get_user_resume_history

logger = logging.getLogger(__name__)

def log_resume_version_history(user_id: int, resume_id: int, version: int, action: str, ats_score: int = 0, status: str = 'Archived'):
    """
    Logs a new entry into resume_history database table.
    Actions: 'Uploaded', 'Replaced', 'Activated', 'Archived', 'Deleted'.
    """
    try:
        save_resume_history(user_id, resume_id, version, action, ats_score, status)
        logger.info(f"Logged resume history: user {user_id}, resume {resume_id}, v{version}, action: {action}")
    except Exception as e:
        logger.error(f"Error logging resume history: {e}")

def fetch_resume_version_history(user_id: int, resume_id: int = None) -> List[Dict[str, Any]]:
    """Fetches version history records for user's resumes."""
    return get_user_resume_history(user_id, resume_id)
