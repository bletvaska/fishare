import fastapi
from fastapi import Depends
from sqlmodel import Session

from fishare.database import get_session

router = fastapi.APIRouter()


@router.get('/{slug}', summary='Download file by {slug}.')
def download_file(slug: str,
                  session: Session = Depends(get_session)):
    return 'downloading file'
