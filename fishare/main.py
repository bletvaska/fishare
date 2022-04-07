import uvicorn
from fastapi import FastAPI

from fishare.api import files
from fishare.models.settings import Settings

app = FastAPI()
app.include_router(files.router, prefix='/api/v1')

settings = Settings()


def main():
    uvicorn.run('fishare.main:app', port=9000, host='0.0.0.0', reload=True)


if __name__ == '__main__':
    main()
