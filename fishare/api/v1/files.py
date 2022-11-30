from fastapi import Depends, Form, UploadFile
import fastapi
from sqlmodel import Session, create_engine
from fishare.dependencies import get_settings

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

@router.post("/", status_code=201)
def create_file(payload: UploadFile = fastapi.File(...),
                max_downloads: int = Form(None),
                settings: Settings = Depends(get_settings)):
    file = File(
        filename=payload.filename,
        size=-1,
        mime_type=payload.content_type,
        max_downloads=1 if max_downloads is None else max_downloads
    )

    engine = create_engine(settings.db_uri)

    with Session(engine) as session:
        session.add(file)
        session.commit()
        session.refresh(file)

    return file
