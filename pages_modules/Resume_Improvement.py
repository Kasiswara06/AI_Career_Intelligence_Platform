import streamlit as st
from services.resume_service import get_user_active_resume
from ai_models.resume_improvement import generate_resume_improvements

def render_resume_improvement_page():
    st.header("✨ Resume Improvement Suggestions (Module 6)")
    st.caption("Improve resume summary, missing keywords, ATS optimization, project suggestions, certification suggestions & formatting tips.")

    user_id = st.session_state.get("user_id", 1)
    active_resume = get_user_active_resume(user_id)

    raw_text = active_resume.get("raw_text", "") if active_resume else ""
    detected_skills = active_resume.get("skills", ["python", "sql"]) if active_resume else ["python", "sql"]

    improvements = generate_resume_improvements(raw_text, detected_skills)

    st.subheader("✨ Enhanced Summary Recommendation")
    st.info(improvements["improved_summary"])

    st.write("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📌 ATS Optimization Tips")
        for tip in improvements["ats_optimization_tips"]:
            st.markdown(f"- {tip}")

    with c2:
        st.subheader("🎓 Suggested Certifications")
        for cert in improvements["certification_suggestions"]:
            st.markdown(f"- {cert}")

    st.write("---")
    st.subheader("🚀 Project Portfolio Suggestions")
    for proj in improvements["project_suggestions"]:
        st.markdown(f"**{proj['title']}** (`{proj['tech_stack']}`)\n- {proj['description']}")

if __name__ == "__main__":
    render_resume_improvement_page()
