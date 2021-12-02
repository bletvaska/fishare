import fastapi
from starlette.responses import JSONResponse
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound

from models.file import File
from models.settings import Settings
from database import engine


router = fastapi.APIRouter()


@router.get('/files/')  # select * from files
def list_of_files():
    return [
        'file1',
        'file2',
        'file3'
    ]


# select * from files where filename={filename}
@router.get('/files/{slug}')
def get_file(slug: str):
    try:
        with Session(engine) as session:
            statement = select(File).where(File.slug == slug)
            file = session.exec(statement).one()
            return file

    except NoResultFound as ex:
        content = {
            'error': 'File not found.',
            'detail':{
                'slug': f'No file with slug "{slug}"'
            }
        }
        return JSONResponse(
            status_code=404,
            content=content
        )

    except Exception as ex:
        return JSONResponse(
            status_code=500,
            content={
                'error': 'Unknown error occurred.'
            }
        )


        # data['link'] = file.url()

        # return data


@router.delete('/files/{filename}')  # delete from files where filename={filename}
def delete_file(filename: str):
    return "deleted"


@router.put('/files/{filename}')  # update files where filename={filename} set ...  # full update
def full_update_file(filename: str):
    return "full update"


@router.patch('/files/{filename}')  # update files where filename={filename} set ... # partial update
def partial_file_update(filename: str):
    return "partial update"


@router.post('/files/')  # insert into files values ()
def create_file():
    return "file was created"
