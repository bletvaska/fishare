from datetime import datetime
from functools import wraps
import mimetypes
from pathlib import Path
import shutil

import fastapi
from fastapi import Depends, Form, Request, UploadFile
from loguru import logger
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound

from fishare.core import ProblemDetailsResponse
from fishare.dependencies import get_session, get_settings
from fishare.models.file_details import FileDetails
from fishare.models.file_details_out import FileDetailsOut
from fishare.models.pager import Pager
from fishare.models.problem_details import ProblemDetails
from fishare.models.settings import Settings

PATH_PREFIX = "/api/v1/files"

router = fastapi.APIRouter()


def log_client_ip(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = kwargs["request"]
        logger.info(f"Incomming connection from {request.client.host}")
        return func(*args, **kwargs)

    return wrapper



@log_client_ip
@router.get("", response_model=Pager)
def get_list_of_files(
    request: Request,
    page: int = 1,
    size: int = 10,
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
):
    url = f"{settings.base_url}{PATH_PREFIX}"
    pager = Pager()

    # count nr of records/files
    pager.count = (
        session.query(FileDetails)
        .where(FileDetails.downloads < FileDetails.max_downloads)
        .where(datetime.now() < FileDetails.expires)
        .count()
    )

    # select results from db
    # SELECT * FROM filedetails
    # WHERE downloads < max_downloads
    # AND now() < expires
    # LIMIT ({page} - 1) * {size}, {size}
    statement = (
        select(FileDetails)
        .where(FileDetails.downloads < FileDetails.max_downloads)
        .where(datetime.now() < FileDetails.expires)
        .offset((page - 1) * size)
        .limit(size)
    )

    pager.results = session.exec(statement).all()

    # create links for first and last page
    pager.first = f"{url}?size={size}"
    pager.last = f"{url}?size={size}&page={pager.count // size + 1}"

    # next page
    if page + 1 <= pager.count // size + 1:
        pager.next = f"{url}?size={size}&page={page + 1}"

    # previous page
    if page - 1 > 0:
        pager.previous = f"{url}?size={size}&page={page - 1}"

    return pager


@log_client_ip
@router.get("/{slug}", response_model=FileDetailsOut)
def get_file_detail(slug: str, session: Session = Depends(get_session)):
    # SELECT * FROM files WHERE slug=slug AND downloads < max_downloads AND now() < expires;
    statement = (
        select(FileDetails)
        .where(FileDetails.slug == slug)
        .where(FileDetails.downloads < FileDetails.max_downloads)
        .where(datetime.now() < FileDetails.expires)
    )

    # get file
    file = session.exec(statement).one_or_none()

    # if not found, then 404
    if file is None:
        problem = ProblemDetails(
            title="File not found",
            detail=f"File with slug '{slug}' was not found.",
            instance="/files/",
            status=404,
        )

        return ProblemDetailsResponse(
            status_code=problem.status, content=problem.dict()
        )

    # return file
    return file


@router.delete("/{slug}", status_code=204)
def delete_file(
    slug: str,
    session: Session = Depends(get_session),
    settings: Settings = Depends(get_settings),
):
    try:
        # prepare statement
        # f'SELECT * FROM files WHERE slug={slug} AND downloads < max_downloads AND now() < expires';
        statement = (
            select(FileDetails)
            .where(FileDetails.slug == slug)
            .where(FileDetails.downloads < FileDetails.max_downloads)
            .where(datetime.now() < FileDetails.expires)
        )

        # exec
        file = session.exec(statement).one()

        # delete from storage
        path = settings.storage / file.slug
        path.unlink(missing_ok=True)  # FIXME maybe need some rework. maybe not.

        # delete file object
        session.delete(file)
        session.commit()

    except NoResultFound as ex:
        problem = ProblemDetails(
            title="File not found",
            detail=f"File with slug '{slug}' was not found.",
            instance=f"/files/{slug}",
            status=404,
        )

        return ProblemDetailsResponse(
            status_code=problem.status, content=problem.dict()
        )


@router.put("/{slug}", status_code=200, response_model=FileDetailsOut)
def full_file_update(
    slug: str,
    payload: UploadFile = fastapi.File(...),
    max_downloads: int = Form(),
    settings: Settings = Depends(get_settings),
    session: Session = Depends(get_session),
):

    try:
        # select given file
        # f'SELECT * FROM files WHERE slug={slug} AND downloads < max_downloads AND now() < expires';
        statement = (
            select(FileDetails)
            .where(FileDetails.slug == slug)
            .where(FileDetails.downloads < FileDetails.max_downloads)
            .where(datetime.now() < FileDetails.expires)
        )

        file = session.exec(statement).one()

        # overwrite file with uploaded one
        path = settings.storage / file.slug
        with open(path, "wb") as dest:
            shutil.copyfileobj(payload.file, dest)

        # update file fields
        file.filename = payload.filename
        file.size = path.stat().st_size
        file.max_downloads = max_downloads
        file.mime_type = mimetypes.guess_type(file.filename)[0]
        file.updated_at = datetime.now()
        # file.mime_type=payload.content_type

        # update in db
        session.add(file)
        session.commit()
        session.refresh(file)

        # return
        return file

    except NoResultFound as ex:
        problem = ProblemDetails(
            title="File not found",
            detail=f"File with slug '{slug}' was not found.",
            instance=f"/files/{slug}",
            status=404,
        )

        return ProblemDetailsResponse(
            status_code=problem.status, content=problem.dict()
        )


@router.patch("/{slug}", status_code=200, response_model=FileDetailsOut)
def partial_file_update(
    slug: str,
    payload: UploadFile = fastapi.File(None),
    max_downloads: int = Form(None),
    filename: str = Form(None),
    settings: Settings = Depends(get_settings),
    session: Session = Depends(get_session),
):

    try:
        # select given file
        # f'SELECT * FROM files WHERE slug={slug} AND downloads < max_downloads AND now() < expires';
        statement = (
            select(FileDetails)
            .where(FileDetails.slug == slug)
            .where(FileDetails.downloads < FileDetails.max_downloads)
            .where(datetime.now() < FileDetails.expires)
        )

        file = session.exec(statement).one()

        # overwrite file with uploaded one
        if payload is not None:
            path = settings.storage / file.slug
            with open(path, "wb") as dest:
                shutil.copyfileobj(payload.file, dest)

            file.filename = payload.filename
            file.size = path.stat().st_size
            file.mime_type = payload.content_type

        # update file fields
        if max_downloads is not None:
            file.max_downloads = max_downloads

        if filename is not None:
            file.filename = filename
            file.mime_type = mimetypes.guess_type(file.filename)[0]

        # update timestamp
        file.updated_at = datetime.now()

        # update in db
        session.add(file)
        session.commit()
        session.refresh(file)

        # return
        return file

    except NoResultFound as ex:
        problem = ProblemDetails(
            title="File not found",
            detail=f"File with slug '{slug}' was not found.",
            instance=f"/files/{slug}",
            status=404,
        )

        return ProblemDetailsResponse(
            status_code=problem.status, content=problem.dict()
        )


# curl \
#   -F "max_downloads=10" \
#   -F "payload=@/etc/passwd" \
#   http://localhost:9000/api/v1/files/

# http -f post http://localhost:9000/api/v1/files/ max_downloads=10 payload@README.md


@router.post("/", status_code=201, response_model=FileDetailsOut)
def create_file(
    payload: UploadFile = fastapi.File(...),
    max_downloads: int = Form(None),
    settings: Settings = Depends(get_settings),
    session: Session = Depends(get_session),
):
    # create file object
    file = FileDetails(
        filename=payload.filename,
        size=-1,
        mime_type=payload.content_type,
        max_downloads=1 if max_downloads is None else max_downloads,
    )

    # save payload to file
    path = settings.storage / file.slug

    with open(path, "wb") as dest:
        shutil.copyfileobj(payload.file, dest)

    # get file size
    file.size = path.stat().st_size

    # insert to db
    session.add(file)
    session.commit()
    session.refresh(file)

    # return FileDetailsOut(**file.dict())
    return file
