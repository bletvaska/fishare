from datetime import datetime

from pydantic import BaseModel, validator


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

    @validator('created_at', pre=True, always=True)
    def set_created_now(cls, value):
        return value or datetime.now()
