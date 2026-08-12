import re
import logging

logger = logging.getLogger(__name__)

# Security configuration: Fields that must NEVER be selected or exposed in admin queries or tables
FORBIDDEN_EXPOSURE_FIELDS = {"password", "password_hash", "token", "secret_key"}

def sanitize_user_dict_for_admin(user_dict: dict) -> dict:
    """
    Guarantees that password, password_hash, or secret fields are scrubbed from dictionary
    before sending data to Admin Dashboard or frontend tables.
    """
    if not isinstance(user_dict, dict):
        return user_dict
    
    clean_dict = dict(user_dict)
    for field in FORBIDDEN_EXPOSURE_FIELDS:
        if field in clean_dict:
            del clean_dict[field]
    return clean_dict

def mask_sensitive_string(val: str, visible_chars: int = 3) -> str:
    """Masks email/phone strings for privacy if needed."""
    if not val or len(val) <= visible_chars * 2:
        return val
    return val[:visible_chars] + "*" * (len(val) - visible_chars * 2) + val[-visible_chars:]
