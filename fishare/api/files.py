import fastapi

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
    return {
        'id': 1234,
        'slug': 'abcde',
        'filename': 'filename',
        'link': 'http://fishare.io/slug',
        'downloads': 0,
        'maxDownloads': 1,
        'size': 10000,
        'mimeType': 'text/plain',
        'created': '2021-12-02 08:16:12'
    }


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
