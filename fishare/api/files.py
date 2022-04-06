from typing import List

import fastapi

from fishare.models.file import File, FileOut

router = fastapi.APIRouter()

files = [
    File(filename='jano.jpg', size=1234, mime_type='image/jpeg'),
    File(filename='juro.jpg', size=21234, mime_type='image/jpeg'),
    File(filename='main.py', size=234, mime_type='plain/text'),
    File(filename='pesnicka.mp3', size=12000000, mime_type='audio/mp3'),
]


@router.get("/files/", response_model=List[FileOut], summary="Get list of files.")
def get_list_of_files():
    return files


@router.head('/files/{slug}')
@router.get('/files/{slug}', response_model=FileOut, summary="Get file identified by the {slug}.")
def get_file(slug: str):
    for file in files:
        if file.slug == slug:
            return file

    return {}

    # found_file = next((file for file in files if file.slug == slug), None)
    # if found_file is None:
    #     raise fastapi.HTTPException(status_code=404, detail="File not found!")
    # return found_file


@router.post('/files/', summary='Uploads file and creates file details.')
def create_file():
    return 'file was created'


@router.delete('/files/{filename}', summary='Deletes the file identified by {slug}.')
def delete_file(filename: str):
    return f'file {filename} was deleted.'


@router.put('/files/{filename}',
            summary='Updates the file identified by {slug}. Any parameters not provided are reset to defaults.')
def full_file_update(filename: str):
    return f'file {filename} is going to be fully updated'


@router.patch('/files/{filename}',
              summary='Updates the file identified by {slug}. For any parameters not provided in request, existing '
                      'values are retained.')
def partial_file_update(filename: str):
    return f'file {filename} is going to be partially updated'
