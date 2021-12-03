from pathlib import Path

from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    base_url: AnyHttpUrl = 'http://localhost:8080'
    slug_length: int = 5
    db_uri: str = 'sqlite:///default.db'
    storage: Path = 'storage'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'