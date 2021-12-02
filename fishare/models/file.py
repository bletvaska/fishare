import secrets
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from models.settings import Settings

settings = Settings()


class File(BaseModel):
    id: Optional[int]
    slug: str = secrets.token_urlsafe(settings.slug_length)
    filename: str
    downloads: int = 0
    max_downloads: int = 1
    size: int
    mime_type: str
    created: datetime = datetime.now()

    def url(self):
        return f'{settings.base_url}/api/v1/files/{self.slug}'

    # print / str
    def __str__(self):
        return f'{self.filename} ({self.url()}) {self.size}B'

    # repr
    # def __repr__(self):
    #     pass
