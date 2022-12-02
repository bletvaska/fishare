import fastapi
from fastapi.templating import Jinja2Templates

from fishare.dependencies import get_templates


router = fastapi.APIRouter()


@router.get("/")
def homepage(request: fastapi.Request, templates: Jinja2Templates = fastapi.Depends(get_templates)):
    data = {
        'request': request,
        'name': 'mikulas',
        'hobbies': ['kreslenie', 'pocitanie', 'programovanie v jazyku Python']
    }
    return templates.TemplateResponse('home.tpl.html', data)
