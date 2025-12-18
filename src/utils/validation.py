import re
from typing import Optional
import html


def sanitize_input(input_str: str) -> str:
    """
    Sanitize input string to prevent injection attacks
    """
    if not input_str:
        return input_str

    # Remove potentially harmful patterns
    # This is a basic implementation - consider using a more robust library for production
    sanitized = input_str

    # Remove script tags and JavaScript
    sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
    sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r'vbscript:', '', sanitized, flags=re.IGNORECASE)

    # Remove event handlers
    sanitized = re.sub(r'on\w+\s*=\s*["\'][^"\']*["\']', '', sanitized, flags=re.IGNORECASE)

    # HTML encode potentially dangerous characters
    sanitized = html.escape(sanitized)

    return sanitized.strip()


def validate_url(url: str) -> bool:
    """
    Validate if a string is a properly formatted URL
    """
    if not url:
        return False

    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return bool(url_pattern.match(url))


def validate_query_length(query: str, min_length: int = 1, max_length: int = 2000) -> bool:
    """
    Validate query length is within acceptable bounds
    """
    if not query:
        return False

    return min_length <= len(query) <= max_length


def validate_session_id(session_id: Optional[str]) -> bool:
    """
    Validate session ID format
    """
    if session_id is None:
        return True  # Optional field

    # Check if session_id contains only allowed characters
    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, session_id))


def validate_score_range(score: float, min_val: float = 0.0, max_val: float = 1.0) -> bool:
    """
    Validate that a score is within the expected range
    """
    return min_val <= score <= max_val


def is_safe_content(content: str) -> bool:
    """
    Check if content contains potentially harmful patterns
    """
    if not content:
        return True

    harmful_patterns = [
        r'<script',  # XSS attempts
        r'javascript:',  # JavaScript injection
        r'vbscript:',  # VBScript injection
        r'on\w+\s*=',  # Event handlers
        r'<iframe',  # Potential clickjacking
        r'<object',  # Potential malicious object inclusion
        r'<embed',  # Potential malicious embed
    ]

    for pattern in harmful_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return False

    return True