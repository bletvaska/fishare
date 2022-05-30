from datetime import datetime

import fastapi
from fastapi import Depends
from sqlalchemy import or_
from sqlmodel import Session, select

from fishare.database import get_session
from fishare.models.file import File
from fishare.models.settings import get_settings

router = fastapi.APIRouter()


@router.get("/", summary="Run background jobs.")
def run_cron_job(session: Session = Depends(get_session)):
    start = datetime.now()

    # query
    statement = select(File).where(or_(datetime.now() > File.expires, File.downloads >= File.max_downloads))
    files = session.exec(statement).all()

    # delete files
    for file in files:
        # prepare path
        path = get_settings().storage / file.slug

        # delete file
        session.delete(file)
        session.commit()

        # delete file from storage
        path.unlink(missing_ok=True)

    # count duration
    end = datetime.now()
    duration = end - start

    return {
        'startedAt': start,
        'finishedAt': end,
        'removedFiles': len(files),
        'duration': duration.total_seconds()
    }
