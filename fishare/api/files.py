import secrets
import shutil
from datetime import datetime
from typing import Optional

import fastapi
from fastapi import Request, APIRouter, UploadFile, Form
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from starlette.responses import JSONResponse, RedirectResponse

from fishare.core.responses import ProblemJSONResponse
from fishare.database import engine
from fishare.models.file import File
from fishare.models.problem_details import ProblemDetails
from fishare.models.settings import Settings

router = APIRouter()
settings = Settings()


@router.get('/subory/')
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
        content = ProblemDetails(
            title='File not found.',
            detail=f"No file with slug '{slug}'",
            status=404,
            instance=f'/files/{slug}'
        )

        return ProblemJSONResponse(
            status_code=404,
            content=content.dict(exclude_unset=True)
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


# update files where filename={filename} set ...  # full update
@router.patch('/files/{slug}')
def partial_file_update(slug: str,
                        payload: Optional[UploadFile] = fastapi.File(None),
                        filename: Optional[str] = Form(None),
                        max_downloads: Optional[int] = Form(None)):
    try:
        # get existing file from db
        with Session(engine) as session:
            statement = select(File).where(File.slug == slug)
            file = session.exec(statement).one()

            # upload/override new file if provided
            if payload is not None:
                path = settings.storage / slug
                with open(path, 'wb') as dest:
                    shutil.copyfileobj(payload.file, dest)

                # update the file object
                file.size = path.stat().st_size
                file.content_type = payload.content_type
                file.updated_at = datetime.now()

            # update filename if provided
            if filename is not None:
                file.filename = filename
                file.updated_at = datetime.now()

            # update max downloads if provided
            if max_downloads is not None:
                file.max_downloads = max_downloads
                file.updated_at = datetime.now()

            # commit changes to db
            session.add(file)
            session.commit()
            session.refresh(file)

            return file

    except NoResultFound:
        content = ProblemDetails(
            title='File not found.',
            detail=f"No file with slug '{slug}'",
            status=404,
            instance=f'/files/{slug}'
        )

        return ProblemJSONResponse(
            status_code=404,
            content=content.dict(exclude_unset=True)
        )


# update files where filename={filename} set ... # partial update
@router.put('/files/{slug}')
def full_update_file(slug: str,
                     payload: UploadFile = fastapi.File(...),
                     filename: str = Form(...),
                     max_downloads: int = Form(...)):
    try:
        # get existing file from db
        with Session(engine) as session:
            statement = select(File).where(File.slug == slug)
            file = session.exec(statement).one()

            # upload new file and update/overwrite existing file/attributes
            path = settings.storage / slug
            with open(path, 'wb') as dest:
                shutil.copyfileobj(payload.file, dest)

            # update the file object
            file.size = path.stat().st_size
            file.filename = filename
            file.max_downloads = max_downloads
            file.content_type = payload.content_type
            file.updated_at = datetime.now()

            session.add(file)
            session.commit()
            session.refresh(file)

            return file

    except NoResultFound:
        content = ProblemDetails(
            title='File not found.',
            detail=f"No file with slug '{slug}'",
            status=404,
            instance=f'/files/{slug}'
        )

        return ProblemJSONResponse(
            status_code=404,
            content=content.dict(exclude_unset=True)
        )


# insert into files values ()
@router.post('/files/', response_model=File)
def create_file(request: Request,
                payload: UploadFile = fastapi.File(...),
                filename: Optional[str] = Form(None),
                max_downloads: Optional[int] = Form(None)):
    # prepare the file entry
    file = File(
        filename=payload.filename if filename is None else filename,
        content_type=payload.content_type,
    )

    # set max downloads, if provided
    if max_downloads is not None:
        file.max_downloads = max_downloads

    # get ready
    path = settings.storage / file.slug

    # check if storage directory exists
    if not settings.storage.is_dir():
        settings.storage.mkdir(parents=True, exist_ok=True)

    # save uploaded file
    with open(path, 'wb') as dest:
        shutil.copyfileobj(payload.file, dest)

    # get file size
    file.size = path.stat().st_size

    # insert file in to db
    with Session(engine) as session:
        session.add(file)
        session.commit()
        session.refresh(file)

    # return RedirectResponse(f'/uploaded/?slug={file.slug}', status_code=302)

    # return newly created file
    return JSONResponse(
        status_code=201,
        content=jsonable_encoder(file)
    )
