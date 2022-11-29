import fastapi


router = fastapi.APIRouter()

files = ["main.py", "obrazok.jpg", "batman.avi", "superman.asf"]


@router.get('/api/v1/files/')
def get_list_of_files():
    return files
