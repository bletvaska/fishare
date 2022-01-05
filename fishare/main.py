from logging.config import dictConfig
import logging
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_health import health
from sqlmodel import SQLModel
from starlette_exporter import PrometheusMiddleware, handle_metrics

from fishare.api import files
from fishare.api import users
from fishare.api.health import is_database_online, is_storage_available, is_storage_writable, health_status
from fishare.database import engine
from fishare.models.logconfig import LogConfig
from fishare.views import homepage, cron, uploaded, download_file

from fishare.models.settings import Settings

settings = Settings()

# initialize app and it's routes
app = FastAPI()

# @app.on_event('startup')
# def on_startup():
# configure logging
dictConfig(LogConfig().dict())
logger = logging.getLogger('uvicorn.error')
logger.info('Initializing application...')

# init storage
if not settings.storage.exists():
    logger.info(f'Creating storage path "{settings.storage}"')
    settings.storage.mkdir(parents=True)

# init db
SQLModel.metadata.create_all(engine)

# health and metrics endpoints
app.add_api_route("/healthz", health([
    is_database_online,
    is_storage_available,
    is_storage_writable,
    health_status])
                  )
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)

# application api
app.include_router(files.router, prefix='/api/v1')
app.include_router(users.router, prefix='/api/v1')
app.include_router(homepage.router)
app.include_router(cron.router)
app.include_router(uploaded.router)
app.include_router(download_file.router)

app.mount('/static', StaticFiles(directory=Path(__file__).parent / 'static'), name='static')


def main():
    uvicorn.run('fishare.main:app', port=8080, host='127.0.0.1', reload=True)


if __name__ == '__main__':
    main()
