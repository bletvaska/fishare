import fastapi
from fastapi import Depends
from sqlmodel import select, Session
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from fishare.dependencies import get_jinja, get_session
from fishare.models.file_details import FileDetails

router = fastapi.APIRouter()


@router.get('/')
def list_of_files(request: Request,
                  jinja: Jinja2Templates = Depends(get_jinja),
                  session: Session = Depends(get_session)):
    # get data
    # SELECT * FROM files
    statement = select(FileDetails)
    files = session.exec(statement).all()

    # prepare data
    data = {
        'request': request,
        'title': 'fishare - List of Files',
        'files': files
    }

    # render
    return jinja.TemplateResponse('admin.html', data)
