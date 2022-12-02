from datetime import datetime

import fastapi
from sqlmodel import Session, or_, select

from fishare.dependencies import get_session, get_settings
from fishare.models.file_details import FileDetails
from fishare.models.settings import Settings

router = fastapi.APIRouter()


@router.get("/cron/")
def cleanup(session: Session = fastapi.Depends(get_session),
            settings: Settings = fastapi.Depends(get_settings)):
    start = datetime.now()

    statement = select(FileDetails).where(
        or_(
            FileDetails.downloads >= FileDetails.max_downloads,
            FileDetails.expires < datetime.now(),
        )
    )

    files = session.exec(statement).all()

    # delete files
    for file in files:
        # delete file from storage
        path = settings.storage / file.slug
        path.unlink(missing_ok=True)

        # delete file in db
        session.delete(file)
        session.commit()

    end = datetime.now()
    duration = end - start

    return {
            'startedAt': start,
            'finishedAt': end,
            'duration': duration.total_seconds(),
            'removedFiles': len(files)
            }
