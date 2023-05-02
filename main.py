from models import User
import client

user = User(username='user', password='pass', roles=['USER', 'MODERATOR', 'JUDGE'])

client.register(user)
client.login(user)







