from pydantic import BaseSettings


class Settings(BaseSettings):
    environment = "production"
    db_uri: str = "sqlite:///db.sqlite"
    slug_length = 5

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "fishare_"


# FISHARE_ENVIRONMENT='devel' python -m fishare.main
# .env
# FISHARE_SLUG_LENGTH=10
