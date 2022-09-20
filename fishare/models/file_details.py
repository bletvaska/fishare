import secrets
from datetime import datetime

from pydantic import BaseModel, validator


class FileDetails(BaseModel):
    # id: int
    slug: str | None = None
    filename: str
    downloads = 0
    max_downloads = 1
    size: int
    mime_type: str
    created_at: datetime | None = None  # Optional[datetime] = None
    updated_at: datetime | None = None

    @validator('mime_type')
    def mime_type_must_contain_slash(cls, v):
        # print('>> validating mime_type')
        if '/' not in v:
            raise ValueError('must contain "/"')
        else:
            return v.lower()

    @validator('created_at', always=True)
    def set_created_time(cls, v):
        # print('>> validating created_at')
        return datetime.now()

    @validator('slug', always=True)
    def set_secret_slug(cls, v):
        return secrets.token_urlsafe(5)
