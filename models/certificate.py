from dataclasses import dataclass
from typing import Optional

@dataclass
class Certificate:
    id: Optional[int]
    user_id: int
    certificate_name: str
    issuing_organization: str
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None
    certificate_path: Optional[str] = None
    title: Optional[str] = None
    issuer: Optional[str] = None
    file_path: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
