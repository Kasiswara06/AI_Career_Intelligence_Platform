import re
import logging
from typing import List, Dict, Any, Tuple
from database.database import (
    save_user_project,
    get_user_projects,
    get_project_by_id,
    update_user_project,
    delete_user_project,
    log_activity
)

logger = logging.getLogger(__name__)

URL_REGEX = re.compile(
    r'^(https?://)?'  # http:// or https://
    r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'  # domain...
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

def validate_project_data(data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validates project fields according to platform requirements."""
    project_name = data.get("project_name", "").strip()
    description = data.get("description", "").strip()
    github_url = data.get("github_url", "").strip()
    live_demo_url = data.get("live_demo_url", "").strip()

    if not project_name:
        return False, "Project Name is required."
    
    if not description:
        return False, "Project Description is required."

    if github_url and not validate_url(github_url):
        return False, "Invalid GitHub URL format."

    if live_demo_url and not validate_url(live_demo_url):
        return False, "Invalid Live Demo URL format."

    return True, ""

def create_project(user_id: int, project_data: Dict[str, Any]) -> Tuple[bool, str, int]:
    """Validates and creates a new project record for user."""
    is_valid, err_msg = validate_project_data(project_data)
    if not is_valid:
        return False, err_msg, 0

    project_id = save_user_project(user_id, project_data)
    if project_id:
        log_activity(user_id, "Add Project", f"Added project '{project_data.get('project_name')}'")
        return True, "Project added successfully!", project_id
    return False, "Failed to save project to database.", 0

def fetch_user_projects(user_id: int) -> List[Dict[str, Any]]:
    """Retrieves all projects for candidate."""
    if not user_id:
        return []
    return get_user_projects(user_id)

def fetch_project(project_id: int, user_id: int = None) -> Dict[str, Any]:
    """Retrieves single project details."""
    return get_project_by_id(project_id, user_id)

def edit_project(project_id: int, user_id: int, project_data: Dict[str, Any]) -> Tuple[bool, str]:
    """Validates and updates existing project record."""
    is_valid, err_msg = validate_project_data(project_data)
    if not is_valid:
        return False, err_msg

    success = update_user_project(project_id, user_id, project_data)
    if success:
        log_activity(user_id, "Edit Project", f"Updated project #{project_id} '{project_data.get('project_name')}'")
        return True, "Project updated successfully!"
    return False, "Failed to update project."

def remove_project(user_id: int, project_id: int) -> Tuple[bool, str]:
    """Deletes project record."""
    proj = get_project_by_id(project_id, user_id)
    proj_name = proj.get("project_name", f"#{project_id}")
    success = delete_user_project(user_id, project_id)
    if success:
        log_activity(user_id, "Delete Project", f"Deleted project '{proj_name}'")
        return True, "Project deleted successfully!"
    return False, "Failed to delete project."
