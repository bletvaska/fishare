from functools import lru_cache

from sqlmodel import Session, create_engine

from fishare.models.settings import Settings


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for: {settings.environment}.")
    return settings


def get_session() -> Session:
    engine = create_engine(get_settings().db_uri)
    with Session(engine) as session:
        yield session
