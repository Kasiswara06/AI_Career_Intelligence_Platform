import streamlit as st
import pandas as pd
from io import BytesIO
from services.report_service import export_analysis_report

def render_reports_page():
    st.header("📋 Comprehensive Reports & Export Center")
    st.caption("Generate, view, and download individual PDF or Excel reports for Resume Analysis, ATS Scoring, Job Matching, Skill Gap, Career Guidance, and Salary Predictions.")

    user_name = st.session_state.get("user_name", "Candidate")

    report_tabs = st.tabs([
        "📄 Resume Report",
        "🎯 ATS Report",
        "💼 Job Matching Report",
        "🧠 Skill Gap Report",
        "🚀 Career Recommendation Report",
        "💰 Salary Report",
        "📥 PDF & Excel Export"
    ])

    sample_summary = {
        "user_name": user_name,
        "ats_score": 85,
        "resume_score": 88,
        "skills": ["Python", "SQL", "Machine Learning", "Streamlit", "PyTorch", "Git"],
        "missing_skills": ["Docker", "Kubernetes", "AWS Cloud"],
        "target_role": "AI / ML Engineer",
        "predicted_salary": "$115,000 / yr"
    }

    with report_tabs[0]:
        st.subheader("📄 Resume Quality & Structure Report")
        st.write(f"**Candidate Name:** {user_name}")
        st.write("**Overall Quality Score:** 88 / 100")
        st.write("**Summary:** High technical competency in Python, SQL, and Machine Learning with clear project bullet points.")

    with report_tabs[1]:
        st.subheader("🎯 ATS Compatibility Report")
        st.write(f"**ATS Score:** {sample_summary['ats_score']}%")
        st.success("✔️ Passes standard ATS header, contact info, and font formatting checks.")
        st.warning("⚠️ Add explicit keywords for containerization (Docker) to reach 95%+ compatibility.")

    with report_tabs[2]:
        st.subheader("💼 Job Matching Audit Report")
        st.markdown("#### Top Matching Benchmark Jobs")
        job_data = [
            {"Job Title": "AI / ML Engineer", "Company": "TechCorp Labs", "Match Score": "92%", "Status": "Highly Recommended"},
            {"Job Title": "Senior Python Developer", "Company": "CloudScale Systems", "Match Score": "86%", "Status": "Eligible"},
            {"Job Title": "Data Scientist Lead", "Company": "DataMind Analytics", "Match Score": "80%", "Status": "Eligible"}
        ]
        st.table(pd.DataFrame(job_data))

    with report_tabs[3]:
        st.subheader("🧠 Skill Gap & Readiness Report")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Detected Skills (6)")
            for s in sample_summary["skills"]:
                st.success(f"✔️ {s}")
        with col2:
            st.markdown("#### Missing Skills (3)")
            for s in sample_summary["missing_skills"]:
                st.error(f"❌ {s}")

    with report_tabs[4]:
        st.subheader("🚀 Career Recommendation Report")
        st.write(f"**Predicted Career Path:** {sample_summary['target_role']}")
        st.write("**Industry Growth:** 35% YoY Growth Rate")
        st.write("**Career Readiness Score:** 88 / 100")

    with report_tabs[5]:
        st.subheader("💰 Salary Prediction Report")
        st.write("**Job Role:** AI / ML Engineer")
        st.write("**Experience Level:** 1.5 Years")
        st.write("**Estimated Salary Range:** $90,000 - $130,000 USD / yr")

    with report_tabs[6]:
        st.subheader("📥 Export Reports (PDF & Excel)")
        
        col_pdf, col_xls = st.columns(2)
        
        with col_pdf:
            st.markdown("#### 📄 Export PDF Report")
            if st.button("Generate & Download PDF Report", type="primary", use_container_width=True):
                with st.spinner("Compiling PDF report..."):
                    file_p = export_analysis_report(user_name, sample_summary, "pdf")
                    with open(file_p, "rb") as f:
                        st.download_button("Download PDF", f, file_name=f"{user_name}_Career_Report.pdf", mime="application/pdf", use_container_width=True)

        with col_xls:
            st.markdown("#### 📊 Export Excel Report")
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                pd.DataFrame([sample_summary]).to_excel(writer, sheet_name='Summary', index=False)
                pd.DataFrame(job_data).to_excel(writer, sheet_name='Jobs', index=False)
            excel_data = output.getvalue()
            
            st.download_button(
                label="Download Excel (.xlsx)",
                data=excel_data,
                file_name=f"{user_name}_Career_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

if __name__ == "__main__":
    render_reports_page()
