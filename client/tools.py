import requests

class GameSession:
    def __init__(self):
        self.nickname: str = str()
        self.session = requests.session()

        self.baseUrl = 'http://localhost:12001'

    def create_game(self, nickname: str):
        url = self.baseUrl + '/create_game'
        data = {
            'nick' : nickname
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

    def start_game(self):
        url = self.baseUrl + '/start_game'

        return self.session.get(url).json()['success']

    def connect_to_game(self, nick: str, game_id: str) -> bool:
        url = self.baseUrl + '/invite'

        data = {
            'nick' : nick,
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

        return True

