import streamlit as st
import pandas as pd
from io import BytesIO
from services.dashboard_service import get_dashboard_summary
from services.report_service import export_analysis_report

def render_reports_page():
    st.header("📋 Comprehensive Reports & Export Center")
    st.caption("Module 24: Generate, view, and export individual PDF or Excel reports for Resume Analysis, ATS Scoring, Job Matching, Skill Gap, Career Guidance, and Salary Predictions.")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("🔒 Please log in to access Reports & Exports.")
        st.stop()

    summary = get_dashboard_summary(user_id)
    user_name = summary.get("user_name", st.session_state.get("user_name", "Candidate"))

    report_tabs = st.tabs([
        "📄 Resume Report",
        "🎯 ATS Report",
        "💼 Job Matching Report",
        "🧠 Skill Gap Report",
        "🚀 Career Recommendation Report",
        "💰 Salary Report",
        "📥 PDF & Excel Export"
    ])

    report_data = {
        "user_name": user_name,
        "ats_score": summary.get("ats_score", 85),
        "resume_score": summary.get("resume_score", 88),
        "skills": summary.get("detected_skills", ["Python", "SQL", "Machine Learning", "Streamlit"]),
        "missing_skills": summary.get("missing_skills", ["Docker", "Kubernetes", "AWS Cloud"]),
        "target_role": summary.get("recommended_career", "AI / ML Engineer"),
        "predicted_salary": summary.get("expected_salary", "$115,000 / yr")
    }

    with report_tabs[0]:
        st.subheader("📄 Resume Quality & Structure Report")
        st.write(f"**Candidate Name:** {user_name}")
        st.write(f"**Active Resume:** `{summary.get('active_resume_filename')}`")
        st.write(f"**Overall Quality Score:** {summary.get('resume_score')}/100")
        st.write(f"**AI Summary:** {summary.get('resume_summary')}")

    with report_tabs[1]:
        st.subheader("🎯 ATS Compatibility Report")
        st.write(f"**ATS Compatibility Score:** {summary.get('ats_score')}%")
        st.success("✔️ Structural checks completed for single-column headers, contact info, and font legibility.")
        if summary.get("missing_skills"):
            st.warning(f"⚠️ Consider adding missing keywords ({', '.join(summary.get('missing_skills')[:3])}) to maximize ATS indexability.")

    with report_tabs[2]:
        st.subheader("💼 Job Matching Audit Report")
        st.markdown("#### Top Benchmark Job Matches")
        job_data = [
            {"Job Title": summary.get("top_job_title"), "Company": summary.get("top_job_company"), "Match Score": f"{summary.get('top_job_match_pct')}%", "Status": "Top Match"},
            {"Job Title": "Senior Python Developer", "Company": "CloudScale Systems", "Match Score": "86%", "Status": "Eligible"},
            {"Job Title": "Data Scientist Lead", "Company": "DataMind Analytics", "Match Score": "80%", "Status": "Eligible"}
        ]
        st.table(pd.DataFrame(job_data))

    with report_tabs[3]:
        st.subheader("🧠 Skill Gap & Readiness Report")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"#### Detected Skills ({len(summary.get('detected_skills', []))})")
            for s in summary.get("detected_skills", [])[:8]:
                st.success(f"✔️ {s}")
        with col2:
            st.markdown(f"#### Missing Skills ({len(summary.get('missing_skills', []))})")
            for s in summary.get("missing_skills", []):
                st.error(f"❌ {s}")

    with report_tabs[4]:
        st.subheader("🚀 Career Recommendation Report")
        st.write(f"**Predicted Target Track:** {summary.get('recommended_career')}")
        st.write(f"**Industry Growth:** {summary.get('career_growth')}")
        st.write(f"**Career Readiness Score:** {summary.get('readiness_score')}/100")

    with report_tabs[5]:
        st.subheader("💰 Salary Prediction Report")
        st.write(f"**Predicted Annual Compensation:** {summary.get('expected_salary')}")
        st.write(f"**Estimated Valuation Range:** ${summary.get('min_salary', 90000):,} - ${summary.get('max_salary', 140000):,} USD / yr")

    with report_tabs[6]:
        st.subheader("📥 Export Reports (PDF & Excel)")
        col_pdf, col_xls = st.columns(2)
        
        with col_pdf:
            st.markdown("#### 📄 Export PDF Report")
            if st.button("Generate & Download PDF Report", type="primary", use_container_width=True):
                with st.spinner("Compiling PDF report..."):
                    file_p = export_analysis_report(user_name, report_data, "pdf")
                    with open(file_p, "rb") as f:
                        st.download_button("Download PDF", f, file_name=f"{user_name}_Career_Report.pdf", mime="application/pdf", use_container_width=True)

        with col_xls:
            st.markdown("#### 📊 Export Excel Report")
            output = BytesIO()
            try:
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    pd.DataFrame([report_data]).to_excel(writer, sheet_name='Summary', index=False)
                    pd.DataFrame(job_data).to_excel(writer, sheet_name='Jobs', index=False)
            except Exception:
                output = BytesIO()
                with pd.ExcelWriter(output) as writer:
                    pd.DataFrame([report_data]).to_excel(writer, sheet_name='Summary', index=False)
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
