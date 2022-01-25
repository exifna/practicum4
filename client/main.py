from time import sleep
try:
    from client.tools import *
except:
    from tools import *

print_banner()
nickname = input(f'Enter your nickname: ')
clear()
session = GameSession(nickname)
action = choose_action()

if not action:   # If action is 0 (create game)
    game_id = session.create_game()
    print_banner()
    print(f'> Game id for connect: {game_id}')
    input('> Press <enter> for start game... ')
    start_state = session.start_game()
    if not start_state:
        exit('Critical error while start game (session.start_state() return False)...')

    print_banner()
    print(f'> Game started...')

elif action == 1:
    print_banner()
    game_id = input('> Enter game id: ')
    connect_state = session.connect_to_game(game_id)
    if not connect_state:
        exit(f'Game not found!')

    print_banner()
    print(f'> Success connect to game (creator: {session.game_creator})')

