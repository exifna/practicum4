import time
from faker import Faker
from typing import List, Optional
from threading import Thread




class Player:
    def __init__(self, nickname: str):
        self.balance = 10_000
        self.workshops = 2
        self.material = 4
        self.flighters = 2
        self.live = True
        self.nickname = nickname
        self.token = Faker().md5()[:8]

    def collector(self):
        self.balance -= 300  * self.material
        self.balance -= 500  * self.flighters
        self.balance -= 1000 * self.workshops
        if self.balance <= 0:
            self.live = False


class GameTypes:
    month = 0
    winner = 1

class Game:

    def __init__(self, creator: Player, game_type : GameTypes = GameTypes.month):

        self.game_id: str = Faker().md5()
        self.players: List[Player] = [creator]
        self.start = False
        self.level = 2
        self.month = 1
        self.game_type = game_type
        self.last_step_time = time.time()
        self.nowPlayer: Optional[Player] = None

    def add_player(self, player: Player):
        self.players.append(player)

    def get_event(self, token: str) -> str:
        player = None

        for _player in self.players:
            if _player.token == token:
                player = _player

        if not player:
            return 'error: player not found'

        if not self.start:
            return 'start'

        if self.nowPlayer and self.nowPlayer.token == token:
            return 'go'

        return 'wait'

    def run(self):
        thread = Thread(
            target=self._run
        ).start()

    def _run(self):
        self.start = True

        while True:
            for player in self.players:
                self.nowPlayer = player
                self.last_step_time = time.time()

                while time.time() - self.last_step_time < 5:
                    time.sleep(0.01)

            self.nowPlayer = None
            self.month += 1




