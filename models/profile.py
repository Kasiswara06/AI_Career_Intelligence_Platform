from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class Profile:
    id: Optional[int]
    user_id: int
    date_of_birth: Optional[str] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = None
    college: Optional[str] = None
    university: Optional[str] = None
    qualification: Optional[str] = None
    branch: Optional[str] = None
    cgpa: Optional[float] = 0.0
    graduation_year: Optional[int] = None
    skills: List[str] = field(default_factory=list)
    technical_skills: List[str] = field(default_factory=list)
    soft_skills: List[str] = field(default_factory=list)
    experience_years: float = 0.0
    current_company: Optional[str] = None
    current_role: Optional[str] = None
    completion_percentage: int = 0
