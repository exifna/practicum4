import time

from client.tools import GameSession

session = GameSession()


session.connect_to_game(
    nick= 'admin',
    game_id=input('game_id: ')
)

while True:
    print(session.get_event())
    time.sleep(1)


