from datetime import datetime, timedelta
import secrets
from pydantic import BaseModel, HttpUrl, validator

from .settings import get_settings


settings = get_settings()

class File(BaseModel):
    # id: int
    slug: str | None = None
    filename: str
    url: HttpUrl | None = None
    expires: datetime | None = None
    downloads = 0
    max_downloads = 1
    size: int
    mime_type: str = 'application/octet-stream'
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @validator('mime_type')
    def mime_type_must_contain_slash(cls, v):
        if '/' not in v:
            raise ValueError('must contain "/"')
        else:
            return v.lower()

    @validator('created_at', always=True)
    def set_created_at_to_now(cls, v):
        return datetime.now()

    @validator('slug', always=True)
    def set_secret_slug(cls, v):
        return secrets.token_urlsafe(settings.slug_length)

    @validator('expires', always=True)
    def set_expiration_for_one_day(cls, v):
        return datetime.now() + timedelta(days=1)
