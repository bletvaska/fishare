import fastapi
from fastapi.templating import Jinja2Templates


router = fastapi.APIRouter()
templates = Jinja2Templates(directory="fishare/templates")


@router.get("/")
def homepage(request: fastapi.Request):
    data = {
        'request': request,
        'name': 'mikulas',
        'hobbies': ['kreslenie', 'pocitanie', 'programovanie v jazyku Python']
    }
    return templates.TemplateResponse('home.tpl.html', data)
