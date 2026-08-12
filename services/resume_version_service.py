import json
import logging
from database.database import execute_query

logger = logging.getLogger(__name__)

def create_resume_version(
    user_id: int,
    target_role: str,
    template_name: str,
    resume_content_dict: dict,
    ats_score: int = 85,
    pdf_path: str = "",
    docx_path: str = ""
) -> dict:
    """
    Creates a new resume version in resume_versions table and syncs with resume_builder table.
    """
    if not user_id:
        return {}

    # Get max version
    v_row = execute_query("SELECT MAX(version_id) as max_v FROM resume_versions WHERE user_id = %s", (user_id,), fetchone=True) or {}
    new_version_num = (v_row.get("max_v") or 0) + 1
    version_name = f"Resume Version {new_version_num} ({target_role})"

    content_json = json.dumps(resume_content_dict)

    # Insert into resume_versions
    v_id = execute_query(
        """
        INSERT INTO resume_versions
        (user_id, version_name, target_role, template, resume_content, summary, skills, education, experience, projects, certifications, achievements, ats_score, is_active, file_path_pdf, file_path_docx)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            user_id,
            version_name,
            target_role,
            template_name,
            content_json,
            resume_content_dict.get("summary", ""),
            resume_content_dict.get("skills", ""),
            resume_content_dict.get("education", ""),
            resume_content_dict.get("experience", ""),
            resume_content_dict.get("projects", ""),
            resume_content_dict.get("certifications", ""),
            resume_content_dict.get("achievements", ""),
            ats_score,
            False,
            pdf_path,
            docx_path
        ),
        commit=True
    )

    # Sync with resume_builder table for backwards compatibility
    execute_query(
        """
        INSERT INTO resume_builder
        (user_id, resume_version, target_role, template, summary, skills, education, experience, projects, certifications, achievements, ats_score, file_path_pdf, file_path_docx)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (
            user_id,
            new_version_num,
            target_role,
            template_name,
            resume_content_dict.get("summary", ""),
            resume_content_dict.get("skills", ""),
            resume_content_dict.get("education", ""),
            resume_content_dict.get("experience", ""),
            resume_content_dict.get("projects", ""),
            resume_content_dict.get("certifications", ""),
            resume_content_dict.get("achievements", ""),
            ats_score,
            pdf_path,
            docx_path
        ),
        commit=True
    )

    return {
        "version_id": v_id,
        "user_id": user_id,
        "version_name": version_name,
        "target_role": target_role,
        "template": template_name,
        "ats_score": ats_score,
        "file_path_pdf": pdf_path,
        "file_path_docx": docx_path
    }


def get_user_resume_versions(user_id: int) -> list:
    """
    Retrieves all resume versions saved for a user.
    """
    if not user_id:
        return []

    versions = execute_query(
        """
        SELECT version_id, user_id, version_name, target_role, template, resume_content, summary, skills, education, experience, projects, certifications, achievements, ats_score, is_active, file_path_pdf, file_path_docx, created_at
        FROM resume_versions
        WHERE user_id = %s
        ORDER BY version_id DESC
        """,
        (user_id,),
        fetchall=True
    ) or []

    if not versions:
        # Fallback to resume_builder table
        builder_rows = execute_query(
            """
            SELECT builder_id AS version_id, user_id, ('Resume Version ' || resume_version) AS version_name, target_role, template, summary, skills, education, experience, projects, certifications, achievements, ats_score, 0 AS is_active, file_path_pdf, file_path_docx, created_at
            FROM resume_builder
            WHERE user_id = %s
            ORDER BY builder_id DESC
            """,
            (user_id,),
            fetchall=True
        ) or []
        return builder_rows

    return versions


def set_active_resume_version(user_id: int, version_id: int) -> bool:
    """
    Sets a specific version as the active primary resume.
    """
    if not user_id or not version_id:
        return False

    execute_query("UPDATE resume_versions SET is_active = 0 WHERE user_id = %s", (user_id,), commit=True)
    execute_query("UPDATE resume_versions SET is_active = 1 WHERE version_id = %s AND user_id = %s", (version_id, user_id), commit=True)
    return True


def delete_resume_version(version_id: int, user_id: int) -> bool:
    """
    Deletes a saved resume version.
    """
    if not version_id:
        return False

    execute_query("DELETE FROM resume_versions WHERE version_id = %s AND user_id = %s", (version_id, user_id), commit=True)
    execute_query("DELETE FROM resume_builder WHERE builder_id = %s AND user_id = %s", (version_id, user_id), commit=True)
    return True
