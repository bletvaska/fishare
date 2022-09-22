from datetime import datetime

import fastapi
from fastapi import Depends
from sqlmodel import select, Session

from fishare.database import get_session
from fishare.models.file_details import FileDetails
from fishare.models.settings import Settings, get_settings

router = fastapi.APIRouter()


@router.get('/')
def cleanup(session: Session = Depends(get_session),
            settings: Settings = Depends(get_settings)):
    start = datetime.now()

    # SELECT * FROM filedetails WHERE downloads >= max_downloads
    statement = select(FileDetails) \
        .where(FileDetails.downloads >= FileDetails.max_downloads)
    files = session.exec(statement).all()

    # delete files
    for file in files:
        # delete file from storage
        path = settings.storage / file.slug
        path.unlink(missing_ok=True)

        # delete file from database
        session.delete(file)
        session.commit()

    # count duration
    end = datetime.now()
    duration = end - start

    return {
        'startedAt': start,
        'finishedAt': end,
        'duration': duration.total_seconds(),
        'removedFiles': len(files)
    }
