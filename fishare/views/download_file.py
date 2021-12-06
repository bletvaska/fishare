import fastapi
from fastapi import Request
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from starlette.responses import FileResponse

from fishare.core.responses import ProblemJSONResponse
from fishare.database import engine
from fishare.models.file import File
from fishare.models.problem_details import ProblemDetails
from fishare.models.settings import Settings

router = fastapi.APIRouter()
settings = Settings()


@router.get('/{slug}')
def download_file(request: Request, slug: str):
    try:
        with Session(engine) as session:
            # selectnem subor z databazy
            statement = select(File).where(File.slug == slug)
            file = session.exec(statement).one()

            # ak sme prekrocili max downloads, tak ProblemJSONResponse
            if file.downloads >= file.max_downloads:
                content = ProblemDetails(
                    title='File not found.',
                    detail=f"No file with slug '{slug}'",
                    status=404,
                    instance=f'/files/{slug}'
                )

                return ProblemJSONResponse(
                    status_code=404,
                    content=content.dict(exclude_unset=True)
                )

            # downloads + 1
            file.downloads += 1
            session.commit()
            session.refresh(file)

            # vratim ho pouzivatelovi
            path = settings.storage / file.slug
            return FileResponse(path, media_type=file.content_type, filename=file.filename)
        
    except NoResultFound:
        # ak neexistuje taky subor, tak ProblemJSONResponse
        content = ProblemDetails(
            title='File not found.',
            detail=f"No file with slug '{slug}'",
            status=404,
            instance=f'/files/{slug}'
        )

        return ProblemJSONResponse(
            status_code=404,
            content=content.dict(exclude_unset=True)
        )

    return "hello world"
