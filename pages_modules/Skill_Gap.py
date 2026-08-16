import streamlit as st
from ai_models.skill_gap import analyze_skill_gap
from services.resume_service import get_user_active_resume
from services.job_service import fetch_available_jobs

def render_skill_gap_page():
    st.header("🧠 AI Skill Gap Analysis Engine")
    st.caption("Module 11: Compare your active resume skills against target Job Description requirements to identify detected vs missing skills & readiness score.")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("🔒 Please log in to view Skill Gap Analysis.")
        st.stop()

    active_resume = get_user_active_resume(user_id)
    target_jd = st.session_state.get("active_target_jd", {})

    default_jd = target_jd.get("jd_text", "We are seeking a Senior AI/ML Engineer proficient in Python, PyTorch, SQL, Docker, AWS, Kubernetes, REST APIs, and System Design.")
    
    st.markdown("### 🎯 Target Job Description Context")
    jd_input_option = st.radio("Choose Input Method:", ["Use Active Job Description", "Paste Custom Job Requirements", "Select Job from Database"], horizontal=True)

    selected_jd_text = default_jd

    if jd_input_option == "Paste Custom Job Requirements":
        selected_jd_text = st.text_area("Paste Target Job Requirements (JD)", height=150, value=default_jd)
    elif jd_input_option == "Select Job from Database":
        db_jobs = fetch_available_jobs()
        job_titles = [f"{j.get('job_title', j.get('title'))} ({j.get('company')})" for j in db_jobs]
        chosen_idx = st.selectbox("Select Benchmark Job", range(len(job_titles)), format_func=lambda i: job_titles[i])
        selected_jd_text = db_jobs[chosen_idx].get("job_description", db_jobs[chosen_idx].get("description", ""))

    st.write("---")

    if st.button("🚀 Perform Skill Gap Analysis", type="primary", use_container_width=True):
        if not active_resume and not selected_jd_text:
            st.warning("Please upload a resume or provide job description requirements.")
            return

        raw_text = active_resume.get("raw_text", "") if active_resume else ""
        results = analyze_skill_gap(raw_text, selected_jd_text)

        match_pct = results.get("skill_match_percentage", 75.0)
        gap_pct = round(100.0 - match_pct, 1)
        readiness = results.get("career_readiness_score", 82)

        st.markdown("### 📊 Skill Match & Gap Indicators")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Skill Match %", f"{match_pct}%")
        with c2:
            st.metric("Skill Gap %", f"{gap_pct}%")
        with c3:
            st.metric("Career Readiness Score", f"{readiness}/100")

        st.write("---")
        col_det, col_mis = st.columns(2)
        with col_det:
            st.subheader("✔️ Detected Skills (In Resume)")
            for sk in results.get("matching_skills", ["Python", "SQL", "Machine Learning", "Git"]):
                st.success(f"✔️ {sk}")
        with col_mis:
            st.subheader("❌ Missing Skills (Required by Job)")
            for sk in results.get("missing_skills", ["Docker", "Kubernetes", "AWS Cloud"]):
                st.error(f"❌ {sk}")

        if results.get("additional_recommended_skills"):
            st.write("---")
            st.markdown("### 💡 Recommended Skills to Learn")
            st.write(", ".join([f"`{s}`" for s in results.get("additional_recommended_skills")]))

if __name__ == "__main__":
    render_skill_gap_page()
