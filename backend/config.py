import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration"""

    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = environment == "development"
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    # API
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    api_title: str = "AI Voice Receptionist API"
    api_version: str = "1.0.0"
    api_prefix: str = "/api/v1"

    # Database
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/business_assistant"
    )
    sqlalchemy_echo: bool = debug

    # Redis
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # JWT
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # OpenAI
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
    openai_voice_model: str = os.getenv("OPENAI_VOICE_MODEL", "tts-1-hd")

    # Twilio
    twilio_account_sid: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    twilio_auth_token: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    twilio_phone_number: str = os.getenv("TWILIO_PHONE_NUMBER", "")

    # Vapi
    vapi_api_key: str = os.getenv("VAPI_API_KEY", "")

    # Google Calendar
    google_client_id: str = os.getenv("GOOGLE_CLIENT_ID", "")
    google_client_secret: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
    google_calendar_api_key: str = os.getenv("GOOGLE_CALENDAR_API_KEY", "")

    # Outlook
    outlook_client_id: str = os.getenv("OUTLOOK_CLIENT_ID", "")
    outlook_client_secret: str = os.getenv("OUTLOOK_CLIENT_SECRET", "")

    # Integrations
    hubspot_api_key: str = os.getenv("HUBSPOT_API_KEY", "")
    zoho_client_id: str = os.getenv("ZOHO_CLIENT_ID", "")
    zoho_client_secret: str = os.getenv("ZOHO_CLIENT_SECRET", "")

    # Email
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_username: str = os.getenv("SMTP_USERNAME", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    smtp_from_email: str = os.getenv("SMTP_FROM_EMAIL", "noreply@businessassistant.com")

    # AWS S3
    aws_access_key_id: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    aws_secret_access_key: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    aws_s3_bucket_name: str = os.getenv("AWS_S3_BUCKET_NAME", "business-assistant-recordings")
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")

    # CORS
    allowed_origins: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
