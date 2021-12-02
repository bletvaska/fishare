import fastapi

router = fastapi.APIRouter()

@router.get('/')
def hello():
    return "hello world"