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


@app.get('/api/v1/files/{filename}')
def get_file(filename: str):
    return {
        'filename': filename
    }


@app.post('/api/v1/files/')
def create_file():
    return 'file was created'


def main():
    uvicorn.run('fishare.main:app', port=9000, host='0.0.0.0', reload=True)


if __name__ == '__main__':
    main()
