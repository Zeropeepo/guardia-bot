import re

def sanitize_input(text: str) -> str:
    """
    Strips control characters and limits the length of the input.
    """
    if not text:
        return ""
    # Remove non-printable characters (keep newlines and tabs)
    sanitized = re.sub(r'[^\x20-\x7E\n\t\r]', '', text)
    # Truncate to reasonable max length (e.g., 2000 characters)
    return sanitized[:2000].strip()

def detect_injection(text: str) -> bool:
    """
    Basic pattern matching for known prompt injection patterns.
    Returns True if an injection attempt is detected.
    """
    text_lower = text.lower()
    
    suspicious_patterns = [
        "ignore previous",
        "ignore all previous",
        "system prompt",
        "you are now",
        "forget everything",
        "bypass",
        "translate the following into", # often used to bypass filters
        "new instructions",
    ]
    
    for pattern in suspicious_patterns:
        if pattern in text_lower:
            return True
            
    return False
