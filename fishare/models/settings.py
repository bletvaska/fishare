from functools import lru_cache

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    base_url: AnyHttpUrl = 'http://localhost:8000'
    port = 8000
    slug_length = 5
    environment = 'development'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = 'fishare_'


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for {settings.environment} environment.")
    return settings
