from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    environment = "production"
    slug_length = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "fishare_"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.environment}.")
    return settings


# FISHARE_ENVIRONMENT='devel' python -m fishare.main
# .env
# FISHARE_SLUG_LENGTH=10
