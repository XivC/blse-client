import random

from models import User, Tournament
import client

user = User(username='user', password='pass')

try:
    client.register(user)
except client.RequestError:
    pass

client.login(user)

judges = client.get_judges()
teams = []
for i in range(10):
    team = client.create_team(f't{i}-{random.randint(1,10000)}')
    teams.append(team)

tournament = Tournament(
    name='t143r',
    startDate='2023-01-01',
    approvalRatio=0.6,
    maxGames=3,
    judges=judges,
    teams=teams,
)

tournament = client.create_tournament(tournament)

print(tournament)





