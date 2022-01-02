import fastapi
from fastapi import Request, Depends
from sqlmodel import select, Session
from starlette.responses import JSONResponse

from fishare.database import get_session
from fishare.models.file import File
from fishare.models.settings import Settings

router = fastapi.APIRouter()
settings = Settings()


@router.get('/cron')
def run_cron(request: Request, session: Session = Depends(get_session)):
    # chceme zmazat vsetky subory, ktorych downloads >= maxDownloads
    statement = select(File)
    files = session.exec(statement).all()

    for file in files:
        # remove file
        if file.downloads >= file.max_downloads:
            print(f'>> Removing file "{file.filename}" with slug "{file.slug}".')
            # zmaze zo storage-u
            path = settings.storage / file.slug
            path.unlink(True)

            # zmaze z databazy
            session.delete(file)
            session.commit()

    return JSONResponse(status_code=200, content={})
