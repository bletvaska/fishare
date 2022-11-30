from fastapi import Form, UploadFile
import fastapi

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
                max_downloads: int = Form(None)):
    print('>> hello')
    pass
