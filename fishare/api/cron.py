import fastapi
from fastapi import Depends
from sqlmodel import Session

from fishare.database import get_session

router = fastapi.APIRouter()


@router.get("/", summary="Get list of files.")
def run_cron_job(session: Session = Depends(get_session)):
    pass
