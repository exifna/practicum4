from time import sleep

from client.tools import GameSession

session = GameSession()

session.create_game('Alex')
print(session.get_event())
print(session.start_game())
while True:
    print(session.get_event())
    sleep(1)

