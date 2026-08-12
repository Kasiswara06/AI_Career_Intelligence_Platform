import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from database.database import get_user_profile
from services.resume_service import get_user_active_resume
from services.dashboard_service import get_dashboard_summary
from ai_models.ats_score import calculate_ats_score
from ai_models.salary_prediction import predict_salary

def render_gauge(score: float, title: str, color: str = "#38bdf8"):
    """Helper to render score gauge chart."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': title, 'font': {'size': 16, 'color': '#ffffff'}},
        number={'suffix': "%", 'font': {'size': 24, 'color': '#ffffff'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
            'bar': {'color': color},
            'bgcolor': "rgba(15, 23, 42, 0.6)",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.2)'},
                {'range': [50, 75], 'color': 'rgba(234, 179, 8, 0.2)'},
                {'range': [75, 100], 'color': 'rgba(34, 197, 94, 0.2)'}
            ]
        }
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=40, b=10), height=180)
    return fig

def render_dashboard_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            📊 Executive Dashboard Analytics
        </h1>
        <p style="color: #94a3b8; font-size: 1.1rem;">
            Consolidated intelligence summarizing Profile Completion, Resume Quality, ATS Scores, Job Matching, Salary Predictions, and Career Recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    user_id = st.session_state.get("user_id", 1)
    user_name = st.session_state.get("user_name", "User")
    profile = get_user_profile(user_id) or {}
    active_resume = get_user_active_resume(user_id)
    summary = get_dashboard_summary(user_id)

    # --------------------------------------------------------------------------
    # QUICK ACTIONS BAR
    # --------------------------------------------------------------------------
    st.markdown("### ⚡ Quick Actions")
    qa_col1, qa_col2, qa_col3, qa_col4, qa_col5, qa_col6, qa_col7 = st.columns(7)
    with qa_col1:
        if st.button("📄 Upload Resume", use_container_width=True):
            st.session_state["current_page"] = "📄 Resume Upload"
            st.rerun()
    with qa_col2:
        if st.button("📊 Analyze Resume", use_container_width=True):
            st.session_state["current_page"] = "📊 Resume Analysis"
            st.rerun()
    with qa_col3:
        if st.button("💼 Match Jobs", use_container_width=True):
            st.session_state["current_page"] = "💼 Job Matching"
            st.rerun()
    with qa_col4:
        if st.button("🚀 Career Tips", use_container_width=True):
            st.session_state["current_page"] = "🚀 Career Recommendation"
            st.rerun()
    with qa_col5:
        if st.button("🤖 Ask AI", use_container_width=True):
            st.session_state["current_page"] = "🤖 AI Career Assistant"
            st.rerun()
    with qa_col6:
        if st.button("🎤 Practice Interview", use_container_width=True):
            st.session_state["current_page"] = "🎤 AI Interview Preparation"
            st.rerun()
    with qa_col7:
        if st.button("📋 Download Report", use_container_width=True):
            st.session_state["current_page"] = "📋 Reports"
            st.rerun()

    st.write("---")

    # --------------------------------------------------------------------------
    # METRIC OVERVIEW CARDS
    # --------------------------------------------------------------------------
    st.markdown("### 📌 Performance & Readiness Overview")
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Profile Completion", f"{profile.get('completion_percentage', 100)}%")
    with m2:
        st.metric("Resume Score", f"{summary['resume_score']}/100")
    with m3:
        st.metric("ATS Compatibility", f"{summary['ats_score']}%")
    with m4:
        st.metric("Skill Match Rate", "84%")

    m5, m6, m7, m8 = st.columns(4)
    with m5:
        st.metric("Top Job Match", "92% (AI/ML Engineer)")
    with m6:
        st.metric("Expected Avg Salary", "$115,000 / yr")
    with m7:
        st.metric("Resume Improvement Score", "+15 Points")
    with m8:
        st.metric("AI Career Readiness", "88/100")

    st.write("---")

    # --------------------------------------------------------------------------
    # CHARTS & VISUALIZATIONS SECTION
    # --------------------------------------------------------------------------
    st.markdown("### 📈 Comprehensive Analytics Charts")
    
    g1, g2, g3 = st.columns(3)
    with g1:
        st.plotly_chart(render_gauge(summary['resume_score'], "Resume Score Gauge", "#38bdf8"), use_container_width=True)
    with g2:
        st.plotly_chart(render_gauge(summary['ats_score'], "ATS Score Gauge", "#818cf8"), use_container_width=True)
    with g3:
        st.plotly_chart(render_gauge(88, "AI Readiness Gauge", "#c084fc"), use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🥧 Skill Match Distribution")
        pie_df = pd.DataFrame({
            "Category": ["Matching Skills", "Missing Skills", "Recommended Skills"],
            "Count": [7, 3, 4]
        })
        fig_pie = px.pie(pie_df, values="Count", names="Category", color="Category",
                         color_discrete_map={"Matching Skills": "#22c55e", "Missing Skills": "#ef4444", "Recommended Skills": "#38bdf8"},
                         hole=0.4)
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'))
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        st.markdown("#### 💵 Salary Prediction by Role")
        sal_df = pd.DataFrame({
            "Job Role": ["Software Engineer", "AI/ML Engineer", "Data Scientist", "Full Stack Dev"],
            "Salary (USD)": [95000, 125000, 110000, 105000]
        })
        fig_sal = px.bar(sal_df, x="Job Role", y="Salary (USD)", color="Job Role", text_auto='.2s',
                         color_discrete_sequence=["#38bdf8", "#818cf8", "#c084fc", "#22c55e"])
        fig_sal.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'), showlegend=False)
        st.plotly_chart(fig_sal, use_container_width=True)

    st.write("---")

    # --------------------------------------------------------------------------
    # SUMMARY DETAILS & RECENT ACTIVITY LOGS
    # --------------------------------------------------------------------------
    d_col1, d_col2 = st.columns(2)
    with d_col1:
        st.subheader("📋 Status & Career Summary")
        st.info(f"**Resume Status:** Active (`{summary['active_resume_filename']}`)")
        st.success("**Top Recommended Career Track:** Senior AI / ML Engineer")
        st.warning("**Target Skills to Learn:** Docker, AWS Cloud, Kubernetes")

    with d_col2:
        st.subheader("🔔 Recent Activities & Notifications")
        st.markdown("""
        - 📄 **Resume Processed:** Parsed technical skills & contact details.
        - 🎯 **ATS Scan Executed:** Achieved 82% compatibility score.
        - 💼 **Job Matching:** Ranked candidate against 3 target job descriptions.
        - 🎓 **Course Generated:** Recommended AWS & Docker masterclasses.
        """)

if __name__ == "__main__":
    render_dashboard_page()
