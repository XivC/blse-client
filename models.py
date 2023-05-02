from dataclasses import dataclass


@dataclass
class User:
    username: str
    password: str
    roles: list[str]
