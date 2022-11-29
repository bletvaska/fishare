from fastapi import FastAPI
import uvicorn

from .api.v1 import files

app = FastAPI()
app.include_router(files.router, prefix=files.PATH_PREFIX)


@app.get("/")
def read_root():
    return {"hello": "world"}


@app.get("/greetings/{name}")
def hello(name: str):
    return f"Hello {name}"


def main():
    uvicorn.run("fishare.main:app", reload=True, host="0.0.0.0", port=9000)


if __name__ == "__main__":
    main()

