from typing import List

from pydantic import BaseModel

from fishare.models.file import File, HttpUrl


class Pager(BaseModel):
    results: List[File] = []
    next: HttpUrl = None
    previous: HttpUrl = None
