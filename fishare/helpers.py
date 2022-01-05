import secrets
from random import choice, randint

from faker import Faker
from sqlmodel import SQLModel, Session

from fishare.database import engine
from fishare.models.file import File
from fishare.models.settings import Settings

settings = Settings()


def create_tables():
    """
    Creates empty tables based on loaded modules
    """
    SQLModel.metadata.create_all(engine)


def populate_data():
    """
    Populates data for testing purposes
    """
    faker = Faker()

    categories = ('audio', 'video', 'image', 'text')

    with Session(engine) as session:
        for _ in range(1000):
            category = choice(categories)

            file = File(
                filename=faker.file_name(category),
                size=randint(10, 1000000),
                content_type=faker.mime_type(category)
            )

            session.add(file)
            session.commit()
            session.refresh(file)

