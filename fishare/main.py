from pathlib import Path
from fastapi import FastAPI
from sqladmin import Admin
from sqlmodel import SQLModel, create_engine
import uvicorn
from starlette.staticfiles import StaticFiles

from .views import homepage
from .dependencies import get_settings
from .models.file_details import FileAdmin
from .api.v1 import files, download, cron

# create app and set routers
app = FastAPI()
app.include_router(files.router, prefix=files.PATH_PREFIX)
app.include_router(download.router)
app.include_router(homepage.router)
app.include_router(cron.router)

# mount static folder
app.mount(
    "/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static"
)

# init db
engine = create_engine(get_settings().db_uri)
SQLModel.metadata.create_all(engine)

# admin view
admin = Admin(app, engine)
admin.add_view(FileAdmin)


def main():
    uvicorn.run("fishare.main:app", reload=True, host="0.0.0.0", port=9000)


if __name__ == "__main__":
    main()
