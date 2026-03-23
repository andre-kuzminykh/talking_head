"""
Application configuration loaded from environment variables.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "talking_head"

    HEDRA_API_KEY: str = ""
    HEDRA_API_URL: str = "https://mercury.dev.dream-ai.com/api"

    TTS_API_URL: str = ""
    TTS_VOICE: str = "Andre AIT eng"

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"
        extra = "ignore"


config = Settings()
