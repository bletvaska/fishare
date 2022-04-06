from datetime import datetime

from pydantic import BaseModel


class File(BaseModel):
    # id: int
    slug: str = None
    filename: str
    downloads = 0
    max_downloads = 1
    size: int
    mime_type: str
    created_at: datetime = None
    updated_at: datetime = None
    # expires: datetime # od uploadu +24 hodin
