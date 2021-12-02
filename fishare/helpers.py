from models.file import File
from sqlmodel import SQLModel

from database import engine


def create_tables():
    SQLModel.metadata.create_all(engine)
