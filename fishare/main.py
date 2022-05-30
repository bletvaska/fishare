from pathlib import Path

import uvicorn
from fastapi import FastAPI, Depends
from fastapi_health import health
from sqlmodel import create_engine, SQLModel
from starlette.staticfiles import StaticFiles

from fishare.database import get_session
from fishare.views import homepage, admin
from fishare.api import files, cron, download
from fishare.models.settings import get_settings

app = FastAPI(title='Fishare')


def is_database_online(session: bool = Depends(get_session)):
    return session


def is_storage_healthy():
    try:
        file = Path(get_settings().storage / '_touch')
        file.touch()
        file.unlink()
        return True
    except FileNotFoundError as ex:
        print("Critical error: no read/write access to storage.")
        return False


def health_status():
    return {
        'session': 'ok' if is_database_online() else 'failed',
        'storage': 'ok' if is_storage_healthy() else 'failed',
    }


app.add_api_route("/health", health([
    is_database_online,
    is_storage_healthy,
    health_status
]))

# rest api
app.include_router(files.router, prefix='/api/v1/files')
app.include_router(cron.router, prefix='/cron')
app.include_router(download.router)

# views
app.include_router(homepage.router)
app.include_router(admin.router)

app.mount('/static',
          StaticFiles(directory=Path(__file__).parent / 'static'),
          name='static')


def main():
    # TODO fix if storage directory does not exist

    # init db
    engine = create_engine(get_settings().db_uri)
    SQLModel.metadata.create_all(engine)

    # populate db
    # populate_data(1000)

    # run webserver
    uvicorn.run('fishare.main:app', port=get_settings().port, host='0.0.0.0', reload=True)


if __name__ == '__main__':
    main()
