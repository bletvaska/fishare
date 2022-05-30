import shutil
from datetime import datetime, timedelta
from typing import Optional

import fastapi
from fastapi import Depends, Form, UploadFile, Response
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select

from fishare.core.decorators import file_exists
from fishare.core.responses import ProblemJSONResponse
from fishare.database import get_session
from fishare.models.file import FileOut, File
from fishare.models.pager import Pager
from fishare.models.problem_details import ProblemDetails
from fishare.models.settings import get_settings

router = fastapi.APIRouter()


# TODO
# 8. requests na kradnutie pocasia


@router.get("/", summary="Get list of files.")
def get_list_of_files(offset: int = 0, page_size: int = 5, session: Session = Depends(get_session)):
    """
    Returns the Pager, which contains the list of files.
    """
    settings = get_settings()

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

    return ProblemJSONResponse(
        status_code=content.status,
        content=content.dict(exclude_unset=True),
    )


@router.get('/{slug}', response_model=FileOut, summary="Get file identified by the {slug}.")
@file_exists
def get_file(slug: str, file=None, session: Session = Depends(get_session)):
    return file


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
    path = get_settings().storage / file.slug

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
@file_exists
def delete_file(slug: str, file=None, session: Session = Depends(get_session)):
    # delete file from storage
    path = get_settings().storage / file.slug
    path.unlink(missing_ok=True)

    # delete file
    session.delete(file)
    session.commit()

    return Response(status_code=204)


@router.put('/{slug}', response_model=FileOut,
            summary='Updates the file identified by {slug}. Any parameters not provided are reset to defaults.')
@file_exists
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
        path = get_settings().storage / file.slug
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

    return ProblemJSONResponse(
        status_code=content.status,
        content=content.dict()
    )


@router.patch('/{slug}', response_model=FileOut,
              summary='Updates the file identified by {slug}. For any parameters not provided in request, existing '
                      'values are retained.')
def update_file(slug: str,
                payload: Optional[UploadFile] = fastapi.File(None),
                filename: str = Form(None),
                max_downloads: int = Form(None),
                session: Session = Depends(get_session)):
    try:
        # get file from db
        statement = select(File).where(File.slug == slug)
        file = session.exec(statement).one()

        # if file was uploaded
        if payload is not None:
            # update filename and mimetype
            file.filename = payload.filename if filename is None else filename
            file.mime_type = payload.content_type

            # upload file
            path = get_settings().storage / file.slug
            with open(path, 'wb') as dest:
                shutil.copyfileobj(payload.file, dest)

            # update file size
            file.size = path.stat().st_size

        else:
            file.filename = file.filename if filename is None else filename

        # update max_download and updated time
        file.max_downloads = file.max_downloads if max_downloads is None else max_downloads
        file.updated_at = datetime.now()
        file.expires = datetime.now() + timedelta(days=1)

        # update
        session.add(file)
        session.commit()
        session.refresh(file)

        return file

    except NoResultFound as ex:
        content = ProblemDetails(
            type='/errors/files/patch',
            title="File not found.",
            status=404,
            detail=f"File with slug '{slug}' was not found.'",
            instance=f"/files/{slug}"
        )

        return ProblemJSONResponse(
            status_code=404,
            content=content.dict()
        )
