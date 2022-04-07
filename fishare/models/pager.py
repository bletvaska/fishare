from typing import List

from pydantic import BaseModel, AnyHttpUrl

from fishare.models.file import FileOut


class Pager(BaseModel):
    results: List[FileOut] = []
    next: AnyHttpUrl = None
    first: AnyHttpUrl = None
    last: AnyHttpUrl = None
    previous: AnyHttpUrl = None
    count: int
