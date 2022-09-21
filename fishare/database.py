from sqlmodel import create_engine, Session

from fishare.models.settings import get_settings


def get_session():
    engine = create_engine(get_settings().db_uri)

    with Session(engine) as session:
        yield session
