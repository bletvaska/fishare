from functools import lru_cache

from pydantic import BaseSettings, AnyHttpUrl, DirectoryPath


class Settings(BaseSettings):
    base_url: AnyHttpUrl = 'http://localhost:8000'
    port = 8000
    slug_length = 5
    environment = 'development'
    db_uri = 'sqlite:///database.db'
    storage: DirectoryPath = 'storage/'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = 'fishare_'
