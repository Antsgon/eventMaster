from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Lee las variables de entorno del archivo .env
    """
    database_url: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    """
    Devuelve la configuración (cacheada para no leer .env cada vez)
    """
    return Settings()