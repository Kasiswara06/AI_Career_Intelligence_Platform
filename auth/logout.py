import streamlit as st
from database.database import execute_query

def logout_user():
    """Clears user authentication session and logs activity."""
    user_id = st.session_state.get("user_id")
    if user_id:
        try:
            execute_query(
                "INSERT INTO activity_logs (user_id, action, details) VALUES (%s, %s, %s)",
                (user_id, "LOGOUT", "User logged out"),
                commit=True
            )
        except Exception:
            pass

    st.session_state.clear()
    st.session_state["authenticated"] = False
    st.session_state["current_page"] = "🏠 Home"
    st.rerun()
