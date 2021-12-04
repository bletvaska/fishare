from typing import Optional

from pydantic import BaseModel


class ProblemDetails(BaseModel):
    type: str = 'about:blank'
    title: str
    status: Optional[int]
    detail: Optional[str]
    instance: Optional[str]
