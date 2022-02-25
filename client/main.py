import time
import traceback
from time import sleep
from inputimeout import inputimeout, TimeoutOccurred
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
        exit('Критическая ошибка (session.start_state() return False)...')

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

while True:
    data = session.get_event()
    success = data['success']
    if not success:
        exit(f'Ошибка (game server return: {data}) - скорее всего вы умерли')
        continue

    if data['text'] == 'dead':
        exit('You умерли')

    if data['text'] == 'win':
        exit('You выиграли')

    balance = data['balance']
    flighters = data['flighters']
    level = data['level']
    material = data['material']
    month = data['month']
    workshops = data['workshops']
    _time = data['time'] + 30 - time.time() - 0.5
    _data = data['data']

    _banner = banner + '\n\n' \
                      f'> Твой баланс: {balance}\n' \
                      f'> Твоих истребителей : {flighters}\n' \
                      f'> Сырья у тебя: {material}\n' \
                      f'> Цехов: {workshops}\n' \
                      f'> Месяц: {month}\n' \
                      f'> Текущий уровень: {level}\n\n' \
                      f'> Максимальная цена за истрибитель - {_data["flighter_max"]}\n' \
                      f'> Кол-во сырья для покупки: {_data["material_count"]}\n' \
                      f'> Кол-во истребителей для покупки: {_data["flighter_demand"]}'


    clear()
    print(_banner)

    if data['text'] == 'go':
        try:

            something = inputimeout(prompt=f'> У тебя есть примерно 30 секунд на ход!\n'
                  f': {"❌ " if balance < 2000 else ""}Введи 1 если хочешь создать новый истребитель (стоимость - 2.000, у тебя {balance})\n'
                  f': Введи 2 <цена> если хочешь продать самолет (курс смотри выше, самолетов у тебя: {flighters}, максимальную и минимальную цену на самолет смотри выше)\n'
                  f': {"❌ " if balance < 5000 else ""}Введи 3 если хочешь построить новых цех (заёмет 4 месяца, стоимость - 5.000)\n'
                  f': Введи 4 <цена> <кол-во> если хочешь купить сырье (минимальная и максимальная цена - смотри выше)\n> ', timeout=_time)

            session.step(something)

        except:
            something = ''