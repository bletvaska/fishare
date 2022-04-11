import random

from faker import Faker
from sqlmodel import create_engine, Session

from fishare.models.file import File
from fishare.models.settings import settings


def populate_data(count: int = 10):
    engine = create_engine(settings.db_uri)

    faker = Faker()
    categories = ('audio', 'video', 'image', 'text')

    with Session(engine) as session:
        for _ in range(count):
            category = random.choice(categories)
            file = File(
                id=_,
                filename=faker.file_name(category=category),
                mime_type=faker.mime_type(category=category),
                size=random.randint(100, 100000000)
            )
            session.add(file)

        session.commit()
