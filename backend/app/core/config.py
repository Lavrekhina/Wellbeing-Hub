from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables
    with support for a local .env file.

    Values can be overridden via environment variables in
    production environments.
    """

    # Human-readable application name (used in OpenAPI docs, etc.)
    app_name: str = "Wellbeing Hub API"

    # API version prefix for route grouping (e.g., /api/v1)
    api_v1_prefix: str = "/api"

    # Database connection string
    # Default uses local SQLite file for development
    # Should be overridden in production (e.g., PostgreSQL)
    database_url: str = "sqlite:///./wellbeing.db"

    # When true, use sklearn LogisticRegression trained on synthetic rule-labelled data.
    # When false or sklearn missing, rule-based scoring is used.
    use_ml_risk_scoring: bool = False

    # When true, GET /api/metrics/risk-classifier returns hold-out accuracy/F1 on synthetic data.
    expose_ml_risk_metrics: bool = False

    # When set (non-empty), /api/admin/* requires header X-Admin-Key with this value.
    admin_api_key: Optional[str] = None

    # Comma-separated browser origins allowed for CORS (e.g. Next.js dev server).
    cors_allow_origins: str = "http://localhost:3000"

    # deployment / ops (optional version string for readiness payloads and logs)
    environment: str = "development"
    app_version: str = ""

    # Pydantic settings configuration
    model_config = SettingsConfigDict(
        env_file=".env",              # Load environment variables from .env file
        env_file_encoding="utf-8",    # Encoding of the .env file
        case_sensitive=False,         # Environment variables are case-insensitive
    )

    def resolved_cors_origins(self) -> list[str]:
        parts = [p.strip() for p in self.cors_allow_origins.split(",")]
        origins = [p for p in parts if p]
        return origins if origins else ["http://localhost:3000"]


# Singleton settings instance used across the application
settings = Settings()