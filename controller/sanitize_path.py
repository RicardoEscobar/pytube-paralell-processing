"""This clears a string of characters that are not allowed in a file path."""
import re


def sanitize_path(path: str) -> str:
    """This clears a string of characters that are not allowed in a file path."""
    return re.sub(r'[<>:"/\\|?*]', "", path)
