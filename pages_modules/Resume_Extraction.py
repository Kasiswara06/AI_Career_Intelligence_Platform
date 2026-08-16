import streamlit as st
from services.resume_service import get_user_active_resume
from ai_models.resume_parser import parse_resume_complete

def render_resume_extraction_page():
    st.header("📑 Resume Information Extraction")
    st.caption("Deep entity extraction detailing personal info, education, technical/soft skills, experience, and projects.")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("🔒 Please log in to view Resume Extraction.")
        st.stop()

    active_resume = get_user_active_resume(user_id)

    if not active_resume:
        st.warning("No active resume uploaded! Visit 'Resume Upload' first.")
        return

    file_path = active_resume.get("file_path", "")
    with st.spinner("Extracting structured metadata..."):
        parsed = parse_resume_complete(file_path) if file_path else {}

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("👤 Personal & Contact Info")
        p_info = parsed.get("personal_info", {})
        st.write(f"**Full Name:** {p_info.get('full_name', 'Candidate')}")
        st.write(f"**Email:** {p_info.get('email', 'N/A')}")
        st.write(f"**Phone:** {p_info.get('phone', 'N/A')}")
        st.write(f"**Location:** {p_info.get('address', 'Bangalore, India')}")
        st.write(f"**LinkedIn:** [{p_info.get('linkedin', '#')}]({p_info.get('linkedin', '#')})")
        st.write(f"**GitHub:** [{p_info.get('github', '#')}]({p_info.get('github', '#')})")

    with c2:
        st.subheader("🎓 Educational Details")
        edu = parsed.get("education", {})
        st.write(f"**Degree:** {edu.get('degree', 'B.Tech')}")
        st.write(f"**Branch:** {edu.get('branch', 'Computer Science')}")
        st.write(f"**College:** {edu.get('college', 'Institute of Technology')}")
        st.write(f"**CGPA:** {edu.get('cgpa', 8.5)}")
        st.write(f"**Graduation Year:** {edu.get('graduation_year', 2024)}")

    st.write("---")

    st.subheader("🛠️ Technical & Soft Skills")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown("#### Technical Skills")
        tech = parsed.get("technical_skills", {})
        for cat, list_s in tech.items():
            st.write(f"**{cat}:** {', '.join(list_s)}")
    with col_s2:
        st.markdown("#### Soft Skills & Languages")
        st.write(f"**Soft Skills:** {', '.join(parsed.get('soft_skills', []))}")
        st.write(f"**Languages Known:** {', '.join(parsed.get('languages_known', []))}")

    st.write("---")

    st.subheader("💼 Experience & Projects")
    prof = parsed.get("professional_details", {})
    st.write(f"**Total Experience:** {prof.get('experience_years', 1.5)} Years")
    st.write(f"**Current Role:** {prof.get('current_role', 'Developer')} @ {prof.get('current_company', 'Tech Enterprise')}")

    st.markdown("#### Project Portfolio")
    for proj in parsed.get("projects", []):
        st.markdown(f"**{proj['name']}** (`{proj['tech_used']}`)\n- {proj['description']}")

    st.write("---")
    st.subheader("✨ AI Generated Resume Summary")
    st.info(parsed.get("ai_resume_summary", "Experienced software engineering candidate."))

if __name__ == "__main__":
    render_resume_extraction_page()
