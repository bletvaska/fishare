import shutil
from time import sleep
from typing import Optional

import fastapi
from fastapi import Depends, Form, UploadFile
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from starlette.responses import JSONResponse, Response

from fishare.database import get_session
from fishare.models.file import FileOut, File
from fishare.models.pager import Pager
from fishare.models.problem_details import ProblemDetails
from fishare.models.settings import Settings

router = fastapi.APIRouter()

settings = Settings()


@router.get("/files/", summary="Get list of files.")
def get_list_of_files(offset: int = 0, page_size: int = 5, session: Session = Depends(get_session)):
    """
    Returns the Pager, which contains the list of files.

    :param offset: page offset
    :param page_size: size of the page
    :return: Pager object
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
            results=files
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


@router.head('/files/{slug}')
@router.get('/files/{slug}', response_model=FileOut, summary="Get file identified by the {slug}.")
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


@router.post('/files/', response_model=FileOut, status_code=201,
             summary='Uploads file and creates file details.')
def create_file(payload: UploadFile = fastapi.File(...), filename: Optional[str] = Form(None),
                session: Session = Depends(get_session)):
    # create file skeleton
    file = File(
        filename=payload.file if filename is None else filename,
        size=None,
        mime_type=payload.content_type
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


@router.delete('/files/{slug}', summary='Deletes the file identified by {slug}.')
def delete_file(slug: str, session: Session = Depends(get_session)):
    try:
        # session.query(File).filter(File.slug == slug).delete()

        # select file by slug
        statement = select(File).where(File.slug == slug)
        file = session.exec(statement).one()

        # delete file
        session.delete(file)
        session.commit()

        # return 204
        return Response(status_code=204)

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


@router.put('/files/{filename}',
            summary='Updates the file identified by {slug}. Any parameters not provided are reset to defaults.')
def full_file_update(filename: str):
    return f'file {filename} is going to be fully updated'


@router.patch('/files/{filename}',
              summary='Updates the file identified by {slug}. For any parameters not provided in request, existing '
                      'values are retained.')
def partial_file_update(filename: str):
    return f'file {filename} is going to be partially updated'
