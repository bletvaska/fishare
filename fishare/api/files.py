import fastapi
from models.file import File
from models.settings import Settings

router = fastapi.APIRouter()


@router.get('/files/')  # select * from files
def list_of_files():
    return [
        'file1',
        'file2',
        'file3'
    ]


# select * from files where filename={filename}
@router.get('/files/{filename}')
def get_file(filename: str):
    file = File(
        filename='batman.movie.avi',
        size=1234567,
        mime_type='video/mp4'
    )

    data = file.dict()
    data['link'] = file.url()

    return data


@router.delete('/files/{filename}')  # delete from files where filename={filename}
def delete_file(filename: str):
    return "deleted"


@router.put('/files/{filename}')  # update files where filename={filename} set ...  # full update
def full_update_file(filename: str):
    return "full update"


@router.patch('/files/{filename}')  # update files where filename={filename} set ... # partial update
def partial_file_update(filename: str):
    return "partial update"


@router.post('/files/')  # insert into files values ()
def create_file():
    return "file was created"
