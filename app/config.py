from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(alias="DATABASE_URL")

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )

@lru_cache
def get_settings():
    return Settings()
