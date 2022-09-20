from pydantic import BaseModel, validator, HttpUrl

from fishare.models.settings import Settings, get_settings


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
