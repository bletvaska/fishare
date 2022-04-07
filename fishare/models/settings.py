from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    slug_length = 5
    base_url: AnyHttpUrl = 'http://localhost:9000'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        env_prefix = 'fishare_'
