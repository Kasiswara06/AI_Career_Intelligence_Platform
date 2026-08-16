import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from services.resume_service import get_user_active_resume, process_and_save_resume
from services.job_service import fetch_available_jobs
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
            💼 AI Job Matching Module
        </h1>
        <p style="color: #94a3b8; font-size: 1.1rem;">
            Powered by <b>all-MiniLM-L6-v2</b>, <b>Sentence Transformers</b>, and <b>Cosine Similarity</b>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("🔒 Please log in to access Job Matching.")
        st.stop()

    active_resume = get_user_active_resume(user_id)

    input_tab1, input_tab2 = st.tabs(["📄 Candidate Resume", "💼 Job Description Input"])

    with input_tab1:
        st.subheader("Candidate Resume Profile")
        if active_resume:
            st.success(f"✔️ Active Resume: **{active_resume.get('filename')}**")
            with st.expander("👁️ View Extracted Skills"):
                skills = active_resume.get("skills", [])
                st.write(", ".join([f"`{s}`" for s in skills]) if skills else "No skills extracted.")
        
        uploaded_file = st.file_uploader("Upload New Resume (PDF / DOCX)", type=["pdf", "docx"])
        if uploaded_file:
            if st.button("Save & Use New Resume"):
                with st.spinner("Parsing resume text..."):
                    active_resume = process_and_save_resume(user_id, uploaded_file)
                    st.success("Resume updated!")
                    st.rerun()

    with input_tab2:
        st.subheader("Target Job Description")
        jd_option = st.radio("Choose Job Description Source:", ["Paste Job Description Text", "Select from Database Jobs", "Upload JD File"], horizontal=True)

        selected_jd_text = ""
        target_job_title = "Software Engineer"

        if jd_option == "Paste Job Description Text":
            target_job_title = st.text_input("Job Title", "Senior AI / Machine Learning Engineer")
            selected_jd_text = st.text_area("Paste Job Requirements", height=180, value="We are seeking a Senior AI/ML Engineer proficient in Python, PyTorch, TensorFlow, SQL, Docker, AWS, and REST API microservices.")
        elif jd_option == "Select from Database Jobs":
            db_jobs = fetch_available_jobs()
            job_titles = [f"{j.get('job_title', j.get('title'))} ({j.get('company')})" for j in db_jobs]
            chosen_idx = st.selectbox("Select Benchmark Job", range(len(job_titles)), format_func=lambda i: job_titles[i])
            chosen_job = db_jobs[chosen_idx]
            target_job_title = chosen_job.get("job_title", chosen_job.get("title", "Software Engineer"))
            selected_jd_text = chosen_job.get("job_description", chosen_job.get("description", ""))
        elif jd_option == "Upload JD File":
            jd_file = st.file_uploader("Upload Job Description File", type=["pdf", "docx", "txt"])
            if jd_file:
                selected_jd_text = jd_file.read().decode("utf-8", errors="ignore")

    st.write("---")
    
    if st.button("🚀 Run AI Semantic Job Matching Engine", type="primary", use_container_width=True):
        resume_text = active_resume.get("raw_text", "") if active_resume else "Python Developer experienced in SQL, Machine Learning, and Data Science."
        skills_list = active_resume.get("skills", []) if active_resume else ["python", "sql", "machine learning"]

        with st.spinner("Generating SentenceTransformer embeddings (all-MiniLM-L6-v2) & calculating Cosine Similarity..."):
            match_res = analyze_job_match_full(
                resume_text=resume_text,
                job_description=selected_jd_text or "Software Engineer Python SQL",
                extracted_skills=skills_list,
                job_title=target_job_title,
                experience_years=1.5
            )

        st.markdown("## 📊 Matching Results")
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Match Percentage", f"{match_res['match_percentage']}%")
        with m2:
            st.metric("ATS Compatibility", f"{match_res['ats_score']}%")
        with m3:
            st.metric("Resume Score", f"{match_res['resume_score']}/100")
        with m4:
            st.metric("Semantic Similarity", f"{match_res['semantic_match_pct']}%")

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.plotly_chart(create_gauge_chart(match_res['match_percentage'], "Overall Job Match", "#38bdf8"), use_container_width=True)
        with col_g2:
            st.plotly_chart(create_gauge_chart(match_res['ats_score'], "ATS Compatibility", "#818cf8"), use_container_width=True)

        st.write("---")
        st.markdown("### 🏷️ Skill Breakdown")
        st.markdown("#### ✔️ Matching Skills")
        st.write(", ".join(match_res["matching_skills"]))
        st.markdown("#### ❌ Missing Skills")
        st.write(", ".join(match_res["missing_skills"]))

if __name__ == "__main__":
    render_job_matching_page()
