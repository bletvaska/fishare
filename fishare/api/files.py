import fastapi

router = fastapi.APIRouter()


# SELECT * FROM files
@router.get('/api/v1/files/', summary='Get list of files.')
def get_list_of_files():
    return [
        'file1',
        'file2',
        'file3'
    ]


# SELECT * FROM files WHERE slug=slug
@router.get('/{slug}', summary='Get file details identified by the {slug}.')
def get_file_detail(slug: str):
    """
    Returns file details.
    """
    return {
        'filename': 'file4',
        'slug': slug
    }


# DELETE FROM files WHERE slug=slug
@router.delete('/{slug}', summary='Delete the file identified by the {slug}.')
def delete_file(slug: str):
    return f'deleted file {slug}'


# UPDATE files WHERE slug=slug SET ....
# full update
@router.put('/{slug}', summary='Updates the file identified by the {slug}. Any parameters not provided are reset to '
                               'their defaults.')
def full_update_file(slug: str):
    return f'full update for file {slug}'


# UPDATE files WHERE slug=slug SET ....
# partial update
@router.patch('/{slug}', summary='Updates the file identified by the {slug}. For any parameters not provided in '
                                 'request, existing values are retained.')
def partial_update_file(slug: str):
    return f'partial update for file {slug}'


# INSERT INTO files VALUES(...)
@router.post('/', summary='Uploads a file and creates file details.')
def create_file():
    return 'file was created'
