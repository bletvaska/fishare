import fastapi
from fastapi import Request
# from fastapi.templating import Jinja2Templates

router = fastapi.APIRouter()
# templates = Jinja2Templates(directory='fishare/templates/')

@router.get('/{slug}')
def download_file(request: Request, slug: str):
    return "hello world"
