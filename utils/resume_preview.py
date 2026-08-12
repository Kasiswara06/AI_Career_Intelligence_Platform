import streamlit as st
from ai_models.resume_parser import parse_resume_complete

def render_resume_preview_panel(resume_data: dict):
    """
    Renders an interactive, scrollable preview panel displaying:
    - Resume Metadata & PDF Details
    - Extracted Plain Text Preview
    - AI Summary
    - Extracted Skills
    - Experience
    - Education
    - Projects
    - Certifications
    """
    file_path = resume_data.get("file_path", "")
    filename = resume_data.get("filename", "Resume.pdf")
    
    if "parsed" in resume_data:
        parsed = resume_data["parsed"]
    else:
        parsed = parse_resume_complete(file_path, fallback_name=filename.split('.')[0])

    st.markdown(f"## 👁️ Resume Preview: `{filename}`")
    st.caption("Detailed structural preview of parsed metadata, AI summary, and technical competencies.")

    # Overview Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.write(f"📄 **Version:** `v{resume_data.get('version', 1)}`")
    with m2:
        st.write(f"💾 **Size:** `{resume_data.get('file_size', '245.8 KB')}`")
    with m3:
        st.write(f"📊 **Resume Score:** `{resume_data.get('resume_score', 85)}%`")
    with m4:
        st.write(f"🎯 **ATS Score:** `{resume_data.get('ats_score', 88)}%`")

    st.write("---")

    # Structured Tabs for Preview Panel
    tab_text, tab_summary, tab_skills, tab_exp, tab_edu, tab_proj = st.tabs([
        "📜 Extracted Text",
        "📝 AI Summary",
        "⚙️ Skills",
        "💼 Experience",
        "🎓 Education",
        "🚀 Projects & Certs"
    ])

    with tab_text:
        raw_text = parsed.get("raw_text", resume_data.get("extracted_text", ""))
        st.text_area("Extracted Plain Text (Scrollable)", raw_text, height=350)

    with tab_summary:
        st.info(f"💡 **AI Generated Summary:**\n\n> {parsed.get('ai_resume_summary')}")

    with tab_skills:
        tech_cats = parsed.get("technical_skills", {})
        for cat, skills in tech_cats.items():
            st.markdown(f"**{cat}:**")
            st.markdown(" ".join([f"`{s}`" for s in skills]))
        st.markdown("**Soft Skills:** " + ", ".join(parsed.get("soft_skills", [])))
        st.markdown("**Languages Known:** " + ", ".join(parsed.get("languages_known", [])))

    with tab_exp:
        prof = parsed.get("professional_details", {})
        st.write(f"**Current Role:** {prof.get('current_role', 'AI Engineer')}")
        st.write(f"**Experience:** {prof.get('experience', '1.5 Years')}")
        st.write(f"**Companies:** {', '.join(prof.get('companies', ['Tech Corp']))}")

    with tab_edu:
        edu = parsed.get("education", {})
        st.write(f"**Degree:** {edu.get('degree', 'B.Tech')} ({edu.get('branch', 'CSE')})")
        st.write(f"**College:** {edu.get('college', 'Institute of Technology')}")
        st.write(f"**CGPA:** {edu.get('cgpa', 8.8)} / 10.0 | **Graduation Year:** {edu.get('graduation_year', 2025)}")

    with tab_proj:
        prof = parsed.get("professional_details", {})
        st.markdown("**Projects:**")
        for proj in prof.get("projects", []):
            st.write(f"- 🚀 {proj}")
        st.markdown("**Certifications:**")
        for cert in prof.get("certifications", []):
            st.write(f"- 🏆 {cert}")
