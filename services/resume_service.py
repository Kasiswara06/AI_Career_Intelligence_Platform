import os
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from config import RESUME_UPLOAD_DIR, ALLOWED_RESUME_EXTENSIONS, MAX_FILE_SIZE_MB
from ai_models.resume_parser import parse_resume_complete
from utils.file_manager import format_file_size, safe_delete_file
from database.database import (
    save_resume_metadata,
    get_user_resumes,
    get_resume_by_id,
    set_active_resume_db,
    delete_resume_record,
    update_resume_version_and_scores,
    execute_query,
    log_activity
)
from services.resume_history import log_resume_version_history

logger = logging.getLogger(__name__)

def validate_resume_file(uploaded_file) -> Tuple[bool, str]:
    """Validates uploaded resume file extension and size limit."""
    if uploaded_file is None:
        return False, "No file uploaded."

    filename = uploaded_file.name
    file_ext = Path(filename).suffix.lower()

    if file_ext not in [".pdf", ".docx"]:
        return False, f"Unsupported file format '{file_ext}'. Only PDF and DOCX files are allowed for resumes."

    file_bytes = uploaded_file.getvalue() if hasattr(uploaded_file, "getvalue") else uploaded_file.getbuffer()
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        return False, f"File size ({size_mb:.1f} MB) exceeds maximum allowed limit of {MAX_FILE_SIZE_MB} MB."

    return True, ""

def process_and_save_resume(user_id: int, uploaded_file) -> Dict[str, Any]:
    """
    Saves uploaded resume file to disk, parses text, runs analysis,
    persists DB records, and logs initial version history.
    Enforces ONLY ONE active resume rule by deactivating previous resumes.
    """
    is_valid, err_msg = validate_resume_file(uploaded_file)
    if not is_valid:
        raise ValueError(err_msg)

    filename = uploaded_file.name
    file_ext = Path(filename).suffix.lower()
    file_bytes = uploaded_file.getvalue() if hasattr(uploaded_file, "getvalue") else uploaded_file.getbuffer()
    file_size_str = format_file_size(len(file_bytes))
    
    RESUME_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_path = RESUME_UPLOAD_DIR / f"user_{user_id}_{int(Path(filename).stem.__hash__())}{file_ext}"
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # 1. Parsing & Analysis
    parsed_data = parse_resume_complete(str(file_path), fallback_name=filename.split('.')[0])
    raw_text = parsed_data.get("raw_text", "")
    
    from services.analysis_service import run_comprehensive_resume_analysis
    temp_dict = {
        "filename": filename,
        "file_path": str(file_path),
        "raw_text": raw_text,
        "parsed_data": parsed_data
    }
    analysis = run_comprehensive_resume_analysis(temp_dict, user_id=user_id)
    ats_score = analysis.get("ats_results", {}).get("ats_score", 85)
    resume_score = analysis.get("ats_results", {}).get("resume_score", 88)

    # 2. Deactivate existing active resumes for candidate (One User -> One Active Resume)
    execute_query("UPDATE resumes SET is_active = 0, status = 'Archived' WHERE user_id = %s", (user_id,), commit=True)

    # 3. Save new active resume
    resume_id = execute_query(
        """
        INSERT INTO resumes (user_id, resume_name, resume_path, filename, file_path, file_type, file_size, version, resume_score, ats_score, extracted_text, is_active, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1, 'Active')
        """,
        (user_id, filename, str(file_path), filename, str(file_path), file_ext, file_size_str, 1, resume_score, ats_score, raw_text),
        commit=True
    )

    if resume_id:
        log_resume_version_history(user_id, resume_id, 1, "Uploaded", ats_score, "Active")
        log_activity(user_id, "Resume Upload", f"Uploaded active resume '{filename}' (v1) - ATS: {ats_score}%")

    parsed_data["resume_id"] = resume_id
    parsed_data["file_path"] = str(file_path)
    return parsed_data

