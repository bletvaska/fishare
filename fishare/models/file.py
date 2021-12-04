import secrets
from datetime import datetime
from typing import Optional

from pydantic import validator
from sqlmodel import SQLModel, Field

from fishare.models.settings import Settings

settings = Settings()


class File(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = secrets.token_urlsafe(settings.slug_length)
    filename: str
    downloads: int = 0
    max_downloads: int = 1
    size: int
    mime_type: str
    created: datetime = None

    @validator('created', pre=True, always=True)
    def set_created_now(cls, v):
        return v or datetime.now()

    def url(self):
        return f'{settings.base_url}/api/v1/files/{self.slug}'

    # print / str
    def __str__(self):
        return f'{self.filename} ({self.url()}) {self.size}B'

    # repr
    # def __repr__(self):
    #     pass
