import uvicorn
from fastapi import FastAPI

from fishare.api import files

# application init
app = FastAPI()
app.include_router(files.router, prefix='/api/v1/files')


@app.get("/")
def read_root():
    """
    Main homepage.
    """
    return "Ahoj Svet!"


if __name__ == '__main__':
    uvicorn.run('fishare.main:app', reload=True, port=8000, host='127.0.0.1')
