import fastapi

router = fastapi.APIRouter()


@router.get('/', status_code=200)
def check_health():
    return {
        'status': 'healthy'
    }
