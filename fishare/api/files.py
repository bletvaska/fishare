import fastapi

router = fastapi.APIRouter()


@router.get("/files/")
def get_list_of_files():
    return [
        "file1",
        "file2",
        "file3"
    ]


@router.head('/files/{filename}')
@router.get('/files/{filename}')
def get_file(filename: str):
    return {
        'filename': filename
    }


@router.post('/files/')
def create_file():
    return 'file was created'


@router.delete('/files/{filename}')
def delete_file(filename: str):
    return f'file {filename} was deleted.'


@router.put('/files/{filename}')
def full_file_update(filename: str):
    return f'file {filename} is going to be fully updated'


@router.patch('/files/{filename}')
def partial_file_update(filename: str):
    return f'file {filename} is going to be partially updated'
