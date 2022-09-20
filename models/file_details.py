from datetime import datetime

from pydantic import BaseModel


class FileDetails(BaseModel):
    id: int
    slug: str
    filename: str
    downloads = 0
    max_downloads = 1
    size: int
    mime_type: str
    created_at: datetime | None = None  # Optional[datetime] = None
    updated_at: datetime | None = None
