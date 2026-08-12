import streamlit as st
from ai_models.course_recommendation import recommend_courses
from services.resume_service import get_user_active_resume

def render_course_recommendation_page():
    st.header("📚 Course & Certification Recommendations")
    st.caption("Module 14: Recommend targeted learning tracks from Coursera, Udemy, NPTEL, Infosys Springboard & Google Cloud Boost based on detected skill gaps.")

    user_id = st.session_state.get("user_id", 1)
    active_resume = get_user_active_resume(user_id)
    target_jd = st.session_state.get("active_target_jd", {})

    detected_missing = target_jd.get("missing_skills", ["Docker", "Kubernetes", "AWS Cloud", "System Design"])
    
    st.markdown("### 🔍 Target Skill Gaps for Learning")
    missing_input = st.text_input(
        "Enter or Modify Missing Skills (Comma-separated)",
        value=", ".join(detected_missing) if detected_missing else "Docker, AWS Cloud, Kubernetes"
    )

    if st.button("🚀 Generate Course Recommendations", type="primary", use_container_width=True):
        missing_list = [s.strip() for s in missing_input.split(",") if s.strip()]
        if not missing_list:
            st.warning("Please specify at least one skill to target.")
            return

        with st.spinner("Searching online course databases..."):
            courses = recommend_courses(missing_list)

        st.markdown("### 🏆 Recommended Learning Courses & Certifications")
        if not courses:
            st.info("No courses found. Try entering standard engineering skills like Docker, AWS, SQL, PyTorch.")
            return

        c_cols = st.columns(2)
        for idx, crs in enumerate(courses):
            target_col = c_cols[idx % 2]
            with target_col:
                with st.container():
                    st.markdown(f"#### 📖 [{crs['course_title']}]({crs['link']})")
                    st.markdown(f"**Target Skill:** `{crs['target_skill']}`")
                    st.markdown(f"**Platform:** `{crs['platform']}` &nbsp;|&nbsp; **Duration:** `{crs['duration']}`")
                    st.markdown(f"[👉 Enroll / View Course]({crs['link']})")
                    st.write("---")

if __name__ == "__main__":
    render_course_recommendation_page()
