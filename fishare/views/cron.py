import fastapi
from fastapi import Request

router = fastapi.APIRouter()

@router.get('/cron')
def run_cron():
    return "cron update"
