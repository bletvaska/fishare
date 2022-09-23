from functools import lru_cache

from sqlmodel import create_engine, Session
from starlette.templating import Jinja2Templates

from fishare.models.settings import Settings


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    print(f"Loading settings for {settings.environment} environment.")
    return settings


def get_session():
    engine = create_engine(get_settings().db_uri)

    with Session(engine) as session:
        yield session


@lru_cache
def get_jinja() -> Jinja2Templates:
    return Jinja2Templates(directory='fishare/templates/')
