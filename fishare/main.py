from fastapi import FastAPI
import uvicorn

app = FastAPI()


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
