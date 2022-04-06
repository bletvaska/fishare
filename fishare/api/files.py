from typing import List

import fastapi
from starlette.responses import JSONResponse

from fishare.models.file import File, FileOut
from fishare.models.problem_details import ProblemDetails

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

    # raise fastapi.HTTPException(status_code=404, detail="File not found!")
    content = ProblemDetails(
        type='/errors/files',
        title="File not found.",
        status=404,
        detail=f"File with slug '{slug} was not found.'",
        instance=f"/files/{slug}"
    )

    return JSONResponse(
        status_code=404,
        content=content.dict(exclude_unset=True)
    )


@router.post('/files/', summary='Uploads file and creates file details.')
def create_file():
    return 'file was created'


@router.delete('/files/{slug}', summary='Deletes the file identified by {slug}.')
def delete_file(slug: str):
    # search and delete file with 204
    for file in files:
        if file.slug == slug:
            files.remove(file)
            return JSONResponse(status_code=204)

    # when not found, then 404
    content = ProblemDetails(type='/errors/files',
                             title="File not found.",
                             status=404,
                             detail=f"File with slug '{slug}' was not found.",
                             instance=f"/files/{slug}")
    return JSONResponse(status_code=404,
                        content=content.dict())


@router.put('/files/{filename}',
            summary='Updates the file identified by {slug}. Any parameters not provided are reset to defaults.')
def full_file_update(filename: str):
    return f'file {filename} is going to be fully updated'


@router.patch('/files/{filename}',
              summary='Updates the file identified by {slug}. For any parameters not provided in request, existing '
                      'values are retained.')
def partial_file_update(filename: str):
    return f'file {filename} is going to be partially updated'
