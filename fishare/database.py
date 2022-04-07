from sqlmodel import Session, create_engine

from fishare.models.settings import Settings

settings = Settings()
engine = create_engine(settings.db_uri)


def get_session() -> Session:
    with Session(engine) as session:
        yield session
