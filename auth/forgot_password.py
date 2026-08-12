import streamlit as st
from utils.helper import is_valid_email, is_strong_password
from utils.password_hash import hash_password
from utils.email_service import send_email_notification
from database.database import execute_query

def render_forgot_password_page():
    """Renders password recovery/reset interface."""
    st.subheader("Reset Password")
    st.write("Enter your registered email and choose a new password.")

    with st.form("forgot_password_form"):
        email = st.text_input("Registered Email Address")
        new_password = st.text_input("New Password", type="password")
        confirm_new_password = st.text_input("Confirm New Password", type="password")
        submit = st.form_submit_button("Reset Password", use_container_width=True)

    if submit:
        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
            return

        user = execute_query("SELECT id FROM users WHERE email = %s", (email.strip().lower(),), fetchone=True)
        if not user:
            st.error("No account found registered with this email.")
            return

        is_strong, msg = is_strong_password(new_password)
        if not is_strong:
            st.error(msg)
            return

        if new_password != confirm_new_password:
            st.error("New passwords do not match.")
            return

        pwd_hash = hash_password(new_password)
        execute_query("UPDATE users SET password_hash = %s WHERE id = %s", (pwd_hash, user["id"]), commit=True)

        send_email_notification(
            email.strip().lower(),
            "Password Reset Confirmation - AI Career Platform",
            "<p>Your password has been successfully updated. You can now login with your new credentials.</p>"
        )

        st.success("Password reset successfully! Please login with your new password.")
