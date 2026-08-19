"""Utility functions"""
import secrets
import uuid
from datetime import datetime
import phonenumbers
from phonenumbers import NumberParseException


def generate_api_key(prefix: str = "sk") -> tuple[str, str]:
    """Generate API key and secret"""
    key = f"{prefix}_{secrets.token_urlsafe(32)}"
    secret = secrets.token_urlsafe(64)
    return key, secret


def generate_call_id() -> str:
    """Generate unique call ID"""
    return f"call_{uuid.uuid4().hex[:12]}"


def format_phone_number(phone: str, region: str = "US") -> str:
    """Format phone number to E.164 format"""
    try:
        parsed = phonenumbers.parse(phone, region)
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except NumberParseException:
        return phone


def parse_datetime_safe(date_string: str) -> datetime:
    """Safely parse datetime string"""
    try:
        return datetime.fromisoformat(date_string)
    except (ValueError, TypeError):
        return datetime.utcnow()


def mask_sensitive_data(text: str, pattern: str = r"\d{4}[\d\-\s]{0,}(?=\d{4})") -> str:
    """Mask sensitive data like credit cards"""
    import re
    return re.sub(pattern, "****", text)
