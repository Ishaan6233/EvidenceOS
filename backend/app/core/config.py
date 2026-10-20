"""Read application settings from environment variables and optional `.env`.

The API and future worker use these settings to choose safe configuration. Keep
secret values out of source files and logs; `.env.example` contains placeholders.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EvidenceOS API"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"

    model_config = SettingsConfigDict(
        env_prefix="EVIDENCEOS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
