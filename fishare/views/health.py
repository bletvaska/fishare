from datetime import datetime

from fastapi import APIRouter

from fishare.models.settings import Settings

router = APIRouter()
settings = Settings()


@router.get('/health', summary='Returns microservice health check.')
def get_health():
    return {
        'ts': datetime.now(),
        'storage': {
            'path': settings.storage,
            'usage': 0,
            'files': 0
        },
        'db': {
            'uri': settings.db_uri
        },
    }
