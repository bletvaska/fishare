from pydantic import BaseModel


class ProblemDetails(BaseModel):
    type = "about:blank"
    title: str
    status: int | None
    detail: str | None
    instance: str | None
