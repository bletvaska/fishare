import fastapi
from fastapi import Depends
from sqlmodel import Session
from starlette.responses import JSONResponse

from fishare.dependencies import get_session, get_settings
from fishare.models.settings import Settings

router = fastapi.APIRouter()


def check_db_state(session: Session):
    return session is not None


def check_storage_state(settings: Settings):
    return settings.storage.exists() \
           and settings.storage.is_dir() \
           and settings.storage.owner() == 'mirek'


@router.get('/', status_code=200)
def check_health(settings: Settings = Depends(get_settings),
                 session: Session = Depends(get_session)):
    db_state = check_db_state(session)
    storage_state = check_storage_state(settings)
    conditions = [db_state, storage_state]

    if all(conditions) == True:
        status = 'healthy'
        status_code = 200
    else:
        status = 'unhealthy'
        status_code = 503

    return JSONResponse(
        status_code=status_code,
        content={
            'status': status,
            'dbState': db_state,
            'storageState': storage_state
        })
