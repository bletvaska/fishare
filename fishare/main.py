import uvicorn
from fastapi import FastAPI

from fishare.api import files

# application init
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
    uvicorn.run('fishare.main:app', reload=True, port=get_settings().port, host='127.0.0.1')
