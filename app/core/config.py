from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = Field(default="BYLD Portfolio API", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    database_url: str | None = Field(default=None, alias="DATABASE_URL")


@lru_cache
def get_settings() -> Settings:
    return Settings()
