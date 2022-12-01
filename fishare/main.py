from fastapi import FastAPI
from sqladmin import Admin
from sqlmodel import SQLModel, create_engine
import uvicorn

from fishare.api.v1 import download


from .dependencies import get_settings
from .models.file_details import FileAdmin
from .api.v1 import files

# create app and set routers
app = FastAPI()
app.include_router(files.router, prefix=files.PATH_PREFIX)
app.include_router(download.router)

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
