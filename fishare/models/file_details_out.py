from datetime import datetime
from pydantic import BaseModel, HttpUrl, validator

from fishare.dependencies import get_settings


class FileDetailsOut(BaseModel):
    slug: str
    max_downloads = 1
    url: HttpUrl = None
    expires: datetime | None = None
    created_at: datetime | None = None

    @validator('url', always=True)
    def set_url_for_download(cls, value, values):
        slug = values['slug']
        return f'{get_settings().base_url}/{slug}'
