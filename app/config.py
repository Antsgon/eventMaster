import os
from functools import lru_cache


class Settings:
    def __init__(self):
        self.database_url = os.environ.get("DATABASE_URL")

        if not self.database_url:
            raise ValueError("DATABASE_URL no está configurada")


@lru_cache
def get_settings():
    return Settings()