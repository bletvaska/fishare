import fastapi
from fastapi import Depends
from sqlmodel import select, Session

from fishare.database import get_session
from fishare.models.file_details import FileDetails

router = fastapi.APIRouter()


@router.get('/')
def cron_job(session: Session = Depends(get_session)):
    statement = select(FileDetails) \
        .where(FileDetails.downloads >= FileDetails.max_downloads)
    files = session.exec(statement).all()

    return files
