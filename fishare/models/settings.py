from pathlib import Path

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    base_url: AnyHttpUrl = 'http://localhost:8080'
    slug_length: int = 5
    db_uri: str = 'sqlite:///data/default.db'
    storage: Path = 'data/storage'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
