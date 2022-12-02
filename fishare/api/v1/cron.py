from datetime import datetime

import fastapi
from sqlmodel import Session, or_, select

from fishare.dependencies import get_session
from fishare.models.file_details import FileDetails

router = fastapi.APIRouter()


@router.get("/cron/")
def cleanup(session: Session = fastapi.Depends(get_session)):
    statement = select(FileDetails).where(
        or_(
            FileDetails.downloads >= FileDetails.max_downloads,
            FileDetails.expires < datetime.now(),
        )
    )

    files = session.exec(statement).all()

    return files
