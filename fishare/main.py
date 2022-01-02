from logging.config import dictConfig

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_health import health

from fishare.api import files
from fishare.api import users
from fishare.api.health import is_database_online, is_storage_available, is_storage_writable, health_status
from fishare.models.logconfig import LogConfig
from fishare.views import homepage, cron, uploaded, download_file
from fishare.models.settings import Settings

settings = Settings()

# configure logging
dictConfig(LogConfig().dict())

# initialize app and it's routes
app = FastAPI()
app.add_api_route("/healthz", health([is_database_online, is_storage_available, is_storage_writable, health_status]))
app.include_router(files.router, prefix='/api/v1')
app.include_router(users.router, prefix='/api/v1')
app.include_router(homepage.router)
app.include_router(cron.router)
app.include_router(uploaded.router)
app.include_router(download_file.router)

app.mount('/static', StaticFiles(directory='fishare/static'), name='static')


def main():
    uvicorn.run('fishare.main:app', port=8080, host='127.0.0.1', reload=True)


if __name__ == '__main__':
    main()
