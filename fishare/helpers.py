import random
from functools import lru_cache

from faker import Faker
from sqlmodel import create_engine, Session
from starlette.templating import Jinja2Templates

from fishare.models.file_details import FileDetails
from fishare.models.settings import get_settings


@lru_cache
def get_jinja() -> Jinja2Templates:
    return Jinja2Templates(directory='fishare/templates/')


def populate_data(count: int = 100):
    engine = create_engine(get_settings().db_uri)

    faker = Faker()
    categories = ('audio', 'video', 'image', 'text')

    with Session(engine) as session:
        for _ in range(count):
            category = random.choice(categories)
            file = FileDetails(
                filename=faker.file_name(category=category),
                mime_type=faker.mime_type(category=category),
                size=random.randint(100, 100000000)
            )
            session.add(file)

        session.commit()


if __name__ == '__main__':
    populate_data()
