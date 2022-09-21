from pydantic import BaseModel, AnyHttpUrl

from fishare.models.file_details_out import FileDetailsOut


class Pager(BaseModel):
    results: list[FileDetailsOut] = []
    next: AnyHttpUrl = None
    first: AnyHttpUrl = None
    last: AnyHttpUrl = None
    previous: AnyHttpUrl = None
