from datetime import datetime
from pydantic import BaseModel, HttpUrl


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
