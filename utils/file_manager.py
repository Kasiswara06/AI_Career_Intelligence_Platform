import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def format_file_size(size_in_bytes: int) -> str:
    """Formats byte count into human-readable KB or MB string."""
    if size_in_bytes < 1024:
        return f"{size_in_bytes} B"
    elif size_in_bytes < 1024 * 1024:
        return f"{round(size_in_bytes / 1024, 1)} KB"
    else:
        return f"{round(size_in_bytes / (1024 * 1024), 2)} MB"

def safe_delete_file(file_path: str) -> bool:
    """Safely removes file from local filesystem if it exists."""
    if not file_path:
        return False
    try:
        p = Path(file_path)
        if p.exists() and p.is_file():
            p.unlink()
            logger.info(f"Successfully deleted file: {file_path}")
            return True
    except Exception as e:
        logger.error(f"Error deleting file {file_path}: {e}")
    return False

def read_file_bytes(file_path: str) -> bytes:
    """Reads raw file bytes for browser downloading."""
    if not file_path:
        return b""
    try:
        p = Path(file_path)
        if p.exists() and p.is_file():
            with open(p, "rb") as f:
                return f.read()
    except Exception as e:
        logger.error(f"Error reading file bytes for {file_path}: {e}")
    return b""
