import fastapi
from fastapi import Depends
from requests import Session
from sqlalchemy.exc import NoResultFound
from sqlmodel import select
from starlette.responses import JSONResponse, FileResponse

from fishare.database import get_session
from fishare.models.file import File
from fishare.models.problem_details import ProblemDetails
from fishare.models.settings import Settings

router = fastapi.APIRouter()
settings = Settings()


@router.head('/{slug}')
@router.get('/{slug}', summary="Download file by it's {slug}.")
def download_file(slug: str, session: Session = Depends(get_session)):
    try:
        # get file from db
        statement = select(File).where(File.slug == slug)
        file = session.exec(statement).one()

        # check downloads

        # increment download counter
        file.downloads += 1
        session.commit()
        session.refresh(file)

        return FileResponse(
            settings.storage / file.slug,  # path
            media_type=file.mime_type,     # content-type
            filename=file.filename         # filename
        )

    except NoResultFound as ex:
        content = ProblemDetails(
            type='/errors/files/download',
            title="File not found.",
            status=404,
            detail=f"File with slug '{slug}' was not found.'",
            instance=f"/{slug}"
        )

    return JSONResponse(
        status_code=content.status,
        content=content.dict(exclude_unset=True)
    )
