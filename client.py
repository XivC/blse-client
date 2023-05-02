import json

import requests
from requests.auth import HTTPBasicAuth

from models import User, Team, Tournament, Match, Game
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
    data = request('post', 'auth/register/', user.dict(exclude_none=True))
    data['password'] = user.password
    return User.parse_obj(data)


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
    req_data.pop('teams')
    req_data.pop('judges')
    data = request('post', 'moderator/tournaments/', req_data)
    Tournament.update_forward_refs()
    return Tournament.parse_obj(data)


def refresh_tournament(tournament: Tournament) -> Tournament:
    data = request('get', f'user/tournaments/{tournament.id}/')
    Tournament.update_forward_refs()
    return Tournament.parse_obj(data)


def play_game(match: Match, winner_id: int) -> Game:
    data = request('post', f'moderator/matches/{match.id}/play-game/?winnerId={winner_id}')
    return Game.parse_obj(data)


def drop_game(match: Match) -> Tournament:
    data = request('post', f'moderator/matches/{match.id}/drop/')
    Tournament.update_forward_refs()
    return Tournament.parse_obj(data)


def approve(game: Game) -> Game:
    data = request('post', f'judge/games/{game.id}/approve/')
    return Game.parse_obj(data)


def disapprove(game: Game) -> Game:
    data = request('post', f'judge/games/{game.id}/disapprove/')
    return Game.parse_obj(data)


def user_info() -> User:
    data = request('get', f'user/me/')
    return User.parse_obj(data)
