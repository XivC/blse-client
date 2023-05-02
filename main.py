import random

from models import User, Tournament
import client
import uuid

seed = uuid.uuid4()
teams = []
tournaments = []

user = User(username=f'user-{random.randint(1,1222222)}', password='pass', roles=['USER', 'MODERATOR', 'JUDGE'])
client.register(user)
client.login(user)
user = client.user_info()


# генерирует 5 случайных турниров, все их отыгрывает, сбрасывает несколько случ. матчей и всё

def play_full_tournament(tournament: Tournament):
    pass



# Teams
for i in range(8):
    team = client.create_team(f'team{i}-{seed}')
    teams.append(team)
    print(team)

# Tournaments
for i in range(5):
    random.shuffle(teams)
    tournament = Tournament(
        name=f'tournament{i}-{seed}',
        startDate='2022-10-10',
        approvalRatio=0.6,
        maxGames=3,
        judges=[user],
        teams=teams[:5],
    )
    tournament = client.create_tournament(tournament)
    tournaments.append(tournament)
    print(tournament)










