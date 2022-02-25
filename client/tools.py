import random
import requests
from pick import pick
import os

class GameSession:
    def __init__(self, nickname: str):
        self.nickname: str = nickname or f'Player #{random.randint(0, 100)}'

        self.session: requests.session = requests.session()
        self.baseUrl: str = 'http://localhost:12001'
        self.game_creator: str = ''

    def create_game(self) -> str:
        url = self.baseUrl + '/create_game'
        data = {
            'nick' : self.nickname
        }

        response = self.session.post(url, json=data)
        game_id = response.json()['game_id']
        token   = response.json()['token']
        self.session.headers = {
            'game_id' : game_id,
            'token' : token
        }
        return game_id

    def get_event(self) -> str:
        url = self.baseUrl + '/get_event'

        r = self.session.get(url)
        return r.json()

    def start_game(self) -> bool:
        url = self.baseUrl + '/start_game'

        return self.session.get(url).json()['success']

    def connect_to_game(self, game_id: str) -> bool:
        url = self.baseUrl + '/invite'

        data = {
            'nick' : self.nickname,
            'game_id' : game_id
        }

        response = self.session.post(url, json=data)
        response_data = response.json()

        success = response_data['success']
        if not success:
            return success

        token = response_data['token']

        self.session.headers = {
            'game_id' : game_id,
            'token'  : token
        }
        self.game_creator = response_data['creator']
        return True

    def step(self, string: str):

        data = {
            'step' : string
        }

        print(self.session.post(self.baseUrl + '/step', data).text)




def choose_action() -> int:

    title = f'{banner}\nPlease choose your action'
    options = ['Create a new game',
               'Connect to an exist game']

    option, index = pick(options, title, indicator='=>')
    return index

banner = """
  ________                       
 /  _____/_____    _____   ____  
/   \\  ___\\__  \\  /     \\_/ __ \\ 
\\    \\_\\  \\/ __ \\|  Y Y  \\  ___/ 
 \______  (____  /__|_|  /\___  >
        \\/     \\/      \\/     \\/    By Exifna...
 """

def print_banner():
    clear()
    print(banner)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
