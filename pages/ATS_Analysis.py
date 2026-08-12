import streamlit as st
from services.resume_service import get_user_active_resume
from services.analysis_service import perform_full_ats_analysis

def render_ats_analysis_page():
    st.header("🎯 ATS Resume Analysis (Module 1)")
    st.caption("Resume Upload vs Job Description Comparison, ATS Score, Resume Score, Match %, Strengths & Weaknesses.")

    user_id = st.session_state.get("user_id", 1)
    active_resume = get_user_active_resume(user_id)
    
    jd_input = st.text_area("Paste Target Job Description (Optional for JD-based ATS comparison)", height=150)

    if st.button("Run Full ATS Scan", type="primary", use_container_width=True):
        if not active_resume:
            st.error("No active resume found! Upload a resume in 'Resume Upload' first.")
            return

        raw_text = active_resume.get("raw_text", "")
        with st.spinner("Analyzing ATS formatting, contact info, structure, and keyword density..."):
            res = perform_full_ats_analysis(raw_text, jd_input)
            ats = res["ats"]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("ATS Score", f"{ats.get('ats_score', 0)}%")
            with col2:
                st.metric("Resume Quality Score", f"{ats.get('resume_score', 0)}/100")
            with col3:
                st.metric("JD Match Percentage", f"{ats.get('jd_match_percentage', 0)}%")

            st.write("---")
            st.subheader("Summary & Feedback")
            st.info(ats.get("summary", "Resume scan completed."))

            st.markdown("#### Detected Skills")
            st.write(", ".join(ats.get("detected_skills", [])))

if __name__ == "__main__":
    render_ats_analysis_page()
