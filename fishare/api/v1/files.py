import fastapi

PATH_PREFIX = '/api/v1/files'

router = fastapi.APIRouter()

files = ["main.py", "obrazok.jpg", "batman.avi", "superman.asf"]


@router.get("/")
def get_list_of_files():
    return files


@router.get("/{slug}")
def get_file_detail(slug: int):
    return files[slug - 1]
