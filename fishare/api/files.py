import shutil
from datetime import datetime
import secrets

from starlette.responses import JSONResponse
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound
from fastapi import Request, APIRouter, UploadFile
import fastapi

from fishare.models.file import File
from fishare.models.settings import Settings
from fishare.database import engine

# from pydantic import BaseModel

router = APIRouter()
settings = Settings()


@router.get('/files/')  # select * from files
def list_of_files(request: Request, offset: int = 0, page: int = 10):
    # TODO zistit, ako ziskat pocet vsetkych suborov
    count_files = 1000

    # set next link
    next_offset = offset + page
    if next_offset > count_files:
        next_link = None
    else:
        next_link = f'{settings.base_url}/api/v1/files/?offset={offset + page}&page={page}'

    # set previous link
    prev_offset = offset - page
    if prev_offset < 0:
        previous_link = None
    else:
        previous_link = f'{settings.base_url}/api/v1/files/?offset={offset - page}&page={page}'

    response = {
        "count": 0,
        "next": next_link,
        "previous": previous_link,
        "results": []
    }

    with Session(engine) as session:
        statement = select(File).offset(offset).limit(page)
        response['results'].extend(session.exec(statement).all())

        return response


# select * from files where filename={filename}
@router.get('/files/{slug}')
def get_file(slug: str):
    try:
        with Session(engine) as session:
            statement = select(File).where(File.slug == slug)
            file = session.exec(statement).one()

            data = file.dict()
            data['link'] = file.url()

            return data

    except NoResultFound as ex:
        content = {
            'error': 'File not found.',
            'detail': {
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


# delete from files where filename={filename}
@router.delete('/files/{slug}')
def delete_file(slug: str):
    try:
        with Session(engine) as session:
            statement = select(File).where(File.slug == slug)
            file = session.exec(statement).one()

            session.delete(file)
            session.commit()

            return JSONResponse(
                status_code=204
            )

    except NoResultFound as ex:
        content = {
            'error': 'File not found.',
            'detail': {
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


@router.put('/files/{filename}')  # update files where filename={filename} set ...  # full update
def full_update_file(filename: str):
    return "full update"


@router.patch('/files/{filename}')  # update files where filename={filename} set ... # partial update
def partial_file_update(filename: str):
    return "partial update"


# class Person(BaseModel):
#     title: str

# insert into files values ()
@router.post('/files/')
def create_file(request: Request, payload: UploadFile = fastapi.File(...)):
    # get ready
    secret_name = secrets.token_urlsafe(settings.slug_length)
    path = settings.storage / secret_name

    # save uploaded file
    with open(path, 'wb') as dest:
        shutil.copyfileobj(payload.file, dest)

    # prepare the file entry
    file = File(
        slug=secret_name,
        filename=payload.filename,
        mime_type=payload.content_type,
        size=0,
        created=datetime.now()
    )

    # insert file in to db
    with Session(engine) as session:
        session.add(file)
        session.commit()
        session.refresh(file)

    # return newly created file
    return JSONResponse(
        status_code=201,
        content=file.json()
    )
