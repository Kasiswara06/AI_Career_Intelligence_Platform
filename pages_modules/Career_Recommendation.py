import streamlit as st
from services.resume_service import get_user_active_resume
from services.recommendation_service import get_career_and_course_recommendations

def render_career_recommendation_page():
    st.header("🚀 Career Recommendation")
    st.caption("Analyze education, skills, experience, career prediction, career roadmap, industry demand & career growth.")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("🔒 Please log in to view Career Recommendations.")
        st.stop()

    active_resume = get_user_active_resume(user_id)

    skills = active_resume.get("skills", []) if active_resume else ["python", "sql", "machine learning"]
    exp_years = active_resume.get("experience_years", 0.0) if active_resume else 1.0

    res = get_career_and_course_recommendations(skills, experience_years=exp_years)
    careers = res.get("career_recommendations", [])

    st.subheader("Predicted Career Tracks")
    for car in careers:
        with st.expander(f"💼 {car['career_role']} - Match Score: {car['match_score']}%"):
            st.write(f"**Industry Demand:** {car['industry_demand']}")
            st.write(f"**Career Growth:** {car['career_growth']}")
            st.write(f"**Career Readiness:** {car['readiness_score']}/100")
            
            st.markdown("#### 🗺️ Recommended Career Roadmap")
            for step in car["roadmap"]:
                st.markdown(f"- {step}")

if __name__ == "__main__":
    render_career_recommendation_page()
