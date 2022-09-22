import fastapi
from fastapi import Depends
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from fishare.helpers import get_jinja

router = fastapi.APIRouter()


@router.get('/')
def homepage(request: Request,
             jinja: Jinja2Templates = Depends(get_jinja)):
    data = {
        'request': request,
        'title': 'fishare - File Sharing for Free'
    }

    return jinja.TemplateResponse('home.html', data)
