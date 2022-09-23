from pydantic import BaseModel, validator, HttpUrl

from fishare.dependencies import get_settings
from fishare.models.settings import Settings


class FileDetailsOut(BaseModel):
    slug: str
    filename: str
    downloads = 0
    max_downloads = 1
    size: int
    mime_type: str
    url: HttpUrl = None

    @validator('url', always=True)
    def set_file_details_url(cls, value, values):
        # print('>> validating url')
        # print(values)
        return f'{get_settings().base_url}/{values["slug"]}'
