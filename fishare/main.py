import argparse
from pathlib import Path

import uvicorn

from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.staticfiles import StaticFiles
from starlette_prometheus import PrometheusMiddleware, metrics

from fishare.api import files, download, healthcheck, cron
from fishare.dependencies import get_settings
from fishare.middlewares import add_process_time_header
from fishare.views import homepage, admin

app = FastAPI()

# add middleware functions
app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
app.add_middleware(PrometheusMiddleware)

# add routes
app.add_route("/metrics/", metrics)
app.include_router(files.router, prefix='/api/v1/files')
app.include_router(healthcheck.router, prefix='/health')
app.include_router(cron.router, prefix='/cron')
app.include_router(admin.router, prefix='/admin')
app.include_router(download.router, prefix='')
app.include_router(homepage.router, prefix='')

# mount static folder
app.mount('/static',
          StaticFiles(directory=Path(__file__).parent / 'static'),
          name='static')


def main():
    # parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                     help='an integer for the accumulator')
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')
    #
    # args = parser.parse_args()
    # print(args.accumulate(args.integers))

    # init database
    engine = create_engine(get_settings().db_uri)
    SQLModel.metadata.create_all(engine)

    uvicorn.run('fishare.main:app', reload=True, port=get_settings().port, host='127.0.0.1')


if __name__ == '__main__':
    main()
