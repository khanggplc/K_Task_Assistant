from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Task Assistant"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    PORT: int = 8000
    HOST: str = "0.0.0.0"

    # Security
    SECRET_KEY: str = "temporary-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./data/assistant.db"

    # AI Configuration
    AI_PROVIDER: str = "openai"  # openai, gemini, ollama
    AI_API_KEY: Optional[str] = None
    AI_MODEL_NAME: str = "gpt-4o-mini"

    # Google Integrations
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"
    GOOGLE_PUBSUB_TOPIC: Optional[str] = None

    # Zalo Integrations
    ZALO_APP_ID: Optional[str] = None
    ZALO_APP_SECRET: Optional[str] = None
    ZALO_OA_SECRET_KEY: Optional[str] = None
    ZALO_WEBHOOK_SECRET: Optional[str] = None

    # Workers
    POLL_INTERVAL_SECONDS: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
