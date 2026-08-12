import streamlit as st
from ai_models.course_recommendation import recommend_courses

def render_course_recommendation_page():
    st.header("🎓 Course Recommendation (Module 5)")
    st.caption("Detect missing skills, recommend tailored courses, learning roadmap, platform, duration & direct course links.")

    skills_input = st.text_input("Enter Missing Skills to Target (comma-separated)", "Docker, AWS, React, Deep Learning")
    
    if st.button("Generate Course Recommendations", type="primary"):
        missing = [s.strip() for s in skills_input.split(",") if s.strip()]
        courses = recommend_courses(missing)

        st.subheader("📚 Recommended Courses")
        for crs in courses:
            with st.container():
                st.markdown(f"### [{crs['course_title']}]({crs['link']})")
                st.markdown(f"**Target Skill:** `{crs['target_skill']}` | **Platform:** `{crs['platform']}` | **Duration:** `{crs['duration']}`")
                st.write("---")

if __name__ == "__main__":
    render_course_recommendation_page()
