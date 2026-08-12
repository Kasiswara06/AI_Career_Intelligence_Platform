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
    get_detailed_user_inspector
)

def render_admin_dashboard_page():
    """Renders commercial-grade Admin Analytics & Platform Monitoring Dashboard."""
    
    # ----------------------------------------------------
    # RBAC AUTHORIZATION CHECK
    # ----------------------------------------------------
    if not check_admin_access():
        st.error("🚫 **Access Denied: Admin Privileges Required**")
        st.warning("You must be logged in with an administrator account (`role = 'admin'`) to access this page.")
        st.info("💡 **Demo Admin Access**: You can sign in using `admin@careerintel.ai` / `Admin@123456`.")
        return

    # Header Title Banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(30, 58, 138, 0.95), rgba(15, 23, 42, 0.95)); padding: 22px 28px; border-radius: 14px; border: 1px solid rgba(59, 130, 246, 0.3); margin-bottom: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style="margin: 0; color: #f8fafc; font-size: 2.1rem; display: flex; align-items: center; gap: 10px;">
                    🛡️ Admin Analytics & Platform Monitoring
                </h1>
                <p style="color: #93c5fd; margin-top: 6px; font-size: 1rem;">
                    MySQL Database Intelligence: Registered Candidates, Login History, Resume Processing, ATS Scans, Activity Logs, and Real-Time Timelines.
                </p>
            </div>
            <span style="background: rgba(16, 185, 129, 0.2); color: #34d399; border: 1px solid #10b981; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 0.9rem;">
                🟢 SECURE ADMIN SESSION
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # SECTION 1: TOP EXECUTIVE KPI CARDS (8 Metrics)
    # ----------------------------------------------------
    st.markdown("### 📌 Platform Usage Metrics & KPIs")
    metrics = get_admin_kpi_metrics()
    
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
    # SECTION 2: INTERACTIVE ANALYTICS CHARTS (Plotly)
    # ----------------------------------------------------
    st.markdown("### 📊 Application Usage Trends & Analytics")
    ch_col1, ch_col2 = st.columns(2)

    with ch_col1:
        st.markdown("#### 📈 Registration & Login Growth Trend")
        chart_df1 = pd.DataFrame({
            "Metric": ["Total Users", "Today's Users", "Total Logins", "Today's Logins", "Active Users"],
            "Count": [metrics["total_users"], metrics["today_users"], metrics["total_logins"], metrics["today_logins"], metrics["active_users"]]
        })
        fig1 = px.bar(chart_df1, x="Metric", y="Count", color="Metric", text_auto=True,
                      color_discrete_sequence=["#38bdf8", "#818cf8", "#c084fc", "#22c55e", "#facc15"])
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'), showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

    with ch_col2:
        st.markdown("#### 🎯 AI Activity Distribution")
        chart_df2 = pd.DataFrame({
            "Activity": ["Resume Uploads", "Resume Analyses", "Job Matches", "Active Users"],
            "Volume": [metrics["total_resumes"], metrics["total_analyses"], metrics["total_job_matches"], metrics["active_users"]]
        })
        fig2 = px.pie(chart_df2, values="Volume", names="Activity", color_discrete_sequence=["#38bdf8", "#818cf8", "#22c55e", "#facc15"])
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#ffffff'))
        st.plotly_chart(fig2, use_container_width=True)

    st.write("---")

    # ----------------------------------------------------
    # MAIN ADMIN TABS
    # ----------------------------------------------------
    admin_tab1, admin_tab2, admin_tab3, admin_tab4, admin_tab5 = st.tabs([
        "👥 Registered Users Table",
        "🔑 Login Activity Logs",
        "📄 Resume Upload & Analysis Logs",
        "📜 System Activity Timeline",
        "🔍 User Inspector & Analytics"
    ])

    # --- TAB 1: REGISTERED USERS TABLE ---
    with admin_tab1:
        st.subheader("👥 Candidate Users Directory")
        st.caption("SECURITY GUARANTEE: User passwords and password hashes are strictly excluded from all database queries and displays.")
        
        f_c1, f_c2, f_c3 = st.columns([3, 2, 2])
        with f_c1:
            search_query = st.text_input("🔍 Search User by Name or Email", placeholder="Type e.g. Rahul, candidate@example.com...")
        with f_c2:
            resume_filter = st.selectbox("📄 Filter by Resume Status", ["All", "With Active Resume", "No Resume"])
        with f_c3:
            role_filter = st.selectbox("🛡️ Filter by Role", ["All", "User", "Admin"])

        users_list = get_admin_users_list(search_query=search_query, resume_filter=resume_filter)
        if role_filter != "All":
            users_list = [u for u in users_list if u.get("role", "").lower() == role_filter.lower()]

        st.markdown(f"**Found {len(users_list)} registered users:**")

        if users_list:
            df_users = pd.DataFrame(users_list)
            # Re-order columns explicitly for clean display
            display_cols = ["user_id", "full_name", "email", "mobile", "role", "registered_date", "last_login", "login_count", "resume_status", "last_activity"]
            df_users = df_users[[c for c in display_cols if c in df_users.columns]]
            df_users.columns = ["ID", "Full Name", "Email", "Mobile", "Role", "Registered (Kolkata)", "Last Login", "Logins", "Resume", "Last Activity"]
            
            st.dataframe(df_users, use_container_width=True, hide_index=True)
        else:
            st.info("No candidate users found matching your search criteria.")

    # --- TAB 2: LOGIN ACTIVITY LOGS ---
    with admin_tab2:
        st.subheader("🔑 Login Activity Logs")
        st.caption("Real-time login history records stored in MySQL `login_activity` table.")
        
        login_logs = get_login_activity_logs(limit=40)
        if login_logs:
            df_logins = pd.DataFrame(login_logs)
            display_cols = ["login_id", "user_id", "full_name", "email", "login_time", "logout_time", "login_status", "session_id"]
            df_logins = df_logins[[c for c in display_cols if c in df_logins.columns]]
            df_logins.columns = ["Login ID", "User ID", "Candidate Name", "Email", "Login Time (Kolkata)", "Logout Time", "Status", "Session ID"]
            st.dataframe(df_logins, use_container_width=True, hide_index=True)
        else:
            st.info("No login records recorded yet.")

    # --- TAB 3: RESUME UPLOAD & ANALYSIS LOGS ---
    with admin_tab3:
        st.subheader("📄 Resume Upload & ATS Analysis Monitoring")
        st.caption("Tracks candidate resume upload, replacement, deletion, and automated ATS analysis events.")

        r_subtab1, r_subtab2 = st.tabs(["📊 Resume Analyses Audit", "📂 Resume File Events"])
        
        with r_subtab1:
            analysis_logs = get_resume_analysis_monitoring(limit=30)
            if analysis_logs:
                df_ans = pd.DataFrame(analysis_logs)
                df_ans = df_ans[["analysis_id", "user_id", "full_name", "email", "resume_name", "resume_score", "ats_score", "resume_quality", "analyzed_at"]]
                df_ans.columns = ["Analysis ID", "User ID", "Candidate", "Email", "Resume File", "Resume Score", "ATS Score", "Quality", "Analyzed At (Kolkata)"]
                st.dataframe(df_ans, use_container_width=True, hide_index=True)
            else:
                st.info("No resume analysis records available.")

        with r_subtab2:
            resume_events = get_resume_activity_logs(limit=30)
            if resume_events:
                df_ev = pd.DataFrame(resume_events)
                df_ev = df_ev[["log_id", "user_id", "full_name", "email", "action", "details", "timestamp"]]
                df_ev.columns = ["Log ID", "User ID", "Candidate", "Email", "Action", "Details", "Timestamp (Kolkata)"]
                st.dataframe(df_ev, use_container_width=True, hide_index=True)
            else:
                st.info("No resume activity events recorded.")

    # --- TAB 4: SYSTEM ACTIVITY TIMELINE ---
    with admin_tab4:
        st.subheader("📜 System-Wide Activity Timeline")
        st.caption("Chronological event log tracking candidate actions across all modules.")

        timeline = get_user_activity_timeline(user_id=None, limit=30)
        if timeline:
            for ev in timeline:
                st.markdown(f"- 🕒 **[{ev['timestamp']}]** `{ev['action']}` — **{ev['full_name']}** ({ev['email']}): {ev['details']}")
        else:
            st.info("No system activity logs recorded yet.")

    # --- TAB 5: USER INSPECTOR & ANALYTICS ---
    with admin_tab5:
        st.subheader("🔍 Individual Candidate Inspector")
        st.caption("Select a candidate to view their complete profile, resume status, activity timeline, and career intelligence metrics.")

        all_users = get_admin_users_list()
        user_options = {f"{u['full_name']} ({u['email']})": u['user_id'] for u in all_users if u.get("user_id")}

        if user_options:
            selected_user_str = st.selectbox("Select Candidate to Inspect", list(user_options.keys()))
            selected_uid = user_options[selected_user_str]
            
            inspector_data = get_detailed_user_inspector(selected_uid)
            
            if inspector_data:
                st.write("---")
                st.markdown(f"### 👤 Candidate: **{inspector_data['full_name']}** (ID: `{inspector_data['user_id']}`)")
                
                insp_col1, insp_col2 = st.columns(2)
                with insp_col1:
                    st.markdown("#### 📋 Profile & Contact Details")
                    st.write(f"**Email:** {inspector_data['email']}")
                    st.write(f"**Mobile:** {inspector_data['mobile']}")
                    st.write(f"**Role:** `{inspector_data['role']}`")
                    st.write(f"**Registration Date:** {inspector_data['registered_at']}")
                    
                    prof = inspector_data.get("profile", {})
                    st.write(f"**College:** {prof.get('college', 'N/A')}")
                    st.write(f"**Qualification:** {prof.get('qualification', 'N/A')} ({prof.get('branch', 'N/A')})")
                    st.write(f"**Experience:** {prof.get('experience_years', 0.0)} Years")

                with insp_col2:
                    st.markdown("#### 📄 Active Resume & AI Scores")
                    resumes = inspector_data.get("resumes", [])
                    if resumes:
                        active_r = next((r for r in resumes if r.get("is_active")), resumes[0])
                        st.success(f"**Active Resume:** `{active_r.get('filename')}`")
                        st.metric("Resume Score", f"{active_r.get('resume_score', 85)}/100")
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
                    st.info("No activity records for this candidate.")
        else:
            st.info("No candidate users available for inspection.")

if __name__ == "__main__":
    render_admin_dashboard_page()
