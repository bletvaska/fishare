from datetime import datetime
from pydantic import BaseModel, HttpUrl


class FileDetailsOut(BaseModel):
    slug: str
    max_downloads: 1
    url: HttpUrl = None
    expires: datetime | None = None
    created_at: datetime | None = None
