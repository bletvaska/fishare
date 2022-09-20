import uvicorn
from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel

from fishare.api import files

# application init
from fishare.helpers import populate_data
from fishare.models.settings import get_settings

app = FastAPI()
app.include_router(files.router, prefix='/api/v1/files')


@app.get("/")
def read_root():
    """
    Main homepage.
    """
    return "Ahoj Svet!"


if __name__ == '__main__':
    # init database
    # engine = create_engine(get_settings().db_uri)
    # SQLModel.metadata.create_all(engine)
    populate_data()

    # uvicorn.run('fishare.main:app', reload=True, port=get_settings().port, host='127.0.0.1')
