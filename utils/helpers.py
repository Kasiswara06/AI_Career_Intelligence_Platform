import re
from utils.helper import is_valid_email, is_strong_password, format_currency_lpa, clean_text

def format_file_size(size_in_bytes: int) -> str:
    """Formats file size in KB or MB."""
    if size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.1f} KB"
    return f"{size_in_bytes / (1024 * 1024):.2f} MB"

def sanitize_filename(filename: str) -> str:
    """Sanitizes filename for safe disk storage."""
    return re.sub(r'[^\w\.-]', '_', filename)
