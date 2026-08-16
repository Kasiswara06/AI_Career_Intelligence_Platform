import streamlit as st
from utils.helper import is_valid_email, is_strong_password
from utils.password_hash import hash_password
from database.database import execute_query

def render_register_page():
    """Renders basic user registration interface."""
    st.subheader("Create Your Account")
    st.write("Fill in your basic information to get started.")

    with st.form("register_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
            email = st.text_input("Email Address", placeholder="rahul@example.com")
            mobile = st.text_input("Mobile Number", placeholder="9876543210")

        with col2:
            age = st.number_input("Age", min_value=16, max_value=80, value=22)
            password = st.text_input("Password", type="password", help="At least 6 chars with letters and numbers")
            confirm_password = st.text_input("Confirm Password", type="password")

        submit = st.form_submit_button("Register Account", use_container_width=True)

    if submit:
        # Validation checks
        if not full_name.strip():
            st.error("Please enter your full name.")
            return

        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
            return

        if not mobile.strip() or len(mobile.strip()) < 10:
            st.error("Please enter a valid 10-digit mobile number.")
            return

        is_strong, msg = is_strong_password(password)
        if not is_strong:
            st.error(msg)
            return

        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        # Check duplicate email
        existing_user = execute_query("SELECT id FROM users WHERE email = %s", (email.strip().lower(),), fetchone=True)
        if existing_user:
            st.error("An account with this email address already exists. Please login instead.")
            return

        # Hash Password and Insert User
        pwd_hash = hash_password(password)
        try:
            user_id = execute_query(
                "INSERT INTO users (full_name, fullname, email, mobile, age, password_hash) VALUES (%s, %s, %s, %s, %s, %s)",
                (full_name.strip(), full_name.strip(), email.strip().lower(), mobile.strip(), int(age), pwd_hash),
                commit=True
            )
        except Exception:
            user_id = execute_query(
                "INSERT INTO users (full_name, email, mobile, age, password_hash) VALUES (%s, %s, %s, %s, %s)",
                (full_name.strip(), email.strip().lower(), mobile.strip(), int(age), pwd_hash),
                commit=True
            )

        if user_id:
            # Create matching initial profile
            execute_query(
                "INSERT INTO profiles (user_id, completion_percentage) VALUES (%s, %s)",
                (user_id, 20),
                commit=True
            )
            st.success("Registration successful! You can now log in to complete your profile.")
            st.session_state["active_auth_tab"] = "Login"
            st.rerun()
        else:
            st.error("Failed to register user. Please try again.")
