import fastapi
from starlette.requests import Request
from starlette.templating import Jinja2Templates

router = fastapi.APIRouter()
templates = Jinja2Templates(directory='fishare/templates/')


@router.get('/')
def homepage(request: Request):
    data = {
        'request': request,
        'title': 'fishare - File Sharing for Free'
    }
    return templates.TemplateResponse('home.html', data)
