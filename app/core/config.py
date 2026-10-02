from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # ============================================================
    # DATABASE
    # ============================================================

    # Required.
    # No SQLite fallback.
    DATABASE_URL: str

    # ============================================================
    # JWT AUTHENTICATION
    # ============================================================

    SECRET_KEY: str

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080

    # ============================================================
    # GOOGLE OAUTH
    # ============================================================

    GOOGLE_CLIENT_ID: str

    GOOGLE_CLIENT_SECRET: str

    GOOGLE_REDIRECT_URI: str

    # ============================================================
    # FRONTEND
    # ============================================================

    FRONTEND_URL: str

    # ============================================================
    # AI APIs
    # ============================================================

    GEMINI_API_KEY: str = ""

    GROQ_API_KEY: str = ""

    # ============================================================
    # PYDANTIC SETTINGS
    # ============================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Create settings object
settings = Settings()