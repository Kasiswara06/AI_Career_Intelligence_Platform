import re
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple
from config import CERT_UPLOAD_DIR, ALLOWED_RESUME_EXTENSIONS, ALLOWED_IMAGE_EXTENSIONS
from utils.file_manager import safe_delete_file
from database.database import (
    save_user_certificate,
    get_user_certificates,
    get_certificate_by_id,
    update_user_certificate,
    delete_user_certificate,
    log_activity
)

logger = logging.getLogger(__name__)

ALLOWED_CERT_EXTENSIONS = [".pdf", ".jpg", ".jpeg", ".png"]

URL_REGEX = re.compile(
    r'^(https?://)?'
    r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'
    r'(:\d+)?(/.*)?$', re.IGNORECASE
)

def validate_url(url: str) -> bool:
    """Validates URL format if provided."""
    if not url or not url.strip():
        return True
    url_clean = url.strip()
    if not (url_clean.startswith("http://") or url_clean.startswith("https://")):
        url_clean = "https://" + url_clean
    return bool(URL_REGEX.match(url_clean))

def validate_certificate_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validates certificate metadata."""
    cert_name = data.get("certificate_name") or data.get("title", "")
    issuer = data.get("issuing_organization") or data.get("issuer", "")
    credential_url = data.get("credential_url", "")

    if not str(cert_name).strip():
        return False, "Certificate Name is required."

    if not str(issuer).strip():
        return False, "Issuing Organization is required."

    if credential_url and not validate_url(credential_url):
        return False, "Invalid Credential URL format."

    return True, ""

def create_certificate(user_id: int, cert_data: Dict[str, Any], file_obj=None) -> Tuple[bool, str, int]:
    """Validates and saves certificate metadata & optional file upload."""
    is_valid, err_msg = validate_certificate_data(cert_data)
    if not is_valid:
        return False, err_msg, 0

    file_path = ""
    if file_obj is not None:
        file_ext = Path(file_obj.name).suffix.lower()
        if file_ext not in ALLOWED_CERT_EXTENSIONS:
            return False, f"Unsupported file type '{file_ext}'. Allowed formats: PDF, JPG, JPEG, PNG.", 0

        CERT_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        safe_filename = f"cert_user_{user_id}_{int(Path(file_obj.name).stem.__hash__())}{file_ext}"
        destination_path = CERT_UPLOAD_DIR / safe_filename
        
        try:
            with open(destination_path, "wb") as f:
                f.write(file_obj.getbuffer() if hasattr(file_obj, "getbuffer") else file_obj.read())
            file_path = str(destination_path)
        except Exception as e:
            return False, f"Failed to save certificate file: {e}", 0

    cert_data["certificate_path"] = file_path
    cert_data["file_path"] = file_path

    cert_id = save_user_certificate(user_id, cert_data)
    if cert_id:
        log_activity(user_id, "Add Certificate", f"Added certificate '{cert_data.get('certificate_name') or cert_data.get('title')}'")
        return True, "Certificate added successfully!", cert_id
    return False, "Failed to save certificate record.", 0

def fetch_user_certificates(user_id: int) -> List[Dict[str, Any]]:
    """Retrieves all certificate records for user."""
    if not user_id:
        return []
    return get_user_certificates(user_id)

def fetch_certificate(cert_id: int, user_id: int = None) -> Dict[str, Any]:
    """Retrieves single certificate details."""
    return get_certificate_by_id(cert_id, user_id)

def edit_certificate(cert_id: int, user_id: int, cert_data: Dict[str, Any], new_file_obj=None) -> Tuple[bool, str]:
    """Updates certificate details and optionally replaces certificate file."""
    is_valid, err_msg = validate_certificate_data(cert_data)
    if not is_valid:
        return False, err_msg

    existing = get_certificate_by_id(cert_id, user_id)
    if not existing:
        return False, "Certificate not found."

    file_path = existing.get("certificate_path") or existing.get("file_path", "")

    if new_file_obj is not None:
        file_ext = Path(new_file_obj.name).suffix.lower()
        if file_ext not in ALLOWED_CERT_EXTENSIONS:
            return False, f"Unsupported file format '{file_ext}'. Allowed formats: PDF, JPG, JPEG, PNG."

        # Delete old file
        if file_path:
            safe_delete_file(file_path)

        CERT_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        safe_filename = f"cert_user_{user_id}_{int(Path(new_file_obj.name).stem.__hash__())}{file_ext}"
        destination_path = CERT_UPLOAD_DIR / safe_filename

        try:
            with open(destination_path, "wb") as f:
                f.write(new_file_obj.getbuffer() if hasattr(new_file_obj, "getbuffer") else new_file_obj.read())
            file_path = str(destination_path)
        except Exception as e:
            return False, f"Failed to save new certificate file: {e}"

    cert_data["certificate_path"] = file_path
    cert_data["file_path"] = file_path

    success = update_user_certificate(cert_id, user_id, cert_data)
    if success:
        log_activity(user_id, "Edit Certificate", f"Updated certificate #{cert_id}")
        return True, "Certificate updated successfully!"
    return False, "Failed to update certificate."

def remove_certificate(user_id: int, cert_id: int) -> Tuple[bool, str]:
    """Deletes certificate record and removes uploaded file from disk."""
    cert = get_certificate_by_id(cert_id, user_id)
    if not cert:
        return False, "Certificate not found."

    file_path = cert.get("certificate_path") or cert.get("file_path", "")
    if file_path:
        safe_delete_file(file_path)

    success = delete_user_certificate(user_id, cert_id)
    if success:
        cert_name = cert.get("certificate_name") or cert.get("title", f"#{cert_id}")
        log_activity(user_id, "Delete Certificate", f"Deleted certificate '{cert_name}'")
        return True, "Certificate deleted successfully!"
    return False, "Failed to delete certificate."
