import uvicorn
from fastapi import FastAPI

from fishare.api import files
from fishare.api import users
from fishare.views import homepage

app = FastAPI()
app.include_router(files.router, prefix='/api/v1')
app.include_router(users.router, prefix='/api/v1')
app.include_router(homepage.router)


def main():
    uvicorn.run('main:app', port=8080, host='0.0.0.0', reload=True)


if __name__ == '__main__':
    main()