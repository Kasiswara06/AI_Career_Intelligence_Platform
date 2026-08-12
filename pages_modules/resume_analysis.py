import streamlit as st
import datetime
import os
from pathlib import Path

from services.resume_service import get_user_active_resume, upload_user_resume
from services.analysis_service import run_comprehensive_resume_analysis
from ai_models.resume_parser import parse_resume_complete
from utils.charts import (
    create_resume_score_gauge,
    create_ats_gauge,
    create_skill_match_pie,
    create_missing_skills_chart,
    create_top_skills_chart,
    create_job_match_chart,
    create_salary_prediction_chart,
    create_career_recommendation_chart,
    create_learning_progress_chart
)

def render_resume_analysis_page():
    """Renders the comprehensive 12-section Professional AI Resume Analysis Module."""
    st.title("⚡ Professional AI Resume Analysis & Career Intelligence")
    st.caption("Commercial-grade ATS Resume Parser, NLP Entity Extraction, Semantic Job Matching, Salary Predictor & Improvement Engine.")

    user_id = st.session_state.get("user_id", 1)
    
    # Session state active analysis cache
    if "analysis_data" not in st.session_state:
        st.session_state["analysis_data"] = None

    # Fetch active resume from DB or default session
    active_resume = get_user_active_resume(user_id)

    # ----------------------------------------------------
    # SECTION 1 – RESUME UPLOAD & FILE DETAILS
    # ----------------------------------------------------
    st.markdown("### 📤 Section 1 – Resume Upload & Management")
    
    uploaded_file = st.file_uploader(
        "Upload Resume (Drag & Drop PDF, DOCX, or TXT)",
        type=["pdf", "docx", "doc", "txt"],
        help="Supports single or multi-page resumes up to 10MB."
    )

    if uploaded_file is not None:
        file_path, file_type = upload_user_resume(user_id, uploaded_file)
        if file_path:
            st.success("✔ Resume uploaded successfully!")
            parsed = parse_resume_complete(file_path, fallback_name=uploaded_file.name.split('.')[0])
            active_resume = {
                "id": 101,
                "filename": uploaded_file.name,
                "file_path": file_path,
                "file_size": f"{round(len(uploaded_file.getvalue()) / 1024, 1)} KB",
                "upload_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "raw_text": parsed["raw_text"],
                "parsed": parsed
            }
            # Trigger analysis refresh
            st.session_state["analysis_data"] = run_comprehensive_resume_analysis(active_resume, resume_id=active_resume.get("id", 1), user_id=user_id)

    if not active_resume and not st.session_state.get("analysis_data"):
        # Default mock sample for demonstration if no resume uploaded yet
        default_parsed = parse_resume_complete("", fallback_name="John Doe (Candidate)")
        active_resume = {
            "id": 1,
            "filename": "John_Doe_AI_Resume.pdf",
            "file_size": "245.8 KB",
            "upload_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "raw_text": default_parsed["raw_text"],
            "parsed": default_parsed
        }
        st.session_state["analysis_data"] = run_comprehensive_resume_analysis(active_resume, user_id=user_id)
    elif active_resume and not st.session_state.get("analysis_data"):
        st.session_state["analysis_data"] = run_comprehensive_resume_analysis(active_resume, user_id=user_id)

    analysis = st.session_state["analysis_data"]
    parsed_info = analysis["parsed_data"]

    # Section 1 File Metadata Details
    st.info("✔ Resume uploaded successfully")
    uc1, uc2, uc3 = st.columns(3)
    with uc1:
        st.write(f"📄 **Resume Name:** `{active_resume.get('filename', 'John_Doe_AI_Resume.pdf')}`")
    with uc2:
        st.write(f"💾 **File Size:** `{active_resume.get('file_size', '245.8 KB')}`")
    with uc3:
        st.write(f"⏰ **Upload Time:** `{active_resume.get('upload_time', 'Just Now')}`")

    with st.expander("👀 View Extracted Resume Raw Text Preview"):
        st.text_area("Extracted Resume Text", active_resume.get("raw_text", parsed_info.get("raw_text", "")), height=180)

    st.write("---")

    # ----------------------------------------------------
    # SECTION 11 – DASHBOARD KPI CARDS (Displayed at top for quick glance)
    # ----------------------------------------------------
    st.markdown("### 📊 Section 11 – Key Performance Indicator (KPI) Cards")
    
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.metric("Resume Uploaded", "Yes ✔️")
    with kpi2:
        st.metric("Resume Score", f"{analysis['ats_results']['resume_score']}/100")
    with kpi3:
        st.metric("ATS Score", f"{analysis['ats_results']['ats_score']}%")
    with kpi4:
        st.metric("Job Match %", f"{analysis['job_matches'][0]['match_pct']}%")
    with kpi5:
        st.metric("Career Readiness", f"{analysis['skill_gap']['career_readiness']}%")

    kpi6, kpi7, kpi8, kpi9 = st.columns(4)
    with kpi6:
        st.metric("Detected Skills", f"{len(analysis['skill_gap']['detected_skills'])} Skills")
    with kpi7:
        st.metric("Missing Skills", f"{len(analysis['skill_gap']['missing_skills'])} Skills")
    with kpi8:
        st.metric("Expected Salary", f"₹ {analysis['salary_data']['predicted_lpa']} LPA")
    with kpi9:
        st.metric("Recommended Jobs", f"{len(analysis['job_matches'])} Matching Roles")

    st.write("---")

    # ----------------------------------------------------
    # SECTION 2 – RESUME INFORMATION EXTRACTION
    # ----------------------------------------------------
    st.markdown("### 🔍 Section 2 – Resume Information Extraction")
    
    tab_personal, tab_edu, tab_prof, tab_tech, tab_soft, tab_lang = st.tabs([
        "👤 Personal Information",
        "🎓 Education",
        "💼 Professional Details",
        "⚙️ Technical Skills",
        "🤝 Soft Skills",
        "🌐 Languages Known"
    ])

    p_info = parsed_info.get("personal_info", {})
    with tab_personal:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Full Name:** {p_info.get('full_name', 'John Doe')}")
            st.markdown(f"**Email:** {p_info.get('email', 'john.doe@example.com')}")
            st.markdown(f"**Mobile Number:** {p_info.get('mobile', '+91 9876543210')}")
            st.markdown(f"**Date of Birth:** {p_info.get('dob', '15-08-2002')}")
        with c2:
            st.markdown(f"**Address:** {p_info.get('address', 'Bangalore, Karnataka, India')}")
            st.markdown(f"**LinkedIn:** [{p_info.get('linkedin')}]({p_info.get('linkedin')})")
            st.markdown(f"**GitHub:** [{p_info.get('github')}]({p_info.get('github')})")
            st.markdown(f"**Portfolio:** [{p_info.get('portfolio')}]({p_info.get('portfolio')})")

    edu = parsed_info.get("education", {})
    with tab_edu:
        e1, e2 = st.columns(2)
        with e1:
            st.markdown(f"**College / Institute:** {edu.get('college', 'Institute of Technology')}")
            st.markdown(f"**University:** {edu.get('university', 'State University')}")
            st.markdown(f"**Degree:** {edu.get('degree', 'B.Tech')}")
        with e2:
            st.markdown(f"**Branch / Field:** {edu.get('branch', 'Artificial Intelligence & Data Science')}")
            st.markdown(f"**CGPA / Percentage:** {edu.get('cgpa', 8.8)} / 10.0")
            st.markdown(f"**Graduation Year:** {edu.get('graduation_year', 2025)}")

    prof = parsed_info.get("professional_details", {})
    with tab_prof:
        st.markdown(f"**Current Role:** {prof.get('current_role', 'AI Engineer Intern')}")
        st.markdown(f"**Experience:** {prof.get('experience', '1.5 Years')}")
        st.markdown(f"**Companies:** {', '.join(prof.get('companies', ['Tech Solutions Inc.']))}")
        
        st.markdown("**Key Projects:**")
        for proj in prof.get('projects', []):
            st.write(f"- 🚀 {proj}")
            
        st.markdown("**Certifications:**")
        for cert in prof.get('certifications', []):
            st.write(f"- 🏆 {cert}")

    tech_cats = parsed_info.get("technical_skills", {})
    with tab_tech:
        for cat_name, skill_list in tech_cats.items():
            st.markdown(f"**{cat_name}:**")
            badges = " ".join([f"`{s}`" for s in skill_list])
            st.markdown(badges)

    with tab_soft:
        soft_list = parsed_info.get("soft_skills", ["Communication", "Leadership", "Teamwork", "Problem Solving", "Time Management"])
        st.markdown(" ".join([f"`{s}`" for s in soft_list]))

    with tab_lang:
        lang_list = parsed_info.get("languages_known", ["English", "Hindi"])
        st.write("🗣️ **Spoken Languages Identified:** " + ", ".join(lang_list))

    st.write("---")

    # ----------------------------------------------------
    # SECTION 3 – RESUME SUMMARY
    # ----------------------------------------------------
    st.markdown("### 📝 Section 3 – Resume Summary")
    st.info(f"💡 **AI Generated Candidate Summary:**\n\n> {parsed_info.get('ai_resume_summary')}")

    st.write("---")

    # ----------------------------------------------------
    # SECTION 4 – RESUME ANALYSIS & ATS SCORES
    # ----------------------------------------------------
    st.markdown("### 🎯 Section 4 – Resume & ATS Analysis")
    
    ats = analysis["ats_results"]
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("✔ Resume Score", f"{ats.get('resume_score')}/100")
    with m2:
        st.metric("✔ ATS Score", f"{ats.get('ats_score')}%")
    with m3:
        st.metric("✔ Resume Quality", f"{ats.get('resume_quality')}")
    with m4:
        st.metric("✔ Resume Completeness", f"{ats.get('completeness_pct')}%")

    q1, q2 = st.columns(2)
    with q1:
        st.metric("✔ Formatting Quality", f"{ats.get('formatting_quality', 85)}%")
    with q2:
        st.metric("✔ Summary Score", f"{ats.get('summary_score', 90)}/100")

    sc1, sc2 = st.columns(2)
    with sc1:
        st.subheader("💪 Resume Strengths")
        for strg in ats.get("strengths", []):
            st.success(f"✔ {strg}")

        st.subheader("🔑 Extracted Resume Keywords")
        kw_badges = " ".join([f"`{kw}`" for kw in ats.get("keywords_found", [])])
        st.markdown(kw_badges)

    with sc2:
        st.subheader("⚠️ Resume Weaknesses")
        for wkn in ats.get("weaknesses", []):
            st.warning(f"⚠️ {wkn}")

        if ats.get("missing_sections"):
            st.subheader("📌 Missing Sections")
            for ms in ats.get("missing_sections", []):
                st.error(f"❌ {ms}")

    st.write("---")

    # ----------------------------------------------------
    # SECTION 5 – SKILL GAP ANALYSIS
    # ----------------------------------------------------
    st.markdown("### 🧠 Section 5 – Skill Gap Analysis")
    
    sg = analysis["skill_gap"]
    g1, g2 = st.columns(2)
    with g1:
        st.metric("Skill Match %", f"{sg['skill_match_pct']}%")
    with g2:
        st.metric("Career Readiness Score", f"{sg['career_readiness']}%")

    sg_c1, sg_c2 = st.columns(2)
    with sg_c1:
        st.markdown("#### ✔ Detected Skills")
        for d_skill in sg["detected_skills"]:
            st.markdown(f"<span style='background-color:#065F46; color:#D1FAE5; padding:4px 12px; border-radius:16px; margin:4px; display:inline-block;'>✔ {d_skill}</span>", unsafe_allow_html=True)

    with sg_c2:
        st.markdown("#### ❌ Missing Skills")
        for m_skill in sg["missing_skills"]:
            st.markdown(f"<span style='background-color:#991B1B; color:#FEE2E2; padding:4px 12px; border-radius:16px; margin:4px; display:inline-block;'>❌ {m_skill}</span>", unsafe_allow_html=True)

    st.markdown("**Recommended Skills to Acquire:** " + ", ".join([f"`{s}`" for s in sg["recommended_skills"]]))

    st.write("---")

    # ----------------------------------------------------
    # SECTION 6 – JOB MATCHING
    # ----------------------------------------------------
    st.markdown("### 💼 Section 6 – Job Matching")
    
    for job in analysis["job_matches"]:
        with st.container():
            st.markdown(f"#### 🏢 {job['job_title']} – `{job['company']}` ({job['location']})")
            jc1, jc2, jc3 = st.columns(3)
            with jc1:
                st.metric("Match Percentage", f"{job['match_pct']}%")
            with jc2:
                st.metric("ATS Compatibility", f"{job['ats_compatibility']}%")
            with jc3:
                st.write("**Matching Skills:** " + ", ".join(job['matching_skills']))
                st.write("**Missing Skills:** " + ", ".join(job['missing_skills']))
            st.write("---")

    # ----------------------------------------------------
    # SECTION 7 – CAREER RECOMMENDATION
    # ----------------------------------------------------
    st.markdown("### 🚀 Section 7 – Career Recommendation")
    
    cr = analysis["career_rec"]
    st.success(f"🌟 **Best Career Fit:** {cr['best_career']}")
    st.write("**Alternative Careers:** " + ", ".join(cr['alternative_careers']))
    st.info(f"🗺️ **Career Roadmap:** {cr['career_roadmap']}")
    st.write(f"📈 **Industry Demand:** {cr['industry_demand']}")
    st.write(f"🔮 **Future Scope:** {cr['future_scope']}")

    st.write("---")

    # ----------------------------------------------------
    # SECTION 8 – COURSE RECOMMENDATION
    # ----------------------------------------------------
    st.markdown("### 📚 Section 8 – Course Recommendation")
    
    course_cols = st.columns(len(analysis["courses"]))
    for idx, c in enumerate(analysis["courses"]):
        with course_cols[idx]:
            st.markdown(f"#### 📖 {c['course']}")
            st.write(f"**Platform:** {c['platform']}")
            st.write(f"**Duration:** {c['duration']}")
            st.write(f"**Difficulty:** {c['difficulty']}")
            st.markdown(f"[🔗 Start Learning]({c['link']})")

    st.write("---")

    # ----------------------------------------------------
    # SECTION 9 – SALARY PREDICTION
    # ----------------------------------------------------
    st.markdown("### 💰 Section 9 – Salary Prediction")
    
    sal = analysis["salary_data"]
    exp_years = float(parsed_info.get("professional_details", {}).get("experience_years", 1.5))
    sal1, sal2, sal3, sal4 = st.columns(4)
    with sal1:
        st.metric("Expected Salary", f"₹ {sal['predicted_lpa']} LPA")
    with sal2:
        st.metric("Minimum Salary", f"₹ {sal['min_lpa']} LPA")
    with sal3:
        st.metric("Maximum Salary", f"₹ {sal['max_lpa']} LPA")
    with sal4:
        st.metric("Experience Level", sal['experience_level'])

    st.plotly_chart(create_salary_prediction_chart(exp_years, sal['predicted_lpa']), use_container_width=True)

    st.write("---")


    # ----------------------------------------------------
    # SECTION 10 – RESUME IMPROVEMENT SUGGESTIONS
    # ----------------------------------------------------
    st.markdown("### ✨ Section 10 – Resume Improvement Suggestions")
    
    imp = analysis["improvements"]
    
    imp_col1, imp_col2 = st.columns(2)
    with imp_col1:
        st.metric("Current ATS Score", f"{imp['current_ats_score']}%")
    with imp_col2:
        st.metric("Potential ATS Score", f"{imp['potential_ats_score']}%", delta=f"+{imp['potential_ats_score'] - imp['current_ats_score']}%")

    st.write("**Improve by:**")
    for item in imp["improvements_needed"]:
        st.write(f"- 📈 {item}")

    with st.expander("✨ AI Enhanced Professional Summary Rewrite"):
        st.write(imp["improved_summary"])

    with st.expander("🔑 Missing Keywords to Add"):
        st.markdown(" ".join([f"`{kw}`" for kw in imp["missing_keywords"]]))

    with st.expander("💡 ATS Optimization Tips"):
        for tip in imp["ats_optimization_tips"]:
            st.write(f"- {tip}")

    with st.expander("🚀 Project & Certification Suggestions"):
        st.markdown("**Project Improvements:**")
        for p_imp in imp["project_improvements"]:
            st.write(f"- **{p_imp['title']}:** {p_imp['improvement']}")
        st.markdown("**Recommended Certifications:**")
        for cert in imp["certification_suggestions"]:
            st.write(f"- 🏆 {cert}")

    with st.expander("🎨 Formatting, Grammar & Step-by-Step Action Plan"):
        st.markdown("**Formatting Advice:**")
        for fmt in imp["formatting_suggestions"]:
            st.write(f"- {fmt}")
        st.markdown("**Grammar Suggestions:**")
        for grm in imp["grammar_suggestions"]:
            st.write(f"- {grm}")
        st.markdown("**Step-by-Step Action Plan:**")
        for act in imp["action_plan"]:
            st.write(f"- {act}")

    st.write("---")

    # ----------------------------------------------------
    # SECTION 12 – INTERACTIVE CHARTS & ANALYTICS GRID
    # ----------------------------------------------------
    st.markdown("### 📊 Section 12 – Interactive Analytics & Visualization Dashboard")
    
    chart_tabs = st.tabs([
        "📊 Score Gauges",
        "🍩 Skill Ratios & Gaps",
        "💼 Job & Market Analytics",
        "📈 Salary & Learning Growth"
    ])

    with chart_tabs[0]:
        g_c1, g_c2 = st.columns(2)
        with g_c1:
            st.plotly_chart(create_resume_score_gauge(ats['resume_score']), use_container_width=True)
        with g_c2:
            st.plotly_chart(create_ats_gauge(ats['ats_score']), use_container_width=True)

    with chart_tabs[1]:
        sr_c1, sr_c2 = st.columns(2)
        with sr_c1:
            st.plotly_chart(create_skill_match_pie(len(sg['detected_skills']), len(sg['missing_skills'])), use_container_width=True)
        with sr_c2:
            st.plotly_chart(create_missing_skills_chart(sg['missing_skills']), use_container_width=True)

    with chart_tabs[2]:
        j_c1, j_c2 = st.columns(2)
        with j_c1:
            st.plotly_chart(create_top_skills_chart(sg['detected_skills']), use_container_width=True)
        with j_c2:
            st.plotly_chart(create_job_match_chart(analysis['job_matches']), use_container_width=True)

    with chart_tabs[3]:
        gr_c1, gr_c2 = st.columns(2)
        with gr_c1:
            st.plotly_chart(create_career_recommendation_chart(len(sg['detected_skills']), ats['ats_score']), use_container_width=True)
        with gr_c2:
            st.plotly_chart(create_learning_progress_chart(), use_container_width=True)

if __name__ == "__main__":
    render_resume_analysis_page()
