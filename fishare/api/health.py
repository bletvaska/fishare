import logging
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, Depends
from sqlmodel import Session

from fishare.database import get_session
from fishare.models.settings import Settings
from fishare import __version__

router = APIRouter()
settings = Settings()


# callables for health check
def is_database_online():
    # FIXME bud je problem s yield-om alebo so session-om, ak je podany cez dependency injection :-/
    try:
        # session = get_session()
        # session.connection()
        return True
    except Exception as ex:
        logging.critical("Can't connect to database.")
        logging.exception(ex)
        return False


def is_storage_available():
    try:
        return settings.storage.exists() and settings.storage.is_dir()
    except Exception as ex:
        logging.critical(f'Storage is not available on path "{settings.storage}".')
        logging.exception(ex)
        return False


def is_storage_writable():
    try:
        file = Path(settings.storage / '_touch')
        file.touch()
        file.unlink()
        return True
    except FileNotFoundError as ex:
        logging.critical(f"File '{file}' can't be created in storage.")
        logging.exception(ex)
        return False


def health_status(session: Session = Depends(get_session)):
    storage_available = is_storage_available()
    storage_writable = is_storage_writable()
    db_active = is_database_online()

    status = 'up' if storage_writable and storage_available and db_active else 'down'

    return {
        'ts': datetime.now(),
        'status': status,
        'appVersion': __version__,  # security
        'python': 0.0,
        'storage': {
            'path': settings.storage.absolute(),  # security
            'exists': storage_available,
            'writable': storage_writable,
        },
        'db': {
            'uri': settings.db_uri,  # security
            'session': db_active
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
