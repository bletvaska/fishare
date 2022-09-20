import fastapi

from fishare.models.file_details import FileDetails
from fishare.models.file_details_out import FileDetailsOut

router = fastapi.APIRouter()


# SELECT * FROM files
@router.get('/', summary='Get list of files.') # , response_model=list[FileDetailsOut])
def get_list_of_files():
    file = FileDetails(filename='fishare.exe', size=1024, mime_type='application/exec')
    return [
        FileDetails(filename='fishare.exe', size=1024, mime_type='application/exec'),
        FileDetails(filename='main.py', size=2048, mime_type='text/PYTHON'),
        FileDetails(filename='jano.jpg', size=65535, mime_type='image/jpeg'),
        FileDetailsOut(**file.dict())
    ]


# SELECT * FROM files WHERE slug=slug
@router.get('/{slug}', summary='Get file details identified by the {slug}.', response_model=FileDetailsOut)
def get_file_detail(slug: str):
    """
    Returns file details.
    """
    return FileDetails(filename='jano.jpg', size=65535, mime_type='image/jpeg')


# DELETE FROM files WHERE slug=slug
@router.delete('/{slug}', summary='Delete the file identified by the {slug}.')
def delete_file(slug: str):
    return f'deleted file {slug}'


# UPDATE files WHERE slug=slug SET ....
# full update
@router.put('/{slug}', summary='Updates the file identified by the {slug}. Any parameters not provided are reset to '
                               'their defaults.')
def full_update_file(slug: str):
    return f'full update for file {slug}'


# UPDATE files WHERE slug=slug SET ....
# partial update
@router.patch('/{slug}', summary='Updates the file identified by the {slug}. For any parameters not provided in '
                                 'request, existing values are retained.')
def partial_update_file(slug: str):
    return f'partial update for file {slug}'


# INSERT INTO files VALUES(...)
@router.post('/', summary='Uploads a file and creates file details.')
def create_file():
    return 'file was created'
