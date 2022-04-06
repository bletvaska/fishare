from typing import Optional

from pydantic import BaseModel, FileUrl


class ProblemDetails(BaseModel):
    type = "about:blank"
    title: str
    status: Optional[int]
    detail: Optional[str]
    instance: Optional[str]
