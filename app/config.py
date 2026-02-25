from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


def get_settings():
    settings = Settings()
    print("DATABASE_URL cargada:", settings.DATABASE_URL)
    return settings