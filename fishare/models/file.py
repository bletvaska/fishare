import secrets
from datetime import datetime, timedelta

from pydantic import BaseModel, validator, HttpUrl


class File(BaseModel):
    id: int = 0
    slug: str = None
    filename: str
    downloads = 0
    max_downloads = 1
    size: int
    mime_type: str
    created_at: datetime = None
    updated_at: datetime = None
    expires: datetime = None

    @validator('created_at', pre=True, always=True)
    def set_created_now(cls, value):
        return datetime.now()

    @validator('expires', always=True)
    def set_expires(cls, value):
        expiry = datetime.now() + timedelta(days=1)
        return expiry

    @validator('slug', always=True)
    def set_secret_slug(cls, value):
        return secrets.token_urlsafe(5)


class FileOut(BaseModel):
    slug: str
    filename: str
    downloads: int
    max_downloads: int
    size: int
    mime_type: str
    url: HttpUrl = None

    @validator('url', always=True)
    def set_file_url(cls, value, values):
        return f'http://localhost:9000/{values["slug"]}'
