import streamlit as st
from utils.password_hash import check_password
from database.database import execute_query

def render_login_page():
    """Renders user login interface."""
    st.subheader("Welcome Back! Sign In")
    st.write("Access your AI Resume Screening & Career Intelligence Dashboard.")

    with st.form("login_form", clear_on_submit=False):
        email = st.text_input("Email Address", placeholder="rahul@example.com")
        password = st.text_input("Password", type="password")
        remember_me = st.checkbox("Remember Me")
        
        submit = st.form_submit_button("Sign In", use_container_width=True)

    if submit:
        if not email or not password:
            st.error("Please enter both email and password.")
            return

        user = execute_query("SELECT * FROM users WHERE email = %s", (email.strip().lower(),), fetchone=True)
        if not user:
            st.error("No account found with this email address.")
            return

        if check_password(password, user["password_hash"]):
            st.session_state.clear()
            st.session_state["authenticated"] = True
            st.session_state["user_id"] = user["id"]
            st.session_state["user_name"] = user["full_name"]
            st.session_state["user_email"] = user["email"]
            st.session_state["user_role"] = str(user.get("role", "user") or "user").strip().lower()
            st.session_state["remember_me"] = remember_me

            import uuid
            sess_id = f"SESS-{uuid.uuid4().hex[:8].upper()}"
            st.session_state["session_id"] = sess_id

            # Log Activity into login_activity & activity_logs
            from database.database import record_login_activity
            record_login_activity(user["id"], "SUCCESS", sess_id)

            st.success(f"Welcome back, {user['full_name']}!")
            st.rerun()
        else:
            st.error("Incorrect password. Please try again.")
