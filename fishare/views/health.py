from datetime import datetime

from fastapi import APIRouter

from fishare.models.settings import Settings
from fishare.database import engine

router = APIRouter()
settings = Settings()


@router.get('/', summary='Returns microservice health check.')
def get_health():
    return {
        'ts': datetime.now(),
        'status': 'running',
        'appVersion': 0.0,
        'python': 0.0,
        'storage': {
            'path': settings.storage,
            'used': 0,
            'max': 0,
            'files': 0
        },
        'db': {
            'uri': settings.db_uri,
        },
    }


@router.get('/ready', summary='Checks readiness.')
def get_readiness():
    return {
        'ts': datetime.now(),
        'status': 'ready'
    }


@router.get('/alive', summary='Checks liveness.')
def get_liveness():
    return {
        'ts': datetime.now(),
        'status': 'up'
    }
