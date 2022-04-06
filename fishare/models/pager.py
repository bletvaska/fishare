from typing import List

from pydantic import BaseModel, AnyHttpUrl

from fishare.models.file import File


class Pager(BaseModel):
    results: List[File] = []
    next: AnyHttpUrl = None
    first: AnyHttpUrl = None
    last: AnyHttpUrl = None
    previous: AnyHttpUrl = None
