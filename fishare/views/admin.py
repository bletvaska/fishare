from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory='fishare/templates/')


@router.get('/admin/')
def list_of_files(request: Request):
    data = {
        'request': request,
        'title': 'fishare Service'
    }

    return templates.TemplateResponse('admin.html', data)
