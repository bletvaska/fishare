import fastapi

from fishare.models.file import File

router = fastapi.APIRouter()

files = [
    File(filename='jano.jpg', size=1234, mime_type='image/jpeg'),
    File(filename='juro.jpg', size=21234, mime_type='image/jpeg'),
    File(filename='main.py', size=234, mime_type='plain/text'),
    File(filename='pesnicka.mp3', size=12000000, mime_type='audio/mp3'),
]


@router.get("/files/")
def get_list_of_files():
    return files


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
