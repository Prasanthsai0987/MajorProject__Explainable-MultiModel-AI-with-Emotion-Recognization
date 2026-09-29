from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Allow the app to start even when env vars are missing (local/dev).
    # Production should provide these via real env vars / .env.
    # Default to a local sqlite DB for local dev so the server can start.
    # (Production should override with a real DATABASE_URL.)
    DATABASE_URL: str = "sqlite:///./dev.db"
    SECRET_KEY: str = "dev-secret-key"

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days

    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDIRECT_URI: str = ""


    FRONTEND_URL: str = "http://localhost:5173"

    GEMINI_API_KEY: str = ""   # kept for reference
    GROQ_API_KEY:   str = ""   # used for ARIA chatbot

    class Config:
        env_file = ".env"

settings = Settings()