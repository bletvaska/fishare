from fastapi import FastAPI
import uvicorn

from .models.settings import Settings
from .api.v1 import files

app = FastAPI()
app.include_router(files.router, prefix=files.PATH_PREFIX)


def main():
    settings = Settings()
    uvicorn.run("fishare.main:app", reload=True, host="0.0.0.0", port=9000)


if __name__ == "__main__":
    main()
