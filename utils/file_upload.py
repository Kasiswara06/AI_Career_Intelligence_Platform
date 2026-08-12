import os
import shutil
from pathlib import Path
from config import RESUME_UPLOAD_DIR, CERT_UPLOAD_DIR, PROFILE_UPLOAD_DIR, MAX_FILE_SIZE_MB

ALLOWED_RESUME_FORMATS = [".pdf", ".docx"]
ALLOWED_CERT_FORMATS = [".pdf", ".jpg", ".jpeg", ".png"]
ALLOWED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png"]

def save_uploaded_file(uploaded_file, upload_type: str = "resume", user_id: int = 0) -> tuple[bool, str, str]:
    """
    Validates and saves an uploaded file to designated directory.
    Returns (success: bool, file_path_or_error: str, filename: str)
    """
    if uploaded_file is None:
        return False, "No file uploaded.", ""

    filename = uploaded_file.name
    file_ext = Path(filename).suffix.lower()

    # Determine destination directory & allowed extensions
    if upload_type == "resume":
        target_dir = RESUME_UPLOAD_DIR
        allowed = ALLOWED_RESUME_FORMATS
    elif upload_type == "certificate":
        target_dir = CERT_UPLOAD_DIR
        allowed = ALLOWED_CERT_FORMATS
    elif upload_type == "photo":
        target_dir = PROFILE_UPLOAD_DIR
        allowed = ALLOWED_IMAGE_FORMATS
    else:
        return False, "Invalid upload type specified.", ""

    # Validate extension
    if file_ext not in allowed:
        return False, f"Invalid file format '{file_ext}'. Allowed formats: {', '.join(allowed)}.", ""

    # Check size
    file_bytes = uploaded_file.getvalue() if hasattr(uploaded_file, "getvalue") else uploaded_file.getbuffer()
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        return False, f"File size ({size_mb:.1f} MB) exceeds maximum limit of {MAX_FILE_SIZE_MB} MB.", ""

    # Generate unique filename to avoid collision
    safe_filename = f"user_{user_id}_{int(Path(filename).stem.__hash__())}{file_ext}"
    target_dir.mkdir(parents=True, exist_ok=True)
    destination_path = target_dir / safe_filename

    try:
        with open(destination_path, "wb") as f:
            f.write(file_bytes)
        return True, str(destination_path), filename
    except Exception as e:
        return False, f"Failed to save file: {str(e)}", ""
