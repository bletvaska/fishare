from typing import List

from pydantic import BaseModel, HttpUrl

from fishare.models.file import File


class Pager(BaseModel):
    count: int = 0
    next: HttpUrl = None
    previous: HttpUrl = None
    results: List[File] = []
