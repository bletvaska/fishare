from sqlmodel import create_engine, Session

from fishare.models.settings import Settings

settings = Settings()
engine = create_engine(settings.db_uri, echo=False)


def get_session():
    with Session(engine) as session:
        yield session
