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

    return jsonify(success = True,
                   text = game.get_event(token),
                   level = game.level,
                   month = game.month,
                   balance = player.balance,
                   workshops = player.workshops,
                   material  = player.material,
                   flighters = player.flighters
                   )



app.run('0.0.0.0', 12001)
