from time import sleep

from client.tools import GameSession

session = GameSession()

print(session.create_game('Alex'))
print(session.get_event())
input('Press <enter> to start game...')
print(session.start_game())
while True:
    print(session.get_event())
    sleep(1)

