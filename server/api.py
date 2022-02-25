import time

from flask import Flask, jsonify, request
from typing import List, Dict
from server.types import Game, Player

app = Flask(__name__)
games: Dict[str, Game] = dict()



@app.post('/create_game')
def create_game():
    global games

    json_data = request.get_json()
    creator_nick = json_data['nick']
    creator = Player(creator_nick)
    game = Game(creator)
    games[game.game_id] = game

    return jsonify({
        'game_id' : game.game_id,
        'token'   : creator.token
    })

@app.get('/start_game')
def start_game():
    global games

    headers = request.headers
    game_id = headers.get('Game-Id')
    token = headers.get('Token')
    if game_id not in games:
        return jsonify(success = False)

    game = games[game_id]
    if game.players[0].token == token:
        game.run()
        return jsonify(success = True)

    return jsonify(success = False)

@app.post('/invite')
def connect_to_game():
    global games

    json_data = request.get_json()
    nick = json_data['nick']
    game_id = json_data['game_id']

    if game_id not in games:
        return jsonify(success = False)

    player = Player(nick)
    games[game_id].add_player(player)
    return jsonify({
        'success' : True,
        'token'   : player.token,
        'creator' : games[game_id].players[0].nickname
    })


@app.get('/get_event')
def get_player_event():
    global games

    headers = request.headers
    game_id = headers.get('Game-Id')
    token = headers.get('Token')
    if game_id not in games:
        return jsonify(success = False)

    game = games[game_id]
    player = game.check_player(token)
    if not player:
        return jsonify(success = False)

    if len(game.players) == 1:
        return jsonify({'success' : True, 'text' : 'win'})


    if not player.live:
        return jsonify({'success' : True, 'text' : 'dead'})

    return jsonify(success = True,
                   text = game.get_event(token),
                   level = game.level,
                   month = game.month,
                   balance = player.balance,
                   workshops = player.workshops,
                   material  = player.material,
                   flighters = player.flighters,
                   time =game.last_step_time,
                   data = game.get_prices().__dict__()
                   )

@app.post('/step')
def step():
    global games

    headers = request.headers
    game_id = headers.get('Game-Id')
    token = headers.get('Token')
    if game_id not in games:
        return jsonify(success = False)

    game = games[game_id]
    player = game.check_player(token)
    if not player:
        return jsonify(success = False)

    data = request.get_json()
    step = data['step']

    if game.nowPlayer.token == token:
        game.skip = True

        if data == '1':
            game.create_flighter(token)
            return

        if data.split()[0] == '2':
            game.buy_flighter(game.check_player(token), data)
            return

        if data == '3':
            return

        if data.split()[0] == '4':
            return


        return {'success' : True}

    return {'success' : False}

app.run('0.0.0.0', 12001)
