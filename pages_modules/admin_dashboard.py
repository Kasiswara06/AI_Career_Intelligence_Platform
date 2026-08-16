import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database.database import execute_query
from auth.authorization import check_admin_access
from services.admin_service import (
    get_admin_kpi_metrics,
    get_admin_users_list,
    get_login_activity_logs,
    get_resume_activity_logs,
    get_resume_analysis_monitoring,
    get_user_activity_timeline,
    get_detailed_user_inspector,
    update_user_role,
    update_user_basic_info,
    delete_user_account,
    get_admin_resumes_directory,
    toggle_resume_active_status,
    delete_admin_resume_record,
    get_resume_parsing_analytics,
    get_admin_jobs_list,
    add_admin_job,
    update_admin_job,
    delete_admin_job,
    get_skill_gap_analytics,
    get_ats_score_analytics,
    get_career_recommendation_analytics,
    get_job_match_analytics,
    get_admin_courses_list,
    add_admin_course,
    update_admin_course,
    delete_admin_course,
    get_admin_certificates_list,
    get_admin_feedback_list,
    update_feedback_status,
    delete_user_feedback,
    submit_user_feedback,
    get_system_health_metrics,
    get_system_notifications,
    generate_csv_report
)

def render_admin_dashboard_page():
    """Renders commercial-grade Admin Analytics & Platform Monitoring Dashboard covering all Milestone 4 features."""
    
    # ----------------------------------------------------
    # FEATURE 1 & 18: RBAC AUTHORIZATION CHECK & SECURE LOGIN
    # ----------------------------------------------------
    if not check_admin_access():
        st.error("🚫 **Access Denied: Admin Privileges Required**")
        st.warning("You must be logged in with an administrator account (`role = 'admin'`) to access this dashboard.")
        st.info("💡 **Demo Admin Credentials**: Sign in with `admin@careerintel.ai` / `Admin@123456`.")
        return

    # Header Title Banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.95), rgba(15, 23, 42, 0.95)); padding: 22px 28px; border-radius: 14px; border: 1px solid rgba(59, 130, 246, 0.3); margin-bottom: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style="margin: 0; color: #f8fafc; font-size: 2.1rem; display: flex; align-items: center; gap: 10px;">
                    🛡️ Admin Dashboard — Milestone 4 Management Console
                </h1>
                <p style="color: #93c5fd; margin-top: 6px; font-size: 1rem;">
                    Complete AI Platform Control: Candidate Management, Resume Parsing, Job Descriptions, ATS Intelligence, Skill Gaps, Feedback, and System Health.
                </p>
            </div>
            <span style="background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 0.9rem;">
                🟢 SECURE ADMIN SESSION
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # FEATURE 17: NOTIFICATIONS & ALERTS BANNER
    # ----------------------------------------------------
    alerts = get_system_notifications()
    if alerts:
        with st.expander("🔔 **System Notifications & Important Alerts**", expanded=True):
            for alert in alerts:
                if alert["type"] == "warning":
                    st.warning(alert["message"])
                elif alert["type"] == "info":
                    st.info(alert["message"])
                elif alert["type"] == "success":
                    st.success(alert["message"])

    # ----------------------------------------------------
    # FEATURE 2: DASHBOARD OVERVIEW & EXECUTIVE STATISTICS (8 KPIs)
    # ----------------------------------------------------
    metrics = get_admin_kpi_metrics()
    st.markdown("### 📌 Platform Overview & Statistics")
    
    k1, k2, k3, k4, k5, k6, k7, k8 = st.columns(8)
    with k1:
        st.metric("Total Users", metrics["total_users"])
    with k2:
        st.metric("Today's Users", metrics["today_users"])
    with k3:
        st.metric("Total Logins", metrics["total_logins"])
    with k4:
        st.metric("Today's Logins", metrics["today_logins"])
    with k5:
        st.metric("Total Resumes", metrics["total_resumes"])
    with k6:
        st.metric("Analyses", metrics["total_analyses"])
    with k7:
        st.metric("Job Matches", metrics["total_job_matches"])
    with k8:
        st.metric("Active Users", metrics["active_users"])

    st.write("---")

    # ----------------------------------------------------
    # MAIN ADMIN MANAGEMENT TABS (9 Comprehensive Tabs)
    # ----------------------------------------------------
    admin_tab1, admin_tab2, admin_tab3, admin_tab4, admin_tab5, admin_tab6, admin_tab7, admin_tab8, admin_tab9 = st.tabs([
        "📊 Overview Analytics",
        "👥 User Management",
        "📄 Resume Management",
        "💼 Job Descriptions",
        "🎯 AI Analytics",
        "🎓 Courses & Certs",
        "💬 User Feedback",
        "🖥️ System Monitoring",
        "📥 Search & Reports"
    ])

    # =====================================================================
    # TAB 1: OVERVIEW & STATISTICS CHARTS
    # =====================================================================
    with admin_tab1:
        st.subheader("📊 Executive Overview & Application Usage Trends")
        st.caption("Real-time visual monitoring of user growth, module adoption, and candidate engagement.")

        ch_col1, ch_col2 = st.columns(2)
        with ch_col1:
            st.markdown("#### 📈 Registration & User Activity Metrics")
            chart_df1 = pd.DataFrame({
                "Metric": ["Total Users", "Today's Users", "Total Logins", "Today's Logins", "Active Users"],
                "Count": [metrics["total_users"], metrics["today_users"], metrics["total_logins"], metrics["today_logins"], metrics["active_users"]]
            })
            fig1 = px.bar(chart_df1, x="Metric", y="Count", color="Metric", text_auto=True,
                          color_discrete_sequence=["#38bdf8", "#818cf8", "#c084fc", "#22c55e", "#facc15"])
            fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'), showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)

        with ch_col2:
            st.markdown("#### 🎯 Core AI Activity Breakdown")
            chart_df2 = pd.DataFrame({
                "Activity": ["Resume Uploads", "Resume Analyses", "Job Matches", "Active Users"],
                "Volume": [metrics["total_resumes"], metrics["total_analyses"], metrics["total_job_matches"], metrics["active_users"]]
            })
            fig2 = px.pie(chart_df2, values="Volume", names="Activity", color_discrete_sequence=["#38bdf8", "#818cf8", "#22c55e", "#facc15"])
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'))
            st.plotly_chart(fig2, use_container_width=True)

    # =====================================================================
    # TAB 2: USER MANAGEMENT & PROFILE MANAGEMENT (FEATURE 3, 4, 18, 19)
    # =====================================================================
    with admin_tab2:
        st.subheader("👥 User Account & Profile Management")
        st.caption("SECURITY GUARANTEE: User passwords and password hashes are strictly excluded from all database queries and displays.")

        u_subtab1, u_subtab2, u_subtab3 = st.tabs(["🔍 Candidate Directory & Actions", "👤 Detailed Candidate Inspector", "🛡️ RBAC Permissions"])

        # --- SUBTAB 1: USER DIRECTORY & ACTIONS ---
        with u_subtab1:
            f_c1, f_c2, f_c3 = st.columns([3, 2, 2])
            with f_c1:
                search_query = st.text_input("🔍 Search User by Name or Email", placeholder="Type candidate name or email...", key="usr_srch")
            with f_c2:
                resume_filter = st.selectbox("📄 Filter by Resume Status", ["All", "With Active Resume", "No Resume"], key="usr_res_flt")
            with f_c3:
                role_filter = st.selectbox("🛡️ Filter by Role", ["All", "User", "Admin"], key="usr_rl_flt")

            users_list = get_admin_users_list(search_query=search_query, resume_filter=resume_filter)
            if role_filter != "All":
                users_list = [u for u in users_list if u.get("role", "").lower() == role_filter.lower()]

            st.markdown(f"**Found {len(users_list)} registered candidate users:**")

            if users_list:
                df_users = pd.DataFrame(users_list)
                display_cols = ["user_id", "full_name", "email", "mobile", "role", "registered_date", "last_login", "login_count", "resume_status"]
                df_users_dsp = df_users[[c for c in display_cols if c in df_users.columns]]
                df_users_dsp.columns = ["User ID", "Full Name", "Email", "Mobile", "Role", "Registered Date", "Last Login", "Logins", "Resume"]
                st.dataframe(df_users_dsp, use_container_width=True, hide_index=True)

                st.write("---")
                st.markdown("#### ⚡ Administrative Account Operations")
                action_u_col1, action_u_col2 = st.columns(2)

                with action_u_col1:
                    with st.expander("🛠️ Update Candidate Info or Role"):
                        user_map = {f"ID #{u['user_id']} — {u['full_name']} ({u['email']})": u for u in users_list if u.get("user_id")}
                        if user_map:
                            sel_usr_label = st.selectbox("Select Target Candidate", list(user_map.keys()), key="upd_usr_sel")
                            target_u = user_map[sel_usr_label]
                            
                            upd_name = st.text_input("Full Name", value=target_u["full_name"], key="upd_fn")
                            upd_email = st.text_input("Email Address", value=target_u["email"], key="upd_em")
                            upd_mobile = st.text_input("Mobile Number", value=target_u["mobile"], key="upd_mb")
                            upd_role = st.selectbox("Assigned Access Role", ["user", "admin"], index=0 if target_u["role"]=="user" else 1, key="upd_rl")

                            if st.button("Save Changes", type="primary", key="btn_save_usr"):
                                b_ok = update_user_basic_info(target_u["user_id"], upd_name, upd_email, upd_mobile)
                                r_ok = update_user_role(target_u["user_id"], upd_role)
                                if b_ok or r_ok:
                                    st.success(f"Successfully updated User #{target_u['user_id']} ({upd_name}).")
                                    st.rerun()

                with action_u_col2:
                    with st.expander("🗑️ Delete Candidate Account"):
                        st.warning("⚠️ Deleting a user permanently purges their resumes, ATS analyses, and activity logs.")
                        del_user_map = {f"ID #{u['user_id']} — {u['full_name']}": u['user_id'] for u in users_list if u.get("user_id")}
                        if del_user_map:
                            del_target_id = st.selectbox("Select Account to Remove", list(del_user_map.keys()), key="del_usr_sel")
                            confirm_del = st.checkbox("I confirm permanent deletion of this user.", key="chk_del_usr")
                            if st.button("Delete Account Permanently", type="secondary", key="btn_del_usr"):
                                if confirm_del:
                                    uid = del_user_map[del_target_id]
                                    if delete_user_account(uid):
                                        st.success(f"Candidate User #{uid} was removed successfully.")
                                        st.rerun()
                                    else:
                                        st.error("Failed to delete user record.")
                                else:
                                    st.info("Please check confirmation box to proceed.")
            else:
                st.info("No registered users match your criteria.")

        # --- SUBTAB 2: CANDIDATE PROFILE INSPECTOR ---
        with u_subtab2:
            all_users = get_admin_users_list()
            user_options = {f"{u['full_name']} ({u['email']})": u['user_id'] for u in all_users if u.get("user_id")}
            if user_options:
                selected_user_str = st.selectbox("Select Candidate to Inspect Profile", list(user_options.keys()), key="insp_sel")
                selected_uid = user_options[selected_user_str]
                inspector_data = get_detailed_user_inspector(selected_uid)

                if inspector_data:
                    st.write("---")
                    st.markdown(f"### 👤 Candidate Profile Inspector: **{inspector_data['full_name']}** (ID: `{inspector_data['user_id']}`)")
                    
                    ic1, ic2 = st.columns(2)
                    with ic1:
                        st.markdown("#### 📋 General Profile Details")
                        st.write(f"**Email:** {inspector_data['email']}")
                        st.write(f"**Mobile:** {inspector_data['mobile']}")
                        st.write(f"**Role:** `{inspector_data['role']}`")
                        st.write(f"**Registration Date:** {inspector_data['registered_at']}")
                        
                        prof = inspector_data.get("profile", {})
                        st.write(f"**College/University:** {prof.get('college', 'N/A')}")
                        st.write(f"**Qualification:** {prof.get('qualification', 'N/A')} ({prof.get('branch', 'N/A')})")
                        st.write(f"**Experience Years:** {prof.get('experience_years', 0.0)} Years")
                        st.write(f"**Current Company:** {prof.get('current_company', 'N/A')}")

                    with ic2:
                        st.markdown("#### 📄 Active Resume & Intelligence Scores")
                        resumes = inspector_data.get("resumes", [])
                        if resumes:
                            active_r = next((r for r in resumes if r.get("is_active")), resumes[0])
                            st.success(f"**Active File:** `{active_r.get('filename')}`")
                            st.metric("Resume Quality Score", f"{active_r.get('resume_score', 85)}/100")
                            st.metric("ATS Compatibility", f"{active_r.get('ats_score', 88)}%")
                        else:
                            st.warning("No active resume uploaded.")

                    st.write("---")
                    st.markdown("#### 📜 Candidate Activity Timeline")
                    user_timeline = inspector_data.get("timeline", [])
                    if user_timeline:
                        for t in user_timeline:
                            st.markdown(f"- 🕒 **[{t['timestamp']}]** `{t['action']}`: {t['details']}")
                    else:
                        st.info("No recorded activity logs for this candidate.")

        # --- SUBTAB 3: ROLE-BASED ACCESS CONTROL (RBAC) MATRIX ---
        with u_subtab3:
            st.markdown("#### 🛡️ Role-Based Access Control (RBAC) Matrix")
            rbac_df = pd.DataFrame([
                {"Module / Feature": "Candidate Dashboard & Resume Builder", "User Access": "✅ Granted", "Admin Access": "✅ Granted"},
                {"Module / Feature": "Resume Upload & ATS Analysis", "User Access": "✅ Granted", "Admin Access": "✅ Granted"},
                {"Module / Feature": "AI Career Assistant & Chat", "User Access": "✅ Granted", "Admin Access": "✅ Granted"},
                {"Module / Feature": "User Management & Role Switching", "User Access": "🚫 Restricted", "Admin Access": "✅ Full Control"},
                {"Module / Feature": "Job Posting Creation & Deletion", "User Access": "🚫 Restricted", "Admin Access": "✅ Full Control"},
                {"Module / Feature": "System/API Health Monitoring", "User Access": "🚫 Restricted", "Admin Access": "✅ Full Control"},
                {"Module / Feature": "User Feedback Audit & Resolution", "User Access": "🚫 Restricted", "Admin Access": "✅ Full Control"},
                {"Module / Feature": "CSV Data Export & Audit Reports", "User Access": "🚫 Restricted", "Admin Access": "✅ Full Control"},
            ])
            st.table(rbac_df)

    # =====================================================================
    # TAB 3: RESUME MANAGEMENT & RESUME PARSING MONITORING (FEATURE 5, 6, 8)
    # =====================================================================
    with admin_tab3:
        st.subheader("📄 Resume Directory & Parsing Health Monitoring")
        st.caption("Monitor candidate uploaded files, resume status, parsing success rates, and ATS analyses.")

        r_m_tab1, r_m_tab2, r_m_tab3 = st.tabs(["📂 Resumes Directory", "⚙️ Parsing Health & Status", "📊 ATS Scores Audit"])

        # --- SUBTAB 1: RESUMES DIRECTORY ---
        with r_m_tab1:
            r_search = st.text_input("🔍 Filter Resumes by Candidate Name / File", placeholder="Type name or file...", key="res_dir_srch")
            res_list = get_admin_resumes_directory(search_query=r_search)

            st.markdown(f"**Found {len(res_list)} uploaded resume records:**")
            if res_list:
                df_res = pd.DataFrame(res_list)
                df_res_dsp = df_res[["resume_id", "candidate_name", "email", "filename", "version", "is_active", "parsing_status", "ats_score", "uploaded_at"]]
                df_res_dsp.columns = ["Resume ID", "Candidate", "Email", "Filename", "Version", "Status", "Parsing Status", "ATS Score", "Uploaded At"]
                st.dataframe(df_res_dsp, use_container_width=True, hide_index=True)

                st.write("---")
                st.markdown("#### ⚡ Resume Actions")
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    with st.expander("🔄 Toggle Active/Archived Status"):
                        res_map = {f"ID #{r['resume_id']} — {r['candidate_name']} ({r['filename']})": r for r in res_list}
                        sel_r_str = st.selectbox("Select Target Resume", list(res_map.keys()), key="tgl_res_sel")
                        target_r = res_map[sel_r_str]
                        if st.button("Toggle Status", key="btn_tgl_res"):
                            if toggle_resume_active_status(target_r["resume_id"], target_r["user_id"]):
                                st.success("Updated resume active status.")
                                st.rerun()

                with res_col2:
                    with st.expander("🗑️ Delete Resume Record"):
                        del_r_str = st.selectbox("Select Resume to Remove", list(res_map.keys()), key="del_res_sel")
                        target_del_r = res_map[del_r_str]
                        if st.button("Delete Resume Record", key="btn_del_res"):
                            if delete_admin_resume_record(target_del_r["resume_id"], target_del_r["user_id"]):
                                st.success("Resume record removed.")
                                st.rerun()

        # --- SUBTAB 2: PARSING HEALTH & STATUS ---
        with r_m_tab2:
            st.markdown("#### ⚙️ Resume Parsing Pipeline Health")
            p_health = get_resume_parsing_analytics()
            p1, p2, p3, p4 = st.columns(4)
            with p1:
                st.metric("Total Resumes", p_health["total_resumes"])
            with p2:
                st.metric("Parsed Successfully", p_health["parsed_successfully"])
            with p3:
                st.metric("Parsing Failures / Empty", p_health["parsing_failures"])
            with p4:
                st.metric("Parsing Success Rate", f"{p_health['success_rate']}%")

            st.write("---")
            st.markdown("#### 📜 Parsing & File Activity Audit Log")
            r_events = get_resume_activity_logs(limit=25)
            if r_events:
                df_ev = pd.DataFrame(r_events)
                df_ev = df_ev[["log_id", "full_name", "email", "action", "details", "timestamp"]]
                df_ev.columns = ["Log ID", "Candidate", "Email", "Action", "Details", "Timestamp"]
                st.dataframe(df_ev, use_container_width=True, hide_index=True)

        # --- SUBTAB 3: ATS SCORES AUDIT ---
        with r_m_tab3:
            st.markdown("#### 📊 ATS Score Audit & Review")
            ans_logs = get_resume_analysis_monitoring(limit=30)
            if ans_logs:
                df_ans = pd.DataFrame(ans_logs)
                df_ans = df_ans[["analysis_id", "full_name", "email", "resume_name", "resume_score", "ats_score", "resume_quality", "analyzed_at"]]
                df_ans.columns = ["Analysis ID", "Candidate", "Email", "Resume File", "Quality Score", "ATS Compatibility", "Quality Rating", "Analyzed At"]
                st.dataframe(df_ans, use_container_width=True, hide_index=True)

    # =====================================================================
    # TAB 4: JOB DESCRIPTION MANAGEMENT (FEATURE 7)
    # =====================================================================
    with admin_tab4:
        st.subheader("💼 Job Description Management")
        st.caption("Add, edit, remove, and manage job postings and required candidate skills.")

        j_tab1, j_tab2 = st.tabs(["📋 Active Job Postings", "➕ Add New Job Description"])

        # --- SUBTAB 1: JOB LIST & EDITING ---
        with j_tab1:
            j_search = st.text_input("🔍 Search Job Descriptions by Title or Company", key="job_srch")
            jobs_list = get_admin_jobs_list(search_query=j_search)

            st.markdown(f"**Found {len(jobs_list)} active job descriptions:**")
            if jobs_list:
                df_jobs = pd.DataFrame(jobs_list)
                df_jobs_dsp = df_jobs[["job_id", "job_title", "company", "location", "experience_level", "qualification", "salary_range", "created_at"]]
                df_jobs_dsp.columns = ["Job ID", "Job Title", "Company", "Location", "Experience", "Qualification", "Salary Range", "Posted At"]
                st.dataframe(df_jobs_dsp, use_container_width=True, hide_index=True)

                st.write("---")
                st.markdown("#### 🛠️ Manage Job Postings")
                j_col1, j_col2 = st.columns(2)

                with j_col1:
                    with st.expander("✏️ Edit Job Description"):
                        job_map = {f"Job #{j['job_id']} — {j['job_title']} ({j['company']})": j for j in jobs_list}
                        sel_job_str = st.selectbox("Select Job Posting to Edit", list(job_map.keys()), key="edit_job_sel")
                        target_j = job_map[sel_job_str]

                        e_title = st.text_input("Job Title", value=target_j["job_title"], key="e_j_title")
                        e_company = st.text_input("Company", value=target_j["company"], key="e_j_comp")
                        e_loc = st.text_input("Location", value=target_j["location"], key="e_j_loc")
                        e_exp = st.selectbox("Experience Level", ["Entry Level", "Mid Level", "Senior Level", "Lead / Principal"],
                                             index=1, key="e_j_exp")
                        e_qual = st.text_input("Qualification", value=target_j["qualification"], key="e_j_qual")
                        e_sal = st.text_input("Salary Range", value=target_j["salary_range"], key="e_j_sal")
                        e_skills = st.text_area("Required Skills (comma separated)", value=target_j["required_skills"], key="e_j_skills")
                        e_desc = st.text_area("Job Description", value=target_j["job_description"], height=120, key="e_j_desc")

                        if st.button("Update Job Description", type="primary", key="btn_upd_job"):
                            if update_admin_job(target_j["job_id"], e_title, e_company, e_loc, e_exp, e_qual, e_sal, e_skills, e_desc):
                                st.success(f"Job #{target_j['job_id']} updated successfully!")
                                st.rerun()

                with j_col2:
                    with st.expander("🗑️ Delete Job Posting"):
                        del_j_str = st.selectbox("Select Job Posting to Remove", list(job_map.keys()), key="del_j_sel")
                        target_del_j = job_map[del_j_str]
                        if st.button("Delete Job Posting", key="btn_del_j"):
                            if delete_admin_job(target_del_j["job_id"]):
                                st.success(f"Job #{target_del_j['job_id']} deleted successfully!")
                                st.rerun()

        # --- SUBTAB 2: ADD NEW JOB DESCRIPTION ---
        with j_tab2:
            st.markdown("#### ➕ Post New Job Description")
            with st.form("add_job_form", clear_on_submit=True):
                col_a, col_b = st.columns(2)
                with col_a:
                    new_title = st.text_input("Job Title *", placeholder="e.g. Senior AI Engineer")
                    new_company = st.text_input("Company *", placeholder="e.g. OpenAI Tech")
                    new_loc = st.text_input("Location", placeholder="e.g. Bangalore / Remote")
                    new_exp = st.selectbox("Experience Level", ["Entry Level", "Mid Level", "Senior Level", "Lead / Executive"])
                with col_b:
                    new_qual = st.text_input("Qualification", placeholder="e.g. B.Tech / M.Tech in CS")
                    new_sal = st.text_input("Salary Range", placeholder="e.g. 12 - 18 LPA")
                    new_skills = st.text_area("Required Skills", placeholder="e.g. Python, PyTorch, Transformers, FastAPI, Docker")
                
                new_desc = st.text_area("Job Description *", placeholder="Detailed responsibilities and candidate expectations...", height=120)
                submit_job = st.form_submit_button("🚀 Add Job Posting")

                if submit_job:
                    if new_title and new_company and new_desc:
                        if add_admin_job(new_title, new_company, new_loc, new_exp, new_qual, new_sal, new_skills, new_desc):
                            st.success("New Job Description posted successfully!")
                            st.rerun()
                    else:
                        st.error("Please fill in all required fields (Title, Company, Description).")

    # =====================================================================
    # TAB 5: AI ANALYTICS (FEATURE 9, 10, 11)
    # =====================================================================
    with admin_tab5:
        st.subheader("🎯 AI Analytics & Candidate Intelligence")
        st.caption("Aggregated analytics on candidate skill deficiencies, career recommendation trends, and job matching success rates.")

        ai_an_tab1, ai_an_tab2, ai_an_tab3 = st.tabs(["📉 Skill Gap Analytics", "🚀 Career Recommendation Trends", "🎯 Job Recommendation Analytics"])

        # --- SKILL GAP ANALYTICS ---
        with ai_an_tab1:
            st.markdown("#### 📉 Most Commonly Missing Skills Among Candidates")
            sg_data = get_skill_gap_analytics()
            
            m1, m2 = st.columns(2)
            with m1:
                st.metric("Total Analyzed Candidate Resumes", sg_data["total_analyzed_gaps"])
            with m2:
                st.metric("Average Career Readiness Score", f"{sg_data['average_readiness_score']}%")

            if sg_data["top_missing_skills"]:
                top_skills_df = pd.DataFrame(sg_data["top_missing_skills"], columns=["Skill Name", "Deficiency Count"])
                fig_sg = px.bar(top_skills_df, x="Deficiency Count", y="Skill Name", orientation="h",
                                color="Deficiency Count", color_continuous_scale="Reds", text_auto=True)
                fig_sg.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'))
                st.plotly_chart(fig_sg, use_container_width=True)

        # --- CAREER RECOMMENDATION ANALYTICS ---
        with ai_an_tab2:
            st.markdown("#### 🚀 Career Recommendations Analytics")
            cr_data = get_career_recommendation_analytics()
            st.metric("Total Generated Career Roadmaps", cr_data["total_career_recommendations"])

            if cr_data["top_target_roles"]:
                cr_df = pd.DataFrame(cr_data["top_target_roles"], columns=["Target Role", "Generation Count"])
                fig_cr = px.pie(cr_df, values="Generation Count", names="Target Role",
                                color_discrete_sequence=px.colors.sequential.Blues_r)
                fig_cr.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'))
                st.plotly_chart(fig_cr, use_container_width=True)

        # --- JOB RECOMMENDATION ANALYTICS ---
        with ai_an_tab3:
            st.markdown("#### 🎯 Recommended Jobs & Matching Results")
            jm_data = get_job_match_analytics()
            
            jm1, jm2, jm3 = st.columns(3)
            with jm1:
                st.metric("Total Candidate Job Matches", jm_data["total_matches"])
            with jm2:
                st.metric("Average Compatibility Match", f"{jm_data['avg_match_pct']}%")
            with jm3:
                st.metric("High Match Count (75%+)", jm_data["high_match_count"])

            jm_chart_df = pd.DataFrame({
                "Compatibility Tier": ["High Match (75%+)", "Medium Match (50-74%)", "Low Match (<50%)"],
                "Count": [jm_data["high_match_count"], jm_data["med_match_count"], jm_data["low_match_count"]]
            })
            fig_jm = px.bar(jm_chart_df, x="Compatibility Tier", y="Count", color="Compatibility Tier", text_auto=True,
                            color_discrete_sequence=["#22c55e", "#facc15", "#ef4444"])
            fig_jm.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'), showlegend=False)
            st.plotly_chart(fig_jm, use_container_width=True)

    # =====================================================================
    # TAB 6: COURSE & CERTIFICATION MANAGEMENT (FEATURE 12)
    # =====================================================================
    with admin_tab6:
        st.subheader("🎓 Course & Certification Management")
        st.caption("Manage recommended upskilling courses and view candidate uploaded certifications.")

        cc_tab1, cc_tab2 = st.tabs(["📚 Managed Courses Catalog", "📜 Candidate Certifications"])

        # --- MANAGED COURSES CATALOG ---
        with cc_tab1:
            c_search = st.text_input("🔍 Search Courses by Title or Skill", key="crs_srch")
            courses_list = get_admin_courses_list(search_query=c_search)

            st.markdown(f"**Found {len(courses_list)} recommended courses:**")
            if courses_list:
                df_crs = pd.DataFrame(courses_list)
                df_crs_dsp = df_crs[["course_id", "course_title", "platform", "target_skill", "difficulty", "duration", "created_at"]]
                df_crs_dsp.columns = ["Course ID", "Course Title", "Platform", "Target Skill", "Difficulty", "Duration", "Added At"]
                st.dataframe(df_crs_dsp, use_container_width=True, hide_index=True)

                st.write("---")
                c_col1, c_col2 = st.columns(2)
                with c_col1:
                    with st.expander("✏️ Edit Course"):
                        crs_map = {f"Course #{c['course_id']} — {c['course_title']}": c for c in courses_list}
                        sel_crs_str = st.selectbox("Select Course to Edit", list(crs_map.keys()), key="edit_crs_sel")
                        target_c = crs_map[sel_crs_str]

                        ec_title = st.text_input("Course Title", value=target_c["course_title"], key="ec_title")
                        ec_plat = st.text_input("Platform", value=target_c["platform"], key="ec_plat")
                        ec_skill = st.text_input("Target Skill", value=target_c["target_skill"], key="ec_skill")
                        ec_diff = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"], key="ec_diff")
                        ec_dur = st.text_input("Duration", value=target_c["duration"], key="ec_dur")
                        ec_link = st.text_input("URL Link", value=target_c["link"], key="ec_link")

                        if st.button("Update Course", type="primary", key="btn_upd_crs"):
                            if update_admin_course(target_c["course_id"], ec_title, ec_plat, ec_skill, ec_diff, ec_dur, ec_link):
                                st.success("Course updated successfully!")
                                st.rerun()

                with c_col2:
                    with st.expander("🗑️ Delete Course"):
                        del_c_str = st.selectbox("Select Course to Remove", list(crs_map.keys()), key="del_crs_sel")
                        target_del_c = crs_map[del_c_str]
                        if st.button("Delete Course", key="btn_del_crs"):
                            if delete_admin_course(target_del_c["course_id"]):
                                st.success("Course removed.")
                                st.rerun()

            st.write("---")
            with st.expander("➕ Add New Recommended Course"):
                with st.form("add_course_form", clear_on_submit=True):
                    nc_title = st.text_input("Course Title *")
                    nc_plat = st.text_input("Platform (e.g. Coursera, Udemy, edX)")
                    nc_skill = st.text_input("Target Skill (e.g. PyTorch, Docker)")
                    nc_diff = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced"])
                    nc_dur = st.text_input("Duration", value="4 Weeks")
                    nc_link = st.text_input("Course Link URL", value="https://coursera.org")
                    submit_crs = st.form_submit_button("🚀 Add Course to Catalog")

                    if submit_crs and nc_title:
                        if add_admin_course(nc_title, nc_plat, nc_skill, nc_diff, nc_dur, nc_link):
                            st.success("New course added to recommended catalog!")
                            st.rerun()

        # --- CANDIDATE CERTIFICATIONS ---
        with cc_tab2:
            certs_list = get_admin_certificates_list()
            st.markdown(f"**Found {len(certs_list)} candidate uploaded certifications:**")
            if certs_list:
                df_certs = pd.DataFrame(certs_list)
                df_certs_dsp = df_certs[["cert_id", "candidate_name", "email", "cert_title", "issuer", "issue_date", "created_at"]]
                df_certs_dsp.columns = ["Cert ID", "Candidate", "Email", "Certification Title", "Issuing Org", "Issue Date", "Uploaded At"]
                st.dataframe(df_certs_dsp, use_container_width=True, hide_index=True)
            else:
                st.info("No candidate certifications recorded yet.")

    # =====================================================================
    # TAB 7: USER FEEDBACK MANAGEMENT (FEATURE 13)
    # =====================================================================
    with admin_tab7:
        st.subheader("💬 User Feedback Management")
        st.caption("Review feedback submitted by candidates, update resolution status, and submit administrative responses.")

        f_status_filter = st.selectbox("Filter Feedback by Status", ["All", "Open", "In Progress", "Resolved"], key="fb_st_flt")
        feedback_list = get_admin_feedback_list(status_filter=f_status_filter)

        st.markdown(f"**Found {len(feedback_list)} feedback entries:**")

        if feedback_list:
            df_fb = pd.DataFrame(feedback_list)
            df_fb_dsp = df_fb[["feedback_id", "candidate_name", "email", "category", "rating", "feedback_text", "status", "admin_response", "created_at"]]
            df_fb_dsp.columns = ["ID", "Candidate", "Email", "Category", "Rating ⭐", "Feedback Text", "Status", "Admin Response", "Submitted At"]
            st.dataframe(df_fb_dsp, use_container_width=True, hide_index=True)

            st.write("---")
            st.markdown("#### ⚡ Respond to Candidate Feedback")
            fb_map = {f"Feedback #{f['feedback_id']} — {f['candidate_name']} ({f['category']})": f for f in feedback_list}
            sel_fb_str = st.selectbox("Select Feedback Item", list(fb_map.keys()), key="fb_sel")
            target_fb = fb_map[sel_fb_str]

            st.info(f"**Candidate Comment:** \"{target_fb['feedback_text']}\"")
            new_fb_status = st.selectbox("Update Status", ["Open", "In Progress", "Resolved"], index=["open", "in progress", "resolved"].index(target_fb["status"].lower()) if target_fb["status"].lower() in ["open", "in progress", "resolved"] else 0, key="n_fb_st")
            new_admin_resp = st.text_area("Admin Response / Internal Note", value=target_fb["admin_response"] if target_fb["admin_response"] != "No response yet" else "", key="n_admin_resp")

            fb_col1, fb_col2 = st.columns(2)
            with fb_col1:
                if st.button("Save Feedback Status & Response", type="primary", key="btn_save_fb"):
                    if update_feedback_status(target_fb["feedback_id"], new_fb_status, new_admin_resp):
                        st.success(f"Feedback #{target_fb['feedback_id']} updated.")
                        st.rerun()

            with fb_col2:
                if st.button("Delete Feedback Entry", key="btn_del_fb"):
                    if delete_user_feedback(target_fb["feedback_id"]):
                        st.success("Feedback item deleted.")
                        st.rerun()
        else:
            st.info("No user feedback records matching criteria.")

        st.write("---")
        with st.expander("🧪 Test Feedback Submission Form (Demo Candidate)"):
            with st.form("test_fb_form", clear_on_submit=True):
                tf_cat = st.selectbox("Feedback Category", ["General UI", "Resume Parser", "ATS Analysis", "Job Matching", "Feature Request"])
                tf_rating = st.slider("Satisfaction Rating ⭐", 1, 5, 5)
                tf_text = st.text_area("Feedback Message", placeholder="The resume parser worked seamlessly with my PDF format...")
                sub_tf = st.form_submit_button("Submit Test Feedback")

                if sub_tf and tf_text:
                    if submit_user_feedback(1, tf_cat, tf_rating, tf_text):
                        st.success("Test feedback recorded successfully!")
                        st.rerun()

    # =====================================================================
    # TAB 8: SYSTEM / API MONITORING (FEATURE 15, 17, 19)
    # =====================================================================
    with admin_tab8:
        st.subheader("🖥️ System & API Infrastructure Monitoring")
        st.caption("Live operational status of MySQL/SQLite database engine, AI services, file storage, and platform uptime.")

        sys_metrics = get_system_health_metrics()

        s1, s2, s3, s4 = st.columns(4)
        with s1:
            st.metric("Database Engine", sys_metrics["db_engine"])
        with s2:
            st.metric("Database Status", sys_metrics["db_status"])
        with s3:
            st.metric("Query Latency", sys_metrics["query_latency_ms"])
        with s4:
            st.metric("Platform Uptime", sys_metrics["system_uptime"])

        st.write("---")
        st.markdown("#### 📦 File Storage & AI Engine Health")
        sf1, sf2, sf3 = st.columns(3)
        with sf1:
            st.metric("Upload Storage Used", sys_metrics["storage_usage"])
        with sf2:
            st.metric("AI Service Engine", sys_metrics["ai_service_status"])
        with sf3:
            st.metric("Total System Log Events", sys_metrics["total_logs"])

        st.write("---")
        st.markdown("#### 📜 System Activity Audit Timeline")
        timeline = get_user_activity_timeline(user_id=None, limit=30)
        if timeline:
            for ev in timeline:
                st.markdown(f"- 🕒 **[{ev['timestamp']}]** `{ev['action']}` — **{ev['full_name']}** ({ev['email']}): {ev['details']}")
        else:
            st.info("No system activity logs recorded yet.")

    # =====================================================================
    # TAB 9: SEARCH, FILTER & REPORT EXPORTS (FEATURE 16)
    # =====================================================================
    with admin_tab9:
        st.subheader("📥 Administrative Search & 1-Click CSV Report Exports")
        st.caption("Filter records and generate downloadable CSV reports for executive presentation and auditing.")

        rep_type = st.selectbox(
            "Select Administrative Dataset to Export",
            ["Users Directory", "Resumes Audit", "ATS Analyses", "Job Postings", "User Feedback", "Activity Audit Logs"],
            key="rep_type_sel"
        )

        df_report = generate_csv_report(rep_type)
        st.markdown(f"**Previewing {len(df_report)} rows for report '{rep_type}':**")
        st.dataframe(df_report, use_container_width=True, hide_index=True)

        csv_bytes = df_report.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=f"📥 Download {rep_type} Report (CSV)",
            data=csv_bytes,
            file_name=f"{rep_type.lower().replace(' ', '_')}_report.csv",
            mime="text/csv",
            type="primary"
        )

if __name__ == "__main__":
    render_admin_dashboard_page()
