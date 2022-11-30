import shutil
from fastapi import Depends, Form, UploadFile
import fastapi
from sqlmodel import Session
from fishare.dependencies import get_session, get_settings

from fishare.models.file import File
from fishare.models.settings import Settings

PATH_PREFIX = "/api/v1/files"

router = fastapi.APIRouter()

files = ["main.py", "obrazok.jpg", "batman.avi", "superman.asf"]


@router.get("/")
def get_list_of_files():
    return files


@router.get("/{slug}")
def get_file_detail(slug: int):
    return files[slug - 1]


# curl \
#   -F "max_downloads=10" \
#   -F "payload=@/etc/passwd" \
#   http://localhost:9000/api/v1/files/

# http -f post http://localhost:9000/api/v1/files/ max_downloads=10 payload@README.md

@router.post("/", status_code=201)
def create_file(payload: UploadFile = fastapi.File(...),
                max_downloads: int = Form(None),
                settings: Settings = Depends(get_settings),
                session: Session = Depends(get_session)):
    # create file object
    file = File(
        filename=payload.filename,
        size=-1,
        mime_type=payload.content_type,
        max_downloads=1 if max_downloads is None else max_downloads
    )

    # save payload to file
    path = settings.storage / file.slug

    with open(path, 'wb') as dest:
        shutil.copyfileobj(payload.file, dest)

    # get file size
    file.size = path.stat().st_size

    # insert to db
    session.add(file)
    session.commit()
    session.refresh(file)

    return file
