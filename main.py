import random

from models import User, Tournament, Match
import client
import uuid

seed = uuid.uuid4()
teams = []
tournaments = []

# user = User(username=f'user-{random.randint(1,1222222)}', password='pass', roles=['USER', 'MODERATOR', 'JUDGE'])
# client.register(user)
# client.login(user)
# user = client.user_info()

moderator = client.register(User(username=f'user-{random.randint(1,1222222)}', password='pass', roles=['USER', 'MODERATOR']))

judges = list(map(
    lambda i: client.register(User(username=f'user-{random.randint(1,1222222)}', password='pass', roles=['USER', 'JUDGE'])),
    range(5)
))


# генерирует 5 случайных турниров, все их отыгрывает, сбрасывает несколько случ. матчей и всё

def play_full_tournament(tournament: Tournament):
    q = []
    finished = []
    next_match = {}
    prev_match = {}
    for match in tournament.matches:
        if match.nextMatchId:
            next_match[match.id] = match.nextMatchId
            if match.nextMatchId not in prev_match:
                prev_match[match.nextMatchId] = []
            prev_match[match.nextMatchId].append(match.id)
    for match in tournament.matches:
        if match.id not in prev_match:
            q.append(match.id)
    while len(q) > 0:
        tournament = client.refresh_tournament(tournament)
        matches = {}
        for match in tournament.matches:
            matches[match.id] = match
        match_id = q.pop(0)
        match = matches[match_id]
        if match_id in next_match:
            q.append(next_match[match_id])
        if match.team2Id is None or match.team2Id is None or match.id in finished:
            continue
        for i in range(tournament.maxGames):
            game = client.play_game(match, random.choice([match.team1Id, match.team2Id]))
            for judge in judges:
                client.login(judge)
                client.approve(game)
            finished.append(match.id)
            client.login(moderator)


def do_all_job():
    client.login(moderator)
    # Teams
    for i in range(8):
        team = client.create_team(f'team{i}-{seed}')
        teams.append(team)
        print(team)

    # Tournaments
    for i in range(3):
        random.shuffle(teams)
        tournament = Tournament(
            name=f'tournament{i}-{seed}',
            startDate='2022-10-10',
            approvalRatio=0.6,
            maxGames=3,
            judges=judges,
            teams=teams[:5],
        )
        tournament = client.create_tournament(tournament)
        tournaments.append(tournament)
        print(tournament)
        play_full_tournament(tournament)


do_all_job()








