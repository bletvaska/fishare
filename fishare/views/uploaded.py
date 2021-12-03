import fastapi
from fastapi import Request
from fastapi.templating import Jinja2Templates

router = fastapi.APIRouter()
templates = Jinja2Templates(directory='fishare/templates/')


@router.get('/uploaded/')
def uploaded_file(request: Request, slug: str):
    return templates.TemplateResponse('uploaded.html', {
        'request': request, 'title': 'fishare Service', 'slug': slug
    })
