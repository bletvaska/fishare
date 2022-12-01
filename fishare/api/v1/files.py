from datetime import datetime
import shutil
import fastapi
from fastapi import Depends, Form, UploadFile
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from fishare.dependencies import get_session, get_settings

from fishare.models.file_details import FileDetails
from fishare.models.file_details_out import FileDetailsOut
from fishare.models.settings import Settings

PATH_PREFIX = "/api/v1/files"

router = fastapi.APIRouter()


@router.get("/")
def get_list_of_files(session: Session = Depends(get_session)):
    statement = select(FileDetails)
    files = session.exec(statement).all()
    result = []
    for file in files:
        result.append(FileDetailsOut(**file.dict()))
    return result


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

    # handle result
    if file is None:
        return JSONResponse(
            status_code=404,
            content={"message": "Ta som nenasiel take, co si kcel."}
            )

    return file


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