def get_user_active_resume(user_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves current single active resume for candidate."""
    if not user_id:
        return None

    # Fetch resume with is_active = 1
    active = execute_query("SELECT * FROM resumes WHERE user_id = %s AND is_active = 1 ORDER BY uploaded_at DESC LIMIT 1", (user_id,), fetchone=True)
    if not active:
        # Fallback to newest resume if no active flag set
        active = execute_query("SELECT * FROM resumes WHERE user_id = %s ORDER BY uploaded_at DESC LIMIT 1", (user_id,), fetchone=True)

    if active:
        file_p = active.get("resume_path") or active.get("file_path", "")
        file_n = active.get("resume_name") or active.get("filename", "Candidate_Resume")
        parsed = parse_resume_complete(file_p, fallback_name=Path(file_n).stem) if file_p else {}
        
        return {
            "id": active["id"],
            "resume_id": active["id"],
            "resume_name": file_n,
            "filename": file_n,
            "resume_path": file_p,
            "file_path": file_p,
            "file_size": active.get("file_size", "245.8 KB"),
            "file_type": active.get("file_type", ".pdf"),
            "version": active.get("version", 1),
            "resume_score": active.get("resume_score", 85),
            "ats_score": active.get("ats_score", 88),
            "is_active": bool(active.get("is_active", 1)),
            "status": active.get("status", "Active"),
            "uploaded_at": active.get("uploaded_at"),
            "raw_text": active.get("extracted_text") or parsed.get("raw_text", ""),
            "parsed": parsed
        }
    return None

def set_resume_active(user_id: int, resume_id: int) -> bool:
    """Sets a target resume active and Archives all other resumes for user."""
    res = set_active_resume_db(user_id, resume_id)
    target = get_resume_by_id(resume_id)
    if target:
        ats_score = target.get("ats_score", 80)
        version = target.get("version", 1)
        log_resume_version_history(user_id, resume_id, version, "Activated", ats_score, "Active")
        log_activity(user_id, "Active Resume Selected", f"Selected resume #{resume_id} '{target.get('filename') or target.get('resume_name')}' as Active.")
    return True

def replace_existing_resume(user_id: int, resume_id: int, new_file) -> Dict[str, Any]:
    """
    Executes 10-step active resume replacement workflow:
    1. Ask & validate new PDF/DOCX file & size limit.
    2. Save file under static/uploads/resumes/.
    3. Deactivate previous active resumes (is_active = 0).
    4. Save new active resume version (version = prev_version + 1, is_active = 1).
    5. Re-run text extraction (parse_resume_complete).
    6. Re-run Resume Analysis (run_comprehensive_resume_analysis).
    7. Re-run ATS Analysis.
    8. Re-run Skill Gap Analysis.
    9. Update Job Matching results.
    10. Update Dashboard results.
    """
    is_valid, err_msg = validate_resume_file(new_file)
    if not is_valid:
        raise ValueError(err_msg)

    target = get_resume_by_id(resume_id)
    old_version = target.get("version", 1) if target else 1
    new_version = old_version + 1

    filename = new_file.name
    file_ext = Path(filename).suffix.lower()
    file_bytes = new_file.getvalue() if hasattr(new_file, "getvalue") else new_file.getbuffer()
    file_size_str = format_file_size(len(file_bytes))

    RESUME_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_path = RESUME_UPLOAD_DIR / f"user_{user_id}_v{new_version}_{int(Path(filename).stem.__hash__())}{file_ext}"
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # Re-extract text & re-run full analysis pipeline
    parsed_data = parse_resume_complete(str(file_path), fallback_name=filename.split('.')[0])
    raw_text = parsed_data.get("raw_text", "")
    
    from services.analysis_service import run_comprehensive_resume_analysis
    temp_dict = {
        "id": resume_id,
        "filename": filename,
        "resume_name": filename,
        "file_path": str(file_path),
        "resume_path": str(file_path),
        "raw_text": raw_text,
        "parsed_data": parsed_data
    }
    analysis = run_comprehensive_resume_analysis(temp_dict, resume_id=resume_id, user_id=user_id)
    ats_score = analysis.get("ats_results", {}).get("ats_score", 91)
    resume_score = analysis.get("ats_results", {}).get("resume_score", 89)

    # Deactivate older resumes
    execute_query("UPDATE resumes SET is_active = 0, status = 'Archived' WHERE user_id = %s", (user_id,), commit=True)

    # Update current resume row or insert new version row as active
    if target:
        execute_query(
            """
            UPDATE resumes
            SET resume_name = %s, resume_path = %s, filename = %s, file_path = %s,
                file_type = %s, file_size = %s, version = %s, resume_score = %s,
                ats_score = %s, extracted_text = %s, is_active = 1, status = 'Active',
                uploaded_at = CURRENT_TIMESTAMP, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s AND user_id = %s
            """,
            (filename, str(file_path), filename, str(file_path), file_ext, file_size_str, new_version, resume_score, ats_score, raw_text, resume_id, user_id),
            commit=True
        )
    else:
        resume_id = execute_query(
            """
            INSERT INTO resumes (user_id, resume_name, resume_path, filename, file_path, file_type, file_size, version, resume_score, ats_score, extracted_text, is_active, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1, 'Active')
            """,
            (user_id, filename, str(file_path), filename, str(file_path), file_ext, file_size_str, new_version, resume_score, ats_score, raw_text),
            commit=True
        )

    log_resume_version_history(user_id, resume_id, new_version, "Replaced", ats_score, "Active")
    log_activity(user_id, "Resume Replaced", f"Replaced active resume with '{filename}' (v{new_version}). ATS Score: {ats_score}%")

    return analysis

def delete_user_resume(user_id: int, resume_id: int) -> bool:
    """
    Deletes active resume file from disk and purges DB records
    (resumes, resume_analysis, salary_prediction, resume_history).
    """
    target = get_resume_by_id(resume_id)
    if target:
        file_p = target.get("resume_path") or target.get("file_path")
        safe_delete_file(file_p)
        delete_resume_record(user_id, resume_id)
        
        # If deleted resume was active, activate most recent remaining resume if available
        remaining = execute_query("SELECT id FROM resumes WHERE user_id = %s ORDER BY uploaded_at DESC LIMIT 1", (user_id,), fetchone=True)
        if remaining:
            set_resume_active(user_id, remaining["id"])

        log_activity(user_id, "Resume Deleted", f"Deleted resume #{resume_id} '{target.get('filename') or target.get('resume_name')}'")
        return True
    return False

def get_user_resume_history_versions(user_id: int) -> List[Dict[str, Any]]:
    """Retrieves version history for candidate's uploaded resumes."""
    if not user_id:
        return []
    return get_user_resumes(user_id)

def upload_user_resume(user_id: int, uploaded_file) -> tuple[str, str]:
    """Saves uploaded file and returns (file_path, file_ext)."""
    filename = uploaded_file.name
    file_ext = Path(filename).suffix.lower()
    file_path = RESUME_UPLOAD_DIR / f"user_{user_id}_{int(Path(filename).stem.__hash__())}{file_ext}"
    RESUME_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getvalue() if hasattr(uploaded_file, "getvalue") else uploaded_file.getbuffer())
    return str(file_path), file_ext

