import streamlit as st
from database.database import execute_query

def logout_user():
    """Clears user authentication session and logs activity."""
    user_id = st.session_state.get("user_id")
    if user_id:
        execute_query(
            "INSERT INTO activity_logs (user_id, action, details) VALUES (%s, %s, %s)",
            (user_id, "LOGOUT", "User logged out"),
            commit=True
        )

    for key in ["authenticated", "user_id", "user_name", "user_email", "remember_me"]:
        if key in st.session_state:
            del st.session_state[key]

    st.rerun()
