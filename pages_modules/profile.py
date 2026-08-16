import os
import streamlit as st
from pathlib import Path
from database.database import get_user_profile, update_user_profile
from services.profile_service import get_full_user_profile, calculate_profile_completion_details
from services.project_service import create_project, fetch_user_projects, fetch_project, edit_project, remove_project
from services.certificate_service import create_certificate, fetch_user_certificates, fetch_certificate, edit_certificate, remove_certificate
from services.resume_service import get_user_active_resume, process_and_save_resume, replace_existing_resume, delete_user_resume, get_user_resume_history_versions

def render_profile_page():
    st.header("👤 Comprehensive Candidate Profile")
    st.caption("Manage your Personal Details, Education, Skills, Projects, Certificates, Active Resume, and Professional Links.")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("🔒 Please log in to view and edit your profile.")
        st.stop()
    
    # Fetch full candidate profile
    profile = get_full_user_profile(user_id) or {}
    completion_info = calculate_profile_completion_details(user_id)
    pct = completion_info.get("percentage", 0)
    checklist = completion_info.get("checklist", {})

    # Top Profile Completion Widget
    st.markdown(f"### 📈 Profile Completion: **{pct}%**")
    st.progress(pct / 100.0)

    with st.expander("🔍 View Profile Completion Checklist Breakdown", expanded=False):
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            st.markdown(f"**Personal Details:** {'✅' if checklist.get('Personal Details') else '❌'}")
            st.markdown(f"**Education:** {'✅' if checklist.get('Education') else '❌'}")
            st.markdown(f"**Skills:** {'✅' if checklist.get('Skills') else '❌'}")
        with col_c2:
            proj_info = checklist.get('Projects', {})
            p_status = proj_info.get('status', False) if isinstance(proj_info, dict) else bool(proj_info)
            p_cnt = proj_info.get('count', 0) if isinstance(proj_info, dict) else 0
            st.markdown(f"**Projects:** {'✅' if p_status else '❌'} ({p_cnt} Added)")

            cert_info = checklist.get('Certificates', {})
            c_status = cert_info.get('status', False) if isinstance(cert_info, dict) else bool(cert_info)
            c_cnt = cert_info.get('count', 0) if isinstance(cert_info, dict) else 0
            st.markdown(f"**Certificates:** {'✅' if c_status else '❌'} ({c_cnt} Added)")

            st.markdown(f"**Active Resume:** {'✅' if checklist.get('Resume') else '❌'}")
        with col_c3:
            st.markdown(f"**LinkedIn:** {'✅' if checklist.get('LinkedIn') else '❌'}")
            st.markdown(f"**GitHub:** {'✅' if checklist.get('GitHub') else '❌'}")
            st.markdown(f"**Portfolio:** {'✅' if checklist.get('Portfolio') else '❌'}")

    st.write("---")

    # Main Profile Tabs
    tab_personal, tab_edu, tab_prof, tab_skills, tab_projects, tab_certs, tab_resume, tab_links = st.tabs([
        "👤 Personal Details",
        "🎓 Education",
        "💼 Professional Details",
        "🛠️ Skills",
        "📁 Projects",
        "🏆 Certifications",
        "📄 Active Resume",
        "🔗 Links"
    ])

    # --- TAB 1: PERSONAL DETAILS ---
    with tab_personal:
        st.subheader("👤 Personal Details")
        with st.form("personal_details_form"):
            c1, c2 = st.columns(2)
            with c1:
                full_name = st.text_input("Full Name *", value=profile.get("full_name", ""))
                email = st.text_input("Email Address *", value=profile.get("email", ""))
                mobile = st.text_input("Mobile Number *", value=profile.get("phone", ""))
                dob = st.text_input("Date of Birth (YYYY-MM-DD)", value=profile.get("dob", ""))
                gender_idx = ["Male", "Female", "Non-Binary", "Prefer Not to Say"].index(profile.get("gender")) if profile.get("gender") in ["Male", "Female", "Non-Binary", "Prefer Not to Say"] else 0
                gender = st.selectbox("Gender", ["Male", "Female", "Non-Binary", "Prefer Not to Say"], index=gender_idx)
            with c2:
                address = st.text_area("Address", value=profile.get("address", ""))
                city = st.text_input("City", value=profile.get("city", ""))
                state = st.text_input("State", value=profile.get("state", ""))
                country = st.text_input("Country", value=profile.get("country", "India"))
                pincode = st.text_input("Pincode", value=profile.get("pincode", ""))

            if st.form_submit_button("Save Personal Details", use_container_width=True):
                data = {
                    "full_name": full_name,
                    "email": email,
                    "mobile": mobile,
                    "date_of_birth": dob,
                    "gender": gender,
                    "address": address,
                    "city": city,
                    "state": state,
                    "country": country,
                    "pincode": pincode
                }
                if update_user_profile(user_id, data):
                    st.success("Personal details updated successfully!")
                    st.rerun()
                else:
                    st.error("Failed to update personal details.")

    # --- TAB 2: EDUCATION ---
    with tab_edu:
        st.subheader("🎓 Educational Details")
        with st.form("educational_details_form"):
            c_ed1, c_ed2 = st.columns(2)
            with c_ed1:
                college = st.text_input("College / Institute", value=profile.get("college", ""))
                university = st.text_input("University", value=profile.get("college", ""))
                qual_options = ["B.Tech", "B.E.", "B.S.", "M.Tech", "M.S.", "Ph.D", "Diploma", "Other"]
                qual_idx = qual_options.index(profile.get("degree")) if profile.get("degree") in qual_options else 0
                qualification = st.selectbox("Qualification", qual_options, index=qual_idx)
            with c_ed2:
                branch = st.text_input("Branch / Specialization", value=profile.get("specialization", ""))
                cgpa_val = float(profile.get("cgpa", 8.0) or 8.0)
                cgpa = st.number_input("CGPA / Percentage", min_value=0.0, max_value=10.0, value=cgpa_val)
                grad_val = int(profile.get("graduation_year", 2024) or 2024)
                grad_year = st.number_input("Graduation Year", min_value=1990, max_value=2030, value=grad_val)

            if st.form_submit_button("Save Educational Details", use_container_width=True):
                data = {
                    "college": college,
                    "university": university,
                    "qualification": qualification,
                    "branch": branch,
                    "cgpa": cgpa,
                    "graduation_year": grad_year
                }
                if update_user_profile(user_id, data):
                    st.success("Educational details updated successfully!")
                    st.rerun()
                else:
                    st.error("Failed to update educational details.")

    # --- TAB 3: PROFESSIONAL DETAILS ---
    with tab_prof:
        st.subheader("💼 Professional Experience")
        with st.form("professional_details_form"):
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                current_company = st.text_input("Current Company", value=profile.get("current_company", ""))
                current_role = st.text_input("Current Role", value=profile.get("current_role", ""))
                exp_years = st.number_input("Experience (Years)", min_value=0.0, max_value=40.0, value=float(profile.get("experience_years", 0.0)))
            with c_p2:
                career_obj = st.text_area("Career Objective", value=profile.get("career_objective", ""))

            if st.form_submit_button("Save Professional Details", use_container_width=True):
                data = {
                    "current_company": current_company,
                    "current_role": current_role,
                    "experience_years": exp_years,
                    "career_objective": career_obj
                }
                if update_user_profile(user_id, data):
                    st.success("Professional details updated successfully!")
                    st.rerun()
                else:
                    st.error("Failed to update professional details.")

    # --- TAB 4: SKILLS ---
    with tab_skills:
        st.subheader("🛠️ Technical & Soft Skills")
        with st.form("skills_form"):
            existing_tech = ", ".join(profile.get("technical_skills", []) + profile.get("tools_and_technologies", []))
            tech_skills = st.text_area("Technical Skills (Comma separated)", value=existing_tech)
            soft_skills = st.text_area("Soft Skills (Comma separated)", value=", ".join(profile.get("soft_skills", [])))

            if st.form_submit_button("Save Skills", use_container_width=True):
                data = {
                    "skills": tech_skills,
                    "technical_skills": tech_skills,
                    "soft_skills": soft_skills
                }
                if update_user_profile(user_id, data):
                    st.success("Skills updated successfully!")
                    st.rerun()
                else:
                    st.error("Failed to update skills.")

    # --- TAB 5: PROJECTS (MULTIPLE PROJECTS) ---
    with tab_projects:
        st.subheader("📁 Candidate Projects")
        st.caption("Add, view, edit, or remove your key engineering and software projects.")

        projects = fetch_user_projects(user_id)

        # Active form state toggles
        if "editing_project_id" not in st.session_state:
            st.session_state["editing_project_id"] = None
        if "show_add_project_form" not in st.session_state:
            st.session_state["show_add_project_form"] = False

        # Add Project Button
        if not st.session_state["show_add_project_form"] and st.session_state["editing_project_id"] is None:
            if st.button("➕ Add Project", type="primary"):
                st.session_state["show_add_project_form"] = True
                st.rerun()

        # Add Project Form
        if st.session_state["show_add_project_form"]:
            st.markdown("#### ➕ Add New Project")
            with st.form("add_project_form"):
                p_name = st.text_input("Project Name *")
                p_desc = st.text_area("Project Description *")
                col_pa, col_pb = st.columns(2)
                with col_pa:
                    p_tech = st.text_input("Technologies Used (e.g. Python, Streamlit, MySQL)")
                    p_role = st.text_input("Project Role (e.g. Lead AI Developer)")
                    p_start = st.text_input("Start Date (e.g. 2024-01-01)")
                    p_end = st.text_input("End Date (e.g. 2024-06-30 or Present)")
                with col_pb:
                    p_type = st.selectbox("Project Type", ["Web App", "AI / ML System", "Mobile App", "Open Source", "Enterprise", "Personal Project"])
                    p_github = st.text_input("GitHub URL")
                    p_live = st.text_input("Live Demo URL")
                
                p_contrib = st.text_area("Key Contributions")
                p_outcome = st.text_area("Project Outcome / Impact")

                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    save_p = st.form_submit_button("Save Project", use_container_width=True)
                with btn_col2:
                    cancel_p = st.form_submit_button("Cancel", use_container_width=True)

                if save_p:
                    p_data = {
                        "project_name": p_name,
                        "description": p_desc,
                        "technologies": p_tech,
                        "project_role": p_role,
                        "start_date": p_start,
                        "end_date": p_end,
                        "github_url": p_github,
                        "live_demo_url": p_live,
                        "project_type": p_type,
                        "key_contributions": p_contrib,
                        "project_outcome": p_outcome
                    }
                    success, msg, _ = create_project(user_id, p_data)
                    if success:
                        st.success(msg)
                        st.session_state["show_add_project_form"] = False
                        st.rerun()
                    else:
                        st.error(msg)
                
                if cancel_p:
                    st.session_state["show_add_project_form"] = False
                    st.rerun()

        # Display Projects List
        st.write("---")
        if not projects:
            st.info("No projects added yet. Click '+ Add Project' above to create your first project.")
        else:
            for proj in projects:
                p_id = proj["id"]
                
                # Check if editing this project
                if st.session_state["editing_project_id"] == p_id:
                    st.markdown(f"#### ✏️ Edit Project: **{proj.get('project_name')}**")
                    with st.form(f"edit_project_form_{p_id}"):
                        ep_name = st.text_input("Project Name *", value=proj.get("project_name", ""))
                        ep_desc = st.text_area("Project Description *", value=proj.get("description", ""))
                        c_ea, c_eb = st.columns(2)
                        with c_ea:
                            ep_tech = st.text_input("Technologies Used", value=proj.get("technologies", ""))
                            ep_role = st.text_input("Project Role", value=proj.get("project_role", ""))
                            ep_start = st.text_input("Start Date", value=str(proj.get("start_date") or ""))
                            ep_end = st.text_input("End Date", value=str(proj.get("end_date") or ""))
                        with c_eb:
                            p_type_opts = ["Web App", "AI / ML System", "Mobile App", "Open Source", "Enterprise", "Personal Project"]
                            cur_t_idx = p_type_opts.index(proj.get("project_type")) if proj.get("project_type") in p_type_opts else 0
                            ep_type = st.selectbox("Project Type", p_type_opts, index=cur_t_idx)
                            ep_github = st.text_input("GitHub URL", value=proj.get("github_url", ""))
                            ep_live = st.text_input("Live Demo URL", value=proj.get("live_demo_url", ""))

                        ep_contrib = st.text_area("Key Contributions", value=proj.get("key_contributions", ""))
                        ep_outcome = st.text_area("Project Outcome", value=proj.get("project_outcome", ""))

                        eb1, eb2 = st.columns(2)
                        with eb1:
                            update_btn = st.form_submit_button("Save Changes", use_container_width=True)
                        with eb2:
                            cancel_edit = st.form_submit_button("Cancel", use_container_width=True)

                        if update_btn:
                            ep_data = {
                                "project_name": ep_name,
                                "description": ep_desc,
                                "technologies": ep_tech,
                                "project_role": ep_role,
                                "start_date": ep_start,
                                "end_date": ep_end,
                                "github_url": ep_github,
                                "live_demo_url": ep_live,
                                "project_type": ep_type,
                                "key_contributions": ep_contrib,
                                "project_outcome": ep_outcome
                            }
                            ok, emsg = edit_project(p_id, user_id, ep_data)
                            if ok:
                                st.success(emsg)
                                st.session_state["editing_project_id"] = None
                                st.rerun()
                            else:
                                st.error(emsg)

                        if cancel_edit:
                            st.session_state["editing_project_id"] = None
                            st.rerun()
                else:
                    # Project Display Card
                    with st.container():
                        st.markdown(f"### 🚀 {proj.get('project_name')}")
                        st.caption(f"**Type:** {proj.get('project_type', 'Web App')} | **Role:** {proj.get('project_role', 'Developer')} | **Duration:** {proj.get('start_date', 'N/A')} to {proj.get('end_date', 'Present')}")
                        st.markdown(f"**Technologies:** `{proj.get('technologies', 'N/A')}`")
                        st.write(proj.get("description", ""))

                        if proj.get("key_contributions"):
                            st.markdown(f"**Key Contributions:** {proj.get('key_contributions')}")
                        if proj.get("project_outcome"):
                            st.markdown(f"**Outcome:** {proj.get('project_outcome')}")

                        links = []
                        if proj.get("github_url"):
                            links.append(f"[🔗 GitHub]({proj['github_url']})")
                        if proj.get("live_demo_url"):
                            links.append(f"[🌐 Live Demo]({proj['live_demo_url']})")
                        if links:
                            st.markdown(" ".join(links))

                        col_act1, col_act2, col_act3 = st.columns([1, 1, 4])
                        with col_act1:
                            if st.button("✏️ Edit", key=f"btn_edit_proj_{p_id}"):
                                st.session_state["editing_project_id"] = p_id
                                st.rerun()
                        with col_act2:
                            if st.button("🗑️ Delete", key=f"btn_del_proj_{p_id}"):
                                ok, dmsg = remove_project(user_id, p_id)
                                if ok:
                                    st.success(dmsg)
                                    st.rerun()
                                else:
                                    st.error(dmsg)
                        st.write("---")

    # --- TAB 6: CERTIFICATIONS (MULTIPLE CERTIFICATES) ---
    with tab_certs:
        st.subheader("🏆 Certificate Management")
        st.caption("Add, view, download, edit, or replace technical certificates and credentials.")

        certificates = fetch_user_certificates(user_id)

        if "editing_cert_id" not in st.session_state:
            st.session_state["editing_cert_id"] = None
        if "show_add_cert_form" not in st.session_state:
            st.session_state["show_add_cert_form"] = False

        if not st.session_state["show_add_cert_form"] and st.session_state["editing_cert_id"] is None:
            if st.button("➕ Add Certificate", type="primary"):
                st.session_state["show_add_cert_form"] = True
                st.rerun()

        # Add Certificate Form
        if st.session_state["show_add_cert_form"]:
            st.markdown("#### ➕ Add New Certificate")
            with st.form("add_cert_form"):
                c_name = st.text_input("Certificate Name *")
                c_org = st.text_input("Issuing Organization *")
                c_col1, c_col2 = st.columns(2)
                with c_col1:
                    c_issue = st.text_input("Issue Date (YYYY-MM-DD)")
                    c_cred_id = st.text_input("Credential ID")
                with c_col2:
                    c_expiry = st.text_input("Expiry Date (optional YYYY-MM-DD)")
                    c_cred_url = st.text_input("Credential URL")

                c_file = st.file_uploader("Upload Certificate File (PDF / JPG / JPEG / PNG)", type=["pdf", "jpg", "jpeg", "png"])

                cb1, cb2 = st.columns(2)
                with cb1:
                    save_c_btn = st.form_submit_button("Save Certificate", use_container_width=True)
                with cb2:
                    cancel_c_btn = st.form_submit_button("Cancel", use_container_width=True)

                if save_c_btn:
                    c_data = {
                        "certificate_name": c_name,
                        "title": c_name,
                        "issuing_organization": c_org,
                        "issuer": c_org,
                        "issue_date": c_issue,
                        "expiry_date": c_expiry,
                        "credential_id": c_cred_id,
                        "credential_url": c_cred_url
                    }
                    ok, cmsg, _ = create_certificate(user_id, c_data, file_obj=c_file)
                    if ok:
                        st.success(cmsg)
                        st.session_state["show_add_cert_form"] = False
                        st.rerun()
                    else:
                        st.error(cmsg)

                if cancel_c_btn:
                    st.session_state["show_add_cert_form"] = False
                    st.rerun()

        # Display Certificates List
        st.write("---")
        if not certificates:
            st.info("No certificates added yet. Click '+ Add Certificate' above to add credentials.")
        else:
            for cert in certificates:
                c_id = cert["id"]
                c_title = cert.get("certificate_name") or cert.get("title", "Certificate")
                c_issuer = cert.get("issuing_organization") or cert.get("issuer", "Organization")
                c_file_p = cert.get("certificate_path") or cert.get("file_path", "")

                if st.session_state["editing_cert_id"] == c_id:
                    st.markdown(f"#### ✏️ Edit Certificate: **{c_title}**")
                    with st.form(f"edit_cert_form_{c_id}"):
                        ec_name = st.text_input("Certificate Name *", value=c_title)
                        ec_org = st.text_input("Issuing Organization *", value=c_issuer)
                        ec_c1, ec_c2 = st.columns(2)
                        with ec_c1:
                            ec_issue = st.text_input("Issue Date", value=str(cert.get("issue_date") or ""))
                            ec_cred_id = st.text_input("Credential ID", value=cert.get("credential_id", ""))
                        with ec_c2:
                            ec_expiry = st.text_input("Expiry Date", value=str(cert.get("expiry_date") or ""))
                            ec_cred_url = st.text_input("Credential URL", value=cert.get("credential_url", ""))

                        ec_file = st.file_uploader("Replace Certificate File (Optional)", type=["pdf", "jpg", "jpeg", "png"])

                        ecb1, ecb2 = st.columns(2)
                        with ecb1:
                            update_c_btn = st.form_submit_button("Save Certificate", use_container_width=True)
                        with ecb2:
                            cancel_ec_btn = st.form_submit_button("Cancel", use_container_width=True)

                        if update_c_btn:
                            ec_data = {
                                "certificate_name": ec_name,
                                "title": ec_name,
                                "issuing_organization": ec_org,
                                "issuer": ec_org,
                                "issue_date": ec_issue,
                                "expiry_date": ec_expiry,
                                "credential_id": ec_cred_id,
                                "credential_url": ec_cred_url
                            }
                            ok, emsg = edit_certificate(c_id, user_id, ec_data, new_file_obj=ec_file)
                            if ok:
                                st.success(emsg)
                                st.session_state["editing_cert_id"] = None
                                st.rerun()
                            else:
                                st.error(emsg)

                        if cancel_ec_btn:
                            st.session_state["editing_cert_id"] = None
                            st.rerun()
                else:
                    # Certificate Card
                    with st.container():
                        st.markdown(f"### 📜 {c_title}")
                        st.markdown(f"**Issued by:** `{c_issuer}` | **Date:** `{cert.get('issue_date', 'N/A')}`" + (f" | **Expires:** `{cert.get('expiry_date')}`" if cert.get('expiry_date') else ""))
                        if cert.get("credential_id"):
                            st.markdown(f"**Credential ID:** `{cert.get('credential_id')}`")
                        if cert.get("credential_url"):
                            st.markdown(f"[🔗 Verify Credential]({cert.get('credential_url')})")

                        btn_c1, btn_c2, btn_c3, btn_c4 = st.columns([1, 1, 1, 3])
                        with btn_c1:
                            if c_file_p and os.path.exists(c_file_p):
                                with open(c_file_p, "rb") as f:
                                    st.download_button("📥 Download", data=f.read(), file_name=Path(c_file_p).name, key=f"dl_cert_{c_id}")
                        with btn_c2:
                            if st.button("✏️ Edit", key=f"btn_edit_cert_{c_id}"):
                                st.session_state["editing_cert_id"] = c_id
                                st.rerun()
                        with btn_c3:
                            if st.button("🗑️ Delete", key=f"btn_del_cert_{c_id}"):
                                ok, dmsg = remove_certificate(user_id, c_id)
                                if ok:
                                    st.success(dmsg)
                                    st.rerun()
                                else:
                                    st.error(dmsg)

                        st.write("---")

    # --- TAB 7: ACTIVE RESUME (EXACTLY ONE ACTIVE RESUME) ---
    with tab_resume:
        st.subheader("📄 Exactly One Active Resume")
        st.caption("Your candidate profile stores exactly ONE active resume used across ATS, Job Matching, and AI Assistant modules.")

        active_res = get_user_active_resume(user_id)
        if "show_replace_resume_form" not in st.session_state:
            st.session_state["show_replace_resume_form"] = False
        if "view_active_resume_text" not in st.session_state:
            st.session_state["view_active_resume_text"] = False

        if not active_res:
            st.warning("⚠️ No Active Resume Uploaded")
            st.info("Please upload your PDF or DOCX resume to activate ATS Analysis, Job Matching, and Career Recommendations.")
            
            with st.form("upload_first_resume_form"):
                res_file = st.file_uploader("Upload Resume (PDF or DOCX)", type=["pdf", "docx"])
                if st.form_submit_button("Upload & Activate Resume", use_container_width=True):
                    if res_file is not None:
                        try:
                            parsed_res = process_and_save_resume(user_id, res_file)
                            st.success("Resume uploaded and set as Active!")
                            st.rerun()
                        except Exception as ex:
                            st.error(f"Upload failed: {ex}")
                    else:
                        st.error("Please select a valid PDF or DOCX file.")
        else:
            # Active Resume Card
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.05); border-left: 4px solid #10B981; padding: 16px; border-radius: 8px; margin-bottom: 20px;">
                <h3 style="margin-top:0; color: #10B981;">✅ Active Resume</h3>
                <p><b>Resume Name:</b> {active_res.get('filename')}</p>
                <p><b>Uploaded Date:</b> {active_res.get('uploaded_at') or 'Recently'}</p>
                <p><b>Version:</b> v{active_res.get('version', 1)} | <b>Status:</b> <span style="background:#10B981; color:white; padding:2px 8px; border-radius:4px; font-size:12px;">Active</span></p>
                <p><b>ATS Match Score:</b> {active_res.get('ats_score', 85)}%</p>
            </div>
            """, unsafe_allow_html=True)

            r_col1, r_col2, r_col3, r_col4 = st.columns(4)
            with r_col1:
                if st.button("👁️ View Resume", use_container_width=True):
                    st.session_state["view_active_resume_text"] = not st.session_state["view_active_resume_text"]
            with r_col2:
                r_path = active_res.get("file_path")
                if r_path and os.path.exists(r_path):
                    with open(r_path, "rb") as f:
                        st.download_button("📥 Download", data=f.read(), file_name=active_res.get("filename"), use_container_width=True)
            with r_col3:
                if st.button("🔄 Replace Resume", type="primary", use_container_width=True):
                    st.session_state["show_replace_resume_form"] = not st.session_state["show_replace_resume_form"]
            with r_col4:
                if st.button("🗑️ Delete Resume", use_container_width=True):
                    if delete_user_resume(user_id, active_res["id"]):
                        st.success("Active resume deleted.")
                        st.rerun()

            # View Extracted Resume Text Modal/Expander
            if st.session_state.get("view_active_resume_text"):
                with st.expander("📑 Extracted Active Resume Content", expanded=True):
                    st.text_area("Raw Extracted Text", value=active_res.get("raw_text", ""), height=250)

            # Replace Resume Workflow Form
            if st.session_state.get("show_replace_resume_form"):
                st.write("---")
                st.markdown("#### 🔄 Replace Active Resume")
                st.caption("Replacing will archive version v{} and execute full re-extraction, ATS Analysis, Skill Gap, Job Matching, and Dashboard updates.").format(active_res.get('version', 1))
                
                with st.form("replace_active_resume_form"):
                    new_res_file = st.file_uploader("Select New PDF or DOCX Resume *", type=["pdf", "docx"])
                    rc_b1, rc_b2 = st.columns(2)
                    with rc_b1:
                        exec_replace = st.form_submit_button("Confirm & Replace Resume", use_container_width=True)
                    with rc_b2:
                        cancel_replace = st.form_submit_button("Cancel", use_container_width=True)

                    if exec_replace:
                        if new_res_file is not None:
                            try:
                                with st.spinner("Replacing resume, re-extracting text, and re-running ATS & Job Matching pipelines..."):
                                    replace_existing_resume(user_id, active_res["id"], new_res_file)
                                st.success(f"Successfully replaced active resume with '{new_res_file.name}'!")
                                st.session_state["show_replace_resume_form"] = False
                                st.rerun()
                            except Exception as ex:
                                st.error(f"Replacement failed: {ex}")
                        else:
                            st.error("Please upload a valid PDF or DOCX file.")

                    if cancel_replace:
                        st.session_state["show_replace_resume_form"] = False
                        st.rerun()

            # Resume History Expander
            st.write("---")
            with st.expander("📚 Resume History (Past Versions)", expanded=False):
                versions = get_user_resume_history_versions(user_id)
                if not versions:
                    st.caption("No past versions found.")
                else:
                    for v in versions:
                        st.markdown(f"• **v{v.get('version', 1)}** - `{v.get('filename') or v.get('resume_name')}` | Uploaded: {v.get('uploaded_at')} | Status: **{v.get('status', 'Archived')}** | ATS Score: {v.get('ats_score', 80)}%")

    # --- TAB 8: PROFESSIONAL LINKS ---
    with tab_links:
        st.subheader("🔗 Professional Social Links")
        with st.form("professional_links_form"):
            linkedin_url = st.text_input("LinkedIn Profile URL", value=profile.get("linkedin", ""))
            github_url = st.text_input("GitHub Profile URL", value=profile.get("github", ""))
            portfolio_url = st.text_input("Portfolio Website URL", value=profile.get("portfolio", ""))

            if st.form_submit_button("Save Social Links", use_container_width=True):
                data = {
                    "linkedin_url": linkedin_url,
                    "github_url": github_url,
                    "portfolio_url": portfolio_url
                }
                if update_user_profile(user_id, data):
                    st.success("Professional links updated successfully!")
                    st.rerun()
                else:
                    st.error("Failed to update professional links.")

if __name__ == "__main__":
    render_profile_page()
