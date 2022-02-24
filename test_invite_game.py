import time

from client.tools import GameSession

session = GameSession('Bot')


session.connect_to_game(
    game_id=input('game_id: ')
)

while True:
    print(session.get_event())
    time.sleep(1)


