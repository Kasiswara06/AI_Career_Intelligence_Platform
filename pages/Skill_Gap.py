import streamlit as st
from ai_models.skill_gap import analyze_skill_gap
from services.resume_service import get_user_active_resume

def render_skill_gap_page():
    st.header("🔍 Skill Gap Analysis (Module 2)")
    st.caption("Compare your extracted resume skills against a target Job Description to identify detected, missing skills & readiness score.")

    user_id = st.session_state.get("user_id", 1)
    active_resume = get_user_active_resume(user_id)

    jd_text = st.text_area("Paste Target Job Description (JD)", height=180, placeholder="Target job requirements...")

    if st.button("Perform Skill Gap Analysis", type="primary", use_container_width=True):
        if not active_resume and not jd_text:
            st.warning("Please upload a resume or paste job description requirements.")
            return

        raw_text = active_resume.get("raw_text", "") if active_resume else ""
        results = analyze_skill_gap(raw_text, jd_text)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Skill Match Percentage", f"{results.get('skill_match_percentage', 0)}%")
        with col2:
            st.metric("Career Readiness Score", f"{results.get('career_readiness_score', 0)}/100")

        st.write("---")
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("✔️ Detected Matching Skills")
            for sk in results.get("matching_skills", []):
                st.success(sk)
        with c2:
            st.subheader("❌ Missing Required Skills")
            for sk in results.get("missing_skills", []):
                st.error(sk)

if __name__ == "__main__":
    render_skill_gap_page()
