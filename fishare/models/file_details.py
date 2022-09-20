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
        if '/' not in v:
            raise ValueError('must contain "/"')
        else:
            return v.lower()
