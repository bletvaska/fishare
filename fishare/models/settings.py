from pydantic import BaseSettings, AnyHttpUrl, validator


class Settings(BaseSettings):
    slug_length = 5
    port = 8000
    base_url: AnyHttpUrl = f'http://localhost:8000'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = 'fishare_'
