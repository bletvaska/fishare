from sqlmodel import Session, create_engine

from fishare.models.settings import get_settings

engine = create_engine(get_settings().db_uri)


def get_session() -> Session:
    with Session(engine) as session:
        yield session
