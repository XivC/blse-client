from models import User, Tournament
import client

user = User(username='user', password='pass')

try:
    client.register(user)
except client.RequestError:
    pass

client.login(user)

print(client.get_judges())

tournament = Tournament(
    name='t1',
    startDate='2023-01-01',
    approvalRatio=0.6,
    maxGames=3,
    judges=[]

)




