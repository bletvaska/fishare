from datetime import datetime
import fastapi
from fastapi.responses import FileResponse
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound

from fishare.core import ProblemDetailsResponse
from fishare.dependencies import get_session, get_settings
from fishare.models.file_details import FileDetails
from fishare.models.problem_details import ProblemDetails
from fishare.models.settings import Settings


router = fastapi.APIRouter()


@router.get("/{slug}", status_code=200)
def download_file(
    slug: str,
    session: Session = fastapi.Depends(get_session),
    settings: Settings = fastapi.Depends(get_settings),
):
    try:
        # SELECT * FROM files WHERE slug=slug AND downloads < max_downloads AND now() < expires;
        statement = (
            select(FileDetails)
            .where(FileDetails.slug == slug)
            .where(FileDetails.downloads < FileDetails.max_downloads)
            .where(datetime.now() < FileDetails.expires)
        )

        # get file
        file = session.exec(statement).one()

        # update file downloads
        file.downloads += 1
        session.commit()
        session.refresh(file)

        # return file
        return FileResponse(
            settings.storage / file.slug,  # path
            filename=file.filename,  # filename
            media_type=file.mime_type  # mime-type / content-type
        )


    except NoResultFound as ex:
        problem = ProblemDetails(
            title="File not found",
            detail=f"File with slug '{slug}' was not found.",
            instance=f"/files/{slug}",
            status=404,
        )

        return ProblemDetailsResponse(
            status_code=problem.status, content=problem.dict()
        )
