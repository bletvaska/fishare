from pydantic import BaseModel


class ProblemDetails(BaseModel):
    type = 'about:blank'
    title: str
    detail: str
    instance: str
    status: int
