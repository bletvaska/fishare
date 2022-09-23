import fastapi
from fastapi import Depends
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from starlette.requests import Request
from starlette.responses import JSONResponse, FileResponse

from fishare.database import get_session
from fishare.decorators import log_client_ip
from fishare.models.file_details import FileDetails
from fishare.models.problem_details import ProblemDetails
from fishare.models.settings import get_settings, Settings

router = fastapi.APIRouter()


@router.head('/{slug}')
@router.get('/{slug}', status_code=200,
            summary='Download file by {slug}.')
@log_client_ip
async def download_file(request: Request, slug: str,
                        session: Session = Depends(get_session),
                        settings: Settings = Depends(get_settings)):
    print('>> downloading')
    try:
        # get file by slug
        # SELECT * FROM filedetails WHERE slug={slug} AND downloads < max_downloads
        statement = select(FileDetails) \
            .where(FileDetails.slug == slug) \
            .where(FileDetails.downloads < FileDetails.max_downloads)
        file = session.exec(statement).one()

        # update the number of downloads
        if request.method.upper() == 'GET':
            file.downloads += 1
            session.commit()
            session.refresh(file)

        # return file
        return FileResponse(
            settings.storage / file.slug,  # path
            media_type=file.mime_type,  # content-type
            filename=file.filename  # filename
        )

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
