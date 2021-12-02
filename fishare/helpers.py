from random import choice, randint
from sqlmodel import SQLModel, Session
from faker import Faker
from time import sleep
import secrets
from datetime import datetime

from fishare.models.file import File
from fishare.models.settings import Settings
from fishare.database import engine

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
                mime_type=faker.mime_type(category),
                slug=secrets.token_urlsafe(settings.slug_length),
                created = datetime.now()
            )

            # print(repr(file))

            session.add(file)
            session.commit()
            session.refresh(file)

            # sleep(0.5)
