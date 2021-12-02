from sqlmodel import create_engine

from models.settings import Settings

settings = Settings()

engine = create_engine(settings.db_uri, echo=False)
