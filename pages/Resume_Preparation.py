import os
import streamlit as st
from services.profile_service import get_full_user_profile
from ai_models.resume_builder import convert_profile_to_resume_dict
from ai_models.resume_summary_generator import generate_ai_professional_summary
from ai_models.ats_optimizer import evaluate_resume_ats_scores
from ai_models.resume_optimizer import ai_rewrite_resume_text
from resume_builder.template_manager import render_resume_html_template, TEMPLATES
from resume_builder.resume_formatter import format_resume_as_plain_text
from services.resume_builder_service import (
    generate_resume_from_profile,
    get_user_saved_resumes,
    delete_user_resume_version
)
from services.resume_version_service import set_active_resume_version
from utils.resume_export import export_resume_all_formats, get_copyable_resume_text

# Target Job Roles list (Section 3 requirement)
TARGET_ROLE_OPTIONS = [
    "Python Developer",
    "Data Analyst",
    "Data Scientist",
    "Machine Learning Engineer",
    "AI Engineer",
    "NLP Engineer",
    "Software Engineer",
    "Full Stack Developer",
    "Backend Developer",
    "Data Engineer",
    "Cloud Engineer",
    "DevOps Engineer",
    "Other / Custom Job Role"
]

DEFAULT_SECTION_ORDER = [
    "summary",
    "skills",
    "education",
    "experience",
    "projects",
    "certifications",
    "achievements"
]

SECTION_LABELS = {
    "summary": "Professional Summary",
    "skills": "Technical Skills",
    "education": "Education",
    "experience": "Professional Experience & Internships",
    "projects": "Key Projects",
    "certifications": "Certifications",
    "achievements": "Achievements"
}

