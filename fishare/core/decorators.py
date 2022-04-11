from functools import wraps

from fastapi import Depends
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from fishare.core.responses import ProblemJSONResponse
from fishare.database import get_session
from fishare.models.file import File
from fishare.models.problem_details import ProblemDetails


def file_exists(func):
    @wraps(func)
    def wrapper(slug: str, session: Session = Depends(get_session), **kwargs):
        try:
            # get the file
            statement = select(File).where(File.slug == slug)
            file = session.exec(statement).one()

            # return func
            return func(slug, file, session)
        except NoResultFound as ex:
            content = ProblemDetails(
                type='/errors/files/get',
                title="File not found.",
                status=404,
                detail=f"File with slug '{slug}' was not found.'",
                instance=f"/files/{slug}"
            )

            return ProblemJSONResponse(
                status_code=content.status,
                content=content.dict(exclude_unset=True)
            )

    return wrapper
