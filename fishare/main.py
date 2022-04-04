import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/api/v1/files/")
def get_list_of_files():
    return [
        "file1",
        "file2",
        "file3"
    ]


@app.get('/hello/{name}')
def greetings(name: str):
    return f'hello {name}'


def main():
    uvicorn.run('fishare.main:app', port=9000, host='0.0.0.0', reload=True)


if __name__ == '__main__':
    main()
