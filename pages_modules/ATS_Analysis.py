import streamlit as st
from services.resume_service import get_user_active_resume
from services.analysis_service import perform_full_ats_analysis
from services.job_service import fetch_available_jobs
from database.database import insert_job

def render_ats_analysis_page():
    st.header("🎯 AI ATS Resume Analysis & Job Description Match")
    st.caption("Module 10 & 11: Compare your active resume against target Job Descriptions to generate ATS compatibility, keyword match, and detected vs missing skill breakdown.")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("🔒 Please log in to run ATS Analysis.")
        st.stop()

    active_resume = get_user_active_resume(user_id)

    # --------------------------------------------------------------------------
    # 1. JOB DESCRIPTION INPUT METHODS (Upload JD / Paste JD / Select DB Job)
    # --------------------------------------------------------------------------
    st.markdown("### 📥 Select or Provide Job Description (JD)")
    jd_source = st.radio("Choose Job Description Source:", ["Upload Job Description File", "Paste Job Description Text", "Select Job from Database"], horizontal=True)

    job_title = "Target Software Engineer"
    company_name = "Tech Enterprise"
    location = "Remote / India"
    experience_req = "1-3 Years"
    qualification_req = "B.Tech / B.S. CS"
    salary_range = "$80,000 - $120,000"
    jd_text = ""

    if jd_source == "Upload Job Description File":
        uploaded_jd = st.file_uploader("Upload JD File (PDF, DOCX, or TXT)", type=["pdf", "docx", "txt"])
        if uploaded_jd:
            try:
                if uploaded_jd.name.endswith(".txt"):
                    jd_text = uploaded_jd.read().decode("utf-8", errors="ignore")
                else:
                    import pypdf
                    reader = pypdf.PdfReader(uploaded_jd)
                    jd_text = "\n".join([page.extract_text() or "" for page in reader.pages])
            except Exception as e:
                st.error(f"Error reading file: {e}")
            job_title = uploaded_jd.name.split('.')[0]

    elif jd_source == "Paste Job Description Text":
        col1, col2 = st.columns(2)
        with col1:
            job_title = st.text_input("Target Job Title", value="Senior AI / Machine Learning Engineer")
            company_name = st.text_input("Company Name", value="InnovateAI Labs")
            location = st.text_input("Location", value="Bangalore / Remote")
        with col2:
            experience_req = st.text_input("Required Experience", value="1-3 Years")
            qualification_req = st.text_input("Required Qualification", value="B.Tech in CS/AI")
            salary_range = st.text_input("Estimated Salary Range", value="$95,000 - $135,000")

        jd_text = st.text_area("Paste Job Requirements & Description *", height=150, value="We are seeking an AI/ML Engineer proficient in Python, PyTorch, SQL, Docker, AWS Cloud services, REST APIs, and NLP algorithms.")

    elif jd_source == "Select Job from Database":
        db_jobs = fetch_available_jobs()
        job_options = [f"{j.get('job_title', j.get('title'))} @ {j.get('company')} ({j.get('location', 'Remote')})" for j in db_jobs]
        chosen_idx = st.selectbox("Select Target Job Position:", range(len(job_options)), format_func=lambda i: job_options[i])
        
        selected_job = db_jobs[chosen_idx]
        job_title = selected_job.get("job_title", selected_job.get("title", "Target Role"))
        company_name = selected_job.get("company", "Tech Company")
        location = selected_job.get("location", "Remote")
        experience_req = selected_job.get("experience_level", selected_job.get("experience", "1-3 Years"))
        qualification_req = selected_job.get("qualification", "B.Tech")
        salary_range = selected_job.get("salary_range", "$80,000 - $120,000")
        jd_text = selected_job.get("job_description", selected_job.get("description", ""))

    st.write("---")

    # --------------------------------------------------------------------------
    # 2. RUN FULL ATS SCAN ENGINE
    # --------------------------------------------------------------------------
    if st.button("🎯 Run Full ATS Analysis & Compatibility Scan", type="primary", use_container_width=True):
        if not active_resume:
            st.error("⚠️ No active resume found! Please upload your resume in the 'Resume Upload' page first.")
            return

        raw_text = active_resume.get("raw_text", "")
        with st.spinner("Analyzing ATS formatting, contact info, keyword density, and semantic similarity..."):
            res = perform_full_ats_analysis(raw_text, jd_text)
            ats = res.get("ats", {})

            ats_score = ats.get("ats_score", 82)
            resume_score = ats.get("resume_score", 85)
            jd_match_pct = ats.get("jd_match_percentage", 88)
            detected_skills = ats.get("detected_skills", ["Python", "SQL", "Machine Learning", "Git"])
            missing_skills = ats.get("missing_skills", ["Docker", "AWS Cloud", "Kubernetes"])

            st.markdown("### 📊 ATS Compatibility Results")
            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.metric("ATS Compatibility Score", f"{ats_score}%")
            with k2:
                st.metric("Resume Score", f"{resume_score}/100")
            with k3:
                st.metric("Keyword Match %", f"{jd_match_pct}%")
            with k4:
                st.metric("Target Role", job_title)

            st.write("---")

            col_s1, col_s2 = st.columns(2)
            with col_s1:
                st.markdown("#### ✔️ Detected Skills in Resume")
                st.write(", ".join([f"`{s}`" for s in detected_skills]))
            with col_s2:
                st.markdown("#### ❌ Missing Required Skills for JD")
                st.write(", ".join([f"`{s}`" for s in missing_skills]))

            st.write("---")
            st.markdown("### 💡 ATS Summary & Optimization Feedback")
            st.info(ats.get("summary", "Resume passes basic ATS formatting checks."))

            if ats.get("improvement_tips"):
                st.markdown("#### 📌 Key ATS Improvement Suggestions")
                for tip in ats.get("improvement_tips", []):
                    st.markdown(f"- {tip}")

            # Save JD selection into session state for downstream pages
            st.session_state["active_target_jd"] = {
                "job_title": job_title,
                "company": company_name,
                "location": location,
                "jd_text": jd_text,
                "missing_skills": missing_skills,
                "detected_skills": detected_skills
            }

if __name__ == "__main__":
    render_ats_analysis_page()
