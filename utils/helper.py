import re

def is_valid_email(email: str) -> bool:
    """Validates email format using regex."""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def is_strong_password(password: str) -> tuple[bool, str]:
    """
    Validates password strength:
    - Minimum 6 characters
    - At least 1 letter and 1 number
    """
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one letter."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit."
    return True, "Strong password."

def format_currency_lpa(amount: float) -> str:
    """Formats LPA salary string."""
    return f"₹{amount:.2f} LPA"

def clean_text(text: str) -> str:
    """Removes extra spaces and linebreaks."""
    if not text:
        return ""
    return re.sub(r'\s+', ' ', text).strip()
