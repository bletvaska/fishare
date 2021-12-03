import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from fishare.api import files
from fishare.api import users
from fishare.views import homepage, cron
from fishare.models.settings import Settings

settings = Settings()

app = FastAPI()
app.include_router(files.router, prefix='/api/v1')
app.include_router(users.router, prefix='/api/v1')
app.include_router(homepage.router)
app.include_router(cron.router)

app.mount('/static', StaticFiles(directory='fishare/static'), name='static')

def main():
    uvicorn.run('fishare.main:app', port=8080, host='127.0.0.1', reload=True)


if __name__ == '__main__':
    main()
