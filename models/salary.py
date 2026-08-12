from dataclasses import dataclass
from typing import Optional

@dataclass
class SalaryEstimate:
    job_role: str
    experience_years: float
    predicted_min_salary: float
    predicted_max_salary: float
    predicted_avg_salary: float
    currency: str = "USD"
