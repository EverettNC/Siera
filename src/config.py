"""Configuration management for SafeHaven AI"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support"""

    # Application
    app_name: str = "SafeHaven AI"
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "change-this-in-production"

    # Server
    host: str = "127.0.0.1"
    port: int = 8000

    # AI Provider Keys
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None

    # Database
    database_url: str = "sqlite+aiosqlite:///./safehaven.db"

    # Security
    session_expire_minutes: int = 60
    encryption_key: Optional[str] = None

    # Privacy Settings
    enable_logging: bool = False
    store_conversations: bool = False
    auto_delete_after_hours: int = 24

    # Emergency Services
    national_dv_hotline: str = "1-800-799-7233"
    crisis_text_line: str = "Text START to 741741"
    emergency_services: str = "911"

    # Feature Flags
    enable_voice_mode: bool = True
    enable_crisis_detection: bool = True
    enable_safety_planning: bool = True
    enable_resource_finder: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
