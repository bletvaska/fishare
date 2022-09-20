import fastapi
from sqlalchemy.exc import NoResultFound
from sqlmodel import create_engine, Session, select
from starlette.responses import JSONResponse

from fishare.models.file_details import FileDetails
from fishare.models.file_details_out import FileDetailsOut
from fishare.models.problem_details import ProblemDetails
from fishare.models.settings import get_settings

router = fastapi.APIRouter()


@router.get('/', summary='Get list of files.', response_model=list[FileDetailsOut])
def get_list_of_files():
    engine = create_engine(get_settings().db_uri)

    with Session(engine) as session:
        # SELECT * FROM files
        statement = select(FileDetails)
        files = session.exec(statement).all()
        return files


@router.get('/{slug}', summary='Get file details identified by the {slug}.', response_model=FileDetailsOut)
def get_file_detail(slug: str):
    """
    Returns file details.
    """
    engine = create_engine(get_settings().db_uri)

    try:
        with Session(engine) as session:
            # SELECT * FROM files WHERE slug=slug
            statement = select(FileDetails).where(FileDetails.slug == slug)
            file = session.exec(statement).one()
            return file
    except NoResultFound as ex:
        problem = ProblemDetails(
            status=404,
            title='File not found',
            detail=f"File with slug '{slug}' does not exist.",
            instance=f'/api/v1/files/{slug}'
        )

        return JSONResponse(
            status_code=problem.status,
            content=problem.dict(),
            media_type='application/problem+json'
        )

        # return ProblemDetailsResponse(problem)


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
