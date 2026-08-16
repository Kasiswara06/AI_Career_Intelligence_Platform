import sys
import os
from pathlib import Path

# Ensure config and sys.path are initialized before relative module imports
import config

import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="AI Resume Screening & Career Intelligence Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS files
css_dir = Path(__file__).resolve().parent / "static" / "css"
if css_dir.exists():
    for css_file in css_dir.glob("*.css"):
        with open(css_file, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Import Auth Modules
from auth.login import render_login_page
from auth.register import render_register_page
from auth.forgot_password import render_forgot_password_page
from auth.authentication import logout_session

# Import Page Components (Imported from pages_modules to disable Streamlit's default alphabetical auto-ordering)
from pages_modules.home import render_home_page
from pages_modules.profile import render_profile_page
from pages_modules.resume_upload import render_resume_upload_page
from pages_modules.resume_management import render_resume_management_page
from pages_modules.Resume_Extraction import render_resume_extraction_page
from pages_modules.resume_analysis import render_resume_analysis_page
from pages_modules.ATS_Analysis import render_ats_analysis_page
from pages_modules.Resume_Improvement import render_resume_improvement_page
from pages_modules.Skill_Gap import render_skill_gap_page
from pages_modules.job_matching import render_job_matching_page
from pages_modules.Career_Recommendation import render_career_recommendation_page
from pages_modules.Course_Recommendation import render_course_recommendation_page
from pages_modules.Salary_Prediction import render_salary_prediction_page
from pages_modules.AI_Career_Assistant import render_ai_career_assistant_page
from pages_modules.AI_Interview import render_ai_interview_page
from pages_modules.Resume_Preparation import render_resume_preparation_page_module as render_resume_prep_page
from pages_modules.dashboard import render_dashboard_page
from pages_modules.reports import render_reports_page
from pages_modules.settings import render_settings_page
from pages_modules.admin_dashboard import render_admin_dashboard_page

from utils.theme_manager import apply_theme, THEMES

def main():
    """Main Application Entry Point & Custom Workflow Navigation Router."""
    
    # Initialize Session State Variables
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "🏠 Home"
    if "app_theme" not in st.session_state:
        st.session_state["app_theme"] = "Dark Glassmorphic"

    # Apply selected theme
    apply_theme(st.session_state["app_theme"])

    # Sidebar Header
    st.sidebar.markdown("## ⚡ AI Career Platform")

    # Theme selection in sidebar
    theme_keys = list(THEMES.keys())
    cur_idx = theme_keys.index(st.session_state["app_theme"]) if st.session_state["app_theme"] in theme_keys else 0
    chosen_theme = st.sidebar.selectbox("🎨 Choose Theme", theme_keys, index=cur_idx)
    if chosen_theme != st.session_state["app_theme"]:
        st.session_state["app_theme"] = chosen_theme
        st.rerun()

    if st.session_state["authenticated"]:
        user_id = st.session_state.get("user_id")
        user_name = st.session_state.get("user_name", "User")

        from auth.authorization import is_admin_user
        if user_id and is_admin_user(user_id):
            st.session_state["user_role"] = "admin"
            user_role = "admin"
        else:
            st.session_state["user_role"] = "user"
            user_role = "user"

        role_badge = "🛡️ Admin" if user_role == "admin" else "👤 Candidate"
        st.sidebar.caption(f"Logged in as: **{user_name}** ({role_badge})")
        st.sidebar.write("---")

        # Custom Navigation Order
        nav_options = [
            "🏠 Home",
            "👤 Profile",
            "📄 Resume Upload",
            "📂 Resume Management",
            "📑 Resume Extraction",
            "📊 Resume Analysis",
            "🎯 ATS Analysis",
            "🧠 Skill Gap Analysis",
            "💼 Job Matching",
            "🚀 Career Recommendation",
            "📚 Course Recommendation",
            "💰 Salary Prediction",
            "✨ Resume Improvement",
            "🤖 AI Career Assistant",
            "🎤 AI Interview Preparation",
            "📊 Dashboard",
            "📋 Reports",
            "⚙️ Settings"
        ]

        if user_role == "admin":
            nav_options.append("🛡️ Admin Dashboard")

        # Render Custom Grouped Sidebar Menu
        st.sidebar.markdown("### 🗺️ Navigation")
        
        default_idx = nav_options.index(st.session_state["current_page"]) if st.session_state["current_page"] in nav_options else 0
        selected_page = st.sidebar.radio("Select Page:", nav_options, index=default_idx)
        st.session_state["current_page"] = selected_page

        st.sidebar.write("---")
        if st.sidebar.button("Logout Account", use_container_width=True):
            logout_session()
            st.rerun()

        # Sequential Workflow Page Map
        page_map = {
            "🏠 Home": render_home_page,
            "👤 Profile": render_profile_page,
            "📄 Resume Upload": render_resume_upload_page,
            "📂 Resume Management": render_resume_management_page,
            "📑 Resume Extraction": render_resume_extraction_page,
            "📊 Resume Analysis": render_resume_analysis_page,
            "🎯 ATS Analysis": render_ats_analysis_page,
            "🧠 Skill Gap Analysis": render_skill_gap_page,
            "💼 Job Matching": render_job_matching_page,
            "🚀 Career Recommendation": render_career_recommendation_page,
            "📚 Course Recommendation": render_course_recommendation_page,
            "💰 Salary Prediction": render_salary_prediction_page,
            "✨ Resume Improvement": render_resume_improvement_page,
            "🤖 AI Career Assistant": render_ai_career_assistant_page,
            "🎤 AI Interview Preparation": render_ai_interview_page,
            "📊 Dashboard": render_dashboard_page,
            "📋 Reports": render_reports_page,
            "⚙️ Settings": render_settings_page,
            "🛡️ Admin Dashboard": render_admin_dashboard_page
        }

        render_func = page_map.get(selected_page, render_home_page)
        render_func()

    else:
        auth_choice = st.sidebar.radio("Account Access", ["🏠 Home", "🔑 Login", "📝 Register", "❓ Forgot Password"])
        
        if auth_choice == "🏠 Home":
            render_home_page()
        elif auth_choice == "🔑 Login":
            render_login_page()
        elif auth_choice == "📝 Register":
            render_register_page()
        elif auth_choice == "❓ Forgot Password":
            render_forgot_password_page()

if __name__ == "__main__":
    main()
