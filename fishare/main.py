import uvicorn

from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel
from starlette.staticfiles import StaticFiles

from fishare.api import files, download, healthcheck, cron
from fishare.models.settings import get_settings

# route initialization
from fishare.views import homepage, admin

app = FastAPI()
app.include_router(files.router, prefix='/api/v1/files')
app.include_router(healthcheck.router, prefix='/health')
app.include_router(cron.router, prefix='/cron')
app.include_router(admin.router, prefix='/admin')
app.include_router(download.router, prefix='')
app.include_router(homepage.router, prefix='')

# mount static folder
app.mount('/static',
          StaticFiles(directory='fishare/static'),
          name='static')

if __name__ == '__main__':
    # init database
    engine = create_engine(get_settings().db_uri)
    SQLModel.metadata.create_all(engine)

    uvicorn.run('fishare.main:app', reload=True, port=get_settings().port, host='127.0.0.1')
