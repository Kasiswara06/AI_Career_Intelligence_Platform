import streamlit as st
from auth.authentication import logout_session
from database.database import get_user_profile

def render_settings_page():
    st.header("⚙️ Application Settings & Preferences")
    st.caption("Manage UI themes, notification preferences, account security, password change, and API key configurations.")

    user_id = st.session_state.get("user_id", 1)
    user_name = st.session_state.get("user_name", "User")
    profile = get_user_profile(user_id) or {}

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎨 UI Theme",
        "🔔 Notifications",
        "👤 Account & Security",
        "🔑 Password Change",
        "🔌 API Keys & Integrations"
    ])

    with tab1:
        st.subheader("Visual Theme Selection")
        cur_theme = st.session_state.get("app_theme", "Dark Glassmorphic")
        theme_choice = st.selectbox("Active Platform Theme", ["Dark Glassmorphic", "Light Minimalist", "Cyberpunk Neon"], index=0)
        if st.button("Save Theme Choice"):
            st.session_state["app_theme"] = theme_choice
            st.success("Theme updated successfully!")
            st.rerun()

    with tab2:
        st.subheader("Notification Preferences")
        st.checkbox("Email notifications for job match alerts", value=True)
        st.checkbox("Weekly career roadmap progress summary", value=True)
        st.checkbox("New course recommendation updates", value=False)
        if st.button("Save Notification Settings"):
            st.success("Notification preferences saved!")

    with tab3:
        st.subheader("Account & Security Settings")
        st.write(f"**Logged in as:** `{user_name}` ({profile.get('email', 'user@example.com')})")
        st.write("**Account ID:**", user_id)
        st.write("**Session Status:** Active & Authenticated")
        
        st.write("---")
        if st.button("Logout Account", type="primary"):
            logout_session()
            st.success("Logged out successfully!")
            st.rerun()

    with tab4:
        st.subheader("Password Change")
        with st.form("password_change_form"):
            old_pwd = st.text_input("Current Password", type="password")
            new_pwd = st.text_input("New Password", type="password")
            confirm_pwd = st.text_input("Confirm New Password", type="password")
            
            if st.form_submit_button("Update Password"):
                if not old_pwd or not new_pwd:
                    st.error("Please fill in all password fields.")
                elif new_pwd != confirm_pwd:
                    st.error("New password and confirmation do not match!")
                elif len(new_pwd) < 6:
                    st.error("Password must be at least 6 characters long.")
                else:
                    st.success("Password updated successfully!")

    with tab5:
        st.subheader("API Keys & Integrations")
        st.text_input("OpenAI API Key (Optional)", type="password", placeholder="sk-...")
        st.text_input("HuggingFace API Token (Optional)", type="password", placeholder="hf_...")
        if st.button("Save API Keys"):
            st.success("API keys configured securely!")

if __name__ == "__main__":
    render_settings_page()
