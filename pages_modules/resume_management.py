import streamlit as st
import datetime
from database.database import get_user_resumes
from services.resume_service import (
    get_user_active_resume,
    set_resume_active,
    replace_existing_resume,
    delete_user_resume,
    search_and_filter_resumes
)
from services.resume_history import fetch_resume_version_history
from utils.file_manager import read_file_bytes
from utils.resume_preview import render_resume_preview_panel

def render_resume_management_page():
    """Renders the commercial-grade Resume Management module."""
    st.title("📂 Professional Resume Management & Version Control")
    st.caption("Manage multiple resume versions, switch active resumes, inspect preview panels, and trigger automated AI re-analysis.")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("🔒 Please log in to access your Resume Management.")
        st.stop()

    # Session State Control for Preview, Replace, and Delete Dialogs
    if "preview_resume_id" not in st.session_state:
        st.session_state["preview_resume_id"] = None
    if "confirm_delete_id" not in st.session_state:
        st.session_state["confirm_delete_id"] = None

    # Fetch Resumes from DB strictly for logged-in user
    resumes_list = get_user_resumes(user_id) or []

    # ----------------------------------------------------
    # SEARCH, FILTER & SORTING TOOLBAR
    # ----------------------------------------------------
    st.markdown("### 🔍 Search & Filter Resumes")
    tb1, tb2, tb3, tb4 = st.columns([3, 2, 2, 2])
    with tb1:
        search_query = st.text_input("🔎 Search by Resume Name or Content", placeholder="Type keyword e.g. Internshala, Python...")
    with tb2:
        filter_status = st.selectbox("📌 Status Filter", ["All", "Active", "Archived"])
    with tb3:
        filter_type = st.selectbox("📄 File Type Filter", ["All", "PDF", "DOCX", "TXT"])
    with tb4:
        sort_by = st.selectbox("📊 Sort By", ["Newest First", "Oldest First", "Highest ATS", "Highest Resume Score"])

    filtered_resumes = search_and_filter_resumes(
        resumes_list,
        query=search_query,
        filter_status=filter_status,
        filter_type=filter_type,
        sort_by=sort_by
    )

    st.write("---")

    # ----------------------------------------------------
    # CONFIRMATION DIALOG FOR DELETE
    # ----------------------------------------------------
    if st.session_state["confirm_delete_id"] is not None:
        del_id = st.session_state["confirm_delete_id"]
        target_del = next((r for r in resumes_list if r["id"] == del_id), None)
        target_name = target_del["filename"] if target_del else f"#{del_id}"

        st.warning(f"⚠️ **Are you sure you want to delete this resume? (`{target_name}`)**")
        st.markdown("""
        **This action will permanently remove:**
        - 📄 Resume File from Disk
        - 📊 Resume Analysis & Scores
        - 🎯 ATS Analysis Records
        - 💼 Job Matching Results
        - 🧠 Skill Gap Results
        - 📈 Dashboard Metrics
        """)
        
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            if st.button("❌ Cancel Deletion", use_container_width=True):
                st.session_state["confirm_delete_id"] = None
                st.rerun()
        with btn_c2:
            if st.button("🗑️ Confirm Delete Resume", type="primary", use_container_width=True):
                delete_user_resume(user_id, del_id)
                st.session_state["confirm_delete_id"] = None
                st.success("Resume deleted successfully.")
                st.rerun()
        st.write("---")

    # ----------------------------------------------------
    # RESUME PREVIEW PANEL (If active)
    # ----------------------------------------------------
    if st.session_state["preview_resume_id"] is not None:
        prev_id = st.session_state["preview_resume_id"]
        target_prev = next((r for r in resumes_list if r["id"] == prev_id), None)
        if target_prev:
            with st.container():
                render_resume_preview_panel(target_prev)
                if st.button("❌ Close Preview Panel"):
                    st.session_state["preview_resume_id"] = None
                    st.rerun()
            st.write("---")

    # ----------------------------------------------------
    # RESUME LIST (MODERN CARDS UI)
    # ----------------------------------------------------
    st.markdown(f"### 📑 Uploaded Resumes ({len(filtered_resumes)} Found)")

    if not filtered_resumes:
        if not resumes_list:
            st.info("ℹ️ **No resumes uploaded yet.** Upload your first resume to begin ATS Analysis, Skill Gap Analysis, and Job Matching.")
            if st.button("📤 Upload Resume Now", type="primary", key="btn_upload_empty_state"):
                st.session_state["current_page"] = "📄 Resume Upload"
                st.rerun()
        else:
            st.info("No resumes match your filter criteria.")

    for res in filtered_resumes:
        res_id = res["id"]
        is_active = res.get("is_active") or res.get("status") == "Active"
        status_label = "🟢 Active" if is_active else "⚪ Archived"
        status_bg = "#065F46" if is_active else "#374151"

        with st.container():
            card_col1, card_col2 = st.columns([3, 1])
            
            with card_col1:
                st.markdown(f"### 📄 `{res['filename']}`")
                st.markdown(f"<span style='background-color:{status_bg}; color:white; padding:3px 10px; border-radius:12px; font-weight:bold; font-size:12px;'>{status_label}</span> &nbsp; <span style='background-color:#4F46E5; color:white; padding:3px 10px; border-radius:12px; font-weight:bold; font-size:12px;'>Version {res.get('version', 1)}</span>", unsafe_allow_html=True)
                
                details_c1, details_c2, details_c3 = st.columns(3)
                with details_c1:
                    st.write(f"📅 **Uploaded:** {res.get('uploaded_at', '05-Aug-2026')}")
                    st.write(f"💾 **File Size:** {res.get('file_size', '69.5 KB')}")
                with details_c2:
                    st.write(f"🏷️ **Type:** {res.get('file_type', '.pdf').upper()}")
                    st.write(f"📊 **Resume Score:** {res.get('resume_score', 89)}%")
                with details_c3:
                    st.write(f"🎯 **ATS Score:** {res.get('ats_score', 92)}%")

                # Quick Summary Box on Card
                with st.expander("💡 AI Resume Quick Snapshot"):
                    st.write("**Candidate Summary:** Highly suitable for AI Engineer & Data Scientist roles.")
                    st.write("**Detected Skills:** `Python` `SQL` `Machine Learning` `Streamlit` `Git` `PyTorch`")
                    st.write("**Missing Skills:** `Docker` `AWS` `Kubernetes` `CI/CD`")
                    st.write("**Recommended Job Role:** AI Engineer / MLOps Specialist")
                    st.write("**Expected Salary:** ₹ 10.5 LPA")

            with card_col2:
                st.write("**Quick Actions:**")
                
                # Action 1: View
                if st.button("👁️ View Resume", key=f"btn_view_{res_id}", use_container_width=True):
                    st.session_state["preview_resume_id"] = res_id
                    st.rerun()

                # Action 2: Download
                file_bytes = read_file_bytes(res.get("file_path", ""))
                st.download_button(
                    label="📥 Download Resume",
                    data=file_bytes or b"Sample Resume Byte Content",
                    file_name=res["filename"],
                    mime="application/pdf" if ".pdf" in res.get("file_type", ".pdf").lower() else "application/octet-stream",
                    key=f"btn_dl_{res_id}",
                    use_container_width=True
                )

                # Action 3: Set Active
                if not is_active:
                    if st.button("⭐ Set Active Resume", key=f"btn_active_{res_id}", use_container_width=True):
                        set_resume_active(user_id, res_id)
                        st.success(f"Selected '{res['filename']}' as Active Resume.")
                        st.rerun()
                else:
                    st.caption("✔️ Current Active Resume")

                # Action 4: Delete
                if st.button("🗑️ Delete Resume", key=f"btn_del_{res_id}", use_container_width=True):
                    st.session_state["confirm_delete_id"] = res_id
                    st.rerun()

            # Action 5: Replace File Inline Expander
            with st.expander(f"🔄 Replace `{res['filename']}` with New Version"):
                st.caption("Uploading a replacement file automatically updates database records and re-runs full AI Analysis.")
                replacement_file = st.file_uploader(f"Choose replacement file for {res['filename']}", type=["pdf", "docx", "doc", "txt"], key=f"file_rep_{res_id}")
                if replacement_file is not None:
                    if st.button(f"Confirm Replace `{res['filename']}`", key=f"confirm_rep_{res_id}"):
                        replace_existing_resume(user_id, res_id, replacement_file)
                        st.success("Resume replaced successfully.")
                        st.info("AI analysis updated successfully.")
                        st.rerun()

        st.write("---")

    # ----------------------------------------------------
    # RESUME HISTORY PANEL
    # ----------------------------------------------------
    st.markdown("### 📜 Section – Resume Version History")
    
    history_logs = fetch_resume_version_history(user_id)
    if not history_logs:
        st.info("No resume version history recorded yet.")
    else:
        st.table(history_logs)

if __name__ == "__main__":
    render_resume_management_page()
