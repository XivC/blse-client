from dataclasses import asdict

import requests
from requests import Response
from requests.auth import HTTPBasicAuth

from models import User
from utlis import url

session = requests.session()
session.headers['Content-type'] = 'application/json'
auth = None


def login(user: User):
    global auth
    auth = HTTPBasicAuth(username=user.username, password=user.password)
    session.auth = auth


def register(user: User) -> Response:
    response = session.post(url('/auth/register/'), json=asdict(user))
    if response.status_code != 200:
        print(f'Register error: {response.text}')
    return response
