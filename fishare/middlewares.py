from time import time

from starlette.requests import Request


async def add_process_time_header(request: Request, call_next):
    start = time()
    response = await call_next(request)
    duration = time() - start
    response.headers['X-Process-Time'] = str(duration)
    return response
