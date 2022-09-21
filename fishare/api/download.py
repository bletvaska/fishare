import fastapi
from fastapi import Depends
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from starlette.requests import Request
from starlette.responses import JSONResponse

from fishare.database import get_session
from fishare.models.file_details import FileDetails
from fishare.models.problem_details import ProblemDetails

router = fastapi.APIRouter()


@router.get('/{slug}', summary='Download file by {slug}.')
def download_file(request: Request, slug: str,
                  session: Session = Depends(get_session)):
    try:
        # get file by slug
        statement = select(FileDetails).where(FileDetails.slug == slug)
        file = session.exec(statement).one()
    except NoResultFound as ex:
        problem = ProblemDetails(
            status=404,
            title='File not found',
            detail=f"File with slug '{slug}' does not exist.",
            instance=f'{request.url.path}'
        )

        return JSONResponse(
            status_code=problem.status,
            content=problem.dict(),
            media_type='application/problem+json'
        )
