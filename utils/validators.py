"""Input validation utilities."""
import re


def validate_api_key(api_key: str) -> bool:
    """Validate Gemini API key format.
    
    Args:
        api_key: API key string
        
    Returns:
        True if valid format, False otherwise
    """
    if not api_key or not api_key.strip():
        return False
    # Basic format check - Gemini API keys are typically alphanumeric and at least 20 characters
    # Adjust based on actual Gemini key format requirements
    cleaned_key = api_key.strip()
    return len(cleaned_key) > 10 and bool(re.match(r'^[A-Za-z0-9_-]+$', cleaned_key))


def validate_job_description(description: str) -> bool:
    """Validate job description input.
    
    Args:
        description: Job description text
        
    Returns:
        True if valid, False otherwise
    """
    if not description or not description.strip():
        return False
    # Minimum length check - job descriptions should be at least 50 characters
    return len(description.strip()) > 50
