from datetime import datetime
import mimetypes
import shutil

import fastapi
from fastapi import Depends, Form, UploadFile, File
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
from starlette.requests import Request
from starlette.responses import JSONResponse

from fishare.database import get_session
from fishare.models.file_details import FileDetails
from fishare.models.file_details_out import FileDetailsOut
from fishare.models.pager import Pager
from fishare.models.problem_details import ProblemDetails
from fishare.models.settings import get_settings, Settings

router = fastapi.APIRouter()


@router.get('/', summary='Get list of files.', response_model=Pager)
def get_list_of_files(request: Request, page: int = 1, size: int = 50,
                      session: Session = Depends(get_session)):
    url = f'{get_settings().base_url}{request.url.path}'

    # create pager object
    pager = Pager()

    # count nr of files
    pager.count = session.query(FileDetails).count()

    # get files
    # SELECT * FROM files LIMIT (offset - 1) * page_size, page_size
    statement = select(FileDetails).offset((page - 1) * size).limit(size)
    pager.results = session.exec(statement).all()

    # create links to first and last page
    pager.first = f'{url}?size={size}'
    pager.last = f'{url}?size={size}&page={pager.count // size + 1}'

    # next page
    if page + 1 <= pager.count // size + 1:
        pager.next = f'{url}?size={size}&page={page + 1}'

    # previous page
    if page - 1 > 0:
        pager.previous = f'{url}?size={size}&page={page - 1}'

    return pager


@router.get('/{slug}', summary='Get file details identified by the {slug}.', response_model=FileDetailsOut)
def get_file_detail(request: Request, slug: str, session: Session = Depends(get_session)):
    """
    Returns file details.
    """
    try:
        # SELECT * FROM files WHERE slug=slug
        statement = select(FileDetails).where(FileDetails.slug == slug)
        file = session.exec(statement).one()
        return file
    except NoResultFound as ex:
        problem = ProblemDetails(
            status=404,
            title='File not found',
            detail=f"File with slug '{slug}' does not exist.",
            instance=f'{request.url.path}'
        )

        return JSONResponse(
            status_code=problem.status,
            content=problem.dict(),
            media_type='application/problem+json'
        )

        # return ProblemResponse(problem)


# DELETE FROM files WHERE slug=slug
@router.delete('/{slug}', summary='Delete the file identified by the {slug}.', status_code=204)
async def delete_file(request: Request, slug: str, session: Session = Depends(get_session)):
    try:
        statement = select(FileDetails).where(FileDetails.slug == slug)
        file = session.exec(statement).one()
        session.delete(file)
        session.commit()
        # return

    except NoResultFound as ex:
        problem = ProblemDetails(
            status=404,
            title='File not found',
            detail=f"File with slug '{slug}' does not exist.",
            instance=f'{request.url.path}'
        )

        return JSONResponse(
            status_code=problem.status,
            content=problem.dict(),
            media_type='application/problem+json'
        )


# UPDATE files WHERE slug=slug SET ....
# full update
@router.put('/{slug}', response_model=FileDetailsOut, status_code=200,
            summary='Updates the file identified by the {slug}. Any parameters not provided are reset to '
                    'their defaults.')
def full_update_file(request: Request, slug: str,
                     max_downloads: int = Form(),
                     payload: UploadFile = File(...),
                     session: Session = Depends(get_session),
                     settings: Settings = Depends(get_settings)):
    try:
        # select file with given slug
        statement = select(FileDetails).where(FileDetails.slug == slug)
        file = session.exec(statement).one()

        # create path for file to save
        path = settings.storage / file.slug

        # save file
        with open(path, 'wb') as dest:
            shutil.copyfileobj(payload.file, dest)

        # update file fields
        file.size = path.stat().st_size
        file.filename = payload.filename
        file.max_downloads = max_downloads
        file.updated_at = datetime.now()

        # update db
        session.add(file)
        session.commit()
        session.refresh(file)

        return file
    except NoResultFound as ex:
        problem = ProblemDetails(
            status=404,
            title='File not found',
            detail=f"File with slug '{slug}' does not exist.",
            instance=f'{request.url.path}'
        )

        return JSONResponse(
            status_code=problem.status,
            content=problem.dict(),
            media_type='application/problem+json'
        )


# UPDATE files WHERE slug=slug SET ....
# partial update
@router.patch('/{slug}', status_code=200, response_model=FileDetailsOut,
              summary='Updates the file identified by the {slug}. For any parameters not provided in '
                      'request, existing values are retained.')
def partial_update_file(request: Request, slug: str,
                        filename: str = Form(None),
                        max_downloads: int = Form(None),
                        payload: UploadFile = File(None),
                        session: Session = Depends(get_session),
                        settings: Settings = Depends(get_settings)
                        ):
    try:
        # select file with given slug
        statement = select(FileDetails).where(FileDetails.slug == slug)
        file = session.exec(statement).one()

        # update filename
        if filename is not None:
            file.filename = filename

        # update max_downloads
        if max_downloads is not None:
            file.max_downloads = max_downloads

        # update payload
        if payload is not None:
            # create path for file to save
            path = settings.storage / file.slug

            # save file
            with open(path, 'wb') as dest:
                shutil.copyfileobj(payload.file, dest)

            # update file fields
            file.size = path.stat().st_size
            file.mime_type = mimetypes.guess_type(payload.filename)[0]

        # update always
        file.updated_at = datetime.now()

        # update db
        session.add(file)
        session.commit()
        session.refresh(file)

        return file
    except NoResultFound as ex:
        problem = ProblemDetails(
            status=404,
            title='File not found',
            detail=f"File with slug '{slug}' does not exist.",
            instance=f'{request.url.path}'
        )

        return JSONResponse(
            status_code=problem.status,
            content=problem.dict(),
            media_type='application/problem+json'
        )


# INSERT INTO files VALUES(...)
@router.post('/', status_code=201, response_model=FileDetailsOut,
             summary='Uploads a file and creates file details.')
def create_file(max_downloads: int | None = Form(None),
                payload: UploadFile = File(...),
                session: Session = Depends(get_session),
                settings: Settings = Depends(get_settings)):
    # create file object
    file = FileDetails(
        max_downloads=max_downloads,
        filename=payload.filename,
        mime_type=mimetypes.guess_type(payload.filename)[0],  # payload.content_type
        size=-1
    )

    # create path for file to save
    path = settings.storage / file.slug

    # save file
    with open(path, 'wb') as dest:
        shutil.copyfileobj(payload.file, dest)

    # get file size
    file.size = path.stat().st_size

    # save to db
    session.add(file)
    session.commit()
    session.refresh(file)

    return file
