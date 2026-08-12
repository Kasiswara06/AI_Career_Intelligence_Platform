from dataclasses import dataclass
from typing import Optional

@dataclass
class Project:
    id: Optional[int]
    user_id: int
    project_name: str
    description: str
    technologies: Optional[str] = ""
    project_role: Optional[str] = ""
    start_date: Optional[str] = ""
    end_date: Optional[str] = ""
    github_url: Optional[str] = ""
    live_demo_url: Optional[str] = ""
    project_type: Optional[str] = "Web App"
    key_contributions: Optional[str] = ""
    project_outcome: Optional[str] = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
