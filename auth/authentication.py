import streamlit as st
from utils.password_hash import verify_password, hash_password
from database.database import get_user_by_email, create_user

def authenticate_user(email, password):
    """
    Authenticates user credentials against the database.
    Returns (success, user_dict_or_error_msg).
    """
    user = get_user_by_email(email)
    if not user:
        return False, "User not found with this email."
    
    stored_hash = user.get("password_hash")
    if stored_hash and verify_password(password, stored_hash):
        return True, user
    return False, "Invalid email or password."

def register_new_user(full_name, email, mobile, age, password):
    """
    Registers a new user into the database after hashing password.
    Returns (success, user_id_or_error_msg).
    """
    user_id = create_user(full_name, email, mobile, age, password)
    if user_id:
        return True, user_id
    return False, "User with this email already exists."

def logout_session():
    """Clears authentication session state and logs activity."""
    user_id = st.session_state.get("user_id")
    sess_id = st.session_state.get("session_id", "")
    if user_id:
        try:
            from database.database import record_logout_activity
            record_logout_activity(user_id, sess_id)
        except Exception:
            pass
    st.session_state["authenticated"] = False
    st.session_state["user_id"] = None
    st.session_state["user_email"] = None
    st.session_state["user_name"] = None
    st.session_state["session_id"] = None
    st.session_state["current_page"] = "🏠 Home"
