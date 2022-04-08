import shutil
from datetime import datetime
from typing import Optional

import fastapi
from fastapi import Depends, Form, UploadFile
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from starlette.responses import JSONResponse

from fishare.database import get_session
from fishare.models.file import FileOut, File
from fishare.models.pager import Pager
from fishare.models.problem_details import ProblemDetails
from fishare.models.settings import Settings

router = fastapi.APIRouter()

settings = Settings()


# TODO
# 2. PATCH
# 3. JsonProblemResponse
# 4. cron


@router.get("/", summary="Get list of files.")
def get_list_of_files(offset: int = 0, page_size: int = 5, session: Session = Depends(get_session)):
    """
    Returns the Pager, which contains the list of files.
    """

    try:
        # count nr of files
        files_count = session.query(File).count()

        # get data
        start = offset * page_size
        statement = select(File).offset(start).limit(page_size)
        files = session.exec(statement).all()

        # prepare next link
        if start + page_size >= files_count:
            next_page = None
        else:
            next_page = f'{settings.base_url}/api/v1/files/?offset={offset + 1}&page_size={page_size}'

        # prepare previous link
        if start - page_size <= 0:
            prev_page = None
        else:
            prev_page = f'{settings.base_url}/api/v1/files/?offset={offset - 1}&page_size={page_size}'

        # get result
        return Pager(
            first=f'{settings.base_url}/api/v1/files/?page_size={page_size}',
            last=f'{settings.base_url}/api/v1/files/?page_size={page_size}&offset={(files_count // page_size) - 1}',
            next=next_page,
            previous=prev_page,
            results=files,
            count=files_count
        )

    except Exception as ex:

        content = ProblemDetails(
            type='/errors/server',
            title="Some error occured.",
            status=500,
            detail=str(ex),
            instance=f"/files/?page_size={page_size}&offset={offset}"
        )

    return JSONResponse(
        status_code=content.status,
        content=content.dict(exclude_unset=True)
    )


@router.head('/{slug}')
@router.get('/{slug}', response_model=FileOut, summary="Get file identified by the {slug}.")
def get_file(slug: str, session: Session = Depends(get_session)):
    try:
        statement = select(File).where(File.slug == slug)
        return session.exec(statement).one()

    except NoResultFound as ex:
        content = ProblemDetails(
            type='/errors/files/get',
            title="File not found.",
            status=404,
            detail=f"File with slug '{slug} was not found.'",
            instance=f"/files/{slug}"
        )

    return JSONResponse(
        status_code=content.status,
        content=content.dict(exclude_unset=True)
    )


@router.post('/', response_model=FileOut, status_code=201,
             summary='Uploads file and creates file details.')
def create_file(payload: UploadFile = fastapi.File(...),
                max_downloads: Optional[str] = Form(None),
                session: Session = Depends(get_session)):
    # create file skeleton
    file = File(
        filename=payload.filename,
        size=-1,
        mime_type=payload.content_type,
        max_downloads=1 if max_downloads is None else max_downloads
    )

    # get ready
    path = settings.storage / file.slug

    # save uploaded file
    with open(path, 'wb') as dest:
        shutil.copyfileobj(payload.file, dest)

    # get file size
    file.size = path.stat().st_size

    # save to db
    session.add(file)
    session.commit()
    session.refresh(file)

    return file


@router.delete('/{slug}', status_code=204,
               summary='Deletes the file identified by {slug}.')
def delete_file(slug: str, session: Session = Depends(get_session)):
    try:
        # session.query(File).filter(File.slug == slug).delete()

        # select file by slug
        statement = select(File).where(File.slug == slug)
        file = session.exec(statement).one()

        # delete file from storage
        path = settings.storage / file.slug
        path.unlink(missing_ok=True)

        # delete file
        session.delete(file)
        session.commit()

        # return 204
        # return Response(status_code=204)
        return  # return None

    except NoResultFound as ex:
        # when not found, then 404
        content = ProblemDetails(
            type='/errors/files/delete',
            title="File not found.",
            status=404,
            detail=f"File with slug '{slug}' was not found.",
            instance=f"/files/{slug}"
        )

    return JSONResponse(status_code=content.status,
                        content=content.dict())


@router.put('/{slug}', response_model=FileOut,
            summary='Updates the file identified by {slug}. Any parameters not provided are reset to defaults.')
def full_file_update(slug: str,
                     payload: UploadFile,  # UploadFile = fastapi.File(...)
                     filename: str = Form(None),
                     max_downloads: int = Form(...),
                     session: Session = Depends(get_session)
                     ):
    try:
        # get the file with given slug
        statement = select(File).where(File.slug == slug)
        file = session.exec(statement).one()

        # save uploaded file
        path = settings.storage / file.slug
        with open(path, 'wb') as dest:
            shutil.copyfileobj(payload.file, dest)

        # update filename if given
        if filename is not None:
            file.filename = filename
        else:
            file.filename = payload.filename

        # update other file fields
        file.size = path.stat().st_size
        file.max_downloads = max_downloads
        file.updated_at = datetime.now()
        file.mime_type = payload.content_type

        # update db
        session.add(file)
        session.commit()
        session.refresh(file)

        return file

    except NoResultFound as ex:
        # when not found, then 404
        content = ProblemDetails(
            type='/errors/files/put',
            title="File not found.",
            status=404,
            detail=f"File with slug '{slug}' was not found.",
            instance=f"/files/{slug}"
        )

    return JSONResponse(status_code=content.status,
                        content=content.dict())


@router.patch('/{slug}',
              summary='Updates the file identified by {slug}. For any parameters not provided in request, existing '
                      'values are retained.')
def partial_file_update(slug: str):
    return f'file {slug} is going to be partially updated'
