"""
Application Configuration Module for INTERVIEWX.
Loads environment variables safely using python-dotenv and Pydantic Settings.
Keeps API keys and sensitive settings out of source code.
"""

import os
from typing import List
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load .env file from the backend directory explicitly
backend_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(backend_env_path)
load_dotenv()  # Fallback to current working directory


class Settings(BaseSettings):
    APP_NAME: str = "INTERVIEWX – AI Interview Simulator"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # Allowed origins for CORS (React default Vite dev server is http://localhost:5173)
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"
    
    # SQLite local database file
    DATABASE_URL: str = "sqlite:///./interviewx.db"
    
    # Gemini LLM Settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "models/gemini-3.1-flash-lite")
    LLM_ENABLED: bool = bool(os.getenv("GEMINI_API_KEY"))

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# Global settings singleton
settings = Settings()
