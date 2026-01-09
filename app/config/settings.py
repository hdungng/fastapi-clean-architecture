from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENV: str = "development"
    DATABASE_URL: str = "mysql+pymysql://root:123456789@127.0.0.1:3306/clean-arc-db"
    SECRET_KEY: str = "super-secret-dev-key-change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    LOG_LEVEL: str = "INFO"

    ENABLE_REFRESH_TOKEN: bool = True
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
