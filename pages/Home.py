import streamlit as st

def render_home_page():
    st.markdown("""
    <div style="text-align: center; padding: 2.5rem 1rem;">
        <h1 style="font-size: 3rem; background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            ⚡ AI Resume Screening & Career Intelligence Platform
        </h1>
        <p style="font-size: 1.25rem; color: #94a3b8; max-width: 800px; margin: 0 auto 2rem auto;">
            Empowering professionals with AI-driven ATS score analysis, skill gap benchmarking, career predictions, job matching, course recommendations, and mock interview prep.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 ATS Compatibility", "Instant Scoring")
    with col2:
        st.metric("📊 Skill Gap Analysis", "Real-Time Matching")
    with col3:
        st.metric("🚀 Career Guidance", "AI Roadmap")
    with col4:
        st.metric("🎓 Learning Courses", "Personalized")

    st.write("---")
    st.markdown("### 🌟 Platform Core Modules")
    
    m1, m2, m3 = st.columns(3)
    with m1:
        st.info("### 📄 1. ATS Resume Analysis\nDeep structural parsing, text extraction, ATS compatibility score, strengths & weakness identification.")
        st.info("### 🔍 2. Skill Gap Analysis\nExtract skills from resume vs job description, identify missing keywords & calculate readiness score.")
        st.info("### 📈 3. Career Recommendation\nPredict high-growth career tracks tailored to your background, experience, and skills.")
    
    with m2:
        st.success("### 🎯 4. Job Matching\nUpload target Job Descriptions for semantic similarity matching and compatibility metrics.")
        st.success("### 📚 5. Course Recommendation\nTargeted course suggestions from Coursera/Udemy to close detected skill gaps.")
    
    with m3:
        st.warning("### 💡 6. Resume Improvement\nActionable formatting, bullet point optimization, keyword addition, and project recommendations.")
        st.warning("### 📊 7. Dashboard Analytics\nComprehensive charts, profile completion progress, salary predictions, and downloadable PDF reports.")

if __name__ == "__main__":
    render_home_page()
