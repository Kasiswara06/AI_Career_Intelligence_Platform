import datetime
from typing import List, Dict, Any
from database.database import (
    get_user_chat_sessions,
    rename_chat_session,
    delete_chat_session,
    toggle_favorite_chat
)

def get_grouped_chat_sessions(user_id: int, search_query: str = "") -> Dict[str, List[Dict[str, Any]]]:
    """
    Fetches user chat sessions and groups them by date:
    - Today's Chats
    - Yesterday
    - Previous Week
    - Previous Month / Older
    """
    sessions = get_user_chat_sessions(user_id)
    if search_query.strip():
        q = search_query.lower()
        sessions = [s for s in sessions if q in str(s.get("session_title", "")).lower()]

    now = datetime.datetime.now().date()
    today_list = []
    yesterday_list = []
    week_list = []
    older_list = []

    for s in sessions:
        last_upd = s.get("last_updated")
        if isinstance(last_upd, str):
            try:
                dt_obj = datetime.datetime.strptime(last_upd[:19], "%Y-%m-%d %H:%M:%S").date()
            except Exception:
                dt_obj = now
        elif isinstance(last_upd, datetime.datetime):
            dt_obj = last_upd.date()
        else:
            dt_obj = now

        diff = (now - dt_obj).days

        if diff == 0:
            today_list.append(s)
        elif diff == 1:
            yesterday_list.append(s)
        elif diff <= 7:
            week_list.append(s)
        else:
            older_list.append(s)

    return {
        "Today's Chats": today_list,
        "Yesterday": yesterday_list,
        "Previous Week": week_list,
        "Previous Month": older_list
    }

def update_session_title(user_id: int, session_id: str, new_title: str):
    """Renames session."""
    return rename_chat_session(user_id, session_id, new_title)

def remove_session(user_id: int, session_id: str):
    """Deletes chat session."""
    return delete_chat_session(user_id, session_id)

def favorite_session(user_id: int, session_id: str, is_fav: bool):
    """Toggles favorite chat status."""
    return toggle_favorite_chat(user_id, session_id, is_fav)
