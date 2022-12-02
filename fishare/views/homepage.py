import fastapi


router = fastapi.APIRouter()

@router.get('/')
def homepage():
    return 'welcome to my homepage'
