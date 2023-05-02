import json

import requests
from pydantic import BaseModel
from requests import Response
from requests.auth import HTTPBasicAuth

from models import User, Team, Tournament
from utlis import url

session = requests.session()
session.headers['Content-type'] = 'application/json'
auth = None


class RequestError(Exception):
    pass


def request(method: str, path: str, data: dict = None) -> json:
    if data:
        data = json.dumps(data)
    response = session.request(method, url(path), data=data)
    if response.status_code >= 400:
        raise RequestError(response.text)
    return response.json()


def login(user: User):
    global auth
    auth = HTTPBasicAuth(username=user.username, password=user.password)
    session.auth = auth


def register(user: User):
    return request('post', 'auth/register/', user.dict(exclude_none=True))


def create_team(name: str) -> Team:
    data = request('post', f'moderator/teams/?name={name}')
    return Team.parse_obj(data)


def get_judges() -> list[User]:
    data = request('get', f'user/judges/')
    return [User.parse_obj(u) for u in data]


def create_tournament(tournament: Tournament) -> Tournament:
    req_data = tournament.dict(exclude_none=True)
    req_data['teamsIds'] = [t.id for t in tournament.teams]
    req_data['judgesIds'] = [u.id for u in tournament.judges]
    data = request('post', 'moderator/tournaments/', req_data)
    return Tournament.parse_obj(data)
