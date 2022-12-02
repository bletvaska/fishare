import fastapi
from sqlmodel import Session

from fishare.dependencies import get_session, get_settings
from fishare.models.settings import Settings


router = fastapi.APIRouter()


def is_db_session(session: Session):
    return session is not None


def check_storage_state(settings: Settings):
    return settings.storage.exists() and settings.storage.is_dir()


@router.get("/healthz")
def healthcheck(
    session: Session = fastapi.Depends(get_session),
    settings: Settings = fastapi.Depends(get_settings),
):
    db_state = is_db_session(session)
    fs_state = check_storage_state(settings)

    return {
        "healthy": db_state and fs_state,
        "dbState": db_state,
        "fsState": fs_state
        }
