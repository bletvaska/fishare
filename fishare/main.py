from datetime import datetime
from pathlib import Path
import time

from fastapi import Depends, FastAPI, Request
from loguru import logger
from sqladmin import Admin
from sqlmodel import SQLModel, Session, create_engine, or_, select
from starlette_prometheus import PrometheusMiddleware, metrics
import uvicorn
from starlette.staticfiles import StaticFiles
from fastapi_utils.tasks import repeat_every
from starlette.middleware.base import BaseHTTPMiddleware

from fishare.models.settings import Settings

from .views import homepage
from .dependencies import get_session, get_settings
from .models.file_details import FileAdmin, FileDetails
from .api.v1 import files, download, cron

# create app and set routers
app = FastAPI()
app.add_route('/metrics', metrics)
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

# creating middleware
async def log_client_ip_in_middleware(request: Request, call_next):
    logger.info(f"Incomming connection from {request.client.host} in middleware.")
    response = await call_next(request)
    return response


async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.add_middleware(BaseHTTPMiddleware, dispatch=log_client_ip_in_middleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
app.add_middleware(PrometheusMiddleware)


def main():
    uvicorn.run("fishare.main:app", reload=True, host="0.0.0.0", port=9000)


@app.on_event("startup")
@repeat_every(seconds=60 * 5)
def cleanup():
    logger.info("running cleanup")
    try:
        session = next(get_session())
        start = datetime.now()

        statement = select(FileDetails).where(
            or_(
                FileDetails.downloads >= FileDetails.max_downloads,
                FileDetails.expires < datetime.now(),
            )
        )

        files = session.exec(statement).all()

        # delete files
        for file in files:
            # delete file from storage
            path = get_settings().storage / file.slug
            path.unlink(missing_ok=True)

            # delete file in db
            session.delete(file)
            session.commit()

        end = datetime.now()
        duration = end - start

        print(
            {
                "startedAt": start,
                "finishedAt": end,
                "duration": duration.total_seconds(),
                "removedFiles": len(files),
            }
        )
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