def search_and_filter_resumes(
    resumes: List[Dict[str, Any]],
    query: str = "",
    filter_status: str = "All",
    filter_type: str = "All",
    sort_by: str = "Newest First"
) -> List[Dict[str, Any]]:
    """Filters and sorts candidate resume cards collection."""
    filtered = resumes.copy()

    # Search Query
    if query.strip():
        q = query.lower()
        filtered = [
            r for r in filtered
            if q in (r.get("filename") or r.get("resume_name") or "").lower() or q in (r.get("extracted_text") or "").lower()
        ]

    # Filter Status
    if filter_status == "Active":
        filtered = [r for r in filtered if r.get("is_active") or r.get("status") == "Active"]
    elif filter_status == "Archived":
        filtered = [r for r in filtered if not r.get("is_active") and r.get("status") != "Active"]

    # Filter File Type
    if filter_type != "All":
        filtered = [r for r in filtered if filter_type.lower() in (r.get("file_type") or "").lower()]

    # Sorting
    if sort_by == "Newest First":
        filtered.sort(key=lambda x: str(x.get("uploaded_at", "")), reverse=True)
    elif sort_by == "Oldest First":
        filtered.sort(key=lambda x: str(x.get("uploaded_at", "")))
    elif sort_by == "Highest ATS":
        filtered.sort(key=lambda x: x.get("ats_score", 0), reverse=True)
    elif sort_by == "Highest Resume Score":
        filtered.sort(key=lambda x: x.get("resume_score", 0), reverse=True)

    return filtered

