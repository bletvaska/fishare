from pydantic import BaseModel, validator, HttpUrl


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
        return f'http://localhost:8000/{values["slug"]}'
