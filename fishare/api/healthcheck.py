import fastapi


router = fastapi.APIRouter()


@router.get("/healthz")
def healthcheck():
    pass