def render_resume_preparation_page():
    user_id = st.session_state.get("user_id", 1)

    # Main Header
    st.markdown('<h1 class="gradient-text">📄 AI Resume Preparation & Resume Builder</h1>', unsafe_allow_html=True)
    st.caption("Automatically prepares a professional, ATS-friendly resume using your verified Profile data without duplicate data entry.")

    # 1. Visual Workflow Stepper (Section 2 requirement)
    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 12px; padding: 12px 18px; margin-bottom: 20px; font-size: 0.82rem; color: #94A3B8;">
        <div style="font-weight: 700; color: #60A5FA; margin-bottom: 6px;">🔄 Profile-Driven Resume Preparation Workflow</div>
        <div style="display: flex; flex-wrap: wrap; gap: 6px; align-items: center; justify-content: space-between;">
            <span style="background: rgba(59, 130, 246, 0.2); color: #93C5FD; padding: 3px 8px; border-radius: 6px;">1. Login</span> ➔
            <span style="background: rgba(59, 130, 246, 0.2); color: #93C5FD; padding: 3px 8px; border-radius: 6px;">2. Load Profile</span> ➔
            <span style="background: rgba(59, 130, 246, 0.2); color: #93C5FD; padding: 3px 8px; border-radius: 6px;">3. Load Education</span> ➔
            <span style="background: rgba(59, 130, 246, 0.2); color: #93C5FD; padding: 3px 8px; border-radius: 6px;">4. Load Skills</span> ➔
            <span style="background: rgba(59, 130, 246, 0.2); color: #93C5FD; padding: 3px 8px; border-radius: 6px;">5. Load Experience</span> ➔
            <span style="background: rgba(59, 130, 246, 0.2); color: #93C5FD; padding: 3px 8px; border-radius: 6px;">6. Load Projects</span> ➔
            <span style="background: rgba(59, 130, 246, 0.2); color: #93C5FD; padding: 3px 8px; border-radius: 6px;">7. AI Generation</span> ➔
            <span style="background: rgba(16, 185, 129, 0.2); color: #34D399; padding: 3px 8px; border-radius: 6px; font-weight: 600;">8. ATS Optimization</span> ➔
            <span style="background: rgba(16, 185, 129, 0.2); color: #34D399; padding: 3px 8px; border-radius: 6px; font-weight: 600;">9. Live Preview & Download</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Fetch User Profile (Section 1 requirement)
    profile = get_full_user_profile(user_id)

    # Candidate Status Card
    tech_skills_count = len(profile.get("technical_skills", []))
    degree_info = f"{profile.get('degree', 'Degree')} ({profile.get('specialization', 'Branch')})"
    st.markdown(f"""
    <div style="background: rgba(30, 41, 59, 0.9); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px; padding: 16px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="font-weight: 700; color: #F8FAFC; font-size: 1.1rem;">👤 Candidate: {profile.get('full_name')}</span>
                <div style="color: #94A3B8; font-size: 0.88rem; margin-top: 3px;">
                    📧 {profile.get('email')} &nbsp;|&nbsp; 📱 {profile.get('phone') or 'N/A'} &nbsp;|&nbsp; 🎓 {degree_info} &nbsp;|&nbsp; 🛠 {tech_skills_count} Skills Detected
                </div>
            </div>
            <div>
                <span style="background: rgba(16, 185, 129, 0.2); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.4); padding: 5px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
                    ✓ Primary Profile Auto-Synced
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Session State Initialization
    if "current_resume_dict" not in st.session_state:
        st.session_state["current_resume_dict"] = convert_profile_to_resume_dict(user_id, target_role="AI Engineer")
        st.session_state["current_target_role"] = "AI Engineer"
        st.session_state["current_template"] = "Modern ATS"
        st.session_state["current_jd"] = ""
        st.session_state["section_order"] = list(DEFAULT_SECTION_ORDER)
        st.session_state["custom_sections"] = {}

    res_dict = st.session_state["current_resume_dict"]

    # Navigation Tabs
    tab_preview, tab_edit, tab_rewrite, tab_ats, tab_versions = st.tabs([
        "📄 Generate & Preview Resume",
        "✏️ Edit & Manage Sections",
        "✨ AI Text Rewrite",
        "📊 ATS Score & Keyword Analysis",
        "📜 Saved Resume Versions"
    ])

    # ==========================================================================
    # TAB 1: GENERATE & PREVIEW RESUME
    # ==========================================================================
    with tab_preview:
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            role_sel = st.selectbox("🎯 Target Job Role", TARGET_ROLE_OPTIONS, index=4, key="prep_role_sel")
            if role_sel == "Other / Custom Job Role":
                target_role = st.text_input("Enter Custom Target Job Role", value="Lead Engineer", key="prep_role_custom")
            else:
                target_role = role_sel

        with col_r2:
            template_name = st.selectbox("🎨 Select ATS Resume Template", TEMPLATES, index=0, key="prep_tpl_sel")

        jd_text = st.text_area(
            "Target Job Description (Optional for Keyword Analysis & ATS Tuning)",
            placeholder="Paste target job description to match exact keywords and missing skill recommendations...",
            height=90,
            key="prep_jd_input"
        )

        col_b1, col_b2 = st.columns(2)
        with col_b1:
            if st.button("🚀 Generate AI Resume", type="primary", use_container_width=True):
                with st.spinner(f"Generating ATS-optimized resume for '{target_role}' using your profile data..."):
                    gen_res = generate_resume_from_profile(
                        user_id=user_id,
                        target_role=target_role,
                        template_name=template_name,
                        job_description=jd_text,
                        use_ai_summary=True
                    )
                    st.session_state["current_resume_dict"] = gen_res["resume_dict"]
                    st.session_state["current_target_role"] = target_role
                    st.session_state["current_template"] = template_name
                    st.session_state["current_jd"] = jd_text
                    st.toast("Generated fresh ATS resume from profile data successfully!")
                    st.rerun()

        with col_b2:
            if st.button("🔄 Sync Directly From Profile", use_container_width=True):
                st.session_state["current_resume_dict"] = convert_profile_to_resume_dict(user_id, target_role=target_role)
                st.toast("Re-synced resume data directly from your latest Profile!")
                st.rerun()

        st.write("---")
        st.subheader("👀 Live Resume Preview")
        st.caption(f"Template: **{st.session_state.get('current_template', 'Modern ATS')}** | Target Role: **{st.session_state.get('current_target_role', 'AI Engineer')}**")

        # HTML Live Preview (Section 13 requirement)
        html_preview = render_resume_html_template(
            st.session_state["current_resume_dict"],
            template_name=st.session_state.get("current_template", "Modern ATS")
        )
        st.components.v1.html(html_preview, height=620, scrolling=True)

        st.write("---")
        st.subheader("⬇ Download Resume Formats (Section 16 requirement)")

        exports = export_resume_all_formats(user_id, 1, st.session_state["current_resume_dict"])

        col_d1, col_d2, col_d3 = st.columns(3)
        with col_d1:
            if os.path.exists(exports["pdf_path"]):
                with open(exports["pdf_path"], "rb") as f:
                    st.download_button(
                        "📄 Download PDF",
                        data=f.read(),
                        file_name=f"{profile.get('full_name', 'Resume').replace(' ', '_')}_Resume.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

        with col_d2:
            if os.path.exists(exports["docx_path"]):
                with open(exports["docx_path"], "rb") as f:
                    st.download_button(
                        "📝 Download DOCX",
                        data=f.read(),
                        file_name=f"{profile.get('full_name', 'Resume').replace(' ', '_')}_Resume.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )

        with col_d3:
            plain_txt_copy = get_copyable_resume_text(st.session_state["current_resume_dict"])
            st.download_button(
                "📋 Download Plain Text",
                data=plain_txt_copy,
                file_name=f"{profile.get('full_name', 'Resume').replace(' ', '_')}_Resume.txt",
                mime="text/plain",
                use_container_width=True
            )

        with st.expander("📋 Click to View / Copy Raw Resume Text"):
            st.code(plain_txt_copy, language="markdown")

    # ==========================================================================
    # TAB 2: EDIT & MANAGE SECTIONS (Section 14 requirement)
    # ==========================================================================
    with tab_edit:
        st.subheader("✏️ Edit Resume Content & Manage Sections")
        st.caption("Modify any section content, add custom sections, or reorder sections before generating the final resume.")

        curr_dict = st.session_state["current_resume_dict"]

        with st.form("edit_resume_form"):
            st.markdown("#### Header Contact Information")
            e_name = st.text_input("Full Name", value=curr_dict.get("full_name", ""))
            e_email = st.text_input("Email Address", value=curr_dict.get("email", ""))
            e_phone = st.text_input("Phone Number", value=curr_dict.get("phone", ""))
            e_loc = st.text_input("Location / Address", value=curr_dict.get("location", ""))
            e_linkedin = st.text_input("LinkedIn Link", value=curr_dict.get("linkedin", ""))
            e_github = st.text_input("GitHub Link", value=curr_dict.get("github", ""))
            e_portfolio = st.text_input("Portfolio Link", value=curr_dict.get("portfolio", ""))

            st.write("---")
            st.markdown("#### Main Resume Sections")
            e_summary = st.text_area("Professional Summary", value=curr_dict.get("summary", ""), height=100)
            e_skills = st.text_area("Technical Skills", value=curr_dict.get("skills", ""), height=110)
            e_education = st.text_area("Education", value=curr_dict.get("education", ""), height=90)
            e_experience = st.text_area("Professional Experience / Internships", value=curr_dict.get("experience", ""), height=120)
            e_projects = st.text_area("Key Projects", value=curr_dict.get("projects", ""), height=110)
            e_certifications = st.text_area("Certifications", value=curr_dict.get("certifications", ""), height=80)
            e_achievements = st.text_area("Achievements", value=curr_dict.get("achievements", ""), height=80)

            btn_save_edits = st.form_submit_button("💾 Save All Edits", type="primary")
            if btn_save_edits:
                curr_dict["full_name"] = e_name
                curr_dict["email"] = e_email
                curr_dict["phone"] = e_phone
                curr_dict["location"] = e_loc
                curr_dict["linkedin"] = e_linkedin
                curr_dict["github"] = e_github
                curr_dict["portfolio"] = e_portfolio
                curr_dict["summary"] = e_summary
                curr_dict["skills"] = e_skills
                curr_dict["education"] = e_education
                curr_dict["experience"] = e_experience
                curr_dict["projects"] = e_projects
                curr_dict["certifications"] = e_certifications
                curr_dict["achievements"] = e_achievements

                st.session_state["current_resume_dict"] = curr_dict
                st.toast("Updated resume section edits successfully!")
                st.rerun()

        st.write("---")
        st.subheader("↕️ Section Actions & Order")

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("##### ➕ Add Custom Section")
            c_sec_name = st.text_input("New Section Name", placeholder="e.g., Languages, Volunteer Work")
            c_sec_content = st.text_area("New Section Content", placeholder="Enter section content...", height=80)
            if st.button("➕ Add Section"):
                if c_sec_name.strip() and c_sec_content.strip():
                    curr_dict[c_sec_name.lower().replace(" ", "_")] = c_sec_content
                    st.session_state["current_resume_dict"] = curr_dict
                    st.toast(f"Added custom section '{c_sec_name}'!")
                    st.rerun()
                else:
                    st.warning("Please enter both section title and content.")

        with col_m2:
            st.markdown("##### 🗑️ Remove Section")
            sec_to_remove = st.selectbox("Select Section to Remove", ["summary", "skills", "education", "experience", "projects", "certifications", "achievements"])
            if st.button("🗑️ Remove Selected Section"):
                curr_dict[sec_to_remove] = ""
                st.session_state["current_resume_dict"] = curr_dict
                st.toast(f"Cleared content of '{sec_to_remove}' section!")
                st.rerun()

    # ==========================================================================
    # TAB 3: AI TEXT REWRITE (Section 15 requirement)
    # ==========================================================================
    with tab_rewrite:
        st.subheader("✨ AI Text & Sentence Rewriter")
        st.caption("Select any section or text snippet and request AI enhancement while preserving 100% factual accuracy.")

        current = st.session_state["current_resume_dict"]

        rw_sec = st.selectbox(
            "Select Section to Rewrite",
            ["Professional Summary", "Technical Skills", "Education", "Professional Experience", "Key Projects", "Certifications", "Achievements"]
        )

        sec_map = {
            "Professional Summary": "summary",
            "Technical Skills": "skills",
            "Education": "education",
            "Professional Experience": "experience",
            "Key Projects": "projects",
            "Certifications": "certifications",
            "Achievements": "achievements"
        }
        target_key = sec_map[rw_sec]
        orig_text = current.get(target_key, "")

        input_text_to_rewrite = st.text_area("Target Text for AI Rewrite", value=orig_text, height=120)

        rewrite_mode = st.selectbox(
            "Choose AI Rewrite Prompt Goal",
            [
                "Make it ATS-friendly",
                "Improve sentence/section",
                "Make it more professional",
                "Make it concise",
                "Add strong action verbs"
            ]
        )

        if st.button("✨ Apply AI Rewrite", type="primary", use_container_width=True):
            if input_text_to_rewrite.strip():
                with st.spinner(f"Rewriting text using mode: '{rewrite_mode}'..."):
                    improved_res = ai_rewrite_resume_text(
                        original_text=input_text_to_rewrite,
                        rewrite_mode=rewrite_mode,
                        target_role=st.session_state.get("current_target_role", "AI Engineer"),
                        section_name=rw_sec
                    )
                    current[target_key] = improved_res
                    st.session_state["current_resume_dict"] = current
                    st.success(f"Rewrote {rw_sec} successfully!")
                    st.text_area("Rewritten Output Preview", value=improved_res, height=120)
                    st.rerun()

    # ==========================================================================
    # TAB 4: ATS SCORE & KEYWORD ANALYSIS (Section 10 & Section 11 requirement)
    # ==========================================================================
    with tab_ats:
        st.subheader("📊 ATS Optimization & Keyword Analysis")
        st.caption(f"Analyzing resume alignment for Target Role: **{st.session_state.get('current_target_role', 'AI Engineer')}**")

        plain_text_cur = exports["plain_text"]
        ats_eval = evaluate_resume_ats_scores(
            resume_dict=res_dict,
            full_resume_text=plain_text_cur,
            target_role=st.session_state.get("current_target_role", "AI Engineer"),
            job_description=st.session_state.get("current_jd", "")
        )

        st.markdown(f"""
        <div style="background: rgba(16, 185, 129, 0.15); border: 2px solid #10B981; border-radius: 14px; padding: 20px; text-align: center; margin-bottom: 20px;">
            <div style="font-size: 1.05rem; color: #34D399; font-weight: 700;">Overall ATS Score</div>
            <div style="font-size: 3.2rem; font-weight: 900; color: #FFFFFF;">{ats_eval['ats_score']}%</div>
            <div style="color: #A7F3D0; font-size: 0.9rem; margin-top: 2px;">
                {'🚀 Excellent ATS Compatibility' if ats_eval['ats_score'] >= 80 else '👍 Good Baseline ATS Compatibility'}
            </div>
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3, m4, m5, m6 = st.columns(6)
        with m1: st.metric("Overall Score", f"{ats_eval['resume_score']}%")
        with m2: st.metric("Keyword Match", f"{ats_eval['keyword_score']}%")
        with m3: st.metric("Skills Score", f"{ats_eval['skills_score']}%")
        with m4: st.metric("Experience", f"{ats_eval['experience_score']}%")
        with m5: st.metric("Education", f"{ats_eval['education_score']}%")
        with m6: st.metric("Completeness", f"{ats_eval['completeness_pct']}%")

        st.write("---")
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            st.markdown("#### ✅ Detected Keywords")
            if ats_eval['detected_keywords']:
                for dk in ats_eval['detected_keywords']:
                    st.success(f"✓ {dk}")
            else:
                st.info("No explicit keywords detected yet.")

        with col_k2:
            st.markdown("#### 💡 Recommended Missing Skills to Learn")
            if ats_eval['missing_keywords']:
                for mk in ats_eval['missing_keywords']:
                    st.warning(f"• {mk}")
            else:
                st.success("All target role keywords matched!")

        st.write("---")
        st.subheader("✨ AI Resume Improvement Summary (Section 11 requirement)")

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("##### 💪 Strengths")
            for st_item in ats_eval['strengths']:
                st.info(f"✔️ {st_item}")

        with col_s2:
            st.markdown("##### ⚠️ Weaknesses & Areas for Growth")
            for wk_item in ats_eval['weaknesses']:
                st.warning(f"⚠️ {wk_item}")

        st.markdown("##### 💡 Actionable Improvement Suggestions")
        for sg_item in ats_eval['suggestions']:
            st.caption(f"💡 {sg_item}")

    # ==========================================================================
    # TAB 5: SAVED RESUME VERSIONS (Section 17 & Section 18 requirement)
    # ==========================================================================
    with tab_versions:
        st.subheader("📜 Saved Resume Versions & History")
        saved_versions = get_user_saved_resumes(user_id)

        if saved_versions:
            for s_ver in saved_versions:
                v_id = s_ver.get("version_id")
                v_name = s_ver.get("version_name") or f"Resume Version #{v_id}"
                v_role = s_ver.get("target_role", "AI Engineer")
                v_tpl = s_ver.get("template", "Modern ATS")
                v_score = s_ver.get("ats_score", 85)
                v_active = s_ver.get("is_active", False)
                v_date = str(s_ver.get("created_at"))[:10]

                badge_active = " ⭐ ACTIVE RESUME" if v_active else ""

                with st.expander(f"📄 {v_name} | {v_role} | {v_tpl} | ATS: {v_score}% | {v_date}{badge_active}"):
                    st.write(f"**Target Role:** {v_role} | **Template:** {v_tpl} | **ATS Score:** {v_score}%")

                    col_v1, col_v2, col_v3 = st.columns(3)
                    with col_v1:
                        if st.button("🔄 Restore Version", key=f"btn_restore_{v_id}"):
                            st.session_state["current_resume_dict"] = {
                                "full_name": profile.get("full_name"),
                                "email": profile.get("email"),
                                "phone": profile.get("phone"),
                                "location": profile.get("location"),
                                "linkedin": profile.get("linkedin"),
                                "github": profile.get("github"),
                                "portfolio": profile.get("portfolio"),
                                "summary": s_ver.get("summary", ""),
                                "skills": s_ver.get("skills", ""),
                                "education": s_ver.get("education", ""),
                                "experience": s_ver.get("experience", ""),
                                "projects": s_ver.get("projects", ""),
                                "certifications": s_ver.get("certifications", ""),
                                "achievements": s_ver.get("achievements", "")
                            }
                            st.session_state["current_target_role"] = v_role
                            st.session_state["current_template"] = v_tpl
                            st.toast(f"Restored '{v_name}' successfully!")
                            st.rerun()

                    with col_v2:
                        if st.button("⭐ Set as Active Resume", key=f"btn_active_{v_id}"):
                            set_active_resume_version(user_id, v_id)
                            st.toast(f"Set '{v_name}' as your active resume!")
                            st.rerun()

                    with col_v3:
                        if st.button("🗑 Delete Version", key=f"btn_del_v_{v_id}"):
                            delete_user_resume_version(v_id, user_id)
                            st.toast(f"Deleted version #{v_id}!")
                            st.rerun()
        else:
            st.info("No saved resume versions found yet. Click '🚀 Generate AI Resume' in the Preview tab to save your first version!")

if __name__ == "__main__":
    render_resume_preparation_page()
