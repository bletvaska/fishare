import fastapi
from starlette.responses import JSONResponse

from fishare.database import get_session
from fishare.models.settings import get_settings

router = fastapi.APIRouter()


def check_db_state():
    session = get_session()
    return session is not None


def check_storage_state():
    settings = get_settings()
    return settings.storage.exists() \
           and settings.storage.is_dir() \
           and settings.storage.owner() == 'mirek'


@router.get('/', status_code=200)
def check_health():
    db_state = check_db_state()
    storage_state = check_storage_state()
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
