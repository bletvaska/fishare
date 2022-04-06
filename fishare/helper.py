import random

from faker import Faker

from fishare.models.file import File


def populate_data(count: int = 10):
    faker = Faker()
    categories = ('audio', 'video', 'image', 'text')
    files = []

    for _ in range(count):
        category = random.choice(categories)
        file = File(
            id=_,
            filename=faker.file_name(category=category),
            mime_type=faker.mime_type(category=category),
            size=random.randint(100, 100000000)
        )
        files.append(file)

    return files
