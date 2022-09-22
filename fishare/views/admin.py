import fastapi

router = fastapi.APIRouter()


@router.get('/')
def list_of_files():
    pass
