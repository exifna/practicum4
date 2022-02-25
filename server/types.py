import random
import time
from operator import itemgetter

from faker import Faker
from typing import List, Optional, Dict
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
        self.run()

    def collector(self):
        self.balance -= 300  * self.material
        self.balance -= 500  * self.flighters
        self.balance -= 1000 * self.workshops
        if self.balance <= 0:
            self.live = False

    def _run(self):
        while self.live:
            if self.balance <= 0:
                self.live = False
            time.sleep(0.1)

    def run(self):
        Thread(target=self._run).start()


class Price:
    def __init__(self, material_min: int, flighter_max: int, flighter_demand: int,
                 material_count: int):

        self.material_min = material_min        # Min material price
        self.flighter_max = flighter_max        # Max flighter price
        self.flighter_demand = flighter_demand  # Demand flighter ??
        self.material_count = material_count    # Material count -_-


    def __dict__(self):
        return {
            'material_min' : self.material_min,
            'flighter_max' : self.flighter_max,
            'flighter_demand' : self.flighter_demand,
            'material_count' : self.material_count
        }


class GameTypes:
    month = 0
    winner = 1

class Game:

    def __init__(self, creator: Player, game_type : GameTypes = GameTypes.month):

        self.game_id: str = Faker().md5()
        self.players: List[Player] = [creator]
        self.game_type = game_type
        self.last_step_time = time.time()
        self.nowPlayer: Optional[Player] = None

        self.start = False
        self.level = 2
        self.month = 1
        self.material_count = self.get_prices().material_count
        self.material_players: List[Dict[str, object]] = list()  # список людей, запросивших сырье
        self.skip = False
        self.create_flighters = list()
        self.buy_flighters = list()
        self.workshops = list() # [{token: token, month: month}]

    def add_player(self, player: Player) -> None:
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

    def get_prices(self) -> Price:
        if self.level == 1:
            return Price(
                material_min= 800,
                flighter_max= 6_500,
                material_count= int(len(self.players) * 1.0),
                flighter_demand= int(len(self.players) * 3.0)
            )

        if self.level == 2:
            return Price(
                material_min= 650,
                flighter_max= 6_000,
                material_count= int(len(self.players) * 1.5),
                flighter_demand= int(len(self.players) * 2.5)
            )

        if self.level == 3:
            return Price(
                material_min= 500,
                flighter_max= 5_500,
                material_count= int(len(self.players) * 2.0),
                flighter_demand= int(len(self.players) * 2.0)
            )

        if self.level == 4:
            return Price(
                material_min= 400,
                flighter_max= 5_000,
                material_count= int(len(self.players) * 2.5),
                flighter_demand= int(len(self.players) * 1.5)
            )


        if self.level == 5:
            return Price(
                material_min= 300,
                flighter_max= 4_500,
                material_count= int(len(self.players) * 3.0),
                flighter_demand= int(len(self.players) * 1.0)
            )

    def create_flighter(self, token : str):
        player = self.check_player(token)
        if player.balance < 2000:
            return

        player.balance -= 2000
        self.create_flighters.append(player)

    def buy_flighter(self, player: Player, step: str):
        if len(step.split()) != 2:
                return

        price = step.split()[1]
        try:
            price = int(price)
        except:
            return

        if price >= self.get_prices().flighter_max:
            return

        self.buy_flighters.append([player, price])

    def new_workshop(self, player: Player):
        if player.balance < 2500:
            return

        player.balance -= 2500
        self.workshops.append({'token' : player.token, 'month' : self.month + 4})

    def buy_material(self, player: Player, count: int, price: int) -> bool:
        min_material_price = self.get_prices().material_min
        if price < min_material_price:
            return False

        self.material_players.append({'player' : Player })


    def check_player(self, token: str) -> Optional[Player]:
        for player in self.players:
            if player.token == token:
                return player

        return None

    def next_level(self):
        d1 = [1/3, 1/3, 1/6, 1/12, 1/12]
        d2 = [1/4, 1/3, 1/4, 1/12, 1/12]
        d3 = [1/12, 1/4, 1/3, 1/4, 1/12]
        d4 = [1/12, 1/12, 1/3, 1/3, 1/4]
        d5 = [1/12, 1/12, 1/6, 1/3, 1/3]

        levels = [1,2,3,4,5]
        if self.level == 1:
            self.level = random.choices(levels, d1)
            return

        if self.level == 2:
            self.level = random.choices(levels, d2)
            return
        if self.level == 3:
            self.level = random.choices(levels, d3)
            return
        if self.level == 4:
            self.level = random.choices(levels, d4)
            return
        if self.level == 5:
            self.level = random.choices(levels, d5)
            return

    def run(self) -> None:
        Thread(
            target=self._run
        ).start()

    def _run(self) -> None:
        self.start = True

        while True:
            for player in self.players:   # Wait player step
                self.nowPlayer = player
                self.last_step_time = time.time()

                while time.time() - self.last_step_time < 30:
                    if self.skip:
                        self.skip = False
                        break

                    time.sleep(0.01)



            self.nowPlayer = None

            for player in self.players:  # Collect balance
                player.collector()

            temp_players = list()
            for player in self.players:
                if player.live:
                    temp_players.append(player)

            for player in self.players:
                if player.token in [x.token for x in temp_players]:
                    break
                if player.token in [x['token'] for x in self.workshops]:
                    ws = list()
                    for w in self.workshops:
                        if w['token'] != player.token:
                            ws.append(w)

                    self.workshops = ws

                if player in self.create_flighters:
                    tmp = self.create_flighters
                    for pl in self.create_flighters:
                        if pl.token != player.token:
                            tmp.append(pl)

                    self.create_flighters = pl

            self.players = temp_players

            self.material_count = self.get_prices().material_count
            self.month += 1

            for player in self.create_flighters:
                player.flighters += 1

            tmp = self.get_prices().flighter_max
            for player, price in list(sorted(self.buy_flighters, key=itemgetter(1))):
                if tmp <= 0:
                    break

                player: Player = player
                player.flighters += 1

            for player, month in self.workshops:
                if month == self.month:
                    try:
                        if player.balance >= 2500:
                            player.balance -= 2500
                            player.workshops += 1

                    except:
                        pass



            self.next_level()







