from pathlib import Path

import uvicorn
from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel
from starlette.staticfiles import StaticFiles

from fishare.views import homepage
from fishare.api import files, cron, download
from fishare.models.settings import Settings

app = FastAPI()

# rest api
app.include_router(files.router, prefix='/api/v1/files')
app.include_router(cron.router, prefix='/cron')
app.include_router(download.router)

# views
app.include_router(homepage.router)

app.mount('/static',
          StaticFiles(directory=Path(__file__).parent / 'static'),
          name='static')


def main():
    # TODO fix if storage directory does not exist
    settings = Settings()

    # init db
    engine = create_engine(settings.db_uri)
    SQLModel.metadata.create_all(engine)

    # populate db
    # populate_data(1000)

    # run webserver
    uvicorn.run('fishare.main:app', port=settings.port, host='0.0.0.0', reload=True)


if __name__ == '__main__':
    main()
