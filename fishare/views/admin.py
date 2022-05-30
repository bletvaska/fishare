from fastapi import Request, APIRouter, Depends
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from fishare.database import get_session
from fishare.models.file import File
from fishare.models.settings import get_settings

router = APIRouter()
templates = Jinja2Templates(directory='fishare/templates/')


@router.get('/admin/')
def list_of_files(request: Request, session: Session = Depends(get_session)):
    # get list of all files
    statement = select(File)
    files = session.exec(statement).all()

    # prepare template data
    data = {
        'request': request,
        'title': 'fishare Admin',
        'files': files,
        'base_url': get_settings().base_url
    }

    # render
    return templates.TemplateResponse('admin.html', data)
