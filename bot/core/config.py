"""
Bot configuration loaded from environment variables.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str = ""
    BACKEND_URL: str = "http://localhost:8000"

    class Config:
        env_file = ".env"
        extra = "ignore"


config = Settings()
