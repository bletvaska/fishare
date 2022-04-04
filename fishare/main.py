import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello():
    return "Hello, World!"


def main():
    uvicorn.run('fishare.main:app', port=9000, host='0.0.0.0', reload=False)


if __name__ == '__main__':
    main()
