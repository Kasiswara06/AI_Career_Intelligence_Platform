import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from database.database import get_user_profile
from services.resume_service import get_user_active_resume
from services.dashboard_service import get_dashboard_summary

def render_gauge_chart(score: float, title: str, bar_color: str = "#38bdf8") -> go.Figure:
    """Helper to render interactive score gauge charts."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': title, 'font': {'size': 16, 'color': '#ffffff'}},
        number={'suffix': "%", 'font': {'size': 24, 'color': '#ffffff'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
            'bar': {'color': bar_color},
            'bgcolor': "rgba(15, 23, 42, 0.6)",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.2)'},
                {'range': [50, 75], 'color': 'rgba(234, 179, 8, 0.2)'},
                {'range': [75, 100], 'color': 'rgba(34, 197, 94, 0.2)'}
            ]
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=15, r=15, t=40, b=15),
        height=180
    )
    return fig

def render_dashboard_page():
    user_id = st.session_state.get("user_id", 1)
    summary = get_dashboard_summary(user_id)

    # Header Title Banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 0.95)); padding: 20px 24px; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.12); margin-bottom: 24px;">
        <h1 style="margin: 0; color: #f8fafc; font-size: 2rem;">⚡ Final Career Intelligence Dashboard</h1>
        <p style="color: #94a3b8; margin-top: 6px; font-size: 1rem;">
            Unified AI Career Analytics: Real-time Profile Status, ATS Optimization, Skill Gap Analysis, Job Matching, Course Recommendations, and Salary Projections.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # QUICK ACTIONS TOOLBAR (Section 20)
    # --------------------------------------------------------------------------
    st.markdown("### ⚡ Quick Actions Toolbar")
    q_col1, q_col2, q_col3, q_col4, q_col5, q_col6, q_col7, q_col8, q_col9 = st.columns(9)
    
    with q_col1:
        if st.button("📄 Upload Resume", use_container_width=True):
            st.session_state["current_page"] = "📄 Resume Upload"
            st.rerun()
    with q_col2:
        if st.button("📊 Analyze Resume", use_container_width=True):
            st.session_state["current_page"] = "📊 Resume Analysis"
            st.rerun()
    with q_col3:
        if st.button("🧠 Skill Gap", use_container_width=True):
            st.session_state["current_page"] = "🧠 Skill Gap Analysis"
            st.rerun()
    with q_col4:
        if st.button("💼 Find Jobs", use_container_width=True):
            st.session_state["current_page"] = "💼 Job Matching"
            st.rerun()
    with q_col5:
        if st.button("🚀 Career Rec", use_container_width=True):
            st.session_state["current_page"] = "🚀 Career Recommendation"
            st.rerun()
    with q_col6:
        if st.button("📚 Find Courses", use_container_width=True):
            st.session_state["current_page"] = "📚 Course Recommendation"
            st.rerun()
    with q_col7:
        if st.button("🤖 Ask AI", use_container_width=True):
            st.session_state["current_page"] = "🤖 AI Career Assistant"
            st.rerun()
    with q_col8:
        if st.button("🎤 Practice Interview", use_container_width=True):
            st.session_state["current_page"] = "🎤 AI Interview Preparation"
            st.rerun()
    with q_col9:
        if st.button("📋 Download Report", use_container_width=True):
            st.session_state["current_page"] = "📋 Reports"
            st.rerun()

    st.write("---")

    # --------------------------------------------------------------------------
    # KEY PERFORMANCE INDICATOR (KPI) CARDS (Section 19)
    # --------------------------------------------------------------------------
    st.markdown("### 📌 Executive KPI Metrics")
    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    with kpi1:
        st.metric("Resume Score", f"{summary['resume_score']}/100")
    with kpi2:
        st.metric("ATS Score", f"{summary['ats_score']}%")
    with kpi3:
        st.metric("Skill Match", f"{summary['skill_match_pct']}%")
    with kpi4:
        st.metric("Job Match", f"{summary['top_job_match_pct']}%")
    with kpi5:
        st.metric("Career Readiness", f"{summary['readiness_score']}/100")
    with kpi6:
        st.metric("Expected Salary", summary['expected_salary'])

    st.write("---")

    # --------------------------------------------------------------------------
    # EXACT 18-SECTION WORKFLOW LAYOUT (Section 18)
    # --------------------------------------------------------------------------
    st.markdown("## 🎯 Structured Milestone 4 Career Intelligence")

    # 1. Welcome / Profile Overview & 2. Profile Completion
    c_sec1, c_sec2 = st.columns([2, 1])
    with c_sec1:
        st.markdown("### 1. 👤 Welcome / Profile Overview")
        st.info(f"**Candidate:** {summary['user_name']} | **Target Role:** {summary['recommended_career']} | **Projects:** {summary['projects_count']} | **Certificates:** {summary['certifications_count']}")
    with c_sec2:
        st.markdown("### 2. 📈 Profile Completion")
        p_pct = summary['profile_completion']
        st.progress(p_pct / 100.0)
        st.caption(f"Profile Completeness: **{p_pct}%**")

    st.write("---")

    # 3. Resume Status, 4. Resume Score, 5. ATS Score
    c_res1, c_res2, c_res3 = st.columns(3)
    with c_res1:
        st.markdown("### 3. 📂 Resume Status")
        status_label = "🟢 Active" if summary['has_active_resume'] else "🔴 Missing"
        st.metric("Status", status_label, summary['active_resume_filename'])
    with c_res2:
        st.markdown("### 4. 📊 Resume Score")
        st.plotly_chart(render_gauge_chart(summary['resume_score'], "Resume Score Gauge", "#38bdf8"), use_container_width=True)
    with c_res3:
        st.markdown("### 5. 🎯 ATS Score")
        st.plotly_chart(render_gauge_chart(summary['ats_score'], "ATS Score Gauge", "#818cf8"), use_container_width=True)

    st.write("---")

    # 6. Resume Summary
    st.markdown("### 6. 📑 AI Resume Summary")
    st.markdown(f"> {summary['resume_summary']}")

    st.write("---")

    # 7. Detected Skills & 8. Missing Skills
    col_sk1, col_sk2 = st.columns(2)
    with col_sk1:
        st.markdown("### 7. ✔️ Detected Skills")
        st.write(", ".join([f"`{s}`" for s in summary['detected_skills']]))
    with col_sk2:
        st.markdown("### 8. ❌ Missing Skills")
        st.write(", ".join([f"`{s}`" for s in summary['missing_skills']]))

    st.write("---")

    # 9. Skill Gap Analysis & Skill Distribution Charts
    st.markdown("### 9. 🧠 Skill Gap & Distribution Analysis")
    gap_col1, gap_col2 = st.columns(2)
    with gap_col1:
        st.markdown("#### Detected vs Missing Skills")
        sk_pie_df = pd.DataFrame({
            "Skill Type": ["Matching Skills", "Missing Skills"],
            "Percentage": [summary['skill_match_pct'], summary['skill_gap_pct']]
        })
        fig_gap = px.pie(sk_pie_df, values="Percentage", names="Skill Type", color="Skill Type",
                         color_discrete_map={"Matching Skills": "#22c55e", "Missing Skills": "#ef4444"},
                         hole=0.4)
        fig_gap.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'))
        st.plotly_chart(fig_gap, use_container_width=True)
        
    with gap_col2:
        st.markdown("#### Skill Distribution")
        sk_dist_df = pd.DataFrame({
            "Skill": summary['detected_skills'][:6],
            "Proficiency (%)": [95, 90, 88, 85, 82, 80][:len(summary['detected_skills'][:6])]
        })
        fig_dist = px.bar(sk_dist_df, x="Skill", y="Proficiency (%)", color="Skill", text_auto=True,
                          color_discrete_sequence=["#38bdf8", "#818cf8", "#c084fc", "#22c55e", "#facc15", "#fb923c"])
        fig_dist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'), showlegend=False)
        st.plotly_chart(fig_dist, use_container_width=True)

    st.write("---")

    # 10. Resume Improvement Suggestions
    st.markdown("### 10. ✨ Resume Improvement Suggestions")
    for idx, tip in enumerate(summary['improvement_tips'], 1):
        st.markdown(f"**{idx}.** {tip}")

    st.write("---")

    # 11. Top Job Recommendations & 12. Job Match Percentage
    st.markdown("### 11. 💼 Top Job Recommendations & Match Percentage")
    job_c1, job_c2 = st.columns([2, 1])
    with job_c1:
        st.markdown(f"#### 🏆 Top Match: **{summary['top_job_title']}** @ `{summary['top_job_company']}`")
        st.success(f"**Match Compatibility Score:** {summary['top_job_match_pct']}%")
    with job_c2:
        jm_df = pd.DataFrame({
            "Job Title": [summary['top_job_title'], "Python Dev Lead", "Data Engineer"],
            "Match %": [summary['top_job_match_pct'], 85.0, 78.0]
        })
        fig_jm = px.bar(jm_df, x="Job Title", y="Match %", color="Job Title", text_auto=True,
                        color_discrete_sequence=["#22c55e", "#38bdf8", "#818cf8"])
        fig_jm.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'), showlegend=False)
        st.plotly_chart(fig_jm, use_container_width=True)

    st.write("---")

    # 13. Career Recommendations
    st.markdown("### 13. 🚀 Career Recommendations & Growth")
    car_c1, car_c2 = st.columns([2, 1])
    with car_c1:
        st.markdown(f"#### Recommended Track: **{summary['recommended_career']}**")
        st.markdown(f"**Industry Demand:** `{summary['career_growth']}`")
    with car_c2:
        car_df = pd.DataFrame({
            "Role": [summary['recommended_career'], "Data Scientist", "Full Stack AI"],
            "Growth Rate %": [35, 28, 22]
        })
        fig_car = px.pie(car_df, values="Growth Rate %", names="Role", color_discrete_sequence=["#38bdf8", "#818cf8", "#c084fc"])
        fig_car.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'))
        st.plotly_chart(fig_car, use_container_width=True)

    st.write("---")

    # 14. Course Recommendations & 15. Certification Recommendations
    st.markdown("### 14 & 15. 📚 Course & Certification Recommendations")
    crs_cols = st.columns(len(summary['recommended_courses'][:3]) or 1)
    for idx, crs in enumerate(summary['recommended_courses'][:3]):
        with crs_cols[idx % len(crs_cols)]:
            st.markdown(f"#### 📖 [{crs['course_title']}]({crs['link']})")
            st.caption(f"**Platform:** {crs['platform']} | **Skill:** `{crs['target_skill']}` | **Duration:** {crs['duration']}")

    st.write("---")

    # 16. Expected Salary
    st.markdown("### 16. 💰 Expected Salary Prediction")
    sal_c1, sal_c2 = st.columns([1, 2])
    with sal_c1:
        st.metric("Predicted Annual Compensation", summary['expected_salary'])
        st.caption(f"Range: **${summary['min_salary']:,}** - **${summary['max_salary']:,}** USD")
    with sal_c2:
        sal_df = pd.DataFrame({
            "Compensation Tier": ["Minimum", "Predicted Average", "Maximum"],
            "Salary ($)": [summary['min_salary'], summary['predicted_salary_num'], summary['max_salary']]
        })
        fig_sal = px.bar(sal_df, x="Compensation Tier", y="Salary ($)", color="Compensation Tier", text_auto='.2s',
                         color_discrete_sequence=["#38bdf8", "#818cf8", "#c084fc"])
        fig_sal.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'), showlegend=False)
        st.plotly_chart(fig_sal, use_container_width=True)

    st.write("---")

    # 17. AI Career Readiness Score
    st.markdown("### 17. 🎓 AI Career Readiness Score")
    r_col1, r_col2 = st.columns([1, 2])
    with r_col1:
        st.metric("Overall Career Readiness", f"{summary['readiness_score']}/100")
    with r_col2:
        st.plotly_chart(render_gauge_chart(summary['readiness_score'], "Career Readiness Index", "#22c55e"), use_container_width=True)

    st.write("---")

    # 18. Recent Activities
    st.markdown("### 18. 📜 Recent Activities Log")
    for act in summary['recent_activities']:
        st.markdown(f"- 🕒 **[{act.get('created_at', 'Recent')}]** `{act.get('action')}`: {act.get('details')}")

if __name__ == "__main__":
    render_dashboard_page()
