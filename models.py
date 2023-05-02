
from pydantic import BaseModel, Field


class User(BaseModel):
    id: int | None
    username: str
    password: str | None
    roles: list[str] | None


class Team(BaseModel):
    id: int | None
    name: str | None


class Tournament(BaseModel):
    id: int | None
    name: str | None
    startDate: str | None
    approvalRatio: float | None
    winner: Team | None
    maxGames: int | None
    judges: list[User] | None
    teams: list[Team] | None
    matches: list['Match'] | None


class Game(BaseModel):
    id: int | None
    winnerId: int | None


class Match(BaseModel):
    id: int | None
    team1: Team | None
    team2: Team | None
    tournament: Tournament | None
    nextMatchId: int | None
    games: list[Game] | None



