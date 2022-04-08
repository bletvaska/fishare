import fastapi
from fastapi import Depends
from sqlmodel import Session

from fishare.database import get_session

router = fastapi.APIRouter()


@router.get("/", summary="Run background jobs.")
def run_cron_job(session: Session = Depends(get_session)):
    return 'running cron jobs.'
