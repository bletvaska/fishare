import fastapi

router = fastapi.APIRouter()


@router.get('/')
def homepage():
    pass
