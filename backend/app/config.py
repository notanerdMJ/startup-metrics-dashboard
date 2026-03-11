# backend/app/config.py
"""
Application configuration.
Loads all settings from .env file using pydantic-settings.
This is the SINGLE SOURCE OF TRUTH for all config values.
"""

from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 1440  # 24 hours

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "mistral"

    # Dataset
    DATASET_PATH: str = "data/startup_data.csv"

    # App
    APP_NAME: str = "Startup Unit Economics Dashboard"
    DEBUG: bool = True
    CORS_ORIGINS: str = "http://localhost:3000"
    ENVIRONMENT: str = "development"

    @field_validator("DATABASE_URL")
    @classmethod
    def fix_postgres_url(cls, v: str) -> str:
        """
        Render provides postgres:// but SQLAlchemy 1.4+ requires postgresql://
        This fixes it automatically without breaking local dev.
        """
        if v and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton instance — import this everywhere
settings = Settings()