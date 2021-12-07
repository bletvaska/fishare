import secrets
from datetime import datetime
from typing import Optional

from pydantic import validator, BaseModel, HttpUrl
from sqlmodel import SQLModel, Field

from fishare.models.settings import Settings

settings = Settings()


class File(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    slug: str = None
    filename: str
    downloads: int = 0
    max_downloads: int = 1
    size: int
    content_type: str
    created_at: datetime = None
    updated_at: datetime = None

    @validator('created_at', pre=True, always=True)
    def set_created_now(cls, v):
        return v or datetime.now()

    @validator('updated_at', pre=True, always=True)
    def set_updated_now(cls, v):
        return v or datetime.now()

    @validator('slug', pre=True, always=True)
    def set_secret_slug(cls, v):
        return v or secrets.token_urlsafe(settings.slug_length)


class FileOut(BaseModel):
    slug: str
    filename: str
    downloads: int
    max_downloads: int
    size: int
    content_type: str
    created_at: datetime
    updated_at: datetime
    url: HttpUrl = None

    @validator('url', always=True)
    def set_file_url(cls, v, values):
        return v or f'{settings.base_url}/{values["slug"]}'
