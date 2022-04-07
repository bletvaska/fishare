import uvicorn
from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel

from fishare.api import files
from fishare.models.settings import Settings

app = FastAPI()
app.include_router(files.router, prefix='/api/v1')

settings = Settings()


def main():
    # init db
    engine = create_engine(settings.db_uri)
    SQLModel.metadata.create_all(engine)

    # run webserver
    uvicorn.run('fishare.main:app', port=settings.port, host='0.0.0.0', reload=True)


if __name__ == '__main__':
    main()
