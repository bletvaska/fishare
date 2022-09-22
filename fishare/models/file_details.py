import secrets
from datetime import datetime
from typing import Optional

from pydantic import validator
from sqlmodel import SQLModel, Field

from fishare.models.settings import get_settings


class FileDetails(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    slug: str | None = None
    filename: str
    downloads = 0
    max_downloads = 1
    size: int
    mime_type: str = 'application/octet-stream'
    created_at: datetime | None = None  # Optional[datetime] = None
    updated_at: datetime | None = None

    @validator('mime_type')
    def mime_type_must_contain_slash(cls, v):
        # print('>> validating mime_type')
        if '/' not in v:
            raise ValueError('must contain "/"')
        else:
            return v.lower()

    @validator('max_downloads')
    def must_be_positive_number(cls, v):
        # print('>> validating max_downloads')
        # print(v)
        if v < 1:
            # print('>> raising')
            raise ValueError('must be positive number greater than 0')
        else:
            return v

    @validator('created_at', always=True)
    def set_created_time(cls, v):
        return datetime.now()

    @validator('slug', always=True)
    def set_secret_slug(cls, v):
        return secrets.token_urlsafe(get_settings().slug_length)
