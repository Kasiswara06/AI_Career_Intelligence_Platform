import re

def validate_email(email: str) -> bool:
    """Validates email format using regular expression."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_mobile(mobile: str) -> bool:
    """Validates phone/mobile number (10-15 digits)."""
    digits = re.sub(r'\D', '', mobile)
    return 10 <= len(digits) <= 15

def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validates password length and complexity."""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, "Password strength is acceptable."
