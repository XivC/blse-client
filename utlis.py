
api_url = 'http://localhost:1453/api'


def url(method: str):
    return f'{api_url}/{method}'


def authenticated(f):
    resp = f()
    if resp.status_code == 401:
        raise RuntimeError('Authentication failed')

