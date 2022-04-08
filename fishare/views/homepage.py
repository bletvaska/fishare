from fastapi.templating import Jinja2Templates
from fastapi import Request, APIRouter

router = APIRouter()
templates = Jinja2Templates(directory='fishare/templates/')


@router.get('/')
def homepage(request: Request):
    data = {
        'request': request,
        'title': 'fishare Service'
    }

    return templates.TemplateResponse('home.html', data)
