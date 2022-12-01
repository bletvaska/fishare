from pydantic import AnyHttpUrl, BaseModel

from .file_details_out import FileDetailsOut


class Pager(BaseModel):
    count: int = 0
    next: AnyHttpUrl = None
    previous: AnyHttpUrl = None
    first: AnyHttpUrl = None
    last: AnyHttpUrl = None
    results: list[FileDetailsOut] = []
