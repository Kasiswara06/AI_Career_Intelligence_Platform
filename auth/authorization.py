import streamlit as st
from database.database import execute_query

def is_admin_user(user_id: int) -> bool:
    """
    Checks if a user has the 'admin' role in the database.
    Does NOT select or check password fields.
    """
    if not user_id:
        return False
    
    # Check session state cache first (case-insensitive)
    session_role = str(st.session_state.get("user_role") or "").strip().lower()
    if session_role == "admin" and st.session_state.get("user_id") == user_id:
        return True
        
    res = execute_query("SELECT role FROM users WHERE id = %s", (user_id,), fetchone=True)
    if res and str(res.get("role") or "").strip().lower() == "admin":
        return True
    return False

def check_admin_access() -> bool:
    """
    Verifies current session authentication and admin authorization.
    """
    if not st.session_state.get("authenticated", False):
        return False
    user_id = st.session_state.get("user_id")
    return is_admin_user(user_id)
