import streamlit as st
from services.salary_service import run_ai_salary_prediction, compare_two_resumes_salary
from utils.resume_loader import load_active_or_uploaded_resume
from utils.charts import (
    create_salary_gauge,
    create_salary_prediction_chart,
    create_salary_comparison_chart,
    create_skill_impact_chart,
    create_exp_vs_salary_chart,
    create_market_salary_comparison_chart
)

def render_salary_prediction_page():
    """Renders the commercial-grade AI Resume-Based Salary Prediction Engine."""
    st.title("💰 AI Resume-Based Salary Prediction Engine")
    st.caption("Random Forest ML model predicting compensation based on candidate resume skills, education, experience, projects, and certifications.")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("🔒 Please log in to view Salary Predictions.")
        st.stop()

    # Session State Control for Mode & File Upload
    if "override_upload" not in st.session_state:
        st.session_state["override_upload"] = False
    if "comparison_result" not in st.session_state:
        st.session_state["comparison_result"] = None

    # Load Active Resume from Database
    active_resume_data = load_active_or_uploaded_resume(user_id=user_id)

    # ----------------------------------------------------
    # 1. RESUME DETECTION BANNER
    # ----------------------------------------------------
    if active_resume_data.get("has_resume") and not st.session_state["override_upload"]:
        st.markdown("### 🟢 Active Resume Detected")
        with st.container():
            banner_c1, banner_c2 = st.columns([3, 1])
            with banner_c1:
                st.write(f"📄 **Resume Name:** `{active_resume_data.get('filename')}`")
                st.write(f"📅 **Uploaded Date:** `{active_resume_data.get('uploaded_at')}`")
                st.write(f"📊 **Resume Score:** `{active_resume_data.get('resume_score')}%` &nbsp;|&nbsp; 🎯 **ATS Score:** `{active_resume_data.get('ats_score')}%`")
            with banner_c2:
                if st.button("🔄 Upload New Resume", use_container_width=True):
                    st.session_state["override_upload"] = True
                    st.rerun()

        uploaded_file = None
    else:
        st.markdown("### 📄 Upload Resume for Salary Prediction")
        if not active_resume_data.get("has_resume"):
            st.info("⚠️ **No Resume Found in Resume Management.** Please upload a resume below to generate an AI Salary Prediction.")
        
        uploaded_file = st.file_uploader(
            "Upload Resume (PDF or DOCX format)",
            type=["pdf", "docx"],
            help="Parses skills, education, experience, and projects automatically."
        )

        if st.session_state["override_upload"] and active_resume_data.get("has_resume"):
            if st.button("⬅️ Use Current Active Resume"):
                st.session_state["override_upload"] = False
                st.rerun()

    st.write("---")

    # ----------------------------------------------------
    # 2. RUN SALARY PREDICTION ENGINE
    # ----------------------------------------------------
    sal_result = run_ai_salary_prediction(user_id=user_id, uploaded_file=uploaded_file)

    if not sal_result.get("has_resume"):
        st.warning("Please upload a resume above to calculate expected compensation.")
        return

    features = sal_result["features"]
    prediction = sal_result["prediction"]
    res_info = sal_result["resume_info"]

    # ----------------------------------------------------
    # 3. KPI DASHBOARD CARDS
    # ----------------------------------------------------
    st.markdown("### 📊 AI Salary Dashboard & KPI Metrics")
    
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    with kpi1:
        st.metric("Resume Used", res_info.get("filename", "Resume")[:15])
    with kpi2:
        st.metric("Resume Score", f"{res_info.get('resume_score', 88)}%")
    with kpi3:
        st.metric("ATS Score", f"{res_info.get('ats_score', 90)}%")
    with kpi4:
        st.metric("Expected Salary", f"₹ {prediction['expected_lpa']} LPA")
    with kpi5:
        st.metric("Confidence Score", f"{prediction['confidence_score']}%")

    val1, val2, val3 = st.columns(3)
    with val1:
        st.success(f"💰 **Expected Range:** ₹ {prediction['min_lpa']} - {prediction['max_lpa']} LPA")
    with val2:
        st.info(f"💵 **USD Estimate:** ${prediction['min_salary_usd']:,} - ${prediction['max_salary_usd']:,} USD/yr")
    with val3:
        st.write(f"🏷️ **Experience Level:** **{prediction['experience_level']}**")

    st.write("---")

    # ----------------------------------------------------
    # 4. RESUME FEATURE EXTRACTION BREAKDOWN
    # ----------------------------------------------------
    st.markdown("### 🔍 Extracted Resume Features (Model Inputs)")
    
    feat_tab1, feat_tab2, feat_tab3, feat_tab4, feat_tab5 = st.tabs([
        "👤 Personal & Edu",
        "💼 Experience",
        "⚙️ Extracted Skills",
        "🏆 Certifications",
        "🚀 Projects Portfolio"
    ])

    with feat_tab1:
        p_det = features["personal_details"]
        edu_det = features["education"]
        st.write(f"**Name:** {p_det['name']} | **Email:** {p_det['email']}")
        st.write(f"**Degree:** {edu_det['degree']} ({edu_det['branch']})")
        st.write(f"**College:** {edu_det['college']} | **CGPA:** {edu_det['cgpa']}")

    with feat_tab2:
        exp_det = features["experience"]
        st.write(f"**Industry Experience:** {exp_det['years']} Years")
        st.write(f"**Current Role:** {exp_det['current_role']} at {exp_det['current_company']}")
        st.write(f"**Work History:** {', '.join(exp_det['companies'])}")

    with feat_tab3:
        st.markdown(" ".join([f"`{s}`" for s in features["skills"]]))

    with feat_tab4:
        for cert in features["certifications"]:
            st.write(f"- 🏆 {cert}")

    with feat_tab5:
        projs = features["projects"]
        st.markdown("**AI Projects:** " + ", ".join(projs["ai_projects"]))
        st.markdown("**ML Projects:** " + ", ".join(projs["ml_projects"]))
        st.markdown("**Web Projects:** " + ", ".join(projs["web_projects"]))

    st.write("---")

    # ----------------------------------------------------
    # 5. SALARY EXPLANATION & MISSING SKILLS
    # ----------------------------------------------------
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        st.markdown("### 💡 Why This Salary?")
        st.caption("Key positive contributing skills and qualifications boosting valuation:")
        for factor in prediction["why_salary_explanation"]:
            st.write(factor)

    with col_exp2:
        st.markdown("### ❌ Missing High-Value Skills")
        st.caption("Adding these high-demand skills can significantly increase your salary band:")
        for ms in prediction["missing_skills"]:
            st.markdown(f"- 🔴 `{ms}`")

    st.write("---")

    # ----------------------------------------------------
    # 6. SALARY IMPROVEMENT SUGGESTIONS & RECOMMENDATIONS
    # ----------------------------------------------------
    st.markdown("### 🚀 Salary Improvement Action Plan")
    imp_cols = st.columns(len(prediction["improvement_suggestions"]))
    for idx, imp in enumerate(prediction["improvement_suggestions"]):
        with imp_cols[idx]:
            st.markdown(f"#### 📈 Tip {idx+1}")
            st.write(f"**Action:** {imp['action']}")
            st.success(f"**Gain:** {imp['impact']}")

    st.write("---")
    
    rec_c1, rec_c2 = st.columns(2)
    with rec_c1:
        st.markdown("### 📚 Recommended Courses for Salary Boost")
        for c in prediction["recommended_courses"]:
            st.write(f"- 📖 [{c['title']}]({c['link']}) ({c['platform']} - {c['duration']})")

    with rec_c2:
        st.markdown("### 💼 Matching High-Paying Roles")
        for j in prediction["recommended_jobs"]:
            st.write(f"- 🎯 **{j['role']}** at {j['company']} ({j['salary_range']})")

    st.write("---")

    # ----------------------------------------------------
    # 7. COMPARE TWO RESUMES MODE
    # ----------------------------------------------------
    st.markdown("### ⚖️ Compare Two Resumes (Current vs New Resume)")
    st.caption("Upload a revised or alternative resume to compare expected salary valuations side-by-side.")

    comp_file = st.file_uploader("Upload Second Resume to Compare", type=["pdf", "docx"], key="comp_resume_uploader")
    if comp_file is not None:
        if st.button("⚖️ Run Resume Salary Comparison"):
            st.session_state["comparison_result"] = compare_two_resumes_salary(
                user_id=user_id,
                current_resume_info=res_info,
                new_file=comp_file
            )

    if st.session_state["comparison_result"] is not None:
        c_res = st.session_state["comparison_result"]
        st.success(f"### 🎉 Salary Improvement: +{c_res['percentage_improvement']}% Gain! (₹ +{c_res['diff_lpa']} LPA)")
        
        cmp1, cmp2 = st.columns(2)
        with cmp1:
            st.info(f"📄 **Old Resume (`{c_res['old_resume_name']}`):**\n### ₹ {c_res['old_lpa']} LPA")
        with cmp2:
            st.success(f"📄 **New Resume (`{c_res['new_resume_name']}`):**\n### ₹ {c_res['new_lpa']} LPA")

        st.plotly_chart(create_salary_comparison_chart(c_res['old_lpa'], c_res['new_lpa']), use_container_width=True)

    st.write("---")

    # ----------------------------------------------------
    # 8. INTERACTIVE PLOTLY CHARTS (6 CHARTS)
    # ----------------------------------------------------
    st.markdown("### 📈 Interactive AI Salary Analytics & Charts")

    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        st.plotly_chart(create_salary_gauge(prediction["expected_lpa"]), use_container_width=True)
    with row1_c2:
        st.plotly_chart(create_salary_prediction_chart(features["experience"]["years"], prediction["expected_lpa"]), use_container_width=True)

    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        st.plotly_chart(create_skill_impact_chart(prediction["skill_impacts"]), use_container_width=True)
    with row2_c2:
        st.plotly_chart(create_exp_vs_salary_chart(features["experience"]["years"], prediction["expected_lpa"]), use_container_width=True)

    st.plotly_chart(create_market_salary_comparison_chart(prediction["expected_lpa"]), use_container_width=True)

if __name__ == "__main__":
    render_salary_prediction_page()
