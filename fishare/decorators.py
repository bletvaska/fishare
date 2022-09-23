from functools import wraps


def log_client_ip(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):  # request=None,
        request = kwargs['request']
        print(f'>> Opened conection from {request.client.host}')
        response = await func(*args, **kwargs)
        print(f'>> Closing conection from {request.client.host}')
        return response

    return wrapper