from functools import lru_cache

from pydantic import BaseSettings, AnyHttpUrl, validator, DirectoryPath


class Settings(BaseSettings):
    slug_length = 5
    port = 8000
    base_url: AnyHttpUrl = f'http://localhost:8000'
    db_uri: str = 'sqlite:///database.db'
    storage: DirectoryPath = 'storage/'
    environment: str = 'development'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = 'fishare_'


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for {settings.environment} environment.")
    return settings
