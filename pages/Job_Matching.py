import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from services.resume_service import get_user_active_resume, process_and_save_resume
from services.job_service import fetch_available_jobs, rank_candidate_against_jobs
from ai_models.job_matching import analyze_job_match_full

def create_gauge_chart(score: float, title: str, bar_color: str = "#38bdf8"):
    """Generates an interactive Plotly Gauge Indicator Chart."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': title, 'font': {'size': 18, 'color': '#ffffff'}},
        number={'suffix': "%", 'font': {'size': 28, 'color': '#ffffff'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
            'bar': {'color': bar_color},
            'bgcolor': "rgba(15, 23, 42, 0.6)",
            'bordercolor': "rgba(255, 255, 255, 0.1)",
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
        margin=dict(l=20, r=20, t=50, b=20),
        height=220
    )
    return fig

def render_job_matching_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🎯 AI Job Matching Module
        </h1>
        <p style="color: #94a3b8; font-size: 1.1rem;">
            Powered by <b>all-MiniLM-L6-v2</b>, <b>Sentence Transformers</b>, and <b>Cosine Similarity</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    user_id = st.session_state.get("user_id", 1)
    active_resume = get_user_active_resume(user_id)

    # Sidebar / Tab Selection for Resume & Job Inputs
    input_tab1, input_tab2 = st.tabs(["📄 Step 1: Candidate Resume", "💼 Step 2: Job Description Input"])

    with input_tab1:
        st.subheader("Candidate Resume Profile")
        if active_resume:
            st.success(f"✔️ Active Resume: **{active_resume.get('filename')}**")
            with st.expander("👁️ View Resume Information & Extracted Skills"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Email:** {active_resume.get('email', 'N/A')}")
                    st.write(f"**Phone:** {active_resume.get('phone', 'N/A')}")
                with c2:
                    st.write(f"**LinkedIn:** {active_resume.get('linkedin', 'N/A')}")
                    st.write(f"**Experience:** {active_resume.get('experience_years', 1.0)} Years")
                
                st.write("**Extracted Skills:**")
                skills = active_resume.get("skills", [])
                st.write(", ".join([f"`{s}`" for s in skills]) if skills else "No skills extracted.")
        
        uploaded_file = st.file_uploader("Upload New / Replace Resume (PDF or DOCX)", type=["pdf", "docx"])
        if uploaded_file:
            if st.button("Save & Use New Resume", type="secondary"):
                with st.spinner("Parsing resume text..."):
                    active_resume = process_and_save_resume(user_id, uploaded_file)
                    st.success("Resume updated!")
                    st.rerun()

    with input_tab2:
        st.subheader("Target Job Description")
        jd_option = st.radio("Choose Job Description Source:", ["Paste Job Description Text", "Select from Database Jobs", "Upload JD File (PDF/DOCX/TXT)"], horizontal=True)

        selected_jd_text = ""
        target_job_title = "Software Engineer"
        target_company = "Target Employer"

        if jd_option == "Paste Job Description Text":
            target_job_title = st.text_input("Job Title", "Senior AI / Machine Learning Engineer")
            target_company = st.text_input("Company", "Innovate AI Labs")
            selected_jd_text = st.text_area("Paste Job Requirements & Responsibilities", height=180, value="""We are seeking a Senior AI/ML Engineer proficient in Python, PyTorch, TensorFlow, SQL, Docker, AWS, and REST API microservices. Responsible for building, training, and deploying scalable deep learning models and predictive pipelines.""")
        
        elif jd_option == "Select from Database Jobs":
            db_jobs = fetch_available_jobs()
            job_titles = [f"{j.get('job_title', j.get('title', 'Job'))} @ {j.get('company', 'Company')}" for j[id_key] in [(j, i) for i, j in enumerate(db_jobs)] for id_key in ['id'] if id_key in j]
            # Simple title select
            job_titles = [f"{j.get('job_title', j.get('title'))} ({j.get('company')})" for j in db_jobs]
            chosen_idx = st.selectbox("Select Benchmark Job", range(len(job_titles)), format_func=lambda i: job_titles[i])
            chosen_job = db_jobs[chosen_idx]
            target_job_title = chosen_job.get("job_title", chosen_job.get("title", "Software Engineer"))
            target_company = chosen_job.get("company", "Tech Company")
            selected_jd_text = chosen_job.get("job_description", chosen_job.get("description", ""))
            st.info(f"**Job Title:** {target_job_title} | **Location:** {chosen_job.get('location', 'Remote')} | **Salary:** {chosen_job.get('salary_range', chosen_job.get('salary', 'N/A'))}")

        elif jd_option == "Upload JD File (PDF/DOCX/TXT)":
            jd_file = st.file_uploader("Upload Job Description File", type=["pdf", "docx", "txt"])
            if jd_file:
                selected_jd_text = jd_file.read().decode("utf-8", errors="ignore")
                st.success(f"Uploaded `{jd_file.name}` ({len(selected_jd_text)} characters extracted)")

    st.write("---")
    
    if st.button("🚀 Run AI Semantic Job Matching Engine", type="primary", use_container_width=True):
        if not active_resume and not selected_jd_text:
            st.error("Please provide candidate resume or job description input!")
            return

        resume_text = active_resume.get("raw_text", "") if active_resume else "Python Developer experienced in SQL, Machine Learning, and Data Science."
        skills_list = active_resume.get("skills", []) if active_resume else ["python", "sql", "machine learning"]
        exp_years = active_resume.get("experience_years", 1.5) if active_resume else 1.5

        with st.spinner("Generating SentenceTransformer embeddings (all-MiniLM-L6-v2) & calculating Cosine Similarity..."):
            match_res = analyze_job_match_full(
                resume_text=resume_text,
                job_description=selected_jd_text or "Software Engineer Python SQL",
                extracted_skills=skills_list,
                job_title=target_job_title,
                experience_years=exp_years
            )

        # ----------------------------------------------------------------------
        # METRIC SUMMARY DASHBOARD
        # ----------------------------------------------------------------------
        st.markdown("## 📊 Matching Results & Dashboard")
        
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Match Percentage", f"{match_res['match_percentage']}%")
        with m2:
            st.metric("ATS Compatibility", f"{match_res['ats_score']}%")
        with m3:
            st.metric("Resume Score", f"{match_res['resume_score']}/100")
        with m4:
            st.metric("Semantic Similarity", f"{match_res['semantic_match_pct']}%")

        m5, m6, m7, m8 = st.columns(4)
        with m5:
            st.metric("Matching Skills", len(match_res["matching_skills"]))
        with m6:
            st.metric("Missing Skills", len(match_res["missing_skills"]))
        with m7:
            sal_avg = match_res["salary_prediction"].get("predicted_avg_salary", 95000)
            st.metric("Expected Avg Salary", f"${sal_avg:,} / yr")
        with m8:
            st.metric("Career Readiness", f"{match_res['career_recommendation']['career_readiness']}/100")

        st.write("---")

        # ----------------------------------------------------------------------
        # VISUALIZATIONS SECTION
        # ----------------------------------------------------------------------
        st.markdown("### 📈 Visual Analytics & Score Gauges")
        col_g1, col_g2, col_g3 = st.columns(3)
        with col_g1:
            st.plotly_chart(create_gauge_chart(match_res['match_percentage'], "Overall Job Match", "#38bdf8"), use_container_width=True)
        with col_g2:
            st.plotly_chart(create_gauge_chart(match_res['ats_score'], "ATS Compatibility", "#818cf8"), use_container_width=True)
        with col_g3:
            st.plotly_chart(create_gauge_chart(match_res['semantic_match_pct'], "Semantic Embedding Match", "#c084fc"), use_container_width=True)

        v1, v2 = st.columns(2)
        with v1:
            st.markdown("#### 🥧 Skill Breakdown (Matching vs Missing)")
            pie_df = pd.DataFrame({
                "Status": ["Matching Skills", "Missing Skills"],
                "Count": [max(1, len(match_res["matching_skills"])), max(1, len(match_res["missing_skills"]))]
            })
            fig_pie = px.pie(pie_df, values="Count", names="Status", color="Status",
                             color_discrete_map={"Matching Skills": "#22c55e", "Missing Skills": "#ef4444"},
                             hole=0.4)
            fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'))
            st.plotly_chart(fig_pie, use_container_width=True)

        with v2:
            st.markdown("#### 💵 Salary Prediction Breakdown")
            sal = match_res["salary_prediction"]
            sal_df = pd.DataFrame({
                "Category": ["Minimum", "Average", "Maximum"],
                "Salary (USD)": [sal.get("predicted_min_salary", 70000), sal.get("predicted_avg_salary", 95000), sal.get("predicted_max_salary", 125000)]
            })
            fig_bar = px.bar(sal_df, x="Category", y="Salary (USD)", text_auto='.2s', color="Category",
                             color_discrete_sequence=["#38bdf8", "#818cf8", "#c084fc"])
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'), showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)

        st.write("---")

        # ----------------------------------------------------------------------
        # SKILLS TAGS SECTION
        # ----------------------------------------------------------------------
        st.markdown("### 🏷️ Skill Alignment & Gap Tags")
        
        st.markdown("#### ✔️ Matching Skills")
        match_tags = "".join([f'<span style="background: rgba(34, 197, 94, 0.2); color: #4ade80; padding: 6px 12px; border-radius: 8px; margin: 4px; display: inline-block; font-weight: 600;">{s.capitalize()}</span>' for s in match_res["matching_skills"]])
        st.markdown(match_tags if match_tags else "*(No exact skills matching found)*", unsafe_allow_html=True)
        st.write("")

        st.markdown("#### ❌ Missing Skills")
        missing_tags = "".join([f'<span style="background: rgba(239, 68, 68, 0.2); color: #f87171; padding: 6px 12px; border-radius: 8px; margin: 4px; display: inline-block; font-weight: 600;">{s.capitalize()}</span>' for s in match_res["missing_skills"]])
        st.markdown(missing_tags if missing_tags else "*(No missing skills detected!)*", unsafe_allow_html=True)
        st.write("")

        st.markdown("#### 💡 Additional Recommended Skills to Upskill")
        rec_tags = "".join([f'<span style="background: rgba(56, 189, 248, 0.2); color: #38bdf8; padding: 6px 12px; border-radius: 8px; margin: 4px; display: inline-block; font-weight: 600;">{s.capitalize()}</span>' for s in match_res["additional_recommended_skills"]])
        st.markdown(rec_tags, unsafe_allow_html=True)

        st.write("---")

        # ----------------------------------------------------------------------
        # AI RATIONALE & IMPROVEMENT RECOMMENDATIONS
        # ----------------------------------------------------------------------
        c_ai1, c_ai2 = st.columns(2)
        with c_ai1:
            st.subheader("🤖 Why this job matches your profile")
            st.info(match_res["why_job_matches"])

            st.subheader("🚀 Future Growth & Career Path")
            c_rec = match_res["career_recommendation"]
            st.write(f"**Target Role:** {c_rec['suitable_role']}")
            st.write(f"**Industry Demand:** {c_rec['industry_demand']}")
            st.write(f"**Future Growth Rate:** {c_rec['future_growth']}")

        with c_ai2:
            st.subheader("📌 Actionable Improvement Suggestions")
            for tip in match_res["improvement_suggestions"]:
                st.warning(f"💡 {tip}")

        st.write("---")

        # ----------------------------------------------------------------------
        # RECOMMENDED COURSES SECTION
        # ----------------------------------------------------------------------
        st.markdown("### 🎓 Recommended Courses for Missing Skills")
        for crs in match_res["recommended_courses"]:
            with st.container():
                st.markdown(f"#### [{crs['course_title']}]({crs['link']})")
                st.caption(f"**Target Skill:** `{crs['target_skill']}` | **Platform:** `{crs['platform']}` | **Duration:** `{crs['duration']}`")

if __name__ == "__main__":
    render_job_matching_page()
