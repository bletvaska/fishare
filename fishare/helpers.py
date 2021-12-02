from random import choice, randint
from models.file import File
from sqlmodel import SQLModel, Session
from faker import Faker

from database import engine


def create_tables():
    SQLModel.metadata.create_all(engine)


def populate_data():
    faker = Faker()

    categories = ('audio', 'video', 'image')

    category = choice(categories)

    file = File(
        filename=faker.file_name(category),
        size=randint(10, 1000000),
        mime_type=faker.mime_type(category)
    )

    print(repr(file))

    session = Session(engine)
    session.add(file)
    session.commit()


