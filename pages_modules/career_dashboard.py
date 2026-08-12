import streamlit as st
from database.database import execute_query
from utils.charts import create_ats_gauge, create_salary_prediction_chart, create_career_growth_graph, create_skill_distribution_pie
from ai_models.salary_prediction import predict_salary
from ai_models.learning_recommendation import get_learning_recommendations

def render_career_dashboard_page():
    """Renders comprehensive AI Career Analytics Dashboard with Plotly visuals."""
    user_id = st.session_state.get("user_id")
    user_name = st.session_state.get("user_name", "User")

    st.markdown('<h1 class="gradient-text">AI Career Intelligence Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.write("Real-time career growth telemetry, salary forecasting, skill gap insights, and learning roadmaps.")

    profile = execute_query("SELECT * FROM profiles WHERE user_id = %s", (user_id,), fetchone=True) or {}
    active_resume = execute_query("SELECT * FROM resumes WHERE user_id = %s AND is_active = 1", (user_id,), fetchone=True)

    analysis = None
    if active_resume:
        analysis = execute_query(
            "SELECT * FROM resume_analysis WHERE resume_id = %s ORDER BY id DESC LIMIT 1",
            (active_resume["id"],),
            fetchone=True
        )

    exp_years = float(profile.get("experience_years") or 1.0)
    skills = [s.strip() for s in (profile.get("skills") or "Python, SQL, Machine Learning").split(",") if s.strip()]

    # Predict Salary via Random Forest
    salary_res = predict_salary(experience_years=exp_years, skill_count=len(skills))

    # Top Telemetry Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Predicted Salary", f"₹{salary_res['predicted_lpa']} LPA", "+14.2% YoY")
    with col2:
        ats = analysis["ats_score"] if analysis else 65
        st.metric("ATS Compatibility", f"{ats}/100")
    with col3:
        st.metric("Identified Skills", f"{len(skills)}")
    with col4:
        st.metric("Experience Level", f"{exp_years} Yrs")

    st.write("---")

    # Plotly Charts Grid 1
    col1, col2 = st.columns(2)
    with col1:
        fig_sal = create_salary_prediction_chart(exp_years=exp_years, predicted_lpa=salary_res["predicted_lpa"])
        st.plotly_chart(fig_sal, use_container_width=True)

    with col2:
        fig_growth = create_career_growth_graph(skill_count=len(skills), ats_score=ats)
        st.plotly_chart(fig_growth, use_container_width=True)

    st.write("---")

    # Courses & Learning Recommendations
    st.subheader("📚 Recommended Upskilling Courses")
    missing_sample = ["Docker", "Kubernetes", "AWS"]
    courses = get_learning_recommendations(missing_sample)

    for course in courses:
        st.markdown(f"""
        <div class="glass-card" style="padding: 12px 18px; margin-bottom: 10px;">
            <b>{course['course_title']}</b> — <i>{course['provider']} ({course['level']})</i><br/>
            <span style="font-size: 13px; color: #9CA3AF;">Skills: {course['skills_covered']}</span><br/>
            <a href="{course['url']}" target="_blank" style="color: #818CF8; font-size: 13px;">View Course Link ↗</a>
        </div>
        """, unsafe_allow_html=True)
