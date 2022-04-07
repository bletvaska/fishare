import fastapi
from starlette.responses import JSONResponse, Response

from fishare.helper import populate_data
from fishare.models.file import FileOut
from fishare.models.pager import Pager
from fishare.models.problem_details import ProblemDetails

router = fastapi.APIRouter()

files = populate_data(1000)


@router.get("/files/", summary="Get list of files.")
def get_list_of_files(offset: int = 0, page_size: int = 5):
    """
    Returns the Pager, which contains the list of files.

    :param offset: page offset
    :param page_size: size of the page
    :return: Pager object
    """
    print(f'query params: {offset} {page_size}')

    start = offset * page_size
    # from IPython import embed
    # embed()

    # prepare next link
    if start + page_size >= len(files):
        next_page = None
    else:
        next_page = f'http://localhost:9000/api/v1/files/?offset={offset + 1}&page_size={page_size}'

    # prepare previous link
    if start - page_size <= 0:
        prev_page = None
    else:
        prev_page = f'http://localhost:9000/api/v1/files/?offset={offset - 1}&page_size={page_size}'

    # get result
    return Pager(
        first=f'http://localhost:9000/api/v1/files/?page_size={page_size}',
        last=f'http://localhost:9000/api/v1/files/?page_size={page_size}&offset={(len(files) // page_size) - 1}',
        next=next_page,
        previous=prev_page,
        results=files[start:start + page_size]
    )


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
            return Response(status_code=204)

    # when not found, then 404
    content = ProblemDetails(
        type='/errors/files',
        title="File not found.",
        status=404,
        detail=f"File with slug '{slug}' was not found.",
        instance=f"/files/{slug}"
    )
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
