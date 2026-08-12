import json
import logging
from database.database import execute_query
from ai_models.resume_builder import convert_profile_to_resume_dict
from ai_models.resume_summary_generator import generate_ai_professional_summary
from ai_models.ats_optimizer import evaluate_resume_ats_scores
from resume_builder.template_manager import render_resume_html_template
from resume_builder.resume_formatter import format_resume_as_plain_text
from services.resume_version_service import create_resume_version, get_user_resume_versions, delete_resume_version
from utils.resume_export import export_resume_all_formats

logger = logging.getLogger(__name__)

def generate_resume_from_profile(
    user_id: int,
    target_role: str = "AI Engineer",
    template_name: str = "Modern ATS",
    job_description: str = "",
    use_ai_summary: bool = True
) -> dict:
    """
    Primary Data Source resume generator (Section 1 & 2 requirement).
    Loads Profile data automatically, generates ATS optimized content, evaluates ATS scores,
    and persists version to resume_versions and resume_builder tables.
    """
    if not user_id:
        return {}

    # 1. Load Profile to Resume Dictionary
    res_dict = convert_profile_to_resume_dict(user_id, target_role=target_role)
    profile_raw = res_dict.get("profile_raw", {})

    # 2. AI Professional Summary Generation (Section 4 requirement)
    if use_ai_summary and profile_raw:
        ai_summary = generate_ai_professional_summary(profile_raw, target_role=target_role)
        if ai_summary:
            res_dict["summary"] = ai_summary

    # 3. Format full text
    full_text = format_resume_as_plain_text(res_dict)

    # 4. ATS Scoring & Optimization Analysis (Section 10 & 11 requirement)
    ats_eval = evaluate_resume_ats_scores(res_dict, full_text, target_role=target_role, job_description=job_description)
    ats_score = ats_eval.get("ats_score", 85)

    # 5. Render HTML preview template (Section 12 & 13 requirement)
    html_preview = render_resume_html_template(res_dict, template_name=template_name)

    # 6. Export PDF, DOCX, TXT files (Section 16 requirement)
    export_files = export_resume_all_formats(user_id, 1, res_dict)

    # 7. Save Resume Version (Section 17 & 18 requirement)
    v_res = create_resume_version(
        user_id=user_id,
        target_role=target_role,
        template_name=template_name,
        resume_content_dict=res_dict,
        ats_score=ats_score,
        pdf_path=export_files.get("pdf_path", ""),
        docx_path=export_files.get("docx_path", "")
    )

    return {
        "user_id": user_id,
        "resume_version": v_res.get("version_id", 1),
        "target_role": target_role,
        "template": template_name,
        "resume_dict": res_dict,
        "full_text": full_text,
        "html_preview": html_preview,
        "ats_evaluation": ats_eval,
        "export_files": export_files
    }


def get_user_saved_resumes(user_id: int) -> list:
    """Fetches all saved resume versions for a user."""
    return get_user_resume_versions(user_id)


def delete_user_resume_version(version_id: int, user_id: int = 1) -> bool:
    """Deletes a saved resume version."""
    return delete_resume_version(version_id, user_id)
