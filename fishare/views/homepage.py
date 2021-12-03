import fastapi
from fastapi import Request
from fastapi.templating import Jinja2Templates

router = fastapi.APIRouter()
templates = Jinja2Templates(directory='fishare/templates/')

@router.get('/')
def hello(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})
