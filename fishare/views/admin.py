from fastapi import Request, APIRouter

router = APIRouter()


@router.get('/admin/')
def list_of_files(request: Request):
    return 'hello world'
